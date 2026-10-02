#!/bin/bash
# Run a command inside the LUMI PyTorch ROCm container with a project venv active.
#   lumi/run_in_container.sh python production/shot.py --story lion_and_mouse_v3 --scene 1 --shot s01_milo_explores --fast --dry-run
#   BLLT_ENV=musubi lumi/run_in_container.sh python ...    # the LoRA-training venv (env_musubi.sh)
# Two venvs because musubi-tuner pins diffusers 0.32 / transformers 4.57, while
# the generation code needs diffusers 0.39 / transformers 4.51 (docs/provenance.md).
# Runs from the repo root, whatever the caller's directory.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$HERE/site.sh"
[ $# -gt 0 ] || { echo "usage: lumi/run_in_container.sh <command> [args...]" >&2; exit 2; }
ENV_FILE=$HERE/env${BLLT_ENV:+_$BLLT_ENV}.sh
[ -f "$ENV_FILE" ] || { echo "no $ENV_FILE (BLLT_ENV=${BLLT_ENV:-})" >&2; exit 2; }
cd "$BLLT_REPO"
# bash -c 'script' ARG0 ARGS...: $0 is the env file, "$@" the command to run.
# `|| exit 1`: a missing venv must stop here, not run on the container's own Python.
exec singularity exec -B "$BLLT_BINDS" "$BLLT_SIF" \
    bash -c 'source "$0" || exit 1; exec "$@"' "$ENV_FILE" "$@"
