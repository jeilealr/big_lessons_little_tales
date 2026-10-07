# The Lion and the Mouse, v5

The current Lion and the Mouse. The owner made the v5 stills (ChatGPT Pro) from the v4 prompt records;
v2 to v4 were deleted on 2026-10-06 and remain in git history (`git show b880c23:stories/lion_and_mouse_v4/...`).

Status (2026-10-06): narration done (English, 11:23.7); 63 shots rendered in fast mode, 3 seeds each;
the owner selects takes. Review: [RENDER_REVIEW.md](RENDER_REVIEW.md).

| File | What it is |
|---|---|
| `SCRIPT_REVIEW.md` | the owner's script, line by line |
| `dialogue_coverage.json` | the line list (narration input and line-to-shot mapping) |
| `SHOT_PLAN.md` | shot order |
| `visual_bible.json` | identities, camera setups, size anchors, plates |
| `prompt_manifest.json` | every image and video prompt record (paths rewritten from v4 to v5) |
| `prompts/*.md` | readable prompts, rendered from the bible |
| `TIMING_SHEET.md`, `timing_plan.json` | which shot covers which narration line |
| `story.yaml`, `runtime_inputs.json` | the runtime story for `production/shot.py`, exported by `production/export_runtime.py` with frozen keyframe hashes |
| `RENDER_REVIEW.md` | review of the rendered clips |

Images: `character/characters/lion_and_mouse_v5/` and `character/locations/lion_and_mouse_v5/`
(same file names and revisions as v4). Generated audio and clips (not in git):
`work/stories/lion_and_mouse_v5/`.

Re-export the runtime story (after an image change):

```bash
python3 production/export_runtime.py --manifest stories/lion_and_mouse_v5/prompt_manifest.json \
    --story lion_and_mouse_v5 --images lion_and_mouse_v5
```

Known lint state: `python3 production/image_prompts.py --story lion_and_mouse_v5 lint` reports 70
errors for v3 reference images named by the expression records (deleted history; only needed to
regenerate those expressions) and 8 warnings for images the owner renamed in v5.
