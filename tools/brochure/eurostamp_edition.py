#!/usr/bin/env python3
"""NovoTech's inch edition of the EUROSTAMP tooling catalogue.

EUROSTAMP's IT-EN catalogue, page for page, with every metric dimension, scale-grid mark, specification length and
length / weight box given in inches and pounds as well (tools/eurostamp_catalogue.py), in NovoTech's catalogue format:
EUROSTAMP's cover becomes a NovoTech cover, its blank page 2 explains the edition (what was added, the clamping styles
and their pages, Max T/m in US tons per foot), and its back cover becomes NovoTech's contact page.  Page numbers stay
EUROSTAMP's, so the product index (pages 8 – 13) still points to the right page.

    python3 tools/brochure/eurostamp_edition.py [--out src/files/NovoTech-Press-Brake-Tooling-Catalogue-2026.pdf]
"""
import argparse
import os
import sys

import fitz
from jinja2 import Environment, FileSystemLoader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_brochure as BB                 # noqa: E402  (img(): the site's image variants flattened for Chromium)
import eurostamp_catalogue as EC            # noqa: E402

OUT = os.path.join(ROOT, "src", "files", "NovoTech-Press-Brake-Tooling-Catalogue-2026.pdf")
STYLES = [("Amada-Promecam (European) style", "14 – 89", "#d71920"), ("— ESH same-height series", "77 – 89", "#f06e74"),
          ("Trumpf style", "90 – 145", "#1fa3dd"), ("Wila style", "146 – 169", "#a54d97"), ("Bystronic style", "170 – 189", "#f07f22"),
          ("Radius, offset, nylon and urethane tools; EUROGRIP clamping; intermediates, clamps, adapters, tangs, adjustable dies, "
           "accessories and special tools", "190 – 269", "#8e9196"),
          ("American style (.500″ tang)", "272 – 277", "#2e8b57")]
LOADS = [25, 30, 35, 40, 50, 60, 65, 70, 80, 85, 90, 100, 120, 125, 150, 160, 180, 200, 250, 300, 340, 400]


def front_back_pdf(sample_png, n_tools, path):
    env = Environment(loader=FileSystemLoader(HERE), autoescape=True)
    loads = [(str(v), f"{v * EC.US_T_FT:.1f}") for v in LOADS]
    rows = [loads[i:i + 3] for i in range(0, len(loads), 3)]
    rows[-1] += [("", "")] * (3 - len(rows[-1]))
    html = env.get_template("eurostamp_edition.html").render(
        fonts="file://" + os.path.join(ROOT, "src", "fonts"), logo=BB.img("novotech-logo", 800, png=True)["src"],
        logo_dark=BB.img("novotech-logo", 800, png=True)["src"], hero=BB.img("es-p-range", 1600)["src"],
        maker_logo=BB.img("eurostamp-logo", 600, png=True)["src"], sample="file://" + sample_png, n_tools=n_tools,
        styles=[{"name": n, "pages": p, "color": c} for n, p, c in STYLES], loads=rows)
    hp = os.path.join(HERE, "out", "eurostamp-edition.html")
    open(hp, "w", encoding="utf-8").write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + hp, wait_until="networkidle")
        pg.wait_for_timeout(400)
        pg.pdf(path=path, width="210mm", height="297mm", print_background=True, prefer_css_page_size=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    return path


def build(out=OUT, pages=None, annotated=None):
    if annotated:                                   # an annotated copy saved by tools/eurostamp_catalogue.py --out
        doc, report = fitz.open(annotated), []
    else:
        doc, tot, report = EC.annotate(pages=pages)
        print("annotated:", tot, len(report), "numbers without a free spot")
    # a sample of the result for page 2: punch 1055 on page 36
    sample = os.path.join(HERE, "out", "img", "es-edition-sample.png")
    os.makedirs(os.path.dirname(sample), exist_ok=True)
    doc[35].get_pixmap(dpi=230, clip=fitz.Rect(40, 56, 331, 462)).save(sample)
    n_tools = len({s for s in EC.catalogue_codes(doc)})
    nt = os.path.join(HERE, "out", "eurostamp-edition-pages.pdf")
    front_back_pdf(sample, f"{n_tools // 50 * 50}+", nt)
    extra = fitz.open(nt)
    final = fitz.open()
    final.insert_pdf(extra, from_page=0, to_page=1)             # NovoTech cover, about this edition
    final.insert_pdf(doc, from_page=2, to_page=doc.page_count - 2)   # EUROSTAMP's pages 3 – 271
    final.insert_pdf(extra, from_page=2, to_page=2)             # NovoTech back cover instead of EUROSTAMP's address page
    final.set_metadata({"title": "Press brake tooling catalogue — EUROSTAMP, inch edition", "author": "NovoTech Machine Tools Inc.",
                        "subject": "EUROSTAMP punches, dies, holders, adapters and clamps with every dimension in millimetres and inches",
                        "keywords": "press brake tooling, punches, dies, Amada-Promecam, European style, Trumpf, Wila, Bystronic, inch",
                        "creator": "NovoTech Machine Tools Inc.", "producer": "NovoTech Machine Tools Inc."})
    final.subset_fonts()
    final.save(out, garbage=3, deflate=True, encryption=fitz.PDF_ENCRYPT_NONE)
    print("saved", out, final.page_count, "pages", os.path.getsize(out) // 1024, "KB")
    return out, report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--annotated", default="")
    a = ap.parse_args()
    build(a.out, annotated=a.annotated or None)
