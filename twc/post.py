#!/usr/bin/env python3
"""Learned post-processing for the Wan renders: interpolation, upscale, grade.

Wan renders 16 fps at 1280x720. Getting from there to 1080p30 was previously
ffmpeg's `minterpolate` (block matching, warps on fast motion) plus a lanczos
scale (soft). This module replaces both with learned models:

  * RIFE (IFNet, MIT, Megvii) for frame interpolation
  * Real-ESRGAN x4plus (BSD-3) for the upscale

Both licences are compatible with a monetised video, which rules out most of
the better-known alternatives.

RIFE here is the classic IFNet: it only produces the midpoint of a pair, so
arbitrary output timing is reached by recursive doubling (16 -> 128 fps) and
then sampling the nearest synthesised frame. At 128 fps the worst-case timing
error is 1/256 s, about a tenth of a frame at 30 fps.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

RIFE_REPO = "TensorForger/RIFE-safetensors"
RIFE_REV = "78a62b7c2dd910536432d6c2c3a25e76f14fbf78"          # pinned
ESRGAN_REPO = "Comfy-Org/Real-ESRGAN_repackaged"
ESRGAN_FILE = "RealESRGAN_x4plus.safetensors"
ESRGAN_REV = "5fd49b7b278836f48af63ecd314d0f98ab336105"        # pinned


def _ffmpeg() -> str:
    from twc.media import locate_ffmpeg
    return locate_ffmpeg()


def probe_size(path: Path) -> tuple[int, int]:
    out = subprocess.run([_ffmpeg(), "-hide_banner", "-i", str(path)],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Video:" in line:
            for token in line.split(","):
                token = token.strip().split(" ")[0]
                if "x" in token:
                    w, _, h = token.partition("x")
                    if w.isdigit() and h.isdigit():
                        return int(w), int(h)
    raise RuntimeError(f"could not read frame size of {path}")


def decode(path: Path) -> np.ndarray:
    """Whole clip as uint8 [N, H, W, 3]."""
    w, h = probe_size(path)
    raw = subprocess.run(
        [_ffmpeg(), "-v", "error", "-i", str(path), "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-"],
        capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w, 3)


def encode(frames: np.ndarray, path: Path, fps: int, crf: int = 12,
           vf: str | None = None) -> None:
    h, w = frames.shape[1:3]
    cmd = [_ffmpeg(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{w}x{h}", "-r", str(fps), "-i", "-"]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
            "-pix_fmt", "yuv420p", str(path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    proc.communicate(frames.tobytes())
    if proc.returncode:
        raise RuntimeError("ffmpeg encode failed")


# --------------------------------------------------------------------------- #
# RIFE
# --------------------------------------------------------------------------- #
def _load_rife(device):
    import torch
    from huggingface_hub import snapshot_download
    from safetensors.torch import load_file

    path = Path(snapshot_download(RIFE_REPO, revision=RIFE_REV))
    sys.path.insert(0, str(path))          # the repo ships its own IFNet
    import interpolation_model as im
    im.device = device                     # warp() reads these module globals
    im.dtype = torch.float16
    net = im.IFNet()
    net.load_state_dict(load_file(path / "flownet.safetensors"))
    return net.to(device).half().eval()


def _midpoints(net, frames: np.ndarray, device, batch: int = 4) -> np.ndarray:
    """Midpoint frame for every consecutive pair; returns N-1 frames."""
    import torch
    import torch.nn.functional as F

    n, h, w = frames.shape[0], frames.shape[1], frames.shape[2]
    ph, pw = (-h) % 64, (-w) % 64          # IFNet needs multiples of 64
    out = np.empty((n - 1, h, w, 3), dtype=np.uint8)

    with torch.no_grad():
        for start in range(0, n - 1, batch):
            stop = min(start + batch, n - 1)
            a = torch.from_numpy(np.ascontiguousarray(frames[start:stop]))
            b = torch.from_numpy(np.ascontiguousarray(frames[start + 1:stop + 1]))
            a = a.to(device).permute(0, 3, 1, 2).half() / 255.0
            b = b.to(device).permute(0, 3, 1, 2).half() / 255.0
            if ph or pw:
                a = F.pad(a, (0, pw, 0, ph), mode="replicate")
                b = F.pad(b, (0, pw, 0, ph), mode="replicate")
            mid = net(torch.cat([a, b], dim=1))
            mid = mid[:, :, :h, :w].clamp(0, 1).mul(255).round()
            out[start:stop] = mid.permute(0, 2, 3, 1).to(torch.uint8).cpu().numpy()
    return out


def interpolate(frames: np.ndarray, doublings: int, device) -> np.ndarray:
    """Recursively insert midpoints; N frames -> (N-1)*2**doublings + 1."""
    net = _load_rife(device)
    for level in range(doublings):
        mids = _midpoints(net, frames, device)
        merged = np.empty((len(frames) + len(mids),) + frames.shape[1:], dtype=np.uint8)
        merged[0::2] = frames
        merged[1::2] = mids
        frames = merged
        print(f"    interpolation pass {level + 1}/{doublings}: {len(frames)} frames",
              flush=True)
    return frames


def retime(frames: np.ndarray, src_fps: int, speed: float, out_fps: int,
           device, doublings: int = 3) -> np.ndarray:
    """Slow `frames` by `speed` and resample to `out_fps` using RIFE."""
    dense = interpolate(frames, doublings, device)
    dense_fps = src_fps * (2 ** doublings)
    n_out = int(round(len(frames) / src_fps * speed * out_fps))
    idx = np.round(np.arange(n_out) / out_fps / speed * dense_fps).astype(int)
    return dense[np.clip(idx, 0, len(dense) - 1)]


# --------------------------------------------------------------------------- #
# Real-ESRGAN
# --------------------------------------------------------------------------- #
def _load_esrgan(device):
    import torch
    from huggingface_hub import hf_hub_download
    from spandrel import ModelLoader

    path = hf_hub_download(ESRGAN_REPO, ESRGAN_FILE, revision=ESRGAN_REV)
    model = ModelLoader().load_from_file(path)
    return model.model.to(device).eval(), model.scale


def _upscale_tiled(net, img, device, tile: int = 384, overlap: int = 32):
    """Tile so a 4x upscale of a 720p frame fits comfortably in VRAM."""
    import torch

    c, h, w = img.shape
    scale = 4
    out = torch.zeros((c, h * scale, w * scale), device=device, dtype=img.dtype)
    weight = torch.zeros((1, h * scale, w * scale), device=device, dtype=img.dtype)
    step = tile - overlap
    with torch.no_grad():
        for y in range(0, h, step):
            for x in range(0, w, step):
                y0, x0 = min(y, max(h - tile, 0)), min(x, max(w - tile, 0))
                patch = img[:, y0:y0 + tile, x0:x0 + tile].unsqueeze(0)
                up = net(patch)[0]
                ys, xs = y0 * scale, x0 * scale
                out[:, ys:ys + up.shape[1], xs:xs + up.shape[2]] += up
                weight[:, ys:ys + up.shape[1], xs:xs + up.shape[2]] += 1
    return out / weight.clamp(min=1)


def upscale(frames: np.ndarray, out_w: int, out_h: int, device) -> np.ndarray:
    """Real-ESRGAN x4 then area-resample down to the delivery size."""
    import torch
    import torch.nn.functional as F

    net, scale = _load_esrgan(device)
    out = np.empty((len(frames), out_h, out_w, 3), dtype=np.uint8)
    with torch.no_grad():
        for i, frame in enumerate(frames):
            img = torch.from_numpy(np.ascontiguousarray(frame)).to(device)
            img = img.permute(2, 0, 1).float() / 255.0
            big = _upscale_tiled(net, img, device)
            small = F.interpolate(big.unsqueeze(0), size=(out_h, out_w),
                                  mode="area")[0]
            out[i] = (small.clamp(0, 1) * 255).round().permute(1, 2, 0) \
                     .to(torch.uint8).cpu().numpy()
            if (i + 1) % 50 == 0:
                print(f"    upscaled {i + 1}/{len(frames)}", flush=True)
    return out


# A restrained finish: light sharpening, a soft bloom on the brightest areas
# only, a touch of contrast and grain so gradients do not band.
#
# The bloom threshold and the saturation are deliberately conservative. The
# first version (0.62 knee, opacity 0.16, saturation 1.07) pushed the warm
# golden burst at the book opening towards magenta, because a screen blend over
# an already-clipped highlight drags in the surrounding violet.
GRADE_VF = (
    "unsharp=5:5:0.45:5:5:0.0,"
    "split[g_a][g_b];"
    "[g_b]gblur=sigma=14,curves=all='0/0 0.80/0.12 1/1'[g_bl];"
    "[g_a][g_bl]blend=all_mode=screen:all_opacity=0.09,"
    "eq=contrast=1.04:saturation=1.01:gamma=0.995,"
    "noise=alls=2:allf=t+u"
)


def grade(src: Path, dst: Path, vf: str = None, crf: int = 12) -> None:
    """Apply the look as its own cheap ffmpeg pass.

    Kept separate from the GPU pass on purpose: grading is taste, and baking it
    into the upscale meant every tweak cost a 20-minute job.
    """
    subprocess.run(
        [_ffmpeg(), "-y", "-v", "error", "-i", str(src), "-vf", vf or GRADE_VF,
         "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", str(dst)],
        check=True,
    )
