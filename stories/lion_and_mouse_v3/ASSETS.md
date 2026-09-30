# The Lion and the Mouse v3: images to create

**Historical v3 production document.** The owner has reviewed the v3 renders.
Use the [v4 packet](../lion_and_mouse_v4/README.md) for the next iteration.
This file preserves the requests used to plan v3; checkboxes mean a file was
saved, not that it passed the later render review. Short prompts and shared
blocks here are not a complete log of actual image-tool submissions. V4 identity,
state and mouth rules supersede these prompts for new production.

Draft 2026-09-27 for the owner. **The to-do list to work from, with file names
and prompts, is `TODO_images.md`** (its IDs are the authoritative ones). Script: `script_dialog_en.txt` (the Gemini
dialog version). Location DNA: `locations_dna.yaml`. v2 evidence:
`../lion_and_mouse_v2/owner_review.yaml`.

## Thoughts on the new script

**What is better than v2**
- It is a real story with cause and effect: Milo is late, takes the shortcut,
  trips over the paw. The accident is Milo's fault in a relatable, childlike
  way, and the lion's kindness has something to forgive.
- The dialogue gives both characters personality (the lion's dry humour, the
  mouse's "I have quite a lot of teeth"), and the ending states the moral
  through the characters instead of only the narrator.
- The theme is consistent and strong: kindness is passed on, not repaid.

**What changes for production**
- **Length: ~1,160 spoken words = about 8-10 minutes** (v2 was 1:46). That is
  roughly 90-110 shots of 5 s. With fast mode (~9 min per seed) it is
  feasible, but every image in the list below is reused many times, so their
  quality decides the film.
- **Time of day now tells the story**: afternoon -> sunset -> dusk and first
  stars -> (days later) morning. The video model must never change the time
  of day inside a shot: each lighting state is its own set of plates
  (`locations_dna.yaml`).
- **Dialogue-heavy (52 character lines)**: the characters have stitched
  mouths and do not lip-sync, so each line is a close-up of the speaker with
  a small head/ear/eye gesture, plus the listener's reaction. That is exactly
  the kind of shot that worked best in v2 (start and end from the expression
  set). The expression set needs a few more emotions (below).
- **The accident beat is the hardest shot**: "tumble, roll, land against the
  lion's enormous nose" is fast contact between the two characters; v1/v2
  showed contact and fast motion fail. Build it from stills: Milo tripping
  (start) -> Milo against the nose (end), a cut, a 2-3 s shot, and let the
  narration carry "a tumble, a roll".
- **The trap (owner, 2026-09-28): the net falls from the branches when Leo
  steps on a hidden trigger.** The script says "the ground suddenly shifted
  beneath him. A hunter's net sprang upward": change it to match, e.g.
  "he stepped on something hidden in the leaves, and a hunter's net dropped
  from the branches above."
- **"A hunter's net sprang upward" and "the ropes only tightened"**: a lion
  lifted and squeezed in a net is closer to YouTube's "animals in distress"
  example (docs/findings-and-risks.md B6). Suggestion: keep the words but
  show the net closing around Leo on the ground, Leo pulling calmly with a
  worried face, never hanging or squeezed; roar = calling out, mouth in an O.
- Small wording points (for the narration script, not the images): "the
  mouse ... themself" in the directions; the story calls him "the mouse"
  throughout (never Milo): fine for the fable style. "The lion rose with a
  deep growl": keep the growl in the sound design gentle.

## Why these images (what v1 and v2 proved)

| Evidence | Consequence for v3 |
|---|---|
| Every shot where the model had to draw Leo in a new state (net, tugging, stepping free) went off-model (all rejected) | owner-made images of **every new state** of each character |
| The best shots start AND end on owner-made images (close-ups from the expression set) | each shot = a **start image and an end image**; make them as pairs with the same framing |
| Backgrounds changed whenever a shot saw more than the plate | shots stay inside the plate (fixed camera, push-ins, close-ups cropped from it); a plate per lighting |
| Low mouse-eye plates were not stable (owner, 2026-09-28); v2 normal views showed the size difference well | **one normal-height view per place**, shared by Leo and Milo |
| Same start and end image = no motion (s04_milo_trembles) | a pair must differ in exactly the action of the shot |

## How to generate (applies to every image)

1. **Single characters: plain warm off-white studio**, full body unless it
   says close-up, the character's canonical as the image reference (as in
   the v2 pack). The pipeline cuts them out and places them on the plates.
2. **Two-character contact images: in the location**, with both canonicals
   and the location's canonical plate as references, Milo at one third of
   Leo's height. These become keyframes directly (cut-outs cannot fake
   contact). Check both characters against their canonicals before using
   them (v2 review frames 08/09 drifted).
3. **Pairs**: when a line says "start / end", make the end image with the
   start image as the reference and change only what the line says.
4. Close-ups: the same head-and-shoulders framing as the existing expression
   set (so they pair with it).
5. Save as `character/characters/<Leo|Milo>/v3/<folder>/<name>.png`,
   interactions in `character/characters/interactions/v3/<name>.png`,
   locations as in `locations_dna.yaml`. No text, logos, watermarks.

## Locations (see locations_dna.yaml for the DNA)

One normal-height view per place (owner, 2026-09-28), plus a plate per lighting:

| Location | Plates |
|---|---|
| stream_bank | wide/afternoon (done), wide/sunset (done) |
| fork | wide/sunset (done) |
| shortcut | side view/dusk |
| great_tree | wide/dusk, sky/dusk, wide/day |
| milo_home (optional) | wide/night |
| distant_forest | medium/morning (the only view) |
| forest_run | side view/morning |

10 plates (9 without Milo's home).

## Leo: new images (studio, canonical as reference)

| ID | Image | Used in |
|---|---|---|
| LEO-01 | asleep, 3/4 view, lying on his side-belly, **one front paw stretched far forward** (across where the path will be), eyes closed | B9 accident setup |
| LEO-02 | same pose, eyes just opened, startled, head slightly raised (pair with LEO-01) | B10 |
| LEO-03 | rising to a crouch, head up, surprised-annoyed, mouth closed, one front paw planted forward flat (the "barrier" paw) | B11 |
| LEO-04 | lying/crouched, looking **down** (3/4, head tilted down), calm | dialogue B12-B16 |
| LEO-05 | sitting upright, 3/4, relaxed, gentle smile | ending B35-37 |
| LEO-06 | walking, side view (exists: pack walking) - check only | B19 |
| LEO-07 | laughing, eyes squeezed happy, mouth open a little, no teeth | B37 |
| LEO-E1..E4 | close-up expressions (same framing as the set): **annoyed but controlled**, **doubtful** ("Your teeth?"), **humbled/grateful**, **reflective (eyes lowered)** | dialogue |

## Leo in the net (the states that failed in v2; the most important images)

Make the net as in `v2` (soft braided cream rope, large square gaps, round
knots), on the **distant_forest medium plate** as reference (so net and
ground are consistent), Leo lying on the ground, never lifted:

| ID | Image | Used in |
|---|---|---|
| NET-01 | the trap set: the net bundled in the branches above the path, a small hidden trigger (button) on the path | B20 |
| NET-01b | Leo's paw pressing the trigger, the net starting to open above him | B20 |
| NET-02 | Leo just caught: the net over him, his body clearly visible through the gaps, surprised | B21 |
| NET-03 | Leo pulling at the net with one front paw, worried, mouth closed (mild) | B22 |
| NET-04 | Leo calling out (roar as a call: mouth open in an O, no teeth, head up) | B23 |
| NET-05 | Leo resting in the net, tired and worried, looking toward the camera-left (where Milo arrives) | B28-31 |
| NET-06 | close-up: Leo's face through the rope gaps, embarrassed-composed | "Little one? ... too strong" |
| NET-07 | the net loosened: several strands broken, sagging open at one side, Leo still inside | B33 end |
| NET-08 | Leo stepping out through the opening, one paw forward, the net slipping off his back | B34 |
| NET-09 | Leo standing free next to the fallen net, amazed, looking down (for the two-shot with Milo) | B34 end |

## Milo: new images (studio, canonical as reference)

| ID | Image | Used in |
|---|---|---|
| MILO-01 | sitting in the grass nibbling an acorn held in both paws, content | B2 |
| MILO-02 | standing, looking up at the sky, startled ("Oh! It's getting late!") | B3 |
| MILO-03 | looking left / MILO-04 looking right (the two paths), thinking | B5 |
| MILO-05 | determined, fists/paws at chest, "Definitely the shortcut" | B6 |
| MILO-06 | **running, side view, mid-stride** (a real run: both feet off the ground or one far forward, ears streaming back) - the pack only has a walk, and a walk start gives a walk | B7, B8, B26 |
| MILO-07 | jumping over a stone (mid-air, side view) | B8 |
| MILO-08 | tripping: falling forward, paws out, surprised ("Whoa!") | B9 |
| MILO-09 | frozen, scared but not crying, ears back, looking up | B11 |
| MILO-10 | apologising, paws together, looking up, earnest | B13 |
| MILO-11 | surprised-grateful, "You're... letting me go?" | B15 |
| MILO-12 | hurrying away, side view, careful (a walk-run), looking back once | B17 |
| MILO-13 | ears lifted, listening, alert (he hears the roar) | B25 |
| MILO-14 | **gnawing**: standing at a thick rope, holding it with both paws, the rope between his teeth (no sharp teeth: small rounded felt teeth) | B32 |
| MILO-15 | gnawing, the rope strand parting at his mouth (pair with MILO-14) | B33 |
| MILO-16 | laughing, eyes happy | B37 |
| MILO-E1..E4 | close-up expressions (same framing as the set): **startled**, **apologetic**, **calm confidence**, **playful/cheeky** ("quite a lot of them") | dialogue |

## Interactions (two characters, in the location, both canonicals as references)

| ID | Image | Location / plate | Used in |
|---|---|---|---|
| INT-01 | Milo mid-run at the edge of frame, Leo asleep with the paw across the path ahead | great_tree / wide dusk | B9 start |
| INT-02 | Milo landed against Leo's big nose, both surprised, Leo's eyes just opened | great_tree / wide dusk | B10 end |
| INT-03 | Leo's big paw planted on the grass right beside Milo (the barrier), Milo frozen, Leo looking down | great_tree / wide dusk | B11, dialogue |
| INT-04 | Leo lying calm, smiling down; Milo standing at his paw looking up, paws together | great_tree / wide dusk | B15-17 |
| INT-05 | Milo arriving at the net, Leo inside looking at him | distant_forest / medium | B29-31 |
| INT-06 | Milo gnawing the rope, Leo's face behind the net watching | distant_forest / medium | B32-33 |
| INT-07 | Leo free, looking down at Milo; the fallen net behind | distant_forest / medium | B34-36 |
| INT-08 | both laughing under the great tree | great_tree / wide/day | B37-38 |

## Beats (script -> shots -> images)

| Beat | Script | Shots (start -> end) |
|---|---|---|
| B1 | "Once upon a time... a little mouse who loved exploring" | stream_bank wide/afternoon + Milo walking (pack) |
| B2 | berries, seeds, the acorn | wide/afternoon: MILO-01 (small nibble motion) |
| B3 | golden light fading; "Oh! It's getting late!" | wide/sunset: MILO-01 -> MILO-02; close-up MILO-E1 |
| B4-6 | two ways home; "The shortcut. Definitely." | fork wide/sunset; MILO-03 -> MILO-04; MILO-05 |
| B7-8 | past a stone, under a branch, around a stump | shortcut side view: MILO-06 (fixed camera, runs across); MILO-07 at the stone |
| B9 | the sleeping lion, paw across the path; "Whoa!" | great_tree wide/dusk: LEO-01; INT-01 -> MILO-08 |
| B10 | tumble onto the nose; eyes open; "What in the forest was THAT?" | INT-02 (short); LEO-E close-up surprised |
| B11 | rises with a growl, paw comes down, mouse freezes | LEO-02 -> LEO-03; INT-03; MILO-09 |
| B12-14 | "finest nap..." / "I'm sorry!..." | close-ups: Leo LEO-E1 (annoyed), Milo MILO-E2 (apologetic), reactions |
| B15-16 | the lion softens; "Go home, little one"; "letting me go?"; "Thank you" | Leo expression neutral -> smile; MILO-11; INT-04 |
| B17 | "Now hurry... stars"; mouse hurries home, carefully | great_tree sky/dusk; MILO-12 on shortcut plate |
| B18 | (home at night, optional) | milo_home |
| B19 | days pass; the lion walks a distant part of the forest | distant_forest medium/morning: LEO-06 walking |
| B20-22 | the trap: Leo steps on the trigger, the net falls from the branches; he pulls | NET-01; LEO-06 walk -> NET-01b; NET-01b -> NET-02 (the fall); NET-03 |
| B23-24 | "Why won't this break?"; the roar | NET-06 close-up; NET-04 |
| B25-27 | two little ears lift; "The lion!"; the run | forest_run: MILO-13; side_track: MILO-06 |
| B28-31 | reaches the clearing; "You should stay back"; "not too strong for my teeth"; "Your teeth?"; "quite a lot of them" | INT-05; close-ups NET-06, MILO-E3, LEO-E2, MILO-E4 |
| B32-33 | nibble, gnaw, pull; strands snap; the net loosens | distant_forest medium (cropped close-up): MILO-14 -> MILO-15 (INT-06); NET-05 -> NET-07 |
| B34 | steps free; "You did it." | NET-07 -> NET-08 -> NET-09; INT-07 |
| B35-36 | the kindness dialogue | close-ups Leo LEO-E3/E4, Milo; INT-07 |
| B37 | "rather large ideas" / "very useful teeth"; they laugh | LEO-07, MILO-16; INT-08 |
| B38 | the moral | great_tree wide/day, slow push-in, INT-08 |

## Counts

10 location plates, Leo 6 + 4 expressions (the walk exists), Leo-in-net 9,
Milo 16 + 4 expressions, 8 interactions: **58 images**. Priority if time is short:
the net set (NET-02..09), MILO-06 (run) and MILO-14/15 (gnaw), INT-02/03/06/07,
and the great_tree and distant_forest plates: these are the shots v2 could not
make.
