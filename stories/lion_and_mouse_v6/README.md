# The Lion and the Mouse, v6 (chained coverage)

The v5 story and narration, re-planned so the pictures last exactly as long as the audio (owner, 2026-10-08):
154 pieces of 2.45 to 6.33 s cover all 11:23.7 of the v5 English narration, and each piece starts on the
image the previous one ended on, unless a planned cut is marked (a face close-up, another place or time, a dissolve).
Rules: `docs/creation-rules.md` CR-21; workflow: `.claude/skills/audio-chained-coverage/SKILL.md`; every change:
`docs/changelog.md`.

## Status (2026-10-08)

- **No v6 images or videos have been generated.** 154 pieces: 25 reuse a v5 render (same endpoints, prompt and 81 frames),
  129 need new renders; 81 are holds or landscapes (start = end: breathing, blinking, ambient motion).
- **33 new images** are needed (bold in `SHOT_PLAN.md`): 16 approved open-mouth calibration images for close-up character dialogue, 3 entrances onto empty plates, the empty trap path with the net, and 13 new story beats. Every clip boundary stays on an approved closed mouth; open-mouth images calibrate timed dialogue only. Narrator-only audio never animates a character's mouth (CR-24). Everything else reuses v5 images through local copies under the v6 character folders; v5 stays intact. Accepted expression studies are listed in `prompts/expressions.md`.
- **Current packet is an interim baseline.** It carries localized v5 assets and 25 reused v5 renders. The owner selected full v6 image regeneration as a later phase; migrate this packet to all-new v6 image records before generating them. The owner instructed that no images be created until the audit, code and documentation are complete and reported. The v5 English narration remains the timing source.
- **Narration alignment ready:** `work/stories/lion_and_mouse_v5/audio/en/word_timings.json` contains word timings for all 161 lines (1,238 words); all lines are marked `aligned`, with no review flags.
- The 37 dialogue close-ups use closed start/end frames plus one separate approved open-mouth anchor each. Silent pauses and narrator-only coverage hold mouths closed.
- V5 source-still regeneration is not certified by the v6 lint: the v5 prompt lint currently reports 70 errors and 8 warnings from missing deleted v3 references.
- Prompts: `python3 production/image_prompts.py --story lion_and_mouse_v6 lint` must report 0 errors.
  Every accepted new image needs a hash-bound approval before runtime export.

## Read in this order

1. `SHOT_PLAN.md`: every piece, its join (chain or the reason for the cut), its images and lines; the new images.
2. `TIMING_SHEET.md`: when each piece plays, its length, frame count and speed (from `chain_plan.py`).
3. `prompts/scene-NN.md`: the exact prompt and ordered references of every new image and every clip.
4. `chain_source.py`: the source of the plan. Before generating images, edit this and rebuild. After an image has
   production/review state, rebuilding preserves it only when the image specification is unchanged; changed records
   require explicit `--invalidate <image-id>` and preserve the old record under `superseded`.

## Rebuild after a change to `chain_source.py`

```bash
python3 production/chain_packet.py stories/lion_and_mouse_v6/chain_source.py
python3 production/image_prompts.py --story lion_and_mouse_v6 build
python3 production/image_prompts.py --story lion_and_mouse_v6 lint
python3 production/image_prompts.py --story lion_and_mouse_v6 md
python3 production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v5 apply
```

## Next steps (each needs the owner)

1. Owner reviews `SHOT_PLAN.md` (the sequence, the holds and landscapes, the cuts).
2. Generate the 33 new images in film order; review each against both pieces it joins. Approve the exact
   target and SHA-256 with `python3 production/image_prompts.py --story lion_and_mouse_v6 approve <image-id> --reviewed-by <name>`.
3. Join test before any GPU time: `production/chain_preview.py --story lion_and_mouse_v6 --stills` (CPU).
4. Export and render scenes 1 to 3, choose takes, then run `chain_preview.py --until 104 --require-takes`.
   Repair a flagged join with `production/chain_repair.py --story lion_and_mouse_v6 --piece <later> --previous-piece <earlier>`,
   render its separate candidate, choose it in `takes.yaml`, and rerun the strict join test. Only then render the rest.
5. Align the existing v5 narration after confirming the dialogue transcript: `bash voice/setup_lipsync_env.sh`, then `.venv-lipsync/bin/python production/lip_sync.py align --story lion_and_mouse_v6 --audio-story lion_and_mouse_v5 --lang en --device cpu`. Review every line marked `review` in `work/stories/lion_and_mouse_v5/audio/en/word_timings.json`.
6. After selecting video takes, run `.venv-lipsync/bin/python production/lip_sync.py apply --story lion_and_mouse_v6`; review mouth motion, pauses and joins. See `docs/lip-sync.md` for the limits of this word-timed approximation.
7. Once every piece has a chosen and, where dialogue is present, lip-synced take, create the DaVinci handoff with `production/edit_manifest.py --story lion_and_mouse_v6`.

## Known risks carried from v5

- Scene 5: Leo's pose differs between the wide frames (one paw stretched across the path) and the two-shot at his nose
  (head on crossed paws); v6 cuts between them (`close_up`) instead of the v5 bridge, which zoomed.
- Scene 8: v5 `s08_milo_surprised` takes show Milo closing his eyes and clasping his paws; v6 does not reuse them.
- Scene 15: the v5 close-up clips drew branches, leaves and paws (prompts named absent things); v6 renders them anew
  with prompts that describe only what is in frame.
