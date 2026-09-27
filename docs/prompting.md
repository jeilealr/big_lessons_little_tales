# Writing prompts that work

Every rule here was **measured** on this project (Wan 2.2 A14B, felt-animal
style), not taken on faith. Each one names the test that showed it. Read this
before writing any shot, pose or design prompt. The last section is a
checklist to run before a prompt goes to a GPU.

Where the tools put your text: every prompt is assembled as

```
<ACTION>  <Character> is <frozen character sheet>.  The scene is <location sheet>.  <style bible>.
```

`production/shot.py`, `character/character.py` and `production/scene_baseline.py`
all build it this way from `stories/<slug>/story.yaml`. **You write only the
ACTION** (and an optional per-shot negative). Everything else is pasted from
the story bible, verbatim, every time.

---

## 1. Consistency: what text can and cannot do

**Rule 1.1: text alone cannot keep a character the same between shots.**
The full description of the fox, word for word, produced four different foxes
in four prompts (black-tipped ears, eyebrows, different faces). The felt bunny
was a different animal from shot to shot.
*Evidence:* `docs/img/fox_lora_grid.jpg`, row "no LoRA".
*Therefore:* every shot starts from an image of the character (a keyframe,
section 4 of the production guide), and main characters get a LoRA.

**Rule 1.2: never reword a character or location sheet.** The sheet is frozen
text. Change the action, never the description. Rewording is how a second,
slightly different character gets in.

**Rule 1.3: name the details that must never change.** Colours, materials, and
the one distinctive feature: Leo's burnt-orange mane, Milo's oversized pink
ears, the fox's white-stitched inner ears. Vague sheets drift more.

**Rule 1.4: the canonical image must agree with its sheet.** The sheet is pasted
into every prompt forever. If the chosen design image contradicts it (a
felt-ball mane when the sheet says "fluffy mane"), every shot pulls back
towards the text. Rewrite the sheet to match the image you chose, or choose
another image; never keep both.

**Rule 1.5: some details the model will not follow.** It drew Leo's eyes black
in all six design candidates although the sheet says "warm brown stitched
eyes", and it added a cream muzzle nobody asked for. Decide once: accept it and
edit the sheet, or keep asking. Do not leave the sheet saying something the
images never show.
*Resolved for Leo (owner, 2026-09-26): keep the black eyes; the sheet now says
"small black stitched eyes".*

## 2. The action line

**Rule 2.1: one whole-body action per shot.**

| Action (starting from a still) | Result | Evidence |
|---|---|---|
| sit down | reliable | `p_sit.jpg`, fox_sits |
| lie down and go to sleep | reliable | leo_sleeps |
| turn to face the camera / turn around | reliable | `p_turn_camera.jpg` |
| raise a paw and wave "high, side to side" | reliable | `p_wave.jpg` |
| press paws together (the gesture *is* the shot) | works, gentle | milo_paws_together |
| raise the head / look up | **does not register** | `p_head_raise.jpg` |
| hop three times | **character teleports** | felt bunny |
| lie down *and* close the eyes (v2 Leo) | lies down, eyes stay open | leo_sleeps |
| close the eyes, as the whole shot, from a lying frame | reliable (1 of 2 seeds) | leo_closes_eyes_a |

A small movement of one body part, starting from a still, is usually lost.
If a gesture matters, make it the whole shot and describe it big ("raises one
tiny paw **high** and waves it **from side to side**").

**Rule 2.2: the action names only the character's body.**
*Bad:* "The fox looks up at the cotton clouds drifting overhead." The model
animated a cloud sliding across the sky; the fox did not move.
*Good:* "The fox slowly raises his head and tilts his nose upward, ears pricked."
Anything else the action names (clouds, a butterfly, a leaf) is something the
model may animate *instead* of the character. The location sheet already puts
those things in the scene.

**Rule 2.3: locomotion needs an energetic verb.**
*Bad:* "Leo walks slowly and calmly forward on his short rounded legs." Leo
turned towards the camera and back, shuffling, and never moved forward
(`p_walk_slow.jpg`).
*Good:* "Milo runs quickly forward on his tiny feet in a happy scamper." Milo
leaned in and ran out of frame (`p_run.jpg`).
"Slowly", "calmly" and "gently" on a movement verb read as a pose change. For
a walk that must travel, say where to: "walks steadily across the clearing
from the left edge to the right edge", and check the result.

**Rule 2.4: a moving character leaves a static frame.** On a fixed camera the
runner exits the frame within the clip. That is fine for a pose clip; in a
scene, give the camera a job: "the camera follows alongside him" or "a
low-angle tracking shot following him".

**Rule 2.5: the direction in the text must match the keyframe.** Milo's
keyframe had him facing left; the first Scene 2 prompt said "runs to the
right". Read the keyframe before writing the action: a character runs the way
it faces.

**Rule 2.6: turn the character, not the camera, to get new views.** "The camera
orbits around the fox" held identity perfectly but turned only about 30
degrees. "The fox slowly turns around until his back faces the camera" gave a
true back view.

**Rule 2.7: say what must NOT change, and put the opposite in the negative.**
Scene 1, seed 5101: the prompt said Leo sleeps; he opened his eyes and smiled
at the camera. The fix is two-sided:
- action: "stays fast asleep beneath the tree **the whole time**, his eyes
  **closed**"
- `negative_extra`: "open eyes, awake, looking at the camera, standing up"
**Confirmed:** with both halves, seed 5103 kept Leo asleep for all five
seconds while the camera moved in.

![Scene 1 v2](img/s01_v2.jpg)

**Rule 2.8: one clear camera move, stated once.** "The camera slowly moves
closer to Leo" works. Two moves in one shot ("pulls back, then orbits, then
dives") get merged or ignored.

**Rule 2.8b: a camera move that reveals what the keyframe does not show
makes the model invent it, and the invention will not match the location.**
Scene 2 v1: the keyframe was a close-up of the clearing that cut off the tree's
canopy; the camera tilted up and the model drew a canopy of flat felt leaves
instead of the clearing's woolly-ball canopy. Prefer push-ins (they reveal
nothing new), or compose the keyframe from the part of the plate that already
contains everything the move will show.

![Scene 2 v1](img/s02_v1.jpg)

**Rule 2.9: keep secondary characters in the action, and keep main characters
out of shots they are not in.** The butterflies appeared because the action
names them. For a Milo-only shot, the negative carries "lion, big animal,
second mouse", so Leo does not wander in from the story's context.
A secondary character with only a text sheet and no keyframe can still come out
on-model when its sheet is specific: the pastel-blue felt butterfly with cream
edging matched its design exactly in Scene 2.

**Rule 2.10: "runs to the left" plus "the camera follows" is not enough to get
a run across the frame.** In Scene 2 v1 Milo turned his back and ran away into
the depth of the scene, shrinking until he vanished. Say the geometry
explicitly: "seen from the side, Milo runs across the frame from right to left;
the camera glides sideways at ground level alongside him, keeping him in the
centre", and negate the failure ("running away from the camera, back view").
**Refuted as written (Scene 2 v2, seed 5202):** Milo no longer ran into
depth, but he did not run at all: the camera glided sideways and Milo turned
and bobbed on the spot. "Keep him in the centre of the frame" can be met by
moving the camera alone. The Milo run that worked (pose clip `milo_runs`) had a
fixed camera. Current version: side-on geometry, **a fixed camera**, and the
run crosses and leaves the frame ("runs across the frame from right to left
and out of the left edge; the camera stays still"); "standing still, on the
spot, camera tracking" in the negative.
**Confirmed for walking (Scene 6, both seeds):** with a fixed camera and room
ahead in the keyframe, Leo walked along the path across most of the frame
(the earlier "walks slowly" shuffled on the spot). **Partly for running (Scene
7):** Milo ran and left the frame, but diagonally into the plants rather than
side-on. Rows: Leo 6101, Leo 6102, Milo hears 7101, Milo runs 7201:

![fixed camera: walk and run](img/s06_s07_fixed_camera.jpg)

![Scene 2 v2](img/s02_v2.jpg)

**Rule 2.11: story continuity beats a nice plate.** Scene 2 v1 showed Leo's tree
without Leo asleep under it, one scene after we saw him there. When a location
has a landmark tied to a character, either keep the landmark out of frame or
show the character in it.

**Rule 2.12: a camera move goes to the dominant subject, not to the one you
name.** Scene 4: "the camera slowly moves closer to tiny Milo" pushed in on
Leo both times; Milo, 1/7 of the frame high, stayed tiny and his paw gesture
was invisible. A small character's gesture needs its **own close-up keyframe**:
crop the continuity frame around them and upscale it (`compose` with only a
`crop:`), so the shot is still continuous with the one before.
**Confirmed:** from the close-up crop, Milo lifted his paws to his chin and
pleaded, clearly, in both seeds (s04_milo_pleads_v2).

![Scene 4](img/s04.jpg)

*(rows: pleads 4101, pleads 4102, smiles 4201, smiles 4202)*

## 3. Words and framing

**Rule 3.1: materials, not photography.** "needle-felted", "stitched", "wool",
"felt". The style bible already carries "handmade felt stop-motion animation";
do not add "photorealistic", "realistic fur", "cinematic 8k" (they fight the
felt look; "photorealistic" and "realistic animal fur" are in the negative).

**Rule 3.2: locations must be told to fill the frame.** "An empty miniature
set" produced props on a studio table in half the berry-patch candidates. The
location design prompt says: the scene fills the frame edge to edge, no studio
backdrop, no table.

**Rule 3.3: design characters as model sheets.** Whole body, three-quarter view,
neutral pose, alone, on a plain felt backdrop. The plain backdrop is what makes
the later cut-out clean.

**Rule 3.4: give the model a destination when you need one.** The channel intro
came out best when the clip was given a white end frame to arrive at, rather
than asked in words to "end in a white flash".

**Rule 3.5: say what you want, not what you don't want, in the positive
prompt.** The text encoder reads "not frightening" as a mention of
"frightening". Carry the quality with positive words (soft, floppy, knitted)
and put the unwanted thing in the negative. *Status: precaution from how the T5
encoder works, not yet measured here.* The net's sheet was rewritten this way
before its first render.

## 4. Settings that are part of the prompt

| Setting | Use | Why |
|---|---|---|
| frames | 81 for scenes (5 s), 49 for pose clips (3 s) | 81 is Wan's native length; 97 frames ran at 250 s per step and could not finish in a 3 h job |
| seeds | 2 per important shot | seeds differ a lot (the same prompt gave one eyes-open and one eyes-closed Leo) |
| guidance | 3.5 / 3.5 image-to-video; 4.0 / 3.0 text-to-video | the two numbers are the high- and low-noise experts |
| negative | story negative + per-shot `negative_extra` | the per-shot part names this shot's specific failure |

## 5. LoRA captions

Every caption: `<trigger>, <identity>, <pose and view>, <framing>, <setting>, <style>`

```
twcfox, a small orange felt fox, sitting, three-quarter view, full body, on a green felt meadow with felt hills, handmade felt stop-motion animation
```

- The trigger word (`twcfox`) carries the identity. Everything that should
  stay controllable is spelled out so it is *not* absorbed into the character.
- Caption what the frame shows, not what was asked for: the "looks up" frames
  where the head barely rose are captioned "standing, side view".
- Vary the background in the data, or the LoRA learns it: the fox LoRA drew the
  training meadow for a forest prompt from step 1000 on. `composite:` in a
  dataset file places cut-out characters into different location plates.

## 6. Checklist before a prompt goes to a GPU

1. The action has **one** whole-body movement, described big.
2. The action names **only** the character's body (no clouds, leaves, sky).
3. A movement that must travel uses an energetic verb, explicit geometry
   ("seen from the side, across the frame from right to left"), a **fixed**
   camera, and room in the keyframe to travel into (the character faces the
   open side); the failures are in the negative ("running away from the
   camera, standing still, on the spot, camera tracking").
3b. The camera move only shows what the keyframe already contains (push-in),
   or the keyframe was cut to include what the move will reveal.
3c. No landmark tied to a character (Leo's tree) appears without that character.
4. The direction matches how the character faces in the keyframe.
5. What must stay still is stated ("the whole time, eyes closed"), and its
   opposite is in `negative_extra`.
6. Characters not in the shot are in `negative_extra`.
7. At most one camera move, and it goes to the biggest subject (Rule 2.12).
8. No photographic or realism words.
9. The sheets were not edited for this shot.
9b. No "not ..." / "no ..." phrases in the action or sheets: they go in the negative.
10. `--dry-run` printed the assembled prompt and it reads as one clear picture.
11. Two seeds for anything that matters.

## Results log

Update this when a rule is confirmed, refuted or refined.

- 2026-09-26: Rule 2.3 from leo_walks (slow, did not travel) and milo_runs
  (energetic, ran out of frame). Rule 2.5 from the Scene 2 keyframe.
- 2026-09-26: Scene 1 seed 5101, Leo woke up; seed 5102 stayed asleep. Rule 2.7
  fix (s01_establish_v2, seed 5103): Leo stayed asleep. **Rule 2.7 confirmed.**
- 2026-09-26: Scene 2 v1 (seed 5201): the butterfly came out on-model from its
  sheet; Milo ran away into depth instead of across (Rule 2.10); the tilt-up
  invented a different tree canopy (Rule 2.8b); Leo's tree without Leo
  (Rule 2.11). v2: a region of the clearing without the tree, Milo larger, explicit
  side-on geometry, a sideways camera.
- 2026-09-26: Scene 3 (first two-character shot, seeds 5301/5302): Leo wakes,
  eyes wide, surprised, never scary; Milo stays frozen; no identity blending
  between the two. The model also blended the pasted characters into the light
  (no cut-out look left). Leo looks at the camera rather than down at Milo: the
  eye-line was not followed. Take 5302, **approved by the owner**: a look to
  camera is acceptable for this channel, so eye-lines are not worth re-renders.

  ![Scene 3](img/s03_wake.jpg)
- 2026-09-26: Scene 2 v2 seed 5202: tracking camera moved, Milo stayed on the
  spot (Rule 2.10 revised to a fixed camera). Seed 5203 the same: no run; the
  camera arced round him and invented a red-barked tree (Rules 2.8b, 2.11).
- 2026-09-26: LoRA A/B (s03_leo_wakes_lora 5301, s02_milo_runs_v2_lora 5202):
  with LoRAs the location drifted away from the keyframe (new canopy, another
  forest) and identity was no better. Shots stay without LoRAs.
- 2026-09-26: Scene 6 (fixed camera): Leo walks across the frame, both seeds.
  Scene 7: the whole-body turn to camera works (7101); the run leaves the
  frame diagonally (7201). Rule 2.10's fixed-camera version confirmed for
  walking. Scene 2 v3 re-tests the run on the clearing keyframe.
- 2026-09-26: Scene 4: "Leo's face softens into a big warm smile and he nods"
  worked (4202: expression changes register when they are the whole shot);
  4201 turned his head down towards Milo instead (eye-line right, no smile).
  Both "push in on Milo" renders pushed in on Leo (Rule 2.12).
- 2026-09-26: Scene 2 v3 (fixed camera): Milo runs left out of the frame in
  both seeds (5204, 5205). **Rule 2.10's fixed-camera version confirmed for
  running.** Scene 6 net (first prop event): 6202 the net drops and drapes
  over Leo, matching the design picked from its sheet; 6201 the net just
  appeared in a pile beside him. A prop described by its sheet in the action
  line comes out on-model.

  ![Scene 2 v3 and the net](img/s02v3_net.jpg)
- 2026-09-26: Scene 4 v2 (close-up crop of the continuity frame): Milo pleads,
  both seeds (Rule 2.12 fix confirmed). Scene 5: "Milo turns and scampers away
  out of the left edge; Leo stays lying down, watching with a smile" worked in
  5501 (a tiny character's big whole-body move reads even when small, unlike a
  gesture). Rows: plead 4103, plead 4104, leaves 5501, leaves 5502.

  ![Scene 4 v2 and 5](img/s04v2_s05.jpg)
- 2026-09-26: Scene 6 call for help: "calls out loudly, mouth in a big round O,
  worried but not scared" gave a mild cartoon call (6302); 6301 pushed into the
  net with rope over his face, which reads as struggling (not used: findings
  B6). Scene 8 arrival from a wide frame: Milo (1/10 of the frame, at the edge)
  barely moved in both seeds (Rule 2.12 again); v2 uses a close-up crop.

  ![Scene 6 call and Scene 8 arrival](img/s06call_s08.jpg)
- 2026-09-27 (v2 cast): pose clips from the owner's canonicals. Milo paws
  together and Milo worried: clean, on-model. Leo lying down: on-model, but
  **his big glossy cartoon eyes never closed** ("gently closes his eyes" in the
  action and "open eyes" in the negative) and "lies awake" ended sitting with
  paw pads to the camera. Eyes this large seem to resist closing without an
  image that shows them closed; round 2 tries closing the eyes as the whole
  shot, from the lying frame. An owner-made "Leo asleep" still would settle it.

  ![v2 poses round 1](img/v2_poses_round1.jpg)
- 2026-09-27 (v2): **Rule 2.1 again, for faces: split a pose change and a face
  change into two shots.** "Lie down and close the eyes" kept the eyes open;
  starting from the lying frame, "Leo slowly closes his big eyes and falls
  asleep" as the whole shot closed them cleanly (seed 2711; seed 2712 turned the
  eyes into yellow discs, so two seeds). "Lies down like a sphinx, both front
  paws flat on the floor and pointing forward" fixed the paw-pads-up pose.
  Rows: closes eyes a, b; sphinx a, b.

  ![v2 poses round 2](img/v2_poses_round2.jpg)

