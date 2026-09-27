#!/bin/bash
# Young Leo / Milo candidates: design (Parler, eager attention) then audition.
bash "$(dirname "$0")/tts_task.sh" design --roles leo_young milo_young
bash "$(dirname "$0")/tts_task.sh" audition --roles leo_young milo_young
