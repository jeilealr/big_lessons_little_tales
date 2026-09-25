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

Stages: generate (GPU) -> post (GPU) -> finish (CPU). This file currently
implements `generate`; `post`/`finish` reuse twc.post, the procedural renderer
and the hybrid cut.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import paths, wan  # noqa: E402

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


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["generate"])
    ap.add_argument("--variant", choices=["white", "open"], required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    generate(args.variant, args.dry_run)


if __name__ == "__main__":
    main()
