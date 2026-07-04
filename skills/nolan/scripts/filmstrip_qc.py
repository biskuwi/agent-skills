#!/usr/bin/env python3
"""Generate timestamped filmstrip/contact-sheet QC images for video review."""

import argparse
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def rational_to_float(value):
    if "/" in value:
        num, den = value.split("/", 1)
        return float(num) / float(den)
    return float(value)


def video_fps(path):
    value = run([
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=r_frame_rate",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ])
    return rational_to_float(value)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--interval", type=float, help="Sample every N seconds, e.g. 0.1.")
    parser.add_argument("--fps", type=float, help="Sample at this many frames per second.")
    parser.add_argument("--every-frame", action="store_true", help="Extract every source frame.")
    parser.add_argument("--frames-per-sheet", type=int, default=30)
    parser.add_argument("--cols", type=int, default=5)
    parser.add_argument("--thumb-width", type=int, default=216)
    parser.add_argument("--thumb-height", type=int, default=384)
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument("--clean", action="store_true", default=True)
    return parser.parse_args()


def choose_sample_fps(args, src_fps):
    selected = [args.interval is not None, args.fps is not None, args.every_frame]
    if sum(selected) > 1:
        raise SystemExit("Choose only one of --interval, --fps, or --every-frame.")
    if args.every_frame:
        return src_fps, False
    if args.fps is not None:
        return args.fps, True
    if args.interval is not None:
        if args.interval <= 0:
            raise SystemExit("--interval must be positive.")
        return 1.0 / args.interval, True
    return 10.0, True


def extract_frames(args, frames_dir, sample_fps, apply_fps_filter):
    vf_parts = []
    if apply_fps_filter:
        vf_parts.append(f"fps={sample_fps:.8f}")
    vf_parts.append(f"scale={args.thumb_width}:{args.thumb_height}")
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(args.video),
        "-vf",
        ",".join(vf_parts),
        "-q:v",
        "3",
        str(frames_dir / "f_%06d.jpg"),
    ]
    subprocess.check_call(cmd)


def load_font(size=18):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def make_sheets(args, frames_dir, sheets_dir, sample_fps):
    frames = sorted(frames_dir.glob("*.jpg"))
    if not frames:
        raise SystemExit("No frames were extracted.")

    rows = math.ceil(args.frames_per_sheet / args.cols)
    label_h = 30
    sheet_w = args.cols * args.thumb_width
    sheet_h = rows * (args.thumb_height + label_h)
    font = load_font()

    for sheet_index, start_index in enumerate(range(0, len(frames), args.frames_per_sheet)):
        batch = frames[start_index:start_index + args.frames_per_sheet]
        sheet = Image.new("RGB", (sheet_w, sheet_h), "black")
        draw = ImageDraw.Draw(sheet)

        for j, fp in enumerate(batch):
            frame_index = int(fp.stem.split("_")[1]) - 1
            t = frame_index / sample_fps
            x = (j % args.cols) * args.thumb_width
            y = (j // args.cols) * (args.thumb_height + label_h) + label_h
            draw.rectangle((x, y - label_h, x + args.thumb_width, y), fill="black")
            draw.text((x + 6, y - label_h + 5), f"{t:07.3f}s", fill="white", font=font)
            with Image.open(fp) as im:
                sheet.paste(im.convert("RGB"), (x, y))

        start_t = (int(batch[0].stem.split("_")[1]) - 1) / sample_fps
        end_t = (int(batch[-1].stem.split("_")[1]) - 1) / sample_fps
        out = sheets_dir / f"sheet_{sheet_index:04d}_{start_t:07.3f}-{end_t:07.3f}.jpg"
        sheet.save(out, quality=args.quality)

    print(f"frames={len(frames)}")
    print(f"sheets={len(list(sheets_dir.glob('*.jpg')))}")
    print(f"frames_dir={frames_dir}")
    print(f"sheets_dir={sheets_dir}")


def main():
    args = parse_args()
    if not args.video.exists():
        raise SystemExit(f"Video not found: {args.video}")
    if args.frames_per_sheet <= 0 or args.cols <= 0:
        raise SystemExit("--frames-per-sheet and --cols must be positive.")

    src_fps = video_fps(args.video)
    sample_fps, apply_fps_filter = choose_sample_fps(args, src_fps)
    frames_dir = args.out_dir / "frames"
    sheets_dir = args.out_dir / "sheets"

    if args.clean and args.out_dir.exists():
        shutil.rmtree(args.out_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)
    sheets_dir.mkdir(parents=True, exist_ok=True)

    extract_frames(args, frames_dir, sample_fps, apply_fps_filter)
    make_sheets(args, frames_dir, sheets_dir, sample_fps)


if __name__ == "__main__":
    main()
