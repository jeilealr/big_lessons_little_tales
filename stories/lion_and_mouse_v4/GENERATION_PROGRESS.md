# V4 image-generation progress

Updated 2026-09-30. Creation has started with the foundation family. The files
listed below are saved project assets, visually inspected in this session, and
are the only generated v4 images so far. Continue from the next foundation
references; do not regenerate these roots unless a deliberate new revision is
requested.

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

The image prompt records remain drafts until their `result` fields are populated.
No clips, keyframes or v4 runtime jobs have been created.
