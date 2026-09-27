#!/bin/bash
# List the generated assets worth keeping, and print the command that copies
# them to your own computer. LUMI deletes project data around 30 March 2027 and
# work/ is not in git, so this is the only copy of designs, packs, shots, LoRAs.
#
#   bash lumi/backup_assets.sh            # from the repo root: writes the list, prints rsync
#   KEEP_STEPS="500 750" bash lumi/backup_assets.sh
#
# Kept: everything in work/ except LoRA training states, other checkpoints and
# latent caches; from each LoRA the final weights and the KEEP_STEPS
# checkpoints (default 500). Model weights are re-downloadable (revisions
# pinned in bllt/wan.py) and not listed.
# Run the printed rsync on your computer (LUMI cannot connect out to it); it
# is incremental.
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/site.sh"
cd "$BLLT_REPO"
KEEP_STEPS=${KEEP_STEPS:-500}
LIST=work/backup_files.txt
{
  find work \( -path 'work/lora/*/out_*' -o -path 'work/lora/*/cache' \) -prune -o -type f -print
  for d in work/lora/*/out_*; do
    [ -d "$d" ] || continue
    ls $d/*.safetensors 2>/dev/null | grep -v -- '-step' || true
    for s in $KEEP_STEPS; do ls $d/*-step$(printf %08d $s).safetensors 2>/dev/null || true; done
  done
  find character -type f \( -name '*.png' -o -name '*.jpg' \)            # owner-made character packs
} | grep -v '^work/backup_files.txt$' | sort -u > $LIST
N=$(wc -l < $LIST)
SIZE=$(tr '\n' '\0' < $LIST | du -ch --files0-from=- | tail -1 | cut -f1)
echo "$N files, $SIZE -> $BLLT_REPO/$LIST"
echo
echo "On your computer:"
echo "  rsync -av --files-from=:$BLLT_REPO/$LIST $USER@lumi.csc.fi:$BLLT_REPO/ ./$(basename "$BLLT_REPO")_backup/"
