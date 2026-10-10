# The Lion and the Mouse v6

This is an independent r02 image and render production. Its character canonicals, expression and pose references, location plates, scene keyframes, narration files and video takes belong to v6. Do not import an older version's assets or rebuild this packet with `production/chain_packet.py`.

The current shot order has 154 pieces across 16 scenes. The saved timing plan covers 11:23.7, but the narration WAV and `timing.json` are absent from this checkout. Stage the v6 narration under `work/stories/lion_and_mouse_v6/audio/en/` and verify the timing on LUMI before rendering. Every piece is a new v6 render.

## Current image state

- 54 r02 foundation assets are accepted and hash-bound: 20 character images, 22 expression studies, 10 location plates and 2 props.
- 42 single-character blurred-background scene candidates remain under `character/characters/lion_and_mouse_v6/interactions/keyframes/.review/`. They are candidates, not approved keyframes.
- 71 scene records are planned with no candidate PNG. Of these, 69 show characters against sharp backgrounds. Eleven setup anchors require generation and approval before their dependent frames.
- No scene frame has been accepted into the main keyframes directory. No v6 video take has been selected.

The current rules and measurements are in `visual_bible.json`. `prompt_manifest.json` is the active image and shot list; `prompts/*.md` are generated reading copies. Use `LUMI_HANDOFF.md` for the exact generation and review sequence.

## Checks from the repository root

```bash
python3 production/image_prompts.py --story lion_and_mouse_v6 build --check
python3 production/image_prompts.py --story lion_and_mouse_v6 lint
python3 production/image_handoff.py --story lion_and_mouse_v6 audit
python3 production/image_handoff.py --story lion_and_mouse_v6 check s01_milo_at_edge
```

The `check` command blocks generation when a reference or required setup anchor is unapproved, missing or changed. Prompt lint verifies the written specification; it does not judge the saved picture. Review anatomy, scale, ground support and plate geometry visually before approving any keyframe.
