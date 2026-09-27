# CLAUDE.md: operating manual for agents working in this repo

Read this first. It is the durable memory of the project: what it is for, how
to run things on LUMI without repeating past failures, and where the knowledge
lives. Keep it current: when you learn something that would have saved you
time, add it here or to the doc it belongs in.

## What this repo is

**Big Lessons, Little Tales**: felt-animal fables for children, each with a
kind message, for the monetised YouTube channel of the same name (Made for
kids). Pictures: open video models (Wan 2.2) on the LUMI supercomputer.
Narration and character voices: Gemini 3.8 Flash TTS (`voice/`). Music and
sound effects: ElevenLabs (owner, paid plan). Final mix: DaVinci Resolve
(owner).

Repo: `/scratch/project_465002727/jelealro/big_lessons_little_tales`
(renamed from `twc_video` on 2026-09-27; GitHub
`jeilealr/big_lessons_little_tales`, private). Current story: **The Lion and
the Mouse, v2** (`stories/lion_and_mouse_v2/`).

## The owner's standing instructions

- Goal: professional, consistent videos (same characters and places across
  shots). Iterate until the result is genuinely good; show evidence (contact
  sheets) for every judgement.
- Everything used must be **licence-clean for a monetised channel**. Check a
  model's licence or service terms before using it; record it in
  `docs/licensing.md`. Rejected so far: HunyuanVideo (excludes the EU),
  MusicGen (CC-BY-NC), Stable Audio Open (revenue cap), RMBG 1.4/2.0
  (non-commercial); ElevenLabs-voice clones (third-party voices).
- **Git: the owner does all git** (add, commit, push). Agents do not run git
  commands unless asked (owner, 2026-09-27). Leave the tree ready for
  `git add . && git commit && git push`.
- Only run GPU jobs when you are sure they are ready: dry-run first (see
  "Before a GPU job").
- Keep the docs as a guide a person can learn from: why, measured results,
  images.
- Voices: one sample line per voice only; do not generate audio the owner has
  not asked for.

## Where the knowledge is

| Need | Read |
|---|---|
| Writing any prompt (shot, pose, design) | **`docs/prompting.md`**: every measured rule, a checklist, results log |
| Every problem found and its fix; gaps and risks | **`docs/findings-and-risks.md`** |
| The whole pipeline, story to shots | `docs/production-guide.md` |
| Voices (Gemini TTS) | **`voice/README.md`** |
| LUMI jobs, times, solved gotchas | `docs/lumi.md` |
| Licences and service terms | `docs/licensing.md`, `docs/google_gemini_terms_question.md` |
| Where code came from | `docs/provenance.md` |
| Story facts (characters, places, voices, scenes, shots) | `stories/<slug>/story.yaml`: the only place they live |
| The owner's story text | `stories/<slug>/story.txt`; narration per language `stories/<slug>/narration/<lang>.yaml` |
| Character packs (identity authority) | `character/characters/<Name>/v2/`, prompts in `character/characters/*.md` |

## Layout and paths

```
stories/<slug>/     story.yaml (bible, voices, scenes, shots), story.txt, narration/, packs/
production/         install_pack, design, keyframe, shot, animatic, scene_baseline
character/          character.py (pose clips); characters/ (owner-made packs)
voice/              Gemini TTS tools; cast/<role>/ and narrators/<name>/ (voice.yaml + samples)
lora/               LoRA dataset/training/eval (musubi-tuner); datasets/ is empty (v1 removed)
bllt/               package: paths, media (ffmpeg), wan (model wrapper), post (RIFE/ESRGAN/grade)
lumi/               site.sh, env*.sh, run_in_container.sh, run_tasks.sbatch, task_exec.sh, setup_env.sh
docs/               guides; docs/img/ evidence images
work/               everything generated (git-ignored); every output has a .json sidecar
```

- **Paths never depend on the repo's folder name.** Python derives them from
  `bllt/paths.py` (`REPO`, `WORK`, `story_work(slug)`, `story_audio(slug,
  lang)`); shell scripts from `lumi/site.sh`, the only file with
  machine-specific locations (project dir, venvs, HF cache, container, Slurm
  account, log dir). Moving or renaming the repo needs no edit; another
  machine or project needs `lumi/site.sh` plus the `#SBATCH` account/output
  lines in `lumi/run_tasks.sbatch`.
- **Everything runs from the repo root.** `run_in_container.sh` cd's there;
  task-file lines are written relative to it (`python production/shot.py ...`);
  submit `sbatch` from the repo root (the script checks).
- Per-story generated files: `work/stories/<slug>/` = `design/` (plates,
  props, installed canonicals), `characters/<name>/` (pack, pack16x9, poses,
  shots), `keyframes/`, `shots/`, `audio/<lang>/sceneNN.wav` (narration, for
  the animatic), `animatic*.mp4`. Task files: `work/tasks/` (old ones in
  `work/tasks/archive/`, with pre-rename paths). LoRAs: `work/lora/`.
- Outside the repo (in `$BLLT_PROJECT`, `/scratch/project_465002727/jelealro`):
  venvs `ltx_env/venv` (generation; legacy name, do not move: venvs hold
  absolute paths), `musubi_env/venv`, `gemini_env/venv`; `hf_cache/`,
  `models/`, `ext/musubi-tuner`, `slurm_logs/`.

## Running things

```bash
cd /scratch/project_465002727/jelealro/big_lessons_little_tales
W=lumi/run_in_container.sh                     # LUMI PyTorch ROCm container + venv
$W python production/shot.py --scene 1 --shot s01_sleeps_3q --fast --dry-run
BLLT_ENV=musubi $W python ...                  # the LoRA-training venv instead
source voice/gemini_env.sh && python voice/list_voices.py   # voices, no container
```

- **Two venvs in the container** + one plain venv. `ltx_env/venv` (default):
  diffusers 0.39, transformers 4.51 (generation, design, keyframes, post).
  `musubi_env/venv` (`BLLT_ENV=musubi`): musubi-tuner pins, LoRA only.
  `gemini_env/venv`: google-genai, outside the container.
- **GPU work = a task file + `lumi/run_tasks.sbatch`**, one command per line,
  one GCD each, from the repo root:
  `sbatch --ntasks=3 --gpus-per-node=3 --mem=330G lumi/run_tasks.sbatch work/tasks/<name>.txt`
  Logs: `$BLLT_LOGS/bllt_tasks_<job>_<task>.log`.
- **Fast mode (Wan2.2-Lightning, `--fast`) is the default way to iterate**:
  ~9-16 min per clip instead of ~2 h 10, same look (docs/prompting.md "Fast
  mode"). Several seeds of one shot in one task share one model load (first
  seed ~17 min incl. load, then ~9 min each).
- Compute: `dev-g` only in practice (**2 jobs per user, pending ones count;
  3 h each**). `standard-g`/`small-g` start days later (sbatch --test-only,
  2026-09-27). **Host RAM, not VRAM, limits Wan**: ~100-110 GB per task, four
  tasks per 512 GB node. The login node has no GPU; keyframe composing
  (BiRefNet, Real-ESRGAN crops) runs there but slowly (~3 min per keyframe,
  15 min per upscaled crop, cached).

## Before a GPU job

1. `--dry-run` every script that has one; read the assembled prompt.
2. Check every input file exists (keyframes, canonicals, pose stills).
3. Look at every composed keyframe (and end keyframe) before rendering.
4. Will it fit in 3 h? Wan model load 10-25 min; fast clip ~9 min per seed;
   40-step 81-frame shot ~2 h 10; 49-frame pose ~1 h (fast ~15 min); LoRA
   1000 steps ~50 min.

## Mistakes already made (do not repeat)

- **`srun --overlap` into another job is not a place for real work.** When that
  job's own tasks finish, the job ends and kills the overlap steps (a LoRA run
  died at step 365/1500). Submit every workload as a task of its own job.
- **Do not assume GPU index k inside an overlap step is task k's GPU.** It
  held once in a 2-task job and failed in a 4-task one (two pose tasks ran out
  of memory). Measure with `torch.cuda.mem_get_info` if you must.
- **accelerate + multi-task Slurm steps:** Cray sets `PMI_SIZE` etc.;
  accelerate reads it as an MPI world and aborts ("MASTER_ADDR"). `lora/musubi_env.sh`
  unsets PMI/PMIX/OMPI/MV2 variables for every musubi script.
- musubi-tuner: `--timestep_boundary` is an integer 0-1000 in training;
  generation takes `--lora_weight` / `--lora_weight_high_noise`, not
  `--network_weights`; `--save_path` is a directory; merging a LoRA on the GPU
  runs out of memory, so use `--blocks_to_swap 10 --lazy_loading`; bitsandbytes
  is broken in the container, so use `--optimizer_type adamw`; fp16 weights force
  fp16 training, so use the bf16 conversions in `models/wan22_musubi/`.
- deepspeed/apex/aiter in the container break imports: the default venv shadows
  them with stubs, the musubi venv hides them with `sitecustomize.py`
  (`lumi/stubs/`).
- ffmpeg `concat` after `trim` silently fell back to 25 fps and made a whole
  video judder (the old channel intro). **Count repeated frames on deliverables**, not just
  duration.
- A reframing step once produced an image of empty floor, and nothing
  downstream noticed. Tools must **assert** their results (see
  `production/design.py reframe`); look at every contact sheet.
- Colour matching a pasted character to its background turned a white chest
  green. Never change a character's hue; brightness only.
- A wait loop on `pgrep -f "<pattern>"` matched its own shell and never ended.
  Wait on output files (timestamps) or PIDs.
- dev-g's 2-job limit counts **pending** jobs: `--dependency` submissions are
  refused while two jobs exist. Submit follow-ups from a waiter after the job ends.
- `lumi/env.sh` and `env_musubi.sh` are sourced inside the container; a variable
  they `export` overrides the caller's. Use `${VAR:-default}`.

- `pkill -f "<pattern>"` in a command also kills that command's own shell when
  the pattern appears in it (it cut a deletion short on 2026-09-27).
- A `yaml` value with a colon inside (`language: en (xx, yy: zz)`) breaks the
  file: quote such values.
- A `google-genai` client created inline and discarded (`genai.Client().x()`)
  closes itself before the call: keep it in a variable.

## Verification habits

- Every clip: a contact sheet (frames 0/20/40/60/80, or every 8th) and look at
  it before judging; full-size frames for faces and contact.
- Cuts and flashes: mean luma per frame by frame index, not `-ss` seeking.
- Deliverables: 0 repeated frames, exact duration, PCM 48 kHz audio in `.mov`.
- Voice lines: transcribe (Whisper) and compare with the text.

## Character and scene design: reusable guidance

The following workflow principles are supported both by this repo's measured
results (see `docs/prompting.md` and `docs/character-consistency.md`) and by
Neolemon's [How to Create Consistent Characters in AI Videos](https://www.neolemon.com/blog/how-to-create-consistent-characters-in-ai-videos-complete-guide/)
(Sachin Kamath, 12 February 2026; accessed 26 September 2026). The article is
published by a character-generation vendor, so treat its tool comparisons,
pricing, timelines, and claims of perfect consistency as vendor claims. Use
the workflow ideas below; the project's measured rules take precedence.

### Define and freeze character identity

- Before generating, write a compact character specification. In this repo,
  put story facts in `stories/<slug>/story.yaml`, not in a separate prompt:
  include name and story role, silhouette/body proportions, distinctive face
  features, fur/felt colours and materials, signature features or props,
  default costume/accessories if any, personality and safe emotional range,
  relative scale, and details that must never change. For felt animals,
  translate the article's age/vibe and hair/skin anchors into animal-appropriate
  traits such as age impression, fur/felt texture, ear shape, and muzzle.
- Keep a short, repeatable palette and a fixed style bible. Ensure the written
  sheet matches the approved canonical image. If the image wins over a detail
  (as with Leo's black stitched eyes), settle that discrepancy once by updating
  the sheet or selecting another canonical; do not carry conflicting text and
  image references downstream.
- Treat each intentional costume or accessory change as a separate visual
  state with its own canonical/anchor and pose references. Do not casually add
  clothing or props in shot actions.
- Generate and approve a neutral, full-body canonical first, alone against a
  plain contrasting felt backdrop. Build only the useful pack for the story:
  side/three-quarter/back views, expressions, and reusable action poses. The
  article's front, three-quarter, side, face, expression, and action coverage
  is a useful completeness checklist; the existing `packs/<character>.yaml`
  and LUMI budget determine what to make, not a fixed image count.
- Create every main character separately before composing a cast. Use the
  story's character sheets, canonicals and pose stills to keep designs distinct.
  For a multi-character keyframe, specify each character's position, scale,
  facing, and interaction in `compose:`; keep the scale relation from the
  story bible and exclude absent characters with `negative_extra`. If one
  character's small gesture is hard to read, make a close-up keyframe for that
  character rather than asking a camera move to find it.

### Design the set and storyboard the story

- Treat each location as a reusable empty background plate. Give it a frozen
  sheet with materials, palette, landmarks, time of day/light direction, and
  staging needs. Design the set edge to edge, with no studio table/backdrop,
  and leave clear open ground where characters must stand or travel. Keep
  story-specific landmarks consistent; a landmark associated with a character
  should not appear empty immediately after that character was established
  there unless the story shows them leaving.
- Design needed props as their own simple entities with a clear silhouette,
  distinctive material/colour, and a contrasting design background. Keep the
  prop's appearance stable in the story bible and compose it into keyframes
  when exact placement matters.
- Break a story into short, modular shots. The article suggests noting shot ID,
  duration, framing, camera movement, one main action, emotion, prop, and
  background. `story.yaml` already stores most of this through scene/shot IDs,
  `frames`, `action`, `characters`, `keyframe`/`compose`, and location/props;
  make missing staging or framing explicit in the action or composition.
- Keep each shot to one legible character action and at most one clear camera
  move. Generate a keyframe for the exact composition before animation, then
  animate that still. This project's 81-frame Wan shots are about five seconds;
  the article's generic 3–6 second suggestion is not a reason to change the
  project's measured Wan frame settings.
- For continuity, start a shot from its approved canonical/pose-based keyframe
  or a chosen frame from the prior take (`continue_from`). Carry forward
  character scale, screen position, facing, prop side/holder, lighting/time of
  day, and the emotional state required by the story. Use transition or
  background/prop-only shots when they help story pacing or bridge a difficult
  cut; they are optional editing tools, not a substitute for correct anchors.
- Prefer a simpler action or shorter shot when identity, felt texture, or
  staging drifts. Reuse the same plate and locked style language; check the
  contact sheet across the full clip, not only its first frame. For critical
  multi-character beats, use the repo's composited keyframe pipeline; the
  article likewise notes that animating a whole cast together is faster but
  can drift more than composing/controlling elements separately.

### Apply these principles to this codebase

The current pipeline implements the same separation of design, composition,
and motion: `production/design.py` makes candidate stills and canonicals;
`character/character.py` creates poses from a canonical; `lora/` trains and
evaluates optional character adapters; `production/keyframe.py` and each
shot's `compose:` recipe place pose stills on a location plate; and
`production/shot.py` animates the composed keyframe with Wan image-to-video.
The primary records are the story bible and shot recipes, not prompts copied
into ad hoc scripts. Keep decisions and measured outcomes in the relevant
`docs/` file and link it here when the guidance becomes too detailed for this
manual.

## Data lifetime

The LUMI project's data is deleted around **30 March 2027**. `work/` (designs,
poses, keyframes, shots, LoRAs) is git-ignored and exists only on scratch:
remind the owner to back it up (`bash lumi/backup_assets.sh`, then the printed
rsync on their computer; see `docs/findings-and-risks.md` B1). Gemini voices
expire 2027-09-27 (recreate from the prompts in `voice/`).

## The Lion and the Mouse v2 (active)

**2026-09-27**: the owner's retelling (`stories/lion_and_mouse_v2/story.txt`,
moral: "Kindness does not create a debt. It creates more kindness.") with an
owner-made character pack made following neolemon's consistency guide.

Authority, in order:
1. Canonicals: `character/characters/{Leo,Milo}/v2/canonical/*.png` (identity
   authority; text follows the image, never the reverse).
2. The rest of the owner's pack (views, expressions, actions) in the same folders.
3. `stories/lion_and_mouse_v2/story.yaml`: sheets (DNA corrected to the
   canonicals), locations, scale, voices, 12 scenes with the owner's narration.
4. Review frames in `work/stories/lion_and_mouse_v2_review/`: **layout guides
   only**, never character references.

How it is made (and why):
- **Owner-made canonicals**: `production/install_pack.py` pads them to 16:9
  (edge-repeat, blurred) into `work/stories/<slug>/design/<name>/canonical.png`,
  copies the pack to `characters/<name>/pack/` (`.png.png` fixed in copies
  only) and 16:9 versions of views/actions to `pack16x9/`. Originals are
  never modified.
- **Scale: Milo = 1/3 of Leo's standing height** (Rule 2.12). In the clearing:
  Leo standing 0.52 of frame; asleep 3/4 h 0.312; sphinx 3/4 0.361; Milo 0.17.
- **Start + end keyframes** (`end_keyframe:` / `end_compose:`): Wan animates
  between two composed stills. Close-ups: the owner's expression images as
  start/end, `blur` background, `background:` text instead of the location
  sheet (Rule 2.13). Continuations from a cropped frame also need an end
  keyframe (Rule 2.14).
- **Leo in 3/4 view** for sleeping and lying (owner request): pose clips from
  `pack16x9/views__leo_view_3q_01.png`; eyes closed in a separate short shot
  (a pose change and a face change in one shot fail).
- Everything from v1 still holds: fixed camera for locomotion, one action per
  shot, close-up crops for small gestures, no LoRA in shots, positive wording,
  several seeds (fast mode makes 3 cheap).

## Voices: Gemini 3.8 Flash TTS (owner decision 2026-09-27)

- **Everything is in `voice/`** (read its README): `gemini_env.sh`,
  `list_voices.py` (-> `voices_list.json`), `speak.py` (one line -> WAV +
  json), `save_voice.py` (record a designed voice: id, exact prompt, expiry,
  Google's sample), `render_samples.py` + `sample_lines.yaml` (the sample
  lines in every language). No GPU, no container.
- **API key: only in `~/.config/gemini/env`** (owner-written, chmod 600,
  `GEMINI_API_KEY=...`). Never print, copy, log or commit it.
- **Voices** (designed "prompted" voices, expire 2027-09-27; recreate from
  the prompt saved in each `voice.yaml` before then):

  | Role | Voice | Folder |
  |---|---|---|
  | **Lion and Mouse v2 narrator** | Moonlight Storyteller 1, `voice_v5bpq98uj7qh` | `voice/narrators/moonlight_storyteller_1/` |
  | Leo | The Noble Lion 1, `voice_zdbgqrcerxqu` | `voice/cast/leo/` |
  | Milo | The Brave Little Mouse 1, `voice_vf2w20rcys8a` | `voice/cast/milo/` |
  | alternative narrators | Golden Hour Storyteller 3 `voice_g00mo8cbdefq` (first pick), The Fireside Grandfather 2 `voice_4rdl7hydi35v`, The Cheery Tale Keeper 2 `voice_8tnxrhfqk3ur`, Bright Trail Narrator 2 `voice_tcrjw3ney7q8` | `voice/narrators/<name>/` |

  The story maps them in `stories/lion_and_mouse_v2/story.yaml` (`voices:`,
  paths relative to `voice/`).
- **Samples**: every voice folder has `google_sample.wav` and ONE sample line
  in en/es/fr/de/ru/uk (narrators: Scene 1; Leo: "You frightened me... Go on
  your way"; Milo: "Thank you..."). English files have no suffix, others
  `_es _fr _de _ru _uk`. Translations in `sample_lines.yaml` are assistant
  drafts: native check before the full scripts. Gemini audio: ~-70 dB noise
  floor; en and es verified word for word (Whisper).
- **Terms**: outputs owned by the user ("Google won't claim ownership"); price
  ~$0.0135/min of audio in 2026, ~$0.027 from 2027 (25 audio tokens/s; free
  tier rate-limited); SynthID watermark; EEA gets paid-tier data terms. Open:
  the Age Requirements ("API Clients" directed at under-18s) vs a Made-for-kids
  channel; the owner's question to Google is drafted in
  `docs/google_gemini_terms_question.md`. Never clone Gemini voices into
  another model (terms forbid replicating components of the Services).
- Chatterbox/Parler were tried and **removed** 2026-09-27 (Parler produced a
  hum; Chatterbox clones were noisy and drifted between lines); they are in
  git history before that date.
- Owner plan: narration first, video fitted to it; languages en, then es, fr,
  de, ru, uk. The full narration renderer is still to write: read
  `stories/<slug>/narration/<lang>.yaml`, speak each line with the story's
  voices (`voice/speak.py`), join per scene into
  `work/stories/<slug>/audio/<lang>/sceneNN.wav`, then
  `production/animatic.py --lang <lang>` times the pictures to it.

## Current state (update when it changes)

Lion and Mouse v2 (2026-09-27): **every scene has a take**; takes are in
story.yaml (`take:`), clips in `work/stories/lion_and_mouse_v2/shots/`
(fast-mode files end in `_fast`; the animatic finds both).
- **Animatic**: `work/stories/lion_and_mouse_v2/animatic.mp4`, 1 min 46 s,
  12 scenes, 22 shots, placeholder timing (no narration yet).
- Takes: s01 3/4 1111, s02 3/4 2111, s03 3/4 3112, s04 Milo trembles 4101,
  s04 Leo softens v2 4203, s05 nod v2 5106, s06 smiles 6101, thanks 6201,
  leaves v2 6305, s07 walks 7101, net falls 7202, tugs 7303, s08 hears 8101,
  runs v2 8204, s09 arrives 9102, can help 9201, s10 gnaws v2 10112
  (PROVISIONAL), steps free 10201, s11 Leo amazed 11101, Milo smiles 11201,
  s12 friends 12101.
- **Open: the gnawing shot.** v1 drifted (camera pulled back); v2 (end
  keyframe = start frame) held the framing but Milo only stands at the rope:
  pinning both ends to the same frame also freezes the action. Next try: a
  tighter crop with Milo larger, his paws on the rope, and an end keyframe
  that differs (a composed frame with the rope parted), or accept the beat
  with the narration carrying "gnaw".
- Places: plates clearing 3003, trap_site 3104, forest_run 3204; net = prop.
- Next: fix the gnaw (owner's call); narration with the Gemini voices when
  the owner asks (write the narration renderer, see Voices); then
  `animatic.py --lang en` times the pictures to it; post (1080p30) and edit.
- Removed 2026-09-27 (owner): v1 story and its generated files, fox tests,
  The Webtoons Corner intro/LTX/felt/music code, Chatterbox. Kept: LoRA
  outputs (`work/lora/`, 86 GB) and old intro renders (`work/intro_v4/`).
