# Provenance: what was changed, and where

Short answer: **no third-party repository was modified.** All our work is new
code, and it now lives in this repo. There is nothing to push to any fork.

## Not modified

| Component | How it is used | State |
|---|---|---|
| **Wan 2.2** (Alibaba) | Never cloned. Used through the `diffusers` Python package (`WanImageToVideoPipeline`, `WanPipeline`) with the official weights from Hugging Face (`Wan-AI/Wan2.2-I2V-A14B-Diffusers`, `Wan-AI/Wan2.2-T2V-A14B-Diffusers`). | unmodified |
| **diffusers** 0.39.0 | pip package | unmodified |
| **LTX-Video** clone (`/scratch/.../jelealro/LTX-Video`) | Upstream `Lightricks/LTX-Video` at commit `4b2d053`. Only used by the legacy LTX intro scripts, through its `ltx_video` package. | no tracked file ever changed; `ltx_video/` never edited |
| **RIFE** (Megvii, via `TensorForger/RIFE-safetensors`) | Architecture file and weights downloaded from Hugging Face at run time. `twc/post.py` sets two of its module globals (`device`, `dtype`) after import; the file itself is not edited. | unmodified |
| **Real-ESRGAN** x4plus (`Comfy-Org/Real-ESRGAN_repackaged`) | weights loaded through `spandrel` | unmodified |
| LUMI PyTorch container | `lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif`, read-only | unmodified |

## What was added, and where it lives now

During the work, our scripts were created *inside* the LTX-Video folder and in
`ltx_env/`. They were all untracked new files. They were moved here:

| Was | Now |
|---|---|
| `LTX-Video/generate_intro_v2.py`, `generate_intro_v3.py` (+ our options) | `legacy/ltx/` |
| `LTX-Video/generate_intro_single.py` | `legacy/ltx/` |
| `LTX-Video/configs/twc-{2b,13b}-0.9.8-distilled.yaml` | `legacy/ltx/configs/` |
| `LTX-Video/INTRO_*.md` | `legacy/ltx/docs/` |
| `LTX-Video/generate_intro_wan.py` | `intro/generate_intro_wan.py` |
| `LTX-Video/video_post.py` | `twc/post.py` |
| `LTX-Video/generate_felt_test.py` | `felt/generate_felt_test.py` |
| `ltx_env/make_music.py` | `audio/make_music.py` |
| `ltx_env/*.sbatch`, `env_ltx.sh`, `run_in_container.sh`, download scripts | `lumi/` (`env_ltx.sh` renamed `env.sh`) |
| `ltx_env/sweep_*.py`, `download_13b.py` | `legacy/ltx/experiments/` |
| the ffmpeg helpers inside `generate_intro_v3.py` | copied verbatim into `twc/media.py` |
| the five transition prompts inside `generate_intro_v3.py` | copied verbatim into `intro/prompts.py` |

The move was regression-tested: the score re-renders byte for byte, a
procedural frame re-renders with zero pixel difference, and the hybrid and
story assemblies rebuild at exactly 10.00 s.

## Environment changes (not in any repo)

The Python environment is a venv at `ltx_env/venv`, created with
`--system-site-packages` on top of the LUMI container. `lumi/setup_env.sh`
rebuilds it. Changes relative to the container:

- **pinned**: `transformers==4.51.3` (LTX-Video needs <4.52), `diffusers==0.39.0`
- **added**: `ltx-video` (editable, from the clone), `imageio-ffmpeg` (LUMI has no
  ffmpeg on PATH), `av`, `timm`, `ftfy` (Wan's prompt cleaner fails without it),
  `spandrel` (loads Real-ESRGAN), `safetensors` 0.8.0
- **stubbed**: `deepspeed` and `apex`. The container's copies pull in `aiter`,
  which tries to JIT-compile HIP kernels at import time and fails because there
  is no C++ compiler on PATH; `transformers` imports deepspeed eagerly, so every
  model import broke. Empty stand-ins in the venv shadow them
  (`lumi/stubs/`); nothing here uses ZeRO or apex.
- **runtime**: MIOpen's kernel database moved from `/tmp` (unwritable on some
  GPU nodes) to `ltx_env/miopen_cache/<job>_<task>`; `HF_HUB_DISABLE_IMPLICIT_TOKEN=1`
  so a stale token is never sent to public repos.
