#!/bin/bash
# Picks line $SLURM_PROCID of the task file and runs it in the container.
LINE=$(grep -v -E '^\s*(#|$)' "$1" | sed -n "$((SLURM_PROCID + 1))p")
echo "[task $SLURM_PROCID] GPU=$ROCR_VISIBLE_DEVICES host=$(hostname) $(date)"
echo "[task $SLURM_PROCID] $LINE"
# shellcheck disable=SC2086  # the task line is meant to word-split
exec "$(dirname "$0")/run_in_container.sh" $LINE
