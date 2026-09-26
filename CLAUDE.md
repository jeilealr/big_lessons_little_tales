# CLAUDE.md: operating manual for agents working in this repo

Read this first. It is the durable memory of the project: what it is for, how
to run things on LUMI without repeating past failures, and where the knowledge
lives. Keep it current: when you learn something that would have saved you
time, add it here or to the doc it belongs in, and commit.

## What this repo is

Felt-animal fables for children with a kind message, made with open video
models (Wan 2.2) on the LUMI supercomputer, for a monetised YouTube channel
(The Webtoons Corner). The owner adds narration, voices and music outside this
repo with ElevenLabs; this repo makes the pictures and, at most, background
ambience.

First story: **The Lion and the Mouse** (`stories/lion_and_mouse/story.yaml`).

## The owner's standing instructions

- Goal: professional, consistent videos (same characters and places across
  shots). Iterate until the result is genuinely good; show evidence (contact
  sheets) for every judgement.
- Everything used must be **licence-clean for a monetised channel**. Check a
  model's licence before downloading it; record it in `docs/licensing.md`.
  Rejected so far: HunyuanVideo (excludes the EU), MusicGen (CC-BY-NC), Stable
  Audio Open (revenue cap), RMBG 1.4/2.0 (non-commercial).
- **Do not push to GitHub.** Commit locally. Commit messages end with the
  `Co-Authored-By:` trailer the session specifies.
- Only run GPU jobs when you are sure they are ready: dry-run and smoke-test
  first (see "Before a GPU job").
- Keep the docs as a guide a person can learn from: why, measured results,
  images.

## Where the knowledge is

| Need | Read |
|---|---|
| Writing any prompt (shot, pose, design) | **`docs/prompting.md`**: every measured rule and a checklist |
| Every problem found and its fix; gaps and risks | **`docs/findings-and-risks.md`** |
| The whole pipeline, story to shots | `docs/production-guide.md` |
| Consistency experiments (the fox) | `docs/character-consistency.md` |
| LUMI jobs, times, solved gotchas | `docs/lumi.md` |
| What was changed where (no third-party repo modified) | `docs/provenance.md` |
| Licences | `docs/licensing.md` |
| Story facts (characters, places, scenes, shots) | `stories/<slug>/story.yaml`: the only place they live |

## Layout

```
stories/<slug>/story.yaml   style bible, frozen sheets, scenes, shots
stories/<slug>/packs/       per-character pose lists
production/                 design.py, keyframe.py, shot.py, scene_baseline.py
character/character.py      pose/turn clips for a character (story or fox test)
lora/                       build_dataset.py, train_character.sh, eval_character.sh, eval_grid.py
twc/                        paths, media (ffmpeg), wan (model wrapper), post (RIFE/ESRGAN/grade)
lumi/                       run_in_container.sh, env.sh, env_musubi.sh, run_tasks.sbatch, setup_env.sh
work/                       generated files (git-ignored); every output has a .json sidecar
```

Paths: the repo is `/scratch/project_465002727/jelealro/twc_video`; run
commands from its parent (the "channel folder"), which also holds `Intro/`
(stills, finished videos) and `audio/`.

## Running things

```bash
cd /scratch/project_465002727/jelealro
W=twc_video/lumi/run_in_container.sh           # LUMI PyTorch ROCm container + venv
$W python twc_video/production/shot.py --scene 1 --shot s01_establish --dry-run
TWC_ENV=musubi $W python ...                   # the LoRA-training venv instead
```

- **Two venvs**, one container. `ltx_env/venv` (default): diffusers 0.39,
  transformers 4.51, for generation, design, keyframes, post. `musubi_env/venv`
  (`TWC_ENV=musubi`): musubi-tuner's pins (diffusers 0.32, transformers 4.57,
  accelerate 1.6), for LoRA training and LoRA inference only.
- **GPU work = a task file + `lumi/run_tasks.sbatch`**, one command per line, one
  GCD each:
  `sbatch --ntasks=4 --gpus-per-node=4 --mem=480G twc_video/lumi/run_tasks.sbatch tasks.txt`
  Logs: `slurm_logs/twc_tasks_<job>_<task>.log`.
- `dev-g`: starts in seconds, **max 2 jobs per user, 3 h each**. `small-g` and
  `standard-g` queue for hours.
- **Host RAM, not VRAM, limits Wan**: ~100-120 GB per Wan task (weights are
  offloaded to CPU). Four tasks per 512 GB node.
- The login node has no GPU; CPU work (Real-ESRGAN on one image, BiRefNet,
  dataset building) runs there but slowly (Real-ESRGAN 1280x720: ~15 min).

## Before a GPU job

1. `--dry-run` every script that has one; read the assembled prompt.
2. Check every input file exists (keyframes, canonicals, pose clips).
3. New pipeline or tool? Run a short smoke test first (`lora/musubi_smoke.sh`
   caught four separate failures in minutes, each of which would have wasted a
   3-hour job).
4. Will it fit in 3 h? Measured: Wan model load 10-21 min; 81-frame 720p shot
   ~2 h (40 steps); 49-frame pose ~1 h; LoRA 1500 steps ~1 h 15 min.

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
- ffmpeg `concat` after `trim` silently fell back to 25 fps and made every
  hybrid intro judder. **Count repeated frames on deliverables**, not just
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

## Tools added for the risks in findings-and-risks.md

- `lumi/backup_assets.sh`: list of assets to keep + the rsync to run at home.
- `production/animatic.py`: whole story at planned pacing (takes, keyframes,
  cards, narration from `audio/<slug>/sceneNN.wav`).
- Keyframe recipes (`compose:`) live in the shot; `shot.py` builds missing
  keyframes on the GPU node.
- Model revisions are pinned (`twc/wan.py REVISIONS`, `twc/post.py`).
- `design.py` designs props too (`--entities net`).

## Verification habits

- Every clip: a contact sheet (`ffmpeg ... select='not(mod(n\,6))',tile=9x1`),
  and look at it before judging.
- Cuts and flashes: mean luma per frame by frame index, not `-ss` seeking.
- Deliverables: 0 repeated frames, exact duration, PCM 48 kHz audio in `.mov`.
- LoRAs: `lora/eval_grid.py` with a no-LoRA row, same seeds for every
  checkpoint, and prompts outside the training data.

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
packs, LoRAs, shots) is git-ignored and exists only on scratch: remind the owner
to back it up (see `docs/findings-and-risks.md` B1).

## Current state (update when it changes)

- Lion and Mouse picks: Leo 1003, Milo 1001 (reframed), butterfly 1004,
  clearing 1002, trap site 1004, berry patch 1003.
- Poses done: Leo sleeps, sits, turns side, turns away, walks (did not travel);
  Milo paws together, turns side, turns away, runs, waves.
- Scene 1: done (s01_establish_s5102, s01_establish_v2_s5103: Leo stays asleep).
- Scene 2: take 5204 (v3, fixed camera: Milo runs out of frame). v1 ran into
  depth, v2 (tracking camera) did not run.
- Scene 3: done, take 5302 approved by the owner (Leo looking at the camera is
  fine: do not spend re-renders on eye-lines).
- Scene 4: Leo smiles (take 4202). Milo's plead: the push-in went to Leo
  (Rule 2.12); v2 starts from a close-up crop of the continuity frame: job
  22368409 with Scene 5 "Milo leaves" (~20:10). Then s05_leo_rests continues
  from the chosen "leaves" take (set its `take: TBD`).
- Scene 6: Leo walks (6101), the net falls (6202). Scene 7: Milo turns (7101),
  runs (7201). Running: job 22369291 (~21:20) with Leo's call for help
  (s06_leo_calls) and Scene 8 Milo arrives (keyframe = Milo pasted into the
  trap's final frame).
- Net prop designed (1001). Still to write: Scene 8 nibbling (close-up),
  Scene 9 (brief truncated), Scene 5 Milo waves (close-up crop).
- LoRAs: `fox` -> `fox_v2` (composited plates fix the background leak). Leo and
  Milo LoRAs: step 500 chosen (eval grid). LoRA inside I2V shots: measured
  worse (location drifts, identity no better): shots render without LoRAs.
- Animatic: `work/stories/lion_and_mouse/animatic.mp4` (placeholder timing).
- Two tasks in one job must not write the same file (e.g. a shared
  continue_from keyframe): extract it before submitting.
- Open questions for the owner: (Leo's eyes: decided, black);
  Leo 1003 vs 1005; the story brief is truncated at Scene 9.
