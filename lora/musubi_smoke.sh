#!/bin/bash
# End-to-end check of Wan 2.2 LoRA training on ONE GCD, before any long run:
# cache latents -> cache text -> train 10 steps (both experts) -> save -> generate.
# Every stage is timed; the numbers size the real training job.
set -euo pipefail
source "$(dirname "$0")/musubi_env.sh"
OUT=$ROOT/twc_video/work/lora/smoke
FOX=$ROOT/twc_video/work/characters/fox
mkdir -p $OUT/images $OUT/cache
CAPTION="twcfox, a small orange felt fox standing on a green felt meadow with felt hills, side view, full body, handmade felt stop-motion animation"
cp $FOX/canonical.png $OUT/images/fox_canonical.png; echo "$CAPTION" > $OUT/images/fox_canonical.txt
for k in 0 1 2 3 4; do cp $FOX/angles/angle_$k.png $OUT/images/fox_angle_$k.png; echo "$CAPTION" > $OUT/images/fox_angle_$k.txt; done
cat > $OUT/dataset.toml <<TOML
[general]
resolution = [960, 544]
caption_extension = ".txt"
batch_size = 1
enable_bucket = true
bucket_no_upscale = false

[[datasets]]
image_directory = "$OUT/images"
cache_directory = "$OUT/cache"
num_repeats = 1
TOML
stamp() { echo "[$(date +%T)] $*"; }
t0=$(date +%s)
stamp "cache latents";   python $MUSUBI/wan_cache_latents.py --dataset_config $OUT/dataset.toml --vae $VAE --skip_existing
stamp "cache text";      python $MUSUBI/wan_cache_text_encoder_outputs.py --dataset_config $OUT/dataset.toml --t5 $T5 --batch_size 16 --skip_existing
t1=$(date +%s); stamp "caching took $((t1 - t0)) s"
stamp "train 10 steps (both experts)"
accelerate launch --num_processes 1 --num_machines 1 --mixed_precision bf16 --dynamo_backend no \
  --num_cpu_threads_per_process 1 $MUSUBI/wan_train_network.py \
  --task t2v-A14B --dit $DIT_LOW --dit_high_noise $DIT_HIGH --timestep_boundary 875 \
  --dataset_config $OUT/dataset.toml --sdpa --mixed_precision bf16 \
  --optimizer_type adamw --learning_rate 2e-4 --gradient_checkpointing \
  --max_data_loader_n_workers 2 --persistent_data_loader_workers \
  --network_module networks.lora_wan --network_dim 32 --network_alpha 16 \
  --timestep_sampling shift --discrete_flow_shift 3.0 \
  --max_train_steps 10 --save_every_n_steps 10 --seed 42 --offload_inactive_dit \
  --output_dir $OUT/out --output_name smoke
t2=$(date +%s); stamp "training took $((t2 - t1)) s"; ls -la $OUT/out
stamp "generate with the LoRA (480x832, 17 frames, 12 steps)"
python $MUSUBI/wan_generate_video.py --task t2v-A14B --dit $DIT_LOW --dit_high_noise $DIT_HIGH \
  --vae $VAE --t5 $T5 --attn_mode sdpa --blocks_to_swap 10 --lazy_loading \
  --prompt "$CAPTION" --video_size 480 832 --video_length 17 --infer_steps 12 --seed 42 \
  --lora_weight $OUT/out/smoke.safetensors --lora_weight_high_noise $OUT/out/smoke.safetensors \
  --save_path $OUT/generated
t3=$(date +%s); stamp "generation took $((t3 - t2)) s"; ls -la $OUT/*.mp4 2>/dev/null
stamp "SMOKE TEST PASSED in $((t3 - t0)) s"
