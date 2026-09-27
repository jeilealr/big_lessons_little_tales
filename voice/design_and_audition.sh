#!/bin/bash
# One GPU task: design every candidate voice, then audition them all.
#   TWC_ENV=tts sbatch --ntasks=1 --gpus-per-node=1 --mem=120G lumi/run_tasks.sbatch <file with this line>
set -e
python "$(dirname "$0")/voices.py" design
python "$(dirname "$0")/voices.py" audition
