#!/usr/bin/env python3
"""EUROSTAMP press brake tooling — punches, dies, holders and adapters made in Italy (Gragnano Trebbiense, Piacenza) since
1970, sold in Canada by NovoTech.  EUROSTAMP is the tooling brand NovoTech distributes: shown in the content, never in the
titles or slugs (those carry the clamping style the tools fit — Amada-Promecam / European, Trumpf, Wila, Bystronic, LVD,
American).

Sources (outside the repository, /home/claude/eurostamp/):
  pages.json                 the maker's web shop, one record per tool: type, height, angle, tip radius, V, load (t/m),
                             material, the drawing and the standard-lengths picture, the DXF link
  parsed/pricelist.json      the 2024 price lists (GENERAL, ESH, EUROGRIP) parsed by position (parsed/parse_pricelist.py):
                             the spec line, the description, the lengths, the out-of-production notes — prices are NOT kept
  parsed/catalog.json        the IT-EN catalogue parsed per tool block (parsed/parse_catalog.py): Max T/m where the shop has none
  dxf12/<code>.dxf           the tool profiles as compact R12 DXF (parsed/dxf_r12.py), published under files/dxf/

Tools the price list marks "out of production — ask for a quotation as a special tool" are left out.  Loads are given as
US tons per foot with the maker's metric tonnes per metre in brackets (1 t/m = 0.336 US t/ft).

Pages fed from here (tools/eurostamp_pages.py): the hub press-brake-tooling-punch-and-die and six pages —
european-press-brake-punches, european-press-brake-dies, trumpf-wila-press-brake-tooling, bystronic-lvd-press-brake-tooling,
american-style-press-brake-tooling, press-brake-tool-holders-adapters.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ES = "/home/claude/eurostamp/"
BRAND = "eurostamp"
DXF_DIR = "files/dxf"            # published path of the R12 profiles

_WEB = json.load(open(ES + "pages.json", encoding="utf-8"))
_PL = json.load(open(ES + "parsed/pricelist.json", encoding="utf-8"))
_CAT = json.load(open(ES + "parsed/catalog.json", encoding="utf-8"))
_URL2CAT = {u: c for c, us in _WEB["cats"].items() for u in us}
STYLE_OF_CAT = {"amada-promecam-style": "amada", "esh-style": "esh", "trumpf-style": "trumpf", "wila-style": "wila",
                "bystronic-style": "bystronic", "lvd-style": "lvd", "accessories": "acc"}
US_T_FT = 0.3048 * 1.10231          # t/m → US tons per foot


# ------------------------------------------------------------------------------------------------ number helpers
def num(s):
    if s is None:
        return None
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(s))
    return float(m.group(0).replace(",", ".")) if m else None


def g(v):
    """12.0 → '12', 0.8 → '0.8'"""
    return f"{v:g}"


def inch(mm, nd=3):
    """decimal inches the North-American way: 2.624″, .031″"""
    s = f"{mm / 25.4:.{nd}f}"
    return (s[1:] if s.startswith("0.") else s) + "″"


def height(mm):
    return f"{inch(mm)} ({g(mm)} mm)" if mm else "—"


def radius(mm):
    return f"R {inch(mm)} ({g(mm)} mm)" if mm is not None else "—"


def vopen(vs):
    """[6] → '.236″ (6 mm)'; [6, 10] → '.236 / .394″ (6 / 10 mm)'"""
    if not vs:
        return "—"
    ins = [inch(v)[:-1] for v in vs]
    return f"{' / '.join(ins)}″ ({' / '.join(g(v) for v in vs)} mm)"


def load(tm):
    return f"{tm * US_T_FT:.1f} US t/ft ({g(tm)} t/m)" if tm else "—"


def angle(a):
    return f"{g(a)}°" if a is not None else "—"


def length_in(mm):
    return f"{mm / 25.4:.1f}″"


MATERIAL = {"c45": "C45", "crmo": "42CrMo4"}


def material(*texts):
    t = " ".join(x for x in texts if x).lower()
    if "crmo" in t or "42cr" in t or "cr mo" in t:
        return "42CrMo4"
    if "c45" in t:
        return "C45"
    return ""


# ------------------------------------------------------------------------------------------------ merge the sources
def _code(title):
    m = re.match(r"\s*(\d{4})(?:\s*(/\d+|S\b|\s?PN))?", title)
    if not m:
        return None
    return m.group(1) + (m.group(2) or "").replace(" ", "")


def _attrs(p):
    out = {}
    for t in p["tables"][:1]:
        for k, v in re.findall(r'<dt class="name">(.*?)</dt>\s*<dd class="value">(.*?)</dd>', t, re.S):
            out[k.strip()] = re.sub(r"<.*?>", "", v).strip()
    return out


def _spec(line):
    """'α=88° ‐ R=0,8 ‐ H=104,65' / 'α =85° ‐ V=8 ‐ H80' / 'α =88° v=16/22 ‐ α =85° v=35/50 ‐ H=60' → dict"""
    s = line.replace("‐", "-")
    d = {}
    a = re.findall(r"α\s*=?\s*(\d+(?:[.,]\d+)?)\s*°", s)
    if a:
        d["angles"] = [num(x) for x in a]
    m = re.search(r"(?<![A-Za-z])R\s*=?\s*(\d+(?:[.,]\d+)?)", s)
    if m:
        d["r"] = num(m.group(1))
    m = re.search(r"(?<![A-Za-z])H\s*=?\s*(\d+(?:[.,]\d+)?)", s)
    if m:
        d["h"] = num(m.group(1))
    vs = re.findall(r"(?<![A-Za-z])[Vv]\s*=\s*(\d+(?:[.,]\d+)?(?:\s*/\s*\d+(?:[.,]\d+)?)*)", s)
    if vs:
        d["v"] = [num(x) for v in vs for x in v.split("/")]
    m = re.search(r"(?<![A-Za-z])U\s*=\s*([\d.,/]+)", s)
    if m:
        d["u"] = [num(x) for x in m.group(1).split("/") if num(x)]
    m = re.search(r"Z\s*=\s*(\d+(?:[.,]\d+)?)", s)
    if m:
        d["z"] = num(m.group(1))
    return d


def _pl_index():
    idx = {}
    for r in _PL:
        idx.setdefault(r["code"], r)
    return idx


PL = _pl_index()


def _web_records():
    recs = {}
    for url, p in _WEB["pages"].items():
        code = _code(p["title"])
        if not code:
            continue
        a = _attrs(p)
        fn = p["imgs"][0].rsplit("/", 1)[1] if p["imgs"] else None
        second = [u for u in p["imgs"] if "default/" in u and u.rsplit("/", 1)[1] == fn]
        rec = recs.setdefault(code, {"code": code, "titles": [], "urls": [], "style": STYLE_OF_CAT.get(_URL2CAT.get(url)), "attrs": {}})
        rec["titles"].append(p["title"])
        rec["urls"].append(url)
        for k, v in a.items():
            rec["attrs"].setdefault(k, v)
        drawing = ES + "img/" + fn if fn and os.path.exists(ES + "img/" + fn) else None
        if drawing and not rec.get("drawing"):
            rec["drawing"] = drawing
        # the second picture of a tool (standard lengths / segmentation) is stored as '<n>-<file>'
        if fn and not rec.get("lengths_pic"):
            cands = [f for f in os.listdir(ES + "img") if f.endswith("-" + fn) and f != fn]
            if cands:
                rec["lengths_pic"] = ES + "img/" + sorted(cands)[0]
    return recs


def _build():
    web = _web_records()
    tools = {}
    for code, w in web.items():
        a = w["attrs"]
        t = {"code": code, "style": w["style"], "title": w["titles"][0], "web_type": (a.get("Type") or "").replace("\n", " + "),
             "h": num(a.get("Height (mm)")), "angle": num(a.get("Angle")), "r": num(a.get("Radius")),
             "load": num(a.get("Max T/m")), "mat_web": a.get("Material", ""), "grooves": num(a.get("Numero cave")),
             "v": [num(x) for x in re.split(r"[-\s]+", a.get("V opening", "")) if num(x)] if a.get("V opening") else [],
             "len_web": num(a.get("Lenght (mm)")), "drawing": w.get("drawing"), "lengths_pic": w.get("lengths_pic"),
             "url": w["urls"][0], "source": "web"}
        tools[code] = t
    # price-list items the shop does not carry (radius and joggle tools, adjustable dies, EUROGRIP, tangs …)
    for code, r in PL.items():
        if code not in tools:
            tools[code] = {"code": code, "style": None, "title": "", "web_type": "", "h": None, "angle": None, "r": None, "load": None,
                           "mat_web": "", "grooves": None, "v": [], "len_web": None, "drawing": None, "lengths_pic": None, "url": None,
                           "source": "pricelist"}
    for code, t in tools.items():
        r = PL.get(code)
        t["pl"] = r
        t["discontinued"] = bool(r and r["discontinued"])
        t["phase_out"] = bool(r and r["phase_out"])
        sp = {}
        if r:
            for ln in r["lines"]:
                if re.search(r"[αVvHRUZ]\s*=|α\s*\d", ln):
                    for k, v in _spec(ln).items():
                        sp.setdefault(k, v)
            t["desc_lines"] = r["lines"]
            t["sizes"] = r["sizes"]
        else:
            t["desc_lines"], t["sizes"] = [], []
        t["spec"] = sp
        # fill the gaps from the price list, then from the catalogue
        if t["h"] is None and sp.get("h"):
            t["h"] = sp["h"]
        if t["angle"] is None and sp.get("angles"):
            t["angle"] = sp["angles"][0]
        if t["r"] is None and sp.get("r") is not None:
            t["r"] = sp["r"]
        if not t["v"] and sp.get("v"):
            t["v"] = sp["v"]
        if sp.get("v") and len(sp["v"]) > len(t["v"]):
            t["v"] = sp["v"]
        cat = (_CAT.get(code) or [{}])[0]
        if not t["load"] and cat.get("max_tm"):
            t["load"] = num(cat["max_tm"])
        t["material"] = material(t["mat_web"], " ".join(t["desc_lines"]), cat.get("mat", ""))
        if not t["material"] and (t["style"] == "esh" or code.startswith("33")):
            t["material"] = "42CrMo4"                      # the ESH series is all CrMo steel
        if not t["material"] and (code.endswith("PN") or code.startswith("3037/")):
            t["material"] = "C45"                          # the hemming dies, mechanical and pneumatic
        t["dxf"] = os.path.exists(ES + "dxf12/" + code + ".dxf")
        if t["style"] is None and r:
            st = r["style"].upper()
            t["style"] = ("esh" if "ESH" in st else "wila" if st.startswith("STILE WILA") else "trumpf" if "TRUMPF" in st and "BYSTRONIC" not in st
                          else "bystronic" if "BYSTRONIC" in st else "amada" if "AMADA" in st else "acc")
    return tools


TOOLS = _build()


# ------------------------------------------------------------------------------------------------ classification
def kind(t):
    """'punch', 'die' or 'holder' (die holders, rails and stoppers of the die sections), else None"""
    s = (t["web_type"] + " " + t["title"] + " " + " ".join(t["desc_lines"])).lower()
    if re.search(r"holder|support for|supporto|rail for|binario|stopper|blocco per", s) and t["style"] != "acc":
        return "holder"
    if "punch" in s or "punzon" in s or "flattening blade" in s:
        return "punch"
    if re.search(r"\bdies?\b|matric", s):
        return "die"
    return None


def _ptype(s, ang, generic=True):
    if "hemming" in s or "flattening" in s:
        return "Hemming"
    if "double gooseneck" in s or "doppio incavo" in s:
        return "Double gooseneck"
    if "reversed gooseneck" in s or "rovesciato" in s:
        return "Reversed gooseneck"
    if "reversed punch" in s:
        return "Reversed"
    if "high thickness" in s or "thick material" in s or "grossi spessori" in s:
        return "Heavy-duty"
    if "gooseneck" in s or "goose neck" in s or "grande incavo" in s:
        return "Gooseneck"
    if "sash" in s:
        return "Sash"
    if "straight" in s or "dritto" in s or (generic and ("punch" in s or "punzon" in s)):
        return "Acute" if ang is not None and ang <= 35 else "Straight"
    return None


def punch_type(t):
    """the maker's web type first (it is per tool), the price-list description only when the shop has none"""
    if t["web_type"]:
        return _ptype((t["web_type"] + " " + t["title"]).lower(), t["angle"])
    return (_ptype(t["title"].lower(), t["angle"], generic=False) or _ptype(" ".join(t["desc_lines"]).lower(), t["angle"])
            or ("Acute" if (t["angle"] or 90) <= 35 else "Straight"))


def _dtype(s):
    if "pneumatic" in s and ("hemming" in s or "piegaschiaccia" in s or "flattening" in s):
        return "Pneumatic hemming"
    if "hemming" in s or "flattening" in s or "piegaschiaccia" in s:
        return "Hemming"
    if re.search(r"\bt[ -]?shape\b|\bt dies?\b|matrice a t\b", s):
        return "T die"
    if "insert die" in s:
        return "Insert"
    if "u dies" in s or "3u" in s:
        return "U"
    if "4v" in s:
        return "4V"
    if "self centering 2v" in s or "reversible 2v" in s or "autocentrante" in s:
        return "2V self-centring"
    if "2v die" in s or "2 v die" in s:
        return "2V bolted"
    if "1v" in s or "single v" in s or "monocava" in s or "die" in s:
        return "1V"
    return None


def die_type(t):
    d = (_dtype((t["web_type"] + " " + t["title"]).lower()) if (t["web_type"] or t["title"]) else None) or _dtype(" ".join(t["desc_lines"]).lower()) or "1V"
    if d == "2V bolted" and (t["h"] or 0) >= 40:          # the 46 mm two-V dies are the self-centring (reversible) ones
        d = "2V self-centring"
    return d


# ------------------------------------------------------------------------------------------------ lengths
SECTIONED = {"amada": {805}, "esh": {800}, "trumpf": {550, 1100}, "wila": {550}, "bystronic": {550, 1100}}


def lengths(t):
    """the sizes a tool is sold in, mm: [(835, ''), (415, ''), (805, 'sectioned')] — short single pieces tagged 'piece'"""
    out = []
    for sz, _w in t["sizes"]:
        m = re.match(r"\s*(?:Sect\.\s*Short[‐-])?(\d+)\s*(Fraz\.|fraz\.|SECT|rig\. Horn)?", sz)
        if not m:
            continue
        mm = int(m.group(1))
        sect = (m.group(2) or "").lower().startswith(("fraz", "sect")) or "Sect" in sz or mm in SECTIONED.get(t["style"], ())
        tag = "sectioned" if sect else ("horn" if "Horn" in sz else ("piece" if mm < 400 and t["style"] != "acc" else ""))
        if (mm, tag) not in out:
            out.append((mm, tag))
    if not out and t.get("len_web"):
        out.append((int(t["len_web"]), ""))
    return out


_BOXES = json.load(open(ES + "parsed/boxes.json", encoding="utf-8"))["codes"]     # the catalogue's length / weight boxes by code
_CAT_TAG = {"sectioned": "sectioned", "short-sectioned": "short-sectioned", "horn": "horn", "standard": "", None: ""}


def _pl_len_rows(t):
    """the price list's sizes → [{mm, kg, tag, n}] — tag '' (full length), 'sectioned', 'short-sectioned', 'right horn',
    'left horn' or 'pair' (two pieces, e.g. the 2 × 150 mm moving horns)"""
    rows = []
    for sz, w in t.get("sizes") or []:
        s = sz.strip().replace("‐", "-")
        kg = num(w) if w and re.match(r"\s*\d", w) else None
        m = re.match(r"^(\d{2,4})(?:\s*(fraz\.?))?$", s, re.I)
        if m:
            rows.append({"mm": int(m.group(1)), "kg": kg, "tag": "sectioned" if m.group(2) else "", "n": 1})
            continue
        m = re.match(r"^Sect\.\s*Short-(\d+)", s, re.I)
        if m:
            rows.append({"mm": int(m.group(1)), "kg": kg, "tag": "short-sectioned", "n": 1})
            continue
        m = re.match(r"^(\d+)\s*(rig\.|right|lef\.|left)\s*ho[rt]n$", s, re.I)
        if m:
            rows.append({"mm": int(m.group(1)), "kg": kg, "tag": "right horn" if m.group(2).lower().startswith("r") else "left horn", "n": 1})
            continue
        m = re.match(r"^(\d)\s*x\s*(\d+)$", s)
        if m:
            rows.append({"mm": int(m.group(2)), "kg": kg, "tag": "pair", "n": int(m.group(1))})
    return rows


def _cat_len_rows(code):
    return [[{"mm": mm, "kg": kg, "tag": _CAT_TAG.get(tag, ""), "n": 1} for mm, kg, tag in b["rows"]] for b in _BOXES.get(code) or []]


_AREA = {}


def dxf_area(code):
    """cross-section of a tool from its DXF profile (LINE / ARC loops), mm² — EUROSTAMP's own weights are this area × length
    × 7.85 g/cm³ to within 1 % (checked on 1011, 1052, 1055, 3080, 3200, 1294, 1315, 1324 …)"""
    if code in _AREA:
        return _AREA[code]
    import math
    path = ES + "dxf12/" + code + ".dxf"
    if not os.path.exists(path):
        _AREA[code] = None
        return None
    lines = open(path, encoding="latin-1").read().split("\n")
    ents, cur = [], None
    for i in range(0, len(lines) - 1, 2):
        c, v = lines[i].strip(), lines[i + 1].strip()
        if c == "0":
            if cur:
                ents.append(cur)
            cur = {"type": v} if v in ("LINE", "ARC", "CIRCLE") else None
        elif cur is not None and re.match(r"^-?[\d.]+(e-?\d+)?$", v):
            cur.setdefault(c, float(v))
    if cur:
        ents.append(cur)
    segs = []
    for e in ents:
        if e["type"] == "LINE":
            segs.append([(e["10"], e["20"]), (e["11"], e["21"])])
        else:
            cx, cy, r = e["10"], e["20"], e["40"]
            a0, a1 = (e.get("50", 0.0), e.get("51", 360.0)) if e["type"] == "ARC" else (0.0, 360.0)
            if a1 < a0:
                a1 += 360
            n = max(2, int((a1 - a0) / 3) + 1)
            segs.append([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / (n - 1))), cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / (n - 1)))) for k in range(n)])
    used, areas = [False] * len(segs), []
    for i in range(len(segs)):
        if used[i]:
            continue
        used[i], path_ = True, list(segs[i])
        for _ in range(len(segs)):
            if len(path_) > 2 and math.dist(path_[-1], path_[0]) < 0.02:
                break
            for j, s in enumerate(segs):
                if not used[j] and math.dist(s[0], path_[-1]) < 0.02:
                    path_ += s[1:]; used[j] = True; break
                if not used[j] and math.dist(s[-1], path_[-1]) < 0.02:
                    path_ += s[::-1][1:]; used[j] = True; break
            else:
                break
        if len(path_) > 2 and math.dist(path_[-1], path_[0]) < 0.02:
            areas.append(abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(path_, path_[1:] + path_[:1]))) / 2)
    areas.sort(reverse=True)
    _AREA[code] = (areas[0] - sum(areas[1:])) if areas else None
    return _AREA[code]


LVD_LENGTH = 510              # EUROSTAMP's LVD-style tools: 510 mm (the shop states it on the tools that carry a length)


def length_rows(t):
    """every length a tool is sold in, with its weight: the 2024 price list first (it is the ordering document and lists the
    right and left horns separately), weights it lacks from the catalogue's box, and the catalogue's rows when the price list
    has none (EUROGRIP, tangs).  A weight nobody publishes (the LVD-style series) is calculated from the DXF profile and
    flagged 'calc'.  [{mm, kg, tag, n, calc}]"""
    rows = _length_rows(t)
    a = None
    for r in rows:
        if r["kg"] is None and r["tag"] in ("", "sectioned", "short-sectioned"):
            a = a if a is not None else dxf_area(t["code"])
            if a:
                r["kg"], r["calc"] = round(a * r["mm"] * r.get("n", 1) * 7.85e-6, 1), True
    return rows


def _length_rows(t):
    pl = _pl_len_rows(t)
    cats = _cat_len_rows(t["code"])
    if not pl:
        if cats:
            return [dict(r) for r in cats[0]]
        if t.get("style") == "lvd":
            return [{"mm": int(t.get("len_web") or LVD_LENGTH), "kg": None, "tag": "", "n": 1}]
        return [{"mm": int(t["len_web"]), "kg": None, "tag": "", "n": 1}] if t.get("len_web") else []
    sect = ("sectioned", "short-sectioned")
    for r in pl:
        if r["kg"] is None:
            for box in cats:
                c = next((c for c in box if c["mm"] == r["mm"] and c["kg"] is not None and (c["tag"] in sect) == (r["tag"] in sect)), None)
                if c:
                    r["kg"] = c["kg"]
                    break
    # a length the catalogue prints and the price list lost (its other rows agree with the price list): add it, in catalogue order
    have = {r["mm"] for r in pl}
    for box in cats:
        mms = {c["mm"] for c in box}
        if have < mms and all(any(c["mm"] == r["mm"] and (c["kg"] is None or r["kg"] is None or abs(c["kg"] - r["kg"]) < 0.25) for c in box) for r in pl):
            out = []
            for c in box:
                same = [r for r in pl if r["mm"] == c["mm"]]
                out.extend(same or [dict(c)])
            return out
    return pl


def inch2(mm):
    """a tool length in decimal inches, two places: 32.87″, .98″"""
    s = f"{mm / 25.4:.2f}"
    return (s[1:] if s.startswith("0.") else s) + "″"


def lb_s(kg):
    v = kg * 2.20462
    return f"{v:,.0f} lb" if v >= 100 else f"{v:.1f} lb"


def kg_s(kg):
    """12.6 → '12.6 kg', 13 → '13.0 kg' (one decimal like the catalogue), 1.375 → '1.375 kg', 594 → '594 kg'"""
    if kg >= 100:
        return f"{kg:,.0f} kg"
    return f"{kg:.1f} kg" if round(kg, 1) == kg else f"{kg:g} kg"


LEN_TAG = {"": "", "sectioned": "sectioned set", "short-sectioned": "short sectioned set", "right horn": "horn, right",
           "left horn": "horn, left", "horn": "horn", "pair": "pair"}


def len_key(r):
    return (r["mm"], r["tag"], r.get("n", 1))


def len_keys(tools):
    """the length columns of a table, in catalogue order: full lengths (long to short), sectioned sets, horns, pairs, then the
    short sections (Trumpf / Wila / Bystronic pieces under 100 mm)"""
    keys = []
    for t in tools:
        for r in length_rows(t):
            k = len_key(r)
            if k not in keys:
                keys.append(k)
    grp = {"": 0, "sectioned": 1, "short-sectioned": 2, "right horn": 3, "horn": 3, "left horn": 4, "pair": 5}

    def order(k):
        mm, tag, n = k
        g = grp.get(tag, 6)
        if tag == "" and mm < 100:
            g = 7
        return (g, -mm)
    return sorted(keys, key=order)


def len_head(k):
    mm, tag, n = k
    lab = f"{n} × {inch2(mm)}" if n > 1 else inch2(mm)
    sub = f"{n} × {mm:,} mm" if n > 1 else f"{mm:,} mm"
    return {"label": lab, "sub": sub, "tag": LEN_TAG.get(tag, tag)}


def len_cell(t, k):
    for r in length_rows(t):
        if len_key(r) == k:
            if r["kg"] is None:
                return {"text": "yes", "cls": "tt-w"}
            pre = "≈ " if r.get("calc") else ""
            return {"text": pre + lb_s(r["kg"]), "sub": pre + kg_s(r["kg"]), "cls": "tt-w"}
    return "—"


INLINE_LENGTHS = 4          # up to this many length columns go into the tool table itself; more get their own table under it


def lengths_text(ls):
    """[(835,''),(415,''),(805,'sectioned')] → '32.9 · 16.3″ · 31.7″ sect. (835 · 415 · 805 sect. mm)';
    short single pieces are summarised: '19.7″ · 21.7″ sect. · pieces (500 · 550 sect. · 25 – 300 mm)'"""
    if not ls:
        return "—"
    full = [mm for mm, tag in ls if tag == ""]
    sect = [mm for mm, tag in ls if tag == "sectioned"]
    pieces = [mm for mm, tag in ls if tag in ("piece", "horn")]
    ins, mms = [], []
    if full:
        ins.append(" · ".join(f"{mm / 25.4:.1f}" for mm in full) + "″")
        mms.append(" · ".join(f"{mm:,}" for mm in full))
    if sect:
        ins.append(" · ".join(f"{mm / 25.4:.1f}" for mm in sect) + "″ sect.")
        mms.append(" · ".join(f"{mm:,}" for mm in sect) + " sect.")
    if pieces:
        ins.append("pieces")
        mms.append(f"{min(pieces)} – {max(pieces)}" if min(pieces) != max(pieces) else f"{pieces[0]}")
    return f"{' · '.join(ins)} ({' · '.join(mms)} mm)"


# ------------------------------------------------------------------------------------------------ tables (rows = tools)
def dxf_cell(code):
    return {"href": f"{DXF_DIR}/{code}.dxf", "text": "DXF", "download": True} if TOOLS.get(code, {}).get("dxf") else "—"


COLS = {
    "type": ("Type", lambda t: t.get("type_label") or ""),
    "angle": ("Angle", lambda t: angle(t["angle"])),
    "angles": ("Angle", lambda t: " / ".join(f"{g(a)}°" for a in (t["spec"].get("angles") or [t["angle"]] if t["angle"] is not None else [])) or "—"),
    "h": ("Height H", lambda t: height(t["h"])),
    "r": ("Tip radius", lambda t: radius(t["r"]) if t["r"] is not None else "—"),
    "rs": ("Shoulder radius", lambda t: radius(t["r"]) if t["r"] is not None else "—"),
    "v": ("V opening", lambda t: vopen(t["v"])),
    "u": ("U width", lambda t: vopen(t["spec"].get("u")) if t["spec"].get("u") else vopen(t["v"])),
    "load": ("Max. load", lambda t: load(t["load"])),
    "len": ("Lengths", lambda t: lengths_text(lengths(t))),
    "mat": ("Steel", lambda t: t["material"] or "—"),
    "dxf": ("Profile", lambda t: dxf_cell(t["code"])),
}


def with_lengths(tab, tools, at=None):
    """add the lengths-and-weights columns to a table dict (rows = tools, same order): every length the tools are sold in,
    in inches and mm, with the weight of each in lb and kg.  Up to INLINE_LENGTHS columns join the table under a
    'Lengths & weights' group header (inserted at `at`, default before a final Profile column); more get a table of their own,
    tab['lw'], shown right under it."""
    keys = len_keys(tools)
    if not keys:
        return tab
    heads = [len_head(k) for k in keys]
    if any(r.get("calc") for t in tools for r in length_rows(t)):
        tab["sub"] = (tab["sub"] + " · " if tab.get("sub") else "") + "weights marked ≈ calculated from the tool profile (steel, 7.85 g/cm³)"
    if len(keys) <= INLINE_LENGTHS:
        if at is None:
            at = len(tab["cols"]) - 1 if tab["cols"] and tab["cols"][-1] == "Profile" else len(tab["cols"])
        tab["cols"] = tab["cols"][:at] + heads + tab["cols"][at:]
        tab["rows"] = [r[:at + 1] + [len_cell(t, k) for k in keys] + r[at + 1:] for r, t in zip(tab["rows"], tools)]
        tab["group"] = {"label": "Lengths & weights", "start": at, "span": len(keys)}
    else:
        tab["lw"] = {"title": tab["title"] + " — lengths and weights", "sub": "weight of each piece or set",
                     "cols": heads, "rows": [[t["code"]] + [len_cell(t, k) for k in keys] for t in tools],
                     "first_col": tab.get("first_col") or "Code", "group": {"label": "Lengths & weights", "start": 0, "span": len(keys)}}
    return tab


def tool_table(title, sub, tools, cols, note=""):
    """one table, one row per tool: the code in the first column, then `cols`.  'len' becomes the lengths-and-weights
    columns (with_lengths)."""
    cols = list(cols)
    want_len = "len" in cols
    if want_len:
        cols.remove("len")
    if "type" in cols and len({t.get("type_label") for t in tools}) == 1:
        cols.remove("type")                        # one type for the whole table: the title says it
    if "load" in cols and not any(t["load"] for t in tools):
        cols.remove("load")
    if "mat" in cols and len({t["material"] for t in tools}) == 1 and tools[0]["material"]:
        sub = (sub + " · " if sub else "") + tools[0]["material"] + " steel"
        cols.remove("mat")
    rows = [[t["code"]] + [COLS[c][1](t) for c in cols] for t in tools]
    tab = {"title": title, "sub": sub, "cols": [COLS[c][0] for c in cols], "rows": rows, "note": note,
           "codes": [t["code"] for t in tools]}
    return with_lengths(tab, tools) if want_len else tab


# ------------------------------------------------------------------------------------------------ selection helpers
def pick(style, k=None, ptype=None, dtype=None, codes=None, keep=lambda t: True):
    out = []
    for c, t in TOOLS.items():
        if codes is not None and c not in codes:
            continue
        if style and t["style"] != style:
            continue
        if t["discontinued"]:
            continue
        if k and kind(t) != k:
            continue
        if ptype and punch_type(t) not in ptype:
            continue
        if dtype and die_type(t) not in dtype:
            continue
        if not keep(t):
            continue
        out.append(t)
    return out


def by_shape(ts, key=None):
    return sorted(ts, key=key or (lambda t: (-(t["angle"] or 0), t["h"] or 0, t["r"] or 0, t["code"])))


def with_type(ts, f):
    for t in ts:
        t["type_label"] = f(t)
    return ts


def rng(vals, fmt=lambda v: g(v)):
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return ""
    return fmt(vals[0]) if vals[0] == vals[-1] else f"{fmt(vals[0])} – {fmt(vals[-1])}"


def summary_numbers(ts):
    """for the hub table and the feature line: angles, heights, loads"""
    hs = [t["h"] for t in ts if t["h"]]
    ls = [t["load"] for t in ts if t["load"]]
    an = [t["angle"] for t in ts if t["angle"] is not None]
    vs = [v for t in ts for v in t["v"]]
    return {
        "n": len(ts),
        "angles": rng(an, lambda v: f"{g(v)}°"),
        "heights": (f"{inch(min(hs))} – {inch(max(hs))} ({g(min(hs))} – {g(max(hs))} mm)" if hs and min(hs) != max(hs) else (height(hs[0]) if hs else "—")),
        "loads": (f"to {max(ls) * US_T_FT:.0f} US t/ft ({g(max(ls))} t/m)" if ls else "—"),
        "v": (f"V {inch(min(vs))} – {inch(max(vs))} ({g(min(vs))} – {g(max(vs))} mm)" if vs and min(vs) != max(vs) else ""),
    }


if __name__ == "__main__":
    import collections
    print(len(TOOLS), "tools;", sum(t["discontinued"] for t in TOOLS.values()), "discontinued;",
          sum(t["dxf"] for t in TOOLS.values()), "with DXF;", sum(bool(t["drawing"]) for t in TOOLS.values()), "with drawings")
    c = collections.Counter((t["style"], kind(t)) for t in TOOLS.values() if not t["discontinued"])
    for k, v in sorted(c.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        print(k, v)
