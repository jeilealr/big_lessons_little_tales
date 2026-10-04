# Licensing (for a monetised channel)

Checked from the installed package metadata and the model cards, 2026-09-25.
Not legal advice.

## Used

| Component | Licence | Notes |
|---|---|---|
| Wan 2.2 weights (I2V/T2V A14B) | Apache-2.0 | no revenue cap, no gate |
| LTX-Video 0.9.8 weights (legacy scripts only) | LTXV Open Weights License | free under $10M annual revenue; disclose AI generation |
| RIFE code + weights | MIT (Megvii) | |
| BiRefNet matting (`ZhengPeng7/BiRefNet`, revision pinned) | MIT | cuts characters out for keyframes and datasets |
| musubi-tuner (LoRA training, `ext/musubi-tuner`) | Apache-2.0 | its `wan/` code derives from Wan2.1 (Apache-2.0) |
| Wan 2.2 repackaged experts (`Comfy-Org/Wan_2.2_ComfyUI_Repackaged`), Wan 2.1 VAE and T5 | Apache-2.0 | the weights musubi-tuner trains on |
| kornia | Apache-2.0 | BiRefNet dependency |
| Real-ESRGAN x4plus weights | BSD-3-Clause | |
| diffusers, transformers, safetensors, huggingface-hub, ftfy | Apache-2.0 | |
| torch, av, numpy, scipy | BSD-3-Clause | |
| opencv-python-headless | Apache-2.0 | |
| spandrel, PyYAML | MIT | |
| pillow | MIT-CMU (HPND) | |
| imageio-ffmpeg | BSD-2-Clause | **the ffmpeg binary it ships is GPLv3** (built with x264). Using a GPL tool does not put the videos under the GPL; do not commit the binary into a repo. |
| Channel emblem and reference stills | the author's own | kept outside the repo (`Intro/reference_img/`) |
| v2 character pack (`character/characters/lion_and_mouse_v2/{Leo,Milo}/`) and v2 review frames | owner-made with an external image tool | **to record: which tool, and that its terms allow commercial use of outputs.** The video pipeline only reads these images; Wan outputs made from them are covered by Wan's Apache-2.0 row above |

## Added 2026-09-27

| Component | Licence / terms | Notes |
|---|---|---|
| Wan2.2-Lightning 4-step LoRAs (`lightx2v/Wan2.2-Lightning`, revision pinned in `bllt/wan.py`) | Apache-2.0 | fast mode (`--fast`) |
| Gemini 3.8 Flash TTS (Gemini API) | Gemini API Additional Terms | outputs owned by the user ("Google won't claim ownership"); SynthID watermark; paid ~$0.0135/min of audio (2026). Open question on the Age Requirements for a Made-for-kids channel: `docs/google_gemini_terms_question.md` |
| google-genai (client) | Apache-2.0 | `gemini_env` venv |
| Qwen-Image-Edit-2511 (`Qwen/Qwen-Image-Edit-2511`, pinned) | Apache-2.0 | downloaded, not used yet (`production/edit_image.py`) |
| Gemini image models (Nano Banana 2 Lite `gemini-3.1-flash-lite-image`, Nano Banana 2 `gemini-3.1-flash-image`, Nano Banana Pro `gemini-3-pro-image[-preview]`; Gemini API) | Gemini API Additional Terms (same as TTS row) | v4 stills since 2026-10-02 (`character/gemini_image.py`; `docs/gemini-images.md`). **To confirm before any output is used:** output ownership/commercial use for images, the SynthID watermark, preview-model terms, and the same Age Requirements question as the TTS row |
| GPT built-in image tool (OpenAI `image_gen`, used from Codex; manifest `result.tool` "built-in image_gen") | **not recorded** (added to this table by the 2026-10-02 documentation audit) | made the v4 r01 stills (2026-09-30 to 2026-10-02) and the in-place repairs after r05; about half of the accepted v4 images. **To record before any output is used:** which product and plan, output ownership and commercial use, and any restriction for a Made-for-kids channel |

## Considered and rejected

| Component | Why not |
|---|---|
| HunyuanVideo 1.5 | its licence states it "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA" |
| MusicGen | weights are CC-BY-NC (non-commercial) |
| Stable Audio Open | gated, and its community licence caps revenue |
| RMBG 1.4 / 2.0 (background removal) | "other" licences, non-commercial |
| Wan 2.5 | not released as open weights |

YouTube description line: *Portions of this video were generated with AI.*
