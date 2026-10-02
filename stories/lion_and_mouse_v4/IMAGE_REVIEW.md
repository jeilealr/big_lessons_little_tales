# lion_and_mouse_v4: image review

Every image of this version, generated from `prompt_manifest.json` by `python3 production/image_review_md.py`. Fill in **Keep**: `keep`, `redo` or `drop`, and add notes; rerunning the script keeps your entries. Framing follows `docs/creation-rules.md` CR-15.

## Shot order and framing

```mermaid
flowchart LR
  subgraph S01["Scene 1"]
    direction LR
    s01_explores["s01_explores<br/>wide scene"]:::wide
    s01_acorn["s01_acorn<br/>wide scene"]:::wide
  end
  subgraph S02["Scene 2"]
    direction LR
    s02_notice["s02_notice<br/>wide scene"]:::wide
    s02_stand_with_acorn["s02_stand_with_acorn<br/>wide scene"]:::wide
    s02_place_acorn["s02_place_acorn<br/>wide scene"]:::wide
  end
  subgraph S03["Scene 3"]
    direction LR
    s03_two_paths["s03_two_paths<br/>wide scene"]:::wide
    s03_decides["s03_decides<br/>close-up, blurred bg"]:::closeup
  end
  subgraph S04["Scene 4"]
    direction LR
    s04_shortcut_run["s04_shortcut_run<br/>wide scene"]:::wide
  end
  subgraph S05["Scene 5"]
    direction LR
    s05_leo_sleeps["s05_leo_sleeps<br/>wide scene"]:::wide
    s05_paw_contact["s05_paw_contact<br/>wide scene"]:::wide
    s05_nose_aftermath["s05_nose_aftermath<br/>close two-shot"]:::two
  end
  subgraph S06["Scene 6"]
    direction LR
    s06_barrier["s06_barrier<br/>wide scene"]:::wide
  end
  subgraph S07["Scene 7"]
    direction LR
    s07_leo_annoyed["s07_leo_annoyed<br/>close-up, blurred bg"]:::closeup
    s07_milo_sorry["s07_milo_sorry<br/>close-up, blurred bg"]:::closeup
  end
  subgraph S08["Scene 8"]
    direction LR
    s08_leo_softens["s08_leo_softens<br/>close-up, blurred bg"]:::closeup
    s08_milo_surprised["s08_milo_surprised<br/>close-up, blurred bg"]:::closeup
    s08_kindness["s08_kindness<br/>wide scene"]:::wide
  end
  subgraph S09["Scene 9"]
    direction LR
    s09_milo_hurries["s09_milo_hurries<br/>wide scene"]:::wide
    s09_stars["s09_stars<br/>plate only"]:::plate
    s09_home["s09_home<br/>wide scene"]:::wide
  end
  subgraph S10["Scene 10"]
    direction LR
    s10_curious_step["s10_curious_step<br/>wide scene"]:::wide
    s10_net_falls["s10_net_falls<br/>wide scene"]:::wide
  end
  subgraph S11["Scene 11"]
    direction LR
    s11_pull_once["s11_pull_once<br/>wide scene"]:::wide
    s11_why_wont_it_break["s11_why_wont_it_break<br/>close-up, blurred bg"]:::closeup
    s11_call["s11_call<br/>close-up, blurred bg"]:::closeup
    s11_waits["s11_waits<br/>wide scene"]:::wide
  end
  subgraph S12["Scene 12"]
    direction LR
    s12_hears["s12_hears<br/>wide scene"]:::wide
    s12_runs["s12_runs<br/>wide scene"]:::wide
  end
  subgraph S13["Scene 13"]
    direction LR
    s13_arrives["s13_arrives<br/>wide scene"]:::wide
    s13_milo_confident["s13_milo_confident<br/>close-up, blurred bg"]:::closeup
    s13_leo_doubtful["s13_leo_doubtful<br/>close-up, blurred bg"]:::closeup
    s13_milo_playful["s13_milo_playful<br/>close-up, blurred bg"]:::closeup
  end
  subgraph S14["Scene 14"]
    direction LR
    s14_gnaw_fray["s14_gnaw_fray<br/>close two-shot"]:::two
    s14_sever_R01["s14_sever_R01<br/>close two-shot"]:::two
    s14_milo_clear["s14_milo_clear<br/>wide scene"]:::wide
    s14_opening["s14_opening<br/>wide scene"]:::wide
    s14_step_clear["s14_step_clear<br/>wide scene"]:::wide
    s14_free_hold["s14_free_hold<br/>wide scene"]:::wide
  end
  subgraph S15["Scene 15"]
    direction LR
    s15_leo_amazed["s15_leo_amazed<br/>close-up, blurred bg"]:::closeup
    s15_milo_modest["s15_milo_modest<br/>close-up, blurred bg"]:::closeup
    s15_leo_reflects["s15_leo_reflects<br/>close-up, blurred bg"]:::closeup
    s15_milo_sincere["s15_milo_sincere<br/>close-up, blurred bg"]:::closeup
  end
  subgraph S16["Scene 16"]
    direction LR
    s16_friends["s16_friends<br/>wide scene"]:::wide
  end
  s01_explores --> s01_acorn
  s01_acorn --> s02_notice
  s02_notice --> s02_stand_with_acorn
  s02_stand_with_acorn --> s02_place_acorn
  s02_place_acorn --> s03_two_paths
  s03_two_paths --> s03_decides
  s03_decides --> s04_shortcut_run
  s04_shortcut_run --> s05_leo_sleeps
  s05_leo_sleeps --> s05_paw_contact
  s05_paw_contact --> s05_nose_aftermath
  s05_nose_aftermath --> s06_barrier
  s06_barrier --> s07_leo_annoyed
  s07_leo_annoyed --> s07_milo_sorry
  s07_milo_sorry --> s08_leo_softens
  s08_leo_softens --> s08_milo_surprised
  s08_milo_surprised --> s08_kindness
  s08_kindness --> s09_milo_hurries
  s09_milo_hurries --> s09_stars
  s09_stars --> s09_home
  s09_home --> s10_curious_step
  s10_curious_step --> s10_net_falls
  s10_net_falls --> s11_pull_once
  s11_pull_once --> s11_why_wont_it_break
  s11_why_wont_it_break --> s11_call
  s11_call --> s11_waits
  s11_waits --> s12_hears
  s12_hears --> s12_runs
  s12_runs --> s13_arrives
  s13_arrives --> s13_milo_confident
  s13_milo_confident --> s13_leo_doubtful
  s13_leo_doubtful --> s13_milo_playful
  s13_milo_playful --> s14_gnaw_fray
  s14_gnaw_fray --> s14_sever_R01
  s14_sever_R01 --> s14_milo_clear
  s14_milo_clear --> s14_opening
  s14_opening --> s14_step_clear
  s14_step_clear --> s14_free_hold
  s14_free_hold --> s15_leo_amazed
  s15_leo_amazed --> s15_milo_modest
  s15_milo_modest --> s15_leo_reflects
  s15_leo_reflects --> s15_milo_sincere
  s15_milo_sincere --> s16_friends
  classDef closeup fill:#ffe0b2,stroke:#e65100,color:#000
  classDef two fill:#fff9c4,stroke:#f9a825,color:#000
  classDef wide fill:#c8e6c9,stroke:#2e7d32,color:#000
  classDef plate fill:#e0e0e0,stroke:#616161,color:#000
```

Orange = character close-up with blurred background; yellow = close two-shot; green = wide scene with whole bodies; grey = background only.

| # | From → to | Framing |
|---|---|---|
| 1 | `s01_explores` → `s01_acorn` | wide scene |
| 2 | `s01_acorn` → `s02_notice` | wide scene |
| 3 | `s02_notice` → `s02_stand_with_acorn` | wide scene |
| 4 | `s02_stand_with_acorn` → `s02_place_acorn` | wide scene |
| 5 | `s02_place_acorn` → `s03_two_paths` | wide scene |
| 6 | `s03_two_paths` → `s03_decides` | wide scene |
| 7 | `s03_decides` → `s04_shortcut_run` | close-up, blurred bg |
| 8 | `s04_shortcut_run` → `s05_leo_sleeps` | wide scene |
| 9 | `s05_leo_sleeps` → `s05_paw_contact` | wide scene |
| 10 | `s05_paw_contact` → `s05_nose_aftermath` | wide scene |
| 11 | `s05_nose_aftermath` → `s06_barrier` | close two-shot |
| 12 | `s06_barrier` → `s07_leo_annoyed` | wide scene |
| 13 | `s07_leo_annoyed` → `s07_milo_sorry` | close-up, blurred bg |
| 14 | `s07_milo_sorry` → `s08_leo_softens` | close-up, blurred bg |
| 15 | `s08_leo_softens` → `s08_milo_surprised` | close-up, blurred bg |
| 16 | `s08_milo_surprised` → `s08_kindness` | close-up, blurred bg |
| 17 | `s08_kindness` → `s09_milo_hurries` | wide scene |
| 18 | `s09_milo_hurries` → `s09_stars` | wide scene |
| 19 | `s09_stars` → `s09_home` | plate only |
| 20 | `s09_home` → `s10_curious_step` | wide scene |
| 21 | `s10_curious_step` → `s10_net_falls` | wide scene |
| 22 | `s10_net_falls` → `s11_pull_once` | wide scene |
| 23 | `s11_pull_once` → `s11_why_wont_it_break` | wide scene |
| 24 | `s11_why_wont_it_break` → `s11_call` | close-up, blurred bg |
| 25 | `s11_call` → `s11_waits` | close-up, blurred bg |
| 26 | `s11_waits` → `s12_hears` | wide scene |
| 27 | `s12_hears` → `s12_runs` | wide scene |
| 28 | `s12_runs` → `s13_arrives` | wide scene |
| 29 | `s13_arrives` → `s13_milo_confident` | wide scene |
| 30 | `s13_milo_confident` → `s13_leo_doubtful` | close-up, blurred bg |
| 31 | `s13_leo_doubtful` → `s13_milo_playful` | close-up, blurred bg |
| 32 | `s13_milo_playful` → `s14_gnaw_fray` | close-up, blurred bg |
| 33 | `s14_gnaw_fray` → `s14_sever_R01` | close two-shot |
| 34 | `s14_sever_R01` → `s14_milo_clear` | close two-shot |
| 35 | `s14_milo_clear` → `s14_opening` | wide scene |
| 36 | `s14_opening` → `s14_step_clear` | wide scene |
| 37 | `s14_step_clear` → `s14_free_hold` | wide scene |
| 38 | `s14_free_hold` → `s15_leo_amazed` | wide scene |
| 39 | `s15_leo_amazed` → `s15_milo_modest` | close-up, blurred bg |
| 40 | `s15_milo_modest` → `s15_leo_reflects` | close-up, blurred bg |
| 41 | `s15_leo_reflects` → `s15_milo_sincere` | close-up, blurred bg |
| 42 | `s15_milo_sincere` → `s16_friends` | close-up, blurred bg |
| 43 | `s16_friends` → end | wide scene |

## Scene keyframes (start and end of each shot)

| Shot | Start | End | Framing | Revision · status | Model | Keep | Owner notes |
|---|---|---|---|---|---|---|---|
| `s01_explores` | <img src="../../character/characters/interactions/v4/keyframes/s01_explores_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s01_explores_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s01_acorn` | <img src="../../character/characters/interactions/v4/keyframes/s01_acorn_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s01_acorn_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s02_notice` | <img src="../../character/characters/interactions/v4/keyframes/s02_notice_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s02_notice_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s02_stand_with_acorn` | <img src="../../character/characters/interactions/v4/keyframes/s02_stand_with_acorn_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s02_stand_with_acorn_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s02_place_acorn` | <img src="../../character/characters/interactions/v4/keyframes/s02_place_acorn_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s02_place_acorn_end_r02.png" width="220"> | wide scene | r01 · accepted / r02 · pending review | GPT image_gen / Nano Banana 2 |  |  |
| `s03_two_paths` | <img src="../../character/characters/interactions/v4/keyframes/s03_two_paths_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s03_two_paths_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s03_decides` | <img src="../../character/characters/interactions/v4/keyframes/s03_decides_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s03_decides_end_r01.png" width="220"> | close-up, blurred bg | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s04_shortcut_run` | <img src="../../character/characters/interactions/v4/keyframes/s04_shortcut_run_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s04_shortcut_run_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s05_leo_sleeps` | <img src="../../character/characters/interactions/v4/keyframes/s05_leo_sleeps_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s05_leo_sleeps_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s05_paw_contact` | <img src="../../character/characters/interactions/v4/keyframes/s05_paw_contact_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s05_paw_contact_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s05_nose_aftermath` | <img src="../../character/characters/interactions/v4/keyframes/s05_nose_aftermath_start_r05.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s05_nose_aftermath_end_r05.png" width="220"> | close two-shot | r05 · pending review / r05 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s06_barrier` | <img src="../../character/characters/interactions/v4/keyframes/s06_barrier_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s06_barrier_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s07_leo_annoyed` | <img src="../../character/characters/interactions/v4/keyframes/s07_leo_annoyed_start_r05.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s07_leo_annoyed_end_r05.png" width="220"> | close-up, blurred bg | r05 · pending review / r05 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s07_milo_sorry` | <img src="../../character/characters/interactions/v4/keyframes/s07_milo_sorry_start_r05.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s07_milo_sorry_end_r05.png" width="220"> | close-up, blurred bg | r05 · pending review / r05 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s08_leo_softens` | <img src="../../character/characters/interactions/v4/keyframes/s08_leo_softens_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s08_leo_softens_end_r01.png" width="220"> | close-up, blurred bg | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s08_milo_surprised` | <img src="../../character/characters/interactions/v4/keyframes/s08_milo_surprised_start_r04.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s08_milo_surprised_end_r04.png" width="220"> | close-up, blurred bg | r04 · pending review / r04 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s08_kindness` | <img src="../../character/characters/interactions/v4/keyframes/s08_kindness_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s08_kindness_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s09_milo_hurries` | <img src="../../character/characters/interactions/v4/keyframes/s09_milo_hurries_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s09_milo_hurries_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s09_stars` | <img src="../../character/characters/interactions/v4/keyframes/s09_stars_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s09_stars_end_r01.png" width="220"> | plate only | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s09_home` | <img src="../../character/characters/interactions/v4/keyframes/s09_home_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s09_home_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s10_curious_step` | <img src="../../character/characters/interactions/v4/keyframes/s10_curious_step_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s10_curious_step_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana Pro / Nano Banana 2 |  |  |
| `s10_net_falls` | <img src="../../character/characters/interactions/v4/keyframes/s10_net_falls_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s10_net_falls_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s11_pull_once` | <img src="../../character/characters/interactions/v4/keyframes/s11_pull_once_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s11_pull_once_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s11_why_wont_it_break` | <img src="../../character/characters/interactions/v4/keyframes/s11_why_wont_it_break_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s11_why_wont_it_break_end_r02.png" width="220"> | close-up, blurred bg | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s11_call` | <img src="../../character/characters/interactions/v4/keyframes/s11_call_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s11_call_end_r02.png" width="220"> | close-up, blurred bg | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s11_waits` | <img src="../../character/characters/interactions/v4/keyframes/s11_waits_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s11_waits_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s12_hears` | <img src="../../character/characters/interactions/v4/keyframes/s12_hears_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s12_hears_end_r02.png" width="220"> | wide scene | r01 · accepted / r02 · pending review | GPT image_gen / Nano Banana 2 |  |  |
| `s12_runs` | <img src="../../character/characters/interactions/v4/keyframes/s12_runs_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s12_runs_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s13_arrives` | <img src="../../character/characters/interactions/v4/keyframes/s13_arrives_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s13_arrives_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s13_milo_confident` | <img src="../../character/characters/interactions/v4/keyframes/s13_milo_confident_start_r04.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s13_milo_confident_end_r04.png" width="220"> | close-up, blurred bg | r04 · pending review / r04 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s13_leo_doubtful` | <img src="../../character/characters/interactions/v4/keyframes/s13_leo_doubtful_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s13_leo_doubtful_end_r02.png" width="220"> | close-up, blurred bg | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s13_milo_playful` | <img src="../../character/characters/interactions/v4/keyframes/s13_milo_playful_start_r04.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s13_milo_playful_end_r04.png" width="220"> | close-up, blurred bg | r04 · pending review / r04 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s14_gnaw_fray` | <img src="../../character/characters/interactions/v4/keyframes/s14_gnaw_fray_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s14_gnaw_fray_end_r02.png" width="220"> | close two-shot | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s14_sever_R01` | <img src="../../character/characters/interactions/v4/keyframes/s14_sever_R01_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s14_sever_R01_end_r02.png" width="220"> | close two-shot | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s14_milo_clear` | <img src="../../character/characters/interactions/v4/keyframes/s14_milo_clear_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s14_milo_clear_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s14_opening` | <img src="../../character/characters/interactions/v4/keyframes/s14_opening_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s14_opening_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s14_step_clear` | <img src="../../character/characters/interactions/v4/keyframes/s14_step_clear_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s14_step_clear_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s14_free_hold` | <img src="../../character/characters/interactions/v4/keyframes/s14_free_hold_start_r02.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s14_free_hold_end_r02.png" width="220"> | wide scene | r02 · pending review / r02 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s15_leo_amazed` | <img src="../../character/characters/interactions/v4/keyframes/s15_leo_amazed_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s15_leo_amazed_end_r01.png" width="220"> | close-up, blurred bg | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s15_milo_modest` | <img src="../../character/characters/interactions/v4/keyframes/s15_milo_modest_start_r04.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s15_milo_modest_end_r04.png" width="220"> | close-up, blurred bg | r04 · pending review / r04 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s15_leo_reflects` | <img src="../../character/characters/interactions/v4/keyframes/s15_leo_reflects_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s15_leo_reflects_end_r01.png" width="220"> | close-up, blurred bg | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |
| `s15_milo_sincere` | <img src="../../character/characters/interactions/v4/keyframes/s15_milo_sincere_start_r04.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s15_milo_sincere_end_r04.png" width="220"> | close-up, blurred bg | r04 · pending review / r04 · pending review | Nano Banana 2 / Nano Banana 2 |  |  |
| `s16_friends` | <img src="../../character/characters/interactions/v4/keyframes/s16_friends_start_r01.png" width="220"> | <img src="../../character/characters/interactions/v4/keyframes/s16_friends_end_r01.png" width="220"> | wide scene | r01 · accepted / r01 · accepted | GPT image_gen / GPT image_gen |  |  |

## Character references, plates and props

| Record | Image | Purpose | Revision · status | Model | Keep | Owner notes |
|---|---|---|---|---|---|---|
| `MILO_CANON` | <img src="../../character/characters/Milo/v4/canonical/full-body_milo_neutral_pose_r01.png" width="160"> | Approve the v4 neutral canonical before any derivatives | r01 · accepted | GPT image_gen |  |  |
| `LEO_CANON` | <img src="../../character/characters/Leo/v4/canonical/full-body_leo_neutral_pose_r01.png" width="160"> | Approve the v4 neutral canonical before any derivatives | r01 · accepted | GPT image_gen |  |  |
| `M_SIDE_R` | <img src="../../character/characters/Milo/v4/references/m_side_r_r01.png" width="160"> | Full body side view facing screen-right; neutral upright bipedal stance, mouth closed. | r01 · accepted | GPT image_gen |  |  |
| `M_SIDE_L` | <img src="../../character/characters/Milo/v4/references/m_side_l_r01.png" width="160"> | Full body side view facing screen-left, matching the approved right view anatomical scale; | r01 · accepted | GPT image_gen |  |  |
| `M_BACK` | <img src="../../character/characters/Milo/v4/references/m_back_r01.png" width="160"> | Full body rear three-quarter view showing the single tail root, slim back and both round e | r01 · accepted | GPT image_gen |  |  |
| `L_SIDE_R` | <img src="../../character/characters/Leo/v4/references/l_side_r_r01.png" width="160"> | Full body right-facing side view, all four paws, mane volume and whole single tail visible | r01 · accepted | GPT image_gen |  |  |
| `L_BACK` | <img src="../../character/characters/Leo/v4/references/l_back_r01.png" width="160"> | Full body rear three-quarter view with one tail root, four legs and the same large mane. | r01 · accepted | GPT image_gen |  |  |
| `M_CLOSED` | <img src="../../character/characters/Milo/v4/references/m_closed_r01.png" width="160"> | Head-and-shoulders reference, neutral closed smile, arms lowered and tail below the crop.  | r01 · accepted | GPT image_gen |  |  |
| `M_SMALL` | <img src="../../character/characters/Milo/v4/references/m_small_r01.png" width="160"> | Exactly the approved M_CLOSED portrait framing; lips slightly parted, small rounded dark w | r01 · accepted | GPT image_gen |  |  |
| `M_OPEN` | <img src="../../character/characters/Milo/v4/references/m_open_r01.png" width="160"> | Exactly the approved M_CLOSED portrait framing; moderate rounded mouth opening, same inter | r01 · accepted | GPT image_gen |  |  |
| `M_GNAW` | <img src="../../character/characters/Milo/v4/references/m_gnaw_r01.png" width="160"> | Matched close view of muzzle, two lowered holding paws and one cream braided rope. Draft m | r01 · accepted | GPT image_gen |  |  |
| `L_CLOSED` | <img src="../../character/characters/Leo/v4/references/l_closed_r01.png" width="160"> | Head-and-shoulders reference, neutral closed smile, paws/tail below the crop; whole mane w | r01 · accepted | GPT image_gen |  |  |
| `L_SMALL` | <img src="../../character/characters/Leo/v4/references/l_small_r01.png" width="160"> | Exactly the L_CLOSED portrait; lips slightly parted, rounded dark warm mouth interior, tin | r01 · accepted | GPT image_gen |  |  |
| `L_OPEN` | <img src="../../character/characters/Leo/v4/references/l_open_r01.png" width="160"> | Exactly the L_CLOSED portrait; moderate rounded opening for gentle speech/call, same inter | r01 · accepted | GPT image_gen |  |  |
| `L_ASLEEP` | <img src="../../character/characters/Leo/v4/references/l_asleep_r01.png" width="160"> | Full body lying asleep in three-quarter view, one front paw extended and planted flat, the | r01 · accepted | GPT image_gen |  |  |
| `L_WAKE` | <img src="../../character/characters/Leo/v4/references/l_wake_r01.png" width="160"> | Local eye/expression edit of L_ASLEEP: same lying body, paws, mane, camera and head size;  | r01 · accepted | GPT image_gen |  |  |
| `M_RUN_R` | <img src="../../character/characters/Milo/v4/references/m_run_r_r01.png" width="160"> | Full body genuine running pose, side view facing right, upright torso and slim legs in a m | r01 · accepted | GPT image_gen |  |  |
| `M_RUN_L` | <img src="../../character/characters/Milo/v4/references/m_run_l_r01.png" width="160"> | Full body genuine running pose facing left, same upright anatomy and gait as M_RUN_R, sing | r01 · accepted | GPT image_gen |  |  |
| `M_SIT_ACORN` | <img src="../../character/characters/Milo/v4/references/m_sit_acorn_r01.png" width="160"> | Milo sits upright holding exactly one small felt acorn in both paws just below his mouth.  | r01 · accepted | GPT image_gen |  |  |
| `M_STAND_ACORN` | <img src="../../character/characters/Milo/v4/references/m_stand_acorn_r01.png" width="160"> | Milo stands holding the same single acorn at chest level with both paws. Register the head | r01 · accepted | GPT image_gen |  |  |
| `PL_stream_afternoon` | <img src="../../character/locations/v4/stream_bank/stream_afternoon_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_stream_sunset` | <img src="../../character/locations/v4/stream_bank/stream_sunset_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_fork_sunset` | <img src="../../character/locations/v4/fork/fork_sunset_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_shortcut_dusk` | <img src="../../character/locations/v4/shortcut/shortcut_dusk_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_tree_dusk` | <img src="../../character/locations/v4/great_tree/tree_dusk_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_tree_day` | <img src="../../character/locations/v4/great_tree/tree_day_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_tree_sky` | <img src="../../character/locations/v4/great_tree/tree_sky_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_home_night` | <img src="../../character/locations/v4/milo_home/home_night_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_trap_morning` | <img src="../../character/locations/v4/trap_path/trap_morning_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PL_run_morning` | <img src="../../character/locations/v4/forest_run/run_morning_r01.png" width="160"> | Approve empty location plate and camera/light geometry | r01 · accepted | GPT image_gen |  |  |
| `PROP_ACORN` | <img src="../../character/locations/v4/props/prop_acorn_r01.png" width="160"> | Freeze prop material and proportions | r01 · accepted | GPT image_gen |  |  |
| `PROP_NET` | <img src="../../character/locations/v4/props/prop_net_r01.png" width="160"> | Freeze prop material and proportions | r01 · accepted | GPT image_gen |  |  |

## Expression references

| Record | Image | Purpose | Revision · status | Model | Keep | Owner notes |
|---|---|---|---|---|---|---|
| `M_EXPR_APOLOGETIC` | <img src="../../character/characters/Milo/v4/expressions/m_expr_apologetic_r01.png" width="160"> | Milo expression reference 'apologetic': same head-and-shoulders crop, studio and identity  | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_CALM_CONFIDENT` | <img src="../../character/characters/Milo/v4/expressions/m_expr_calm_confident_r01.png" width="160"> | Milo expression reference 'calm_confident': same head-and-shoulders crop, studio and ident | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_CONCERNED` | <img src="../../character/characters/Milo/v4/expressions/m_expr_concerned_r01.png" width="160"> | Milo expression reference 'concerned': same head-and-shoulders crop, studio and identity a | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_CONFIDENT` | <img src="../../character/characters/Milo/v4/expressions/m_expr_confident_r01.png" width="160"> | Milo expression reference 'confident': same head-and-shoulders crop, studio and identity a | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_CURIOUS` | <img src="../../character/characters/Milo/v4/expressions/m_expr_curious_r01.png" width="160"> | Milo expression reference 'curious': same head-and-shoulders crop, studio and identity as  | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_NEUTRAL` | <img src="../../character/characters/Milo/v4/expressions/m_expr_neutral_r01.png" width="160"> | Milo expression reference 'neutral': same head-and-shoulders crop, studio and identity as  | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_PLAYFUL` | <img src="../../character/characters/Milo/v4/expressions/m_expr_playful_r01.png" width="160"> | Milo expression reference 'playful': same head-and-shoulders crop, studio and identity as  | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_PLEASANT_SURPRISE` | <img src="../../character/characters/Milo/v4/expressions/m_expr_pleasant_surprise_r01.png" width="160"> | Milo expression reference 'pleasant_surprise': same head-and-shoulders crop, studio and id | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_RELIEVED_PROUD` | <img src="../../character/characters/Milo/v4/expressions/m_expr_relieved-proud_r01.png" width="160"> | Milo expression reference 'relieved-proud': same head-and-shoulders crop, studio and ident | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_SMILE` | <img src="../../character/characters/Milo/v4/expressions/m_expr_smile_r01.png" width="160"> | Milo expression reference 'smile': same head-and-shoulders crop, studio and identity as M_ | r01 · pending review | NB2 Lite |  |  |
| `M_EXPR_STARTLED` | <img src="../../character/characters/Milo/v4/expressions/m_expr_startled_r01.png" width="160"> | Milo expression reference 'startled': same head-and-shoulders crop, studio and identity as | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_ANNOYED` | <img src="../../character/characters/Leo/v4/expressions/l_expr_annoyed_r01.png" width="160"> | Leo expression reference 'annoyed': same head-and-shoulders crop, studio and identity as L | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_CONCERNED` | <img src="../../character/characters/Leo/v4/expressions/l_expr_concerned_r01.png" width="160"> | Leo expression reference 'concerned': same head-and-shoulders crop, studio and identity as | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_CONFIDENT` | <img src="../../character/characters/Leo/v4/expressions/l_expr_confident_r01.png" width="160"> | Leo expression reference 'confident': same head-and-shoulders crop, studio and identity as | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_CURIOUS` | <img src="../../character/characters/Leo/v4/expressions/l_expr_curious_r01.png" width="160"> | Leo expression reference 'curious': same head-and-shoulders crop, studio and identity as L | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_DOUBTFUL` | <img src="../../character/characters/Leo/v4/expressions/l_expr_doubtful_r01.png" width="160"> | Leo expression reference 'doubtful': same head-and-shoulders crop, studio and identity as  | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_GRATEFUL` | <img src="../../character/characters/Leo/v4/expressions/l_expr_grateful_r01.png" width="160"> | Leo expression reference 'grateful': same head-and-shoulders crop, studio and identity as  | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_NEUTRAL` | <img src="../../character/characters/Leo/v4/expressions/l_expr_neutral_r01.png" width="160"> | Leo expression reference 'neutral': same head-and-shoulders crop, studio and identity as L | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_PLEASANT_SURPRISE` | <img src="../../character/characters/Leo/v4/expressions/l_expr_pleasant_surprise_r01.png" width="160"> | Leo expression reference 'pleasant_surprise': same head-and-shoulders crop, studio and ide | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_REFLECTIVE` | <img src="../../character/characters/Leo/v4/expressions/l_expr_reflective_r01.png" width="160"> | Leo expression reference 'reflective': same head-and-shoulders crop, studio and identity a | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_RELIEVED_PROUD` | <img src="../../character/characters/Leo/v4/expressions/l_expr_relieved-proud_r01.png" width="160"> | Leo expression reference 'relieved-proud': same head-and-shoulders crop, studio and identi | r01 · pending review | NB2 Lite |  |  |
| `L_EXPR_SMILE` | <img src="../../character/characters/Leo/v4/expressions/l_expr_smile_r01.png" width="160"> | Leo expression reference 'smile': same head-and-shoulders crop, studio and identity as L_C | r01 · pending review | NB2 Lite |  |  |
