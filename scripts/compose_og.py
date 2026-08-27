#!/usr/bin/env python3
"""Crop a generated illustration to 1200x630 and overlay 認知の足場 titles."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 630
SITE_NAME = "認知の足場"
FONT_REGULAR = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
FONT_BOLD = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
FONT_INDEX = 0


def crop_to_og(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    target_ratio = WIDTH / HEIGHT
    crop_h = int(w / target_ratio)
    if crop_h > h:
        im = im.crop((0, 0, int(h * target_ratio), h))
    else:
        top = max(0, int((h - crop_h) * 0.18))
        im = im.crop((0, top, w, min(h, top + crop_h)))
    return im.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def darken_left(im: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    fade_until = 740
    for x in range(fade_until):
        t = 1 - (x / fade_until)
        ov.line([(x, 0), (x, HEIGHT)], fill=(22, 21, 19, int(210 * (t ** 1.12))))
    return Image.alpha_composite(im.convert("RGBA"), overlay)


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.is_file():
        raise FileNotFoundError(f"font not found: {path}")
    return ImageFont.truetype(str(path), size, index=FONT_INDEX)


def draw_titles(
    im: Image.Image,
    title_lines: list[str],
    subtitle: str | None,
    title_size: int,
) -> Image.Image:
    d = ImageDraw.Draw(im)
    site = load_font(FONT_REGULAR, 28)
    title = load_font(FONT_BOLD, title_size)
    sub = load_font(FONT_REGULAR, 26)
    x, y = 56, 88
    d.text((x, y), SITE_NAME, font=site, fill=(142, 196, 224, 255))
    y += 50
    d.line([(x, y), (x + 84, y)], fill=(142, 196, 224, 200), width=2)
    y += 26
    for line in title_lines:
        d.text((x, y), line, font=title, fill=(243, 239, 230, 255))
        y += title_size + 16
    if subtitle:
        y += 8
        d.text((x, y), subtitle, font=sub, fill=(221, 216, 207, 255))
    return im


def compose(
    src: Path,
    out: Path,
    title_lines: list[str],
    subtitle: str | None = None,
    title_size: int = 40,
) -> Path:
    im = Image.open(src)
    im = crop_to_og(im)
    im = darken_left(im)
    im = draw_titles(im, title_lines, subtitle, title_size)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(out, "PNG", optimize=True)
    return out


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose a 1200x630 OGP PNG with 認知の足場 titles."
    )
    parser.add_argument("src", type=Path, help="source illustration")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output PNG (default: assets/images/alts/<src-stem>.png)",
    )
    parser.add_argument(
        "--title",
        action="append",
        dest="title_lines",
        required=True,
        help="title line; pass multiple times to wrap",
    )
    parser.add_argument("--subtitle", default=None)
    parser.add_argument("--title-size", type=int, default=40)
    return parser.parse_args(argv)


def default_output(src: Path) -> Path:
    repo = Path(__file__).resolve().parents[1]
    return repo / "assets" / "images" / "alts" / f"{src.stem}.png"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    src = args.src.expanduser().resolve()
    if not src.is_file():
        print(f"source not found: {src}", file=sys.stderr)
        return 1
    out = (args.output or default_output(src)).expanduser()
    if not out.is_absolute():
        out = Path.cwd() / out
    compose(src, out, args.title_lines, args.subtitle, args.title_size)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
