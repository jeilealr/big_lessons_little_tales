from huggingface_hub import hf_hub_download
print("->", hf_hub_download(repo_id="Lightricks/LTX-Video", filename="ltxv-13b-0.9.8-distilled.safetensors", repo_type="model"), flush=True)
print("DOWNLOAD DONE")
