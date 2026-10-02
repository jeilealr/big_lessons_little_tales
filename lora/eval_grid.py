#!/usr/bin/env python3
"""Assemble a LoRA evaluation grid: one row per checkpoint, one column per prompt.

  lumi/run_in_container.sh python lora/eval_grid.py fox base 500 1000 final

Reads work/lora/<name>/eval/<checkpoint>/*.png (from lora/eval_character.sh, in
prompt order) and the prompts in lora/datasets/<name>.yaml; writes eval/grid.png.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
import yaml
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths  # noqa: E402

if len(sys.argv) < 3:
    sys.exit(__doc__)
name, rows = sys.argv[1], sys.argv[2:]
cfg = yaml.safe_load((paths.REPO / "lora" / "datasets" / f"{name}.yaml").read_text())
cols = [p.split(",")[0] + " / " + p.split(",")[-1].strip()[:26] for p in cfg["eval"]["prompts"]]
D = paths.WORK / "lora" / name / "eval"
tw, th = 384, 218
grid = []
header = np.full((30, 120 + tw * len(cols), 3), 20, np.uint8)
for i, c in enumerate(cols):
    cv2.putText(header, c[:44], (124 + i * tw, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
grid.append(header)
for r in rows:
    files = sorted((D / r).glob("*.png"))
    label = np.full((th, 120, 3), 20, np.uint8)
    text = {"base": "no LoRA", "final": "final"}.get(r, f"step {r}")
    cv2.putText(label, text, (8, th // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    tiles = [cv2.resize(np.asarray(Image.open(f).convert("RGB")), (tw, th)) for f in files[:len(cols)]]
    while len(tiles) < len(cols):
        tiles.append(np.zeros((th, tw, 3), np.uint8))
    grid.append(np.concatenate([label] + tiles, 1))
out = D / "grid.png"
Image.fromarray(np.concatenate(grid, 0)).save(out)
print(out)
