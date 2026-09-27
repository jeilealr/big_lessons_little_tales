#!/usr/bin/env python3
"""Build a captioned image dataset for a character LoRA (step 3).

Driven by lora/datasets/<name>.yaml: which stills and which clip frames to use,
each with the pose/view it shows. Every caption follows one recipe:

    <trigger>, <identity>, <pose and view>, <framing>, <setting>, <style>

The trigger word carries the identity. Everything that should stay
controllable (pose, view, framing, setting) is written out, so the LoRA does
not absorb it into the character. Medium-shot crops around the subject add
framing variety, which character-LoRA practice asks for alongside angles and
backgrounds.

Output: work/lora/<name>/dataset/*.png + *.txt, and contact_sheet.png.
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import media, paths  # noqa: E402


def subject_box(img: np.ndarray, how: dict) -> tuple[int, int, int, int] | None:
    """Bounding box of the character: the BiRefNet matte, a hue range, or
    'not the plain backdrop'."""
    if how["method"] == "matte":
        sys.path.insert(0, str(paths.REPO / "production"))
        from keyframe import subject_bbox
        return subject_bbox(img)
    if how["method"] == "hue":
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        lo, hi = how["hue"]
        mask = ((hsv[..., 0] >= lo) & (hsv[..., 0] <= hi)
                & (hsv[..., 1] > how.get("min_sat", 110)) & (hsv[..., 2] > 60))
    else:  # plain backdrop: distance from the colours along the image border
        border = np.concatenate([img[:8].reshape(-1, 3), img[-8:].reshape(-1, 3),
                                 img[:, :8].reshape(-1, 3), img[:, -8:].reshape(-1, 3)])
        ref = np.median(border, axis=0)
        mask = np.linalg.norm(img.astype(float) - ref, axis=2) > how.get("threshold", 60)
    mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask)
    if n < 2:
        return None
    k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = stats[k, :4]
    return (int(x), int(y), int(w), int(h)) if w * h > 0.01 * img.shape[0] * img.shape[1] else None


def medium_crop(img: np.ndarray, box, aspect: float = 16 / 9) -> np.ndarray | None:
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    ch = max(h * 1.5, w * 1.5 / aspect)
    cw = ch * aspect
    H, W = img.shape[:2]
    if cw >= W * 0.9:            # the subject already fills the frame; no crop needed
        return None
    x0 = int(np.clip(cx - cw / 2, 0, W - cw)); y0 = int(np.clip(cy - ch / 2, 0, H - ch))
    return img[y0:y0 + int(ch), x0:x0 + int(cw)]


def main() -> None:
    import yaml

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="lora/datasets/<name>.yaml")
    ap.add_argument("--allow-missing", action="store_true",
                    help="skip sources whose files do not exist yet")
    args = ap.parse_args()
    cfg = yaml.safe_load((paths.REPO / "lora" / "datasets" / f"{args.name}.yaml").read_text())
    base = paths.WORK / cfg["workdir"]
    out = paths.WORK / "lora" / cfg["name"] / "dataset"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*"):
        old.unlink()

    def caption(pose: str, framing: str) -> str:
        return ", ".join([cfg["trigger"], cfg["identity"], pose, framing, cfg["setting"], cfg["style"]])

    items, crops, skipped = [], 0, []
    pose_of = {}
    for src in cfg["sources"]:
        if "image" in src:
            files = sorted(glob.glob(str(base / src["image"])))
            frames = [(Path(f).stem, np.asarray(Image.open(f).convert("RGB"))) for f in files]
            if not files:
                skipped.append(src["image"])
        else:
            clip = Path(src["clip"]) if src["clip"].startswith("/") else (
                base / src["clip"])
            if not clip.is_file():
                skipped.append(str(clip)); frames = []
            else:
                all_frames = media.read_frames(clip)
                frames = [(f"{clip.stem}_f{i:02d}", all_frames[min(i, len(all_frames) - 1)])
                          for i in src["frames"]]
        for stem, img in frames:
            Image.fromarray(img).save(out / f"{stem}.png")
            (out / f"{stem}.txt").write_text(caption(src["pose"], "full body"))
            items.append(stem); pose_of[stem] = src["pose"]
            if src.get("crop", cfg.get("crop_every", True)):
                box = subject_box(img, cfg["subject"])
                c = medium_crop(img, box) if box else None
                if c is not None:
                    Image.fromarray(c).save(out / f"{stem}_medium.png")
                    (out / f"{stem}_medium.txt").write_text(caption(src["pose"], "medium shot"))
                    items.append(f"{stem}_medium"); crops += 1
    # Background diversity: cut each full-body still out and composite it into
    # several different location plates. Without this the LoRA memorises the
    # training background (the fox LoRA drew its meadow for a "forest" prompt).
    comp = cfg.get("composite")
    if comp:
        import random

        sys.path.insert(0, str(paths.REPO / "production"))
        from keyframe import place, subject_bbox

        rng = random.Random(comp.get("seed", 7))
        plates = []
        for spec in comp["plates"]:
            for f in sorted(glob.glob(str(paths.WORK / spec["glob"]))):
                plates.append((f, spec["caption"]))
        if not plates:
            raise SystemExit("composite: no plates found")
        full = [st for st in items if not st.endswith("_medium")]
        n_comp = 0
        for stem in full:
            src = np.asarray(Image.open(out / f"{stem}.png").convert("RGB"))
            _, _, _, bh = subject_bbox(src)
            share = bh / src.shape[0]
            pose = pose_of[stem]
            for k in range(comp.get("per_image", 2)):
                plate_path, plate_caption = rng.choice(plates)
                plate = np.asarray(Image.open(plate_path).convert("RGB").resize((src.shape[1], src.shape[0])))
                h = float(np.clip(share * rng.uniform(0.8, 1.1), 0.25, 0.8))
                frame, _ = place(plate.astype(np.float32), src, x=rng.uniform(0.35, 0.65),
                                 y=rng.uniform(0.82, 0.92), height=h, flip=rng.random() < 0.5,
                                 light=0.0)       # never alter identity colours in training data
                name = f"{stem}_comp{k}"
                Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(out / f"{name}.png")
                cap = ", ".join([cfg["trigger"], cfg["identity"], pose, "full body", plate_caption, cfg["style"]])
                (out / f"{name}.txt").write_text(cap)
                items.append(name); n_comp += 1
        print(f"composited {n_comp} images into {len(plates)} plates")

    if skipped and not args.allow_missing:
        raise SystemExit("missing sources:\n  " + "\n  ".join(skipped))

    tiles = []
    for stem in items:
        t = cv2.resize(np.asarray(Image.open(out / f"{stem}.png").convert("RGB")), (240, 135)).copy()
        cv2.putText(t, stem[-18:], (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(t)
    while len(tiles) % 8:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.concatenate(tiles[i:i + 8], 1) for i in range(0, len(tiles), 8)]
    Image.fromarray(np.concatenate(rows, 0)).save(out.parent / "contact_sheet.png")
    (out.parent / "dataset.json").write_text(json.dumps(dict(
        images=len(items), crops=crops, skipped=skipped, config=cfg), indent=2))
    print(f"{cfg['name']}: {len(items)} images ({crops} medium crops) -> {out}")
    if skipped:
        print("skipped (not yet rendered):", *skipped, sep="\n  ")


if __name__ == "__main__":
    main()
