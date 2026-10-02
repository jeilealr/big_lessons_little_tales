# lion_and_mouse_v4: image review

Every image of this version, generated from `prompt_manifest.json` by `python3 production/image_review_md.py`. Mark each file `yes` or `no` in the last table; rerunning the script keeps your answers. Framing follows `docs/creation-rules.md` CR-15.

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

## Keep or not

All 136 image files of this version, every revision. Write `yes` or `no` in **Keep**.

| Image file | Keep |
|---|---|
| [`full-body_leo_neutral_pose_r01.png`](../../character/characters/Leo/v4/canonical/full-body_leo_neutral_pose_r01.png) |  |
| [`l_expr_annoyed_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_annoyed_r01.png) |  |
| [`l_expr_concerned_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_concerned_r01.png) |  |
| [`l_expr_confident_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_confident_r01.png) |  |
| [`l_expr_curious_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_curious_r01.png) |  |
| [`l_expr_doubtful_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_doubtful_r01.png) |  |
| [`l_expr_grateful_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_grateful_r01.png) |  |
| [`l_expr_neutral_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_neutral_r01.png) |  |
| [`l_expr_pleasant_surprise_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_pleasant_surprise_r01.png) |  |
| [`l_expr_reflective_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_reflective_r01.png) |  |
| [`l_expr_relieved-proud_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_relieved-proud_r01.png) |  |
| [`l_expr_smile_r01.png`](../../character/characters/Leo/v4/expressions/l_expr_smile_r01.png) |  |
| [`l_asleep_r01.png`](../../character/characters/Leo/v4/references/l_asleep_r01.png) |  |
| [`l_back_r01.png`](../../character/characters/Leo/v4/references/l_back_r01.png) |  |
| [`l_closed_r01.png`](../../character/characters/Leo/v4/references/l_closed_r01.png) |  |
| [`l_open_r01.png`](../../character/characters/Leo/v4/references/l_open_r01.png) |  |
| [`l_side_r_r01.png`](../../character/characters/Leo/v4/references/l_side_r_r01.png) |  |
| [`l_small_r01.png`](../../character/characters/Leo/v4/references/l_small_r01.png) |  |
| [`l_wake_r01.png`](../../character/characters/Leo/v4/references/l_wake_r01.png) |  |
| [`full-body_milo_neutral_pose_r01.png`](../../character/characters/Milo/v4/canonical/full-body_milo_neutral_pose_r01.png) |  |
| [`m_expr_apologetic_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_apologetic_r01.png) |  |
| [`m_expr_calm_confident_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_calm_confident_r01.png) |  |
| [`m_expr_concerned_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_concerned_r01.png) |  |
| [`m_expr_confident_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_confident_r01.png) |  |
| [`m_expr_curious_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_curious_r01.png) |  |
| [`m_expr_neutral_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_neutral_r01.png) |  |
| [`m_expr_playful_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_playful_r01.png) |  |
| [`m_expr_pleasant_surprise_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_pleasant_surprise_r01.png) |  |
| [`m_expr_relieved-proud_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_relieved-proud_r01.png) |  |
| [`m_expr_smile_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_smile_r01.png) |  |
| [`m_expr_startled_r01.png`](../../character/characters/Milo/v4/expressions/m_expr_startled_r01.png) |  |
| [`m_back_r01.png`](../../character/characters/Milo/v4/references/m_back_r01.png) |  |
| [`m_closed_r01.png`](../../character/characters/Milo/v4/references/m_closed_r01.png) |  |
| [`m_gnaw_r01.png`](../../character/characters/Milo/v4/references/m_gnaw_r01.png) |  |
| [`m_open_r01.png`](../../character/characters/Milo/v4/references/m_open_r01.png) |  |
| [`m_run_l_r01.png`](../../character/characters/Milo/v4/references/m_run_l_r01.png) |  |
| [`m_run_r_r01.png`](../../character/characters/Milo/v4/references/m_run_r_r01.png) |  |
| [`m_side_l_r01.png`](../../character/characters/Milo/v4/references/m_side_l_r01.png) |  |
| [`m_side_r_r01.png`](../../character/characters/Milo/v4/references/m_side_r_r01.png) |  |
| [`m_sit_acorn_r01.png`](../../character/characters/Milo/v4/references/m_sit_acorn_r01.png) |  |
| [`m_small_r01.png`](../../character/characters/Milo/v4/references/m_small_r01.png) |  |
| [`m_stand_acorn_r01.png`](../../character/characters/Milo/v4/references/m_stand_acorn_r01.png) |  |
| [`s01_acorn_end_r01.png`](../../character/characters/interactions/v4/keyframes/s01_acorn_end_r01.png) |  |
| [`s01_acorn_start_r01.png`](../../character/characters/interactions/v4/keyframes/s01_acorn_start_r01.png) |  |
| [`s01_explores_end_r01.png`](../../character/characters/interactions/v4/keyframes/s01_explores_end_r01.png) |  |
| [`s01_explores_start_r01.png`](../../character/characters/interactions/v4/keyframes/s01_explores_start_r01.png) |  |
| [`s02_notice_end_r01.png`](../../character/characters/interactions/v4/keyframes/s02_notice_end_r01.png) |  |
| [`s02_notice_start_r01.png`](../../character/characters/interactions/v4/keyframes/s02_notice_start_r01.png) |  |
| [`s02_place_acorn_end_r01.png`](../../character/characters/interactions/v4/keyframes/s02_place_acorn_end_r01.png) |  |
| [`s02_place_acorn_start_r01.png`](../../character/characters/interactions/v4/keyframes/s02_place_acorn_start_r01.png) |  |
| [`s02_stand_with_acorn_end_r01.png`](../../character/characters/interactions/v4/keyframes/s02_stand_with_acorn_end_r01.png) |  |
| [`s02_stand_with_acorn_start_r01.png`](../../character/characters/interactions/v4/keyframes/s02_stand_with_acorn_start_r01.png) |  |
| [`s03_decides_end_r01.png`](../../character/characters/interactions/v4/keyframes/s03_decides_end_r01.png) |  |
| [`s03_decides_start_r01.png`](../../character/characters/interactions/v4/keyframes/s03_decides_start_r01.png) |  |
| [`s03_two_paths_end_r01.png`](../../character/characters/interactions/v4/keyframes/s03_two_paths_end_r01.png) |  |
| [`s03_two_paths_start_r01.png`](../../character/characters/interactions/v4/keyframes/s03_two_paths_start_r01.png) |  |
| [`s04_shortcut_run_end_r01.png`](../../character/characters/interactions/v4/keyframes/s04_shortcut_run_end_r01.png) |  |
| [`s04_shortcut_run_start_r01.png`](../../character/characters/interactions/v4/keyframes/s04_shortcut_run_start_r01.png) |  |
| [`s05_leo_sleeps_end_r01.png`](../../character/characters/interactions/v4/keyframes/s05_leo_sleeps_end_r01.png) |  |
| [`s05_leo_sleeps_start_r01.png`](../../character/characters/interactions/v4/keyframes/s05_leo_sleeps_start_r01.png) |  |
| [`s05_nose_aftermath_end_r05.png`](../../character/characters/interactions/v4/keyframes/s05_nose_aftermath_end_r05.png) |  |
| [`s05_nose_aftermath_start_r05.png`](../../character/characters/interactions/v4/keyframes/s05_nose_aftermath_start_r05.png) |  |
| [`s05_paw_contact_end_r01.png`](../../character/characters/interactions/v4/keyframes/s05_paw_contact_end_r01.png) |  |
| [`s05_paw_contact_start_r01.png`](../../character/characters/interactions/v4/keyframes/s05_paw_contact_start_r01.png) |  |
| [`s06_barrier_end_r01.png`](../../character/characters/interactions/v4/keyframes/s06_barrier_end_r01.png) |  |
| [`s06_barrier_start_r01.png`](../../character/characters/interactions/v4/keyframes/s06_barrier_start_r01.png) |  |
| [`s07_leo_annoyed_end_r05.png`](../../character/characters/interactions/v4/keyframes/s07_leo_annoyed_end_r05.png) |  |
| [`s07_leo_annoyed_start_r05.png`](../../character/characters/interactions/v4/keyframes/s07_leo_annoyed_start_r05.png) |  |
| [`s07_milo_sorry_end_r05.png`](../../character/characters/interactions/v4/keyframes/s07_milo_sorry_end_r05.png) |  |
| [`s07_milo_sorry_start_r05.png`](../../character/characters/interactions/v4/keyframes/s07_milo_sorry_start_r05.png) |  |
| [`s08_kindness_end_r01.png`](../../character/characters/interactions/v4/keyframes/s08_kindness_end_r01.png) |  |
| [`s08_kindness_start_r01.png`](../../character/characters/interactions/v4/keyframes/s08_kindness_start_r01.png) |  |
| [`s09_home_end_r01.png`](../../character/characters/interactions/v4/keyframes/s09_home_end_r01.png) |  |
| [`s09_home_start_r01.png`](../../character/characters/interactions/v4/keyframes/s09_home_start_r01.png) |  |
| [`s09_milo_hurries_end_r01.png`](../../character/characters/interactions/v4/keyframes/s09_milo_hurries_end_r01.png) |  |
| [`s09_milo_hurries_start_r01.png`](../../character/characters/interactions/v4/keyframes/s09_milo_hurries_start_r01.png) |  |
| [`s09_stars_end_r01.png`](../../character/characters/interactions/v4/keyframes/s09_stars_end_r01.png) |  |
| [`s09_stars_start_r01.png`](../../character/characters/interactions/v4/keyframes/s09_stars_start_r01.png) |  |
| [`s10_curious_step_end_r02.png`](../../character/characters/interactions/v4/keyframes/s10_curious_step_end_r02.png) |  |
| [`s10_curious_step_start_r02.png`](../../character/characters/interactions/v4/keyframes/s10_curious_step_start_r02.png) |  |
| [`s10_net_falls_end_r02.png`](../../character/characters/interactions/v4/keyframes/s10_net_falls_end_r02.png) |  |
| [`s10_net_falls_start_r02.png`](../../character/characters/interactions/v4/keyframes/s10_net_falls_start_r02.png) |  |
| [`s11_call_end_r02.png`](../../character/characters/interactions/v4/keyframes/s11_call_end_r02.png) |  |
| [`s11_call_start_r02.png`](../../character/characters/interactions/v4/keyframes/s11_call_start_r02.png) |  |
| [`s11_pull_once_end_r02.png`](../../character/characters/interactions/v4/keyframes/s11_pull_once_end_r02.png) |  |
| [`s11_pull_once_start_r02.png`](../../character/characters/interactions/v4/keyframes/s11_pull_once_start_r02.png) |  |
| [`s11_waits_end_r02.png`](../../character/characters/interactions/v4/keyframes/s11_waits_end_r02.png) |  |
| [`s11_waits_start_r02.png`](../../character/characters/interactions/v4/keyframes/s11_waits_start_r02.png) |  |
| [`s11_why_wont_it_break_end_r02.png`](../../character/characters/interactions/v4/keyframes/s11_why_wont_it_break_end_r02.png) |  |
| [`s11_why_wont_it_break_start_r02.png`](../../character/characters/interactions/v4/keyframes/s11_why_wont_it_break_start_r02.png) |  |
| [`s12_hears_end_r02.png`](../../character/characters/interactions/v4/keyframes/s12_hears_end_r02.png) |  |
| [`s12_hears_start_r01.png`](../../character/characters/interactions/v4/keyframes/s12_hears_start_r01.png) |  |
| [`s12_runs_end_r01.png`](../../character/characters/interactions/v4/keyframes/s12_runs_end_r01.png) |  |
| [`s12_runs_start_r01.png`](../../character/characters/interactions/v4/keyframes/s12_runs_start_r01.png) |  |
| [`s13_arrives_end_r02.png`](../../character/characters/interactions/v4/keyframes/s13_arrives_end_r02.png) |  |
| [`s13_arrives_start_r02.png`](../../character/characters/interactions/v4/keyframes/s13_arrives_start_r02.png) |  |
| [`s13_leo_doubtful_end_r02.png`](../../character/characters/interactions/v4/keyframes/s13_leo_doubtful_end_r02.png) |  |
| [`s13_leo_doubtful_start_r02.png`](../../character/characters/interactions/v4/keyframes/s13_leo_doubtful_start_r02.png) |  |
| [`s13_milo_confident_end_r04.png`](../../character/characters/interactions/v4/keyframes/s13_milo_confident_end_r04.png) |  |
| [`s13_milo_confident_start_r04.png`](../../character/characters/interactions/v4/keyframes/s13_milo_confident_start_r04.png) |  |
| [`s13_milo_playful_end_r04.png`](../../character/characters/interactions/v4/keyframes/s13_milo_playful_end_r04.png) |  |
| [`s13_milo_playful_start_r04.png`](../../character/characters/interactions/v4/keyframes/s13_milo_playful_start_r04.png) |  |
| [`s14_free_hold_end_r02.png`](../../character/characters/interactions/v4/keyframes/s14_free_hold_end_r02.png) |  |
| [`s14_free_hold_start_r02.png`](../../character/characters/interactions/v4/keyframes/s14_free_hold_start_r02.png) |  |
| [`s14_gnaw_fray_end_r02.png`](../../character/characters/interactions/v4/keyframes/s14_gnaw_fray_end_r02.png) |  |
| [`s14_gnaw_fray_start_r02.png`](../../character/characters/interactions/v4/keyframes/s14_gnaw_fray_start_r02.png) |  |
| [`s14_milo_clear_end_r02.png`](../../character/characters/interactions/v4/keyframes/s14_milo_clear_end_r02.png) |  |
| [`s14_milo_clear_start_r02.png`](../../character/characters/interactions/v4/keyframes/s14_milo_clear_start_r02.png) |  |
| [`s14_opening_end_r02.png`](../../character/characters/interactions/v4/keyframes/s14_opening_end_r02.png) |  |
| [`s14_opening_start_r02.png`](../../character/characters/interactions/v4/keyframes/s14_opening_start_r02.png) |  |
| [`s14_sever_R01_end_r02.png`](../../character/characters/interactions/v4/keyframes/s14_sever_R01_end_r02.png) |  |
| [`s14_sever_R01_start_r02.png`](../../character/characters/interactions/v4/keyframes/s14_sever_R01_start_r02.png) |  |
| [`s14_step_clear_end_r02.png`](../../character/characters/interactions/v4/keyframes/s14_step_clear_end_r02.png) |  |
| [`s14_step_clear_start_r02.png`](../../character/characters/interactions/v4/keyframes/s14_step_clear_start_r02.png) |  |
| [`s15_leo_amazed_end_r01.png`](../../character/characters/interactions/v4/keyframes/s15_leo_amazed_end_r01.png) |  |
| [`s15_leo_amazed_start_r01.png`](../../character/characters/interactions/v4/keyframes/s15_leo_amazed_start_r01.png) |  |
| [`s15_leo_reflects_end_r01.png`](../../character/characters/interactions/v4/keyframes/s15_leo_reflects_end_r01.png) |  |
| [`s15_leo_reflects_start_r01.png`](../../character/characters/interactions/v4/keyframes/s15_leo_reflects_start_r01.png) |  |
| [`s15_milo_modest_end_r04.png`](../../character/characters/interactions/v4/keyframes/s15_milo_modest_end_r04.png) |  |
| [`s15_milo_modest_start_r04.png`](../../character/characters/interactions/v4/keyframes/s15_milo_modest_start_r04.png) |  |
| [`s15_milo_sincere_end_r04.png`](../../character/characters/interactions/v4/keyframes/s15_milo_sincere_end_r04.png) |  |
| [`s15_milo_sincere_start_r04.png`](../../character/characters/interactions/v4/keyframes/s15_milo_sincere_start_r04.png) |  |
| [`s16_friends_end_r01.png`](../../character/characters/interactions/v4/keyframes/s16_friends_end_r01.png) |  |
| [`s16_friends_start_r01.png`](../../character/characters/interactions/v4/keyframes/s16_friends_start_r01.png) |  |
| [`run_morning_r01.png`](../../character/locations/v4/forest_run/run_morning_r01.png) |  |
| [`fork_sunset_r01.png`](../../character/locations/v4/fork/fork_sunset_r01.png) |  |
| [`tree_day_r01.png`](../../character/locations/v4/great_tree/tree_day_r01.png) |  |
| [`tree_dusk_r01.png`](../../character/locations/v4/great_tree/tree_dusk_r01.png) |  |
| [`tree_sky_r01.png`](../../character/locations/v4/great_tree/tree_sky_r01.png) |  |
| [`home_night_r01.png`](../../character/locations/v4/milo_home/home_night_r01.png) |  |
| [`prop_acorn_r01.png`](../../character/locations/v4/props/prop_acorn_r01.png) |  |
| [`prop_net_r01.png`](../../character/locations/v4/props/prop_net_r01.png) |  |
| [`shortcut_dusk_r01.png`](../../character/locations/v4/shortcut/shortcut_dusk_r01.png) |  |
| [`stream_afternoon_r01.png`](../../character/locations/v4/stream_bank/stream_afternoon_r01.png) |  |
| [`stream_sunset_r01.png`](../../character/locations/v4/stream_bank/stream_sunset_r01.png) |  |
| [`trap_morning_r01.png`](../../character/locations/v4/trap_path/trap_morning_r01.png) |  |
