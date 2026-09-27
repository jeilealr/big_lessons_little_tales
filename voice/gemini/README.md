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

Every voice folder: `voice.yaml` (id, name, model, the exact design prompt,
expiry, notes) and `google_sample.wav` (the sample Google stores with the
voice; no audio was generated for it). Save a voice with
`python voice/gemini/save_voice.py --id <voice_id> --dir <folder> --role <role>`.

| Role | Voice | Folder |
|---|---|---|
| Leo | The Noble Lion 1 (`voice_zdbgqrcerxqu`) | `cast/leo/` |
| Milo | The Brave Little Mouse 1 (`voice_vf2w20rcys8a`) | `cast/milo/` |
| narrator (alternative) | The Fireside Grandfather 2 (`voice_4rdl7hydi35v`) | `narrators/fireside_grandfather_2/` |
| **narrator (Lion and Mouse v2)** | Moonlight Storyteller 1 (`voice_v5bpq98uj7qh`) | `narrators/moonlight_storyteller_1/` |
| narrator (alternative) | Golden Hour Storyteller 3 (`voice_g00mo8cbdefq`) | `narrators/golden_hour_storyteller_3/` |
| narrator (alternative) | The Cheery Tale Keeper 2 (`voice_8tnxrhfqk3ur`) | `narrators/cheery_tale_keeper_2/` |
| narrator (alternative) | Bright Trail Narrator 2 (`voice_tcrjw3ney7q8`) | `narrators/bright_trail_narrator_2/` |

`cast/` holds character voices; `narrators/` is the pool of narrator voices.
A story picks its voices in its `story.yaml` (`voices:`), e.g. the Lion and
Mouse v2 narrator is `narrators/moonlight_storyteller_1`. Samples:
`google_sample.wav` (Google's own) and `sample_scene*.wav` (story lines). All designed voices
expire on 2027-09-27: recreate each from its saved prompt before then.
