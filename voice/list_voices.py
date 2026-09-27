#!/usr/bin/env python3
"""List the Gemini TTS voices available to this API key and save the list.

  source voice/gemini_env.sh
  python voice/list_voices.py

Prints every voice (id, display name, type) and writes voices_list.json next
to this script, so the owner can see which voices exist and pick by id.
The API key is read from GEMINI_API_KEY (never printed or written).
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from google import genai

if not os.environ.get("GEMINI_API_KEY"):
    sys.exit("GEMINI_API_KEY is not set: source voice/gemini_env.sh")
client = genai.Client()
rows = []
resp = client.voices.list()
voices = getattr(resp, "voices", None)
if voices is None:            # some versions return an iterable/pager
    voices = list(resp)
for v in voices or []:
    rows.append({k: getattr(v, k, None) for k in ("id", "display_name", "type", "language_code", "gender")})
rows = [{k: (str(x) if x is not None and not isinstance(x, (str, int, float, list)) else x)
         for k, x in r.items()} for r in rows]
for r in rows:
    print(f"{r['id']:40s} {str(r['display_name']):40s} {r['type']}")
out = Path(__file__).with_name("voices_list.json")
out.write_text(json.dumps({"listed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                           "voices": rows}, indent=2))
print(f"{len(rows)} voices -> {out}")
