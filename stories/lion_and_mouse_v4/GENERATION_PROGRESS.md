# V4 image-generation progress

Updated 2026-10-01. This is a partial execution log of accepted and rejected v4
image attempts. Existing accepted roots are listed first; newly accepted assets
and their hashes/review notes follow. Continue with the next dependency-ready
manifest record and do not regenerate accepted roots unless a deliberate new
revision is requested.

| Record | Saved asset | SHA-256 | Review result |
|---|---|---|---|
| `MILO_CANON` | `character/characters/Milo/v4/canonical/full-body_milo_neutral_pose_r01.png` | `fab5cd7767ddbd6ed76a0367a3649cb4b0a53c02435f778a9c4a8b8f4072c306` | Smooth crown; original identity, pose, scale, tail and studio frame retained. |
| `LEO_CANON` | `character/characters/Leo/v4/canonical/full-body_leo_neutral_pose_r01.png` | `2ed72a4da14c02e65380842e79fbf634d5147a06ba373fbaacf8918e88273f0e` | Full rust-orange mane, brown eyes, four paws and original studio framing retained. |
| `M_SIDE_R` | `character/characters/Milo/v4/references/m_side_r_r01.png` | `863aa85c04e66893b13ebfc4c3b6ac7d2942e6e6a8b3b055f6404c827c17967a` | One tail, smooth crown, slim upright side view. |
| `M_SIDE_L` | `character/characters/Milo/v4/references/m_side_l_r01.png` | `03b6042a66ba7e95abb6b5c6d7f191b34188eb9b407a6df84cf97afa0827c655` | One tail, smooth crown, slim upright mirrored side view. |
| `M_BACK` | `character/characters/Milo/v4/references/m_back_r01.png` | `2cbf2390665aaa17be7d1de387e061fb2cf5aced9019f15d791b901dc2cad005` | Corrected candidate: both visible ear backs use taupe-grey outer felt. |
| `L_SIDE_R` | `character/characters/Leo/v4/references/l_side_r_r01.png` | `189211c6e2a1a3ae3aeb6d3539b58a6fe7f8422edbb86b0772ea63d67551bc4c` | Full mane volume, four paws and one tail retained. |
| `L_BACK` | `character/characters/Leo/v4/references/l_back_r01.png` | `cbb500480296d8582512205e6524903bc48db33d2e6c434ff75a784d6b389715` | Rear three-quarter view with stable mane and one tail. |
| `PL_stream_afternoon` | `character/locations/v4/stream_bank/stream_afternoon_r01.png` | `727eb39f3e7e3e99ff798879d5ba5dde2adedd7b47285319a160faf64e1392c6` | Clean empty afternoon plate; no characters or loose story acorns. |
| `M_CLOSED` | `character/characters/Milo/v4/references/m_closed_r01.png` | `c3ff875b653c405dce89bf4f2154f8f94512a23521381f57c6eb5f90c1e36934` | Previously accepted closed-mouth portrait, carried forward from user-provided approval. |
| `L_CLOSED` | `character/characters/Leo/v4/references/l_closed_r01.png` | `d4eb4526e9c85e864a26b64793409f92efa1c518069e7e0f4cc8f8b16a2cd765` | Previously accepted closed-mouth portrait, carried forward from user-provided approval. |
| `L_ASLEEP` | `character/characters/Leo/v4/references/l_asleep_r01.png` | `674d3d0e2f7e8b2b6a1f4e59cce947323bbff3b2873cd935096701c2aa1a971c` | Previously accepted asleep pose, carried forward from user-provided approval. |

Rejected and **not** copied into the repository: first `M_BACK` candidate. Its
left ear showed the dusty-rose inner surface as though it had been flipped.

## Resume order

1. Finish independent foundation assets: remaining character expression/pose
   references, location plates and prop material references.
2. Use these approved candidates as direct inputs for dependent v4 assets.
3. Create every scene start/end pair in dependency order, inspecting each saved
   result before using it downstream.
4. Update `prompt_manifest.json` result fields with actual paths, hashes, tool
   details and selection status as each asset is accepted.

Every accepted result is recorded with path/hash/review status in the manifest.
Some records remain rejected or pending; no clips, animatics, audio or GPU jobs
have been created.

- `M_RUN_R` — `character/characters/Milo/v4/references/m_run_r_r01.png` — SHA-256 `56444d3ee7d4f73179d83a7846d3b6c61844515cd999ed2c3e6f0058febe8559`. Accepted after visual review; first attempt rejected (airborne stride, arms too far out); second has planted foot, compact stride, low close arms, slim build, smooth crown and one tail. Output normalized from 1254x1254 to planned 1536x1536 with aspect preserved. Tool: built-in image_gen; model/seed not exposed.

- `M_SMALL` — `character/characters/Milo/v4/references/m_small_r01.png` — SHA-256 `04ecca80719a7dbc9be3104d4fab5f54d341e4775ac58ef3d7ee8730fe261a68`. Accepted after visual review; first attempt rejected for full-body framing, second preserves portrait framing and adds the specified small parted mouth. Canvas normalized from 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `L_SMALL` — `character/characters/Leo/v4/references/l_small_r01.png` — SHA-256 `4c61100073843de27d6caafd2158d8ce84c5f849f102f5eef175cc5dac9d6432`. Accepted after visual review; two framing attempts rejected, final matches L_CLOSED head-and-shoulders crop and keeps the full rust mane/upper chest, with a small parted mouth and no fangs. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `L_WAKE` — `character/characters/Leo/v4/references/l_wake_r01.png` — SHA-256 `50ef9161e84e912209d2f222e5930f8016ead824fd3b83ec02caa8e216e3f736`. Accepted after visual review; preserved asleep pose, body/paw contacts, mane, tail and crop, changing only the eyes to open brown eyes with cream sclera. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `M_RUN_L` — `character/characters/Milo/v4/references/m_run_l_r01.png` — SHA-256 `f33c2f0d18ed9229e6ba968719604e0254a206cc8ed6133cd61dc3a473ac7081`. Accepted after visual review; first attempt rejected for broad arm swing/stride, second has one planted foot, compact left-facing stride, upright body and arms close to torso. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `PROP_ACORN` — `character/locations/v4/props/prop_acorn_r01.png` — SHA-256 `d0cbebfed8a6befba298c60299b628c586538c43620bc53636fca922a3ba916c`. Accepted after visual review; one centered felt acorn with cap/stem and clear margins on blue background. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `PROP_NET` — `character/locations/v4/props/prop_net_r01.png` — SHA-256 `8d798b644fe5cc959c0845812d25cc38c5cd905038205683539f05e6e21b1fe9`. Accepted after visual review; one flat cream braided net material sample with square gaps and chunky knots, on blue. No topology implied. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `PL_stream_sunset` — `character/locations/v4/stream_bank/stream_sunset_r01.png` — SHA-256 `7ecf218c679b9c09268e4c68ef614163b59c979d233ef607e4e8f719aafd35db`. Accepted after visual review; first attempt rejected for copied acorns changing plate geometry; accepted version retains empty foreground and exact afternoon set layout, changing lighting only. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_fork_sunset` — `character/locations/v4/fork/fork_sunset_r01.png` — SHA-256 `9320ec95385b407d084d41561be9f14b962a07b4bdac9c54eebbe8e2d247d2bf`. Accepted after visual review; empty fork plate retains both path branches, central boulder and stable set geometry, no characters. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_shortcut_dusk` — `character/locations/v4/shortcut/shortcut_dusk_r01.png` — SHA-256 `df9a6ae0f9c18992c46a8108d191e6476e248a1856cfb929ba195fb7ff55eeb1`. Accepted after visual review; empty plate retains path lane, fallen log, stump, boulder, trunks and berry bushes. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_tree_dusk` — `character/locations/v4/great_tree/tree_dusk_r01.png` — SHA-256 `f447f682caf4a99ebdc536e8afd79e9b582c8bb902128c5b26d6eebb514466fa`. Accepted after visual review; empty great-tree clearing plate retains trunk/root geometry and left stream, with no characters. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_tree_day` — `character/locations/v4/great_tree/tree_day_r01.png` — SHA-256 `0446fe3094938842c77fb12a92f8bbb310c2aa894c81757e06f87024ff2c8cbf`. Accepted after visual review; day lighting applied to dusk plate geometry, preserving great tree, roots, clearing and left stream. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_tree_sky` — `character/locations/v4/great_tree/tree_sky_r01.png` — SHA-256 `ac3eeeb26d7488c2b90eec16030d4f15d8aec1cfbb04a125c4cdda6d252b1478`. Accepted after visual review; upward canopy plate retains branch silhouettes, stars and dusk sky framing, without props/characters. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_home_night` — `character/locations/v4/milo_home/home_night_r01.png` — SHA-256 `d538c75392ba535a42bc2dfc798c8898b3cce9ba8a2e775267d114071069e22e`. Accepted after visual review; low bank burrow and round door remain distinct from great-tree set; creek/stone bank retained. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_trap_morning` — `character/locations/v4/trap_path/trap_morning_r01.png` — SHA-256 `bd7bac850e64c4c3b78ad4b3e5ed032fe701fd4b1c609a6dc711d0275ec2ff23`. Accepted after visual review; empty morning forest path with all old overhead net/rope/trigger removed; forest geometry retained. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `PL_run_morning` — `character/locations/v4/forest_run/run_morning_r01.png` — SHA-256 `49b1e431f836b9def51248a6c37689898739b5f0c0d991b436b2a46082bb1794`. Accepted after visual review; empty run plate preserves foreground roots, middle bush, low branch and a clear travel lane. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `M_SIT_ACORN` — `character/characters/Milo/v4/references/m_sit_acorn_r01.png` — SHA-256 `78b6f2e85d3d524cb7a42e1e1d5fb5b4e8d18998c05998a792b688fa355a79dc`. Accepted after visual review; upright seated Milo holds one acorn with both paws, slim body, brown eyes, two large ears, one tail and smooth crown. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `M_STAND_ACORN` — `character/characters/Milo/v4/references/m_stand_acorn_r01.png` — SHA-256 `5024fa2e99db909cd8368210526d0177ced968ed8999656e4d8d5274ca0129de`. Accepted after visual review; standing slim bipedal Milo holds one acorn in both paws, brown eyes, two large ears, one tail and smooth crown. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.


Rejected scene endpoint attempt: `s01_explores_start` has four inspected built-in image_gen candidates, all rejected because Milo exceeded the manifest 0.30 frame-height target (the first also misplaced the acorn). Their paths, hashes and review notes are in the manifest result; none was saved at the target.

- `s09_stars_start` — `character/characters/interactions/v4/keyframes/s09_stars_start_r01.png` — SHA-256 `629510de5c609d9f90626c53ed7a22fa866dad7c6d10c23d204c28d23d335fdb`. Accepted after visual review; empty sky/canopy endpoint preserves plate framing, branches, stars and clouds. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `s09_stars_end` — `character/characters/interactions/v4/keyframes/s09_stars_end_r01.png` — SHA-256 `c9600eb070a6eb32a07ed6a9f6139ef2e68ca7a29ca0e456191939646952b920`. Accepted after visual review; clouds drift slightly while stars, canopy and framing stay stable. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `M_OPEN` — `character/characters/Milo/v4/references/m_open_r01.png` — SHA-256 `31ead959183bfa8a3c7142f0c212f5345b76fb8f6367f00c3ed9892671e12df8`. Accepted after visual review; moderate rounded mouth opening with matching small-mouth interior/tongue, no added teeth or muzzle change. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `M_GNAW` — `character/characters/Milo/v4/references/m_gnaw_r01.png` — SHA-256 `282cca5d0c7a678f9c3e273e8284c86ea2ff022d5626b8a097b5d030f057168a`. Accepted after visual review; rejected first full-body attempt; accepted chest-up crop shows two small upper incisors at one bite point on one continuous rope held by both paws. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `L_OPEN` — `character/characters/Leo/v4/references/l_open_r01.png` — SHA-256 `bc9ae02cbbe7b55e94669aa4ec8ae1f50c57c81e6a9e3d220d217aca33224a91`. Accepted after visual review; moderate rounded mouth opening, same small-mouth interior/tongue, stable muzzle and full rust mane, brown eyes and no fangs. Normalized 1254x1254 to 1536x1536. Built-in image_gen; model/seed not exposed.

- `s09_home_start` — `character/characters/interactions/v4/keyframes/s09_home_start_r01.png` — SHA-256 `e7b6523edb71964d2953514540f1c5b4c36ec36a1bb4635e95ed45540306f469`. Accepted after visual review; first three candidates rejected for scale, latch gesture and a crown tuft. Accepted image has one slim Milo facing the open doorway, paws down, brown eye, two ears, one tail and smooth crown. Measured Milo height about 0.33 frame / 1.0 doorway opening. Normalized 1680x945 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `s05_leo_sleeps_start` — `character/characters/interactions/v4/keyframes/s05_leo_sleeps_start_r01.png` — SHA-256 `e72d01ed76d851647939184bc40f7cab68367ea4ed4ab10754aca6c446add7f6`. Accepted after full-frame inspection; correct single sleeping Leo with full rust mane, one tail, one extended front paw and other paws naturally tucked; great-tree dusk landmarks and crop remain visually consistent with the supplied plate. Normalized 1672x941 to 1920x1080. Built-in image_gen; model/seed not exposed.

- `s05_leo_sleeps_end` — `character/characters/interactions/v4/keyframes/s05_leo_sleeps_end_r01.png` — SHA-256 `d5bca311f93e20281eb48eb5700f1902df45e01415622bc88e9699d87c649e2e`. Accepted after visual review; subtle breathing phase, closed eyes and mouth, paw contacts, mane, tail and great-tree layout match the approved start. Normalized 1672x941 to 1920x1080. Built-in image_gen; model/seed not exposed.

## Retry queue (2026-10-01)
The following starts/endpoints were attempted with the built-in image generator and remain unaccepted. Rejected candidates and their hashes/review notes are in `prompt_manifest.json`; none is approved for use as a reference. Retry these before generating their dependent endpoints.
- `s01_explores_start` — 7 recorded attempt(s); Milo again substantially exceeds 0.30 frame height. Acorn is on a stone but is oversized. Plate details also redrawn versus locked plate. Rejected and not used as reference.
- `s03_two_paths_start` — 1 recorded attempt(s); Milo is far taller than the required 0.30 frame height (about 0.40). Generated plate also substantially changes the approved fork layout and light. Rejected; not used as reference.
- `s04_shortcut_run_start` — 1 recorded attempt(s); Milo remains larger than the 0.30 frame-height target (about 0.34). Despite a grounded foot and close arms, scale is outside approved calibration; rejected, not used as reference.
- `s05_paw_contact_start` — 1 recorded attempt(s); Milo is much larger than 0.18 frame-height calibration (roughly 0.27); rejected and not used as reference. Leo anatomy, full mane and sleeping pose otherwise look consistent.
- `s09_home_end` — 2 recorded attempt(s); Milo absent, but plate geometry changed from approved start, including doorway placement/shape and background landmarks. Rejected; not used as reference.
- `s10_curious_step_start` — 1 recorded attempt(s); One net and correct Leo appear, but the mesh is taut overhead and has no clearly inspectable R01 near-left closure strand at the specified x=0.43,y=0.71 location. It cannot anchor monotonic rescue damage continuity. Rejected, not used as reference.
- `s12_hears_start` — 1 recorded attempt(s); Milo is much taller than the required 0.30 frame height (approximately 0.50); reject for scale. Crown smooth, brown eye and one tail otherwise visible. Not used as reference.
- `s16_friends_start` — 1 recorded attempt(s); Milo is about 0.31 frame height and about 0.64 Leo height, far above the required 0.18 / one-third ratio. Rejected and not used as reference. Both faces and smiles otherwise match; plate is visually similar but redrawn.

All other unaccepted records depend on one of these endpoints or on another unaccepted scene keyframe, so the dependency chain currently has no additional reference-ready scene to proceed with.

- `s04_shortcut_run_start` — `character/characters/interactions/v4/keyframes/s04_shortcut_run_start_r01.png` — SHA-256 `2f92db6b632c75faaa370c3f357edbe513e632e5fb70e9bb9a94cc81207ac029`. Accepted after visual review; exact shortcut plate preserved. Milo is at x=0.15, y=0.82, 0.30 frame-height, right-facing grounded short stride, low close arms, brown eye, smooth crown, two ears and one tail. Composed approved imagegen pose source onto locked plate with Pillow after `production/keyframe.py` could not import missing `cv2`; subtle contact shadow under planted paw.

- `s05_paw_contact_start` — `character/characters/interactions/v4/keyframes/s05_paw_contact_start_r01.png` — SHA-256 `8d5a9f62394b8f4f98a52a3f8b4f9f3bb75bd34678bb23f3cd484545660119e5`. Accepted after visual review; accepted sleeping Leo and plate unchanged; Milo approaches from left at x=0.32, y=0.84, 0.18 frame-height, slim with brown eye, smooth crown, two ears, one tail and low close arms. He is just short of contact. Composed from the accepted scene base and approved imagegen pose using Pillow after `production/keyframe.py` could not import `cv2`.

- `s05_paw_contact_end` — `character/characters/interactions/v4/keyframes/s05_paw_contact_end_r01.png` — SHA-256 `a7cdeceb3db441adda721f1716e80f6995b0aeceae2e80f785e1cc988b74e52e`. Accepted after review; Leo remains asleep, and exactly one small Milo reaches the paw with his leading planted foot. Arms remain low/close; smooth crown, brown eye, two ears and one tail. Composed from accepted scene/pose sources with Pillow after `production/keyframe.py` could not import `cv2`; exact plate pixels retained. The direct generated candidate was rejected for an arm reach; a first compositor draft was rejected for a duplicate Milo.

- `s05_nose_aftermath_start` — `character/characters/interactions/v4/keyframes/s05_nose_aftermath_start_r01.png` — SHA-256 `56aa3740736865b99475900042ded0a37346599a1b12a26a1f78d65b5c15d073`. Accepted after full-resolution inspection; editorial close two-shot with one Milo resting nose-to-nose against sleeping Leo, paws supported, Leo's eyes closed. Milo remains slim with smooth crown, two ears and one tail; Leo has full rust mane and one tail. Normalized 1672x941 to 1920x1080. Built-in image_gen; model/seed not exposed. The final two ordered Leo pose references were combined left-to-right in a temporary sheet to fit the tool's five-reference limit.

- `s05_nose_aftermath_end` — candidate rejected after saved-file inspection: Milo’s eye opened even though only Leo’s eyes could change. Candidate SHA-256 `acefe650c2753a21b6be38779b3ccdabf407ff3a1c47a343fe7e55d891acef49`; removed from target and not used as a reference. Retry required.

- `s05_nose_aftermath_end` — `character/characters/interactions/v4/keyframes/s05_nose_aftermath_end_r01.png` — SHA-256 `b8b5bc544c27b0710219e11e56d2c8593dbe9cc74e4dc7fc2e37da2d2d61f6dc`. Accepted after review; Leo’s brown eyes open in mild surprise, Milo’s eye remains closed, and nose/paw support, positions, scale, rust mane, tails and crop remain stable. Normalized 1672x941 to 1920x1080. Built-in image_gen; model/seed not exposed. First candidate was rejected and removed because Milo’s eye opened.

- `s04_shortcut_run_end` — `character/characters/interactions/v4/keyframes/s04_shortcut_run_end_r01.png` — SHA-256 `0b439cb502108e94cb56cc5492265bde3ec0b2f1ecd8a3d542ee68483a0f61e0`. Accepted after visual review; Milo is fully visible near x=0.86 at 0.30 frame-height, right-facing in the approved grounded short-stride pose with low close arms, smooth crown, brown eye, two ears and one tail. Exact shortcut plate retained. Composed from accepted imagegen pose and plate with Pillow after `production/keyframe.py` could not import `cv2`; direct generated candidate was rejected for excessive scale.

Rejected `s06_barrier_start` candidate: SHA-256 `5ec9870c4583728d73570ecbd8212bff23213973d823c0bc36b6aee25cda64c6`. Milo was about 0.32 frame-height instead of 0.18, and the generated background did not preserve the locked great-tree plate; candidate not saved or used as a reference. Retry required.

Rejected `s03_two_paths_start` retry: SHA-256 `4e46a30bb37fc4b5895f368f683a460837b1de4f8a98a41e101df8a77c891b07`. Milo is approximately 0.50 frame-height instead of 0.30, and the fork plate geometry differs; not saved or used as a reference. Retry required.

Rejected `s10_curious_step_start` retry: SHA-256 `008fb1a83268313642a7387c7897b2247816aaa9127898319da7522db4d3ab73`. Net became a broad overhead canopy; R01 closure and its knot anchors are not identifiable, and the trap-path plate changed. Not saved or used as reference; retry required.

- `s09_milo_hurries_start` — `character/characters/interactions/v4/keyframes/s09_milo_hurries_start_r01.png` — SHA-256 `2f92db6b632c75faaa370c3f357edbe513e632e5fb70e9bb9a94cc81207ac029`. Accepted after full-resolution and 1280x720 inspection; one right-facing Milo at x=0.15, 0.30 frame-height, using the approved grounded run pose. Smooth crown, brown eye, two ears, one tail and low close arms; exact shortcut plate pixels retained. Built-in image_gen pose source composed onto locked plate with Pillow because repo compositor import failed on missing `cv2`; model/seed not exposed. Small contact shadow under planted foot.

Rejected `s12_hears_start` retry: SHA-256 `d5ab0fde37f928827738f32c05bd0135abe902a65e8e8c628ffa6fd932884b16`. Milo is approximately 0.50 frame-height instead of 0.30; the forest-run plate changed. Not saved or used as reference; retry required.

- `s03_two_paths_start` — `character/characters/interactions/v4/keyframes/s03_two_paths_start_r01.png` — SHA-256 `fdc14def4fca770c800c955ba653f4503786d3ea4fd3e00c88ba31079f51263b`. Accepted after full-resolution and 1280x720 inspection. Milo is 0.30 frame-height at x=0.50, facing toward the safe left path in the approved grounded left-facing stride; slim body, smooth crown, brown eye and one tail. Exact fork plate pixels, both branches and central boulder retained. Built-in image_gen approved M_RUN_L pose composed onto locked plate with Pillow because repo compositor import failed on missing `cv2`; model/seed not exposed. Direct-generation candidate rejected for scale/plate mismatch.

Rejected `s03_two_paths_end` candidate: SHA-256 `94aac1e0124b492c42777738d52092f20aefba0f82bfc6904e2bf6cd7d0935f2`. Milo turns his whole body toward camera rather than keeping the same body/paws/tail and changing only the head; the tail is not visible. Not saved or used as reference; retry required.

Rejected `s16_friends_start` candidate: SHA-256 `06205453a4257d552e41abadd9cf69472042a95161b8e67825d142dbd63e27cb`. Milo is about 0.31 frame-height instead of 0.18, and tree/day set geometry shifted. Not saved or used as reference; retry required.

Rejected `s09_home_end` retry: SHA-256 `903f5f8e011b84aefb94ce4647ea1dfb5a8904a10edb26626d537967dc967a13`. Milo is occluded, but the doorway, lantern, bank and crop differ from the approved home-start/locked plate. Not saved or used as reference; retry required.

- `s01_explores_start` — `character/characters/interactions/v4/keyframes/s01_explores_start_r01.png` — SHA-256 `27c01db3c0bde0b1e72ffabb5bd2f79400b63ab3b119efb9b1e258e26bed4dfe`. Accepted after full-resolution and 1280x720 inspection. Milo is x=0.30, 0.30 frame-height, upright right-facing short walking stride, empty paws, closed mouth; slim, brown eye, smooth crown, two ears and one tail. Exact stream-afternoon plate and feeding-stone position retained; no acorn visible. Built-in image_gen approved M_RUN_R pose composed onto locked plate with Pillow after repo compositor import failed due to missing `cv2`; model/seed not exposed. Earlier direct-generation attempts rejected for excessive scale and/or prop/plate mismatch.

Withdrawn `s01_explores_start` composite: prior SHA-256 `27c01db3c0bde0b1e72ffabb5bd2f79400b63ab3b119efb9b1e258e26bed4dfe`. A manifest consistency audit found the required single story acorn at the feeding stone was omitted (zero visible instead of one). Removed from target, marked retry-needed, and not used as a reference.

- `s09_milo_hurries_end` — `character/characters/interactions/v4/keyframes/s09_milo_hurries_end_r01.png` — SHA-256 `0b439cb502108e94cb56cc5492265bde3ec0b2f1ecd8a3d542ee68483a0f61e0`. Accepted after review by byte-identical reuse of the already accepted/inspected `s04_shortcut_run_end` composition: one right-facing Milo at x=0.86, 0.30 frame-height, same depth, normal gait and same locked shortcut plate. The record’s authorized delta is horizontal travel only. Built-in image_gen approved pose source plus Pillow-composed locked plate; source SHA-256 `0b439cb502108e94cb56cc5492265bde3ec0b2f1ecd8a3d542ee68483a0f61e0`; model/seed not exposed.

- `s01_explores_start` — `character/characters/interactions/v4/keyframes/s01_explores_start_r01.png` — SHA-256 `e895a5c5108e73aad6d6f98c1f80107d4b2d2b3f80f3f21aaa827ba00ed5e478`. Accepted after full-resolution and 1280x720 review. One Milo at x=0.30, 0.30 frame-height, right-facing walking stride, empty paws and closed mouth; slim, brown eye, smooth crown, two ears and one tail. Exactly one small approved acorn rests on the feeding stone at x=0.60. Exact stream plate retained. Built-in image_gen approved M_RUN_R and PROP_ACORN sources composed with Pillow because the repo compositor could not import missing `cv2`; model/seed not exposed. An earlier composite missing the acorn was withdrawn and not used as a reference.

- `s01_explores_end` — `character/characters/interactions/v4/keyframes/s01_explores_end_r01.png` — SHA-256 `c472fae0571c824c5c13ecb6c793d26570070112c56977e6a00796a3970c515e`. Accepted after full-resolution and 1280x720 review. Same Milo pose, depth, scale and expression as start, moved from x=0.30 to 0.55; exactly one acorn remains on the feeding stone. Exact stream plate retained. Built-in image_gen approved M_RUN_R and PROP_ACORN sources composited with Pillow after repo compositor import failed because `cv2` is unavailable; model/seed not exposed.

- `s01_acorn_start` — `character/characters/interactions/v4/keyframes/s01_acorn_start_r01.png` — SHA-256 `1a2bc8e89579d67bc3c8eae5b5557c0f7e66151bd06746c8b885a4dae81d4d2c`. Accepted after full-resolution and 1280x720 inspection. One slim seated Milo at x=0.55, baseline y=0.84, 0.30 frame-height, holding exactly one approved acorn in both paws at mouth contact. Brown eyes, smooth crown, two ears, one tail; exact stream plate retained and no loose acorn remains on stone. Built-in image_gen generated the seated holding pose; Pillow composited it onto the exact plate because repo compositor import failed due to missing `cv2`. Six ordered refs were passed using a labeled sheet for refs 3+4 to meet the tool's five-reference limit. Model/seed not exposed.

Rejected `s01_acorn_end` direct scene candidate: SHA-256 `809d7498dec44de62c45109be5d692dd9f000ddfd91edab0390e9a13ca50511e`. Imagegen returned a full scene instead of the requested pose-layer edit; Milo was much larger than 0.30 frame-height, body/pose drifted, and the locked plate changed. Not saved or used as reference; retry required.

- `s01_acorn_end` — `character/characters/interactions/v4/keyframes/s01_acorn_end_r01.png` — SHA-256 `787148a4491520ee7f782f97661d016fe83923152615ce015dcada1dbca41f0b`. Accepted after full-resolution and 1280x720 review against the start frame. Same seated body, hand contacts, scale and position; one acorn remains identifiable at the mouth, with a small nibble visible and the nut intact. Brown eyes, smooth crown, two ears and one tail; exact stream plate retained. Built-in image_gen pose edit composed with Pillow after repo compositor import failed because `cv2` is unavailable; model/seed not exposed.

- `s02_notice_start` — `character/characters/interactions/v4/keyframes/s02_notice_start_r01.png` — SHA-256 `c8a97d101ef6ba0e2255d6a7dc0b3558922ca93b8f8041c4b4e22ef05d34e845`. Accepted after full-resolution and 1280x720 review. Seated Milo at x=0.55, baseline 0.84, holding one acorn at chest level, mouth closed, content eyes; brown eyes, smooth crown, two ears and one tail. Exact stream-sunset plate retained. Built-in image_gen approved M_SIT_ACORN pose composed onto locked plate with Pillow after repo compositor import failed due to missing `cv2`; model/seed not exposed.

- `s02_notice_end` — `character/characters/interactions/v4/keyframes/s02_notice_end_r01.png` — SHA-256 `3ad219dd9f164598029fb45d21713a0fab29a7fc12a7bbe627284583e2d8d50b`. Accepted after full-resolution and 1280x720 comparison with start. Same seated body, hand-held acorn, paws, scale and tail; eyes now look slightly upward with mild realization, mouth closed. Brown eyes, smooth crown, two ears; exact stream-sunset plate retained. Built-in image_gen studio edit composed with Pillow after repo compositor import failed due to missing `cv2`; model/seed not exposed.

- `s02_stand_with_acorn_start` — `character/characters/interactions/v4/keyframes/s02_stand_with_acorn_start_r01.png` — SHA-256 `3ad219dd9f164598029fb45d21713a0fab29a7fc12a7bbe627284583e2d8d50b`. Accepted by byte-identical reuse of the already accepted `s02_notice_end`, because the manifest's start endpoint is exactly the same seated Milo/acorn pose, gaze, mouth and location. Exact image was inspected at full resolution and 1280x720. Source SHA-256 `3ad219dd9f164598029fb45d21713a0fab29a7fc12a7bbe627284583e2d8d50b`.

- `s02_stand_with_acorn_end` — `character/characters/interactions/v4/keyframes/s02_stand_with_acorn_end_r01.png` — SHA-256 `9839c1e15de84e85a3f871c6d46c806032afd4eaee99a76280caa9bef1ea9f8c`. Accepted after full-resolution and 1280x720 review. Milo stands on the same ground contacts and at the same scale, holding the same single acorn with both paws; brown eyes, smooth crown, two ears and one tail. Exact sunset plate retained. Built-in image_gen approved M_STAND_ACORN pose composed with Pillow after repo compositor import failed because `cv2` is unavailable; model/seed not exposed.

- `s02_place_acorn_start` — `character/characters/interactions/v4/keyframes/s02_place_acorn_start_r01.png` — SHA-256 `dc2367cac8132abfbeb4e0deca5d77d46c3e118231228608b88ebf304b4948bf`. Accepted after full-resolution and 1280x720 inspection. One slim Milo at x=0.55, 0.30 frame-height, standing and oriented toward feeding stone x=0.60, holding exactly one acorn at chest level; brown eyes, smooth crown, two ears, one tail, low arms. Exact sunset plate retained. Built-in image_gen pose edit composed with Pillow after repo compositor import failed because `cv2` is unavailable; model/seed not exposed.

- `s02_place_acorn_end` — `character/characters/interactions/v4/keyframes/s02_place_acorn_end_r01.png` — SHA-256 `1da09dd93639cce41bdb5c62fceb3d0eac88fd5d7f72864e81e2294847894c50`. Accepted after full-resolution and 1280x720 inspection. Milo bends slightly with both empty paws immediately above one acorn placed beside the feeding stone at the ground plane; brown eyes, smooth crown, two ears and one tail. Exact sunset plate retained. Built-in image_gen produced the approved pose/object layer; Pillow composed onto the exact plate after repo compositor import failed because `cv2` is unavailable. First asymmetrical-paw candidate rejected and recorded. Model/seed not exposed.

- `s03_two_paths_end` — `character/characters/interactions/v4/keyframes/s03_two_paths_end_r01.png` — SHA-256 `14956d3a07c78e3ea900cba276ffba31e85408011bfc721a5d08afcbc69e87c2`. Accepted after full-resolution and 1280x720 review beside start. Milo remains at x=0.50 and the same scale, low paws, short-stride feet and one tail; only head/gaze turns modestly toward the right shortcut. Smooth crown, brown eyes, two ears; exact fork plate and both branches/central boulder retained. Built-in image_gen studio edit composed with Pillow after repo compositor import failed due to missing `cv2`; earlier whole-body-turn candidate rejected and recorded. Model/seed not exposed.

Rejected `s06_barrier_start` composition experiment: SHA-256 `f9ece76317d2428570c59ae8fcd7defb83b7b35579375fdf8720b695495862dd` (temporary, not saved to target). It used the exact tree plate and target character scale, but the white-background matte left visible gaps/floor artifacts around Leo, including near the muzzle/paw edges. Not saved or used as reference; needs a better cutout workflow.

- `s09_home_end` — rejected built-in image_gen attempt SHA-256 `7d3e3c9557b6bedcf3e836073150380c218bdf63c2a6641d50c8e6cc9ef6577b`. Milo was fully occluded, but doorway, lantern, bank, creek, lighting and crop changed substantially versus the locked start. Not saved to target and not used as a reference.

- `s03_decides_start` — rejected built-in image_gen attempt SHA-256 `3a9b2dea0aa7a84169260a35cc37cfe4dc38570ca2379f656b52b4fd7849d25b`. Milo keeps the smooth crown, but fork path/vegetation/horizon and sunset illumination do not match the approved plate; not saved to target or used as a reference.

- `s12_hears_start` — rejected built-in image_gen attempt SHA-256 `4d8b3dea21bb8231cb7413de2ea775c993d0e03a6b287e6d0efc79728cea63d6`. Mouse is recognizable, but its full silhouette is about half the frame height against the 0.30 target; the forest path, foreground roots and surrounding set geometry are redrawn. Rejected; not saved or used as a reference.

- `s16_friends_start` — rejected built-in image_gen attempt SHA-256 `b3a080c090d7cabf19884a0a9c11b46ee275e666e125e328eefee718397516d6`. Milo is substantially larger than the 0.18 frame-height calibration and both characters/plate landmarks are redrawn versus the locked daylight great-tree setup. Rejected; not saved or used as a reference.

- `s10_curious_step_start` — rejected built-in image_gen attempt SHA-256 `031edd705e99e52598c38ac2335e624e3aedbb677506ba96c0005d1aa80f9166`. The net is a broad overhead canopy rather than the specified single low slack net with identifiable R01 closure strand; Milo is large, Leo is walking rather than supported, and trap-path geometry changed. Rejected; not saved or used as a reference.

## Continuation retry status (2026-10-01)

A first batch of candidates was rejected for `s09_home_end`, `s03_decides_start`, `s16_friends_start`, `s12_hears_start`, and `s10_curious_step_start`; each candidate path, SHA-256 and reason is recorded in its manifest result above. A new transparent-character-layer workflow then produced accepted `s12_hears_start` on the exact run-morning plate. The same approach was tried on `s16_friends_start`; the combined cutout made Milo much larger than the required scale, so it was rejected. A retry for `s12_hears_end` returned a redrawn scene and the wrong running pose, so it was rejected and not used downstream.

The manifest currently has 58 accepted image records with existing saved outputs out of 118 total. Unresolved scene starts are `s03_decides_start`, `s09_home_end`, `s10_curious_step_start`, and `s16_friends_start`; `s12_runs_start` is additionally blocked until `s12_hears_end` is accepted. Continue in dependency order with the remaining start/end records and only use accepted sources.

- `s12_hears_start` — `character/characters/interactions/v4/keyframes/s12_hears_start_r01.png` — SHA-256 `29d73b499e4b325d4b1847974ea8e04344ac9ebbe990884b73c63d93f900b3a1`. Accepted after full-frame and enlarged-edge inspection. Built-in image_gen transparent character layer on the exact approved run-morning plate; one slim left-facing Milo at x=0.78, 0.30 frame-height, feet grounded at y=0.82, brown eye, two ears, one tail, smooth crown, low arms. Plate pixels retained outside Milo/contact shadow. Source layer SHA-256 `2c2328e83d77642947fd9f356082c908a283411715fd501d9a6192dca92b0b7f`; model/seed not exposed.

- `s12_hears_end` — rejected built-in image_gen attempt SHA-256 `1853aa9ddcacfe63b781c1e7da1bc5358eb5018a240b90bdd6e408972dc1c01b`. Despite requesting a transparent layer, the output is a full redrawn forest scene; Milo leans into a running stride instead of retaining the grounded listening pose, and plate pixels drift. Not saved to target or used downstream.

- `s16_friends_start` — rejected transparent built-in image_gen layer SHA-256 `962d64f1b6f07213592b63f6cd7372cf68bef312ee3fcc4c440b3b394f47bbd7`. Character anatomy and poses are usable, but Milo is roughly 0.42 frame-height relative to Leo versus the required 0.18; separate scaled character layers are needed. Not composited, saved to target, or used downstream.

- `s16_friends_start` — `character/characters/interactions/v4/keyframes/s16_friends_start_r01.png` — SHA-256 `bf274f37709a7886c1351d59d0fabad1f416d0cd36cfcd86f2cd089b2c91d14e`. Accepted after full-frame and enlarged crop inspection. Separate built-in image_gen transparent Leo (`483cefec3de4980db74808b1c93bc500f6864845d2654a1f46d3bf89fdde3cf9`) and Milo (`76d601219596d5fc35cba37b91e47bc72c97cfd9b32012f07e1208789f1814f9`) layers were placed independently on the exact approved great-tree daylight plate. Leo lies with full rust mane, brown eyes, four paws and one tail. Milo sits by Leo's paw, slim with smooth crown, brown eyes, two ears and one tail. No props or duplicates; both grounded at y=0.84. Model/seed not exposed.

### Successful separate-layer scale method

For mixed-size cast frames, generate each character as an isolated transparent PNG using the record’s ordered approved references and full positive prompt, with a character-only intermediate instruction. Inspect each layer before use. Derive the layer resize from approved canonical subject height and matching mane/ear width, so the manifest’s neutral standing-equivalent scale still holds for lying or seated poses. Trim low-alpha fringe, place each layer independently at its specified center and shared ground baseline on the exact approved plate, then inspect the full frame and contact crop before saving. For `s16_friends_start`, Leo was placed at 699×444 px, x=0.72; Milo at 159×157 px, x=0.54; baseline y=0.84. Preserve this output as the accepted reference for its dependent end frame.

- `s16_friends_end` — `character/characters/interactions/v4/keyframes/s16_friends_end_r01.png` — SHA-256 `438e39b3b46caf0fb7030b868be1ce0296098f5f8bae33b45e73df7b514ad4f1`. Accepted after full-frame and eye-detail review. Built-in image_gen Leo (`c88fa4b7abef6bc694423dd994f8508d34005728041f6c4f82826bfa2dedfe93`) and Milo (`368a68afb44e2718fb2d73623096f9ec81af4714ae8e51d7e65572ad6db3360a`) transparent end-expression layers supplied only narrowed-eye pixels; feathered eye masks were applied to the exact accepted start. Body poses, full mane, ears, tails, paw contacts, character scale, and daylight plate remain identical to the start outside eye regions. Model/seed not exposed.

### Successful localized expression method

For subtle paired endpoints, generate transparent expression layers from the approved start and canonical identities, then copy only the authorised facial change into the accepted start frame with small feathered masks. Align eye features first; keep every other pixel from the start. This avoids regenerated mane, body or plate drift. `s16_friends_end` uses two Leo eye masks and two Milo eye masks; mask locations, feather and source hashes are in the manifest composition record.

- `s12_hears_end` — rejected transparent-layer retry SHA-256 `8a3df0816cadbc155c123a61dd45b74a01100268e61a697c563dd6a4a98b081d`. The built-in image_gen returned a full redrawn forest scene with changed Milo pose/scale despite the approved start and transparent pose inputs. No target saved or downstream use.

- `s03_decides_start` — rejected transparent-portrait retry SHA-256 `f2b10068ff79d584416c372f508d0b62b0e8d69a396c9bcf5c96db665939bee5`. The built-in image_gen returned a full scene with redrawn path/trees/boulder and wrong crop calibration. Not saved to target or used downstream.

- `s09_home_end` — `character/characters/interactions/v4/keyframes/s09_home_end_r01.png` — SHA-256 `d6144b5a46cb8dd811e6650d6642ae89e152dcaa9adbabdb66a573a5b8b153f0`. Accepted after local crop and full-frame inspection. Built-in image_gen empty doorway patch (`4f318379070026aa2c71f99bfd5eb8f420f9407a4d32b7bd9b367edbfba051f9`) was masked into the approved `s09_home_start` only where Milo and his tail had occluded the set; the open door, lantern, creek and surrounding plate remain in position. Zero visible Milo or tail, no acorn. Model/seed not exposed.

### Successful local inpaint method

For an exit/occlusion endpoint, crop the approved start around the character and fixed landmarks; send the ordered approved references plus that exact derivative crop to built-in image_gen, requesting only the empty local crop. Inspect the generated fill, then insert it under a feathered mask around the character and all appendages into the exact approved start. Review the crop and whole frame for remaining limbs/tail, seams and landmark drift. `s09_home_end` used crop x=430..1129, y=330..889 and a 9 px feather. Exact crop box and patch hashes are in the manifest.

- `s06_barrier_start` — `character/characters/interactions/v4/keyframes/s06_barrier_start_r01.png` — SHA-256 `7ccd0c3b5dd8f9a08d9da74341afcabab84aaca06c1e4d9003375c8249a1a70c`. Accepted after full-frame and contact-crop inspection. Built-in image_gen produced separate transparent Leo (`eba6d0fd4c4547633fcdeafb12f931758222612e304311012c18a13f3199c3e3`) and Milo (`c2bf3cca5af3c6841f95b649557d06841816ec0cbb389e769db72565cb00e12d`) layers, each inspected before Pillow placement on the exact approved dusk tree plate. Leo has four paws, one tail, full rust mane and brown eyes, and places the near paw beside Milo. Slim Milo has two ears, one tail, smooth crown and brown eyes; both are grounded at y=0.84 with manifest-calibrated scale. Direct-scene attempt rejected for plate/scale drift. Model/seed not exposed.

### Successful dusk barrier layer method

The previous white-matte approach left gaps around Leo. Generating Leo and Milo as separate transparent layers and trimming low alpha allowed exact plate geometry and independent scale. The accepted character/contact crop was inspected at original resolution. The source layer paths, hashes and composition dimensions are recorded in the manifest.

- `s12_hears_end` — `character/characters/interactions/v4/keyframes/s12_hears_end_r01.png` — SHA-256 `299f4a98a00a259928bee17e046e403e6e5dbf03a334d919e82eaba07a6a816c`. Accepted after source-head, full-frame and enlarged crop inspection. Built-in image_gen isolated a transparent Milo head (`9570c35a28e1a15c02bbc5abd45598283b890795f94cc294fdb43d17de100d3d`) from the accepted start plus canonical reference and exact head crop. The old head region was restored from the locked plate, then the new head was attached at the same scale to the accepted slim body. Two ears, smooth crown, brown leftward gaze, one tail, low arms and grounded feet; plate and body retained. Model/seed not exposed.

### Successful local head replacement method

For a small listening-expression change, crop the approved start around the head and use that exact crop after the ordered references in built-in image_gen. Generate only an isolated transparent head, inspect it, restore the old head silhouette from the exact approved plate, then composite the new head at the same size and position over the unchanged body. Inspect the neck join, ears, eyes and full frame. This kept `s12_hears_end` grounded and the forest landmarks fixed after full-scene retries drifted.

- `s03_decides_start` — `character/characters/interactions/v4/keyframes/s03_decides_start_r01.png` — SHA-256 `4af56d33714bcfe39d96b14d42ce15ee096966c584a3ee7ef08d614e19c2b903`. Accepted after transparent portrait-layer and full-frame inspection. Built-in image_gen Milo portrait (`903a50affa9899a20ba573443b16530d2004afd667660a3427dfbded19ba9979`) has two large ears, smooth crown, brown eyes and closed thinking expression. It was placed over a softly blurred, fixed crop of the exact approved fork-sunset plate, with skull width about 0.32 and eye line about 0.43; paws/tail outside crop, no acorn or extra landmarks. Model/seed not exposed.

### Successful exact-plate portrait method

When full-scene portrait generations changed fork landmarks, generate only a transparent upper-body character using the ordered approved references plus an accepted head guide. Use a single measured crop of the locked location plate for the blurred background, scale the head to the manifest skull width and eye line, and extend only the lower torso to the bottom of frame so no cut edge remains. Inspect the source and full composition. The same crop should be reused for the paired end frame.
