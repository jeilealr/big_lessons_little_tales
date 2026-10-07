# Provenance: what was changed, and where

Short answer: **no third-party repository was modified.** All our work is new
code, and it now lives in this repo. There is nothing to push to any fork.

## Not modified

| Component | How it is used | State |
|---|---|---|
| **Wan 2.2** (Alibaba) | Never cloned. Used through the `diffusers` Python package (`WanImageToVideoPipeline`, `WanPipeline`) with the official weights from Hugging Face (`Wan-AI/Wan2.2-I2V-A14B-Diffusers`, `Wan-AI/Wan2.2-T2V-A14B-Diffusers`). | unmodified |
| **diffusers** 0.39.0 | pip package | unmodified |
| **RIFE** (Megvii, via `TensorForger/RIFE-safetensors`) | Architecture file and weights downloaded from Hugging Face at run time. `feltwillow/post.py` sets two of its module globals (`device`, `dtype`) after import; the file itself is not edited. | unmodified |
| **Real-ESRGAN** x4plus (`Comfy-Org/Real-ESRGAN_repackaged`) | weights loaded through `spandrel` | unmodified |
| LUMI PyTorch container | `lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif`, read-only | unmodified |

## What was added, and where it lives now

All pipeline code is new and lives in this repo. Two pieces were carried over
from the earlier channel work (The Webtoons Corner intro, done with
LTX-Video) and kept because the fable pipeline uses them:

| Was | Now |
|---|---|
| `LTX-Video/video_post.py` | `feltwillow/post.py` (RIFE, Real-ESRGAN, grade) |
| the ffmpeg helpers inside `generate_intro_v3.py` | `feltwillow/media.py` |
| `ltx_env/*.sbatch`, `run_in_container.sh`, download scripts | `lumi/` |

The intro, LTX, felt-test and synthesised-music code was removed on
2026-09-27 when the repo became *Big Lessons, Little Tales* (renamed *Feltwillow* on 2026-10-07); it remains in the
git history before that date. The Chatterbox/Parler voice experiments were
removed at the same time (voices now come from Gemini TTS, `voice/`).
