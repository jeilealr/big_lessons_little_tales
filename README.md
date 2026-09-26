# twc_video

Felt-animal fables for children, made with open video models on LUMI.

Every story is a data file (`stories/<slug>/story.yaml`): a style bible, frozen
character and location descriptions, and scenes broken into shots. The tools
turn it into consistent pictures: the same lion and the same mouse, in the same
forest, from scene to scene. Narration, voices and music are added outside this
repo (ElevenLabs); here we make the video, plus optional background ambience.

First story: **The Lion and the Mouse**.

## How a story gets made

```
story.yaml -> design -> character pack -> LoRA -> keyframes -> shots -> post -> edit
```

| Stage | Tool | What it produces |
|---|---|---|
| Story bible | `stories/<slug>/story.yaml` | the single source of truth for style, characters, places, scenes |
| Design | `production/design.py` | candidate stills; the chosen canonical per character and location |
| Character pack | `character/character.py` + `stories/<slug>/packs/*.yaml` | turns and story poses, each starting from the canonical |
| LoRA | `lora/` (musubi-tuner) | a small model per main character, trained on the pack |
| Keyframes | `production/keyframe.py` | a shot's first frame: character cut out (BiRefNet) and placed in the location |
| Shots | `production/shot.py` | Wan 2.2 image-to-video from the keyframe, one action per shot |
| Post | `twc/post.py` | RIFE 16->30 fps, Real-ESRGAN to 1080p, grade |

**Read [docs/production-guide.md](docs/production-guide.md)**: the complete
guide, with the results and the rules measured along the way.

## Layout

```
stories/      one folder per story: story.yaml (bible, scenes, shots) and packs/
production/   design, keyframes, shots, text-only baseline
character/    character packs (poses and turns) for story characters and tests
lora/         dataset builder, training, evaluation (musubi-tuner)
twc/          shared package: paths, ffmpeg helpers, Wan wrapper, post-processing
lumi/         container wrapper, two venvs, multi-GPU task runner, env rebuild
docs/         production guide, character consistency, licensing, LUMI, provenance
felt/         the first felt-animal test (text-to-video)
intro/, procedural/, audio/, legacy/   the channel intro and its history
work/         generated intermediates (git-ignored)
```

## Quick start (LUMI)

```bash
cd /scratch/project_465002727/jelealro
W=twc_video/lumi/run_in_container.sh
$W python twc_video/production/design.py prompt              # the design prompts
$W python twc_video/production/shot.py --scene 1 --shot s01_establish --dry-run
# GPU work: one command per line in a task file, several GCDs per job
sbatch --ntasks=4 --gpus-per-node=4 --mem=480G twc_video/lumi/run_tasks.sbatch tasks.txt
```

## Docs

- [Production guide](docs/production-guide.md): story to finished shots, with measured results
- [Character consistency](docs/character-consistency.md): the first experiments, on a felt fox
- [Licensing](docs/licensing.md): every model and library, checked for a monetised channel
- [Running on LUMI](docs/lumi.md): jobs, multi-GPU tasks, times, solved gotchas
- [Provenance](docs/provenance.md): no third-party repo was modified
- [The intro](docs/intro.md): the channel intro and how it evolved
