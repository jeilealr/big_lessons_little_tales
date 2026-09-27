# Big Lessons, Little Tales

Felt-animal fables for children, each with a kind message, made with open
video models on the LUMI supercomputer, for the YouTube channel
*Big Lessons, Little Tales*.

Every story is a data file (`stories/<slug>/story.yaml`): a style bible,
frozen character and location descriptions, the narration, and scenes broken
into shots. The tools turn it into consistent pictures: the same lion and the
same mouse, in the same forest, from shot to shot. Narration and character
voices come from Gemini TTS (`voice/`); music and sound effects from
ElevenLabs; the final mix is done in DaVinci Resolve.

Current story: **The Lion and the Mouse** (`stories/lion_and_mouse_v2/`).

## How a story gets made

```
story + narration -> cast (owner pack) -> places -> poses -> keyframes -> shots -> animatic -> post -> edit
```

| Stage | Tool | What it produces |
|---|---|---|
| Story bible | `stories/<slug>/story.yaml` | style, characters, places, voices, scenes, shots |
| Narration | `stories/<slug>/narration/<lang>.yaml`, `voice/` | the script per language; Gemini voices |
| Cast | `character/characters/<Name>/v2/` + `production/install_pack.py` | owner-made canonical, views, expressions, actions |
| Places and props | `production/design.py` | empty location plates, props (Wan 2.2 stills) |
| Poses | `character/character.py` + `stories/<slug>/packs/*.yaml` | extra poses from the canonical |
| Keyframes | `production/keyframe.py` (or `compose:` in a shot) | start/end frames: characters cut out (BiRefNet) and placed |
| Shots | `production/shot.py` (`--fast`) | Wan 2.2 image-to-video between keyframes, one action per shot |
| Animatic | `production/animatic.py` | the whole story at its pacing, with the narration |
| Post | `bllt/post.py` | RIFE 16->30 fps, Real-ESRGAN to 1080p, grade |

**Read [CLAUDE.md](CLAUDE.md) first** (current state, rules, commands), then
[docs/production-guide.md](docs/production-guide.md) and
[docs/prompting.md](docs/prompting.md).

## Layout

```
stories/     one folder per story: story.yaml, story.txt, narration/, packs/
production/  install_pack, design, keyframe, shot, animatic, scene_baseline
character/   character.py (pose clips) and characters/ (owner-made packs)
voice/       Gemini TTS: tools, saved voices (cast/, narrators/), samples
lora/        LoRA dataset builder, training, evaluation (musubi-tuner)
bllt/        shared package: paths, ffmpeg helpers, Wan wrapper, post-processing
lumi/        site.sh (machine paths), container wrapper, venvs, task runner
docs/        guides, measured rules, findings, licensing, LUMI, provenance
work/        everything generated (git-ignored)
```

## Quick start (LUMI)

```bash
cd /scratch/project_465002727/jelealro/big_lessons_little_tales   # always from the repo root
W=lumi/run_in_container.sh
$W python production/shot.py --scene 1 --shot s01_sleeps_3q --fast --dry-run
# GPU work: one command per line in a task file (commands run from the repo root)
sbatch --ntasks=3 --gpus-per-node=3 --mem=330G lumi/run_tasks.sbatch work/tasks/<name>.txt
# voices (no GPU)
source voice/gemini_env.sh && python voice/list_voices.py
```

Machine-specific paths (venvs, model cache, container, Slurm account) are all
in `lumi/site.sh`; nothing depends on the repo's folder name.

## Docs

- [CLAUDE.md](CLAUDE.md): operating manual and current state
- [Production guide](docs/production-guide.md): story to finished shots, with measured results
- [Writing prompts](docs/prompting.md): every measured prompt rule, and a checklist
- [Findings and risks](docs/findings-and-risks.md): every problem and its fix
- [Voices](voice/README.md): Gemini TTS setup, saved voices, languages
- [Licensing](docs/licensing.md): every model and service, checked for a monetised channel
- [Running on LUMI](docs/lumi.md): jobs, multi-GPU tasks, times, gotchas
- [Character consistency](docs/character-consistency.md): the first experiments
- [Provenance](docs/provenance.md): what came from where
