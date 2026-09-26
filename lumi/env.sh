# Source inside the container (or via run_in_container.sh) to get the LTX-Video env.
export HF_HOME=/scratch/project_465002727/jelealro/hf_cache
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export THE_WEBTOONS_CORNER_ROOT=${THE_WEBTOONS_CORNER_ROOT:-/scratch/project_465002727/jelealro}
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false
export LC_ALL=C.UTF-8 LANG=C.UTF-8
$WITH_CONDA
source /scratch/project_465002727/jelealro/ltx_env/venv/bin/activate
# MIOpen kernel cache: /tmp on some GPU nodes is full/unwritable (job 22225720 died with
# "Cannot open database file:/tmp/gfx90a6e.ukdb"), so keep it on scratch, per job.
export MIOPEN_USER_DB_PATH=/scratch/project_465002727/jelealro/ltx_env/miopen_cache/${SLURM_JOB_ID:-login}_${SLURM_PROCID:-0}
export MIOPEN_CUSTOM_CACHE_DIR=$MIOPEN_USER_DB_PATH
mkdir -p "$MIOPEN_USER_DB_PATH"
