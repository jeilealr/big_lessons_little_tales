#!/usr/bin/env python3
"""Render a story's narration with the Gemini voices: one WAV per scene.

  source voice/gemini_env.sh
  python voice/narrate_scenes.py --lines stories/lion_and_mouse_v4/dialogue_coverage.json \\
      --story lion_and_mouse_v4 --lang en [--scenes 1 2] [--redo]

Input: a JSON with `lines`: [{id, scene, speaker, performance_direction, text}]
(the v4 dialogue_coverage.json format). Each line is spoken by its speaker's
voice (`--voices`, default narrator/lion/mouse -> the saved voices in voice/),
with its performance direction as Gemini's style note, then the lines of a
scene are joined with short pauses.

Output (git-ignored), under work/stories/<story>/audio/<lang>/:
  sceneNN.wav       one file per scene (for the animatic and the edit)
  lines/<ID>.wav    every line alone (+ .json: text, voice, style, seconds)
  timing.json       seconds per line and per scene
Existing line files are reused (delete one, or --redo, to re-render it).
The API key comes from GEMINI_API_KEY (never printed or written).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import signal
import sys
import time
import wave
from pathlib import Path

import yaml
from google import genai

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from speak import audio_bytes, to_wav  # noqa: E402
from bllt import paths  # noqa: E402

MODEL = "gemini-3.8-flash-tts"
VOICES = {"NARRATOR": "narrators/moonlight_storyteller_1", "LION": "cast/leo", "MOUSE": "cast/milo"}
PAUSE_SAME = 0.45      # seconds between two lines of the same speaker
PAUSE_CHANGE = 0.70    # seconds when the speaker changes
TAIL = 1.0             # silence at the end of each scene
MIN_GAP = 8.0          # seconds between calls: Tier 1 allows 10 requests/min, 10K tokens/min
                       # and 100 requests/day for this model (AI Studio > Rate limits)
_last_call = [0.0]


def speak(client, voice: str, text: str, style: str) -> tuple[bytes, int]:
    """One line -> (PCM16 mono frames, sample rate). Retries on rate limits."""
    content = {"type": "text", "text": text}
    if style:
        content["annotations"] = [{"type": "speech_metadata", "style": style}]
    def _timeout(*_):
        raise TimeoutError("no answer in 90 s")

    signal.signal(signal.SIGALRM, _timeout)
    for attempt in range(2):                       # every retry counts toward the 100/day
        try:
            time.sleep(max(0.0, _last_call[0] + MIN_GAP - time.time()))
            _last_call[0] = time.time()
            signal.alarm(90)                       # hard limit: a call once hung for an hour
            inter = client.interactions.create(
                model=MODEL, input=[{"type": "user_input", "content": [content]}],
                response_format={"type": "audio"},
                generation_config={"speech_config": [{"voice": voice}]},
                timeout=120)
            signal.alarm(0)
            data, mime = audio_bytes(inter)
            with wave.open(io.BytesIO(to_wav(data, mime))) as w:
                assert w.getnchannels() == 1 and w.getsampwidth() == 2
                return w.readframes(w.getnframes()), w.getframerate()
        except Exception as e:                     # rate limit / timeout / transient error
            signal.alarm(0)
            wait = 20 * (attempt + 1)
            print(f"    retry in {wait} s ({type(e).__name__}: {str(e)[:120]})", flush=True)
            time.sleep(wait)
    raise SystemExit(f"giving up on: {text[:60]}")


def write_wav(path: Path, frames: bytes, rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(frames)


def read_wav(path: Path) -> tuple[bytes, int]:
    with wave.open(str(path)) as w:
        return w.readframes(w.getnframes()), w.getframerate()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lines", type=Path, required=True)
    ap.add_argument("--story", required=True)
    ap.add_argument("--lang", default="en")
    ap.add_argument("--scenes", nargs="+", type=int)
    ap.add_argument("--voices", nargs="+", default=[],
                    help="SPEAKER=folder overrides, e.g. NARRATOR=narrators/golden_hour_storyteller_3")
    ap.add_argument("--redo", action="store_true")
    args = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set: source voice/gemini_env.sh")

    voices = {**VOICES, **dict(v.split("=", 1) for v in args.voices)}
    ids = {sp: yaml.safe_load((HERE / f / "voice.yaml").read_text())["voice_id"] for sp, f in voices.items()}
    lines = json.loads((paths.REPO / args.lines if not args.lines.is_absolute() else args.lines).read_text())["lines"]
    out = paths.story_audio(args.story, args.lang)
    client = genai.Client()

    timing = json.loads((out / "timing.json").read_text()) if (out / "timing.json").is_file() else {}
    for scene in sorted({l["scene"] for l in lines}):
        if args.scenes and scene not in args.scenes:
            continue
        chunks, rate, rows, prev = [], None, [], None
        for l in [x for x in lines if x["scene"] == scene]:
            f = out / "lines" / f"{l['id']}.wav"
            if f.is_file() and not args.redo:
                pcm, r = read_wav(f)
            else:
                t0 = time.time()
                pcm, r = speak(client, ids[l["speaker"]], l["text"], l.get("performance_direction", ""))
                write_wav(f, pcm, r)
                f.with_suffix(".json").write_text(json.dumps(dict(
                    id=l["id"], scene=scene, speaker=l["speaker"], voice=ids[l["speaker"]],
                    voice_folder=voices[l["speaker"]], model=MODEL, text=l["text"],
                    style=l.get("performance_direction", ""), lang=args.lang,
                    seconds=round(len(pcm) / 2 / r, 2), render_seconds=round(time.time() - t0, 1)), indent=2))
                print(f"  {l['id']} {l['speaker']:8s} {len(pcm) / 2 / r:5.1f} s", flush=True)
            if rate and r != rate:
                raise SystemExit(f"sample rate changed ({rate} -> {r}) in {l['id']}")
            rate = r
            if prev is not None:
                gap = PAUSE_SAME if prev == l["speaker"] else PAUSE_CHANGE
                chunks.append(b"\0\0" * int(gap * rate))
            chunks.append(pcm); prev = l["speaker"]
            rows.append(dict(id=l["id"], speaker=l["speaker"], seconds=round(len(pcm) / 2 / rate, 2)))
        chunks.append(b"\0\0" * int(TAIL * rate))
        pcm = b"".join(chunks)
        write_wav(out / f"scene{scene:02d}.wav", pcm, rate)
        timing[str(scene)] = dict(seconds=round(len(pcm) / 2 / rate, 2), lines=rows)
        (out / "timing.json").write_text(json.dumps(timing, indent=2))
        print(f"scene {scene:2d}: {len(pcm) / 2 / rate:6.1f} s ({len(rows)} lines) -> {out / f'scene{scene:02d}.wav'}", flush=True)
    total = sum(v["seconds"] for v in timing.values())
    print(f"total {total / 60:.1f} min in {len(timing)} scenes")


if __name__ == "__main__":
    main()
