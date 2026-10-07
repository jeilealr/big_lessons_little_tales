# Prompt for an agent: start producing The Ugly Duckling (ugly_duckling_v1)

Written 2026-10-04. Work on LUMI in `/scratch/project_465002727/jelealro/big_lessons_little_tales`,
always from the repo root.

## Read first

1. `CLAUDE.md` (all of it: current state, standing instructions, "Mistakes already made").
2. `docs/creation-rules.md` CR-01 to CR-18, and `.claude/skills/consistent-image-prompts/SKILL.md`.
3. This story's packet: `README.md`, `SCRIPT.md`, `SHOT_PLAN.md`, `prompts/`, `visual_bible.json`,
   `prompt_manifest.json`, `dialogue_coverage.json`.
4. How the Lion and the Mouse was done end to end: `stories/lion_and_mouse_v5/README.md`,
   `docs/gemini-images.md`, `voice/README.md`, `docs/v4-preflight.md` (gates A to E).

## Rules for this task

- **Gate first (CR-01):** confirm with the owner that the script and shot order are approved
  before any image. Record their decision under "Owner decisions" in `README.md`.
- **Images:** the owner makes the images by default. Make images yourself
  (`character/gemini_image.py`, see `docs/gemini-images.md`) only if the owner asks for it in
  that session. Either way, every image goes to its record's `target` in `prompt_manifest.json`,
  under `character/characters/ugly_duckling_v1/<Name>/`, `.../ugly_duckling_v1/interactions/` or
  `character/locations/ugly_duckling_v1/<place>/`. Never put this story's images in another
  story's folder, and never use Lion and Mouse images as references.
- Edit prompts only through `visual_bible.json` and the record templates, then
  `python3 production/image_prompts.py --story ugly_duckling_v1 build` and `lint` (0 errors).
- No GPU jobs, audio or git unless the owner asks. Temp files: `/scratch/project_465002727/jelealro/tmp`.

## Order of work (each step reviewed by the owner before the next)

1. **Canonicals** of the 6 characters (studio, full body; Ollie has two: cygnet and swan).
   Review each one at full size. After approval, rewrite each identity in the bible from
   the image (sample the colours from it) and rebuild the prompts.
2. **Size lineup** (`LINEUP`): measure it and update the setup sizes in the bible.
3. **Plates (7) and props**, then views, poses, portraits, and mouth and expression studies.
4. **Scene frames in story order**, each start before its end. The first frame of each
   camera setup is its size anchor. Check every frame against its canonical, the lineup,
   the previous shot and the plate (CR-13, CR-16, CR-17); make contact sheets as evidence.
5. **Voices and narration**, when asked:
   - Design and save a voice for each speaking character with `voice/save_voice.py`
     (one sample line each); the narrator is `voice/narrators/moonlight_storyteller_1`.
   - Then run `voice/narrate_scenes.py --lines stories/ugly_duckling_v1/dialogue_coverage.json --story ugly_duckling_v1 --voices SPEAKER=folder ...`.
   - The Gemini TTS limit is 100 requests a day, resetting at 09:00 Germany time;
     65 lines fit in one day.
   - Then run `production/timing_sheet.py --story ugly_duckling_v1`.
6. **Clips**, when asked, exactly as Lion and Mouse v5 was done:
   - `python3 production/export_runtime.py --manifest stories/ugly_duckling_v1/prompt_manifest.json --images ugly_duckling_v1 --story ugly_duckling_v1`
     (it expects README tables in the image folders, as in `character/characters/lion_and_mouse_v5/*/README.md`;
     generate them first, or extend the exporter to read the manifest `target`s).
   - Then a token check, a `--dry-run` of every shot, and
     `setsid nohup bash lumi/render_story.sh ugly_duckling_v1 > $BLLT_PROJECT/tmp/render_ugly_duckling.log 2>&1 &`.
   - The owner selects the takes. Assembly only when asked.

## Report

At each step, tell the owner:
- what was made and checked, and where the contact sheets are;
- what is open;
- what the owner needs to decide.

Keep `README.md` (Status, Owner decisions, Still open) and the "Current state" section of
`CLAUDE.md` up to date.
