#!/bin/bash
# Train ONE expert's LoRA for a character.   bash lora/train_character.sh <name> <low|high> [steps]
#
# Wan 2.2 A14B has two experts. Training both in one run swaps 28 GB of
# weights between CPU and GPU whenever a step changes expert (~20 s per swap,
# measured); training each expert alone runs at ~2-3 s/step. So two tasks run
# in parallel, one per expert, on two GCDs. The `low` task builds the latent
# and text caches; the `high` task waits for them (a per-job ready file).
set -euo pipefail
source "$(dirname "$0")/musubi_env.sh"
NAME=$1; EXPERT=$2; STEPS=${3:-2000}
D=$ROOT/work/lora/$NAME
READY=$D/.cache_ready_${SLURM_JOB_ID:-manual}
mkdir -p $D/cache $D/out_$EXPERT
# (PMI/MPI variables are cleared in musubi_env.sh)
stamp() { echo "[$(date +%T)] [$NAME/$EXPERT] $*"; }

if [ "$EXPERT" = low ]; then
  cat > $D/dataset.toml <<TOML
[general]
resolution = [960, 544]
caption_extension = ".txt"
batch_size = 1
enable_bucket = true
bucket_no_upscale = false

[[datasets]]
image_directory = "$D/dataset"
cache_directory = "$D/cache"
num_repeats = 1
TOML
  stamp "cache latents"; python $MUSUBI/wan_cache_latents.py --dataset_config $D/dataset.toml --vae $VAE --skip_existing
  stamp "cache text";    python $MUSUBI/wan_cache_text_encoder_outputs.py --dataset_config $D/dataset.toml --t5 $T5 --batch_size 16 --skip_existing
  touch $READY
else
  stamp "waiting for the low-noise task to build the caches"
  until [ -f $READY ]; do sleep 20; done
fi

case $EXPERT in
  low)  DIT=$DIT_LOW;  TMIN=0;   TMAX=875 ;;
  high) DIT=$DIT_HIGH; TMIN=875; TMAX=1000 ;;
  *) echo "expert must be low or high"; exit 2 ;;
esac
# Resumable: full training state is saved every 250 steps (last two kept). If
# a job is killed, rerunning this script continues from the newest state.
RESUME=()
LAST=$(ls -d $D/out_$EXPERT/${NAME}_$EXPERT-step*-state 2>/dev/null | sort | tail -1 || true)
if [ -n "$LAST" ]; then RESUME=(--resume "$LAST"); stamp "resuming from $(basename $LAST)"; fi
stamp "train $STEPS steps (timesteps $TMIN-$TMAX)"
accelerate launch --num_processes 1 --num_machines 1 --mixed_precision bf16 --dynamo_backend no \
  --num_cpu_threads_per_process 1 $MUSUBI/wan_train_network.py \
  --task t2v-A14B --dit $DIT --min_timestep $TMIN --max_timestep $TMAX --preserve_distribution_shape \
  --dataset_config $D/dataset.toml --sdpa --mixed_precision bf16 \
  --optimizer_type adamw --learning_rate 2e-4 --gradient_checkpointing \
  --max_data_loader_n_workers 2 --persistent_data_loader_workers \
  --network_module networks.lora_wan --network_dim 32 --network_alpha 16 \
  --timestep_sampling shift --discrete_flow_shift 3.0 \
  --max_train_steps $STEPS --save_every_n_steps 250 --seed 42 \
  --save_state --save_last_n_steps_state 500 "${RESUME[@]}" \
  --output_dir $D/out_$EXPERT --output_name ${NAME}_$EXPERT
stamp "done"; ls -la $D/out_$EXPERT
