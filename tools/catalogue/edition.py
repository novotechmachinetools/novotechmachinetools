#!/usr/bin/env python3
"""NovoTech's English / inch edition of the EUROSTAMP tooling catalogue.

Every EUROSTAMP page (3 – 271) goes through:
  1. pages.py      the page's own handler, where it has one: running text set again in North American English, tables
                   given their imperial twin, the page-6 bending chart in inches …
  2. cleanup.py    the rest of the Italian taken out line by line, SECTIONED / HORN tags, decimal points, round Ø
  3. specblock.py  'Max US t/ft = …' under every 'Max T/m = …'
  4. annotate.py   inch values: dimensions (parallel to their number, under it where there is room), grids, tool data
                   lines, piece lengths, length / weight boxes (with their tags), dimensions drawn as outlines (OCR)
  5. logo.py       NovoTech's logo, linked to the website
then NovoTech's cover and edition page replace EUROSTAMP's pages 1 – 2, the American-style section follows page 271 and
NovoTech's back cover closes the book.  EUROSTAMP's page numbers are kept, so the index still points to the right pages.

    python3 tools/catalogue/edition.py --pages 3-140 --part a      process a range into a part file
    python3 tools/catalogue/edition.py --assemble                  join the parts with the NovoTech pages
"""
import argparse
import json
import os
import sys
import time

import fitz
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))

from cleanup import clean_page                  # noqa: E402
from specblock import add_us_lines              # noqa: E402
from annotate import annotate_page              # noqa: E402
from logo import place_logo                     # noqa: E402
import eurostamp_codes                          # noqa: E402
import pages as PG                              # noqa: E402

CAT = "/home/claude/eurostamp/pdf/cat.pdf"
WORK = os.path.join(ROOT, "tools", "cache", "edition")
OCR_PAGES = {16, 17, 23, 27, 28, 61, 63, 64, 172, 195, 216, 228, 229, 231, 232, 237, 238, 239}
NO_NUMBERS = set(range(1, 14)) | {14, 90, 146, 170, 190}          # cover, intro, index and section openers


def process(page, ppage, codes, report):
    pno = page.number + 1
    h = PG.HANDLERS.get(pno)
    ctx = {"skip_rects": [], "skip_lines": set(), "no_clean": False, "no_numbers": pno in NO_NUMBERS}
    if h:
        h(page, ppage, ctx)
        ppage = None                                # the page changed: no pdfplumber matrices for the cleanup
    if not ctx["no_clean"]:
        clean_page(page, ppage, report=report)
    add_us_lines(page, None, report=report)
    n = {}
    if not ctx["no_numbers"]:
        n = annotate_page(page, codes=codes, skip_rects=ctx["skip_rects"], ocr=pno in OCR_PAGES, report=report)
    post = PG.POST.get(pno)
    if post:
        post(page, ctx)
    place_logo(page)
    return n


def run_part(pages, part):
    os.makedirs(WORK, exist_ok=True)
    doc = fitz.open(CAT)
    pl = pdfplumber.open(CAT)
    codes = eurostamp_codes.codes(doc)
    report, t0 = [], time.time()
    for p in pages:
        n = process(doc[p - 1], pl.pages[p - 1], codes, report)
        print(p, n, f"{time.time() - t0:.0f}s", flush=True)
    out = fitz.open()
    for p in pages:
        out.insert_pdf(doc, from_page=p - 1, to_page=p - 1)
    out.save(os.path.join(WORK, f"part-{part}.pdf"), garbage=3, deflate=True)
    json.dump({"pages": pages, "report": report}, open(os.path.join(WORK, f"part-{part}.json"), "w"))
    print("saved part", part, len(pages), "pages;", len(report), "left")


def assemble(out_path):
    parts = sorted((f for f in os.listdir(WORK) if f.startswith("part-") and f.endswith(".json")),
                   key=lambda f: os.path.getmtime(os.path.join(WORK, f)))      # later runs of a page win
    by_page = {}
    for pj in parts:
        meta = json.load(open(os.path.join(WORK, pj)))
        pdf = fitz.open(os.path.join(WORK, pj.replace(".json", ".pdf")))
        for i, p in enumerate(meta["pages"]):
            by_page[p] = (pdf, i)
    front = PG.front_pages()                         # NovoTech cover + edition page (+ back cover last)
    final = fitz.open()
    final.insert_pdf(front, from_page=0, to_page=1)
    for p in range(3, 272):
        src, i = by_page[p]
        final.insert_pdf(src, from_page=i, to_page=i)
    am = PG.american_pages()
    if am is not None:
        final.insert_pdf(am)
    final.insert_pdf(front, from_page=front.page_count - 1, to_page=front.page_count - 1)
    final.set_metadata({"title": "Press brake tooling catalogue — EUROSTAMP, NovoTech inch edition", "author": "NovoTech Machine Tools Inc.",
                        "subject": "EUROSTAMP punches, dies, holders, adapters and clamps with every dimension in inches and millimetres",
                        "keywords": "press brake tooling, punches, dies, Amada-Promecam, European style, Trumpf, Wila, Bystronic, American style, inch",
                        "creator": "NovoTech Machine Tools Inc.", "producer": "NovoTech Machine Tools Inc."})
    final.subset_fonts()
    final.save(out_path, garbage=3, deflate=True, encryption=fitz.PDF_ENCRYPT_NONE)
    print("saved", out_path, final.page_count, "pages", os.path.getsize(out_path) // 1024, "KB")


def parse_pages(s):
    out = []
    for a in s.split(","):
        if "-" in a:
            x, y = a.split("-")
            out += list(range(int(x), int(y) + 1))
        elif a:
            out.append(int(a))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="")
    ap.add_argument("--part", default="a")
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "src", "files", "NovoTech-Press-Brake-Tooling-Catalogue-2026.pdf"))
    a = ap.parse_args()
    if a.assemble:
        assemble(a.out)
    else:
        run_part(parse_pages(a.pages), a.part)
