"""Where things live. Everything else derives from these."""

from __future__ import annotations

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# The channel folder holds the inputs that are not code: reference stills,
# the soundtrack, finished videos. By default it is the repo's parent.
CHANNEL = Path(os.environ.get("THE_WEBTOONS_CORNER_ROOT", REPO.parent)).resolve()
REFERENCE = CHANNEL / "Intro" / "reference_img"
AUDIO = CHANNEL / "audio"
OUTPUT = CHANNEL / "Intro"
# Generated intermediates (clips, keyframes, datasets). Git-ignored.
WORK = REPO / "work"
