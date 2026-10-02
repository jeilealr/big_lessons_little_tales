# Creation rules: scripts, images and video

Current policy, updated 2026-10-02, for v4 and future stories. Based on the owner's
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

Preserve earlier-version inputs and reviews. An active production request may
authorize image work; video and assembly remain separately scoped.

## CR-02. Freeze one versioned character identity

An explicit owner redesign precedes the next canonical. For v4 **Milo has a
smooth felt crown with no separate top-hair tuft**. This supersedes all earlier
attempts to shrink the tuft. Retain ordinary felt fibres, eyebrows and whiskers.
First revise the neutral canonical; once approved, derive the pack and every
interaction from that v4 root. Independently erasing hair in many old images
is not proof that their faces and bodies agree.

Until approved, the new canonical is pending; v3 is reference material for the
unchanged traits, not an approved v4 asset. (Status 2026-10-02: the v4 roots
exist, `character/characters/{Milo,Leo}/v4/canonical/full-body_*_neutral_pose_r01.png`,
accepted from the owner's list on 2026-10-01.) Freeze and review:

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
(Status 2026-10-02: S14 images for this order exist at r02 and the owner chose
two of them as the size reference, CR-14; an explicit approval of the order is
not recorded.) Narration must match the chosen number/order of visible breaks
and trap motion.

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
| Milo, ear tips to feet | 0.34–0.36 (ears y≈0.48, feet y≈0.83) | Milo in the measured S14 setup and matching closer/solo shots |
| Leo's mane, top to bottom | ≈0.40 | Milo's whole body ≈ Leo's mane diameter |
| Milo's head, ear tips to chin | ≈0.14 | Milo's head ≈ Leo's face from brow to chin, a little smaller |
| Leo lying or crouched, mane top to paws | ≈0.50–0.52 | |

- Milo alone in the measured closer/solo wide or medium setup keeps the size
  he would have if Leo stood in the same place: about 0.30–0.36 of the frame.
  Other depth planes use their own approved setup anchor (CR-16); for example,
  S05's small same-depth Milo is about 0.18 of frame height. Never enlarge
  him solely because Leo is absent. (s08 and s13 r02 had Milo at 0.6–0.75
  of the frame, which the owner rejected.)
- *Which number applies (clarified 2026-10-02):* the table and the 0.30–0.36
  range describe the S14 trap-path setup only. The current rule is CR-16:
  every setup uses its own approved anchor, and no frame fraction or
  Leo-to-Milo ratio is carried from one setup to another. The two owner-chosen
  anchors differ: at the great tree (S05) Leo's mane is also about 0.39 of the
  frame high but Milo is about 0.18, half the mane and one third of Leo's
  standing-equivalent height (CR-02); in the S14 look Milo is about the mane's
  height. Which ratio the trap scenes should keep is an open owner decision.
  The draft `geometry_profiles` numbers of 2026-09-30 (e.g. `trap_pair` Milo 0.18) were
  replaced on 2026-10-02 by the measured `setups` in `visual_bible.json` (CR-18).
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

## CR-15. Which shots are face close-ups (dialogue format) and which are scene shots

Every scene image record in `prompt_manifest.json` now has a `framing` field.
Decide it before writing a prompt; it controls everything else.

| `framing` | When | Look | Size rule |
|---|---|---|---|
| `dialogue_close_up` | One character speaks, listens or reacts alone; the line is about feelings | Head and upper chest centred in 16:9 (ear tips or mane top y≈0.05, chin y≈0.70), facing the camera, the scene's plate strongly blurred behind, nothing in front (except the net when the character is inside it) | Close-up; no size relation needed |
| `close_two_shot` | A contact action needs both characters readable (nose contact, gnawing) | Both characters, plate softly blurred | Use one shared crop of the approved same-depth pair; preserve the measured actor ratio for that setup |
| `scene_wide` | Arrivals, exits, travel, actions, any shot that shows where we are | Whole bodies on the sharp plate, fixed normal-height camera | Use the approved setup and depth anchor in CR-16; the CR-14 0.30–0.36 range applies to its measured solo/closer setup |
| `empty_plate` | Establishing or time-passing shots | Plate only | n/a |

**Recipe for a `dialogue_close_up` (what fixed s07 and S15):**
1. References, in this order: the record's previous state (for an end frame,
   the accepted start = `approved_start_exact_edit_base`), the canonical
   (`identity_root`), an approved close-up of the same character as
   `close_up_format_reference_framing_only_ignore_its_background`
   (`s15_leo_reflects_end` for Leo, `s15_milo_modest_start` r04 for Milo),
   and one expression from `character/characters/<Name>/v4/expressions/`
   as `face_and_expression_reference`. Drop full-scene and portrait
   references that disagree with this framing.

2. The prompt names the location plate and asks for it "very strongly
   blurred (like a portrait lens at f/1.4)". Without that phrase Nano Banana 2
   kept the background half sharp.
3. Name the expression in words as well as by reference (CR-13 rule 7), and
   say "exactly two eyes and two brows".
4. The end frame changes only the expression: "keep framing, head size and
   background exactly as in reference image 1".
5. Review: framing numbers, blur strength, face side by side with the
   canonical, two brows.

## CR-16. Apparent size across adjacent scene shots (owner, 2026-10-02)

For every wide or medium shot, record the plate, camera crop, ground baseline,
character depth plane, and visible bounding box (normalized `x0,y0,x1,y1`)
for the head or mane and for the complete body. Choose an approved shot of the
same setup as the size anchor. Compare the next shot at equal image size before
acceptance; changes in pose may change the silhouette but must keep the head,
mane, torso and paw size consistent at the same depth. A close-up with a blurred
plate is a deliberate editorial cut and uses its separate close-up framing.

**Great-tree dusk wide-shot anchor:** use `s05_paw_contact_end_r01.png` for
Leo's anatomical and mane scale and Milo's small same-depth scale. S06 barrier
and S08 kindness are on the same plate and ground plane. Leo's mane must not
shrink between them; use the S05 mane diameter and body proportions as the
visual ruler while changing pose. Keep Milo at the same apparent height unless
the shot explicitly moves him in depth. The smaller Leo in the first S06 and
S08 kindness images was repaired on 2026-10-02 (S06 recomposed at the S05
scale; all four S06/S08 kindness endpoints now use that composite; see
`stories/lion_and_mouse_v4/GENERATION_PROGRESS.md`). Compare both start and
end of each pair.

**Trap-path anchor:** use one owner-approved S11 or S14 wide frame to measure
each actor on its stated depth plane. The owner chose `s14_opening_start_r02`
and `s14_milo_clear_*_r02` as the trap-path look (CR-14). If S13 Milo walks
toward the camera, save start and end positions and scale progression; if he
only moves sideways, keep
his ear-to-foot height constant. Preserve Leo's mane and muzzle dimensions
through S11 to S14 unless a shot changes camera or depth.

When an actor moves forward or backward, annotate the initial and final depth
and resulting size in the manifest. A scale jump with no visible depth move or
camera cut fails review. Prefer a measured bounding-box comparison to broad
instructions such as “same size.” Do not apply the solo Milo 0.30–0.36 frame
fraction to a farther-away two-character shot; use the chosen shot's depth
anchor and Leo-to-Milo anatomical ratio instead.

## CR-17. Reusable setup and acceptance contract for every story

Complete this setup **before the first scene image**, including stories with
only one character. Save its measurements in the story's visual bible and
repeat the applicable facts in each individual image prompt. Repetition is
deliberate: a tool call must be understandable without earlier chat or prompts.

| Freeze first | Record and use for every relevant image |
|---|---|
| Character identity | One approved, prop-free neutral root per character; front, side and back when needed; intrinsic colours; head, eyes, brows, nose, muzzle, cheeks, ears or mane, torso, limbs, tail root, material seams and feature counts. List forbidden drift (for example hair, extra limbs, changed nose). |
| Shared cast scale | A same-depth lineup with neutral standing-equivalent heights and head/mane widths. Store ratios between every pair of characters. Repose or lie down without scaling skulls, manes or limbs. |
| Location camera | One approved plate per place, camera and light state; image size, crop, lens/framing, horizon, ground plane, light direction and at least three fixed landmarks. Reuse it or derive an explicitly registered close-up. |
| Shot size and depth | For each scene setup, choose an approved size anchor. Store each actor's normalized head/mane and whole-body box, screen centre, feet/baseline and depth plane in start and end frames. For two or more actors, compare them **in one frame at the same depth** and record their relative scale. |
| Persistent world state | Prop count, holder, contact, damage, attachment, front/back occlusion, and off-screen location; current state comes from the latest accepted shot, never from an older attractive image. |

Every scene prompt repeats the complete frozen identity of **each visible
character**, even if the same words appeared in the previous prompt. It also
states character counts, anatomical counts, the size anchor and measured frame
fractions, depth, foot/contact positions, plate landmarks, expression parts,
prop state, and the only allowed change from the accepted parent. A face
expression reference controls brows, eyes and mouth; it cannot replace the
canonical head, body or prop state. Prop-bearing images are action references,
not neutral identity roots.

At review, compare (1) each face and body against its canonical, (2) every
character against the shared lineup and the setup's previous shot, (3) the
background against its locked plate, and (4) the pair's start and end at final
delivery size. Inspect nose/muzzle shape, whiskers, cheek width, eyes, ears,
seams, mane, all visible paws and tails, ground shadows, scale, occlusion and
object counts. Review close-ups at full resolution and wide shots both full
size and delivery size. A pleasing composition does not excuse identity,
scale or plate drift. A rejected or unreviewed output cannot become a later
reference.

If a model changes protected geometry, make a focused edit from the approved
parent, use a reviewed isolated actor/prop layer on the locked plate, or reject
the take. A request for transparent output is not proof of transparency:
inspect the actual alpha channel and edges, especially whiskers, ears and
tail, before any composite. Reject a matte with background gradients, colour
fringing, clipped parts or leftover objects; never feed that rejected image
into the next generation call. Record the exact tool, prompt, ordered reference paths and hashes,
output hash, inspection note and any unresolved defect. A new result is accepted
only when the actual saved file has been reopened and checked. Maintain one
active target per manifest record where the owner requests replacement; retain
earlier provenance in the record instead of accumulating unnecessary active
`r**` files. Invalidate dependent frames when an upstream identity, plate,
scale or prop state changes, then repair them in dependency order.

**Never mix framings inside one shot.** Wan animates between the start and
end frames; a wide start with a close-up end becomes an unwanted zoom.
(The first `s08_leo_softens` r01 pair had exactly this problem: a wide start
and a close-up end. Both endpoints were remade as close-ups on 2026-10-02.)

**Edits must not add characters.** When the reference images contain the
same character more than once (an approved frame plus a second frame of the
same character), the model may draw that character twice: s05 r05 got two
Milos. For a change of expression or eyes, send only the frame being edited
plus the canonical, and state "exactly one Milo".

## CR-18. One source of truth for every prompt (2026-10-02)

**Why:** the v4 audit of 2026-10-02 found the same character described in many slightly
different ways across 140 image prompts, 62 video prompts and five revision files, size numbers
that contradicted the accepted frames, and references attached without the prompt saying what
they were for. Image models follow the words they are given, so word drift became image drift.

**Rule:** for every story, all prompt text that describes a character, a place, a camera setup,
a size relation, the light or the style lives once in `stories/<slug>/visual_bible.json`.
Prompts are templates (`prompt_template` in `prompt_manifest.json`) that pull it in through
placeholders and add only frame-specific words: pose, position, expression, action, prop state.

- Write each character's `identity` from its approved canonical image, never from memory or an
  older version. Colours are named with the hex sampled from the canonical; proportions as
  ratios; every feature counted. `short`/`sheet` may only reuse its colour words.
- Never write a character's colour or body feature in a record: `lint` rejects a sentence
  that pairs a colour word with a body feature outside the canonical blocks.
- Every attached reference is listed in the prompt (`{{refs}}`) with its role in plain words,
  and every visible character's canonical is attached; a canonical is never attached for a
  character that is not in the frame.
- Sizes come from the setup (`setups.<id>.size`, measured on its `anchor_record`, which every
  start frame attaches as its size anchor) and the lineup (`blocks.cast_scale`); never estimate
  them per record. A frame states only the sizes of the characters in it.
- A reference that shows a character who is not in the frame is not attached (it can draw that
  character in); the edit base comes first, then plate, canonicals, poses, faces, props, size anchor.
- Nothing is appended at generation time: no revision fix text, no `--extra`. The prompt sent is
  the rendered prompt.
- After any change: `python3 production/image_prompts.py build`, then `lint` (0 errors), then
  `md`. The rendered prompt is the only text sent to a tool.

Reference: [`image-prompts.md`](image-prompts.md); workflow: the repo skill
`.claude/skills/consistent-image-prompts/SKILL.md`.
