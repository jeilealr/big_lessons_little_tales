#!/bin/bash
# One task: (low only) build the dataset in the generation venv, then train.
#   bash lora/build_and_train.sh <name> <low|high> [steps]
set -euo pipefail
[ $# -ge 2 ] || { echo "usage: bash lora/build_and_train.sh <name> <low|high> [steps]" >&2; exit 2; }
HERE=$(cd "$(dirname "$0")" && pwd)
if [ "$2" = low ]; then
  echo "[$(date +%T)] build dataset $1"
  # generation venv: BiRefNet for the composites. On failure, tell the waiting
  # high task to stop (the failed file of train_character.sh).
  python "$HERE/build_dataset.py" "$1" || {
    mkdir -p "$HERE/../work/lora/$1"
    touch "$HERE/../work/lora/$1/.cache_failed_${SLURM_JOB_ID:-manual}"
    exit 1
  }
fi
exec bash "$HERE/train_character.sh" "$@"
