#!/usr/bin/env python3
"""Install an owner-made character pack (v2 style: canonical + views +
expressions + actions, made outside this repo) into a story's work folder.

  python production/install_pack.py --story lion_and_mouse_v2

For every character in story.yaml with a `canonical:` path:
  * design/<name>/canonical.png   the canonical, PADDED to 16:9 with its own
    studio colour and resized to 1280x720. Wan renders 16:9 and wan.fit()
    centre-crops, which would cut off a square canonical's mane or feet.
  * characters/<name>/pack/*.png  every view, expression and action image,
    unchanged except for the file name (".png.png" -> ".png").
  * characters/<name>/pack/manifest.json  source path and size of each file.
  * characters/<name>/pack16x9/  full-body views/actions padded to 16:9 like
    the canonical, as start images for pose clips.

The originals under character/characters/ are never modified.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths  # noqa: E402


def pad_16x9(img, size=(1280, 720)):
    """Extend the canvas sideways by repeating the edge columns, blurred, so the
    studio backdrop continues without a visible seam; then resize."""
    import cv2
    from PIL import Image

    a = np.asarray(img.convert("RGB"))
    h, w = a.shape[:2]
    tw = max(w, round(h * 16 / 9))
    left = (tw - w) // 2
    out = cv2.copyMakeBorder(a, 0, 0, left, tw - w - left, cv2.BORDER_REPLICATE)
    soft = cv2.GaussianBlur(out, (0, 0), sigmaX=25)
    ramp = np.zeros(tw, np.float32)                       # 0 inside the original, 1 in the padding
    ramp[:left] = 1
    ramp[left + w:] = 1
    ramp = cv2.GaussianBlur(ramp[None], (0, 0), sigmaX=12)[0][None, :, None]
    blend = (out * (1 - ramp) + soft * ramp).astype(np.uint8)
    colour = tuple(int(v) for v in np.median(a[:, 0], axis=0))
    return Image.fromarray(blend).resize(size, Image.LANCZOS), colour


def main() -> None:
    import yaml
    from PIL import Image

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v2")
    args = ap.parse_args()
    story = yaml.safe_load((paths.REPO / "stories" / args.story / "story.yaml").read_text())
    work = paths.WORK / "stories" / args.story
    for name, ch in story["characters"].items():
        if not ch.get("canonical"):
            continue
        src = paths.REPO / ch["canonical"]
        out = work / "design" / name / "canonical.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        img, colour = pad_16x9(Image.open(src))
        img.save(out)
        out.with_suffix(".json").write_text(json.dumps(dict(
            stage="canonical", source=str(src), how="owner-made; padded to 16:9 by repeating "
            f"the edge columns (blurred; edge colour ~{colour}), resized to 1280x720"), indent=2))
        pack_dir = work / "characters" / name / "pack"
        pack_dir.mkdir(parents=True, exist_ok=True)
        manifest = {}
        for sub in ("canonical", "views", "expressions", "actions"):
            for f in sorted((src.parent.parent / sub).glob("*.png")):
                clean = f.name.replace(".png.png", ".png")
                dst = pack_dir / f"{sub}__{clean}"
                if not dst.is_file():
                    dst.write_bytes(f.read_bytes())
                manifest[dst.name] = dict(source=str(f), size=Image.open(f).size)
        (pack_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
        # 16:9 padded copies of the full-body images, for pose clips that start
        # from a view or action instead of the canonical (wan.fit would crop them).
        pad_dir = work / "characters" / name / "pack16x9"
        pad_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(pack_dir.glob("*.png")):
            if f.name.startswith(("views__", "actions__")) and "face" not in f.name:
                dst = pad_dir / f.name
                if not dst.is_file():
                    pad_16x9(Image.open(f))[0].save(dst)
        print(f"{name}: canonical -> {out} (pad colour {colour}); {len(manifest)} pack images")


if __name__ == "__main__":
    main()
