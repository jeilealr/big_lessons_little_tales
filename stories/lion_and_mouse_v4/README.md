# The Lion and the Mouse — v4 review packet

**Prompts for making or remaking any image:** [`prompts/*.md`](prompts/) or `python3 production/image_prompts.py show <record>` (the exact prompt and the references to attach, in order).

## Status (2026-10-02)

- **Stills exist; clips do not.** The manifest has 140 image records: the 118
  planned ones plus 22 expression studies (`*/v4/expressions/`). 139 are
  accepted with their file on disk; `s02_place_acorn_end` is missing. They were
  made from 2026-09-30 to 2026-10-02 with GPT's built-in image tool (r01 and
  later in-place repairs) and the Gemini API (r02 to r05); every accepted and
  rejected take is in [generation progress](GENERATION_PROGRESS.md) and the
  records' `result` fields. "Accepted" is an agent's visual review: 63 records
  still read `accepted_pending_owner_review` (the owner's review sheet
  `IMAGE_REVIEW.md` was retired on 2026-10-02).
- **The owner now creates new images personally** (instruction of 2026-10-02);
  agents generate nothing unless asked. The "Resume order" in
  [generation progress](GENERATION_PROGRESS.md) is part of that dated log, not
  a current task.
- **Audio:** the English narration was rendered on 2026-10-02 from the
  [script](SCRIPT_REVIEW.md); [TIMING_SHEET.md](TIMING_SHEET.md) maps its lines
  to the shots (11:23.7 of narration; 42 of the 43 coverage shots give 3.4
  minutes at normal speed).
- No clip, take selection, runtime `story.yaml` or GPU job exists.

## Open issues (found by the 2026-10-02 documentation audit)

1. **`s02_place_acorn_end` has no image.** The owner deleted its r02 and two
   later attempts were rejected. The `s02_place_acorn_end_r01.png` still on
   disk is the owner-rejected r01; it is not a reference.
2. **S13 Milo size.** The `s13_milo_confident_*`/`s13_milo_playful_*` images are wide two-shots
   at the S14 scale (Milo 0.33-0.36 of the frame high); since 2026-10-02 their records say so
   (setup `trap_wide`, Leo counted). The preceding `s13_arrives_*` shows Milo at 0.21 with the same
   camera: a size jump without a depth move (CR-16). The prompts state the setup size (0.35), so a
   regenerated `s13_arrives` would match S13/S14; owner to decide whether to redo it.
3. **Leo-to-Milo ratio: decided 2026-10-02 (owner).** Milo standing = **0.55 of Leo's mane
   height** (Milo's head with ears about 0.4 of Leo's face height), as in
   `s05_nose_aftermath_start` (Milo 0.20 of the frame, Leo's mane 0.36). The bible
   (`cast_scale`, `blocks.cast_scale`, `setups`) and all prompts follow it; frames with both
   characters attach that frame as the size lineup. **Accepted images that no longer match**
   (remake when convenient): every S13/S14 trap-path wide frame (Milo 0.33-0.36, now 0.23), the
   S14 gnaw/sever two-shots (Milo 0.76, now 0.40), S05 paw contact, S06 barrier and S08 kindness
   (Milo 0.18, now 0.21; within about 15%) and S16 friends (Milo sitting 0.13, now 0.16).
4. **S06 barrier and S08 kindness share one image.** Since the 2026-10-02
   repair all four endpoints (`s06_barrier_*`, `s08_kindness_*`) are the same
   byte-identical composite, so both shots are holds. The shot records plan
   more: in S06 Leo places a front paw forward beside Milo, and S08 kindness
   cuts from the crouched barrier to an already-lying Leo with a gentle change
   of expression. Owner to decide whether the holds are acceptable.
5. **More findings of the 2026-10-02 audits** (details in `docs/image-prompts.md` and the bible):
   - Milo's portrait family drifted from the canonical: `M_CLOSED` (the root of all 11 Milo
     expressions and the mouth studies) has a head about 14% wider at the cheeks, a wider, lower
     nose and larger pupils; `m_expr_startled` is the worst. Close-ups take their faces from these.
   - Leo's 11 expression studies have a duller, darker mane (chroma about 65 vs 73) drawn as ribbed
     cords, and less saturated irises.
   - Seated Milo in S01-S02 was scaled to the standing box, so his head is about 1.5x too large
     when he sits (the prompts now say "sitting, he keeps exactly the same head size").
   - The S14 gnaw/sever two-shots enlarge the characters about 2.2x while the background stays
     at wide scale.
   - `s14_milo_clear` and later frames show several broken strands where only R01 was cut; the
     prompts keep the planned single cut.
   - `s12_runs` leaves frame left and `s13_arrives` enters from the left (screen direction).
6. **Bookkeeping.** `IMAGE_REVIEW.md` and its generator were deleted (owner, 2026-10-02).
   `dialogue_coverage.json` keeps
   `status: draft_no_audio_or_edit_created`. The manifest's top-level revision and every
   record's `bible_revision` now read `v4-consistency-2026-10-02`.

## About this packet

*Written as a documentation draft on 2026-09-30, before any v4 image existed;
the sections below keep that plan. Where they say "draft", "planned" or
"pending", read the status above for what has happened since.*

This packet turns the owner's v3 render notes into explicit story, identity,
image and motion requirements. It preserves v3 evidence and proposes a new
version; it does not overwrite the old assets or claim that a written prompt
guarantees a correct render.

## Read in this order

1. [Repair plan](REPAIR_PLAN.md): every observation, preferred v3 filename,
   unresolved attribution and proposed story change.
2. [Complete draft script](SCRIPT_REVIEW.md): scene order and proposed wording
   in context, with stable spoken-line IDs for later timing.
3. [Shot plan](SHOT_PLAN.md): chronological coverage and links to all scene prompts.
4. [Creation rules](../../docs/creation-rules.md): identity, scale, paired images,
   props, ambient motion and review requirements for v4 and future stories.
5. [Prompt records](../../docs/prompt-records.md) and
   [preflight](../../docs/v4-preflight.md): what to save and what to inspect.

## What is ready

| Record | Purpose |
|---|---|
| [visual_bible.json](visual_bible.json) | the single source of truth (2026-10-02): canonical identities with hex colours and review checklists, size lineup, plates with measured landmarks, camera setups with measured sizes and anchor records, shared prompt blocks, reference roles, prop states |
| [prompt_manifest.json](prompt_manifest.json) | 118 individual planned images (140 records since the 22 expression studies were added on 2026-10-02, each with its accepted `result`); 43 coverage shots with 62 video-mode prompt records |
| [Foundation prompts](prompts/foundation.md) | neutral canonicals, views, pose references, mouth shapes, empty plates and prop materials |
| [Scene prompts](SHOT_PLAN.md) | full positive and negative text for every planned start/end and video mode, references and acceptance checks |
| [dialogue_coverage.json](dialogue_coverage.json) | complete draft spoken text, scene/speaker IDs and candidate coverage; the line list the narration was rendered from (its timing fields are still empty; see [TIMING_SHEET.md](TIMING_SHEET.md)) |
| [Original owner notes](../../docs/reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt) | verbatim copy of `work/shots/notes.txt`, including its ambiguities |
| [GENERATION_PROGRESS.md](GENERATION_PROGRESS.md), `revisions/` | added during image creation: the dated log of accepted and rejected takes, the fix texts used for the Gemini passes r02 to r05 and `gemini_ledger.csv` (every Gemini call) |

The manifest is the authoritative planning record; Markdown prompts are readable
snapshots of the same full text. Video records also include compact runtime
candidates, with token review pending; the exhaustive specification stays as the
acceptance contract. Fast mode has no negative CFG pass, so the runtime positives
carry explicit desired states. The JSON is **not** an executable `story.yaml`
and existing tools do not enforce its new fields. Update the bible, affected
manifest records and readable snapshots together. Actual submitted prompts,
tool settings and file hashes must be logged when generation starts (since
2026-09-30 they are in each image record's `result`).

Scene-keyframe targets live under
`character/characters/interactions/v4/keyframes/`; these reference PNGs are within
the repository's existing media allowlist. Future generated clip candidates and
runtime composites go under `work/stories/lion_and_mouse_v4/` and require backup.

## Decisions before production

- Review the proposed script order, especially the acorn placement, paw contact
  before waking, curious trap trigger, and single closure-strand rescue. The
  multiple-cut alternative requires additional individually documented states.
- Milo's top tuft removal is already requested. A new smooth-crown neutral
  canonical still needs to be created and visually approved; all derivatives
  must follow it. Preserve his face, large ears, slim body and brown eyes.
  *(Done: `character/characters/Milo/v4/canonical/full-body_milo_neutral_pose_r01.png`,
  accepted from the owner's list on 2026-10-01.)*
- Keep Leo's full canonical rust-orange mane and brown eyes. Approve mouth
  families, including Milo's proposed two rounded gnawing incisors, before use.
  *(The mouth references exist, `*/v4/references/`, accepted by agent review;
  an owner approval of the mouth family is not recorded.)*
- Measure geometry from approved images. Numeric staging and tolerances in this
  packet are proposals, not measurements of saved assets. *(Done 2026-10-02: character proportions are in the bible's `characters.*.proportions`,
  measured landmarks in `locations`, per-setup sizes and anchors in `setups`.)*
- Time the approved script when audio is requested. The 43 coverage shots are
  not enough to assume a complete 8–10 minute edit. Expand the per-line plan
  with additional documented holds/reactions as needed; do not fill time with
  repeated takes or consecutive mouth-mode alternatives. *(The English
  narration lasts 11:23.7; [TIMING_SHEET.md](TIMING_SHEET.md) is the starting
  plan.)*

## Next production order

Owner script review → approved canonicals/reference families → individually
reviewed image pairs → small clip pilot → individual candidate review and owner
selection → separately requested animatic → post/edit.

Expressive/dialogue coverage has a closed-mouth baseline and a separate bounded
mouth-motion alternative. Functional nibbling/gnawing uses an approved contact
mouth and separate closed reaction coverage. Sleeping, silent travel and empty
scenery keep their appropriate state. Mouth motion is not audio-synchronised.

No v4 take is selected (no clip exists). No runtime story or job list exists;
the image execution log is [GENERATION_PROGRESS.md](GENERATION_PROGRESS.md)
plus the manifest results. The actual v3 clips were unavailable in this checkout;
the repair plan attributes their visual defects to the owner's review and marks
possible causes as hypotheses. The local neutral canonicals and production code
were inspected to ground the identity and pipeline rules.

## Documentation checks completed

2026-10-02 audit: every Markdown link and image embed in the docs, this packet
and `CLAUDE.md` resolves (the one broken embed, in the since-deleted `IMAGE_REVIEW.md`, is gone). Every
manifest output path exists except that record's.

2026-09-30: the JSON records parse; image IDs and target paths are unique; reference
chains resolve in dependency order; existing historical source paths and local
Markdown links resolve. Readable prompt text matches the manifest, including
runtime assembly fields. The notes archive matches the source byte for byte.
The six critical stream/net handoffs explicitly carry the preceding world state.
These checks establish document integrity, not image or video quality; actual
media review and deployed-tokenizer checks remain pending production.
