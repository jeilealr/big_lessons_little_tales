#!/usr/bin/env python3
"""Write stories/<slug>/IMAGE_REVIEW.md: every manifest image as a thumbnail table with an
owner decision column, plus a Mermaid diagram of the shot order and framing.

    python3 production/image_review_md.py --story lion_and_mouse_v4

Rerun after each revision. Decisions typed into the Keep and Owner notes columns are kept
(matched by record id), so the file can be edited by hand between runs.
"""
import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FRAMING = {  # docs/creation-rules.md CR-15
    "dialogue_close_up": ("close-up, blurred bg", "closeup"),
    "close_two_shot": ("close two-shot", "two"),
    "scene_wide": ("wide scene", "wide"),
    "empty_plate": ("plate only", "plate"),
}
MODEL = {None: "GPT image_gen", "gemini-3.1-flash-image": "Nano Banana 2",
         "gemini-3.1-flash-lite-image": "NB2 Lite", "gemini-3-pro-image": "Nano Banana Pro"}


def previous_decisions(path):
    """{record id: (keep, notes)} from an earlier IMAGE_REVIEW.md."""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        cells = [c.strip() for c in line.split("|")]
        ids = re.findall(r"`([A-Za-z0-9_]+)`", line)
        if len(cells) > 3 and ids:
            out[ids[0]] = (cells[-3], cells[-2])
    return out


def thumb(rec, story_dir, width=220):
    rel = Path("../" * len(story_dir.relative_to(REPO).parts)) / rec["target"]
    return f'<img src="{rel.as_posix()}" width="{width}">'


def model_of(rec):
    res = rec.get("result") or {}
    return MODEL.get(res.get("model") if "gemini" in str(res.get("tool", "")) else None,
                     res.get("model") or "GPT image_gen")


def status(rec):
    rv = (rec.get("result") or {}).get("review") or {}
    rv = rv.get("status", "") if isinstance(rv, dict) else str(rv)
    return f'{rec.get("revision")} · {"pending review" if "pending" in rv else rec.get("status")}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", default="lion_and_mouse_v4")
    args = ap.parse_args()
    story = REPO / "stories" / args.story
    m = json.loads((story / "prompt_manifest.json").read_text())
    images = {r["id"]: r for r in m["images"]}
    out = story / "IMAGE_REVIEW.md"
    old = previous_decisions(out)

    def keep(i):
        return old.get(i, ("", ""))

    shots = sorted(m["shots"], key=lambda s: (s["scene"], s["order"]))
    L = [f"# {args.story}: image review", "",
         "Every image of this version, generated from `prompt_manifest.json` by "
         "`python3 production/image_review_md.py`. Fill in **Keep**: `keep`, `redo` "
         "or `drop`, and add notes; rerunning the script keeps your entries. "
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

    L += ["", "## Scene keyframes (start and end of each shot)", "",
          "| Shot | Start | End | Framing | Revision · status | Model | Keep | Owner notes |",
          "|---|---|---|---|---|---|---|---|"]
    for s in shots:
        a, b = images[s["start_image"]], images[s["end_image"]]
        k, note = keep(s["id"])
        fr = FRAMING[a.get("framing", "scene_wide")][0]
        L.append(f'| `{s["id"]}` | {thumb(a, story)} | {thumb(b, story)} | {fr} | '
                 f'{status(a)} / {status(b)} | {model_of(a)} / {model_of(b)} | {k} | {note} |')

    for title, group in [("Character references, plates and props", "foundation"),
                         ("Expression references", "expressions")]:
        L += ["", f"## {title}", "", "| Record | Image | Purpose | Revision · status | Model | Keep | Owner notes |",
              "|---|---|---|---|---|---|---|"]
        for r in [r for r in m["images"] if r["group"] == group]:
            k, note = keep(r["id"])
            L.append(f'| `{r["id"]}` | {thumb(r, story, 160)} | {r.get("purpose", "")[:90]} | '
                     f'{status(r)} | {model_of(r)} | {k} | {note} |')
    out.write_text("\n".join(L) + "\n")
    print(out.relative_to(REPO), len(shots), "shots")


if __name__ == "__main__":
    main()
