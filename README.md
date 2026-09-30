# Big Lessons, Little Tales

Felt-animal fables for children, each with a kind message, made with open
video models on the LUMI supercomputer, for the YouTube channel
*Big Lessons, Little Tales*.

Every story is a data file (`stories/<slug>/story.yaml`): a style bible,
frozen character and location descriptions, the narration, and scenes broken
into shots. The tools compose references and generate candidate clips; visual
review checks that the same characters and forest remain consistent across shots. Narration and character
voices come from Gemini TTS (`voice/`); music and sound effects from
ElevenLabs; the final mix is done in DaVinci Resolve.

Current work: **The Lion and the Mouse, v4 documentation and prompt plan**.
Start with the [v4 review packet](stories/lion_and_mouse_v4/README.md).
V3 has been rendered and reviewed by the owner; v2/v3 remain historical inputs.
V4 images and clips have **not** been generated. The script order and revised
canonicals need review before production.

**New here? See [Where to find things](#where-to-find-things) below.**

## How a story gets made

```
script + shot order review -> approved cast/places/props -> paired keyframes
-> individual pilot/clips -> owner take selection -> separately requested animatic -> post/edit
```

| Stage | Tool | What it produces |
|---|---|---|
| Story and prompt plan | v4 `visual_bible.json`, `prompt_manifest.json`; later approved `story.yaml` | complete draft image/video prompts and state/geometry records; current scripts require story YAML |
| Narration | `stories/<slug>/narration/<lang>.yaml`, `voice/` | the script per language; Gemini voices |
| Cast | `character/characters/<Name>/v3/` + `production/install_pack.py` | owner-made canonical, views, expressions, actions, story states |
| Places | `character/locations/<place>/` + `stories/<slug>/locations_dna.yaml` | owner-made empty plates, one per lighting |
| Props (optional) | `production/design.py` | Wan 2.2 stills of places and props (the v1/v2 method) |
| Poses (optional) | `character/character.py` + `stories/<slug>/packs/*.yaml` | extra poses animated from the canonical |
| Keyframes | `production/compose_keyframes.py` (`compose:` in each shot) | start/end frames: characters cut out (BiRefNet) and placed; a contact sheet to check |
| Shots | `production/shot.py` (`--fast`) | Wan 2.2 image-to-video between keyframes, one action per shot |
| Animatic (separate owner request) | `production/animatic.py` | assembly after actual take selection; source choices and dialogue timing need manual review |
| Post | `bllt/post.py` | RIFE 16->30 fps, Real-ESRGAN to 1080p, grade |

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

## Quick start (LUMI; existing v3 example)

```bash
cd /scratch/project_465002727/jelealro/big_lessons_little_tales   # always from the repo root
W=lumi/run_in_container.sh
$W python production/shot.py --story lion_and_mouse_v3 --scene 1 --shot s01_milo_explores --fast --dry-run
# GPU work: one command per line in a task file (commands run from the repo root)
sbatch --ntasks=3 --gpus-per-node=3 --mem=330G lumi/run_tasks.sbatch work/tasks/<name>.txt
# voices (no GPU)
source voice/gemini_env.sh && python voice/list_voices.py
```

V4 has no runnable `story.yaml` yet. These are command examples, not a v4 task list.
Pass the story slug explicitly; some tools default to v2.

Machine-specific paths (venvs, model cache, container, Slurm account) are all
in `lumi/site.sh`; nothing depends on the repo's folder name.

## Where to find things

### Guides: which one to read

| I want to... | Read |
|---|---|
| **review the next iteration** | **[V4 packet](stories/lion_and_mouse_v4/README.md)**: owner observations, proposed sequence and complete draft prompts |
| preserve exact prompts and references | [Prompt records](docs/prompt-records.md) |
| approve images and prepare clip jobs | [V4 preflight](docs/v4-preflight.md): manual gates and current tooling gaps |
| **write a script, an image prompt or a shot description** | **[docs/creation-rules.md](docs/creation-rules.md)**: rules for scripts, character and location images, interactions and shots, identity, scale, pair, prop, motion and review requirements |
| understand the whole pipeline, story to finished shots | [docs/production-guide.md](docs/production-guide.md) |
| check a video-prompt rule and the evidence behind it | [docs/prompting.md](docs/prompting.md): every measured rule, a checklist, the results log |
| know what went wrong before and how it was fixed | [docs/findings-and-risks.md](docs/findings-and-risks.md) |
| work with voices (Gemini TTS) | [voice/README.md](voice/README.md) |
| run things on LUMI (jobs, times, gotchas) | [docs/lumi.md](docs/lumi.md) |
| check a model's or service's licence | [docs/licensing.md](docs/licensing.md), [docs/google_gemini_terms_question.md](docs/google_gemini_terms_question.md) |
| see the current state, standing decisions and commands (also for AI agents) | [CLAUDE.md](CLAUDE.md) |
| read the first consistency experiments | [docs/character-consistency.md](docs/character-consistency.md) |
| know where code came from | [docs/provenance.md](docs/provenance.md) |

### Historical runtime story files (example: `stories/lion_and_mouse_v3/`)

| File | What it is |
|---|---|
| `script_dialog_en.txt` | the story text, with narrator and character lines |
| `story.yaml` | the story bible: style, characters, places, voices, scenes and every shot |
| `locations_dna.yaml` | each place: description, what must never change, lighting, plates |
| `TODO_images.md` | historical short prompts plus shared style blocks; not a complete executed prompt log |
| `ASSETS.md` | why those images, and the beat-by-beat shot plan |
| `../lion_and_mouse_v2/owner_review.yaml` | the owner's verdict on every v2 clip |

### Existing images, voices and generated files

| What | Where |
|---|---|
| V4 planned references and prompts (not generated) | `stories/lion_and_mouse_v4/prompt_manifest.json`; each record names its future asset path |
| Existing v3 character packs (canonical, views, expressions, actions, story states) | `character/characters/<Name>/v3/` |
| Character DNA (the written identity) | `character/characters/<Name>/v3/dna.yaml` |
| Two-character images | `character/characters/interactions/v3/` |
| Location plates | `character/locations/<place>/` |
| Saved voices (id, design prompt, samples in 6 languages) | `voice/cast/<role>/`, `voice/narrators/<name>/` |
| Rendered clips, keyframes, animatic (not in git) | `work/stories/<slug>/shots/`, `keyframes/`, `animatic.mp4` |
| GPU task files and logs | `work/tasks/`, `/scratch/project_465002727/jelealro/slurm_logs/` |
| Evidence images used in the docs | `docs/img/` |

## All docs

- [V4 review packet](stories/lion_and_mouse_v4/README.md): start here for the fourth iteration
- [Prompt records](docs/prompt-records.md): exact text, references, revisions and execution provenance
- [V4 preflight](docs/v4-preflight.md): image, pair, clip and assembly gates

- [CLAUDE.md](CLAUDE.md): operating manual and current state
- [Creation rules](docs/creation-rules.md): how to write scripts, image prompts and shot descriptions
- [Production guide](docs/production-guide.md): story to finished shots, with measured results
- [Writing prompts](docs/prompting.md): every measured prompt rule, and a checklist
- [Findings and risks](docs/findings-and-risks.md): every problem and its fix
- [Voices](voice/README.md): Gemini TTS setup, saved voices, languages
- [Licensing](docs/licensing.md): every model and service, checked for a monetised channel
- [Running on LUMI](docs/lumi.md): jobs, multi-GPU tasks, times, gotchas
- [Character consistency](docs/character-consistency.md): the first experiments
- [Provenance](docs/provenance.md): what came from where
