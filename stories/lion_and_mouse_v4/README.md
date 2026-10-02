# The Lion and the Mouse — v4 review packet

**Image review:** [`IMAGE_REVIEW.md`](IMAGE_REVIEW.md) shows every v4 image with a Keep column for the owner and a diagram of the shot order and framing (rebuild with `python3 production/image_review_md.py`).

**Documentation draft, 2026-09-30. No v4 images or videos generated.**

Image generation started later on 2026-09-30. Eight inspected foundation assets
are saved; see [generation progress](GENERATION_PROGRESS.md). No scene images,
clips or runtime jobs have been created yet.

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
| [visual_bible.json](visual_bible.json) | frozen draft identities, camera/scale profiles, locations, ambient motion, prop states |
| [prompt_manifest.json](prompt_manifest.json) | 118 individual planned images; 43 coverage shots with 62 video-mode prompt records |
| [Foundation prompts](prompts/foundation.md) | neutral canonicals, views, pose references, mouth shapes, empty plates and prop materials |
| [Scene prompts](SHOT_PLAN.md) | full positive and negative text for every planned start/end and video mode, references and acceptance checks |
| [dialogue_coverage.json](dialogue_coverage.json) | complete draft spoken text, scene/speaker IDs and candidate coverage; timing/selection pending |
| [Original owner notes](../../docs/reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt) | verbatim copy of `work/shots/notes.txt`, including its ambiguities |

The manifest is the authoritative planning record; Markdown prompts are readable
snapshots of the same full text. Video records also include compact runtime
candidates, with token review pending; the exhaustive specification stays as the
acceptance contract. Fast mode has no negative CFG pass, so the runtime positives
carry explicit desired states. The JSON is **not** an executable `story.yaml`
and existing tools do not enforce its new fields. Update the bible, affected
manifest records and readable snapshots together. Actual submitted prompts,
tool settings and file hashes must be logged when generation starts.

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
- Keep Leo's full canonical rust-orange mane and brown eyes. Approve mouth
  families, including Milo's proposed two rounded gnawing incisors, before use.
- Measure geometry from approved images. Numeric staging and tolerances in this
  packet are proposals, not measurements of saved assets.
- Time the approved script when audio is requested. The 43 coverage shots are
  not enough to assume a complete 8–10 minute edit. Expand the per-line plan
  with additional documented holds/reactions as needed; do not fill time with
  repeated takes or consecutive mouth-mode alternatives.

## Next production order

Owner script review → approved canonicals/reference families → individually
reviewed image pairs → small clip pilot → individual candidate review and owner
selection → separately requested animatic → post/edit.

Expressive/dialogue coverage has a closed-mouth baseline and a separate bounded
mouth-motion alternative. Functional nibbling/gnawing uses an approved contact
mouth and separate closed reaction coverage. Sleeping, silent travel and empty
scenery keep their appropriate state. Mouth motion is not audio-synchronised.

No v4 take is selected. No execution ledger, runtime story or job list is being
presented as complete. The actual v3 clips were unavailable in this checkout;
the repair plan attributes their visual defects to the owner's review and marks
possible causes as hypotheses. The local neutral canonicals and production code
were inspected to ground the identity and pipeline rules.

## Documentation checks completed

The JSON records parse; image IDs and target paths are unique; reference
chains resolve in dependency order; existing historical source paths and local
Markdown links resolve. Readable prompt text matches the manifest, including
runtime assembly fields. The notes archive matches the source byte for byte.
The six critical stream/net handoffs explicitly carry the preceding world state.
These checks establish document integrity, not image or video quality; actual
media review and deployed-tokenizer checks remain pending production.
