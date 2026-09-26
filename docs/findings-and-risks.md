# Findings, fixes, and what you may be missing

Two parts. **A** lists every problem found so far, what caused it, and how it
was solved (or that it is still open). **B** lists gaps and risks nobody has
raised yet, with a recommendation for each. Keep both current.

Checked 2026-09-26.

---

## A. Findings and their solutions

### Consistency

| Finding | Cause | Solution | Status |
|---|---|---|---|
| Same text gives a different character every shot (4 different foxes) | text describes a *kind* of character, the model samples one | start every shot from an image (keyframe); train a LoRA per main character | solved |
| Characters stay consistent within a shot but not between shots | nothing ties shots together but words | same as above | solved |
| LoRA learns the training background (forest prompt returns the meadow from step 1000) | every training image had the same meadow | composite the cut-out character into varied plates (`composite:` in the dataset file); pick the earliest good checkpoint | **solved** (`fox_v2`: no leak at any checkpoint) |
| LoRA can't do poses it never saw ("sleeping curled up" came out lying stretched) | no such pose in the data | put every pose the story needs into the character pack before training | rule |
| Design picked that contradicts its text sheet gets pulled back to the text | the sheet is in every prompt | make canonical and sheet agree | rule |
| Model ignores some sheet details (Leo's eyes always black, not brown) | model prior | decide and edit the sheet, or keep asking | **open: owner's call** |

### Prompting (full rules in `docs/prompting.md`)

| Finding | Solution |
|---|---|
| "looks up at the clouds" animated a cloud, not the fox | the action names only the character's body |
| head raise from a still barely registers | one whole-body action; make a gesture the whole shot, described big |
| "walks slowly and calmly" did not travel; "runs quickly, a scamper" did | locomotion needs an energetic verb and a direction |
| a runner leaves a fixed frame | give the camera a job ("follows alongside") |
| Milo faced left, the prompt said run right | read the keyframe first; direction must match |
| "hops three times": the bunny teleported | no repeated fast actions |
| sleeping Leo woke up in one seed | state what must not change + its opposite in `negative_extra`; render 2 seeds (**confirmed**, Scene 1 v2) |
| LoRA pose freedom shrinks with training (fox_v2 sleeps at step 500, sits awake later) | ~1000 steps; choose the earliest checkpoint that holds identity; train every story pose |
| keyframe with a sharp character over a blurred foreground object reads as floating | place the character on the in-focus plane |
| camera orbit around a still character: only ~30 degrees | turn the character instead |
| Scene 2: Milo ran away into depth, not across | explicit side-on geometry + sideways camera + negate "running away" (v2 testing) |
| Scene 2: a tilt-up revealed a canopy the keyframe lacked; the model invented a different tree | push-ins, or keyframes that contain what the move reveals |
| Scene 2 showed Leo's tree without Leo | keep character-tied landmarks out of frame or include the character |
| a secondary character with only a text sheet (butterfly) came out on-model | a specific sheet is enough for small, simple secondary characters |
| location prompt drew props on a table | say the scene fills the frame, no backdrop |

### Tools and pipeline

| Finding | Solution |
|---|---|
| colour-key matting cut a notch out of the grey mouse on a grey-green backdrop | BiRefNet matting (MIT) |
| colour-matching a pasted character turned its white chest green | brightness-only matching; none at all for training data |
| a reframe step produced an image of empty floor, silently | tools assert their results (`design.py reframe`) |
| ffmpeg concat after trim fell back to 25 fps, every hybrid intro juddered | exact timestamps + forced 30 fps; count repeated frames on deliverables |
| a luma check with `-ss` seeking showed a false 48-level jump | measure by frame index |
| 97-frame clips cost ~250 s per step, could not finish in 3 h | 81 frames max; retime with RIFE |
| ffmpeg minterpolate warped fast motion; lanczos upscale was soft | RIFE (MIT) + Real-ESRGAN (BSD-3) |

### LUMI and training

| Finding | Solution |
|---|---|
| deepspeed/apex/aiter in the container break model imports | stubs (default venv), `sitecustomize.py` hider (musubi venv) |
| musubi-tuner and the generation code need incompatible library versions | two venvs in one container (`TWC_ENV=musubi`) |
| training both Wan experts in one run: 11-13 s/step (28 GB swapped per expert change) | one LoRA per expert, trained in parallel: 2.6-3.5 s/step |
| accelerate aborted in multi-task jobs ("MASTER_ADDR") | unset Cray PMI variables (`lora/musubi_env.sh`) |
| work launched with `srun --overlap` died when the host job ended | submit every workload as its own job's task |
| GPU index k inside an overlap step is not task k's GPU | never assume; measure |
| musubi flag mismatches (boundary int; `--lora_weight`; `--save_path` is a dir) | recorded in `CLAUDE.md` and scripts |
| LoRA merge on GPU ran out of memory | `--blocks_to_swap 10 --lazy_loading` |
| training could not survive a job ending | `--save_state`, automatic `--resume` |
| MIOpen cache in /tmp unwritable on some nodes | per-job/task cache on scratch |
| login node refused to memory-map a 28 GB file | streaming fp16 -> bf16 converter |

---

## B. What you may be missing

### 1. Everything generated will be deleted in 185 days  (**act on this**)

The LUMI project's data is removed on about **30 March 2027**. Everything in
`work/` (47 GB: the chosen designs, character packs, LoRAs, rendered shots) is
git-ignored and exists **only on LUMI scratch**. The code is safe in git; the
assets are not.

*Recommendation:* back up the irreplaceable part regularly to your laptop:
canonical stills, `packs` clips, trained LoRAs, finished shots. That is a few
GB. Model weights (~420 GB) can be re-downloaded and need no backup. A
`lumi/backup_assets.sh` (rsync of the small set) would make this one command.

### 2. The narration should come before the video

Professional animation times pictures to a finished voice track, not the
other way round. Each shot here is at most 5 seconds and costs about 2 GPU
hours; a narration line that runs 9 seconds needs two shots, and you only
find out after rendering.

*Recommendation:* for each story, first produce the ElevenLabs narration per
scene, measure each line's length, then plan shots to fit. Before rendering
any video, cut an **animatic**: the keyframe stills (cheap, minutes on a CPU)
laid on the narration with the planned durations. It shows pacing problems for
free. The repo can build animatics automatically from `story.yaml` + audio.

### 3. Who speaks, and how (dialogue)

Milo has a line ("Please let me go. Maybe one day I can help you too."). The
characters have stitched mouths, and Wan cannot lip-sync to audio.

*Recommendation:* decide the convention once for the channel. The simplest
that fits felt stop-motion: a narrator tells the story and reads the lines; the
character "speaks" with body language (paws together, a nod), mouth still. Avoid
tight face close-ups during spoken lines, which invite the viewer to expect
moving lips.

### 4. Two characters touching: the hardest shots are untested

Scenes 3, 4, 8 and 9 need contact: Milo running over Leo's paw, climbing his
mane, Leo's paw stopping Milo, Milo nibbling the net. None of that is tested.
Risks: identity blending between the two, Milo's tiny size (at 1/6 of Leo's
height in a two-shot he may be only a few dozen pixels high), and two LoRAs
active at once (untested; they can bleed into each other).

*Recommendation:* test one interaction shot early (Scene 3 "paw in front of
Milo"), before producing the easy shots. Use close-ups for Milo's moments
rather than wide two-shots.

### 5. Props are not designed yet

The rope net appears in scenes 6, 8 and 9 and changes state (ropes break one
by one). `design.py` handles characters and locations only.

*Recommendation:* design the net as a third kind of entity (canonical still,
frozen sheet), and plan its states (whole / one rope broken / open) as
separate keyframes.

### 6. The trap scene is close to YouTube's own example of distressing content

YouTube's July 2026 clarification names "animals in distress followed by a
rescue" as an example of off-putting content. That is the shape of scenes 6-9.

*Recommendation:* keep the peril short and mild (the brief already says soft
rope, worried not suffering; keep it that way in every shot), make the roar a
call for help rather than something frightening (sound design matters here for
toddlers), never use the trapped lion in the thumbnail or title, and let the
kindness message carry the video.

### 7. Channel settings for children's content

*Recommendation:* mark every video **Made for kids** in YouTube Studio (legally
required for child-directed content; it disables comments and personalised
ads, and changes what end screens can do). Keep kids videos out of playlists
mixed with the channel's other content.

### 8. Reproducibility: model versions are not pinned

Each output's sidecar records prompt, seed and settings, but not the model
revision. Hugging Face repos can be updated, and the same seed could then give
a different image. Revisions in use on 2026-09-26:

| Model | Revision |
|---|---|
| Wan-AI/Wan2.2-I2V-A14B-Diffusers | `596658fd9ca6b7b71d5057529bbf319ecbc61d74` |
| Wan-AI/Wan2.2-T2V-A14B-Diffusers | `5be7df9619b54f4e2667b2755bc6a756675b5cd7` |
| Comfy-Org/Wan_2.2_ComfyUI_Repackaged | `ee6f4a40737a995bf5818954cfce6d59443b0f04` |
| Wan-AI/Wan2.1-T2V-14B (VAE, T5) | `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4` |
| TensorForger/RIFE-safetensors | `78a62b7c2dd910536432d6c2c3a25e76f14fbf78` |
| Comfy-Org/Real-ESRGAN_repackaged | `5fd49b7b278836f48af63ecd314d0f98ab336105` |
| ZhengPeng7/BiRefNet | `e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4` (pinned in code) |

*Recommendation:* pin these revisions in `twc/wan.py` and the download scripts,
and write the revision into every sidecar.

### 9. Time, not GPU budget, is the limit

GPU hours used: 9,030 of 250,000 (3.6%). A fable is cheap in budget. Wall
time is the constraint: `dev-g` allows 2 jobs of 4 GCDs, about 8 shots per
2.5 hours. A 3-minute fable is roughly 36 five-second shots; with ~50% retakes,
about 55 renders, which is about 17 hours of `dev-g` time spread over a few
days.

*Recommendation:* plan a story's renders in batches of 8, and lock the animatic
(point 2) first so renders are not wasted on shots that get cut.

### 10. One style for the whole channel

The style bible sits inside `story.yaml`. If future fables are meant to look
like the same series, the style should live in one shared file that every
story uses, and recurring characters would need one shared character bible.

*Recommendation:* decide whether Leo and Milo are a one-off or the channel's
recurring cast; if recurring, move style and characters to a shared place
before the second story.

### Open decisions (owner)

- Leo's eyes: keep the black the model draws, or insist on "warm brown".
- Leo's look: 1003 (fluffy mane, chosen) or 1005 (felt-ball mane).
- The story brief stops mid-sentence at Scene 9; the rest of the scenes are needed.
- Narration convention (point 3).
