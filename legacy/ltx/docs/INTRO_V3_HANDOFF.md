# Intro V3 — handoff brief

Paste this whole file into Claude Code running in
`/Users/lealroja/Documents/youtube/TheWebtoonsCorner`.

## Goal

Render a 7-second channel intro for "The Webtoons Corner" with LTX-Video, then
verify it and report back. The script is written and validated; it has never
completed a real generation because of a Hugging Face auth problem (below).

## Layout

- Repo: `repositories/LTX-Video` (commit `4b2d053`, Apache 2.0 code)
- Conda env: `ltxvideo`
- Script: `repositories/LTX-Video/generate_intro_v3.py`
- Guide: `repositories/LTX-Video/INTRO_V3_GUIDE.md`
- Reference stills: `Intro/reference_img/1.png` … `6.png`, all 1672x941, 16:9
- Soundtrack source: `Intro/Intro_channel_video.mov` (6.016 s, looped to fit)
- Output: `Intro/Intro_channel_video_v3.mov`
- Segment cache: `Intro/intro_v3_work/segments/<res>_<fps>_seed<n>/`

## How the script works

Six approved stills, five transitions. Each segment is one LTX generation
conditioned on its own start image (strength 1.0) and end image (strength 0.92,
`--end-strength`), with a prompt written for that transition. The five clips are
concatenated with the duplicated frame at each seam dropped, retimed to exactly
7.000 s, scaled to 1920x1080 at 30 fps, and given the soundtrack with fades.

Frame counts come from a 3.5/4/3.5/3.5/3.5 weighting snapped to the 8k+1 counts
LTX requires: 33/41/33/33/33 at 24 fps. That is 169 frames after seam dedup =
7.04 s, retimed by x0.994 — a 0.6% change, invisible.

Segments are cached by name and frame count, so a rerun only generates what is
missing. `--only N` forces one transition to regenerate; `--redo` forces all.

An earlier `generate_intro_v2.py` synthesised its own keyframes and they were
bad. V3 replaces that approach entirely. Do not reuse v2's keyframe code, and
note that v2 read real manga panels from `Mangas/...` while v3 deliberately
does not — its only image inputs are `Intro/reference_img/`.

## Current blocker

`--preview --accept-ltx-license` fails during the checkpoint download:

```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url:
  https://huggingface.co/Lightricks/LTX-Video/resolve/main/ltxv-2b-0.9.8-distilled.safetensors
huggingface_hub.errors.RepositoryNotFoundError: 401 Client Error
OAuth token has expired: "exp" claim timestamp check failed
```

The repo is public and not gated. The cause is the last line: a stored Hugging
Face OAuth token has expired, `huggingface_hub` sends it anyway, and HF rejects
the request. The "Repository Not Found" wording is misleading — the file is
downloadable anonymously.

Try in this order:

1. `HF_HUB_DISABLE_IMPLICIT_TOKEN=1` in front of the command, which stops the
   token being sent to public repos and changes nothing on disk.
2. `conda run -n ltxvideo huggingface-cli logout` to clear the dead credential.
3. Only if a token is wanted for other work: the user creates a fresh read token
   at huggingface.co/settings/tokens and runs `huggingface-cli login` themselves.
   Do not ask for, read, echo or store the token value.

## Commands

```bash
cd /Users/lealroja/Documents/youtube/TheWebtoonsCorner

# validate inputs, no model, no download
conda run -n ltxvideo python repositories/LTX-Video/generate_intro_v3.py --dry-run

# low-res test, 512x288, 25 frames per segment; downloads weights once
HF_HUB_DISABLE_IMPLICIT_TOKEN=1 conda run -n ltxvideo python \
  repositories/LTX-Video/generate_intro_v3.py --preview --accept-ltx-license

# full render
HF_HUB_DISABLE_IMPLICIT_TOKEN=1 conda run -n ltxvideo python \
  repositories/LTX-Video/generate_intro_v3.py --accept-ltx-license --force

# redo one transition (1-5) after changing its prompt or reference image
HF_HUB_DISABLE_IMPLICIT_TOKEN=1 conda run -n ltxvideo python \
  repositories/LTX-Video/generate_intro_v3.py --only 3 --accept-ltx-license --force
```

Preview and full runs write to the same output path, hence `--force` on the full
run. They cache separately, so preview clips are not lost.

First download is ~6.34 GB for the checkpoint, ~505 MB for the upscaler, plus
the text encoder. Expect several minutes per segment on MPS.

## What is already verified

Run on this machine and passing: `py_compile`; `--dry-run`; the `--segment-frames`
8k+1 guard; the `--only` range guard; and the full concat -> retime -> mux path
exercised with stand-in clips built from the reference stills, producing
1920x1080 at 30 fps, exactly 7.000000 s, 210 frames, PCM 48 kHz stereo, with the
seam dedup landing on the correct 169-frame concat.

Never executed: LTX itself. No segment has been generated.

## Gotchas

- **Audio must stay PCM.** The output is a `.mov` with `pcm_s16le`, not AAC.
  DaVinci Resolve decodes AAC-in-MOV unreliably: it draws the waveform in the
  timeline and then renders silence. This already cost a day on the V1 intro. Do
  not "optimise" the encode to AAC.
- Everything in this project is 48 kHz end to end.
- `--segment-frames` must be 8k+1 (25, 33, 41, 49...). Omit it to let the weights
  size each transition.
- Each segment uses `seed + index` so two similar prompts do not land on the same
  noise and read as the same shot twice.
- Changing `--width`, `--height`, `--fps` or `--seed` starts a fresh cache
  directory; old clips are kept.

## What to check in the result

1. Does each segment actually arrive at its end image, or snap onto it in the
   last few frames? If it snaps, lower `--end-strength` (default 0.92).
   If it drifts and no longer matches the next segment's opening, raise it.
2. Do the seams read as one continuous shot?
3. Is the book identity stable across all five segments — same cover, same TWC
   emblem, no second book, no invented text?

Judge these at preview resolution before paying for the full render.

## Licensing, already researched

Repo code is Apache 2.0. The `ltxv-2b-0.9.8-distilled` checkpoint and the 0.9.8
upscaler are under the LTXV Open Weights License 0.X: paid commercial licensing
is reserved for entities with annual revenue of at least $10,000,000, and
Lightricks "claims no rights in the Output you generate using the Model". Below
that threshold, monetised use is permitted subject to the restrictions, one of
which is disclosing that content is machine generated. The text encoder comes
from PixArt under CreativeML Open RAIL++-M. YouTube description line:

> Portions of this video were generated with AI using LTX-Video.

The reference stills are the user's own work and contain no manga artwork, so
the intro carries no third-party image rights. Not legal advice.
