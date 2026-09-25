#!/bin/bash
# Run a command inside the LUMI PyTorch ROCm container with a project venv active.
#   lumi/run_in_container.sh python intro/intro_v4.py generate --variant white
#   TWC_ENV=musubi lumi/run_in_container.sh python ...    # the LoRA-training venv
# Two venvs because musubi-tuner pins diffusers 0.32 / transformers 4.57, while
# the generation code needs diffusers 0.39 / transformers 4.51 (docs/provenance.md).
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SIF=/appl/local/containers/sif-images/lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif
# bash -c 'script' ARG0 ARGS...: $0 is the env file, "$@" the command to run
exec singularity exec -B /scratch,/pfs,/project,/flash "$SIF" \
    bash -c 'source "$0"; exec "$@"' "$HERE/env${TWC_ENV:+_$TWC_ENV}.sh" "$@"
