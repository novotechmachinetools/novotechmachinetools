#!/usr/bin/env python3
"""Parse the specification tables of the NovoTech Şahinler catalogue (imperial) into /home/claude/sahinler/tables.json.

    python3 tools/sahinler_tables.py            # all pages
    python3 tools/sahinler_tables.py 6 7        # print the tables of those pages (1-based)

Every table starts with a "Model" row; the rows that follow (label · unit · one cell per model) belong to it until the
next "Model" row or the end of the page.  Fractions are typeset as superscript / subscript digits around "⁄", so the
cells are rebuilt from the characters sorted by x inside each model column.
Output: {page: [{"title", "models": [...], "rows": [{"label", "unit", "cells": [...]}]}]}
"""
import json
import re
import sys

import pdfplumber

PDF = "/home/claude/sahinler/catalogue/sahinler-2027.pdf"
OUT = "/home/claude/sahinler/tables.json"
UNITS = {"FT", "in", "HP", "ft/min", "lb", "mm", "kW", "L", "psi", "US", "t", "rpm", "ga", "deg", "°", "in/min", "lb/ft", "gal", "kg", "mm/min", "m/min", "ton", "tons", "V", "A", "Hz", "ft", "ft²", "in²", "pcs", "s", "sec", "min", "dB", "bar", "N", "kN", "mm²", "inch", "lbs", "pc", "°F", "kg/cm²"}
FRACTION = re.compile(r"(\d+)-?(\d{1,2})⁄(\d{1,2})″")


def fix_frac(s):
    """'1316⁄″' style leftovers never occur after char sorting; here we only tidy spacing."""
    s = s.replace(" ⁄ ", "⁄").replace("⁄ ", "⁄").replace(" ⁄", "⁄")
    s = re.sub(r"(\d)\s+⁄", r"\1⁄", s)
    s = re.sub(r"⁄\s+(\d)", r"⁄\1", s)
    s = re.sub(r"(\d)\s+″", r"\1″", s)
    s = re.sub(r"^(\d+)-?\s+(\d+⁄\d+″)$", r"\1-\2", s)   # "1 1⁄8″" -> "1-1⁄8″"
    s = re.sub(r"^(\d+)-\s+(\d+⁄\d+″)$", r"\1-\2", s)
    return s.strip()


def tokens(chars, gap=2.0):
    """Characters sorted by x → [(x0, x1, text)], split where the PDF positioned a new cell (no space char, gap > 2 pt)."""
    chars = sorted(chars, key=lambda c: (c["x0"], c["top"]))
    out = []
    for c in chars:
        if out and c["x0"] - out[-1][1] <= gap:
            out[-1][1] = max(out[-1][1], c["x1"]); out[-1][2] += c["text"]
        else:
            out.append([c["x0"], c["x1"], c["text"]])
    res = []
    for x0, x1, t in out:
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            res.append((x0, x1, fix_frac(t)))
    return res


def text_of(chars):
    return " ".join(t for _, _, t in tokens(chars))


def page_tables(page):
    chars = page.chars
    # label rows: a character run starting at x ≈ 42 in the table body
    starts = sorted({round(c["top"]) for c in chars if 39 <= c["x0"] <= 46 and 95 < c["top"] < 740 and c["text"].strip()})
    rows = []
    for t in starts:
        if rows and t - rows[-1] < 6:
            continue
        rows.append(t)
    raw = []
    for t in rows:
        band = [c for c in chars if abs(c["top"] - t) <= 7.5]
        label = text_of([c for c in band if c["x0"] < 178])
        unit = text_of([c for c in band if 178 <= c["x0"] < 203])
        if unit and unit not in UNITS:          # a long label running past x=178, or no unit column on this table
            label = text_of([c for c in band if c["x0"] < 203])
            unit = ""
            cells = tokens([c for c in band if c["x0"] >= 203])
        else:
            cells = tokens([c for c in band if c["x0"] >= 203])
        raw.append((label, unit, cells, t))
    tables, cur = [], None
    for label, unit, cells, t in raw:
        if label == "Model":
            cur = {"title": "", "models": [x for _, _, x in cells], "centers": [((a + b) / 2) for a, b, _ in cells], "rows": [], "top": t}
            tables.append(cur)
            continue
        if cur is None or len(label) < 2 or label.startswith("Capacities") or label.startswith("N/mm") or label.startswith("*"):
            continue
        n = len(cur["models"])
        out = [""] * n
        for a, b, x in cells:
            xc = (a + b) / 2
            i = min(range(n), key=lambda k: abs(cur["centers"][k] - xc))
            out[i] = (out[i] + " " + x).strip() if out[i] else x
        cur["rows"].append({"label": label, "unit": unit, "cells": out})
    words = page.extract_words(x_tolerance=1.5, y_tolerance=2)
    for tb in tables:
        above = [w for w in words if tb["top"] - 40 < w["top"] < tb["top"] - 8 and w["x0"] > 90]
        line_tops = sorted({round(w["top"]) for w in above})
        if line_tops:
            lt = line_tops[0]
            tb["title"] = " ".join(w["text"] for w in sorted([w for w in above if abs(w["top"] - lt) < 3], key=lambda w: w["x0"]))
        del tb["centers"], tb["top"]
    return tables


def cell_lines(chars):
    """Split a cell's characters into text lines: full-size characters start lines, the small fraction digits attach
    to the nearest line.  Returns [(text, min_dia)]."""
    main = sorted([c for c in chars if c["size"] >= 6 and c["text"].strip()], key=lambda c: c["top"])
    lines = []
    for c in main:
        if lines and c["top"] - lines[-1][0] < 4.5:
            lines[-1][1].append(c)
        else:
            lines.append([c["top"], [c]])
    for c in chars:
        if c["size"] < 6 or not c["text"].strip():
            if not lines:
                continue
            ln = min(lines, key=lambda L: abs(L[0] - c["top"]))
            if abs(ln[0] - c["top"]) < 7:
                ln[1].append(c)
    out = []
    for _, cs in lines:
        tk = tokens(cs)
        if not tk:
            continue
        dia = ""
        if re.fullmatch(r"\d+″|[\d.]+ ?FT", tk[-1][2]):
            dia = tk[-1][2].replace("FT", "ft"); tk = tk[:-1]
        out.append((" ".join(x for _, _, x in tk), dia))
    return out


def page_chart(page):
    """Section-bending capacity chart (pages 32–34): profile rows × machine columns, each cell 1–3 lines of
    'max section → min rolling Ø'.  Rows are located by the profile icons.  None when the page has no chart."""
    words = page.extract_words(x_tolerance=1.5, y_tolerance=2)
    maxw = [w for w in words if w["text"] == "Max." and 100 < w["top"] < 200]
    if not maxw:
        return None
    T = maxw[0]["top"]
    dias = [w for w in words if w["text"] == "Dia." and abs(w["top"] - T) < 3]
    spans = [(m["x0"] - 1, d["x1"] + 1) for m, d in zip(sorted(maxw, key=lambda w: w["x0"]), sorted(dias, key=lambda w: w["x0"]))]
    pw = [w["x0"] for w in words if w["text"] == "Profile"]
    if not pw:
        return None
    prof_x0 = min(pw) - 4
    names = []
    for a, b in spans:
        ws = sorted([w for w in words if T - 20 < w["top"] < T - 6 and a <= (w["x0"] + w["x1"]) / 2 <= b], key=lambda w: w["x0"])
        names.append(" ".join(w["text"] for w in ws))
    foot = min([w["top"] for w in words if w["text"] in ("STD", "OPT") and w["x0"] < 60 and w["top"] > T] + [760])
    icons = sorted([im for im in page.images if im["x0"] < 60 and T + 5 < im["top"] < foot and im["width"] < 80], key=lambda im: im["top"])
    centers = [im["top"] + im["height"] / 2 for im in icons]
    DIES = ("STD", "OPT", "OPT*", "STD*", "OPT**", "STD**")
    rows = []
    for i, cy in enumerate(centers):
        lo = (centers[i - 1] + cy) / 2 if i else T + 8
        hi = (cy + centers[i + 1]) / 2 if i + 1 < len(centers) else foot - 2
        band = [c for c in page.chars if lo <= c["top"] < hi]
        pl = cell_lines([c for c in band if prof_x0 <= c["x0"] < spans[0][0] - 2])
        dies = [t for t, _ in pl if t in DIES]
        name = " ".join(t for t, _ in pl if t not in DIES)
        cells = [cell_lines([c for c in band if a <= (c["x0"] + c["x1"]) / 2 <= b]) for a, b in spans]
        rows.append({"profile": name, "dies": dies[0] if dies else "", "cells": cells})
    return {"machines": names, "rows": rows}


def main():
    pdf = pdfplumber.open(PDF)
    want = [int(a) for a in sys.argv[1:]]
    out = {}
    for i, page in enumerate(pdf.pages, 1):
        if want and i not in want:
            continue
        tb = page_tables(page)
        ch = page_chart(page)
        if ch:
            out.setdefault("charts", {})[str(i)] = ch
            if want:
                print(f"--- chart page {i}: {ch['machines']}")
                for r in ch["rows"]:
                    print(f"  {r['profile'][:28]:28s} {r['dies']:4s} {r['cells']}")
        if tb:
            out[str(i)] = tb
            if want:
                for t in tb:
                    print(f"--- page {i}: {t['title']}  models={t['models']}")
                    for r in t["rows"]:
                        print(f"  {r['label'][:46]:46s} {r['unit']:7s} {r['cells']}")
    if not want:
        json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("pages with tables:", len(out), "tables:", sum(len(v) for v in out.values()), "->", OUT)


if __name__ == "__main__":
    main()
