# The Lion and the Mouse v3: images to create (to-do)

One entry per image: tick it when the image is saved. Each entry has the
**file** to save as (paths from the repo root), the **references** to attach
in the image tool, and a **prompt** to paste. Append the matching style block
below to every prompt. Background and reasons: `ASSETS.md`; location DNA:
`locations_dna.yaml`.

Priority (v2 could not make these shots): the net set (N-02..N-09),
M-06 run, M-14/M-15 gnaw, I-02/I-03/I-06/I-07, and the great_tree and
distant_forest plates. They are marked **(P)**.

## Style blocks (append to every prompt)

**STUDIO** (single-character images):
> Handcrafted wool-felt stop-motion storybook miniature, softly stuffed matte
> felt, tactile fuzzy wool fibres, delicate visible stitching, charming
> handmade irregularities. Warm off-white seamless studio floor and backdrop,
> soft even studio light, small soft ground shadow. The whole character in
> frame (ears, paws, tail), one character only. Keep the exact identity of the
> reference: same face, colours, proportions, materials. No text, no logo, no
> watermark, no clothing.

**LOCATION** (plates):
> Handcrafted wool-felt stop-motion storybook miniature set, matte felt
> surfaces, visible delicate stitching, rounded soft shapes, warm children's
> storybook palette, miniature diorama photography, shallow depth of field.
> 16:9, the scene fills the frame edge to edge, no studio table or backdrop.
> Empty: no animals, no characters, no text.

**SCENE** (two characters, or a character in a location):
> Handcrafted wool-felt stop-motion storybook miniature, 16:9. Keep both
> characters exactly like their reference images (face, colours,
> proportions, materials). Milo (the mouse) is one third of Leo's (the lion's)
> standing height. Keep the location exactly like its reference plate. No
> text, no logo, no watermark.

Canonicals (attach as references):
`character/characters/Leo/v3/canonical/full-body_leo_neutral_pose.png` (LEO),
`character/characters/Milo/v3/canonical/full-body_milo_neutral_pose.png` (MILO).
For close-ups also attach one image of the existing expression set
(`character/characters/<Leo|Milo>/v3/expressions/`) so the framing matches.

File names in the v3 folders have no `_01` suffix (renamed 2026-09-29): one
image per name; a second take of the same image gets `_02`, `_03`. The v2
folders keep their old names (the v2 story uses them).

---

## 1. Locations (plates) - LOCATION block

**Owner decision (2026-09-28): one normal-height view per place, no
low (mouse-eye) angles.** The low-angle images were not good or stable, and
the v2 videos already showed Leo and Milo at a good relative size in normal
views. So Leo and Milo share the same plate; close-ups are made by the
pipeline (a crop of the plate, blurred behind the character). A second image
of a place is only made for a different time of day or a clearly different
part of it. IDs of removed plates are left out (L-02, L-05, L-07, L-08, L-10,
L-11, L-15, L-17, L-18, L-20). For a new lighting, attach the place's first plate
as the reference and change only the light.

### stream_bank (Milo's feeding ground)
- [x] **L-01 Stream bank, wide, afternoon**
  File: `character/locations/stream_bank/stream_bank_wide_afternoon.png` · Refs: none
  Prompt: A felt stream of layered blue and teal felt with small white stitched ripples running left to right, low berry bushes with round red felt berries on the near bank, tall soft green felt grass tufts, a few acorns on the ground, a hollow felt log on the right bank, rounded felt trees behind. Warm golden afternoon light from the left. Wide establishing view.
- [x] **L-03 Stream bank, wide, sunset**
  File: `character/locations/stream_bank/stream_bank_wide_sunset.png` · Refs: L-01
  Prompt: Exactly the same view as the reference, but at sunset: low orange sun, long soft shadows, the sky turning pink.

### fork (the safe path and the shortcut)
- [x] **L-04 Fork, wide, sunset**
  File: `character/locations/fork/fork_wide_sunset.png` · Refs: L-01 (for the world's look)
  Prompt: A felt path splitting in two: the left path curves around a sunny open meadow with small felt flowers; the right path goes straight into a darker, quieter part of the forest with tall close-set felt trees. No sign, no text. Sunset: low orange sun, the first blue dusk on the shortcut side.

### shortcut (the quiet forest path)
- [x] **L-06 Shortcut, side view, dusk**
  File: `character/locations/shortcut/shortcut_side_track_dusk.png` · Refs: L-04
  Prompt: A narrow mossy felt path running left to right across the frame under tall dark-green felt trees; along it, in this order from left to right: a mossy felt stone, a fallen felt branch across the path, an old stitched tree stump. Blue dusk with the last orange light between the trunks. Side view, the path in focus.

### great_tree (Leo's tree) (P)
- [x] **L-09 Great tree, wide, dusk (P)**
  File: `character/locations/great_tree/great_tree_wide_dusk.png` · Refs: L-01 (for the world's look)
  Prompt: A great old felt tree with a wide stitched brown trunk on the right and big exposed roots, a rounded canopy of layered green felt leaves, soft felt grass, a narrow path crossing left to right in front of the trunk, a big root on the left of the path, a few small white felt flowers, open grass in front of the trunk (room for a large lying lion and a small mouse). Blue dusk, warm last light on the canopy, the first tiny stars in the sky.
- [x] **L-12 Great tree, sky, dusk**
  File: `character/locations/great_tree/great_tree_sky_dusk.png` · Refs: L-09
  Prompt: Looking up past the felt canopy of the same tree at the dusk sky, the first small stitched stars appearing. ("Those stars you were worried about are almost here.")
- [ ] **L-13 Great tree, wide, day**
  File: `character/locations/great_tree/great_tree_wide_day.png` · Refs: L-09
  Prompt: Exactly the same view as the reference, but in warm midday light, blue sky with small cotton-wool clouds, no stars.

### milo_home (optional)
- [x] **L-14 Milo's home, night (optional)**
  File: `character/locations/milo_home/milo_home_wide_night.png` · Refs: L-01
  Prompt: A small round felt burrow door among big tree roots, a tiny warm felt lantern glowing beside it, deep blue night, first stars.

### distant_forest (where the net is) (P)
The distant forest has one view only, L-16 (owner, 2026-09-28: the wide view
L-15 was dropped). Leo walking in, the net, Milo's arrival, the gnawing and
Leo free all happen on this plate.
- [x] **L-16 Distant forest, medium, morning (P)**
  File: `character/locations/distant_forest/distant_forest_medium_morning.png` · Refs: L-01 (for the world's look)
  Prompt: A quieter, older part of the felt forest: tall rounded felt trees, green felt ferns on both sides, rounded grey felt rocks with a big grey rock beside the path, a pale felt path in the centre, morning mist of soft white wool between the trunks, soft cool morning light. Room on the path for a large lion lying down and a small mouse beside him.

### forest_run (Milo racing to the roar)
- [x] **L-19 Forest run, side view, morning**
  File: `character/locations/forest_run/forest_run_side_track_morning.png` · Refs: L-16
  Prompt: A felt forest floor seen from the side: big felt roots in the foreground, low leafy felt bushes in the middle, a low felt branch to run under, morning light in soft shafts. A clear run line from right to left across the frame.

## 2. Leo - STUDIO block, refs: LEO canonical

(The walking pose already exists: `Leo/v3/actions/leo_action_walking.png`.)

- [x] **LEO-01 Asleep, paw across the path**
  File: `character/characters/Leo/v3/actions/leo_asleep_paw_forward.png`
  Prompt: Leo lying on his belly in a relaxed three-quarter view, fast asleep, eyes closed, head resting low, one front paw stretched far forward on the floor, the whole body and the long tufted tail visible.
- [x] **LEO-02 Just woken (pair with LEO-01)**
  File: `character/characters/Leo/v3/actions/leo_just_woken.png` · Refs: + LEO-01
  Prompt: The same pose as the reference, but his eyes just opened wide, startled, head raised a little, mouth closed.
- [x] **LEO-03 Barrier paw**
  File: `character/characters/Leo/v3/actions/leo_barrier_paw.png`
  Prompt: Leo risen to a low crouch, head up, surprised and a little annoyed but not scary, mouth closed, one big front paw planted flat and forward on the floor, the other paw back.
- [x] **LEO-04 Looking down, calm**
  File: `character/characters/Leo/v3/actions/leo_looking_down.png`
  Prompt: Leo lying on his belly like a sphinx in a three-quarter view, head tilted down as if looking at something small on the floor in front of his paws, calm and gentle, mouth closed.
- [x] **LEO-05 Sitting, gentle smile**
  File: `character/characters/Leo/v3/actions/leo_sitting_smile.png`
  Prompt: Leo sitting upright on his haunches in a three-quarter view, relaxed, gentle closed-mouth smile, tail curled around his paws.
- [x] **LEO-06 Laughing**
  File: `character/characters/Leo/v3/actions/leo_laughing.png`
  Prompt: Leo lying relaxed, laughing warmly, eyes squeezed happy, head tilted back a little, mouth slightly open with no teeth showing.
- [x] **LEO-E1 Annoyed but controlled (close-up)**
  File: `character/characters/Leo/v3/expressions/leo_expression_annoyed.png` · Refs: + `Leo/v3/expressions/leo_expression_neutral.png`
  Prompt: The same head-and-shoulders framing as the expression reference. Leo mildly annoyed but controlled: brows lowered a little, eyes half-lidded, mouth closed. Never angry or scary.
- [x] **LEO-E2 Doubtful (close-up)**
  File: `character/characters/Leo/v3/expressions/leo_expression_doubtful.png` · Refs: + neutral expression
  Prompt: Same framing. Leo doubtful and gently amused: one brow raised, head tilted slightly, mouth closed ("Your teeth?").
- [x] **LEO-E3 Humbled, grateful (close-up)**
  File: `character/characters/Leo/v3/expressions/leo_expression_grateful.png` · Refs: + neutral expression
  Prompt: Same framing. Leo humbled and deeply grateful: soft eyes, brows raised in the middle, small closed-mouth smile.
- [x] **LEO-E4 Reflective (close-up)**
  File: `character/characters/Leo/v3/expressions/leo_expression_reflective.png` · Refs: + neutral expression
  Prompt: Same framing. Leo thoughtful and quiet: eyes lowered, calm, mouth closed.

## 3. Leo in the net (P) - SCENE block, refs: LEO canonical + L-16

The net: soft braided cream craft rope, large square gaps, chunky round knots.
Leo is always on the ground, never lifted or squeezed; worried at most.

How the trap works (owner, 2026-09-28): the net hangs gathered in the
branches above the path; Leo steps on a small hidden trigger on the path (like
a button) and the net **falls from above** onto him. The video goes N-01 ->
N-01b (Leo's paw on the trigger) -> the net falls -> N-02. The script's line
"A hunter's net sprang upward" should then say that the net dropped from the
branches above (see ASSETS.md).

- [x] **N-01 The trap before it springs (P)**
  File: `character/characters/Leo/v3/net/net_trap_set.png` · Refs: L-16 only
  Prompt: On the reference path: a soft braided cream rope net gathered into a loose bundle and hanging in the tree branches just above the middle of the path, held by a thin rope; on the path below it, a small round felt trigger (like a button) half hidden among a few felt leaves. No animals, no people.
- [x] **N-01b Leo's paw on the trigger (P)**
  File: `character/characters/Leo/v3/net/leo_steps_on_trigger.png` · Refs: + N-01
  Prompt: The same scene as N-01: Leo walking along the path, his front paw pressing down on the small round felt trigger; the net still bundled in the branches above him, just starting to open. Leo looks down at his paw, surprised, mouth closed.
- [x] **N-02 Just caught (P)**
  File: `character/characters/Leo/v3/net/leo_net_caught.png` · Refs: + N-01b
  Prompt: The same place: the net has fallen from the branches and settled over Leo, who is lying on the path under it, his whole body clearly visible through the large gaps, surprised, mouth closed. The empty branch above.
- [x] **N-03 Pulling at the net (P)**
  File: `character/characters/Leo/v3/net/leo_net_pulling.png` · Refs: + N-02
  Prompt: The same scene as N-02, Leo pulling at one rope with a front paw, worried, mouth closed. Calm, not struggling wildly.
- [x] **N-04 Calling out (P)**
  File: `character/characters/Leo/v3/net/leo_net_calling.png` · Refs: + N-02
  Prompt: The same scene, Leo lifting his head and calling out for help, mouth open in a round O, no teeth showing, worried but not scared.
- [x] **N-05 Resting, waiting (P)**
  File: `character/characters/Leo/v3/net/leo_net_resting.png` · Refs: + N-02
  Prompt: The same scene, Leo lying still under the net, tired and worried, looking toward the left of the frame.
- [x] **N-06 Face through the ropes, close-up (P)**
  File: `character/characters/Leo/v3/net/leo_net_face_closeup.png` · Refs: + Leo neutral expression, L-16
  Prompt: A close-up of Leo's face seen through the rope gaps, embarrassed but trying to stay composed, mouth closed, background soft.
- [ ] **N-07 Net loosened (P)**
  File: `character/characters/Leo/v3/net/leo_net_loosened.png` · Refs: + N-05
  Prompt: The same scene as N-05, but several rope strands broken and the net sagging open on the left side; Leo still inside, hopeful.
- [ ] **N-08 Stepping out (P)**
  File: `character/characters/Leo/v3/net/leo_net_stepping_out.png` · Refs: + N-07
  Prompt: The same scene, Leo stepping out through the opening, one front paw forward on the path, the net slipping off his back.
- [ ] **N-09 Free (P)**
  File: `character/characters/Leo/v3/net/leo_free.png` · Refs: + N-08
  Prompt: The same place, Leo standing free on the path next to the fallen net, amazed and happy, looking down at the ground in front of him.

## 4. Milo - STUDIO block, refs: MILO canonical

- [x] **M-01 Nibbling an acorn**
  File: `character/characters/Milo/v3/actions/milo_acorn.png`
  Prompt: Milo sitting on the floor nibbling a small felt acorn held in both paws, content.
- [x] **M-02 Startled, looking up**
  File: `character/characters/Milo/v3/actions/milo_startled_up.png`
  Prompt: Milo standing, looking up at the sky, startled, ears up, eyes wide, mouth a small O.
- [ ] **M-03 Looking left**
  File: `character/characters/Milo/v3/actions/milo_look_left.png`
  Prompt: Milo standing, head and body turned to his left, thinking.
- [ ] **M-04 Looking right**
  File: `character/characters/Milo/v3/actions/milo_look_right.png`
  Prompt: Milo standing, head and body turned to his right, thinking.
- [ ] **M-05 Determined**
  File: `character/characters/Milo/v3/actions/milo_determined.png`
  Prompt: Milo standing tall, determined, paws closed at his chest, small confident smile.
- [ ] **M-06 Running, side view (P)**
  File: `character/characters/Milo/v3/actions/milo_run_side.png`
  Prompt: Milo running fast in side view, facing right, mid-stride with one foot far forward and the other pushing off, arms swinging, ears streaming back, tail out behind. A real run, not a walk.
- [ ] **M-07 Jumping over a stone**
  File: `character/characters/Milo/v3/actions/milo_jump.png`
  Prompt: Milo jumping, side view facing right, mid-air, legs tucked, ears up, joyful.
- [ ] **M-08 Tripping**
  File: `character/characters/Milo/v3/actions/milo_tripping.png`
  Prompt: Milo tripping forward, side view facing right, falling with his paws out in front, surprised ("Whoa!"), not hurt.
- [ ] **M-09 Frozen, scared**
  File: `character/characters/Milo/v3/actions/milo_frozen.png`
  Prompt: Milo standing frozen, looking up, scared but not crying, ears back, paws close to his chest.
- [ ] **M-10 Apologising**
  File: `character/characters/Milo/v3/actions/milo_apologising.png`
  Prompt: Milo looking up, earnest and sorry, paws pressed together in front of his chest.
- [ ] **M-11 Surprised, grateful**
  File: `character/characters/Milo/v3/actions/milo_surprised_grateful.png`
  Prompt: Milo looking up with wide surprised eyes turning grateful, paws open at his sides, a small hopeful smile.
- [ ] **M-12 Hurrying away**
  File: `character/characters/Milo/v3/actions/milo_hurrying.png`
  Prompt: Milo hurrying in side view facing right, a quick careful walk-run, looking back over his shoulder with a smile.
- [ ] **M-13 Listening, ears up**
  File: `character/characters/Milo/v3/actions/milo_listening.png`
  Prompt: Milo standing still, ears lifted high and turned, alert and concerned, listening to a far sound.
- [ ] **M-14 Gnawing a rope (P)**
  File: `character/characters/Milo/v3/actions/milo_gnawing.png`
  Prompt: Milo standing and holding a thick braided cream rope with both paws, the rope between his small rounded felt teeth, busy and determined. (Only the rope, no net.)
- [ ] **M-15 The rope snaps (P)**
  File: `character/characters/Milo/v3/actions/milo_rope_snaps.png` · Refs: + M-14
  Prompt: The same as the reference, but the rope has just parted at his mouth into two frayed loose ends, Milo surprised and proud.
- [ ] **M-16 Laughing**
  File: `character/characters/Milo/v3/actions/milo_laughing.png`
  Prompt: Milo laughing, eyes happy, head tilted back a little, paws at his tummy.
- [ ] **MILO-E1 Startled (close-up)**
  File: `character/characters/Milo/v3/expressions/milo_expression_startled.png` · Refs: + `Milo/v3/expressions/milo_expression_neutral.png`
  Prompt: The same head-and-shoulders framing as the reference. Milo startled: eyes very wide, ears straight up, mouth a small O.
- [ ] **MILO-E2 Apologetic (close-up)**
  File: `character/characters/Milo/v3/expressions/milo_expression_apologetic.png` · Refs: + neutral expression
  Prompt: Same framing. Milo sorry and earnest: brows up in the middle, ears slightly back, mouth closed.
- [ ] **MILO-E3 Calm confidence (close-up)**
  File: `character/characters/Milo/v3/expressions/milo_expression_calm_confident.png` · Refs: + neutral expression
  Prompt: Same framing. Milo calm and confident: steady eyes, small closed-mouth smile.
- [ ] **MILO-E4 Playful, cheeky (close-up)**
  File: `character/characters/Milo/v3/expressions/milo_expression_playful.png` · Refs: + neutral expression
  Prompt: Same framing. Milo playful and cheeky: one eye slightly narrowed, lopsided grin, mouth closed ("I have quite a lot of them").

## 5. Interactions - SCENE block, refs: LEO + MILO canonicals + the plate

- [ ] **I-01 Milo racing toward the sleeping Leo**
  File: `character/characters/interactions/v3/int_milo_runs_to_paw.png` · Refs: + L-09, LEO-01, M-06
  Prompt: On the reference path: Milo running in from the left edge; ahead of him Leo asleep against the trunk, one enormous paw stretched across the path.
- [ ] **I-02 Milo against Leo's nose (P)**
  File: `character/characters/interactions/v3/int_milo_on_nose.png` · Refs: + L-09, LEO-02
  Prompt: A close two-shot: Milo has landed against Leo's big nose, both surprised, Leo's eyes just opened wide, Milo's ears up. Funny, not scary.
- [ ] **I-03 The barrier paw (P)**
  File: `character/characters/interactions/v3/int_barrier_paw.png` · Refs: + L-09, LEO-03, M-09
  Prompt: Leo's big front paw planted on the grass right beside tiny Milo, blocking his way; Milo frozen, looking up; Leo looking down at him, surprised and a little annoyed, mouth closed.
- [ ] **I-04 Kindness under the tree**
  File: `character/characters/interactions/v3/int_kindness.png` · Refs: + L-09, LEO-04, M-10
  Prompt: Leo lying calm, smiling gently down at Milo; Milo standing at his paw, paws together, looking up hopefully.
- [ ] **I-05 Milo arrives at the net (P)**
  File: `character/characters/interactions/v3/int_milo_at_net.png` · Refs: + L-16, N-05
  Prompt: Milo standing at the edge of the rope net on the path, looking up; Leo inside the net looking at him, surprised and embarrassed.
- [ ] **I-06 Milo gnawing, Leo watching (P)**
  File: `character/characters/interactions/v3/int_gnawing.png` · Refs: + L-16, M-14, N-06
  Prompt: A close-up: Milo gnawing a braided rope of the net in the foreground; behind the rope gaps, Leo's face watching hopefully, slightly out of focus.
- [ ] **I-07 Leo free, looking at Milo (P)**
  File: `character/characters/interactions/v3/int_free.png` · Refs: + L-16, N-09
  Prompt: Leo standing free on the path, looking down amazed and grateful at tiny Milo, who smiles up at him; the fallen net lies behind them.
- [ ] **I-08 Both laughing under the tree**
  File: `character/characters/interactions/v3/int_laughing.png` · Refs: + L-13, LEO-06, M-16
  Prompt: Under the great tree in daylight, Leo lying relaxed and Milo sitting beside his paw, both laughing together.

---

When a batch is saved, tell the assistant: it checks each image against the
canonicals (identity, scale 1:3, framing of the pairs), installs them
(`production/install_pack.py`), and builds the shots.
