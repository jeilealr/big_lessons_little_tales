# Timed dialogue mouth animation

The recorded line WAVs and speaker labels remain the timing source. For each project, forced-align the exact approved transcript to each line recording, review alignment exceptions, then apply mouth animation only to owner-selected video takes whose `mode: mouth` variant names the speaking character. `NARRATOR` lines are voice-over and must never drive a character's mouth, even when the narrator describes speech or a call. During narration, keep the approved mouth pose still. Distant wide shots also keep their mouth poses still because the mouth cannot be reliably masked or reviewed at that scale. The separate compositor preserves each take's first and last frames. A chained dialogue take must have closed-mouth boundary images and a separate approved open-mouth calibration image edited from one of those closed frames. It changes only the named speaker's mouth region during that speaker's aligned words; silent gaps stay in the approved closed pose. Open-mouth boundary frames are rejected because preserving them would cause a mouth to open during a pause. A piece without one explicit character speaker is rejected; mixed speakers must be split or explicitly select the visible character whose line is being animated, leaving other speakers' intervals closed.

## Lion and Mouse v6

WhisperX lives in a separate CPU Python environment, with CPU-only PyTorch and its own FFmpeg executable, so it does not change the Wan/ROCm renderer environment. Setup has completed on LUMI:

```bash
bash voice/setup_lipsync_env.sh
.venv-lipsync/bin/python production/lip_sync.py align \
  --story lion_and_mouse_v6 --audio-story lion_and_mouse_v5 --lang en --device cpu
```

The v6 alignment is already generated at `work/stories/lion_and_mouse_v5/audio/en/word_timings.json`: all 161 lines (1,238 words) aligned with no review flags. The aligner used the v6 dialogue transcript against the reused v5 line recordings; the output records audio hashes and the WhisperX version. For a changed transcript or audio, rerun the command and review any line marked `review` before applying. `NARRATOR` remains a valid timing record for coverage but its words are always excluded from character mouth cues.

After images are approved, video takes are rendered, and choices are recorded in `stories/lion_and_mouse_v6/takes.yaml`:

```bash
.venv-lipsync/bin/python production/lip_sync.py apply --story lion_and_mouse_v6
```

The generated clips and hash-bound index live in `work/stories/lion_and_mouse_v6/lipsync/`. Inspect each processed clip at normal speed and frame-by-frame around words, pauses, and joins. Re-run `chain_preview.py --require-takes` after processing. The final `production/edit_manifest.py` export refuses a `mode: mouth` piece unless its selected source is still unchanged and the corresponding lip-sync output passes its hashes.

## Scope and accuracy

WhisperX provides word-level timestamps through forced alignment. The compositor uses each word interval and vowel groups to create broad opening pulses, blending only the pixel difference between the approved closed/open images in the configured face ROI. It is a controlled approximation, not phoneme-level viseme synthesis: it does not create distinct /m/, /f/, /o/ or /ee/ mouth shapes. Reviewers should reject clips where the single open shape looks wrong for the line or where the mask includes anything beyond the mouth. If the approved endpoint or calibration images are missing, mismatched, or produce an ambiguous mask, the compositor stops instead of guessing. A changed timing plan, prompt manifest, visual bible, dialogue coverage, word alignment, line audio or approved mouth image invalidates the cached lip-sync output and edit handoff until `apply` runs again.

For another project, provide line-level WAVs, exact transcript/speaker metadata, a `timing_plan.json`, `dialogue_coverage.json`, a prompt manifest with matched open/closed endpoints and `mouth_character` markers, and `mouth` variant rows with one explicit character `speaker`. Run the same two steps after narration is finalized and after takes are selected. Preserve the timing and sync manifests with the edit handoff. Review that narrator-only intervals leave the character mouth unchanged and that another character's line never opens the selected speaker's mouth.
