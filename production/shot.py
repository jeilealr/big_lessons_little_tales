#!/usr/bin/env python3
"""Render a story shot: image-to-video from its composed keyframe.

The shot is defined in story.yaml under its scene (`shots:`). The prompt is
the shot's action, then each character's frozen sheet, then the location sheet
and the style bible, exactly like the text-only baseline (production/
scene_baseline.py), so the only difference between the two is the anchored
first frame.

  python production/shot.py --scene 1 --shot s01_establish [--seed 5101]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import paths, post, wan  # noqa: E402

RENDER = dict(width=1280, height=720, steps=40, guidance=3.5, guidance_2=3.5)


def main() -> None:
    import yaml
    from PIL import Image

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse")
    ap.add_argument("--scene", type=int, required=True)
    ap.add_argument("--shot", required=True)
    ap.add_argument("--seed", type=int, help="default: every seed listed for the shot")
    ap.add_argument("--recompose", action="store_true",
                    help="rebuild the keyframe from the shot's compose: recipe even if it exists")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    story = yaml.safe_load((paths.REPO / "stories" / args.story / "story.yaml").read_text())
    scene = story["scenes"][args.scene]
    shot = next(s for s in scene["shots"] if s["name"] == args.shot)
    work = paths.WORK / "stories" / args.story
    keyframe = work / shot["keyframe"]
    parts = [shot["action"].strip()]
    # `lora: true` on a shot: every character in it that has a chosen LoRA
    # (`lora:` under the character) gets it, and its trigger word in the prompt,
    # the way the training captions put it: "<trigger>, <description>".
    loras = []
    for c in shot.get("characters", scene.get("characters", [])):
        ch = story["characters"][c]
        use = shot.get("lora") and ch.get("lora")
        if use:
            d = paths.WORK / "lora" / ch["lora"]["name"]
            suf = f"-step{int(ch['lora']['step']):08d}" if ch["lora"].get("step") else ""
            loras.append(dict(name=c, weight=ch["lora"].get("weight", 1.0),
                              high=d / "out_high" / f"{ch['lora']['name']}_high{suf}.safetensors",
                              low=d / "out_low" / f"{ch['lora']['name']}_low{suf}.safetensors"))
        name = ch["name"][0].upper() + ch["name"][1:]
        parts.append(f"{name} is {ch['trigger'] + ', ' if use else ''}{ch['sheet']}.")
    # `background:` replaces the location sheet, for close-ups: the full sheet
    # names landmarks (a tree trunk...) that the model then tries to show,
    # wandering away from the keyframes mid-shot (v2 s04_leo_softens).
    if shot.get("background"):
        parts.append(f"The background is {shot['background'].strip()}.")
    else:
        parts.append(f"The scene is {story['locations'][scene['location']]['sheet']}.")
    parts.append(story["style"] + ".")
    prompt = " ".join(parts)
    seeds = [args.seed] if args.seed else shot["seeds"]
    frames = shot.get("frames", 81)
    print(f"[{args.shot}] keyframe {keyframe.name}, {frames} frames, seeds {seeds}\n{prompt}\n",
          flush=True)
    # `continue_from: {shot, take, frame}`: the keyframe is a frame (default: the
    # last) of another shot's render, so the cut is continuous.
    cont = shot.get("continue_from")
    if cont:
        src = work / "shots" / f"{cont['shot']}_s{cont['take']}.mp4"
        if not src.is_file():
            raise SystemExit(f"continue_from: missing render {src}")
        print(f"keyframe = frame {cont.get('frame', -1)} of {src.name}")
    recipe = shot.get("compose")
    if recipe and not cont:
        for c in recipe["characters"]:
            if not (work / c["still"]).is_file():
                raise SystemExit(f"keyframe recipe: missing still {work / c['still']}")
        if not (work / recipe["plate"]).is_file():
            raise SystemExit(f"keyframe recipe: missing plate {work / recipe['plate']}")
    elif not cont and not keyframe.is_file():
        raise SystemExit(f"missing keyframe {keyframe} and no compose: recipe")
    for lo in loras:
        for f in (lo["high"], lo["low"]):
            if not f.is_file():
                raise SystemExit(f"missing LoRA {f}")
        print(f"LoRA {lo['name']}: {lo['high'].name} + {lo['low'].name} x{lo['weight']}")
    if (shot.get("end_keyframe") and shot["end_keyframe"] != shot["keyframe"]
            and not (work / shot["end_keyframe"]).is_file()):
        er = shot.get("end_compose")
        if not er:
            raise SystemExit(f"missing end keyframe {shot['end_keyframe']} and no end_compose")
        for c in er["characters"]:
            if not (work / c["still"]).is_file():
                raise SystemExit(f"end_compose: missing still {work / c['still']}")
    if args.dry_run:
        print("dry run: inputs ok" + (" (keyframe will be composed)" if recipe else ""))
        return
    if cont and (args.recompose or not keyframe.is_file()):
        frames_ = post.decode(src)
        keyframe.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(frames_[int(cont.get("frame", -1))]).save(keyframe)
        print(f"keyframe from {src.name} -> {keyframe}", flush=True)
    elif recipe and (args.recompose or not keyframe.is_file()):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from keyframe import compose

        compose(work / recipe["plate"],
                [{**c, "still": str(work / c["still"])} for c in recipe["characters"]],
                keyframe, recipe.get("crop"), recipe.get("blur", 0.0))
        print(f"composed keyframe {keyframe}", flush=True)
    # `end_keyframe:` (+ optional `end_compose:` recipe): the frame the shot must
    # arrive at. Wan 2.2 I2V-A14B then animates between two stills (first/last
    # frame), which pins identity and pose at both ends (docs/prompting.md 3.4).
    end_key = work / shot["end_keyframe"] if shot.get("end_keyframe") else None
    end_recipe = shot.get("end_compose")
    if end_key and (args.recompose or not end_key.is_file()):
        if not end_recipe:
            raise SystemExit(f"missing end keyframe {end_key} and no end_compose: recipe")
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from keyframe import compose

        compose(work / end_recipe["plate"],
                [{**c, "still": str(work / c["still"])} for c in end_recipe["characters"]],
                end_key, end_recipe.get("crop"), end_recipe.get("blur", 0.0))
        print(f"composed end keyframe {end_key}", flush=True)
    pipe = wan.load("i2v", frames, loras=loras)
    print("model loaded", flush=True)
    for seed in seeds:
        out = work / "shots" / f"{args.shot}_s{seed}.mp4"
        if out.is_file():
            print(f"exists, skipping {out.name}"); continue
        t0 = time.time()
        negative = story["negative"] + (", " + shot["negative_extra"] if shot.get("negative_extra") else "")
        video = wan.generate(pipe, prompt, negative=negative, frames=frames, seed=seed,
                             image=Image.open(keyframe),
                             last_image=Image.open(end_key) if end_key else None, **RENDER)
        wan.save(video, out)
        out.with_suffix(".json").write_text(json.dumps(dict(
            stage="shot", scene=args.scene, shot=args.shot, keyframe=str(keyframe),
            end_keyframe=str(end_key) if end_key else None,
            model=wan.model_id("i2v"), seed=seed, frames=frames, prompt=prompt,
            negative=negative, loras=[{k: str(v) for k, v in lo.items()} for lo in loras],
            seconds=round(time.time() - t0), **RENDER), indent=2))
        print(f"saved {out} ({time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
