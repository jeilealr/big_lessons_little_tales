# The Boy Who Cried Wolf (boy_who_cried_wolf_v1)

Third story of *Big Lessons, Little Tales*: Aesop's boy who cried wolf for ages 3 to 7, with a gentle ending (the wolf is silly rather than scary and runs away from a bell; no animal is hurt; the lost sheep are found and Finn learns to rebuild trust). Felt storybook style of the channel, made with the consistency rules of `docs/creation-rules.md` CR-01 to CR-18.

Moral: *Always tell the truth, about big things and little things, so that people can believe you when it matters most; and when you make a mistake, saying sorry and telling the truth is the first step back.*

## Status (2026-10-04)

- **Documentation done; nothing generated.** Script (78 lines, about 8.5 minutes of narration), 46 shots, 62 foundation and expression image records and 92 scene frames, every prompt rendered from `visual_bible.json`; `python3 production/image_prompts.py --story boy_who_cried_wolf_v1 lint` reports 0 errors.
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
| Farmer Ben | the farmer, big and fair; warns Finn | one tall broad felt farmer with a chestnut-brown beard, a straw-yellow hat, two dark-brown eyes, denim-blue overalls over a cream shirt and dark-brown boots |
| Grandma Rosie | Finn's grandmother, the village baker; wise and kind | one round elderly felt grandmother with a silver-white bun, rosy cheeks, two kind brown eyes, a long lavender-purple dress and a cream apron |
| Lena | Finn's friend, about nine | one young felt girl with two long dark-brown braids tied with sunflower-yellow ribbons, two dark-brown eyes, a sky-blue dress with a white collar and red shoes |
| Finn | the shepherd boy, about eight; plays tricks, learns honesty | one young felt boy with curly copper-orange hair, rosy cheeks and freckles, two hazel-green eyes, a moss-green tunic, a short red scarf, brown trousers and dark-brown boots |
| the Wolf | a lanky, silly, hungry wolf; never hurts anyone | one long lanky smoke-grey felt wolf with a pale-grey muzzle and chest, tall pointed ears, two golden-yellow eyes, a big black nose and a big bushy tail, more silly than scary |
| the Sheep | the flock: five identical ewes | a round fluffy cream-white felt sheep with a biscuit-beige face and legs, small ears with rosy-pink insides and two dark-brown eyes |
| Daisy | Finn's favourite lamb, with a white heart on her forehead | one small fluffy cream-white felt lamb with a charcoal-black face and legs, a white heart-shaped patch on her forehead, rosy-pink ear insides and two amber-brown eyes |

Size lineup: At equal depth, with Finn's height as 1.0: Ben 1.5 (1.6 with hat), Rosie 1.33, Lena 1.05, Wolf 0.75 (to ear tips, on four legs), each sheep 0.55, Daisy 0.35.

## Production order (each step reviewed before the next)

1. Owner approves script and shot order.
2. Canonicals of the 7 characters (studio, full body); owner approves; identities rewritten from them.
3. Size lineup image (`LINEUP`), then measure it and update the setup sizes.
4. Plates (9), props, views and poses, portraits, mouth and expression studies.
5. Scene frames in story order, each start before its end; the first frame of each camera setup is its size anchor.
6. Narration with the saved narrator (`voice/narrators/moonlight_storyteller_1`, the default) and character voices chosen later: `voice/narrate_scenes.py --lines stories/boy_who_cried_wolf_v1/dialogue_coverage.json --story boy_who_cried_wolf_v1 --voices SPEAKER=folder ...`.
7. Clips on LUMI (fast mode), owner selects takes; assembly only when asked.

## Image folders

- Characters: `character/characters/{Ben,Rosie,Lena,Finn,Wolf,Sheep,Daisy}/boy_who_cried_wolf_v1/{canonical,references,expressions}/`
- Scene frames: `character/characters/interactions/boy_who_cried_wolf_v1/keyframes/`; size lineup: `character/characters/interactions/boy_who_cried_wolf_v1/lineup_r01.png`
- Plates and props: `character/locations/boy_who_cried_wolf_v1/<place>/`, `.../props/`
- Each record's `target` in `prompt_manifest.json` is the exact file name.

## Owner decisions

- 2026-10-04: narration 7 to 10 minutes; narrator: reuse the saved narrator voice for now (`voice/narrators/moonlight_storyteller_1`); character voices are decided later.
- Gentle ending as asked: the Wolf is silly, never touches a sheep, and runs from the bell; the sheep are found; Finn apologises and rebuilds trust.

## Still open

- Owner review of the script and shot order (CR-01) before the first image.
- 46 shots give about 3.8 minutes of picture at 5 s each; the narration is longer, so shots will be slowed, held or given extra coverage when the narration is timed (`production/timing_sheet.py`).
- Cast style (assumption, owner to confirm): Finn and the villagers are felt-doll humans, as the title needs a boy; an all-animal cast (for example a young goat as shepherd) is possible.
- Names (Finn, Grandma Rosie, Farmer Ben, Lena, Daisy) are proposals.
- Frames with the whole flock (five sheep and Daisy) and up to four people are the hardest for image models; count sheep on every review.
