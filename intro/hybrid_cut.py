#!/usr/bin/env python3
"""Hybrid TWC intro: Wan's generated journey, then the procedural logo reveal.

Diffusion is good at the organic part (the book, the page hurricane, the dive)
and poor at the part that must be exact (emblem and wordmark). The procedural
renderer is the reverse. The cut sits on the flash at 7.10 s, where the Wan
render peaks at near-white and the procedural flash starts at full white, so
the join is invisible.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from twc import media, paths  # noqa: E402



def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wan", type=Path,
                    default=paths.OUTPUT / "Intro_channel_video_wan_story_final.mov")
    ap.add_argument("--procedural", type=Path,
                    default=paths.OUTPUT / "Intro_channel_video_procedural_silent.mp4")
    ap.add_argument("--audio", type=Path, default=paths.AUDIO / "twc_intro_score.wav")
    ap.add_argument("--fps", type=int, default=30, help="the Wan cut's rate")
    ap.add_argument("--cut", type=float, default=7.10,
                    help="seconds: where the Wan part whites out and the reveal takes over")
    ap.add_argument("--duration", type=float, default=10.0)
    ap.add_argument("-o", "--output", type=Path,
                    default=paths.OUTPUT / "Intro_channel_video_hybrid.mov")
    args = ap.parse_args()

    CUT = args.cut
    silent = args.output.with_name(args.output.stem + "_silent.mp4")
    cut_frame = int(round(CUT * args.fps))
    # The Wan flash peaks at 7.10 s but never reaches full white (mean luma
    # ~182/255: the book and vortex still show at the edges), so a straight cut
    # jumps. Ramp the Wan side to pure white over the last few frames; the
    # procedural side starts at full white, so the join then happens inside white.
    white_from = CUT - 0.17
    graph = (
        f"[0:v]trim=end_frame={cut_frame},setpts=PTS-STARTPTS,fps={args.fps},"
        f"fade=t=out:st={white_from:.3f}:d=0.17:color=white[a];"
        f"[1:v]fps={args.fps},trim=start={CUT},setpts=PTS-STARTPTS[b];"
        f"[a][b]concat=n=2:v=1:a=0,format=yuv420p[v]"
    )
    subprocess.run(
        [media.locate_ffmpeg(), "-y", "-v", "error", "-i", str(args.wan), "-i", str(args.procedural),
         "-filter_complex", graph, "-map", "[v]", "-c:v", "libx264", "-preset", "slow",
         "-crf", "12", str(silent)],
        check=True)
    media.finish(concat_video=silent, audio_source=args.audio, output=args.output,
              target_duration=args.duration, source_duration=args.duration, final_width=1920,
              final_height=1080, final_fps=args.fps, hold_end=0.0, audio_restart_at=None)
    print(f"Saved hybrid: {args.output}  (cut at {CUT:.2f} s = frame {cut_frame})")


if __name__ == "__main__":
    main()
