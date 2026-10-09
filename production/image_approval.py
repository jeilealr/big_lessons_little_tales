"""Shared hash for the image specification an owner reviewed and approved."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SPEC_FIELDS = (
    "group", "revision", "bible_revision", "target", "canvas", "purpose", "label",
    "prompt_kind", "counts", "ordered_references", "setup", "framing", "frame",
    "prompt_template", "allowed_delta", "protected", "acceptance",
)


def spec_sha256(record: dict) -> str:
    payload = {key: record.get(key) for key in SPEC_FIELDS}
    payload["rendered_prompt"] = record.get("positive_prompt")
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def reference_files(record: dict, repo: Path) -> list[dict]:
    """Hash every attached reference in exact prompt order; missing inputs cannot be approved."""
    refs = []
    for ref in record.get("ordered_references", []):
        path = repo / ref["path"]
        if not path.is_file():
            raise FileNotFoundError(f"reference {ref.get('id')} is missing: {path}")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        refs.append({"id": ref["id"], "path": ref["path"], "sha256": digest.hexdigest()})
    return refs
