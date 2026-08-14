# The type portrait on cv.html: a photo redrawn from the letters S A C R V M
# plus the shade blocks (U+2592/2593/2588) for the dark mass, dissolving to
# the right into wind-blown letters.
#
# Usage: python ascii-portrait.py <portrait.jpg> [> portrait.txt]
#   Source should be a high-contrast B/W portrait on a clean white background
#   (the shipped one was made from the profile photo with Grok Imagine).
#
# Cell aspect 0.7 is measured, not guessed: Martian Mono advances 0.7em per
# character at line-height 1 (measured in Chrome via getBoundingClientRect,
# 2026-08-14). The block glyphs live in assets/fonts/martian-mono-blocks.woff2,
# a Google Fonts text= subset (unicode-range U+2588, U+2591-2593).
import sys, random, math
from PIL import Image, ImageOps, ImageFilter

COLS = 120
PAD = 20                    # room for glyphs drifting off to the right
CELL_ASPECT = 0.7
RAMP = " VCSARM▒▓█"   # bright -> dark; letters carry the face
GAMMA = 0.9
PAPER = 210                 # everything brighter than this is bare paper
DISSOLVE_AT = 0.60          # of COLS, jittered per row
DISSOLVE_LEN = 0.42         # of COLS until fully gone
rnd = random.Random(1976)   # seeded: the artwork is reproducible

img = Image.open(sys.argv[1]).convert('L')
img = ImageOps.autocontrast(img, cutoff=1)
img = img.filter(ImageFilter.UnsharpMask(radius=6, percent=160, threshold=2))
img = img.point(lambda v: int(255 * (v / 255) ** GAMMA))
img = img.filter(ImageFilter.GaussianBlur(0.4))
w, h = img.size
rows = round(COLS * (h / w) * CELL_ASPECT)
img = img.resize((COLS, rows), Image.LANCZOS)

def level(v):
    if v >= PAPER: return 0
    return min(1 + int((PAPER - 1 - v) / PAPER * (len(RAMP) - 1)), len(RAMP) - 1)

px = img.load()
out = []
for y in range(rows):
    row = [' '] * (COLS + PAD)
    xs = COLS * DISSOLVE_AT + 6 * math.sin(y * 0.55) + rnd.uniform(-4, 4)
    for x in range(COLS):
        lv = level(px[x, y])
        if lv == 0: continue
        p = max(0.0, min(1.0, (x - xs) / (COLS * DISSOLVE_LEN))) ** 1.1
        if rnd.random() < p:
            # let go: most cells empty, some drift off as light letters
            if rnd.random() < 0.35:
                dx = x + rnd.randint(4, PAD - 2)
                if dx < COLS + PAD and row[dx] == ' ':
                    row[dx] = rnd.choice('VCS')
            continue
        if p > 0 and rnd.random() < p * 0.8:
            lv = max(1, lv - rnd.randint(2, 4))   # crumble before vanishing
        row[x] = RAMP[lv]
    out.append(''.join(row).rstrip())

while out and out[0].strip() == '': out.pop(0)
while out and out[-1].strip() == '': out.pop()
sys.stdout.reconfigure(encoding='utf-8')
print('\n'.join(out))
