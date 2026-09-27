#!/usr/bin/env python3
"""Speak one line with a Gemini 3.8 Flash TTS voice and save it as a WAV.

  source voice/gemini_env.sh
  python voice/speak.py --voice voice_g00mo8cbdefq \
      --text "Once upon a time..." --out work/voices/test.wav \
      [--style "warm bedtime storytelling"] [--model gemini-3.8-flash-tts]

Writes the WAV plus a .json sidecar (voice, model, text, style, seconds).
The API key comes from GEMINI_API_KEY (never printed or written).
"""
import argparse
import base64
import io
import json
import os
import sys
import wave
from pathlib import Path

from google import genai


def audio_bytes(interaction) -> tuple[bytes, str]:
    """Find the audio payload in an Interaction, whatever its exact shape."""
    def walk(o, depth=0):
        if depth > 8 or o is None:
            return
        if isinstance(o, dict):
            items = o.items()
        elif hasattr(o, "model_dump"):
            items = o.model_dump().items()
        elif isinstance(o, (list, tuple)):
            for x in o:
                yield from walk(x, depth + 1)
            return
        else:
            return
        d = dict(items)
        if d.get("data") and ("mime_type" in d or "mimeType" in d or d.get("type") == "audio"):
            yield d
        for v in d.values():
            yield from walk(v, depth + 1)
    for d in walk(interaction):
        data = d["data"]
        if isinstance(data, str):
            data = base64.b64decode(data)
        return data, d.get("mime_type") or d.get("mimeType") or ""
    raise SystemExit("no audio in the response")


def to_wav(data: bytes, mime: str) -> bytes:
    if data[:4] == b"RIFF":
        return data
    rate = 24000
    for part in mime.split(";"):
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
    ap.add_argument("--voice", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--style", default="")
    ap.add_argument("--model", default="gemini-3.8-flash-tts")
    args = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set: source voice/gemini_env.sh")
    client = genai.Client()
    content = {"type": "text", "text": args.text}
    if args.style:
        content["annotations"] = [{"type": "speech_metadata", "style": args.style}]
    inter = client.interactions.create(
        model=args.model,
        input=[{"type": "user_input", "content": [content]}],
        response_format={"type": "audio"},
        generation_config={"speech_config": [{"voice": args.voice}]},
    )
    data, mime = audio_bytes(inter)
    wav = to_wav(data, mime)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(wav)
    with wave.open(str(args.out)) as w:
        secs = w.getnframes() / w.getframerate()
    args.out.with_suffix(".json").write_text(json.dumps(dict(
        model=args.model, voice=args.voice, text=args.text, style=args.style,
        mime=mime, seconds=round(secs, 2)), indent=2))
    print(f"{args.out} ({secs:.1f} s, {mime})")


if __name__ == "__main__":
    main()
