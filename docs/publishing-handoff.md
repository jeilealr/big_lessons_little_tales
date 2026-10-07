# Handing finished stories to publishing

**PROPOSED** (Feltwillow Blueprint v3, change set G3). This repository makes stories. A separate private
repository, `jeilealr/feltwillow-publishing`, publishes them (website, podcast, YouTube metadata). The two
repositories share no code and are never checked out side by side. The only thing production
gives publishing is a **handoff package**: one `.tar` file you move by hand.

A handoff is not an approval to publish. It says "these are the files I selected, and this is where
they came from". Publishing reviews and approves separately.

A handoff has up to three components: **images** (illustrations, cover), **audio** (the final master as
WAV or FLAC, optional spoken transcript) and **video** (master, captions, thumbnail). The reading text for
the website is not part of a handoff: publishing writes it (its own `reading-edition` record) from the
script and line list you include as source files.

## The pieces

| Path | What it is |
|---|---|
| `production/export_handoff.py` | builds the package; reads the repo, writes only to `--out` |
| `production/contracts/CONTRACT.lock` + `feltwillow-contracts/<version>/` | the pinned publishing contract (see `production/contracts/README.md`) |
| `stories/<slug>/handoff_selection.yaml` | your explicit list of what goes into the handoff (committed) |
| `production/handoff/allocations/<story_id>.json` | the story ID record issued by publishing (or pass `--allocation`) |

Story IDs (`lion-and-mouse`) come from publishing, not from folder names (`lion_and_mouse_v5`). Ask
publishing for an allocation before the first export.

## Export, step by step

1. **Write the selection.** Copy `stories/lion_and_mouse_v5/handoff_selection.example.yaml`, name every
   file explicitly (no patterns, no "newest file"), set `example: false`, quote timestamps.
   Stores: `production-git` (tracked files), `production-work` (`work/`, i.e. `FELTWILLOW_WORK`),
   `owner-master-store` (`FELTWILLOW_MASTER_ROOT`: final mixes, DaVinci exports). Audio masters are WAV or FLAC;
   do not hand off MP3/M4A (publishing makes the delivery MP3). Video needs `ffprobe` (see below).
2. **Commit** the selection and every tracked file it names. Unrelated uncommitted files are fine; they
   are listed in the handoff. A selected file that is modified, untracked or differs from the commit
   stops the export (`SELECTED_SOURCE_DIRTY`).
3. **Run** from the repo root (system Python with PyYAML is enough):

   ```bash
   python3 production/export_handoff.py export \
       --selection stories/lion_and_mouse_v5/handoff_selection.yaml \
       --allocation production/handoff/allocations/lion-and-mouse.json \
       --operator "<your name>" \
       --out /path/outside/the/repo/handoffs \
       --master-root "$FELTWILLOW_MASTER_ROOT"        # only if the selection uses owner-master-store
   ```

   Output: `<handoff_id>.tar`, `<handoff_id>.tar.sha256`, `<handoff_id>.export.json` (summary; private).
   Nothing is overwritten; nothing is written into the repository.
4. **Move** the tar to the publishing machine's inbox (`FELTWILLOW_HANDOFF_INBOX`). Send the archive sha256
   separately (the line printed at the end, or the `.sha256` file); the importer checks it.
5. A **correction** is a new export with `handoff_revision: 2`, `purpose: correction`, a `reason`, and
   `supersedes: {handoff_id, payload_sha256}` of the earlier export (from its `.export.json`).

Try first with `--dry-run`: it reports every problem at once and still writes a `*.DRYRUN.tar` so you
can see the size; a dry-run package can never be imported.

## What the exporter refuses, and what to do

| Code | Meaning | Fix |
|---|---|---|
| `SELECTION_MISSING` | no selection file at the given path | there is no default; write and commit one |
| `SELECTION_INVALID` | unknown/missing key, duplicate YAML key, unquoted timestamp, bad value | fix the YAML |
| `SELECTION_GLOB_FORBIDDEN` | `*`, `?`, `[...]` in a path | name each file |
| `UNSAFE_PATH`, `PATH_OUTSIDE_REPO`, `SYMLINK_FORBIDDEN`, `NOT_A_REGULAR_FILE` | path absolute, with `..`, through a symlink, or not a plain file | select the real file inside its store |
| `SELECTED_FILE_MISSING`, `SELECTED_SOURCE_UNTRACKED` | the named file is not there / not in Git | check the name; commit it |
| `SELECTED_SOURCE_DIRTY` | a selected tracked file (or the selection itself) has uncommitted changes or is untracked | commit it |
| `EVIDENCE_REF_DIRTY` | a `repo_path` evidence file (e.g. `docs/licensing.md`) is uncommitted | commit it |
| `DIRTY_PATH_UNREPRESENTABLE` | an unrelated uncommitted path cannot be recorded (e.g. a name with a space; leading-dot names such as `.DS_Store` are fine since contract H2) | commit, restore, rename or delete it |
| `EXPORTER_DIRTY`, `CONTRACT_PIN_DIRTY` | the exporter or the pinned contract is uncommitted, or the exporter runs from outside the repo | commit; run the repo's own copy |
| `CONTRACT_LOCK_MISSING`, `CONTRACT_LOCK_INVALID`, `CONTRACT_PIN_MISSING`, `CONTRACT_LOCK_MISMATCH`, `LOCK_MISSING_EMITTED_SCHEMA`, `CONTRACT_VERSION_UNSUPPORTED` | pinned contract absent, edited or for another handoff version | re-pin the released contract (`production/contracts/README.md`) |
| `STORY_NOT_ALLOCATED`, `ALLOCATION_INVALID`, `SLUG_NOT_ALLOCATED`, `LANGUAGE_NOT_PLANNED` | story ID / slug / language not covered by the publishing allocation | ask publishing for a (new) allocation |
| `MEDIA_TYPE_MISMATCH`, `MEDIA_TYPE_ROLE_MISMATCH` | bytes are not the declared type, or type not allowed for the role | fix `media_type` or the file |
| `HANDOFF_AUDIO_NOT_LOSSLESS` | an MP3/M4A audio file was selected | select the WAV/FLAC master |
| `MEASUREMENT_TOOL_UNAVAILABLE` | a video is selected but no working `ffprobe` was found | install/load FFmpeg, or pass `--ffprobe PATH` |
| `MEASUREMENT_FAILED`, `MEASUREMENT_UNSUPPORTED` | `ffprobe` could not read the video, a required value could not be measured, or a video comes from a tracked file | check the file; take video from `work/` or the master store |
| `COMPONENT_INCOMPLETE`, `NO_COMPONENTS`, `UNKNOWN_ASSET`, `WRONG_ASSET_ROLE`, `UNREFERENCED_ASSET` | a component lacks its required file, or assets and components disagree | complete the component or leave it `null` |
| `PURPOSE_REVISION_MISMATCH`, `REASON_REQUIRED`, `TIMESTAMP_ORDER` | lineage fields inconsistent | see step 5 |
| `OUT_INSIDE_REPO`, `OUT_EXISTS` | `--out` inside the repo, or package already there | choose another folder |
| `STATE_ROOT_UNSET`, `STATE_ROOT_UNSAFE` | master store (`FELTWILLOW_MASTER_ROOT`) not given, or inside the repo | set `FELTWILLOW_MASTER_ROOT` outside Git |
| `SCHEMA_VIOLATION` | pinned schema rejects the record (only checked when `jsonschema` is installed) | read the message |
| `SOURCE_CHANGED_DURING_EXPORT` | a file changed between hashing and packing | re-run when nothing is writing |

## What is measured

Every image, audio and video asset records which tool measured it (`measurement: {tool, version}`):

- PNG, JPEG, WebP width/height and WAV, FLAC duration (integer ms, rounded half up), sample rate,
  channels: the exporter itself (`feltwillow-stdlib`, version `export_handoff-<version>+py<python>`).
- MP4/MOV width, height, duration and frame rate (a fraction such as 25/1): `ffprobe`, version taken
  from the first line of `ffprobe -version`. The exporter uses `ffprobe` on `PATH` or `--ffprobe PATH`.
  On LUMI: `module load LUMI/25.09 partition/L FFmpeg/7.1.3-cpeGNU-25.09` (tested with ffprobe 7.1.3).
  Without it, a video is refused (`MEASUREMENT_TOOL_UNAVAILABLE`); nothing is estimated.

Text assets (transcript, captions, chapters) must be UTF-8 in NFC; their `measurement` is empty.

## Guarantees

- Read-only on this repository: Git runs with optional locks disabled (`git status` does not refresh the
  index); files are opened read-only; `--out` must be outside the repository.
- Tracked files are shipped as the committed bytes, after checking the working copy is identical.
- Deterministic: same selection, same commit, same `--created-at` gives the same archive digest; the
  payload digest (logical identity) does not depend on export time or operator.
- `handoff.json` is canonical JSON (sorted keys, no spaces, UTF-8, integers only, NFC strings).

## Data lifetime

LUMI scratch (including `work/`) is deleted around 2027-03-30. A handoff that takes audio from
`production-work` is the moment to copy that audio to the master store as well.
