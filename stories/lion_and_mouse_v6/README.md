# The Lion and the Mouse, v6 (chained coverage)

The v5 story and narration, re-planned so the pictures last exactly as long as the audio (owner, 2026-10-08):
154 pieces of 2.45 to 6.33 s cover all 11:23.7 of the v5 English narration, and each piece starts on the
image the previous one ended on, unless a planned cut is marked (a face close-up, another place or time, a dissolve).
Rules: `docs/creation-rules.md` CR-21; workflow: `.claude/skills/audio-chained-coverage/SKILL.md`; every change:
`docs/changelog.md`.

## Status (2026-10-08)

- **Plan only: nothing generated.** 154 pieces: 25 reuse a v5 render (same endpoints, prompt and 81 frames),
  129 need new renders; 48 are holds or landscapes (start = end: breathing, blinking, ambient motion).
- **33 new images** are needed (bold in `SHOT_PLAN.md`): open-mouth key frames for the talking chains (CR-19),
  entrances onto empty plates, the empty trap path with the net, and a few new beats (Leo's sleeping face, Leo
  sitting and bowing, the friends resting). Everything else reuses the v5 images, which keep their files.
- **Defaults the agent took (owner to confirm):** reuse the v5 English narration (no new TTS) and the v5 images.
- Prompts: `python3 production/image_prompts.py --story lion_and_mouse_v6 lint` must report 0 errors.

## Read in this order

1. `SHOT_PLAN.md`: every piece, its join (chain or the reason for the cut), its images and lines; the new images.
2. `TIMING_SHEET.md`: when each piece plays, its length, frame count and speed (from `chain_plan.py`).
3. `prompts/scene-NN.md`: the exact prompt and ordered references of every new image and every clip.
4. `chain_source.py`: the source of the plan (edit this, then rebuild; see its docstring).

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
2. The 33 new images, made in film order; each reviewed against both pieces it joins (CR-21 item 8).
3. Join test before any GPU time: `production/chain_preview.py --story lion_and_mouse_v6 --stills` (CPU).
4. Pilot: render scenes 1 to 3, owner chooses takes, then `chain_preview.py --until 104` measures every join of
   the start of the film; repair flagged joins (`continue_from`) before rendering the rest.

## Known risks carried from v5

- Scene 5: Leo's pose differs between the wide frames (one paw stretched across the path) and the two-shot at his nose
  (head on crossed paws); v6 cuts between them (`close_up`) instead of the v5 bridge, which zoomed.
- Scene 8: v5 `s08_milo_surprised` takes show Milo closing his eyes and clasping his paws; v6 does not reuse them.
- Scene 15: the v5 close-up clips drew branches, leaves and paws (prompts named absent things); v6 renders them anew
  with prompts that describe only what is in frame.
