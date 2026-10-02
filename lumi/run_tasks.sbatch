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
# comments ignored); task k runs line k inside the container (lumi/task_exec.sh).
# --ntasks must equal the number of lines: the job stops if there are more
# lines than tasks (they would never run).
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
TASKS=${1:-}
[ -f "$TASKS" ] || { echo "usage: sbatch --ntasks=N ... lumi/run_tasks.sbatch <tasks file> (got '$TASKS')"; exit 1; }
N=$(grep -c -v -E '^\s*(#|$)' "$TASKS" || true)
echo "Job $SLURM_JOB_ID on $(hostname), $SLURM_NTASKS tasks, $N lines in $TASKS, repo $BLLT_REPO, started $(date)"
[ "${SLURM_JOB_ACCOUNT:-}" = "$BLLT_ACCOUNT" ] || echo "warning: job account ${SLURM_JOB_ACCOUNT:-?} is not BLLT_ACCOUNT=$BLLT_ACCOUNT (lumi/site.sh)"
[ "$N" -gt 0 ] || { echo "no commands in $TASKS"; exit 1; }
grep -v -E '^\s*(#|$)' "$TASKS" | nl -v0 -w1 -s': '
if [ "$N" -gt "$SLURM_NTASKS" ]; then
  echo "$N lines but $SLURM_NTASKS tasks: lines $((SLURM_NTASKS + 1))-$N would never run; resubmit with --ntasks=$N"
  exit 1
fi
[ "$N" -eq "$SLURM_NTASKS" ] || echo "warning: $SLURM_NTASKS tasks for $N lines: $((SLURM_NTASKS - N)) task(s) will have nothing to run"
rc=0     # keep going after a failed task, to log the end and the exit code
srun --ntasks="$SLURM_NTASKS" --gpus-per-task=1 --kill-on-bad-exit=0 \
     --output="$BLLT_LOGS/bllt_tasks_%j_%t.log" \
     "$BLLT_REPO/lumi/task_exec.sh" "$TASKS" || rc=$?
echo "Finished $(date), exit $rc"
[ "$rc" -eq 0 ] || echo "at least one task failed: see the per-task logs"
exit "$rc"
