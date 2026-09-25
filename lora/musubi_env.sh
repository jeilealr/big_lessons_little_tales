# Paths for LoRA training with musubi-tuner (Wan 2.2 T2V A14B). Sourced by the scripts here.
ROOT=/scratch/project_465002727/jelealro
MUSUBI=$ROOT/ext/musubi-tuner/src/musubi_tuner
W=$ROOT/models/wan22_musubi
DIT_LOW=$W/split_files/diffusion_models/wan2.2_t2v_low_noise_14B_bf16.safetensors
DIT_HIGH=$W/split_files/diffusion_models/wan2.2_t2v_high_noise_14B_bf16.safetensors
VAE=$W/Wan2.1_VAE.pth
T5=$W/models_t5_umt5-xxl-enc-bf16.pth
# the musubi venv (diffusers 0.32 / transformers 4.57), inside the same container
source $ROOT/twc_video/lumi/env_musubi.sh
export HF_HUB_OFFLINE=1          # everything is cached; a job must never need the network
