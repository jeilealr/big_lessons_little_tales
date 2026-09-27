"""Where things live. Everything else derives from these.

The repo can sit anywhere: every path is derived from this file's location.
Only machine-specific locations (venvs, model cache, container) live in
lumi/site.sh, and they do not depend on the repo's name.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Generated files (designs, keyframes, shots, audio, LoRAs). Git-ignored.
WORK = Path(os.environ.get("BLLT_WORK", REPO / "work")).resolve()
STORIES = REPO / "stories"          # story bibles (tracked)
VOICE = REPO / "voice"              # Gemini voice tools and saved voices (tracked)
CHARACTERS = REPO / "character" / "characters"   # owner-made character packs


def story_work(slug: str) -> Path:
    """Generated files of one story: design/, characters/, keyframes/, shots/, audio/."""
    return WORK / "stories" / slug


def story_audio(slug: str, lang: str | None = None) -> Path:
    """Narration for a story (one sceneNN.wav per scene), per language."""
    base = story_work(slug) / "audio"
    return base / lang if lang else base
