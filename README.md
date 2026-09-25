# twc_video

Video production for **The Webtoons Corner**: generative shots (Wan 2.2), code-rendered
motion graphics, learned post-processing and synthesised audio, run on LUMI.

## Two render backends, one pipeline

| | Generative (Wan 2.2) | Procedural (code) |
|---|---|---|
| Good at | organic motion, felt, paper, light, camera moves | logos, text, motion graphics, anything that must be exact |
| Cost | ~2 GPU-hours per 5 s shot | minutes on a CPU |
| Lives in | `twc/wan.py`, `intro/`, `felt/`, `character/` | `procedural/` |

Both feed the same post chain (`twc/post.py`: RIFE + Real-ESRGAN + grade) and the same
audio treatment (`twc/media.finish`: PCM 48 kHz in MOV, because Resolve decodes AAC-in-MOV
unreliably).

## Layout

```
twc/          shared package: paths, ffmpeg helpers, Wan wrapper, post-processing
character/    consistent characters: sheets -> canonical still -> angles -> shots -> LoRA dataset
intro/        the channel intro (current: intro_v4.py + hybrid_cut.py)
procedural/   code-rendered ident / logo reveal
felt/         felt-animal text-to-video test
audio/        synthesised score and lullaby (original, licence-free)
lumi/         container wrapper, env, sbatch files, multi-GPU task runner, env rebuild
legacy/ltx/   the LTX-Video era scripts, configs, guides and experiments
docs/         guides (start with character-consistency.md)
assets/       Cinzel font (SIL OFL)
work/         generated intermediates (git-ignored)
```

Inputs that are not code (reference stills, emblem, finished videos, soundtracks) live in
the channel folder next to this repo (`../Intro`, `../audio`); see `twc/paths.py`.

## Quick start (LUMI)

```bash
cd /scratch/project_465002727/jelealro
W=twc_video/lumi/run_in_container.sh
$W python twc_video/character/character.py prompt            # see how prompts are built
$W python twc_video/procedural/twc_ident.py --still 9.5      # render one reveal frame
sbatch --ntasks=3 --gpus-per-node=3 --mem=400G twc_video/lumi/run_tasks.sbatch tasks.txt
```

## Docs

- [Character and set consistency](docs/character-consistency.md): the step-by-step guide
- [The intro](docs/intro.md): what was tried, what worked, how it is made now
- [Provenance](docs/provenance.md): what was changed where (no third-party repo was modified)
- [Licensing](docs/licensing.md): everything used, checked for a monetised channel
- [Running on LUMI](docs/lumi.md): jobs, multi-GPU tasks, measured times, solved gotchas
