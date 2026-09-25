#!/usr/bin/env python3
"""Consistent characters: text sheets + image anchors, and a LoRA dataset.

The three techniques stack into one pipeline (docs/character-consistency.md):

  1. Sheets   - a fixed description of the character and the set, pasted into
                every prompt. Narrows drift; does not stop it on its own.
  2. Anchors  - every shot starts from a real image of the character (Wan
                image-to-video), so identity is exact at frame 0. One orbit
                shot around the canonical still yields the other camera angles.
  3. LoRA     - later: train on the stills step 2 produced, so the model knows
                the character without an anchor. `dataset` prepares that.

Stages, in order:
  canonical  choose the reference still                      CPU, seconds
  orbit      the camera circles the still (I2V)              GPU, ~2.5 h
  angles     keep orbit frames as keyframes + contact sheet  CPU, seconds
  shots      each shot starts from one keyframe (I2V)        GPU, ~2.5 h each
  dataset    stills + captions for LoRA training             CPU, seconds
  prompt     print the assembled prompt for a stage          no compute

Each output gets a .json sidecar with the exact prompt, seed, source image and
settings that produced it.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import media, paths, wan  # noqa: E402


# The design backdrop. Poses are shot on it so every pose cuts out cleanly.
PLAIN_SET = "a plain cream felt floor in front of a plain pale sage-green felt backdrop"
DEFAULT_RENDER = dict(width=1280, height=720, frames=81, steps=40, guidance=3.5, guidance_2=3.5)


def load_config(path: Path | None = None, story: str | None = None,
                character: str | None = None) -> dict:
    """A standalone character file (the fox), or a character from a story.

    Story characters are never re-described here: the sheet, style and
    negative come from stories/<slug>/story.yaml, and only the poses to shoot
    live in stories/<slug>/packs/<character>.yaml.
    """
    import yaml

    if story is None:
        cfg = yaml.safe_load(path.read_text())
        cfg.setdefault("subject", "The fox")
        cfg["_workdir"] = paths.WORK / "characters" / cfg["name"]
        return cfg
    root = paths.REPO / "stories" / story
    s = yaml.safe_load((root / "story.yaml").read_text())
    c = s["characters"][character]
    pack_file = root / "packs" / f"{character}.yaml"
    pack = yaml.safe_load(pack_file.read_text()) if pack_file.is_file() else {}
    return dict(
        name=character, subject=c["name"][0].upper() + c["name"][1:],
        trigger=c.get("trigger", f"twc{character}"), character=c["sheet"],
        set=pack.get("set", PLAIN_SET), style=s["style"], negative=s["negative"],
        render={**DEFAULT_RENDER, **pack.get("render", {})},
        canonical={"design": str(paths.WORK / "stories" / story / "design" / character)},
        orbit=pack.get("orbit"), shots=pack.get("shots", []),
        _workdir=paths.WORK / "stories" / story / "characters" / character,
    )


def assemble(cfg: dict, action: str) -> str:
    """Step 1: every prompt = the action + the character sheet + the set + style."""
    return (f"{action.strip()} {cfg['subject']} is {cfg['character']}. "
            f"The scene is {cfg['set']}. {cfg['style']}.")


def sidecar(path: Path, **info) -> None:
    info["created"] = time.strftime("%Y-%m-%d %H:%M:%S")
    path.with_suffix(".json").write_text(json.dumps(info, indent=2, default=str))


def stage_canonical(cfg: dict) -> None:
    import cv2
    from PIL import Image

    c = cfg["canonical"]
    if "design" in c:                      # a story character: the still picked in design
        import shutil

        src = Path(c["design"]) / "canonical.png"
        out = cfg["_workdir"] / "canonical.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, out)
        sidecar(out, stage="canonical", source=str(src), how="picked in production/design.py")
        print(f"canonical: {src} -> {out}")
        return
    clip = paths.CHANNEL / c["clip"]
    frames = media.read_frames(clip)
    if c.get("frame", "auto") == "auto":
        lo, hi = c.get("window", [0, len(frames) - 1])
        scores = {i: float(cv2.Laplacian(cv2.cvtColor(frames[i], cv2.COLOR_RGB2GRAY),
                                         cv2.CV_64F).var())
                  for i in range(lo, min(hi, len(frames) - 1) + 1)}
        index = max(scores, key=scores.get)
    else:
        index, scores = int(c["frame"]), {}
    out = cfg["_workdir"] / "canonical.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(frames[index]).save(out)
    sidecar(out, stage="canonical", source_clip=str(clip), frame=index,
            sharpness=scores.get(index), how="sharpest frame (variance of Laplacian) in window"
            if scores else "frame given in config")
    print(f"canonical: frame {index} of {clip.name} -> {out}")


def _render(cfg: dict, stage: str, action: str, image_path: Path, seed: int, out: Path,
            negative_extra: str = "") -> None:
    from PIL import Image

    r = cfg["render"]
    prompt = assemble(cfg, action)
    negative = cfg["negative"] + (", " + negative_extra if negative_extra else "")
    print(f"[{stage}] {out.name}\n  from  {image_path}\n  seed  {seed}\n  prompt {prompt}",
          flush=True)
    pipe = wan.load("i2v", r["frames"])
    print("  model loaded", flush=True)
    frames = wan.generate(pipe, prompt, negative=negative, width=r["width"],
                          height=r["height"], frames=r["frames"], steps=r["steps"],
                          guidance=r["guidance"], guidance_2=r["guidance_2"], seed=seed,
                          image=Image.open(image_path))
    wan.save(frames, out)
    sidecar(out, stage=stage, model=wan.MODELS["i2v"], start_image=str(image_path),
            seed=seed, prompt=prompt, negative=negative, **r)
    print(f"  saved {out}", flush=True)


def stage_orbit(cfg: dict, redo: bool = False) -> None:
    o = cfg["orbit"]
    wd = cfg["_workdir"]
    if (wd / "orbit.mp4").is_file() and not redo:
        print(f"orbit: {wd / 'orbit.mp4'} exists, skipping (use --redo to re-render)")
        return
    _render(cfg, "orbit", o["action"], wd / "canonical.png", o["seed"], wd / "orbit.mp4",
            o.get("negative_extra", ""))


def stage_angles(cfg: dict) -> None:
    import cv2
    import numpy as np
    from PIL import Image

    wd = cfg["_workdir"]
    frames = media.read_frames(wd / "orbit.mp4")
    tiles = []
    for k, index in enumerate(cfg["orbit"]["angles"]):
        index = min(index, len(frames) - 1)
        out = wd / "angles" / f"angle_{k}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(frames[index]).save(out)
        sidecar(out, stage="angles", source_clip=str(wd / "orbit.mp4"), frame=index)
        tile = cv2.resize(frames[index], (384, 216)).copy()
        cv2.putText(tile, f"angle_{k} (f{index})", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255), 2, cv2.LINE_AA)
        tiles.append(tile)
    Image.fromarray(np.concatenate(tiles, axis=1)).save(wd / "angles" / "contact_sheet.png")
    print(f"angles: {len(tiles)} keyframes -> {wd / 'angles'}")


def stage_shots(cfg: dict, only: list[str] | None, redo: bool = False) -> None:
    wd = cfg["_workdir"]
    for shot in cfg["shots"]:
        if only and shot["name"] not in only:
            continue
        out = wd / "shots" / f"{shot['name']}.mp4"
        if out.is_file() and not redo:
            print(f"shot {shot['name']}: {out} exists, skipping (use --redo to re-render)")
            continue
        src = wd / ("canonical.png" if shot["from"] == "canonical"
                    else f"angles/{shot['from']}.png")
        _render(cfg, "shot", shot["action"], src, shot["seed"], wd / "shots" / f"{shot['name']}.mp4")


def stage_dataset(cfg: dict, every: int) -> None:
    """Step 3 preparation: stills of the character with captions, ready for a LoRA."""
    import shutil

    from PIL import Image

    wd = cfg["_workdir"]
    ds = wd / "dataset"
    ds.mkdir(parents=True, exist_ok=True)
    caption = f"{cfg['trigger']}, {cfg['character']}, {cfg['style']}"
    items = [wd / "canonical.png"] + sorted((wd / "angles").glob("angle_*.png"))
    n = 0
    for src in items:
        if src.is_file():
            shutil.copy(src, ds / src.name)
            (ds / src.name).with_suffix(".txt").write_text(caption)
            n += 1
    for clip in sorted((wd / "shots").glob("*.mp4")):
        for i, frame in enumerate(media.read_frames(clip)[::every]):
            name = f"{clip.stem}_{i:03d}.png"
            Image.fromarray(frame).save(ds / name)
            (ds / name).with_suffix(".txt").write_text(caption)
            n += 1
    print(f"dataset: {n} captioned stills -> {ds}")


def stage_assemble(cfg: dict, clips: list[str], out: Path) -> None:
    """Join shots with hard cuts, bring them to 1080p30 and add a lullaby.

    `clips` are shot names from the config, or paths (relative to the channel
    folder) for clips made elsewhere, such as the shot the canonical still was
    taken from.
    """
    import subprocess

    import numpy as np
    import torch

    from twc import post as vp

    wd = cfg["_workdir"]
    paths_in = []
    for c in clips:
        p = wd / "shots" / f"{c}.mp4"
        paths_in.append(p if p.is_file() else paths.CHANNEL / c)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    parts, cuts, t = [], [], 0.0
    for p in paths_in:
        frames = vp.retime(vp.decode(p), wan.FPS, 1.0, 30, device)
        print(f"  {p.name}: {len(frames)} frames at 30 fps", flush=True)
        parts.append(frames)
        t += len(frames) / 30
        cuts.append(t)
    frames = np.concatenate(parts)
    print(f"  upscaling {len(frames)} frames to 1920x1080 on {device}", flush=True)
    frames = vp.upscale(frames, 1920, 1080, device)
    silent = wd / f"{out.stem}_silent.mp4"
    vp.encode(frames, silent, 30, vf=vp.GRADE_VF)
    duration = len(frames) / 30
    music = wd / f"{out.stem}_lullaby.wav"
    subprocess.run([sys.executable, str(paths.REPO / "audio" / "make_lullaby.py"),
                    "--duration", f"{duration + 0.1:.2f}", "--chime-at",
                    *[f"{c:.3f}" for c in cuts[:-1]], "-o", str(music)], check=True)
    media.finish(concat_video=silent, audio_source=music, output=out,
                 target_duration=duration, source_duration=duration, final_width=1920,
                 final_height=1080, final_fps=30, hold_end=0.0, audio_restart_at=None)
    sidecar(out, stage="assemble", clips=[str(p) for p in paths_in], cuts=cuts[:-1],
            duration=duration)
    print(f"Saved {out} ({duration:.2f} s, cuts at {', '.join(f'{c:.2f}' for c in cuts[:-1])})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["canonical", "orbit", "angles", "shots", "dataset",
                                      "assemble", "prompt"])
    ap.add_argument("--config", type=Path,
                    default=Path(__file__).resolve().parent / "characters" / "fox.yaml")
    ap.add_argument("--story", help="use a story character: --story lion_and_mouse --character leo")
    ap.add_argument("--character")
    ap.add_argument("--only", nargs="+", help="shots: render only these shot names")
    ap.add_argument("--every", type=int, default=8, help="dataset: keep every Nth shot frame")
    ap.add_argument("--clips", nargs="+",
                    help="assemble: shot names, or clip paths relative to the channel folder")
    ap.add_argument("-o", "--output", type=Path, help="assemble: output video")
    ap.add_argument("--redo", action="store_true",
                    help="orbit/shots: re-render even if the output already exists")
    args = ap.parse_args()
    cfg = load_config(args.config, args.story, args.character)

    if args.stage == "prompt":
        if cfg.get("orbit"):
            print("orbit:", assemble(cfg, cfg["orbit"]["action"]), "\n")
        for s in cfg["shots"]:
            print(f"{s['name']} (from {s['from']}):", assemble(cfg, s["action"]), "\n")
        return
    {"canonical": lambda: stage_canonical(cfg), "orbit": lambda: stage_orbit(cfg, args.redo),
     "angles": lambda: stage_angles(cfg), "shots": lambda: stage_shots(cfg, args.only, args.redo),
     "dataset": lambda: stage_dataset(cfg, args.every),
     "assemble": lambda: stage_assemble(cfg, args.clips,
                                        args.output or paths.OUTPUT / f"{cfg['name']}_sequence.mov"),
     }[args.stage]()


if __name__ == "__main__":
    main()
