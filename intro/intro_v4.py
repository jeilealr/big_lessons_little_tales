#!/usr/bin/env python3
"""Intro v4: one Wan clip from 1.png, described in text, into the procedural reveal.

Why this shape: forcing the video through intermediate stills made it feel like
interpolating between pictures; the version with fewer stills was better, and
the part everyone liked in the hybrid was the code-rendered logo reveal. Since
the hybrid joins inside a white flash, the Wan part no longer has to end on any
particular image, so only the opening still (the approved book) is kept.

Variants:
  white  last_image = a white card, which forces the clip to end in a white-out
         and makes the join to the reveal airtight (experimental: may wash out early)
  open   first frame only; the prompt alone asks for the light burst

Stages:
  generate --variant V            Wan I2V clip                          GPU, ~2.5 h
  analyze  --variant V            when does the clip white out?         CPU, seconds
  post     --variant V --hit T    RIFE + ESRGAN, retimed so the
                                  white-out lands at T seconds          GPU, ~15 min
  finish   --variant V --hit T    grade, score and procedural reveal
                                  timed to T, hybrid cut                CPU, ~4 min
T (default 6.0) is where the logo lands; the rest of the 10 s belongs to it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import media, paths, wan  # noqa: E402

JOURNEY = (
    "One continuous cinematic shot. A slow push-in on the ornate closed book resting on "
    "the wooden desk in the candlelit library; the glowing TWC emblem on its cover pulses "
    "with blue and magenta light. The front cover slowly lifts and swings open on its "
    "spine, and warm golden light spills out from between the pages. Illustrated manga "
    "pages tear free and spiral upward around the book while blue, violet and magenta "
    "energy streams gather into a swirling vortex of pages. The camera flies forward "
    "through the vortex toward the glowing centre of the open book, and the light at the "
    "centre grows brighter and brighter until a brilliant white light bursts out and "
    "fills the entire frame. Smooth continuous camera movement, no cuts, realistic paper "
    "physics, volumetric light. The same ornate book and the same TWC emblem throughout."
)
NEGATIVE = (
    "bright tones, overexposed, static, blurred details, subtitles, style, artwork, "
    "painting, picture, still, overall gray, worst quality, low quality, JPEG artifacts, "
    "ugly, deformed, motionless frame, cluttered background, duplicate book, second book, "
    "deformed book, morphing book, warped emblem, changed logo, extra logos, random text, "
    "misspelled text, watermark, flickering"
)
RENDER = dict(width=1280, height=720, frames=81, steps=40, guidance=3.5, guidance_2=3.5)
SEED = 20260925
WORK = paths.WORK / "intro_v4"


def generate(variant: str, dry_run: bool) -> None:
    from PIL import Image

    start = paths.REFERENCE / "1.png"
    end = Image.new("RGB", (RENDER["width"], RENDER["height"]), (255, 253, 248)) \
        if variant == "white" else None
    out = WORK / f"{variant}.mp4"
    print(f"[intro v4 / {variant}] start={start.name} end={'white card' if end else 'none'} "
          f"seed={SEED} {RENDER}", flush=True)
    if dry_run:
        print("dry run: inputs ok, model not loaded")
        return
    pipe = wan.load("i2v", RENDER["frames"])
    print("  model loaded", flush=True)
    frames = wan.generate(pipe, JOURNEY, negative=NEGATIVE, seed=SEED,
                          image=Image.open(start), last_image=end, **RENDER)
    wan.save(frames, out)
    out.with_suffix(".json").write_text(json.dumps(dict(
        stage="generate", variant=variant, model=wan.MODELS["i2v"], start_image=str(start),
        end_image="white card (255,253,248)" if end else None, seed=SEED, prompt=JOURNEY,
        negative=NEGATIVE, created=time.strftime("%Y-%m-%d %H:%M:%S"), **RENDER), indent=2))
    print(f"  saved {out}", flush=True)


def analyze(variant: str) -> dict:
    """Find the white-out: the first frame, late in the clip, within a few
    luma levels of the clip's brightest frame. If the clip never gets really
    bright (the `open` variant may not), cut at the end of the clip."""
    clip = WORK / f"{variant}.mp4"
    luma = media.luma_curve(clip)
    start = int(len(luma) * 0.4)
    peak = float(luma[start:].max())
    if peak >= 200:
        index = start + int((luma[start:] >= peak - 8).argmax())
        how = "first frame within 8 luma levels of the late peak"
    else:
        # Cutting at the brightest frame of a clip that never gets bright would
        # throw away the journey. Cut at the end instead; the hybrid cut's white
        # ramp then provides the flash.
        index = len(luma) - 1
        how = (f"no real white-out (peak luma {peak:.0f}); cutting at the end of the clip, "
               f"the hybrid's white ramp makes the flash")
    info = dict(variant=variant, frames=len(luma), whiteout_frame=index,
                whiteout_time=index / wan.FPS, peak_luma=peak, how=how,
                luma=[round(float(v), 1) for v in luma])
    (WORK / f"{variant}_analysis.json").write_text(json.dumps(info, indent=2))
    print(f"[analyze / {variant}] white-out at frame {index} = {index / wan.FPS:.2f} s "
          f"(peak luma {peak:.0f}); {how}")
    return info


def post(variant: str, hit: float) -> None:
    import torch

    from twc import post as vp

    info = analyze(variant)
    speed = hit / info["whiteout_time"]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[post / {variant}] retime x{speed:.3f} so the white-out lands at {hit:.2f} s "
          f"(on {device})", flush=True)
    frames = vp.decode(WORK / f"{variant}.mp4")
    frames = vp.retime(frames, wan.FPS, speed, 30, device)
    frames = vp.upscale(frames, 1920, 1080, device)
    master = WORK / f"{variant}_master_hit{hit:.2f}.mp4"
    vp.encode(frames, master, 30)
    print(f"  wrote {master} ({len(frames)} frames, ungraded)", flush=True)


def finish(variant: str, hit: float, duration: float) -> None:
    from twc import post as vp

    repo = paths.REPO
    py = sys.executable
    tag = f"hit{hit:.2f}"
    master = WORK / f"{variant}_master_{tag}.mp4"
    graded = WORK / f"{variant}_graded_{tag}.mp4"
    score = WORK / f"score_{tag}.wav"
    reveal = WORK / f"procedural_{tag}.mov"
    out = paths.OUTPUT / f"Intro_channel_video_v4_{variant}.mov"
    print(f"[finish / {variant}] grade", flush=True)
    vp.grade(master, graded)
    print(f"[finish / {variant}] score with the impact at {hit:.2f} s", flush=True)
    subprocess.run([py, str(repo / "audio" / "make_music.py"), "--duration", str(duration),
                    "--impact-at", f"{hit:.3f}", "-o", str(score)], check=True)
    if not reveal.with_name(reveal.stem + "_silent.mp4").is_file():
        print(f"[finish / {variant}] procedural reveal at {hit:.2f} s", flush=True)
        subprocess.run([py, str(repo / "procedural" / "twc_ident.py"), "--hit", f"{hit:.3f}",
                        "--audio", str(score), "-o", str(reveal)], check=True)
    print(f"[finish / {variant}] hybrid cut", flush=True)
    subprocess.run([py, str(repo / "intro" / "hybrid_cut.py"), "--wan", str(graded),
                    "--procedural", str(reveal.with_name(reveal.stem + "_silent.mp4")),
                    "--audio", str(score), "--cut", f"{hit:.3f}",
                    "--duration", str(duration), "-o", str(out)], check=True)
    print(f"\nSaved intro v4 ({variant}): {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["generate", "analyze", "post", "finish"])
    ap.add_argument("--variant", choices=["white", "open"], required=True)
    ap.add_argument("--hit", type=float, default=6.0,
                    help="seconds at which the white-out, the score's impact and the "
                         "logo reveal all land")
    ap.add_argument("--duration", type=float, default=10.0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.stage == "generate":
        generate(args.variant, args.dry_run)
    elif args.stage == "analyze":
        analyze(args.variant)
    elif args.stage == "post":
        post(args.variant, args.hit)
    else:
        finish(args.variant, args.hit, args.duration)


if __name__ == "__main__":
    main()
