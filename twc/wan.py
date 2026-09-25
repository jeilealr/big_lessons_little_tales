"""Wan 2.2 (A14B, mixture of experts) through diffusers.

Everything learned running it on LUMI lives here:

* Only the I2V-A14B pipeline honours `last_image`. The TI2V-5B path
  (`expand_timesteps`) silently drops it, so first+last keyframing needs A14B.
* Two 14B experts plus the 11B text encoder do not fit one 64 GB MI250X GCD:
  weights are offloaded per module (`enable_model_cpu_offload`), which needs
  ~80-100 GB of host RAM per process.
* The Hugging Face repos ship fp32; loading converts to bf16 (10-20 min).
* Clips are 4k+1 frames at 16 fps. 81 frames is the native length; longer
  clips cost quadratically in attention (97 frames ran ~250 s/step and could
  not finish inside a 3 h dev-g job), and need VAE tiling to decode.
* Guidance is a pair: high-noise expert, low-noise expert.
  I2V default (3.5, 3.5); T2V default (4.0, 3.0).
"""

from __future__ import annotations

from pathlib import Path

MODELS = {
    "i2v": "Wan-AI/Wan2.2-I2V-A14B-Diffusers",
    "t2v": "Wan-AI/Wan2.2-T2V-A14B-Diffusers",
}
NATIVE_FRAMES = 81
FPS = 16


def check_frames(n: int) -> None:
    if (n - 1) % 4:
        raise ValueError(f"Wan needs 4k+1 frames, got {n}")


def fit(image, width: int, height: int):
    """Centre-crop a PIL image to the target aspect, then resize."""
    from PIL import Image

    w, h = image.size
    target = width / height
    if w / h > target:
        nw = int(round(h * target))
        image = image.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < target:
        nh = int(round(w / target))
        image = image.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return image.convert("RGB").resize((width, height), Image.LANCZOS)


def load(kind: str, frames: int = NATIVE_FRAMES):
    import torch
    from diffusers import AutoencoderKLWan, WanImageToVideoPipeline, WanPipeline

    repo = MODELS[kind]
    vae = AutoencoderKLWan.from_pretrained(repo, subfolder="vae", torch_dtype=torch.float32)
    cls = WanImageToVideoPipeline if kind == "i2v" else WanPipeline
    pipe = cls.from_pretrained(repo, vae=vae, torch_dtype=torch.bfloat16)
    pipe.enable_model_cpu_offload()
    if frames > NATIVE_FRAMES:
        pipe.vae.enable_tiling()
    return pipe


def generate(pipe, prompt: str, *, negative: str, width: int, height: int, frames: int,
             steps: int, guidance: float, guidance_2: float, seed: int,
             image=None, last_image=None):
    """Returns a list of PIL frames. `image`/`last_image` only for I2V."""
    import torch

    check_frames(frames)
    kwargs = dict(prompt=prompt, negative_prompt=negative, height=height, width=width,
                  num_frames=frames, num_inference_steps=steps, guidance_scale=guidance,
                  guidance_scale_2=guidance_2,
                  generator=torch.Generator(device="cpu").manual_seed(seed))
    if image is not None:
        kwargs["image"] = fit(image, width, height)
    if last_image is not None:
        kwargs["last_image"] = fit(last_image, width, height)
    return pipe(**kwargs).frames[0]


def save(frames, path: Path, fps: int = FPS) -> None:
    from diffusers.utils import export_to_video

    path.parent.mkdir(parents=True, exist_ok=True)
    export_to_video(frames, str(path), fps=fps)
