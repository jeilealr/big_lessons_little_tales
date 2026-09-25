#!/bin/bash
# Only the last stage of musubi_smoke.sh: render a short clip with the trained smoke LoRA.
set -euo pipefail
source "$(dirname "$0")/musubi_env.sh"
OUT=$ROOT/twc_video/work/lora/smoke
CAPTION="twcfox, a small orange felt fox standing on a green felt meadow with felt hills, side view, full body, handmade felt stop-motion animation"
t0=$(date +%s); echo "[$(date +%T)] generate with the LoRA (480x832, 17 frames, 12 steps)"
python $MUSUBI/wan_generate_video.py --task t2v-A14B --dit $DIT_LOW --dit_high_noise $DIT_HIGH \
  --vae $VAE --t5 $T5 --attn_mode sdpa --blocks_to_swap 10 --lazy_loading \
  --prompt "$CAPTION" --video_size 480 832 --video_length 17 --infer_steps 12 --seed 42 \
  --lora_weight $OUT/out/smoke.safetensors --lora_weight_high_noise $OUT/out/smoke.safetensors \
  --save_path $OUT/generated
echo "[$(date +%T)] generation took $(( $(date +%s) - t0 )) s"; ls -la $OUT/*.mp4
echo "[$(date +%T)] SMOKE TEST PASSED"
