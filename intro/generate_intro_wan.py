#!/usr/bin/env python3
"""Render the TWC intro with Wan 2.2 I2V-A14B instead of LTX-Video.

Same structure as generate_intro_v3: the six approved stills define five
transitions, each generated as one clip conditioned on its own start image
(`image`) and end image (`last_image`). Only the picture comes from Wan; the
concat / retime / 1080p scale / soundtrack tail is generate_intro_v3's, so the
audio treatment is identical to the LTX cut.

Wan 2.2 I2V-A14B is a mixture-of-experts model: a high-noise transformer runs
above the boundary timestep and a low-noise one below it, which is why both
guidance scales exist and why the weights are offloaded per module.

Wan renders at 16 fps natively, so the concat is motion-interpolated to the
final 30 fps rather than frame-duplicated (--no-interpolate to skip).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prompts import SEGMENTS  # noqa: E402  (intro/prompts.py)
from twc import media  # noqa: E402
# imported under another name: main() has a local list called `paths`
from twc import paths as twc_paths  # noqa: E402
from twc import post as vp  # noqa: E402

DEFAULT_AUDIO = twc_paths.OUTPUT / "Intro_channel_video.mov"

MODEL = "Wan-AI/Wan2.2-I2V-A14B-Diffusers"

# Wan's own recommended negative prompt (translated) plus the identity guards
# from the LTX cut: no second book, no invented text, no warped emblem.
NEGATIVE_PROMPT = (
    "bright tones, overexposed, static, blurred details, subtitles, style, artwork, "
    "painting, picture, still, overall gray, worst quality, low quality, JPEG artifacts, "
    "ugly, deformed, extra fingers, poorly drawn hands, poorly drawn face, malformed, "
    "disfigured, fused fingers, motionless frame, cluttered background, three legs, "
    "many people in the background, walking backwards, "
    "duplicate book, second book, deformed book, morphing book, warped emblem, "
    "changed logo, extra logos, random text, misspelled text, watermark, flickering"
)

# 16 fps native; 4k+1 frame counts. Same 3.5/4/3.5/3.5/3.5 weighting as V3.
DEFAULT_FRAMES = [33, 41, 33, 33, 33]

# "story" plan: keep only stills 1, 5 and 6. The journey from the closed book to
# the open book at the heart of the vortex is described in text and pinned at
# both ends (1.png -> 5.png) instead of being forced through the intermediate
# keyframes; the reveal 5.png -> 6.png is the chain's segment 5, given a second
# more screen time.
STORY_SEGMENTS = [
    {
        "name": "01_journey",
        "start": "1.png",
        "end": "5.png",
        "prompt": (
            "One continuous cinematic shot. A slow push-in on an ornate closed "
            "book resting on a wooden desk in a candlelit library; the glowing "
            "TWC emblem on its cover pulses with blue and magenta light. The "
            "front cover lifts by itself and swings open on its spine, and warm "
            "golden light spills out from between the pages. Illustrated manga "
            "and webtoon pages tear free one after another and spiral upward, "
            "more and more of them, while blue, violet and magenta energy "
            "streams wrap around the book and gather into a growing vortex. The "
            "camera pulls back through that vortex: hundreds of loose pages turn "
            "around the floating book like a hurricane made of stories, the book "
            "small and calm at the centre, pages sweeping close past the lens "
            "with strong parallax and motion blur. The camera then orbits the "
            "book while it rotates in the air until its open illustrated pages "
            "face the lens, and finally accelerates forward again, flying "
            "through the eye of the vortex toward the book, which grows larger "
            "and larger until the open pages and their manga panels fill most "
            "of the frame and a warm light glows from the central binding. "
            "Smooth continuous camera movement, no cuts, realistic paper "
            "physics, deep perspective, volumetric light. The same ornate book "
            "and the same TWC emblem throughout, no second book, no new objects."
        ),
    },
    # The reveal the chain already got right, kept verbatim.
    dict(SEGMENTS[4]),
]
STORY_FRAMES = [97, 41]

# "story" plan: keep only stills 1, 5 and 6. The whole journey from the closed
# book to the open book at the heart of the vortex is described in text and
# pinned at both ends (1.png -> 5.png) instead of being forced through the
# intermediate keyframes; the reveal 5.png -> 6.png is the chain's segment 5,
# given a second more screen time.
STORY_SEGMENTS = [
    {
        "name": "01_journey",
        "start": "1.png",
        "end": "5.png",
        "prompt": (
            "One continuous cinematic shot. A slow push-in on an ornate closed "
            "book resting on a wooden desk in a candlelit library; the glowing "
            "TWC emblem on its cover pulses with blue and magenta light. The "
            "front cover lifts by itself and swings open on its spine, and warm "
            "golden light spills out from between the pages. Illustrated manga "
            "and webtoon pages tear free one after another and spiral upward, "
            "more and more of them, while blue, violet and magenta energy "
            "streams wrap around the book and gather into a growing vortex. The "
            "camera pulls back through that vortex: hundreds of loose pages turn "
            "around the floating book like a hurricane made of stories, the book "
            "small and calm at the centre, pages sweeping close past the lens "
            "with strong parallax and motion blur. The camera then orbits the "
            "book while it rotates in the air until its open illustrated pages "
            "face the lens, and finally accelerates forward again, flying "
            "through the eye of the vortex toward the book, which grows larger "
            "and larger until the open pages and their manga panels fill most "
            "of the frame and a warm light glows from the central binding. "
            "Smooth continuous camera movement, no cuts, realistic paper "
            "physics, deep perspective, volumetric light. The same ornate book "
            "and the same TWC emblem throughout, no second book, no new objects."
        ),
    },
    # The reveal the chain already got right, kept verbatim.
    dict(SEGMENTS[4]),
]
STORY_FRAMES = [97, 41]


def generate_segment(pipe, segment, out_path, width, height, frames, seed,
                     steps, guidance, guidance_2, fps):
    import torch
    from diffusers.utils import export_to_video
    from PIL import Image

    start = Image.open(twc_paths.REFERENCE / segment["start"]).convert("RGB")
    end = Image.open(twc_paths.REFERENCE / segment["end"]).convert("RGB")

    result = pipe(
        image=start,
        last_image=end,
        prompt=segment["prompt"],
        negative_prompt=NEGATIVE_PROMPT,
        height=height,
        width=width,
        num_frames=frames,
        num_inference_steps=steps,
        guidance_scale=guidance,
        guidance_scale_2=guidance_2,
        generator=torch.Generator(device="cpu").manual_seed(seed),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    export_to_video(result.frames[0], str(out_path), fps=fps)


def probe_duration(path: Path) -> float:
    """Seconds of `path`, read back from ffmpeg's own report.

    minterpolate does not land on the requested length exactly, so the hold is
    sized from what the file actually is rather than from what we asked for.
    """
    ffmpeg = media.locate_ffmpeg()
    proc = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path)],
                          capture_output=True, text=True)
    for line in proc.stderr.splitlines():
        if "Duration:" in line:
            h, m, sec = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(sec)
    raise RuntimeError(f"could not read duration of {path}")


def retime_and_interpolate(concat_video, out_path, speed, final_fps, interpolate):
    """Slow the 16 fps concat to its final length, then resample to final_fps.

    The speed change happens before interpolation so the interpolator sees the
    final timing; otherwise the fps filter would just duplicate frames twice.
    """
    ffmpeg = media.locate_ffmpeg()
    if interpolate:
        resample = (
            f"minterpolate=fps={final_fps}:mi_mode=mci:mc_mode=aobmc:"
            f"me_mode=bidir:vsbmc=1"
        )
    else:
        resample = f"fps={final_fps}"
    subprocess.run(
        [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(concat_video),
         "-vf", f"setpts={speed:.6f}*PTS,{resample}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p",
         str(out_path)],
        check=True,
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--fps", type=int, default=16, help="Wan's native rate")
    p.add_argument("--plan", choices=("chain", "story"), default="chain",
                   help="chain: all six stills; story: only 1/5/6, middle described")
    p.add_argument("--frames", type=int, nargs="+", default=None,
                   help="frames per transition (4k+1 each); defaults follow --plan")
    p.add_argument("--steps", type=int, default=40)
    p.add_argument("--guidance", type=float, default=3.5, help="high-noise expert")
    p.add_argument("--guidance-2", type=float, default=3.5, help="low-noise expert")
    p.add_argument("--seed", type=int, default=20260921)
    p.add_argument("--duration", type=float, default=10.0)
    p.add_argument("--hold-end", type=float, default=1.0)
    p.add_argument("--audio-source", type=Path, default=None,
                   help="soundtrack; defaults to the channel reference video")
    p.add_argument("--audio-restart-at", type=float, default=4.15,
                   help="crossfade the soundtrack back to its start here; pass a "
                        "negative value for a track already long enough to play once")
    p.add_argument("--final-fps", type=int, default=30)
    p.add_argument("--no-interpolate", action="store_true",
                   help="duplicate frames for the 16->30 fps step instead of interpolating")
    p.add_argument("--interpolator", choices=("rife", "minterpolate"), default="rife",
                   help="rife: learned interpolation (MIT); minterpolate: ffmpeg block matching")
    p.add_argument("--upscale", choices=("esrgan", "none"), default="esrgan",
                   help="esrgan: Real-ESRGAN x4 then resample (BSD-3); none: lanczos in finish()")
    p.add_argument("--no-grade", action="store_true",
                   help="skip the bloom/contrast/grain finish")
    p.add_argument("--work-dir", type=Path,
                   default=twc_paths.OUTPUT / "intro_wan_work")
    p.add_argument("-o", "--output", type=Path,
                   default=twc_paths.OUTPUT / "Intro_channel_video_wan.mov")
    p.add_argument("--only", type=int, nargs="+", metavar="N",
                   help="generate only these transitions (1-5)")
    p.add_argument("--segments-only", action="store_true",
                   help="generate clips and stop before assembly")
    p.add_argument("--assemble-only", action="store_true",
                   help="skip generation; concat + finish from the cache")
    args = p.parse_args()

    segments = STORY_SEGMENTS if args.plan == "story" else SEGMENTS
    if args.frames is None:
        args.frames = STORY_FRAMES if args.plan == "story" else DEFAULT_FRAMES
    if len(args.frames) != len(segments):
        raise SystemExit(f"--frames needs {len(segments)} values for --plan {args.plan}")
    for n in args.frames:
        if (n - 1) % 4 != 0:
            raise SystemExit(f"Wan needs 4k+1 frames per clip, got {n}")

    tag = f"{args.width}x{args.height}_{args.fps}fps_seed{args.seed}_s{args.steps}"
    seg_dir = args.work_dir / "segments" / tag
    paths = [seg_dir / f"{s['name']}_{n}f.mp4" for s, n in zip(segments, args.frames)]
    selected = set(args.only or range(1, len(segments) + 1))

    total_frames = sum(args.frames) - (len(segments) - 1)
    source_duration = total_frames / args.fps
    print(f"Model      : {MODEL}")
    print(f"Generation : {args.width}x{args.height} at {args.fps} fps, "
          f"{'/'.join(map(str, args.frames))} frames, {args.steps} steps")
    print(f"Concat     : {total_frames} frames ({source_duration:.2f} s) -> "
          f"{args.duration:.2f} s incl. {args.hold_end:.2f} s hold")
    print(f"Cache      : {seg_dir}")

    if not args.assemble_only:
        todo = [i for i in selected if not paths[i - 1].is_file()]
        if todo:
            import torch
            from diffusers import AutoencoderKLWan, WanImageToVideoPipeline

            print(f"\nLoading {MODEL} ...", flush=True)
            vae = AutoencoderKLWan.from_pretrained(MODEL, subfolder="vae",
                                                   torch_dtype=torch.float32)
            pipe = WanImageToVideoPipeline.from_pretrained(MODEL, vae=vae,
                                                           torch_dtype=torch.bfloat16)
            # The two 14B experts plus the 11B text encoder do not fit on one
            # GCD together; this keeps only the module in use resident.
            pipe.enable_model_cpu_offload()
            if max(args.frames) > 81:
                # Beyond Wan's native 81-frame clip the VAE decode is what runs
                # out of memory first, so decode it in tiles.
                pipe.vae.enable_tiling()
            print("Loaded.", flush=True)

            for index in sorted(todo):
                segment = segments[index - 1]
                print(f"\n[{index}/{len(segments)}] {segment['name']}: "
                      f"{segment['start']} -> {segment['end']} "
                      f"({args.frames[index - 1]} frames)", flush=True)
                generate_segment(pipe, segment, paths[index - 1], args.width,
                                 args.height, args.frames[index - 1],
                                 args.seed + index, args.steps, args.guidance,
                                 args.guidance_2, args.fps)
                print(f"    saved {paths[index - 1]}", flush=True)
        else:
            print("\nAll requested clips are cached.")

    if args.segments_only:
        print("\nSegments-only run complete; skipping assembly.")
        return

    missing = [p for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("Missing clips:\n  " + "\n  ".join(str(m) for m in missing))

    concat = args.work_dir / f"concat_{tag}.mp4"
    print("\nConcatenating segments...", flush=True)
    media.concat_segments(paths, concat, args.fps)

    retimed = args.work_dir / f"retimed_{tag}.mp4"
    speed = (args.duration - args.hold_end) / source_duration
    use_learned = args.interpolator == "rife" and not args.no_interpolate
    if use_learned or args.upscale == "esrgan" or not args.no_grade:
        import torch

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Post-processing on {device} "
              f"(interpolator={args.interpolator}, upscale={args.upscale}, "
              f"grade={not args.no_grade})...", flush=True)
        frames = vp.decode(concat)
        print(f"  decoded {len(frames)} frames at {frames.shape[2]}x{frames.shape[1]}",
              flush=True)
        if use_learned:
            frames = vp.retime(frames, args.fps, speed, args.final_fps, device)
        else:
            retime_and_interpolate(concat, retimed, speed, args.final_fps,
                                   not args.no_interpolate)
            frames = vp.decode(retimed)
        if args.upscale == "esrgan":
            print(f"  upscaling {len(frames)} frames to 1920x1080...", flush=True)
            frames = vp.upscale(frames, 1920, 1080, device)
        vp.encode(frames, retimed, args.final_fps,
                  vf=None if args.no_grade else vp.GRADE_VF)
        print(f"  wrote {retimed}", flush=True)
    else:
        print(f"Retiming x{speed:.3f} and resampling to {args.final_fps} fps"
              f"{'' if args.no_interpolate else ' (motion interpolated)'}...", flush=True)
        retime_and_interpolate(concat, retimed, speed, args.final_fps,
                               not args.no_interpolate)

    actual = probe_duration(retimed)
    hold = max(0.0, args.duration - actual)
    print(f"Scaling to 1080p and adding the soundtrack "
          f"(retimed clip {actual:.2f} s, holding {hold:.2f} s)...", flush=True)
    media.finish(
        concat_video=retimed,
        audio_source=args.audio_source or DEFAULT_AUDIO,
        output=args.output,
        target_duration=args.duration,
        source_duration=actual,
        final_width=1920,
        final_height=1080,
        final_fps=args.final_fps,
        hold_end=hold,
        audio_restart_at=None if args.audio_restart_at < 0 else args.audio_restart_at,
    )
    print(f"\nSaved Wan intro: {args.output}")


if __name__ == "__main__":
    main()
