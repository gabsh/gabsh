"""Prepare profile.jpg for ASCII conversion: square crop, resize, boost contrast.

Writes data/photo_prepped.png (COLS x ROWS*2 pixels; a terminal cell is ~2x taller than wide).
"""
import io
import os
import sys
import urllib.request

from PIL import Image, ImageEnhance, ImageOps

COLS, ROWS = 58, 29


USER = os.environ.get("GH_USER", "gabsh")


def load(local="profile.jpg"):
    """GitHub avatar first; fall back to a local profile.jpg if the download fails."""
    try:
        req = urllib.request.Request(f"https://github.com/{USER}.png?size=460", headers={"User-Agent": "profile-art"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    except Exception as e:  # noqa: BLE001
        print(f"avatar download failed ({e}), using {local}")
        return Image.open(local).convert("RGB")


def prep(dst="data/photo_prepped.png"):
    im = load()
    s = min(im.size)
    left, top = (im.width - s) // 2, (im.height - s) // 2
    im = im.crop((left, top, left + s, top + s))
    im = im.resize((COLS, ROWS * 2), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=2)
    im = ImageEnhance.Color(im).enhance(1.3)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst)
    return dst


if __name__ == "__main__":
    print(prep(*sys.argv[1:2]))
