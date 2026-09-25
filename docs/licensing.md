# Licensing (for a monetised channel)

Checked from the installed package metadata and the model cards, 2026-09-25.
Not legal advice.

## Used

| Component | Licence | Notes |
|---|---|---|
| Wan 2.2 weights (I2V/T2V A14B) | Apache-2.0 | no revenue cap, no gate |
| LTX-Video 0.9.8 weights (legacy scripts only) | LTXV Open Weights License | free under $10M annual revenue; disclose AI generation |
| RIFE code + weights | MIT (Megvii) | |
| Real-ESRGAN x4plus weights | BSD-3-Clause | |
| Cinzel typeface (`assets/fonts/`) | SIL Open Font License 1.1 | bundled with its `OFL.txt` |
| diffusers, transformers, safetensors, huggingface-hub, ftfy | Apache-2.0 | |
| torch, av, numpy, scipy | BSD-3-Clause | |
| opencv-python-headless | Apache-2.0 | |
| spandrel, PyYAML | MIT | |
| pillow | MIT-CMU (HPND) | |
| imageio-ffmpeg | BSD-2-Clause | **the ffmpeg binary it ships is GPLv3** (built with x264). Using a GPL tool does not put the videos under the GPL; do not commit the binary into a repo. |
| Music (`audio/`) and procedural visuals (`procedural/`) | our own code | synthesised from oscillators, noise and code; no samples, no model weights |
| Channel emblem and reference stills | the author's own | kept outside the repo (`Intro/reference_img/`) |

## Considered and rejected

| Component | Why not |
|---|---|
| HunyuanVideo 1.5 | its licence states it "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA" |
| MusicGen | weights are CC-BY-NC (non-commercial) |
| Stable Audio Open | gated, and its community licence caps revenue |
| Wan 2.5 | not released as open weights |

YouTube description line: *Portions of this video were generated with AI.*
