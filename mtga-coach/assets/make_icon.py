#!/usr/bin/env python3
"""Generate the app icon with no image library: raw PNG bytes into an ICO.

The mark is a fractured diamond - the left half whole, the right half split
away and displaced downward, which is the Echoverse idea in one shape and
still reads at 16 pixels.
"""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

GROUND = (0x12, 0x16, 0x1D)
LEFT = (0x4F, 0xB2, 0xBF)
ECHO = (0x8A, 0xD6, 0xE0)
SIZES = (256, 128, 64, 48, 32, 16)


def png_bytes(w: int, h: int, pixels: bytes) -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    raw = b"".join(b"\x00" + pixels[y * w * 4:(y + 1) * w * 4] for y in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def render(n: int) -> bytes:
    px = bytearray(n * n * 4)
    r_corner = 0.18 * n
    cx = cy = n / 2.0
    radius = 0.34 * n
    gap = max(1.0, 0.022 * n)          # the crack
    shift = 0.10 * n                   # how far the echo half falls
    for y in range(n):
        for x in range(n):
            fx, fy = x + 0.5, y + 0.5
            # rounded-square mask
            qx = max(abs(fx - cx) - (n / 2 - r_corner), 0)
            qy = max(abs(fy - cy) - (n / 2 - r_corner), 0)
            if (qx * qx + qy * qy) ** 0.5 > r_corner:
                continue
            col = GROUND
            right = fx > cx + gap
            left = fx < cx - gap
            sy = fy - shift if right else fy
            if (left or right) and abs(fx - cx) + abs(sy - cy) <= radius:
                col = ECHO if right else LEFT
            i = (y * n + x) * 4
            px[i:i + 4] = bytes(col) + b"\xff"
    return bytes(px)


def main() -> None:
    here = Path(__file__).resolve().parent
    images = [(s, png_bytes(s, s, render(s))) for s in SIZES]
    out = bytearray(struct.pack("<HHH", 0, 1, len(images)))
    offset = 6 + 16 * len(images)
    for size, data in images:
        dim = 0 if size >= 256 else size
        out += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
    for _, data in images:
        out += data
    (here / "mtga-coach.ico").write_bytes(bytes(out))
    (here / "mtga-coach.png").write_bytes(images[0][1])
    print(f"wrote mtga-coach.ico ({len(out)} bytes, {len(images)} sizes) and .png")


if __name__ == "__main__":
    main()
