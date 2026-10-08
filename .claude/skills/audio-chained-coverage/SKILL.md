---
name: audio-chained-coverage
description: Use when planning, changing or checking the shot list of a story whose video must last as long as its narration, i.e. any story with `"chained_coverage": true` in its visual_bible.json (Lion and Mouse v6 onward) or when making a new version of a story from its rendered narration; when adding landscape/establishing pieces, cuts or dissolves; before exporting or rendering a chained story; and when testing how the clips join (chain_preview). Covers CR-21: the narration is the timeline, every piece is one 49-81 frame clip, each piece starts on the image the previous one ended on unless a checked cut is planned.
---

# Audio-driven chained coverage (CR-21)

The narration is the timeline. A story is a row of **pieces**; each piece is one Wan clip of 49 to
81 frames, covers the narration lines it lists, and starts on the exact image record the previous
piece ended on. That shared still is the hand-off, so clips join without a jump, and the film lasts
exactly as long as the audio. Rules and reasons: `docs/creation-rules.md` CR-21. Every change to the
rules, tools or packets goes into `docs/changelog.md` (what, why, files, how it was checked).

This skill plans pieces. Every image and prompt still follows the repo skill
`consistent-image-prompts` (identity, sizes, plates, review gate): read it before writing any image
record or accepting an image.

## Tools

| Step | Command (from the repo root) |
|---|---|
| How many pieces each line needs | `python3 production/chain_plan.py --story <slug> --audio-story <audio slug> suggest` |
| Build the packet from its source | `python3 production/chain_packet.py stories/<slug>/chain_source.py` |
| Render prompts, check them | `python3 production/image_prompts.py --story <slug> build`, then `lint` (0 errors), then `md` |
| Time the pieces, set frame counts, timing sheet | `python3 production/chain_plan.py --story <slug> --audio-story <audio slug> apply` |
| Join test without clips (CPU) | `lumi/run_in_container.sh python production/chain_preview.py --story <slug> --stills [--until S]` |
| Runtime story for the GPU | `python3 production/export_runtime.py --manifest stories/<slug>/prompt_manifest.json --story <slug> [--scenes ...]` |
| Join test with chosen takes | `lumi/run_in_container.sh python production/chain_preview.py --story <slug> --until S` |

`chain_preview.py` and `animatic.py` assemble pictures: run them when the owner asks for a preview or
join test, never automatically after a render (CR-01).

## Planning a story's pieces

1. **Start from the rendered narration** (`work/stories/<audio slug>/audio/<lang>/timing.json`). Run
   `suggest`: every line's span (the line plus the pause after it; the last line also owns the 1 s
   scene tail) and how many pieces it needs alone. A piece covers **2.45 to 6.33 s** (49 to 81
   frames at 16 fps, retimed 0.80 to 1.25).
2. **Write `chain_source.py`** (copy `stories/lion_and_mouse_v6/chain_source.py`): `BASE` (the story
   whose bible and images are reused), `NEW_IMAGES`, `PIECES` in film order. Each piece: id
   (`sNN_<name>`), scene, setup, start and end image ids, `lines`, one action sentence, mode
   (`closed`, `mouth`, `ambient`), and either `join="chain"` (default) or a cut.
3. **Fit the lines.** Consecutive pieces may share a line (its span is split evenly). If a piece
   comes out too short, give it a neighbouring line; too long (a line over 6.33 s), split the line
   over two pieces. Prefer to change the plan, not the bounds.
4. **One action per piece**, reachable from the start image to the end image. Long narration with
   nothing happening gets a **hold** (start = end: breathing, blinking, ears, tail tip) or a
   **landscape** (mode `ambient`, no cast, start = end = the plate `PL_<loc>`, or an empty scene
   frame when a prop must show). Avoid long runs of holds on one image; alternate with a close-up,
   a landscape or a small action.
5. **Entrances and exits.** A character never pops in on a fixed camera: chain an entrance piece
   from the empty plate to a frame with the character just inside the edge, and an exit piece to the
   empty plate.
6. **Cuts** (`join="cut"`, `cut=<reason>`, optional `transition`): `close_up` (into or out of a
   close-up or close two-shot), `camera_change` (another setup at the same place), `time_change`
   (same place, another light: use `crossfade`), `location_change`, `dissolve` (time passes on the
   same camera; needs `crossfade` or `dip`; the only cut allowed within one setup). The first piece is
   `film_start`. Lint checks that each reason is true; any other same-setup cut is a jump cut.
7. **Talking chains.** A run of dialogue pieces in a close-up alternates the closed frame and its
   `_open` frame (CR-19): closed → open, open → closed. The `mouth` sentence is chosen from the
   endpoints (ends open / starts open / both closed). One open frame per expression that speaks.
8. **Reuse.** If a piece's endpoints are exactly an earlier variant's and its length fits 81 frames
   at 0.80 to 1.25 speed (4.05 to 6.33 s), set `reuse="<variant id>"`: its prompt is copied verbatim
   and it is not re-rendered. Do not reuse takes the render review rejected.
9. **Video prompts describe only what is in frame** (fast mode, CFG 1: a named absent object is drawn
   in; v5 scene 15). Never write "stays outside", "stays empty" or name paws in a portrait.
10. Build, `lint` 0 errors, `md`, `apply`. Read `SHOT_PLAN.md` and `TIMING_SHEET.md` as the owner will.
    Log the change in `docs/changelog.md`.

## New images in a chain

- A frame that first appears as the **end** of a piece is an edit of that piece's start
  (`edit_base` first, `edit_chain_frame` wording, the locked plate next). Lint enforces it for the
  story's own new images.
- A **boundary image** serves two clips: review it against the earlier piece's start and the later
  piece's end (the pose must be reachable by one small action from both), plus the usual gate
  (canonical, size anchor, plate) of `consistent-image-prompts` D.
- New images are named `sNN_KK_<name>_r01.png`, `KK` = first use in the scene (lint checks it);
  reused images keep their names.
- An empty view that must keep a prop where a scene frame has it (the net in the branches) uses the
  role `empty_copy` on that frame, not `edit_base`.

## Before rendering

- `export_runtime.py` skips reused pieces and refuses while any endpoint image is missing; use
  `--scenes` for a pilot of scenes whose images exist.
- Run `chain_preview.py --stills` first: pacing, cuts and the chain against the narration, minutes on
  a CPU.
- Render a **pilot of the first scenes**, let the owner choose takes (`takes.yaml`: `piece: seed` or
  a file, or the `best_` prefix), then run `chain_preview.py --until <end of pilot>`. A flagged join
  (jump/motion > 3) or a pace far from 1 is repaired by re-rendering the later piece with
  `continue_from` the chosen take's last frame, or by fixing the boundary image. Only then render
  the rest (`lumi/render_story.sh`).
