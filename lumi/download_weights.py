"""Pre-fetch everything generate_intro_v3.py needs so the GPU job never waits on the network."""
from huggingface_hub import hf_hub_download, snapshot_download

for f in ("ltxv-2b-0.9.8-distilled.safetensors", "ltxv-spatial-upscaler-0.9.8.safetensors"):
    print("->", hf_hub_download(repo_id="Lightricks/LTX-Video", filename=f, repo_type="model"), flush=True)
print("->", snapshot_download("PixArt-alpha/PixArt-XL-2-1024-MS",
                              allow_patterns=["text_encoder/*", "tokenizer/*", "model_index.json"]), flush=True)
print("DOWNLOAD DONE")
