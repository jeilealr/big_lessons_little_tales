# Lion and Mouse v6: LUMI image handoff

## Source of truth and scope

Use only the v6 `visual_bible.json`, `prompt_manifest.json`, r02 character and location assets, and v6 narration. The packet is independent. `production/chain_packet.py` is an older inheritance builder and deliberately refuses to overwrite this bible. Do not copy an older image, render, pose, plate or audio path into v6. The saved timing plan is a planning value until its v6-local audio is present and checked.

Current state: 54 approved foundation assets; 42 blurred single-character portrait candidates for owner review; 71 planned scene frames without candidate PNG; 154 new v6 clips. The 11 sharp setup anchors listed by `image_handoff.py audit` are still unapproved. The review folder contains only the 42 portraits. `work/review/v6_regenerated_contact_sheets/` contains portrait-only sheets for scenes 03, 05, 06, 07, 08, 11, 13 and 15.

## Moving this work to LUMI

The code, packet, approvals and r02 foundation PNGs are currently local repository changes. Commit or otherwise transfer those changes before using a LUMI checkout; a pull of the previous commit will not contain them. Git ignores every `.review/` directory, including the 42 portrait candidates, and ignores `work/review/` contact sheets. If these are needed for review on LUMI, copy those two directories separately into the matching paths on LUMI. Do not treat an absent review candidate as an approved keyframe or regenerate it from a different character root. Stage the v6 narration under the v6 audio path described below; it is also absent from this local checkout.

## First LUMI checks

From the repo root, use the available Python environment (the `feltwillow` Conda environment on the Mac or the LUMI container):

```bash
python production/image_prompts.py --story lion_and_mouse_v6 build --check
python production/image_prompts.py --story lion_and_mouse_v6 lint
python production/image_handoff.py --story lion_and_mouse_v6 audit
python production/image_handoff.py --story lion_and_mouse_v6 check s01_milo_at_edge
```

A clean prompt lint is necessary but does not approve an image. The handoff audit verifies accepted files, prompt hashes, reference hashes and an acyclic generation order. `check <id>` confirms the exact references and locked plate are ready for generation. Generate a setup's `anchor_record` first, review and approve it, then generate other sharp frames in dependency order. The first available sharp anchor is `s01_milo_at_edge`; it uses approved v6 foundation assets. At the tree and trap, earlier single-character frames are listed in the setup's `bootstrap_records`: review them against their numeric size targets first, then approve the two-character anchor before generating the later paired frames.

## Character size, position and plate

The owner-set wide and two-character Milo target is **0.21 of frame height** from ear tips to planted feet; head plus ears is about **0.10**. When Milo and Leo are at the same depth, Milo's standing height is about **0.55 of Leo's mane height**, and his head is about **0.42 of Leo's face height**. Those are anatomical lineup checks, not a reason to make characters the same screen size at different depths. The exact setup targets, including Leo's mane/face and Milo's seated silhouette, are under `setups.<id>.numeric_size_targets` in the bible. Portraits use their own close-up crop.

Keep Leo's and Milo's head, mane and body dimensions stable within a setup and between start/end frames unless the shot explicitly changes camera or depth. Record each actor's depth plane. For a composite, use the approved v6 pose still and the exact locked v6 plate. `production/keyframe.py` accepts `--char still.png:x=…,y=…,h=…`: `x,y` are the support point as fractions of the frame, and `h` is the cut-out silhouette height as a fraction of frame height. Repeat `--char` for both actors. The script applies a soft contact shadow and brightness harmonization. Inspect the matte for missing whiskers, ears, tail, or background fringe before keeping the output.

The planted foot or paw must touch the setup's `walkable_surface` on the same depth plane: a grass lane, dirt path or other actual support in the plate. Water, flowers and bush canopies are not ground. Sitting, lying, jumping, climbing and touching a prop also require believable physical support, shadow and occlusion. For trapped Leo, the net wraps his body, connects at every rope end, and leaves his face readable; it must not look like a loose screen between Leo and the camera.

## Candidate, review and approval

Keep one active candidate PNG per image record in `interactions/keyframes/.review/`; keep its generation prompt, exact attached reference paths/hashes and measurements in the manifest result. Never use a candidate as a later reference. Compare the saved PNG against the canonical, pose, plate, setup anchor and adjacent chain frame at full resolution and delivery size. Check anatomy, color, scale, placement, supports, prop state and start/end continuity. Only after the candidate passes, copy that exact PNG to the record's `target`.

For sharp scene frames, fill `result.review_checks` before approval. Example for the first Milo anchor (replace values with actual measurements from the saved image):

```json
{
  "identity_match": true,
  "plate_match": true,
  "pair_match": true,
  "measured_size": {"milo": {"height": 0.21, "head": 0.10}},
  "ground_contact": {"milo": {"surface": "clear grass lane", "x": 0.30, "y": 0.84}}
}
```

Run `python production/image_handoff.py --story lion_and_mouse_v6 check <image-id> --for-approval`, then `python production/image_prompts.py --story lion_and_mouse_v6 approve <image-id> --reviewed-by <name> --note "<visual review>"`. The approval records the exact target, prompt and reference hashes. Numeric checks catch size jumps; the visual review decides whether the stated support and character likeness are actually correct. If an approved root, plate, anchor or parent frame changes, its dependent frames need a fresh review and approval.

## Audio and render handoff

Keep narration, scene WAVs, `timing.json` and word timings under `work/stories/lion_and_mouse_v6/audio/en/`. They are not present locally. Once staged on LUMI, run `python production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v6 check` and `apply`; inspect the resulting `TIMING_SHEET.md` and `timing_plan.json`. Render only after every endpoint used by that scene has a current hash-bound approval. Export with `python production/export_runtime.py --manifest stories/lion_and_mouse_v6/prompt_manifest.json --story lion_and_mouse_v6 --scenes <numbers>` for a pilot. Run a still join preview, select takes, then render later scenes. All 154 clips are new v6 jobs.
