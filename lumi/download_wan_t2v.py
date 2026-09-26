from huggingface_hub import snapshot_download
p = snapshot_download("Wan-AI/Wan2.2-T2V-A14B-Diffusers", revision="5be7df9619b54f4e2667b2755bc6a756675b5cd7",
                      allow_patterns=["*.json","*.txt","*.model","*.safetensors","*.py"],
                      max_workers=8)
print("->", p, flush=True); print("DOWNLOAD DONE")
