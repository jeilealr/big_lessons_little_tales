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
