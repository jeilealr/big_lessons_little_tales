"""Sweep end-strength / noise / frame count on one transition to see what spreads the motion.

Usage: python sweep_seg.py <segment_index 1-5> <out_dir> [pipeline_config]
Writes <out_dir>/<name>_f<frames>_es<es>_n<noise>.mp4 for each combo.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/scratch/project_465002727/jelealro/LTX-Video")
import generate_intro_v3 as g

idx = int(sys.argv[1]) - 1
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
cfg = Path(sys.argv[3]) if len(sys.argv) > 3 else g.DEFAULT_CONFIG
seg = g.SEGMENTS[idx]
combos = [
    # frames, end_strength, noise
    (49, 0.92, 0.08),
    (49, 0.70, 0.08),
    (49, 0.50, 0.08),
    (49, 0.92, 0.20),
    (73, 0.70, 0.08),
    (97, 0.70, 0.08),
]
for frames, es, noise in combos:
    target = out / f"{seg['name']}_f{frames}_es{es}_n{noise}.mp4"
    if target.exists():
        print("skip", target); continue
    print(f"=== {seg['name']} frames={frames} end_strength={es} noise={noise}", flush=True)
    g.generate_segment(seg, g.DEFAULT_REFERENCE_DIR, target, out / "scratch", cfg,
                       width=512, height=288, num_frames=frames, fps=24,
                       seed=g.build_parser().get_default("seed") + idx + 1,
                       end_strength=es, noise_scale=noise)
    print("saved", target, flush=True)
print("SWEEP DONE")
