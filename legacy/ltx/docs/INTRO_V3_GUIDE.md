# Intro V3 — keyframe-driven

V2 drew its own conditioning frames and they came out badly. V3 draws nothing.
It takes the six approved stills in `Intro/reference_img/` (`1.png` … `6.png`)
and asks LTX-Video to animate the five transitions between them, one segment
per transition, each pinned to its own start and end image.

| # | Transition | Prompt | Frames | Share of the cut |
|---|-----------|--------|--------|------------------|
| 1 | 1 → 2 | The book awakens | 33 | ~1.4 s |
| 2 | 2 → 3 | The page tornado | 41 | ~1.7 s |
| 3 | 3 → 4 | Rotation inside the vortex | 33 | ~1.4 s |
| 4 | 4 → 5 | Dive toward the stories | 33 | ~1.4 s |
| 5 | 5 → 6 | Enter the book, TWC reveal | 33 | ~1.4 s |

Frame counts come from the suggested 3.5 / 4 / 3.5 / 3.5 / 3.5 weighting,
snapped to the 8k+1 counts LTX accepts. The five clips are concatenated (the
duplicated frame at each seam is dropped), retimed to exactly 7.000 s, scaled to
1920×1080 at 30 fps, and given the reference soundtrack.

## Running it

Validate inputs without touching the model:

```bash
conda run -n ltxvideo python \
  repositories/LTX-Video/generate_intro_v3.py --dry-run
```

Low-resolution test (512×288, 25 frames per segment):

```bash
conda run -n ltxvideo python \
  repositories/LTX-Video/generate_intro_v3.py --preview --accept-ltx-license
```

Full render:

```bash
conda run -n ltxvideo python \
  repositories/LTX-Video/generate_intro_v3.py --accept-ltx-license
```

Output: `Intro/Intro_channel_video_v3.mov`.

## Iterating on one transition

Segments are cached under
`Intro/intro_v3_work/segments/<resolution>_<fps>_<seed>/`, so a rerun only
generates what is missing. To redo a single transition after editing its prompt
or its reference image:

```bash
conda run -n ltxvideo python \
  repositories/LTX-Video/generate_intro_v3.py --only 3 --accept-ltx-license --force
```

`--redo` rebuilds all five. Changing `--width`, `--height`, `--fps` or `--seed`
starts a new cache directory, so the old clips are kept.

## Knobs worth knowing

- `--end-strength` (default 0.92) — how hard the last frame is pinned to the end
  reference. Lower it if a segment snaps abruptly onto its final image; raise it
  if a segment drifts and no longer matches the next one's opening.
- `--image-cond-noise-scale` (default 0.08) — more noise gives the model more
  freedom and less fidelity to the reference stills.
- `--duration` (default 7.0) — frame allocation and the final retime both follow
  it, so changing it keeps the relative pacing intact.
- Each segment uses `seed + its index`, so two similar prompts do not land on
  the same noise and read as the same shot twice.

## Audio format

The output is a `.mov` with **PCM** audio, not AAC. Resolve decodes AAC-in-MOV
unreliably: it draws the waveform in the timeline and then renders silence. This
is the same failure that cost a day on the V1 intro, so the deliverable ships
uncompressed.

## Licensing

The repository code is Apache 2.0, but the `ltxv-2b-0.9.8-distilled` checkpoint
and the 0.9.8 upscaler are under the LTXV Open Weights License 0.X, which is why
weights are only downloaded after `--accept-ltx-license`. Under $10M annual
revenue, monetised use appears permitted subject to the license restrictions,
including disclosing that the content is AI-generated. Suggested line for the
YouTube description:

> Portions of this video were generated with AI using LTX-Video.

This is a practical summary, not legal advice.
