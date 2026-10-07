#!/bin/bash
# Render every shot of a runtime story in fast mode on dev-g, unattended.
#   setsid nohup bash lumi/render_story.sh lion_and_mouse_v5 > $FELTWILLOW_PROJECT/tmp/render_v5.log 2>&1 &
# Round 1: PER_TASK shots per GPU task, 4 tasks per job (host RAM limit), jobs
# submitted while dev-g has fewer than 2 of the user's jobs (pending ones count).
# Catch-up rounds: every shot still missing a seed, one shot per task (a task
# that hit the 3 h limit, or a failure). shot.py skips seeds already rendered.
# Task files: work/tasks/<story>_*.txt. Waits on squeue, never kills anything.
set -uo pipefail
STORY=${1:?story slug}
PER_TASK=${PER_TASK:-3}
cd "$(dirname "$0")/.."
source lumi/site.sh
NAME=feltwillow_${STORY##*_}           # e.g. feltwillow_v5

missing() {   # one shot.py command per shot that lacks a seed
python3 - "$STORY" <<'PY'
import sys, yaml
from pathlib import Path
story = sys.argv[1]
y = yaml.safe_load(open(f"stories/{story}/story.yaml"))
d = Path(f"work/stories/{story}/shots")
for n, sc in y["scenes"].items():
    for s in sc["shots"]:
        if any(not (d / f"{s['name']}_s{k}_fast.mp4").is_file() for k in s["seeds"]):
            print(f"python production/shot.py --story {story} --scene {n} --shot {s['name']} --fast")
PY
}

submit_all() {   # $1 = shots per task line; submits part files as slots open
  local per=$1 part f k
  rm -f work/tasks/${STORY}_part_*
  missing | paste -d';' $(printf -- '- %.0s' $(seq "$per")) | sed 's/;;*$//; s/;/ ; /g' > work/tasks/${STORY}_lines.txt
  split -l 4 -d work/tasks/${STORY}_lines.txt work/tasks/${STORY}_part_
  for f in work/tasks/${STORY}_part_*; do
    while [ "$(squeue -u "$USER" -h -p dev-g | wc -l)" -ge 2 ]; do sleep 60; done
    k=$(grep -c . "$f")
    sbatch --ntasks="$k" --gpus-per-node="$k" --mem=$((k * 110))G -J "$NAME" lumi/run_tasks.sbatch "$f"
    sleep 30
  done
  while squeue -u "$USER" -h -o %j | grep -qx "$NAME"; do sleep 60; done
}

echo "$(date '+%F %T') $(missing | wc -l) shots to render"
submit_all "$PER_TASK"
for round in 1 2; do
  n=$(missing | wc -l)
  echo "$(date '+%F %T') after round $round: $n shots still missing a seed"
  [ "$n" -eq 0 ] && break
  submit_all 1
done
echo "$(date '+%F %T') done: $(missing | wc -l) shots missing"
