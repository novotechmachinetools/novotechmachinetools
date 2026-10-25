#!/usr/bin/env python3
"""Band saw blades page (band-saw-blades.html): WIKUS metal-cutting band saw blades — bimetal, carbide-tipped and CBN-coated.

Source: tools/wikus/products.json, the product pages of wikus.de/en/products/band-saw-blades scraped in the browser
(text blocks and tables per product; photos in /home/claude/wikus/img, data sheets in /home/claude/wikus/pdf).  Only the
metal-cutting blades are used: the DIAGRIT (glass, stone, ceramics), TCGRIT (tyres, cables, composites) and TCTYRE
blades, and the wood-cutting GENERO, are left out.  Sizes are shown inch (mm) as WIKUS gives them; tooth pitches in TPI.

    python3 tools/wikus_pages.py        # families + page + image_map entries (tools/wikus_keys.txt) + data sheets
    python3 tools/make_images.py --only $(cat tools/wikus_keys.txt)
"""
import json
import os
import re
import shutil

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_IMG = "/home/claude/wikus/img/"
SRC_PDF = "/home/claude/wikus/pdf/"
SET = "band-saw-blades"
P_BLADES = "band-saw-blades"
BRAND = "wikus"
SECTION = "Band saw blades"
NOISE = {"has been added to the watchlist.", "has been removed from the watchlist."}

# product order within the groups: small to large by product level, then the width range
GROUPS = [
    ("bimetal-m42", "Bimetal band saw blades — M42", "The workhorses of the saw shop: an M42 high-speed-steel cutting edge welded to a spring-steel back, from the economical PRIMAR to the SKALAR and SELEKTA GS production blades — profiles and solid material to 1,000 N/mm² (145,000 psi).",
     ["primar-m42", "marathon-m42", "marathon-sw-m42", "proflex-m42", "proflex-sw-m42", "skalar-m42", "selekta-gs-m42"]),
    ("bimetal-premium", "Bimetal band saw blades — M42 with hard coating", "The PREMIUM versions: the same M42 blades with a hard coating on the teeth for the highest cutting rates and blade life on profiles and solid material.",
     ["proflex-premium-m42", "proflex-premium-sw-m42", "skalar-premium-m42"]),
    ("bimetal-x3000", "Bimetal band saw blades — X3000®", "WIKUS's own X3000® cutting material: higher hardness and toughness than M42 for difficult-to-machine materials and special alloys.",
     ["marathon-x3000", "skalar-x3000", "selekta-gs-x3000"]),
    ("carbide", "Carbide-tipped band saw blades", "Carbide teeth on an alloyed spring-steel back for production sawing of solid material: from the entry-level TAURUS and MARADUR to the FUTURA family, the NE blades for non-ferrous metals and the specialists for hardened and case-hardened parts.",
     ["taurus", "maradur", "duroset", "ecodur", "duroset-ne", "futura", "futura-va", "futura-718", "futura-ne", "futura-ne-rs", "futura-sn", "tct"]),
    ("carbide-premium", "Carbide-tipped band saw blades with hard coating", "Coated carbide teeth for the highest performance when the saw is the bottleneck: the PREMIUM versions of TAURUS, DUROSET and FUTURA, the PROFIDUR for profiles and the ARION FG for large solid material.",
     ["taurus-premium", "duroset-premium", "futura-premium", "profidur", "futura-premium-va", "arion-fg", "futura-premium-sn"]),
    ("cbn", "CBN-coated band saw blades for hardened steel", "CUBOGRIT® blades with a cubic boron nitride grit edge: cutting hardened HSS, tool steels above 55 HRC, stellite and chilled castings that no toothed blade can cut.",
     ["cubogrit-k", "cubogrit-s", "cubogrit-u"]),
]
ORDER = [s for g in GROUPS for s in g[3]]
GROUP_OF = {s: g[0] for g in GROUPS for s in g[3]}


def load():
    return {e["url"].split("/")[-1]: e for e in json.load(open(os.path.join(ROOT, "tools", "wikus", "products.json"), encoding="utf-8"))}


def parse(e):
    b = [x for x in e["blocks"] if x["t"] == "TABLE" or x["x"] not in NOISE]
    slug = e["url"].split("/")[-1]
    i = next(k for k, x in enumerate(b) if x["t"] == "H1")
    name = b[i]["x"]
    tagline = b[i + 1]["x"] if b[i + 1]["t"] == "P" else ""
    hdr = [x["x"] for x in b[i + 1:i + 9] if x["t"] == "LI"]
    level = next((h.split()[-1] for h in hdr if h.lower().startswith("product level")), "")
    tooth = next((h for h in hdr if "tooth" in h.lower() or h.startswith("Tooth shape")), "")
    appl = next((h for h in hdr if h.startswith(("Solid", "Profiles"))), "")
    band = next((h for h in hdr if h.startswith(("Band w", "Band thickness"))), "")
    coating = next((h for h in hdr if "coating" in h.lower()), "")
    size_class = next((h for h in hdr if h.startswith("Workpiece dimension")), "")
    ds = next(k for k, x in enumerate(b) if x["t"] == "LI" and x["x"] == "Download Data Sheet")
    ar = next((k for k, x in enumerate(b) if k > ds and ((x["t"] in ("H2", "H3") and x["x"].startswith(("Application", "Areas of Application"))) or x["t"] == "TABLE")), len(b))
    desc = []
    for k, x in enumerate(b[ds + 1:ar], ds + 1):
        if x["t"] == "P" and len(x["x"]) > 40 and not (b[k - 1]["t"] == "LI" and b[k - 1]["x"] == x["x"]):
            desc.append(x["x"])
    dim_i = next((k for k, x in enumerate(b) if x["t"] == "TABLE"), len(b))
    sections = {"application": [], "advantages": [], "features": []}
    cur = None
    for k, x in enumerate(b[ar:dim_i], ar):
        t = x["x"].lower().rstrip(":") if x["t"] != "TABLE" else ""
        if x["t"] in ("H2", "H3", "P") and t in ("application", "applications", "areas of application", "application range"):
            cur = "application"
        elif x["t"] in ("H3", "P") and t == "advantages":
            cur = "advantages"
        elif x["t"] in ("H3", "P") and t == "features":
            cur = "features"
        elif x["t"] == "H3" and t.startswith(("qr", "dimensions", "tooth pitch")):
            cur = None
        elif x["t"] == "LI" and cur and x["x"] not in sections[cur]:
            sections[cur].append(x["x"])
    tables = [x for x in b if x["t"] == "TABLE"]
    dsheet = next((k for k, x in enumerate(b) if x["t"] == "H2" and x["x"].startswith("Product data sheet")), len(b))
    t_end = max((k for k, x in enumerate(b) if x["t"] == "TABLE"), default=None)
    materials = [x["x"] for x in b[t_end + 1:dsheet] if x["t"] == "LI"] if t_end is not None else []
    dims = [r for r in tables[0]["rows"] if len(r) == 2 and re.match(r"^[\d.]+ x [\d.]+$", r[0])] if tables else []
    pitch = tables[1]["rows"] if len(tables) > 1 else None
    return dict(slug=slug, name=name, tagline=tagline, level=level, tooth=tooth, appl=appl, band=band, coating=coating, size_class=size_class,
                desc=desc, **sections, materials=materials, dims=dims, pitch=pitch, img=e["img_name"], pdf=e["pdf_name"])


def inch_size(mm, inch):
    """'13 x 0.65', '1/2 x 0.025' → '1/2 × 0.025″ (13 × 0.65 mm)'."""
    return f"{inch.replace(' x ', ' × ')}″ ({mm.replace(' x ', ' × ')} mm)"


def contact(cell):
    """'30-601.2-2.4' → '1.2 – 2.4″ (30 – 60 mm)'; '< 5< 0.2' → 'under 0.2″ (5 mm)'."""
    c = cell.replace(" ", "")
    m = re.match(r"^<(\d+)<([\d.]+)$", c)
    if m:
        return f"under {m.group(2)}″ ({m.group(1)} mm)"
    for cut in range(1, len(c)):
        a, bb = c[:cut], c[cut:]
        if re.match(r"^\d+(-\d+)?$", a) and re.match(r"^[\d.]+(-[\d.]+)?$", bb) and "." in bb:
            mm = [float(v) for v in a.split("-")]; ins = [float(v) for v in bb.split("-")]
            if len(mm) == len(ins) and all(abs(i - m_ / 25.4) < 0.35 for i, m_ in zip(ins, mm)):
                return f"{bb.replace('-', ' – ')}″ ({a.replace('-', ' – ')} mm)"
    return cell


def tables_for(p):
    """Dimensions + tooth pitch availability (one row per band size) and the contact-length table."""
    rows = []
    sizes = [inch_size(mm, i) for mm, i in p["dims"]]
    if p["pitch"]:
        pr = p["pitch"]
        labels = pr[1]
        var = [l for l in labels if " - " in l]
        const = [l for l in labels if " - " not in l]
        marks = pr[2:2 + len(sizes)]
        cl = pr[-1] if len(pr) > 2 + len(sizes) else None
        models = ["Variable tooth pitch (TPI)"] + (["Constant tooth pitch (TPI)"] if const else [])
        for s, mk in zip(sizes, marks):
            avail = [l for l, m in zip(labels, mk) if m]
            v = " · ".join(l.replace(" - ", "–") for l in avail if " - " in l) or "—"
            c = " · ".join(l for l in avail if " - " not in l) or "—"
            rows.append({"label": s, "sub": "", "cells": [v] + ([c] if const else []), "key": False})
        t1 = {"title": f"{p['name']} — sizes and tooth pitches", "sub": "Band width × thickness; the tooth pitches available in each size", "models": models, "rows": rows}
        out = [t1]
        if cl and len(cl) == len(labels):
            t2 = {"title": "Workpiece size per tooth pitch", "sub": "Contact length of the cut — choose the pitch so that 4 to 12 teeth are in the material", "models": ["Contact length"],
                  "rows": [{"label": f"{l.replace(' - ', '–')} TPI", "sub": "", "cells": [contact(c)], "key": False} for l, c in zip(labels, cl)]}
            out.append(t2)
        return out
    rows = [{"label": s, "sub": "", "cells": ["✓"], "key": False} for s in sizes]
    return [{"title": f"{p['name']} — sizes", "sub": "Band width × thickness", "models": ["Available"], "rows": rows}]


def band_range(p):
    """'Band width 13 x 0.65 - 80 x 1.6mmBand width 1/2 x 0.025 - 3-1/8 x 0.063 Inch' → ('1/2″ to 3-1/8″', '13 – 80 mm')."""
    m = re.search(r"([\d/\-]+) x [\d.]+ [-–] ([\d/\-]+) x [\d.]+ Inch", p["band"])
    mm = re.search(r"([\d.]+) x [\d.]+ [-–] ([\d.]+) x [\d.]+ ?mm", p["band"])
    return (f"{m.group(1)}″ to {m.group(2)}″" if m else ""), (f"{mm.group(1)} – {mm.group(2)} mm" if mm else "")


KIND = {"bimetal-m42": "bimetal band saw blade", "bimetal-premium": "coated bimetal band saw blade", "bimetal-x3000": "X3000® bimetal band saw blade",
        "carbide": "carbide-tipped band saw blade", "carbide-premium": "coated carbide band saw blade", "cbn": "CBN-coated band saw blade"}
LEVEL = {"1": "product level 1 — entry level", "2": "product level 2 — universal", "3": "product level 3 — high performance", "S": "product level S — specialist"}


def family(p):
    g = GROUP_OF[p["slug"]]
    ins, mm = band_range(p)
    name = f"{p['name']} {KIND[g]}, {ins}"
    glance_pitch = ""
    if p["pitch"]:
        labels = p["pitch"][1]
        glance_pitch = ", ".join(l.replace(" - ", "–") for l in labels) + " TPI"
    summary = " ".join([p["tagline"] + "." if p["tagline"] and not p["tagline"].endswith(".") else p["tagline"]] + p["desc"])[:900].rsplit(". ", 1)[0] + "."
    if len(summary) < 60:
        summary = (p["tagline"] + ". " if p["tagline"] else "") + "Applications: " + "; ".join(p["application"][:4]) + "."
    feats = []
    if p["level"]:
        feats.append(LEVEL.get(p["level"], "product level " + p["level"]))
    if p["tooth"]:
        feats.append(p["tooth"].replace("Tooth shape ", "") + " · " + (p["appl"].replace(" + ", " and ").lower() if p["appl"] else "solid materials"))
    if p["coating"]:
        feats.append(p["coating"] + (" · " + p["size_class"].replace("Workpiece dimension ", "workpieces ") if p["size_class"] else ""))
    apps = [a for a in p["application"] if not a.lower().startswith(("required cutting speed", "dry and wet"))][:4]
    if apps:
        feats.append("For: " + "; ".join(a[0].lower() + a[1:] for a in apps))
    feats += p["features"][:4]
    feats += p["advantages"][:3]
    feats += ["Cuts: " + "; ".join(p["materials"][:8])] if p["materials"] else []
    adv = p["advantages"][:7]
    specs = {"kind": "table", "tables": tables_for(p), "models": [{"name": p["name"], "glance": [LEVEL.get(p["level"], p["level"]), p["tooth"], p["appl"], ins + " (" + mm + ")", glance_pitch]}],
             "glance_keys": ["product_level", "tooth_form", "application", "band_width", "tooth_pitches"], "caps": {}, "no_voltage": True,
             "note": "Band length is cut and welded to your saw: tell us the machine or the blade length. Tooth pitch is chosen by the contact length (width) of the cut — "
                     "4 to 12 teeth in the material. Sizes in inches with WIKUS's metric size in brackets."}
    return dict(id="wk-" + p["slug"], group=g, page=P_BLADES, brand=BRAND, name=name, short=p["name"],
                models_label=f"{p['name']} · {ins} ({mm})",
                summary=summary, features=feats, optional=adv,
                images=["wk-" + p["slug"]], videos=[], specs=specs,
                pdf={"file": f"files/wikus/{p['slug']}.pdf", "label": f"{p['name']} data sheet", "size": "PDF · WIKUS data sheet"})


PAGE = dict(
    title="Band Saw Blades for Metal — Bimetal & Carbide | NovoTech",
    meta="WIKUS metal-cutting band saw blades welded to length in Canada: M42 and X3000 bimetal, carbide-tipped and coated carbide, CBN for hardened steel — 1/2″ to 4″ wide, all tooth pitches.",
    h1="Band saw blades for metal cutting — bimetal, carbide-tipped and CBN",
    intro="A band saw blade is the one consumable that decides what a band saw machine can do: the right cutting material, tooth form and "
          "tooth pitch cut faster, straighter and longer than the wrong one on any saw. NovoTech supplies WIKUS band saw blades — made in "
          "Germany by the world's largest band saw blade maker — welded to the length of your machine in Canada: M42 bimetal blades from the "
          "economical PRIMAR through the MARATHON, PROFLEX, SKALAR and SELEKTA GS, the coated PREMIUM versions and the X3000® blades for "
          "difficult alloys; carbide-tipped blades from the entry-level TAURUS and MARADUR to the FUTURA family for solid steel, the NE "
          "blades for aluminum and copper and the specialists for hardened parts; coated carbide blades for production; and CUBOGRIT® CBN "
          "blades that cut hardened HSS and tool steel above 55 HRC. Widths from 1/2″ to 4″ in every tooth pitch, for Bekamak, NovoTech "
          "value-line and any other horizontal or vertical band saw. Blade selection and pitch advice from Mississauga, ON.",
    points=["Bimetal M42 and X3000® blades, 1/2″ to 4″ wide — profiles, bundles and solid material to 145,000 psi",
            "Carbide-tipped and coated carbide blades for production sawing of solid steel, stainless, titanium and aluminum",
            "CBN-coated CUBOGRIT® blades for hardened steel above 55 HRC; every blade welded to your machine's length in Canada"],
    hero="wk-marathon-m42", minis=["wk-futura", "wk-proflex-m42"],
    groups=[(g[0], g[1], g[2], BRAND) for g in GROUPS],
    faq=[{"q": "Bimetal or carbide — which band saw blade do I need?",
          "a": "A bimetal blade (M42 high-speed-steel teeth on a spring-steel back) is the right blade for a fabrication shop: structural profiles, tube, bundles and solid bar up to about 145,000 psi, mixed materials, on any band saw. A carbide-tipped blade cuts solid material two to three times faster and lasts longer, but it wants a rigid saw with enough motor power and band tension — the Bekamak production saws and most saws with a carbide package. The TAURUS and MARADUR are made to run on saws without a carbide package, so they are the first step up; stainless, titanium and nickel alloys call for the FUTURA VA and 718; aluminum and copper for the NE blades; hardened steel for the FUTURA SN or the CBN-coated CUBOGRIT."},
         {"q": "How do I choose the tooth pitch?",
          "a": "By the contact length — the width of material the blade is in at any moment: 4 to 12 teeth should be in the cut. Thin-wall tube and small profiles need a fine pitch (10–14 TPI), bar of 2 to 4 inches a 3–4 or 2–3 TPI blade, and large solid material 1.4–2 TPI and coarser. A variable pitch (for example 3–4 TPI) runs quieter and resists vibration on profiles and bundles; a constant pitch is used on uniform solid material. Each blade's table on this page lists the pitches available in every width and the contact length each pitch is meant for."},
         {"q": "What do the product levels mean?",
          "a": "WIKUS grades its blades: level 1 is the economical entry blade (PRIMAR, TAURUS, MARADUR), level 2 the universal production blade (MARATHON, PROFLEX, DUROSET, ECODUR), level 3 the high-performance blade for the highest cutting rates and blade life (SKALAR, SELEKTA GS, FUTURA) and level S the specialists for one job — hardened parts (FUTURA SN), large solid material (ARION FG), thin-walled tube (TCT)."},
         {"q": "Which blade width and length fits my saw?",
          "a": "The width and thickness are set by the saw's wheels and guides — 1″ × 0.035″ on most 10″ to 13″ shop saws, 1-1/4″ × 0.042″ and 1-1/2″ × 0.050″ on the mid-size automatic saws, 2″ to 3-1/8″ on the double-column production saws. The length is the loop length of your machine; we weld the blade to it from coil. Send the saw make and model and we look it up."},
         {"q": "Can carbide blades run on my saw?",
          "a": "On the Bekamak BMSO and BMSY automatic saws, the double-column saws and any saw with a carbide package (high band tension, rigid guides, enough motor power) — yes, any of the carbide blades on this page. On a lighter saw, use the TAURUS or MARADUR, which are set and ground to run without the carbide package, or stay with a level 3 bimetal blade such as the SKALAR M42."},
         {"q": "What is the X3000® cutting material?",
          "a": "A WIKUS high-speed steel with higher hardness and toughness than M42, used on the MARATHON, SKALAR and SELEKTA GS X3000 blades for difficult-to-machine materials and special alloys — stainless, nickel and titanium alloys, high-strength steels — where an M42 edge dulls early but a carbide blade is not justified."},
         {"q": "Do you stock blades and weld them in Canada?",
          "a": "Yes — the common widths are stocked as coil in Mississauga and welded and annealed to your length; the complete WIKUS program is available to order. Tell us the saw, the materials you cut and the sizes, and we propose the blade and the pitch — and we are happy to run a test blade on a difficult job."}],
    faq_title="Questions we get asked about band saw blades",
    related_pages=[{"href": "band-saw.html", "label": "Metal cutting band saws"}, {"href": "double-column-band-saws.html", "label": "Bekamak double-column band saws"},
                   {"href": "automatic-band-saws.html", "label": "Bekamak automatic band saws"}, {"href": "circular-cold-saws.html", "label": "Circular cold saws"}],
    related_title="Band saws from NovoTech",
)
BRAND_LINE = "WIKUS band saw blades are made in Germany by WIKUS-Sägenfabrik, Spangenberg — the world's largest producer of band saw blades. Sold, welded to length and supported in Canada by NovoTech."
ORIGIN = {"title": "Made in Germany by WIKUS", "text": "WIKUS has made band saw blades in Spangenberg, Germany since 1958 — bimetal, carbide-tipped and coated blades for metal cutting, developed in its own Technical Competence Center and cut and welded to length by its partners worldwide."}


def register_images(products):
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "wikus"); os.makedirs(d, exist_ok=True)
    keys = []
    for p in products:
        key = "wk-" + p["slug"]
        dst = os.path.join(d, key + ".jpg")
        if not os.path.exists(dst):
            shutil.copy(SRC_IMG + p["slug"] + ".jpg", dst)
        imap[key] = {"src": f"tools/src-images/wikus/{key}.jpg", "alt": f"WIKUS {p['name']} {KIND[GROUP_OF[p['slug']]]} — {p['tagline'] or p['appl']}", "section": "wikus", "trim": False, "quality": 82, "cutout": False}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "wikus_keys.txt"), "w").write(",".join(keys))
    return keys


def copy_datasheets(products):
    d = os.path.join(ROOT, "src", "files", "wikus"); os.makedirs(d, exist_ok=True)
    for p in products:
        dst = os.path.join(d, p["slug"] + ".pdf")
        if not os.path.exists(dst):
            shutil.copy(SRC_PDF + p["slug"] + ".pdf", dst)


def build():
    raw = load()
    products = [parse(raw[s]) for s in ORDER]
    fams = [family(p) for p in products]
    write_families(SET, fams)
    write_category(P_BLADES, PAGE, fams, SET, SECTION, extra={"nav_label": "Band saw blades", "hero_brand_line": BRAND_LINE, "catalogue_pdf": None, "origin_feature": ORIGIN})
    keys = register_images(products)
    copy_datasheets(products)
    print(f"band saw blades: {len(fams)} blades · {sum(len(f['specs']['tables']) for f in fams)} tables · images: {len(keys)}")


if __name__ == "__main__":
    build()
