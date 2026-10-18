#!/usr/bin/env python3
"""NovoTech static site generator.

    python3 build.py            -> writes the whole site to dist/
    python3 build.py --staging  -> same, but with <meta name=robots content=noindex> for the test host

Content lives in content/, templates in templates/, static assets in src/.
"""
import json, os, re, shutil, sys, datetime, hashlib
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
STAGING = "--staging" in sys.argv
ARTIFACT = "--artifact" in sys.argv   # claude.ai artifact preview: page fragment, no doc skeleton
if ARTIFACT:
    DIST = os.path.join(ROOT, "dist-artifact")

site = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))

# ---------------------------------------------------------------- unit helpers
# Inch equivalents for rebar diameters, following NovoTech's catalogue convention
# (common fractions with denominators 2/4/8/16, the same values used in the printed brochures).
INCH = {6: "1/4", 8: "5/16", 10: "3/8", 12: "1/2", 14: "9/16", 16: "5/8", 18: "11/16", 20: "13/16",
        22: "7/8", 24: "15/16", 26: "1", 28: "1-1/8", 30: "1-1/8", 32: "1-1/4", 34: "1-3/8", 36: "1-3/8",
        38: "1-1/2", 40: "1-5/8", 42: "1-5/8", 45: "1-3/4", 50: "2", 52: "2", 55: "2-1/8", 60: "2-3/8"}
CA_BARS = [("10M", 11.3), ("15M", 16.0), ("20M", 19.5), ("25M", 25.2), ("30M", 29.9), ("35M", 35.7), ("45M", 43.7), ("55M", 56.4)]
US_BARS = [("#3", 9.5), ("#4", 12.7), ("#5", 15.9), ("#6", 19.1), ("#7", 22.2), ("#8", 25.4), ("#9", 28.7), ("#10", 32.3), ("#11", 35.8), ("#14", 43.0), ("#18", 57.3)]


def inch(mm):
    s = INCH.get(mm)
    if s is None:
        v = mm / 25.4
        whole = int(v); frac = round((v - whole) * 16)
        if frac == 16: whole += 1; frac = 0
        from fractions import Fraction
        f = Fraction(frac, 16)
        s = (f"{whole}-{f.numerator}/{f.denominator}" if whole and frac else (str(whole) if not frac else f"{f.numerator}/{f.denominator}"))
    return s + "″"


def dia(mm):
    """Ø1-3/8″ (36 mm)"""
    return f"Ø{inch(mm)} ({mm} mm)"


def bar_sizes(mm):
    ca = [n for n, d in CA_BARS if d <= mm]
    us = [n for n, d in US_BARS if d <= mm]
    parts = []
    if ca: parts.append(ca[-1])
    if us: parts.append(us[-1])
    return " / ".join(parts)


def hp(kw):
    v = kw * 1.34102
    r = round(v, 1)
    if abs(r - round(r)) <= 0.1:
        return f"{int(round(r))} HP"
    return f"{r:g} HP"


def kw_str(kw):
    return f"{kw:g} kW"


def lb(kg):
    return f"{round(kg * 2.20462):,} lb"


def cm_to_in(v):
    return str(round(v / 2.54))


def dims(cm3):
    w, l, h = cm3
    return f"{cm_to_in(w)} × {cm_to_in(l)} × {cm_to_in(h)} in ({w:g} × {l:g} × {h:g} cm)"


def cap_cell(pairs):
    """[[36,1],[22,2]] -> list of (text, barsizes) for the template"""
    out = []
    for mm, n in pairs:
        out.append({"dia": dia(mm), "n": n, "bars": bar_sizes(mm)})
    return out


def build_spec_table(spec):
    """Turn the compact spec JSON into table rows for the template."""
    models = spec["models"]
    names = [m["name"] for m in models]
    rows = []
    kind = "Bending" if spec.get("kind") == "bending" else "Cutting"
    for grade, psi in (("45", "64,000"), ("65", "92,500"), ("85", "120,900")):
        cells = [cap_cell(c) for c in spec["capacity"][grade]]
        rows.append({"label": f"{kind} capacity · {grade} kg/mm² steel", "sub": f"≈ {psi} psi tensile", "cells": cells, "type": "cap"})
    if spec.get("cutting_capacity"):
        for grade, psi in (("45", "64,000"), ("65", "92,500"), ("85", "120,900")):
            cells = [cap_cell(c) for c in spec["cutting_capacity"][grade]]
            rows.append({"label": f"Cutting capacity · {grade} kg/mm² steel", "sub": f"≈ {psi} psi tensile", "cells": cells, "type": "cap"})
    rows.append({"label": "Motor power", "cells": [m.get("kw_text") or f"{hp(m['kw'])} ({kw_str(m['kw'])})" for m in models], "type": "text"})
    if any("tank_l" in m for m in models):
        rows.append({"label": "Hydraulic oil tank", "cells": [f"{m['tank_l']:g} L" if "tank_l" in m else "—" for m in models], "type": "text"})
    extras = {}
    for m in models:
        for k, v in (m.get("extra") or {}).items():
            extras.setdefault(k, {})[m["name"]] = v
    for k, vals in extras.items():
        rows.append({"label": k, "cells": [vals.get(m["name"], "—") for m in models], "type": "text"})
    rows.append({"label": "Weight", "cells": [m.get("kg_text") or f"{lb(m['kg'])} ({m['kg']:g} kg)" for m in models], "type": "text"})
    rows.append({"label": "Dimensions W × L × H", "cells": [m.get("dims_text") or dims(m["dims_cm"]) for m in models], "type": "text"})
    rows.append({"label": "Voltage", "cells": [m.get("voltage") or spec.get("voltage", "") for m in models], "type": "text"})
    return {"models": names, "rows": rows}


# ---------------------------------------------------------------- images
def img(name):
    e = manifest.get(name)
    if not e:
        raise SystemExit(f"image not in manifest: {name}")
    v = sorted(e["variants"], key=lambda x: x["w"])
    largest = v[-1]
    return {
        "name": name,
        "alt": e["alt"],
        "src": largest["file"],
        "w": largest["w"], "h": largest["h"],
        "srcset": ", ".join(f"{x['file']} {x['w']}w" for x in v),
        "small": v[0]["file"],
        "thumb": (e.get("thumb") or v[0])["file"],
        "alpha": e["alpha"],
    }


# ---------------------------------------------------------------- jinja
env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
env.globals.update(site=site, img=img, staging=STAGING, year=datetime.date.today().year, dia=dia, inch=inch, bar_sizes=bar_sizes)


def asset_hash(path):
    h = hashlib.md5(open(path, "rb").read()).hexdigest()[:8]
    return h


def absurl(path):
    return f"{site['domain']}/{path}"


def organization_ld():
    a = site["address"]
    return {
        "@type": ["Organization", "LocalBusiness", "Store"],
        "@id": site["domain"] + "/#organization",
        "name": site["name"],
        "alternateName": site["short_name"],
        "url": site["domain"] + "/",
        "logo": absurl(img("novotech-logo")["src"]),
        "image": absurl(img("novotech-logo")["src"]),
        "telephone": site["phone"],
        "email": site["email"],
        "description": site["founded_note"],
        "address": {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"], "addressRegion": a["region"], "postalCode": a["postal"], "addressCountry": "CA"},
        "geo": {"@type": "GeoCoordinates", "latitude": site["geo"]["lat"], "longitude": site["geo"]["lng"]},
        "areaServed": {"@type": "Country", "name": "Canada"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "17:00"}],
        "sameAs": [site["youtube_channel"]],
    }


def page_ld(page):
    """Structured data for a product-category page: WebPage, BreadcrumbList, ItemList of Products, VideoObjects, FAQPage."""
    url = page["url"]
    graph = [organization_ld()]
    crumbs = []
    for i, c in enumerate(page.get("breadcrumb", []), 1):
        item = {"@type": "ListItem", "position": i, "name": c["label"]}
        item["item"] = absurl(c["href"]) if c.get("href") else url
        crumbs.append(item)
    graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumbs})
    hero = img(page["hero_image"]) if page.get("hero_image") else None
    graph.append({
        "@type": "WebPage", "@id": url, "url": url, "name": page["title"], "description": page["meta_description"],
        "inLanguage": "en-CA", "isPartOf": {"@id": site["domain"] + "/#website"},
        "about": {"@id": url + "#products"}, "breadcrumb": {"@id": url + "#breadcrumb"},
        **({"primaryImageOfPage": {"@type": "ImageObject", "url": absurl(hero["src"]), "width": hero["w"], "height": hero["h"]}} if hero else {}),
        "publisher": {"@id": site["domain"] + "/#organization"},
    })
    graph.append({"@type": "WebSite", "@id": site["domain"] + "/#website", "url": site["domain"] + "/", "name": site["name"], "publisher": {"@id": site["domain"] + "/#organization"}})
    products = []
    pos = 0
    brand = page.get("brand", {})
    for g in page.get("groups", []):
        for f in g["families"]:
            pos += 1
            purl = (absurl(g["id"] + ".html") if page.get("subpages") else url) + "#" + f["id"]
            gal = f.get("gallery") or []
            models = [m["name"] for m in (f.get("specs") or {}).get("models", [])] or [s.strip() for s in f.get("models_label", "").split("·") if s.strip()]
            prod = {
                "@type": "Product", "@id": purl, "url": purl,
                "name": f["name"], "description": f["summary"],
                "image": [absurl(i["src"]) for i in gal[:6]],
                "brand": {"@type": "Brand", "name": brand.get("name", "")},
                "manufacturer": {"@type": "Organization", "name": brand.get("name", ""), "address": {"@type": "PostalAddress", "addressCountry": "TR"}},
                "category": g["title"],
                "model": models,
                "additionalProperty": [{"@type": "PropertyValue", "name": "Standard equipment", "value": "CSA-approved electrical panel; 1-year warranty; spare parts and technical support in Canada"}],
            }
            products.append(prod)
    graph.append({"@type": "ItemList", "@id": url + "#products", "name": page["h1"], "numberOfItems": len(products), "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": p} for i, p in enumerate(products)]})
    # videos
    vids = []
    for g in page.get("groups", []):
        for f in g["families"]:
            for v in f.get("videos") or []:
                vids.append((v, url + "#" + f["id"] + "-video"))
    if page.get("intro_video"):
        vids.append((page["intro_video"], url + "#GMS-introduction-video"))
    for v, vurl in vids:
        t = img(v["thumb"])
        graph.append({
            "@type": "VideoObject", "@id": vurl, "name": v["title"], "description": v["title"] + " — NovoTech Machine Tools, Canada.",
            "thumbnailUrl": [absurl(t["src"])], "uploadDate": v.get("upload_date", "2023-12-26"), "duration": v.get("duration", "PT2M"),
            "contentUrl": "https://www.youtube.com/watch?v=" + v["id"], "embedUrl": "https://www.youtube-nocookie.com/embed/" + v["id"],
            "publisher": {"@id": site["domain"] + "/#organization"},
        })
    if page.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in page["faq"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


FAMILY_SETS = {}
for fn in os.listdir(os.path.join(ROOT, "content", "families")):
    if fn.endswith(".json"):
        FAMILY_SETS[fn[:-5]] = json.load(open(os.path.join(ROOT, "content", "families", fn), encoding="utf-8"))["families"]


def family(page, fid):
    """A deep copy of a family record from the page's family set."""
    fs = FAMILY_SETS[page.get("family_set", "rebar")]
    if fid not in fs:
        raise SystemExit(f"unknown family {fid}")
    return json.loads(json.dumps(fs[fid]))


def max_single_bar(spec, grade="45"):
    """Largest single-bar diameter (mm) across a family's models at the given steel grade."""
    best = 0
    for cells in spec["capacity"][grade]:
        for mm, n in cells:
            if n == 1 and mm > best:
                best = mm
    return best


def prepare_family(f):
    if f.get("specs"):
        f["table"] = build_spec_table(f["specs"])
        f["max_mm"] = max_single_bar(f["specs"])
        kind = "Cuts" if f["specs"].get("kind") == "cutting" else "Bends"
        f["headline"] = f.get("headline") or f"{kind} single bars to {dia(f['max_mm'])}"
    f["gallery"] = [img(n) for n in f.get("images", [])]
    f["card_image"] = f["gallery"][0] if f["gallery"] else None
    return f


def range_table(subpages):
    """One row per model across the range: for the hub's 'at a glance' table."""
    rows = []
    for sp in subpages:
        for f in sp["families"]:
            spec = f.get("specs")
            if not spec:
                continue
            for i, m in enumerate(spec["models"]):
                def single(grade):
                    for mm, n in spec["capacity"][grade][i]:
                        if n == 1:
                            return dia(mm)
                    return "—"
                rows.append({"model": m["name"], "family": f["short"], "href": f"{sp['slug']}.html#{f['id']}", "kind": "Cutter" if spec.get("kind") == "cutting" else "Bender",
                             "cap45": single("45"), "cap65": single("65"), "motor": m.get("kw_text") or f"{hp(m['kw'])} ({kw_str(m['kw'])})",
                             "weight": m.get("kg_text") or f"{lb(m['kg'])} ({m['kg']:g} kg)",
                             "voltage": "110/220 V 1-phase" if "110" in (m.get("voltage") or "") else "600 V 3-phase"})
    return rows


def render_page(page):
    page = dict(page)
    if page.get("subpages"):  # hub: resolve each sub-page's families and derive groups for the quote form / structured data
        for sp in page["subpages"]:
            sp["families"] = [prepare_family(family(page, fid)) for fid in sp["families"]]
            sp["href"] = sp["slug"] + ".html"
        page["groups"] = [{"id": sp["slug"], "title": sp["title"], "families": sp["families"]} for sp in page["subpages"]]
        page["range_rows"] = range_table(page["subpages"])
    for g in page.get("groups", []):
        g["families"] = [prepare_family(family(page, f)) if isinstance(f, str) else f for f in g["families"]]
    if not page.get("jump_links") and page.get("groups") and not page.get("subpages"):
        page["jump_links"] = [{"href": "#" + f["id"], "label": f["short"]} for g in page["groups"] for f in g["families"]] + [{"href": "#reques-a-quote", "label": "Request a quote"}]
    page["url"] = f"{site['domain']}/{page['slug']}.html"
    tpl = env.get_template(page.get("template", "page.html"))
    return tpl.render(page=page, ld_json=page_ld(page), build_ts=int(datetime.datetime.now().timestamp()),
                      css_hash=asset_hash(os.path.join(ROOT, "src", "css", "site.css")), js_hash=asset_hash(os.path.join(ROOT, "src", "js", "site.js")))


def artifact_fragment(html, page):
    """Strip the document skeleton (the artifact host adds its own) and add a preview banner."""
    html = re.sub(r"<!DOCTYPE html>\s*", "", html)
    html = re.sub(r"<html[^>]*>|</html>|<head>|</head>|<body>|</body>", "", html)
    html = re.sub(r'<meta charset="utf-8">\s*|<meta name="viewport"[^>]*>\s*', "", html)
    html = re.sub(r"<title>.*?</title>", "<title>" + page.get("artifact_title", page["h1"]) + "</title>", html, count=1, flags=re.S)
    banner = ('<div class="preview-note"><div class="wrap">Preview of the new NovoTechMachineTools.com page. '
              'Video playback, the PDF download and the quote form only work on the live site.</div></div>\n')
    html = html.replace('<a class="skip"', banner + '<a class="skip"', 1)
    return html.strip() + "\n"


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    # static assets (CSS and JS are minified on the way)
    for sub in ("css", "js", "fonts", "img", "files"):
        s = os.path.join(ROOT, "src", sub)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(DIST, sub))
    try:
        import rcssmin, rjsmin
        for fn in os.listdir(os.path.join(DIST, "css")):
            if fn.endswith(".css"):
                fp = os.path.join(DIST, "css", fn); src = open(fp, encoding="utf-8").read(); open(fp, "w", encoding="utf-8").write(rcssmin.cssmin(src))
        for fn in os.listdir(os.path.join(DIST, "js")):
            if fn.endswith(".js"):
                fp = os.path.join(DIST, "js", fn); src = open(fp, encoding="utf-8").read(); open(fp, "w", encoding="utf-8").write(rjsmin.jsmin(src))
    except ImportError:
        print("rcssmin/rjsmin not installed - shipping unminified CSS/JS")
    for extra in ("robots.txt", "llms.txt", ".htaccess", "quote.php", "favicon.ico", "favicon.svg", "site.webmanifest"):
        s = os.path.join(ROOT, "src", "root", extra)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(DIST, extra))
    pages = []
    pdir = os.path.join(ROOT, "content", "pages")
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        page = json.load(open(os.path.join(pdir, fn), encoding="utf-8"))
        html = render_page(page)
        if ARTIFACT:
            html = artifact_fragment(html, page)
        out = os.path.join(DIST, page["slug"] + ".html")
        open(out, "w", encoding="utf-8").write(html)
        pages.append(page)
        print(f"wrote {out} ({len(html)//1024} KB)")
    # sitemap
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{site['domain']}/{p['slug']}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{'0.9' if p.get('subpages') else '0.8'}</priority></url>\n" for p in pages)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    if STAGING:
        open(os.path.join(DIST, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("done", "(staging)" if STAGING else "")


if __name__ == "__main__":
    main()
