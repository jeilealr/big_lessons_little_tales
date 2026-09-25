"""720p seed sweep on transition 1 with the script's (focused) prompt, 13B.
Usage: python sweep_seg1_720p.py <out_dir>
"""
import sys
from pathlib import Path
sys.path.insert(0, "/scratch/project_465002727/jelealro/LTX-Video")
import generate_intro_v3 as g

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
cfg = g.REPO_ROOT / "configs" / "twc-13b-0.9.8-distilled.yaml"
seg = g.SEGMENTS[0]
for seed, noise in [(20260922, 0.08), (7, 0.15), (123, 0.15)]:
    target = out / f"seg1_seed{seed}_n{noise}.mp4"
    if target.exists():
        print("skip", target); continue
    print(f"=== seed={seed} noise={noise}", flush=True)
    g.generate_segment(seg, g.DEFAULT_REFERENCE_DIR, target, out / "scratch", cfg,
                       width=1280, height=720, num_frames=49, fps=24, seed=seed,
                       end_strength=0.7, noise_scale=noise)
    print("saved", target, flush=True)
print("SWEEP DONE")
