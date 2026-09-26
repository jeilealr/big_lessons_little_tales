from huggingface_hub import snapshot_download
p = snapshot_download("Wan-AI/Wan2.2-I2V-A14B-Diffusers", revision="596658fd9ca6b7b71d5057529bbf319ecbc61d74",
                      allow_patterns=["*.json", "*.txt", "*.model", "*.safetensors", "*.py"],
                      max_workers=8)
print("->", p, flush=True)
print("DOWNLOAD DONE")
