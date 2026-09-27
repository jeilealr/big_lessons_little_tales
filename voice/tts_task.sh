#!/bin/bash
# Run a voice command as one task of a video job (lumi/run_tasks.sbatch runs
# every line in the default venv; this switches to the tts venv first).
#   line in a task file:  bash twc_video/voice/tts_task.sh design --roles leo_young milo_young
source "$(dirname "$0")/../lumi/env_tts.sh"
set -e
python "$(dirname "$0")/voices.py" "$@"
