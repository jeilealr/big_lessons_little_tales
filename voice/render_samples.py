#!/usr/bin/env python3
"""Render the sample lines (sample_lines.yaml) for every saved voice.

  source voice/gemini_env.sh
  python voice/render_samples.py [--langs es fr de ru uk] [--only narrators/moonlight_storyteller_1]

For each line, each voice folder its `speakers:` entry covers (`narrators`
= every folder in narrators/, or a single folder such as `cast/leo`) and each
language (default: `languages:` in the yaml), writes <folder>/<line>[_<lang>].wav
+ .json with speak.py. Files that exist are skipped (delete one to redo it).
Calls are MIN_GAP s apart (speak.py: the rate limit); the run stops at the
first failed call (rerun to continue).
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

import yaml

from speak import MIN_GAP

HERE = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--langs", nargs="+")
    ap.add_argument("--only", nargs="+", help="voice folders relative to voice/")
    args = ap.parse_args()
    cfg = yaml.safe_load((HERE / "sample_lines.yaml").read_text())
    langs = args.langs or cfg["languages"]
    made = skipped = 0
    for name, line in cfg["lines"].items():
        if missing := [lang for lang in langs if lang not in line]:
            sys.exit(f"{name} has no text for {missing} in sample_lines.yaml")
        folders = []
        for sp in line["speakers"]:
            folders += sorted(p for p in (HERE / sp).iterdir() if p.is_dir()) if sp == "narrators" \
                else [HERE / sp]
        for folder in folders:
            rel = str(folder.relative_to(HERE))
            if args.only and rel not in args.only:
                continue
            voice = yaml.safe_load((folder / "voice.yaml").read_text())["voice_id"]
            for lang in langs:
                out = folder / (f"{name}.wav" if lang == "en" else f"{name}_{lang}.wav")
                if out.is_file():
                    skipped += 1
                    continue
                if made:
                    time.sleep(MIN_GAP)
                r = subprocess.run([sys.executable, str(HERE / "speak.py"), "--voice", voice,
                                    "--text", line[lang], "--out", str(out)])
                if r.returncode:
                    sys.exit(f"stopped: speak.py failed for {out.relative_to(HERE)} "
                             f"(made {made}, skipped {skipped} existing)")
                made += 1
    print(f"made {made}, skipped {skipped} existing")


if __name__ == "__main__":
    main()
