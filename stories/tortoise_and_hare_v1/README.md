# The Tortoise and the Hare (tortoise_and_hare_v1)

Second story of *Big Lessons, Little Tales*: Aesop's tortoise and hare for ages 3 to 7, in the felt stop-motion style of the channel, made with the consistency rules learnt on The Lion and the Mouse (`docs/creation-rules.md` CR-01 to CR-18).

Moral: *Keep going, step by step, and you can reach places you never thought you could; and a kind friend cheers for you whether you win or lose.*

## Status (2026-10-04)

- **Documentation done; nothing generated.** Script (61 lines, about 5 minutes), 33 shots, 39 foundation and expression image records and 66 scene frames, every prompt rendered from `visual_bible.json`; `python3 production/image_prompts.py --story tortoise_and_hare_v1 lint` reports 0 errors.
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
| Hattie | the hare, fast and proud, learns not to stop trying | one tall slim caramel-tan felt hare standing upright, very long ears with pink insides and chocolate-brown tips, cream belly, two amber-brown eyes, a rose-brown nose and one small round white tail |
| Toby | the tortoise, slow, calm and kind, wins by keeping going | one small rounded olive-green felt tortoise with a domed shell of honey-tan hexagonal plates, sage-green head and legs, cream chin, two brown eyes, four short legs and a short pointed tail |
| Olive | the owl, wise race starter | one small round tawny-brown felt owl with cream speckles, a buff-cream face disc, two big golden-amber eyes, a small brown beak and two folded wings |
| Pip | the squirrel, excited cheerleader | one small rust-orange felt squirrel with a cream belly, a big bushy curled tail, small rounded ears and two dark-brown eyes |
| Bramble | the hedgehog, cosy spectator | one small round felt hedgehog with soft chestnut-brown cream-tipped spines, a biscuit-beige face and tummy, a black nose and two small brown eyes |

Size lineup: At equal depth, with Hattie's height from feet to ear tips as 1.0: Toby's shell top 0.33 and shell length 0.50; Olive 0.40; Pip 0.33 to the ear tips (tail top 0.50); Bramble 0.25.

## Production order (each step reviewed before the next)

1. Owner approves script and shot order.
2. Canonicals of the five characters (studio, full body); owner approves; identities rewritten from them.
3. Size lineup image (`LINEUP`), then measure it and update the setup sizes.
4. Plates (6), the ribbon prop, views and poses, portraits, mouth and expression studies.
5. Scene frames in story order, each start before its end; the first frame of each camera setup is its size anchor.
6. Voices for Hattie, Toby, Olive, Pip and Bramble (one sample line each, owner picks), then the narration (`voice/narrate_scenes.py --lines stories/tortoise_and_hare_v1/dialogue_coverage.json --story tortoise_and_hare_v1 --voices ...`).
7. Clips on LUMI (fast mode), owner selects takes; assembly only when asked.

## Image folders

- Characters: `character/characters/{Hattie,Toby,Olive,Pip,Bramble}/tortoise_and_hare_v1/{canonical,references,expressions}/`
- Scene frames: `character/characters/interactions/tortoise_and_hare_v1/keyframes/`; size lineup: `character/characters/interactions/tortoise_and_hare_v1/lineup_r01.png`
- Plates and props: `character/locations/tortoise_and_hare_v1/<place>/`, `.../props/`
- Each record's `target` in `prompt_manifest.json` is the exact file name.

## Decisions for the owner

1. Names: Hattie (hare), Toby (tortoise), Olive (owl), Pip (squirrel), Bramble (hedgehog).
2. Cast size: five characters; the start and finish scenes show all five at once, the hardest frames for image models. A smaller crowd (Olive only) would be safer.
3. Ending: Toby wins and invites Hattie to walk together; Hattie apologises for teasing. Classic moral kept ("Slow and steady wins the race") plus the channel's kindness message.
4. Length: about 5 minutes of narration; scene 7 and 11 could take more lines if a longer video is wanted.
5. Narrator voice: reuse one of the saved narrators (`voice/narrators/`) or design a new one.
