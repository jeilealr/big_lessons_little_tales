#!/usr/bin/env bash
# Separate CPU word-aligner environment. Do not change the Wan/ROCm renderer venv.
set -euo pipefail
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ENV_DIR=${FELTWILLOW_LIPSYNC_ENV:-"$REPO_ROOT/.venv-lipsync"}
python3 -m venv "$ENV_DIR"
PY="$ENV_DIR/bin/python"
"$PY" -m pip install --upgrade pip
# Install the CPU PyTorch wheels explicitly so the AMD LUMI login node does not
# pull NVIDIA CUDA libraries into this unrelated, CPU-only alignment environment.
"$PY" -m pip install --index-url https://download.pytorch.org/whl/cpu \
  'torch==2.8.0' 'torchaudio==2.8.0' 'torchvision==0.23.0'
"$PY" -m pip install -r "$REPO_ROOT/voice/requirements-lipsync.txt"
FFMPEG=$("$PY" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')
ln -sf "$FFMPEG" "$ENV_DIR/bin/ffmpeg"
"$PY" -c 'import torch, torchaudio, whisperx, imageio_ffmpeg; print("WhisperX", __import__("importlib.metadata", fromlist=["version"]).version("whisperx"), "torch", torch.__version__, "CPU", not torch.cuda.is_available(), "ffmpeg", imageio_ffmpeg.get_ffmpeg_exe())'
