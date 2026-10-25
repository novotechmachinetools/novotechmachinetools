#!/usr/bin/env python3
"""NovoTech brochure generator — the site's family data rendered as a Letter-size PDF catalogue (Playwright / Chromium).

    python3 tools/brochure/build_brochure.py tools/brochure/specs/production-presses.json [--html]

The spec names the family set, the families (in order), cover / about text and the output file.  Every page is one
<section class="page"> sized exactly to the sheet, so page numbers are known before rendering (contents page).  The
layout follows the NovoTech catalogue style: charcoal header band with an orange series tab, photo band, MODEL tag,
description, standard / optional equipment, "Included with every NovoTech machine" box, orange footer rule with the
address and page number, specification tables with the imperial (metric) cells used on the site.
"""
import json
import os
import re
import sys

from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
MANIFEST = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))

INCLUDED = [("Made in {country} with European components", ""), ("CSA-approved electrical panel", ""), ("1-year warranty", ""),
            ("7-day money-back guarantee", "in-stock machines only"), ("Spare parts & technical support", "readily available in Canada"),
            ("Order today with just 10% down", "0% down financing available"), ("Installation and training available", "")]


def img(key, size=1200, png=False):
    """The site's WebP variant ≤ size, flattened over white and saved as a JPEG in tools/brochure/out/img/ — Chromium keeps
    JPEG data as-is in the PDF, while a PNG / WebP cut-out is re-encoded losslessly and makes the PDF ten times larger."""
    e = MANIFEST.get(key)
    if not e:
        return None
    best = max((v for v in e["variants"] if v["w"] <= size), key=lambda v: v["w"], default=e["variants"][-1])
    src = os.path.join(ROOT, "src", best["file"])
    out = os.path.join(HERE, "out", "img", f"{key}-{best['w']}." + ("png" if png else "jpg"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        from PIL import Image
        im = Image.open(src)
        if png:                                   # logos on dark backgrounds keep their transparency
            im.convert("RGBA").save(out, optimize=True)
        else:
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA")
                bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
            im.convert("RGB").save(out, quality=86, optimize=True)
    return {"src": "file://" + out, "alpha": e.get("alpha"), "w": best["w"], "h": best["h"], "alt": e.get("alt", "")}


def table_weight(t):
    return 2 + len(t["rows"]) * (1.0 + 0.08 * max(0, len(t["models"]) - 4))


def paginate_tables(tables, budget=34):
    pages, cur, w = [], [], 0
    for t in tables:
        tw = table_weight(t)
        if cur and w + tw > budget:
            pages.append(cur); cur, w = [], 0
        cur.append(t); w += tw
    if cur:
        pages.append(cur)
    return pages


def layout(families, no_inline):
    """A short first table goes on the family page itself unless the page overflowed on the previous pass."""
    for f in families:
        tables = list(f["specs"]["tables"])
        f["inline_table"] = None
        if tables and f["id"] not in no_inline and table_weight(tables[0]) <= 20:
            f["inline_table"] = tables.pop(0)
        f["spec_pages"] = paginate_tables(tables)


def overflowing(pg):
    """Family ids whose page content runs into the footer."""
    return pg.evaluate("""() => [...document.querySelectorAll('section.page[data-fam]')].filter(p => {
        const b = p.querySelector('.body'), f = p.querySelector('.foot'); if (!b || !f) return false;
        const kids = [...b.children]; if (!kids.length) return false;
        const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
        return bottom > f.getBoundingClientRect().top - 4; }).map(p => p.dataset.fam)""")


def render(spec, no_inline):
    fams_all = {}
    for s in spec["family_sets"]:
        fams_all.update(json.load(open(os.path.join(ROOT, "content", "families", f"{s}.json"), encoding="utf-8"))["families"])
    families = []
    for fid in spec["families"]:
        f = dict(fams_all[fid])
        f["hero"] = img(f["images"][0]) if f["images"] else None
        f["minis"] = [img(k) for k in f["images"][1:3]]
        f["mini_alts"] = [MANIFEST.get(k, {}).get("alt", "") for k in f["images"][1:3]]
        f["series"] = f.get("short", f["name"]).split(" ")[0] if not f.get("series") else f["series"]
        families.append(f)
    layout(families, no_inline)
    # page numbering: cover 1, contents 2, about 3, then families, back cover
    page = 4
    for f in families:
        f["page"] = page
        page += 1 + len(f["spec_pages"])
    total = page
    groups = []
    for g in spec.get("groups", []):
        groups.append({"title": g["title"], "families": [f for f in families if f["id"] in g["families"]]})
    if not groups:
        groups = [{"title": spec["title"], "families": families}]
    env = Environment(loader=FileSystemLoader(HERE), autoescape=False)
    env.filters["img"] = img
    html = env.get_template("brochure.html").render(spec=spec, site=SITE, families=families, groups=groups, total=total, included=INCLUDED,
                                                     fonts="file://" + os.path.join(ROOT, "src", "fonts"), logo=img("novotech-logo", 800, png=True),
                                                     cover_imgs=[img(k) for k in spec["cover_photos"]], year=spec.get("year", "2026"))
    out_html = os.path.join(HERE, "out", os.path.basename(spec["out"]).replace(".pdf", ".html"))
    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    open(out_html, "w", encoding="utf-8").write(html)
    return out_html, total


def build(spec_path, html_only=False):
    spec = json.load(open(spec_path, encoding="utf-8"))
    no_inline = set(spec.get("no_inline", []))
    out_html, total = render(spec, no_inline)
    if html_only:
        print("html:", out_html); return
    from playwright.sync_api import sync_playwright
    out_pdf = os.path.join(ROOT, spec["out"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        for _ in range(3):      # inline tables that run into the footer go to a specifications page, then re-render
            pg = b.new_page()
            pg.goto("file://" + out_html, wait_until="networkidle")
            pg.emulate_media(media="print")
            over = set(overflowing(pg))
            new = over - no_inline
            if not new:
                if over:
                    print("!! pages still overflow:", sorted(over))
                break
            print("inline table does not fit, moved to a specifications page:", ", ".join(sorted(new)))
            no_inline |= new
            pg.close()
            out_html, total = render(spec, no_inline)
        pg.pdf(path=out_pdf, format="Letter", print_background=True, prefer_css_page_size=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    print(f"pdf: {out_pdf} ({os.path.getsize(out_pdf) / 1e6:.1f} MB, {total} pages)")


if __name__ == "__main__":
    build(sys.argv[1], "--html" in sys.argv)
