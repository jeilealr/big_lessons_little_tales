#!/usr/bin/env python3
"""Render a story's narration with the Gemini voices: one WAV per scene.

  source voice/gemini_env.sh
  python voice/narrate_scenes.py --lines stories/lion_and_mouse_v5/dialogue_coverage.json \\
      --story lion_and_mouse_v5 --lang en [--scenes 1 2] [--redo]

Input: a JSON with `lines`: [{id, scene, speaker, performance_direction, text}]
(the v4 dialogue_coverage.json format; a relative path is taken from the repo
root). The text is spoken as written: `--lang` only names the output folder,
so another language needs its own translated lines file. Each line is spoken
by its speaker's voice (`--voices-file` and `--voices`, default
narrator/lion/mouse -> the saved voices in voice/), with its performance
direction as Gemini's style note, then the lines of a scene are joined with
short pauses.

A speaker can have several voices (a chorus, e.g. three ducklings): each voice
speaks the line into its own file, lines/<ID>_v1.wav, _v2, ... (for layering in
the edit), and the scene file carries their mix, as long as the longest take.
  --voices-file stories/<story>/voices.yaml   SPEAKER: folder, or a list of folders
  --voices SPEAKER=folder[,folder...]          overrides, after the file

Output (git-ignored), under work/stories/<story>/audio/<lang>/:
  sceneNN.wav       one file per scene (for the animatic and the edit)
  lines/<ID>.wav    every line alone (+ .json: text, voice, style, seconds)
  timing.json       seconds per line and per scene
Existing line files are reused (delete one, or --redo, to re-render it).

Rate limits (voice/README.md): one call every MIN_GAP s, at most two attempts
per line (every attempt counts toward the 100 requests/day; past that limit a
call hangs, so each is cut at CALL_LIMIT s), and the run stops when a line
fails twice. A rerun continues where it stopped.
The API key comes from GEMINI_API_KEY (never printed or written).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
import wave
from pathlib import Path

import yaml
from google import genai

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from speak import MIN_GAP, MODEL, synthesize, to_wav  # noqa: E402
from feltwillow import paths  # noqa: E402

VOICES = {"NARRATOR": "narrators/moonlight_storyteller_1", "LION": "cast/leo", "MOUSE": "cast/milo"}
PAUSE_SAME = 0.45      # seconds between two lines of the same speaker
PAUSE_CHANGE = 0.70    # seconds when the speaker changes (production/timing_sheet.py repeats both)
TAIL = 1.0             # silence at the end of each scene
_last_call = [0.0]


def speak(client, voice: str, text: str, style: str) -> tuple[bytes, int]:
    """One line -> (PCM16 mono frames, sample rate), in at most two attempts."""
    for attempt in (1, 2):
        time.sleep(max(0.0, _last_call[0] + MIN_GAP - time.time()))
        _last_call[0] = time.time()
        try:
            data, mime = synthesize(client, voice, text, style, MODEL)
            with wave.open(io.BytesIO(to_wav(data, mime))) as w:
                if (w.getnchannels(), w.getsampwidth()) != (1, 2):
                    raise ValueError(f"expected 16-bit mono, got {w.getnchannels()} channel(s), "
                                     f"{8 * w.getsampwidth()} bit")
                return w.readframes(w.getnframes()), w.getframerate()
        except Exception as e:                     # rate limit / timeout / no audio / transient error
            print(f"    attempt {attempt}/2 failed ({type(e).__name__}: {str(e)[:120]})", flush=True)
            if attempt == 1:
                time.sleep(20)
    raise SystemExit(f"giving up on: {text[:60]}")


def write_wav(path: Path, frames: bytes, rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames)


def mix(takes: list[bytes]) -> bytes:
    """Several PCM16 takes of one line, started together: their sum scaled by
    1/sqrt(n) (about the loudness of one voice), clipped; as long as the longest."""
    import array
    arrs = [array.array("h", t) for t in takes]
    n, g = max(len(a) for a in arrs), 1 / len(arrs) ** 0.5
    out = array.array("h", bytes(2 * n))
    for i in range(n):
        v = sum(a[i] for a in arrs if i < len(a)) * g
        out[i] = max(-32768, min(32767, int(v)))
    return out.tobytes()


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
    ap.add_argument("--voices-file", type=Path,
                    help="YAML SPEAKER: folder (or list of folders, relative to voice/)")
    ap.add_argument("--voices", nargs="+", default=[],
                    help="SPEAKER=folder[,folder...] overrides, e.g. NARRATOR=narrators/golden_hour_storyteller_3")
    ap.add_argument("--redo", action="store_true")
    args = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set: source voice/gemini_env.sh")

    if bad := [v for v in args.voices if "=" not in v]:
        sys.exit(f"--voices takes SPEAKER=folder, got {bad}")
    voices = dict(VOICES)
    if args.voices_file:
        vf = args.voices_file if args.voices_file.is_absolute() else paths.REPO / args.voices_file
        voices.update(yaml.safe_load(vf.read_text())["voices"])
    voices.update({k: v.split(",") for k, v in (x.split("=", 1) for x in args.voices)})
    voices = {sp: [f] if isinstance(f, str) else list(f) for sp, f in voices.items()}
    ids = {sp: [yaml.safe_load((HERE / f / "voice.yaml").read_text())["voice_id"] for f in fs]
           for sp, fs in voices.items()}
    lines = json.loads((args.lines if args.lines.is_absolute() else paths.REPO / args.lines).read_text())["lines"]
    todo = [line for line in lines if not args.scenes or line["scene"] in args.scenes]
    # checked before the first call, so a missing voice does not waste the daily quota
    if missing := sorted({line["speaker"] for line in todo} - ids.keys()):
        sys.exit(f"no voice for speaker(s) {missing}: add --voices SPEAKER=folder")
    out = paths.story_audio(args.story, args.lang)
    client = genai.Client()             # keep a reference: an unreferenced client closes itself

    timing = json.loads((out / "timing.json").read_text()) if (out / "timing.json").is_file() else {}
    for scene in sorted({line["scene"] for line in todo}):
        chunks, rate, rows, prev = [], None, [], None
        for line in [x for x in todo if x["scene"] == scene]:
            takes = []
            for k, (vid, folder) in enumerate(zip(ids[line["speaker"]], voices[line["speaker"]])):
                suffix = f"_v{k + 1}" if len(ids[line["speaker"]]) > 1 else ""
                f = out / "lines" / f"{line['id']}{suffix}.wav"
                if f.is_file() and not args.redo:
                    takes.append(read_wav(f))
                    continue
                t0 = time.time()
                style = line.get("performance_direction", "")
                pcm, r = speak(client, vid, line["text"], style)
                write_wav(f, pcm, r)
                f.with_suffix(".json").write_text(json.dumps(dict(
                    id=line["id"], scene=scene, speaker=line["speaker"], voice=vid,
                    voice_folder=folder, model=MODEL, text=line["text"],
                    style=style, lang=args.lang,
                    seconds=round(len(pcm) / 2 / r, 2), render_seconds=round(time.time() - t0, 1)), indent=2))
                print(f"  {line['id']}{suffix} {line['speaker']:9s} {len(pcm) / 2 / r:5.1f} s", flush=True)
                takes.append((pcm, r))
            if len({r for _, r in takes}) > 1:
                raise SystemExit(f"sample rates differ between the voices of {line['id']}")
            pcm, r = takes[0] if len(takes) == 1 else (mix([p for p, _ in takes]), takes[0][1])
            if rate and r != rate:
                raise SystemExit(f"sample rate changed ({rate} -> {r}) in {line['id']}")
            rate = r
            if prev is not None:
                gap = PAUSE_SAME if prev == line["speaker"] else PAUSE_CHANGE
                chunks.append(b"\0\0" * int(gap * rate))
            chunks.append(pcm)
            prev = line["speaker"]
            rows.append(dict(id=line["id"], speaker=line["speaker"], seconds=round(len(pcm) / 2 / rate, 2)))
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
