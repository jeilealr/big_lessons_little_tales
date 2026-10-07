#!/usr/bin/env python3
"""Cut an animatic: the whole story at its planned pacing, before (and while)
rendering. Minutes on a CPU; no GPU. Run it only when the owner asks for an
assembly (docs/production-guide.md section 8): it is not a take selector.

For every scene in story.yaml, in order, each shot (except `superseded_by` and
`variant_of` ones) shows
  * its chosen render, if the shot has `take: <seed>` and the clip exists
    (<shot>_s<take>.mp4, else <shot>_s<take>_fast.mp4),
  * else its keyframe still, if composed,
  * else (a scene without shots yet) a card with the scene's title and text.
Every such fallback is listed in the report.

Timing comes from the narration when it exists: put the narration for
scene N (Gemini voices, voice/) at `work/stories/<story>/audio/<lang>/sceneNN.wav`
(or .mp3/.m4a; without --lang: `work/stories/<story>/audio/sceneNN.wav`). The scene then
lasts the narration plus a short breath, split evenly across its shots, and the
narration is the soundtrack. Without narration: a clip keeps its own length, a
still 5 s, a card 4 s.

The report at the end is the point: which scenes need more shots than they
have (the narration outlasts the clips), and where a render is held on its last
frame.

  python production/animatic.py [--story lion_and_mouse_v2] [--size 960x540] [--lang en]

Output: work/stories/<story>/animatic[_<lang>].mp4 + .json (the report).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from feltwillow import media, paths, wan  # noqa: E402

FPS = 24
SR = 48000
BREATH = 0.6          # seconds of silence after each scene's narration
DEFAULT = dict(clip=None, still=5.0, card=4.0)


def narration(story: str, n: int, lang: str | None = None) -> Path | None:
    base = paths.story_audio(story, lang)
    for ext in ("wav", "mp3", "m4a"):
        p = base / f"scene{n:02d}.{ext}"
        if p.is_file():
            return p
    return None


def read_audio(path: Path) -> np.ndarray:
    raw = subprocess.run([media.locate_ffmpeg(), "-v", "error", "-i", str(path), "-f", "s16le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16)


def font(size: int):
    from PIL import ImageFont

    return ImageFont.load_default(size=size)


def caption(img, text: str):
    """A strip along the bottom: scene, shot, source. Burned in on purpose."""
    from PIL import ImageDraw

    d = ImageDraw.Draw(img, "RGBA")
    h = img.height // 14
    d.rectangle([0, img.height - h, img.width, img.height], fill=(0, 0, 0, 150))
    d.text((12, img.height - h + h // 5), text, font=font(int(h * 0.55)), fill=(255, 255, 255))
    return img


def card(size, title: str, body: str):
    from PIL import Image, ImageDraw

    img = Image.new("RGB", size, (58, 74, 52))
    d = ImageDraw.Draw(img)
    w, h = size
    d.text((w // 12, h // 6), title, font=font(h // 12), fill=(250, 238, 210))
    y = h // 6 + h // 8
    for line in textwrap.wrap(body, width=58)[:9]:
        d.text((w // 12, y), line, font=font(h // 26), fill=(230, 225, 205))
        y += h // 18
    return img


def main() -> None:
    import yaml
    from PIL import Image

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v2")
    ap.add_argument("--size", default="960x540")
    ap.add_argument("--lang", help="narration from work/stories/<story>/audio/<lang>/")
    args = ap.parse_args()
    size = tuple(int(v) for v in args.size.split("x"))

    story = yaml.safe_load((paths.STORIES / args.story / "story.yaml").read_text())
    work = paths.story_work(args.story)
    out = work / (f"animatic_{args.lang}.mp4" if args.lang else "animatic.mp4")
    # Per-output temporary names, so animatics of two languages can run side by side.
    tmp_video = out.with_name(f"{out.stem}_video.mp4")
    tmp_audio = out.with_name(f"{out.stem}_audio.wav")
    cmd = [media.locate_ffmpeg(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{size[0]}x{size[1]}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
           "-crf", "23", "-pix_fmt", "yuv420p", str(tmp_video)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    audio: list[np.ndarray] = []
    report, t = [], 0.0
    written = 0           # video frames so far; slots are rounded on the running total

    for n in sorted(story["scenes"]):
        scene = story["scenes"][n]
        segs, notes = [], []
        for shot in scene.get("shots", []):
            if shot.get("superseded_by") or shot.get("variant_of"):
                continue
            clip = None
            if shot.get("take"):          # a 40-step render, or a fast-mode one (_fast)
                found = [work / "shots" / f"{shot['name']}_s{shot['take']}{sfx}.mp4"
                         for sfx in ("", "_fast")]
                found = [f for f in found if f.is_file()]
                clip = found[0] if found else None
                if len(found) > 1:
                    notes.append(f"{shot['name']}: take {shot['take']} exists as standard and "
                                 f"_fast render; the standard one is shown")
                elif not found:
                    notes.append(f"{shot['name']}: no render of take {shot['take']}")
            if clip:
                segs.append(("clip", clip, shot["name"]))
            elif (work / shot["keyframe"]).is_file():
                segs.append(("still", work / shot["keyframe"], shot["name"]))
            else:
                notes.append(f"{shot['name']}: no render and no keyframe, left out")
        if not segs:
            segs.append(("card", None, "no shots yet"))

        voice = narration(args.story, n, args.lang)
        if voice is not None:
            wav = read_audio(voice)
            length = len(wav) / SR + BREATH
            slots = [length / len(segs)] * len(segs)
            audio.append(np.concatenate([wav, np.zeros(int(length * SR) - len(wav), np.int16)]))
        else:
            slots = []
            for kind, src, _ in segs:
                slots.append(len(media.read_frames(src)) / wan.FPS if kind == "clip" else DEFAULT[kind])
            length = sum(slots)
            audio.append(np.zeros(int(length * SR), np.int16))

        end = t
        for (kind, src, name), slot in zip(segs, slots):
            source = (f"take {src.stem.split('_s')[-1]}" if kind == "clip"
                      else "keyframe only" if kind == "still" else "not planned")
            label = f"{n}. {scene['title']}  |  {name}  |  {source}"
            # Rounding each slot on its own drifted the pictures away from the
            # narration (up to ~1.7 s over a film); round the running end instead.
            end += slot
            nframes = int(round(end * FPS)) - written
            written += nframes
            if kind == "clip":
                frames = media.read_frames(src)
                have = len(frames) / wan.FPS
                if have + 0.05 < slot:
                    notes.append(f"{name}: clip {have:.1f}s held to fill {slot:.1f}s")
                for i in range(nframes):
                    f = frames[min(int(i / FPS * wan.FPS), len(frames) - 1)]
                    img = caption(Image.fromarray(f).resize(size, Image.LANCZOS), label)
                    enc.stdin.write(np.asarray(img).tobytes())
                continue
            if kind == "still":
                img = Image.open(src).convert("RGB").resize(size, Image.LANCZOS)
            else:
                text = scene.get("text") or scene.get("narration") or scene.get("beat", "")
                img = card(size, f"{n}. {scene['title']}", " ".join(text.split()))
            frame = np.asarray(caption(img, label)).tobytes()
            for _ in range(nframes):
                enc.stdin.write(frame)
        if voice is not None and len(segs) and length / len(segs) > 5.1:
            notes.append(f"narration {length:.1f}s over {len(segs)} shot(s): "
                         f"{length / len(segs):.1f}s each (renders are 5.1s)")
        report.append(dict(scene=n, title=scene["title"], start=round(t, 1),
                           seconds=round(length, 1), shots=len(segs),
                           narration=str(voice) if voice else None, notes=notes))
        t += length

    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("ffmpeg encode failed")
    with wave.open(str(tmp_audio), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.concatenate(audio).tobytes())
    subprocess.run([media.locate_ffmpeg(), "-y", "-v", "error", "-i", str(tmp_video),
                    "-i", str(tmp_audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", str(out)], check=True)
    tmp_video.unlink()
    tmp_audio.unlink()
    out.with_suffix(".json").write_text(json.dumps(dict(stage="animatic", fps=FPS,
                                                        seconds=round(t, 1), scenes=report), indent=2))
    for r in report:
        flag = "" if r["narration"] else "  (no narration)"
        print(f"{r['start']:6.1f}s  scene {r['scene']:>2}  {r['seconds']:5.1f}s  "
              f"{r['shots']} shot(s)  {r['title']}{flag}")
        for note in r["notes"]:
            print(f"          ! {note}")
    print(f"total {t:.1f}s -> {out}")


if __name__ == "__main__":
    main()
