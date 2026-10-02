# Cloud trial: Gemini canonical takes (2026-10-02)

Alternative neutral full-body takes of Leo and Milo from a Gemini Pro image
model, conditioned on the v4 canonicals (`<Name>/v4/canonical/`) and the
identity/style text of `stories/lion_and_mouse_v4/visual_bible.json`.
**Candidates for owner review only**; nothing here replaces a v4 canonical.

- Script: `character/gemini_canonical_trial.py` (stdlib API calls; Pillow for the sheet).
- Outputs: `<Name>/cloud_trial/full-body_<name>_neutral_pose_gemini_tNN.{png,json}`;
  each `.json` is the full prompt record (prompt, reference hash, model,
  settings, acceptance checks, result hash or error).
- Contact sheet: `cloud_trial_contact_sheet.jpg` (first column = current v4
  canonical, green frame).
- Licence check pending: `docs/licensing.md`.

Status: the records are `planned_not_executed`. In the cloud session of
2026-10-02 the Gemini API answered 403 "unregistered caller": no API key
reached Google, so no image was generated. To run once a key works:

```bash
python3 character/gemini_canonical_trial.py --list-models   # confirms key + model name
python3 character/gemini_canonical_trial.py --takes 3        # images, records, contact sheet
```
