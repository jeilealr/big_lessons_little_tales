# revisions/: history of the 2026-10-02 Gemini revision rounds

`r02.json` to `r05.json` hold the per-record correction texts that `character/gemini_image.py`
appended to the planned prompt during the r02–r05 rounds, and `gemini_ledger.csv` logs every
Gemini image call with its model and estimated cost. The exact text sent for each accepted image
is stored in that record's `result.prompt_sent` in `../prompt_manifest.json`.

These files are **history, not instructions**. Since 2026-10-02 every prompt is a template
built from `../visual_bible.json` (`docs/image-prompts.md`); the corrections that the owner
accepted were folded into the records' templates, and the identity sentences these files repeat
were replaced by the canonical identity blocks. Do not add new correction files: change the
record's `prompt_template` or the bible, then run `python3 production/image_prompts.py build`
and `lint`.
