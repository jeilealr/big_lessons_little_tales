# character/: images, one folder per story

```
characters/<story>/<Name>/        canonical/, references/, expressions/ (owner-made or recorded generations)
characters/<story>/interactions/  scene start/end frames (keyframes/) and two-character images
locations/<story>/<place>/        empty plates; locations/<story>/props/
```

`<story>` is the folder name in `stories/` (e.g. `lion_and_mouse_v5`, `ugly_duckling_v1`), so a
story's folder holds only its own cast and places. Each image's exact file name and prompt is in
`stories/<story>/prompt_manifest.json` (v5 uses the v4 manifest; the READMEs in its folders list
the file names). Since 2026-10-04; before that the layout was `characters/<Name>/<version>/`.

Tools: `gemini_image.py` (optional stills via the Gemini API).
