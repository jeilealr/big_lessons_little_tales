#!/bin/bash
# Run a command inside the LUMI PyTorch ROCm container with a project venv active.
#   lumi/run_in_container.sh python production/shot.py --scene 1 --shot s01_sleeps_3q --dry-run
#   BLLT_ENV=musubi lumi/run_in_container.sh python ...    # the LoRA-training venv
# Two venvs because musubi-tuner pins diffusers 0.32 / transformers 4.57, while
# the generation code needs diffusers 0.39 / transformers 4.51 (docs/provenance.md).
# Runs from the repo root, whatever the caller's directory.
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$HERE/site.sh"
cd "$BLLT_REPO"
# bash -c 'script' ARG0 ARGS...: $0 is the env file, "$@" the command to run
exec singularity exec -B /scratch,/pfs,/project,/flash "$BLLT_SIF" \
    bash -c 'source "$0"; exec "$@"' "$HERE/env${BLLT_ENV:+_$BLLT_ENV}.sh" "$@"
