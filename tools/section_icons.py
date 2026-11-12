#!/usr/bin/env python3
"""Section pictures for the capacity tables of the profile benders (the owner, Nov 11 2026: "the original tables of the Şahinler
and TTMC profile benders show every section as a picture — use them in the site's tables and in the brochures instead of
descriptions"; and the same night: "take the section pictures from this high-resolution Şahinler PDF, exactly as they are,
and use them for TTMC too — do not draw your own").

src/img/sections/sec-01.png … sec-20.png are the pictures of the Şahinler capacity chart (the owner's PDF, Nov 11 2026),
unchanged — turned upright (the chart pages are printed sideways) and converted from CMYK:
  sec-01 – sec-15  the separate pictures of rows 1 – 15 of the PK 30 – HPK 60 chart
  sec-16 – sec-20  rows 16 – 20 of the HPK 65 – HPK 120 chart (one picture strip, cut at the row height)
The row's text stays beside the picture for screen readers and search engines.

    icon_id(family_id, label)   -> a key of FILES, or None (not a profile bender, or not a section row)
    html(icon_id, base)         -> <img> markup ("" for None)
"""
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "src", "img", "sections")

FILES = {   # icon -> the chart row whose picture shows it
    "flat-edge": 1, "flat-flat": 2, "square-bar": 3, "round-bar": 4, "round-tube": 5, "pipe": 6, "rect-tube": 7,
    "square-tube": 8, "angle-out": 9, "angle-in": 10, "tee-out": 11, "tee-in": 12, "tee-flat": 13, "ch-out": 14,
    "ch-in": 15, "i-easy": 16, "h-easy": 17, "ch-flat": 18, "i-hard": 19, "h-hard": 20,
}

# the profile benders whose capacity tables get the pictures: Şahinler (premium line) PK / HPK, TTMC (value line) RBM / HRBM
FAMILIES = re.compile(r"^(sahinler-pk|sahinler-hpk|tt-rbm)")

RULES = [   # (pattern on the row label, icon); the first match wins
    (r"^flat bar.*(on edge|hard way)", "flat-edge"),
    (r"^flat bar.*(flat|easy way)", "flat-flat"),
    (r"^square bar", "square-bar"),
    (r"^round bar", "round-bar"),
    (r"^pipe", "pipe"),
    (r"^round tube", "round-tube"),
    (r"^rectangular tube", "rect-tube"),
    (r"^square tube", "square-tube"),
    (r"^angle.*leg out", "angle-out"),
    (r"^angle.*leg in", "angle-in"),
    (r"^(tee|t-bar).*stem out", "tee-out"),
    (r"^(tee|t-bar).*stem in", "tee-in"),
    (r"^(tee|t-bar).*flange", "tee-flat"),
    (r"^channel.*flanges out", "ch-out"),
    (r"^channel.*flanges in", "ch-in"),
    (r"^channel.*(hard way|web flat)", "ch-flat"),
    (r"^i-beam.*easy way", "i-easy"),
    (r"^i-beam.*hard way", "i-hard"),
    (r"^h-beam.*easy way", "h-easy"),
    (r"^h-beam.*hard way", "h-hard"),
]

_SIZES = {}


def icon_id(family_id, label):
    if not family_id or not FAMILIES.match(family_id) or not label:
        return None
    low = label.lower()
    for pat, ico in RULES:
        if re.search(pat, low):
            return ico
    return None


def html(icon, base="img/sections/", width=104, lazy=True):
    """the chart's picture of the section, shown `width` px wide (lazy=False for the brochures: printed at once)"""
    if icon not in FILES:
        return ""
    name = f"sec-{FILES[icon]:02d}.png"
    if name not in _SIZES:
        with Image.open(os.path.join(DIR, name)) as im:
            _SIZES[name] = im.size
    w, h = _SIZES[name]
    return f'<img class="sec-ico" src="{base}{name}" width="{width}" height="{round(width * h / w)}" alt=""{' loading="lazy" decoding="async"' if lazy else ''}>'
