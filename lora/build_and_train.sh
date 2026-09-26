#!/bin/bash
# One task: (low only) build the dataset in the generation env, then train.
#   bash lora/build_and_train.sh <name> <low|high> [steps]
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
if [ "$2" = low ]; then
  echo "[$(date +%T)] build dataset $1"
  python $HERE/build_dataset.py "$1"            # ltx venv: BiRefNet for the composites
fi
exec bash $HERE/train_character.sh "$@"
