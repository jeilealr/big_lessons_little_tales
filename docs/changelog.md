# Change log

Dated record of changes to the rules, tools and story packets, newest first within a day.
Each entry says what changed, why, which files, and how it was checked. Owner instructions
are quoted or summarised with their date. Git history has the diffs; this file has the reasons.

## 2026-10-08: Lion and Mouse v6, audio-driven chained coverage

Owner, 2026-10-08: the v5 audio is far longer than the 5 s clips; for v6, create as many
prompts, images and clips as the narration needs, so the video lasts as long as the audio, and
the end of one scene is the beginning of the next, keeping the consistency skills. Landscape
clips (e.g. the stream plate) cover narration with nothing happening. A cut is fine where it
makes sense (a face close-up, day to night). `continue_from` stays a repair option. Add a test
of how the joins work together once the inputs exist. Make the changes one at a time and
record them. Defaults taken by the agent (no owner answer yet): reuse the v5 English narration
(no new TTS) and reuse v5 images wherever they fit the chain.

### 1. Rule CR-21: audio-driven chained coverage

- **What:** new rule in `docs/creation-rules.md`: the narration is the timeline; pieces of 49 to
  81 frames; chain by shared image records; marked, checkable cuts (`film_start`, `close_up`,
  `camera_change`, `time_change`, `location_change`); no same-setup cut; landscape pieces and
  entrance pieces; holds; talking chains; boundary-image review; reuse of earlier renders; the
  join test, with `continue_from` as the repair.
- **Why:** the owner's request above; clips longer than 81 frames are quadratic in cost and
  drift (`docs/lumi.md`), so length comes from more pieces, not longer clips; trimming a clip
  would cut off the shared end image, so frame counts are chosen per piece instead.
- **Files:** `docs/creation-rules.md` (CR-21), `docs/changelog.md` (new).
- **Checked:** text only; the tools it names are the next entries.

### 2. Lint: chain, cut, frame and landscape rules (`production/image_prompts.py`)

- **What:** when the bible has `"chained_coverage": true`, `lint` runs `lint_chain`: one variant
  per piece; every piece has a bible `setup` and `lines`; endpoints are scene records of that
  setup or the setup's own empty plate (landscape and entrance pieces); `join_in: chain` starts
  on the predecessor's end image; `join_in: cut` needs a `cut_reason` that is true for the two
  setups (`close_up`, `camera_change`, `time_change`, `location_change`; the first piece is
  `film_start`); a cut inside one setup is reported as a jump cut; `transition` is `cut`,
  `crossfade` or `dip`; frames are 4k+1 within 49 to 81; start = end only with `hold: true` or
  mode `ambient`; ambient pieces have no cast; `reuse` must name an earlier variant with the same
  endpoints, runtime prompt and frame count. The start/end pair rules (same setup, an end frame
  edits its start) now apply where an image first appears in the chain, since one image is the
  end of one piece and the start of the next. New chained images are named `sNN_KK_...` by first
  use in the scene (`chain_chrono_names`); images reused from an earlier version keep their names.
- **Why:** CR-21 (entry 1); the lint is the gate every prompt passes (CR-18).
- **Files:** `production/image_prompts.py`.
- **Checked:** lint output of all four existing stories is byte-identical before and after
  (Lion and Mouse v5: 70 errors, 8 warnings; Ugly Duckling v1: 22 errors; Tortoise and Hare v1
  and Boy Who Cried Wolf v1: 0). A test manifest built from v5 records passes clean, and a
  broken copy reports each planted fault: a wrong first piece, a broken chain, a false
  `cut_reason`, an 83-frame clip, a same-setup cut with endpoints from another setup, and an
  unflagged hold.
- **Found, not caused:** Ugly Duckling v1 lint reports 22 errors (missing `.review/` raw files
  and `review/reference_boards/*_character_guide.png` references), although `CLAUDE.md` says 0.
  Not changed here.

### 3. Planner: `production/chain_plan.py` (new)

- **What:** times a chained story's pieces from the narration. Each line owns the span to the
  next line's start (pause included; the last line also owns the 1 s scene tail), so spans add
  up to the scene audio exactly. A piece lists its `lines`; a line shared by consecutive pieces is
  split evenly. Each piece gets the Wan frame count (4k+1, 49 to 81) closest to its seconds and a
  retime speed within 0.80 to 1.25, so a piece covers 2.45 to 6.33 s. `suggest` lists every line
  and how many pieces it needs; `check` reports uncovered lines, out-of-order or non-consecutive
  lines and out-of-bound pieces; `apply` writes the frame counts into the manifest variants and
  writes `TIMING_SHEET.md` and `timing_plan.json` (start, length, frames, speed, join, endpoints
  of every piece; nothing held or stretched).
- **Why:** CR-21; `timing_sheet.py` (kept for unchained stories) can only stretch a fixed shot
  list over the audio. Frame counts below 81 replace trimming, which would cut off the shared end
  image.
- **Files:** `production/chain_plan.py`.
- **Checked:** `suggest` on the v5 narration: 11:23.7 in 16 scenes, at least 108 pieces and
  about 135 at full length (scene 15 alone 17 to 20); frame selection gives 49 frames at
  1.25 speed for 2.45 s, 81 frames at 1.00 for 5.06 s and 0.80 for 6.33 s.

### 4. CR-21 and lint amended while planning v6: `dissolve`, same-place camera change, empty scene frames

- **What:** new `cut_reason` `dissolve` (time passes; requires `transition` crossfade or dip; the
  only cut allowed inside one setup). `camera_change` now means the same place (the plate's
  folder), not the same location profile, because the great tree's dusk wide, close-ups and
  upward sky view are separate profiles of one place. A landscape piece may also hold on an
  approved empty scene frame of its setup, when a prop belongs in the view.
- **Why:** found while planning v6: the film should end on the empty tree after the friends
  (same camera, time passes), the tree's sky cutaway is a camera change, and the trap path's
  bare plate has no net, so a landscape of the trap needs the net drawn in.
- **Files:** `docs/creation-rules.md` (CR-21 items 4 and 5), `production/image_prompts.py`.
- **Checked:** lint output of the four existing stories still byte-identical to the baseline.

### 5. Packet builder `production/chain_packet.py` (new) and the Lion and Mouse v6 packet

- **What:** `chain_packet.py <source>` writes a chained story from a source file and a base story:
  the base bible with `chained_coverage` and `keyframe_chrono_naming` on, the base image records
  (marked `carried_from`; the expression-study records stay in the base story and are attached
  by path), the new image records (CR-18 template order; a chain frame edits its neighbour with
  the new block `edit_chain_frame`, an open-mouth frame follows CR-19 with `edit_open_mouth`),
  one shot per piece, the line list mapped to pieces, `SHOT_PLAN.md` and `README.md`. A `reuse`
  piece copies the base variant verbatim. New video prompts describe only what is in frame (the
  v5 scene 15 lesson). Carried records whose files the owner renamed after v5 (three `.png.png`
  references, two `s08_milo_surprised` frames now r01, `s12_runs_end` now r02) are resolved
  through the v5 image-set READMEs, as `export_runtime.py --images` does; the old name stays in
  `base_target`.
- **The plan** (`stories/lion_and_mouse_v6/chain_source.py`): 154 pieces cover the v5 English
  narration (11:23.7) exactly; 25 reuse v5 renders, 129 need new renders; 48 are holds or
  landscapes (opening stream landscape, fork, dusk sky, empty lanes, the trap with the net set,
  and four tree, trap and stream landscapes in the closing narration). 33 new images: 16
  open-mouth frames for the talking chains, 3 entrance frames (Milo at the stream, Milo at the
  fork, Leo back at his tree), the empty trap with the net, and 13 frames for new beats (Milo at
  the feeding stone, Milo looking at the sky, Leo's sleeping face, the tumble ending in the wide
  shot, Leo lifting his head, Milo at the net, a Milo close-up for his S13 lines, the frame before
  the first bite, the gnawing seen wide, Leo sitting, Leo bowing, Leo's smile, the friends
  resting). Frame counts 49 to 81, speeds 0.80 to 1.23.
- **Lint changes made for it** (`production/image_prompts.py`): records with `carried_from` skip
  the reference-file check (their story's lint covers them); in a chained story the "end frame
  edits its start" rule applies to new images only; new role `empty_copy` (copy a frame without
  its characters) may show characters absent from the frame; `edit_chain_frame` counts as an
  edit block.
- **Files:** `production/chain_packet.py`, `production/image_prompts.py`,
  `stories/lion_and_mouse_v6/` (source, bible, manifest, line list, `SHOT_PLAN.md`, `README.md`,
  `prompts/`, `TIMING_SHEET.md`, `timing_plan.json`), the empty folder
  `character/characters/lion_and_mouse_v6/interactions/keyframes/`.
- **Checked:** `image_prompts.py --story lion_and_mouse_v6 lint`: 0 errors, 0 warnings;
  `chain_plan.py ... apply`: 154 pieces cover 11:23.7 of 11:23.7, 0 errors; video prompts 75 to
  218 words (v5 measured up to 346 umT5 tokens for similar prompts, limit 512); the other four
  stories' lint output unchanged. Fixed on the way: the plate attached twice on entrance frames,
  a colour word and a body word in one action sentence, Milo counted in Leo's solo frame.
- **Found, not caused:** `CLAUDE.md` says the 70 v5 lint errors are all expression-record
  references; they also include `staging_only` references to deleted v3 images in scene
  records (s10 to s14). v5 is unchanged.

### 6. `production/export_runtime.py`: reused pieces are not exported

- **What:** a piece with `reuse` is left out of the runtime story and listed under `reused:` in
  `story.yaml`, so `lumi/render_story.sh` never re-renders it.
- **Checked:** a test export of v6 scenes 2 and 4 (the scenes that need no new image) gave 5
  runtime shots with planned frame counts (61, 77, 81, 77, 81) and seeds, and 3 reused pieces;
  the test `story.yaml`, `runtime_inputs.json` and frozen keyframes were removed afterwards (no
  runtime story exists for v6 yet). A full export stops, as designed, on the 33 images not yet
  made.

### 7. Join test `production/chain_preview.py` (new)

- **What:** plays a stretch of a chained film against its narration. `--stills`: the planned
  images, each piece blending from its start to its end image, not-yet-made images as labelled
  grey cards (no clips, no GPU). Default: the owner's chosen takes (`takes.yaml` or the `best_`
  prefix; reused pieces from the base story's `shots/`), others shown as stills and listed, or
  `--any-seed N` captioned UNSELECTED. Planned crossfades and dips are applied at cuts. For each
  chain join between two clips it reports `jump` (last frame vs next first frame), `motion`
  (median frame-to-frame change around the join), their ratio (flagged above 3) and `pace`, and
  writes a join sheet (last frame, first frame, difference).
- **Checked:** `--stills --until 64` on v6 (scenes 1 and 2): 1550 frames at 24 fps = 64.58 s,
  narration 64.60 s, voice from 0.27 s; contact sheet looked at (landscape opening, placeholder
  cards, the sunset crossfade). Takes mode with a temporary `takes.yaml` that put a v5 clip
  before the reused `s01_explores`: the join was flagged (ratio 7.3; Milo jumps from x=0.55 back
  to 0.30), as it should be; test files deleted. Kept:
  `work/stories/lion_and_mouse_v6/review/chain_preview_0-64_stills.mp4`.

### 8. Skills: new `audio-chained-coverage`, section F in `consistent-image-prompts`

- **What:** a new repo skill for planning and checking chained stories (tools table, the planning
  steps: lines and bounds, holds and landscapes, entrances and exits, cut reasons, talking chains,
  reuse, in-frame-only video prompts; new images in a chain; the pilot and join test before the full
  render). The image-prompt skill gets section F: boundary-image review, chain frame edits, landscape
  pieces and `empty_copy`, chained file names.
- **Why:** the owner asked for the skills to carry the new way of working; the consistency rules stay
  in the existing skill and the new one points to them.
- **Files:** `.claude/skills/audio-chained-coverage/SKILL.md`,
  `.claude/skills/consistent-image-prompts/SKILL.md`.
- **Checked:** every command in the new skill's table was run in this session (entries 3 to 7).

### 9. `CLAUDE.md` and `docs/production-guide.md` point to the new way of working

- **What:** `CLAUDE.md`: a v6 bullet at the top of "Current state" (what v6 is, numbers, defaults to
  confirm, where to start, next steps), the lint states found today (Ugly Duckling 22 errors; the v5
  70 errors include v3 `staging_only` references in scene records), three rows in "Where the knowledge
  is" (the new skill and tools, the v6 folder, this change log), the new tools in the layout.
  `docs/production-guide.md` section 9: the narration-first planning and its tools.
- **Files:** `CLAUDE.md`, `docs/production-guide.md`.
- **Checked:** recounted the new image records in `chain_source.py`: 33 total (16 open-mouth,
  3 entrance, 1 empty-trap and 13 beat frames); the totals match `CLAUDE.md`, the v6 README and
  the generated shot plan. `image_prompts.py --story lion_and_mouse_v6 lint` reports 0 errors
  and 0 warnings; `chain_plan.py ... check` covers all 154 pieces and all 11:23.7 with 0 errors;
  `git diff --check` is clean.
