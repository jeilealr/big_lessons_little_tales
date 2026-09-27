# Voices and narration

Original, licence-clean voices for the channel's fables, one canonical voice per
role (narrator, each character), usable in every language.

## Why this way

- **No cloning of real or third-party voices.** Voices are *designed* from a
  written description with Parler-TTS (Apache-2.0). Parler's named speakers
  (Jon, Lea, ...) are real audiobook readers and are never used. The older
  chatterboxTTS "Nate"/"Derek" references are excerpts of ElevenLabs voices and
  are not used here (third-party voices; ElevenLabs terms).
- **One voice, many languages.** Chatterbox multilingual (MIT) clones a ~10 s
  reference and speaks 23 languages with it (en, de, es, fr, ru ...). For a
  language other than the reference's, `cfg_weight` 0 reduces accent carry-over
  (Resemble AI's guidance).
- **Audio first.** Narration decides each scene's length; the animatic and the
  shot plan follow it (docs/findings-and-risks.md B2). The characters' stitched
  mouths do not lip-sync, so any language fits the same pictures; plan scene
  length for the longest language.
- Outputs carry Resemble AI's imperceptible Perth watermark.

## Steps

```bash
cd /scratch/project_465002727/jelealro
W="env TWC_ENV=tts twc_video/lumi/run_in_container.sh"
# 1+2 (GPU task, ~40 min): design every candidate in voice/voices.yaml, audition them
TWC_ENV=tts sbatch --ntasks=1 --gpus-per-node=1 --mem=120G twc_video/lumi/run_tasks.sbatch twc_video/work/tasks_voices.txt
#   -> work/voices/<candidate>/{reference,audition_en}.wav
#   -> work/voices/audition_<role>.wav   all candidates of a role, a beep between them
# 3 listen, then make the choice canonical (copies into voice/cast/<role>/):
$W python twc_video/voice/voices.py pick --role leo --candidate leo_deep_warm_s201
# 4 narration for a story and language (GPU task):
$W python twc_video/voice/narrate.py --story lion_and_mouse_v2 --lang en
#   -> audio/<story>/<lang>/sceneNN.wav, lines/*.wav, timing.json
# 5 the animatic with that narration:
twc_video/lumi/run_in_container.sh python twc_video/production/animatic.py --story lion_and_mouse_v2 --lang en
```

Scripts per language: `stories/<slug>/narration/<lang>.yaml` (same scenes,
speakers and line order in every language). The canonical voices live in the
repo (`voice/cast/<role>/reference.wav` + `voice.yaml`), like the character
images: they define the cast.

Environment: `TWC_ENV=tts` (lumi/env_tts.sh): chatterbox-tts 0.1.6 and
parler-tts 0.2.2 on the container's ROCm torch 2.7.1, transformers 4.46.3,
protobuf 6 (descript-audiotools pins protobuf < 3.20, which breaks
s3tokenizer's onnx; its pin is ignored). Chatterbox's built-in `conds.pt` only
loads on a GPU node (it was saved on CUDA).
