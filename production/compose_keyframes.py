#!/usr/bin/env python3
"""Compose every keyframe recipe of a story (start `compose:` and end
`end_compose:` of each shot) so they can be looked at before rendering.

  python production/compose_keyframes.py --story lion_and_mouse_v3 [--redo]

Reads stories/<slug>/story.yaml (shots with `superseded_by` or `variant_of`
are skipped). Seconds per keyframe on a GPU node (BiRefNet matting), minutes on
the login node. Writes work/stories/<slug>/keyframes/*.png (missing ones, or
all with --redo) and a contact sheet keyframes/contact_sheet.jpg: start and
end side by side, one row per shot; a keyframe that does not exist yet (no
recipe, e.g. a `continue_from` frame taken from a render) is marked missing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v3")
    ap.add_argument("--redo", action="store_true")
    args = ap.parse_args()

    import yaml
    from PIL import Image, ImageDraw

    from keyframe import compose_recipe            # cv2, BiRefNet

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
                    compose_recipe(work, rec, out)
                    print(f"composed {key}", flush=True)
                pair.append(out)
            rows.append((s["name"], pair))
    w, h = 480, 270
    sheet = Image.new("RGB", (2 * w, len(rows) * (h + 20)), "white")
    draw = ImageDraw.Draw(sheet)
    missing = 0
    for k, (name, pair) in enumerate(rows):
        draw.text((4, k * (h + 20) + 4), name, fill="black")
        for j, f in enumerate(pair):
            x, y = j * w, k * (h + 20) + 20
            if f.is_file():
                with Image.open(f) as im:
                    sheet.paste(im.convert("RGB").resize((w, h)), (x, y))
            else:
                missing += 1
                draw.text((x + 8, y + h // 2), f"missing: {f.name}", fill="red")
    out = work / "keyframes" / "contact_sheet.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=80)
    print(f"{len(rows)} shots -> {out}" + (f" ({missing} keyframes missing)" if missing else ""))


if __name__ == "__main__":
    main()
