#!/bin/bash
# Evaluate a character LoRA as a grid of stills.
#   bash lora/eval_character.sh <name> <step|final|base> ...
# Same prompts and seeds for every checkpoint; `base` renders without a LoRA,
# describing the character with its full text sheet instead of the trigger word.
set -euo pipefail
source "$(dirname "$0")/musubi_env.sh"
NAME=$1; shift
D=$ROOT/twc_video/work/lora/$NAME
mkdir -p $D/eval
# Wait for training to finish (both final LoRAs) so this can be queued together
# with the training job and start the moment the weights exist.
until [ -f $D/out_low/${NAME}_low.safetensors ] && [ -f $D/out_high/${NAME}_high.safetensors ]; do
  echo "[$(date +%T)] waiting for final $NAME LoRAs"; sleep 120
done
python - "$NAME" <<'PY'
import sys, yaml
from pathlib import Path
name = sys.argv[1]
root = Path("/scratch/project_465002727/jelealro/twc_video")
cfg = yaml.safe_load((root / "lora" / "datasets" / f"{name}.yaml").read_text())
e = cfg["eval"]
out = root / "work" / "lora" / name / "eval"
neg = "plastic, realistic animal fur, photorealistic, text, watermark, deformed, extra limbs, blurry, low quality"
for tag, ident in (("lora", f"{cfg['trigger']}, {cfg['identity']}"), ("base", e["baseline_identity"])):
    lines = [f"{ident}, {p}, {cfg['style']} --w 960 --h 544 --f 1 --d {e['seed']} --s {e['steps']} --n {neg}"
             for p in e["prompts"]]
    (out / f"prompts_{tag}.txt").write_text("\n".join(lines) + "\n")
print("prompt files written")
PY
for CK in "$@"; do
  if [ "$CK" = base ]; then
    LORA=(); PROMPTS=$D/eval/prompts_base.txt
  else
    SUF=$([ "$CK" = final ] && echo "" || printf -- "-step%08d" "$CK")
    LORA=(--lora_weight $D/out_low/${NAME}_low$SUF.safetensors --lora_weight_high_noise $D/out_high/${NAME}_high$SUF.safetensors)
    PROMPTS=$D/eval/prompts_lora.txt
  fi
  echo "[$(date +%T)] eval $CK"
  python $MUSUBI/wan_generate_video.py --task t2v-A14B --dit $DIT_LOW --dit_high_noise $DIT_HIGH \
    --vae $VAE --t5 $T5 --attn_mode sdpa --blocks_to_swap 10 --lazy_loading \
    "${LORA[@]}" --from_file $PROMPTS --output_type images --save_path $D/eval/$CK
  echo "[$(date +%T)] eval $CK done: $(ls $D/eval/$CK | wc -l) files"
done
