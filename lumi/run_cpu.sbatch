#!/bin/bash
#SBATCH --job-name=twc_cpu
#SBATCH --account=project_465002727
#SBATCH --partition=interactive
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/project_465002727/jelealro/slurm_logs/twc_cpu_%j.log
# CPU-only work (voices on the `interactive` partition: 1 job, 8 h max, usually
# starts in minutes; no GPU). Runs one command line in the container:
#   TWC_ENV=tts sbatch twc_video/lumi/run_cpu.sbatch python twc_video/voice/voices.py audition ...
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
exec /scratch/project_465002727/jelealro/twc_video/lumi/run_in_container.sh "$@"
