#!/usr/bin/env python3
"""One-shot variant of intro V3: condition only on the first and last stills
(1.png -> 6.png) and let a single text prompt carry the whole journey.

Reuses generate_intro_v3's segment generator and finishing (retime, scale,
soundtrack), so the output is directly comparable with the 5-keyframe cut.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import generate_intro_v3 as v3

STORY = {
    "name": "single_shot",
    "start": "1.png",
    "end": "6.png",
    "weight": 1.0,
    "prompt": (
        "One continuous cinematic shot. It begins with a slow push-in on an "
        "ornate closed book resting on a wooden desk in a candlelit library; the "
        "glowing TWC emblem on its cover pulses with blue and magenta light. The "
        "front cover slowly lifts and swings open on its spine, and warm golden "
        "light spills from the pages. Illustrated manga and webtoon pages tear "
        "free and spiral upward, more and more of them, while blue, violet and "
        "magenta energy streams wrap around the book and form a growing vortex. "
        "The camera pulls back through the vortex: hundreds of pages rotate "
        "around the floating book like a hurricane made of stories, the book "
        "small at the calm center. The camera orbits the book as it turns to "
        "show its open illustrated pages, then accelerates forward again, diving "
        "through the eye of the vortex toward the open book until the manga "
        "panels fill the frame. A brilliant white-blue light swells from the "
        "center binding and floods the screen for a brief moment. Out of the "
        "light the glowing TWC emblem resolves, sharp and centered, with the "
        "text THE WEBTOONS CORNER beneath it, on a deep cosmic blue background "
        "with drifting pages and stars at the edges. The camera comes to rest "
        "and holds on the finished logo. Smooth continuous camera motion, no "
        "cuts, realistic paper physics, volumetric light, the same book and the "
        "same emblem throughout."
    ),
}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--width", type=int, default=768)
    p.add_argument("--height", type=int, default=432)
    p.add_argument("--frames", type=int, default=241, help="8k+1; 241 = 10 s at 24 fps")
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--duration", type=float, default=10.0)
    p.add_argument("--hold-end", type=float, default=0.0)
    p.add_argument("--audio-restart-at", type=float, default=None)
    p.add_argument("--seed", type=int, default=20260921)
    p.add_argument("--end-strength", type=float, default=0.9)
    p.add_argument("--image-cond-noise-scale", type=float, default=0.1)
    p.add_argument("--pipeline-config", type=Path,
                   default=v3.REPO_ROOT / "configs" / "twc-13b-0.9.8-distilled.yaml")
    p.add_argument("--work-dir", type=Path, default=v3.CHANNEL_ROOT / "Intro" / "intro_single_work")
    p.add_argument("-o", "--output", type=Path,
                   default=v3.CHANNEL_ROOT / "Intro" / "Intro_channel_video_single.mov")
    p.add_argument("--accept-ltx-license", action="store_true")
    p.add_argument("--segments-only", action="store_true", help="generate the clip, skip finishing")
    args = p.parse_args()

    if (args.frames - 1) % 8 != 0:
        raise SystemExit("--frames must be 8k+1")
    if not args.accept_ltx_license:
        raise SystemExit("rerun with --accept-ltx-license (LTXV Open Weights License 0.X)")

    tag = f"{args.width}x{args.height}_{args.fps}fps_seed{args.seed}"
    clip = args.work_dir / "segments" / tag / (
        f"single_{args.frames}f_es{args.end_strength}_n{args.image_cond_noise_scale}.mp4"
    )
    print(f"Clip: {clip}  [{'cached' if clip.is_file() else 'generate'}]")
    if not clip.is_file():
        v3.generate_segment(
            STORY, v3.DEFAULT_REFERENCE_DIR, clip, args.work_dir / "scratch",
            args.pipeline_config, width=args.width, height=args.height,
            num_frames=args.frames, fps=args.fps, seed=args.seed,
            end_strength=args.end_strength, noise_scale=args.image_cond_noise_scale,
        )
        print(f"    saved {clip}")
    if args.segments_only:
        return
    source_duration = args.frames / args.fps
    v3.finish(
        concat_video=clip, audio_source=v3.DEFAULT_AUDIO_SOURCE, output=args.output,
        target_duration=args.duration, source_duration=source_duration,
        final_width=1920, final_height=1080, final_fps=30,
        hold_end=args.hold_end, audio_restart_at=args.audio_restart_at,
    )
    print(f"\nSaved single-shot intro: {args.output}")


if __name__ == "__main__":
    main()
