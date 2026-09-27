#!/usr/bin/env python3
"""Render a story's narration from its script and the cast's canonical voices.

  TWC_ENV=tts lumi/run_in_container.sh python voice/narrate.py --story lion_and_mouse_v2 --lang en

Reads stories/<slug>/narration/<lang>.yaml (one entry per spoken line, with
its speaker) and voice/cast/<speaker>/reference.wav, and writes

  <channel>/audio/<slug>/<lang>/lines/sNN_KK_<speaker>.wav   every line alone
  <channel>/audio/<slug>/<lang>/sceneNN.wav                  each scene, lines joined
  <channel>/audio/<slug>/<lang>/timing.json                  seconds per line/scene

The scene files are what production/animatic.py (--lang) lays under the
pictures, so every scene takes its narration's real length. Lines are the
units to move around in DaVinci. Existing lines are kept (delete to redo).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import paths  # noqa: E402
import voices  # noqa: E402

DEFAULT_PAUSE = 0.35      # seconds after a line, unless the script says otherwise


def main() -> None:
    import soundfile as sf
    import yaml

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v2")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--scenes", nargs="+", type=int)
    args = ap.parse_args()

    script = yaml.safe_load((paths.REPO / "stories" / args.story / "narration" /
                             f"{args.lang}.yaml").read_text())
    cfg = voices.load_cfg()
    settings = cfg["chatterbox"]
    speakers = {l["speaker"] for lines in script["scenes"].values() for l in lines}
    missing = [s for s in speakers if not (voices.CAST / s / "reference.wav").is_file()]
    if missing:
        raise SystemExit(f"no canonical voice for {missing}: run voices.py design/audition/pick")
    out = paths.AUDIO / args.story / args.lang
    (out / "lines").mkdir(parents=True, exist_ok=True)
    model = voices.load_chatterbox()
    sr = model.sr
    timing = {}
    for n in sorted(script["scenes"]):
        if args.scenes and n not in args.scenes:
            continue
        parts, rows = [], []
        for k, line in enumerate(script["scenes"][n]):
            f = out / "lines" / f"s{n:02d}_{k:02d}_{line['speaker']}.wav"
            if f.is_file():
                wav, _ = sf.read(str(f), dtype="float32")
            else:
                voice = yaml.safe_load((voices.CAST / line["speaker"] / "voice.yaml").read_text())
                wav = voices.speak(model, line["text"], args.lang,
                                   voices.CAST / line["speaker"] / "reference.wav",
                                   {**settings, **voice.get("settings", {})},
                                   settings["seed"] + 100 * n + k)
                voices.save_wav(f, wav, sr, stage="narration", story=args.story,
                                lang=args.lang, scene=n, index=k, **line)
            pause = float(line.get("pause_after", DEFAULT_PAUSE))
            parts += [wav, np.zeros(int(pause * sr), np.float32)]
            rows.append(dict(speaker=line["speaker"], seconds=round(len(wav) / sr, 2),
                             pause=pause, text=line["text"]))
        scene = np.concatenate(parts)
        sf.write(str(out / f"scene{n:02d}.wav"), scene, sr)
        timing[n] = dict(seconds=round(len(scene) / sr, 2), lines=rows)
        print(f"scene {n:2d}: {len(scene) / sr:5.1f} s  ({len(rows)} lines)", flush=True)
    (out / "timing.json").write_text(json.dumps(timing, indent=2))
    total = sum(t["seconds"] for t in timing.values())
    print(f"total {total:.1f} s -> {out}")


if __name__ == "__main__":
    main()
