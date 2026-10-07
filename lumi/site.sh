# Machine-specific locations for LUMI (the only file to edit on another
# machine or project). Sourced by every script in lumi/ and voice/.
# Nothing here depends on the repo's name: the repo location is derived.
# Always derived, never inherited: this file is sourced into interactive shells
# (voice/gemini_env.sh), and an exported value from another clone, or from
# before the 2026-09-27 rename, would send every later job to that tree.
BLLT_REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export BLLT_REPO
export BLLT_PROJECT=${BLLT_PROJECT:-/scratch/project_465002727/jelealro}   # venvs, models, caches, logs
export BLLT_ACCOUNT=${BLLT_ACCOUNT:-project_465002727}                      # Slurm account (#SBATCH lines repeat it)
export BLLT_SIF=${BLLT_SIF:-/appl/local/containers/sif-images/lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif}
export BLLT_BINDS=${BLLT_BINDS:-/scratch,/pfs,/project,/flash}              # host folders visible in the container
export BLLT_SSH_HOST=${BLLT_SSH_HOST:-lumi.csc.fi}                          # for rsync from your computer (backup_assets.sh)
export BLLT_VENV_GEN=$BLLT_PROJECT/ltx_env/venv       # generation venv (diffusers 0.39); legacy name, keep
export BLLT_VENV_GEMINI=$BLLT_PROJECT/gemini_env/venv # google-genai client (voices)
export BLLT_LOGS=$BLLT_PROJECT/slurm_logs
export HF_HOME=${HF_HOME:-$BLLT_PROJECT/hf_cache}
