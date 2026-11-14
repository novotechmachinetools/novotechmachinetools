#!/usr/bin/env python3
"""NovoTech static site generator.

    python3 build.py            -> writes the whole site to dist/
    python3 build.py --staging  -> same, but with <meta name=robots content=noindex> for the test host

Content lives in content/, templates in templates/, static assets in src/.
"""
import html as html_lib
import urllib.parse
import glob, json, os, re, shutil, sys, datetime, hashlib
import html as html_mod
from zoneinfo import ZoneInfo
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
INDEXNOW_KEY = "a9f4c2e7b16d4d0e8c3b5f7a2d9e1c46"   # IndexNow (Bing, Yandex, Naver…): the key file sits at the site root; tools/indexnow.py submits changed URLs
if os.environ.get("LENIENT_IMAGES"):   # preview build with placeholder images: never into dist/, so it cannot be deployed
    DIST = os.path.join(ROOT, "dist-preview")
STAGING = "--staging" in sys.argv
DRAFTS = "--drafts" in sys.argv     # also render content/drafts/*.json (design candidates) into dist/
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

# Band saw blade width × thickness: North American blades are sold in nominal inch sizes, not converted
# millimetres — a 27 × 0.9 mm blade is a 1″ × .035″ blade.  (NovoTech, Oct 2026; blade length converts
# normally.)  Keyed by (width mm, thickness mm); unknown sizes fall back to a plain conversion.
BLADE_SIZES_IN = {
    (13, 0.65): "1/2 × .025", (20, 0.9): "3/4 × .035", (27, 0.9): "1 × .035", (34, 1.1): "1-1/4 × .042",
    (34, 1.07): "1-1/4 × .042", (41, 1.3): "1-1/2 × .050", (41, 1.277): "1-1/2 × .050", (54, 1.27): "2 × .050",
    (54, 1.3): "2 × .050", (54, 1.6): "2 × .063", (67, 1.3): "2-5/8 × .050", (67, 1.6): "2-5/8 × .063",
    (80, 1.6): "3-1/8 × .063", (80, 1.3): "3-1/8 × .050",
}


def blade_size_in(w, t):
    """'1 × .035 in' for a 27 × 0.9 mm blade; width values like '54/67' are converted part by part."""
    if isinstance(w, str) and "/" in w:
        parts = [blade_size_in(float(x), t).replace(" in", "") for x in w.split("/")]
        return " / ".join(parts) + " in"
    try:
        key = (int(round(float(w))), round(float(t), 3))
    except (TypeError, ValueError):
        return f"{w} × {t} in"
    for (kw, kt), name in BLADE_SIZES_IN.items():
        if kw == key[0] and abs(kt - key[1]) < 0.06:
            return name + " in"
    return f"{inch_frac(float(w), 8).replace('″', '')} × {float(t) / 25.4:.3f} in"


def inch_frac(mm, denom=8):
    """270 -> '10-5/8″' (nearest 1/denom inch)."""
    v = mm / 25.4
    whole = int(v); fr = Fraction(round((v - whole) * denom), denom)
    if fr == 1:
        whole += 1; fr = Fraction(0)
    if fr == 0:
        return f"{whole}″"
    return (f"{whole}-" if whole else "") + f"{fr.numerator}/{fr.denominator}″"


def inch_cap(m, mm):
    """Inch label of a capacity for model m: the model's nominal label when it defines one
    ("inch_labels": {"250": "10″"} — the trade size the saw is sold as), else the exact 1/8″ conversion."""
    lab = (m.get("inch_labels") or {}).get(f"{mm:g}")
    return lab or inch_frac(mm)


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
                    cells.append(("Ø" if key == "round" else "") + f"{inch_cap(m, v)} ({v:g} mm)")
            if any_val:
                rows.append({"label": f"Capacity {ang_label(a)} — {lab}", "cells": cells, "type": "text", "cap": key == "round" and a == "0"})
    rows.append({"label": "Blade speed", "cells": [rng(m.get("blade_speed_m_min"), lambda x: x * 3.2808, "ft/min", "m/min") for m in models], "type": "text"})
    def band(m):
        bd = m.get("band_mm")
        if not bd:
            return "—"
        L, W, T = bd
        if L is None:  # width × thickness only
            return f"{blade_size_in(W, T)} ({W} × {T} mm)"
        return f"{inch_frac(L, 2).replace('″', '')} × {blade_size_in(W, T)} ({L:g} × {W} × {T} mm)"
    if any(m.get("band_mm") for m in models):     # vertical saws give blade length and width as ranges in "other" instead
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

    def num(t):
        """'1,5' (European decimal) -> 1.5; '40,000' (thousands separator) -> 40000."""
        t = t.replace(",", "") if re.fullmatch(r"\d{1,3}(,\d{3})+", t) else t.replace(",", ".")
        return float(t)

    def conv(v):
        mm = re.match(r"^\s*([\d.,]+)\s*kW", str(v))
        if mm:
            return hp_range(str(num(mm.group(1))))
        mm = re.match(r"^\s*([\d.,]+)\s*kg\s*$", str(v))
        if mm:
            x = num(mm.group(1)); return f"{lb(x)} ({x:,.10g} kg)"
        mm = re.match(r"^\s*([\d.,]+)\s*mm\s*$", str(v))
        if mm:
            x = num(mm.group(1)); return f"{inch_frac(x)} ({x:g} mm)"
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
    rows.append({"label": "Weight", "cells": [f"{lb(m['weight_kg'])} ({m['weight_kg']:,.10g} kg)" if m.get("weight_kg") else "—" for m in models], "type": "text"})
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


# ---------------------------------------------------------------- band saws: standard / optional equipment by model
# (the owner, Nov 13 2026: "the standard and optional accessories are on Bekamak's own site but not on ours — add a section to
# the spec table: the features down the left and, for every model, a tick if it has it, a cross if it does not").
# Bekamak: "model_features" (the Standard / Optional Features tabs of every model on bekamak.com).  Captions that name the
# same part in different words on different models are merged, so a model is not marked as lacking a part it has; the band
# blade rows are left out (the blade size is a row of the spec table).  Other saws: "equipment" in the family data.
EQUIP_SAME = {
    "chip brush": "Blade brush", "coolant pump (boron oil)": "Coolant pump", "2° inclined head": "2° inclined blade",
    "cutting pressure control": "Cutting pressure adjustment", "material length stop rod": "Material length stop",
    "cutting speed indicator": "Cutting speed display", "hydraulic vise cylinder": "Hydraulic vise",
    "blade deviation sensor": "Blade deflection control", "double vise": "Second vise", "hydraulic split vise": "Split vise",
    "motorized chip brush": "Motorized swarf brush",
}


def equipment_rows(f, names):
    """rows for the spec table: [{"label", "cells": ["std" | "opt" | "no" | "na"], "type": "equip"}] and a note, or ([], "")
    "no": an option the manufacturer lists for other models of the family but not for this one; "na": not listed"""
    status, order = {}, []          # title -> {model: "std" | "opt"}

    def put(title, model, kind):
        t = EQUIP_SAME.get(title.lower(), title)
        if t not in status:
            status[t] = {}; order.append(t)
        if status[t].get(model) != "std":
            status[t][model] = kind

    listed = []
    if f.get("model_features"):
        for mf in f["model_features"]:
            if mf["model"] not in names:
                continue
            listed.append(mf["model"])
            for kind, k in (("standard", "std"), ("optional", "opt")):
                for it in mf[kind]:
                    if not it["title"].lower().startswith("band saw blade"):
                        put(it["title"], mf["model"], k)
    elif f.get("equipment"):
        listed = list(names)
        for kind, k in (("standard", "std"), ("optional", "opt")):
            for it in f["equipment"].get(kind) or []:
                title, models = (it, names) if isinstance(it, str) else (it["title"], it.get("models") or names)
                for m in models:
                    put(title, m, k)
    if not order:
        return [], ""
    is_option = {t: any(v == "opt" for v in status[t].values()) for t in order}
    n_std = lambda t: sum(1 for v in status[t].values() if v == "std")
    # the parts every saw has first (standard on the most models), the options after them
    pos = {t: i for i, t in enumerate(order)}
    order.sort(key=lambda t: (1 if n_std(t) == 0 else 0, -n_std(t) if n_std(t) else -len(status[t]), pos[t]))
    rows = []
    for t in order:
        cells = [(status[t].get(m) or ("no" if is_option[t] else "na")) if m in listed else "na" for m in names]
        rows.append({"label": t, "cells": cells, "type": "equip"})
    missing = [m for m in names if m not in listed]
    note = ("The manufacturer publishes no equipment list for the " + " · ".join(missing) + " — ask us for it.") if missing else ""
    return rows, note


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
    rows.append({"label": "Weight", "cells": [m.get("kg_text") or f"{lb(m['kg'])} ({m['kg']:,.10g} kg)" for m in models], "type": "text"})
    rows.append({"label": "Dimensions W × L × H", "cells": [m.get("dims_text") or dims(m["dims_cm"]) for m in models], "type": "text"})
    rows.append({"label": "Voltage", "cells": [m.get("voltage") or spec.get("voltage", "") for m in models], "type": "text"})
    return {"models": names, "rows": rows}


# ---------------------------------------------------------------- images
MISSING_IMAGES = set()   # filled only with LENIENT_IMAGES=1 (preview builds; never deployed)


def hub_card(hub, hub_info, g, groups, p, alt, by_slug_all):
    """The "All …" card at the foot of a section page shows a photo that no other card there shows, and not the page's own hero
    either (the owner, Nov 1 2026): the hub's hero, else its small hero pictures, else the section pages' card and hero photos."""
    used = {m["image"]["name"] for m in g["members"] if m.get("image") and m["slug"] != p["slug"]}
    if alt and alt.get("image"):
        used.add(alt["image"]["name"])
    used |= {k for k in [p.get("hero_image")] + list(p.get("hero_image_secondary") or []) if isinstance(k, str)}
    cands = [hub.get("hero_image")] + list(hub.get("hero_image_secondary") or [])
    for x in groups:
        for m in x["members"]:
            t = by_slug_all.get(m["slug"], {})
            cands += [m["image"]["name"] if m.get("image") else None, t.get("hero_image")] + list(t.get("hero_image_secondary") or [])
    for k in cands:
        if isinstance(k, str) and k in manifest and k not in used:
            return dict(hub_info, image=img(k)) if (hub_info.get("image") or {}).get("name") != k else hub_info
    return hub_info


def img(name, max_w=None):
    """Variants of an image for the templates; max_w drops the variants wider than that (the header logo: 360 px is plenty)."""
    e = manifest.get(name)
    if not e and os.environ.get("LENIENT_IMAGES") and name != "novotech-logo":   # local preview while images are still being made
        MISSING_IMAGES.add(name)
        return img("novotech-logo", max_w)
    if not e:
        raise SystemExit(f"image not in manifest: {name}")
    v = sorted(e["variants"], key=lambda x: x["w"])
    if max_w:
        v = [x for x in v if x["w"] <= max_w] or v[:1]
    largest = v[-1]
    # photos changed in place after they were published get ?v=<content hash>: the server lets browsers keep images a year
    # ("immutable"), so without it a returning visitor would go on seeing the old photo (the TTMC photos recoloured grey, Nov 10 2026;
    # the brochure covers, redrawn in place whenever a brochure is rebuilt — the grey TTMC brochures, Nov 11 2026)
    q = (lambda f: f"{f}?v={file_v(f)}") if (image_map.get(name, {}).get("recolor") or name.startswith("pdf-")) else (lambda f: f)
    return {
        "name": name,
        "alt": image_map.get(name, {}).get("alt") or e["alt"],
        "src": q(largest["file"]),
        "w": largest["w"], "h": largest["h"],
        "srcset": ", ".join(f"{q(x['file'])} {x['w']}w" for x in v),
        "small": q(v[0]["file"]),
        "thumb": q((e.get("thumb") or v[0])["file"]),
        "thumb_w": (e.get("thumb") or v[0])["w"],
        "thumb_srcset": ", ".join(f"{q(x['file'])} {x['w']}w" for x in ([e["thumb"]] if e.get("thumb") else []) + [v[0]]),
        "alpha": e["alpha"],
    }


FILE_V = {}


def file_v(f):
    """8 hex digits of a src/ file's content, for ?v="""
    if f not in FILE_V:
        FILE_V[f] = hashlib.md5(open(os.path.join(ROOT, "src", f), "rb").read()).hexdigest()[:8]
    return FILE_V[f]


# ---------------------------------------------------------------- jinja
env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
def nav_contains(item, slug):
    """True when the page `slug` is this nav item or anywhere in its sub-tree."""
    if (item.get("href") or "").split("#")[0] == slug + ".html":
        return True
    return any(nav_contains(c, slug) for c in item.get("children", []))


def nav_is(item, slug):
    return (item.get("href") or "").split("#")[0] == slug + ".html" and "#" not in (item.get("href") or "")


def css_text(name):
    """A stylesheet from dist/css inlined into a page (minified by main() before any page renders), URLs re-based to the page."""
    return open(os.path.join(DIST, "css", name), encoding="utf-8").read().replace("../fonts/", "fonts/")


RFQ = {k: v for k, v in json.load(open(os.path.join(ROOT, "content", "rfq.json"), encoding="utf-8")).items() if not k.startswith("_")}
RFQ_WARNED = set()


def rfq_type(x):
    """The short machine name in the subject of the quote-form e-mail, 'RFQ for <name>' (the owner, Nov 11 2026: "RFQ for press
    brake, RFQ for plate roller, RFQ for bandsaw — short, no model or specs"), for a page (dict) or a page slug / href.
    From content/rfq.json; a page not listed there gets its menu label, singular and in lower case, and a warning."""
    if isinstance(x, dict):
        slug, label = x.get("slug", ""), x.get("nav_label") or ""
    else:
        slug, label = str(x).split("#")[0], ""
        slug = slug[:-5] if slug.endswith(".html") else slug
    if slug in RFQ:
        return RFQ[slug]
    if slug and slug not in RFQ_WARNED:
        RFQ_WARNED.add(slug)
        print(f"  note: {slug} is not in content/rfq.json — its quote e-mails are titled from the menu label")
    name = re.split(r" & | &amp; | and |, | — | – | \(", re.sub(r"^All ", "", label))[0].strip()
    if not name:
        return ""
    words = name.split()
    w = words[-1]
    words[-1] = (w[:-3] + "y" if w.endswith("ies") else w[:-2] if re.search(r"(ch|sh|x)es$", w) else
                 w[:-1] if w.endswith("s") and not w.endswith("ss") else w)
    return " ".join(v if (v.isupper() or any(ch.isdigit() for ch in v)) else v.lower() for v in words)


env.globals.update(site=site, img=img, staging=STAGING, year=datetime.date.today().year, dia=dia, inch=inch, bar_sizes=bar_sizes,
                   nav_contains=nav_contains, nav_is=nav_is, css_text=css_text, rfq_type=rfq_type)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import section_icons  # noqa: E402  the section pictures of the profile benders' capacity tables (the owner, Nov 11 2026)
env.globals["sec_icon"] = lambda fid, label: section_icons.html(section_icons.icon_id(fid, label))
env.globals["asset_v"] = lambda name: hashlib.md5(open(os.path.join(ROOT, "src", name), "rb").read()).hexdigest()[:8]   # ?v= for any src/ file


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
        "email": f"{site['email_user']}@{site['email_domain']}",
        "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "telephone": site["phone_tel"], "email": f"{site['email_user']}@{site['email_domain']}",
                          "areaServed": "CA", "availableLanguage": ["English"]}],
        "hasMap": "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(f"{site['name']}, {a['street']}, {a['city']}, {a['region']} {a['postal']}"),
        "knowsAbout": ["press brakes", "fiber laser cutting machines", "hydraulic shears", "ironworkers", "metal band saws", "plate rolling machines",
                       "angle rolls and tube rollers", "pipe and tube benders", "rebar benders and cutters", "hydraulic presses", "deburring and finishing machines",
                       "press brake tooling", "welding positioners", "CNC machine tools"],
    }


_DATE_CACHE = {}


def page_dates(slug):
    """(datePublished, dateModified) of a page from the git history of its content file — the first and last commit
    that touched it — so the structured data and the visible 'updated' line carry a real date, not the build date."""
    if slug in _DATE_CACHE:
        return _DATE_CACHE[slug]
    import subprocess
    path = os.path.join("content", "pages", slug + ".json")
    today = datetime.date.today().isoformat()
    try:
        out = subprocess.run(["git", "log", "--follow", "--format=%cs", "--", path], cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.split()
        pub, mod = (out[-1], out[0]) if out else (today, today)
        if subprocess.run(["git", "status", "--porcelain", "--", path], cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip():
            mod = today                                          # uncommitted edits: modified now
    except Exception:
        pub, mod = today, today
    _DATE_CACHE[slug] = (pub, mod)
    return pub, mod


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
        "datePublished": page["date_published"], "dateModified": page["date_modified"],
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
                **({"countryOfOrigin": {"@type": "Country", "name": fb["country"]}} if fb.get("country") else {}),
                "additionalProperty": ([{"@type": "PropertyValue", "name": "Capacity", "value": f["headline"]}] if f.get("headline") else [])
                + [{"@type": "PropertyValue", "name": "Standard equipment", "value": "CSA-approved electrical panel; 1-year warranty; spare parts and technical support in Canada"}],
            }
            products.append(prod)
    graph.append({"@type": "ItemList", "@id": url + "#products", "name": page["h1"], "numberOfItems": len(products), "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": p} for i, p in enumerate(products)]})
    # videos
    # one VideoObject per video with an @id of its own: all the videos of a family used to share "#<family>-video", and
    # nodes with one @id are one node to a JSON-LD reader — a family's 10 videos merged into a single video with 10 names
    # (Nov 13 2026). A video shown in two families of the page is listed once.
    vids, seen_v = [], set()
    for g in ([] if page.get("subpages") else page.get("groups", [])):      # a hub shows cards only: its videos (and their anchors) are on the line pages
        for f in g["families"]:
            for v in f.get("videos") or []:
                if v["id"] not in seen_v:
                    seen_v.add(v["id"])
                    vids.append((v, url + "#video-" + v["id"]))
    if page.get("intro_video") and page["intro_video"]["id"] not in seen_v:
        vids.append((page["intro_video"], url + "#GMS-introduction-video"))
    for v, vurl in vids:
        t = img(v["thumb"])
        graph.append({
            "@type": "VideoObject", "@id": vurl, "name": v["title"], "description": v["title"] + " — NovoTech Machine Tools, Canada.",
            "thumbnailUrl": [absurl(t["src"])], "uploadDate": upload_datetime(v),
            **({"duration": v["duration"]} if v.get("duration") else {}),      # a length we don't know is left out, not guessed
            "contentUrl": "https://www.youtube.com/watch?v=" + v["id"], "embedUrl": "https://www.youtube-nocookie.com/embed/" + v["id"],
            "publisher": {"@id": site["domain"] + "/#organization"},
        })
    if page.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in page["faq"]]})
    if page.get("article_html"):   # the buying guide at the bottom of the page
        aid = page.get("article_id") or "buying-guide"
        words = len(re.sub(r"<[^>]+>", " ", page["article_html"]).split())
        graph.append({"@type": "Article", "@id": url + "#" + aid, "url": url + "#" + aid,
                      "headline": page.get("article_title") or "Buying guide", "description": page.get("article_intro") or page["meta_description"],
                      "articleSection": [t["label"] for t in page.get("article_toc", [])], "wordCount": words, "inLanguage": "en-CA",
                      "datePublished": page["date_published"], "dateModified": page["date_modified"],
                      **({"image": absurl(hero["src"])} if hero else {}),
                      "author": {"@id": site["domain"] + "/#organization"}, "publisher": {"@id": site["domain"] + "/#organization"},
                      "isPartOf": {"@id": url}, "mainEntityOfPage": {"@id": url}})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


FAMILY_SETS = {}
for fn in os.listdir(os.path.join(ROOT, "content", "families")):
    if fn.endswith(".json"):
        FAMILY_SETS[fn[:-5]] = json.load(open(os.path.join(ROOT, "content", "families", fn), encoding="utf-8"))["families"]

# content/family_pdfs.json (tools/value_brochures.py): the NovoTech brochure on every family that has none of its own, and on every
# page that shows none (the owner, Nov 7 2026: "no product without a PDF brochure") — the families here, as they load, the pages in
# apply_family_pdfs()
_fp = os.path.join(ROOT, "content", "family_pdfs.json")
FAMILY_PDFS = json.load(open(_fp, encoding="utf-8")) if os.path.exists(_fp) else {"families": {}, "pages": {}}


def family_pdf_entry(x):
    f = os.path.join(ROOT, "src", x["file"])
    if not os.path.exists(f):
        if __name__ == "__main__":       # the site build stops; an import (the brochure builder, before the brochure exists) goes on
            raise SystemExit(f"content/family_pdfs.json: {x['file']} is missing — build it with tools/brochure/build_brochure.py")
        return None
    units = "mm and inches" if "Tooling-Catalogue" in x["file"] else "imperial units"
    return {"file": x["file"], "label": x["label"], "size": f"PDF · {os.path.getsize(f) / 1e6:.1f} MB · {units}"}


for _fs in FAMILY_SETS.values():
    for _fid, _f in _fs.items():
        if _fid in FAMILY_PDFS["families"] and not _f.get("pdf") and family_pdf_entry(FAMILY_PDFS["families"][_fid]):
            _f["pdf"] = family_pdf_entry(FAMILY_PDFS["families"][_fid])
            _f["no_pdf"] = False                       # the value-line families were marked "no brochure yet"


def refresh_pdf_sizes(obj):
    """every {"file": "files/….pdf", "size": "PDF · 1 MB · imperial units"} shows the PDF's real size — the brochures are rebuilt
    more often than the page data that names them (the owner, Nov 1 2026: brochures with every photo are larger)"""
    if isinstance(obj, dict):
        f, sz = obj.get("file"), obj.get("size")
        if isinstance(f, str) and f.endswith(".pdf") and isinstance(sz, str) and "MB" in sz:
            fp = os.path.join(ROOT, "src", f)
            if os.path.exists(fp):
                obj["size"] = re.sub(r"[\d.]+ MB", f"{os.path.getsize(fp) / 1e6:.1f} MB", sz, count=1)
        for v in obj.values():
            refresh_pdf_sizes(v)
    elif isinstance(obj, list):
        for v in obj:
            refresh_pdf_sizes(v)


refresh_pdf_sizes(FAMILY_SETS)
# the nameplate badge names the model only when a family has one model: "DB 2017", not "DB 2017 · 1 model" (the owner, Oct 31 2026)
for _fs in FAMILY_SETS.values():
    for _f in (_fs.values() if isinstance(_fs, dict) else _fs):
        if isinstance(_f, dict) and _f.get("models_label"):
            _f["models_label"] = re.sub(r"\s*·\s*1 model\s*$", "", _f["models_label"])


def family(page, fid, fset=None):
    """A deep copy of a family record from the page's family set (or the set of the group / section page that lists it)."""
    fs = FAMILY_SETS[fset or page.get("family_set", "rebar")]
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
            if r: parts.append(f"cuts Ø{inch_cap(m, r)} ({r:g} mm) round")
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
    first = head.split(" ", 1)[0]
    if len(first) > 1 and first[0].isupper() and first[1:].isalpha() and first[1:].islower():
        head = head[0].lower() + head[1:]          # 'Bends …' → 'bends …', but 'V .24 – .98″' and 'Z1 / Z2' stay
    return f"{f['short']} · {head}" if head else f["short"], alt


# ---------------------------------------------------------------- videos: content/videos.json lists, per family, every
# NovoTech YouTube video that shows it (display order; titles of new ones written for the site) — it replaces the family's
# own list.  Durations come from the channel export tools/novotech-youtube-videos.tsv; thumbnails are video-<id> images.
YT_CHANNEL = {}
for _l in open(os.path.join(ROOT, "tools", "novotech-youtube-videos.tsv"), encoding="utf-8"):
    _p = _l.rstrip("\n").split("\t")
    if len(_p) == 3:
        YT_CHANNEL[_p[0]] = (_p[2].strip(), _p[1].strip())
_vp = os.path.join(ROOT, "content", "videos.json")
VIDEO_MAP = json.load(open(_vp, encoding="utf-8")) if os.path.exists(_vp) else {}


def _iso_dur(mmss):
    p = [int(x) for x in mmss.split(":")]
    p = [0] * (3 - len(p)) + p                     # "15", "2:13" or "1:02:13" (yt-dlp gives seconds alone under a minute)
    return f"PT{p[0]}H{p[1]}M{p[2]}S" if p[0] else f"PT{p[1]}M{p[2]}S"


def family_videos(f):
    lst = VIDEO_MAP.get(f["id"])
    extra = (VIDEO_MAP.get("_add") or {}).get(f["id"]) or []
    # "_drop": a video the family would show twice — the same footage uploaded again under another title (Nov 13 2026)
    drop = set((VIDEO_MAP.get("_drop") or {}).get(f["id"]) or [])
    if lst is None and extra:                      # "_add": videos appended to the family's own list
        lst = [v["id"] for v in f.get("videos") or []]
    if lst is None:
        if drop and f.get("videos"):
            f["videos"] = [v for v in f["videos"] if v["id"] not in drop]
        return
    lst = [it for it in lst if (it if isinstance(it, str) else it["id"]) not in drop]
    extra = [it for it in extra if it["id"] not in drop]
    have = {(it if isinstance(it, str) else it["id"]) for it in lst}
    lst = list(lst) + [dict(it, new=True) for it in extra if it["id"] not in have]
    cur = {v["id"]: v for v in f.get("videos") or []}
    out = []
    for it in lst:
        i = it if isinstance(it, str) else it["id"]
        v = dict(cur[i]) if i in cur else {"id": i, "thumb": "video-" + i}
        if not isinstance(it, str) and it.get("title") and (i not in cur or it.get("new")):
            v["title"] = it["title"]
        if not v.get("title"):
            v["title"] = YT_CHANNEL[i][0]
        if not v.get("duration") and i in YT_CHANNEL:
            v["duration"] = _iso_dur(YT_CHANNEL[i][1])
        if not v.get("duration") and not isinstance(it, str) and it.get("duration"):   # an unlisted video (not in the export)
            v["duration"] = _iso_dur(it["duration"])
        out.append(v)
    f["videos"] = out


# Upload order of the channel: tools/novotech-youtube-videos.tsv lists the regular uploads newest first (the channel's
# Videos tab). Shorts are not on that tab: tools/video_dates.json gives their publish dates and a few dated anchors from the
# list, and each Short gets the rank its date falls at between the anchors.
YT_ORDER = {}
for _n, _l in enumerate(open(os.path.join(ROOT, "tools", "novotech-youtube-videos.tsv"), encoding="utf-8")):
    _p = _l.split("\t", 1)
    if _p[0].strip():
        YT_ORDER.setdefault(_p[0].strip(), float(_n))
_vd = os.path.join(ROOT, "tools", "video_dates.json")
if os.path.exists(_vd):
    _d = json.load(open(_vd, encoding="utf-8"))
    _when = lambda t: datetime.datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp()
    _anc = sorted(((_when(t), YT_ORDER[i]) for i, t in _d.get("anchors", {}).items() if i in YT_ORDER), reverse=True)  # newest first
    for _i, _t in _d.get("shorts", {}).items():
        if _i in YT_ORDER or not _anc:
            continue
        _x = _when(_t)
        if _x >= _anc[0][0]:
            YT_ORDER[_i] = _anc[0][1] - 0.5
        elif _x <= _anc[-1][0]:
            YT_ORDER[_i] = _anc[-1][1] + 0.5
        else:
            for (_t0, _r0), (_t1, _r1) in zip(_anc, _anc[1:]):
                if _t1 <= _x <= _t0:
                    YT_ORDER[_i] = _r0 + (_r1 - _r0) * (_t0 - _x) / ((_t0 - _t1) or 1) + 0.01
                    break

# VideoObject uploadDate is a full ISO 8601 date-time with its UTC offset: a bare date makes Search Console report
# 'Invalid datetime value for "uploadDate"' and 'Datetime property "uploadDate" is missing a timezone' (the owner, Nov 9
# 2026, on every page). Publish times known from YouTube (tools/video_dates.json: "dates", "shorts", "anchors", UTC) are
# used as they are; a bare date (a video's "upload_date", or the old default) becomes midday Mississauga time that day.
TORONTO = ZoneInfo("America/Toronto")
VIDEO_PUBLISHED = {}
VIDEO_APPROX = {}          # the channel's Videos tab: "3 weeks ago", "2 years ago" turned into a date (tools/video_dates.json "approx")
if os.path.exists(_vd):
    for _sec in ("anchors", "shorts", "dates"):
        VIDEO_PUBLISHED.update(json.load(open(_vd, encoding="utf-8")).get(_sec) or {})
    VIDEO_APPROX = json.load(open(_vd, encoding="utf-8")).get("approx") or {}


def upload_datetime(v):
    t = (VIDEO_PUBLISHED.get(v.get("id")) or v.get("upload_date") or VIDEO_APPROX.get(v.get("id")) or "2023-12-26").strip()
    if "T" not in t:
        return datetime.datetime.fromisoformat(t + "T12:00:00").replace(tzinfo=TORONTO).isoformat()
    dt = datetime.datetime.fromisoformat(t.replace("Z", "+00:00"))
    return (dt if dt.tzinfo else dt.replace(tzinfo=TORONTO)).isoformat()


GENERAL_VIDEO = re.compile(r"\b(factory|assembly line|tour|instructions?|how to|how-to|vs\.?|versus|comparison|compar\w+|install\w*|"
                           r"operating|training|tutorial|exhibition|trade fair|catalogue|overview)\b", re.I)


def video_tier(v):
    """0: a video of the machine itself; 1: a general one — how-to, operating instructions, factory or plant tour,
    installation, comparison"""
    text = (v.get("title") or "") + " " + YT_CHANNEL.get(v["id"], ("", ""))[0]
    return 1 if GENERAL_VIDEO.search(text) else 0


def sort_videos(f):
    """Every family lists its videos by upload date, newest first (the owner, Oct 31 2026 - he had asked for upload order
    before; the Oct 30 rule that put the machine's own clips ahead of newer how-tos and comparisons is gone)."""
    vs = f.get("videos") or []
    # "_first" in content/videos.json: videos the owner wants at the front of a family, in his order (the XL, Oct 30 2026);
    # the rest follow newest first (the channel's upload order; Shorts placed by their publish date)
    first = {vid: i for i, vid in enumerate((VIDEO_MAP.get("_first") or {}).get(f["id"]) or [])}
    if len(vs) > 1:
        f["videos"] = sorted(vs, key=lambda v: (0, first[v["id"]]) if v["id"] in first
                             else (1, YT_ORDER.get(v["id"], 1e9)))[:MAX_VIDEOS]


MAX_VIDEOS = None      # no limit: every video of the product, three in view on desktop, the rest in the slider
                       # (the owner, Nov 12 2026; it was 10 since Oct 30 2026)


def family_thumb(f):
    """the family's photo on the other pages — the menu, the cards, the photos under the hero, the AI catalogue: its first
    gallery photo, or "thumb_image" when the owner picked another gallery photo for it (the owner, Nov 1 2026: the Senfeng
    compact lasers' thumbnail is gallery photo 5)"""
    th = f.get("thumb_image")
    return th if th and th in manifest else (f.get("images") or [None])[0]


def prepare_family(f):
    family_videos(f)
    sort_videos(f)
    if f.get("specs") and f["specs"].get("kind") == "tools":
        # press brake tooling: the data generator supplies the tool tables (rows = tools) as f["tool_tables"]
        f["headline"] = f.get("headline") or f["specs"].get("headline", "")
        f["model_caps"] = {**(f["specs"].get("caps") or {}), **(f.get("model_caps") or {})}
    elif f.get("specs") and f["specs"].get("kind") == "table":
        # generic spec kind: the data generator supplies finished tables (cells already "imperial (metric)")
        f["tables"] = f["specs"]["tables"]
        f["headline"] = f.get("headline") or f["specs"].get("headline", "")
        f["model_caps"] = {**(f["specs"].get("caps") or {}), **(f.get("model_caps") or {})}
    elif f.get("specs") and f["specs"].get("kind") == "bandsaw":
        f["table"] = build_bandsaw_table(f["specs"])
        eq_rows, eq_note = equipment_rows(f, f["table"]["models"])
        if eq_rows:
            f["table"]["rows"] += [{"label": "Standard and optional equipment", "type": "section"}] + eq_rows
            f["table"]["equip_note"] = eq_note
            f["table"]["has_no"] = any("no" in r["cells"] for r in eq_rows)
            f["table"]["has_na"] = any("na" in r["cells"] for r in eq_rows)
        rounds = [bandsaw_round0(m) for m in f["specs"]["models"]]
        f["max_mm"] = max(rounds) if rounds else 0
        lo = min(r for r in rounds if r) if any(rounds) else 0
        m_lo = next((m for m in f["specs"]["models"] if bandsaw_round0(m) == lo), {})
        m_hi = next((m for m in f["specs"]["models"] if bandsaw_round0(m) == f["max_mm"]), {})
        f["headline"] = f.get("headline") or (f"Round capacity Ø{inch_cap(m_lo, lo)} – Ø{inch_cap(m_hi, f['max_mm'])} ({lo:g}–{f['max_mm']:g} mm)" if lo != f["max_mm"] else f"Round capacity Ø{inch_cap(m_hi, f['max_mm'])} ({f['max_mm']:g} mm)")
    elif f.get("specs"):
        f["table"] = build_spec_table(f["specs"])
        f["max_mm"] = max_single_bar(f["specs"])
        kind = "Cuts" if f["specs"].get("kind") == "cutting" else "Bends"
        f["headline"] = f.get("headline") or f"{kind} single bars to {dia(f['max_mm'])}"
    f["gallery"] = [img(n) for n in f.get("images", [])]
    for im in f["gallery"]:
        im["cap1"], im["cap2"] = caption_for(f, im["alt"])
    th = f.get("thumb_image")
    f["card_image"] = img(th) if th and th in manifest else (f["gallery"][0] if f["gallery"] else None)
    f["gallery"] += feature_gallery(f)
    if f.get("control") and f["control"].get("images"):       # the control note under the summary (press brakes, Oct 28 2026)
        ims = []
        for k in f["control"]["images"]:
            key, cap = (k, None) if isinstance(k, str) else (k[0], k[1])
            if key in manifest:
                im = img(key)
                ims.append(dict(im, caption=cap or re.split(r"[:—–,]", im["alt"])[0].strip(), prog=CONTROL_PROG.get(key)))
        f["control"] = dict(f["control"], images=ims)
    return f


# a short line under each control in the control note: how it is programmed (the owner, Oct 30 2026: "2D or 3D under each model");
# the kinds follow the control comparison in the press brake buying guide
CONTROL_PROG = {
    "ctl-esa-s840-card": "2D programming", "ctl-esa-s875w-card": "3D programming",
    "ctl-delem-da66s": "2D programming", "ctl-delem-da69s": "3D programming",
    "ctl-delem-da53tx": "Numeric programming", "ctl-delem-da58tx": "2D programming", "ctl-cybelec-ct12": "2D programming",
    "ctl-scs920": "Graphic programming", "ctl-estun-e21ps": "Numeric (NC)", "ctl-estun-e315ps": "Numeric (NC)",
    "ctl-delem-da41t": "Numeric (NC)", "ctl-esa-s630": "Numeric and 2D", "dn-det-esabend-3d": "3D offline software",
}


def feature_gallery(f):
    """The Standard / Optional Feature photos from bekamak.com, appended to the family gallery after the
    machine views: one entry per photo, captioned with the feature and — when it is not standard on
    every model — which models have it as standard and which as an option."""
    # "all models" = the models bekamak.com has feature lists for (catalogue-only models are not counted)
    all_models = [mf["model"] for mf in f.get("model_features") or []]
    order, info, status = [], {}, {}
    # the caption describes the FEATURE (which models have it standard / optional), gathered over every
    # photo of that feature — bekamak.com often shows a different photo of the same part for each model
    for mf in f.get("model_features") or []:
        for kind in ("standard", "optional"):
            for it in mf[kind]:
                st = status.setdefault(it["title"].lower(), {"standard": [], "optional": []})
                if mf["model"] not in st[kind]:
                    st[kind].append(mf["model"])
                key = it.get("image")
                # one photo per feature and family: bekamak.com shows the same part again for every model
                # (four "hydraulic vise" photos, four "safety switch" photos …), which reads as repetition
                if key and key not in info and it["title"].lower() not in {t.lower() for t in info.values()}:
                    info[key] = it["title"]
                    order.append(key)
    out = []
    # standard (on at least one model) first, then option-only photos
    for key in sorted(order, key=lambda k: (0 if status[info[k].lower()]["standard"] else 1, order.index(k))):
        title = info[key]
        im = img(key)
        std = [m for m in all_models if m in status[title.lower()]["standard"]]
        opt = [m for m in all_models if m in status[title.lower()]["optional"] and m not in std]
        if std and not opt and set(std) >= set(all_models):
            cap2, cap1 = title, "Standard on all models"
        elif std and not opt:
            cap2, cap1 = title, "Standard on " + " · ".join(std)
        elif opt and not std:
            cap2, cap1 = f"{title} (optional)", "Optional on " + (" · ".join(opt) if set(opt) < set(all_models) else "all models")
        else:
            cap2, cap1 = f"{title} (optional on some models)", "Standard on " + " · ".join(std) + " — optional on " + " · ".join(opt)
        im["alt"] = f"Bekamak {f['short']} — {cap2[0].lower() + cap2[1:]}"
        im["cap1"], im["cap2"] = cap1, cap2
        out.append(im)
    return out


def range_table(subpages, pick=None):
    """One row per model across the range: for the hub's 'at a glance' table.  `pick` (page.range_pick) names the glance keys
    to show, in order, so families whose glance columns differ (ISITAN Edgebender vs Dener XL) still line up under one header."""
    rows = []
    for sp in subpages:
        for f in sp["families"]:
            spec = f.get("specs")
            if not spec:
                continue
            if spec.get("kind") == "tools":      # tooling: one row per family, not per tool
                rows.append({"model": f["short"], "family": spec.get("family_row_sub", ""), "href": f"{sp['slug']}.html#{f['id']}",
                             "kind": sp.get("nav_label") or sp["title"], "cols": spec.get("family_row", []), "line": ""})
                continue
            if spec.get("kind") == "table":
                gk = spec.get("glance_keys", [])

                def cell(g, k):
                    """one picked column: k is a glance key or a list of alternative keys (Dener 'working_area' = Senfeng 'area')"""
                    for key in ([k] if isinstance(k, str) else k):
                        if key in gk and gk.index(key) < len(g) and g[gk.index(key)]:
                            return g[gk.index(key)]
                    return "—"
                for m in spec["models"]:
                    g = m.get("glance", [])
                    cols = [cell(g, k) for k in pick] if pick else g
                    rows.append({"model": m["name"], "family": f["short"], "href": f"{sp['slug']}.html#{f['id']}", "kind": sp.get("nav_label") or sp["title"],
                                 "cols": cols, "line": ""})
                continue
            if spec.get("kind") == "bandsaw":
                for m in spec["models"]:
                    r = bandsaw_round0(m)
                    rect = ((m.get("capacity_mm") or {}).get("0") or {}).get("rect")
                    rows.append({"model": m["name"], "family": f["short"], "href": f"{sp['slug']}.html#{f['id']}", "line": "Premium · Bekamak" if f.get("line") == "premium" else "Value · NovoTech",
                                 "kind": sp.get("nav_label") or sp["title"], "round": f"Ø{inch_cap(m, r)} ({r:g} mm)" if r else "—",
                                 "rect": f"{inch_frac(rect[0])} × {inch_frac(rect[1])} ({rect[0]:g} × {rect[1]:g} mm)" if rect else "—",
                                 "motor": hp_range(m.get("main_motor_kw")), "weight": f"{lb(m['weight_kg'])} ({m['weight_kg']:,.10g} kg)" if m.get("weight_kg") else "—"})
                continue
            for i, m in enumerate(spec["models"]):
                def single(grade):
                    for mm, n in spec["capacity"][grade][i]:
                        if n == 1:
                            return dia(mm)
                    return "—"
                rows.append({"model": m["name"], "family": f["short"], "href": f"{sp['slug']}.html#{f['id']}", "kind": "Cutter" if spec.get("kind") == "cutting" else "Bender",
                             "cap45": single("45"), "cap65": single("65"), "motor": m.get("kw_text") or f"{hp(m['kw'])} ({kw_str(m['kw'])})",
                             "weight": m.get("kg_text") or f"{lb(m['kg'])} ({m['kg']:,.10g} kg)",
                             "voltage": "110/220 V 1-phase" if "110" in (m.get("voltage") or "") else "600 V 3-phase"})
    return rows


CATALOG_DATA = json.load(open(os.path.join(ROOT, "content", "catalog.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(ROOT, "content", "catalog.json")) else {"groups": [], "blurbs": {}, "card_image": {}, "featured": [], "brands": []}
SITE_TEMPLATES = {"home.html", "products.html", "contact.html", "about.html", "brochures.html", "articles.html", "privacy.html", "article.html"}
CATALOG = {}      # slug → category card (menu label, image, blurb, sub-pages), filled by main()
SHOWN_FAMILIES = [0]   # machine families that appear on the product pages, counted by main()
def apply_extra_groups(loaded):
    """content/extra_groups/<name>.json adds product groups (or a section page of a hub) from another family set to a page that
    another generator writes — e.g. the NovoTech value-line cold saws on circular-cold-saws.html — so that generator need not change:
        {"slug": page, "family_set": set, "groups": [{"id", "title", "lead", "brand", "families": [...], "after": group id}],
         "subpages": [{"slug", "title", "image", "blurb", "nav_label", "families", "in_range": false, "after": slug}],
         "subpage_add": {slug: {"families": [...], "blurb_add": text}},
         "intro_add": text, "points_add": [...], "faq_add": [...], "related_add": [...], "set": {field: value}}
    "subpage_add" puts families of the other set into a hub's existing section card and line-up (as "set:id"), e.g. the
    NovoTech value-line ESR / HER slip rolls in the plate-roller hub (the owner, Nov 10 2026)."""
    d = os.path.join(ROOT, "content", "extra_groups")
    if not os.path.isdir(d):
        return
    by_slug = {p["slug"]: p for p in loaded}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json"):
            continue
        x = json.load(open(os.path.join(d, fn), encoding="utf-8"))
        p = by_slug.get(x["slug"])
        if p is None:
            raise SystemExit(f"content/extra_groups/{fn}: no page {x['slug']}")
        for key, idkey in (("groups", "id"), ("subpages", "slug")):
            for e in x.get(key, []):
                e = dict(e)
                after = e.pop("after", None)
                e.setdefault("family_set", x.get("family_set"))
                lst = p.setdefault(key, [])
                pos = next((i + 1 for i, o in enumerate(lst) if o[idkey] == after), len(lst)) if after else len(lst)
                if any(o[idkey] == e[idkey] for o in lst):
                    raise SystemExit(f"content/extra_groups/{fn}: {key} {e[idkey]} is already on {x['slug']}")
                lst.insert(pos, e)
        for sslug, add in (x.get("subpage_add") or {}).items():
            sp = next((s for s in p.get("subpages", []) if s["slug"] == sslug), None)
            if sp is None:
                raise SystemExit(f"content/extra_groups/{fn}: {x['slug']} has no section page {sslug}")
            fset = add.get("family_set") or x.get("family_set")
            for fid in add.get("families", []):
                if fid not in FAMILY_SETS.get(fset, {}):
                    raise SystemExit(f"content/extra_groups/{fn}: unknown family {fset}:{fid}")
            sp["families"] = list(sp.get("families", [])) + [f"{fset}:{fid}" for fid in add.get("families", [])]
            if add.get("blurb_add"):
                sp["blurb"] = (sp.get("blurb") or "").rstrip() + " " + add["blurb_add"]
        if x.get("intro_add"):
            p["intro"] = p["intro"].rstrip() + " " + x["intro_add"]
        if x.get("points_add"):
            p["hero_points"] = list(p.get("hero_points", [])) + x["points_add"]
        if x.get("faq_add"):
            faq = list(p.get("faq", []))
            pos = len(faq) - 1 if faq and faq[-1]["q"].startswith("What voltage") else len(faq)     # the generic voltage answer stays last
            p["faq"] = faq[:pos] + x["faq_add"] + faq[pos:]
        if x.get("related_add"):
            have = {r["href"] for r in p.get("related_pages", [])}
            p["related_pages"] = list(p.get("related_pages", [])) + [r for r in x["related_add"] if r["href"] not in have]
        p.update(x.get("set", {}))


BRAND_WORDS = ("Dener", "Senfeng", "NovoTech", "Bekamak", "CSM", "Cevisa", "GMS", "Gecam", "Eurofintec", "ISITAN", "Plastmak",
               "EUROSTAMP", "Wecotech", "WIKUS")


def pdf_brand_label(pdf):
    """A brochure button names its brand ("Download the Dener servo-electric press brake brochure"), so two brochures of the same
    kind of machine on one page can be told apart.  The brand comes from the file name — files/NovoTech-Dener-… is Dener's,
    files/NovoTech-Senfeng-… Senfeng's, every other NovoTech-… brochure NovoTech's own (value or premium line)."""
    if not isinstance(pdf, dict) or not pdf.get("label", "").startswith("Download the "):
        return
    low = pdf["label"].lower()
    if any(w.lower() in low for w in BRAND_WORDS):
        return
    f = os.path.basename(pdf.get("file", ""))
    brand = "Dener" if "-Dener-" in f else "Senfeng" if "-Senfeng-" in f else "NovoTech" if f.startswith("NovoTech-") else None
    if brand:
        pdf["label"] = "Download the " + brand + " " + pdf["label"][len("Download the "):]


def apply_family_pdfs(loaded):
    """the page half of content/family_pdfs.json (the families get theirs when the family sets load): a page that shows no
    brochure gets the one of its families"""
    for p in loaded:
        x = FAMILY_PDFS["pages"].get(p["slug"])
        if x and not p.get("catalogue_pdf") and not p.get("catalogue_pdfs"):
            p["catalogue_pdf"] = family_pdf_entry(x)


def brand_all_pdf_labels(loaded):
    for p in loaded:
        pdf_brand_label(p.get("catalogue_pdf"))
        for x in p.get("catalogue_pdfs") or []:
            pdf_brand_label(x)
        for ln in p.get("lines") or []:
            pdf_brand_label(ln.get("pdf"))
    for fs in FAMILY_SETS.values():
        for f in fs.values():
            pdf_brand_label(f.get("pdf"))
            pdf_brand_label(f.get("spec_pdf"))
            for x in f.get("spec_pdfs") or []:
                pdf_brand_label(x)
    for b in site["brands"].values():
        pdf_brand_label(b.get("pdf"))


PDF_INDEX = {}    # files/x.pdf → {"label", "size", "pages": [{"href", "label"}]}, filled by main()


def build_catalog(loaded):
    by_slug = {p["slug"]: p for p in loaded}
    out = {}
    for c in site["nav"][0]["children"]:
        slug = c["href"].split("#")[0][:-5]
        p = by_slug.get(slug, {})
        im = CATALOG_DATA["card_image"].get(slug) or p.get("hero_image")
        out[slug] = {"slug": slug, "href": c["href"], "label": c["label"], "image": img(im) if im else None,
                     "blurb": CATALOG_DATA["blurbs"].get(slug) or p.get("meta_description", ""),
                     "children": [{"label": x["label"], "href": x["href"]} for x in c.get("children") or []]}
    return out


def build_nav_preview(loaded):
    """nav-preview.json — the photos of every category of the Products menu: the desktop menu shows all of those of the category
    under the pointer (no limit, the owner, Nov 1 2026) and the mobile menu a thumbnail beside each category (src/js/site.js). Loaded on the first
    open of the menu, so the pages carry none of it.  Per category: the pages and sections of its menu entries (their hero photo,
    or for an anchor to a product group the photo of the group's first family), then the product families of its own page, then
    the section pages of a hub."""
    by_slug = {p["slug"]: p for p in loaded}

    def page_of(href):
        return by_slug.get(href.split("#")[0][:-5])

    def clean(href):                       # the links as clean_urls() writes them into the pages: page, not page.html
        return re.sub(r"^([a-z0-9-]+)\.html", lambda m: "./" if m.group(1) == "index" else m.group(1), href)

    def group_family(p, g):
        for fid in g.get("families", []):
            f = FAMILY_SETS.get(g.get("family_set") or p.get("family_set") or "", {}).get(fid) if isinstance(fid, str) else None
            if f and f.get("images"):
                return f
        return None

    out = {}
    for c in site["nav"][0]["children"]:
        slug = c["href"].split("#")[0][:-5]
        p = by_slug.get(slug, {})
        cards, keys, hrefs = [], set(), set()

        def add(label, href, key, note=""):
            if not key or key not in manifest or key in keys or href in hrefs:      # every product, no limit (the owner, Nov 1 2026)
                return
            keys.add(key); hrefs.add(href)
            im = img(key, 800)
            cards.append({"l": label, "n": note or "", "h": clean(href), "s": img(key, 480)["src"], "ss": im["srcset"], "a": bool(im["alpha"]),
                          "t": im["thumb"], "k": key})

        entries, lines = [], []
        for t in c.get("children") or []:
            if t.get("children"):           # a tree group (Bekamak · premium line): its pages, named with the line
                lines.append([dict(u, label=f"{u['label']} · {t['label'].split(' · ')[0]}") for u in t["children"]])
            else:
                entries.append(t)
        for i in range(max((len(x) for x in lines), default=0)):     # alternate the lines: premium, value, premium, value
            entries += [x[i] for x in lines if i < len(x)]
        for e in entries:
            ep = page_of(e["href"])
            if not ep:
                continue
            key, anchor = None, e["href"].partition("#")[2]
            if anchor:
                g = next((g for g in ep.get("groups", []) if g.get("id") == anchor), None)
                f = group_family(ep, g) if g else None
                key = family_thumb(f) if f else None
            # "image" on a menu entry in content/site.json: the owner's pick for its card (Nov 7 2026: the CNC tube benders card
            # shows the CSM 50 MRE2-RBE), otherwise the page's large photo
            pick = e.get("image") if e.get("image") in manifest else None
            add(e["label"], e["href"], pick or key or ep.get("hero_image"))
        swap = c.get("menu_swap") or {}     # family id → the family whose card the menu shows instead (Nov 7 2026: Angle rolls shows
        for g in p.get("groups", []):       # the HPK 80 instead of the TC-42 coiler)
            f = group_family(p, g)
            if f and f["id"] in swap:
                f = FAMILY_SETS.get(g.get("family_set") or p.get("family_set") or "", {}).get(swap[f["id"]]) or f
            if f:
                add(f.get("short") or g.get("title", ""), f"{slug}.html#{f['id']}", family_thumb(f), f.get("headline", ""))
        for sp in p.get("subpages", []):
            add(sp.get("nav_label") or sp["title"], f"{sp['slug']}.html", sp.get("image"))
        if not cards:
            add(c["label"], c["href"], CATALOG_DATA["card_image"].get(slug) or p.get("hero_image"))
        thumb = img(cards[0]["k"])["thumb"] if cards else None
        for cd in cards:
            del cd["k"]
        out[clean(c["href"])] = {"t": c["label"], "b": CATALOG_DATA["blurbs"].get(slug) or p.get("meta_description", ""), "h": clean(c["href"]), "c": cards, "th": thumb}

        # the sub-menu entries (section pages, product groups, a product line): their own photos when the pointer rests on them
        def sub_entry(e):
            key = clean(e["href"])
            if key in out:
                return
            ep = page_of(e["href"])
            if not ep:
                return
            scards, skeys, shrefs = [], set(), set()

            def sadd(label, href, k, note=""):
                if not k or k not in manifest or k in skeys or href in shrefs:
                    return
                skeys.add(k); shrefs.add(href)
                im = img(k, 800)
                scards.append({"l": label, "n": note or "", "h": clean(href), "s": img(k, 480)["src"], "ss": im["srcset"], "a": bool(im["alpha"])})

            anchor = e["href"].partition("#")[2]
            blurb = ""
            if e.get("children"):                                  # a product line: the pages of that line
                for u in e["children"]:
                    up = page_of(u["href"])
                    if up:
                        sadd(u["label"], u["href"], up.get("hero_image"))
                blurb = ep.get("meta_description", "")
            elif anchor:                                           # a product group on a page: its families
                g = next((g for g in ep.get("groups", []) if g.get("id") == anchor), None)
                if g:
                    blurb = g.get("lead") or ""
                    fs = FAMILY_SETS.get(g.get("family_set") or ep.get("family_set") or "", {})
                    for fid in g.get("families", []):
                        f = fs.get(fid) if isinstance(fid, str) else None
                        if f and f.get("images"):
                            sadd(f.get("short") or f.get("name", ""), f"{ep['slug']}.html#{f['id']}", family_thumb(f), f.get("headline", ""))
            else:                                                  # a section page: the families of its groups, or its hub sections
                blurb = ep.get("meta_description", "")
                # "menu_series" on a page: the versions of one series as a single card that opens the series on the page (the
                # owner, Nov 7 2026: one SRGM card in the Mechanical shears menu, not six)
                series = {fid: sr for sr in ep.get("menu_series", []) for fid in sr["families"]}
                for g in ep.get("groups", []):
                    fs = FAMILY_SETS.get(g.get("family_set") or ep.get("family_set") or "", {})
                    for fid in g.get("families", []):
                        f = fs.get(fid) if isinstance(fid, str) else None
                        if not (f and f.get("images")):
                            continue
                        sr = series.get(f["id"])
                        if sr:
                            lead = fs.get(sr.get("image_family") or sr["families"][0]) or f
                            sadd(sr["label"], sr["href"], family_thumb(lead), sr.get("note", ""))
                            continue
                        sadd(f.get("short") or f.get("name", ""), f"{ep['slug']}.html#{f['id']}", family_thumb(f), f.get("headline", ""))
                for sp in ep.get("subpages", []):
                    sadd(sp.get("nav_label") or sp["title"], f"{sp['slug']}.html", sp.get("image"))
            if not scards:
                sadd(e["label"], e["href"], ep.get("hero_image"))
            if scards:
                out[key] = {"t": e["label"], "b": blurb, "h": key, "c": scards, "th": None}

        for t in c.get("children") or []:
            sub_entry(t)
            for u in t.get("children") or []:
                sub_entry(dict(u, label=f"{u['label']} · {t['label'].split(' · ')[0]}"))
    return out


def build_pdf_index(loaded):
    """every PDF a product page offers for download, with the pages that offer it"""
    idx = {}
    label_of = {c["href"].split("#")[0][:-5]: c["label"] for c in site["nav"][0]["children"]}
    for c in site["nav"][0]["children"]:
        for x in c.get("children") or []:
            label_of[x["href"].split("#")[0][:-5]] = x["label"]

    def walk(o, page):
        if isinstance(o, dict):
            f = o.get("file")
            if isinstance(f, str) and f.endswith(".pdf") and f.startswith("files/"):
                e = idx.setdefault(f, {"file": f, "label": o.get("label") or "", "size": o.get("size") or "", "pages": []})
                if not e["label"] and o.get("label"):
                    e["label"] = o["label"]
                ref = {"href": page["slug"] + ".html", "label": label_of.get(page["slug"]) or page.get("nav_label") or page.get("h1", "")}
                if ref not in e["pages"]:
                    e["pages"].append(ref)
            for v in o.values():
                walk(v, page)
        elif isinstance(o, list):
            for v in o:
                walk(v, page)
    for p in loaded:
        if p.get("template") in SITE_TEMPLATES:
            continue
        walk(p, p)
        # the brochures on the families' own buttons too (the value-line brochures of Nov 7 2026 are only there on some pages)
        for g in p.get("groups") or []:
            for fid in g.get("families") or []:
                f = FAMILY_SETS.get(g.get("family_set") or p.get("family_set") or "", {}).get(fid) if isinstance(fid, str) else None
                if f and f.get("pdf") and not f.get("no_pdf"):
                    walk({"pdf": f["pdf"]}, p)
    top = {c["href"].split("#")[0] for c in site["nav"][0]["children"]}
    for f, e in idx.items():
        e["pages"].sort(key=lambda r: (r["href"] not in top, r["label"]))      # the main category pages first
        seen_l, keep = set(), []
        for r in e["pages"]:
            if r["label"] not in seen_l:
                seen_l.add(r["label"])
                keep.append(r)
        e["pages"] = keep
        fp = os.path.join(ROOT, "src", f)
        if os.path.exists(fp):
            if not e["size"]:
                e["size"] = f"{os.path.getsize(fp) / 1048576:.1f} MB"
            try:
                import fitz
                e["page_count"] = fitz.open(fp).page_count
            except Exception:
                pass
        key = "pdf-" + re.sub(r"[^a-z0-9]+", "-", os.path.basename(f)[:-4].lower()).strip("-")
        e["cover"] = img(key) if key in manifest else None
    return idx


def prepare_site_page(page):
    """the data the site's own pages show: category cards, brands, brochures, article cards"""
    t = page.get("site_template") or page.get("template")   # draft homepage designs render with home.html's data
    page["catalog_groups"] = [{"id": g["id"], "title": g["title"], "lead": g["lead"],
                               "cards": [CATALOG[s_] for s_ in g["slugs"] if s_ in CATALOG]} for g in CATALOG_DATA["groups"]]
    page["featured"] = [CATALOG[s_] for s_ in CATALOG_DATA["featured"] if s_ in CATALOG]
    page["category_count"] = len(CATALOG)
    page["family_count"] = SHOWN_FAMILIES[0]
    page["brands"] = [dict(b, logo_img=img(b["logo"]) if b.get("logo") else None) for b in CATALOG_DATA["brands"]]
    makers = [b for b in CATALOG_DATA["brands"] if not b["name"].startswith("NovoTech")]
    page["maker_count"] = len(makers)
    page["country_count"] = len({b["country"] for b in makers})
    for k in ("showroom",):
        if page.get(k):
            page[k + "_imgs"] = [img(n) for n in page[k]]
    if t == "brochures.html":
        titles = {e["group"]: [] for e in CATALOG_DATA.get("brochures", [])}
        for e in CATALOG_DATA.get("brochures", []):
            if e["file"] in PDF_INDEX:                 # only brochures a product page offers
                titles[e["group"]].append(dict(PDF_INDEX[e["file"]], title=e["title"]))
        page["brochure_groups"] = [{"id": g["id"], "title": g["title"], "cards": titles[g["id"]]}
                                   for g in CATALOG_DATA["groups"] if titles.get(g["id"])]
        page["brochure_count"] = sum(len(g["cards"]) for g in page["brochure_groups"])
    if page.get("showcase"):   # the homepage designs: the best-selling product groups (content/home_showcase.json)
        sc = json.load(open(os.path.join(ROOT, "content", "home_showcase.json"), encoding="utf-8"))
        groups = []
        for g in sc["groups"]:
            c = CATALOG.get(g["slug"], {})
            try:
                src_page = json.load(open(os.path.join(ROOT, "content", "pages", g["slug"] + ".json"), encoding="utf-8"))
                fams = sum(len(sp.get("families", [])) for sp in src_page.get("subpages", [])) or sum(len(gr.get("families", [])) for gr in src_page.get("groups", []))
            except FileNotFoundError:
                fams = 0
            groups.append(dict(g, href=g["slug"] + ".html", img=img(g["image"]), count=fams, blurb=c.get("blurb")))
        page["showcase"] = {"groups": groups, "hero": [g for g in groups if g.get("hero")], "video": sc.get("video")}
    if t == "home.html":
        pick = ["files/NovoTech-Dener-Hydraulic-Press-Brakes-2026.pdf", "files/NovoTech-GMS-Rebar-Bending-Cutting-Machines-Catalogue.pdf",
                "files/NovoTech-Bekamak-Band-Saws-Catalogue-2026.pdf", "files/NovoTech-Press-Brake-Tooling-Catalogue-2026.pdf"]
        names = {e["file"]: e["title"] for e in CATALOG_DATA.get("brochures", [])}
        page["brochure_pick"] = [dict(PDF_INDEX[f], title=names.get(f, "")) for f in pick if f in PDF_INDEX]
        page["brochure_count"] = len([e for e in CATALOG_DATA.get("brochures", []) if e["file"] in PDF_INDEX])
        art = json.load(open(os.path.join(ROOT, "content", "pages", "metal-fabricating-articles.json"), encoding="utf-8"))
        pick = [a for a in art.get("articles", []) if a.get("featured")] or art.get("articles", [])[:5]
        page["guides"] = [dict(a, img=img(a["image"]) if a.get("image") else None) for a in pick]
    if page.get("effective"):
        page["effective_label"] = datetime.date.fromisoformat(page["effective"]).strftime("%B %-d, %Y")
    if page.get("articles"):
        for a in page["articles"]:
            a["img"] = img(a["image"]) if a.get("image") else None
    return page


def site_page_ld(page):
    """structured data for the site's own pages"""
    url = page["url"]
    graph = [organization_ld(),
             {"@type": "WebSite", "@id": site["domain"] + "/#website", "url": site["domain"] + "/", "name": site["name"],
              "publisher": {"@id": site["domain"] + "/#organization"}, "inLanguage": "en-CA"}]
    crumbs = []
    for i, c in enumerate(page.get("breadcrumb", []), 1):
        crumbs.append({"@type": "ListItem", "position": i, "name": c["label"], "item": absurl(c["href"]) if c.get("href") else url})
    if len(crumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumbs})
    kind = {"home.html": "WebPage", "products.html": "CollectionPage", "contact.html": "ContactPage", "about.html": "AboutPage",
            "brochures.html": "CollectionPage", "articles.html": "CollectionPage", "privacy.html": "WebPage", "article.html": "WebPage"}[page.get("site_template") or page["template"]]
    wp = {"@type": kind, "@id": url, "url": url, "name": page["title"], "description": page["meta_description"], "inLanguage": "en-CA",
          "isPartOf": {"@id": site["domain"] + "/#website"}, "publisher": {"@id": site["domain"] + "/#organization"},
          "datePublished": page["date_published"], "dateModified": page["date_modified"]}
    if len(crumbs) > 1:
        wp["breadcrumb"] = {"@id": url + "#breadcrumb"}
    if page["template"] in ("contact.html", "about.html", "home.html"):
        wp["about"] = {"@id": site["domain"] + "/#organization"}
    graph.append(wp)
    if page["template"] in ("products.html", "home.html"):
        items = page["featured"] if page["template"] == "home.html" else [c for g in page["catalog_groups"] for c in g["cards"]]
        graph.append({"@type": "ItemList", "@id": url + "#categories", "name": "Machine categories", "numberOfItems": len(items),
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c["label"], "url": absurl(c["href"])}
                                          for i, c in enumerate(items)]})
    if page["template"] == "brochures.html":
        docs = [e for g in page["brochure_groups"] for e in g["cards"]]
        graph.append({"@type": "ItemList", "@id": url + "#brochures", "name": "Brochures", "numberOfItems": len(docs),
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
                          "@type": "DigitalDocument", "name": e.get("title") or e["label"] or os.path.basename(e["file"]), "url": absurl(e["file"]),
                          "encodingFormat": "application/pdf"}} for i, e in enumerate(docs)]})
    if page["template"] == "articles.html":
        graph.append({"@type": "ItemList", "@id": url + "#articles", "name": "Articles and buying guides",
                      "numberOfItems": len(page["articles"]),
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a["title"], "url": absurl(a["href"])}
                                          for i, a in enumerate(page["articles"])]})
    if page["template"] == "article.html":
        hero = img(page["hero_image"]) if page.get("hero_image") else None
        graph.append({"@type": "Article", "@id": url + "#article", "headline": page["h1"], "description": page["meta_description"],
                      "mainEntityOfPage": {"@id": url}, "inLanguage": "en-CA",
                      "datePublished": page["date_published"], "dateModified": page["date_modified"],
                      "author": {"@id": site["domain"] + "/#organization"}, "publisher": {"@id": site["domain"] + "/#organization"},
                      **({"image": [absurl(hero["src"])]} if hero else {})})
    vids = list(page.get("videos") or [])
    if page.get("intro_video"):
        vids.insert(0, page["intro_video"])
    for v in vids:
        t = img(v["thumb"])
        graph.append({"@type": "VideoObject", "@id": url + "#video-" + v["id"], "name": v["title"],
                      "description": v["title"] + " — NovoTech Machine Tools, Canada.", "thumbnailUrl": [absurl(t["src"])],
                      "uploadDate": upload_datetime(v), **({"duration": v["duration"]} if v.get("duration") else {}),
                      "contentUrl": "https://www.youtube.com/watch?v=" + v["id"], "embedUrl": "https://www.youtube-nocookie.com/embed/" + v["id"],
                      "publisher": {"@id": site["domain"] + "/#organization"}})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def lead_sentence(text, limit=210):
    """The first sentence of a family summary (two when the first is very short), cut at a word under `limit` characters —
    the hub line-up shows this much; the whole text stays on the family's own page."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9Ø])", (text or "").strip())
    out = ""
    for s_ in parts:
        if out and len(out) + 1 + len(s_) > limit:
            break
        out = (out + " " + s_).strip()
        if len(out) >= 90:
            break
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0].rstrip(",;:—– ") + "…"
    return out


def hub_lineup_spec(hub, by_slug):
    """A short hub's line-up: every family on its section pages (and on the pages of its extra cards), grouped by brand and
    line — premium lines first, then 'made in' brands, then the value lines — each family linking to its anchor on the page
    that holds it.  Families are listed in page order, then group order."""
    targets = [(sp["slug"], sp.get("nav_label") or sp["title"].split(" — ")[0]) for sp in hub["subpages"]]
    targets += [(x["href"][:-5], x.get("nav_label") or x["title"].split(" — ")[0]) for x in hub.get("extra_cards", [])
                if x["href"].endswith(".html") and x["href"][:-5] in by_slug]
    seen, groups, order = set(), {}, []
    for slug, label in targets:
        p = by_slug[slug]
        for g in p.get("groups", []):
            fset = g.get("family_set") or p.get("family_set")
            for fid in g["families"]:
                if not isinstance(fid, str) or (fset, fid) in seen:
                    continue
                seen.add((fset, fid))
                brand = FAMILY_SETS[fset][fid].get("brand") or g.get("brand") or "novotech"
                if brand not in groups:
                    groups[brand] = []
                    order.append(brand)
                groups[brand].append({"slug": slug, "type": label, "set": fset, "fid": fid})

    # a hub may swap two cards of a brand's line-up ("lineup_swaps": [[fid, fid]]) — the sheet-laser hub shows the Senfeng
    # HM sheet-and-tube laser beside the H series and the NP after the compact lasers (the owner, Nov 1 2026)
    for a, b in hub.get("lineup_swaps") or []:
        for items in groups.values():
            ids = [it["fid"] for it in items]
            if a in ids and b in ids:
                i, j = ids.index(a), ids.index(b)
                items[i], items[j] = items[j], items[i]

    def rank(b):
        line = site["brands"].get(b, {}).get("line", "")
        return 0 if line == "Premium line" else 2 if line == "Value line" else 1
    return [{"brand": b, "items": groups[b]} for b in sorted(order, key=lambda b: (rank(b), order.index(b)))]


def _outside_links(text, phrase):
    """index of the first occurrence of phrase in text that is outside any tag or existing link and not part of a longer word"""
    blocked = [(m.start(), m.end()) for m in re.finditer(r"<a\b.*?</a>|<[^>]+>", text, re.S)]
    start = 0
    while True:
        i = text.find(phrase, start)
        if i < 0:
            return None
        j = i + len(phrase)
        inside = any(a < j and i < b for a, b in blocked)
        word_before = phrase[0].isalnum() and i > 0 and text[i - 1].isalnum()
        word_after = phrase[-1].isalnum() and j < len(text) and text[j].isalnum()
        if not (inside or word_before or word_after):
            return i
        start = i + 1


def link_hero_points(by_slug):
    """The product names in the hero bullet points link to their family on the page (#id) or, on a hub, to the page of that
    kind (the owner, Nov 1 2026) — content/point_links.json: {slug: [[phrase, target], ...]}, target a family id on the page or
    'page.html' / 'page.html#family'.  The first occurrence of each phrase outside an existing link is wrapped; a phrase or
    target that is not there stops the build, so a reworded point cannot silently lose its link."""
    path = os.path.join(ROOT, "content", "point_links.json")
    if not os.path.exists(path):
        return
    spec = json.load(open(path, encoding="utf-8"))
    for slug, pairs in spec.items():
        if slug.startswith("_"):
            continue
        p = by_slug.get(slug)
        if not p:
            raise SystemExit(f"content/point_links.json: no page {slug}")

        def fams_of(pg):
            return {f for g in pg.get("groups", []) for f in g.get("families", []) if isinstance(f, str)}
        pts = list(p.get("hero_points") or [])
        for phrase, target in pairs:
            if ".html" in target:
                page_slug, _, anchor = target.partition(".html")
                if page_slug not in by_slug:
                    raise SystemExit(f"content/point_links.json: {slug}: no page {page_slug}")
                if anchor and anchor[1:] not in fams_of(by_slug[page_slug]):
                    raise SystemExit(f"content/point_links.json: {slug}: {anchor[1:]} is not a family on {page_slug}")
                href = target
            else:
                if target not in fams_of(p):
                    raise SystemExit(f"content/point_links.json: {slug}: {target} is not a family on the page")
                href = "#" + target
            for k, t in enumerate(pts):
                i = _outside_links(t, phrase)
                if i is not None:
                    pts[k] = t[:i] + f'<a href="{href}">{phrase}</a>' + t[i + len(phrase):]
                    break
            else:
                raise SystemExit(f"content/point_links.json: {slug}: phrase not in the hero points: {phrase}")
        p["hero_points"] = pts


def unique_pdfs(fams):
    """the brochures of a set of families, each once, in order"""
    out, seen = [], set()
    for f in fams:
        for p in (f.get("pdf"),):          # brochures only — the full technical specifications stay on their product's buttons (the owner, Nov 1 2026)
            if p and p.get("file") and p["file"] not in seen:
                seen.add(p["file"]); out.append(p)
    return out


def hub_lineup(page):
    noun = page.get("lineup_noun") or page.get("section_label", "machines").lower()
    out = []
    for grp in page["lineup_spec"]:
        info = site["brands"].get(grp["brand"], {"name": grp["brand"].title(), "line": ""})
        name = info["name"]
        if name == "NovoTech" and info.get("line"):
            name = "NovoTech " + info["line"].lower().replace(" line", "-line")
        origin = info.get("origin")
        items = []
        for it in grp["items"]:
            f = prepare_family(family(page, it["fid"], it["set"]))
            items.append({"f": f, "href": f"{it['slug']}.html#{it['fid']}", "type": it["type"], "text": lead_sentence(f.get("summary", ""))})
        out.append({"brand": grp["brand"], "info": info, "id": "lineup-" + grp["brand"], "pdfs": unique_pdfs([it["f"] for it in items]),
                    "title": f"{name} {noun}" + (f" — {origin[0].lower() + origin[1:]}" if origin else ""), "cards": items})
    return out


HERO_NAMES_PATH = os.path.join(ROOT, "content", "hero_names.json")
HERO_NAMES = {k: v for k, v in json.load(open(HERO_NAMES_PATH, encoding="utf-8")).items() if not k.startswith("_")}
HERO_OF = {k[5:]: v for k, v in HERO_NAMES.items() if k.startswith("hero:")}      # hero photo → the family it shows
NO_HERO_NAME = set()


def hero_name(key, fallback):
    """the short name under a small hero photo — content/hero_names.json says what the machine is, never its model code"""
    if key in HERO_NAMES:
        return HERO_NAMES[key]
    NO_HERO_NAME.add(key)
    return fallback


def hero_cols(n):
    """columns of the small photos under the hero: (desktop, phone) — full rows where possible"""
    desk = n if n <= 4 else 3 if n in (5, 6, 9) else 4 if n in (7, 8, 11, 12) else 5
    return desk, (n if n <= 3 else 2 if n == 4 else 3)


def set_hero_many(page, keys, labels, links=None):
    """every product of the page small under the large photo, each with its short name (the owner, Nov 1 2026)"""
    page["hero_image_secondary"], page["hero_mini_labels"], page["hero_many"] = keys, labels, True
    page["hero_cols"] = hero_cols(len(keys))
    # about 15 % larger than before (the owner, Nov 7 2026: "a little bigger, 10 – 20 %"), and 15 % again the same afternoon
    page["hero_mini_h"] = 127 if len(keys) <= 4 else 110 if len(keys) <= 8 else 97    # desktop height of a small photo, px
    page["hero_mini_hm"] = 106 if page["hero_cols"][1] <= 2 else 76                   # phone height: bigger when two a row or fewer
    page["hero_mini_links"] = links or {}
    # many products (more than 8): on a desktop the strip runs the full width under the hero instead of under the photo only,
    # so the hero stays as tall as its text — balanced rows of up to 8
    n = len(keys)
    if n > 8:
        rows = -(-n // 8)
        page["hero_wide"], page["hero_cols_wide"] = True, -(-n // rows)
        page["hero_mini_h"] = 127                      # the full-width strip has room for the larger photos


def hero_keys(hero):
    """the large photo and the photo it was made from ("…-hero", "…-cut" versions of a family photo)"""
    return {hero} | {hero[: -len(s)] for s in ("-cut", "-hero") if hero and hero.endswith(s)} if hero else set()


def all_item_minis(page):
    """Every product item on the page small under the hero (the owner, Nov 1 2026): the first photo of each family, in page
    order, except the family the large photo already shows (its name goes under the large photo); the names say what the
    machine is (content/hero_names.json, by family id), not its model code."""
    hero, keys, labels = page.get("hero_image"), [], {}
    hc = hero_keys(hero)
    for g in page.get("groups") or []:
        for f in g["families"]:
            if not isinstance(f, dict) or not f.get("images"):
                continue
            if hc & set(f["images"]) or f["id"] == HERO_OF.get(hero):
                page.setdefault("hero_caption", hero_name(f["id"], f.get("short") or f["name"]))
                continue
            k = next((k for k in [family_thumb(f)] + f["images"] if k in manifest), None)
            if k and k not in keys and k not in hc:
                keys.append(k)
                labels[k] = hero_name(f["id"], f.get("short") or f["name"])
    return keys, labels


def hub_item_minis(page):
    """On a hub the products are its section pages: each card's photo small under the hero with the page's short name, linking
    to the page; the card whose photo (or one of whose families) the large photo shows names the large photo instead."""
    hero, keys, labels, links = page.get("hero_image"), [], {}, {}
    cards = [(sp.get("image"), sp["slug"], sp.get("nav_label") or sp["title"].split(" — ")[0], sp["slug"] + ".html",
              [f.get("images") or [] for f in sp.get("families") or [] if isinstance(f, dict)]) for sp in page.get("subpages") or []]
    cards += [(x.get("image"), x["href"].split(".html")[0].split("#")[0], x.get("nav_label") or x["title"].split(" — ")[0], x["href"], [])
              for x in page.get("extra_cards") or []]
    hc = hero_keys(hero)
    for im, slug, lab, href, fims in cards:
        if not im or im not in manifest:
            continue
        if im in hc:
            page.setdefault("hero_caption", hero_name("page:" + slug, lab))
            continue
        if im not in keys:
            keys.append(im)
            labels[im], links[im] = hero_name("page:" + slug, lab), href
    if "hero_caption" not in page:
        for im, slug, lab, href, fims in cards:
            if any(hc & set(ims) for ims in fims):
                page["hero_caption"] = hero_name("page:" + slug, lab)
                break
    return keys, labels, links


def hero_links(page):
    """Where each hero photo (the large one and the two small ones) links to: the family section that shows the same photo —
    on a hub the section page and its anchor, on a category page the anchor on the page itself; on a hub without such a family,
    the section page whose card uses the photo."""
    def cands(k):
        c = {k}
        for suf in ("-cut", "-hero"):
            if k.endswith(suf):
                c.add(k[: -len(suf)])
        return c

    def find(k):
        cs = cands(k)
        for lg in page.get("lineup") or []:
            for it in lg["cards"]:
                if cs & set(it["f"].get("images") or []):
                    return it["href"]
        if page.get("subpages"):
            for sp in page["subpages"]:
                for f in sp["families"]:
                    if cs & set(f.get("images") or []):
                        return f"{sp['slug']}.html#{f['id']}"
            for sp in page["subpages"]:
                if sp.get("image") in cs:
                    return sp["slug"] + ".html"
            for x in page.get("extra_cards") or []:
                if x.get("image") in cs:
                    return x["href"]
            return None
        for g in page.get("groups") or []:
            for f in g["families"]:
                if isinstance(f, dict) and cs & set(f.get("images") or []):
                    return "#" + f["id"]
        return None
    keys = [page.get("hero_image")] + list(page.get("hero_image_secondary") or [])
    return {k: h for k in keys if k for h in [find(k)] if h}



# ---------------------------------------------------------------------------------------------- press brake tonnage, both units
# Every tonnage on the press brake pages is shown in US tons and metric tonnes (Oct 28 2026): "44 US tons (40 t)",
# "16 to 66 US tons (15 to 60 t)", "110-ton (100 t)", "400 to 1,200 t (441 to 1,323 US tons)".  The sources keep their original
# figures; this pass adds the other unit at render time, idempotently (a figure already followed by its equivalent is skipped).
# US → t uses the catalogue pairs found in the family data ("44 US tons (40 t)"), so a converted figure is the maker's rating.
US_T = 1.1023113
PRESS_BRAKE_SLUGS = {"press-brake", "hydraulic-press-brake", "electric-press-brake", "compact-hydraulic-press-brakes", "horizontal-press-brake"}
_NUM = r"\d{1,3}(?:,\d{3})*(?:\.\d+)?"
_SEP = r"(?:to|–|-|—|and|or)"
_NOT_AFTER = r"(?!\s*(?:\(\s*\d|\)|<small|per\b|/|a foot|of force|-ton))"
_CAT_T = {}


def _num(s):
    return float(s.replace(",", ""))


def _fmt(x):
    return f"{x:,.0f}" if float(x).is_integer() else f"{x:,.1f}".rstrip("0").rstrip(".")


def _us_to_t(s):
    us = _num(s)
    if us in _CAT_T:
        return _fmt(_CAT_T[us])
    m = us / US_T
    return _fmt(round(m) if m >= 10 else round(m * 2) / 2)


def _t_to_us(s):
    return _fmt(round(_num(s) * US_T))


def load_catalogue_tons(loaded):
    """US-ton → tonne pairs as the maker rates them, read from every string of the family data"""
    pairs = re.compile(r"(" + _NUM + r")\s*US tons?\s*\((" + _NUM + r")\s*t\)")

    def walk(x):
        if isinstance(x, str):
            for us, t in pairs.findall(x):
                _CAT_T.setdefault(_num(us), _num(t))
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(loaded)
    walk(FAMILY_SETS)


_LIST = _NUM + r"(?:\s*(?:,|to|–|-|—|and|or)\s*" + _NUM + r")*"          # "33, 44 and 66", "16 to 66", "11 – 110"


def _map_nums(lst, conv):
    return re.sub(_NUM, lambda n: conv(n.group(0)), lst)


def _both_tons_text(text):
    # "132- and 165-ton", "400 and 600-ton"
    text = re.sub(r"(?<![(\d])\b(" + _NUM + r")(-?\s*(?:and|or)\s*)(" + _NUM + r")-ton\b(?!\s*\(\s*\d)",
                  lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}-ton ({_us_to_t(m.group(1))}{m.group(2).lstrip('-')}{_us_to_t(m.group(3))} t)", text)
    # "110-ton"
    text = re.sub(r"(?<![(\d])\b(" + _NUM + r")-ton\b(?!\s*\(\s*\d)", lambda m: f"{m.group(1)}-ton ({_us_to_t(m.group(1))} t)", text)
    # "44 US tons", "16 to 66 US tons", "33, 44 and 66 US tons", "1,323 tons", "11 – 110 US ton"
    text = re.sub(r"(?<![(\d])(?<!<small>)\b(" + _LIST + r")(\s*(?:US tons?|tons?))\b" + _NOT_AFTER,
                  lambda m: f"{m.group(1)}{m.group(2)} ({_map_nums(m.group(1), _us_to_t)} t)", text)
    # metric-only figures: "400 to 1,200 t", "3, 6 and 12 t", "110 t and up" — never "t/m", "t²", "(40 t)" or a figure already paired
    text = re.sub(r"(?<![(\d])(?<!<small>)\b(" + _LIST + r")(\s*t)\b(?!\s*(?:\(\s*\d|\)|<|/|per\b|²|-|\d))",
                  lambda m: f"{m.group(1)}{m.group(2)} ({_map_nums(m.group(1), _t_to_us)} US tons)", text)
    return text


def both_tons(text):
    """add the missing unit after every press brake tonnage in a string (HTML or plain); the generated tonnage table
    (between its markers) already carries both units in its own layout and is left alone"""
    if "ton" not in text and not re.search(r"\d\s*t\b", text):
        return text
    parts = re.split(r"(<!-- tonnage-table -->.*?<!-- /tonnage-table -->)", text, flags=re.S)
    return "".join(p if p.startswith("<!-- tonnage-table -->") else _both_tons_text(p) for p in parts)


def both_tons_page(page, everything):
    """walk the page dict; convert every string on a press brake page, elsewhere only strings about press brakes"""
    skip = {"slug", "href", "src", "id", "url", "image", "hero", "minis", "canonical", "file", "template", "section", "thumb", "thumb_image", "small", "srcset", "key"}

    def walk(x, key=None):
        if isinstance(x, str):
            if key in skip or key in ("title", "meta_description") and x is page.get(key):   # the search snippet stays ≤ 158 characters
                return x
            if everything or "press brake" in x.lower():
                return both_tons(x)
            return x
        if isinstance(x, dict):
            for k, v in list(x.items()):
                x[k] = walk(v, k)
            return x
        if isinstance(x, list):
            for i, v in enumerate(x):
                x[i] = walk(v, key)
            return x
        return x
    walk(page)

PREPARED = []   # prepared page dicts (families resolved) — used for the AI assistant's catalogue
FAMILY_PAGE = {}   # (family set, family id) → the product page that shows it (not a hub), filled by main()
ALL_PAGES = {}     # slug → page data as loaded, filled by main()


def _singular(s):
    """'XL hydraulic press brakes' -> 'XL hydraulic press brake' (the last word only)"""
    words = s.split()
    if not words:
        return s
    w = words[-1]
    words[-1] = (w[:-3] + "y" if w.endswith("ies") else w[:-2] if re.search(r"(ch|sh|x)es$", w) else
                 w[:-1] if w.endswith("s") and not w.endswith("ss") else w)
    return " ".join(words)


def _cell_text(c):
    if isinstance(c, dict):
        c = c.get("t") or c.get("text") or c.get("html") or ""
    if isinstance(c, (list, tuple)):
        c = " · ".join(_cell_text(x) for x in c)
    return html_mod.unescape(re.sub(r"<[^>]+>", "", str(c))).strip()


def model_spec_rows(f, model, limit=7):
    """the spec rows of one model, from the family's prepared tables: the key rows first; a band saw shows its straight
    capacities and one 45° capacity, then motor, blade and weight (the Black Friday cards)"""
    norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower())
    tables = f.get("tables") or ([f["table"]] if f.get("table") else [])
    for t in tables:
        names = [m if isinstance(m, str) else (m.get("name") or "") for m in t.get("models", [])]
        idx = next((i for i, n in enumerate(names) if norm(n) == norm(model)), None)
        if idx is None and len(names) == 1 and norm(model) in norm(names[0]):
            idx = 0
        if idx is None:
            continue
        rows, seen45, seen_cap = [], False, False
        for r in t.get("rows", []):
            if r.get("type") == "section":
                break
            cells = r.get("cells") or []
            if idx >= len(cells):
                continue
            c = cells[idx]
            if r.get("type") == "cap" and isinstance(c, list):
                # rebar machines: the first steel grade only, as "1 × 35M / #11 · 2 × 20M / #6"
                if seen_cap:
                    continue
                seen_cap = True
                sub = (r.get("sub") or "").replace("tensile", "").strip()
                label = (r.get("label") or "").split(" · ")[0] + (f", {sub} steel" if sub else "")
                val = " · ".join(f"{e.get('n', 1)} × {e.get('bars') or e.get('dia')}" for e in c if isinstance(e, dict))
                if val:
                    rows.append({"label": label, "value": val, "key": True})
                continue
            label = _cell_text(r.get("label") or "") + (f" ({r['sub']})" if r.get("sub") else "")
            val = _cell_text(c)
            if not re.search(r"[A-Za-z0-9]", val):
                continue
            if not val or val in ("—", "-", "–", "no", "na"):
                continue
            if label.startswith("Capacity"):
                straight = "0° (straight)" in label
                is45 = "45°" in label and label.endswith("round") and not seen45
                if not (straight or is45):
                    continue
                seen45 = seen45 or is45
                label = label.replace("Capacity ", "").replace(" — ", ", ").replace("0° (straight)", "Capacity at 0°")
                if is45:
                    label = "Capacity at " + label
            rows.append({"label": label, "value": val, "key": bool(r.get("key") or r.get("cap"))})
        rows = [r for r in rows if r["key"]] + [r for r in rows if not r["key"]]
        return rows[:limit]
    return []


def machine_type(f, model):
    """the kind of machine in a few words, from the family name without its series and model: 'XL hydraulic CNC press
    brakes, 66 – 661 US tons' -> 'Hydraulic CNC press brake'; 'BMSO 350GA automatic single-miter band saw with encoder
    feed' -> 'Automatic single-miter band saw'"""
    name = re.split(r" with |, | — | – | · |\(", f.get("name") or "")[0]
    toks = name.split()
    mtoks = {t.lower() for t in re.split(r"[\s/]+", model)}
    while toks and (toks[0].lower() in mtoks or toks[0].lower() in ("series", "range") or re.sub(r"[^a-z0-9]", "", toks[0].lower()) in
                    {re.sub(r"[^a-z0-9]", "", m) for m in mtoks}):
        toks = toks[1:]
    t = _singular(" ".join(toks)) if toks else _singular(f.get("short") or "")
    return t[:1].upper() + t[1:]


def stock_items(page):
    """content/pages/black-friday-machine-sale.json "stock": [{"family": "set:id", "model", "qty", "id"?, "image"?, "name"?,
    "type"?, "specs"? [[label, value]], "highlights"? [...], "note"?}] -> the cards of the Black Friday page: the model's own
    photo when the gallery has one named after it, its spec rows, three standard-equipment lines and a link to its family on
    its product page. Prices never come here: they are e-mailed by bf-quote.php from the private price list."""
    out = []
    for it in page.get("stock") or []:
        fset, fid = it["family"].split(":", 1)
        f = prepare_family(family(page, fid, fset))
        model = it.get("model") or f.get("short", "")
        keys = [k for k in (f.get("images") or []) if isinstance(k, str) and k in manifest]
        pk = it.get("image") or model_photo(model, keys) or ((f.get("card_image") or {}).get("name"))
        slug = FAMILY_PAGE.get((fset, fid))
        brand = site.get("brands", {}).get(f.get("brand"), {}) or (ALL_PAGES.get(slug) or {}).get("brand") or {}
        specs = [{"label": a, "value": b} for a, b in it["specs"]] if it.get("specs") else model_spec_rows(f, model)
        strip = lambda x: html_mod.unescape(re.sub(r"<[^>]+>", "", x)) if isinstance(x, str) else ""
        highlights = it.get("highlights") or [strip(x) for x in (f.get("features") or [])[:3]]
        sid = it.get("id") or re.sub(r"[^a-z0-9]+", "-", model.lower()).strip("-")
        out.append({
            "id": sid, "model": model, "name": it.get("name") or f"{brand.get('name', '')} {model}".strip(),
            "type": it.get("type") or machine_type(f, model), "qty": it.get("qty", 1),
            "condition": it.get("condition", "New"), "note": it.get("note", ""),
            "brand": brand.get("name", ""), "line": brand.get("line", ""), "origin": brand.get("origin") or brand.get("country", ""),
            "img": img(pk) if pk else None, "specs": specs, "highlights": highlights,
            "href": f"{slug}#{fid}" if slug else "", "family_name": f.get("name", ""),
        })
    seen = set()
    for x in out:
        if x["id"] in seen:
            raise SystemExit(f"black friday stock: two machines with the id {x['id']} — give one an \"id\"")
        seen.add(x["id"])
    return out


def render_page(page):
    page = dict(page)
    if page.get("subpages"):  # hub: resolve each sub-page's families and derive groups for the quote form / structured data
        for sp in page["subpages"]:
            # "set:id" is a family of another set (content/extra_groups "subpage_add")
            sp["families"] = [prepare_family(family(page, fid.split(":", 1)[1], fid.split(":", 1)[0]) if ":" in fid
                                             else family(page, fid, sp.get("family_set"))) for fid in sp["families"]]
            sp["has_videos"] = any(f.get("videos") for f in sp["families"])
            sp["href"] = sp["slug"] + ".html"
        page["groups"] = [{"id": sp["slug"], "title": sp["title"], "families": sp["families"]} for sp in page["subpages"]]
        if page.get("lines"):   # two product lines, each with its own sub-pages and range table
            by_slug = {sp["slug"]: sp for sp in page["subpages"]}
            for ln in page["lines"]:
                ln["subpages"] = [by_slug[sp["slug"]] for sp in ln["subpages"]]
                ln["range_rows"] = range_table(ln["subpages"])
                ln["brand_info"] = site["brands"].get(ln["brand"], {})
        page["range_rows"] = range_table([sp for sp in page["subpages"] if sp.get("in_range", True)], page.get("range_pick"))
        if page.get("range_big_first"):
            # the sheet metal brake hub (the owner, Nov 7 2026: the big machine first): in each family the heaviest model first
            def row_lb(r):
                for c in reversed(r.get("cols") or []):
                    m = re.search(r"([\d,]+) lb", str(c))
                    if m:
                        return int(m.group(1).replace(",", ""))
                return -1
            rows, block = [], []
            for r in page["range_rows"] + [None]:
                if block and (r is None or r["href"] != block[0]["href"]):
                    rows += sorted(block, key=row_lb, reverse=True)
                    block = []
                if r is not None:
                    block.append(r)
            page["range_rows"] = rows
        if page.get("range_groups"):   # e.g. rebar hub: benders and cutters in separate tables
            for rg in page["range_groups"]:
                rg["rows"] = [row for row in page["range_rows"] if row.get("kind") == rg["kind"]]
    for g in page.get("groups", []):
        g["families"] = [prepare_family(family(page, f, g.get("family_set"))) if isinstance(f, str) else f for f in g["families"]]
        g["pdfs"] = unique_pdfs(g["families"])
    if page.get("groups") and not page.get("subpages"):   # no "every model at a glance" table on a category page (the owner, Nov 1 2026)
        page.pop("range_rows", None)
    if not page.get("jump_links") and page.get("groups") and not page.get("subpages"):
        page["jump_links"] = ([{"href": "#range-at-a-glance", "label": "All models"}] if page.get("range_rows") else []) + [{"href": "#" + f["id"], "label": f["short"]} for g in page["groups"] for f in g["families"]] + ([{"href": "#compare", "label": "Compare"}] if page.get("compare") else []) + ([{"href": "#loading-options", "label": "Loading options"}] if page.get("loading") else []) + [{"href": "#reques-a-quote", "label": "Request a quote"}]   # compare and loading after the products (the owner, Nov 1 2026)
    if page.get("lineup_spec"):
        page["lineup"] = hub_lineup(page)
    if not page.get("jump_links") and page.get("hub_compact"):   # a short hub: its pages, then the parts of the page
        page["jump_links"] = ([{"href": sp["slug"] + ".html", "label": sp.get("nav_label") or sp["title"]} for sp in page["subpages"]]
                              + [{"href": x["href"], "label": x.get("nav_label") or x["title"].split(" — ")[0]} for x in page.get("extra_cards", [])]
                              + ([{"href": "#lineup", "label": "Line-up"}] if page.get("lineup") else [])
                              + ([{"href": "#compare", "label": "Compare"}] if page.get("compare") else [])
                              + [{"href": "#faq-title", "label": "Questions"}, {"href": "#reques-a-quote", "label": "Request a quote"}])   # no range table on hubs (the owner, Nov 1 2026)
    # every page: the large hero photo and, under it, every product of the page small with a short name, from desktop to
    # phone (the owner, Nov 1 2026); a page with one product keeps its two small photos
    if page.get("template") == "category.html" and page.get("groups") and page.get("hero_minis_all", True) is not False:
        keys, labels = all_item_minis(page)
        # "hero_minis_replace": {photo: {"image", "label"}} puts another photo the owner picked in a small photo's place (angle
        # rolls, Nov 10 2026: the HRBM 50 HV and HRBM 65 instead of the small ring roller and the tube roller)
        for old, new in (page.get("hero_minis_replace") or {}).items():
            if old in keys and new["image"] in manifest and new["image"] not in keys:
                keys[keys.index(old)] = new["image"]
                labels[new["image"]] = new.get("label") or labels.get(old)
        if keys:
            set_hero_many(page, keys, labels)
    if page.get("template") == "hub.html" and page.get("hero_minis_pick"):
        # the small photos under a hub's hero picked by the owner — [{image, label, href}] (shear hub, Nov 7 2026)
        pick = [m for m in page["hero_minis_pick"] if m["image"] in manifest]
        set_hero_many(page, [m["image"] for m in pick], {m["image"]: m["label"] for m in pick},
                      {m["image"]: m["href"] for m in pick if m.get("href")})
        # "sub": a short description under the model name; "scale": a photo drawn smaller on a desktop, so a compact machine
        # looks its size beside the others (press brake hub, the owner, Nov 12 2026)
        page["hero_mini_subs"] = {m["image"]: m["sub"] for m in pick if m.get("sub")}
        page["hero_mini_scale"] = {m["image"]: m["scale"] for m in pick if m.get("scale")}
    elif page.get("template") == "hub.html" and page.get("subpages") and page.get("hero_image") and page.get("hero_minis_all", True) is not False:
        keys, labels, links = hub_item_minis(page)
        if keys:
            set_hero_many(page, keys, labels, links)
    if page.get("template") in ("hub.html", "category.html") and page.get("hero_image"):
        page["hero_links"] = {**hero_links(page), **(page.get("hero_mini_links") or {})}
    page["url"] = f"{site['domain']}/{page['slug']}" if page["slug"] != "index" else site["domain"] + "/"   # clean URLs: pages are served without .html
    page["date_published"], page["date_modified"] = page_dates(page["slug"])
    page["updated_label"] = datetime.date.fromisoformat(page["date_modified"]).strftime("%B %Y")
    if page.get("article"):   # long-form guide kept from the old site (HTML fragment with <figure data-img> placeholders)
        art = open(os.path.join(ROOT, "content", "articles", page["article"]), encoding="utf-8").read()
        def fig(m):
            im = img(m.group(2))
            alt = html_mod.escape(m.group(4)) if m.group(4) else im["alt"]
            extra = (m.group(1) or "").strip()                     # e.g. "is-small" / "is-half": the figure floats beside the text
            cls = "guide-figure is-cutout" if im.get("alpha") else "guide-figure"
            cls = (cls + " " + extra).strip()
            cap = f"<figcaption>{html_mod.escape(m.group(3))}</figcaption>" if m.group(3) else ""
            sizes = "(max-width: 700px) 92vw, 330px" if "is-small" in extra else ("(max-width: 700px) 92vw, 560px" if "is-half" in extra else "(max-width: 700px) 92vw, 760px")
            return (f'<figure class="{cls}"><img src="{im["small"]}" srcset="{im["srcset"]}" sizes="{sizes}" '
                    f'width="{im["w"]}" height="{im["h"]}" style="--ar: {im["w"] / im["h"]:.4f}" alt="{alt}" loading="lazy" decoding="async">{cap}</figure>')
        art = re.sub(r'<figure class="guide-figure((?: [a-z-]+)*)" data-img="([^"]+)"(?: data-caption="([^"]*)")?(?: data-alt="([^"]*)")?></figure>', fig, art)
        # two or more half-width figures in a row sit side by side in a grid row (clear of any floated figure above)
        art = re.sub(r'((?:<figure class="guide-figure[^"]*\bis-half\b[^"]*">.*?</figure>\s*){2,})', r'<div class="guide-figure-row">\1</div>', art, flags=re.S)
        # a small figure floats beside the paragraph that follows it: the pair is one block (display: flow-root), so the photo
        # stays beside its own topic and never runs down beside the next one; on phones the photo goes under the text (the owner,
        # Oct 31 2026: "the photo of each topic under it or beside it")
        art = re.sub(r'((?:<figure class="guide-figure[^"]*\bis-small\b[^"]*">.*?</figure>\s*)+)(<p>.*?</p>)',
                     r'<div class="guide-pair">\1\2</div>', art, flags=re.S)
        page["article_toc"] = [{"id": i, "label": re.sub(r"<[^>]+>", "", t)} for i, t in re.findall(r'<section class="guide-section" id="([^"]+)">\s*<h3>(.*?)</h3>', art)]
        if page.get("template") == "article.html":   # a standalone article: its sections sit directly under the H1, so h3/h4 become h2/h3
            art = re.sub(r"<(/?)h4\b", r"<\1h3", re.sub(r"<(/?)h3\b", r"<\1h2", art))
        page["article_html"] = art
        gid = "#" + (page.get("article_id") or "buying-guide")
        if page.get("jump_links") and not any(j["href"] == gid for j in page["jump_links"]):   # the guide in the bar under the hero
            jl = list(page["jump_links"])
            jl.insert(next((i for i, j in enumerate(jl) if j["href"] == "#reques-a-quote"), len(jl)), {"href": gid, "label": "Buying guide"})
            page["jump_links"] = jl
    if page.get("template") == "black-friday.html":
        page["stock_items"] = stock_items(page)
    is_site = (page.get("site_template") or page.get("template")) in SITE_TEMPLATES
    if is_site:
        prepare_site_page(page)
    both_tons_page(page, page["slug"] in PRESS_BRAKE_SLUGS)
    tpl = env.get_template(page.get("template", "page.html"))
    inline_css = None if ARTIFACT else open(os.path.join(DIST, "css", "site.css"), encoding="utf-8").read().replace("../fonts/", "fonts/")   # minified by main(); URLs re-based to the page
    html = tpl.render(page=page, ld_json=site_page_ld(page) if is_site else page_ld(page), build_ts=int(datetime.datetime.now().timestamp()), inline_css=inline_css,
                      css_hash=asset_hash(os.path.join(ROOT, "src", "css", "site.css")), js_hash=asset_hash(os.path.join(ROOT, "src", "js", "site.js")),
                      ai_hash=asset_hash(os.path.join(ROOT, "src", "js", "ai.js")))
    PREPARED.append(page)
    return clean_urls(html)


def model_photo(name, gallery):
    """the gallery photo of one model, by its key ('sh-hpk65' for HPK 65, 'b-36' for B 36), for the finder's cards — the owner
    (Nov 9 2026) wants each model's own photo, not the series photo for all of them. Best first: the key names exactly this
    model; the key adds a suffix (HPK 120 -> sh-hpk120nc); the model adds a suffix to a photographed one (RBM40HV ->
    tm-rbm40, never tm-hrbm40); a run of the key's parts is the model (bk-bmso-350ga-1), or the model with a suffix (3041 ->
    es-d-3041pn)."""
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    mk = norm(name)
    if len(mk) < 3 or not re.search(r"\d", mk):
        return None
    cands = []
    for k in gallery:
        parts = [norm(p) for p in k.split("-") if norm(p)]
        forms = {norm(k)} | ({"".join(parts[1:])} if len(parts) > 1 else set())   # with and without the line prefix ('tm', 'sh')
        if mk in forms:
            cands.append((0, k))
        elif any(x.startswith(mk) and not x[len(mk)].isdigit() for x in forms if len(x) > len(mk)):
            cands.append((1, k))
        elif any(len(x) >= 3 and re.search(r"\d", x) and mk.startswith(x) and mk[len(x):].isalpha() for x in forms):
            cands.append((2, k))
        elif any("".join(parts[i:j]) == mk for i in range(len(parts)) for j in range(i + 1, len(parts) + 1)):
            cands.append((3, k))
        elif any("".join(parts[i:j]).startswith(mk) and "".join(parts[i:j])[len(mk):].isalpha()
                 for i in range(len(parts)) for j in range(i + 1, len(parts) + 1)):
            cands.append((4, k))                                   # 3041 -> es-d-3041pn
    return min(cands, key=lambda c: c[0])[1] if cands else None


def ai_catalogue(pages):
    """Machine-finder index (dist/ai/catalogue.json): one entry per family, with the page it lives on, its models and
    their headline capacities, and — for the finder to know everything the site says (the owner, Nov 7 2026) — every
    feature and option, every spec table, the words of its PDF brochure and structured capacities per model
    (tools/ai_index.py); plus every page with its introduction, key points and questions and answers."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import ai_index
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
                    if spec.get("kind") in ("table", "tools"):
                        if spec.get("tables"):
                            models.append(entry)    # the full tables follow in "specs"
                            continue
                        for k, v in zip(spec.get("glance_keys", []), m.get("glance", [])):
                            entry[k] = v
                    elif spec.get("kind") == "bandsaw":
                        r = bandsaw_round0(m)
                        rect = ((m.get("capacity_mm") or {}).get("0") or {}).get("rect")
                        angles = [a for a in (m.get("capacity_mm") or {}) if a != "0"]
                        entry["round_capacity"] = f"Ø{inch_cap(m, r)} ({r:g} mm)" if r else None
                        entry["rectangular_capacity"] = f"{inch_frac(rect[0])} × {inch_frac(rect[1])} ({rect[0]:g} × {rect[1]:g} mm)" if rect else None
                        entry["miter_angles"] = [a.replace("+", "+") + "°" for a in angles] or None
                        entry["motor"] = hp_range(m.get("main_motor_kw"))
                        entry["blade_speed"] = rng(m.get("blade_speed_m_min"), lambda x: x * 3.2808, "ft/min", "m/min")
                        if m.get("feed_length_mm"):
                            entry["feed_per_stroke"] = f"{inch_frac(m['feed_length_mm'])} ({m['feed_length_mm']:g} mm)"
                        if spec.get("voltage"):
                            entry["voltage"] = spec["voltage"]
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
                ci = f.get("card_image")
                thumb = (ci.get("thumb") or ci.get("small")) if ci else None
                # sharp photos for the finder's cards (the owner, Nov 7 2026: the thumbnails looked blurry): the family's
                # card photo up to 800 px, and a model's own photo when the gallery has one named after it ('b-36' for B 36)
                def card_img(name):
                    if not name or name not in manifest:
                        return None
                    x = img(name, max_w=800)
                    return {"src": x["small"], "srcset": x["srcset"], "alpha": x["alpha"]}
                fam_img = card_img(ci.get("name")) if ci else None
                gallery = [k for k in (f.get("images") or []) if isinstance(k, str) and k in manifest]
                for m in models:
                    k = model_photo(m["name"], gallery)
                    if k:
                        m["img"] = card_img(k)
                brand = site.get("brands", {}).get(f.get("brand"), {})
                pdf = f.get("pdf") if isinstance(f.get("pdf"), dict) else None
                strip = lambda x: html_mod.unescape(re.sub(r"<[^>]+>", "", x)) if isinstance(x, str) else ""
                items.append({
                    "id": f["id"], "name": f["name"], "short": f["short"], "models_label": f.get("models_label", ""),
                    "brand": brand.get("name") or (page.get("brand") or {}).get("name", ""), "line": brand.get("line"),
                    "category": g["title"], "page_title": page["h1"], "page": page["slug"], "page_nav": page.get("nav_label") or "",
                    "href": f"{page['slug']}#{f['id']}",
                    "headline": f.get("headline", ""), "summary": strip(f.get("summary", "")),
                    "features": [strip(x) for x in f.get("features", [])],
                    "optional": [strip(x) for x in (f.get("optional") or []) if isinstance(x, str)],
                    "automation": f.get("group"), "models": models, "image": thumb, "img": fam_img,
                    "pdf": pdf.get("file") if pdf else None,
                    "specs": ai_index.table_rows(spec) or None,
                    "caps": ai_index.family_caps(f, model_single, bandsaw_round0),
                })
    return items


def ai_pages(pages, families):
    """Every page for the finder: title, description, introduction, key points, questions and answers, photo, and the
    words of the page (and of the PDF brochures) that the product entries do not already hold."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import ai_index
    fam_words = {}
    for f in families:
        txt = " ".join([f["name"], f["short"], f["models_label"], f["category"], f["headline"], f["summary"]] + f["features"] + f["optional"]
                       + [m["name"] for m in f["models"]] + [" ".join(r) for t in (f.get("specs") or []) for r in t["rows"]])
        fam_words[f["id"]] = set(ai_index.words(txt))
    by_page = {}
    for f in families:
        by_page.setdefault(f["page"], set()).update(fam_words[f["id"]])
    out = []
    for p in pages:
        if p.get("noindex") or p.get("draft"):
            continue
        fp = os.path.join(DIST, p["slug"] + ".html")
        html = open(fp, encoding="utf-8").read() if os.path.exists(fp) else ""
        known = by_page.get(p["slug"], set())
        extra = []
        for w in ai_index.page_words(html):
            if w not in known and w not in extra:
                extra.append(w)
        hero = p.get("hero_image")
        im = img(hero) if isinstance(hero, str) and hero in manifest else None
        out.append({
            "slug": p["slug"], "nav": p.get("nav_label") or "", "h1": re.sub(r"<[^>]+>", "", p.get("h1") or ""),
            "desc": p.get("meta_description") or "", "intro": re.sub(r"<[^>]+>", "", p.get("intro") or ""),
            "points": [re.sub(r"<[^>]+>", "", x) if isinstance(x, str) else re.sub(r"<[^>]+>", "", x.get("text") or "") for x in (p.get("hero_points") or [])],
            "faq": [[re.sub(r"<[^>]+>", "", q.get("q", "")), re.sub(r"<[^>]+>", "", q.get("a", ""))] for q in (p.get("faq") or []) if isinstance(q, dict)],
            "kind": p.get("template", "page.html").replace(".html", ""), "hub": bool(p.get("subpages")),
            "image": (im.get("thumb") or im.get("small")) if im else None,
            "words": " ".join(extra[:400]),
        })
    pdfs = {}
    users = {}
    for f in families:
        if f.get("pdf"):
            users.setdefault(f["pdf"], set()).update(fam_words[f["id"]])
    for file, known in users.items():
        src = os.path.join(ROOT, "src", file)
        if os.path.exists(src):
            pdfs[file] = " ".join(sorted(w for w in ai_index.pdf_words(src) if w not in known))
    return out, pdfs


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


def social_images():
    """every page shares with a 1200 × 630 preview image (og:image = img/social/<slug>.jpg): WhatsApp, Facebook and the other
    chat and social apps show no picture when it is missing. make_social draws the cards that are missing or whose photo,
    heading or tagline changed (and removes the cards of pages that are gone) before the images are copied."""
    import subprocess
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "tools", "make_social.py"), "--stale"],
                       check=True, capture_output=True, text=True)
    made = [ln.split()[0] for ln in r.stdout.splitlines() if ln.endswith(tuple("0123456789"))]
    if made:
        print(f"social images: drew {len(made)} — " + ", ".join(made[:6]) + (" …" if len(made) > 6 else ""))
    pdir, sdir = os.path.join(ROOT, "content", "pages"), os.path.join(ROOT, "src", "img", "social")
    slugs = [json.load(open(os.path.join(pdir, fn), encoding="utf-8"))["slug"] for fn in sorted(os.listdir(pdir))
             if fn.endswith(".json") and not fn.startswith("_")]
    still = [s for s in slugs if not os.path.exists(os.path.join(sdir, s + ".jpg"))]
    if still:
        raise SystemExit(f"no social image for: {', '.join(still)}")


def main():
    social_images()
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
    for extra in ("robots.txt", "llms.txt", ".htaccess", ".user.ini", "quote.php", "quote-mail.php", "mail-lib.php", "ask.php", "ai-config.sample.php", "form-config.sample.php",
                  "bf-quote.php", "bf-config.sample.php",
                  "favicon.ico", "favicon.svg", "site.webmanifest", INDEXNOW_KEY + ".txt", ".cpanel.yml", ".deploy-hostpapa.sh"):
        s = os.path.join(ROOT, "src", "root", extra)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(DIST, extra))
    pages = []
    pdir = os.path.join(ROOT, "content", "pages")
    loaded = [json.load(open(os.path.join(pdir, fn), encoding="utf-8")) for fn in sorted(os.listdir(pdir)) if fn.endswith(".json") and not fn.startswith("_")]
    apply_extra_groups(loaded)
    refresh_pdf_sizes(loaded)
    apply_family_pdfs(loaded)
    brand_all_pdf_labels(loaded)
    load_catalogue_tons(loaded)
    by_slug_all = {p["slug"]: p for p in loaded}
    link_hero_points(by_slug_all)
    # cross-selling links at the foot of every product page — the machines its buyers also use (content/related.json, the owner,
    # Oct 31 2026); the section cards below drop the links they already cover
    rel = json.load(open(os.path.join(ROOT, "content", "related.json"), encoding="utf-8"))
    for slug, targets in rel["pages"].items():
        if slug not in by_slug_all:
            raise SystemExit(f"content/related.json: no page {slug}")
        for t in targets:
            if t not in by_slug_all or t not in rel["labels"]:
                raise SystemExit(f"content/related.json: {slug} → {t}: no such page or no label")
        by_slug_all[slug]["related_pages"] = [{"href": t + ".html", "label": rel["labels"][t]} for t in targets if t != slug]
    for hub in [p for p in loaded if p.get("hub_compact") and p.get("subpages")]:   # short hubs list every family by brand
        hub["lineup_spec"] = hub_lineup_spec(hub, by_slug_all)
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
                    p["section"] = {"hub": hub_card(hub, hub_info, g, groups, p, alt, by_slug_all), "label": (g["label"] + " band saws") if g.get("label") else hub.get("section_label", "Rebar machinery"),
                                    "line": g.get("line"), "brand": g.get("brand"), "line_name": g.get("label"),
                                    "pages": [dict(m, current=(m["slug"] == p["slug"])) for m in g["members"]], "alt": alt,
                                    "related_title": hub.get("related_title_" + (g.get("line") or ""), None)}
                    if hub.get("article") and not p.get("article") and not p.get("related_article"):   # the hub's buying guide, linked under the hero
                        p["related_article"] = {"href": f"{hub['slug']}.html#{hub.get('article_id') or 'buying-guide'}", "label": hub.get("article_title") or "Buying guide"}
                    covered = {m["href"] for m in g["members"]} | {hub["slug"] + ".html"} | ({alt["href"]} if alt else set())
                    p["related_pages"] = [r for r in p.get("related_pages", []) if r["href"] not in covered]   # cards already link to these
    # the related links ("More … from NovoTech", "Machines in this article") show a small picture of the page they open (the owner,
    # Oct 31 2026): the target page's hero image
    for p in loaded:
        for key in ("related_pages", "related"):
            items = p.get(key)
            if not isinstance(items, list):
                continue
            out = []
            for r in items:
                if isinstance(r, dict) and r.get("href"):
                    t = by_slug_all.get(r["href"].split("#")[0].replace(".html", "")) or {}
                    k = t.get("hero_image") or t.get("image")
                    r = dict(r, image=img(k) if isinstance(k, str) and k in manifest else None)
                out.append(r)
            p[key] = out
    CATALOG.update(build_catalog(loaded))
    nav_preview = build_nav_preview(loaded)
    json.dump(nav_preview, open(os.path.join(DIST, "nav-preview.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    # the Products page shows each category's sub-pages, sections and products with their photos, the same as the menu (the
    # owner, Nov 7 2026: every main page and hub on the Products page, their sub-branches' photos under the pointer)
    for c in CATALOG.values():
        c["subs"] = (nav_preview.get(re.sub(r"\.html$", "", c["href"].split("#")[0])) or {}).get("c") or []
    shown = set()
    for p in loaded:
        if p.get("template") in SITE_TEMPLATES:
            continue
        for g in p.get("groups", []):
            shown |= {(g.get("family_set") or p.get("family_set"), f) for f in g.get("families", []) if isinstance(f, str)}
    SHOWN_FAMILIES[0] = len(shown)
    PDF_INDEX.update(build_pdf_index(loaded))
    # the Black Friday popup leads to the sale page once that page is published (not a draft): the "deals_url" of the promo
    bf_live = [p["slug"] for p in loaded if p.get("template") == "black-friday.html" and not p.get("draft")]
    if site.get("promo") and bf_live:
        site["promo"]["deals_url"] = bf_live[0]
    ALL_PAGES.update(by_slug_all)
    for p in loaded:   # where each family is shown, for the links of the Black Friday page's cards
        if p.get("subpages") or p.get("template") in SITE_TEMPLATES or p.get("template") == "black-friday.html":
            continue
        for g in p.get("groups", []):
            for f in g.get("families", []):
                if isinstance(f, str):
                    FAMILY_PAGE.setdefault((g.get("family_set") or p.get("family_set"), f), p["slug"])
    for page in loaded:
        html = render_page(page)
        if ARTIFACT:
            html = artifact_fragment(html, page)
        out = os.path.join(DIST, page["slug"] + ".html")
        open(out, "w", encoding="utf-8").write(html)
        pages.append(page)
        print(f"wrote {out} ({len(html)//1024} KB)")
    # draft pages (content/drafts/*.json): design candidates shown on the staging host only — noindex, not in the sitemap, nav or catalogue
    ddir = os.path.join(ROOT, "content", "drafts")
    if (STAGING or DRAFTS) and os.path.isdir(ddir):
        for fn in sorted(os.listdir(ddir)):
            if fn.endswith(".json") and not fn.startswith("_"):
                page = json.load(open(os.path.join(ddir, fn), encoding="utf-8"))
                page["draft"] = True
                html = render_page(page)
                out = os.path.join(DIST, page["slug"] + ".html")
                open(out, "w", encoding="utf-8").write(html)
                print(f"wrote {out} (draft, {len(html)//1024} KB)")
    # AI assistant catalogue (read by ask.php on the server and by the search panel in the browser)
    os.makedirs(os.path.join(DIST, "ai"), exist_ok=True)
    cat = ai_catalogue(PREPARED)
    ai_pg, ai_pdfs = ai_pages(PREPARED, cat)
    json.dump({"generated": datetime.date.today().isoformat(), "site": site["domain"], "families": cat, "pages": ai_pg, "pdfs": ai_pdfs,
               "contact": {"phone": site["phone"], "phone_tel": site["phone_tel"], "email": f"{site['email_user']}@{site['email_domain']}",
                           "hours": site["hours"], "address": site["address"]}},
              open(os.path.join(DIST, "ai", "catalogue.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"ai catalogue: {len(cat)} families, {len(ai_pg)} pages, {len(ai_pdfs)} brochures, "
          f"{os.path.getsize(os.path.join(DIST, 'ai', 'catalogue.json'))//1024} KB")
    # sitemap
    today = datetime.date.today().isoformat()
    # <lastmod> is the day the page's content file last changed in git (a date that is always "today" is ignored by Google)
    changed = {}
    try:
        import subprocess
        log = subprocess.run(["git", "log", "--format=%cs", "--name-only", "--", "content/pages"], cwd=ROOT, capture_output=True, text=True, timeout=30).stdout
        cur = None
        for line in log.splitlines():
            if not line.strip():
                continue
            if "/" not in line and line[:4].isdigit():
                cur = line.strip()
            elif cur and line.startswith("content/pages/"):
                changed.setdefault(os.path.basename(line)[:-5], cur)
    except Exception:
        pass
    def loc(p):
        return site["domain"] + "/" if p["slug"] == "index" else f"{site['domain']}/{p['slug']}"
    def prio(p):
        return "1.0" if p["slug"] == "index" else "0.9" if p.get("subpages") or p["slug"] == "products" else "0.5" if p["slug"] == "privacy-policy" else "0.8"
    def page_videos(p):
        """<video:video> entries for the page: the VideoObjects of its JSON-LD (the same videos the page embeds), so Google's
        video report finds them from the sitemap as it did on the old site (Nov 8 2026)."""
        fn = os.path.join(DIST, ("index" if p["slug"] == "index" else p["slug"]) + ".html")
        if not os.path.exists(fn):
            return ""
        out, seen = [], set()
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', open(fn, encoding="utf-8").read(), re.S):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            for o in data.get("@graph", []) if isinstance(data, dict) else []:
                if not isinstance(o, dict) or o.get("@type") != "VideoObject" or o.get("embedUrl") in seen or not o.get("thumbnailUrl"):
                    continue
                seen.add(o["embedUrl"])
                m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", o.get("duration") or "")
                secs = (int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)) if m else 0
                e = lambda x: html_lib.escape(str(x), quote=True)
                out.append("    <video:video><video:thumbnail_loc>" + e(o["thumbnailUrl"][0]) + "</video:thumbnail_loc>"
                           + "<video:title>" + e(o["name"][:100]) + "</video:title><video:description>" + e(o.get("description", o["name"])[:2048]) + "</video:description>"
                           + "<video:player_loc>" + e(o["embedUrl"]) + "</video:player_loc>"
                           + (f"<video:duration>{secs}</video:duration>" if 0 < secs <= 28800 else "")
                           + ("<video:publication_date>" + e(o["uploadDate"]) + "</video:publication_date>" if o.get("uploadDate") else "")
                           + "<video:family_friendly>yes</video:family_friendly></video:video>\n")
                if len(out) >= 100:
                    break
        return "".join(out)
    urls = "".join(f"  <url><loc>{loc(p)}</loc><lastmod>{changed.get(p['slug'], today)}</lastmod><changefreq>monthly</changefreq><priority>{prio(p)}</priority>\n{page_videos(p)}  </url>\n" for p in pages
                   if not p.get("noindex"))   # the page-not-found page stays out
    open(os.path.join(DIST, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n{urls}</urlset>\n')
    if STAGING:
        open(os.path.join(DIST, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    if MISSING_IMAGES:
        print(f"PREVIEW ONLY: {len(MISSING_IMAGES)} images missing, logo shown instead: " + ", ".join(sorted(MISSING_IMAGES)[:12]) + " …")
    if NO_HERO_NAME:
        print(f"WARNING: {len(NO_HERO_NAME)} small hero photos have no short name in content/hero_names.json: " + ", ".join(sorted(NO_HERO_NAME)))
    big = [f for f in glob.glob(os.path.join(ROOT, "src", "files", "**", "*.pdf"), recursive=True) if os.path.getsize(f) > 13_900_000]
    if big:     # the owner, Nov 9 2026: every brochure must fit in an e-mail
        print(f"WARNING: {len(big)} PDFs are too big to attach to an e-mail — python3 tools/pdf_email_fit.py: "
              + ", ".join(os.path.basename(f) for f in big))
    print("done", "(staging)" if STAGING else "")


if __name__ == "__main__":
    main()
