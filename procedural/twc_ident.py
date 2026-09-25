#!/usr/bin/env python3
"""Procedural TWC ident: every frame is drawn by this program.

No generative video model is involved. The only external inputs are the
channel's own emblem (a transparent PNG) and the Cinzel typeface (SIL OFL 1.1),
so the output carries no model or stock licence and is safe to monetise.

Timeline (seconds), locked to audio/twc_intro_score.wav:
  0.0 - 6.94  a vortex of comic pages spirals out of a light core while the
              camera pushes forward through the stars; the core pulses on the
              score's accelerating taiko beats (same beat grid as make_music.py)
  6.94 - 7.10 the "inhale": everything is pulled into the core and dims, under
              the score's beat of silence
  7.10        the hit: white flash, shockwave ring, sparks, the emblem lands
  7.45 -      the wordmark tracks in, then the tagline
  -> 10.0     hold on the logo, framed by drifting pages

Every frame is a pure function of t, so frames render in parallel and a
re-render is bit-identical.
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import media, paths  # noqa: E402

W, H = 1920, 1080
CX, CY = W / 2, 460.0          # emblem centre, leaving room for the wordmark
HIT = 7.10                     # the score's impact; set with --hit
DUCK = HIT - 0.16              # start of the score's beat of silence
DUR = 10.0

BLUE = np.array([0.24, 0.45, 1.00], np.float32)
VIOLET = np.array([0.50, 0.26, 1.00], np.float32)
MAGENTA = np.array([1.00, 0.20, 0.52], np.float32)
WARM = np.array([1.00, 0.86, 0.62], np.float32)
ICE = np.array([0.90, 0.95, 1.00], np.float32)


# --------------------------------------------------------------------------- #
# timing helpers
# --------------------------------------------------------------------------- #
def smoothstep(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def ease_out_cubic(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def set_hit(hit: float) -> None:
    """Move the impact (and everything timed from it) to `hit` seconds."""
    global HIT, DUCK
    HIT, DUCK = hit, hit - 0.16


def beat_times(impact: float | None = None) -> list[float]:
    """Exactly the taiko grid in make_music.py, so light and drums coincide."""
    impact = HIT if impact is None else impact
    beats, pos, gap = [], 1.0, 0.62
    while pos < impact - 0.12:
        beats.append(pos)
        gap *= 0.88
        pos += max(gap, 0.11)
    return beats


def vortex_angle(t: float) -> float:
    """Accumulated spin of the page vortex; accelerates toward the hit."""
    return 0.9 * t + 1.1 * t**3 / HIT**2


# --------------------------------------------------------------------------- #
# assets (built once per worker, deterministic)
# --------------------------------------------------------------------------- #
def _screentone(img, x0, y0, x1, y1, rng, pitch=6):
    """Manga halftone: a dot grid whose dot size follows a gradient."""
    ang = rng.uniform(0, 2 * math.pi)
    dx, dy = math.cos(ang), math.sin(ang)
    span = abs(dx) * (x1 - x0) + abs(dy) * (y1 - y0) + 1e-6
    lo, hi = sorted(rng.uniform(0.0, 1.0, 2))
    for yy in np.arange(y0 + pitch / 2, y1, pitch):
        for xx in np.arange(x0 + pitch / 2 + (pitch / 2 if int((yy - y0) / pitch) % 2 else 0), x1, pitch):
            g = ((xx - x0) * dx + (yy - y0) * dy) / span % 1.0
            rad = (lo + (hi - lo) * g) * pitch * 0.55
            if rad > 0.6:
                cv2.circle(img, (int(xx), int(yy)), int(round(rad)), (0.1, 0.1, 0.12), -1, cv2.LINE_AA)


def _figure(img, cx, base, height, ink):
    """A readable bust: head, neck gap, shoulders -- not a keyhole."""
    head = max(4, int(height * 0.17))
    cv2.circle(img, (cx, base - height + head), head, ink, -1, cv2.LINE_AA)
    sh = int(height * 0.34)
    top = base - height + int(head * 2.35)
    pts = np.array([[cx - sh // 3, top], [cx + sh // 3, top],
                    [cx + sh, base], [cx - sh, base]], np.int32)
    cv2.fillPoly(img, [pts], ink, cv2.LINE_AA)


def make_page(rng: np.random.Generator, w: int = 300, h: int = 420) -> np.ndarray:
    """An original manga-style page: ink panels, screentone, speed lines, figures."""
    img = np.empty((h, w, 3), np.float32)
    img[:] = (0.97, 0.96, 0.93)
    ink = (0.07, 0.07, 0.09)
    m, gutter = 14, 9
    rows = int(rng.integers(2, 4))
    row_h = (h - 2 * m - (rows - 1) * gutter) / rows
    for r in range(rows):
        cols = int(rng.integers(1, 3))
        col_w = (w - 2 * m - (cols - 1) * gutter) / cols
        for c in range(cols):
            x0, y0 = m + c * (col_w + gutter), m + r * (row_h + gutter)
            x1, y1 = x0 + col_w, y0 + row_h
            p0, p1 = (int(x0), int(y0)), (int(x1), int(y1))
            kind = rng.choice(["tone", "speed", "night", "horizon"], p=[0.35, 0.25, 0.15, 0.25])
            if kind == "night":
                cv2.rectangle(img, p0, p1, ink, -1)
                for _ in range(int(rng.integers(8, 20))):
                    q = (int(rng.uniform(x0, x1)), int(rng.uniform(y0, y1)))
                    cv2.circle(img, q, 1, (0.9, 0.9, 0.95), -1, cv2.LINE_AA)
                _figure(img, int(rng.uniform(x0 + 20, x1 - 20)), int(y1),
                        int(row_h * 0.7), (0.85, 0.86, 0.9))
            else:
                if kind == "tone":
                    _screentone(img, x0, y0, x1, y1, rng)
                elif kind == "speed":
                    vx, vy = rng.uniform(x0, x1), rng.uniform(y0, y1)
                    for _ in range(int(rng.integers(18, 34))):
                        a = rng.uniform(0, 2 * math.pi)
                        inner = rng.uniform(0.25, 0.5)
                        q0 = (int(vx + math.cos(a) * col_w * inner), int(vy + math.sin(a) * row_h * inner))
                        q1 = (int(vx + math.cos(a) * col_w * 1.4), int(vy + math.sin(a) * row_h * 1.4))
                        cv2.line(img, q0, q1, ink, 1, cv2.LINE_AA)
                else:  # horizon: hills and a sky tone
                    _screentone(img, x0, y0, x1, y0 + row_h * 0.55, rng, pitch=5)
                    xs = np.linspace(x0, x1, 9)
                    ys = y1 - row_h * (0.2 + 0.25 * rng.random(9))
                    pts = np.array([[x0, y1]] + list(zip(xs, ys)) + [[x1, y1]], np.int32)
                    cv2.fillPoly(img, [pts], ink, cv2.LINE_AA)
                if rng.random() < 0.6:
                    _figure(img, int(rng.uniform(x0 + 22, x1 - 22)), int(y1),
                            int(row_h * rng.uniform(0.55, 0.85)), ink)
                img[int(y0):int(y1), int(x0):int(x1)] = np.clip(
                    img[int(y0):int(y1), int(x0):int(x1)], 0, 1)
            cv2.rectangle(img, p0, p1, ink, 3, cv2.LINE_AA)
    alpha = np.ones((h, w, 1), np.float32)
    return np.concatenate([img, alpha], 2)


def blurred(tex: np.ndarray, sigma: float) -> np.ndarray:
    """Depth-of-field copy; the pad keeps the blurred edge from being clipped."""
    pad = int(sigma * 3)
    t = cv2.copyMakeBorder(tex, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    return cv2.GaussianBlur(t, (0, 0), sigma)


def glyph_run(font: ImageFont.FreeTypeFont, text: str):
    """Each character as its own coverage mask, plus its advance width."""
    ascent, descent = font.getmetrics()
    out = []
    for ch in text:
        adv = font.getlength(ch)
        im = Image.new("L", (int(math.ceil(adv)) + 4, ascent + descent + 4), 0)
        ImageDraw.Draw(im).text((2, 2), ch, font=font, fill=255)
        out.append((np.asarray(im, np.float32) / 255.0, adv))
    return out


class Assets:
    def __init__(self, emblem: Path, font: Path, seed: int):
        rng = np.random.default_rng(seed)

        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        self.d2 = (xx - CX) ** 2 + ((yy - CY) * 1.15) ** 2
        rr = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
        base = np.clip(1.0 - rr * 1.3, 0, 1)[..., None]
        self.bg = (np.array([0.008, 0.010, 0.030], np.float32)
                   + base * np.array([0.028, 0.030, 0.080], np.float32))
        self.vignette = (1.0 - 0.55 * np.clip(rr * 1.35, 0, 1) ** 2)[..., None]

        self.nebula = []
        for k, col in enumerate((BLUE, VIOLET, MAGENTA)):
            n = rng.standard_normal((270, 480)).astype(np.float32)
            n = cv2.GaussianBlur(n, (0, 0), 26 + 12 * k)
            n = (n - n.min()) / (n.max() - n.min() + 1e-9)
            n = np.clip((n - 0.48) * 2.4, 0, 1) ** 1.5
            self.nebula.append((n, col, (0.20, 0.15, 0.10)[k], (1, -1, 1)[k]))

        n_stars = 800
        self.star_xy = rng.uniform(-1, 1, (n_stars, 2)).astype(np.float32)
        self.star_xy[:, 1] *= 0.62
        self.star_z = rng.uniform(0.0, 1.0, n_stars)
        self.star_b = rng.uniform(0.3, 1.0, n_stars)
        self.star_ph = rng.uniform(0, 2 * math.pi, n_stars)
        self.star_f = rng.uniform(0.6, 2.4, n_stars)

        self.page_tex = [make_page(rng) for _ in range(10)]
        # depth of field: sharp, soft (mid-distance), very soft (at the lens)
        self.page_dof = [[tex, blurred(tex, 2.2), blurred(tex, 6.0)] for tex in self.page_tex]
        n_pages = 120
        self.p_spawn = np.sort(rng.uniform(0.2, HIT - 0.7, n_pages))
        self.p_life = rng.uniform(1.5, 2.7, n_pages)
        self.p_theta0 = rng.uniform(0, 2 * math.pi, n_pages)
        self.p_phi0 = rng.uniform(0, 2 * math.pi, n_pages)
        self.p_flip = rng.uniform(2.0, 4.5, n_pages) * rng.choice([-1, 1], n_pages)
        self.p_tex = rng.integers(0, len(self.page_tex), n_pages)
        self.p_tilt = rng.uniform(-0.5, 0.5, n_pages)

        # Pages that the hit throws out to frame the logo, as in the still 6.png.
        n_frame = 12
        ang = np.linspace(0, 2 * math.pi, n_frame, endpoint=False) + rng.uniform(-0.12, 0.12, n_frame)
        self.f_dest = np.stack([W / 2 + np.cos(ang) * rng.uniform(820, 960, n_frame),
                                 540 + np.sin(ang) * rng.uniform(450, 540, n_frame)], 1)
        self.f_rot = rng.uniform(-0.6, 0.6, n_frame)
        self.f_scale = rng.uniform(0.38, 0.6, n_frame)
        self.f_tex = rng.integers(0, len(self.page_tex), n_frame)
        self.f_drift = rng.uniform(-1, 1, (n_frame, 2)) * 14

        em = Image.open(emblem).convert("RGBA").resize((560, 560), Image.LANCZOS)
        a = np.asarray(em, np.float32) / 255.0
        self.em_a = a[..., 3:4]
        self.em_pm = a[..., :3] * self.em_a
        pad = 120
        padded = cv2.copyMakeBorder(self.em_pm, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        self.em_glow = (cv2.GaussianBlur(padded, (0, 0), 16) * 0.8
                        + cv2.GaussianBlur(padded, (0, 0), 48) * 1.0)

        n_sparks = 280
        ang = rng.uniform(0, 2 * math.pi, n_sparks)
        speed = rng.uniform(350, 1600, n_sparks)
        self.sp_v = np.stack([np.cos(ang), np.sin(ang) * 0.82], 1) * speed[:, None]
        palette = np.stack([BLUE, VIOLET, MAGENTA, ICE, ICE])
        self.sp_col = palette[rng.integers(0, len(palette), n_sparks)]
        self.sp_life = rng.uniform(0.5, 1.4, n_sparks)

        title = ImageFont.truetype(str(font), 74)
        title.set_variation_by_axes([640])
        tag = ImageFont.truetype(str(font), 28)
        tag.set_variation_by_axes([520])
        self.title = glyph_run(title, "THE WEBTOONS CORNER")
        self.tag = glyph_run(tag, "MORE STORIES. TOGETHER.")

        self.beats = beat_times()

        # energy ribbons: spiral arms of the vortex
        self.rib_theta = np.linspace(0, 2 * math.pi, 7, endpoint=False) + rng.uniform(-0.2, 0.2, 7)
        palette = [BLUE, VIOLET, MAGENTA, BLUE, VIOLET, ICE * 0.8, BLUE]
        self.rib_col = [palette[k] for k in range(7)]
        self.rib_phase = rng.uniform(0, 2 * math.pi, 7)

        n_rays = 56
        self.ray_ang = rng.uniform(0, 2 * math.pi, n_rays)
        self.ray_len = rng.uniform(0.45, 1.0, n_rays)
        self.ray_w = rng.uniform(4, 16, n_rays)
        self.ray_col = [(BLUE, VIOLET, MAGENTA, ICE, ICE)[int(k)] for k in rng.integers(0, 5, n_rays)]


A: Assets | None = None


def _init(emblem: str, font: str, seed: int, hit: float = HIT) -> None:
    global A
    set_hit(hit)
    A = Assets(Path(emblem), Path(font), seed)


# --------------------------------------------------------------------------- #
# drawing primitives
# --------------------------------------------------------------------------- #
def blit_rgba(canvas: np.ndarray, tex: np.ndarray, x: float, y: float, rot: float,
              sx: float, sy: float, tint: np.ndarray, opacity: float) -> None:
    """Affine-warp a straight-alpha RGBA texture onto the canvas (region only)."""
    th, tw = tex.shape[:2]
    c, s = math.cos(rot), math.sin(rot)
    m = np.array([[c * sx, -s * sy, 0.0], [s * sx, c * sy, 0.0]], np.float32)
    m[:, 2] = np.array([x, y]) - m[:, :2] @ np.array([tw / 2, th / 2])
    corners = np.array([[0, 0, 1], [tw, 0, 1], [0, th, 1], [tw, th, 1]], np.float32) @ m.T
    x0, y0 = np.floor(corners.min(0)).astype(int)
    x1, y1 = np.ceil(corners.max(0)).astype(int)
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    if x1 <= x0 or y1 <= y0 or opacity <= 0.003:
        return
    m[:, 2] -= (x0, y0)
    warped = cv2.warpAffine(tex, m, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    a = warped[..., 3:4] * opacity
    roi = canvas[y0:y1, x0:x1]
    roi *= 1 - a
    roi += warped[..., :3] * tint * a


def paste_centered(canvas, img, x, y, scale, additive=False, alpha=None):
    """Scale a premultiplied image about its centre and paste/add it at (x, y)."""
    h, w = img.shape[:2]
    m = np.array([[scale, 0, x - w * scale / 2], [0, scale, y - h * scale / 2]], np.float32)
    x0, y0 = int(max(x - w * scale / 2 - 1, 0)), int(max(y - h * scale / 2 - 1, 0))
    x1, y1 = int(min(x + w * scale / 2 + 1, W)), int(min(y + h * scale / 2 + 1, H))
    if x1 <= x0 or y1 <= y0:
        return
    m[:, 2] -= (x0, y0)
    size = (x1 - x0, y1 - y0)
    roi = canvas[y0:y1, x0:x1]
    im = cv2.warpAffine(img, m, size, flags=cv2.INTER_LINEAR)
    if additive:
        roi += im
        return
    a = cv2.warpAffine(alpha, m, size, flags=cv2.INTER_LINEAR)[..., None]
    roi *= 1 - a
    roi += im


def draw_text(layer: np.ndarray, glyphs, cx: float, top: float, spacing: float,
              opacity: float) -> None:
    total = sum(adv for _, adv in glyphs) + spacing * (len(glyphs) - 1)
    x = cx - total / 2
    for mask, adv in glyphs:
        h, w = mask.shape
        xi, yi = int(round(x)), int(round(top))
        xa, ya = max(xi, 0), max(yi, 0)
        xb, yb = min(xi + w, W), min(yi + h, H)
        if xb > xa and yb > ya:
            region = layer[ya:yb, xa:xb]
            np.maximum(region, mask[ya - yi:yb - yi, xa - xi:xb - xi] * opacity, out=region)
        x += adv + spacing


# --------------------------------------------------------------------------- #
# the frame
# --------------------------------------------------------------------------- #
def render(t: float) -> np.ndarray:
    a = A
    canvas = a.bg.copy()
    build = min(t / HIT, 1.0)
    after = t - HIT                              # < 0 before the hit
    duck = smoothstep((t - DUCK) / (HIT - DUCK)) if t < HIT else 0.0

    # nebula, slowly turning
    for n, col, weight, sign in a.nebula:
        ang = sign * (1.2 + 3.5 * build) * t
        m = cv2.getRotationMatrix2D((240, 135), ang, 1.0 + 0.03 * t)
        layer = cv2.resize(cv2.warpAffine(n, m, (480, 270), borderMode=cv2.BORDER_REFLECT),
                           (W, H), interpolation=cv2.INTER_LINEAR)
        canvas += layer[..., None] * col * weight * (0.7 + 0.6 * build)

    # stars streaming past a camera that pushes forward, faster toward the hit
    travel = 0.035 * t + 0.10 * t**2 / HIT if t < HIT else 0.035 * HIT + 0.10 * HIT + 0.012 * after
    z = (a.star_z - travel) % 1.0 * 0.95 + 0.05
    px = CX + a.star_xy[:, 0] / z * 330
    py = CY + a.star_xy[:, 1] / z * 330
    tw = 0.6 + 0.4 * np.sin(a.star_ph + a.star_f * t * 6)
    bright = a.star_b * tw * np.clip((1 - z) * 1.6, 0.15, 1.0)
    stars = np.zeros((H, W, 3), np.float32)
    for x, y, b, zz in zip(px, py, bright, z):
        if 0 <= x < W and 0 <= y < H:
            cv2.circle(stars, (int(x), int(y)), 1 + int((1 - zz) * 2.2),
                       (float(b), float(b), float(b * 1.1)), -1, cv2.LINE_AA)
    canvas += stars * 0.85

    # light core, breathing on the drum hits
    if t < HIT + 0.4:
        pulse = sum(math.exp(-(t - b) / 0.11) for b in a.beats if t >= b)
        intensity = (0.10 + 0.95 * build**2.2) * (1 + 0.55 * pulse)
        intensity *= (1 - duck * 0.6) if t < HIT else math.exp(-after / 0.15)
        sigma = 55 + 150 * build
        core = np.exp(-a.d2 / (2 * sigma**2))[..., None]
        canvas += core * (WARM * (1 - build) + ICE * build) * intensity

    # energy ribbons: glowing spiral arms, flowing outward, strongest at the hit
    if t < HIT:
        rib = np.zeros((H // 2, W // 2, 3), np.float32)
        spin = vortex_angle(t)
        amount = smoothstep((t - 0.6) / 2.5) * (0.35 + 0.65 * build) * (1 - 0.7 * duck)
        reach = 1 - 0.75 * duck
        segs = 70
        for k in range(len(a.rib_theta)):
            pts = []
            for q in range(segs + 1):
                sq = q / segs
                r = (30 + 1150 * sq**1.3) * reach
                th = a.rib_theta[k] + spin * 0.85 + 3.4 * sq
                pts.append(((CX + r * math.cos(th)) / 2, (CY + r * math.sin(th) * 0.62) / 2))
            for q in range(segs):
                sq = q / segs
                flow = 0.55 + 0.45 * math.sin(18 * sq - 7 * t + a.rib_phase[k])
                lum = amount * flow * (1 - sq) ** 0.8
                if lum < 0.01:
                    continue
                c = a.rib_col[k] * lum
                p0 = (int(pts[q][0]), int(pts[q][1]))
                p1 = (int(pts[q + 1][0]), int(pts[q + 1][1]))
                cv2.line(rib, p0, p1, tuple(float(v) * 0.5 for v in c), 9, cv2.LINE_AA)
                cv2.line(rib, p0, p1, tuple(float(v) * 1.4 for v in c), 2, cv2.LINE_AA)
        rib = cv2.GaussianBlur(rib, (0, 0), 3) + cv2.GaussianBlur(rib, (0, 0), 12) * 0.8
        canvas += cv2.resize(rib, (W, H), interpolation=cv2.INTER_LINEAR)

    # the page vortex, with motion blur (temporal supersampling) and depth of field
    if t < HIT:
        suck = 1 - 0.8 * duck
        sub = (0.0, 1 / 150, 2 / 150)
        for i in range(len(a.p_spawn)):
            u0 = (t - a.p_spawn[i]) / a.p_life[i]
            if not 0 <= u0 <= 1:
                continue
            for k, dt in enumerate(sub):
                ts = t - dt
                u = (ts - a.p_spawn[i]) / a.p_life[i]
                if not 0 <= u <= 1:
                    continue
                theta = a.p_theta0[i] + vortex_angle(ts) + 1.3 * u
                r = (22 + 1300 * u**1.5) * suck
                x = CX + r * math.cos(theta)
                y = CY + r * math.sin(theta) * 0.62
                sc = 0.10 + 1.15 * u**1.7
                flip = math.cos(a.p_phi0[i] + a.p_flip[i] * (ts - a.p_spawn[i]))
                flip = math.copysign(max(abs(flip), 0.07), flip)
                op = (min(1.0, u / 0.1) * min(1.0, (1 - u) / 0.14) * (1 - 0.5 * duck)
                      * (0.62, 0.42, 0.3)[k])
                # lit warm by the core when close, violet-blue rim light when far
                near = math.exp(-r / 260)
                tint = (np.ones(3, np.float32) * (0.5 + 0.4 * u)
                        + WARM * 0.45 * near * (0.3 + build)
                        + VIOLET * 0.14 * (1 - near) + BLUE * 0.10)
                level = 2 if u > 0.8 else (1 if u > 0.55 else 0)
                tex = a.page_dof[a.p_tex[i]][level]
                blit_rgba(canvas, tex, x, y, theta + math.pi / 2 + a.p_tilt[i],
                          sc * flip, sc, tint, op)

    canvas *= 1 - 0.55 * duck

    # after the hit: framing pages, shockwave, sparks
    if after >= 0:
        # the post-hit world is richer: lift the nebula behind the logo
        halo = np.exp(-a.d2 / (2 * 420.0**2))[..., None]
        canvas += halo * (BLUE * 0.10 + VIOLET * 0.06) * min(1.0, after / 0.4)

        land = ease_out_cubic(after / 0.9)
        for j in range(len(a.f_dest)):
            dx, dy = a.f_dest[j] + a.f_drift[j] * math.sin(0.5 * after + j)
            ox, oy = CX + (dx - CX) * 0.35, CY + (dy - CY) * 0.35   # start outside the emblem
            x = ox + (dx - ox) * land
            y = oy + (dy - oy) * land
            rot = a.f_rot[j] + 0.15 * math.sin(0.4 * after + j * 1.7)
            sc = a.f_scale[j] * (0.5 + 0.5 * land)
            tint = np.ones(3, np.float32) * 0.30 + BLUE * 0.16 + VIOLET * 0.08
            blit_rgba(canvas, a.page_dof[a.f_tex[j]][2], x, y, rot, sc, sc, tint, 0.8 * land)

        fx = np.zeros((H // 2, W // 2, 3), np.float32)
        if after < 0.9:
            reach = 1500 * (0.25 + 0.75 * ease_out_cubic(after / 0.3))
            fade = math.exp(-after / 0.33)
            for ang, ln, wd, col in zip(a.ray_ang, a.ray_len, a.ray_w, a.ray_col):
                tip = (CX + math.cos(ang) * reach * ln, CY + math.sin(ang) * reach * ln * 0.85)
                side = (-math.sin(ang) * wd, math.cos(ang) * wd)
                pts = np.array([[CX + side[0], CY + side[1]], [CX - side[0], CY - side[1]], tip],
                               np.float32) / 2
                cv2.fillPoly(fx, [pts.astype(np.int32)], tuple(float(c) * fade * 0.9 for c in col),
                             cv2.LINE_AA)
            radius = 30 + 1500 * after**0.55
            band = 1.3 * (1 - after / 0.9) ** 2
            cv2.ellipse(fx, (int(CX / 2), int(CY / 2)), (int(radius / 2), int(radius * 0.85 / 2)),
                        0, 0, 360, (float(band * 0.55), float(band * 0.7), float(band)), 9, cv2.LINE_AA)
            fx = cv2.GaussianBlur(fx, (0, 0), 5) * 0.8 + cv2.GaussianBlur(fx, (0, 0), 14)
        fx = cv2.resize(fx, (W, H), interpolation=cv2.INTER_LINEAR)
        drag = (1 - math.exp(-2.4 * after)) / 2.4
        for v, col, life in zip(a.sp_v, a.sp_col, a.sp_life):
            if after > life:
                continue
            fade = (1 - after / life) ** 2
            head = (CX + v[0] * drag, CY + v[1] * drag)
            tail_len = 0.022 * math.exp(-2.4 * after)
            tail = (head[0] - v[0] * tail_len, head[1] - v[1] * tail_len)
            cv2.line(fx, (int(tail[0]), int(tail[1])), (int(head[0]), int(head[1])),
                     tuple(float(c) * fade * 1.4 for c in col), 2, cv2.LINE_AA)
        canvas += fx

        # the emblem lands a little large and settles, then the camera creeps in
        settle = 1 + 0.2 * (1 - ease_out_cubic(after / 0.6))
        scale = settle * (1 + 0.03 * after / (DUR - HIT))
        glow = 0.45 + 1.6 * math.exp(-after / 0.35) + 0.08 * math.sin(2 * math.pi * 0.55 * t)
        paste_centered(canvas, a.em_glow * glow, CX, CY, scale, additive=True)
        paste_centered(canvas, a.em_pm, CX, CY, scale, alpha=a.em_a[..., 0])

    # wordmark and tagline
    if t >= HIT + 0.35:
        text = np.zeros((H, W), np.float32)
        e1 = ease_out_cubic((t - HIT - 0.35) / 0.8)
        draw_text(text, a.title, W / 2, 760, 7 + 40 * (1 - e1), e1)
        if t >= HIT + 1.05:
            e2 = ease_out_cubic((t - HIT - 1.05) / 0.6)
            draw_text(text, a.tag, W / 2, 858, 5 + 18 * (1 - e2), e2)
            half = int(170 * e2)
            if half > 2:
                for side in (-1, 1):
                    start = int(W / 2 + side * 250)
                    cv2.line(text, (start, 876), (start + side * half, 876),
                             float(0.8 * e2), 2, cv2.LINE_AA)
        glow_t = cv2.resize(cv2.GaussianBlur(cv2.resize(text, (W // 2, H // 2)), (0, 0), 7),
                            (W, H))
        canvas += glow_t[..., None] * BLUE * 0.9
        canvas = canvas * (1 - text[..., None]) + text[..., None] * ICE

    # bloom
    small = cv2.resize(canvas, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    bright = np.clip(small - 0.6, 0, None)
    bloom = cv2.GaussianBlur(bright, (0, 0), 5) * 0.6 + cv2.GaussianBlur(bright, (0, 0), 16) * 0.8
    canvas += cv2.resize(bloom, (W, H), interpolation=cv2.INTER_LINEAR)

    # the flash
    if after >= 0:
        canvas += math.exp(-after / 0.16) * 1.3

    canvas *= a.vignette
    grain = np.random.default_rng(int(t * 1000)).standard_normal((H // 2, W // 2)).astype(np.float32)
    canvas += cv2.resize(grain, (W, H))[..., None] * 0.012

    knee = 0.82
    over = canvas > knee
    canvas[over] = knee + (1 - knee) * np.tanh((canvas[over] - knee) / (1 - knee))
    return (np.clip(canvas, 0, 1) * 255 + 0.5).astype(np.uint8)


def _frame(i_fps):
    i, fps = i_fps
    return render(i / fps).tobytes()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--emblem", type=Path,
                    default=paths.REFERENCE / "watermark_big.png")
    ap.add_argument("--font", type=Path,
                    default=paths.REPO / "assets" / "fonts" / "Cinzel.ttf")
    ap.add_argument("--audio", type=Path, default=paths.AUDIO / "twc_intro_score.wav")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--hit", type=float, default=7.10,
                    help="seconds at which the reveal lands (match make_music.py --impact-at)")
    ap.add_argument("--still", type=float, nargs="*",
                    help="render only these timestamps to PNG and exit")
    ap.add_argument("-o", "--output", type=Path,
                    default=paths.OUTPUT / "Intro_channel_video_procedural.mov")
    args = ap.parse_args()

    set_hit(args.hit)
    if args.still:
        _init(str(args.emblem), str(args.font), args.seed, args.hit)
        for t in args.still:
            path = args.output.with_name(f"still_{t:05.2f}.png")
            Image.fromarray(render(t)).save(path)
            print("still", path)
        return

    frames = int(round(DUR * args.fps))
    silent = args.output.with_name(args.output.stem + "_silent.mp4")
    ff = media.locate_ffmpeg()
    enc = subprocess.Popen(
        [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(args.fps), "-i", "-",
         "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
         str(silent)],
        stdin=subprocess.PIPE)
    with Pool(args.workers, initializer=_init,
              initargs=(str(args.emblem), str(args.font), args.seed, args.hit)) as pool:
        for k, data in enumerate(pool.imap(_frame, [(i, args.fps) for i in range(frames)],
                                           chunksize=4)):
            enc.stdin.write(data)
            if (k + 1) % 120 == 0:
                print(f"  rendered {k + 1}/{frames}", flush=True)
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("ffmpeg encode failed")

    # Same audio treatment as every other cut: PCM 48 kHz in a MOV.
    media.finish(concat_video=silent, audio_source=args.audio, output=args.output,
              target_duration=DUR, source_duration=DUR, final_width=W, final_height=H,
              final_fps=args.fps, hold_end=0.0, audio_restart_at=None)
    print(f"Saved procedural ident: {args.output}")


if __name__ == "__main__":
    main()
