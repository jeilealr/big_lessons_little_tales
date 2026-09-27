# Paths for LoRA training with musubi-tuner (Wan 2.2 T2V A14B). Sourced by the scripts here.
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/../lumi" && pwd)/site.sh"
ROOT=$BLLT_REPO                     # scripts refer to $ROOT/work/...
MUSUBI=$BLLT_EXT/musubi-tuner/src/musubi_tuner
W=$BLLT_MODELS/wan22_musubi
DIT_LOW=$W/split_files/diffusion_models/wan2.2_t2v_low_noise_14B_bf16.safetensors
DIT_HIGH=$W/split_files/diffusion_models/wan2.2_t2v_high_noise_14B_bf16.safetensors
VAE=$W/Wan2.1_VAE.pth
T5=$W/models_t5_umt5-xxl-enc-bf16.pth
# the musubi venv (diffusers 0.32 / transformers 4.57), inside the same container
source "$BLLT_REPO/lumi/env_musubi.sh"
export HF_HUB_OFFLINE=1          # everything is cached; a job must never need the network

# Every musubi script runs as ONE process. Inside a multi-task Slurm step, Cray's
# process manager sets PMI_SIZE etc., which accelerate (used by training AND by
# generation) reads as an MPI world size, then aborts asking for MASTER_ADDR.
for v in $(env | grep -oE '^(PMI|PMIX|OMPI|MV2|MPI_LOCAL)[A-Z_]*' || true); do unset "$v"; done
