"""Generate the favicon set from the site's own Martian Mono subset.

Outputs (repo root):
  favicon.svg          - the S glyph as a real path, no font dependency
  favicon.ico          - 16/32/48, each size rendered natively
  apple-touch-icon.png - 180x180

Layout mirrors the old inline data-URI icon: 64-unit canvas, paper ground,
3-unit ink border inset 4 units, glyph at font-size 34 on baseline y=44.
"""

import io
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
WOFF2 = ROOT / "assets" / "fonts" / "martian-mono-latin.woff2"

PAPER = "#A1C9C8"
INK = "#121211"
GLYPH = "S"
WEIGHT = 700

# 64-unit reference layout (same numbers as the old data-URI SVG)
CANVAS = 64
BORDER_INSET = 4
BORDER_WIDTH = 3
FONT_SIZE = 34
BASELINE_Y = 44

font = TTFont(WOFF2)
if "fvar" in font:
    from fontTools.varLib.instancer import instantiateVariableFont
    instantiateVariableFont(font, {"wght": WEIGHT}, inplace=True)

# --- favicon.svg: extract the glyph outline as a path -----------------------
upem = font["head"].unitsPerEm
glyph_name = font.getBestCmap()[ord(GLYPH)]
advance = font["hmtx"][glyph_name][0]

pen = SVGPathPen(font.getGlyphSet())
font.getGlyphSet()[glyph_name].draw(pen)
path = pen.getCommands()

scale = FONT_SIZE / upem
x = (CANVAS - advance * scale) / 2
b = BORDER_INSET + BORDER_WIDTH / 2  # stroke is centered on its rect

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}">'
    f'<rect width="{CANVAS}" height="{CANVAS}" fill="{PAPER}"/>'
    f'<rect x="{b}" y="{b}" width="{CANVAS - 2 * b}" height="{CANVAS - 2 * b}"'
    f' fill="none" stroke="{INK}" stroke-width="{BORDER_WIDTH}"/>'
    f'<path transform="translate({x:.2f} {BASELINE_Y}) scale({scale:.6f} -{scale:.6f})"'
    f' fill="{INK}" d="{path}"/>'
    f"</svg>\n"
)
(ROOT / "favicon.svg").write_text(svg, encoding="utf-8")

# --- raster sizes: render each natively so 16px stays crisp -----------------
ttf_bytes = io.BytesIO()
font.flavor = None
font.save(ttf_bytes)


def render(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(img)
    o = max(1, round(size * BORDER_INSET / CANVAS))
    w = max(1, round(size * BORDER_WIDTH / CANVAS))
    d.rectangle([o, o, size - 1 - o, size - 1 - o], outline=INK, width=w)
    ttf_bytes.seek(0)
    f = ImageFont.truetype(ttf_bytes, round(size * FONT_SIZE / CANVAS))
    d.text((size / 2, size * BASELINE_Y / CANVAS), GLYPH, font=f, fill=INK, anchor="ms")
    return img


# Write the ICO container by hand: this Pillow build silently drops
# append_images frames on ICO save, and each size must be rendered natively
# (a 48->16 downscale turns the 1px border to mush). PNG frames are fine for
# every browser and for Windows 10+.
import struct

sizes = [16, 32, 48]
frames = []
for s in sizes:
    buf = io.BytesIO()
    render(s).save(buf, format="PNG")
    frames.append((s, buf.getvalue()))

ico = struct.pack("<HHH", 0, 1, len(frames))
offset = 6 + 16 * len(frames)
for s, data in frames:
    ico += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(data), offset)
    offset += len(data)
(ROOT / "favicon.ico").write_bytes(ico + b"".join(d for _, d in frames))

render(180).save(ROOT / "apple-touch-icon.png")

print("favicon.svg, favicon.ico (16/32/48), apple-touch-icon.png written")
