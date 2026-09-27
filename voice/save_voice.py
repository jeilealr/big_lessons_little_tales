#!/usr/bin/env python3
"""Record a Gemini designed voice in the repo so its id and design are never lost.

  source voice/gemini_env.sh
  python voice/save_voice.py --id voice_zdbgqrcerxqu --dir cast/leo --role leo

Writes voice/<dir>/voice.yaml (id, name, model, the exact design
prompt, expiry) and google_sample.wav: the sample Google stores with the
voice (voices.get), so no new audio is generated. Existing notes in the
yaml (`notes:`) are kept.
"""
import argparse
import base64
import io
import sys
import wave
from pathlib import Path

import yaml
from google import genai

HERE = Path(__file__).resolve().parent


def to_wav(data: bytes, mime: str) -> bytes:
    if data[:4] == b"RIFF":
        return data
    rate = 24000
    for part in (mime or "").split(";"):
        if part.strip().lower().startswith("rate="):
            rate = int(part.split("=", 1)[1])
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(data)
    return buf.getvalue()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True)
    ap.add_argument("--dir", required=True, help="relative to voice/, e.g. cast/leo")
    ap.add_argument("--role", required=True)
    ap.add_argument("--note", default="")
    args = ap.parse_args()
    client = genai.Client()             # keep a reference: an unreferenced client closes itself
    v = client.voices.get(args.id).model_dump()
    out = HERE / args.dir
    out.mkdir(parents=True, exist_ok=True)
    sample = v.get("sample_audio") or {}
    if sample.get("data"):
        data = sample["data"]
        data = base64.b64decode(data) if isinstance(data, str) else data
        (out / "google_sample.wav").write_bytes(to_wav(data, sample.get("mime_type", "")))
    old = {}
    if (out / "voice.yaml").is_file():
        old = yaml.safe_load((out / "voice.yaml").read_text()) or {}
    rec = dict(
        role=args.role,
        provider="Gemini 3.8 Flash TTS (Gemini API)",
        voice_id=v["id"],
        display_name=v.get("display_name"),
        type=v.get("type"),
        model=v.get("model"),
        expires=str(v.get("expire_time")),
        prompt=(v.get("prompted") or {}).get("input"),
        google_sample="google_sample.wav" if sample.get("data") else None,
        notes=old.get("notes") or args.note or None,
    )
    for k in ("sample", "licence", "language"):
        if k in old:
            rec[k] = old[k]
    (out / "voice.yaml").write_text(
        "# Gemini designed voice. Google deletes it at `expires`: recreate it from\n"
        "# `prompt` with the same model before then, compare with the samples,\n"
        "# and update voice_id.\n" + yaml.safe_dump(rec, sort_keys=False, allow_unicode=True, width=80))
    print(f"{args.role}: {v['id']} {v.get('display_name')} -> {out}")


if __name__ == "__main__":
    if not __import__("os").environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set: source voice/gemini_env.sh")
    main()
