#!/usr/bin/env python3
"""Download the Wan 2.2 A14B diffusers weights into the Hugging Face cache ($HF_HOME).

  lumi/run_in_container.sh python lumi/download_wan.py          # I2V: shots, poses
  lumi/run_in_container.sh python lumi/download_wan.py t2v      # T2V: design stills
  lumi/run_in_container.sh python lumi/download_wan.py i2v t2v

Run on a login node (network). Repos and pinned revisions come from bllt/wan.py,
so the download always matches what the pipeline loads offline.
"""
import sys
from pathlib import Path

from huggingface_hub import snapshot_download

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt.wan import MODELS, REVISIONS  # noqa: E402

kinds = sys.argv[1:] or ["i2v"]
if unknown := [k for k in kinds if k not in MODELS]:
    sys.exit(f"unknown model {unknown}; choose from {sorted(MODELS)}")
for kind in kinds:
    p = snapshot_download(MODELS[kind], revision=REVISIONS[kind],
                          allow_patterns=["*.json", "*.txt", "*.model", "*.safetensors", "*.py"],
                          max_workers=8)
    print("->", p, flush=True)
print("DOWNLOAD DONE")
