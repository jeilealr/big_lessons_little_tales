#!/usr/bin/env python3
"""A gentle music-box cue for the felt test, synthesised from scratch.

Same principle as ltx_env/make_music.py: oscillators, envelopes and a small
synthetic reverb, no samples and no model weights, so it is original and safe
to monetise. The melody is a plain original arpeggio over C | F | G | C, not a
known tune.
"""

from __future__ import annotations

import argparse
import wave
import sys
from pathlib import Path

import numpy as np
from scipy.signal import fftconvolve

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc.paths import AUDIO as _AUDIO  # noqa: E402

SR = 48000


def note(name: str) -> float:
    idx = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}[name[0]]
    return 440.0 * 2 ** ((idx + 12 * (int(name[1:]) - 4)) / 12)


def tone(freq, dur, partials, decay, attack=0.004):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(t / attack, 1.0) * np.exp(-t / decay)
    return env * sum(a * np.sin(2 * np.pi * freq * m * t) for m, a in partials)


def build(duration: float, chime_at: list[float] | None, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    mix = np.zeros((n, 2))

    def put(sig, at, gain, pan=0.0):
        i = int(at * SR)
        if i >= n:
            return
        j = min(n, i + len(sig))
        mix[i:j, 0] += sig[: j - i] * gain * (1 - pan) / 2 * 2 ** 0.5
        mix[i:j, 1] += sig[: j - i] * gain * (1 + pan) / 2 * 2 ** 0.5

    beat = 60 / 96
    bars = [("C", ["C5", "E5", "G5", "E5", "C5", "E5", "G5", "C6"], ["C3", "E4", "G4"]),
            ("F", ["A5", "F5", "C5", "F5", "A5", "C6", "A5", "F5"], ["F3", "A4", "C5"]),
            ("G", ["B4", "D5", "G5", "D5", "B4", "D5", "G5", "B5"], ["G3", "B4", "D5"]),
            ("C", ["C6", "G5", "E5", "C5"], ["C3", "E4", "G4"])]
    music_box = [(1, 1.0), (3.0, 0.22), (5.1, 0.06)]      # bright, bell-like
    marimba = [(1, 1.0), (4.0, 0.12)]                      # round, woody
    t0 = 0.35
    repeats = max(1, int(np.ceil((duration - t0) / (len(bars) * 4 * beat))))
    bars = bars[:-1] * (repeats - 1) + bars if repeats > 1 else bars
    for b, (_, melody, chord) in enumerate(bars):
        start = t0 + b * 4 * beat
        step = beat / 2 if len(melody) == 8 else beat
        for k, name in enumerate(melody):
            at = start + k * step
            last = b == len(bars) - 1 and k == len(melody) - 1
            put(tone(note(name), 2.5 if last else 1.0, music_box, 1.1 if last else 0.45),
                at, 0.16, pan=float(rng.uniform(-0.3, 0.3)))
        for k in range(4):
            if b == len(bars) - 1 and k > 1:
                break
            put(tone(note(chord[0]), 0.8, marimba, 0.3), start + k * beat, 0.30 if k == 0 else 0.18)
        pad = sum(tone(note(p), 4 * beat + 0.4, [(1, 1.0), (2, 0.15)], 3.0, attack=0.35)
                  for p in chord)
        put(pad, start, 0.035)

    for cut in chime_at or []:                  # a little sparkle on each cut
        for k, name in enumerate(["C6", "E6", "G6", "C7"]):
            put(tone(note(name), 1.2, music_box, 0.5), cut - 0.12 + k * 0.05, 0.07,
                pan=-0.4 + 0.27 * k)

    ir_len = int(1.4 * SR)
    t = np.arange(ir_len) / SR
    for ch in range(2):
        ir = rng.standard_normal(ir_len) * np.exp(-t / 0.45)
        ir /= np.abs(ir).max()
        mix[:, ch] += 0.18 * fftconvolve(mix[:, ch], ir)[:n] / np.sqrt(ir_len) * 30

    fade = int(0.6 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    mix *= 0.8 / (np.abs(mix).max() + 1e-9)
    return mix


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--duration", type=float, default=10.2)
    ap.add_argument("--chime-at", type=float, nargs="*", default=None,
                    help="seconds of each cut that gets a chime")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("-o", "--output", type=Path, default=_AUDIO / "felt_lullaby.wav")
    args = ap.parse_args()
    audio = build(args.duration, args.chime_at, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(args.output), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())
    rms = 20 * np.log10(np.sqrt((audio ** 2).mean(1))[: len(audio) // (SR // 2) * (SR // 2)]
                        .reshape(-1, SR // 2).mean(1) + 1e-9)
    print(f"Wrote {args.output} {len(audio)/SR:.2f} s")
    print("RMS per 0.5 s:", " ".join(f"{v:4.0f}" for v in rms))


if __name__ == "__main__":
    main()
