"""Hash-checked lookup for post-render lip-synced chained takes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import paths


def entry_for(story: str, piece: str) -> dict | None:
    index = paths.story_work(story) / "lipsync" / "lipsync_manifest.json"
    if not index.is_file():
        return None
    try:
        return json.loads(index.read_text(encoding="utf-8")).get("pieces", {}).get(piece)
    except (OSError, json.JSONDecodeError):
        return None



def recipe_sha256(story: str, piece: str) -> str | None:
    """Fingerprint the current timing, speaker assignment and approved mouth anchors."""
    story_dir = paths.STORIES / story
    try:
        plan_path = story_dir / "timing_plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        row = next(r for r in plan["segments"] if r["piece"] == piece)
        if row.get("mode") != "mouth":
            return None
        manifest_path = story_dir / "prompt_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        shot = next(s for s in manifest["shots"] if s["id"] == piece)
        variant = next(v for v in shot["variants"] if v["id"] == row["variant"])
        audio_dir = paths.story_audio(plan.get("audio_story", story), plan.get("lang", "en"))
        word_path = audio_dir / "word_timings.json"
        words = json.loads(word_path.read_text(encoding="utf-8"))
        images = {r["id"]: r for r in manifest["images"]}
        image_ids = {variant.get("start_image", shot["start_image"]),
                     variant.get("end_image", shot["end_image"]), variant.get("mouth_open_image")}
        files = [plan_path, manifest_path, story_dir / "visual_bible.json",
                 story_dir / "dialogue_coverage.json", audio_dir / "timing.json", word_path]
        files.extend(paths.REPO / images[i]["target"] for i in image_ids if i)
        files.extend(Path(words["lines"][lid]["audio_file"]) for lid in row["lines"])
        digest = hashlib.sha256()
        for path in files:
            digest.update(str(path.resolve()).encode("utf-8"))
            digest.update(b"\0")
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
        return digest.hexdigest()
    except (OSError, KeyError, StopIteration, TypeError, ValueError, json.JSONDecodeError):
        return None


def resolve_synced_take(story: str, piece: str, source: Path) -> Path | None:
    """Return a lipsynced take only when it was made from this unchanged source clip."""
    entry = entry_for(story, piece)
    current_recipe = recipe_sha256(story, piece)
    if not entry or current_recipe is None or entry.get("recipe_sha256") != current_recipe:
        return None
    try:
        source = source.resolve()
        output = Path(entry["output_file"]).resolve()
        source_stat, out_stat = source.stat(), output.stat()
    except (KeyError, OSError):
        return None
    if (str(source) != entry.get("source_file") or source_stat.st_size != entry.get("source_size")
            or source_stat.st_mtime_ns != entry.get("source_mtime_ns")
            or out_stat.st_size != entry.get("output_size")
            or out_stat.st_mtime_ns != entry.get("output_mtime_ns")):
        return None
    # Stat checks cheaply reject stale entries; digests bind the handoff to exact media.
    for path, field in ((source, "source_sha256"), (output, "output_sha256")):
        digest = hashlib.sha256()
        try:
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
        except OSError:
            return None
        if digest.hexdigest() != entry.get(field):
            return None
    return output
