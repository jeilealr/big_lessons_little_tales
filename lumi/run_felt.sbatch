#!/bin/bash
#SBATCH --job-name=twc_felt
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1 --ntasks=1 --gpus-per-node=1 --cpus-per-task=14 --mem=160G
#SBATCH --time=03:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/twc_felt_%j.log
set -euo pipefail
cd /scratch/project_465002727/jelealro
echo "Job $SLURM_JOB_ID on $(hostname) started $(date)"
srun twc_video/lumi/run_in_container.sh python twc_video/felt/generate_felt_test.py "$@"
echo "Finished $(date)"
