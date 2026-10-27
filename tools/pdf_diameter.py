#!/usr/bin/env python3
"""The diameter sign in a finished PDF: every 'Ø' set in Barlow / Barlow Condensed / Oswald (narrow, like a slashed zero)
becomes Inter's round Ø, the rest of its line moving over by the difference in width.  For the NovoTech PDFs that were
made by editing a supplier's PDF (no HTML source to rebuild from).

    python3 tools/pdf_diameter.py <in.pdf> [<out.pdf>]        (out defaults to in, saved incrementally-free)
"""
import io
import os
import re
import sys

import fitz
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FONTS = os.path.join(ROOT, "src", "fonts")
OSWALD = "/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad/fonts/fontsource-oswald-5.3.0/package/files"
CACHE = os.path.join(ROOT, "tools", "cache", "fonts")
INTER = {300: "/usr/share/fonts/opentype/inter/Inter-Light.otf", 400: "/usr/share/fonts/opentype/inter/Inter-Regular.otf", 500: "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
         600: "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 700: "/usr/share/fonts/opentype/inter/Inter-Bold.otf"}
WEIGHTS = {"Thin": 100, "ExtraLight": 200, "Light": 300, "Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700,
           "ExtraBold": 800, "Black": 900}
_fonts = {}


def woff2_ttf(path):
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, os.path.basename(path).replace(".woff2", ".ttf"))
    if not os.path.exists(out):
        f = TTFont(path)
        f.flavor = None
        f.save(out)
    return out


def font_file(pdf_font):
    """TTF for a PDF font name like 'ABCDEF+BarlowCondensed-SemiBold' (None when not one of ours)"""
    name = re.sub(r"^[A-Z]{6}\+", "", pdf_font)
    m = re.match(r"(BarlowCondensed|Barlow|Oswald|Roboto)-(\w+)", name)
    if not m:
        return None, None
    fam, st = m.groups()
    w = WEIGHTS.get(st.replace("Italic", "") or "Regular", 400)
    if fam == "Roboto":
        p = os.path.join(ROOT, "tools", "fonts", "roboto", f"Roboto-{st}.ttf")
        return (p if os.path.exists(p) else None), w
    if fam == "Oswald":
        p = os.path.join(OSWALD, f"oswald-latin-{min(max(w, 200), 700)}-normal.woff2")
    elif fam == "BarlowCondensed":
        p = os.path.join(SRC_FONTS, f"barlow-condensed-latin-{min(max(w, 500), 700)}-normal.woff2")
    else:
        p = os.path.join(SRC_FONTS, f"barlow-latin-{min(max(w, 400), 700)}-normal.woff2")
    return (woff2_ttf(p) if os.path.exists(p) else None), w


def fobj(path):
    if path not in _fonts:
        _fonts[path] = fitz.Font(fontfile=path)
    return _fonts[path]


def cap_height(path):
    f = TTFont(path)
    return f["OS/2"].sCapHeight / f["head"].unitsPerEm


def fix_page(page):
    n = 0
    raw = page.get_text("rawdict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
    edits = []
    for b in raw["blocks"]:
        for l in b.get("lines", []):
            chars = [(c, s) for s in l["spans"] for c in s["chars"]]
            if not any(c["c"] == "Ø" for c, s in chars):
                continue
            if abs(l["dir"][1]) > 0.01:
                continue                                   # rotated lines: none so far
            k0 = next(i for i, (c, s) in enumerate(chars) if c["c"] == "Ø")
            items, shift, ok = [], 0.0, True
            for c, s in chars[k0:]:
                path, w = font_file(s["font"])
                if path is None:
                    ok = False
                    break
                o = fitz.Point(c["origin"])
                if c["c"] == "Ø":
                    ip = INTER[min(INTER, key=lambda k: abs(k - (w or 400)))]
                    size = s["size"] * cap_height(path) / cap_height(ip)
                    w_old = fobj(path).text_length("Ø", s["size"])
                    w_new = fobj(ip).text_length("Ø", size)
                    items.append((fitz.Point(o.x + shift, o.y), "Ø", ip, size, s["color"], c))
                    shift += w_new - w_old
                else:
                    items.append((fitz.Point(o.x + shift, o.y), c["c"], path, s["size"], s["color"], c))
            if ok:
                edits.append(items)
    if not edits:
        return 0
    for items in edits:
        for pos, ch, path, size, col, c in items:
            if not ch.strip():
                continue
            r = fitz.Rect(c["bbox"])
            cx, cy = (r.x0 + r.x1) / 2, c["origin"][1] - 0.32 * size
            h = max(0.25, min(r.width, size) * 0.16)
            page.add_redact_annot(fitz.Rect(cx - h, cy - h, cx + h, cy + h), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE, text=fitz.PDF_REDACT_TEXT_REMOVE)
    for items in edits:
        by = {}
        for pos, ch, path, size, col, c in items:
            if ch.strip():
                by.setdefault(col, []).append((pos, ch, path, size))
        for col, its in by.items():
            tw = fitz.TextWriter(page.rect)
            for pos, ch, path, size in its:
                tw.append(pos, ch, font=fobj(path), fontsize=size)
            tw.write_text(page, color=fitz.sRGB_to_pdf(col))
        n += sum(1 for it in items if it[1] == "Ø")
    return n


def main(src, out=None):
    doc = fitz.open(src)
    total = 0
    for page in doc:
        total += fix_page(page)
    out = out or src
    tmp = out + ".tmp.pdf"
    doc.subset_fonts()
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, out)
    print(f"{os.path.basename(src)}: {total} Ø replaced → {out} ({os.path.getsize(out) // 1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
