#!/bin/bash
# List the generated assets worth keeping, and print the command that copies
# them to your own computer. LUMI deletes project data around 30 March 2027 and
# work/ is not in git, so this is the only copy of designs, packs, shots, LoRAs.
#
#   bash lumi/backup_assets.sh            # from anywhere: writes the list, prints rsync
#   KEEP_STEPS="500 750" bash lumi/backup_assets.sh
#
# Kept: everything in work/ except LoRA training states, other checkpoints and
# latent caches; from each LoRA the final weights and the KEEP_STEPS
# checkpoints (default 500); every image under character/ (tracked or not) and
# the git-ignored Gemini candidates with their .json sidecars
# (character/**/gemini/). Model weights are re-downloadable (revisions pinned
# in feltwillow/wan.py) and not listed.
# Run the printed rsync on your computer (LUMI cannot connect out to it); it
# is incremental.
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/site.sh"
cd "$FELTWILLOW_REPO"
KEEP_STEPS=${KEEP_STEPS:-500}
LIST=work/backup_files.txt
{
  find work \( -path 'work/lora/*/out_*' -o -path 'work/lora/*/cache' \) -prune -o -type f -print
  for d in work/lora/*/out_*; do
    [ -d "$d" ] || continue
    for f in "$d"/*.safetensors; do      # final weights (checkpoints end in -stepNNNNNNNN)
      [ -f "$f" ] || continue
      case ${f##*/} in *-step[0-9]*.safetensors) ;; *) echo "$f" ;; esac
    done
    for s in $KEEP_STEPS; do ls "$d"/*-step"$(printf %08d "$s")".safetensors 2>/dev/null || true; done
  done
  find character -type f \( -name '*.png' -o -name '*.jpg' -o -path '*/gemini/*' \)
} | grep -v '^work/backup_files.txt$' | sort -u > "$LIST"
N=$(wc -l < "$LIST")
SIZE=$(tr '\n' '\0' < "$LIST" | du -ch --files0-from=- | tail -1 | cut -f1)
echo "$N files, $SIZE -> $FELTWILLOW_REPO/$LIST"
echo
echo "On your computer:"
echo "  rsync -av --files-from=:$FELTWILLOW_REPO/$LIST ${USER:-$(id -un)}@$FELTWILLOW_SSH_HOST:$FELTWILLOW_REPO/ ./$(basename "$FELTWILLOW_REPO")_backup/"
