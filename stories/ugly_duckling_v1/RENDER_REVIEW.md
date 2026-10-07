# Ugly Duckling v1, scenes 1-9: render review (agent, 2026-10-07)

All 42 runtime clips of scenes 1-9, 3 seeds each, fast mode (Wan 2.2 I2V A14B + Lightning, 4 steps,
CFG 1, 81 frames at 16 fps, 1280x720): **126 takes** in
`work/stories/ugly_duckling_v1/shots/<clip>_s<seed>_fast.mp4` (+ `.json` sidecar), rendered
2026-10-06 by `PER_TASK=2 lumi/render_story.sh ugly_duckling_v1`. (The driver process ended with the
session before writing its `done:` line; all 126 takes and sidecars exist.)

Evidence: one contact sheet per scene, every take on a row, frames 0/20/40/60/80:
`work/stories/ugly_duckling_v1/review/sceneNN.jpg`. Contact-sheet review only: **watch the clips at
normal speed** before choosing; gait, wing timing and mouth timing are not visible on a sheet. Mark
chosen takes by renaming with a `best_` prefix, as for Lion and Mouse v5.

## Summary

- Identity holds in every take: Ollie (grey cygnet, later white swan), Mama Duck, the three ducklings,
  Ottie and the swans keep their canonical look; plates stay locked. No duplicated characters seen.
- The hard beats work: the family swims off in `s03_to_the_water` (all 3), the swans cross the sky in
  `s05_swans_fly` (all 3), **Ollie grows in `s07_ollie_grows` (all 3)**, and the swan flies across the
  lake in `s08_flies` (all 3).
- **Recurring fault: some `_closed` close-ups open the beak mid-clip**, so they cannot cover silent
  stretches. Two causes: prompts that say the character speaks (`s01_mama_closeup`, `s02_ollie_sad`,
  `s06_ottie_closeup`) and fast-mode drift where nothing asks for it (`s04_decision`, `s09_ollie_nervous`).
  Use the `_mouth` takes for speech and pick the closed take whose beak stays shut, or trim.
- `_mouth` takes open the beak near the end as designed (the open end frame).

## Per scene ("ok" = nothing wrong on the sheet)

| Scene | Clips | Notes |
|---|---|---|
| 1 | pond, mama_nest, ducklings_hatch, mama_closeup (closed, mouth), big_egg, ollie_hatches | ok, gentle motion. `mama_closeup_closed`: beak opens in a smile mid-clip in s2 and s3 (prompt says "speaks warmly"); s1 is the quietest. |
| 2 | ducklings_stare, ollie_sad (closed, mouth), mama_comforts | ok. `ollie_sad_closed` keeps the beak mostly shut in all three. `mama_comforts`: Mama hugs Ollie in all three. |
| 3 | to_the_water, ollie_glides, honk, ollie_alone (closed, mouth) | ok. `honk`: almost no visible motion on the sheet (the honk is a sound; check that a beak movement reads at speed). `ollie_alone_closed`: eyes close at the end in all three (fine if wanted). |
| 4 | decision (closed, mouth), leaves | **`decision_closed`: all 3 takes throw both wings up with an open beak around frame 60** and settle again; reads as a sudden outburst, not a quiet decision. Use `decision_mouth` or re-render with a stillness prompt. `leaves`: Ollie walks off right in all three, ok. |
| 5 | lake, ollie_lake (closed, mouth), swans_fly, ollie_watches (closed, mouth) | ok. `ollie_watches` starts with the beak slightly open (start frame) in both variants. |
| 6 | winter, ollie_cold, ottie_finds, ottie_approaches, ottie_closeup (closed, mouth), ollie_shy (closed, mouth) | **`winter s2`: a washed-out / hazy frame around frame 40** (exposure flash); use s1 or s3. `ottie_finds`: Ottie is small inside the burrow, motion subtle. `ottie_closeup_closed` opens to a laugh at the end (prompt says "speaks... laughs"). `ollie_shy_closed`: blinks/eyes close briefly, ok. |
| 7 | sliding, ollie_grows | ok; sliding together in all three; growth reads in all three (s1 and s2 clearest). |
| 8 | spring, goodbye, flies | `spring`: white petals drift over the water (fine). **`goodbye s3`: a dark grey blob appears on the snow at frame 60** (artifact); use s1 or s2. The goodbye plate is the fully snowy winter plate, while the prompt says the snow has nearly melted (known, owner review). |
| 9 | swans_lake, ollie_nervous (closed, mouth), ollie_bows | ok. **`ollie_nervous_closed`: beak opens around frame 20 in all three** (no speech in the prompt: fast-mode drift); rely on `ollie_nervous_mouth` or trim. `ollie_bows`: the bow is subtle on the sheet; watch at speed. |

## Suggested re-renders (only if the takes do not work at speed)

- `s04_decision_closed`: prompt that keeps wings folded and beak closed ("Ollie stands still, wings
  folded against his body, beak closed, and looks up with quiet determination").
- `s09_ollie_nervous_closed` and `s01_mama_closeup_closed`: remove "speaks" from the closed variant and
  state the beak stays closed (positive wording; fast mode ignores negatives).

Scenes 10-12 wait for the owner's images.
