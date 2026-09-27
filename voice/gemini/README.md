# Gemini 3.8 Flash TTS voices

Owner's choice (2026-09-27) for narration and character voices; the Chatterbox
tools in `voice/` are paused. Gemini runs on Google's servers: no GPU, no LUMI
job; any login-node shell works.

## Setup (once)

1. API key, stored by the owner outside every repo:
   ```
   mkdir -p ~/.config/gemini && chmod 700 ~/.config/gemini
   read -s -p "Gemini API key: " K && printf 'GEMINI_API_KEY=%s\n' "$K" > ~/.config/gemini/env && chmod 600 ~/.config/gemini/env && unset K
   ```
2. Client: `/scratch/project_465002727/jelealro/gemini_env/venv` (google-genai
   2.25.0; voice design needs >= 2.25.0).

## Use

```bash
cd /scratch/project_465002727/jelealro
source twc_video/voice/gemini/gemini_env.sh
python twc_video/voice/gemini/list_voices.py      # -> voices_list.json
```

## Facts (checked 2026-09-27; see CLAUDE.md for sources)

- Models: `gemini-3.8-flash-tts` (quality), `gemini-3.8-flash-lite-tts`.
- Designed ("prompted") voices: stored per project, **200 voices max, 1-year
  TTL**. Keep each chosen voice's prompt and id here so it can be recreated.
- Price (paid tier): ~$0.0135 per minute of audio until 2026-12-31, ~$0.027
  from 2027 (25 audio tokens/s). Free tier: rate-limited.
- Outputs are the owner's ("Google won't claim ownership"); SynthID watermark.
- Open question for Google: API terms exclude services "directed towards or
  likely to be accessed by individuals under the age of 18".

## Cast

| Role | Voice | File |
|---|---|---|
| narrator | Golden Hour Storyteller 3 (`voice_g00mo8cbdefq`) | `cast/narrator/voice.yaml` |

Each `voice.yaml` keeps the id, the exact design prompt (Google deletes
designed voices after a year) and a reference sample to compare a recreated
voice against.
