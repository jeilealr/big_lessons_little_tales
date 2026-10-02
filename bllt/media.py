"""ffmpeg helpers shared by every tool: locate ffmpeg, probe and decode clips
(`read_frames`, `probe_size`, `probe_duration`, `luma_curve` for flash checks),
and two encoders kept from the LTX-era intro script.

`concat_segments` and `finish` were validated there and have no caller in the
current pipeline; `finish` documents the deliverable audio treatment (PCM
48 kHz in MOV, because Resolve decodes AAC-in-MOV unreliably).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np


def locate_ffmpeg() -> str:
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError(
            "FFmpeg is unavailable: put ffmpeg on PATH or install imageio-ffmpeg"
        ) from error


def concat_segments(segments: list[Path], out_path: Path, fps: int) -> None:
    """Join the segments, dropping each one's first frame after the first.

    Segment N ends on the same reference image segment N+1 starts on, so without
    the trim every seam would hold a duplicated frame.
    """
    ffmpeg = locate_ffmpeg()
    command = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
    for path in segments:
        command += ["-i", str(path)]

    parts = []
    for index in range(len(segments)):
        if index == 0:
            parts.append(f"[{index}:v]setpts=PTS-STARTPTS[v{index}];")
        else:
            parts.append(
                f"[{index}:v]select='gte(n\\,1)',setpts=PTS-STARTPTS[v{index}];"
            )
    labels = "".join(f"[v{i}]" for i in range(len(segments)))
    filtergraph = "".join(parts) + f"{labels}concat=n={len(segments)}:v=1:a=0[out]"

    command += [
        "-filter_complex",
        filtergraph,
        "-map",
        "[out]",
        "-r",
        str(fps),
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "12",
        "-pix_fmt",
        "yuv420p",
        str(out_path),
    ]
    subprocess.run(command, check=True)


def finish(
    concat_video: Path,
    audio_source: Path,
    output: Path,
    target_duration: float,
    source_duration: float,
    final_width: int,
    final_height: int,
    final_fps: int,
    hold_end: float = 0.0,
    audio_restart_at: float | None = None,
) -> None:
    """Retime to the exact target duration, scale, and lay the soundtrack on.

    `hold_end` freezes the last generated frame for that many seconds at the
    end (inside the target duration), so the logo reveal gets a real hold.

    `audio_restart_at` replaces the blind `-stream_loop` with a musical loop:
    the soundtrack plays from 0, is crossfaded back to its start at that
    second, and then plays through to its own ending. Pick it so the track's
    hit lands on the logo reveal and its natural fade-out lands near the end.
    """
    ffmpeg = locate_ffmpeg()
    speed = (target_duration - hold_end) / source_duration
    hold = f",tpad=stop_mode=clone:stop_duration={hold_end:.3f}" if hold_end > 0 else ""
    fade_out_start = max(0.0, target_duration - 0.65)
    output.parent.mkdir(parents=True, exist_ok=True)
    fades = f"afade=t=in:st=0:d=0.12,afade=t=out:st={fade_out_start:.3f}:d=0.65"
    if audio_restart_at is None:
        audio_inputs = ["-stream_loop", "-1", "-i", str(audio_source)]
        audio_filter = ["-map", "1:a:0", "-af", fades]
    else:
        audio_inputs = ["-i", str(audio_source)]
        audio_filter = [
            "-filter_complex",
            (
                f"[1:a]asplit[s0][s1];"
                f"[s0]atrim=0:{audio_restart_at:.3f},asetpts=PTS-STARTPTS[a0];"
                f"[s1]asetpts=PTS-STARTPTS[a1];"
                f"[a0][a1]acrossfade=d=0.3:c1=tri:c2=tri,{fades}[aout]"
            ),
            "-map",
            "[aout]",
        ]
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(concat_video),
        *audio_inputs,
        "-map",
        "0:v:0",
        *audio_filter,
        "-vf",
        (
            f"setpts={speed:.6f}*PTS,"
            f"scale={final_width}:{final_height}:flags=lanczos,"
            f"fps={final_fps},format=yuv420p{hold}"
        ),
        "-t",
        f"{target_duration:.6f}",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "17",
        # PCM, not AAC. DaVinci Resolve decodes AAC-in-MOV unreliably: it draws
        # the waveform in the timeline and then renders silence. This cost a day
        # on the V1 intro, so the deliverable ships uncompressed.
        "-c:a",
        "pcm_s16le",
        "-ar",
        "48000",
        "-movflags",
        "+faststart",
        str(output),
    ]
    subprocess.run(command, check=True)


def probe_duration(path: Path) -> float:
    """Seconds, read back from ffmpeg's own report."""
    # No check=True: `ffmpeg -i` without an output exits 1 but still prints the header.
    proc = subprocess.run([locate_ffmpeg(), "-hide_banner", "-i", str(path)],
                          capture_output=True, text=True)
    for line in proc.stderr.splitlines():
        if "Duration:" in line:
            h, m, sec = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(sec)
    raise RuntimeError(f"could not read duration of {path}")


def probe_size(path: Path) -> tuple[int, int]:
    out = subprocess.run([locate_ffmpeg(), "-hide_banner", "-i", str(path)],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Video:" in line:
            for token in line.split(","):
                token = token.strip().split(" ")[0]
                w, _, h = token.partition("x")
                if w.isdigit() and h.isdigit():
                    return int(w), int(h)
    raise RuntimeError(f"could not read frame size of {path}")


def read_frames(path: Path) -> np.ndarray:
    """Whole clip as uint8 [N, H, W, 3] RGB."""
    w, h = probe_size(path)
    raw = subprocess.run([locate_ffmpeg(), "-v", "error", "-i", str(path), "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w, 3)


def luma_curve(path: Path, fps: float | None = None) -> np.ndarray:
    """Mean luma (0-255) per frame; used to find flashes and white-outs."""
    cmd = [locate_ffmpeg(), "-v", "error", "-i", str(path)]
    vf = "scale=64:36,format=gray" if fps is None else f"fps={fps},scale=64:36,format=gray"
    raw = subprocess.run(cmd + ["-vf", vf, "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, 36 * 64).mean(axis=1)
