# Running on LUMI

Account `project_465002727`. Everything runs inside the LUMI PyTorch ROCm
container through `lumi/run_in_container.sh`, which activates the venv at
`ltx_env/venv` (rebuild with `lumi/setup_env.sh`).

```bash
W=twc_video/lumi/run_in_container.sh
$W python twc_video/character/character.py prompt      # anything, on a login node
```

## GPU jobs

- **Partition**: `dev-g` starts almost immediately but allows **2 jobs per user**
  and **3 h** per job. `small-g` / `standard-g` allow days but had 700–1000 jobs
  queued when this was written.
- **Several tasks in one job**: a `dev-g` job may use several GCDs of a node.
  `lumi/run_tasks.sbatch` runs one command per line of a task file, one GCD
  each, in parallel:
  ```bash
  sbatch --ntasks=3 --gpus-per-node=3 --mem=400G twc_video/lumi/run_tasks.sbatch tasks.txt
  ```
  Each task reports `ROCR_VISIBLE_DEVICES=0`: that is its *own* GCD renumbered
  inside its task cgroup, not a shared device. Verified: the three tasks of job
  22348370 held `renderD133`, `renderD130` and `renderD131`.
- **Host RAM is the limit for Wan**, not VRAM: two 14B experts plus the text
  encoder are offloaded to host memory (~80–100 GB per task, ~34 GB VRAM). About
  4 Wan tasks fit on one 512 GB node.

## Measured times (one MI250X GCD)

| Work | Time |
|---|---|
| Wan A14B model load (fp32 on disk → bf16) | 10–21 min |
| Wan I2V 720p, 40 steps: 33 / 41 / 81 frames | ~25 min / ~42 min / ~2 h |
| Wan 720p, 97 frames | ~250 s per step: does not fit in 3 h |
| Wan T2V 81-frame shot, including load | ~2.5 h |
| RIFE + Real-ESRGAN, 10 s clip | ~20 min |
| Procedural ident, 10 s 1080p60 | ~2 min on 8 CPU cores |
| Score synthesis | seconds |

## Gotchas already solved

- No ffmpeg on PATH: `twc.media.locate_ffmpeg` falls back to imageio-ffmpeg's binary.
- `deepspeed`/`apex` import failures: see `docs/provenance.md` and `lumi/stubs/`.
- `Cannot open database file: /tmp/gfx90a…ukdb`: MIOpen cache moved to scratch,
  one directory per job *and task* (`lumi/env.sh`).
- tqdm progress bars do not flush through `srun`; a job that looks silent may be
  computing: check `rocm-smi` with `srun --overlap --jobid=<id>`.
- Clips longer than 81 frames need `pipe.vae.enable_tiling()` and cost
  quadratically; prefer 81 frames and retime with RIFE.
