#!/bin/bash
#SBATCH --job-name=twc_tasks
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1
#SBATCH --cpus-per-task=7
#SBATCH --time=03:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/twc_tasks_%j.log
#
# Run several independent GPU tasks in ONE job, one GCD each, in parallel.
#   sbatch --ntasks=3 --gpus-per-node=3 --mem=400G twc_video/lumi/run_tasks.sbatch tasks.txt
# tasks.txt: one command per line (blank lines and # comments ignored); task k
# runs line k inside the container. Per-task logs: twc_tasks_<job>_<k>.log
#
# Why: dev-g allows only 2 jobs per user but a job may use up to a whole node
# (8 GCDs). Host RAM is the real limit for Wan: ~80-100 GB per task with CPU
# offload, so ~4 Wan tasks fit on one 512 GB node.
set -euo pipefail
cd /scratch/project_465002727/jelealro
echo "Job $SLURM_JOB_ID on $(hostname), $SLURM_NTASKS tasks, started $(date)"
grep -v -E '^\s*(#|$)' "$1" | nl -v0 -w1 -s': '
srun --ntasks="$SLURM_NTASKS" --gpus-per-task=1 --kill-on-bad-exit=0 \
     --output=/scratch/project_465002727/jelealro/slurm_logs/twc_tasks_%j_%t.log \
     twc_video/lumi/task_exec.sh "$1"
echo "Finished $(date)"
