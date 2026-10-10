# Timing sheet: lion_and_mouse_v6 (en), chained coverage

This sheet retains the saved piece durations and recalculated frame counts for the independent v6 packet. Verify all durations against the v6-local narration on LUMI, then regenerate it with `production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v6 apply`. Every second of narration is covered by exactly one piece; nothing is held or stretched. A piece's clip is rendered at the frame count shown and retimed by the speed shown (RIFE in post). `chain` = starts on the previous piece's end image; `cut (...)` = a planned cut and its reason (CR-21).

## Summary

| Scene | Narration | Pieces | New renders | Reused | Speed range |
|---|---|---|---|---|---|
| 1 | 40.2 s | 8 | 8 | 0 | 0.96-0.99 |
| 2 | 24.4 s | 5 | 5 | 0 | 0.84-1.02 |
| 3 | 39.1 s | 10 | 10 | 0 | 0.85-1.14 |
| 4 | 15.0 s | 3 | 3 | 0 | 0.99-1.01 |
| 5 | 44.2 s | 9 | 9 | 0 | 0.83-1.04 |
| 6 | 36.8 s | 8 | 8 | 0 | 0.87-1.02 |
| 7 | 23.8 s | 5 | 5 | 0 | 0.88-1.00 |
| 8 | 83.4 s | 19 | 19 | 0 | 0.81-1.03 |
| 9 | 23.7 s | 5 | 5 | 0 | 0.93-1.02 |
| 10 | 24.0 s | 5 | 5 | 0 | 0.82-1.01 |
| 11 | 30.8 s | 8 | 8 | 0 | 0.90-1.03 |
| 12 | 32.1 s | 7 | 7 | 0 | 0.84-1.12 |
| 13 | 52.6 s | 13 | 13 | 0 | 0.85-1.09 |
| 14 | 53.6 s | 12 | 12 | 0 | 0.81-1.23 |
| 15 | 103.5 s | 24 | 24 | 0 | 0.81-1.04 |
| 16 | 56.7 s | 13 | 13 | 0 | 0.80-1.02 |
| **total** | **11:23.7** | 154 | 154 | 0 | |

## Scene 01 (0:00.0 - 0:40.2, 40.2 s, audio `scene01.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 0:00.0 | 4.87 s | `s01_stream_landscape` | cut (film_start, cut) | 77 | 0.99 | `stream_afternoon_r01.png` → `stream_afternoon_r01.png` | S01-L001 |
| 0:04.9 | 4.87 s | `s01_enter` | chain | 77 | 0.99 | `stream_afternoon_r01.png` → `s01_01_milo_at_edge_r01.png` | S01-L001 |
| 0:09.7 | 4.68 s | `s01_walk_on` | chain | 73 | 0.97 | `s01_01_milo_at_edge_r01.png` → `s01_01_explores_start_r01.png` | S01-L002 |
| 0:14.4 | 4.68 s | `s01_explores` | chain | 73 | 0.97 | `s01_01_explores_start_r01.png` → `s01_01_explores_end_r01.png` | S01-L002 |
| 0:19.1 | 5.25 s | `s01_to_stone` | chain | 81 | 0.96 | `s01_01_explores_end_r01.png` → `s01_04_milo_at_stone_r01.png` | S01-L003 |
| 0:24.4 | 5.28 s | `s01_takes_acorn` | chain | 81 | 0.96 | `s01_04_milo_at_stone_r01.png` → `s01_02_acorn_start_r01.png` | S01-L004 |
| 0:29.6 | 5.28 s | `s01_acorn` | chain | 81 | 0.96 | `s01_02_acorn_start_r01.png` → `s01_02_acorn_end_r01.png` | S01-L004 |
| 0:34.9 | 5.28 s | `s01_content` | chain | 81 | 0.96 | `s01_02_acorn_end_r01.png` → `s01_02_acorn_end_r01.png` | S01-L004 |

<details><summary>Lines</summary>

- `S01-L001` 0:00.0 (9.7 s incl. pause) **NARRATOR**: Once upon a time, at the edge of a wide and peaceful forest, there lived a little mouse who loved exploring.
- `S01-L002` 0:09.7 (9.4 s incl. pause) **NARRATOR**: The mouse knew every berry bush, every hollow log, and nearly every winding path beneath the trees.
- `S01-L003` 0:19.1 (5.2 s incl. pause) **NARRATOR**: One afternoon, the mouse wandered farther from home than usual.
- `S01-L004` 0:24.3 (15.8 s incl. pause) **NARRATOR**: There had been so many wonderful things to eat — tiny seeds beneath the tall grass, sweet berries beside the stream, and one particularly delicious acorn that took much longer to enjoy than expected.

</details>

## Scene 02 (0:40.2 - 1:04.6, 24.4 s, audio `scene02.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 0:40.2 | 3.83 s | `s02_sunset_hold` | cut (time_change, crossfade) | 61 | 1.00 | `s02_01_notice_start_r01.png` → `s02_01_notice_start_r01.png` | S02-L001 |
| 0:44.0 | 6.00 s | `s02_notice` | chain | 81 | 0.84 | `s02_01_notice_start_r01.png` → `s02_01_notice_end_r01.png` | S02-L001, S02-L002 |
| 0:50.0 | 4.71 s | `s02_oh_late` | chain | 77 | 1.02 | `s02_01_notice_end_r01.png` → `s02_02_stand_with_acorn_end_r01.png` | S02-L002, S02-L003 |
| 0:54.7 | 4.94 s | `s02_turn_to_stone` | chain | 81 | 1.02 | `s02_02_stand_with_acorn_end_r01.png` → `s02_03_place_acorn_start_r01.png` | S02-L004 |
| 0:59.7 | 4.94 s | `s02_place_acorn` | chain | 81 | 1.02 | `s02_03_place_acorn_start_r01.png` → `s02_05_place_acorn_end_r02.png` | S02-L004 |

<details><summary>Lines</summary>

- `S02-L001` 0:40.2 (7.7 s incl. pause) **NARRATOR**: By the time the mouse finally looked up, the golden afternoon light had begun to fade.
- `S02-L002` 0:47.8 (4.3 s incl. pause) **NARRATOR**: The shadows beneath the trees were growing longer.
- `S02-L003` 0:52.2 (2.5 s incl. pause) **MOUSE**: Oh! It's getting late!
- `S02-L004` 0:54.7 (9.9 s incl. pause) **NARRATOR**: Still holding the acorn, the mouse stood up. Then the little traveler set it carefully beside a stone at the stream.

</details>

## Scene 03 (1:04.6 - 1:43.7, 39.1 s, audio `scene03.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 1:04.6 | 3.49 s | `s03_fork_landscape` | cut (location_change, cut) | 57 | 1.02 | `fork_sunset_r01.png` → `fork_sunset_r01.png` | S03-L001 |
| 1:08.1 | 3.61 s | `s03_enter` | chain | 57 | 0.99 | `fork_sunset_r01.png` → `s03_01_milo_at_fork_edge_r01.png` | S03-L002 |
| 1:11.7 | 5.85 s | `s03_to_fork` | chain | 81 | 0.86 | `s03_01_milo_at_fork_edge_r01.png` → `s03_01_two_paths_start_r01.png` | S03-L003 |
| 1:17.5 | 5.96 s | `s03_two_paths` | chain | 81 | 0.85 | `s03_01_two_paths_start_r01.png` → `s03_01_two_paths_end_r01.png` | S03-L004, S03-L005 |
| 1:23.5 | 2.94 s | `s03_eyes_shortcut` | chain | 49 | 1.04 | `s03_01_two_paths_end_r01.png` → `s03_01_two_paths_end_r01.png` | S03-L005 |
| 1:26.5 | 3.49 s | `s03_sky` | chain | 57 | 1.02 | `s03_01_two_paths_end_r01.png` → `s03_04_milo_looks_up_r01.png` | S03-L006 |
| 1:29.9 | 2.69 s | `s03_long_path` | chain | 49 | 1.14 | `s03_04_milo_looks_up_r01.png` → `s03_01_two_paths_start_r01.png` | S03-L007 |
| 1:32.6 | 3.46 s | `s03_shortcut_again` | chain | 57 | 1.03 | `s03_01_two_paths_start_r01.png` → `s03_01_two_paths_end_r01.png` | S03-L008 |
| 1:36.1 | 3.69 s | `s03_says_shortcut` | cut (close_up, cut) | 61 | 1.03 | `s03_02_decides_start_r01.png` → `s03_02_decides_start_r01.png` | S03-L009 |
| 1:39.8 | 3.88 s | `s03_home_before_stars` | chain | 61 | 0.98 | `s03_02_decides_start_r01.png` → `s03_02_decides_end_r01.png` | S03-L010 |

<details><summary>Lines</summary>

- `S03-L001` 1:04.6 (3.5 s incl. pause) **NARRATOR**: Home was still quite a distance away.
- `S03-L002` 1:08.1 (3.6 s incl. pause) **NARRATOR**: There were two ways to get there.
- `S03-L003` 1:11.7 (5.8 s incl. pause) **NARRATOR**: One was the familiar path that curved safely around a sunny meadow.
- `S03-L004` 1:17.5 (3.0 s incl. pause) **NARRATOR**: The other was much shorter.
- `S03-L005` 1:20.6 (5.9 s incl. pause) **NARRATOR**: It cut straight through a quiet part of the forest that the mouse rarely visited.
- `S03-L006` 1:26.4 (3.5 s incl. pause) **NARRATOR**: The mouse looked at the darkening sky.
- `S03-L007` 1:29.9 (2.7 s incl. pause) **NARRATOR**: Then at the long path.
- `S03-L008` 1:32.6 (3.5 s incl. pause) **NARRATOR**: Then at the shortcut.
- `S03-L009` 1:36.1 (3.7 s incl. pause) **MOUSE**: The shortcut. Definitely the shortcut.
- `S03-L010` 1:39.8 (3.9 s incl. pause) **MOUSE**: I'll be home before the stars come out!

</details>

## Scene 04 (1:43.7 - 1:58.6, 15.0 s, audio `scene04.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 1:43.7 | 4.86 s | `s04_run_in` | cut (location_change, cut) | 77 | 0.99 | `shortcut_dusk_r01.png` → `s04_01_shortcut_run_start_r01.png` | S04-L001, S04-L002 |
| 1:48.5 | 5.10 s | `s04_shortcut_run` | chain | 81 | 0.99 | `s04_01_shortcut_run_start_r01.png` → `s04_01_shortcut_run_end_r01.png` | S04-L003, S04-L004 |
| 1:53.6 | 5.00 s | `s04_run_out` | chain | 81 | 1.01 | `s04_01_shortcut_run_end_r01.png` → `shortcut_dusk_r01.png` | S04-L005 |

<details><summary>Lines</summary>

- `S04-L001` 1:43.7 (2.4 s incl. pause) **NARRATOR**: And off the mouse hurried.
- `S04-L002` 1:46.0 (2.5 s incl. pause) **NARRATOR**: Past a mossy stone.
- `S04-L003` 1:48.5 (2.8 s incl. pause) **NARRATOR**: Under a fallen branch.
- `S04-L004` 1:51.3 (2.3 s incl. pause) **NARRATOR**: Around an old tree stump.
- `S04-L005` 1:53.6 (5.0 s incl. pause) **NARRATOR**: The mouse ran faster and faster, thinking only of getting home.

</details>

## Scene 05 (1:58.6 - 2:42.8, 44.2 s, audio `scene05.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 1:58.6 | 4.68 s | `s05_leo_sleeps` | cut (location_change, crossfade) | 73 | 0.97 | `s05_01_leo_sleeps_start_r01.png` → `s05_01_leo_sleeps_end_r01.png` | S05-L001 |
| 2:03.3 | 4.68 s | `s05_breathes` | chain | 73 | 0.97 | `s05_01_leo_sleeps_end_r01.png` → `s05_01_leo_sleeps_start_r01.png` | S05-L001 |
| 2:08.0 | 5.26 s | `s05_sleeping_face` | cut (close_up, cut) | 81 | 0.96 | `s05_03_leo_asleep_cu_r01.png` → `s05_03_leo_asleep_cu_r01.png` | S05-L002, S05-L003 |
| 2:13.2 | 5.89 s | `s05_milo_comes` | cut (close_up, cut) | 81 | 0.86 | `s05_01_leo_sleeps_start_r01.png` → `s05_02_paw_contact_start_r01.png` | S05-L004 |
| 2:19.1 | 5.21 s | `s05_paw_contact` | chain | 81 | 0.97 | `s05_02_paw_contact_start_r01.png` → `s05_02_paw_contact_end_r01.png` | S05-L005, S05-L006, S05-L007 |
| 2:24.3 | 5.72 s | `s05_tumble` | chain | 81 | 0.89 | `s05_02_paw_contact_end_r01.png` → `s05_06_milo_lands_wide_r01.png` | S05-L008, S05-L009 |
| 2:30.1 | 2.95 s | `s05_dazed` | cut (close_up, cut) | 49 | 1.04 | `s05_03_nose_aftermath_start_r05.png` → `s05_03_nose_aftermath_start_r05.png` | S05-L009 |
| 2:33.0 | 6.13 s | `s05_eyes_open` | chain | 81 | 0.83 | `s05_03_nose_aftermath_start_r05.png` → `s05_03_nose_aftermath_end_r05.png` | S05-L009, S05-L010 |
| 2:39.2 | 3.68 s | `s05_what_was_that` | chain | 57 | 0.97 | `s05_03_nose_aftermath_end_r05.png` → `s05_03_nose_aftermath_end_r05.png` | S05-L011 |

<details><summary>Lines</summary>

- `S05-L001` 1:58.6 (9.4 s incl. pause) **NARRATOR**: What the mouse did not notice was the enormous lion sleeping beneath a great old tree.
- `S05-L002` 2:08.0 (2.7 s incl. pause) **NARRATOR**: His mane rested against the grass.
- `S05-L003` 2:10.6 (2.6 s incl. pause) **NARRATOR**: His eyes were closed.
- `S05-L004` 2:13.2 (5.9 s incl. pause) **NARRATOR**: And one enormous paw stretched directly across the path.
- `S05-L005` 2:19.1 (2.1 s incl. pause) **NARRATOR**: The mouse rounded a root—
- `S05-L006` 2:21.3 (1.6 s incl. pause) **NARRATOR**: and—
- `S05-L007` 2:22.9 (1.5 s incl. pause) **MOUSE**: Whoa!
- `S05-L008` 2:24.3 (2.8 s incl. pause) **NARRATOR**: The mouse tripped over the lion's paw.
- `S05-L009` 2:27.1 (8.9 s incl. pause) **NARRATOR**: There was a tumble, a roll, and a very surprised little mouse landed right against the lion's enormous nose.
- `S05-L010` 2:36.0 (3.2 s incl. pause) **NARRATOR**: The lion's eyes opened.
- `S05-L011` 2:39.2 (3.7 s incl. pause) **LION**: What in the forest was THAT?

</details>

## Scene 06 (2:42.8 - 3:19.6, 36.8 s, audio `scene06.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 2:42.8 | 4.11 s | `s06_lifts_head` | chain | 65 | 0.99 | `s05_03_nose_aftermath_end_r05.png` → `s06_01_leo_head_up_r01.png` | S06-L001 |
| 2:46.9 | 4.11 s | `s06_wide_awake` | cut (close_up, cut) | 65 | 0.99 | `s06_01_barrier_start_r01.png` → `s06_01_barrier_start_r01.png` | S06-L001 |
| 2:51.0 | 5.25 s | `s06_barrier` | chain | 81 | 0.96 | `s06_01_barrier_start_r01.png` → `s06_01_barrier_end_r01.png` | S06-L002 |
| 2:56.3 | 5.25 s | `s06_blocked` | chain | 81 | 0.96 | `s06_01_barrier_end_r01.png` → `s06_01_barrier_end_r01.png` | S06-L002 |
| 3:01.5 | 3.33 s | `s06_froze` | cut (close_up, cut) | 53 | 0.99 | `s07_02_milo_sorry_start_r05.png` → `s07_02_milo_sorry_start_r05.png` | S06-L003 |
| 3:04.9 | 4.46 s | `s06_dusk_sky` | cut (camera_change, cut) | 73 | 1.02 | `tree_sky_r01.png` → `tree_sky_r01.png` | S06-L004 |
| 3:09.3 | 4.46 s | `s06_still_blocked` | cut (camera_change, cut) | 73 | 1.02 | `s06_01_barrier_end_r01.png` → `s06_01_barrier_end_r01.png` | S06-L004 |
| 3:13.8 | 5.80 s | `s06_leo_frowns` | cut (close_up, cut) | 81 | 0.87 | `s07_01_leo_annoyed_start_r05.png` → `s07_01_leo_annoyed_end_r05.png` | S06-L005 |

<details><summary>Lines</summary>

- `S06-L001` 2:42.8 (8.2 s incl. pause) **NARRATOR**: The lion lifted his head in surprise. The mouse scrambled down onto the path.
- `S06-L002` 2:51.0 (10.5 s incl. pause) **NARRATOR**: Before the mouse could scramble away, one enormous paw came down beside the tiny traveler, blocking the path.
- `S06-L003` 3:01.5 (3.3 s incl. pause) **NARRATOR**: The mouse froze.
- `S06-L004` 3:04.9 (8.9 s incl. pause) **NARRATOR**: Only moments earlier, getting home before dark had seemed like the biggest problem in the world.
- `S06-L005` 3:13.8 (5.8 s incl. pause) **NARRATOR**: Suddenly, it did not seem very important at all.

</details>

## Scene 07 (3:19.6 - 3:43.4, 23.8 s, audio `scene07.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 3:19.6 | 5.73 s | `s07_you_woke_me` | chain | 81 | 0.88 | `s07_01_leo_annoyed_end_r05.png` → `s07_01_leo_annoyed_end_r05.png` | S07-L001 |
| 3:25.3 | 5.14 s | `s07_why_racing` | chain | 81 | 0.98 | `s07_01_leo_annoyed_end_r05.png` → `s07_01_leo_annoyed_end_r05.png` | S07-L002 |
| 3:30.5 | 5.21 s | `s07_im_sorry` | cut (close_up, cut) | 81 | 0.97 | `s07_02_milo_sorry_start_r05.png` → `s07_02_milo_sorry_start_r05.png` | S07-L003 |
| 3:35.7 | 3.89 s | `s07_shortcut_home` | chain | 61 | 0.98 | `s07_02_milo_sorry_start_r05.png` → `s07_02_milo_sorry_end_r05.png` | S07-L004 |
| 3:39.6 | 3.80 s | `s07_promise` | chain | 61 | 1.00 | `s07_02_milo_sorry_end_r05.png` → `s07_02_milo_sorry_end_r05.png` | S07-L005 |

<details><summary>Lines</summary>

- `S07-L001` 3:19.6 (5.7 s incl. pause) **LION**: You woke me from the finest nap I've had all week.
- `S07-L002` 3:25.3 (5.1 s incl. pause) **LION**: Why were you racing through here without watching where you were going?
- `S07-L003` 3:30.5 (5.2 s incl. pause) **MOUSE**: I'm sorry! I was eating by the stream, and I didn't notice how late it had become.
- `S07-L004` 3:35.7 (3.9 s incl. pause) **MOUSE**: I took a shortcut because I wanted to get home before dark.
- `S07-L005` 3:39.6 (3.8 s incl. pause) **MOUSE**: I wasn't trying to disturb you. I promise.

</details>

## Scene 08 (3:43.4 - 5:06.7, 83.4 s, audio `scene08.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 3:43.4 | 5.54 s | `s08_looks_down` | cut (close_up, cut) | 81 | 0.91 | `s06_01_barrier_end_r01.png` → `s06_01_barrier_end_r01.png` | S08-L001, S08-L002 |
| 3:48.9 | 4.45 s | `s08_could_frighten` | cut (close_up, cut) | 73 | 1.02 | `s08_01_leo_softens_start_r01.png` → `s08_01_leo_softens_start_r01.png` | S08-L003 |
| 3:53.3 | 5.46 s | `s08_milo_trembles` | cut (close_up, cut) | 81 | 0.93 | `s07_02_milo_sorry_start_r05.png` → `s07_02_milo_sorry_start_r05.png` | S08-L004, S08-L005 |
| 3:58.8 | 5.85 s | `s08_strongest` | cut (close_up, cut) | 81 | 0.86 | `s06_01_barrier_end_r01.png` → `s06_01_barrier_end_r01.png` | S08-L005, S08-L006 |
| 4:04.7 | 2.96 s | `s08_did_not_mean` | cut (close_up, cut) | 49 | 1.03 | `s08_01_leo_softens_start_r01.png` → `s08_01_leo_softens_start_r01.png` | S08-L006 |
| 4:07.6 | 3.62 s | `s08_softened` | chain | 57 | 0.98 | `s08_01_leo_softens_start_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L007 |
| 4:11.2 | 5.38 s | `s08_well` | chain | 81 | 0.94 | `s08_01_leo_softens_end_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L008, S08-L009 |
| 4:16.6 | 3.37 s | `s08_go_home` | chain | 53 | 0.98 | `s08_01_leo_softens_end_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L010 |
| 4:20.0 | 3.94 s | `s08_look_where` | chain | 65 | 1.03 | `s08_01_leo_softens_end_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L011 |
| 4:23.9 | 3.82 s | `s08_letting_go` | cut (close_up, cut) | 61 | 1.00 | `s08_02_milo_surprised_start_r01.png` → `s08_02_milo_surprised_start_r01.png` | S08-L012 |
| 4:27.8 | 4.38 s | `s08_mistake` | cut (close_up, cut) | 69 | 0.98 | `s08_01_leo_softens_end_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L013, S08-L014 |
| 4:32.1 | 3.50 s | `s08_no_reason` | chain | 57 | 1.02 | `s08_01_leo_softens_end_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L015 |
| 4:35.6 | 3.77 s | `s08_stares` | cut (close_up, cut) | 61 | 1.01 | `s08_02_milo_surprised_start_r01.png` → `s08_02_milo_surprised_start_r01.png` | S08-L016 |
| 4:39.4 | 3.09 s | `s08_expected_anger` | cut (close_up, cut) | 49 | 0.99 | `s08_03_kindness_start_r01.png` → `s08_03_kindness_start_r01.png` | S08-L017 |
| 4:42.5 | 4.66 s | `s08_kindness` | chain | 73 | 0.98 | `s08_03_kindness_start_r01.png` → `s08_03_kindness_end_r01.png` | S08-L018 |
| 4:47.1 | 4.14 s | `s08_thank_you` | cut (close_up, cut) | 65 | 0.98 | `s08_02_milo_surprised_end_r01.png` → `s08_02_milo_surprised_end_r01.png` | S08-L019, S08-L020 |
| 4:51.3 | 4.82 s | `s08_same_kindness` | chain | 77 | 1.00 | `s08_02_milo_surprised_end_r01.png` → `s08_02_milo_surprised_end_r01.png` | S08-L021 |
| 4:56.1 | 6.26 s | `s08_perhaps` | cut (close_up, cut) | 81 | 0.81 | `s08_01_leo_softens_end_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L022, S08-L023 |
| 5:02.4 | 4.36 s | `s08_stars_almost` | chain | 69 | 0.99 | `s08_01_leo_softens_end_r01.png` → `s08_01_leo_softens_end_r01.png` | S08-L024 |

<details><summary>Lines</summary>

- `S08-L001` 3:43.4 (2.8 s incl. pause) **NARRATOR**: The lion looked down.
- `S08-L002` 3:46.2 (2.7 s incl. pause) **NARRATOR**: The mouse was trembling.
- `S08-L003` 3:48.9 (4.4 s incl. pause) **NARRATOR**: He could easily have frightened the little creature even more.
- `S08-L004` 3:53.4 (2.6 s incl. pause) **NARRATOR**: He could have become angry.
- `S08-L005` 3:55.9 (5.8 s incl. pause) **NARRATOR**: After all, he was the strongest animal for miles around.
- `S08-L006` 4:01.7 (5.9 s incl. pause) **NARRATOR**: But being able to frighten someone did not mean that he had to.
- `S08-L007` 4:07.6 (3.6 s incl. pause) **NARRATOR**: The lion's expression softened.
- `S08-L008` 4:11.2 (1.4 s incl. pause) **LION**: Well...
- `S08-L009` 4:12.7 (4.0 s incl. pause) **LION**: you certainly chose an exciting shortcut.
- `S08-L010` 4:16.6 (3.4 s incl. pause) **LION**: Go home, little one.
- `S08-L011` 4:20.0 (3.9 s incl. pause) **LION**: And next time, look where you're running.
- `S08-L012` 4:23.9 (3.8 s incl. pause) **MOUSE**: You're... letting me go?
- `S08-L013` 4:27.8 (2.1 s incl. pause) **LION**: You made a mistake.
- `S08-L014` 4:29.9 (2.2 s incl. pause) **LION**: You meant no harm.
- `S08-L015` 4:32.1 (3.5 s incl. pause) **LION**: I see no reason to hurt you for that.
- `S08-L016` 4:35.6 (3.8 s incl. pause) **NARRATOR**: The mouse stared up at the lion.
- `S08-L017` 4:39.4 (3.1 s incl. pause) **NARRATOR**: Anger was what had been expected.
- `S08-L018` 4:42.5 (4.7 s incl. pause) **NARRATOR**: Instead, the lion had chosen kindness.
- `S08-L019` 4:47.2 (1.7 s incl. pause) **MOUSE**: Thank you.
- `S08-L020` 4:48.9 (2.4 s incl. pause) **MOUSE**: I won't forget this.
- `S08-L021` 4:51.3 (4.8 s incl. pause) **MOUSE**: I hope someday I can show someone the same kindness.
- `S08-L022` 4:56.1 (3.4 s incl. pause) **LION**: Perhaps you will.
- `S08-L023` 4:59.5 (2.9 s incl. pause) **LION**: Now hurry.
- `S08-L024` 5:02.4 (4.4 s incl. pause) **LION**: Those stars you were worried about are almost here.

</details>

## Scene 09 (5:06.7 - 5:30.4, 23.7 s, audio `scene09.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 5:06.7 | 5.38 s | `s09_hurries` | cut (location_change, cut) | 81 | 0.94 | `s09_01_milo_hurries_start_r01.png` → `s09_01_milo_hurries_end_r01.png` | S09-L001, S09-L002 |
| 5:12.1 | 4.22 s | `s09_stars` | cut (location_change, crossfade) | 69 | 1.02 | `s09_02_stars_start_r01.png` → `s09_02_stars_end_r01.png` | S09-L003, S09-L004 |
| 5:16.3 | 4.45 s | `s09_home` | cut (location_change, crossfade) | 73 | 1.02 | `s09_03_home_start_r01.png` → `s09_03_home_end_r01.png` | S09-L005 |
| 5:20.8 | 4.17 s | `s09_leo_returns` | cut (location_change, crossfade) | 65 | 0.97 | `tree_day_r01.png` → `s09_07_leo_rests_r01.png` | S09-L006 |
| 5:24.9 | 5.44 s | `s09_leo_dozes` | chain | 81 | 0.93 | `s09_07_leo_rests_r01.png` → `s09_07_leo_rests_r01.png` | S09-L007 |

<details><summary>Lines</summary>

- `S09-L001` 5:06.7 (3.6 s incl. pause) **NARRATOR**: The mouse smiled and hurried home.
- `S09-L002` 5:10.3 (1.8 s incl. pause) **NARRATOR**: But this time...
- `S09-L003` 5:12.1 (2.1 s incl. pause) **NARRATOR**: a little more carefully.
- `S09-L004` 5:14.2 (2.1 s incl. pause) **NARRATOR**: Days passed.
- `S09-L005` 5:16.3 (4.4 s incl. pause) **NARRATOR**: The mouse returned to the usual routines of the forest.
- `S09-L006` 5:20.8 (4.2 s incl. pause) **NARRATOR**: And the lion returned to his favorite shady tree.
- `S09-L007` 5:25.0 (5.4 s incl. pause) **NARRATOR**: Neither of them expected that their paths would cross again so soon.

</details>

## Scene 10 (5:30.4 - 5:54.4, 24.0 s, audio `scene10.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 5:30.4 | 4.50 s | `s10_trap_landscape` | cut (location_change, crossfade) | 73 | 1.01 | `s10_01_trap_set_r01.png` → `s10_01_trap_set_r01.png` | S10-L001 |
| 5:34.9 | 4.50 s | `s10_leo_walks_in` | chain | 73 | 1.01 | `s10_01_trap_set_r01.png` → `s10_02_curious_step_start_r02.png` | S10-L001 |
| 5:39.4 | 5.51 s | `s10_curious_step` | chain | 81 | 0.92 | `s10_02_curious_step_start_r02.png` → `s10_03_curious_step_end_r02.png` | S10-L002, S10-L003 |
| 5:44.9 | 3.31 s | `s10_release` | chain | 53 | 1.00 | `s10_03_curious_step_end_r02.png` → `s10_04_net_falls_start_r02.png` | S10-L003 |
| 5:48.2 | 6.20 s | `s10_net_falls` | chain | 81 | 0.82 | `s10_04_net_falls_start_r02.png` → `s10_05_net_falls_end_r02.png` | S10-L004 |

<details><summary>Lines</summary>

- `S10-L001` 5:30.4 (9.0 s incl. pause) **NARRATOR**: Then, one morning, something small beneath the leaves caught the lion's eye as he walked through a distant part of the forest.
- `S10-L002` 5:39.4 (2.2 s incl. pause) **NARRATOR**: He stepped closer.
- `S10-L003` 5:41.6 (6.6 s incl. pause) **NARRATOR**: His paw pressed a hidden trigger, and a soft rope net dropped from the branches above.
- `S10-L004` 5:48.2 (6.2 s incl. pause) **NARRATOR**: The net settled over him, leaving his paws safely on the ground.

</details>

## Scene 11 (5:54.4 - 6:25.2, 30.8 s, audio `scene11.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 5:54.4 | 3.33 s | `s11_grips` | chain | 53 | 0.99 | `s10_05_net_falls_end_r02.png` → `s11_01_pull_once_start_r02.png` | S11-L001 |
| 5:57.8 | 3.34 s | `s11_tug` | chain | 53 | 0.99 | `s11_01_pull_once_start_r02.png` → `s11_02_pull_once_end_r02.png` | S11-L002 |
| 6:01.1 | 3.26 s | `s11_no_come_on` | cut (close_up, cut) | 53 | 1.02 | `s11_03_why_wont_it_break_start_r02.png` → `s11_03_why_wont_it_break_start_r02.png` | S11-L003, S11-L004 |
| 6:04.4 | 3.46 s | `s11_why_wont` | chain | 57 | 1.03 | `s11_03_why_wont_it_break_start_r02.png` → `s11_05_why_wont_it_break_end_r02.png` | S11-L005 |
| 6:07.8 | 3.13 s | `s11_lies_low` | cut (close_up, cut) | 49 | 0.98 | `s11_02_pull_once_end_r02.png` → `s11_06_waits_start_r02.png` | S11-L006 |
| 6:10.9 | 4.65 s | `s11_waits` | chain | 73 | 0.98 | `s11_06_waits_start_r02.png` → `s11_07_waits_end_r02.png` | S11-L007 |
| 6:15.6 | 5.61 s | `s11_calls` | cut (close_up, cut) | 81 | 0.90 | `s11_08_call_start_r02.png` → `s11_09_call_end_r02.png` | S11-L008 |
| 6:21.2 | 4.00 s | `s11_echo` | chain | 65 | 1.02 | `s11_09_call_end_r02.png` → `s11_09_call_end_r02.png` | S11-L009 |

<details><summary>Lines</summary>

- `S11-L001` 5:54.4 (3.3 s incl. pause) **NARRATOR**: He tried one careful tug.
- `S11-L002` 5:57.8 (3.3 s incl. pause) **NARRATOR**: But the knotted ropes held firm.
- `S11-L003` 6:01.1 (1.5 s incl. pause) **LION**: No...
- `S11-L004` 6:02.6 (1.8 s incl. pause) **LION**: Come on!
- `S11-L005` 6:04.4 (3.5 s incl. pause) **LION**: Why won't this break?
- `S11-L006` 6:07.8 (3.1 s incl. pause) **NARRATOR**: The lion was powerful.
- `S11-L007` 6:10.9 (4.6 s incl. pause) **NARRATOR**: But strength alone could not free him.
- `S11-L008` 6:15.6 (5.6 s incl. pause) **NARRATOR**: At last, he let out a deep call for help.
- `S11-L009` 6:21.2 (4.0 s incl. pause) **NARRATOR**: It echoed through the forest.

</details>

## Scene 12 (6:25.2 - 6:57.3, 32.1 s, audio `scene12.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 6:25.2 | 6.05 s | `s12_hears` | cut (location_change, cut) | 81 | 0.84 | `s12_01_hears_start_r01.png` → `s12_02_hears_end_r02.png` | S12-L001 |
| 6:31.2 | 5.28 s | `s12_the_lion` | chain | 81 | 0.96 | `s12_02_hears_end_r02.png` → `s12_02_hears_end_r02.png` | S12-L002, S12-L003 |
| 6:36.5 | 4.82 s | `s12_runs` | chain | 77 | 1.00 | `s12_02_hears_end_r02.png` → `s12_03_runs_end_r02.png` | S12-L004, S12-L005 |
| 6:41.4 | 4.58 s | `s12_runs_out` | chain | 73 | 1.00 | `s12_03_runs_end_r02.png` → `run_morning_r01.png` | S12-L006, S12-L007 |
| 6:45.9 | 4.97 s | `s12_empty_lane` | chain | 81 | 1.02 | `run_morning_r01.png` → `run_morning_r01.png` | S12-L008 |
| 6:50.9 | 2.73 s | `s12_leo_waits` | cut (location_change, cut) | 49 | 1.12 | `s11_07_waits_end_r02.png` → `s11_07_waits_end_r02.png` | S12-L009 |
| 6:53.6 | 3.64 s | `s12_milo_arrives` | chain | 57 | 0.98 | `s11_07_waits_end_r02.png` → `s12_04_arrives_start_r02.png` | S12-L010 |

<details><summary>Lines</summary>

- `S12-L001` 6:25.2 (6.0 s incl. pause) **NARRATOR**: And far away, two little ears lifted.
- `S12-L002` 6:31.3 (3.3 s incl. pause) **NARRATOR**: The mouse knew that voice.
- `S12-L003` 6:34.6 (2.0 s incl. pause) **MOUSE**: The lion!
- `S12-L004` 6:36.5 (2.9 s incl. pause) **NARRATOR**: The mouse ran toward the sound.
- `S12-L005` 6:39.4 (1.9 s incl. pause) **NARRATOR**: Over roots.
- `S12-L006` 6:41.4 (2.4 s incl. pause) **NARRATOR**: Between bushes.
- `S12-L007` 6:43.7 (2.2 s incl. pause) **NARRATOR**: Under branches.
- `S12-L008` 6:45.9 (5.0 s incl. pause) **NARRATOR**: This time there was no shortcut and no thought of getting home.
- `S12-L009` 6:50.9 (2.7 s incl. pause) **NARRATOR**: Someone was in trouble.
- `S12-L010` 6:53.6 (3.6 s incl. pause) **NARRATOR**: That was reason enough to run.

</details>

## Scene 13 (6:57.3 - 7:49.9, 52.6 s, audio `scene13.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 6:57.3 | 4.49 s | `s13_arrives` | chain | 73 | 1.02 | `s12_04_arrives_start_r02.png` → `s13_01_arrives_end_r02.png` | S13-L001 |
| 7:01.8 | 3.98 s | `s13_sees_lion` | chain | 65 | 1.02 | `s13_01_arrives_end_r02.png` → `s13_01_arrives_end_r02.png` | S13-L002 |
| 7:05.7 | 4.62 s | `s13_little_one` | cut (close_up, cut) | 73 | 0.99 | `s13_02_leo_doubtful_start_r02.png` → `s13_02_leo_doubtful_start_r02.png` | S13-L003, S13-L004 |
| 7:10.4 | 5.99 s | `s13_stay_back` | chain | 81 | 0.85 | `s13_02_leo_doubtful_start_r02.png` → `s13_02_leo_doubtful_start_r02.png` | S13-L004, S13-L005 |
| 7:16.3 | 3.89 s | `s13_looks_ropes` | cut (close_up, cut) | 61 | 0.98 | `s13_01_arrives_end_r02.png` → `s13_02_milo_confident_start_r04.png` | S13-L006 |
| 7:20.2 | 4.61 s | `s13_ropes_big` | chain | 73 | 0.99 | `s13_02_milo_confident_start_r04.png` → `s13_02_milo_confident_start_r04.png` | S13-L007 |
| 7:24.8 | 3.19 s | `s13_not_nothing` | chain | 49 | 0.96 | `s13_02_milo_confident_start_r04.png` → `s13_02_milo_confident_end_r04.png` | S13-L008 |
| 7:28.0 | 3.19 s | `s13_leo_doubts` | cut (close_up, cut) | 49 | 0.96 | `s13_02_leo_doubtful_start_r02.png` → `s13_06_leo_doubtful_end_r02.png` | S13-L008 |
| 7:31.2 | 3.30 s | `s13_steps_closer` | cut (close_up, cut) | 53 | 1.00 | `s13_02_milo_confident_end_r04.png` → `s13_07_milo_at_net_r01.png` | S13-L009 |
| 7:34.5 | 3.01 s | `s13_too_strong` | cut (close_up, cut) | 49 | 1.02 | `s13_08_milo_cu_r01.png` → `s13_08_milo_cu_r01.png` | S13-L010 |
| 7:37.5 | 4.02 s | `s13_my_teeth` | chain | 65 | 1.01 | `s13_08_milo_cu_r01.png` → `s13_08_milo_cu_r01.png` | S13-L011 |
| 7:41.5 | 2.82 s | `s13_your_teeth` | cut (close_up, cut) | 49 | 1.09 | `s13_06_leo_doubtful_end_r02.png` → `s13_06_leo_doubtful_end_r02.png` | S13-L012 |
| 7:44.4 | 5.49 s | `s13_lots_of_them` | cut (close_up, cut) | 81 | 0.92 | `s13_08_milo_cu_r01.png` → `s13_08_milo_cu_r01.png` | S13-L013, S13-L014 |

<details><summary>Lines</summary>

- `S13-L001` 6:57.3 (4.5 s incl. pause) **NARRATOR**: At last, the mouse reached the straight forest path.
- `S13-L002` 7:01.8 (4.0 s incl. pause) **NARRATOR**: There was the lion, caught inside the great net.
- `S13-L003` 7:05.7 (2.1 s incl. pause) **LION**: Little one?
- `S13-L004` 7:07.9 (5.0 s incl. pause) **LION**: You should stay back. These ropes are too strong.
- `S13-L005` 7:12.8 (3.5 s incl. pause) **LION**: I've tried everything.
- `S13-L006` 7:16.3 (3.9 s incl. pause) **NARRATOR**: The mouse looked carefully at the ropes.
- `S13-L007` 7:20.2 (4.6 s incl. pause) **NARRATOR**: They were certainly much bigger than the mouse.
- `S13-L008` 7:24.8 (6.4 s incl. pause) **NARRATOR**: But being smaller than a problem did not mean there was nothing you could do about it.
- `S13-L009` 7:31.2 (3.3 s incl. pause) **NARRATOR**: The mouse stepped closer.
- `S13-L010` 7:34.5 (3.0 s incl. pause) **MOUSE**: Maybe they're too strong for your paws.
- `S13-L011` 7:37.5 (4.0 s incl. pause) **MOUSE**: But perhaps they're not too strong for my teeth.
- `S13-L012` 7:41.5 (2.8 s incl. pause) **LION**: Your teeth?
- `S13-L013` 7:44.4 (2.0 s incl. pause) **MOUSE**: They're small.
- `S13-L014` 7:46.4 (3.5 s incl. pause) **MOUSE**: But I have quite a lot of them.

</details>

## Scene 14 (7:49.9 - 8:43.5, 53.6 s, audio `scene14.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 7:49.9 | 4.42 s | `s14_takes_rope` | cut (close_up, cut) | 69 | 0.97 | `s14_01_milo_holds_rope_r01.png` → `s14_02_gnaw_fray_start_r02.png` | S14-L001 |
| 7:54.3 | 4.42 s | `s14_gnaw_fray` | chain | 69 | 0.97 | `s14_02_gnaw_fray_start_r02.png` → `s14_03_gnaw_fray_end_r02.png` | S14-L001 |
| 7:58.7 | 3.42 s | `s14_nibble_gnaw` | chain | 53 | 0.97 | `s14_03_gnaw_fray_end_r02.png` → `s14_03_gnaw_fray_end_r02.png` | S14-L002, S14-L003 |
| 8:02.1 | 6.02 s | `s14_gnaw_wide` | cut (close_up, cut) | 81 | 0.84 | `s14_04_gnaw_wide_r01.png` → `s14_04_gnaw_wide_r01.png` | S14-L004, S14-L005 |
| 8:08.1 | 5.36 s | `s14_leo_doubts` | cut (close_up, cut) | 81 | 0.94 | `s13_06_leo_doubtful_end_r02.png` → `s13_06_leo_doubtful_end_r02.png` | S14-L006, S14-L007 |
| 8:13.5 | 6.24 s | `s14_keeps_going` | cut (close_up, cut) | 81 | 0.81 | `s14_03_gnaw_fray_end_r02.png` → `s14_05_sever_R01_start_r02.png` | S14-L007, S14-L008 |
| 8:19.7 | 4.53 s | `s14_fibres` | chain | 73 | 1.01 | `s14_05_sever_R01_start_r02.png` → `s14_05_sever_R01_start_r02.png` | S14-L009 |
| 8:24.3 | 3.69 s | `s14_parted` | chain | 61 | 1.03 | `s14_05_sever_R01_start_r02.png` → `s14_06_sever_R01_end_r02.png` | S14-L010 |
| 8:27.9 | 4.45 s | `s14_steps_aside` | cut (close_up, cut) | 73 | 1.02 | `s14_07_milo_clear_start_r02.png` → `s14_08_milo_clear_end_r02.png` | S14-L011 |
| 8:32.4 | 2.49 s | `s14_widens` | chain | 49 | 1.23 | `s14_08_milo_clear_end_r02.png` → `s14_09_step_clear_start_r02.png` | S14-L012 |
| 8:34.9 | 6.05 s | `s14_step_clear` | chain | 81 | 0.84 | `s14_09_step_clear_start_r02.png` → `s14_10_step_clear_end_r02.png` | S14-L013 |
| 8:40.9 | 2.52 s | `s14_free` | chain | 49 | 1.22 | `s14_10_step_clear_end_r02.png` → `s14_11_free_hold_start_r02.png` | S14-L014 |

<details><summary>Lines</summary>

- `S14-L001` 7:49.9 (8.8 s incl. pause) **NARRATOR**: The mouse found the rope holding a fold of the net closed. With both little paws holding it steady, the mouse began to gnaw.
- `S14-L002` 7:58.7 (1.5 s incl. pause) **NARRATOR**: Nibble.
- `S14-L003` 8:00.2 (1.9 s incl. pause) **NARRATOR**: Gnaw.
- `S14-L004` 8:02.1 (3.3 s incl. pause) **NARRATOR**: One tiny bite at a time.
- `S14-L005` 8:05.5 (2.7 s incl. pause) **NARRATOR**: The ropes were thick.
- `S14-L006` 8:08.1 (2.0 s incl. pause) **NARRATOR**: The work was slow.
- `S14-L007` 8:10.2 (6.7 s incl. pause) **NARRATOR**: And more than once, it seemed as though such a tiny creature could never make a difference.
- `S14-L008` 8:16.8 (2.9 s incl. pause) **NARRATOR**: But the mouse kept going.
- `S14-L009` 8:19.7 (4.5 s incl. pause) **NARRATOR**: The fibres frayed, one tiny bite at a time.
- `S14-L010` 8:24.3 (3.7 s incl. pause) **NARRATOR**: At last, the rope parted.
- `S14-L011` 8:28.0 (4.5 s incl. pause) **NARRATOR**: The mouse let go and stepped safely aside.
- `S14-L012` 8:32.4 (2.5 s incl. pause) **NARRATOR**: The opening widened.
- `S14-L013` 8:34.9 (6.1 s incl. pause) **NARRATOR**: The lion stepped through, and the loosened net slipped onto the path behind him.
- `S14-L014` 8:40.9 (2.5 s incl. pause) **NARRATOR**: He was free.

</details>

## Scene 15 (8:43.5 - 10:26.9, 103.5 s, audio `scene15.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 8:43.5 | 6.15 s | `s15_you_did_it` | cut (close_up, cut) | 81 | 0.82 | `s15_01_leo_amazed_start_r01.png` → `s15_01_leo_amazed_start_r01.png` | S15-L001, S15-L002 |
| 8:49.6 | 3.06 s | `s15_told_you` | cut (close_up, cut) | 49 | 1.00 | `s15_02_milo_modest_start_r04.png` → `s15_02_milo_modest_start_r04.png` | S15-L003 |
| 8:52.7 | 6.25 s | `s15_looked` | cut (close_up, cut) | 81 | 0.81 | `s14_11_free_hold_start_r02.png` → `s15_05_free_hold_end_r02.png` | S15-L004 |
| 8:58.9 | 3.61 s | `s15_rescued` | chain | 57 | 0.99 | `s15_05_free_hold_end_r02.png` → `s15_05_free_hold_end_r02.png` | S15-L005 |
| 9:02.5 | 3.61 s | `s15_grateful_look` | cut (close_up, cut) | 57 | 0.99 | `s15_01_leo_amazed_end_r01.png` → `s15_01_leo_amazed_end_r01.png` | S15-L005 |
| 9:06.1 | 3.19 s | `s15_came_to_help` | chain | 53 | 1.04 | `s15_01_leo_amazed_end_r01.png` → `s15_01_leo_amazed_end_r01.png` | S15-L006 |
| 9:09.3 | 3.19 s | `s15_didnt_have_to` | chain | 53 | 1.04 | `s15_01_leo_amazed_end_r01.png` → `s15_01_leo_amazed_end_r01.png` | S15-L006 |
| 9:12.5 | 4.14 s | `s15_kind_to_me` | cut (close_up, cut) | 65 | 0.98 | `s15_02_milo_modest_start_r04.png` → `s15_02_milo_modest_end_r04.png` | S15-L007 |
| 9:16.7 | 4.02 s | `s15_repaid` | cut (close_up, cut) | 65 | 1.01 | `s15_01_leo_amazed_end_r01.png` → `s15_01_leo_amazed_end_r01.png` | S15-L008 |
| 9:20.7 | 3.98 s | `s15_not_like_that` | cut (close_up, cut) | 65 | 1.02 | `s15_04_milo_sincere_start_r04.png` → `s15_04_milo_sincere_start_r04.png` | S15-L009 |
| 9:24.7 | 4.42 s | `s15_what_mean` | cut (close_up, cut) | 69 | 0.97 | `s15_01_leo_amazed_end_r01.png` → `s15_01_leo_amazed_end_r01.png` | S15-L010, S15-L011 |
| 9:29.1 | 5.93 s | `s15_no_debt` | cut (close_up, cut) | 81 | 0.85 | `s15_04_milo_sincere_start_r04.png` → `s15_04_milo_sincere_start_r04.png` | S15-L011, S15-L012 |
| 9:35.0 | 3.85 s | `s15_saw_someone` | chain | 61 | 0.99 | `s15_04_milo_sincere_start_r04.png` → `s15_04_milo_sincere_start_r04.png` | S15-L013 |
| 9:38.9 | 6.03 s | `s15_so_i_helped` | chain | 81 | 0.84 | `s15_04_milo_sincere_start_r04.png` → `s15_04_milo_sincere_end_r04.png` | S15-L014, S15-L015 |
| 9:44.9 | 4.17 s | `s15_quiet` | cut (close_up, cut) | 65 | 0.97 | `s15_03_leo_reflects_start_r01.png` → `s15_03_leo_reflects_end_r01.png` | S15-L016 |
| 9:49.1 | 3.58 s | `s15_thinks` | chain | 57 | 0.99 | `s15_03_leo_reflects_end_r01.png` → `s15_03_leo_reflects_end_r01.png` | S15-L017 |
| 9:52.7 | 3.58 s | `s15_sits` | cut (close_up, cut) | 57 | 0.99 | `s15_05_free_hold_end_r02.png` → `s15_14_leo_sits_r01.png` | S15-L017 |
| 9:56.2 | 4.82 s | `s15_claws_roar` | chain | 77 | 1.00 | `s15_14_leo_sits_r01.png` → `s15_14_leo_sits_r01.png` | S15-L018, S15-L019 |
| 10:01.1 | 5.63 s | `s15_understood` | cut (close_up, cut) | 81 | 0.90 | `s15_03_leo_reflects_end_r01.png` → `s15_01_leo_amazed_end_r01.png` | S15-L019, S15-L020 |
| 10:06.7 | 3.71 s | `s15_understands` | chain | 61 | 1.03 | `s15_01_leo_amazed_end_r01.png` → `s15_01_leo_amazed_end_r01.png` | S15-L020 |
| 10:10.4 | 3.65 s | `s15_gentleness` | cut (close_up, cut) | 57 | 0.98 | `s15_14_leo_sits_r01.png` → `s15_15_leo_bows_r01.png` | S15-L021 |
| 10:14.0 | 3.65 s | `s15_gentle_hold` | chain | 57 | 0.98 | `s15_15_leo_bows_r01.png` → `s15_15_leo_bows_r01.png` | S15-L021 |
| 10:17.7 | 5.53 s | `s15_not_powerless` | cut (close_up, cut) | 81 | 0.92 | `s15_02_milo_modest_end_r04.png` → `s15_02_milo_modest_end_r04.png` | S15-L022 |
| 10:23.2 | 3.72 s | `s15_smiled` | cut (close_up, cut) | 61 | 1.02 | `s15_01_leo_amazed_end_r01.png` → `s15_16_leo_smiles_r01.png` | S15-L023 |

<details><summary>Lines</summary>

- `S15-L001` 8:43.5 (2.9 s incl. pause) **LION**: You did it.
- `S15-L002` 8:46.4 (3.3 s incl. pause) **LION**: You actually did it.
- `S15-L003` 8:49.6 (3.1 s incl. pause) **MOUSE**: I told you my teeth might help.
- `S15-L004` 8:52.7 (6.2 s incl. pause) **NARRATOR**: For a moment, the great lion simply looked at the tiny mouse.
- `S15-L005` 8:58.9 (7.2 s incl. pause) **NARRATOR**: The strongest creature in that part of the forest had been rescued by one of the smallest.
- `S15-L006` 9:06.1 (6.4 s incl. pause) **LION**: You came to help me even though you didn't have to.
- `S15-L007` 9:12.5 (4.1 s incl. pause) **MOUSE**: You were kind to me when you didn't have to either.
- `S15-L008` 9:16.7 (4.0 s incl. pause) **LION**: So you repaid what I did for you.
- `S15-L009` 9:20.7 (4.0 s incl. pause) **MOUSE**: I don't think kindness works like that.
- `S15-L010` 9:24.7 (2.2 s incl. pause) **LION**: What do you mean?
- `S15-L011` 9:26.8 (4.5 s incl. pause) **MOUSE**: When you let me go, you didn't give me a debt.
- `S15-L012` 9:31.3 (3.7 s incl. pause) **MOUSE**: You showed me what kindness looks like.
- `S15-L013` 9:35.0 (3.9 s incl. pause) **MOUSE**: Today I saw someone who needed help.
- `S15-L014` 9:38.9 (1.9 s incl. pause) **MOUSE**: So I helped.
- `S15-L015` 9:40.7 (4.2 s incl. pause) **MOUSE**: Maybe someday, someone else will do the same.
- `S15-L016` 9:44.9 (4.2 s incl. pause) **NARRATOR**: The lion became quiet.
- `S15-L017` 9:49.1 (7.2 s incl. pause) **NARRATOR**: He had always thought of strength as something that belonged to the biggest paws...
- `S15-L018` 9:56.2 (2.9 s incl. pause) **NARRATOR**: the sharpest claws...
- `S15-L019` 9:59.1 (3.9 s incl. pause) **NARRATOR**: or the loudest roar.
- `S15-L020` 10:03.0 (7.4 s incl. pause) **NARRATOR**: But now he understood something he had not understood before.
- `S15-L021` 10:10.4 (7.3 s incl. pause) **NARRATOR**: Strength could also mean choosing gentleness when you could choose anger.
- `S15-L022` 10:17.7 (5.5 s incl. pause) **NARRATOR**: And being small did not mean being powerless.
- `S15-L023` 10:23.2 (3.7 s incl. pause) **NARRATOR**: The lion smiled.

</details>

## Scene 16 (10:26.9 - 11:23.7, 56.7 s, audio `scene16.wav`)

| Start | Length | Piece | Join | Frames | Speed | Start image → end image | Lines |
|---|---|---|---|---|---|---|---|
| 10:26.9 | 6.30 s | `s16_tree_landscape` | cut (location_change, crossfade) | 81 | 0.80 | `tree_day_r01.png` → `tree_day_r01.png` | S16-L001 |
| 10:33.2 | 4.80 s | `s16_you_know` | cut (dissolve, crossfade) | 77 | 1.00 | `s16_01_friends_start_r01.png` → `s16_01_friends_start_r01.png` | S16-L002, S16-L003 |
| 10:38.0 | 3.31 s | `s16_large_ideas` | chain | 53 | 1.00 | `s16_01_friends_start_r01.png` → `s16_01_friends_start_r01.png` | S16-L003 |
| 10:41.3 | 3.50 s | `s16_useful_teeth` | chain | 57 | 1.02 | `s16_01_friends_start_r01.png` → `s16_01_friends_start_r01.png` | S16-L004 |
| 10:44.8 | 4.66 s | `s16_laugh` | chain | 73 | 0.98 | `s16_01_friends_start_r01.png` → `s16_01_friends_end_r01.png` | S16-L005, S16-L006 |
| 10:49.5 | 6.17 s | `s16_laughter_settles` | chain | 81 | 0.82 | `s16_01_friends_end_r01.png` → `s16_01_friends_end_r01.png` | S16-L006, S16-L007 |
| 10:55.7 | 4.41 s | `s16_old_tree` | cut (dissolve, crossfade) | 69 | 0.98 | `tree_day_r01.png` → `tree_day_r01.png` | S16-L007 |
| 11:00.1 | 3.53 s | `s16_net_memory` | cut (location_change, crossfade) | 57 | 1.01 | `s10_01_trap_set_r01.png` → `s10_01_trap_set_r01.png` | S16-L008 |
| 11:03.6 | 4.61 s | `s16_stream_memory` | cut (location_change, crossfade) | 73 | 0.99 | `stream_afternoon_r01.png` → `stream_afternoon_r01.png` | S16-L009 |
| 11:08.2 | 3.65 s | `s16_friends_again` | cut (location_change, crossfade) | 57 | 0.98 | `s16_01_friends_end_r01.png` → `s16_01_friends_end_r01.png` | S16-L010 |
| 11:11.9 | 5.25 s | `s16_rest` | chain | 81 | 0.96 | `s16_01_friends_end_r01.png` → `s16_03_friends_resting_r01.png` | S16-L011 |
| 11:17.1 | 3.28 s | `s16_resting` | chain | 53 | 1.01 | `s16_03_friends_resting_r01.png` → `s16_03_friends_resting_r01.png` | S16-L012 |
| 11:20.4 | 3.28 s | `s16_final_landscape` | cut (dissolve, crossfade) | 53 | 1.01 | `tree_day_r01.png` → `tree_day_r01.png` | S16-L012 |

<details><summary>Lines</summary>

- `S16-L001` 10:26.9 (6.3 s incl. pause) **NARRATOR**: Later, beneath the great old tree, the two new friends rested together.
- `S16-L002` 10:33.2 (1.5 s incl. pause) **LION**: You know...
- `S16-L003` 10:34.7 (6.6 s incl. pause) **LION**: for someone so small, you have rather large ideas.
- `S16-L004` 10:41.3 (3.5 s incl. pause) **MOUSE**: And very useful teeth.
- `S16-L005` 10:44.8 (2.9 s incl. pause) **NARRATOR**: The lion laughed.
- `S16-L006` 10:47.7 (3.5 s incl. pause) **NARRATOR**: And the mouse laughed too.
- `S16-L007` 10:51.3 (8.8 s incl. pause) **NARRATOR**: From that day forward, whenever either of them found someone who needed help, they remembered what had happened beneath the old tree...
- `S16-L008` 11:00.1 (3.5 s incl. pause) **NARRATOR**: and inside the hunter's net.
- `S16-L009` 11:03.6 (4.6 s incl. pause) **NARRATOR**: Because kindness is not a debt that must be repaid.
- `S16-L010` 11:08.2 (3.7 s incl. pause) **NARRATOR**: Kindness is something we can pass on.
- `S16-L011` 11:11.9 (5.2 s incl. pause) **NARRATOR**: And sometimes, one small act is enough to begin another.
- `S16-L012` 11:17.1 (6.6 s incl. pause) **NARRATOR**: Kindness does not create a debt. It creates more kindness.

</details>
