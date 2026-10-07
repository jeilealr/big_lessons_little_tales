# Machine-specific locations for LUMI (the only file to edit on another
# machine or project). Sourced by every script in lumi/ and voice/.
# Nothing here depends on the repo's name: the repo location is derived.
# Always derived, never inherited: this file is sourced into interactive shells
# (voice/gemini_env.sh), and an exported value from another clone, or from
# before the 2026-09-27 rename, would send every later job to that tree.
FELTWILLOW_REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export FELTWILLOW_REPO
export FELTWILLOW_PROJECT=${FELTWILLOW_PROJECT:-/scratch/project_465002727/jelealro}   # venvs, models, caches, logs
export FELTWILLOW_ACCOUNT=${FELTWILLOW_ACCOUNT:-project_465002727}                      # Slurm account (#SBATCH lines repeat it)
export FELTWILLOW_SIF=${FELTWILLOW_SIF:-/appl/local/containers/sif-images/lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif}
export FELTWILLOW_BINDS=${FELTWILLOW_BINDS:-/scratch,/pfs,/project,/flash}              # host folders visible in the container
export FELTWILLOW_SSH_HOST=${FELTWILLOW_SSH_HOST:-lumi.csc.fi}                          # for rsync from your computer (backup_assets.sh)
export FELTWILLOW_VENV_GEN=$FELTWILLOW_PROJECT/ltx_env/venv       # generation venv (diffusers 0.39); legacy name, keep
export FELTWILLOW_VENV_GEMINI=$FELTWILLOW_PROJECT/gemini_env/venv # google-genai client (voices)
export FELTWILLOW_LOGS=$FELTWILLOW_PROJECT/slurm_logs
export HF_HOME=${HF_HOME:-$FELTWILLOW_PROJECT/hf_cache}
