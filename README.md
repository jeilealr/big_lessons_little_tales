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

Current work: **The Lion and the Mouse, v4: still images under owner review**
(status 2026-10-02). Start with the [v4 review packet](stories/lion_and_mouse_v4/README.md)
and its [readable prompts](stories/lion_and_mouse_v4/prompts/).
V3 has been rendered and reviewed by the owner; v2/v3 remain historical inputs.
Next stories in preparation (script and shot plan ready for review): [The Tortoise and the Hare](stories/tortoise_and_hare_v1/README.md) and [The Boy Who Cried Wolf](stories/boy_who_cried_wolf_v1/README.md).
V4 stills were made from 2026-09-30 to 2026-10-02 with GPT's built-in image
tool and the Gemini API (139 of 140 image records accepted, one missing); the
owner now makes new images personally. The English narration exists. **No v4
clip has been rendered**; there is no runnable v4 `story.yaml` yet.

**New here? See [Where to find things](#where-to-find-things) below.**

## How a story gets made

```
script + shot order review -> approved cast/places/props -> paired keyframes
-> individual pilot/clips -> owner take selection -> separately requested animatic -> post/edit
```

| Stage | Tool | What it produces |
|---|---|---|
| Story and prompt plan | v4 `visual_bible.json`, `prompt_manifest.json`; later approved `story.yaml` | complete image/video prompts, state/geometry records and each accepted image's result; current render scripts require story YAML |
| Narration | v4: `dialogue_coverage.json` + `voice/narrate_scenes.py`; v2: `stories/<slug>/narration/<lang>.yaml`; `voice/` | the spoken lines; one WAV per scene with Gemini voices; `production/timing_sheet.py` maps lines to shots |
| Cast | v4: `character/characters/<Name>/v4/`; v3: `character/characters/<Name>/v3/` + `production/install_pack.py` | canonical, views, expressions, actions, story states (v4 made with image models, see `docs/gemini-images.md`) |
| Places | v4: `character/locations/v4/<place>/` (bible `locations`); v3: `character/locations/<place>/` + `stories/<slug>/locations_dna.yaml` | empty plates, one per lighting |
| Scene stills (v4) | `character/characters/interactions/v4/keyframes/` | the start and end image of every shot, made with image models and recorded in the manifest |
| Props (optional) | `production/design.py` | Wan 2.2 stills of places and props (the v1/v2 method) |
| Poses (optional) | `character/character.py` + `stories/<slug>/packs/*.yaml` | extra poses animated from the canonical |
| Keyframes | `production/compose_keyframes.py` (`compose:` in each shot) | start/end frames: characters cut out (BiRefNet) and placed; a contact sheet to check |
| Shots | `production/shot.py` (`--fast`) | Wan 2.2 image-to-video between keyframes, one action per shot |
| Animatic (separate owner request) | `production/animatic.py` | assembly after actual take selection; source choices and dialogue timing need manual review |
| Post | `bllt/post.py` | RIFE 16->30 fps, Real-ESRGAN to 1080p, grade |

## Consistent images (start here before any image)

Every story keeps one visual bible (`stories/<slug>/visual_bible.json`): canonical character
descriptions written from the approved canonical images, the size lineup, locked location plates
and camera setups with measured character sizes. All image and video prompts in
`prompt_manifest.json` are templates built from it:

```bash
python3 production/image_prompts.py build   # render the templates
python3 production/image_prompts.py lint    # must report 0 errors
python3 production/image_prompts.py md      # readable prompts in stories/<slug>/prompts/
python3 production/image_prompts.py review <record> --image <candidate>   # side-by-side gate
python3 production/image_prompts.py --story lion_and_mouse_v4 new-story <slug>   # skeleton for a new story
```

Claude Code loads the repo skill `consistent-image-prompts` (`.claude/skills/`) for any image
work; it walks through the setup for a new story, prompt writing, generation and review.
Details: `docs/image-prompts.md`; rules: `docs/creation-rules.md` (CR-11 to CR-18).

To make an image yourself: `python3 production/image_prompts.py show <record>` (or
`stories/<slug>/prompts/*.md`) gives the exact prompt; attach the references it lists, in that
order.

## Layout

```
stories/     one folder per story: story.yaml, story.txt, narration/, packs/
production/  install_pack, design, keyframe, shot, animatic, image_prompts
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
| **review the next iteration** | **[V4 packet](stories/lion_and_mouse_v4/README.md)**: status, open issues, owner observations, proposed sequence and complete prompts |
| **make or remake a v4 image** | **[Readable prompts](stories/lion_and_mouse_v4/prompts/)**: every image's exact prompt and references; `python3 production/image_prompts.py show <record>` |
| make v4 still images with the Gemini API | [docs/gemini-images.md](docs/gemini-images.md): workflow, model choice, cost, lessons |
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
| V4 prompt records and their results | `stories/lion_and_mouse_v4/prompt_manifest.json`; each record names its image path, hash and review |
| V4 character images (canonical, references, 11 expressions each) | `character/characters/<Name>/v4/` |
| V4 scene start/end images | `character/characters/interactions/v4/keyframes/` |
| V4 location plates and props | `character/locations/v4/` |
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
- [V4 prompts](stories/lion_and_mouse_v4/prompts/): every v4 image and video prompt, rendered from the bible
- [Prompt records](docs/prompt-records.md): exact text, references, revisions and execution provenance
- [V4 preflight](docs/v4-preflight.md): image, pair, clip and assembly gates
- [Gemini images](docs/gemini-images.md): making v4 stills with the Gemini API

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
