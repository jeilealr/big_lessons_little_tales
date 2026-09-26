#!/usr/bin/env python3
"""Render a story shot: image-to-video from its composed keyframe.

The shot is defined in story.yaml under its scene (`shots:`). The prompt is
the shot's action, then each character's frozen sheet, then the location sheet
and the style bible, exactly like the text-only baseline (production/
scene_baseline.py), so the only difference between the two is the anchored
first frame.

  python production/shot.py --scene 1 --shot s01_establish [--seed 5101]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import paths, wan  # noqa: E402

RENDER = dict(width=1280, height=720, steps=40, guidance=3.5, guidance_2=3.5)


def main() -> None:
    import yaml
    from PIL import Image

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse")
    ap.add_argument("--scene", type=int, required=True)
    ap.add_argument("--shot", required=True)
    ap.add_argument("--seed", type=int, help="default: every seed listed for the shot")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    story = yaml.safe_load((paths.REPO / "stories" / args.story / "story.yaml").read_text())
    scene = story["scenes"][args.scene]
    shot = next(s for s in scene["shots"] if s["name"] == args.shot)
    work = paths.WORK / "stories" / args.story
    keyframe = work / shot["keyframe"]
    parts = [shot["action"].strip()]
    for c in shot.get("characters", scene.get("characters", [])):
        ch = story["characters"][c]
        parts.append(f"{ch['name'][0].upper() + ch['name'][1:]} is {ch['sheet']}.")
    parts.append(f"The scene is {story['locations'][scene['location']]['sheet']}.")
    parts.append(story["style"] + ".")
    prompt = " ".join(parts)
    seeds = [args.seed] if args.seed else shot["seeds"]
    frames = shot.get("frames", 81)
    print(f"[{args.shot}] keyframe {keyframe.name}, {frames} frames, seeds {seeds}\n{prompt}\n",
          flush=True)
    if not keyframe.is_file():
        raise SystemExit(f"missing keyframe {keyframe}")
    if args.dry_run:
        return
    pipe = wan.load("i2v", frames)
    print("model loaded", flush=True)
    for seed in seeds:
        out = work / "shots" / f"{args.shot}_s{seed}.mp4"
        if out.is_file():
            print(f"exists, skipping {out.name}"); continue
        t0 = time.time()
        video = wan.generate(pipe, prompt, negative=story["negative"], frames=frames, seed=seed,
                             image=Image.open(keyframe), **RENDER)
        wan.save(video, out)
        out.with_suffix(".json").write_text(json.dumps(dict(
            stage="shot", scene=args.scene, shot=args.shot, keyframe=str(keyframe),
            model=wan.MODELS["i2v"], seed=seed, frames=frames, prompt=prompt,
            negative=story["negative"], seconds=round(time.time() - t0), **RENDER), indent=2))
        print(f"saved {out} ({time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
