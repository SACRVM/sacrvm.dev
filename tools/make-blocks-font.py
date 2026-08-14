# Builds assets/fonts/sacrvm-blocks.woff2: a four-glyph font providing the
# shade blocks U+2591/2592/2593 and the full block U+2588 for the type
# portrait on cv.html.
#
# Why hand-built: the Evil Martians release of Martian Mono does not contain
# these glyphs (checked v1.1.0: cmap has no U+2588), and Google's hosted build
# that does is served from an endpoint that refuses non-browser clients. So we
# draw them ourselves — advance 700/1000 units = 0.7em, matching Martian
# Mono's measured advance, so the blocks sit pixel-exact in the letter grid.
# Ascent 750 / descent 250 sum to exactly one em, so full blocks tile
# seamlessly across lines at line-height 1.
#
# Usage: python tools/make-blocks-font.py   (from the repo root)
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

UPM = 1000
ADV = 700           # 0.7em: Martian Mono's advance, measured in Chrome
TOP, BOT = 750, -250

def rect(pen, x0, y0, x1, y1):
    pen.moveTo((x0, y0)); pen.lineTo((x0, y1)); pen.lineTo((x1, y1)); pen.lineTo((x1, y0)); pen.closePath()

def full_block():
    pen = TTGlyphPen(None)
    rect(pen, 0, BOT, ADV, TOP)
    return pen.glyph()

def checker(cols, rows, keep):
    """Checkerboard shade: draw the cells `keep` selects; coverage = kept/total."""
    pen = TTGlyphPen(None)
    cw, ch = ADV / cols, (TOP - BOT) / rows
    for j in range(rows):
        for i in range(cols):
            if keep(i, j):
                x0, y0 = i * cw, BOT + j * ch
                rect(pen, round(x0), round(y0), round(x0 + cw), round(y0 + ch))
    return pen.glyph()

glyphs = {
    '.notdef': TTGlyphPen(None).glyph(),
    'lightshade':  checker(8, 10, lambda i, j: (i + j) % 4 == 0),   # ~25%
    'mediumshade': checker(8, 10, lambda i, j: (i + j) % 2 == 0),   # 50%
    'darkshade':   checker(8, 10, lambda i, j: (i + j) % 4 != 1),   # ~75%
    'fullblock':   full_block(),                                    # 100%
}
cmap = {0x2591: 'lightshade', 0x2592: 'mediumshade', 0x2593: 'darkshade', 0x2588: 'fullblock'}

fb = FontBuilder(UPM, isTTF=True)
fb.setupGlyphOrder(list(glyphs))
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
metrics = {name: (ADV, 0) for name in glyphs}
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=TOP, descent=BOT)
fb.setupNameTable({'familyName': 'SACRVM Blocks', 'styleName': 'Regular'})
fb.setupOS2(sTypoAscender=TOP, sTypoDescender=BOT, sTypoLineGap=0,
            usWinAscent=TOP, usWinDescent=-BOT)
fb.setupPost()
fb.font.flavor = 'woff2'
fb.save('assets/fonts/sacrvm-blocks.woff2')
print('written assets/fonts/sacrvm-blocks.woff2')
