# Sourced inside the container (BLLT_ENV=qwen run_in_container.sh): the image-edit
# venv for production/edit_image.py. Not created yet (lumi/setup_env_qwen.sh
# builds it). Same rules as env.sh.
source "$(dirname "${BASH_SOURCE[0]}")/site.sh"
export HF_HUB_DISABLE_IMPLICIT_TOKEN=${HF_HUB_DISABLE_IMPLICIT_TOKEN:-1}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}
export TOKENIZERS_PARALLELISM=${TOKENIZERS_PARALLELISM:-false}
export LC_ALL=C.UTF-8 LANG=C.UTF-8      # forced (see env.sh)
${WITH_CONDA:-}
source "$BLLT_VENV_QWEN/bin/activate" || { echo "no venv at $BLLT_VENV_QWEN: run lumi/setup_env_qwen.sh" >&2; return 1; }
export MIOPEN_USER_DB_PATH=$BLLT_VENV_QWEN/../miopen_cache/${SLURM_JOB_ID:-login}_${SLURM_PROCID:-0}   # forced (see env.sh)
export MIOPEN_CUSTOM_CACHE_DIR=$MIOPEN_USER_DB_PATH
mkdir -p "$MIOPEN_USER_DB_PATH"
