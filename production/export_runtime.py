#!/usr/bin/env python3
"""Export a runtime story.yaml for production/shot.py from a prompt manifest and
an owner-made image set.

  python3 production/export_runtime.py --manifest stories/lion_and_mouse_v5/prompt_manifest.json \\
      --images lion_and_mouse_v5 --story lion_and_mouse_v5
  python3 production/export_runtime.py --manifest stories/ugly_duckling_v1/prompt_manifest.json \\
      --story ugly_duckling_v1 --scenes 1 2 3 4 5 6 7 8 9

One runtime shot per video variant of the manifest (name = variant id, e.g.
`s03_two_paths_closed_r01`), with
  keyframe / end_keyframe  copies of the image set's files for the variant's
                           start/end records (highest `_rNN` revision on disk),
                           frozen in work/stories/<story>/keyframes/ so that
                           moving or replacing source images cannot change a run
  prompt / negative        the variant's reviewed runtime prompts, verbatim
  frames, size, seeds      from the variant
Without --images each record's `target` in the manifest is its file. With
--images the record -> file map comes from the image set's READMEs
(character/characters/<set>/{Leo,Milo,interactions}/README.md and
character/locations/<set>/README.md). Also writes stories/<story>/runtime_inputs.json: every
endpoint file with its sha256, so a later change of an image is visible.
Variants without seeds get 1 2 3; without size, 1280x720. --scenes limits the
export to scenes whose images exist (the others are listed as skipped).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths  # noqa: E402


def image_map(image_set: str) -> dict[str, Path]:
    """Record id -> newest file of that record in the image set."""
    roots = [paths.REPO / "character/characters" / image_set / n for n in ("Leo", "Milo", "interactions")]
    roots.append(paths.REPO / "character/locations" / image_set)
    out = {}
    for root in roots:
        folder = None
        for line in (root / "README.md").read_text().splitlines():
            m = re.match(r"## `(.+?)/?`", line)
            if m:
                folder = paths.REPO / m.group(1)
                continue
            m = re.match(r"\| `([^`]+)_r01\.png` \| `([^`]+)`", line)
            if m and folder:
                # exact stem only: `l_side_r01.png` must not pick up `l_side_r_r01.png`
                rev = re.compile(rf"{re.escape(m.group(1))}_r(\d+)\.png")
                found = sorted((int(r.group(1)), f) for f in folder.glob("*.png")
                               if (r := rev.fullmatch(f.name)))
                if found:
                    out[m.group(2)] = found[-1][1]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--images", help="image set with README file lists (story folder under character/), "
                    "e.g. lion_and_mouse_v5; default: the manifest's record targets")
    ap.add_argument("--story", required=True)
    ap.add_argument("--scenes", nargs="+", type=int)
    args = ap.parse_args()
    man = json.loads((paths.REPO / args.manifest).read_text())
    if args.images:
        files = image_map(args.images)
    else:
        files = {i["id"]: paths.REPO / i["target"] for i in man["images"]
                 if i.get("target") and (paths.REPO / i["target"]).is_file()}
    work = paths.story_work(args.story)
    scenes, inputs, missing = {}, {}, []
    for s in sorted(man["shots"], key=lambda s: (s["scene"], s["order"])):
        if args.scenes and s["scene"] not in args.scenes:
            continue
        for v in s["variants"]:
            ends = {}
            for key in ("start_image", "end_image"):
                f = files.get(v[key])
                if f is None:
                    missing.append(f"{v['id']}: {v[key]}")
                    continue
                frozen = work / "keyframes" / f.name
                frozen.parent.mkdir(parents=True, exist_ok=True)
                if not frozen.is_file() or frozen.read_bytes() != f.read_bytes():
                    shutil.copy2(f, frozen)
                ends[key] = f"keyframes/{f.name}"
                inputs[v[key]] = dict(file=str(f.relative_to(paths.REPO)), frozen=ends[key],
                                      sha256=hashlib.sha256(f.read_bytes()).hexdigest())
            if len(ends) < 2:
                continue
            scenes.setdefault(s["scene"], {"shots": []})["shots"].append(dict(
                name=v["id"], shot=s["id"], mode=v["mode"], speaker=v.get("speaker"),
                dialogue_line_ids=v.get("dialogue_line_ids", []),
                keyframe=ends["start_image"], end_keyframe=ends["end_image"],
                prompt=v["positive_prompt"], negative=v.get("negative_prompt", ""),
                frames=v["frames"], size=v.get("size") or [1280, 720], seeds=v.get("seeds") or [1, 2, 3]))
    if missing:
        sys.exit("missing images:\n  " + "\n  ".join(missing))
    sd = paths.STORIES / args.story
    sd.mkdir(parents=True, exist_ok=True)
    story = dict(
        title=man.get("title") or args.story, slug=args.story,
        source=dict(manifest=str(args.manifest), manifest_revision=man.get("revision"),
                    images=args.images or "manifest targets", scenes=args.scenes or "all"),
        note="Generated by production/export_runtime.py; do not edit by hand. "
             "Each shot carries its full prompt (shot.py uses `prompt:` verbatim).",
        negative="", style="", scenes=scenes)
    (sd / "story.yaml").write_text(yaml.safe_dump(story, sort_keys=False, width=100, allow_unicode=True))
    (sd / "runtime_inputs.json").write_text(json.dumps(inputs, indent=2, sort_keys=True))
    n = sum(len(sc["shots"]) for sc in scenes.values())
    print(f"{n} runtime shots in {len(scenes)} scenes -> {sd / 'story.yaml'}")


if __name__ == "__main__":
    main()
