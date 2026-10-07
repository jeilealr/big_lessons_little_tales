---
name: consistent-image-prompts
description: Use before writing, editing or sending ANY image, keyframe, plate, expression or video prompt for a story in this repo (stories/<slug>/), before accepting a generated image, and when starting a new story's characters and locations. Keeps every character identical to its canonical (features, colours, brightness), every background identical to its locked plate, and every character size consistent with the story's size lineup and setup anchors, by building all prompts from one visual bible, linting them, and reviewing each result side by side.
---

# Consistent image prompts

Consistency is the product. A child watching notices a mane that changed colour, a mouse that
grew between two cuts, or a tree that moved. Every rule below comes from such a defect
(`docs/creation-rules.md` CR-11 to CR-18 record the evidence; the reference is
`docs/image-prompts.md`).

**One source of truth.** For a story `stories/<slug>/`:

| File | Holds |
|---|---|
| `visual_bible.json` | `characters` (canonical `identity` text, `sheet`/`short` for video, `mouth` design, palette with hex, proportions, review checklist, drift phrases, canonical image and record), `cast_scale` (same-depth size lineup), `locations` (one locked plate each: description, landmarks, light), `setups` (camera, background treatment, measured character sizes and the size-anchor record per camera setup), `blocks` (shared text: style, light and colour, studio, edit rules, world-state rules), `reference_roles` (what each kind of attached image is for, in plain words) |
| `prompt_manifest.json` | one record per image: `prompt_kind`, `label`, `setup`/`framing` and `frame` for scene frames, `counts`, `ordered_references`, `prompt_template`; one entry per video shot with variant templates |
| `prompts/*.md` | readable copies, generated |

Prompts are **templates**. Shared facts enter only through placeholders:

| Placeholder | Becomes |
|---|---|
| `{{identity:<char>}}` | the full canonical description (image prompts, video full specification) |
| `{{short:<char>}}` | the one-sentence description (video runtime prompt) |
| `{{mouth:<char>}}` | the approved open-mouth design (open-mouth studies and `<shot>_open` talking key frames) |
| `{{setup:<id>}}` | camera, background (plate text, blurred for close-ups) and measured sizes |
| `{{plate:<loc>}}` | location description, fixed landmarks and light |
| `{{block:<name>}}` | shared text, e.g. `style`, `cast_scale`, `light_and_colour`, `net_world` |
| `{{refs}}` | every attached reference, numbered in attachment order, with its role and file name |
| `{{frame}}` / `{{frame:<record>}}` | what this frame shows (the record's `frame`), or another record's |

The record's own words describe only what is unique to that frame: pose, position, expression,
action, prop state. **Never write a character's colour or body feature in a record** (not in
the template, `frame` or `label`): that is a second description that competes with the
canonical. Lint rejects any sentence that pairs a colour word with a body-feature word outside
the bible's character text.

Tool: `production/image_prompts.py` (`lint`, `build`, `show`, `md`, `review`, `new-story`;
`--story <slug>`, default `lion_and_mouse_v5`).

## A. Starting a new story (before any scene image)

Fastest start: copy a story's `packet_source.py` (e.g. `stories/tortoise_and_hare_v1/packet_source.py`)
to `stories/<slug>/packet_source.py`, write the script lines, characters, places, camera setups and
shots there, and run `python3 production/story_packet.py stories/<slug>/packet_source.py`. It writes the
bible, every prompt record, the narration line list and SCRIPT/SHOT_PLAN/README; then build, lint, md.
Use it only until the first image is accepted; afterwards edit the bible and records directly. The
steps below say what each part must contain.

1. `python3 production/image_prompts.py --story <template story> new-story <slug>` creates
   the bible skeleton and an empty manifest, copying the generic blocks, reference roles and
   lint settings.
2. **Characters.** For each character, approve one prop-free, neutral, full-body canonical on a
   plain studio backdrop, and add it as a manifest record (`canonical_record`). Write
   `characters.<id>` **from the image, never from memory or an older version**:
   - `identity`: 180–260 words, positively worded. Cover silhouette and proportions as ratios,
     head and crown, ears, eyes (iris colour, sclera, highlight, size relative to head), brows,
     nose shape and colour, muzzle, mouth, cheeks, whiskers on both sides, seams, torso, belly,
     limbs, paws and toes, tail root, length and tip, mane or hair, surface texture, feature
     counts. Name each colour once, with the hex sampled from the canonical, and use the same
     colour word everywhere. End with the brightness rule: intrinsic colours stay the same;
     only scene light tints them.
   - `sheet` (one predicate line) and `short` (`"<Name> is <sheet>..."`) for video prompts.
     They may only use colour words that also appear in `identity` (lint enforces this).
   - `mouth`: the open-mouth design (interior, tongue, which teeth may show), from the
     approved mouth study.
   - `palette`, `proportions`, `checklist` (12–20 checkable review items) and `drift_phrases`
     (observed or likely drift, e.g. "cool grey", "crimson"; lint rejects any prompt that
     contains one).
3. **Size lineup** (`cast_scale` and `blocks.cast_scale`). Put all characters side by side at
   the same depth, or measure them against a shared reference. Record standing heights and head
   or mane widths as ratios between every pair. A pose change never rescales a head, mane or limb.
4. **Locations.** One approved empty plate per place, camera and light, each its own record.
   Record `description`, at least three `landmarks` with frame positions, `light` (direction,
   time of day, colour temperature) and `plate`. A new light state reuses the same geometry.
   For a new location/camera, the first plate is the seed and is the only plate generated with no
   location-image reference, because no approved master exists yet. After owner approval, register
   its record ID as `composition_master_record` in the location entry; its manifest target path is the composition master. Every same-location/camera variant must attach
   that master as `edit_base` in `ordered_references`, even when only time of day changes; always
   derive variants directly from the master, not from one another. If the master is omitted, stop
   and repair the record—text describing a plate is not an image reference. No reference means a
   fresh scene, never an implicit link to an earlier image. Compare the result beside the master
   and check its landmarks. If season or camera changes intentionally alter geometry, register a
   distinct profile and state the allowed changes.
5. **Setups.** Every camera setup (location + framing) gets `camera`, `background_treatment`
   for close-ups, `size` (measured frame fractions per character at its depth plane, plus a
   comparison sentence such as "Milo's whole body is about as tall as Leo's mane is wide") and
   `anchor_record`, the approved frame the numbers were measured on. Use the four framings of
   CR-15: `dialogue_close_up`, `close_two_shot`, `scene_wide`, `empty_plate`.
6. Make the expression set before close-ups: one studio head study per needed emotion, each an
   edit of the approved closed-mouth portrait (only brows, eyelids, gaze and mouth change). Approve
   the single open-mouth study `*_OPEN` per speaking character too (`characters.<id>.mouth`): it is
   the one speech-mouth shape every talking clip reuses (CR-19).

## B. Writing or changing a prompt

1. Edit the bible (shared text) or the record (`prompt_template`, `frame`, `label`,
   `ordered_references`), never the rendered `positive_prompt`.
2. A scene template contains, in this order: the frame line (canvas, start/end of which shot,
   the setup's label); `{{refs}}`; for an end frame `{{block:edit_end_frame}}`; the cast line
   with exact counts; one `{{identity:...}}` per visible character; `{{block:cast_scale}}`
   when two or more characters share the frame; exactly one `{{setup:...}}`;
   `{{block:light_and_colour}}`; the world-state blocks of the props in this place and one
   sentence for the current prop state; `This frame shows: {{frame}}.`; `{{block:style}}`;
   `{{block:final_check}}`.
3. `frame` says only the pose, position (x/y fractions of the frame), facing, expression
   (named by brows, eyelids, gaze and mouth), contacts and prop state.
4. **References.** `ordered_references` is the exact list a generator attaches, in this order:
   the edit base or the previous accepted frame first, then the locked plate, the canonical of
   **every** visible character (and never of an absent one), pose, expression, mouth and prop
   references, the setup's size anchor, framing and staging references. Each has a `role` from
   `reference_roles`; `{{refs}}` writes the list into the prompt in plain words, so the prompt
   itself says which image is which and what to take from it. An older version's image may only
   be `staging_only`, `expression` or `camera_geometry`. An end frame's first reference is its
   start frame (role `edit_base`).
5. Positive wording only: fast video mode has no negative pass, and image models follow positive
   specifics better. Exclusions live in `negative_prompt` as review criteria.
6. Sizes are numbers plus a comparison and come from the setup; never estimate them per record.
7. `python3 production/image_prompts.py build && python3 production/image_prompts.py lint`
   must end with **0 errors**. Then `md` refreshes `prompts/*.md`; `show <record>` prints one.
8. **Talking clips need an open-mouth key frame (CR-19).** A `mouth` video variant only
   interpolates between its two key frames, so the open mouth must be one of them. Every
   dialogue close-up with a `mouth` variant gets a scene record `<shot>_open`: an edit of the
   closed start frame (`{{block:edit_open_mouth}}`, first reference `edit_base`) that opens only
   the mouth to the character's approved speech shape, attaching the start frame, the canonical
   (`identity_root`) and the character's `*_OPEN` study (`mouth_design`), with `{{mouth:<char>}}`.
   Each variant has its own `start_image`/`end_image`: `closed` runs start→end, `mouth` runs
   start→`<shot>_open`. `story_packet.py` emits these for new stories; keep them when editing by
   hand (Lion and Mouse v4 is exempt — its clips are nearly final).

## C. Generating

- The owner remains the default image maker. When the owner asks the agent to create an image,
  use the built-in OpenAI `image_gen` tool by default. Gemini is an optional provider; use
  `character/gemini_image.py` only when the owner chooses Gemini and API access is configured.
- Send the rendered `positive_prompt` and only its `ordered_references`, in order. Do not add
  unstated character, scene or reference details. If an image needs a correction, record the
  correction as a separate edit prompt with its parent image and tool in the manifest result;
  do not leave generation or edit prompts undocumented. Changes to the intended image prompt
  itself go into the bible or record template first, then `build` and `lint`.
- Built-in `image_gen` saves generated files under `$CODEX_HOME/generated_images/`; copy the
  selected output into the record's exact `target` under this story's folder. Preserve the raw
  generated source under that target directory's `.review/` folder when normalization is needed.
  Record the tool, model/version when exposed, exact prompt(s), ordered reference paths and hashes,
  output hash, normalization and review note. Never leave a project-referenced image only in
  the generated-images cache.
- `character/gemini_image.py gen --story <slug>` is the optional API workflow; it refuses to run
  while lint has errors. Gemini candidates and accepts stay within the selected story's target
  folders and manifest.
- Never pass a rejected or unreviewed image as a reference.
- One change per edit. To change an expression or a pose, edit the approved same-setup frame;
  do not regenerate the character.
- If the tool cannot keep the plate, use a focused edit or a reviewed isolated layer on the
  locked plate (CR-17); never accept a moved background.

## D. Review gate (every image, before it becomes a reference)

`python3 production/image_prompts.py review <record> --image <candidate>` writes
`work/review/<record>.jpg`: the canonicals, expression references, setup size anchor, plate and
previous shot's end above, the candidate with a 0.1 grid below. Check at full size and at
delivery size:

1. **Identity:** every item of `characters.<id>.checklist` against the canonical (nose and muzzle
   shape, eye size and colour, brows, whiskers on both sides, ears or mane, seams, limb and tail
   counts, colour temperature and brightness).
2. **Size:** read the character boxes on the grid against the setup's `size` numbers and the
   anchor. Same depth means same size: a jump without a depth move or cut fails. A shared frame
   keeps the lineup ratio.
3. **Background:** the landmarks sit where the plate has them, with the same light and crop.
   For close-ups, the plate is blurred but not replaced.
4. **Pair:** the end frame equals the start except for the stated change.
5. **World state and counts:** props, damage, contacts; exactly the counted characters; two
   eyes and two brows each; one tail each; no text.

Record the result in the manifest (tool, model, the references actually sent with their
hashes, the prompt actually sent, output hash, review note), and if an identity, plate, size or prop state changed
upstream, mark dependent frames stale and redo them in story order.

## E. Pitfalls already paid for

- A second description of a character in a record (e.g. "his rust mane" in shot text) made
  frames disagree. Lint's identity-conflict check now blocks it.
- Correction texts appended at generation time (revision files, `--extra`) made the sent prompt
  differ from the recorded one and attached references the prompt never mentioned.
- Older-version references leaked their identity (red, short V3 mane; tufted V3 Milo).
- A canonical attached for a character who is not in the frame drew that character in.
- End frames re-enlarged a character that the start had fixed; compare each end with its start.
- Expressions drift to a smile unless brows, eyes and mouth are named.
- A wide start with a close-up end becomes a zoom in video; keep one framing per shot.
- A talking clip with two closed key frames invents a different open mouth each render; give the
  `mouth` variant a `<shot>_open` end key frame built from the one approved `*_OPEN` study (CR-19).
