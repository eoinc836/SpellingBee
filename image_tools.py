#!/usr/bin/env python3
"""
Image helpers for the GC9A01 round display.

Two ways to get an image on screen:

  1. Convert at runtime (flexible, ~5 ms with numpy):
         tft.blit(to_rgb565(prepare(Image.open("bee.png"))))

  2. Pre-convert once, blit the blob later (~0 ms, best for fixed assets):
         $ python image_tools.py bee.png bee.raw
         tft.blit(load_raw("bee.raw"))

Deps:  pip install pillow numpy
"""

import sys

import numpy as np
from PIL import Image, ImageDraw

SIZE = 240


def prepare(img, size=SIZE, fit="cover", background="black", mask=True):
    """Square up an image to the panel and mask off the corners.

    fit="cover"   fills the circle, cropping overflow  (photos)
    fit="contain" fits the whole image, letterboxing   (logos, icons)
    """
    img = img.convert("RGB")
    w, h = img.size

    if fit == "cover":
        scale = max(size / w, size / h)
    else:
        scale = min(size / w, size / h)

    img = img.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                     Image.LANCZOS)

    canvas = Image.new("RGB", (size, size), background)
    canvas.paste(img, ((size - img.width) // 2, (size - img.height) // 2))

    if mask:
        # The panel is round — anything outside the circle is invisible
        # anyway, so blank it rather than letting it bleed at the edge.
        circle = Image.new("L", (size, size), 0)
        ImageDraw.Draw(circle).ellipse((0, 0, size - 1, size - 1), fill=255)
        canvas = Image.composite(canvas, Image.new("RGB", (size, size),
                                                   background), circle)
    return canvas


def to_rgb565(img):
    """PIL RGB image -> big-endian RGB565 bytes, vectorised."""
    a = np.asarray(img.convert("RGB"), dtype=np.uint16)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    v = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    # GC9A01 wants high byte first; numpy is little-endian natively.
    return v.astype(">u2").tobytes()


def load_raw(path, size=SIZE):
    data = open(path, "rb").read()
    expected = size * size * 2
    if len(data) != expected:
        raise ValueError(f"{path}: expected {expected} bytes, got {len(data)}")
    return data


def convert(src, dst, fit="cover"):
    img = prepare(Image.open(src), fit=fit)
    with open(dst, "wb") as f:
        f.write(to_rgb565(img))
    print(f"{src} -> {dst}  ({SIZE}x{SIZE}, {SIZE * SIZE * 2} bytes)")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit("usage: image_tools.py <in.png> <out.raw> [cover|contain]")
    convert(sys.argv[1], sys.argv[2],
            fit=sys.argv[3] if len(sys.argv) == 4 else "cover")
