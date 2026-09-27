#!/usr/bin/env python3
"""Design, audition and pick the channel's voices (voice/voices.yaml).

  TWC_ENV=tts lumi/run_in_container.sh python voice/voices.py design     [--roles leo milo]
  TWC_ENV=tts lumi/run_in_container.sh python voice/voices.py audition   [--roles ...]
  TWC_ENV=tts lumi/run_in_container.sh python voice/voices.py pick --role leo --candidate leo_deep_warm_s201

design    Parler-TTS large v1 (Apache-2.0): each candidate's description reads
          `reference_text` -> work/voices/<candidate>/reference.wav (~10 s).
audition  Chatterbox multilingual (MIT) clones each reference and reads the
          role's audition lines -> work/voices/<candidate>/audition_en.wav, plus
          one file per role with all candidates in a row, each introduced by a
          short beep, for listening: work/voices/audition_<role>.wav.
pick      copies the chosen reference into voice/cast/<role>/ with a
          voice.yaml recording where it came from (the canonical voice).

GPU recommended (a dev-g task); design and audition each take a few minutes.
Every output has a .json sidecar (description, seed, model revisions).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import paths  # noqa: E402

CFG = paths.REPO / "voice" / "voices.yaml"
OUT = paths.WORK / "voices"
CAST = paths.REPO / "voice" / "cast"
PARLER = ("parler-tts/parler-tts-large-v1", "50cb4b874c83902f930d7c2e753224c15654f11e")
CHATTERBOX = ("ResembleAI/chatterbox", "5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18")
SR_OUT = 24000


def load_cfg() -> dict:
    import yaml

    return yaml.safe_load(CFG.read_text())


def cand_name(c: dict) -> str:
    return f"{c['id']}_s{c['seed']}"


def device():
    import torch

    return "cuda" if torch.cuda.is_available() else "cpu"


def save_wav(path: Path, wav: np.ndarray, sr: int, **meta) -> None:
    import soundfile as sf

    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), np.asarray(wav, dtype=np.float32), sr)
    path.with_suffix(".json").write_text(json.dumps(meta, indent=2, default=str))


def stage_design(cfg: dict, roles: list[str]) -> None:
    import torch
    from parler_tts import ParlerTTSForConditionalGeneration
    from transformers import AutoTokenizer

    dev = device()
    # attn_implementation="eager": the default (sdpa) run produced a hum instead
    # of speech on LUMI (2026-09-27); T5 has no sdpa kernel in transformers 4.46.
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        PARLER[0], revision=PARLER[1], attn_implementation="eager",
        torch_dtype=torch.float32).to(dev).eval()
    tok = AutoTokenizer.from_pretrained(PARLER[0], revision=PARLER[1])
    text_ids = tok(cfg["reference_text"].strip(), return_tensors="pt").input_ids.to(dev)
    for role in roles:
        for c in cfg["roles"][role]["candidates"]:
            out = OUT / cand_name(c) / "reference.wav"
            if out.is_file():
                print(f"exists: {out}"); continue
            torch.manual_seed(c["seed"])
            desc = tok(c["description"], return_tensors="pt").input_ids.to(dev)
            with torch.no_grad():
                audio = model.generate(input_ids=desc, prompt_input_ids=text_ids,
                                       do_sample=True, temperature=1.0)
            wav = audio.float().cpu().numpy().squeeze()
            save_wav(out, wav, model.config.sampling_rate, stage="design", role=role,
                     candidate=cand_name(c), description=c["description"], seed=c["seed"],
                     text=cfg["reference_text"], model=f"{PARLER[0]}@{PARLER[1]}")
            print(f"[{role}] {out} ({len(wav) / model.config.sampling_rate:.1f} s)", flush=True)


def load_chatterbox():
    import torch
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from huggingface_hub import snapshot_download

    if device() == "cpu":        # conds.pt was saved on CUDA: map every load to the CPU
        _load = torch.load
        torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": "cpu"})

    ckpt = snapshot_download(CHATTERBOX[0], revision=CHATTERBOX[1], allow_patterns=[
        "ve.pt", "t3_mtl23ls_v2.safetensors", "s3gen.pt",
        "grapheme_mtl_merged_expanded_v1.json", "conds.pt", "Cangjie5_TC.json"])
    return ChatterboxMultilingualTTS.from_local(ckpt, device())


def speak(model, text: str, lang: str, reference: Path, settings: dict, seed: int) -> np.ndarray:
    """One line with Chatterbox; returns float32 mono at SR_OUT."""
    import torch

    torch.manual_seed(seed)
    cfg_w = settings["cfg_weight"] if lang == "en" else settings["cfg_weight_other_language"]
    wav = model.generate(text, language_id=lang, audio_prompt_path=str(reference),
                         exaggeration=settings["exaggeration"], cfg_weight=cfg_w)
    return wav.squeeze().cpu().numpy().astype(np.float32)


def beep(sr: int, secs: float = 0.25, f: float = 880.0) -> np.ndarray:
    t = np.arange(int(sr * secs)) / sr
    return (0.2 * np.sin(2 * np.pi * f * t) * np.hanning(len(t))).astype(np.float32)


def stage_audition(cfg: dict, roles: list[str], names: list[str] | None = None) -> None:
    model = load_chatterbox()
    sr = model.sr
    gap = np.zeros(int(0.5 * sr), np.float32)
    for role in roles:
        reel = []
        cands = names or [cand_name(c) for c in cfg["roles"][role]["candidates"]]
        if names:                            # explicit folders: only those of this role
            cands = [n for n in names if n.startswith(role)]
        for name in cands:
            ref = OUT / name / "reference.wav"
            if not ref.is_file():
                print(f"no reference for {name}; run design first"); continue
            out = OUT / name / "audition_en.wav"
            if out.is_file():
                import soundfile as sf
                wav, _ = sf.read(str(out), dtype="float32")
            else:
                parts = []
                for k, line in enumerate(cfg["audition"][role]):
                    one = speak(model, line, "en", ref, cfg["chatterbox"],
                                cfg["chatterbox"]["seed"] + k)
                    save_wav(OUT / name / f"audition_en_line{k}.wav", one, sr, stage="audition",
                             role=role, candidate=name, line=line)
                    parts += [one, gap]
                wav = np.concatenate(parts)
                save_wav(out, wav, sr, stage="audition", role=role, candidate=name,
                         reference=str(ref), lines=cfg["audition"][role],
                         settings=cfg["chatterbox"], model=f"{CHATTERBOX[0]}@{CHATTERBOX[1]}")
                print(f"[{role}] {out} ({len(wav) / sr:.1f} s)", flush=True)
            reel += [beep(sr), gap, wav, gap, gap]
        if reel and not names:
            save_wav(OUT / f"audition_{role}.wav", np.concatenate(reel), sr,
                     stage="audition_reel", role=role, order=cands)
            print(f"[{role}] reel -> {OUT / f'audition_{role}.wav'}", flush=True)


def split_lines(wav: np.ndarray, sr: int, min_gap: float = 0.45) -> list[np.ndarray]:
    """Split an audition at the exact-zero gaps written between its lines."""
    zero = wav == 0.0
    cuts, run, start = [], 0, None
    for i, z in enumerate(zero):
        if z:
            run += 1
            if run == int(min_gap * sr):
                cuts.append(i - run + 1)
        else:
            run = 0
    pieces, prev = [], 0
    for c in cuts:
        seg = wav[prev:c]
        if len(seg) > sr * 0.3:
            pieces.append(seg)
        nz = np.nonzero(~zero[c:])[0]
        prev = c + (nz[0] if len(nz) else len(wav) - c)
    if len(wav) - prev > sr * 0.3:
        pieces.append(wav[prev:])
    return pieces


def stage_refine(cfg: dict, candidate: str, line: int, trim: float, role: str) -> None:
    """Make a clean reference from one line of an audition the owner liked:
    trim the start (Chatterbox onsets can carry echo/distortion), fade in/out."""
    import soundfile as sf

    src = OUT / candidate / "audition_en.wav"
    wav, sr = sf.read(str(src), dtype="float32")
    seg = split_lines(wav, sr)[line][int(trim * sr):]
    fade = int(0.02 * sr)
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    name = f"{candidate}_l{line}"
    save_wav(OUT / name / "reference.wav", seg, sr, stage="refine", role=role,
             candidate=name, source=str(src), line=line, trim_start=trim,
             text=cfg["audition"][role][line], seed=None,
             description=f"line {line} of {candidate}'s audition, start trimmed {trim}s",
             model=f"{CHATTERBOX[0]}@{CHATTERBOX[1]}")
    print(f"{name}: {len(seg) / sr:.1f} s reference")


def stage_pick(cfg: dict, role: str, candidate: str) -> None:
    import yaml

    src = OUT / candidate / "reference.wav"
    if not src.is_file():
        raise SystemExit(f"no such candidate reference: {src}")
    meta = json.loads(src.with_suffix(".json").read_text())
    dst = CAST / role
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst / "reference.wav")
    (dst / "voice.yaml").write_text(yaml.safe_dump(dict(
        role=role, candidate=candidate, description=meta["description"], seed=meta["seed"],
        reference_text=meta["text"], design_model=meta["model"],
        tts_model=f"{CHATTERBOX[0]}@{CHATTERBOX[1]}", settings=cfg["chatterbox"],
        licence="Parler-TTS Apache-2.0 (voice designed from a text description, no real "
                "person's voice); Chatterbox MIT. Outputs carry Resemble AI's Perth watermark.",
    ), sort_keys=False))
    print(f"{role}: canonical voice = {candidate} -> {dst}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["design", "audition", "refine", "pick"])
    ap.add_argument("--candidates", nargs="+", help="audition: these work/voices folders only")
    ap.add_argument("--line", type=int, default=0)
    ap.add_argument("--trim", type=float, default=0.3, help="refine: seconds cut from the start")
    ap.add_argument("--roles", nargs="+", help="default: all roles")
    ap.add_argument("--role")
    ap.add_argument("--candidate")
    args = ap.parse_args()
    cfg = load_cfg()
    roles = args.roles or list(cfg["roles"])
    if args.stage == "design":
        stage_design(cfg, roles)
    elif args.stage == "audition":
        stage_audition(cfg, roles, args.candidates)
    elif args.stage == "refine":
        stage_refine(cfg, args.candidate, args.line, args.trim, args.role)
    else:
        stage_pick(cfg, args.role, args.candidate)


if __name__ == "__main__":
    main()
