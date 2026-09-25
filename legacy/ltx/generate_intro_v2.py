#!/usr/bin/env python3
"""Generate TheWebtoonsCorner intro V2 with LTX-Video.

The script builds two deterministic conditioning frames from the channel logo
and manga panels, asks LTX-Video to animate the transition, then adds the
reference intro's soundtrack and encodes a 1080p MOV.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


REPO_ROOT = Path(__file__).resolve().parent


def default_channel_root() -> Path:
    override = os.environ.get("THE_WEBTOONS_CORNER_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    if REPO_ROOT.parent.name == "repositories":
        return REPO_ROOT.parent.parent
    return REPO_ROOT


CHANNEL_ROOT = default_channel_root()
DEFAULT_LOGO = CHANNEL_ROOT / "img" / "watermark_big.png"
DEFAULT_AUDIO_SOURCE = CHANNEL_ROOT / "Intro" / "Intro_channel_video.mov"
DEFAULT_OUTPUT = CHANNEL_ROOT / "Intro" / "Intro_channel_video_v2.mov"
DEFAULT_PAGES_DIR = (
    CHANNEL_ROOT
    / "Mangas"
    / "Surviving_the_Game_as_a_Barbarian"
    / "chp1"
)
DEFAULT_WORK_DIR = CHANNEL_ROOT / "Intro" / "intro_v2_work"
DEFAULT_CONFIG = REPO_ROOT / "configs" / "ltxv-2b-0.9.8-distilled.yaml"

PROMPT = (
    "The shot opens on a dark ancient leather manga spellbook standing upright "
    "and perfectly centered inside the calm eye of a huge blue and violet cosmic "
    "hurricane. The camera makes one extremely slow cinematic push forward. The "
    "book remains fixed in the middle, facing the camera, with the exact luminous "
    "blue, white, and magenta TWC emblem embedded in its front cover. Dim particles "
    "and mist rotate behind it. The cover opens slightly and individual black and "
    "white manga chapter pages begin lifting out from between the covers. First two "
    "pages drift upward, then more pages emerge and move in graceful slow motion. "
    "The pages follow wide curved orbital paths around the book, gradually forming "
    "a controlled spiral that echoes the hurricane eye. Their printed comic panels "
    "remain visible and rectangular while page corners flex naturally in the wind. "
    "The central book never leaves its position and the emblem remains readable and "
    "unchanged. Blue and violet rim light illuminates the page edges. The movement "
    "becomes richer but never chaotic, ending with the book still centered and the "
    "manga pages suspended around it in an elegant circular composition. One "
    "continuous shot, premium anime fantasy channel intro, dramatic volumetric "
    "lighting, deep blacks, crisp details, restrained slow motion."
)

NEGATIVE_PROMPT = (
    "worst quality, blurry, low detail, jitter, fast motion, camera cuts, camera "
    "shake, book moving away, duplicate book, deformed book, warped logo, changed "
    "logo, misspelled text, subtitles, captions, extra letters, torn pages, melted "
    "pages, fused pages, chaotic motion, people, hands, faces, watermark"
)

LTX_LICENSE_URL = (
    "https://huggingface.co/Lightricks/LTX-Video/blob/main/"
    "LTX-Video-Open-Weights-License-0.X.txt"
)


def vortex_background(width: int, height: int, seed: int) -> Image.Image:
    """Create a dark blue-violet spiral background for conditioning."""
    yy, xx = np.mgrid[0:height, 0:width]
    cx, cy = width * 0.5, height * 0.49
    nx = (xx - cx) / (width * 0.55)
    ny = (yy - cy) / (height * 0.62)
    radius = np.sqrt(nx * nx + ny * ny)
    angle = np.arctan2(ny, nx)
    spiral = 0.5 + 0.5 * np.sin(angle * 4.0 - radius * 18.0)
    halo = np.exp(-((radius - 0.48) ** 2) / 0.075)
    core = np.exp(-(radius**2) / 0.12)
    vignette = np.clip(1.0 - radius * 0.82, 0.0, 1.0)

    rgb = np.zeros((height, width, 3), dtype=np.float32)
    rgb[..., 0] = 3 + 23 * halo * spiral + 12 * core
    rgb[..., 1] = 5 + 27 * halo * (1.0 - spiral * 0.45) + 17 * core
    rgb[..., 2] = 12 + 75 * halo + 62 * core + 22 * spiral * vignette
    rgb *= (0.27 + 0.73 * vignette)[..., None]

    rng = np.random.default_rng(seed)
    rgb += rng.normal(0, 2.0, rgb.shape)
    image = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert(
        "RGBA"
    )

    stars = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(stars)
    random_source = random.Random(seed)
    for _ in range(max(30, width * height // 12000)):
        x = random_source.randrange(width)
        y = random_source.randrange(height)
        distance = math.hypot((x - cx) / width, (y - cy) / height)
        if distance < 0.18:
            continue
        radius_px = random_source.choice((1, 1, 1, 2))
        alpha = random_source.randrange(60, 175)
        color = random_source.choice(
            ((125, 185, 255, alpha), (202, 125, 255, alpha), (255, 255, 255, alpha))
        )
        draw.ellipse(
            (x - radius_px, y - radius_px, x + radius_px, y + radius_px),
            fill=color,
        )
    return Image.alpha_composite(image, stars.filter(ImageFilter.GaussianBlur(0.35)))


def add_glow(
    canvas: Image.Image,
    center: tuple[int, int],
    size: tuple[int, int],
) -> None:
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    cx, cy = center
    w, h = size
    draw.ellipse(
        (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2),
        fill=(64, 80, 255, 150),
    )
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(w, h) // 5)))


def draw_book(canvas: Image.Image, logo_path: Path) -> None:
    """Draw a centered upright fantasy book with the exact logo on its cover."""
    width, height = canvas.size
    book_w = int(width * 0.30)
    book_h = int(height * 0.66)
    left = (width - book_w) // 2
    top = int(height * 0.18)
    right = left + book_w
    bottom = top + book_h
    bevel = max(8, width // 70)

    add_glow(canvas, (width // 2, int(height * 0.52)), (book_w * 2, book_h))
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Page block and spine give the flat conditioning art a readable 3D form.
    draw.polygon(
        [
            (left - bevel, top + bevel),
            (right - bevel, top),
            (right + bevel, bottom - bevel),
            (left, bottom + bevel),
        ],
        fill=(194, 174, 133, 255),
        outline=(239, 222, 176, 255),
        width=max(2, bevel // 3),
    )
    draw.rounded_rectangle(
        (left, top, right, bottom),
        radius=bevel,
        fill=(22, 17, 31, 255),
        outline=(88, 125, 224, 255),
        width=max(3, bevel // 2),
    )
    draw.rounded_rectangle(
        (left + bevel, top + bevel, right - bevel, bottom - bevel),
        radius=bevel,
        outline=(172, 72, 194, 210),
        width=max(2, bevel // 3),
    )
    draw.line(
        (left + bevel, top + bevel, left + bevel, bottom - bevel),
        fill=(84, 150, 255, 210),
        width=max(3, bevel // 3),
    )
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.25)))

    logo = Image.open(logo_path).convert("RGBA")
    logo_size = int(book_w * 0.77)
    logo = ImageOps.contain(logo, (logo_size, logo_size), Image.Resampling.LANCZOS)
    glow = logo.getchannel("A").filter(ImageFilter.GaussianBlur(max(5, logo_size // 18)))
    logo_glow = Image.new("RGBA", logo.size, (70, 80, 255, 0))
    logo_glow.putalpha(glow.point(lambda value: min(150, value)))
    logo_x = (width - logo.width) // 2
    logo_y = top + (book_h - logo.height) // 2
    canvas.alpha_composite(logo_glow, (logo_x, logo_y))
    canvas.alpha_composite(logo, (logo_x, logo_y))


def find_page_images(folder: Path, limit: int = 12) -> list[Path]:
    extensions = {".png", ".jpg", ".jpeg", ".webp"}
    if not folder.is_dir():
        return []
    return [
        path
        for path in sorted(folder.rglob("*"))
        if path.is_file() and path.suffix.lower() in extensions
    ][:limit]


def stylized_page(size: tuple[int, int], index: int) -> Image.Image:
    page = Image.new("RGBA", size, (230, 229, 224, 255))
    draw = ImageDraw.Draw(page)
    margin = max(3, size[0] // 18)
    draw.rectangle(
        (margin, margin, size[0] - margin, size[1] - margin),
        outline=(28, 29, 38, 255),
        width=max(1, margin // 2),
    )
    rng = random.Random(index)
    y = margin * 2
    while y < size[1] - margin * 3:
        panel_h = rng.randint(max(8, size[1] // 10), max(12, size[1] // 5))
        draw.rectangle(
            (margin * 2, y, size[0] - margin * 2, min(size[1] - margin * 2, y + panel_h)),
            outline=(45, 46, 58, 255),
            width=1,
        )
        y += panel_h + margin
    return page


def load_page(path: Path | None, size: tuple[int, int], index: int) -> Image.Image:
    if path is None:
        return stylized_page(size, index)
    try:
        panel = Image.open(path).convert("RGB")
        panel = ImageOps.grayscale(panel)
        panel = ImageEnhance.Contrast(panel).enhance(1.35)
        panel = ImageOps.fit(panel, size, method=Image.Resampling.LANCZOS)
        page = ImageOps.expand(panel, border=max(3, size[0] // 18), fill="#eee9dc")
        return page.convert("RGBA")
    except Exception:
        return stylized_page(size, index)


def add_orbiting_pages(
    canvas: Image.Image,
    page_paths: list[Path],
    seed: int,
) -> None:
    width, height = canvas.size
    rng = random.Random(seed)
    count = 10
    page_w = max(48, int(width * 0.095))
    page_h = max(66, int(height * 0.29))
    center_x, center_y = width * 0.5, height * 0.50
    radius_x, radius_y = width * 0.39, height * 0.36

    for index in range(count):
        theta = -0.35 + index * (math.tau / count)
        x = int(center_x + math.cos(theta) * radius_x)
        y = int(center_y + math.sin(theta) * radius_y)
        scale = 0.72 + 0.30 * ((math.sin(theta) + 1.0) / 2.0)
        size = (max(32, int(page_w * scale)), max(46, int(page_h * scale)))
        source = page_paths[index % len(page_paths)] if page_paths else None
        page = load_page(source, size, index)
        angle = math.degrees(theta) + 90 + rng.uniform(-14, 14)
        page = page.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

        shadow = Image.new("RGBA", page.size, (0, 0, 0, 0))
        shadow.putalpha(page.getchannel("A").filter(ImageFilter.GaussianBlur(7)))
        shadow_color = Image.new("RGBA", page.size, (17, 8, 35, 150))
        shadow_color.putalpha(shadow.getchannel("A"))
        position = (x - page.width // 2, y - page.height // 2)
        canvas.alpha_composite(shadow_color, (position[0] + 7, position[1] + 8))
        canvas.alpha_composite(page, position)


def build_keyframes(
    logo_path: Path,
    pages_dir: Path,
    work_dir: Path,
    width: int,
    height: int,
    seed: int,
) -> tuple[Path, Path]:
    work_dir.mkdir(parents=True, exist_ok=True)
    start_path = work_dir / "intro-v2-start.png"
    end_path = work_dir / "intro-v2-end.png"

    start = vortex_background(width, height, seed)
    draw_book(start, logo_path)
    start.convert("RGB").save(start_path, quality=95)

    end = vortex_background(width, height, seed + 1)
    page_paths = find_page_images(pages_dir)
    add_orbiting_pages(end, page_paths, seed)
    draw_book(end, logo_path)
    end.convert("RGB").save(end_path, quality=95)
    return start_path, end_path


def locate_ffmpeg() -> str:
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError(
            "FFmpeg is unavailable. Install inference extras with: "
            "python -m pip install -e '.[inference]'"
        ) from error


def add_reference_audio(
    raw_video: Path,
    audio_source: Path,
    output: Path,
    duration: float,
    final_width: int,
    final_height: int,
) -> None:
    ffmpeg = locate_ffmpeg()
    fade_out_start = max(0.0, duration - 0.65)
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(raw_video),
        "-stream_loop",
        "-1",
        "-i",
        str(audio_source),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-vf",
        f"scale={final_width}:{final_height}:flags=lanczos,format=yuv420p",
        "-af",
        f"afade=t=in:st=0:d=0.12,afade=t=out:st={fade_out_start:.3f}:d=0.65",
        "-t",
        f"{duration:.6f}",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "17",
        "-c:a",
        "aac",
        "-b:a",
        "256k",
        "-ar",
        "48000",
        "-movflags",
        "+faststart",
        str(output),
    ]
    subprocess.run(command, check=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logo", type=Path, default=DEFAULT_LOGO)
    parser.add_argument("--pages-dir", type=Path, default=DEFAULT_PAGES_DIR)
    parser.add_argument("--audio-source", type=Path, default=DEFAULT_AUDIO_SOURCE)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK_DIR)
    parser.add_argument("--pipeline-config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--width", type=int, default=768)
    parser.add_argument("--height", type=int, default=432)
    parser.add_argument("--num-frames", type=int, default=121)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--final-width", type=int, default=1920)
    parser.add_argument("--final-height", type=int, default=1080)
    parser.add_argument(
        "--preview",
        action="store_true",
        help="use 512x288 and 65 frames for a quicker low-memory test",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="build conditioning frames and print settings without loading LTX",
    )
    parser.add_argument(
        "--accept-ltx-license",
        action="store_true",
        help=(
            "confirm that you reviewed and accept the LTXV Open Weights "
            "License 0.X before model weights are downloaded or loaded"
        ),
    )
    parser.add_argument("--force", action="store_true", help="replace final output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    logo = args.logo.expanduser().resolve()
    pages_dir = args.pages_dir.expanduser().resolve()
    audio_source = args.audio_source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    work_root = args.work_dir.expanduser().resolve()
    pipeline_config = args.pipeline_config.expanduser().resolve()

    if args.preview:
        width, height, num_frames = 512, 288, 65
    else:
        width, height, num_frames = args.width, args.height, args.num_frames

    if width < 256 or height < 256:
        raise ValueError("LTX conditioning dimensions must be at least 256 pixels")
    if num_frames < 9:
        raise ValueError("--num-frames must be at least 9")
    if not logo.is_file():
        raise FileNotFoundError(f"Logo not found: {logo}")
    if not audio_source.is_file():
        raise FileNotFoundError(f"Reference video/audio not found: {audio_source}")
    if not pipeline_config.is_file():
        raise FileNotFoundError(f"Pipeline config not found: {pipeline_config}")
    if output.exists() and not args.force and not args.dry_run:
        raise FileExistsError(f"Output exists: {output}\nUse --force to replace it.")

    run_name = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = work_root / run_name
    keyframe_dir = run_dir / "keyframes"
    raw_dir = run_dir / "raw"
    start_frame, end_frame = build_keyframes(
        logo_path=logo,
        pages_dir=pages_dir,
        work_dir=keyframe_dir,
        width=width,
        height=height,
        seed=args.seed,
    )

    duration = (num_frames - 1) / args.fps
    print(f"Device: MPS if available, otherwise CUDA/CPU")
    print(f"Pipeline: {pipeline_config}")
    print(f"Resolution: {width}x{height}, {num_frames} frames at {args.fps} fps")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Start keyframe: {start_frame}")
    print(f"End keyframe: {end_frame}")
    print(f"Manga page source: {pages_dir}")
    print(f"Reference soundtrack: {audio_source}")
    print(f"Final output: {output}")

    if args.dry_run:
        print("Dry run complete: keyframes created; LTX model was not loaded.")
        return

    if not args.accept_ltx_license:
        raise SystemExit(
            "Model generation was not started. Review the checkpoint license at:\n"
            f"  {LTX_LICENSE_URL}\n"
            "Then rerun with --accept-ltx-license if you accept its terms."
        )

    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    from ltx_video.inference import InferenceConfig, infer

    raw_dir.mkdir(parents=True, exist_ok=True)
    config = InferenceConfig(
        prompt=PROMPT,
        output_path=str(raw_dir),
        pipeline_config=str(pipeline_config),
        seed=args.seed,
        height=height,
        width=width,
        num_frames=num_frames,
        frame_rate=args.fps,
        negative_prompt=NEGATIVE_PROMPT,
        conditioning_media_paths=[str(start_frame), str(end_frame)],
        conditioning_strengths=[1.0, 0.90],
        conditioning_start_frames=[0, num_frames - 1],
        image_cond_noise_scale=0.08,
        offload_to_cpu=False,
    )
    print("Loading LTX-Video and generating the raw animation...")
    print("License acknowledged: LTXV Open Weights License 0.X")
    print("The first run downloads the 2B checkpoint, upscaler, and text encoder.")
    infer(config=config)

    candidates = sorted(raw_dir.glob("*.mp4"), key=lambda path: path.stat().st_mtime)
    if not candidates:
        raise RuntimeError(f"LTX-Video produced no MP4 in {raw_dir}")
    raw_video = candidates[-1]
    print(f"Raw LTX video: {raw_video}")
    print("Adding the reference soundtrack and encoding the 1080p MOV...")
    add_reference_audio(
        raw_video=raw_video,
        audio_source=audio_source,
        output=output,
        duration=duration,
        final_width=args.final_width,
        final_height=args.final_height,
    )
    print(f"Saved final intro V2: {output}")


if __name__ == "__main__":
    main()
