# Creation rules: scripts, images and video

Current policy, 2026-09-30, for v4 and future stories. Based on the owner's
[v3 render notes](reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt).
The [repair map](../stories/lion_and_mouse_v4/REPAIR_PLAN.md) connects observations
to these rules. Historical experiments in [prompting.md](prompting.md) remain
evidence, but do not override the current rules.

Prompts alone cannot guarantee correct anatomy or motion. Production requires
specific prompts, approved references, registered pairs, persistent state records
and visual review before downstream use. A completed job is not approval.

## CR-01. Production order and owner selection

1. Write the script, proposed shot order and cause-and-effect state table. Plan
   dialogue durations; generate audio only when requested.
2. Owner reviews the sequence before its images, especially revised contact,
   trap and rescue beats. A written storyboard is sufficient for this gate.
3. Freeze the visual bible; create and approve neutral canonicals, scale
   calibration, expression/mouth references, plates and prop states.
4. Create a separate prompt record for every image, edit, reused asset, endpoint
   and mouth variant. Follow [prompt-records.md](prompt-records.md). Review each
   image before using it as another image's reference.
5. Register and inspect start/end pairs and adjacent-shot handoffs using
   [v4-preflight.md](v4-preflight.md).
6. Render a small pilot of individual clips; review it before expanding the batch.
7. Give the owner individual clips, contact sheets and a selection ledger. Record
   the exact selected file, revision, seed, mouth mode, trim and order.
8. **After owner take selection and an instruction to assemble, run the animatic
   as a separate job.** Never append assembly/post to a clip task file. Never
   build an animatic automatically after each batch.
9. Post-process selected material and inspect it again. Upscaling/interpolation
   cannot repair identity, impossible contact or prop causality.

The current task is documentation only. V4 is a draft plan, not authorisation to
produce media. Preserve v2/v3 inputs and reviews; future assets use v4 paths.

## CR-02. Freeze one versioned character identity

An explicit owner redesign precedes the next canonical. For v4 **Milo has a
smooth felt crown with no separate top-hair tuft**. This supersedes all earlier
attempts to shrink the tuft. Retain ordinary felt fibres, eyebrows and whiskers.
First revise the neutral canonical; once approved, derive the pack and every
interaction from that v4 root. Independently erasing hair in many old images
is not proof that their faces and bodies agree.

Until approved, the new canonical is pending; v3 is reference material for the
unchanged traits, not an approved v4 asset. Freeze and review:

- Milo: slender taupe-grey torso, elongated cream belly, youthful rounded head,
  two large circular ears with dusty-rose interiors, dark-brown irises with cream
  sclera, small brown nose, slim bipedal limbs, one thin rosy-taupe tail.
- Leo: compact golden-ochre quadruped, cream muzzle/chest, dark-brown irises with
  cream sclera, four paws, one golden tail with rust tuft; full circular
  burnt-orange/rust mane with the canonical volume and lock pattern.
- Head/torso ratio, muzzle width, ear diameter/spacing, eye spacing, torso width,
  limb thickness and tail root. Chubby Milo, different eyes, extra tails and a
  thinner/crimson mane fail even if the scene looks attractive.
- Lighting may change brightness/shadows, not intrinsic identity colours. Compare
  neutral references as well as the scene light; never recolour the cast to fit
  a background.
- Count anatomical parts, and specify which are visible versus hidden. An
  occluded tail has a recorded location; it is not permission to create another.

The v1 black stitched eyes and 1:6 size ratio are historical. The current cast
has brown eyes. Milo is **one third of Leo's neutral standing height at the
same depth**; this ratio does not use a lying lion's shorter silhouette.

## CR-03. Canvas size, anatomical scale and scene scale

Equal PNG dimensions do not imply equal characters. Equal silhouette heights
also do not imply equal body scale across sitting, standing and running poses.

1. Lock dimensions and camera for each family: square studio canonicals/views,
   matched portrait expressions, exact 16:9 scene endpoints. Record any pad/crop
   transform; never stretch an image to force a ratio.
2. Calibrate neutral standing height and stable anatomical landmarks: head width
   excluding ears/hair, eye spacing, torso length and ground contacts. Measure
   comparable views; a head turn needs perspective-aware review.
3. Maintain anatomical scale through pose changes. Sitting reduces the pose's
   height; the skull does not shrink on standing. Keep ground contacts separate
   from the top of the pose's silhouette.
4. `production/keyframe.py` mattes and tightly crops the entire silhouette, then
   scales it to `h * frame_height`. Its `h` is pose-box height, not anatomical
   calibration. Reusing `h: 0.36` for sitting and standing can cause S02's shrink.
   After registering the poses to equal anatomical scale, compute
   `h_pose = h_neutral * B_pose / B_neutral`, where B is the pose/neutral box
   height in that registered space. Ratios of unaligned source files are invalid.
   Save head scale and foot/contact placement alongside the resulting `h`.
5. Inside a fixed-camera shot use the same plate, crop, focal framing, light,
   depth plane and layer order. Actor depth motion changes actor scale smoothly;
   trees and rocks do not zoom with the actor.
6. Overlay both endpoints at the actual video input size. Inspect after all
   resize/pad/crop operations, not only at original image resolution.

Initial review tolerances (proposed, not measured model guarantees): unchanged
view head/eye spacing within 2%; planted ground contact within 0.5% of frame
height; static landmarks within 0.2% of frame dimensions after a common camera
transform. Visible identity/scale jumps fail regardless of tolerance. Intentional
motion uses its recorded trajectory; do not compare moving feet as planted feet.

## CR-04. Registered start and end images

Every v4 character shot needs approved start AND end images. Derive the end from
the approved start using the same canonical roots and plate. Unrelated attractive
stills are not a pair.

- Record pair ID, camera profile, dimensions, crop, colour treatment, depth and
  exactly what may change. Everything else is protected. Use local image edits,
  masks or composition where supported. Restore protected regions from the base
  or reject a candidate if whole-image regeneration moves them.
- Endpoints reduce drift; inspect the middle too. A perfect last frame cannot
  excuse a distorted paw, eye, tail or prop halfway through.
- For state changes, the end depicts the actual result. Identical start/end is
  allowed for an explicitly planned hold/loop, never to depict a rope breaking.
- Exits have a clean end plate and a continuous visible path through a frame
  boundary. An empty endpoint alone may cause disappearance. If necessary cut
  from a validated pre-exit frame to the empty scene instead of accepting a fade.
- The owner accepts slight close-up reframing (S07). Make it intentional, record
  start/end crop and transform, keep anatomy and blurred context consistent.
  Prefer a controlled digital crop in post to a generative camera move.

## CR-05. Expression, mouth and gesture controls

Before speech alternatives, approve closed, slightly open and moderately open
mouth references in identical face framing. Freeze jaw hinge, muzzle, lip
outline, mouth interior, tongue and dentition. Create Leo's just-woken surprised
reference from his asleep pose; opening the eyes must reveal the same brown eyes.

For **every speaking or expressive character beat**, render separate named modes:

- `closed`: preferred edit-safe baseline. Lips closed, jaw steady; eyes/expression
  carry the beat. Paws and tail stay anchored.
- `mouth`: gentle mouth movement using the approved mouth family, with onset,
  offset, opening limit and quiet lead/tail specified. This is editorial coverage,
  **not phoneme-synchronised audio**. Record usable motion intervals and speaker.

A different seed is not a different mode. Both modes need compatible endpoint
images: a closed clip cannot end on an open mouth. Sleep, silent locomotion and
empty scenery remain silent. Gnawing needs functional mouth contact; its safe
backup is a separate closed observing/reaction shot, not sealed-mouth chewing.
The closed alternative to a call is a worried reaction with off-screen audio.

Default body control: paws lowered/resting, shoulders and torso steady, tail
settled in its recorded position. A smile does not authorise waving, pointing,
hand clasping, arm lifts or tail flicks. An essential gesture gets its own shot,
contact path and endpoints. Simplifying unreliable decoration in any future
character requires a versioned canonical decision, as with Milo's hair.

V4 proposes two small rounded cream upper incisors for Milo's gnaw reference,
subject to mouth-design approval. Keep that tooth design whenever visible.
Leo never acquires fangs. Avoid a global `visible teeth` negative when approved
teeth are required, or a global `mouth open` negative for a speech variant.

## CR-06. Locations and ambient motion

One approved plate per place/camera/light. New lighting preserves its geometry.
Close-ups use the same scene state; blurring a wrong place or old net state does
not fix it. Freeze trunk centres, roots, rocks, horizon, path edges, ground plane
and light direction. Record at least three static landmarks. Preserve identical
protected background pixels in still pairs where possible.

Each place has an ambient profile reused across its shots:

- Gentle leaf/grass-tip movement; stems, roots and trunk bases stay fixed. Canopy
  leaves may flutter; the tree skeleton does not bend or slide.
- Visible water continuously ripples/flows in the approved direction. It cannot
  freeze between S01 and S02; banks, rocks and water level stay fixed.
- Visible clouds drift slowly in one consistent direction; stars may twinkle
  softly in a cutaway. Sun and time of day remain fixed within a shot.
- Soft leaf shadows may shift slightly with the same breeze; no global flicker
  or relighting. Inspect amplitude/direction continuity across adjacent cuts.

Keep the main action dominant. Add a short frozen ambient clause rather than
another story about clouds. In empty scenery, ambient motion is the main action.
A difference of location/light may justify another profile; record that change.

## CR-07. Prop permanence, contact and net topology

Give each prop an ID and start/event/end state: count, holder, position, attachment
points, layer order and visibility. Carry it into the next shot. Hidden, off-screen
and removed are different states.

- One acorn stays in Milo's paws while he notices the time in the proposed v4
  plan. A separate placement shot leaves it at a recorded ground point before he
  travels. A falling object follows a visible path to a resting place; it never
  disappears. Later views retain it if that place is visible.
- Leo stays asleep until Milo contacts his paw. Contact precedes waking. A fast
  tumble/nose aftermath can be an explicit editorial cut, not a morph from a wide
  scene to a close-up under a supposedly fixed camera.
- One net: suspended -> falling -> draped -> frayed -> severed -> opening ->
  slipping behind Leo -> fallen behind him. After release the overhead branch
  is empty in all later frames, including close-up backgrounds.
- Establish why cutting the selected strand opens the net. The v4 proposal uses
  a closure strand securing an existing fold; releasing it cannot delete other
  mesh strands. Review this topology in the intact state before any bite image.
- Annotate the selected strand, two neighbouring knots and bite point outside
  the generated picture. Cut at the bite point. Track the resulting two ends
  and their occlusions. A single cut does not delete a length of rope. Any
  detached fragment gets an ID, a falling path and a resting location.
- A broken strand remains broken. Additional breaks require distinct strand IDs
  and visible work or a planned time-ellipsis cut with cumulative damage. Never
  return to an intact net for a second magical snap.
- Preserve rope/leaf/paw/body occlusion order. Leaves cannot pass through intact
  netting. The net slips behind Leo by gravity, without teleporting sideways or
  reforming around him after release.
- Milo remains present or has an explicit off-screen place/entrance. A Leo-only
  start cannot simply gain Milo at the endpoint.

The proposed S14 order in the v4 packet needs owner review before images.
Narration must match the chosen number/order of visible breaks and trap motion.

## CR-08. Readable locomotion and source quality

Use an approved side-view running pose, upright bipedal Milo, a fixed camera,
one direction and a clear ground lane. Specify start/end position, depth, gait
and ground contacts. Exactly one mouse follows one continuous path; his single
tail stays attached. Avoid combining a run, glance back, jump and camera track.
For S09 use a forward-looking careful run; a glance back can be a separate hold.
Depth movement (S10) changes actor scale, not background scale.

Sharp source images need enough actual subject pixels, legible eyes/face, intact
paws and silhouette separation. Inspect at 1280x720. An initial planning floor
for solo running Milo is about 180 pixels of upright-equivalent height at 720p
(25% of frame height), subject to visual review, not a guarantee. If correct
cast scale makes him too small, give him a separate closer shot. Do not enlarge
him relative to Leo. Avoid smear, foreground obstruction and detail crossing
his face. Upscaling cannot restore missing original features.

## CR-09. Exhaustive records and focused model prompts

Every image record includes ordered reference paths and roles, purpose, counts,
geometry, state, full positive text, exclusions, edit scope, protected areas and
acceptance checks. Submit complete frozen identity/style descriptions; do not
submit only “same as before”. Record exact submitted prompts, output location,
tool/model/seed where exposed, reference hashes and selected output hash. Mark
unknown settings `unknown`; never invent provenance for earlier images.

Every video record adds paired dependencies, event timeline, camera/ambient
clauses, prop transitions, mouth mode, candidate naming and reject criteria.
The runtime instruction focuses on one action; exhaustive planning must not
become a pile of conflicting requests to the model. Keep the full specification
and a separately recorded, complete runtime candidate. Measure its actual token
length against the deployed text encoder before submission; never silently lose
critical constraints to truncation. Fast Lightning runs at CFG 1 with no negative
pass, so desired states must be present positively and in the approved images;
negative lists alone do not control this mode.

Use explicit local reference paths when supported. Inspect the actual files and
confirm ordered roles. Filenames alone did not catch I-07's wrong sleeping scene.
Reopen the saved output; a preview or save command is not visual verification.

## CR-10. Revisions and downstream invalidation

Use v4 paths and revision IDs; preserve v3. Approved-image edits produce a new
revision. Identity, plate, prop or prompt changes make dependent prompts,
installed packs, mattes/crops, keyframes and renders stale. Rebuild in dependency
order. Current scripts may skip existing outputs; use new revisioned paths and
shot names, or explicitly rebuild affected files. Do not trust stale caches.

Documentation states: `draft`, `needs_reference`, `ready_for_image_review`,
`approved_image`, `ready_for_pair_review`, `approved_pair`, `render_candidate`,
`owner_selected`, `rejected`, `stale`. Current scripts do not enforce these gates.

## CR-11. Anatomy readability and prop layers

Keep identity references prop-free. Acorns, nets and other story objects belong
to separate prop references and scene passes; an action-pose guide may show a
character's hands or mouth contacting an object, but must not replace the
character's canonical anatomy reference. For a held object, preserve a clean
grip pose and composite the approved prop at the contact point so the fingers
or paws visibly meet it.

A prop that crosses a character in depth remains one continuous world object.
For compositing, derive front and rear occlusion masks from that same approved
prop source; do not redraw it as multiple objects or change its mesh, count,
scale, knots or state. In particular, an intact net over Leo may have strands
behind his body and strands in front, with a continuous path through the
occlusion. Preserve all broken ends and the net's state across cuts.

For Milo, the pale belly ends above the crotch. Keep a visible taupe-grey gap
between the two slim legs from the crotch down; do not let the cream belly form
a white bridge or wedge between them. Keep both legs distinct and planted, with
the feet separated enough to read clearly. Retain his approved slim waist,
softly rounded cheeks, fine visible whiskers on both sides, smooth crown,
brown eyes, two large ears and one attached tail. Do not compensate for a
cropped or incomplete body by stretching or enlarging the head.

For full-body or medium shots, state the complete visible anatomy in the prompt:
Milo's crown through both feet and entire tail; Leo's full mane, torso, four
paws and tail. Keep a margin around ears, mane, paws and tail. Place solo
characters at the established lower-centre/screen position unless the approved
shot plan specifies otherwise. Close portraits are intentional only when the
shot plan calls for a face crop; preserve a complete body in all other shots.
When using a composited character pass, match contact shadows, edge softness,
light direction, depth blur and ground contact to the locked plate so the
character does not read as a pasted cutout.

Before accepting an image, inspect leg separation, whiskers, cheek volume,
whole-body visibility and character-to-plate integration at full resolution
and at delivery size. Reject any white belly bridge between Milo's legs, missing
whiskers, visibly clipped anatomy, floating feet, hard cutout edges, or altered
plate landmarks.

## CR-12. Expression references and face seams

Keep expression references as clean, prop-free face or head studies with the
canonical skull, muzzle, cheek width, ear spacing, eye spacing and whiskers.
Use them to guide only the eyes, brows and mouth in a scene. Anchor every scene
to an approved full-body character and the locked plate; a face study alone
must never supply an entire scene actor or replace the torso, paws or tail.

Milo and Leo may retain their subtle central felt stitching, but it should
read as a material seam, not a dark line cutting across the face. In close
shots, keep the seam low contrast and consistent with the canonical reference.
Inspect the forehead, muzzle and silhouette at delivery size for a strong
or misaligned seam before acceptance.

## CR-13. Generated-image gates (lessons from the Gemini r02/r03 pass, 2026-10-02)

Each rule names the defect that made it necessary. Tooling: `character/gemini_image.py`
(`docs/gemini-images.md`). These rules apply to any image model.

1. **Whole bodies unless the shot is a face close-up.** In a wide, medium or
   two-shot, every character's body stays in frame and attached: a lying lion
   shows mane, torso, paws and tail. A head with no body is a reject.
   (s05 r02: Leo became a floating head.) Anchor contact shots on the
   previous shot's camera and pose, and say "no part of the body is cut by the
   frame edge".
2. **Side-by-side identity gate.** Before accepting a frame with a face,
   compare it at full size beside the canonical (the review sheet puts the
   identity roots first in every row). Check colour temperature (warm taupe,
   not cool grey), iris size and colour, face seam, cheek width and the
   head-to-body ratio. (s08 r02: off-model Milo face accepted at thumbnail size.)
3. **Reuse an approved frame from the same setup.** When a character
   reappears in a setup the owner has already approved, edit that frame and
   change only the expression or pose; do not generate the character afresh.
   (s08 r03 was fixed as an edit of the approved s07 frame. The same approach
   held Milo's face across S13 and S15.)
4. **Scale as frame fractions and comparisons.** "Same size as reference 1"
   is ignored. Write "from ear tips to feet y=0.55 to y=0.87, centred
   x=0.55" and relative statements such as "Milo's whole body is as tall as
   Leo's head" or "his head is smaller than Leo's muzzle", plus depth ("at
   the same depth as Leo"). (s02, s05, s13 grew Milo to twice his size.)
5. **Staging references are staging only.** An older-version image used for
   composition leaks its identity (the V3 references gave Leo a red, short
   mane). Name the reference's role and restate the identity explicitly.
6. **Spell out small props.** "A small plain round felt disc with no markings,
   half hidden under leaves". (Unspecified, the trigger got an "X".) A prop
   whose state is fixed (a net with the lion inside) is named in every
   frame where it appears. (One s13 take showed the net empty.)
7. **Name the expression parts.** Image models default to a smile. Write
   brows, eyes and mouth explicitly: "brows high, eyes wide, mouth closed in
   a small neutral line, no smile".
8. **Continuity cascades.** When an upstream world state changes (the net
   staging), mark every downstream frame that shows the old state `stale` and
   redo the chain in dependency order. Redo a start and its end together, and
   generate each end from its accepted start.
9. **Plate check per take.** A model can silently replace the locked plate
   (Pro did, on several takes). Compare background landmarks with the
   previous frame before judging the character.
10. **Record every take.** Each API call is logged in
    `stories/lion_and_mouse_v4/revisions/gemini_ledger.csv`; each accepted take
    in the manifest stores its prompt, references, model and review note, and
    the replaced result stays under `superseded`.

## CR-14. Character size guide and expression close-ups (owner, 2026-10-02)

**Relative size.** The story bible fixes Milo's standing height at one third of
Leo's. The owner chose `s14_opening_start_r02` and `s14_milo_clear_*_r02` as
the reference look. Measured on them (fractions of frame height, 16:9):

| What | Measured | Use as |
|---|---|---|
| Milo, ear tips to feet | 0.34–0.36 (ears y≈0.48, feet y≈0.83) | Milo in any wide or medium scene shot |
| Leo's mane, top to bottom | ≈0.40 | Milo's whole body ≈ Leo's mane diameter |
| Milo's head, ear tips to chin | ≈0.14 | Milo's head ≈ Leo's face from brow to chin, a little smaller |
| Leo lying or crouched, mane top to paws | ≈0.50–0.52 | |

- Milo alone in a wide or medium shot keeps the size he would have if Leo
  stood in the same place: about 0.30–0.36 of the frame. Never above 0.40
  unless the shot is a planned close-up. (s08 and s13 r02 had Milo at 0.6–0.75
  of the frame, which the owner rejected.)
- Write the size into the prompt as frame fractions plus a comparison (CR-13
  rule 4), and pass one of the reference frames above as
  `camera_and_character_scale_reference`.

**Dialogue and expression close-ups.** When a character speaks or reacts
alone, use the `s15_leo_reflects` format: head and upper chest fill the
centre of the 16:9 frame (ear tips or mane top near y=0.05, chin near
y=0.70), facing the camera, in front of a strongly blurred version of the
scene's plate. The face comes from the expression references:

- `character/characters/Milo/v4/expressions/` and `.../Leo/v4/expressions/`
  each hold 11 head studies (manifest group `expressions`, records
  `M_EXPR_*` / `L_EXPR_*`). They were made from the V4 closed-mouth
  portrait, taking only the expression from the V3 set.
- Pass the matching `*_EXPR_*` record as `face_and_expression_reference`
  (close-ups) or `expression_reference_copy_brows_eyes_mouth_only` (wide
  shots). An expression missing from the set is added as a new record first
  (about $0.03 on Lite), never improvised in a scene.
- Every face keeps exactly two brows and two eyes. (`s07_leo_annoyed_end_r01`
  had a second brow line painted over the first.)
