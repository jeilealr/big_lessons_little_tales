# Creation rules: scripts, images and shots

The one guide to read before writing a script, generating an image or
describing a video shot for *Big Lessons, Little Tales*. Every rule here was
learned on this project (v1, v2 and v3 of The Lion and the Mouse); the
evidence for the video rules is in [prompting.md](prompting.md) (rule numbers
in brackets), the problems and fixes in
[findings-and-risks.md](findings-and-risks.md).

Order of work: **script -> DNA -> images -> keyframes -> shots -> animatic ->
narration and edit.**

---

## 1. Writing the script

1. **Narration first, pictures fitted to it.** The spoken text sets each
   scene's length; shots are planned to fill it (about one 5-second shot per
   10-12 spoken words).
2. **Length.** ~1,160 spoken words = 8-10 minutes = ~90-110 shots. Decide the
   target length before writing; every extra minute is ~12 shots to make.
3. **One beat per shot.** Write the story so each moment is one clear action
   (Milo trips; Leo wakes; the net falls), not several at once.
4. **Dialogue = close-ups.** The characters' stitched mouths do not lip-sync,
   so each spoken line becomes a close-up of the speaker (a small gesture or
   expression change) and a reaction of the listener. Keep lines short.
5. **Write what the pictures can show.** Fast contact between characters
   (tumbles, rolls, catching) and complex physical actions cannot be animated
   reliably: show them as a cut between two stills (before and after) and let
   the narration carry the motion ("a tumble, a roll").
6. **Peril is brief, mild and resolved kindly** (YouTube's "animals in
   distress" example, findings B6). No hanging, squeezing, pain or teeth; a
   roar is a call for help. The villain's device is simple and visible (the
   net drops from the branches when Leo steps on a trigger).
7. **Time of day tells the story** (afternoon -> sunset -> dusk -> morning):
   each lighting state needs its own location plate, so decide them in the
   script.
8. **Name the places.** Every scene happens in a named location with its own
   DNA (section 3). Keep the number of places small and reuse them.
9. **The moral in the characters' words** at the end, repeated once by the
   narrator.
10. Script format: one line per spoken sentence, each tagged with its speaker
    and a delivery note (`LION — calm, slightly amused`); one file per
    language, same scenes and line order (`stories/<slug>/narration/<lang>.yaml`).

## 2. Character images

**Authority:** the canonical image of each character is the identity; its
DNA text (`character/characters/<Name>/<version>/dna.yaml`) describes that
image, never the reverse (prompting 1.4). Settle any mismatch once (Leo's eye
colour, Milo's hair tuft).

1. **One character per image, plain warm off-white studio**, soft even light,
   small ground shadow: the pipeline cuts the character out (BiRefNet) and
   places it on the plates. Never draw scenery behind a single-character
   reference.
2. **Always attach the canonical** as the image reference, and change only
   the pose or expression the prompt asks for.
3. **Full body means everything in frame**: paws, whole tail, ear tips, the
   whole mane. A cropped paw or tail cannot be restored in a shot (v3
   LEO-03 lost its "barrier paw").
4. **One pose per image, the pose the story needs.** The video model keeps
   the start pose's gait: a walking still gives a walk, not a run (v2 Scene 8);
   a real run needs a running still (mid-stride, ears back).
5. **Expressions: identical head-and-shoulders framing** for the whole set,
   so any two can be a shot's start and end without a jump or zoom.
6. **Pairs are made from each other.** When two images are a shot's start and
   end (asleep -> just woken; gnawing -> rope snaps), make the second with the
   first attached as the reference and change only the action.
7. **Every new state of a character gets an owner-made image.** In v2 every
   shot where the model had to invent Leo in a new state (inside the net,
   tugging, stepping free) went off-model; in v3 every such state is an image.
8. **A pose change and a face change are two images, not one** (the eyes of a
   lion lying down would not close in the same step).
9. **Side views face one direction**; the pipeline mirrors them for the other.
10. **Positive wording** ("mouth closed", "soft, floppy rope"), never "no
    teeth" or "not scary": a negation names the thing. Put unwanted things in
    the negative prompt (prompting 3.5).
11. **Check every image against the canonical** (face, colours, proportions,
    the one distinctive feature: Leo's mane colour, Milo's ears and hair tuft)
    before it is used. Batches made from a different reference drift (v3: the
    net set's mane came out redder).

## 3. Location images (plates)

**Authority:** the location DNA (`stories/<slug>/locations_dna.yaml`): what the
place is, what must never change, its lighting states, its plates.

1. **Empty plates**: no characters, animals or props unless the entry says so.
2. **The scene fills the frame edge to edge**; no studio table, backdrop or
   border (prompting 3.2). 16:9.
3. **One normal-height view per place** (owner, 2026-09-28): low "mouse-eye"
   angles were not stable, and normal views show the Leo-Milo size
   difference well. Close-ups are made by the pipeline (a crop of the plate
   with a blurred background).
4. **One plate per lighting state** (afternoon, sunset, dusk, night,
   morning), made with the place's first plate as the reference and changing
   only the light. The video model must never change time of day in a shot.
5. **Leave the stage area open, flat and in focus**, where characters stand
   or travel; put the feet there, never over blurred foreground objects
   (production-guide section 4).
6. **Landmarks never change**: list them in `never_change` (the trunk on the
   right, the path in front) and keep them in every plate of that place.
7. **A cutaway** (the sky with the first stars) is a separate plate used on
   its own; characters are never placed on it.
8. **Different places look different**: a character's home must not look like
   another character's landmark (v3: Milo's burrow first sat in a tree like
   Leo's).
9. When a set of character images already defines a place (the v3 net
   scenes), that place **is** the location; do not mix it with a different
   plate of "the same" place.

## 4. Interaction images (two characters)

1. **Made in the location**, with both canonicals and the plate attached, when
   the characters touch or interact closely (on the nose, the barrier paw,
   gnawing the net). Cut-out compositing cannot fake contact.
2. **Scale: Milo is one third of Leo's standing height**, in every image.
3. **Pairs again**: an interaction that is a shot's end frame is made with its
   start frame as the reference (runs to the paw -> on the nose -> barrier paw).
4. Check both characters against their canonicals; interactions drift more
   than single images (v2 review frames 08/09).

## 5. Video shots (the description of a shot)

The full rules with evidence: [prompting.md](prompting.md). In short:

1. **Start AND end on owner-made images** where possible (the best v2 and v3
   shots). The model only animates between them.
2. **One whole-body action per shot**, described big (2.1). Small gestures
   from a still are lost.
3. **The action names only the characters' bodies** (2.2); anything else it
   names may be animated instead.
4. **Locomotion: an energetic verb, side-on geometry, a fixed camera, room
   ahead, and the run leaves the frame** (2.3, 2.10).
5. **At most one camera move**, and it goes to the biggest subject (2.8,
   2.12); a move that reveals what the image does not show makes the model
   invent it (2.8b).
6. **Say what must not change, and negate its opposite** (2.7): "stays fast
   asleep the whole time" + negative "open eyes, awake".
7. **Close-ups: `background:` instead of the location sheet** (2.13); the full
   sheet names landmarks the model then tries to show.
8. **A continuation from a cropped frame needs an end keyframe** (2.14); an
   end identical to the start freezes the action, so the end must show the
   result.
9. **Characters not in the shot go in the negative** (2.9).
10. Fast mode (4 steps) for iterating, 3 seeds per shot; pick the best.

## 6. Checklist before generating

**Image**
- [ ] The canonical (and the plate, for scenes) is attached.
- [ ] The prompt changes only the pose, expression or light it is for.
- [ ] Full body in frame (studio images); stage area open (plates).
- [ ] Positive wording; unwanted things in the negative.
- [ ] Pairs: the start image attached when making the end image.
- [ ] Saved under the name and folder of the to-do list, no `_01` suffix
      (extra takes `_02`, `_03`).

**Shot**
- [ ] Start (and end) keyframe composed and looked at.
- [ ] One action, only bodies named, direction matches the image.
- [ ] Camera fixed or one move; nothing revealed that the image lacks.
- [ ] What must not change is stated and negated.
- [ ] `--dry-run` read.

## 7. Style blocks (copy into image prompts)

**STUDIO** (single character):
> Handcrafted wool-felt stop-motion storybook miniature, softly stuffed matte
> felt, tactile fuzzy wool fibres, delicate visible stitching, charming
> handmade irregularities. Warm off-white seamless studio floor and backdrop,
> soft even studio light, small soft ground shadow. The whole character in
> frame (ears, paws, tail), one character only. Keep the exact identity of the
> reference: same face, colours, proportions, materials. No text, no logo, no
> watermark, no clothing.

**LOCATION** (plate):
> Handcrafted wool-felt stop-motion storybook miniature set, matte felt
> surfaces, visible delicate stitching, rounded soft shapes, warm children's
> storybook palette, miniature diorama photography, shallow depth of field.
> 16:9, the scene fills the frame edge to edge, no studio table or backdrop.
> Empty: no animals, no characters, no text.

**SCENE** (characters in a place):
> Handcrafted wool-felt stop-motion storybook miniature, 16:9. Keep both
> characters exactly like their reference images (face, colours,
> proportions, materials). Milo (the mouse) is one third of Leo's (the lion's)
> standing height. Keep the location exactly like its reference plate. No
> text, no logo, no watermark.

## 8. Files and names

| What | Where |
|---|---|
| Character pack (canonical, views, expressions, actions, story states) | `character/characters/<Name>/<version>/<folder>/<name>.png` |
| Interactions | `character/characters/interactions/<version>/<name>.png` |
| Location plates | `character/locations/<place>/<place>_<angle>_<light>.png` |
| Character DNA | `character/characters/<Name>/<version>/dna.yaml` |
| Location DNA | `stories/<slug>/locations_dna.yaml` |
| A story's image to-do list | `stories/<slug>/TODO_images.md` |

No `_01` suffix on file names; a second take of the same image is `_02`.
