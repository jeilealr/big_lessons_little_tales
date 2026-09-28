#!/usr/bin/env python3
"""Make a still image from reference images and an instruction (image editing).

Qwen-Image-Edit-2511 (Apache-2.0): up to 3 reference images, e.g. an owner-made
scene plus a character canonical. It changes what the prompt says and keeps
the rest. For missing story stills (a new state of a character in a scene),
not for animation.

  python production/edit_image.py --images SCENE.png [CHAR.png ...] \\
      --prompt "..." --out work/.../name.png [--seeds 1 2 3] [--steps 40]

Output: <out stem>_s<seed>.png per seed + .json sidecar (prompt, refs, seed,
model revision). The size follows the first image (rounded to multiples of 16).
GPU: one task (~20B model with CPU offload; host RAM ~100 GB).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bllt import paths  # noqa: E402

MODEL = ("Qwen/Qwen-Image-Edit-2511", "6f3ccc0b56e431dc6a0c2b2039706d7d26f22cb9")
NEGATIVE = ("photorealistic, realistic animal fur, plastic, glossy CGI, text, letters, "
            "watermark, logo, deformed, extra limbs, extra tails, duplicate character, "
            "blurry, low quality, teeth, fangs, scary, angry")


def main() -> None:
    import torch
    from diffusers import QwenImageEditPlusPipeline
    from PIL import Image

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--images", nargs="+", type=Path, required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seeds", nargs="+", type=int, default=[1])
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--cfg", type=float, default=4.0)
    args = ap.parse_args()

    refs = [Image.open(p).convert("RGB") for p in args.images]
    w, h = refs[0].size
    scale = min(1.0, (1536 * 1024 / (w * h)) ** 0.5)          # keep ~1.5 MP
    w, h = int(w * scale) // 16 * 16, int(h * scale) // 16 * 16
    out = args.out if args.out.is_absolute() else paths.REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    todo = [s for s in args.seeds if not out.with_name(f"{out.stem}_s{s}.png").is_file()]
    if not todo:
        print("all seeds exist"); return
    pipe = QwenImageEditPlusPipeline.from_pretrained(MODEL[0], revision=MODEL[1],
                                                     torch_dtype=torch.bfloat16)
    pipe.enable_model_cpu_offload()
    print("model loaded", flush=True)
    for seed in todo:
        t0 = time.time()
        img = pipe(image=refs, prompt=args.prompt, negative_prompt=NEGATIVE,
                   true_cfg_scale=args.cfg, num_inference_steps=args.steps, width=w, height=h,
                   generator=torch.Generator("cpu").manual_seed(seed)).images[0]
        f = out.with_name(f"{out.stem}_s{seed}.png")
        img.save(f)
        f.with_suffix(".json").write_text(json.dumps(dict(
            stage="edit_image", model=f"{MODEL[0]}@{MODEL[1]}", seed=seed, prompt=args.prompt,
            negative=NEGATIVE, references=[str(p) for p in args.images], size=[w, h],
            steps=args.steps, cfg=args.cfg, seconds=round(time.time() - t0)), indent=2))
        print(f"saved {f} ({time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
