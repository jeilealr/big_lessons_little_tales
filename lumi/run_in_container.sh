#!/bin/bash
# Run a command inside the LUMI PyTorch ROCm container with a project venv active.
#   lumi/run_in_container.sh python production/shot.py --story lion_and_mouse_v5 --scene 1 --shot s01_explores --fast --dry-run
# FELTWILLOW_ENV=<name> selects lumi/env_<name>.sh instead of lumi/env.sh (only env.sh exists now;
# the LoRA and Qwen venvs were removed from the repo on 2026-10-06).
# Runs from the repo root, whatever the caller's directory.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$HERE/site.sh"
[ $# -gt 0 ] || { echo "usage: lumi/run_in_container.sh <command> [args...]" >&2; exit 2; }
ENV_FILE=$HERE/env${FELTWILLOW_ENV:+_$FELTWILLOW_ENV}.sh
[ -f "$ENV_FILE" ] || { echo "no $ENV_FILE (FELTWILLOW_ENV=${FELTWILLOW_ENV:-})" >&2; exit 2; }
cd "$FELTWILLOW_REPO"
# bash -c 'script' ARG0 ARGS...: $0 is the env file, "$@" the command to run.
# `|| exit 1`: a missing venv must stop here, not run on the container's own Python.
exec singularity exec -B "$FELTWILLOW_BINDS" "$FELTWILLOW_SIF" \
    bash -c 'source "$0" || exit 1; exec "$@"' "$ENV_FILE" "$@"
