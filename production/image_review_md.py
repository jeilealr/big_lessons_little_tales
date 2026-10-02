#!/usr/bin/env python3
"""Write stories/<slug>/IMAGE_REVIEW.md: a Mermaid diagram of the shot order and
framing, then a yes/no Keep column per image file (all revisions).

    python3 production/image_review_md.py --story lion_and_mouse_v4 [--force]

Inputs: stories/<slug>/prompt_manifest.json (shots in scene order; each shot's
framing is its start image's `framing`, docs/creation-rules.md CR-15) and the
image files on disk under character/characters/*/v4/ and character/locations/v4/
(Gemini candidate folders excluded). Files on disk, not `git ls-files`: new
takes are reviewed before the owner commits them, and agents run no git.

Rerun after each revision. Answers typed into the Keep column are kept (matched
by file path), so the file can be edited by hand between runs. If the existing
file holds answers in a layout this script cannot carry over, it stops instead
of overwriting them; --force overwrites.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths  # noqa: E402

REPO = paths.REPO
IMAGES = ("character/characters/*/v4/**/*.png", "character/locations/v4/**/*.png")
FRAMING = {  # docs/creation-rules.md CR-15
    "dialogue_close_up": ("close-up, blurred bg", "closeup"),
    "close_two_shot": ("close two-shot", "two"),
    "scene_wide": ("wide scene", "wide"),
    "empty_plate": ("plate only", "plate"),
}
# One row of the Keep table: | [`name.png`](link) | answer |
KEEP_ROW = re.compile(r"\| \[`[^`]+\.png`\]\(([^)]*)\) \| *(.*?) *\|\s*$")
ANSWER_COLUMNS = {"Keep", "Owner notes"}


def previous_decisions(path):
    """({link: keep} from an earlier IMAGE_REVIEW.md, [first cell of every other
    table row that holds an answer this script cannot carry over])."""
    keep, lost, header = {}, [], None
    if not path.exists():
        return keep, lost
    for line in path.read_text(encoding="utf-8").splitlines():
        hit = KEEP_ROW.match(line)
        if hit:
            keep[hit.group(1)] = hit.group(2)
            continue
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if ANSWER_COLUMNS & set(cells):
            header = cells
        elif header and len(cells) == len(header) and not re.fullmatch(r"[|\-: ]+", line.strip()):
            if any(cells[i] for i, name in enumerate(header) if name in ANSWER_COLUMNS):
                lost.append(cells[0])
    return keep, lost


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v4")
    ap.add_argument("--force", action="store_true",
                    help="overwrite even if the old file holds answers this script cannot keep")
    args = ap.parse_args()
    story = paths.STORIES / args.story
    m = json.loads((story / "prompt_manifest.json").read_text(encoding="utf-8"))
    images = {r["id"]: r for r in m["images"]}
    out = story / "IMAGE_REVIEW.md"
    old, lost = previous_decisions(out)
    if lost and not args.force:
        sys.exit(f"{out.relative_to(REPO)} has answers in a layout this script does not write "
                 f"({len(lost)} rows, e.g. {', '.join(lost[:3])}); copy them elsewhere first, "
                 f"or rerun with --force to overwrite them")

    shots = sorted(m["shots"], key=lambda s: (s["scene"], s["order"]))
    L = [f"# {args.story}: image review", "",
         "Every image of this version, generated from `prompt_manifest.json` by "
         "`python3 production/image_review_md.py`. Mark each file `yes` or `no` in "
         "the last table; rerunning the script keeps your answers. "
         "Framing follows `docs/creation-rules.md` CR-15.", "",
         "## Shot order and framing", "",
         "```mermaid", "flowchart LR"]
    for sc in sorted({s["scene"] for s in shots}):
        L.append(f'  subgraph S{sc:02d}["Scene {sc}"]')
        L.append("    direction LR")
        for s in [s for s in shots if s["scene"] == sc]:
            fr = images[s["start_image"]].get("framing", "scene_wide")
            L.append(f'    {s["id"]}["{s["id"]}<br/>{FRAMING[fr][0]}"]:::{FRAMING[fr][1]}')
        L.append("  end")
    for a, b in zip(shots, shots[1:]):
        L.append(f'  {a["id"]} --> {b["id"]}')
    L += ["  classDef closeup fill:#ffe0b2,stroke:#e65100,color:#000",
          "  classDef two fill:#fff9c4,stroke:#f9a825,color:#000",
          "  classDef wide fill:#c8e6c9,stroke:#2e7d32,color:#000",
          "  classDef plate fill:#e0e0e0,stroke:#616161,color:#000",
          "```", "",
          "Orange = character close-up with blurred background; yellow = close two-shot; "
          "green = wide scene with whole bodies; grey = background only.", "",
          "| # | From → to | Framing |", "|---|---|---|"]
    for n, (a, b) in enumerate(zip(shots, [*shots[1:], None]), 1):
        fr = FRAMING[images[a["start_image"]].get("framing", "scene_wide")][0]
        L.append(f'| {n} | `{a["id"]}` → {"`" + b["id"] + "`" if b else "end"} | {fr} |')

    # Every v4 image file, all revisions: file name (linked) and a yes/no keep column.
    files = sorted({p.relative_to(REPO).as_posix() for pattern in IMAGES for p in REPO.glob(pattern)
                    if "gemini" not in p.parts})
    if not files:
        sys.exit("no v4 image files found: nothing written")
    up = "../" * len(story.relative_to(REPO).parts)
    L += ["", "## Keep or not", "",
          f"All {len(files)} image files of this version, every revision. Write `yes` or `no` in **Keep**.", "",
          "| Image file | Keep |", "|---|---|"]
    for f in files:
        L.append(f"| [`{Path(f).name}`]({up}{f}) | {old.get(up + f, '')} |")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out.relative_to(REPO), len(shots), "shots,", len(files), "image files")


if __name__ == "__main__":
    main()
