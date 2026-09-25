#!/bin/bash
#SBATCH --job-name=twc_sweep
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1 --ntasks=1 --gpus-per-node=1 --cpus-per-task=7 --mem=60G
#SBATCH --time=01:30:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/twc_sweep_%j.log
set -euo pipefail
cd /scratch/project_465002727/jelealro
SCRIPT=${SWEEP_SCRIPT:-twc_video/legacy/ltx/experiments/sweep_seg.py}
srun twc_video/lumi/run_in_container.sh python $SCRIPT "$@"
