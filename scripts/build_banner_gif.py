from math import sin, cos, pi
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "thejus_light_v2.svg"
OUT = ROOT / "thejus_light_motion.gif"

base_bytes = cairosvg.svg2png(url=str(SVG), output_width=1200, output_height=390)
base = Image.open(BytesIO(base_bytes)).convert("RGBA")
frames = []
N = 24

for i in range(N):
    t = 2 * pi * i / N
    frame = base.copy()

    glow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    # Slow, soft, organic movement inspired by modern fluid UI motion.
    cx = 1020 + 55 * sin(t) + 18 * sin(2 * t + 0.7)
    cy = 195 + 32 * cos(t * 0.9) + 10 * sin(2.1 * t)
    rx = 92 + 24 * sin(t + 0.5)
    ry = 68 + 20 * cos(t * 1.1)

    gd.ellipse((cx-rx*1.35, cy-ry*1.35, cx+rx*1.35, cy+ry*1.35), fill=(255, 75, 50, 55))
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    frame = Image.alpha_composite(frame, glow)

    blob = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    pts = []
    for j in range(64):
        a = 2 * pi * j / 64
        wobble = 1 + 0.13 * sin(3*a + t) + 0.08 * cos(5*a - 0.7*t)
        x = cx + rx * wobble * cos(a)
        y = cy + ry * (1 + 0.10*sin(4*a-t)) * sin(a)
        pts.append((x, y))
    bd.polygon(pts, fill=(255, 75, 50, 235))

    # Breathing cutout keeps the motion light rather than mechanical.
    hole_pts = []
    hrx = rx * (0.43 + 0.05 * sin(t))
    hry = ry * (0.38 + 0.05 * cos(t))
    for j in range(64):
        a = 2 * pi * j / 64
        wobble = 1 + 0.10 * sin(3*a-t)
        hole_pts.append((cx + hrx*wobble*cos(a), cy + hry*wobble*sin(a)))
    mask = Image.new("L", frame.size, 0)
    md = ImageDraw.Draw(mask)
    md.polygon(hole_pts, fill=255)
    blob.paste((244, 241, 234, 235), mask=mask)

    frame = Image.alpha_composite(frame, blob)
    frames.append(frame.convert("RGB"))

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
