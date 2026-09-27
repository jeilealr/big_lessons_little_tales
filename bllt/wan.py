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
# Hugging Face repos can change under the same name; a pinned commit keeps a
# seed reproducible. Update deliberately, and note it in docs/findings-and-risks.md.
REVISIONS = {
    "i2v": "596658fd9ca6b7b71d5057529bbf319ecbc61d74",
    "t2v": "5be7df9619b54f4e2667b2755bc6a756675b5cd7",
}
# Wan2.2-Lightning (lightx2v, Apache-2.0): 4-step distillation LoRAs for I2V
# A14B. Reference settings (their ComfyUI workflow): 4 Euler steps, shift 5,
# CFG 1 (no negative pass), high-noise expert steps 0-2, low-noise 2-4, which is
# what boundary_ratio 0.9 gives with these timesteps (1000, 937 | 833, 625).
LIGHTNING = dict(
    repo="lightx2v/Wan2.2-Lightning", revision="18bccf8884ec0a078eed79785eb4ef13ea16ce1e",
    folder="Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1",
    render=dict(steps=4, guidance=1.0, guidance_2=1.0), shift=5.0,
)
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


def model_id(kind: str) -> str:
    """`repo@commit`, for sidecars."""
    return f"{MODELS[kind]}@{REVISIONS[kind]}"


def lightning_lora() -> dict:
    from huggingface_hub import hf_hub_download

    L = LIGHTNING
    get = lambda f: Path(hf_hub_download(L["repo"], f"{L['folder']}/{f}", revision=L["revision"]))
    return dict(name="lightning", high=get("high_noise_model.safetensors"),
                low=get("low_noise_model.safetensors"), weight=1.0)


def load(kind: str, frames: int = NATIVE_FRAMES, loras: list[dict] | None = None,
         fast: bool = False):
    """`loras`: [{name, high, low, weight}], musubi-tuner files (one per expert).

    A LoRA trained on T2V A14B loads into I2V A14B too: it only touches the
    attention and FFN layers, which have the same shapes in both (checked: all
    400 targets exist in both experts). diffusers' `transformer` is the
    high-noise expert, `transformer_2` the low-noise one. musubi's alpha/rank is
    folded into the weights by the converter, so an adapter weight of 1.0 means
    "as trained".
    """
    import torch
    from diffusers import AutoencoderKLWan, WanImageToVideoPipeline, WanPipeline

    repo, rev = MODELS[kind], REVISIONS[kind]
    vae = AutoencoderKLWan.from_pretrained(repo, subfolder="vae", revision=rev,
                                           torch_dtype=torch.float32)
    cls = WanImageToVideoPipeline if kind == "i2v" else WanPipeline
    pipe = cls.from_pretrained(repo, vae=vae, revision=rev, torch_dtype=torch.bfloat16)
    if fast:                                   # 4-step Lightning (see LIGHTNING)
        from diffusers import FlowMatchEulerDiscreteScheduler

        loras = [*(loras or []), lightning_lora()]
        pipe.scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000,
                                                         shift=LIGHTNING["shift"])
    if loras:
        for lo in loras:
            for path, second in ((Path(lo["high"]), False), (Path(lo["low"]), True)):
                pipe.load_lora_weights(str(path.parent), weight_name=path.name,
                                       adapter_name=lo["name"], load_into_transformer_2=second)
        names, weights = [lo["name"] for lo in loras], [lo.get("weight", 1.0) for lo in loras]
        pipe.transformer.set_adapters(names, weights)
        pipe.transformer_2.set_adapters(names, weights)
        for part in ("transformer", "transformer_2"):     # assert, don't assume
            layers = [m for m in getattr(pipe, part).modules() if hasattr(m, "lora_A")]
            active = {n for m in layers for n in m.lora_A.keys()}
            if len(layers) < 400 or not set(names) <= active:
                raise RuntimeError(f"LoRA not applied to {part}: {len(layers)} layers, {active}")
            print(f"LoRA {names} on {part}: {len(layers)} layers", flush=True)
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
