#!/usr/bin/env python3
"""ISITAN data library: unit conversions, table builders and page writers shared by tools/isitan_data.py.

Sources (outside the repository):
  /home/claude/isitan/tables.json   spec tables parsed from the NovoTech catalogue (parse_tables.py, imperial)
  /home/claude/isitan/img/          isitan.com product photos (1366 px, white background)
  /home/claude/isitan/cut/          photos extracted from the NovoTech catalogue (alpha cut-outs)

Writes content/families/plate-rolls.json, the image_map entries (prefix "is-") and the pages
content/pages/plate-rollers.json + four spoke pages.  Metric values in brackets are the manufacturer's
nominal capacities (the catalogue was converted from metric); other metric values are converted back.

    python3 tools/isitan_data.py && python3 tools/make_images.py --only $(cat tools/isitan_keys.txt) && python3 build.py
"""
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/isitan"
TABLES = json.load(open(os.path.join(SRC, "tables.json"), encoding="utf-8"))
IMG_DST = os.path.join(ROOT, "tools", "src-images", "isitan")

# ------------------------------------------------------------------ conversions
GAUGE_MM = {"22 ga": 0.8, "20 ga": 1.0, "18 ga": 1.2, "16 ga": 1.5, "14 ga": 2.0, "12 ga": 2.5, "11 ga": 3.0, "10 ga": 3.5, "8 ga": 4.0, "7 ga": 4.5}
FRAC_MM = {"3/16″": 5, "1/4″": 6, "5/16″": 8, "3/8″": 10, "7/16″": 11, "1/2″": 12, "9/16″": 14, "5/8″": 16, "3/4″": 20}
WIRE_MM = {"3/16″": 4, "1/4″": 6, "3/8″": 10, "1/2″": 12}
KW_STD = [0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37]


def fx(s):
    return s.replace("⁄", "/")


def thick_mm(v):
    v = fx(v).strip()
    if v in GAUGE_MM:
        return f"{GAUGE_MM[v]:g}"
    if v in FRAC_MM:
        return f"{FRAC_MM[v]:g}"
    return None


def thickness(cell):
    """'11 ga / 8 ga' → '11 ga / 8 ga (3 / 4 mm)'"""
    parts = [p.strip() for p in fx(cell).split("/") if p.strip()]
    # fractions contain "/" themselves: re-split on " / " only
    parts = [p.strip() for p in fx(cell).split(" / ")]
    mm = [thick_mm(p) for p in parts]
    if all(mm):
        return f"{' / '.join(parts)} ({' / '.join(mm)} mm)"
    return fx(cell)


def hp_kw(v):
    try:
        hp = float(v)
    except ValueError:
        return v
    kw = hp * 0.7457
    return f"{min(KW_STD, key=lambda k: abs(k - kw)):g}"


def motor(cell):
    parts = [p.strip() for p in cell.split("+")]
    kws = [hp_kw(p) for p in parts]
    hp = " + ".join(f"{float(p):g}" if re.fullmatch(r"[\d.]+", p) else p for p in parts)
    return f"{hp} HP ({' + '.join(kws)} kW)"


def inch_mm(cell, step=5):
    parts = [p.strip() for p in cell.split("/")]
    try:
        mm = [round(float(p) * 25.4 / step) * step for p in parts]
    except ValueError:
        return cell
    return f"{' / '.join(p + '″' for p in parts)} ({' / '.join(f'{m:g}' for m in mm)} mm)"


def roll_mm(cell):
    try:
        return f"{cell}″ ({round(float(cell) * 25.4):g} mm)"
    except ValueError:
        return cell


def dims(cell):
    parts = [p.strip() for p in cell.split("×")]
    try:
        mm = [round(float(p) * 25.4 / 10) * 10 for p in parts]
    except ValueError:
        return cell
    return f"{' × '.join(parts)}″ ({' × '.join(f'{m:g}' for m in mm)} mm)"


def weight(cell):
    try:
        lb = float(cell.replace(",", ""))
    except ValueError:
        return cell
    kg = lb / 2.20462
    kg = round(kg / 5) * 5 if kg < 2000 else round(kg / 10) * 10
    return f"{cell} lb ({kg:,.0f} kg)"


def speed(cell):
    try:
        m = round(float(cell) * 0.3048 * 2) / 2
    except ValueError:
        return cell
    return f"{cell} ft/min ({m:g} m/min)"


def wire(cell):
    parts = [p.strip() for p in fx(cell).split(",")]
    mm = [WIRE_MM.get(p) for p in parts]
    if all(mm):
        return f"{', '.join(parts)} ({', '.join(str(m) for m in mm)} mm)"
    return fx(cell)


def length_mm(model):
    m = re.search(r"(\d{3,4})\s*x", model)
    return int(m.group(1)) if m else None


def convert_table(t, title, sub=""):
    """Merge the two working-length rows, convert every cell to 'imperial (metric)'."""
    models = t["models"]
    rows_in = {}
    for r in t["rows"]:
        rows_in.setdefault(r["label"], []).append(r)
    out = []
    wl_ft = next((r for r in t["rows"] if r["label"] == "Working length" and r["unit"] == "FT"), None)
    wl_in = next((r for r in t["rows"] if r["label"] == "Working length" and r["unit"] == "in"), None)
    if wl_ft and wl_in:
        cells = []
        for m, ft, inch in zip(models, wl_ft["cells"], wl_in["cells"]):
            mm = length_mm(m)
            cells.append(f"{ft.replace(' FT', ' ft')} · {inch}″" + (f" ({mm} mm)" if mm else ""))
        out.append({"label": "Working length", "cells": cells, "key": True})
    for r in t["rows"]:
        lab, unit, c = r["label"], r["unit"], r["cells"]
        if lab == "Working length":
            continue
        if lab in ("Pre-bending capacity", "Rolling capacity"):
            out.append({"label": lab, "sub": "at 1.5× / 5× top roll Ø" if " / " in c[0] else "", "cells": [thickness(x) for x in c], "key": lab == "Rolling capacity"})
        elif lab in ("Top & bottom roll Ø", "Side roll Ø", "Roll Ø"):
            out.append({"label": lab, "cells": [roll_mm(x) for x in c]})
        elif lab == "Min. rolling Ø":
            out.append({"label": "Min. rolling Ø", "sub": "at 1.5× / 5× top roll Ø", "cells": [inch_mm(x) for x in c]})
        elif lab in ("Motor power", "Back roll motor"):
            out.append({"label": lab, "cells": [motor(x) for x in c]})
        elif lab == "Rolling speed":
            out.append({"label": lab, "cells": [speed(x) for x in c]})
        elif lab == "Oil tank capacity":
            out.append({"label": "Hydraulic oil tank", "cells": [f"{x} L" for x in c]})
        elif lab.startswith("Dimensions"):
            out.append({"label": "Dimensions L × W × H", "cells": [dims(x) for x in c]})
        elif lab == "Weight":
            out.append({"label": lab, "cells": [weight(x) for x in c]})
        elif lab == "Wire grooves Ø":
            out.append({"label": "Wire grooves Ø", "cells": [wire(x) for x in c]})
        elif len(lab) > 2:
            out.append({"label": lab, "unit": unit, "cells": [fx(x) for x in c]})
    return {"title": title, "sub": sub, "models": models, "rows": out}


def glance(t):
    """Per-model summary for the hub table and the AI catalogue: [working length, rolling capacity, roll Ø, motor, weight]."""
    def row(label):
        return next((r for r in t["rows"] if r["label"] == label), None)
    res = []
    for i, m in enumerate(t["models"]):
        wl = row("Working length"); cap = row("Rolling capacity"); rd = row("Top & bottom roll Ø") or row("Roll Ø"); mo = row("Motor power"); wt = row("Weight")
        res.append({"name": m, "glance": [wl["cells"][i] if wl else "—", cap["cells"][i] if cap else "—", rd["cells"][i] if rd else "—", mo["cells"][i] if mo else "—", wt["cells"][i] if wt else "—"]})
    return res


def caps(t):
    """Gallery caption per model: 'rolls up to 3/8″ (10 mm) plate × 6.7 ft'."""
    out = {}
    cap = next((r for r in t["rows"] if r["label"] == "Rolling capacity"), None)
    wl = next((r for r in t["rows"] if r["label"] == "Working length"), None)
    for i, m in enumerate(t["models"]):
        c = cap["cells"][i] if cap else ""
        up = c.split(" (")[0].split(" / ")[-1] if c else ""
        mm = re.search(r"\(([^)]*)\)", c)
        mm_up = mm.group(1).split(" / ")[-1].replace(" mm", "") + " mm" if mm else ""
        ft = wl["cells"][i].split(" ·")[0] if wl else ""
        out[m] = f"rolls up to {up} ({mm_up}) × {ft}" if up and mm_up else (f"{ft} working length" if ft else "")
    return out


GLANCE_KEYS = ["working_length", "rolling_capacity", "roll_diameter", "motor", "weight"]


def spec(table_refs, note):
    """table_refs: list of (page, index, title, sub)"""
    tables, models = [], []
    for pg, idx, title, sub in table_refs:
        t = convert_table(TABLES[str(pg)][idx], title, sub)
        tables.append(t)
        models += glance(t)
    c = {}
    for t in tables:
        c.update(caps(t))
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": GLANCE_KEYS, "caps": c, "note": note}


def drop_models(sp, keep):
    """Remove the model columns of a table spec for which keep(name) is false — e.g. the hand-operated models of a series."""
    for t in sp["tables"]:
        idx = [i for i, m in enumerate(t["models"]) if keep(m)]
        t["models"] = [t["models"][i] for i in idx]
        for r in t["rows"]:
            r["cells"] = [r["cells"][i] for i in idx if i < len(r["cells"])]
    sp["models"] = [m for m in sp["models"] if keep(m["name"])]
    sp["caps"] = {k: v for k, v in sp.get("caps", {}).items() if keep(k)}
    return sp


NOTE_ROLLS = ("Capacities are for mild steel with a yield strength of 34,100 psi (24 kg/mm²), shown as two values where the manufacturer "
              "states them: at a minimum rolling diameter of 1.5× the top roll diameter / at 5× the top roll diameter. Thin sheet is "
              "given in gauge; metric values in brackets are the manufacturer's nominal figures. Dimensions are overall L × W × H.")
NOTE_SIMPLE = ("Capacities are for mild steel with a yield strength of 34,100 psi (24 kg/mm²); thin sheet is given in gauge with the "
               "manufacturer's nominal metric value in brackets. Dimensions are overall L × W × H.")
VOLT = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase, or 240 V single-phase on models with a small enough motor"



# ------------------------------------------------------------------ hand-written tables (sections whose catalogue tables are 2-column)
def manual_table(title, sub, models, rows, key_labels=("Capacity",)):
    """rows: list of (label, [cells…]) or (label, sub, [cells…]); cells already finished strings."""
    out = []
    for r in rows:
        if len(r) == 3:
            label, s, cells = r
        else:
            label, cells = r
            s = ""
        out.append({"label": label, "sub": s, "cells": list(cells), "key": any(label.startswith(k) for k in key_labels)})
    return {"title": title, "sub": sub, "models": list(models), "rows": out}


def manual_spec(tables, glance_keys, glance, caps, note):
    """glance: {model: [cols…]} in the order of glance_keys; caps: {model: caption}."""
    models = [{"name": m, "glance": glance.get(m, [])} for t in tables for m in t["models"]]
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": glance_keys, "caps": caps, "note": note}


BRAND_LINE = "ISITAN machines are made in Turkey by ISITAN Makine — sheet-metal forming machinery since 1959, with European components. Sold, installed and supported in Canada by NovoTech."
ORIGIN = {"title": "Made in Turkey by ISITAN", "text": "ISITAN has built sheet-metal machinery in Bursa since 1959 — two factories, CE-certified machines with European components."}
PDF = {"file": "files/NovoTech-Isitan-Sheet-Metal-Forming-Catalogue-2025.pdf", "label": "Download the ISITAN machinery catalogue", "size": "PDF · 29 MB · imperial units"}
PDF_BK = {"file": "files/NovoTech-Bekamak-Band-Saws-Catalogue-2026.pdf", "label": "Bekamak saw catalogue", "size": "PDF · 7.5 MB · imperial units"}
VOLT_FAQ_GENERIC = {"q": "What voltage do these machines run on?",
                    "a": "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208 V, 240 V and 480 V 3-phase are available on request, and 240 V single-phase on models with a small enough motor. Manual machines have no electrics."}
CRUMBS = [{"label": "Home", "href": "index.html"}, {"label": "Products", "href": "products.html"}]
# "Inside the factory" section on every ISITAN-led page (NovoTech's own channel)
ISITAN_INTRO_VIDEO = {"intro_video": {"id": "XMn6YkPPOig", "title": "ISITAN company introduction video", "thumb": "video-XMn6YkPPOig", "duration": "PT3M55S"},
                      "intro_video_heading": "Inside the factory — where the machines are built",
                      "intro_video_text": "A tour of the ISITAN plant in Bursa, Turkey, where the sheet-metal and tube machinery on these pages has been built since 1959."}
SAHINLER_INTRO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}   # the supplier's factory tour carried its brand (Oct 2026)


def lower_keep_acronyms(text):
    """'NC tube benders' -> 'NC tube benders', 'Compact hydraulic press brakes' -> 'compact hydraulic press brakes'."""
    return " ".join(w if (w.isupper() and len(w) > 1) else w.lower() for w in text.split(" "))


def write_json(path, data):
    json.dump(data, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def register_images(images, keys_out):
    """images: {key: (source relative to SRC, alt)} → tools/src-images/isitan + image_map entries."""
    os.makedirs(IMG_DST, exist_ok=True)
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key, val in images.items():
        src, alt = val[0], val[1]
        opts = val[2] if len(val) > 2 else {}             # extra image_map options, e.g. {"cut_params": {...}}
        ext = os.path.splitext(src)[1].lower()
        dst = os.path.join(IMG_DST, key + ext)
        full = os.path.join(SRC, src)
        if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(full):   # new key, or the key now points at another photo
            shutil.copy(full, dst)
        imap[key] = {"src": f"tools/src-images/isitan/{key}{ext}", "alt": alt, "section": "forming", "trim": ext == ".png", "quality": 82, **opts}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", keys_out), "w").write(",".join(keys))
    return keys


def write_families(set_name, families):
    fam = {}
    for f in families:
        d = {k: v for k, v in f.items() if k not in ("page", "group")}
        d["group"] = f.get("group", "")
        d["brand"] = f.get("brand", "isitan")
        fam[f["id"]] = d
    write_json(os.path.join(ROOT, "content", "families", f"{set_name}.json"), {"order": [f["id"] for f in families], "families": fam})


def write_category(slug, p, families, set_name, section_label, *, hub=None, siblings=None, guide=None, extra=None):
    """A category page (category.html).  p: dict(title, meta, h1, intro, points, hero, minis, groups=[(gid,title,lead)], faq).
    hub: {"slug","label","image","blurb"} when the page belongs to a hub; siblings: [(slug, nav_label, label)]."""
    groups = [{"id": f"{g[0]}-group", "title": g[1], "lead": g[2], **({"brand": g[3]} if len(g) > 3 else {}),
               "families": [f["id"] for f in families if f["group"] == g[0]]} for g in p["groups"]]
    crumbs = CRUMBS + ([{"label": section_label, "href": f"{hub['slug']}.html"}] if hub else []) + [{"label": p["h1"]}]
    page = {
        "slug": slug, "template": "category.html", "family_set": set_name,
        "title": p["title"], "artifact_title": p["h1"], "meta_description": p["meta"], "h1": p["h1"], "intro": p["intro"],
        "hero_points": p["points"], "hero_image": p["hero"], "hero_image_secondary": p["minis"],
        "breadcrumb": crumbs, "hero_brand_line": BRAND_LINE,
        "groups": groups, "faq": p["faq"], "faq_title": p.get("faq_title") or f"Questions we get asked about {lower_keep_acronyms(p['h1'].split(' — ')[0])}",
        "catalogue_pdf": PDF, "origin_feature": ORIGIN, "section_label": section_label,
        "related_pages": p.get("related_pages", []),
        "related_title": p.get("related_title", "More sheet-metal machinery from NovoTech"),
    }
    if hub:
        page["section"] = {"label": section_label, "hub": {"href": f"{hub['slug']}.html", "label": hub["label"], "image": hub["image"], "blurb": hub["blurb"]},
                           "pages": [{"href": f"{s}.html", "label": nav, "current": s == slug} for s, nav, _ in siblings]}
        page["related_pages"] = [{"href": f"{s}.html", "label": lab} for s, _, lab in siblings if s != slug] + [{"href": f"{hub['slug']}.html", "label": hub["label"]}] + p.get("related_pages", [])
    if guide:
        page["related_article"] = guide
    page.update(ISITAN_INTRO_VIDEO)
    if extra:
        page.update(extra)
    write_json(os.path.join(ROOT, "content", "pages", f"{slug}.json"), page)


def write_hub(slug, h, families, set_name, section_label, subpages, *, extra=None):
    """subpages: [(slug, title, image, blurb, nav_label)]"""
    page = {
        "slug": slug, "template": "hub.html", "family_set": set_name, "nav_label": h.get("nav_label", "All " + section_label.lower()),
        "title": h["title"], "artifact_title": h.get("artifact_title", h["h1"]), "meta_description": h["meta"], "h1": h["h1"], "intro": h["intro"],
        "hero_points": h["points"], "hero_image": h["hero"], "hero_image_secondary": h["minis"],
        "breadcrumb": CRUMBS + [{"label": section_label}], "hero_brand_line": BRAND_LINE,
        "subpages": [{"slug": s, "title": t, "image": im, "blurb": b, "families": [f["id"] for f in families if f["page"] == s], "nav_label": nav} for s, t, im, b, nav in subpages],
        "range_kind": "table", "range_cols": h["range_cols"], "range_lead": h["range_lead"], "range_caption": h["range_caption"], "range_note": h["range_note"],
        "faq": h["faq"], "faq_title": h.get("faq_title", "Questions we get asked"),
        "catalogue_pdf": PDF, "origin_feature": ORIGIN, "section_label": section_label,
        "related_blurb": h.get("related_blurb", ""),
        "related_pages": [{"href": f"{s}.html", "label": t} for s, t, _, _, _ in subpages],
    }
    page.update(ISITAN_INTRO_VIDEO)
    if extra:
        page.update(extra)
    write_json(os.path.join(ROOT, "content", "pages", f"{slug}.json"), page)
