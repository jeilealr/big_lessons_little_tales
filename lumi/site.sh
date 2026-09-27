# Machine-specific locations for LUMI (the only file to edit on another
# machine or project). Sourced by every script in lumi/, lora/ and voice/.
# Nothing here depends on the repo's name: the repo location is derived.
export BLLT_REPO=${BLLT_REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
export BLLT_PROJECT=${BLLT_PROJECT:-/scratch/project_465002727/jelealro}   # venvs, models, caches, logs
export BLLT_ACCOUNT=${BLLT_ACCOUNT:-project_465002727}                      # Slurm account
export BLLT_SIF=${BLLT_SIF:-/appl/local/containers/sif-images/lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif}
export BLLT_VENV_GEN=$BLLT_PROJECT/ltx_env/venv       # generation venv (diffusers 0.39); legacy name, keep
export BLLT_VENV_MUSUBI=$BLLT_PROJECT/musubi_env/venv # LoRA training venv (musubi-tuner pins)
export BLLT_VENV_GEMINI=$BLLT_PROJECT/gemini_env/venv # google-genai client (voices)
export BLLT_MODELS=$BLLT_PROJECT/models               # musubi bf16 weights
export BLLT_EXT=$BLLT_PROJECT/ext                     # musubi-tuner checkout
export BLLT_LOGS=$BLLT_PROJECT/slurm_logs
export HF_HOME=${HF_HOME:-$BLLT_PROJECT/hf_cache}
