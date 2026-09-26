# Prompt: Audit and complete Lion and Mouse v2 visual references

Use this prompt when continuing the Leo and Milo v2 design work. The goal is to inspect the existing image assets and written DNA, resolve inconsistencies, fill only genuine reference gaps, and prepare a clean handoff to story-video production.

## Repository and authority

Repository: `/scratch/project_465002727/jelealro/twc_video`

Inspect these folders completely:

- `character/characters/Leo/v2/`
- `character/characters/Milo/v2/`

Read each folder's `dna.yaml`, every `README.txt`, and all images in its canonical, views, expressions, actions, and explorations folders. Also read:

- `character/characters/character_pack_prompts_v2.md`
- `CLAUDE.md`
- `docs/character-consistency.md`
- `stories/lion_and_mouse/story.yaml`
- `work/stories/lion_and_mouse_v2_review/README.txt` (if present)
- Existing location sheets and plates under `work/stories/lion_and_mouse/design/`

The v2 canonical neutral images are the highest-priority character identity anchors:

- Leo: `character/characters/Leo/v2/canonical/full-body_leo_neutral_pose_01.png`
- Milo: `character/characters/Milo/v2/canonical/full-body_milo_neutral_pose_01.png`

Use the actual image pixels, not just filenames or their descriptions, to review consistency. Compare the written DNA and every candidate image to the appropriate canonical. The canonical image is the visual authority; text should be corrected to describe it when there is a mismatch. Do not silently change the canonical.

## Phase 1 — inventory and visual audit

1. Make a checklist of all files found. Open and visually inspect each image. If an image cannot be opened or passed to the image review/generation tool, report that limitation and stop short of claiming it was inspected.
2. Assess every non-canonical image for identity stability: silhouette, proportions, face and eye design, mane or ears, palette, material/stitching, tail, pose readability, crop, and image quality. Classify each as **keep**, **uncertain**, or **reject**, with a short reason. Pay special attention to whether the expression/action changes only the requested feature while preserving identity.
3. Compare each `dna.yaml` against the actual canonical image. List inaccuracies, omitted identity anchors, over-specific details unsupported by the canonical, contradictions, and useful details to preserve. Recommend a corrected DNA before editing it.
4. Check pack completeness for this story, not an abstract exhaustive pack. The pack should support the required camera angles, expressions, and actions in the Lion and Mouse fable. Identify which images are genuinely missing, unusable, duplicated, mislabeled, or unnecessarily redundant. Flag filename issues such as accidental `.png.png`, but do not rename or delete assets without first checking references and preserving the original.
5. Inspect the current v2 story-image review frames and note which are usable only as story-layout references versus which, if any, are safe as character references. In particular, honor every explicit rejection in the review README. Never use a rejected or uncertain story frame to define Leo or Milo.

Present the inventory and findings before generating anything. Do not treat a filename as proof that an image is good.

## Phase 2 — fill only approved gaps with review drafts

If images are genuinely needed, create only the minimum useful set to resolve the gaps:

- Generate a missing character reference only when it will materially help maintain identity or support an important story action.
- Use the correct character's canonical image as a direct visual reference for every character generation. For a two-character image, reference both canonical images. A text description alone is not an adequate substitute when direct references can be supplied.
- Preserve the canonical silhouette, colors, face, age impression, materials, and Leo-to-Milo scale relationship. Vary only the requested view, expression, or action.
- For locations, first write a concise location DNA for each recurring set (at minimum the clearing and trap site if both remain in the v2 story). Define stable landmarks, layout, palette, felt materials, time of day, light direction, and open staging areas. Compare the v1 location plate to the desired v2 style; do not assume it is an exact v2 plate.
- If exact composition continuity is needed and no suitable plate exists, create one **empty v2 background plate per recurring location**, with no characters, props, text, or studio edges. Use each plate directly as the image reference for images in that location. Do not independently invent a new background for every shot.
- Avoid incidental changes to set landmarks, weather, season, time, or light direction between images in one scene. Story-motivated changes must be recorded explicitly.

Save every newly generated image immediately, including a clear filename, under:

`work/stories/lion_and_mouse_v2_review/`

Use dedicated subfolders such as `characters/Leo/`, `characters/Milo/`, and `backgrounds/<location>/` if that keeps the review set clear. Never overwrite an existing image. Keep the generator's original output intact and record the source path, prompt, and reference image paths in a sidecar or manifest when possible. Update the review README with each new draft's purpose and status. These are review drafts; do not place them in canonical folders yet.

If the image tool cannot access the canonical reference files, do not generate more text-only guesses. Report exactly which reference attachment or access is needed to proceed.

## Phase 3 — reconcile documentation

After the visual audit, update the relevant `dna.yaml` only if the image evidence supports the change. Preserve version history or note the change in the README; never rewrite DNA from memory alone. Update character-pack prompts if they contain stale filenames or contradict the approved canonicals. Record location DNA and plate paths in the appropriate story documentation, keeping v1 and v2 distinct. Summarize what changed and what still needs owner review.

Do not promote an image to canonical, modify the v1 story bible for v2, delete rejected drafts, or commit/push anything without explicit owner approval. Work files under `work/` are git-ignored temporary scratch: remind the owner to back up approved assets before scratch cleanup or expiry.

## Phase 4 — hand off to video production

Only after the owner approves the v2 character references, location plates, and DNA:

1. Confirm the v2 story beats and shot list against the owner's current Lion and Mouse retelling. Do not assume the older v1 shots still match.
2. Keep v2 video work isolated in `work/stories/lion_and_mouse_v2/` (or another clearly named v2 work directory), preserving the existing v1 outputs.
3. Reuse the approved character references and location plates when building keyframes; use the existing repo pipeline and practices in `CLAUDE.md`, `docs/production-guide.md`, and `docs/prompting.md`.
4. For every shot, inspect the keyframe and a contact sheet of the rendered clip for identity, staging, background continuity, and frame defects before calling it usable.
5. Do not submit GPU jobs until the usual dry-run, input checks, and smoke-test requirements are met.

## Expected report

Return:

- file inventory and visual review results;
- DNA corrections proposed or made, with the image evidence behind them;
- the minimum missing images needed and why;
- background DNA / plate requirements and consistency risks;
- paths to any new review drafts and their prompt/reference metadata;
- what the owner needs to approve;
- a clear handoff plan for resuming the v2 video workflow under `work/`.

## Lessons from video production (added 2026-09-27; see docs/prompting.md)

These come from rendering the v1 story with Wan 2.2 on LUMI. They change what a
*useful* reference image is, not how the character looks.

**What the video pipeline does with these images.** Each character image is
cut out (BiRefNet matting) and placed into an empty location plate to make a
shot's first frame (and, when useful, its last frame); Wan 2.2 then animates
between them. So:

1. **Keep the plain warm off-white studio for every pack image.** It is what
   makes the cut-out clean. Never add scenery to a character reference.
2. **Full body means everything in frame**: feet/paws, whole tail, ear tips,
   the full mane. A cropped tail or ear cannot be restored in a shot.
3. **One pose per image, the pose the story needs.** Poses that exist only as
   story frames cannot be reused. This story needs, as full-body studio
   stills: Leo lying on his belly asleep (eyes closed); Leo lying on his belly
   awake, head up, front paws forward; Milo with paws pressed together
   (thank you); Milo worried, paws to his chest; Milo running (mid-stride).
   The first four are being generated from the canonicals with Wan
   (`stories/lion_and_mouse_v2/packs/`); if your image tool can make them with
   the canonical as a direct reference, those are preferred, and should be
   saved into `actions/` with the same naming.
4. **Expressions: keep the identical head-and-shoulders crop** for all of them
   (as now). They are used as start/end frames of close-ups (neutral -> smile),
   and any change of crop or head size between two expressions becomes a zoom
   or a jump in the video. `leo_expression_confident_01.png` has a different
   crop and a browner, softer mane than the rest: regenerate it or do not use it.
5. **Side views face one direction only**; the pipeline mirrors them for the
   other direction. Check asymmetric details (Milo's hair tuft, Leo's mane
   parting) survive a mirror.
6. **Two characters touching are composed, never drawn together.** Generate
   each character alone; the keyframe tool places them at the fixed scale
   (Milo standing = one third of Leo standing, story.yaml `scale:`).
7. **Positive words only in prompts** ("mouth closed", not "no teeth"): text
   encoders read a negation as a mention. Put unwanted things in the negative.
8. **Rounded paws**: `milo_action_pointing_01.png` shows a pointing finger,
   which the DNA excludes. Regenerate if the pointing pose is needed.
9. **Locations**: an empty plate per recurring location, filling the frame
   edge to edge, with the stage area open and in focus. v2 plates are being
   designed with Wan from the location sheets in
   `stories/lion_and_mouse_v2/story.yaml`; review frames stay as layout guides.
