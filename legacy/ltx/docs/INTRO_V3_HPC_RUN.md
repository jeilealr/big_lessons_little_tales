# Intro V3 — HPC run guide

Self-contained instructions to render the 7-second "The Webtoons Corner"
channel intro with LTX-Video on an HPC / cloud GPU node. Written because the
pipeline needs ~24 GB of resident model weights and the author's laptop has
only 16 GB RAM (Apple Silicon / MPS), where the CUDA CPU-offload path is
disabled and the machine swap-dies. On a CUDA GPU this runs unmodified.

The full design rationale is in `INTRO_V3_HANDOFF.md` and `INTRO_V3_GUIDE.md`
in this same folder. This file is the operational subset needed to run remotely.

---

## 1. Why it must run off the laptop

| Component | Resident size |
|---|---|
| PixArt text encoder (T5-XXL, `PixArt-alpha/PixArt-XL-2-1024-MS`) | ~18 GB on disk (fp32); ~9-10 GB in bf16 |
| LTX-Video 2B distilled checkpoint | ~6.4 GB |
| LTX spatial upscaler (multi-scale 2nd pass) | ~0.5 GB |
| VAE + activations during generation | several GB |

On CUDA the script offloads idle components to CPU RAM
(`inference.py`: `offload_to_cpu = config.offload_to_cpu and get_total_gpu_memory() < 30`).
That path is gated behind `torch.cuda.is_available()`, so on MPS it never runs
and everything stays resident at once — hence the crash on 16 GB.

**On the HPC you do not have this problem.** Any single CUDA GPU with
**>= 24 GB VRAM** (A100, A10G, L40S, RTX 3090/4090, etc.) runs the full
multi-scale pipeline comfortably. With 12-16 GB VRAM it still works if you
enable CPU offload — see step 5.

---

## 2. Files to transfer to the HPC

Everything is small except the model weights, which download automatically on
first run (~7 GB of LTX weights + the PixArt text encoder from Hugging Face).

Transfer this whole channel subtree (keep the relative layout — the script
resolves paths from the repo location):

```
TheWebtoonsCorner/
├── Intro/
│   ├── reference_img/            # 1.png … 6.png, 1672x941, 16:9   (~16 MB)
│   └── Intro_channel_video.mov   # soundtrack source, 6.016 s      (~6.3 MB)
└── repositories/
    └── LTX-Video/                # code only, no weights           (~1.5 MB)
        ├── generate_intro_v3.py
        ├── configs/ltxv-2b-0.9.8-distilled.yaml
        └── ... (rest of the repo)
```

Total upload is ~25 MB. Example:

```bash
# from the laptop
rsync -av --exclude '.git' \
  TheWebtoonsCorner/Intro \
  TheWebtoonsCorner/repositories \
  USER@hpc.example.edu:/scratch/USER/TheWebtoonsCorner/
```

The script anchors paths on the repo's own location: with `repositories/LTX-Video`
two levels under the channel root, `Intro/` is found automatically. If you place
the repo elsewhere, set the channel root explicitly:

```bash
export THE_WEBTOONS_CORNER_ROOT=/scratch/USER/TheWebtoonsCorner
```

---

## 3. Environment

Reproduce the environment that already validated locally:

- Python 3.11
- torch 2.14 (use the CUDA build matching the node's driver, e.g. cu121/cu124)
- diffusers 0.39.0, transformers 4.51.3, safetensors 0.8.0,
  sentencepiece 0.2.2, einops 0.8.2, imageio 2.37, timm, av, torchvision

```bash
module load cuda            # or whatever your site uses
conda create -n ltxvideo python=3.11 -y
conda activate ltxvideo

cd /scratch/USER/TheWebtoonsCorner/repositories/LTX-Video

# install the LTX package + its declared inference extras
python -m pip install --upgrade pip
python -m pip install -e ".[inference]"

# pin torch to the CUDA build appropriate for the node if the default is CPU-only
# python -m pip install torch==2.14.0 --index-url https://download.pytorch.org/whl/cu124
```

`pyproject.toml` declares: torch>=2.1, diffusers>=0.28.2,
transformers>=4.47.2,<4.52, sentencepiece, huggingface-hub~=0.30, einops, timm;
inference extra adds imageio[ffmpeg], av, torchvision.

Confirm the GPU is visible:

```bash
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

---

## 4. Hugging Face access (important gotcha)

The weights are on a **public, non-gated** repo (`Lightricks/LTX-Video`) plus
the public PixArt text encoder. No token is required.

The laptop failed with a misleading `401 ... RepositoryNotFoundError` because a
**stale HF OAuth token** was being sent to a public repo. Prevent that on the
HPC by disabling the implicit token:

```bash
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
```

Set an HF cache location on fast scratch with quota headroom (the download is
several GB, and the PixArt cache alone is large):

```bash
export HF_HOME=/scratch/USER/hf_cache
```

Do **not** log in / paste any token unless your site actually requires one for
outbound HF access. If it does, use a fresh read token via `huggingface-cli login`.

---

## 5. Run

All commands from the channel root:

```bash
cd /scratch/USER/TheWebtoonsCorner
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export HF_HOME=/scratch/USER/hf_cache
```

**a) Validate inputs (no model, no download, seconds):**

```bash
python repositories/LTX-Video/generate_intro_v3.py --dry-run
```

Expected plan: 768x432 @ 24 fps, frames 33/41/33/33/33 per transition,
169-frame concat (7.04 s) retimed to exactly 7.00 s, final 1920x1080 @ 30 fps.

**b) Low-res preview (512x288, 25 frames/segment; downloads weights once):**

```bash
python repositories/LTX-Video/generate_intro_v3.py \
  --preview --accept-ltx-license --force
```

**c) Full render:**

```bash
python repositories/LTX-Video/generate_intro_v3.py \
  --accept-ltx-license --force
```

**d) Redo a single transition (1-5) after tweaking its prompt / end image:**

```bash
python repositories/LTX-Video/generate_intro_v3.py \
  --only 3 --accept-ltx-license --force
```

Segments are cached at
`Intro/intro_v3_work/segments/<w>x<h>_<fps>fps_seed<seed>/`, so a rerun only
regenerates what is missing (or what `--only` / `--redo` forces). Preview and
full runs cache separately; both write the same final output, hence `--force`.

### If the node's GPU has < ~24 GB VRAM

Enable CPU offload — the script currently hardcodes it off. In
`generate_intro_v3.py`, `generate_segment()`, change:

```python
offload_to_cpu=False,
```

to

```python
offload_to_cpu=True,
```

On CUDA with `get_total_gpu_memory() < 30`, this moves idle components (notably
the text encoder) to CPU RAM between stages, cutting peak VRAM at some speed
cost. Requires the node to have enough **CPU** RAM (>= 32 GB recommended).

---

## 6. SLURM example

```bash
#!/bin/bash
#SBATCH --job-name=twc_intro_v3
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1              # >=24 GB VRAM ideal
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=02:00:00
#SBATCH --output=twc_intro_v3_%j.log

module load cuda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate ltxvideo

export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export HF_HOME=/scratch/$USER/hf_cache

cd /scratch/$USER/TheWebtoonsCorner

# preview first, then swap to the full-render line once it looks right
python repositories/LTX-Video/generate_intro_v3.py --preview --accept-ltx-license --force
# python repositories/LTX-Video/generate_intro_v3.py --accept-ltx-license --force
```

Budget: first run spends several minutes downloading weights, then a few
minutes per segment on a datacenter GPU (five segments). Two hours of walltime
is generous. `--mem=48G` gives room if you enable CPU offload.

---

## 7. Output and what to check

Final file: `Intro/Intro_channel_video_v3.mov`
— 1920x1080, 30 fps, exactly 7.000 s, video H.264 (crf 17),
audio **PCM `pcm_s16le` 48 kHz stereo** (see gotcha below).

Judge the preview before paying for the full render:

1. Does each segment actually arrive at its end image, or snap onto it in the
   last frames? If it snaps, lower `--end-strength` (default 0.92); if it drifts
   and no longer matches the next segment's opening, raise it.
2. Do the five seams read as one continuous shot?
3. Is the book identity stable across all segments — same cover, same TWC
   emblem, no second book, no invented text?

**Audio gotcha — do not "fix" it:** the output is deliberately PCM in a MOV,
not AAC. DaVinci Resolve decodes AAC-in-MOV unreliably (draws the waveform,
renders silence). Keep `pcm_s16le`. Everything in the project is 48 kHz.

`--segment-frames` must be 8k+1 (25, 33, 41, 49…). Omit it to let the weights
size each transition. Changing `--width`/`--height`/`--fps`/`--seed` starts a
fresh cache directory.

---

## 8. Bring it back

```bash
# from the laptop
rsync -av USER@hpc.example.edu:/scratch/USER/TheWebtoonsCorner/Intro/Intro_channel_video_v3.mov \
  ~/Documents/youtube/TheWebtoonsCorner/Intro/
```

Optionally also copy back `Intro/intro_v3_work/segments/` so future single-clip
tweaks reuse the cache.

---

## 9. Licensing (already researched)

Repo code is Apache 2.0. The `ltxv-2b-0.9.8` checkpoint + upscaler are under the
LTXV Open Weights License 0.X — `--accept-ltx-license` is your acknowledgement.
Paid commercial licensing is reserved for entities with >= $10M annual revenue;
below that, monetised use is permitted subject to restrictions, one of which is
disclosing machine-generated content. Text encoder (PixArt) is CreativeML Open
RAIL++-M. The reference stills are the author's own work and contain no manga
artwork. YouTube description line to use:

> Portions of this video were generated with AI using LTX-Video.

Repo commit for reference: `4b2d053`. Not legal advice.
