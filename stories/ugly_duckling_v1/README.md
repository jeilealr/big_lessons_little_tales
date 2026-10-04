# The Ugly Duckling (ugly_duckling_v1)

Fourth story of *Big Lessons, Little Tales*: Hans Christian Andersen's ugly duckling (public domain) for ages 3 to 7, retold gently: the ducklings' teasing is mild and they say sorry, a kind otter shelters Ollie through the winter, and Ollie finds both the swans and his first family again. Felt storybook style of the channel, made with the consistency rules of `docs/creation-rules.md` CR-01 to CR-18.

Moral: *Everyone grows in their own way and in their own time; being different is nothing to be ashamed of, and kindness to someone who feels different can help them find where they belong.*

## Status (2026-10-04)

- **Documentation done; nothing generated.** Script (65 lines, about 7.7 minutes of narration), 43 shots, 54 foundation and expression image records and 86 scene frames, every prompt rendered from `visual_bible.json`; `python3 production/image_prompts.py --story ugly_duckling_v1 lint` reports 0 errors.
- **Gate before images (CR-01):** the owner reviews the script and the shot order.
- Character descriptions are design specifications until each canonical image is approved; then they are rewritten from the image (colours sampled from it) and the prompts rebuilt.

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
6. Narration with the saved narrator (`voice/narrators/moonlight_storyteller_1`, the default) and character voices chosen later: `voice/narrate_scenes.py --lines stories/ugly_duckling_v1/dialogue_coverage.json --story ugly_duckling_v1 --voices SPEAKER=folder ...`.
7. Clips on LUMI (fast mode), owner selects takes; assembly only when asked.

## Image folders

- Characters: `character/characters/ugly_duckling_v1/{Swans,OllieSwan,Ottie,MamaDuck,Ollie,Ducklings}/{canonical,references,expressions}/`
- Scene frames: `character/characters/ugly_duckling_v1/interactions/keyframes/`; size lineup: `character/characters/ugly_duckling_v1/interactions/lineup_r01.png`
- Plates and props: `character/locations/ugly_duckling_v1/<place>/`, `.../props/`
- Each record's `target` in `prompt_manifest.json` is the exact file name.

## Owner decisions

- 2026-10-04: owner chose The Ugly Duckling as the fourth story; narration 7 to 10 minutes; narrator: the saved narrator voice for now.

## Still open

- Owner review of the script and shot order (CR-01) before the first image.
- 43 shots give about 3.6 minutes of picture at 5 s each; the narration is longer, so shots will be slowed, held or given extra coverage when the narration is timed (`production/timing_sheet.py`).
- Names (Ollie, Mama Duck, Ottie) are proposals.
- Ollie has two canonicals: the grey cygnet (scenes 1-7) and the white swan (scenes 8-12); the change happens off-screen over the winter.
- The reflection shot (s10_reflection) asks an image model for a mirror image in water; check that the reflection matches the swan exactly.
