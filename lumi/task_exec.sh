#!/bin/bash
# One task of lumi/run_tasks.sbatch: picks line $SLURM_PROCID of the task file
# (blank lines and # comments skipped) and runs it in the container, from the
# repo root. The line is parsed by bash, so quoted arguments (e.g. a prompt with
# spaces) work.
set -uo pipefail
K=${SLURM_PROCID:-0}
LINE=$(grep -v -E '^\s*(#|$)' "$1" | sed -n "$((K + 1))p")
# cpus: what this task may use (srun does not always inherit --cpus-per-task)
echo "[task $K] GPU=${ROCR_VISIBLE_DEVICES:-?} cpus=$(nproc) host=$(hostname) $(date)"
if [ -z "$LINE" ]; then
  echo "[task $K] no line $((K + 1)) in $1: nothing to run"
  exit 0
fi
echo "[task $K] $LINE"
exec "$(dirname "$0")/run_in_container.sh" bash -c "$LINE"
