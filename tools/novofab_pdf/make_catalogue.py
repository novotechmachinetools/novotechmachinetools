#!/usr/bin/env python3
"""Build the NovoFab Machinery band saw catalogue PDF (imperial units, Letter size).

    python3 tools/novofab_pdf/make_catalogue.py [--work DIR] [--out FILE] [--keep-html]

Data: content/families/bandsaw.json (brand == "novofab", in data["order"]). Spec tables come
from build.build_bandsaw_table (the site's own imperial converter). Photos are the PNGs in
tools/src-images/novofab/, resized to max 1400 px and embedded as JPEG (q85).

The page is written as HTML + CSS (catalogue.html.j2 / catalogue.css next to this script) and
rendered with Playwright Chromium (page.pdf, Letter, zero margins). After layout, every page is
measured in the browser: a page whose content spills past the sheet gets a "fit-N" class that
tightens type and photo sizes, and the check is repeated. Finally pikepdf sets the metadata.
"""
import argparse
import json
import os
import re
import sys
import tempfile

from jinja2 import Environment, FileSystemLoader, select_autoescape
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # repo root
sys.path.insert(0, ROOT)
from build import build_bandsaw_table, inch_frac, hp_range, manifest  # noqa: E402  (site converter)

DATA = os.path.join(ROOT, "content", "families", "bandsaw.json")
PHOTOS = os.path.join(ROOT, "tools", "src-images", "novofab")
FONTS = os.path.join(ROOT, "tools", "fonts")
NOVOFAB_LOGO = os.path.join(ROOT, "tools", "novofab", "novofab-logo-1420.png")
NOVOTECH_LOGO = "/home/claude/novotech-src/gms2026/cutouts/p01-000-cut.png"
DEFAULT_OUT = os.path.join(ROOT, "src", "files", "NovoFab-Band-Saws-Catalogue-2026.pdf")

MAX_W = 1400          # px, photos
JPEG_Q = 85

GROUPS = [
    ("manual", "Manual band saws"),
    ("semi-automatic", "Semi-automatic band saws"),
    ("automatic", "Automatic band saws"),
    ("double-column", "Double column band saws"),
]
GROUP_TYPE = {"manual": "Manual", "semi-automatic": "Semi-automatic", "automatic": "Automatic", "double-column": "Double column"}

COMPANY_LINE = ("NovoTech Machine Tools Inc. · 1365 Mid-Way Blvd, Unit 26, Mississauga, ON L5T 2J5, Canada · "
                "NovoTechMachineTools.com · info@NovoTechMachineTools.com · +1 647 526 5510")
INCLUDED_LABEL = "Included with every NovoTech machine"
INCLUDED_ITEMS = [
    "CSA-approved electrical panel",
    "1-year warranty",
    "7-day money-back guarantee (in-stock machines only)",
    "Spare parts & technical support readily available from Mississauga, Ontario",
    "Order today with just 10% down — 0% down financing available",
    "Installation and training available",
]
VOLTAGE_LINE = "Custom voltage available: 208 V, 240 V, 480 V or 600 V 3-phase."
COVER_PHOTOS = ["nf-a13-1", "nf-h13-1", "nf-m10t-1", "nf-dc24-1"]   # wide, tall, square-ish, wide

PDF_TITLE = "NovoFab Machinery band saws — Catalogue 2026"
PDF_AUTHOR = "NovoTech Machine Tools Inc."


# ---------------------------------------------------------------- images
def prepare_photo(key, out_dir):
    """PNG (RGB, white background) -> JPEG, max 1400 px wide. Returns the relative file name."""
    src = os.path.join(PHOTOS, key + ".png")
    if not os.path.exists(src):
        raise SystemExit(f"photo missing: {src}")
    dst = os.path.join(out_dir, key + ".jpg")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        im = Image.open(src)
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
            bg.alpha_composite(im.convert("RGBA"))
            im = bg
        im = im.convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=JPEG_Q, optimize=True, progressive=False)
    return "img/" + key + ".jpg"


def prepare_logo(src, name, out_dir, max_w):
    dst = os.path.join(out_dir, name)
    if not os.path.exists(dst):
        im = Image.open(src).convert("RGBA")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(dst, "PNG", optimize=True)
    return "img/" + name


MODEL_RE = re.compile(r"NF-[A-Z]+ \d+(?: [A-Z]+)?")


def caption(key):
    """Thumbnail caption from the site's image manifest alt text: the model code for a photo of a
    model variant ('NovoFab NF-M 10 S manual band saw ...' -> 'NF-M 10 S'), the detail for a
    detail photo ('NF-H 12 SC — hydraulic jaw clamping vise' -> 'Hydraulic jaw clamping vise')."""
    alt = (manifest.get(key) or {}).get("alt", "")
    if alt.startswith("NovoFab "):
        m = MODEL_RE.search(alt)
        return m.group(0) if m else alt[len("NovoFab "):]
    if " — " in alt:
        alt = alt.split(" — ", 1)[1].strip()
        return alt[:1].upper() + alt[1:]
    return alt


def pick_thumbs(keys, n=4):
    """Remaining images of a family: prefer the '-1' photos (model variants), keep source order."""
    rest = keys[1:]
    primary = [k for k in rest if k.endswith("-1")]
    chosen = primary[:n]
    for k in rest:
        if len(chosen) >= n:
            break
        if k not in chosen:
            chosen.append(k)
    return [k for k in rest if k in chosen]


# ---------------------------------------------------------------- spec cells
def split_cell(text):
    """'Ø10″ (254 mm)' -> ('Ø10″', '(254 mm)') so the metric part can wrap onto its own line.
    Cells with several bracket groups (e.g. body/feeder packing sizes) are left whole."""
    text = str(text)
    if text.count("(") == 1 and text.endswith(")") and " (" in text:
        a, b = text.split(" (", 1)
        return a, "(" + b
    return text, ""


CAP_RE = re.compile(r"^Capacity (?P<angle>[+-]?\d+°(?: \(straight\))?(?: right| left)?) — (?P<kind>.+)$")


def short_label(label):
    """'Capacity +45° right — rectangular W × H' -> 'Rectangular W × H at 45° right' (one line in the
    label column). The values are untouched; only the row label is rephrased."""
    m = CAP_RE.match(label)
    if not m:
        return label
    angle = m.group("angle").lstrip("+-")
    kind = m.group("kind")
    if kind != "round":
        angle = angle.replace(" (straight)", "")      # keep the label on one line; the round row says it
    return f"{kind[:1].upper()}{kind[1:]} at {angle}"


def family_table(fam):
    t = build_bandsaw_table(fam["specs"])
    n = len(t["models"])
    rows = []
    cap_group_done = False
    for r in t["rows"]:
        label = r["label"]
        if label.startswith("Capacity ") and not cap_group_done:
            rows.append({"group": True, "label": "Cutting capacity", "cells": [], "span": n})
            cap_group_done = True
        cells = [str(c) for c in r["cells"]]
        if n > 1 and len(set(cells)) == 1:
            # identical for every model (voltage, motor, drive ...) -> one merged cell
            rows.append({"group": False, "label": short_label(label), "cells": [split_cell(cells[0])], "span": n, "same": True})
        else:
            rows.append({"group": False, "label": short_label(label), "cells": [split_cell(c) for c in cells], "span": 1, "same": False})
    return {"models": t["models"], "rows": rows, "raw": t}


def row_cells(table, label_re):
    """Values of the row whose original label matches label_re, one per model (plain text)."""
    for r in table["raw"]["rows"]:
        if re.match(label_re, r["label"]):
            return [str(c) for c in r["cells"]]
    return None


# ---------------------------------------------------------------- build
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.path.join(tempfile.gettempdir(), "novofab_pdf_build"), help="scratch dir for the HTML and prepared images")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--keep-html", action="store_true", help="just say where the HTML is (it is kept anyway)")
    args = ap.parse_args()

    work = os.path.abspath(args.work)
    img_dir = os.path.join(work, "img")
    os.makedirs(img_dir, exist_ok=True)

    data = json.load(open(DATA, encoding="utf-8"))
    fams_all = data["families"]
    order = [k for k in data["order"] if fams_all[k].get("brand") == "novofab"]
    fams = [fams_all[k] for k in order]
    if len(fams) != 14:
        print(f"warning: expected 14 NovoFab families, found {len(fams)}", file=sys.stderr)

    # page numbering: 1 cover, 2 range, 3.. products, last = services
    first_product_page = 3
    pages = []
    group_first = {}
    for i, f in enumerate(fams):
        pn = first_product_page + i
        thumbs = pick_thumbs(f["images"])
        # model notes go under the table (data-source remarks such as 'not printed in the catalogue' are skipped)
        notes = [(f"{m['name']}: " if len(f["specs"]["models"]) > 1 else "") + m["notes"]
                 for m in f["specs"]["models"] if m.get("notes") and "catalogue" not in m["notes"].lower()]
        page = {
            "n": pn,
            "id": f["id"],
            "group": f["group"],
            "group_label": dict(GROUPS)[f["group"]],
            "name": f["name"],
            "short": f["short"],
            "models_label": f["models_label"],
            "summary": f["summary"],
            "features": f["features"],
            "optional": f.get("optional") or [],
            "main": {"src": prepare_photo(f["images"][0], img_dir), "alt": caption(f["images"][0])},
            "thumbs": [{"src": prepare_photo(k, img_dir), "cap": caption(k)} for k in thumbs],
            "table": family_table(f),
            "n_models": len(f["specs"]["models"]),
            "notes": notes,
            "section": None,
        }
        if f["group"] not in group_first:
            group_first[f["group"]] = pn
        pages.append(page)
    last_page = first_product_page + len(fams)

    # section strips on the first page of each group
    for g, label in GROUPS:
        members = [p for p in pages if p["group"] == g]
        if not members:
            continue
        first, last = members[0]["n"], members[-1]["n"]
        n_models = sum(len(p["table"]["models"]) for p in members)
        members[0]["section"] = {
            "num": f"{[x for x, _ in GROUPS].index(g) + 1:02d}",
            "label": label,
            "desc": f"{n_models} models · page{'s' if last != first else ''} {first}{'–' + str(last) if last != first else ''}",
        }

    # range table (every model)
    range_rows = []
    for g, label in GROUPS:
        members = [p for p in pages if p["group"] == g]
        if not members:
            continue
        range_rows.append({"group": True, "label": label, "pages": f"{members[0]['n']}–{members[-1]['n']}" if len(members) > 1 else str(members[0]["n"])})
        for p in members:
            t = p["table"]
            rnd = row_cells(t, r"^Capacity 0° \(straight\) — round$") or ["—"] * len(t["models"])
            rect = row_cells(t, r"^Capacity 0° \(straight\) — rectangular") or ["—"] * len(t["models"])
            motor = row_cells(t, r"^Main motor$") or ["—"] * len(t["models"])
            for j, m in enumerate(t["models"]):
                range_rows.append({"group": False, "model": m, "type": GROUP_TYPE[p["group"]], "round": rnd[j], "rect": rect[j], "motor": motor[j], "page": p["n"], "series": p["short"]})
    n_models = sum(1 for r in range_rows if not r["group"])

    contents = [{"label": "Cover", "page": "1"}, {"label": "Model range", "page": "2"}]
    for g, label in GROUPS:
        members = [p for p in pages if p["group"] == g]
        if members:
            contents.append({"label": label, "page": f"{members[0]['n']}–{members[-1]['n']}" if len(members) > 1 else str(members[0]["n"])})
    contents.append({"label": "NovoTech services & contact", "page": str(last_page)})

    ctx = {
        "title": PDF_TITLE,
        "fonts_dir": "file://" + FONTS,
        "novofab_logo": prepare_logo(NOVOFAB_LOGO, "novofab-logo.png", img_dir, 1263),
        "novotech_logo": prepare_logo(NOVOTECH_LOGO, "novotech-logo.png", img_dir, 900),
        "cover_photos": [prepare_photo(k, img_dir) for k in COVER_PHOTOS],
        "pages": pages,
        "range_rows": range_rows,
        "n_models": n_models,
        "n_series": len(pages),
        "contents": contents,
        "last_page": last_page,
        "company_line": COMPANY_LINE,
        "included_label": INCLUDED_LABEL,
        "included_items": INCLUDED_ITEMS,
        "voltage_line": VOLTAGE_LINE,
        "first_product_page": first_product_page,
        "last_product_page": last_page - 1,
    }

    env = Environment(loader=FileSystemLoader(HERE), autoescape=select_autoescape(["html", "j2"]), trim_blocks=True, lstrip_blocks=True)
    css = open(os.path.join(HERE, "catalogue.css"), encoding="utf-8").read().replace("__FONTS__", "file://" + FONTS)
    html = env.get_template("catalogue.html.j2").render(css=css, **ctx)
    html_path = os.path.join(work, "catalogue.html")
    open(html_path, "w", encoding="utf-8").write(html)
    print("html:", html_path)

    render_pdf(html_path, args.out)
    set_metadata(args.out)
    print("pdf:", args.out, f"({os.path.getsize(args.out) / 1e6:.1f} MB)")


# ---------------------------------------------------------------- render
OVERFLOW_JS = """() => {
  const out = [];
  document.querySelectorAll('.page').forEach((pg, i) => {
    const r = pg.getBoundingClientRect();
    let worst = 0, el = null;
    pg.querySelectorAll('*').forEach(e => {
      const b = e.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) return;
      const ov = Math.max(b.bottom - r.bottom, b.right - r.right, r.left - b.left, r.top - b.top);
      if (ov > worst) { worst = ov; el = e; }
    });
    if (worst > 0.5) out.push({page: i + 1, id: pg.id, overflow: Math.round(worst), tag: el.tagName + '.' + el.className});
  });
  return out;
}"""

FIT_JS = """(ids) => {
  ids.forEach(id => {
    const pg = document.getElementById(id);
    const lvl = (+pg.dataset.fit || 0) + 1;
    pg.dataset.fit = lvl;
    pg.classList.add('fit-' + lvl);
  });
}"""

# After fitting, product pages may have free space above the footer: let the main photo grow into it
# (up to `cap` px). The photo column is only allowed to become as tall as the text column plus the
# free space, so nothing moves off the page.
BALANCE_JS = """(caps) => {
  const grown = [];
  document.querySelectorAll('.page.product').forEach(pg => {
    const roomy = pg.classList.contains('m1') || pg.classList.contains('m2');
    const fig = pg.querySelector('figure.main'); const img = fig.querySelector('img');
    const free = () => pg.querySelector('footer').getBoundingClientRect().top - pg.querySelector('.content').getBoundingClientRect().bottom;
    const colsRoom = () => Math.max(0, pg.querySelector('.left').getBoundingClientRect().height - pg.querySelector('.right').getBoundingClientRect().height);
    // main photo: up to the cap, never taller than the image itself at column width
    const h = fig.getBoundingClientRect().height;
    const byAspect = fig.getBoundingClientRect().width * img.naturalHeight / img.naturalWidth;
    const newH = Math.min(roomy ? caps.roomy : caps.tight, byAspect, h + colsRoom() + free() - 6);
    if (newH > h + 3) { fig.style.height = newH + 'px'; grown.push(pg.id + ':photo+' + Math.round(newH - h)); }
    // thumbnails take what is left (shared between their rows), capped relative to their width
    const thumbs = Array.from(pg.querySelectorAll('.thumb img'));
    if (thumbs.length) {
      const rows = new Set(thumbs.map(t => Math.round(t.getBoundingClientRect().top))).size;
      const th = thumbs[0].getBoundingClientRect().height, tw = thumbs[0].getBoundingClientRect().width;
      const newT = Math.min(caps.thumb, tw * 0.8, th + (colsRoom() + free() - 6) / rows);
      if (newT > th + 3) { thumbs.forEach(t => t.style.height = newT + 'px'); grown.push(pg.id + ':thumbs+' + Math.round(newT - th)); }
    }
  });
  return grown;
}"""


def render_pdf(html_path, out_pdf):
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 816, "height": 1056})
        page.emulate_media(media="print")
        page.goto("file://" + html_path, wait_until="load")
        page.evaluate("document.fonts.ready")
        page.wait_for_function("Array.from(document.images).every(i => i.complete)")
        for attempt in range(6):
            bad = page.evaluate(OVERFLOW_JS)
            if not bad:
                break
            print(f"fit pass {attempt + 1}: tightening", ", ".join(f"p{b['page']} ({b['overflow']}px, {b['tag']})" for b in bad))
            page.evaluate(FIT_JS, [b["id"] for b in bad])
        else:
            bad = page.evaluate(OVERFLOW_JS)
            if bad:
                print("WARNING: still overflowing:", bad, file=sys.stderr)
        fits = page.evaluate("() => Array.from(document.querySelectorAll('.page')).map(p => +p.dataset.fit || 0)")
        print("fit levels per page:", fits)
        grown = page.evaluate(BALANCE_JS, {"roomy": 3.8 * 96, "tight": 3.3 * 96, "thumb": 1.3 * 96})
        if grown:
            print("photo grown into free space:", ", ".join(grown))
        bad = page.evaluate(OVERFLOW_JS)
        if bad:
            print("WARNING: overflow after balancing:", bad, file=sys.stderr)
        page.pdf(path=out_pdf, format="Letter", print_background=True, prefer_css_page_size=True,
                 margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                 display_header_footer=False)
        browser.close()


def set_metadata(path):
    try:
        import pikepdf
    except ImportError:
        print("pikepdf not installed - /Author not set", file=sys.stderr)
        return
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        pdf.docinfo["/Title"] = PDF_TITLE
        pdf.docinfo["/Author"] = PDF_AUTHOR
        pdf.docinfo["/Subject"] = "NovoFab Machinery metal cutting band saws — manual, semi-automatic, automatic and double column models, imperial specifications"
        pdf.docinfo["/Creator"] = PDF_AUTHOR
        pdf.docinfo["/Producer"] = PDF_AUTHOR
        pdf.docinfo["/Keywords"] = "NovoFab, NovoTech, band saw, bandsaw, metal cutting, Canada"
        pdf.save(path)
    print("metadata set (title/author)")


if __name__ == "__main__":
    main()
