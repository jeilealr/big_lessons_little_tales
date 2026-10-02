# V4 release checks and current tool limits

This checklist implements [creation-rules.md](creation-rules.md). Checks are
manual documentation gates unless a tool below explicitly implements one.
No new validator or rendering behaviour was installed by this documentation pass.

**Status (2026-10-02).** Foundation and scene stills now exist: 139 of the 140
manifest image records are accepted after agent visual review (one,
`s02_place_acorn_end`, is missing), and the owner's review is ongoing. The boxes below are a template
and have not been formally ticked. Since 2026-10-02 `visual_bible.json` holds measured
character proportions, plate landmarks and per-setup sizes with anchor records, and
`production/image_prompts.py lint` checks the prompt items; the owner has not yet ticked
gates A and B. No clip exists, so gates C to
E have not started. The current owner instruction (the owner creates images;
agents only on request) is in `CLAUDE.md`.

## Gate A: story first, then foundation approval

- [ ] Owner has reviewed the proposed chronological shot plan and changed wording
      (trap falling from above; number/order of rope cuts; contact before waking).
- [ ] Every planned image has an individual expanded prompt and ordered references.

After script review, create foundation references in dependency order. The checks
below apply before **derivative/scene** images; a new canonical cannot be required
to exist before its own creation. Review each foundation before using it as a
parent. No media was authorised by the 2026-09-30 documentation task (image
creation was requested later; see the status above).

- [ ] Approved v4 Milo neutral reference has a smooth felt crown; face, ears, slim
      torso, eye palette and single tail match the chosen design.
- [ ] Leo has approved brown eyes, full rust/burnt-orange mane and four paws.
- [ ] Mouth references include closed, small and moderate openings plus Milo's
      functional gnawing mouth. All tooth/interior shapes have been approved.
- [ ] Character and camera calibration measurements are populated from images,
      not guessed from file dimensions or copied `h` values.
- [ ] A prop-free canonical and a same-depth cast lineup are approved. Each
      character has measured neutral height, head/mane width and relative
      size against every co-star before scene image generation.
- [ ] Each location has an approved plate and each shot setup has a size anchor,
      normalized actor boxes, ground baseline and depth plane. Close-ups have
      their own intentional camera/crop record.
- [ ] Shared plates have registered geometry for each light. The trap path uses
      one actual set, not a mixture of L-16 and unrelated net backgrounds.
- [ ] Acorn and net states and all expected occlusions are defined.

## Gate B: each saved image and pair

- [ ] Open the actual saved file and confirm it depicts its ID/purpose. I-07 must
      show standing free Leo with Milo and a fallen net behind them.
- [ ] Count cast, limbs and tails; inspect hidden roots/contacts as well as edges.
- [ ] Compare full-resolution face, eyes, torso/ear ratios and mane to canonicals.
- [ ] Compare every actor's nose/muzzle, cheeks, whiskers, eyes, seams, limbs
      and tail against the canonical and approved same-setup frame; confirm the
      complete identity list was repeated in the submitted prompt.
- [ ] Measure head/mane and whole-body boxes for each actor against the size
      anchor. Two characters sharing a depth plane retain their approved ratio;
      any size change has a documented forward/backward move or camera cut.
- [ ] Reject hair on v4 Milo, changed teeth, chubby torso, eye-colour drift.
- [ ] Confirm crop/pad/resize retains the required paws, tail, mane and props.
- [ ] Compare start/end at final video size, then blink/overlay them. Anatomical
      size, ground contacts and protected landmarks match the permitted delta.
- [ ] Fixed background is the approved plate: no trunk/rock movement or scene zoom.
- [ ] Only allowed pose/state changed; count/color/form of all props is continuous.
- [ ] All post-fall frames have an empty overhead branch. Broken ropes remain
      broken; labels/marks used for review are absent from the submitted picture.
- [ ] Pair endpoint truth matches motion text, including closed vs open mouths.
- [ ] Approvals bind to actual source/output hashes and prompt revision.

## Gate C: before individual video jobs

- [ ] Both endpoints are approved and available; no `TBD`, missing hash, stale
      image or draft script decision remains on the shot's dependency chain.
- [ ] One action; an explicit path/contact event; fixed or deliberately planned
      camera; frozen location-specific ambient clause.
- [ ] Exact positive and combined negative reviewed together. Specifically catch:
      closed mouth vs open end, teeth banned vs gnawing required, camera fixed vs
      push-in, sleeping vs open eyes, lion absent vs lion visible in a background.
- [ ] Tokenise the actual assembled positive/negative with the deployed model;
      record encoder limit, counts and truncation result. Preserve critical
      constraints when shortening; do not submit the full planning specification
      as an additional runtime suffix.
- [ ] Fast Lightning CFG 1 has no negative pass. Positive wording and endpoints
      explicitly carry each critical desired state; exclusions alone are insufficient.
- [ ] Separate `closed` and `mouth` candidates for each speaking/expressive beat;
      functional exceptions have closed reaction coverage documented.
- [ ] Start/end/handoff prop state is monotonic (especially damaged rope).
- [ ] Correct story slug, input paths, model/settings and revisioned outputs;
      image/crop/matte/installed-pack caches are rebuilt after source changes.
- [ ] Read `--dry-run`; independently inspect the effective negative and images.
- [ ] Pilot includes scale transition, wake/contact, run, gnaw/rope and a mouth
      pair. A failed pilot causes a prompt/anchor/plan change before another batch.
- [ ] Clip task file has no animatic, post-processing or assembly command.

## Gate D: candidate review and handoff to owner

- [ ] Watch every candidate at normal speed: readability, gait, ambient continuity,
      mouth interval and pacing. A contact sheet alone cannot show a bad trajectory.
- [ ] Inspect start, quarter, middle, three-quarter, end and frames around every
      contact/cut. Look closely at eyes, paws, tail roots, teeth and rope ends.
- [ ] Exactly one of each expected character throughout; continuous entry/exit,
      no duplicate, disappearance, identity blend, unwanted arm lift or tail reveal.
- [ ] Acorn persists; bite and cut align; rope ends persist; net falls behind Leo;
      no extra net overhead and no restored strand in later shots.
- [ ] Leaves/water/clouds follow their profile; trunks/roots/rocks and background
      scale stay fixed. Compare adjacent shots, not only each in isolation.
- [ ] Record `pass_for_owner_review`, `reject` or `needs_edit`, with reason and
      evidence. Do not mark a visually unreviewed save as fixed.
- [ ] Owner's selections include exact filenames, mode, seed, revision, trim and
      intended order. Ambiguous notes remain ambiguous until resolved.
- [ ] No automatic animatic. Separate assembly only after owner selection/request.

## Gate E: assembly (later, separately authorised)

Verify chosen clips exist with matching hashes/revisions; no silent fallback to
another mode, stale seed or still. Verify cut continuity and intentional ellipses,
match narration to observed mouth intervals where applicable, and review post
for newly warped paws/rope. Current animatic's equal splitting of scene audio is
not per-line dialogue timing. Do not claim it performs mouth/audio alignment.

## Findings in the code and data (read 2026-09-30, not changed)

Re-check the named code before relying on a row: the tools may have changed
since.

| Evidence | Consequence for v4 |
|---|---|
| `production/keyframe.py:place` crops a matte bounding box then normalises it to `h` | sitting/standing/running need anatomical registration and pose-specific box heights; same `h` is insufficient |
| `compose` uses only plate, crop, blur, still, x/y/h/flip; cache keys include path/crop, not input-content hashes | record calibration externally, version inputs and invalidate caches manually; new manifest fields do not auto-enforce geometry |
| `compose_keyframes.py` skips entries with `variant_of` | do not use that field for unbuilt mouth alternates and assume their frames will be composed |
| `shot.py` skips a render if its output exists | a changed prompt/input needs a new revisioned shot name or an explicit rebuild |
| `bllt/wan.py LIGHTNING` sets guidance 1.0/1.0 and documents no negative pass | fast-mode exclusions must also have positive desired-state wording and correct anchors; logging a negative is not enforcing it |
| `wan.generate` passes text without an explicit encoder length setting | count tokens with deployed tokenizer, check real limit/truncation; use the compact runtime candidate and preserve full specification in records |
| `shot.py` appends `negative_extra` to global negative | v3's blanket visible-teeth negative conflicts with gnawing; make v4 global terms mode-neutral |
| `shot.py --dry-run` checks some files and prints positive prompt | not a visual/negative/state/approval gate; no guarantee end plate or semantic contents are correct |
| `shot.py continue_from` currently looks for `<shot>_s<take>.mp4`, not the `_fast` fallback | resolve exact fast take and extract a new explicit keyframe when needed; do not assume fast continuation works |
| `animatic.py` prefers normal render before `_fast`, falls back to stills/cards, skips `variant_of`, splits audio equally | unsuitable as an unreviewed owner-selection resolver; use explicit selected filenames/modes and check actual source mapping before assembly |
| v3 `s16_laughing` asks camera to move closer but negates camera movement | remove contradiction in v4; proposed v4 baseline is fixed camera |
| v3 Milo sheet asks for rust-orange top hair; Leo sheet says rust-red while DNA says burnt-orange/rust | v4 identity and derived story sheets must match the revised approved canonicals |
| v3 S13/S15 portraits use blurred `net_trap_set.png` | trap's suspended net may survive as an incorrect background shape; use the correct world-state scene crop or a verified empty plate |
| current sidecars log prompts/settings but not complete approval/dependency hashes | append execution ledger and selection metadata manually until tooling is extended |

These explain plausible mechanisms. The owner's videos are not present under
`work/shots/` in this checkout (only notes were available); no claim of a fresh
video diagnosis or measured v4 success is made. New rules and thresholds need
validation on the future pilot.
