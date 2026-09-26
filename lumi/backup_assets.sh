#!/bin/bash
# List the generated assets worth keeping, and print the command that copies
# them to your own computer. LUMI deletes project data around 30 March 2027 and
# work/ is not in git, so this is the only copy of designs, packs, LoRAs, shots.
#
#   bash twc_video/lumi/backup_assets.sh            # write the list, print the command
#   KEEP_STEPS="500 750" bash twc_video/lumi/backup_assets.sh
#
# Kept: everything in work/ except LoRA training outputs and latent caches, plus from each LoRA
# the final weights and the checkpoints in KEEP_STEPS (default 500). Not kept:
# optimizer states (*-state, ~1 GB each), the other checkpoints, model weights
# (re-downloadable at the revisions pinned in twc/wan.py). Channel videos in
# Intro/ are included.
#
# Run the printed rsync on your computer (LUMI cannot connect out to it). It is
# incremental: re-running copies only what changed.
set -euo pipefail
ROOT=/scratch/project_465002727/jelealro
cd $ROOT
KEEP_STEPS=${KEEP_STEPS:-500}
LIST=twc_video/work/backup_files.txt

{
  find twc_video/work \( -path 'twc_video/work/lora/*/out_*' -o -path 'twc_video/work/lora/*/cache' \) -prune -o -type f -print
  for d in twc_video/work/lora/*/out_*; do
    ls $d/*.safetensors 2>/dev/null | grep -v -- '-step' || true
    for s in $KEEP_STEPS; do ls $d/*-step$(printf %08d $s).safetensors 2>/dev/null || true; done
  done
  find Intro -maxdepth 1 -type f \( -name '*.mov' -o -name '*.mp4' -o -name '*.png' -o -name '*.json' \)
} | grep -v "/lora/smoke/" | sort -u > $LIST

N=$(wc -l < $LIST)
SIZE=$(tr '\n' '\0' < $LIST | du -ch --files0-from=- | tail -1 | cut -f1)
echo "$N files, $SIZE -> $LIST"
echo
echo "On your computer:"
echo "  rsync -av --files-from=:$ROOT/$LIST $USER@lumi.csc.fi:$ROOT/ ./twc_backup/"
