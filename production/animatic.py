#!/usr/bin/env python3
"""Cut an animatic: the whole story at its planned pacing, before (and while)
rendering. Minutes on a CPU; no GPU.

For every scene in story.yaml, in order, each shot shows
  * its chosen render, if the shot has `take: <seed>` and the clip exists,
  * else its keyframe still, if composed,
  * else (a scene without shots yet) a card with the scene's title and text.

Timing comes from the narration when it exists: put the ElevenLabs file for
scene N at `<channel>/audio/<story>/sceneNN.wav` (or .mp3/.m4a). The scene then
lasts the narration plus a short breath, split evenly across its shots, and the
narration is the soundtrack. Without narration: a clip keeps its own length, a
still 5 s, a card 4 s.

The report at the end is the point: which scenes need more shots than they
have (the narration outlasts the clips), and where a render is held on its last
frame.

  python production/animatic.py [--story lion_and_mouse] [--size 960x540]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import paths, post  # noqa: E402

FPS = 24
SR = 48000
BREATH = 0.6          # seconds of silence after each scene's narration
DEFAULT = dict(clip=None, still=5.0, card=4.0)


def narration(story: str, n: int) -> Path | None:
    for ext in ("wav", "mp3", "m4a"):
        p = paths.AUDIO / story / f"scene{n:02d}.{ext}"
        if p.is_file():
            return p
    return None


def read_audio(path: Path) -> np.ndarray:
    raw = subprocess.run([post._ffmpeg(), "-v", "error", "-i", str(path), "-f", "s16le",
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
    ap.add_argument("--story", default="lion_and_mouse")
    ap.add_argument("--size", default="960x540")
    args = ap.parse_args()
    size = tuple(int(v) for v in args.size.split("x"))

    story = yaml.safe_load((paths.REPO / "stories" / args.story / "story.yaml").read_text())
    work = paths.WORK / "stories" / args.story
    out = work / "animatic.mp4"
    tmp_video = out.with_name("animatic_video.mp4")
    cmd = [post._ffmpeg(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{size[0]}x{size[1]}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
           "-crf", "23", "-pix_fmt", "yuv420p", str(tmp_video)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    audio: list[np.ndarray] = []
    report, t = [], 0.0

    for n in sorted(story["scenes"]):
        scene = story["scenes"][n]
        segs = []
        for shot in scene.get("shots", []):
            if shot.get("superseded_by") or shot.get("variant_of"):
                continue
            clip = work / "shots" / f"{shot['name']}_s{shot['take']}.mp4" if shot.get("take") else None
            if clip and clip.is_file():
                segs.append(("clip", clip, shot["name"]))
            elif (work / shot["keyframe"]).is_file():
                segs.append(("still", work / shot["keyframe"], shot["name"]))
        if not segs:
            segs.append(("card", None, "no shots yet"))

        voice = narration(args.story, n)
        if voice is not None:
            wav = read_audio(voice)
            length = len(wav) / SR + BREATH
            slots = [length / len(segs)] * len(segs)
            audio.append(np.concatenate([wav, np.zeros(int(length * SR) - len(wav), np.int16)]))
        else:
            slots = []
            for kind, src, _ in segs:
                slots.append(len(post.decode(src)) / 16 if kind == "clip" else DEFAULT[kind])
            length = sum(slots)
            audio.append(np.zeros(int(length * SR), np.int16))

        notes = []
        for (kind, src, name), slot in zip(segs, slots):
            source = (f"take {src.stem.rsplit('_s', 1)[-1]}" if kind == "clip"
                      else "keyframe only" if kind == "still" else "not planned")
            label = f"{n}. {scene['title']}  |  {name}  |  {source}"
            nframes = int(round(slot * FPS))
            if kind == "clip":
                frames = post.decode(src)
                have = len(frames) / 16
                if have + 0.05 < slot:
                    notes.append(f"{name}: clip {have:.1f}s held to fill {slot:.1f}s")
                for i in range(nframes):
                    f = frames[min(int(i / FPS * 16), len(frames) - 1)]
                    img = caption(Image.fromarray(f).resize(size, Image.LANCZOS), label)
                    enc.stdin.write(np.asarray(img).tobytes())
                continue
            if kind == "still":
                img = Image.open(src).convert("RGB").resize(size, Image.LANCZOS)
            else:
                img = card(size, f"{n}. {scene['title']}", " ".join(scene.get("text", "").split()))
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
    wav = out.with_name("animatic_audio.wav")
    import wave

    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.concatenate(audio).tobytes())
    subprocess.run([post._ffmpeg(), "-y", "-v", "error", "-i", str(tmp_video), "-i", str(wav),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)], check=True)
    tmp_video.unlink(); wav.unlink()
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
