#!/usr/bin/env python3
"""Generate TheWebtoonsCorner intro V3 from hand-picked reference keyframes.

V2 synthesised its own keyframes and they came out badly. V3 does not draw
anything: it takes the six approved stills in Intro/reference_img/ and asks
LTX-Video to animate the five transitions between them, one segment per
transition, each conditioned on its own start and end image. The segments are
then concatenated, retimed to exactly seven seconds and given the reference
soundtrack.

Segments are cached on disk, so a rerun only regenerates what changed. Use
--only to iterate on a single transition without paying for the other four.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def default_channel_root() -> Path:
    override = os.environ.get("THE_WEBTOONS_CORNER_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    if REPO_ROOT.parent.name == "repositories":
        return REPO_ROOT.parent.parent
    return REPO_ROOT


CHANNEL_ROOT = default_channel_root()
DEFAULT_REFERENCE_DIR = CHANNEL_ROOT / "Intro" / "reference_img"
DEFAULT_AUDIO_SOURCE = CHANNEL_ROOT / "Intro" / "Intro_channel_video.mov"
DEFAULT_OUTPUT = CHANNEL_ROOT / "Intro" / "Intro_channel_video_v3.mov"
DEFAULT_WORK_DIR = CHANNEL_ROOT / "Intro" / "intro_v3_work"
# The upstream LTX configs live in the LTX-Video clone, not in this repo.
LTX_VIDEO_ROOT = Path(os.environ.get("LTX_VIDEO_ROOT", CHANNEL_ROOT / "LTX-Video"))
DEFAULT_CONFIG = LTX_VIDEO_ROOT / "configs" / "ltxv-2b-0.9.8-distilled.yaml"

LTX_LICENSE_URL = (
    "https://huggingface.co/Lightricks/LTX-Video/blob/main/"
    "LTX-Video-Open-Weights-License-0.X.txt"
)

# Shared with every segment. The per-segment "no ..." lines from the briefs are
# folded in here, because LTX applies one negative prompt per generation.
NEGATIVE_PROMPT = (
    "worst quality, low detail, blurry, jittery, stuttering motion, camera shake, "
    "camera cut, scene change, sudden zoom, duplicate book, second book, deformed "
    "book, morphing book, warped emblem, changed logo, extra logos, random text, "
    "misspelled text, duplicated text, extra words, subtitles, captions, watermark, "
    "new objects, additional books, characters outside the illustrated pages, "
    "melted pages, fused pages, flickering"
)

# Keyframe-to-keyframe transitions. `weight` sets each segment's share of the
# final seven seconds, taken from the suggested 3.5 / 4 / 3.5 / 3.5 / 3.5 split.
SEGMENTS = [
    {
        "name": "01_book_awakens",
        "start": "1.png",
        "end": "2.png",
        "weight": 3.5,
        # Rewritten 2026-09-22: the original listed ~8 events (levitate,
        # particles, open, fan, light burst, pages tearing, vortex...) and the
        # model resolved that as an explosion/morph. One physical action in
        # order, and the cover actually hinges open (13B, 49 frames, seed+1).
        "prompt": (
            "Slow cinematic push-in on an ornate closed book resting on a wooden "
            "desk in a candlelit library. The glowing TWC emblem on the front "
            "cover pulses gently. The front cover slowly lifts by itself and "
            "swings open like a door, hinging on the spine, revealing bright "
            "pages inside. Warm golden light spills out from between the pages "
            "as the cover opens. Loose illustrated pages begin to lift out of the "
            "open book and float upward, with blue and violet magical particles "
            "gathering around it. Smooth, continuous, realistic motion. The book "
            "stays on the desk in the same position; same book, same cover "
            "design, same emblem throughout."
        ),
    },
    {
        "name": "02_page_tornado",
        "start": "2.png",
        "end": "3.png",
        "weight": 4.0,
        "prompt": (
            "The camera begins rapidly pulling backward away from the open magical "
            "book. Hundreds of illustrated manga and webtoon pages spiral outward "
            "from the book, forming a massive tunnel-shaped vortex. The book remains "
            "floating at the exact center of the vortex while becoming progressively "
            "smaller as the camera moves farther away. The loose pages rotate around "
            "the book in a powerful organized spiral, like a hurricane made entirely "
            "from illustrated stories. Bright electric blue, violet and magenta "
            "energy streams trace the circular motion of the vortex. Pages pass very "
            "close to the camera with strong natural motion blur and parallax, while "
            "distant pages remain sharper. The vortex grows enormous as the camera "
            "continues retreating through it. Maintain the same book, same magical "
            "environment and same visual identity. Epic cinematic scale, fluid camera "
            "movement, realistic flexible paper motion, deep perspective, volumetric "
            "light."
        ),
    },
    {
        "name": "03_vortex_rotation",
        "start": "3.png",
        "end": "4.png",
        "weight": 3.5,
        "prompt": (
            "Continue seamlessly from the enormous page vortex. The camera maintains "
            "approximately the same distance from the floating book while slowly "
            "orbiting around it. The book rotates smoothly in three-dimensional "
            "space, changing from the previous exterior-facing orientation until the "
            "open illustrated pages become clearly visible to the camera. The book "
            "remains centered inside the eye of the vortex. Hundreds of manga and "
            "webtoon pages continue flowing around it in a circular hurricane motion. "
            "Blue, violet and magenta energy streams follow the vortex. The loose "
            "pages contain varied fantasy illustrations and different scenes rather "
            "than repeating identical images. Strong depth and parallax as foreground "
            "pages sweep past the lens while distant pages spiral deeper into the "
            "tunnel. Smooth continuous cinematic rotation. Preserve the exact same "
            "book shape, scale and environment."
        ),
    },
    {
        "name": "04_dive_toward_stories",
        "start": "4.png",
        "end": "5.png",
        "weight": 3.5,
        "prompt": (
            "The open illustrated book remains floating at the center of the swirling "
            "page vortex. The camera pauses briefly, then begins accelerating forward "
            "toward the book. The book grows progressively larger as the camera flies "
            "through the eye of the vortex. Loose illustrated pages sweep past both "
            "sides of the camera at increasing speed, creating strong parallax and "
            "controlled motion blur. As the camera approaches, the individual "
            "illustrated panels printed across the open book become increasingly "
            "detailed and visible. The magical vortex continues spinning behind the "
            "book with intense blue, violet and magenta energy. A brilliant warm "
            "white light begins glowing from the center binding of the book and "
            "gradually becomes stronger. The camera moves extremely close to the open "
            "pages until the book fills most of the frame. Cinematic forward flight, "
            "smooth acceleration, realistic paper physics, dramatic depth of field."
        ),
    },
    {
        "name": "05_twc_reveal",
        "start": "5.png",
        "end": "6.png",
        "weight": 3.5,
        "prompt": (
            "Continue the forward camera movement directly toward the open book. The "
            "camera pushes closer and closer between the illustrated pages toward the "
            "brilliant light emerging from the center binding. The manga panels rush "
            "past the edges of the frame as the camera appears to enter the world "
            "inside the book. The central light rapidly intensifies into brilliant "
            "white, electric blue and magenta until it fills the entire screen. For a "
            "brief moment the screen becomes an almost complete luminous white-blue "
            "flash. From inside the light, the glowing TWC emblem gradually resolves "
            "into focus. The book itself is no longer visible. As the brightness "
            "fades, reveal a clean deep cosmic blue background filled with subtle "
            "blue and violet energy, tiny stars and drifting particles. A controlled "
            "number of manga and webtoon pages continue floating slowly around the "
            "outer edges of the frame, framing the logo without obscuring it. The TWC "
            "emblem remains perfectly centered, large, sharp and stable. The final "
            "composition becomes calm and elegant after the chaotic vortex. Camera "
            "movement gradually stops completely. Hold on the finished logo."
        ),
    },
]


def locate_ffmpeg() -> str:
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError(
            "FFmpeg is unavailable. Install inference extras with: "
            "python -m pip install -e '.[inference]'"
        ) from error


def nearest_valid_frames(target: float, minimum: int = 25) -> int:
    """LTX only accepts 8k+1 frame counts, so snap to the closest one."""
    k = max(round((target - 1) / 8), (minimum - 1) // 8)
    return int(k * 8 + 1)


def allocate_frames(duration: float, fps: int, override: int | None) -> list[int]:
    """Give each transition a frame count proportional to its weight."""
    if override is not None:
        return [override] * len(SEGMENTS)
    weights = [s["weight"] for s in SEGMENTS]
    total = sum(weights)
    # +len-1 because every seam after the first drops a duplicated frame.
    budget = duration * fps + (len(SEGMENTS) - 1)
    return [nearest_valid_frames(budget * w / total) for w in weights]


def generate_segment(
    segment: dict,
    reference_dir: Path,
    out_path: Path,
    scratch_dir: Path,
    pipeline_config: Path,
    width: int,
    height: int,
    num_frames: int,
    fps: int,
    seed: int,
    end_strength: float,
    noise_scale: float,
) -> None:
    from ltx_video.inference import InferenceConfig, infer

    start_image = reference_dir / segment["start"]
    end_image = reference_dir / segment["end"]
    scratch_dir.mkdir(parents=True, exist_ok=True)

    config = InferenceConfig(
        prompt=segment["prompt"],
        output_path=str(scratch_dir),
        pipeline_config=str(pipeline_config),
        seed=seed,
        height=height,
        width=width,
        num_frames=num_frames,
        frame_rate=fps,
        negative_prompt=NEGATIVE_PROMPT,
        conditioning_media_paths=[str(start_image), str(end_image)],
        # The start frame is pinned hard so each segment continues the previous
        # one exactly; the end frame is slightly softer so the model is allowed
        # to earn its way there instead of snapping on the last frame.
        conditioning_strengths=[1.0, end_strength],
        conditioning_start_frames=[0, num_frames - 1],
        image_cond_noise_scale=noise_scale,
        offload_to_cpu=False,
    )
    infer(config=config)

    produced = sorted(scratch_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
    if not produced:
        raise RuntimeError(f"LTX-Video produced no MP4 in {scratch_dir}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(produced[-1]), out_path)


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


def per_segment(cast):
    """argparse type for 'N=value,N=value' per-transition overrides."""

    def parse(text: str) -> dict[int, float]:
        result = {}
        for item in filter(None, text.split(",")):
            index, value = item.split("=", 1)
            index = int(index)
            if not 1 <= index <= len(SEGMENTS):
                raise argparse.ArgumentTypeError(
                    f"segment index must be 1..{len(SEGMENTS)}, got {index}"
                )
            result[index] = cast(value)
        return result

    return parse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-dir", type=Path, default=DEFAULT_REFERENCE_DIR)
    parser.add_argument("--audio-source", type=Path, default=DEFAULT_AUDIO_SOURCE)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK_DIR)
    parser.add_argument("--pipeline-config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--width", type=int, default=768)
    parser.add_argument("--height", type=int, default=432)
    parser.add_argument(
        "--segment-frames",
        type=int,
        default=None,
        help=(
            "force the same frame count for every transition; LTX requires 8k+1 "
            "(25, 33, 41, 49...). Omit to size each one from its weight."
        ),
    )
    parser.add_argument("--fps", type=int, default=24, help="generation frame rate")
    parser.add_argument("--duration", type=float, default=7.0)
    parser.add_argument(
        "--audio-restart-at",
        type=float,
        default=None,
        help=(
            "instead of blindly looping the soundtrack, crossfade it back to "
            "its start at this second so its hit and natural ending line up "
            "with the cut (the 6.0 s source: 4.15 puts the hit on the reveal)"
        ),
    )
    parser.add_argument(
        "--hold-end",
        type=float,
        default=0.0,
        help="seconds to freeze the final frame (logo hold) inside --duration",
    )
    parser.add_argument(
        "--gen-duration",
        type=float,
        default=None,
        help=(
            "seconds of footage to generate before retiming to --duration. "
            "Longer gives LTX more latent frames to spread each transition over "
            "(the preview snapped start->end within 3 frames). Default: --duration."
        ),
    )
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--final-width", type=int, default=1920)
    parser.add_argument("--final-height", type=int, default=1080)
    parser.add_argument("--final-fps", type=int, default=30)
    parser.add_argument(
        "--end-strength",
        type=float,
        default=0.92,
        help="how hard the last frame is pinned to the end reference image",
    )
    parser.add_argument("--image-cond-noise-scale", type=float, default=0.08)
    parser.add_argument(
        "--seg-seed",
        type=per_segment(int),
        default={},
        metavar="N=SEED,...",
        help="per-transition seed override (default seed+N), e.g. 1=123",
    )
    parser.add_argument(
        "--seg-frames",
        type=per_segment(int),
        default={},
        metavar="N=FRAMES,...",
        help="per-transition frame count override, e.g. 1=49 (must be 8k+1)",
    )
    parser.add_argument(
        "--seg-end-strength",
        type=per_segment(float),
        default={},
        metavar="N=STRENGTH,...",
        help="per-transition end-strength override, e.g. 1=0.7",
    )
    parser.add_argument(
        "--seg-noise",
        type=per_segment(float),
        default={},
        metavar="N=SCALE,...",
        help="per-transition image_cond_noise_scale override, e.g. 1=0.15",
    )
    parser.add_argument(
        "--only",
        type=int,
        nargs="+",
        metavar="N",
        help="regenerate only these transitions (1-5); the rest reuse their cache",
    )
    parser.add_argument(
        "--segments-only",
        action="store_true",
        help=(
            "generate the --only transitions (or every missing one) and stop "
            "before concatenation; lets several jobs fill one cache in parallel"
        ),
    )
    parser.add_argument(
        "--redo",
        action="store_true",
        help="ignore cached segments and generate every transition again",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="512x288 and 25 frames per segment for a quick low-memory test",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate inputs and print the plan without loading LTX",
    )
    parser.add_argument(
        "--accept-ltx-license",
        action="store_true",
        help=(
            "confirm that you reviewed and accept the LTXV Open Weights "
            "License 0.X before model weights are downloaded or loaded"
        ),
    )
    parser.add_argument("--force", action="store_true", help="replace final output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    reference_dir = args.reference_dir.expanduser().resolve()
    audio_source = args.audio_source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    work_root = args.work_dir.expanduser().resolve()
    pipeline_config = args.pipeline_config.expanduser().resolve()

    if args.preview:
        width, height, override = 512, 288, 25
    else:
        width, height, override = args.width, args.height, args.segment_frames

    if override is not None and (override - 1) % 8 != 0:
        raise ValueError(
            f"--segment-frames must be 8k+1 (25, 33, 41, 49...), got {override}"
        )
    gen_duration = args.gen_duration or args.duration
    frame_counts = allocate_frames(gen_duration, args.fps, override)
    for index, frames in args.seg_frames.items():
        if (frames - 1) % 8 != 0:
            raise ValueError(f"--seg-frames {index}={frames}: must be 8k+1")
        frame_counts[index - 1] = frames
    if width < 256 or height < 256:
        raise ValueError("LTX dimensions must be at least 256 pixels")
    if not pipeline_config.is_file():
        raise FileNotFoundError(f"Pipeline config not found: {pipeline_config}")
    if not audio_source.is_file():
        raise FileNotFoundError(f"Reference video/audio not found: {audio_source}")

    missing = []
    for segment in SEGMENTS:
        for key in ("start", "end"):
            path = reference_dir / segment[key]
            if not path.is_file():
                missing.append(str(path))
    if missing:
        raise FileNotFoundError(
            "Reference keyframes are missing:\n  " + "\n  ".join(sorted(set(missing)))
        )
    if output.exists() and not args.force and not args.dry_run:
        raise FileExistsError(f"Output exists: {output}\nUse --force to replace it.")

    selected = set(args.only or ())
    bad = sorted(n for n in selected if not 1 <= n <= len(SEGMENTS))
    if bad:
        raise ValueError(f"--only accepts 1..{len(SEGMENTS)}, got {bad}")

    # Cache key: anything that changes the pixels invalidates the segment.
    tag = f"{width}x{height}_{args.fps}fps_seed{args.seed}"
    segment_dir = work_root / "segments" / tag
    scratch_dir = work_root / "scratch"
    # Per-transition knobs; the cache name carries them only when they differ
    # from the global values so earlier caches stay valid.
    def seg_knobs(index: int) -> tuple[float, float]:
        return (
            args.seg_end_strength.get(index, args.end_strength),
            args.seg_noise.get(index, args.image_cond_noise_scale),
        )

    def seg_seed(index: int) -> int:
        return args.seg_seed.get(index, args.seed + index)

    def seg_filename(index: int, segment: dict, frames: int) -> str:
        es, noise = seg_knobs(index)
        suffix = ""
        if index in args.seg_seed:
            suffix += f"_s{args.seg_seed[index]}"
        if es != args.end_strength:
            suffix += f"_es{es}"
        if noise != args.image_cond_noise_scale:
            suffix += f"_n{noise}"
        return f"{segment['name']}_{frames}f{suffix}.mp4"

    segment_paths = [
        segment_dir / seg_filename(i, s, n)
        for i, (s, n) in enumerate(zip(SEGMENTS, frame_counts), start=1)
    ]

    def needs_generating(index: int, path: Path) -> bool:
        """--redo rebuilds everything, --only rebuilds those, otherwise fill gaps."""
        if args.segments_only and selected:
            return index in selected
        return args.redo or index in selected or not path.is_file()

    total_frames = sum(frame_counts) - (len(SEGMENTS) - 1)
    source_duration = total_frames / args.fps
    scale = args.duration / source_duration
    shares = [n / args.fps * scale for n in frame_counts]

    print(f"Reference keyframes : {reference_dir}")
    print(f"Pipeline            : {pipeline_config}")
    print(f"Generation          : {width}x{height} at {args.fps} fps, "
          f"{'/'.join(str(n) for n in frame_counts)} frames per transition")
    print(f"Segment cache       : {segment_dir}")
    print(f"Concatenated length : {total_frames} frames ({source_duration:.2f} s)")
    print(f"Retimed to          : {args.duration:.2f} s "
          f"(x{(args.duration - args.hold_end) / source_duration:.3f} speed"
          f"{f', last frame held {args.hold_end:.2f} s' if args.hold_end else ''})")
    print(f"Final output        : {output} "
          f"({args.final_width}x{args.final_height} at {args.final_fps} fps)")
    print(f"Soundtrack          : {audio_source}")
    print("")
    for index, (segment, path, share) in enumerate(
        zip(SEGMENTS, segment_paths, shares), start=1
    ):
        state = "generate" if needs_generating(index, path) else "cached"
        print(
            f"  {index}. {segment['start']} -> {segment['end']}  "
            f"{segment['name']:<24} ~{share:.1f} s in the cut  [{state}]"
        )

    if args.dry_run:
        print("\nDry run complete: inputs validated, LTX model was not loaded.")
        return

    if not args.accept_ltx_license:
        raise SystemExit(
            "\nModel generation was not started. Review the checkpoint license at:\n"
            f"  {LTX_LICENSE_URL}\n"
            "Then rerun with --accept-ltx-license if you accept its terms."
        )

    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    print("\nLicense acknowledged: LTXV Open Weights License 0.X")
    print("The first run downloads the 2B checkpoint, upscaler, and text encoder.\n")

    for index, (segment, path, frames) in enumerate(
        zip(SEGMENTS, segment_paths, frame_counts), start=1
    ):
        if not needs_generating(index, path):
            print(f"[{index}/{len(SEGMENTS)}] {segment['name']}: reusing cached clip")
            continue
        end_strength, noise_scale = seg_knobs(index)
        print(f"[{index}/{len(SEGMENTS)}] {segment['name']}: generating "
              f"{segment['start']} -> {segment['end']} "
              f"({frames} frames, end-strength {end_strength}, noise {noise_scale}, "
              f"seed {seg_seed(index)})")
        generate_segment(
            segment=segment,
            reference_dir=reference_dir,
            out_path=path,
            scratch_dir=scratch_dir / segment["name"],
            pipeline_config=pipeline_config,
            width=width,
            height=height,
            num_frames=frames,
            fps=args.fps,
            # Per-segment seed offset, so two transitions with similar prompts
            # do not land on the same noise and look like the same shot twice.
            seed=seg_seed(index),
            end_strength=end_strength,
            noise_scale=noise_scale,
        )
        print(f"    saved {path}")

    if args.segments_only:
        print("\nSegments-only run complete; skipping concatenation.")
        return

    absent = [p for p in segment_paths if not p.is_file()]
    if absent:
        raise RuntimeError(
            "Missing segment clips:\n  " + "\n  ".join(str(p) for p in absent)
        )

    concat_video = work_root / f"concat_{tag}.mp4"
    print("\nConcatenating segments...")
    concat_segments(segment_paths, concat_video, args.fps)
    print(f"  {concat_video}")

    print("Retiming, scaling and adding the soundtrack...")
    finish(
        concat_video=concat_video,
        audio_source=audio_source,
        output=output,
        target_duration=args.duration,
        source_duration=source_duration,
        final_width=args.final_width,
        final_height=args.final_height,
        final_fps=args.final_fps,
        hold_end=args.hold_end,
        audio_restart_at=args.audio_restart_at,
    )
    print(f"\nSaved intro V3: {output}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
