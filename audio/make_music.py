#!/usr/bin/env python3
"""Synthesise the TWC intro score from scratch — no samples, no model weights.

Everything here is generated from oscillators, noise and envelopes, so the
result is an original work with nothing to clear: no sample library, no
CC-BY-NC model (MusicGen) and no gated licence (Stable Audio). That matters
because the channel is monetised.

Shape: a D minor trailer cue that swells, accelerates, drops out for a beat and
lands a hit on the logo reveal, then rings out under the hold.
"""

from __future__ import annotations

import argparse
import wave
import sys
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc.paths import AUDIO as _AUDIO  # noqa: E402

SR = 48000

# D minor. The whole cue is built from these, so it stays in key by construction.
D1, D2, A2, D3, F3, A3, D4, F4, A4, D5, F5, A5 = (
    36.71, 73.42, 110.00, 146.83, 174.61, 220.00, 293.66, 349.23, 440.00,
    587.33, 698.46, 880.00,
)


def t_axis(n: int) -> np.ndarray:
    return np.arange(n) / SR


def env_exp(n: int, attack: float, decay: float) -> np.ndarray:
    """Percussive envelope: fast linear attack, exponential decay."""
    t = t_axis(n)
    a = np.clip(t / max(attack, 1e-6), 0, 1)
    return a * np.exp(-t / max(decay, 1e-6))


def saw(freq: float, n: int, harmonics: int = 24, detune: float = 0.0) -> np.ndarray:
    """Band-limited sawtooth by additive synthesis (no aliasing)."""
    t = t_axis(n)
    out = np.zeros(n)
    for k in range(1, harmonics + 1):
        f = freq * k * (1.0 + detune)
        if f >= SR / 2:
            break
        out += np.sin(2 * np.pi * f * t) / k
    return out


def lowpass(x: np.ndarray, cutoff, order: int = 4) -> np.ndarray:
    """Static or per-sample-swept lowpass."""
    if np.isscalar(cutoff):
        sos = butter(order, min(cutoff, SR / 2 - 100), "lowpass", fs=SR, output="sos")
        return sosfilt(sos, x)
    # Swept: process in short blocks, each with its own cutoff.
    out = np.zeros_like(x)
    block = 512
    for start in range(0, len(x), block):
        stop = min(start + block, len(x))
        fc = float(np.mean(cutoff[start:stop]))
        sos = butter(order, np.clip(fc, 40, SR / 2 - 100), "lowpass", fs=SR, output="sos")
        out[start:stop] = sosfilt(sos, x[start:stop])
    return out


def highpass(x: np.ndarray, cutoff: float, order: int = 4) -> np.ndarray:
    sos = butter(order, cutoff, "highpass", fs=SR, output="sos")
    return sosfilt(sos, x)


def add(mix: np.ndarray, part: np.ndarray, at: float, gain: float = 1.0) -> None:
    """Mix `part` into `mix` starting at `at` seconds, clipped to the buffer."""
    i = int(at * SR)
    if i >= len(mix):
        return
    j = min(len(mix), i + len(part))
    mix[i:j] += gain * part[: j - i]


def reverb_ir(seconds: float, decay: float, rng: np.random.Generator) -> np.ndarray:
    """Synthetic exponential-decay impulse response, darkened like a big hall."""
    n = int(seconds * SR)
    ir = rng.standard_normal(n) * np.exp(-t_axis(n) / decay)
    ir[: int(0.008 * SR)] *= np.linspace(0, 1, int(0.008 * SR))  # soften the attack
    return lowpass(ir, 4200) / (np.abs(ir).max() + 1e-9)


def build(duration: float, impact: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    dry = np.zeros(n)

    # --- low drone: the bed the whole cue sits on -------------------------
    drone_n = int((impact + 0.1) * SR)
    drone = (
        0.9 * saw(D1, drone_n, 12)
        + 0.7 * saw(D2, drone_n, 16, detune=0.004)
        + 0.4 * saw(A2, drone_n, 16, detune=-0.003)
    )
    swell = np.linspace(0.05, 1.0, drone_n) ** 1.7
    cutoff = 120 + 900 * np.linspace(0, 1, drone_n) ** 2
    add(dry, lowpass(drone * swell, cutoff), 0.0, 0.16)

    # --- riser: noise sweep + rising tone, the tension under the vortex ----
    rise_start, rise_n = 0.6, int((impact - 0.6) * SR)
    ramp = np.linspace(0, 1, rise_n)
    noise = rng.standard_normal(rise_n)
    noise = lowpass(highpass(noise, 300), 700 + 7000 * ramp**2)
    add(dry, noise * (ramp**2.4), rise_start, 0.18)

    sweep_f = 180 * (2 ** (4.2 * ramp**1.5))  # ~180 Hz -> ~3.2 kHz
    phase = 2 * np.pi * np.cumsum(sweep_f) / SR
    add(dry, np.sin(phase) * (ramp**3) * 0.5, rise_start, 0.10)

    # --- taiko pulses, accelerating toward the hit ------------------------
    beats, pos, gap = [], 1.0, 0.62
    while pos < impact - 0.12:
        beats.append(pos)
        gap *= 0.88                      # each gap shorter: the accelerando
        pos += max(gap, 0.11)
    for i, at in enumerate(beats):
        hit_n = int(0.5 * SR)
        f = np.linspace(110, 52, hit_n)
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(hit_n, 0.002, 0.16)
        click = lowpass(rng.standard_normal(hit_n), 2500) * env_exp(hit_n, 0.001, 0.03)
        loud = 0.35 + 0.65 * (i / max(len(beats) - 1, 1)) ** 1.4
        add(dry, (body + 0.35 * click) * loud, at, 0.42)

    # --- shimmer bells: the pages catching the light ----------------------
    bell_notes = [D5, F5, A5, D5 * 2, A4, F5, D5, A5, F5 * 2, D5, A5, D5 * 2]
    for i, freq in enumerate(bell_notes):
        at = 2.1 + i * (impact - 2.6) / len(bell_notes)
        bn = int(1.6 * SR)
        tb = t_axis(bn)
        tone = (
            np.sin(2 * np.pi * freq * tb)
            + 0.5 * np.sin(2 * np.pi * freq * 2.01 * tb)
            + 0.25 * np.sin(2 * np.pi * freq * 3.02 * tb)
        )
        add(dry, tone * env_exp(bn, 0.004, 0.42), at, 0.055 + 0.05 * (i / len(bell_notes)))

    # --- IMPACT ----------------------------------------------------------
    boom_n = int(2.2 * SR)
    bf = 95 * np.exp(-t_axis(boom_n) / 0.45) + 32
    boom = np.sin(2 * np.pi * np.cumsum(bf) / SR) * env_exp(boom_n, 0.004, 0.75)
    add(dry, boom, impact, 0.62)

    crash_n = int(2.6 * SR)
    crash = highpass(rng.standard_normal(crash_n), 1800) * env_exp(crash_n, 0.002, 0.9)
    add(dry, crash, impact, 0.20)

    # Sustained D minor chord holding under the logo.
    chord_n = int(max(duration - impact, 0.5) * SR)
    chord = np.zeros(chord_n)
    for freq, amp in ((D2, 1.0), (D3, 0.8), (A3, 0.6), (F3, 0.55), (D4, 0.45),
                      (F4, 0.3), (A4, 0.25)):
        chord += amp * saw(freq, chord_n, 20, detune=rng.uniform(-0.003, 0.003))
    tc = t_axis(chord_n)
    chord_env = np.minimum(tc / 0.03, 1.0) * (0.45 + 0.55 * np.exp(-tc / 1.5))
    add(dry, lowpass(chord * chord_env, 300 + 2600 * np.exp(-tc / 0.8)), impact, 0.10)

    # Put the build a fixed distance under the hit. Without this the riser
    # reaches full level early and the impact lands on top of a wall instead of
    # cutting through it.
    i_impact = int(impact * SR)
    pre_peak = np.abs(dry[:i_impact]).max() + 1e-9
    post_peak = np.abs(dry[i_impact:]).max() + 1e-9
    dry[:i_impact] *= 0.34 * post_peak / pre_peak      # build tops out ~9 dB down

    # --- space ------------------------------------------------------------
    left = dry + 0.34 * fftconvolve(dry, reverb_ir(2.6, 0.85, rng))[:n]
    right = dry + 0.34 * fftconvolve(dry, reverb_ir(2.6, 0.88, rng))[:n]
    stereo = np.stack([left, right], axis=1)

    # The beat of silence that makes the hit land. It has to be applied after
    # the reverb, or the tail of the build simply fills the gap.
    duck_a, duck_b = int((impact - 0.16) * SR), int(impact * SR)
    stereo[duck_a:duck_b] *= (np.linspace(1.0, 0.06, duck_b - duck_a) ** 1.6)[:, None]

    # Fade the very start and let the tail die inside the clip.
    fade_in = int(0.06 * SR)
    stereo[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    fade_out = int(0.5 * SR)
    stereo[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]

    # Normalise BEFORE limiting: on the raw mix everything already sits above
    # the knee, so clipping first would flatten the build and the hit to the
    # same ceiling and throw away the dynamics the cue is built on.
    stereo *= 0.95 / (np.abs(stereo).max() + 1e-9)
    knee = 0.86
    over = np.abs(stereo) > knee
    stereo[over] = np.sign(stereo[over]) * (
        knee + (1 - knee) * np.tanh((np.abs(stereo[over]) - knee) / (1 - knee))
    )
    stereo *= 0.89 / (np.abs(stereo).max() + 1e-9)          # leave ~1 dB headroom
    return stereo


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--duration", type=float, default=10.0)
    ap.add_argument("--impact-at", type=float, default=8.0,
                    help="seconds at which the logo reveal lands")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("-o", "--output", type=Path,
                    default=_AUDIO / "twc_intro_score.wav")
    args = ap.parse_args()

    audio = build(args.duration, args.impact_at, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")
    with wave.open(str(args.output), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

    rms = 20 * np.log10(np.sqrt((audio**2).mean(axis=1)).reshape(-1, SR // 2).mean(axis=1) + 1e-9)
    print(f"Wrote {args.output}  {len(audio)/SR:.2f} s, {SR} Hz stereo")
    print("RMS per 0.5 s (dBFS):", " ".join(f"{v:5.0f}" for v in rms))


if __name__ == "__main__":
    main()
