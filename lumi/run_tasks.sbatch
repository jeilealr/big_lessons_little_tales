#!/bin/bash
#SBATCH --job-name=bllt_tasks
#SBATCH --account=project_465002727
#SBATCH --partition=dev-g
#SBATCH --nodes=1
#SBATCH --cpus-per-task=7
#SBATCH --time=03:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/bllt_tasks_%j.log
#
# Run several independent GPU tasks in ONE job, one GCD each, in parallel.
# Submit from the repo root:
#   sbatch --ntasks=3 --gpus-per-node=3 --mem=330G lumi/run_tasks.sbatch work/tasks/<name>.txt
# tasks file: one command per line, run from the repo root (blank lines and #
# comments ignored); task k runs line k inside the container.
# Per-task logs: $BLLT_LOGS/bllt_tasks_<job>_<k>.log
# (#SBATCH lines cannot use variables: account and log folder are repeated
# from lumi/site.sh; change both together.)
#
# Why: dev-g allows only 2 jobs per user but a job may use up to a whole node
# (8 GCDs). Host RAM is the real limit for Wan: ~100-110 GB per task with CPU
# offload, so ~4 Wan tasks fit on one 512 GB node.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
[ -f lumi/site.sh ] || { echo "submit from the repo root (lumi/site.sh not found in $PWD)"; exit 1; }
source lumi/site.sh
echo "Job $SLURM_JOB_ID on $(hostname), $SLURM_NTASKS tasks, repo $BLLT_REPO, started $(date)"
grep -v -E '^\s*(#|$)' "$1" | nl -v0 -w1 -s': '
srun --ntasks="$SLURM_NTASKS" --gpus-per-task=1 --kill-on-bad-exit=0 \
     --output="$BLLT_LOGS/bllt_tasks_%j_%t.log" \
     "$BLLT_REPO/lumi/task_exec.sh" "$1"
echo "Finished $(date)"
