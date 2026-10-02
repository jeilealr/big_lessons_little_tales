#!/usr/bin/env python3
"""Weights for LoRA training with musubi-tuner (Wan 2.2 T2V A14B), ~69 GB.

  lumi/run_in_container.sh python lumi/download_musubi_weights.py    # login node (network)

Into $BLLT_MODELS/wan22_musubi (lumi/site.sh). musubi-tuner reads the
ComfyUI-repackaged experts and the original Wan 2.1 VAE / T5 files, not the
diffusers layout in Wan-AI/*-Diffusers. All Apache-2.0. The fp16 experts are
then converted to bf16 with lumi/convert_dit_bf16.py.
"""
import os
import sys

from huggingface_hub import hf_hub_download

REVISIONS = {   # pinned; see docs/findings-and-risks.md
    "Comfy-Org/Wan_2.2_ComfyUI_Repackaged": "ee6f4a40737a995bf5818954cfce6d59443b0f04",
    "Wan-AI/Wan2.1-T2V-14B": "a064a6c71f5be440641209c07bf2a5ce7a2ff5e4",
}

FILES = [
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_t2v_low_noise_14B_fp16.safetensors"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_t2v_high_noise_14B_fp16.safetensors"),
    ("Wan-AI/Wan2.1-T2V-14B", "Wan2.1_VAE.pth"),
    ("Wan-AI/Wan2.1-T2V-14B", "models_t5_umt5-xxl-enc-bf16.pth"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/tokenizer.json"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/tokenizer_config.json"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/special_tokens_map.json"),
    ("Wan-AI/Wan2.1-T2V-14B", "google/umt5-xxl/spiece.model"),
    # 4-step distillation LoRAs (lightx2v) for T2V; nothing uses them yet (fast
    # mode uses the I2V Lightning LoRAs, bllt/wan.py)
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_low_noise.safetensors"),
]

if not os.environ.get("BLLT_MODELS"):
    sys.exit("BLLT_MODELS is not set: run through lumi/run_in_container.sh (it sources lumi/site.sh)")
dest = os.path.join(os.environ["BLLT_MODELS"], "wan22_musubi")
for repo, name in FILES:
    print("->", hf_hub_download(repo, name, revision=REVISIONS[repo], local_dir=dest), flush=True)
print("DOWNLOAD DONE")
