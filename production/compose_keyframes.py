#!/usr/bin/env python3
"""Compose every keyframe recipe of a story (start `compose:` and end
`end_compose:` of each shot) so they can be looked at before rendering.

  python production/compose_keyframes.py --story lion_and_mouse_v3 [--redo]

Seconds per keyframe on a GPU node (BiRefNet matting), minutes on the login
node. Writes work/stories/<slug>/keyframes/*.png and a contact sheet
keyframes/contact_sheet.jpg (start and end side by side, one row per shot).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths  # noqa: E402


def main() -> None:
    import yaml
    from PIL import Image, ImageDraw

    from keyframe import compose

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v3")
    ap.add_argument("--redo", action="store_true")
    args = ap.parse_args()
    story = yaml.safe_load((paths.STORIES / args.story / "story.yaml").read_text())
    work = paths.story_work(args.story)
    rows = []
    for n in sorted(story["scenes"]):
        for s in story["scenes"][n].get("shots", []):
            if s.get("superseded_by") or s.get("variant_of"):
                continue
            pair = []
            for key, rec in ((s["keyframe"], s.get("compose")), (s.get("end_keyframe"), s.get("end_compose"))):
                if not key:
                    continue
                out = work / key
                if rec and (args.redo or not out.is_file()):
                    compose(work / rec["plate"], [{**c, "still": str(work / c["still"])} for c in rec["characters"]],
                            out, rec.get("crop"), rec.get("blur", 0.0))
                    print(f"composed {key}", flush=True)
                pair.append(out)
            rows.append((s["name"], pair))
    w, h = 480, 270
    sheet = Image.new("RGB", (2 * w, len(rows) * (h + 20)), "white")
    for k, (name, pair) in enumerate(rows):
        ImageDraw.Draw(sheet).text((4, k * (h + 20) + 4), name, fill="black")
        for j, f in enumerate(pair):
            im = Image.open(f).convert("RGB").resize((w, h))
            sheet.paste(im, (j * w, k * (h + 20) + 20))
    out = work / "keyframes" / "contact_sheet.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=80)
    print(f"{len(rows)} shots -> {out}")


if __name__ == "__main__":
    main()
