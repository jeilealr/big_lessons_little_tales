# Source inside the container (or via TWC_ENV=tts run_in_container.sh): the
# voice/narration venv (Chatterbox multilingual TTS, Parler-TTS voice design).
# Separate because chatterbox pins transformers 4.46 / diffusers 0.29.
export HF_HOME=/scratch/project_465002727/jelealro/hf_cache
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-1}   # compute nodes may have no internet; models are cached (download with HF_HUB_OFFLINE=0 on the login node)
export THE_WEBTOONS_CORNER_ROOT=${THE_WEBTOONS_CORNER_ROOT:-/scratch/project_465002727/jelealro}
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false
export LC_ALL=C.UTF-8 LANG=C.UTF-8
$WITH_CONDA
source /scratch/project_465002727/jelealro/tts_env/venv/bin/activate
export MIOPEN_USER_DB_PATH=/scratch/project_465002727/jelealro/tts_env/miopen_cache/${SLURM_JOB_ID:-login}_${SLURM_PROCID:-0}
export MIOPEN_CUSTOM_CACHE_DIR=$MIOPEN_USER_DB_PATH
mkdir -p "$MIOPEN_USER_DB_PATH"
