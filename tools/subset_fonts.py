"""Small "core" copies of the Barlow / Barlow Condensed latin fonts (PageSpeed, Nov 13 2026).

Every page loads up to seven 22 KB woff2 files before its first paint (five are preloaded); on PageSpeed's slow-4G phone that
is about 150 KB in front of the large photo.  The site's text uses about 130 different characters of the 227 in those
files, so this keeps ASCII, the symbols the pages use (× Ø ° ± ″ – — …), the French / German accented letters and the usual
punctuation, with kerning, ligatures and tabular figures, in src/fonts/<name>-core.woff2.  The Barlow text weights keep their
TrueType hinting (17 KB, from 22 KB: body text at 13 - 17 px on Windows), the Barlow Condensed heading weights drop it (11 KB:
headings, buttons and labels at 18 px and more look the same without it).

The stylesheet lists the full latin file first and the core file after it, each with its unicode-range: a browser takes a
character from the core file when it has it, and downloads the full file only on a page that uses a character outside the
core set (the latin-ext files stay as they were).  Prints the unicode-range of the core files for src/css/site.css.

    python3 tools/subset_fonts.py
"""
import os

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "src", "fonts")
FILES = ["barlow-latin-400-normal", "barlow-latin-500-normal", "barlow-latin-600-normal", "barlow-latin-700-normal",
         "barlow-condensed-latin-500-normal", "barlow-condensed-latin-600-normal", "barlow-condensed-latin-700-normal"]

CORE = ("".join(chr(c) for c in range(0x20, 0x7F)) + " "
        + "©®°±²³µ·¹º¼½¾×÷ØøßÄÖÜäöüÀÂÇÈÉÊËÎÏÔÙÛàâçèéêëîïôùûÿ«»¡¿§¶"
        + "‐‑–—‘’‚“”„•…′″‹›€™−")


def ranges(cps):
    cps = sorted(cps)
    out, start, prev = [], cps[0], cps[0]
    for c in cps[1:] + [None]:
        if c is not None and c == prev + 1:
            prev = c
            continue
        out.append(f"U+{start:04X}" if start == prev else f"U+{start:04X}-{prev:04X}")
        if c is not None:
            start = prev = c
    return ",".join(out)


cover = None
for name in FILES:
    src = os.path.join(FONTS, name + ".woff2")
    have = set(TTFont(src).getBestCmap())
    keep = sorted(ord(c) for c in set(CORE) if ord(c) in have)
    cover = keep if cover is None else sorted(set(cover) & set(keep))
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "ccmp", "locl", "mark", "mkmk", "tnum", "pnum"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.hinting = "condensed" not in name
    font = subset.load_font(src, opts)
    s = subset.Subsetter(opts)
    s.populate(unicodes=keep)
    s.subset(font)
    out = os.path.join(FONTS, name.replace("-latin-", "-core-").replace("-normal", "") + ".woff2")
    subset.save_font(font, out, opts)
    print(f"{os.path.basename(out):38s} {os.path.getsize(src) // 1024:3d} KB -> {os.path.getsize(out) / 1024:5.1f} KB, {len(keep)} characters")
print("unicode-range:", ranges(cover))
