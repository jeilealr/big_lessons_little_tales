#!/bin/bash
# Picks line $SLURM_PROCID of the task file and runs it in the container,
# from the repo root. The line is parsed by bash, so quoted arguments (e.g. a
# prompt with spaces) work.
LINE=$(grep -v -E '^\s*(#|$)' "$1" | sed -n "$((SLURM_PROCID + 1))p")
echo "[task $SLURM_PROCID] GPU=$ROCR_VISIBLE_DEVICES host=$(hostname) $(date)"
echo "[task $SLURM_PROCID] $LINE"
exec "$(dirname "$0")/run_in_container.sh" bash -c "$LINE"
