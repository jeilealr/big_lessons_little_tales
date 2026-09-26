#!/usr/bin/env python3
"""Compose a shot's first frame: characters cut from their pose stills, placed
into a location plate.

Why: image-to-video keeps what is in the first frame. If that frame already
holds the exact character (from its canonical or a pose clip) in the exact
place (the location plate), the shot starts on-model and on-set, which text
alone cannot guarantee.

Cut-out: every pose is shot on the plain design backdrop, so the matte is
"differs from the backdrop colour" (estimated from the image border), refined
with GrabCut and feathered. Placement: the character's feet go to (x, y) in
the plate, scaled to a height given as a fraction of the frame. A soft contact
shadow grounds it, and its colours are pulled slightly towards the plate's
lighting so it does not look pasted on.

  python production/keyframe.py --plate PLATE.png --out KEY.png \\
      --char STILL.png:x=0.5,y=0.82,h=0.45[,flip]  [--char ...]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


BIREFNET = ("ZhengPeng7/BiRefNet", "e2bf8e4460fc8fa32bba5ea4d94b3233d367b0e4")   # MIT; pinned
_birefnet = None


def matte(img: np.ndarray) -> np.ndarray:
    """Soft alpha (0..1) of the character.

    BiRefNet (MIT licence, revision pinned because it runs remote code) is a
    learned matting model: it keeps a grey mouse whole against a grey-green
    backdrop and preserves thin tails and wispy felt, where colour keying cut
    holes. Falls back to the colour key if the model cannot be loaded.
    """
    global _birefnet
    try:
        import torch
        from torchvision import transforms
        from transformers import AutoModelForImageSegmentation

        if _birefnet is None:
            _birefnet = AutoModelForImageSegmentation.from_pretrained(
                BIREFNET[0], trust_remote_code=True, revision=BIREFNET[1]).eval().float()
            if torch.cuda.is_available():
                _birefnet = _birefnet.cuda()
        dev = next(_birefnet.parameters()).device
        tf = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(),
                                 transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        with torch.no_grad():
            pred = _birefnet(tf(Image.fromarray(img))[None].to(dev))[-1].sigmoid()[0, 0].cpu().numpy()
        return cv2.resize(pred, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)
    except Exception as err:                        # pragma: no cover
        print(f"BiRefNet unavailable ({type(err).__name__}: {err}); using the colour key")
        return matte_colour_key(img)


def matte_colour_key(img: np.ndarray, t_lo: float = 8.0, t_hi: float = 18.0) -> np.ndarray:
    """Soft alpha (0..1) for a character on the plain design backdrop.

    Measured on the design stills: backdrop chroma (Lab a/b distance from the
    per-row backdrop colour, sampled at the left and right edges) stays below
    ~3, while the characters sit at 20-60. So chroma alone separates them, and
    the character's shadow on the floor (darker, same hue) never qualifies.
    The alpha is a soft ramp between t_lo and t_hi, which keeps the felt's
    wispy fibres semi-transparent instead of cutting them into a hard edge.
    No GrabCut: it pulled floor and backdrop fringe in with the subject.
    Interior pixels close to the backdrop colour (a cream muzzle, a grey belly)
    are kept by filling holes in the solid core.
    """
    h, w = img.shape[:2]
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB).astype(np.float32)
    k = max(8, w // 20)
    bg = np.median(np.concatenate([lab[:, :k], lab[:, -k:]], axis=1), axis=1)
    bg = cv2.GaussianBlur(bg[:, None, :], (1, 0), sigmaX=0.1, sigmaY=6)[:, 0, :]
    d = lab - bg[:, None, :]
    chroma = np.hypot(d[..., 1], d[..., 2])
    soft = np.clip((chroma - t_lo) / (t_hi - t_lo), 0, 1)
    core = (soft > 0.5).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab_cc, stats, _ = cv2.connectedComponentsWithStats(core)
    if n < 2:
        raise ValueError("no subject found against the backdrop")
    keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    core = (lab_cc == keep).astype(np.uint8)
    solid = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    flood = solid.copy(); ff = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, ff, (0, 0), 1)
    solid = solid | (1 - flood)                                    # holes filled
    near = cv2.dilate(solid, np.ones((7, 7), np.uint8)).astype(np.float32)
    alpha = np.maximum(soft * near, solid.astype(np.float32))
    return cv2.GaussianBlur(alpha, (0, 0), 0.7)


def subject_bbox(img: np.ndarray) -> tuple[int, int, int, int]:
    """Tight box around the character, from the matte (x, y, w, h)."""
    ys, xs = np.nonzero(matte(img) > 0.5)
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)


def harmonise(rgb: np.ndarray, alpha: np.ndarray, plate_region: np.ndarray,
              amount: float = 0.35) -> np.ndarray:
    """Match the character's brightness to the plate's local light: luminance
    only, never hue. A character's colours are part of its identity; the first
    version matched each channel and turned the fox's white chest pale green
    in a green forest.
    """
    m = alpha > 0.5
    if m.sum() < 50 or amount <= 0:
        return rgb
    w = np.array([0.299, 0.587, 0.114])
    src = float(rgb[m] @ w.mean() if False else (rgb[m] * w).sum(1).mean())
    dst = float((plate_region.reshape(-1, 3) * w).sum(1).mean())
    gain = 1 + amount * (dst / max(src, 1.0) - 1)
    return np.clip(rgb * float(np.clip(gain, 0.8, 1.1)), 0, 255)


def place(plate: np.ndarray, still: np.ndarray, x: float, y: float, height: float,
          flip: bool = False, shadow: float = 0.45, light: float = 0.35) -> tuple[np.ndarray, dict]:
    H, W = plate.shape[:2]
    alpha = matte(still)
    ys, xs = np.nonzero(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgb = still[y0:y1, x0:x1].astype(np.float32); a = alpha[y0:y1, x0:x1]
    if flip:
        rgb, a = rgb[:, ::-1], a[:, ::-1]
    scale = height * H / rgb.shape[0]
    nw, nh = max(1, int(rgb.shape[1] * scale)), max(1, int(rgb.shape[0] * scale))
    rgb = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA)
    a = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA)
    left, top = int(x * W - nw / 2), int(y * H - nh)              # feet at (x, y)
    out = plate.astype(np.float32).copy()
    # contact shadow: a soft dark ellipse under the feet
    sh = np.zeros((H, W), np.float32)
    cv2.ellipse(sh, (int(x * W), int(y * H)), (int(nw * 0.42), max(3, int(nh * 0.06))),
                0, 0, 360, 1.0, -1)
    sh = cv2.GaussianBlur(sh, (0, 0), max(3, nh * 0.03))
    out *= (1 - shadow * sh)[..., None]
    # paste, clipped to the frame
    sx0, sy0 = max(0, -left), max(0, -top)
    dx0, dy0 = max(0, left), max(0, top)
    dx1, dy1 = min(W, left + nw), min(H, top + nh)
    if dx1 <= dx0 or dy1 <= dy0:
        raise ValueError("character placed outside the frame")
    rgb_c = rgb[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0]
    a_c = a[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0][..., None]
    region = out[dy0:dy1, dx0:dx1]
    rgb_c = harmonise(rgb_c, a_c[..., 0], region, light)
    out[dy0:dy1, dx0:dx1] = region * (1 - a_c) + rgb_c * a_c
    return out, dict(box=[dx0, dy0, dx1 - dx0, dy1 - dy0], scale=round(scale, 3))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plate", type=Path, required=True)
    ap.add_argument("--char", action="append", required=True,
                    help="STILL.png:x=..,y=..,h=..[,flip]  (x,y = feet, fractions of the frame)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--plate-crop", help="x,y,w,h as fractions: a virtual close-up of the plate, "
                                         "cropped and upscaled with Real-ESRGAN (same place, closer)")
    args = ap.parse_args()
    frame = np.asarray(Image.open(args.plate).convert("RGB")).astype(np.float32)
    if args.plate_crop:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        import torch
        from twc import post
        H, W = frame.shape[:2]
        fx, fy, fw, fh = map(float, args.plate_crop.split(","))
        x0, y0, cw = int(fx * W), int(fy * H), int(fw * W)
        ch = int(cw * H / W)                                  # keep the plate's aspect
        crop = frame[y0:y0 + ch, x0:x0 + cw].astype(np.uint8)
        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        frame = post.upscale(crop[None], W, H, dev)[0].astype(np.float32)
    placed = []
    for spec in args.char:
        path, _, opts = spec.partition(":")
        kv = dict(o.split("=") if "=" in o else (o, "1") for o in opts.split(",") if o)
        still = np.asarray(Image.open(path).convert("RGB"))
        frame, info = place(frame, still, float(kv.get("x", 0.5)), float(kv.get("y", 0.85)),
                            float(kv.get("h", 0.4)), flip="flip" in kv)
        placed.append(dict(still=path, **kv, **info))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(args.out)
    args.out.with_suffix(".json").write_text(json.dumps(
        dict(stage="keyframe", plate=str(args.plate), characters=placed), indent=2))
    print(f"keyframe -> {args.out}  {placed}")


if __name__ == "__main__":
    main()
