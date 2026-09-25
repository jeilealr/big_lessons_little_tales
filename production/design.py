#!/usr/bin/env python3
"""Design a story's characters and locations as still images.

Wan 2.2 T2V is used as an *image* generator (a 1-frame video). That way every
design is drawn by the same model, in the same look, that will later animate
it, so nothing gets lost in translation between an image model and the video
model.

  candidates  N stills per character (model-sheet pose on a plain felt
              backdrop, easy to cut out) and per location (empty plate)
  sheet       contact sheet per entity, to choose from
  pick        record the chosen candidate as the entity's canonical still
  reframe     crop the canonical around a small character and upscale it, so the
              character fills the frame (for pose shots and LoRA training)

Outputs: work/stories/<slug>/design/<entity>/cand_<seed>.png (+ .json sidecar)
         work/stories/<slug>/design/<entity>/canonical.png   after `pick`
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import paths, wan  # noqa: E402

RENDER = dict(width=1280, height=720, steps=40, guidance=4.0, guidance_2=3.0)

# A model-sheet photo: one character, plain backdrop, whole body, neutral pose.
# The plain backdrop matters: it makes the later cut-out clean.
CHARACTER_SHOT = (
    "A character model photograph of {sheet}. {pose} The character is alone on a "
    "plain cream felt floor in front of a plain pale sage-green felt backdrop, the "
    "whole body in frame, centred, eye level, soft even studio lighting. {style}."
)
LOCATION_SHOT = (
    "An empty handmade miniature set with no animals and no characters: {sheet}. "
    "Wide shot at eye level, the centre of the frame left open as a stage. {style}."
)
POSES = {
    "leo": "He stands calmly on all four paws in a three-quarter view, head turned "
           "slightly toward the camera, with a gentle friendly expression.",
    "milo": "He stands upright on his hind legs in a three-quarter view, tiny paws in "
            "front of his chest, with a cheerful curious expression.",
    "butterfly": "It rests on a small felt flower with its wings open.",
}


def load_story(slug: str) -> dict:
    import yaml

    story = yaml.safe_load((paths.REPO / "stories" / slug / "story.yaml").read_text())
    story["_design"] = paths.WORK / "stories" / slug / "design"
    return story


def prompt_for(story: dict, entity: str) -> tuple[str, str]:
    if entity in story["characters"]:
        c = story["characters"][entity]
        prompt = CHARACTER_SHOT.format(sheet=c["sheet"], pose=POSES.get(entity, ""),
                                       style=story["style"])
        negative = story["negative"] + ", busy background, scenery, other animals"
    else:
        loc = story["locations"][entity]
        prompt = LOCATION_SHOT.format(sheet=loc["sheet"], style=story["style"])
        negative = story["negative"] + ", animals, characters, lion, mouse, creature"
    return prompt, negative


def frame_to_uint8(frames):
    import numpy as np

    arr = np.asarray(frames[0] if isinstance(frames, list) else frames)
    if arr.ndim == 4:                 # (F, H, W, 3)
        arr = arr[0]
    if arr.dtype != np.uint8:
        arr = (np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8)
    return arr


def candidates(story: dict, entities: list[str], n: int, seed0: int) -> None:
    from PIL import Image

    pipe = wan.load("t2v", 1)
    print("model loaded", flush=True)
    for entity in entities:
        prompt, negative = prompt_for(story, entity)
        out_dir = story["_design"] / entity
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"[{entity}] {prompt[:120]}...", flush=True)
        for k in range(n):
            seed = seed0 + k
            out = out_dir / f"cand_{seed}.png"
            if out.is_file():
                continue
            t0 = time.time()
            try:
                frames = wan.generate(pipe, prompt, negative=negative, frames=1, seed=seed,
                                      **RENDER)
                used = 1
            except Exception as err:      # defensive: fall back to a short clip
                print(f"  1-frame generation failed ({type(err).__name__}: {err}); "
                      f"falling back to 5 frames", flush=True)
                frames = wan.generate(pipe, prompt, negative=negative, frames=5, seed=seed,
                                      **RENDER)
                used = 5
            Image.fromarray(frame_to_uint8(frames)).save(out)
            out.with_suffix(".json").write_text(json.dumps(dict(
                stage="design", entity=entity, model=wan.MODELS["t2v"], seed=seed,
                frames_generated=used, prompt=prompt, negative=negative,
                seconds=round(time.time() - t0, 1), **RENDER), indent=2))
            print(f"  saved {out.name} ({time.time() - t0:.0f} s)", flush=True)
        sheet(story, entity)


def sheet(story: dict, entity: str) -> None:
    import cv2
    import numpy as np
    from PIL import Image

    out_dir = story["_design"] / entity
    tiles = []
    for p in sorted(out_dir.glob("cand_*.png")):
        t = cv2.resize(np.asarray(Image.open(p).convert("RGB")), (480, 270)).copy()
        cv2.rectangle(t, (0, 0), (480, 28), (0, 0, 0), -1)
        cv2.putText(t, p.stem, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                    cv2.LINE_AA)
        tiles.append(t)
    if not tiles:
        return
    cols = 3
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.concatenate(tiles[i:i + cols], 1) for i in range(0, len(tiles), cols)]
    Image.fromarray(np.concatenate(rows, 0)).save(out_dir / "contact_sheet.png")
    print(f"  contact sheet -> {out_dir / 'contact_sheet.png'}", flush=True)


def pick(story: dict, entity: str, seed: int) -> None:
    import shutil

    d = story["_design"] / entity
    shutil.copy(d / f"cand_{seed}.png", d / "canonical.png")
    info = json.loads((d / f"cand_{seed}.json").read_text())
    info.update(stage="canonical", picked_from=f"cand_{seed}.png",
                picked=time.strftime("%Y-%m-%d %H:%M:%S"))
    (d / "canonical.json").write_text(json.dumps(info, indent=2))
    print(f"{entity}: canonical = cand_{seed}.png")


def reframe(story: dict, entity: str, fill: float = 0.62) -> None:
    """Crop the picked candidate around the character, 16:9, subject at `fill`
    of the frame height, then Real-ESRGAN it back up to 1280x720.

    Uses the BiRefNet matte for the subject box (production/keyframe.py). If the
    padded crop would be larger than the image, it shrinks to fit instead of
    running off the edge, and the result is checked: the character must be
    inside it and fill a sensible share of the frame.
    """
    import numpy as np
    import torch
    from PIL import Image

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from keyframe import subject_bbox
    from twc import post

    d = story["_design"] / entity
    info = json.loads((d / "canonical.json").read_text())
    src = d / info["picked_from"]
    img = np.asarray(Image.open(src).convert("RGB"))
    H, W = img.shape[:2]
    x, y, w, h = subject_bbox(img)
    ch = min(float(H), h / fill)
    cw = ch * 16 / 9
    if cw > W:
        cw, ch = float(W), W * 9 / 16
    cw, ch = int(cw), int(ch)
    cx, cy = x + w / 2, y + h / 2
    x0 = int(np.clip(cx - cw / 2, 0, W - cw))
    y0 = int(np.clip(cy - ch / 2, 0, H - ch))
    assert x0 >= 0 and y0 >= 0 and x0 + cw <= W and y0 + ch <= H, "crop outside the image"
    assert x >= x0 and y >= y0 and x + w <= x0 + cw and y + h <= y0 + ch, \
        f"character {x, y, w, h} not inside crop {x0, y0, cw, ch}"
    crop = img[y0:y0 + ch, x0:x0 + cw]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    up = post.upscale(crop[None], 1280, 720, device)[0]
    bx, by, bw, bh = subject_bbox(up)
    share = bh / up.shape[0]
    assert 0.3 < share < 0.95, f"after reframing the character fills {share:.0%} of the height"
    Image.fromarray(crop).save(d / "canonical_crop_raw.png")
    Image.fromarray(up).save(d / "canonical.png")
    info.update(stage="canonical", reframed=dict(
        crop_xywh=[x0, y0, cw, ch], subject_box=[x, y, w, h], subject_share=round(share, 2),
        how=f"16:9 crop, subject ~{fill:.0%} of height, Real-ESRGAN x4 -> 1280x720"))
    (d / "canonical.json").write_text(json.dumps(info, indent=2))
    print(f"{entity}: reframed {src.name}, crop {x0},{y0} {cw}x{ch}; "
          f"character now fills {share:.0%} of the frame height")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["candidates", "sheet", "pick", "reframe", "prompt"])
    ap.add_argument("--story", default="lion_and_mouse")
    ap.add_argument("--entities", nargs="+", help="characters and/or locations (default: all)")
    ap.add_argument("-n", type=int, default=6, help="candidates per entity")
    ap.add_argument("--seed", type=int, default=1000)
    args = ap.parse_args()
    story = load_story(args.story)
    entities = args.entities or [*story["characters"], *story["locations"]]
    unknown = [e for e in entities if e not in story["characters"] and e not in story["locations"]]
    if unknown:
        raise SystemExit(f"unknown entities: {unknown}")
    if args.stage == "prompt":
        for e in entities:
            p, neg = prompt_for(story, e)
            print(f"== {e}\n{p}\nNEGATIVE: {neg}\n")
    elif args.stage == "candidates":
        candidates(story, entities, args.n, args.seed)
    elif args.stage == "sheet":
        for e in entities:
            sheet(story, e)
    elif args.stage == "reframe":
        for e in entities:
            reframe(story, e)
    else:
        if len(entities) != 1:
            raise SystemExit("pick one entity: --entities leo --seed 1003")
        pick(story, entities[0], args.seed)


if __name__ == "__main__":
    main()
