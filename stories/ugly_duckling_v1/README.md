# The Ugly Duckling (ugly_duckling_v1)

Fourth story of *Feltwillow*: Hans Christian Andersen's ugly duckling (public domain) for ages 3 to 7, retold gently: the ducklings' teasing is mild and they say sorry, a kind otter shelters Ollie through the winter, and Ollie finds both the swans and his first family again. Felt storybook style of the channel, made with the consistency rules of `docs/creation-rules.md` CR-01 to CR-19.

Moral: *Everyone grows in their own way and in their own time; being different is nothing to be ashamed of, and kindness to someone who feels different can help them find where they belong.*

## Status (2026-10-06)

- Documentation packet is complete: 65 script lines (about 7.7 minutes of narration), 44 shots, 54 foundation and expression image records and 102 scene image records, one superseded (including 13 `<shot>_open` talking key frames, CR-19). Prompts are rendered from `visual_bible.json`; lint reports 0 errors.
- **CR-01 approved:** the owner confirmed reading and approved the script and shot order on 2026-10-05. The first canonical is `SWANS_CANON`.
- **Image status:** all six character canonicals are owner-approved (2026-10-05). Their identity text and palettes were updated from the images in `visual_bible.json`; rendered prompts rebuilt and lint passes with 0 errors and 0 warnings. `LINEUP` was generated with all six canonical identities represented as references and saved at `character/characters/ugly_duckling_v1/interactions/lineup_r01.png` (1920×1080). The saved lineup was reopened and checked for cast count, left-to-right order, shared baseline and relative sizes; the owner approved it on 2026-10-05. The lineup is the full-cast comparison image; the two swan references are paired left/right at `character/characters/ugly_duckling_v1/interactions/.review/lineup_swans_reference_pair.png` to fit the image tool's five-reference limit.
- Measured on the owner-approved LINEUP: adult swans 0.75 and 0.64 of frame height, Ottie 0.41, Mama Duck 0.38, cygnet Ollie 0.22 and duckling 0.14. Cast proportions and every setup size were updated from these measurements. At the owner’s direction, `O_SWIM` and `O_WALK_R` were generated and are awaiting review. The owner then directed generation of all remaining foundation records from `prompts/foundation.md`, continuing at line 121. All 23 records after `O_WALK_R` were generated at their manifest targets: six pose studies, ten mouth studies and seven environment plates. They are marked `accepted_pending_owner_review`. After owner feedback that the pond variants changed the nest and scenery, the corrected morning and day variants were made as direct lighting edits from `pond_evening_r01.png`. The owner replaced the earlier files and renamed the corrected variants `pond_morning_r01.png` and `pond_day_r01.png`; all scene-frame references and bible plate paths now point to those current r01 files. The earlier drift happened because morning was generated without an image reference, then day and evening were independently generated from it; the model reinterpreted the scene despite geometry instructions. Final prompt rebuild and lint report 0 errors and 0 warnings. Review sheets: [character studies](review/foundation_characters_contact_sheet.png) and [environment plates](review/foundation_plates_contact_sheet.png). At the owner’s direction, all 22 expression records in `prompts/expressions.md` were generated from their ordered closed-mouth portrait and canonical identity references, saved to manifest targets, and marked `accepted_pending_owner_review`; [expression contact sheet](review/expressions_contact_sheet.png).
- Character descriptions and palettes now follow the six owner-approved canonical images; further changes require owner review.
- **Scene frames:** at the owner’s direction, Scenes 01–08 have been generated from the rendered prompt records with built-in ImageGen and saved at their manifest targets. For Scene 08, the empty spring start is an exact copy of its locked lake plate to preserve the background pixel-for-pixel; the paired end adds blossoms on the water. The two-character goodbye start/end and the grown-swan flight start/end were generated using their ordered world-state, plate, identity, expression, pose and size references; mouth poses were corrected to stay closed per the shot descriptions. All six Scene 08 frames are pending owner review; see the [Scene 08 contact sheet](review/contact_sheets/scene-08_contact_sheet.png). The goodbye prompt says the snow has nearly melted, but the locked winter plate remains fully snow-covered; resolve that story/plate mismatch during owner review. Scene 06 has 14 active frames awaiting owner review; the superseded `s06_ottie_stays_end` record is retained for provenance. The owner renamed the helping endpoint to `s06_ottie_approaches_end_r01.png` and duplicated the original start as `s06_ottie_finds_end_r01.png`, making the burrow hold an identical start/end pair. The contact sheet is [scene 06](review/contact_sheets/scene-06_contact_sheet.png). Scene 07’s four keyframes have their own [contact sheet](review/contact_sheets/scene-07_contact_sheet.png) and are pending owner review. The prompt manifest was rebuilt and lint passes with 0 errors and 0 warnings.

## Read in this order

1. [SCRIPT.md](SCRIPT.md): the story, line by line, with speakers and performance notes.
2. [SHOT_PLAN.md](SHOT_PLAN.md): every shot with its start and end, the cause-and-effect state table and the camera setups.
3. [prompts/](prompts/): the exact prompt and reference list of every image and video clip.
4. `visual_bible.json`: characters, size lineup, places, camera setups and shared prompt text (the single source).

## Cast

| Character | Who | Design |
|---|---|---|
| the Swans | the swan family: two identical adult swans | a large graceful snow-white felt swan with a long curved neck, a coral-orange beak with a black knob and two kind dark-brown eyes |
| Ollie the swan | Ollie grown up into a white swan (a separate visual state) | one young graceful snow-white felt swan with a long curved neck, a coral-orange beak with a black knob, charcoal-grey feet and two dark-brown eyes |
| Ottie | a kind otter who shelters Ollie through the winter | one cheerful chocolate-brown felt otter with a creamy-beige face and chest, a big dark-brown nose, long whiskers, two dark-brown eyes and a long thick tail |
| Mama Duck | the mother duck, loving and kind | one plump warm-brown felt mother duck with buff-cream speckles, a pale cream chest, an orange-yellow beak and feet, two dark-brown eyes and a teal-blue wing patch |
| Ollie | the 'ugly duckling', a grey cygnet who feels different | one gangly young dove-grey felt cygnet with pale-grey cheeks, a slate-grey beak, big charcoal-grey webbed feet and two dark-brown eyes |
| the Ducklings | Ollie's three yellow duckling siblings; tease a little, later say sorry | a small round fluffy buttercup-yellow felt duckling with a small orange beak and feet and two dark-brown eyes |

Size lineup: At equal depth, with Mama Duck's height as 1.0: each duckling 0.35, Ollie the cygnet 0.55, Ottie upright 1.1, Ollie the swan 1.9 (neck up), each adult swan 2.1.

## Production order (each step reviewed before the next)

1. Owner approves script and shot order.
2. Canonicals of the 6 characters (studio, full body); owner approves; identities rewritten from them.
3. Size lineup image (`LINEUP`), then measure it and update the setup sizes.
4. Plates (7), props, views and poses, portraits, mouth and expression studies.
5. Scene frames in story order, each start before its end; the first frame of each camera setup is its size anchor.
6. Narration (voices chosen by the owner 2026-10-06, in [voices.yaml](voices.yaml): narrator The Cheery Tale Keeper 2, one duckling voice for the three ducklings): `voice/narrate_scenes.py --lines stories/ugly_duckling_v1/dialogue_coverage.json --story ugly_duckling_v1 --voices-file stories/ugly_duckling_v1/voices.yaml`; audio in `work/stories/ugly_duckling_v1/audio/en/`.
7. Clips on LUMI (fast mode), owner selects takes; assembly only when asked.

## Image folders

- Characters: `character/characters/ugly_duckling_v1/{Swans,OllieSwan,Ottie,MamaDuck,Ollie,Ducklings}/{canonical,references,expressions}/`
- Scene frames: `character/characters/ugly_duckling_v1/interactions/keyframes/`; size lineup: `character/characters/ugly_duckling_v1/interactions/lineup_r01.png`
- Plates and props: `character/locations/ugly_duckling_v1/<place>/`, `.../props/`
- Each record's `target` in `prompt_manifest.json` is the exact file name.

## Owner decisions

- 2026-10-04: owner chose The Ugly Duckling as the fourth story; narration 7 to 10 minutes; narrator: the saved narrator voice for now.
- 2026-10-05: owner confirmed reading and approved `SCRIPT.md` and `SHOT_PLAN.md` (CR-01); canonical-image work may begin.
- 2026-10-05: owner directed the agent to create the Ugly Duckling canonical images with built-in ImageGen and asked that Gemini remain an optional provider rather than a dependency. The owner supplied all six canonical records in sequence, then approved all six canonicals on 2026-10-05. The owner also authorized their use as identity references for `LINEUP`, approved the completed lineup on 2026-10-05, and requested `O_SWIM` and then `O_WALK_R`. The owner subsequently directed generation of all remaining foundation images from `prompts/foundation.md`, starting at line 121, and authorized proceeding through completion. The owner selected `pond_evening_r01.png` as the composition master for the pond lighting variants, replaced the earlier morning/day images with the corrected versions, and reset their filenames to r01. The owner then directed continuation through `prompts/expressions.md`; all 22 records were generated with built-in ImageGen from their listed portrait and canonical references and saved at their manifest targets, pending owner review. The owner subsequently directed scene-frame creation in order through `scene-07.md`; Scenes 01–07 are generated and pending owner review, with the Scene 06 contact sheet at `review/contact_sheets/scene-06_contact_sheet.png`. On 2026-10-06 the owner split `s06_ottie_finds` into two shots: Ottie watches from inside the burrow, then approaches Ollie. The owner renamed the helping image as `s06_ottie_approaches_end_r01.png` and copied the original start to `s06_ottie_finds_end_r01.png` for a held first shot; the prior generated hold-end record is marked superseded. The owner then directed Scene 07 creation; its four frames were generated in prompt order and saved to their manifest targets, pending review. The owner next directed Scene 08. Its six keyframes were generated in prompt order and are pending review; the empty spring start is an exact copy of the locked lake plate, the remaining backgrounds follow the listed plates, and the closed-mouth frame instructions were made explicit to match the shot descriptions. The [Scene 08 contact sheet](review/contact_sheets/scene-08_contact_sheet.png) is ready. The goodbye frame describes nearly melted snow while its locked winter plate is fully snow-covered, so that mismatch remains for owner review.

- Documentation update: CR-06 and the consistent-image-prompts skill now require a first approved location plate to become the explicit composition master for later variants; a missing reference is treated as a new scene, not an implicit continuation.

## Still open

- Owner review of the generated foundation, expression, and Scenes 01–08 image sets, including the corrected pond morning/day r01 plates, `O_SWIM`, `O_WALK_R`, and all contact sheets. The seven environment plates are complete. Confirm the applicable OpenAI account and service terms for monetised use before using the output downstream; see `docs/licensing.md`.
- The review sheets were built with the system image framework because Pillow is unavailable in the active Python environment.
- 44 shots give about 3.7 minutes of picture at 5 s each; the narration is longer, so shots will be slowed, held or given extra coverage when the narration is timed (`production/timing_sheet.py`).
- Names (Ollie, Mama Duck, Ottie) are proposals.
- Ollie has two canonicals: the grey cygnet (scenes 1-7) and the white swan (scenes 8-12); the change happens off-screen over the winter.
- The reflection shot (s10_reflection) asks an image model for a mirror image in water; check that the reflection matches the swan exactly.
