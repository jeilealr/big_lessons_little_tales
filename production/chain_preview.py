#!/usr/bin/env python3
"""Join test for a chained story (CR-21): play a stretch of the film against its narration and
measure every join. CPU only, minutes; run it when the owner asks for a preview or a join test.

  # before any GPU time: the planned images, timed to the narration (pacing and chain check)
  python production/chain_preview.py --story lion_and_mouse_v6 --stills --until 120
  # after a pilot is rendered and takes are chosen: the start of the film from the chosen takes
  python production/chain_preview.py --story lion_and_mouse_v6 --until 120

Reads stories/<story>/timing_plan.json (production/chain_plan.py apply), the manifest (image
files) and the narration (work/stories/<audio story>/audio/<lang>/sceneNN.wav).

Pictures per piece, in film order, each lasting exactly its planned seconds:
  --stills    the start image blending into the end image (a hold stays still). No clips needed.
  (default)   the owner's chosen take: stories/<story>/takes.yaml maps a piece (or variant) id to
              a seed (`s01_enter: 2`) or a file path, or the take is the one renamed with a `best_`
              prefix in work/stories/<story>/shots/ (for a `reuse` piece, in the reused story's
              shots/). A piece without a chosen take is shown as its stills and listed as such;
              `--any-seed N` shows seed N instead, captioned UNSELECTED (never an owner choice).
Clips are retimed to their slot by nearest frame (post uses RIFE; this is a preview).
Cuts with `transition: crossfade` blend 0.5 s, `dip` fades through black; chains are hard joins.

Join report (takes mode): for every chain join with a clip on both sides, `jump` is the mean
absolute difference (0-255, quarter-size grey) between the last frame of the earlier clip and the
first frame of the next; `motion` is the median frame-to-frame difference in the 8 frames on each
side. jump/motion above 3 is flagged: it reads as a visible jump. Repair: re-render the later
piece with `continue_from` the chosen take's last frame, or adjust the boundary image (CR-21).
Also `pace`: the motion just before the join over the motion just after; far from 1 means the
movement speeds up or stops at the cut.

Output: work/stories/<story>/review/chain_preview_<from>-<until>[_stills].mp4, its .json report
and, in takes mode, chain_joins_<from>-<until>.jpg (per join: last frame, first frame, difference).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import media, paths  # noqa: E402

FPS = 24
SR = 48000
CLIP_FPS = 16
XFADE, DIP = 0.5, 0.4
FLAG = 3.0


def load_img(path: Path, size, rid: str = "") -> np.ndarray:
    """The image, or a grey card naming it when it is not made yet (a planned record)."""
    from PIL import Image, ImageDraw, ImageFont

    if path.is_file():
        return np.asarray(Image.open(path).convert("RGB").resize(size, Image.LANCZOS), dtype=np.float32)
    img = Image.new("RGB", size, (70, 70, 70))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=size[1] // 18)
    d.text((size[0] // 12, size[1] // 3), f"not made yet:\n{rid}\n{path.name}", fill=(235, 235, 235), font=font)
    return np.asarray(img, dtype=np.float32)


def caption(frame: np.ndarray, text: str) -> np.ndarray:
    from PIL import Image, ImageDraw, ImageFont

    img = Image.fromarray(frame)
    d = ImageDraw.Draw(img, "RGBA")
    h = img.height // 16
    d.rectangle([0, img.height - h, img.width, img.height], fill=(0, 0, 0, 150))
    d.text((10, img.height - h + h // 5), text, font=ImageFont.load_default(size=int(h * 0.55)),
           fill=(255, 255, 255))
    return np.asarray(img)


def small_grey(f: np.ndarray) -> np.ndarray:
    g = f[::4, ::4].astype(np.float32)
    return g @ np.array([0.299, 0.587, 0.114], dtype=np.float32)


def find_take(story: str, row: dict, takes: dict, any_seed: int | None) -> tuple[Path | None, str]:
    """(clip, how): the owner's chosen take, else seed --any-seed (UNSELECTED), else none."""
    src_story, variant = story, row["variant"]
    if row.get("reuse"):
        src_story, variant = row["reuse"]["story"], row["reuse"]["variant"]
    shots = paths.story_work(src_story) / "shots"
    choice = takes.get(row["piece"], takes.get(row["variant"]))
    if isinstance(choice, int):
        for sfx in ("_fast", ""):
            for pre in ("best_", ""):
                f = shots / f"{pre}{variant}_s{choice}{sfx}.mp4"
                if f.is_file():
                    return f, f"take s{choice}"
        return None, f"takes.yaml seed {choice} not found"
    if isinstance(choice, str):
        f = paths.REPO / choice
        return (f, "take file") if f.is_file() else (None, f"takes.yaml file {choice} not found")
    best = sorted(shots.glob(f"best_{variant}_s*.mp4"))
    if len(best) == 1:
        return best[0], f"take {best[0].stem.split('_s')[-1]}"
    if len(best) > 1:
        return None, f"{len(best)} best_ takes; choose one in takes.yaml"
    if any_seed is not None:
        for sfx in ("_fast", ""):
            f = shots / f"{variant}_s{any_seed}{sfx}.mp4"
            if f.is_file():
                return f, f"UNSELECTED seed {any_seed}"
    return None, "no chosen take"


def narration(story: str, lang: str, scenes: list[int]) -> np.ndarray:
    parts = []
    for n in scenes:
        p = paths.story_audio(story, lang) / f"scene{n:02d}.wav"
        raw = subprocess.run([media.locate_ffmpeg(), "-v", "error", "-i", str(p), "-f", "s16le", "-ac", "1",
                              "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        parts.append(np.frombuffer(raw, dtype=np.int16))
    return np.concatenate(parts) if parts else np.zeros(0, np.int16)


def main() -> None:
    import yaml

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", required=True)
    ap.add_argument("--from", dest="t0", type=float, default=0.0, help="film seconds (default 0)")
    ap.add_argument("--until", type=float, help="film seconds (default: the end)")
    ap.add_argument("--stills", action="store_true", help="planned images only, no clips")
    ap.add_argument("--any-seed", type=int, help="show this seed where no take is chosen (captioned UNSELECTED)")
    ap.add_argument("--size", default="960x540")
    ap.add_argument("--no-captions", action="store_true")
    args = ap.parse_args()
    size = tuple(int(v) for v in args.size.split("x"))

    sd = paths.STORIES / args.story
    tp = json.loads((sd / "timing_plan.json").read_text())
    if tp.get("kind") != "chained_coverage":
        sys.exit(f"{sd / 'timing_plan.json'} is not a chained plan (run production/chain_plan.py apply)")
    man = json.loads((sd / "prompt_manifest.json").read_text())
    target = {i["id"]: paths.REPO / i["target"] for i in man["images"]}
    takes_file = sd / "takes.yaml"
    takes = (yaml.safe_load(takes_file.read_text()) or {}) if takes_file.is_file() else {}
    t1 = args.until if args.until is not None else tp["seconds"]
    rows = [r for r in tp["segments"] if r["film_start"] + r["seconds"] > args.t0 and r["film_start"] < t1]
    if not rows:
        sys.exit("no pieces in that time range")
    t0 = rows[0]["film_start"]                      # start on a piece boundary
    t1 = min(t1, rows[-1]["film_start"] + rows[-1]["seconds"])

    tag = f"{int(t0)}-{int(t1)}" + ("_stills" if args.stills else "")
    out = paths.story_work(args.story) / "review" / f"chain_preview_{tag}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp_v, tmp_a = out.with_name(out.stem + "_video.mp4"), out.with_name(out.stem + "_audio.wav")
    enc = subprocess.Popen([media.locate_ffmpeg(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{size[0]}x{size[1]}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-crf", "20", "-pix_fmt", "yuv420p", str(tmp_v)], stdin=subprocess.PIPE)

    report, joins, written, prev = [], [], 0, None
    for r in rows:
        clip, how = (None, "stills") if args.stills else find_take(args.story, r, takes, args.any_seed)
        frames = None
        if clip is not None:
            frames = media.read_frames(clip)
            if len(frames) != r["frames"]:
                how += f" ({len(frames)} frames, plan {r['frames']})"
        start_img = load_img(target[r["start_image"]], size, r["start_image"])
        end_img = load_img(target[r["end_image"]], size, r["end_image"])
        end_t = r["film_start"] + r["seconds"] - t0
        n = int(round(end_t * FPS)) - written
        label = (f"{r['piece']}  |  {'chain' if r['join_in'] == 'chain' else 'cut: ' + str(r['cut_reason'])}"
                 f"  |  {how}  |  {r['frames']}f x{r['speed']:.2f}")
        out_frames = []
        for i in range(n):
            if frames is not None:
                k = min(int(round(i / FPS * CLIP_FPS * r["speed"])), len(frames) - 1)
                f = np.asarray(media_resize(frames[k], size), dtype=np.float32)
            else:
                a = i / max(1, n - 1)
                f = start_img * (1 - a) + end_img * a
            out_frames.append(f)
        # planned transitions at cuts: blend over the first frames of this piece
        if prev is not None and r["join_in"] == "cut" and r.get("transition") in ("crossfade", "dip"):
            span = int((XFADE if r["transition"] == "crossfade" else DIP) * FPS)
            for i in range(min(span, len(out_frames))):
                a = (i + 1) / (span + 1)
                if r["transition"] == "crossfade":
                    out_frames[i] = prev["last_out"] * (1 - a) + out_frames[i] * a
                else:
                    out_frames[i] = out_frames[i] * abs(2 * a - 1)
        for f in out_frames:
            f8 = np.clip(f, 0, 255).astype(np.uint8)
            enc.stdin.write((f8 if args.no_captions else caption(f8, label)).tobytes())
        written += n
        if prev is not None and r["join_in"] == "chain" and frames is not None and prev["frames"] is not None:
            a, b = prev["frames"], frames
            jump = float(np.abs(small_grey(a[-1]) - small_grey(b[0])).mean())
            steps_a = [float(np.abs(small_grey(a[k]) - small_grey(a[k - 1])).mean()) for k in range(max(1, len(a) - 8), len(a))]
            steps_b = [float(np.abs(small_grey(b[k]) - small_grey(b[k - 1])).mean()) for k in range(1, min(9, len(b)))]
            motion = max(float(np.median(steps_a + steps_b)), 0.5)
            pace = (np.mean(steps_a[-4:]) + 0.25) / (np.mean(steps_b[:4]) + 0.25)
            joins.append(dict(before=prev["piece"], after=r["piece"], image=r["start_image"],
                              jump=round(jump, 2), motion=round(motion, 2), ratio=round(jump / motion, 2),
                              pace=round(float(pace), 2), flagged=jump / motion > FLAG,
                              last=a[-1], first=b[0]))
        report.append(dict(piece=r["piece"], film_start=r["film_start"], seconds=r["seconds"], frames=r["frames"],
                           speed=r["speed"], join_in=r["join_in"], cut_reason=r.get("cut_reason"), shown=how,
                           clip=str(clip.relative_to(paths.WORK)) if clip else None))
        prev = dict(piece=r["piece"], frames=frames, last_out=out_frames[-1] if out_frames else end_img)
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("ffmpeg encode failed")

    scenes = sorted({r["scene"] for r in tp["segments"]})
    audio = narration(tp.get("audio_story") or args.story, tp.get("lang", "en"), scenes)
    a0, a1 = int(t0 * SR), int(t0 * SR) + int(round(written / FPS * SR))
    clipped = audio[a0:a1]
    clipped = np.concatenate([clipped, np.zeros(max(0, a1 - a0 - len(clipped)), np.int16)])
    with wave.open(str(tmp_a), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(clipped.tobytes())
    subprocess.run([media.locate_ffmpeg(), "-y", "-v", "error", "-i", str(tmp_v), "-i", str(tmp_a), "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)], check=True)
    tmp_v.unlink()
    tmp_a.unlink()

    if joins:
        join_sheet(joins, out.with_name(f"chain_joins_{tag}.jpg"))
    out.with_suffix(".json").write_text(json.dumps(dict(
        stage="chain_preview", story=args.story, mode="stills" if args.stills else "takes", fps=FPS,
        film_from=t0, film_until=round(t0 + written / FPS, 3), pieces=report,
        joins=[{k: v for k, v in j.items() if k not in ("last", "first")} for j in joins]), indent=2) + "\n")
    missing = [p for p in report if not args.stills and p["clip"] is None]
    print(f"{len(report)} pieces, {written / FPS:.1f} s -> {out}")
    if missing:
        print(f"{len(missing)} pieces shown as stills (no chosen take): " + ", ".join(p["piece"] for p in missing))
    for j in joins:
        flag = "  <-- visible jump: repair candidate" if j["flagged"] else ""
        print(f"join {j['before']} -> {j['after']}: jump {j['jump']:.1f}, motion {j['motion']:.1f}, "
              f"ratio {j['ratio']:.1f}, pace {j['pace']:.2f}{flag}")


def media_resize(frame: np.ndarray, size) -> np.ndarray:
    from PIL import Image

    if frame.shape[1] == size[0] and frame.shape[0] == size[1]:
        return frame
    return np.asarray(Image.fromarray(frame).resize(size, Image.BILINEAR))


def join_sheet(joins: list[dict], path: Path) -> None:
    """One row per chain join: last frame before, first frame after, amplified difference."""
    from PIL import Image, ImageDraw, ImageFont

    w, h = 384, 216
    font = ImageFont.load_default(size=16)
    sheet = Image.new("RGB", (3 * w + 8, len(joins) * (h + 24)), "white")
    for k, j in enumerate(joins):
        a = Image.fromarray(j["last"]).resize((w, h))
        b = Image.fromarray(j["first"]).resize((w, h))
        d = np.clip(np.abs(np.asarray(a, np.int16) - np.asarray(b, np.int16)) * 4, 0, 255).astype(np.uint8)
        y = k * (h + 24)
        for x, im in enumerate((a, b, Image.fromarray(d))):
            sheet.paste(im, (x * (w + 4), y))
        ImageDraw.Draw(sheet).text(
            (4, y + h + 3), f"{j['before']} -> {j['after']}  jump {j['jump']:.1f}  motion {j['motion']:.1f}  "
            f"ratio {j['ratio']:.1f}  pace {j['pace']:.2f}{'  FLAGGED' if j['flagged'] else ''}",
            fill="red" if j["flagged"] else "black", font=font)
    sheet.save(path, quality=88)


if __name__ == "__main__":
    main()
