#!/bin/bash
# Run a command inside the LUMI PyTorch ROCm container with the project venv active.
#   lumi/run_in_container.sh python intro/intro_v4.py generate --variant white
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SIF=/appl/local/containers/sif-images/lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif
# bash -c 'script' ARG0 ARGS...: $0 is the env file, "$@" the command to run
exec singularity exec -B /scratch,/pfs,/project,/flash "$SIF" \
    bash -c 'source "$0"; exec "$@"' "$HERE/env.sh" "$@"
