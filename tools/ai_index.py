"""Machine-finder index (dist/ai/catalogue.json), read by js/ai.js in the browser and by ask.php on the server.

The owner, Nov 7 2026: the AI search must know every product on the site, their descriptions and even what is in the
PDF brochures, and it must answer questions like "I want to roll 2-inch pipe to a 30-inch diameter" with a recommended
machine and the similar ones. So the index holds, for every product family:
  - what the product page shows: name, maker line, category, headline, summary, every feature and option, every row of
    every spec table, the model names;
  - the words of its PDF brochure that the page does not already use (so a search for a term found only in the PDF still
    finds the machine);
  - structured capacities per model ("caps"), parsed from the spec tables, that the finder compares with the sizes a
    visitor types: sheet and plate thickness, working length, force, minimum rolling diameter, tube and pipe size,
    bending radius (CLR), saw capacity, punching and shearing capacity of ironworkers, rebar size, laser power and bed,
    weight capacity of positioners and turning rolls, drilling capacity, and for section benders (angle rolls) every
    profile with its largest size and the minimum rolling diameter;
and for every page of the site its title, description and words, so questions about the company (warranty, financing,
delivery, location) find the right page.

All lengths are inches, forces US tons, weights lb, powers kW. Values come from the metric figures in brackets where a
cell has them (they are the manufacturers' own), otherwise from the inch figures.
"""
import html as html_mod
import os
import re

# ---------------------------------------------------------------------------------------------------- number parsing
GA = {3: .2391, 4: .2242, 5: .2092, 6: .1943, 7: .1793, 8: .1644, 9: .1495, 10: .1345, 11: .1196, 12: .1046, 13: .0897,
      14: .0747, 15: .0673, 16: .0598, 17: .0538, 18: .0478, 19: .0418, 20: .0359, 21: .0329, 22: .0299, 23: .0269,
      24: .0239, 25: .0209, 26: .0179, 27: .0164, 28: .0149, 29: .0135, 30: .0120}
NPS_OD = {"1/8": .405, "1/4": .54, "3/8": .675, "1/2": .84, "3/4": 1.05, "1": 1.315, "1-1/4": 1.66, "1-1/2": 1.9,
          "2": 2.375, "2-1/2": 2.875, "3": 3.5, "3-1/2": 4.0, "4": 4.5, "5": 5.563, "6": 6.625, "8": 8.625, "10": 10.75,
          "12": 12.75, "14": 14.0, "16": 16.0, "18": 18.0, "20": 20.0, "24": 24.0}
NUM = r"\d+-\d+/\d+|\d+/\d+|\d*\.\d+|\d+"


def num(s):
    """'1-1/2' → 1.5, '3/8' → 0.375, '.114' → 0.114, '1,300' → 1300"""
    s = s.strip().replace(",", "")
    m = re.fullmatch(r"(\d+)-(\d+)/(\d+)", s)
    if m:
        return int(m[1]) + int(m[2]) / int(m[3])
    m = re.fullmatch(r"(\d+)/(\d+)", s)
    if m:
        return int(m[1]) / int(m[2])
    return float(s)


def r3(x):
    return None if x is None else round(x, 3)


def mm_values(cell):
    """Numbers inside the '(… mm)' brackets of a cell, in order: '(Ø32 × 3 mm)' → [32, 3]; '(2.5 / 3 mm)' → [2.5, 3]."""
    out = []
    for grp in re.findall(r"\(([^()]*?)\s*mm\)", cell):
        out += [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", grp)]
    return out


def inch_values(cell):
    """Inch figures of a cell in order (metric brackets removed): 'Ø1-1/4″ × 11 ga' → [1.25]; '2-3/8 × 3/8″' →
    [2.375, 0.375]; '4′3″' → [51]; '10.1 ft · 121.3″' → [121.2, 121.3]."""
    c = re.sub(r"\([^()]*\)", " ", cell)
    out = []
    for ft, inch in re.findall(r"(\d+)′\s*(\d+(?:\.\d+)?)?″?", c):
        out.append(int(ft) * 12 + (float(inch) if inch else 0))
    c = re.sub(r"(\d+)′\s*(\d+(?:\.\d+)?)?″?", " ", c)
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*ft\b", c):
        out.append(float(m[1]) * 12)
    c = re.sub(r"(\d+(?:\.\d+)?)\s*ft\b", " ", c)
    # a run of numbers joined by × / – ending in ″: every number in the run is inches
    for m in re.finditer(r"((?:" + NUM + r")(?:\s*[×x–/-]\s*(?:" + NUM + r"))*)\s*″", c):
        out += [num(x) for x in re.findall(NUM, m[1])]
    return out


def gauge_values(cell):
    return [GA[int(g)] for g in re.findall(r"(\d+)\s*ga\b", cell) if int(g) in GA]


def thickness(cell):
    """Largest thickness in a capacity cell, inches: '12 ga / 11 ga (2.5 / 3 mm)' → 0.118; '1/4″ (6 mm)' → 0.236."""
    cell = re.sub(r"\S+″\s+offsets?\b[^,;]*", " ", cell)          # '20 ga — 1/2″ offsets to 90°': the offset is not a thickness
    mm = mm_values(cell)
    if mm:
        top = max(mm) / 25.4
    else:
        vals = inch_values(cell)
        top = max(vals) if vals else None
    ga = gauge_values(cell)
    if ga and (top is None or max(ga) >= top * 0.85):
        return max(ga)            # the gauge is the rating a buyer reads ('24 ga (0.7 mm)' is a 24 ga brake, not a 23 ga one)
    return top


def length(cell):
    """Working length, inches: first metric value, else the largest inch value."""
    mm = mm_values(cell)
    if mm:
        return mm[0] / 25.4
    vals = inch_values(cell)
    return max(vals) if vals else None


def tons(cell):
    m = re.search(r"([\d,]+(?:\.\d+)?)\s*US tons?", cell)
    if m:
        return float(m[1].replace(",", ""))
    m = re.search(r"([\d,]+(?:\.\d+)?)\s*kN", cell)
    return float(m[1].replace(",", "")) * 0.1124 if m else None


def pounds(cell):
    m = re.search(r"([\d,]+(?:\.\d+)?)\s*lb\b", cell)
    return float(m[1].replace(",", "")) if m else None


def kw_range(cell):
    vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", re.sub(r"\([^()]*\)", " ", cell.split("kW")[0]))]
    return [min(vals), max(vals)] if vals and "kW" in cell else None


def od_value(cell):
    """Largest tube or bar diameter in a cell, inches (first number of each metric group, or the largest Ø inch value)."""
    mm_groups = re.findall(r"\(([^()]*?)\s*mm\)", cell)
    if mm_groups:
        firsts = []
        for g in mm_groups:
            nums = [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", g)]
            if not nums:
                continue
            # 'Ø8 – 120' is a range → its top; 'Ø16, 19, … 76' a list → its largest; 'Ø32 × 3' is diameter × wall → the first
            if re.search(r"\d\s*[–-]\s*Ø?\d", g):
                firsts.append(max(nums[:2]))
            elif ", " in g:
                firsts.append(max(nums))
            else:
                firsts.append(nums[0])
        if firsts:
            return max(firsts) / 25.4
    vals = inch_values(cell)
    return max(vals) if vals else None


def ranges(cell):
    """'1.5 – 7.1″ (38 – 180 mm)' → [1.5, 7.1]; '9.8″ (250 mm)' → [None, 9.8]."""
    mm = mm_values(cell)
    if len(mm) >= 2 and re.search(r"\d\s*–\s*\d", cell):
        return [mm[0] / 25.4, mm[1] / 25.4]
    if mm:
        return [None, mm[0] / 25.4]
    vals = inch_values(cell)
    if len(vals) >= 2 and "–" in cell:
        return [vals[0], vals[1]]
    return [None, vals[0]] if vals else None


# ---------------------------------------------------------------------------------------- section-bender profiles
PROFILE = [  # row label → profile key used by the finder
    (r"^pipe", "pipe"), (r"^round tube", "rd_tube"), (r"^square tube", "sq_tube"), (r"^rectangular tube", "rect_tube"),
    (r"^flat bar.*(easy|flat)", "flat_easy"), (r"^flat bar.*(hard|edge)", "flat_hard"), (r"^square bar", "sq_bar"),
    (r"^round bar", "rd_bar"), (r"^angle.*(out)", "angle_out"), (r"^angle.*(in)", "angle_in"), (r"^(tee|t-bar)", "tee"),
    (r"^channel", "channel"), (r"^(i-beam|h-beam)", "beam"),
]


def section_size(profile, text):
    """Governing size (inches) of a section in a capacity cell: pipe → OD of the NPS size; tube and bar → OD or side;
    flat bar → [width, thickness]; angle → [leg, thickness]; channel / beam → depth."""
    t = text.strip()
    if profile == "pipe":
        m = re.search(r"NPS\s*(\d+-\d+/\d+|\d+/\d+|\d+)", t)
        return NPS_OD.get(m[1]) if m else None
    mm = mm_values(t)
    if profile in ("channel", "beam"):
        m = re.search(r"\((" + NUM + r")″\)", t)      # 'UPN 80 (3-1/8″)'
        if m:
            return num(m[1])
        return mm[0] / 25.4 if mm else (inch_values(t) or [None])[0]
    if profile in ("flat_easy", "flat_hard", "angle_out", "angle_in", "tee"):
        vals = [v / 25.4 for v in mm] if mm else inch_values(t)
        if len(vals) >= 2:
            return [vals[0], vals[-1]]
        return [vals[0], None] if vals else None
    if mm:
        rng = re.search(r"\(\s*Ø?\d[\d.]*\s*–\s*(\d[\d.]*)", t)   # 'Ø1-3/16 – 2-3/4 × 0.08″ (30 – 70 × 2 mm)' → 70
        return (float(rng[1]) if rng else mm[0]) / 25.4
    vals = inch_values(t)
    return vals[0] if vals else None


def section_points(profile, cell):
    """Points [size, min. rolling Ø] of a section-bender capacity cell, largest section first.
    'NPS 2 × .114″ → Ø39″ · NPS 1/2 × .091″ → Ø12″' (premium line) or '2 × 3/8″ (50 × 10 mm), min. Ø23.6″ (600 mm)'."""
    pts = []
    if "→" in cell:
        for part in cell.split(" · "):
            if "→" not in part:
                continue
            sec, d = part.split("→", 1)
            dv = inch_values(d)
            size = section_size(profile, sec.replace("*", ""))
            if size is not None and dv:
                pts.append([size, dv[0]])
    elif "min. Ø" in cell:
        sec, d = cell.split("min. Ø", 1)
        dmm = mm_values(d)
        dv = dmm[0] / 25.4 if dmm else (inch_values(d) or [None])[0]
        size = section_size(profile, sec.rstrip(", "))
        if size is not None and dv:
            pts.append([size, dv])
    out = []
    for s, d in pts:
        out.append([[r3(x) for x in s] if isinstance(s, list) else r3(s), r3(d)])
    return out


def tube_pipe(cell, caps):
    """Capacity written as a sentence: 'Round tube 1/2 – 2″, pipe 1/4 – 1-1/2″, square tube 1/2 – 1″',
    '2″ schedule 40 pipe (0.154″ wall)', 'Tube 1/2 – 3″ OD, pipe 1/2 – 2-1/2″ schedule 40', '1″ NPS pipe · Ø1-5/16″ × 11 ga'."""
    c = re.sub(r"\([^()]*\)", " ", cell)
    nps = re.findall(r"(" + NUM + r")″\s*(?:schedule 40|sch\.? ?40|NPS)", c, re.I)
    nps += re.findall(r"pipe\s+(?:" + NUM + r")\s*[–-]\s*(" + NUM + r")″", c, re.I)
    nps += re.findall(r"NPS\s*(" + NUM + r")", c)
    ods = [NPS_OD[x] for x in nps if x in NPS_OD]
    if ods:
        caps["nps_od"] = r3(max(ods + [caps.get("nps_od") or 0]))
    od = re.findall(r"tube[^,;·]*?(?:" + NUM + r")\s*[–-]\s*(" + NUM + r")″", c, re.I)
    od += re.findall(r"(?:" + NUM + r")\s*[–-]\s*(" + NUM + r")″\s*OD", c)
    od += re.findall(r"Ø(" + NUM + r")″", c)
    vals = [num(x) for x in od]
    if vals:
        caps["od"] = r3(max(vals + [caps.get("od") or 0]))
    return bool(ods or vals)


# ------------------------------------------------------------------------------------------------ capacity rules
def row_caps(label, cell, caps):
    """Fill caps from one spec-table cell of one model."""
    L = label.lower()
    c = cell.strip()
    if not c or c in ("—", "-", "–"):
        return
    # section benders (angle rolls, profile benders): profile → points
    if "→" in c or "min. Ø" in c:
        for rx, key in PROFILE:
            if re.search(rx, L):
                pts = section_points(key, c)
                if pts:
                    caps.setdefault("sec", {}).setdefault(key, [])
                    caps["sec"][key] += pts
                return
    # thickness of sheet / plate, mild steel
    if re.search(r"stainless", L):
        if re.search(r"capacity|thickness", L):
            v = thickness(c)
            if v:
                caps["thk_ss"] = r3(max(v, caps.get("thk_ss") or 0))
        return
    if re.search(r"alumin", L):
        return
    if c == "✓" and tons(label):                                   # heavy press brakes: tonnage rows ticked per model
        caps["ton"] = r3(max(tons(label), caps.get("ton") or 0))
        return
    if re.search(r"^(capacity|tube capacity|max\. bending capacity)$", L) and re.search(r"tube|pipe|\bOD\b|NPS|Ø", c, re.I):
        tube_pipe(c, caps)
        if "Ø" in c and not re.search(r"tube|pipe|NPS", c, re.I):  # automatic cold saws: 'Ø1-3/4″ – 4″ … / Ø1/2″ – 2-1/2″'
            v = od_value(c.split(" / ")[0])
            if v:
                caps["rnd"] = r3(max(v, caps.get("rnd") or 0))
        return
    if re.search(r"capacity", L) and "Ø" in c and re.search(r"mild steel", L):   # 'Capacity, mild steel | Ø1-3/4″ – 4″ …'
        v = od_value(c.split(" / ")[0])
        if v:
            caps["rnd"] = r3(max(v, caps.get("rnd") or 0))
        return
    if re.search(r"^(cutting|shearing|rolling|bending|beading|seaming)? ?capacity(, mild steel| × width| \(mild steel\))?$|"
                 r"^capacity, mild steel|^max\.? thickness, mild steel|^max\. plate thickness — mild steel|"
                 r"^plate thickness|^sheet thickness|^material thickness|^coil thickness|^part thickness|^workpiece thickness|"
                 r"^rolling capacity|^shear / brake / roll capacity|^bending and shearing capacity|"
                 r"^max\. recommended thickness|^plate & tube thickness|^welding thickness|^capacity, length × mild steel|"
                 r"^max tube wall thickness", L) and not re.search(r"^pre-bend", L) and not re.search(r"Ø|\btube\b|\bpipe\b|\bOD\b", c):
        if re.search(r"capacity, length ×|capacity × width", L):    # '2 ft × 16 ga (625 × 1.6 mm)', '16 ga × 52″ (1.5 × 1,320 mm)'
            mm = mm_values(c)
            if len(mm) >= 2:
                v, ln = min(mm[:2]) / 25.4, max(mm[:2]) / 25.4
            else:
                parts = c.split("×", 1)
                vals = sorted(x for x in [thickness(p) for p in parts] + [length(p) for p in parts] if x)
                v, ln = (vals[0], vals[-1]) if len(vals) >= 2 else (None, None)
            if ln:
                caps["len"] = r3(max(ln, caps.get("len") or 0))
        elif re.search(r"wall thickness", L):
            v = thickness(c)
            if v:
                caps["wall"] = r3(max(v, caps.get("wall") or 0))
            return
        elif re.search(r"alumin|stainless|copper|brass", c, re.I):
            # one cell, several materials: '24 ga (0.7 mm) steel, 0.032″ (0.8 mm) aluminum' — the mild-steel figure is the
            # rating, the others are kept apart (a 22 ga steel job must not pass on the aluminum number)
            v = None
            for seg in re.split(r"[,;]|\s[—–-]\s", c):
                sv = thickness(seg)
                if not sv:
                    continue
                if re.search(r"stainless", seg, re.I):
                    caps["thk_ss"] = r3(max(sv, caps.get("thk_ss") or 0))
                elif re.search(r"alumin", seg, re.I):
                    caps["thk_al"] = r3(max(sv, caps.get("thk_al") or 0))
                elif re.search(r"copper|brass", seg, re.I):
                    continue
                else:
                    v = max(v or 0, sv)
            if v is None and not re.search(r"steel", c, re.I) and not re.search(r"mild steel", L):
                return
        else:
            v = thickness(c)
        if v and v < 6:
            # plate rolls: the capacity with pre-bending is the rating; without pre-bending is kept apart
            key = "thk_np" if re.search(r"no pre-bend", L) else "thk"
            caps[key] = r3(max(v, caps.get(key) or 0))
        return
    if re.search(r"bending width × thickness", L):                  # 'Bending width × thickness | 24″ (610 mm) × 5/32″ (4 mm)'
        parts = c.split("×")
        if len(parts) >= 2:
            ln, v = length(parts[0]), thickness(parts[1])
            if ln:
                caps["len"] = r3(max(ln, caps.get("len") or 0))
            if v:
                caps["thk"] = r3(max(v, caps.get("thk") or 0))
        return
    # working length / width
    if re.search(r"^(cutting length|max\.? shearing length|max shearing length|bending length|working length|working width|"
                 r"max\. bending width|bending edge length|max\. grooving length|max shearing width|cutting width|"
                 r"planing width|max\. bevel length, mild steel|max\. bevel length, any material|seaming length|"
                 r"max\. edge length|working width, max)", L):
        v = length(c)
        if v:
            caps["len"] = r3(max(v, caps.get("len") or 0))
        return
    # force
    if re.search(r"^(bending|press|punching|hydraulic|max\.?|crimping|clamping)? ?force$|^force$|^max\. force|^lifting force", L):
        v = tons(c)
        if v:
            caps["ton"] = r3(max(v, caps.get("ton") or 0))
        return
    # minimum rolling diameter of plate rolls
    if re.search(r"^min\.? rolling (ø|diameter)", L):
        mm = mm_values(c)
        v = (mm[0] / 25.4) if mm else (inch_values(c) or [None])[0]
        if v:
            caps["min_d"] = r3(v)
        return
    # bending radius (CLR)
    if re.search(r"clr|centreline radius|bending radius", L):
        rg = ranges(c)
        if rg:
            lo, hi = rg
            if "min" in L and lo is None:
                lo, hi = hi, None
            old = caps.get("clr") or [None, None]
            caps["clr"] = [r3(min(x for x in (lo, old[0]) if x is not None)) if (lo or old[0]) else None,
                           r3(max(x for x in (hi, old[1]) if x is not None)) if (hi or old[1]) else None]
        return
    # pipe (NPS) capacity of tube and pipe benders
    if re.search(r"gas pipe|sch\. ?40|^pipe dies|^pipe size", L):
        sizes = re.findall(r"(\d+-\d+/\d+|\d+/\d+|\d+)(?=[\s,″]|$)", re.sub(r"\([^()]*\)", " ", c))
        ods = [NPS_OD[s] for s in sizes if s in NPS_OD]
        if ods:
            caps["nps_od"] = r3(max(ods + [caps.get("nps_od") or 0]))
        return
    # tube / bar OD capacity (tube benders, notchers, tube lasers, polishers, tube-end machines)
    if re.search(r"^(max\. tube capacity|tube capacity|steel tube|mild steel tube|max\. bending capacity|tube diameter|"
                 r"round tube|bar and tube ø|pipe and bar ø|tube ø|tube size|notching capacity|work diameter|"
                 r"max\. turning diameter|swing over bed|max\. swing · clamping ø|bar capacity)", L):
        if re.search(r"work diameter", L):
            rg = ranges(c)
            if rg:
                caps["work_d"] = [r3(x) for x in rg]
            return
        if re.search(r"turning diameter|swing over bed|swing · clamping", L):
            v = od_value(c)
            if v:
                caps["swing"] = r3(max(v, caps.get("swing") or 0))
            return
        if "NPS" in c or re.search(r"schedule 40|sch\.? ?40", c, re.I):
            tube_pipe(c, caps)
        v = od_value(c.split(" · ")[-1] if "NPS" in c else c)
        if v:
            caps["od"] = r3(max(v, caps.get("od") or 0))
        return
    if re.search(r"^square tube$|^profile size", L):
        v = od_value(c)
        if v:
            caps["sq"] = r3(max(v, caps.get("sq") or 0))
        return
    # saws: round and rectangular capacity at 90°
    if re.search(r"^round( pipe| bar)?(, | — )90°|^cutting capacity — round|^round, 90° and 45°|^round$", L):
        v = od_value(c.split(" / ")[0])
        if v:
            caps["rnd"] = r3(max(v, caps.get("rnd") or 0))
        return
    if re.search(r"^(rectangular|square)(, | — )90°|^cutting capacity — square|^capacity at 90°|^rectangular, 90°", L):
        vals = [v / 25.4 for v in mm_values(c.split(" at 45")[0])] or inch_values(c)
        if "square" in L and re.search(r"\d″?\s*–\s*\d", c) and len(vals) >= 2:   # 'Cutting capacity — square | 3/8″ – 2″ (10 – 50 mm)'
            vals = [max(vals[:2]), max(vals[:2])]
        if len(vals) >= 2:
            w, h = sorted(vals[:2], reverse=True)
            old = caps.get("rect") or [0, 0]
            caps["rect"] = [r3(max(w, old[0])), r3(max(h, old[1]))]
        return
    # ironworkers and punching machines
    if re.search(r"^punching, (max\. thickness|larger hole|max\. ø)|^punching$", L):
        m = re.search(r"Ø(" + NUM + r")\s*×\s*(" + NUM + r")″", c)
        if m:
            caps.setdefault("punch", []).append([r3(num(m[1])), r3(num(m[2]))])
        return
    if re.search(r"^flat[- ]bar shear", L):
        vals = inch_values(c)
        if len(vals) >= 2:
            caps.setdefault("fbs", []).append([r3(vals[0]), r3(vals[-1])])
        elif vals and "thickness" in L:
            caps.setdefault("fbs", []).append([None, r3(vals[0])])
        return
    if re.search(r"^angle shear 90", L):
        vals = inch_values(c)
        if len(vals) >= 2:
            caps["ang"] = [r3(vals[0]), r3(vals[-1])]
        return
    if re.search(r"^bar shear", L):
        m = re.search(r"Ø(" + NUM + r")″", c)
        if m:
            caps["bar_rd"] = r3(num(m[1]))
        return
    # lasers
    if re.search(r"^laser (source )?power|^laser source$", L):
        v = kw_range(c)
        if v:
            caps["kw"] = v
        return
    if re.search(r"^working area|^sheet working area|^travel range x × y|^working area l × w", L):
        mm = mm_values(c)
        if len(mm) >= 2:
            caps["bed"] = [r3(max(mm[:2]) / 25.4), r3(min(mm[:2]) / 25.4)]
        return
    # weight capacity (positioners, turning rolls, tables, manipulators)
    if re.search(r"^(rated load|load, max|load per set|nominal load capacity|load, horizontal|max\. table load|"
                 r"table load, max|load capacity|max\. carriage load|max\. tube weight|max\. coil weight)", L):
        v = pounds(c)
        if v:
            caps["load"] = r3(max(v, caps.get("load") or 0))
        return
    # drilling
    if re.search(r"^drilling capacity", L):
        mm = mm_values(c)
        v = (mm[0] / 25.4) if mm else (inch_values(c) or [None])[0]
        if v:
            caps["drill"] = r3(max(v, caps.get("drill") or 0))
        return


def family_caps(f, model_single=None, bandsaw_round0=None):
    """caps for every model of a family, in the order of f['specs']['models']."""
    spec = f.get("specs") or {}
    names = [m["name"] for m in spec.get("models", [])]
    out = {n: {} for n in names}
    kind = spec.get("kind")
    if kind == "bandsaw":
        for m in spec["models"]:
            cap = (m.get("capacity_mm") or {})
            c0 = cap.get("0") or {}
            r = (bandsaw_round0(m) if bandsaw_round0 else c0.get("round")) or c0.get("round")
            d = out[m["name"]]
            if r:
                d["rnd"] = r3(r / 25.4)
            if c0.get("rect"):
                d["rect"] = [r3(max(c0["rect"]) / 25.4), r3(min(c0["rect"]) / 25.4)]
            miters = [a for a in cap if a != "0" and (cap[a] or {}).get("round")]
            if miters:
                d["miter"] = sorted({abs(int(a.replace("+", ""))) for a in miters if re.fullmatch(r"[+-]?\d+", a)})
                d["rnd45"] = r3(max((cap[a] or {}).get("round") or 0 for a in miters if a.endswith("45")) / 25.4) \
                    if any(a.endswith("45") for a in miters) else None
    elif kind in ("bending", "cutting"):
        for i, m in enumerate(spec["models"]):
            d = out[m["name"]]
            if model_single:
                b45, b65 = model_single(spec, i, grade="45"), model_single(spec, i, grade="65")
                if b45:
                    d["bar45"] = b45
                if b65:
                    d["bar65"] = b65
                if spec.get("cutting_capacity"):
                    c65 = model_single(spec, i, "cutting_capacity", grade="65")
                    if c65:
                        d["cut65"] = c65
            d["op"] = "cut" if kind == "cutting" else "bend"
    for t in spec.get("tables") or []:
        for r in t.get("rows", []):
            for name, cell in zip(t.get("models") or [], r.get("cells") or []):
                if name in out and isinstance(cell, str):
                    row_caps(r["label"], cell, out[name])
    # a model with no table of its own (a family table listing other names) gets nothing — fine
    res = []
    for n in names:
        d = {k: v for k, v in out[n].items() if v not in (None, [], {})}
        if "sec" in d:     # largest section first for each profile
            for k in d["sec"]:
                d["sec"][k].sort(key=lambda p: -(p[0][0] if isinstance(p[0], list) else p[0]))
        res.append(d)
    return res


# ------------------------------------------------------------------------------------------------- text and tokens
STOP = set("""a an and are as at be by for from has have in is it its of on or that the this to with without was were will
can not no your you our we their they them than then there these those into per each other more most also only such may
which when where who how what all any both via up out over under after before about above below between while""".split())


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return html_mod.unescape(s)


def words(text):
    """Lowercase search words of a text (letters and digits, model codes kept whole)."""
    t = clean(text).lower().replace("″", '"')
    return [w.strip("-./") for w in re.findall(r"[a-z0-9][a-z0-9\-./]*", t) if len(w.strip("-./")) > 1]


def table_rows(spec):
    """Spec tables in a compact form: [{"title", "models", "rows": [[label, cell, cell…]]}]."""
    out = []
    if not spec:
        return out
    for t in spec.get("tables") or []:
        rows = [[(r.get("label") or "") + (f" ({r['sub']})" if r.get("sub") else "")] + [c if isinstance(c, str) else str(c) for c in r.get("cells") or []]
                for r in t.get("rows", [])]
        out.append({"title": t.get("title") or "", "models": t.get("models") or [], "rows": rows})
    return out


def pdf_words(path):
    """Unique words of a PDF brochure (PyMuPDF), or an empty set."""
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            return set()
    try:
        doc = fitz.open(path)
        text = " ".join(page.get_text() for page in doc)
        doc.close()
    except Exception:
        return set()
    return {w for w in words(text) if w not in STOP and not re.fullmatch(r"[\d.\-/]+", w) and 2 < len(w) < 30}


def page_words(html):
    """Words of a rendered page's main content (header, menu, footer, scripts and the finder panel left out)."""
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
    body = m.group(1) if m else html
    body = re.sub(r"<(script|style|svg|form)[^>]*>.*?</\1>", " ", body, flags=re.S)
    body = re.sub(r'<div class="ai-panel".*', " ", body, flags=re.S)
    return [w for w in words(body) if w not in STOP]
