# V3 review -> v4 repair plan

Prepared 2026-09-30 from the owner's [original notes](../../docs/reviews/lion_and_mouse_v3_owner_notes_2026-09-30.txt),
archived verbatim from `work/shots/notes.txt`. This is a documentation revision.
The clips themselves were not available in this checkout; observations below
are the owner's, while proposed causes are hypotheses informed by code/recipes.
Nothing here selects a v4 take or authorises a render.

## Observation coverage

Rule IDs refer to [creation-rules.md](../../docs/creation-rules.md).

| Note | Owner observation / preference | V4 requirement and inspection |
|---|---|---|
| Overall | assembly before clip selection wastes time/resources | CR-01: separate individual renders, owner selection, then requested assembly |
| S01 first/second | likes `s01_milo_acorn_s1_fast.mp4` and `s01_milo_explores_s2_fast.mp4` | preserve preferences by filename, not ordinal; use the opening's established water/breeze profile across S01/S02 |
| S02 | acorn falls/disappears; Milo shrinks from eating to startled; water stops moving | CR-03/06/07: anatomical registration, retain acorn while looking up, explicit ground placement afterward, continuous water |
| S03 | likes `s03_decides_s2_fast.mp4`, `s03_two_paths_s3_fast.mp4` | retain selection preferences; matched endpoints and frozen fork geometry |
| S04 | likes `s04_shortcut_run_s3_fast.mp4`, but Milo is hard to follow | CR-08: sharp run reference, clear ground lane, enough subject pixels at actual render size, readable gait; upscaling alone insufficient |
| S05 first | incorrect/ugly eyes on waking; prefers sleeping version; quoted filename belongs to S04 | CR-02/05/07: keep asleep setup, approved brown-eye waking reference, contact before eyes open; filename unresolved, do not assign a seed |
| S05 second | likes `s05_the_trip_s2_fast` but characters and scene zoom; wake must follow paw touch | CR-03/04/07: separate approach/contact, aftermath cut and wake; one registered setup, no wide-to-close interpolation |
| S06 | both character/background sizes change without depth travel | CR-03/04: camera/plate locked, pair alignment, deliberate cut if framing changes |
| S07 first | likes `s07_leo_annoyed_s3_fast.mp4`; would accept more mouth movement | CR-05: closed default and separate mouth alternative using Leo mouth canonicals |
| S07 second | likes `s07_milo_sorry_s2_fast.mp4`; small close-up scale changes can be pleasing | CR-04/05: intentional gentle reframe permitted, preserve face proportions, no accidental zoom |
| S08 first | inconsistent hair leads to explicit removal of Milo's top hair | CR-02: new smooth-crown v4 canonical and all descendants; no more small-tuft compromises |
| S08 second/third | unrequested hands/paws; wants both mouth-moving and still-mouth versions as standing policy | CR-05: two labelled modes for expressive/dialogue shots, limbs anchored, no seed-as-mode substitution |
| S09 home | likes `s09_home_s1_fast.mp4` | preserve preference; home entry follows a visible doorway path, not disappearance |
| S09 hurry | likes `s09_milo_hurries_s3_fast.mp4`; others duplicate Milo or crouch oddly | CR-08: one bipedal Milo, forward gaze, no simultaneous look-back, continuous single trajectory |
| S09 stars | likes `s09_stars_s3_fast.mp4`; canopy/cloud motion is good | CR-06: retain gentle leaf/cloud profile, keep trunks fixed |
| S10 entry | deliberate trigger press may suit a curious Leo; depth motion is legitimate | CR-03/07: actor-depth path only; proposed curious-step narration below for owner review |
| S10 fall | falling net and plants good; tree stems move | CR-04/06/07: identical static plate geometry, local foliage only; one net leaves branches and lands |
| S11 first | mouth motion needs a closed alternative | CR-05: two modes, no claim of audio lip-sync |
| S11 second | background trunks move again | CR-04/06: registered backgrounds and effective prompt checks |
| S11 third | plants/shadows good; trunks stable | CR-06: use this distinction as the target ambient policy |
| S11 fourth | late paw/mane distortion; suspects missing end; note trails off | CR-04/05: approve end frames and inspect last quarter. By recipe, `s11_why_wont_it_break` lacks an end; ordinal may refer to another clip, so mapping remains unresolved |
| S12 first/second | good clips but wants delicate leaf motion; worries about Milo jumping across the cut | CR-04/06/08: shared start position/facing/depth at hear->run handoff, same ambient profile |
| S13 arrival | liked all, tail acceptable | CR-02/07: preserve one tail and continuous entrance; still review in v4 |
| S13 confidence | prefers seed 1 by ordinal; weird eyes in others; leaf changes side of net | CR-02/07: brown-eye reference, explicit rope/leaf layer order; candidate filename needs confirmation |
| S13 doubtful | seed 1 good, seed 2 safest; seed 3 paw wrong | CR-05: paws remain planted or fully outside portrait frame; retain ordinal preference as provisional |
| S13 playful | large arm changes fail; prefers arms lowered and endpoints | CR-04/05: expression-only playfulness, lower/hidden paws, matching end |
| S14 release/free appearance | two Milo tails; wrong hair; net should fall behind Leo | CR-02/07: one tail with explicit root, smooth crown, net behind lion; match by content rather than scene ordinal |
| S14 bite | Milo chubby/off-model; cut location differs from bite; rope pieces disappear | CR-02/07: slim torso, fixed bite strand/knots, persistent severed ends/fragments |
| S14 snap | rope restores then breaks magically | CR-07: monotonic damage state; no resetting to intact starting frame |
| S14 exit/order | net movement poor; unclear where Milo belongs; wants to review sequence first | CR-01/07: proposed ordered state chain below, Milo position carried through, owner review before images |
| S15 first | paw/tail embellishments often fail even if seed 1 works | CR-05: expression-only baseline, fixed limbs/tail |
| S15 second | closed mouth safest; wants optional mouth coverage | CR-05: distinct baseline and mouth alternative |
| S15 third/fourth | raised paws and changing mouth/teeth | CR-02/05: canonical mouth shapes, anchored limbs, inspect all frames |
| S16 | chubby/off-model Milo and inconsistent hair | CR-02/03: full canonical comparison, hair removal, torso/head/ear ratios and cast scale in ending |
| Prior image review | I-07 once contained the sleeping scene; N-02/N-08 overhead net; home resembled great tree; net mane redder | CR-02/06/07/09: semantic image ID check, single-net state, distinct low bank home, approved rust palette throughout |

A source filename identifies a preferred **v3** candidate only. No `take:` fields
have been modified. Scene numbering/ordinal inconsistencies are preserved rather
than silently resolved. In particular S01 notes reverse the YAML order, S05 names
an S04 file, S11's missing-end observation does not align cleanly to ordinal 4,
and S14's ordinal comments differ from the YAML ordering.

## Proposed v4 story changes to review before images

The original script remains at `../lion_and_mouse_v3/script_dialog_en.txt`.
The complete proposed version is [SCRIPT_REVIEW.md](SCRIPT_REVIEW.md), with
spoken-line IDs in [dialogue_coverage.json](dialogue_coverage.json).
These are draft changes, not approved new narration:

1. **S02 food:** Milo looks up while still holding the acorn; he then places it
   beside a fixed stone before leaving. This adds visible object continuity.
2. **S05 accident:** approach and paw contact; editorial cut over the tumble to
   the nose aftermath; only then show Leo's eyes opening. Keep the wide setup
   asleep. A subsequent cut places Milo on the ground before the barrier shot.
   Narration carries the omitted tumble; never render a body teleport as action.
3. **S09 order:** careful hurry -> stars cutaway -> home, followed by the
   existing days-passed narration before morning. The notes' “first/second” are
   review labels, not authority to reverse narrative chronology.
4. **S10 trigger:** suggested replacement for the script's upward-net wording:
   “One morning, something small beneath the leaves caught the lion's eye.
   He stepped closer. His paw pressed a hidden trigger, and a soft rope net
   dropped from the branches above.” This follows the owner's curiosity option.
   If the owner prefers an accident, remove the curious pause and use an ordinary
   walking footfall. Choose one before making endpoints.
5. **S14 simplify causality:** use one clearly identified load-bearing rope
   closure strand R01 that secures an existing folded opening. Establish this
   topology in the intact net before the bite; other mesh strands do not vanish.
   First fray it, then sever it at the bite point, widen the opening,
   let Leo step clear as the net slides behind him, then hold the free two-shot.
   Suggested narration replaces repeated unexplained snaps with: “The fibres
   frayed, one tiny bite at a time. At last the rope parted. The opening widened,
   and the lion stepped free.” If multiple cuts are retained in the story, add
   separately identified R02/R03 cuts with cumulative damage; never reset R01.
6. **S15/S16 speech/laugh:** closed smile/reaction coverage plus restrained mouth
   alternatives; the voice can carry laughter over a closed smile. No decorative
   paw or tail movement. The teeth dialogue does not authorise new tooth shapes.

## Rescue state chain proposed for approval

| Order | Start -> end | Milo and net continuity | Edit-safe fallback |
|---|---|---|---|
| 1. Gnaw/fray | `draped_intact` -> `frayed_R01` | both paws hold R01; incisors meet its fixed bite point; Leo waits | closed observing close-up plus narration |
| 2. Sever | `frayed_R01` -> `severed_R01` | R01 parts exactly at mouth; two ends persist, other knots unchanged | cut between approved frayed and severed stills |
| 3. Milo clear | `severed_R01` -> `severed_R01` | mouse releases his holding paws and steps to the safe side; broken ends remain | deliberate close-to-wide cut preserving contact/world state |
| 4. Sag | `severed_R01` -> `opening_R01` | gravity widens opening; ends remain broken; Milo already clear at recorded side | paired gentle hold with narration |
| 5. Step clear | `opening_R01` -> `fallen_behind` | Leo follows open lane; one net slides behind; Milo holds safe side position | split at approved intermediate `slipping_behind` frame |
| 6. Free hold | `fallen_behind` -> `fallen_behind` | Leo stands looking at Milo; one tail each, fallen net behind both | closed two-shot |

Before the sag shot, show Milo moving from bite contact to the safe side.
This is included as a separate clearance shot in the prompt packet; do not
teleport him when cutting from the bite close-up to a wide view. If a perspective
change is necessary, mark an editorial cut and preserve world state.

## Priorities and release status

- **P0:** smooth-crown Milo canonical; identity/mouth/geometry approval; script
  order decision; exact plate/state continuity; net/acorn permanence.
  *(Status 2026-10-02: the smooth-crown canonical exists; the other P0 items
  are still open or under owner review; see the packet's "Open issues".)*
- **P1:** matched endpoints for every character shot, readable run, dual mouth
  coverage, fixed limbs, location-specific ambient continuity.
- **P2:** final dialogue-to-shot duration expansion and owner candidate selection.

All new prompts are drafts. Image paths are planned and hashes/measurements remain
unfilled until actual creation. Required pilot: sitting->standing, asleep->wake,
run, fray->cut, and closed/mouth facial alternatives. No v4 success is claimed.

*Status 2026-10-02: the images now exist and their paths and hashes are in the
manifest results; the bible holds measured proportions, landmarks and per-setup
sizes (2026-10-02), and the clip pilot has not been run.*
