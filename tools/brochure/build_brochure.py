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


def cover_layout(imgs, W=7.9, H=4.35, pad=0.2, gap=0.2):
    """the cover photos placed whole in the white band (the owner, Nov 7 2026: in a flex row the side photos ran half off the
    page and wide machines left the band empty above them).  The main photo is the second one (the first when there is one); the
    candidate layouts — one justified row, the main photo large on the left / right / top with the others beside or under it,
    a 2 × 2 grid — are tried and the one that shows the most photo wins, the main photo counting more.  Every photo is fitted
    whole (contain) and centred in its cell: positions in inches inside the band."""
    imgs = [i for i in imgs if i][:4]
    n = len(imgs)
    if not n:
        return []
    ar = [i["w"] / i["h"] for i in imgs]
    m = 1 if n >= 2 else 0
    w, h = W - 2 * pad, H - 2 * pad
    others = [k for k in range(n) if k != m]

    def fit(k, cell):
        x, y, cw, ch = cell
        fw = min(cw, ch * ar[k]); fh = fw / ar[k]
        return {"k": k, "x": x + (cw - fw) / 2, "y": y + (ch - fh) / 2, "w": fw, "h": fh}

    def score(place):
        return sum(p["w"] * p["h"] * (1.7 if p["k"] == m else 1.0) for p in place)

    cands = []
    if n == 1:
        cands.append([fit(0, (pad, pad, w, h))])
    else:
        # one justified row, the main photo 1.25 × the others' height
        sc = [1.25 if k == m else 1.0 for k in range(n)]
        row_h = min((w - gap * (n - 1)) / sum(a * s for a, s in zip(ar, sc)), h / max(sc))
        total_w = sum(a * s * row_h for a, s in zip(ar, sc)) + gap * (n - 1)
        x = pad + (w - total_w) / 2
        place = []
        for k in range(n):
            cw, ch = ar[k] * sc[k] * row_h, sc[k] * row_h
            place.append({"k": k, "x": x, "y": pad + (h - ch) / 2, "w": cw, "h": ch})
            x += cw + gap
        cands.append(place)
        for f in (0.55, 0.62, 0.7):
            bw = w * f
            sw = w - bw - gap
            sh = (h - gap * (len(others) - 1)) / len(others)
            # main on the left, the others stacked on the right — and the mirror
            cands.append([fit(m, (pad, pad, bw, h))] + [fit(k, (pad + bw + gap, pad + i * (sh + gap), sw, sh)) for i, k in enumerate(others)])
            cands.append([fit(m, (pad + sw + gap, pad, bw, h))] + [fit(k, (pad, pad + i * (sh + gap), sw, sh)) for i, k in enumerate(others)])
            # main across the top, the others in a row under it
            bh = h * f
            rw = (w - gap * (len(others) - 1)) / len(others)
            cands.append([fit(m, (pad, pad, w, bh))] + [fit(k, (pad + i * (rw + gap), pad + bh + gap, rw, h - bh - gap)) for i, k in enumerate(others)])
        if n == 4:
            cw, ch = (w - gap) / 2, (h - gap) / 2
            cands.append([fit(k, (pad + (k % 2) * (cw + gap), pad + (k // 2) * (ch + gap), cw, ch)) for k in range(4)])
    best = max(cands, key=score)
    return [dict(imgs[p["k"]], x=round(p["x"], 3), y=round(p["y"], 3), w_in=round(p["w"], 3), h_in=round(p["h"], 3)) for p in best]


def table_weight(t):
    return 2 + len(t["rows"]) * (1.0 + 0.08 * max(0, len(t["models"]) - 4))


def split_rows(t, budget):
    """A table that alone is heavier than a page goes on as row chunks of the same table (the header row repeats)."""
    per = 1.0 + 0.08 * max(0, len(t["models"]) - 4)
    n = max(3, int((budget - 2) / per))
    if len(t["rows"]) <= n:
        return [t]
    return [dict(t, rows=t["rows"][i:i + n], title=t["title"] + (" (continued)" if i else "")) for i in range(0, len(t["rows"]), n)]


def paginate_tables(tables, budget=34):
    pages, cur, w = [], [], 0
    tables = [c for t in tables for c in (split_rows(t, budget) if table_weight(t) > budget else [t])]
    for t in tables:
        tw = table_weight(t)
        if cur and w + tw > budget:
            pages.append(cur); cur, w = [], 0
        cur.append(t); w += tw
    if cur:
        pages.append(cur)
    return pages


def split_cols(t, n):
    """A table too wide for the page (its model columns ran past the right edge — the owner's PDF check, Nov 7 2026) goes on as
    n tables of the same rows, each with a share of the model columns; the later ones are titled "(continued)"."""
    models = t["models"]
    if n <= 1 or len(models) < 2:
        return [t]
    n = min(n, len(models))
    per = -(-len(models) // n)
    out = []
    for k, i in enumerate(range(0, len(models), per)):
        rows = [dict(r, cells=r["cells"][i:i + per]) if len(r["cells"]) == len(models) else r for r in t["rows"]]
        out.append(dict(t, models=models[i:i + per], rows=rows, title=t["title"] + (" (continued)" if k else "")))
    return out


def layout(families, no_inline, budgets=None, colsplit=None):
    """A short first table goes on the family page itself unless the page overflowed on the previous pass; a family whose
    specification page ran into the footer gets a smaller per-page budget (budgets[fid]) and is paginated again; a table
    wider than the page is split by columns (colsplit[(fid, table index)] parts)."""
    for f in families:
        src = list((f.get("brochure_specs") or f["specs"])["tables"])        # brochure_specs: the site shows a shorter table
        tables = [c for i, t in enumerate(src) for c in split_cols(dict(t, key=i), (colsplit or {}).get((f["id"], i), 1))]
        f["inline_table"] = None
        if tables and f["id"] not in no_inline and table_weight(tables[0]) <= 20:
            f["inline_table"] = tables.pop(0)
        f["spec_pages"] = paginate_tables(tables, (budgets or {}).get(f["id"], 34))


def overflowing(pg, sel="section.page[data-fam]"):
    """Family ids whose page (family page, or with sel='section.page[data-spec]' a specifications page) runs into the footer."""
    return pg.evaluate("""(sel) => [...document.querySelectorAll(sel)].filter(p => {
        const b = p.querySelector('.body'), f = p.querySelector('.foot'); if (!b || !f) return false;
        const kids = [...b.children]; if (!kids.length) return false;
        const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
        return bottom > f.getBoundingClientRect().top - 4; }).map(p => p.dataset.fam || p.dataset.spec)""", sel)


def too_wide(pg):
    """(family id, table index) of every specification table that runs past the right edge of its page body."""
    return [tuple(x) for x in pg.evaluate("""() => [...document.querySelectorAll('table[data-fam]')].filter(t => {
        const b = t.parentElement.getBoundingClientRect(); return t.getBoundingClientRect().right > b.right + 1;
    }).map(t => [t.dataset.fam, +t.dataset.t])""")]


def bandsaw_tables(f):
    """a band-saw family (spec kind "bandsaw": capacities per model, the site builds the table) with the site's table as the
    brochure's (the Bekamak supplement, Nov 7 2026)"""
    sys.path.insert(0, ROOT)
    from build import build_bandsaw_table
    t = build_bandsaw_table(f["specs"])
    note = ("Capacities are the largest stock the saw passes at the stated angle, converted from the manufacturer's metric data and "
            "rounded to the nearest 1/8″. Blade size is length × width × thickness.")          # the note under the site's band-saw tables
    return dict(f["specs"], tables=[{"title": f.get("short") or f["name"], "sub": "", "models": t["models"], "rows": t["rows"]}], note=note)


def render(spec, no_inline, budgets=None, tight=None, colsplit=None):
    fams_all = {}
    for s in spec["family_sets"]:
        fams_all.update(json.load(open(os.path.join(ROOT, "content", "families", f"{s}.json"), encoding="utf-8"))["families"])
    families = []
    for fid in spec["families"]:
        f = dict(fams_all[fid])
        if f.get("brochure_specs"):
            f["specs"] = f["brochure_specs"]
        elif (f.get("specs") or {}).get("kind") == "bandsaw" and "tables" not in f["specs"]:
            f["specs"] = bandsaw_tables(f)
        f["hero"] = img(f["images"][0]) if f["images"] else None
        f["minis"] = [img(k) for k in f["images"][1:3]]
        f["mini_alts"] = [MANIFEST.get(k, {}).get("alt", "") for k in f["images"][1:3]]
        f["series"] = f.get("short", f["name"]).split(" ")[0] if not f.get("series") else f["series"]
        f["tight"] = (tight or {}).get(fid, 0)       # 1 / 2 / 3: smaller photo band and type when the equipment lists overflow
        # every other photo of the family on detail pages after the family page, nine to a page with their captions — the
        # brochure carries all the photos and details, not a summary (the owner, Nov 1 2026: "summarize no PDF catalogue");
        # a spec can turn it off with "gallery": false
        gal = [g for g in (img(k) for k in f["images"][3:]) if g] if spec.get("gallery", True) else []
        f["gallery_pages"] = [gal[i:i + 9] for i in range(0, len(gal), 9)]
        families.append(f)
    layout(families, no_inline, budgets, colsplit)
    # spec "intro_pages": overview pages after About — the series side by side, the loading options (the owner, Nov 1 2026)
    intro = []
    for ip in spec.get("intro_pages") or []:
        ip = dict(ip)
        ip["cards"] = [dict(c, img=img(c["image"], 800) if c.get("image") else None) for c in ip.get("cards", [])]
        ip["photos"] = [g for g in (img(k, 800) for k in ip.get("photos", [])) if g]
        intro.append(ip)
    # page numbering: cover 1, contents 2, about 3, overview pages, then families, back cover
    page = 4 + len(intro)
    for f in families:
        f["page"] = page
        page += 1 + len(f["gallery_pages"]) + len(f["spec_pages"])
    total = page
    groups = []
    for g in spec.get("groups", []):
        groups.append({"title": g["title"], "families": [f for f in families if f["id"] in g["families"]]})
    if not groups:
        groups = [{"title": spec["title"], "families": families}]
    env = Environment(loader=FileSystemLoader(HERE), autoescape=False)
    env.filters["img"] = img
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import section_icons   # the section shapes of the profile benders' capacity rows, as on the site (the owner, Nov 11 2026)
    env.globals["sec_icon"] = lambda fid, label: section_icons.svg(section_icons.icon_id(fid, label) or "")
    included = [(spec["made_in"], "")] + INCLUDED[1:] if spec.get("made_in") else INCLUDED   # value line: "Built in China to North American standards"
    html = env.get_template("brochure.html").render(spec=spec, site=SITE, families=families, groups=groups, total=total, included=included, intro=intro,
                                                     fonts="file://" + os.path.join(ROOT, "src", "fonts"), logo=img("novotech-logo", 800, png=True),
                                                     cover_imgs=cover_layout([img(k) for k in spec["cover_photos"]]), year=spec.get("year", "2026"))
    out_html = os.path.join(HERE, "out", os.path.basename(spec["out"]).replace(".pdf", ".html"))
    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    open(out_html, "w", encoding="utf-8").write(html)
    return out_html, total


def build(spec_path, html_only=False):
    spec = json.load(open(spec_path, encoding="utf-8"))
    no_inline = set(spec.get("no_inline", []))
    budgets, tight, colsplit = {}, {}, {}
    out_html, total = render(spec, no_inline, budgets, tight, colsplit)
    if html_only:
        print("html:", out_html); return
    from playwright.sync_api import sync_playwright
    out_pdf = os.path.join(ROOT, spec["out"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        for _ in range(10):     # inline tables that run into the footer go to a specifications page; specification pages that
            pg = b.new_page()   # run into the footer are paginated with a smaller budget; tables wider than the page are split
            pg.goto("file://" + out_html, wait_until="networkidle")   # by columns; then re-render
            pg.emulate_media(media="print")
            over = set(overflowing(pg))
            new = over - no_inline
            spec_over = set(overflowing(pg, "section.page[data-spec]"))
            squeeze = {fid for fid in over - new if tight.get(fid, 0) < 3}     # inline table already gone: tighten the page
            wide = set(too_wide(pg))
            for key in wide:
                colsplit[key] = colsplit.get(key, 1) + 1
                print(f"table {key[1]} of {key[0]} is wider than the page — splitting its columns in {colsplit[key]}")
            if not new and not spec_over and not squeeze and not wide:
                if over:
                    print("!! pages still overflow:", sorted(over))
                break
            for fid in squeeze:
                tight[fid] = tight.get(fid, 0) + 1
                print(f"family page of {fid} still overflows — tightening (level {tight[fid]})")
            if new:
                print("inline table does not fit, moved to a specifications page:", ", ".join(sorted(new)))
                no_inline |= new
            for fid in spec_over:
                budgets[fid] = budgets.get(fid, 34) * 0.75
                print(f"specifications page of {fid} runs into the footer — paginating at {budgets[fid]:.0f}")
            pg.close()
            out_html, total = render(spec, no_inline, budgets, tight, colsplit)
        else:
            print("!! still overflowing after 10 passes")
            pg = b.new_page()
            pg.goto("file://" + out_html, wait_until="networkidle")
            pg.emulate_media(media="print")
        pg.pdf(path=out_pdf, format="Letter", print_background=True, prefer_css_page_size=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    print(f"pdf: {out_pdf} ({os.path.getsize(out_pdf) / 1e6:.1f} MB, {total} pages)")


if __name__ == "__main__":
    build(sys.argv[1], "--html" in sys.argv)
