#!/usr/bin/env python3
"""Record a reproducible continuation repair for a bad chained join (CR-21).

Use after the owner has chosen a take for both pieces and chain_preview flags the join:
  python3 production/chain_repair.py --story lion_and_mouse_v6 \\
      --piece s01_to_stone --previous-piece s01_explores

The command records the exact chosen source MP4 and its SHA-256 in
stories/<story>/repair_overrides.json. Re-export runtime to create a distinct repair candidate;
render that candidate with production/shot.py. The original keyframe and render stay untouched.
Point the repaired piece at the new MP4 in takes.yaml, then rerun chain_preview --require-takes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import paths  # noqa: E402
from chain_preview import find_take  # noqa: E402


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", required=True)
    ap.add_argument("--piece", required=True, help="later piece to repair")
    ap.add_argument("--previous-piece", required=True, help="immediately preceding piece with the chosen take")
    args = ap.parse_args()
    sd = paths.STORIES / args.story
    manifest = json.loads((sd / "prompt_manifest.json").read_text())
    plan = json.loads((sd / "timing_plan.json").read_text())
    rows = {r["piece"]: r for r in plan["segments"]}
    pieces = {s["id"]: s for s in manifest["shots"]}
    if args.piece not in rows or args.previous_piece not in rows:
        raise SystemExit("both piece IDs must exist in timing_plan.json")
    target, previous = pieces[args.piece], pieces[args.previous_piece]
    ordered = sorted(manifest["shots"], key=lambda s: s["order"])
    idx = next((i for i, p in enumerate(ordered) if p["id"] == args.piece), -1)
    if idx < 1 or ordered[idx - 1]["id"] != args.previous_piece:
        raise SystemExit(f"{args.previous_piece} is not immediately before {args.piece}")
    if target.get("join_in") != "chain" or target.get("start_image") != previous.get("end_image"):
        raise SystemExit("repair target is not a chained handoff from the preceding piece")
    import yaml as _yaml
    takes_path = sd / "takes.yaml"
    takes = (_yaml.safe_load(takes_path.read_text()) or {}) if takes_path.is_file() else {}
    source, how = find_take(args.story, rows[args.previous_piece], takes, None)
    if source is None:
        raise SystemExit(f"no owner-chosen take for {args.previous_piece}: {how}; select it in takes.yaml first")
    source = source.resolve()
    try:
        source_ref = str(source.relative_to(paths.WORK))
    except ValueError:
        source_ref = str(source)
    doc_path = sd / "repair_overrides.json"
    doc = json.loads(doc_path.read_text()) if doc_path.is_file() else {"schema": 1, "repairs": {}}
    revisions = doc.setdefault("repairs", {}).setdefault(args.piece, [])
    revision = max((int(x["revision"]) for x in revisions), default=0) + 1
    entry = {"revision": revision, "source_piece": args.previous_piece,
             "source_story": (rows[args.previous_piece].get("reuse") or {}).get("story", args.story),
             "source_file": source_ref, "sha256": hash_file(source), "frame": -1}
    revisions.append(entry)
    doc_path.write_text(json.dumps(doc, indent=2) + "\n")
    print(f"recorded repair{revision:02d} for {args.piece} from {source} ({how})")
    print(f"next: python3 production/export_runtime.py --manifest stories/{args.story}/prompt_manifest.json --story {args.story}")


if __name__ == "__main__":
    main()
