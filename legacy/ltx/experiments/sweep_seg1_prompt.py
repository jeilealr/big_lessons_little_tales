"""Full-res seed x prompt sweep on transition 1 (book awakens): the one transition
that still morphs instead of opening. Writes clips + a contact sheet per clip.

Usage: python sweep_seg1_prompt.py <out_dir> [pipeline_config]
"""
import copy, sys
from pathlib import Path

sys.path.insert(0, "/scratch/project_465002727/jelealro/LTX-Video")
import generate_intro_v3 as g

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
cfg = Path(sys.argv[2]) if len(sys.argv) > 2 else g.DEFAULT_CONFIG
base = g.SEGMENTS[0]

PROMPTS = {
    "orig": base["prompt"],
    # One physical action, described in order, nothing else competing for the 2 s.
    "focus": (
        "Slow cinematic push-in on an ornate closed book resting on a wooden desk in "
        "a candlelit library. The glowing TWC emblem on the front cover pulses gently. "
        "The front cover slowly lifts by itself and swings open like a door, hinging "
        "on the spine, revealing bright pages inside. Warm golden light spills out from "
        "between the pages as the cover opens. Loose illustrated pages begin to lift "
        "out of the open book and float upward, with blue and violet magical particles "
        "gathering around it. Smooth, continuous, realistic motion. The book stays on "
        "the desk in the same position; same book, same cover design, same emblem "
        "throughout."
    ),
}
SEEDS = [20260922, 7, 123]

for pname, prompt in PROMPTS.items():
    seg = copy.deepcopy(base); seg["prompt"] = prompt
    for seed in SEEDS:
        target = out / f"seg1_{pname}_seed{seed}.mp4"
        if target.exists():
            print("skip", target); continue
        print(f"=== prompt={pname} seed={seed}", flush=True)
        g.generate_segment(seg, g.DEFAULT_REFERENCE_DIR, target, out / "scratch", cfg,
                           width=768, height=432, num_frames=49, fps=24, seed=seed,
                           end_strength=0.7, noise_scale=0.15)
        print("saved", target, flush=True)
print("SWEEP DONE")
