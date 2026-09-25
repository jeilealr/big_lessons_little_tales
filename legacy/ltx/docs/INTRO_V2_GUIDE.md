# TheWebtoonsCorner Intro V2 — LTX-Video guide

This project generates a short channel intro from deterministic keyframes and
LTX-Video motion synthesis. The book stays centered, the TWC logo is placed on
its cover, manga pages orbit it, and the existing intro soundtrack is added to
the final video.

## Model license — read before generation

The repository source code is Apache-2.0, but this workflow uses these model
weights:

- `ltxv-2b-0.9.8-distilled.safetensors`
- `ltxv-spatial-upscaler-0.9.8.safetensors`

Both are covered by the **LTXV Open Weights License 0.X**, not Apache-2.0:

<https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt>

As of 2026-09-21, the license grants a royalty-free license for uses that obey
its restrictions, but entities with annual revenue of at least USD 10 million
must obtain Lightricks' paid commercial-use license. It also requires generated
content to be expressly and intelligibly disclosed as machine generated. Read
the complete license yourself; this summary is not legal advice.

The pipeline also downloads the text encoder from
`PixArt-alpha/PixArt-XL-2-1024-MS`, which is marked CreativeML Open RAIL++-M:

<https://huggingface.co/PixArt-alpha/PixArt-XL-2-1024-MS>

Suggested YouTube description disclosure:

> Portions of this video were generated with AI using LTX-Video.

The script will not download or load model weights unless you explicitly pass
`--accept-ltx-license`.

## Files used by default

- Logo: `img/watermark_big.png`
- Manga pages: `Mangas/Surviving_the_Game_as_a_Barbarian/chp1/`
- Soundtrack: `Intro/Intro_channel_video.mov`
- Final video: `Intro/Intro_channel_video_v2.mov`
- Intermediate runs: `Intro/intro_v2_work/<timestamp>/`

All paths are resolved from the channel workspace, so the command can be run
from any directory.

## 1. Create only the keyframes (no model download)

```bash
conda run -n ltxvideo python \
  /Users/lealroja/Documents/youtube/TheWebtoonsCorner/repositories/LTX-Video/generate_intro_v2.py \
  --dry-run
```

Open the two printed PNG paths and check the composition before generation.

## 2. Generate a smaller preview

After reviewing and accepting the linked licenses:

```bash
conda run -n ltxvideo python \
  /Users/lealroja/Documents/youtube/TheWebtoonsCorner/repositories/LTX-Video/generate_intro_v2.py \
  --preview \
  --accept-ltx-license
```

The first real run downloads several gigabytes of weights. On Apple Silicon,
generation may be slow and may use substantial unified memory. The final file
is still encoded as a 1920x1080 MOV; `--preview` reduces the generated detail
and duration to make testing cheaper.

## 3. Generate the full default intro

```bash
conda run -n ltxvideo python \
  /Users/lealroja/Documents/youtube/TheWebtoonsCorner/repositories/LTX-Video/generate_intro_v2.py \
  --accept-ltx-license
```

If the output already exists and you intentionally want to replace it, append
`--force`.

## Useful variations

Use pages from another chapter and save a separate version:

```bash
conda run -n ltxvideo python \
  /Users/lealroja/Documents/youtube/TheWebtoonsCorner/repositories/LTX-Video/generate_intro_v2.py \
  --pages-dir /Users/lealroja/Documents/youtube/TheWebtoonsCorner/Mangas/Surviving_the_Game_as_a_Barbarian/chp2 \
  --output /Users/lealroja/Documents/youtube/TheWebtoonsCorner/Intro/Intro_channel_video_v2_chp2.mov \
  --seed 20260922 \
  --accept-ltx-license
```

Use different audio:

```bash
conda run -n ltxvideo python \
  /Users/lealroja/Documents/youtube/TheWebtoonsCorner/repositories/LTX-Video/generate_intro_v2.py \
  --audio-source /absolute/path/to/owned-or-licensed-audio.wav \
  --output /Users/lealroja/Documents/youtube/TheWebtoonsCorner/Intro/Intro_channel_video_v2_alt_audio.mov \
  --accept-ltx-license
```

Only use audio, manga panels, logos, and other source material for which you
have the necessary rights. Reusing the reference intro's soundtrack does not
create new rights in that soundtrack.

## Main options

```text
--preview                 512x288, 65 frames; quicker test
--dry-run                 keyframes only; never loads model weights
--accept-ltx-license      required for model generation
--pages-dir PATH          folder containing source manga images
--audio-source PATH       soundtrack or video containing an audio stream
--output PATH             final MOV location
--seed INTEGER            produces a different motion variation
--width/--height          generation resolution
--num-frames INTEGER      must be 8n+1 for best compatibility
--fps INTEGER             output frame rate
--force                   replace an existing final output
```

The script keeps timestamped raw renders and keyframes so failed or alternative
runs can be inspected without overwriting previous attempts.
