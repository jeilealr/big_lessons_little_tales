# The channel intro: how it evolved and how it is made now

A 10-second ident for The Webtoons Corner. Inputs: the approved stills in
`Intro/reference_img/` (`1.png` … `6.png`), the emblem `watermark_big.png`.

## What was tried, and what it taught

| Version | Approach | Lesson |
|---|---|---|
| LTX v3, 2B, preview | 5 transitions, each pinned to a start and end still | 25–33 frames per clip is too few: the model jumps to the end still in 3 frames and holds |
| LTX iterations 1–10 | more frames, 13B model, 720p, per-segment seeds, re-timed soundtrack | frames and model size fix the snap; long clips (73–97 f) make state changes hold then wipe |
| Wan 2.2 chain | same 5 transitions with Wan I2V-A14B (first + last frame) | clearly better motion: the cover hinges open for real |
| Wan story | only stills 1, 5, 6; the middle described in text | fewer forced stills read as one continuous shot |
| post chain | RIFE (16→30 fps) + Real-ESRGAN + grade instead of ffmpeg minterpolate + lanczos | resolves detail lanczos lost; keep grading as a separate cheap pass |
| procedural | every frame drawn by code (`procedural/twc_ident.py`) | the logo and wordmark are pixel-exact, which diffusion never managed |
| **hybrid** | Wan journey, then the procedural reveal, joined inside a white flash | **the best of both; the favourite** |

## Current approach: intro v4

1. **Wan I2V from `1.png` only** (`intro/intro_v4.py generate`), the journey
   described in text and ending in a white burst. Two variants: `white` forces
   the end with a white end frame, `open` relies on the prompt.
2. **Post**: RIFE + Real-ESRGAN, retimed so the white-out lands at the chosen
   hit time (`twc/post.py`).
3. **Reveal**: `procedural/twc_ident.py --hit T` and `audio/make_music.py
   --impact-at T`, both timed from the same hit.
4. **Cut**: `intro/hybrid_cut.py --cut T`, joined inside white (the Wan side is
   ramped to full white over 0.17 s so luma is continuous across the join).

Changing where the logo lands is one number, `T`, plus a two-minute CPU
re-render.
