#!/usr/bin/env python3
"""NovoTech static site generator.

    python3 build.py            -> writes the whole site to dist/
    python3 build.py --staging  -> same, but with <meta name=robots content=noindex> for the test host

Content lives in content/, templates in templates/, static assets in src/.
"""
import json, os, re, shutil, sys, datetime, hashlib
import html as html_mod
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
STAGING = "--staging" in sys.argv
ARTIFACT = "--artifact" in sys.argv   # claude.ai artifact preview: page fragment, no doc skeleton
if ARTIFACT:
    DIST = os.path.join(ROOT, "dist-artifact")

site = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
if STAGING:
    # absolute URLs (canonical, og:url, og:image, structured data) point at the test host while testing
    site["domain"] = site.get("staging_domain", site["domain"])
manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
image_map = json.load(open(os.path.join(ROOT, "tools", "image_map.json"), encoding="utf-8"))   # alt text edits apply without re-encoding

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


# ---------------------------------------------------------------- band saws
from fractions import Fraction

def inch_frac(mm, denom=8):
    """270 -> '10-5/8″' (nearest 1/denom inch)."""
    v = mm / 25.4
    whole = int(v); fr = Fraction(round((v - whole) * denom), denom)
    if fr == 1:
        whole += 1; fr = Fraction(0)
    if fr == 0:
        return f"{whole}″"
    return (f"{whole}-" if whole else "") + f"{fr.numerator}/{fr.denominator}″"


def rng(s, conv, unit_i, unit_m, nd=0):
    """'15-120' m/min -> '49–394 ft/min (15–120 m/min)'; single numbers too.
    Step speeds '35/60/88/115' -> '115/197/289/377 ft/min (35/60/88/115 m/min)'."""
    if s is None:
        return "—"
    fmt = (lambda x: f"{x:,.{nd}f}") if nd else (lambda x: f"{round(x):,}")
    if "/" in str(s):
        parts = [p.strip() for p in str(s).split("/") if p.strip()]
        try:
            nums = [float(p.replace(",", ".")) for p in parts]
        except ValueError:
            return str(s)
        return "/".join(fmt(conv(n)) for n in nums) + f" {unit_i} (" + "/".join(f"{n:g}" for n in nums) + f" {unit_m})"
    parts = [p.strip() for p in str(s).replace("–", "-").split("-") if p.strip()]
    try:
        nums = [float(p.replace(",", ".")) for p in parts]
    except ValueError:
        return str(s)
    a = "–".join(fmt(conv(n)) for n in nums)
    m = "–".join(f"{n:g}" for n in nums)
    return f"{a} {unit_i} ({m} {unit_m})"


def hp_range(kw):
    if kw is None:
        return "—"
    parts = [p.strip() for p in str(kw).replace("–", "-").split("-") if p.strip()]
    try:
        nums = [float(p.replace(",", ".")) for p in parts]
    except ValueError:
        return str(kw)
    h = "–".join(hp(n).replace(" HP", "") for n in nums)
    return f"{h} HP ({'–'.join(f'{n:g}' for n in nums)} kW)"


ANGLE_ORDER = ["0", "+15", "+30", "+45", "+60", "-30", "-45", "-60"]


def build_bandsaw_table(spec):
    models = spec["models"]
    names = [m["name"] for m in models]
    rows = []
    angles = []
    for m in models:
        for a in (m.get("capacity_mm") or {}):
            if a not in angles:
                angles.append(a)
    angles.sort(key=lambda a: ANGLE_ORDER.index(a) if a in ANGLE_ORDER else 99)
    def ang_label(a):
        return "0° (straight)" if a == "0" else (a.replace("+", "+") + "°" + (" right" if a.startswith("+") else " left"))
    for a in angles:
        for key, lab in (("round", "round"), ("rect", "rectangular W × H"), ("square", "square")):
            cells = []
            any_val = False
            for m in models:
                c = (m.get("capacity_mm") or {}).get(a) or {}
                v = c.get(key)
                if v is None:
                    cells.append("—"); continue
                any_val = True
                if key == "rect":
                    cells.append(f"{inch_frac(v[0])} × {inch_frac(v[1])} ({v[0]:g} × {v[1]:g} mm)")
                else:
                    cells.append(("Ø" if key == "round" else "") + f"{inch_frac(v)} ({v:g} mm)")
            if any_val:
                rows.append({"label": f"Capacity {ang_label(a)} — {lab}", "cells": cells, "type": "text", "cap": key == "round" and a == "0"})
    rows.append({"label": "Blade speed", "cells": [rng(m.get("blade_speed_m_min"), lambda x: x * 3.2808, "ft/min", "m/min") for m in models], "type": "text"})
    def band(m):
        bd = m.get("band_mm")
        if not bd:
            return "—"
        L, W, T = bd
        Wi = inch_frac(W, 8) if isinstance(W, (int, float)) else str(W)
        Ti = f"{T / 25.4:.3f}" if isinstance(T, (int, float)) else str(T)
        if L is None:  # width × thickness only
            return f"{Wi.replace('″', '')} × {Ti} in ({W} × {T} mm)"
        return f"{inch_frac(L, 2).replace('″', '')} × {Wi.replace('″', '')} × {Ti} in ({L:g} × {W} × {T} mm)"
    rows.append({"label": "Band blade L × W × T", "cells": [band(m) for m in models], "type": "text"})
    rows.append({"label": "Main motor", "cells": [hp_range(m.get("main_motor_kw")) for m in models], "type": "text"})
    if any(m.get("hydraulic_motor_kw") for m in models):
        rows.append({"label": "Hydraulic motor", "cells": [hp_range(m.get("hydraulic_motor_kw")) if m.get("hydraulic_motor_kw") else "—" for m in models], "type": "text"})
    if any(m.get("coolant_pump_kw") for m in models):
        rows.append({"label": "Coolant pump", "cells": [hp_range(m.get("coolant_pump_kw")) if m.get("coolant_pump_kw") else "—" for m in models], "type": "text"})
    extras = {}
    for m in models:
        for k, v in (m.get("other") or {}).items():
            extras.setdefault(k, {})[m["name"]] = v
    late = {k: v for k, v in extras.items() if re.search(r"weight|packing", k, re.I)}

    def conv(v):
        mm = re.match(r"^\s*([\d.,]+)\s*kW", str(v))
        if mm:
            return hp_range(mm.group(1).replace(",", "."))
        mm = re.match(r"^\s*([\d.,]+)\s*kg\s*$", str(v))
        if mm:
            x = float(mm.group(1).replace(",", ".")); return f"{lb(x)} ({x:g} kg)"
        mm = re.match(r"^\s*([\d.,]+)\s*mm\s*$", str(v))
        if mm:
            x = float(mm.group(1).replace(",", ".")); return f"{inch_frac(x)} ({x:g} mm)"
        # '2300 × 830 × 1580 mm' (possibly several, separated by commas) -> inches + mm
        def dims3(mt):
            d = [float(t) for t in mt.group(1).replace("×", "x").split("x")]
            return " × ".join(str(round(t / 25.4)) for t in d) + " in (" + " × ".join(f"{t:g}" for t in d) + " mm)"
        if re.search(r"\d+\s*[×x]\s*\d+\s*[×x]\s*\d+\s*mm", str(v)):
            return re.sub(r"(\d+(?:\s*[×x]\s*\d+){2})\s*mm", dims3, str(v))
        return str(v)

    for k, vals in extras.items():
        if k in late:
            continue
        rows.append({"label": k, "cells": [conv(vals[m["name"]]) if m["name"] in vals else "—" for m in models], "type": "text"})
    if any(m.get("working_height_mm") for m in models):
        rows.append({"label": "Working height", "cells": [f"{inch_frac(m['working_height_mm'], 2)} ({m['working_height_mm']:g} mm)" if m.get("working_height_mm") else "—" for m in models], "type": "text"})
    rows.append({"label": "Weight", "cells": [f"{lb(m['weight_kg'])} ({m['weight_kg']:g} kg)" if m.get("weight_kg") else "—" for m in models], "type": "text"})
    for k, vals in late.items():
        rows.append({"label": k, "cells": [conv(vals[m["name"]]) if m["name"] in vals else "—" for m in models], "type": "text"})
    def dims_mm(d):
        if not d:
            return "—"
        return " × ".join(str(round(x / 25.4)) for x in d) + " in (" + " × ".join(f"{x:g}" for x in d) + " mm)"
    if any(m.get("dims_mm") for m in models):
        rows.append({"label": "Dimensions L × W × H", "cells": [dims_mm(m.get("dims_mm")) for m in models], "type": "text"})
    rows.append({"label": "Voltage", "cells": [spec.get("voltage", "600 V 3-phase (208/240/480 V on request)") for m in models], "type": "text"})
    return {"models": names, "rows": rows}


def bandsaw_round0(m):
    try:
        return m["capacity_mm"]["0"]["round"] or 0
    except (KeyError, TypeError):
        return 0


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
        "alt": image_map.get(name, {}).get("alt") or e["alt"],
        "src": largest["file"],
        "w": largest["w"], "h": largest["h"],
        "srcset": ", ".join(f"{x['file']} {x['w']}w" for x in v),
        "small": v[0]["file"],
        "thumb": (e.get("thumb") or v[0])["file"],
        "alpha": e["alpha"],
    }


# ---------------------------------------------------------------- jinja
env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
def nav_contains(item, slug):
    """True when the page `slug` is this nav item or anywhere in its sub-tree."""
    if (item.get("href") or "").split("#")[0] == slug + ".html":
        return True
    return any(nav_contains(c, slug) for c in item.get("children", []))


def nav_is(item, slug):
    return (item.get("href") or "").split("#")[0] == slug + ".html" and "#" not in (item.get("href") or "")


env.globals.update(site=site, img=img, staging=STAGING, year=datetime.date.today().year, dia=dia, inch=inch, bar_sizes=bar_sizes,
                   nav_contains=nav_contains, nav_is=nav_is)


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
        "description": site["founded_note"],
        "address": {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"], "addressRegion": a["region"], "postalCode": a["postal"], "addressCountry": "CA"},
        "geo": {"@type": "GeoCoordinates", "latitude": site["geo"]["lat"], "longitude": site["geo"]["lng"]},
        "areaServed": {"@type": "Country", "name": "Canada"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}],
        "sameAs": [x["url"] for x in site.get("social", []) if x.get("url")],
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
            purl = (absurl(g["id"]) if page.get("subpages") else url) + "#" + f["id"]
            gal = f.get("gallery") or []
            models = [m["name"] for m in (f.get("specs") or {}).get("models", [])] or [s.strip() for s in f.get("models_label", "").split("·") if s.strip()]
            fb = site.get("brands", {}).get(f.get("brand"), {}) or brand
            prod = {
                "@type": "Product", "@id": purl, "url": purl,
                "name": f["name"], "description": f["summary"],
                "image": [absurl(i["src"]) for i in gal[:6]],
                "brand": {"@type": "Brand", "name": fb.get("name", "")},
                **({"manufacturer": {"@type": "Organization", "name": fb["manufacturer"], "address": {"@type": "PostalAddress", "addressCountry": fb.get("country_code", "TR")}}} if fb.get("manufacturer") else {}),
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


def model_single(spec, i, key="capacity", grade="45"):
    """Largest single-bar diameter (mm) of model i, or 0."""
    for mm, n in spec.get(key, {}).get(grade, [[]] * (i + 1))[i]:
        if n == 1:
            return mm
    return 0


def caption_for(f, alt):
    """Two caption lines for a gallery photo: 'B 36 · bends up to Ø1-3/8″ (36 mm)' and the photo description."""
    caps = {}
    spec = f.get("specs")
    if spec and spec.get("kind") == "bandsaw":
        for m in spec["models"]:
            r = bandsaw_round0(m)
            rect = ((m.get("capacity_mm") or {}).get("0") or {}).get("rect")
            parts = []
            if r: parts.append(f"cuts Ø{inch_frac(r)} ({r:g} mm) round")
            if rect: parts.append(f"{inch_frac(rect[0])} × {inch_frac(rect[1])} ({rect[0]:g} × {rect[1]:g} mm)")
            caps[m["name"]] = " · ".join(parts)
    elif spec:
        verb = "cuts" if spec.get("kind") == "cutting" else "bends"
        for i, m in enumerate(spec["models"]):
            parts = []
            mm = model_single(spec, i)
            if mm:
                parts.append(f"{verb} up to {dia(mm)}")
            cmm = model_single(spec, i, "cutting_capacity")
            if cmm:
                parts.append(f"cuts up to {dia(cmm)}")
            caps[m["name"]] = " · ".join(parts)
    caps.update(f.get("model_caps") or {})
    for name in sorted(caps, key=len, reverse=True):           # longest model name first: "MG 26 Junior" before "MG 26"
        if re.search(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", alt):
            return f"{name} · {caps[name]}" if caps[name] else name, alt
    head = f.get("headline", "")
    return f"{f['short']} · {head[0].lower() + head[1:]}" if head else f["short"], alt


def prepare_family(f):
    if f.get("specs") and f["specs"].get("kind") == "table":
        # generic spec kind: the data generator supplies finished tables (cells already "imperial (metric)")
        f["tables"] = f["specs"]["tables"]
        f["headline"] = f.get("headline") or f["specs"].get("headline", "")
        f["model_caps"] = {**(f["specs"].get("caps") or {}), **(f.get("model_caps") or {})}
    elif f.get("specs") and f["specs"].get("kind") == "bandsaw":
        f["table"] = build_bandsaw_table(f["specs"])
        rounds = [bandsaw_round0(m) for m in f["specs"]["models"]]
        f["max_mm"] = max(rounds) if rounds else 0
        lo = min(r for r in rounds if r) if any(rounds) else 0
        f["headline"] = f.get("headline") or (f"Round capacity Ø{inch_frac(lo)} – Ø{inch_frac(f['max_mm'])} ({lo:g}–{f['max_mm']:g} mm)" if lo != f["max_mm"] else f"Round capacity Ø{inch_frac(f['max_mm'])} ({f['max_mm']:g} mm)")
    elif f.get("specs"):
        f["table"] = build_spec_table(f["specs"])
        f["max_mm"] = max_single_bar(f["specs"])
        kind = "Cuts" if f["specs"].get("kind") == "cutting" else "Bends"
        f["headline"] = f.get("headline") or f"{kind} single bars to {dia(f['max_mm'])}"
    f["gallery"] = [img(n) for n in f.get("images", [])]
    for im in f["gallery"]:
        im["cap1"], im["cap2"] = caption_for(f, im["alt"])
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
            if spec.get("kind") == "table":
                for m in spec["models"]:
                    rows.append({"model": m["name"], "family": f["short"], "href": f"{sp['slug']}.html#{f['id']}", "kind": sp.get("nav_label") or sp["title"],
                                 "cols": m.get("glance", []), "line": ""})
                continue
            if spec.get("kind") == "bandsaw":
                for m in spec["models"]:
                    r = bandsaw_round0(m)
                    rect = ((m.get("capacity_mm") or {}).get("0") or {}).get("rect")
                    rows.append({"model": m["name"], "family": f["short"], "href": f"{sp['slug']}.html#{f['id']}", "line": "Premium · Bekamak" if f.get("line") == "premium" else "Value · NovoTech",
                                 "kind": sp.get("nav_label") or sp["title"], "round": f"Ø{inch_frac(r)} ({r:g} mm)" if r else "—",
                                 "rect": f"{inch_frac(rect[0])} × {inch_frac(rect[1])} ({rect[0]:g} × {rect[1]:g} mm)" if rect else "—",
                                 "motor": hp_range(m.get("main_motor_kw")), "weight": f"{lb(m['weight_kg'])} ({m['weight_kg']:g} kg)" if m.get("weight_kg") else "—"})
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


PREPARED = []   # prepared page dicts (families resolved) — used for the AI assistant's catalogue


def render_page(page):
    page = dict(page)
    if page.get("subpages"):  # hub: resolve each sub-page's families and derive groups for the quote form / structured data
        for sp in page["subpages"]:
            sp["families"] = [prepare_family(family(page, fid)) for fid in sp["families"]]
            sp["has_videos"] = any(f.get("videos") for f in sp["families"])
            sp["href"] = sp["slug"] + ".html"
        page["groups"] = [{"id": sp["slug"], "title": sp["title"], "families": sp["families"]} for sp in page["subpages"]]
        if page.get("lines"):   # two product lines, each with its own sub-pages and range table
            by_slug = {sp["slug"]: sp for sp in page["subpages"]}
            for ln in page["lines"]:
                ln["subpages"] = [by_slug[sp["slug"]] for sp in ln["subpages"]]
                ln["range_rows"] = range_table(ln["subpages"])
                ln["brand_info"] = site["brands"].get(ln["brand"], {})
        page["range_rows"] = range_table(page["subpages"])
        if page.get("range_groups"):   # e.g. rebar hub: benders and cutters in separate tables
            for rg in page["range_groups"]:
                rg["rows"] = [row for row in page["range_rows"] if row.get("kind") == rg["kind"]]
    for g in page.get("groups", []):
        g["families"] = [prepare_family(family(page, f)) if isinstance(f, str) else f for f in g["families"]]
    if not page.get("jump_links") and page.get("groups") and not page.get("subpages"):
        page["jump_links"] = [{"href": "#" + f["id"], "label": f["short"]} for g in page["groups"] for f in g["families"]] + [{"href": "#reques-a-quote", "label": "Request a quote"}]
    page["url"] = f"{site['domain']}/{page['slug']}"      # clean URLs: pages are served without .html
    if page.get("article"):   # long-form guide kept from the old site (HTML fragment with <figure data-img> placeholders)
        art = open(os.path.join(ROOT, "content", "articles", page["article"]), encoding="utf-8").read()
        def fig(m):
            im = img(m.group(1))
            alt = html_mod.escape(m.group(2)) if m.group(2) else im["alt"]
            cls = "guide-figure is-cutout" if im.get("alpha") else "guide-figure"
            return (f'<figure class="{cls}"><img src="{im["small"]}" srcset="{im["srcset"]}" sizes="(max-width: 700px) 92vw, 760px" '
                    f'width="{im["w"]}" height="{im["h"]}" alt="{alt}" loading="lazy" decoding="async"></figure>')
        art = re.sub(r'<figure class="guide-figure" data-img="([^"]+)"(?: data-alt="([^"]*)")?></figure>', fig, art)
        page["article_html"] = art
        page["article_toc"] = [{"id": i, "label": re.sub(r"<[^>]+>", "", t)} for i, t in re.findall(r'<section class="guide-section" id="([^"]+)">\s*<h3>(.*?)</h3>', art)]
    tpl = env.get_template(page.get("template", "page.html"))
    inline_css = None if ARTIFACT else open(os.path.join(DIST, "css", "site.css"), encoding="utf-8").read().replace("../fonts/", "fonts/")   # minified by main(); URLs re-based to the page
    html = tpl.render(page=page, ld_json=page_ld(page), build_ts=int(datetime.datetime.now().timestamp()), inline_css=inline_css,
                      css_hash=asset_hash(os.path.join(ROOT, "src", "css", "site.css")), js_hash=asset_hash(os.path.join(ROOT, "src", "js", "site.js")),
                      ai_hash=asset_hash(os.path.join(ROOT, "src", "js", "ai.js")))
    PREPARED.append(page)
    return clean_urls(html)


def ai_catalogue(pages):
    """Compact machine catalogue for the AI assistant (dist/ai/catalogue.json): one entry per family,
    with the page it lives on, its models and their headline capacities in inches and mm."""
    items = []
    seen = set()
    for page in pages:
        if page.get("subpages"):
            continue   # hubs repeat the families of their sub-pages
        for g in page.get("groups", []):
            for f in g["families"]:
                if f["id"] in seen:
                    continue
                seen.add(f["id"])
                spec = f.get("specs") or {}
                models = []
                for i, m in enumerate(spec.get("models", [])):
                    entry = {"name": m["name"]}
                    if spec.get("kind") == "table":
                        for k, v in zip(spec.get("glance_keys", []), m.get("glance", [])):
                            entry[k] = v
                    elif spec.get("kind") == "bandsaw":
                        r = bandsaw_round0(m)
                        rect = ((m.get("capacity_mm") or {}).get("0") or {}).get("rect")
                        angles = [a for a in (m.get("capacity_mm") or {}) if a != "0"]
                        entry["round_capacity"] = f"Ø{inch_frac(r)} ({r:g} mm)" if r else None
                        entry["rectangular_capacity"] = f"{inch_frac(rect[0])} × {inch_frac(rect[1])} ({rect[0]:g} × {rect[1]:g} mm)" if rect else None
                        entry["miter_angles"] = [a.replace("+", "+") + "°" for a in angles] or None
                        entry["motor"] = hp_range(m.get("main_motor_kw"))
                        entry["blade_speed"] = rng(m.get("blade_speed_m_min"), lambda x: x * 3.2808, "ft/min", "m/min")
                        if m.get("feed_length_mm"):
                            entry["feed_per_stroke"] = f"{inch_frac(m['feed_length_mm'])} ({m['feed_length_mm']:g} mm)"
                    else:
                        mm = model_single(spec, i)
                        if mm:
                            entry["max_single_bar"] = dia(mm)
                        cmm = model_single(spec, i, "cutting_capacity")
                        if cmm:
                            entry["cutting_capacity"] = dia(cmm)
                        if m.get("kw") or m.get("kw_text"):
                            entry["motor"] = m.get("kw_text") or f"{hp(m['kw'])} ({kw_str(m['kw'])})"
                        if m.get("voltage"):
                            entry["voltage"] = m["voltage"]
                    models.append({k: v for k, v in entry.items() if v})
                thumb = f["gallery"][0]["thumb"] if f.get("gallery") and f["gallery"][0].get("thumb") else (f["gallery"][0]["small"] if f.get("gallery") else None)
                brand = site.get("brands", {}).get(f.get("brand"), {})
                items.append({
                    "id": f["id"], "name": f["name"], "short": f["short"], "models_label": f.get("models_label", ""),
                    "brand": brand.get("name") or (page.get("brand") or {}).get("name", ""), "line": brand.get("line"),
                    "category": g["title"], "page_title": page["h1"], "page": page["slug"], "href": f"{page['slug']}#{f['id']}",
                    "headline": f.get("headline", ""), "summary": f.get("summary", ""), "features": f.get("features", [])[:7],
                    "automation": f.get("group"), "models": models, "image": thumb,
                })
    return items


def clean_urls(html):
    """Internal page links without the .html extension (the server maps /page to page.html)."""
    html = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', lambda m: f'href="{m.group(1)}{m.group(2) or ""}"', html)
    html = re.sub(r'href="index"', 'href="./"', html)
    dom = re.escape(site["domain"])
    html = re.sub(dom + r'/([a-z0-9-]+)\.html(?=[#"\s<\\])', lambda m: f'{site["domain"]}/{m.group(1)}', html)
    return external_links_new_tab(html)


def external_links_new_tab(html):
    """Every link to another website opens in a new tab (target=_blank + rel=noopener)."""
    own = {re.sub(r"^https?://", "", site["domain"]).lower(), "novotechmachinetools.com", "www.novotechmachinetools.com"}
    def fix(m):
        tag = m.group(0)
        href = re.search(r'href="(https?://[^"/]+)', tag)
        if not href:
            return tag
        host = re.sub(r"^https?://", "", href.group(1)).lower()
        if host in own or 'target=' in tag:
            return tag
        rel = re.search(r'rel="([^"]*)"', tag)
        if rel:
            vals = rel.group(1).split()
            if "noopener" not in vals:
                vals.append("noopener")
            tag = tag.replace(rel.group(0), 'rel="' + " ".join(vals) + '"')
        else:
            tag = tag[:-1] + ' rel="noopener">'
        return tag[:-1] + ' target="_blank">'
    return re.sub(r'<a\s[^>]*href="https?://[^"]*"[^>]*>', fix, html)


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
    for extra in ("robots.txt", "llms.txt", ".htaccess", "quote.php", "ask.php", "ai-config.sample.php", "favicon.ico", "favicon.svg", "site.webmanifest"):
        s = os.path.join(ROOT, "src", "root", extra)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(DIST, extra))
    pages = []
    pdir = os.path.join(ROOT, "content", "pages")
    loaded = [json.load(open(os.path.join(pdir, fn), encoding="utf-8")) for fn in sorted(os.listdir(pdir)) if fn.endswith(".json") and not fn.startswith("_")]
    # every page of a hub's section gets links to the hub and to its sibling pages (cross-linking the benders / cutters / lines pages)
    for hub in [p for p in loaded if p.get("subpages")]:
        def member(sp):
            return {"href": sp["slug"] + ".html", "slug": sp["slug"], "label": sp.get("nav_label") or sp["title"], "blurb": sp.get("blurb", ""), "image": img(sp["image"]) if sp.get("image") else None, "cat": sp.get("cat")}
        groups = [{"label": None, "members": [member(sp) for sp in hub["subpages"]]}]
        if hub.get("lines"):
            groups = [{"label": ln.get("short") or ln["name"], "line": ln["id"], "brand": ln["brand"], "members": [member(sp) for sp in ln["subpages"]]} for ln in hub["lines"]]
        hub_info = {"href": hub["slug"] + ".html", "label": hub.get("nav_label") or hub["h1"], "image": img(hub["hero_image"]) if hub.get("hero_image") else None, "blurb": hub.get("related_blurb", "")}
        for p in loaded:
            for g in groups:
                if any(m["slug"] == p["slug"] for m in g["members"]):
                    me = next(m for m in g["members"] if m["slug"] == p["slug"])
                    alt = None
                    if len(groups) > 1:
                        og = next(x for x in groups if x is not g)
                        alt_m = next((m for m in og["members"] if m.get("cat") == me.get("cat")), None)
                        alt = dict(alt_m, line_label=og["label"], line=og.get("line"), brand=og.get("brand")) if alt_m else None
                    p["section"] = {"hub": hub_info, "label": (g["label"] + " band saws") if g.get("label") else hub.get("section_label", "Rebar machinery"),
                                    "line": g.get("line"), "brand": g.get("brand"), "line_name": g.get("label"),
                                    "pages": [dict(m, current=(m["slug"] == p["slug"])) for m in g["members"]], "alt": alt,
                                    "related_title": hub.get("related_title_" + (g.get("line") or ""), None)}
                    covered = {m["href"] for m in g["members"]} | {hub["slug"] + ".html"} | ({alt["href"]} if alt else set())
                    p["related_pages"] = [r for r in p.get("related_pages", []) if r["href"] not in covered]   # cards already link to these
    for page in loaded:
        html = render_page(page)
        if ARTIFACT:
            html = artifact_fragment(html, page)
        out = os.path.join(DIST, page["slug"] + ".html")
        open(out, "w", encoding="utf-8").write(html)
        pages.append(page)
        print(f"wrote {out} ({len(html)//1024} KB)")
    # AI assistant catalogue (read by ask.php on the server and by the search panel in the browser)
    os.makedirs(os.path.join(DIST, "ai"), exist_ok=True)
    cat = ai_catalogue(PREPARED)
    json.dump({"generated": datetime.date.today().isoformat(), "site": site["domain"], "families": cat},
              open(os.path.join(DIST, "ai", "catalogue.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"ai catalogue: {len(cat)} families, {os.path.getsize(os.path.join(DIST, 'ai', 'catalogue.json'))//1024} KB")
    # sitemap
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{site['domain']}/{p['slug']}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{'0.9' if p.get('subpages') else '0.8'}</priority></url>\n" for p in pages)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    if STAGING:
        open(os.path.join(DIST, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("done", "(staging)" if STAGING else "")


if __name__ == "__main__":
    main()
