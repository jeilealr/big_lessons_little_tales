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
*(Result of the fixed version is recorded in the results log below.)*

**Rule 2.8: one clear camera move, stated once.** "The camera slowly moves
closer to Leo" works. Two moves in one shot ("pulls back, then orbits, then
dives") get merged or ignored.

**Rule 2.9: keep secondary characters in the action, and keep main characters
out of shots they are not in.** The butterflies appeared because the action
names them. For a Milo-only shot, the negative carries "lion, big animal,
second mouse", so Leo does not wander in from the story's context.

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
3. A movement that must travel uses an energetic verb **and** a direction, and
   the camera has a job ("follows alongside").
4. The direction matches how the character faces in the keyframe.
5. What must stay still is stated ("the whole time, eyes closed"), and its
   opposite is in `negative_extra`.
6. Characters not in the shot are in `negative_extra`.
7. At most one camera move.
8. No photographic or realism words.
9. The sheets were not edited for this shot.
10. `--dry-run` printed the assembled prompt and it reads as one clear picture.
11. Two seeds for anything that matters.

## Results log

Update this when a rule is confirmed, refuted or refined.

- 2026-09-26: Rule 2.3 from leo_walks (slow, did not travel) and milo_runs
  (energetic, ran out of frame). Rule 2.5 from the Scene 2 keyframe.
- 2026-09-26: Scene 1 seed 5101, Leo woke up; seed 5102 stayed asleep. Rule 2.7
  fix (s01_establish_v2, seed 5103) rendering.
- 2026-09-26: Scene 2 (Milo runs with a following camera, s02_milo_runs)
  rendering: the first test of Rules 2.3-2.5 inside a scene.
