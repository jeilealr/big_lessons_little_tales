#!/bin/bash
#SBATCH --job-name=twc_intro_v3
#SBATCH --account=project_465002727
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=60G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/twc_intro_v3_%j.log

# Usage: sbatch run_intro_v3.sbatch [extra generate_intro_v3.py args]
#   default          -> full render (768x432, 33/41/33/33/33 frames), 1920x1080@30 output
#   --preview        -> 512x288, 25 frames/segment quick test
#   --only 3         -> regenerate one transition
# One MI250X GCD (64 GB) holds the whole multi-scale pipeline; no CPU offload needed.

set -euo pipefail
cd /scratch/project_465002727/jelealro
echo "Job $SLURM_JOB_ID on $(hostname) started $(date)"
rocm-smi --showproductname --showmeminfo vram 2>/dev/null | grep -E "GPU\[|Card series|Total" || true

srun twc_video/lumi/run_in_container.sh python twc_video/legacy/ltx/generate_intro_v3.py \
    --accept-ltx-license --force "$@"

echo "Finished $(date)"
