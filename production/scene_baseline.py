#!/usr/bin/env python3
"""Render a scene straight from the story text: no anchors, no LoRA.

The baseline every consistency technique is measured against. The prompt is
the scene text from story.yaml, then each character's frozen sheet, then the
location sheet, then the style bible.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths, wan  # noqa: E402

RENDER = dict(width=1280, height=720, frames=49, steps=40, guidance=4.0, guidance_2=3.0)


def build_prompt(story: dict, n: int) -> tuple[str, str]:
    sc = story["scenes"][n]
    parts = [sc["text"].strip()]
    for c in sc.get("characters", []):
        ch = story["characters"][c]
        parts.append(f"{ch['name'][0].upper() + ch['name'][1:]} is {ch['sheet']}.")
    parts.append(f"The scene is {story['locations'][sc['location']]['sheet']}.")
    parts.append(story["style"] + ".")
    return " ".join(parts), story["negative"]


def main() -> None:
    import yaml

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--story", default="lion_and_mouse_v2")
    ap.add_argument("--scene", type=int, required=True)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--frames", type=int, default=RENDER["frames"],
                    help="4k+1; 49 = 3 s keeps the baseline inside one dev-g job")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    RENDER["frames"] = args.frames
    story = yaml.safe_load((paths.REPO / "stories" / args.story / "story.yaml").read_text())
    prompt, negative = build_prompt(story, args.scene)
    out = paths.WORK / "stories" / args.story / "scenes" / f"scene{args.scene:02d}_t2v_baseline.mp4"
    print(f"[scene {args.scene} baseline] {len(prompt.split())} words\n{prompt}\n", flush=True)
    if args.dry_run:
        return
    t0 = time.time()
    pipe = wan.load("t2v", RENDER["frames"])
    print("model loaded", flush=True)
    frames = wan.generate(pipe, prompt, negative=negative, seed=args.seed, **RENDER)
    wan.save(frames, out)
    out.with_suffix(".json").write_text(json.dumps(dict(
        stage="scene_baseline", scene=args.scene, model=wan.model_id("t2v"), seed=args.seed,
        prompt=prompt, negative=negative, seconds=round(time.time() - t0), **RENDER), indent=2))
    print(f"saved {out}", flush=True)


if __name__ == "__main__":
    main()
