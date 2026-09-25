"""Weights for LoRA training with musubi-tuner (Wan 2.2 T2V A14B), ~69 GB.

musubi-tuner reads the ComfyUI-repackaged experts and the original Wan 2.1
VAE / T5 files, not the diffusers layout in Wan-AI/*-Diffusers. All Apache-2.0.
"""
from huggingface_hub import hf_hub_download

FILES = [
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_t2v_low_noise_14B_fp16.safetensors"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_t2v_high_noise_14B_fp16.safetensors"),
    ("Wan-AI/Wan2.1-T2V-14B", "Wan2.1_VAE.pth"),
    ("Wan-AI/Wan2.1-T2V-14B", "models_t5_umt5-xxl-enc-bf16.pth"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/tokenizer.json"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/tokenizer_config.json"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/special_tokens_map.json"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/spiece.model"),
    # 4-step distillation LoRAs (lightx2v), for fast drafts later
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors"),
]
for repo, name in FILES:
    print("->", hf_hub_download(repo, name, local_dir="/scratch/project_465002727/jelealro/models/wan22_musubi"), flush=True)
print("DOWNLOAD DONE")
