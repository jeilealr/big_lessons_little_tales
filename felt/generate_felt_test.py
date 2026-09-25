#!/usr/bin/env python3
"""Text-only test render: a short felt-animal scene for children.

No reference stills — every shot comes from its prompt alone, which makes this
a cleaner test bed for quality work than the intro (no keyframes to match, so
what you see is purely the model plus the post-processing chain).

Handmade-felt stop motion is deliberate: woollen fuzz and fabric weave show up
interpolation smearing and upscaling artefacts far more readably than the
intro's motion-blurred vortex did.

Wan renders 16 fps; video_post carries it to 30 fps with RIFE, upscales with
Real-ESRGAN and applies the grade.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import media  # noqa: E402
# imported under another name: main() has a local list called `paths`
from twc import paths as twc_paths  # noqa: E402
from twc import post as vp  # noqa: E402

MODEL = "Wan-AI/Wan2.2-T2V-A14B-Diffusers"

STYLE = (
    "handmade felt stop-motion animation, everything made of soft wool felt with "
    "visible fibres and small hand stitches, tabletop miniature set, warm soft "
    "natural light, gentle shallow depth of field, cosy children's picture-book "
    "mood, pastel colours, smooth steady camera"
)

NEGATIVE_PROMPT = (
    "photorealistic, live action, real animal fur, plastic, glossy CGI, harsh "
    "lighting, scary, dark, text, letters, watermark, subtitles, deformed, "
    "extra limbs, distorted face, flickering, jittery motion, blurry, low quality, "
    "overexposed, cluttered background"
)

SHOTS = [
    {
        "name": "01_fox_meadow",
        "prompt": (
            "A small orange felt fox with a white stitched chest and button eyes "
            "walks slowly through a meadow of green felt grass dotted with tiny "
            "wool flowers. Its bushy tail sways gently with each step. The camera "
            "tracks smoothly alongside it at its own height. Soft felt hills roll "
            "away behind, under a pale blue fabric sky with fluffy cotton clouds."
        ),
    },
    {
        "name": "02_bunny_hop",
        "prompt": (
            "A round cream-coloured felt bunny with long floppy ears hops three "
            "times across a small green felt hill, its ears bouncing on each "
            "landing. The camera follows the hops in a gentle arc. Tiny felt "
            "daisies wobble as it passes. Cotton-wool clouds drift slowly behind."
        ),
    },
    {
        "name": "03_bear_tree",
        "prompt": (
            "A chubby brown felt bear sits at the foot of a felt tree with a "
            "stitched trunk and layered green wool leaves, and slowly waves one "
            "paw at the camera. A few small felt leaves come loose and tumble "
            "softly to the ground. The camera pushes in very slowly on the bear."
        ),
    },
    {
        "name": "04_meadow_wide",
        "prompt": (
            "A wide view of the whole felt meadow: the orange fox, the cream "
            "bunny and the brown bear sit together on a green felt hill beside a "
            "felt tree. Cotton clouds drift across the fabric sky and the wool "
            "grass sways. The camera pulls slowly back to reveal the whole "
            "handmade miniature landscape resting on a wooden table."
        ),
    },
]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--fps", type=int, default=16, help="Wan's native rate")
    p.add_argument("--frames", type=int, default=81, help="4k+1; 81 = Wan's native clip")
    p.add_argument("--steps", type=int, default=40)
    p.add_argument("--guidance", type=float, default=4.0, help="high-noise expert")
    p.add_argument("--guidance-2", type=float, default=3.0, help="low-noise expert")
    p.add_argument("--seed", type=int, default=1234)
    p.add_argument("--final-fps", type=int, default=30)
    p.add_argument("--upscale", choices=("esrgan", "none"), default="esrgan")
    p.add_argument("--no-grade", action="store_true")
    p.add_argument("--audio-source", type=Path, default=None)
    p.add_argument("--work-dir", type=Path,
                   default=twc_paths.OUTPUT / "felt_test_work")
    p.add_argument("-o", "--output", type=Path,
                   default=twc_paths.OUTPUT / "felt_test.mov")
    p.add_argument("--only", type=int, nargs="+", metavar="N")
    p.add_argument("--segments-only", action="store_true")
    p.add_argument("--assemble-only", action="store_true")
    args = p.parse_args()

    if (args.frames - 1) % 4 != 0:
        raise SystemExit("--frames must be 4k+1")

    tag = f"{args.width}x{args.height}_{args.fps}fps_seed{args.seed}_s{args.steps}"
    seg_dir = args.work_dir / "shots" / tag
    paths = [seg_dir / f"{s['name']}_{args.frames}f.mp4" for s in SHOTS]
    selected = set(args.only or range(1, len(SHOTS) + 1))

    print(f"Model : {MODEL}")
    print(f"Shots : {len(SHOTS)} x {args.frames} frames at {args.width}x{args.height}, "
          f"{args.fps} fps -> {args.final_fps} fps")
    print(f"Cache : {seg_dir}")

    if not args.assemble_only:
        todo = [i for i in selected if not paths[i - 1].is_file()]
        if todo:
            import torch
            from diffusers import AutoencoderKLWan, WanPipeline
            from diffusers.utils import export_to_video

            print(f"\nLoading {MODEL} ...", flush=True)
            vae = AutoencoderKLWan.from_pretrained(MODEL, subfolder="vae",
                                                   torch_dtype=torch.float32)
            pipe = WanPipeline.from_pretrained(MODEL, vae=vae,
                                               torch_dtype=torch.bfloat16)
            pipe.enable_model_cpu_offload()
            print("Loaded.", flush=True)

            for index in sorted(todo):
                shot = SHOTS[index - 1]
                print(f"\n[{index}/{len(SHOTS)}] {shot['name']}", flush=True)
                result = pipe(
                    prompt=f"{shot['prompt']} {STYLE}",
                    negative_prompt=NEGATIVE_PROMPT,
                    height=args.height,
                    width=args.width,
                    num_frames=args.frames,
                    num_inference_steps=args.steps,
                    guidance_scale=args.guidance,
                    guidance_scale_2=args.guidance_2,
                    generator=torch.Generator(device="cpu").manual_seed(
                        args.seed + index),
                )
                paths[index - 1].parent.mkdir(parents=True, exist_ok=True)
                export_to_video(result.frames[0], str(paths[index - 1]), fps=args.fps)
                print(f"    saved {paths[index - 1]}", flush=True)
        else:
            print("\nAll requested shots are cached.")

    if args.segments_only:
        print("\nShots-only run complete.")
        return

    # Assemble only the selected shots when --only is given, so a partial set
    # can be reviewed before every shot has rendered.
    if args.only:
        paths = [paths[i - 1] for i in sorted(selected)]
    missing = [p for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("Missing shots:\n  " + "\n  ".join(str(m) for m in missing))

    # Separate shots, so unlike the intro's continuous move these are hard cuts
    # and no seam frame is dropped.
    import numpy as np
    import torch

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    clips = [vp.decode(path) for path in paths]
    print(f"\nDecoded {sum(len(c) for c in clips)} frames from {len(clips)} shots",
          flush=True)

    out_clips = []
    for i, clip in enumerate(clips, start=1):
        print(f"  shot {i}: interpolating {len(clip)} frames "
              f"{args.fps} -> {args.final_fps} fps", flush=True)
        out_clips.append(vp.retime(clip, args.fps, 1.0, args.final_fps, device))
    frames = np.concatenate(out_clips)

    if args.upscale == "esrgan":
        print(f"  upscaling {len(frames)} frames to 1920x1080...", flush=True)
        frames = vp.upscale(frames, 1920, 1080, device)

    video = args.work_dir / f"felt_{tag}.mp4"
    vp.encode(frames, video, args.final_fps,
              vf=None if args.no_grade else vp.GRADE_VF)
    print(f"  wrote {video}", flush=True)

    duration = len(frames) / args.final_fps
    if args.audio_source:
        media.finish(concat_video=video, audio_source=args.audio_source,
                  output=args.output, target_duration=duration,
                  source_duration=duration, final_width=1920, final_height=1080,
                  final_fps=args.final_fps, hold_end=0.0, audio_restart_at=None)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        video.replace(args.output)
    print(f"\nSaved felt test ({duration:.2f} s): {args.output}")


if __name__ == "__main__":
    main()
