"""Turn data/photo_prepped.png into colored ASCII <text> elements (SVG fragment)."""
from xml.sax.saxutils import escape

from PIL import Image

RAMP = " .'`^:;-~+=*#%@"
CHAR_W, LINE_H, FONT = 5.4, 10, 9


def _lum(p):
    return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255


def _q(v):
    return min(255, int(round(v / 24)) * 24)


def ascii_group(src="data/photo_prepped.png", x0=0, y0=0, delay=0.2):
    """Return (svg_fragment, width, height). Each row fades in for a scan-in effect."""
    im = Image.open(src).convert("RGB")
    cols, rows = im.width, im.height // 2
    out = []
    for r in range(rows):
        runs, cur = [], None
        for c in range(cols):
            a, b = im.getpixel((c, r * 2)), im.getpixel((c, r * 2 + 1))
            px = tuple((a[i] + b[i]) // 2 for i in range(3))
            lum = _lum(px)
            ch = RAMP[min(len(RAMP) - 1, int(lum ** 0.9 * len(RAMP)))]
            if ch == " ":
                cur = None
                continue
            # lift colors so dim pixels stay readable on the dark card
            col = "#%02x%02x%02x" % tuple(_q(min(255, v * 1.15 + 30)) for v in px)
            if cur and cur["col"] == col and cur["end"] == c:
                cur["s"] += ch
                cur["end"] += 1
            else:
                cur = {"col": col, "s": ch, "start": c, "end": c + 1}
                runs.append(cur)
        if runs:
            y = y0 + r * LINE_H + FONT
            body = "".join(
                f'<text x="{x0 + u["start"] * CHAR_W:.1f}" y="{y}" fill="{u["col"]}" textLength="{len(u["s"]) * CHAR_W:.1f}" lengthAdjust="spacing">{escape(u["s"])}</text>'
                for u in runs
            )
            out.append(f'<g class="row" style="animation-delay:{delay + r * 0.04:.2f}s">{body}</g>')
    return "".join(out), cols * CHAR_W, rows * LINE_H
