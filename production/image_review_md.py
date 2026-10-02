#!/usr/bin/env python3
"""Write stories/<slug>/IMAGE_REVIEW.md: a yes/no keep
column per image file (all revisions), plus a Mermaid diagram of the shot order and framing.

    python3 production/image_review_md.py --story lion_and_mouse_v4

Rerun after each revision. Answers typed into the Keep column are kept (matched by file
name), so the file can be edited by hand between runs.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FRAMING = {  # docs/creation-rules.md CR-15
    "dialogue_close_up": ("close-up, blurred bg", "closeup"),
    "close_two_shot": ("close two-shot", "two"),
    "scene_wide": ("wide scene", "wide"),
    "empty_plate": ("plate only", "plate"),
}


def previous_decisions(path):
    """{file stem: keep} from an earlier IMAGE_REVIEW.md."""
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            hit = re.match(r"\| \[`([^`]+)\.png`\]\([^)]*\) \| *([^|]*?) *\|$", line)
            if hit:
                out[hit.group(1)] = hit.group(2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", default="lion_and_mouse_v4")
    args = ap.parse_args()
    story = REPO / "stories" / args.story
    m = json.loads((story / "prompt_manifest.json").read_text())
    images = {r["id"]: r for r in m["images"]}
    out = story / "IMAGE_REVIEW.md"
    old = previous_decisions(out)

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
    for n, (a, b) in enumerate(zip(shots, shots[1:] + [None]), 1):
        fr = FRAMING[images[a["start_image"]].get("framing", "scene_wide")][0]
        L.append(f'| {n} | `{a["id"]}` → {"`" + b["id"] + "`" if b else "end"} | {fr} |')

    # Every v4 image file in git, all revisions: file name (linked) and a yes/no keep column.
    files = sorted(set(subprocess.run(
        ["git", "ls-files", "character/characters/*/v4/*.png", "character/characters/*/v4/**/*.png",
         "character/locations/v4/**/*.png"], cwd=REPO, capture_output=True, text=True).stdout.split()))
    up = "../" * len(story.relative_to(REPO).parts)
    L += ["", "## Keep or not", "",
          f"All {len(files)} image files of this version, every revision. Write `yes` or `no` in **Keep**.", "",
          "| Image file | Keep |", "|---|---|"]
    for f in files:
        L.append(f"| [`{Path(f).name}`]({up}{f}) | {old.get(Path(f).stem, '')} |")
    out.write_text("\n".join(L) + "\n")
    print(out.relative_to(REPO), len(shots), "shots")


if __name__ == "__main__":
    main()
