#!/usr/bin/env python3
"""NovoTech premium line data library: unit conversions and table builders over the parsed NovoTech NovoTech premium line catalogue.

Sources (outside the repository):
  /home/claude/sahinler/tables.json        spec tables + capacity charts parsed from the imperial NovoTech catalogue
                                            (tools/sahinler_tables.py over /home/claude/sahinler/catalogue/sahinler-2027.pdf)
  /home/claude/sahinler/orig/pg-NN.txt     OCR of the manufacturer's metric pages (used for the nominal metric values)
  tools/src-images/sahinler/               logo-free photos exported by tools/sahinler_photos.py

Catalogue cells are imperial; every converter returns 'imperial (metric)'.  Thin sheet in gauge and plate in common
fractions map back to the manufacturer's nominal metric capacities (FRAC_MM); roll, shaft, throat and table dimensions are
rounded to 5 mm, machine dimensions to 50 mm, weights to 5/10 kg and motors to the kW sizes NovoTech premium line uses.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open("/home/claude/sahinler/tables.json", encoding="utf-8"))
CHARTS = T.get("charts", {})

# ------------------------------------------------------------------ conversions
GAUGE_MM = {"22 ga": 0.8, "20 ga": 1.0, "18 ga": 1.2, "16 ga": 1.5, "14 ga": 2.0, "12 ga": 2.5, "11 ga": 3.0, "10 ga": 3.5, "8 ga": 4.0, "7 ga": 4.5}
FRAC_MM = {"1/8": 3, "3/16": 5, "1/4": 6, "5/16": 8, "3/8": 10, "7/16": 11, "1/2": 12, "9/16": 15, "5/8": 16, "11/16": 18, "3/4": 19, "13/16": 20,
           "7/8": 22, "1": 25, "1-1/8": 30, "1-1/4": 32, "1-3/8": 35, "1-1/2": 38, "1-5/8": 40, "1-3/4": 45, "2": 50, "2-1/8": 55, "2-1/4": 57,
           "2-3/8": 60, "2-1/2": 65, "2-3/4": 70, "3": 75, "3-1/8": 80, "3-3/8": 85, "3-1/2": 90}
KW_STD = [0.24, 0.37, 0.55, 0.75, 1, 1.1, 1.47, 1.5, 2, 2.2, 2.25, 3, 3.75, 4, 4.75, 5.5, 7.5, 8.75, 9, 11, 15, 16.5, 18.5, 20, 22, 23.5, 30, 31.5,
          37, 38.5, 45, 47, 52, 55, 63, 70, 73, 75, 77, 90, 110, 123, 132, 150, 160, 170, 180]


def fx(s):
    return s.replace("⁄", "/").replace("″", "").replace("″", "").strip()


def frac_mm(v):
    """'1-1⁄8″' → 30, '8 ga' → 4, '13⁄16″' → 20; None if unknown."""
    v = fx(v).rstrip("*").strip()
    if v in GAUGE_MM:
        return GAUGE_MM[v]
    if v in FRAC_MM:
        return FRAC_MM[v]
    return None


def fmt(v):
    return f"{v:g}"


def cap(cell):
    """Plate / sheet capacity: '1-1⁄8″' → '1-1/8″ (30 mm)'; '8 ga' → '8 ga (4 mm)'; '—' stays."""
    c = cell.strip()
    if c in ("—", "-", ""):
        return "—"
    star = "*" * (len(c) - len(c.rstrip("*")))
    base = c.rstrip("*")
    mm = frac_mm(base)
    txt = fx(base) + ("″" if "ga" not in base else "") + star
    return f"{txt} ({fmt(mm)} mm)" if mm is not None else txt


def mm5(inch, step=5):
    return round(float(inch) * 25.4 / step) * step


def inch(cell, step=5, override=None):
    """'11.0' → '11″ (280 mm)'; '2.4 / 3.1' → '2.4″ / 3.1″ (60 / 80 mm)'."""
    parts = [p.strip() for p in cell.split("/")]
    try:
        vals = [float(p) for p in parts]
    except ValueError:
        return cell
    mm = override if override else [mm5(v, step) for v in vals]
    ins = " / ".join(fmt(v) + "″" for v in vals)
    return f"{ins} ({' / '.join(fmt(m) for m in mm)} mm)"


def dims(cell):
    parts = [p.strip() for p in cell.split("×")]
    try:
        vals = [float(p) for p in parts]
    except ValueError:
        return cell
    mm = [round(v * 25.4 / (50 if v * 25.4 >= 1000 else 10)) * (50 if v * 25.4 >= 1000 else 10) for v in vals]
    return f"{' × '.join(fmt(v) for v in vals)}″ ({' × '.join(f'{m:,}' for m in mm)} mm)"


def weight(cell):
    m = re.match(r"\s*([\d,]+)", cell)
    if not m:
        return cell
    cell = m.group(1)
    try:
        lb = float(cell.replace(",", ""))
    except ValueError:
        return cell
    kg = lb / 2.20462
    kg = round(kg / 5) * 5 if kg < 2000 else round(kg / 10) * 10
    return f"{cell} lb ({kg:,.0f} kg)"


def kw(hp):
    k = float(hp) / 1.341
    return min(KW_STD, key=lambda s: abs(s - k))


def motor(cell):
    """'22' → '22 HP (16.5 kW)'; '4.0 + 2.0' → '4 + 2 HP (3 + 1.5 kW)'; '0.9 – 1.1' → '0.9 – 1.1 HP (0.7 – 0.85 kW)'."""
    c = cell.replace("-", "–")
    sep = " + " if "+" in c else (" – " if "–" in c else None)
    parts = [p.strip() for p in (c.split(sep) if sep else [c])]
    try:
        vals = [float(p) for p in parts]
    except ValueError:
        return cell
    kws = [kw(v) for v in vals]
    if sep == " – " and len(vals) == 2:        # two-speed motor: catalogue ratio 0.7 / 0.85 kW
        kws = [0.7, 0.85] if vals == [0.9, 1.1] else kws
    j = sep or ""
    return f"{j.join(fmt(v) for v in vals)} HP ({j.join(fmt(k) for k in kws)} kW)"


def speed(cell):
    """ft/min → m/min: '4.9 – 16' → '4.9 – 16 ft/min (1.5 – 5 m/min)'."""
    c = cell.replace("-", "–")
    parts = [p.strip() for p in c.split("–")]
    try:
        vals = [float(p) for p in parts]
    except ValueError:
        return cell
    m = [round(v * 0.3048 * 2) / 2 for v in vals]
    return f"{' – '.join(fmt(v) for v in vals)} ft/min ({' – '.join(fmt(x) for x in m)} m/min)"


def ins(cell):
    """in/s → mm/s: '0.35 / 0.20 / 0.39' → '0.35 / 0.20 / 0.39 in/s (9 / 5 / 10 mm/s)'."""
    parts = [p.strip() for p in cell.split("/")]
    mm = []
    for p in parts:
        try:
            mm.append(f"{round(float(p) * 25.4):g}")
        except ValueError:
            mm.append("—")
    return f"{cell} in/s ({' / '.join(mm)} mm/s)"


def psi(cell):
    try:
        v = float(cell.replace(",", ""))
    except ValueError:
        return cell
    return f"{cell} psi ({round(v / 14.504 / 5) * 5:g} bar)"


def tons(metric, us):
    return f"{us} US tons ({metric} t)"


def wl(ft_cell, in_cell):
    ft = ft_cell.replace("FT", "ft").strip()
    try:
        mm = round(float(in_cell) * 25.4 / 10) * 10
    except ValueError:
        return f"{ft} · {in_cell}″"
    return f"{ft} · {in_cell}″ ({mm:,} mm)"


def litres(cell):
    try:
        v = float(cell)
    except ValueError:
        return cell
    return f"{cell} L ({v / 3.785:.0f} US gal)"


# ------------------------------------------------------------------ table access
def table(page, idx=0):
    return T[str(page)][idx]


def rows_of(tb):
    """{label: cells} with the stray caption rows removed and glued units split off the label."""
    out = {}
    for r in tb["rows"]:
        lab = re.sub(r"\s+(FT|in|HP|lb|ft/min|ft/m|ft/|ft|f|in/s|psi|rpm|°|L)$", "", r["label"]).strip()
        cells = [re.sub(r"^(in|min|ft|FT|HP|lb|psi|rpm|L|in/s|ft/min|°)\s+(?=\S)", "", c) for c in r["cells"]]
        if not all(cells) or lab.startswith(("Capacities", "N/mm", "thickness in", "OPTIONAL", "+ ", "available", "Mild-steel", "TECHNICAL", "STANDARD")):
            continue
        if lab in out:                       # Working length appears twice (FT and in): keep both
            lab = lab + " " + (r["unit"] or "in")
        out[lab] = cells
    return out


def build_rows(tb, spec, overrides=None):
    """spec: list of (label_prefix, new_label, sub, converter, key) → rows for manual_table.
    overrides: {(label_prefix, model): [mm…]} nominal metric values for the inch() converter."""
    R = rows_of(tb)
    rows = []
    for pref, new, sub, conv, key in spec:
        src = next((k for k in R if k.startswith(pref)), None)
        if src is None:
            continue
        cells = []
        for m, c in zip(tb["models"], R[src]):
            ov = (overrides or {}).get((pref, m))
            if conv is inch and ov:
                cells.append(inch(c, override=ov))
            else:
                cells.append(conv(c) if conv else c)
        rows.append({"label": new, "sub": sub, "cells": cells, "key": key})
    return rows


def spec_table(tb, title, sub, spec, overrides=None):
    return {"title": title, "sub": sub, "models": list(tb["models"]), "rows": build_rows(tb, spec, overrides)}


def chart_table(page, machines, title, sub):
    """Section-bending capacity chart as a spec table: rows = profiles, cells = 'max section → min rolling Ø' lines."""
    ch = CHARTS[str(page)]
    idx = [ch["machines"].index(m) for m in machines]
    rows = []
    for r in ch["rows"]:
        cells = []
        for i in idx:
            lines = [a.replace("⁄", "/") + (f" → Ø{d}" if d else "") for a, d in r["cells"][i]]
            cells.append(" · ".join(lines) if lines else "—")
        label = r["profile"]
        rows.append({"label": label, "sub": {"STD": "standard rolls", "OPT": "optional rolls", "STD*": "standard rolls*", "OPT*": "optional rolls*", "OPT**": "optional rolls**", "STD**": "standard rolls**"}.get(r["dies"], ""), "cells": cells, "key": False})
    return {"title": title, "sub": sub, "models": list(machines), "rows": rows}


CHART_NOTE = ("Capacity chart: each cell gives the largest section the machine rolls and, after the arrow, the minimum rolling diameter "
              "(outside) for it; a second value is a smaller section with its tighter minimum diameter. 'Standard rolls' profiles are rolled with the "
              "rolls supplied; 'optional rolls' need the matching roll set. * a special spacer may be needed · ** only with the beam-bending "
              "attachment. Beam sizes are European UPN / IPN / HEA / HEB designations with the nominal depth in inches. Based on 37,700 psi "
              "(260 N/mm²) yield-strength material; sizes are converted from the manufacturer's metric chart.")

NOTE_ROLLS = ("Plate bending capacities are for mild steel with a yield strength of 37,700 psi (260 N/mm²), given at a minimum rolling diameter of "
              "5× and of 1.5× the top roll diameter, without and with pre-bending. Capacities without pre-bending leave a flat end depending on "
              "diameter. Thin sheet in gauge; metric values in brackets are the manufacturer's nominal figures. Dimensions are overall L × W × H.")
NOTE_SIMPLE = "Capacities are for mild steel unless stated; metric values in brackets are the manufacturer's nominal figures. Dimensions are overall L × W × H."
VOLT = "Custom voltage: 208 V, 240 V, 480 V or 600 V 3-phase, or 240 V single-phase on models with a main motor of 2.2 kW (3 HP) or less"
BRAND_LINE = "NovoTech premium line — machines built in Turkey to NovoTech's specification with European hydraulic and electrical components, sold with a CSA-approved panel, 1-year warranty and parts and support from Mississauga, ON, Canada."
ORIGIN = {"title": "NovoTech premium line — made in Turkey", "text": "Built in Turkey to NovoTech's specification by a CE-certified metal-forming plant with European hydraulic and electrical components; inspected before shipping, with the same CSA panel, warranty and Mississauga, ON, Canada support as every machine we sell."}
PDF = None   # the supplier's catalogue carried its brand; NovoTech-format brochures per section are generated instead (tools/sahinler_brochures.py)


def premium_pdf(name):
    """The premium-line brochure entry for a page: premium-angle-rolls, premium-ironworkers, premium-shop-presses, premium-plate-rolls, premium-sheet-metal."""
    from sahinler_brochures import pdf_entry
    return pdf_entry(name)


def vid(i, title, dur):
    return {"id": i, "title": title, "duration": dur, "thumb": "video-" + i}


def yt_dur(mmss):
    """'4:07' → 'PT4M7S'."""
    p = [int(x) for x in mmss.split(":")]
    if len(p) == 3:
        return f"PT{p[0]}H{p[1]}M{p[2]}S"
    return f"PT{p[0]}M{p[1]}S"


# ------------------------------------------------------------------ NovoTech YouTube uploads (tools/novotech-youtube-videos.tsv)
_YT = {}
for _l in open(os.path.join(ROOT, "tools", "novotech-youtube-videos.tsv"), encoding="utf-8"):
    _p = _l.rstrip("\n").split("\t")
    if len(_p) == 3:
        _YT[_p[0]] = (_p[2].strip(), _p[1].strip())


def vids(*ids_titles):
    """vids("id", ("id", "nicer title"), …) → video dicts; the title defaults to the YouTube title."""
    out = []
    for it in ids_titles:
        i, title = (it, None) if isinstance(it, str) else it
        t, d = _YT[i]
        out.append(vid(i, title or t, yt_dur(d)))
    return out


def pair(a, b):
    """Two capacity cells (1.5× / 5× top roll Ø) → '1/2″ / 5/8″ (12 / 16 mm)'."""
    ma, mb = frac_mm(a), frac_mm(b)
    ta = fx(a).rstrip("*") + ("" if "ga" in a else "″")
    tb = fx(b).rstrip("*") + ("" if "ga" in b else "″")
    if ma is not None and mb is not None:
        return f"{ta} / {tb} ({fmt(ma)} / {fmt(mb)} mm)"
    return f"{ta} / {tb}"


GLANCE_ROLLS = ["working_length", "rolling_capacity", "roll_diameter", "motor", "weight"]


def plate_table(page, idx, title, sub, roll_label="Top & bottom roll Ø", side_label="Side roll Ø"):
    """4R HSS / 4R HS / 3R tables: working length, capacity pairs, rolls, motor, speed, dimensions, weight."""
    tb = table(page, idx)
    R = rows_of(tb)
    models = tb["models"]
    n = len(models)
    rows = [{"label": "Working length", "sub": "", "cells": [wl(R["Working length"][i], R["Working length in"][i]) for i in range(n)], "key": True}]
    np5 = next(k for k in R if k.startswith("No pre-bend") and "5×" in k)
    np15 = next(k for k in R if k.startswith("No pre-bend") and "1.5×" in k)
    wp5 = next(k for k in R if k.startswith("With pre-bend") and "5×" in k)
    wp15 = next(k for k in R if k.startswith("With pre-bend") and "1.5×" in k)
    rows.append({"label": "Rolling capacity, with pre-bend", "sub": "at min. rolling Ø ≥ 1.5× / 5× top roll Ø", "cells": [pair(R[wp15][i], R[wp5][i]) for i in range(n)], "key": True})
    rows.append({"label": "Rolling capacity, no pre-bend", "sub": "at min. rolling Ø ≥ 1.5× / 5× top roll Ø", "cells": [pair(R[np15][i], R[np5][i]) for i in range(n)], "key": False})
    for lab, new in ((roll_label, roll_label), (side_label, side_label), ("Top roll Ø", "Top roll Ø"), ("Bottom rolls Ø", "Bottom rolls Ø")):
        if lab in R and not any(r["label"] == new for r in rows):
            rows.append({"label": new, "sub": "", "cells": [inch(c) for c in R[lab]], "key": False})
    rows.append({"label": "Motor power", "sub": "", "cells": [motor(c) for c in R["Motor power"]], "key": False})
    rows.append({"label": "Rolling speed", "sub": "", "cells": [speed(c) for c in R["Rolling speed"]], "key": False})
    rows.append({"label": "Dimensions L × W × H", "sub": "", "cells": [dims(c) for c in R["Dimensions L × W × H"]], "key": False})
    rows.append({"label": "Weight", "sub": "", "cells": [weight(c) for c in R["Weight"]], "key": False})
    return {"title": title, "sub": sub, "models": list(models), "rows": rows}


def plate_spec(tables, note=NOTE_ROLLS):
    """manual_spec-style dict for plate rolls: glance = [working length, capacity (with pre-bend), top roll Ø, motor, weight]."""
    models, caps = [], {}
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        roll = rr.get("Top & bottom roll Ø") or rr.get("Top roll Ø") or rr.get("Largest roll Ø (cone end)")
        for i, m in enumerate(t["models"]):
            capc = rr.get("Rolling capacity, with pre-bend", rr.get("Rolling capacity", [""] * 99))[i]
            models.append({"name": m, "glance": [rr["Working length"][i], capc, roll[i] if roll else "—", rr["Motor power"][i], rr["Weight"][i]]})
            up = capc.split(" (")[0].split(" / ")[-1]
            mm = re.search(r"\(([^)]*)\)", capc)
            mm_up = (mm.group(1).split(" / ")[-1].replace(" mm", "") + " mm") if mm else ""
            ft = rr["Working length"][i].split(" ·")[0]
            caps[m] = f"rolls up to {up} ({mm_up}) × {ft}" if mm_up else f"{ft} working length"
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": GLANCE_ROLLS, "caps": caps, "note": note}


def simple_spec(tables, glance_keys, glance_from, note=NOTE_SIMPLE, caps=None):
    """glance_from: list of row labels whose cells fill the glance columns, in order."""
    models = []
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        for i, m in enumerate(t["models"]):
            models.append({"name": m, "glance": [rr[l][i] if l in rr else "—" for l in glance_from]})
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": glance_keys, "caps": caps or {}, "note": note}


def generic_table(page, idx, title, sub, spec, overrides=None):
    return spec_table(table(page, idx), title, sub, spec, overrides)
