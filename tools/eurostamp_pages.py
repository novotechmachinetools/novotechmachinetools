#!/usr/bin/env python3
"""EUROSTAMP press brake tooling section: the hub press-brake-tooling-punch-and-die (the old page's URL) and six pages —
european-press-brake-punches, european-press-brake-dies, trumpf-wila-press-brake-tooling, bystronic-lvd-press-brake-tooling,
american-style-press-brake-tooling and press-brake-tool-holders-adapters.  Tool data from tools/eurostamp_data.py (rows = tools,
DXF profile per tool), photos and drawings from tools/eurostamp_photos.py (section 'tooling'); family set 'tooling'.

    python3 tools/eurostamp_photos.py            # drawings, photos, standard-length diagrams → tools/src-images/eurostamp
    python3 tools/eurostamp_pages.py             # families, pages, image_map entries (tools/eurostamp_keys.txt), DXF + PDF files
    python3 tools/make_images.py --only $(cat tools/eurostamp_keys.txt)
"""
import json
import re
import os
import shutil

import eurostamp_data as D
from isitan_lib import CRUMBS, write_category, write_hub, write_families

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "tooling"
BRAND = D.BRAND
HUB = "press-brake-tooling-punch-and-die"
P_EUP, P_EUD = "european-press-brake-punches", "european-press-brake-dies"
P_TW, P_BL = "trumpf-wila-press-brake-tooling", "bystronic-lvd-press-brake-tooling"
P_AM, P_ACC = "american-style-press-brake-tooling", "press-brake-tool-holders-adapters"
SECTION = "Press brake tooling"
# NovoTech's inch edition of the EUROSTAMP catalogue (tools/brochure/eurostamp_edition.py); the old site's URL of the metric
# catalogue redirects to it (src/root/.htaccess)
CAT_FILE = "files/NovoTech-Press-Brake-Tooling-Catalogue-2026.pdf"
CATALOGUE = {"file": CAT_FILE, "label": "Download the EUROSTAMP catalogue — inch edition", "size": "PDF · {mb} MB · mm and inches"}

BRAND_LINE = ("EUROSTAMP tooling is made in Gragnano Trebbiense, Italy, by a company that has built nothing but press brake tools "
              "since 1970 — sold, shipped and supported in Canada by NovoTech from Mississauga, ON, Canada.")
ORIGIN = {"title": "Made in Italy since 1970", "text": "EUROSTAMP has built press brake tooling in Gragnano Trebbiense, near Piacenza, since 1970."}
WHY = [
    {"title": "Made in Italy since 1970", "text": "EUROSTAMP builds only press brake tooling — punches, dies, adapters and clamping — in Gragnano Trebbiense, near Piacenza.", "icon": "factory"},
    {"title": "Hardened where it wears", "text": "C45 and 42CrMo4 steel, induction-hardened to 55 – 60 HRC up to 3 mm (.118″) deep on the working surfaces.", "icon": "warranty"},
    {"title": "DXF profiles to download", "text": "Most punches and dies here link to their DXF profile — load it into the tool library of your Delem, ESA or Cybelec control, or into offline software.", "icon": "receipt"},
    {"title": "Fits your press brake", "text": "European (Amada-Promecam), Trumpf, Wila, Bystronic, LVD and American styles, and adapters between them.", "icon": "repeat"},
    {"title": "Special tools to your drawing", "text": "EUROSTAMP's technical department designs special punches and dies for the parts standard tooling cannot bend.", "icon": "panel"},
    {"title": "Shipped across Canada", "text": "Quoted, ordered and shipped by NovoTech from Mississauga, ON, Canada, with the freight arranged at competitive rates.", "icon": "truck"},
]
QUOTE = {"intro": "Tell us your press brake (make, model and clamping), the tool codes or the part you need to bend, and the lengths, and we "
                  "will come back with pricing and delivery.",
         "select_label": "Tooling of interest", "select_placeholder": "Choose a tooling family…",
         "message_label": "Press brake, tool codes, lengths, quantities, delivery city…"}
INTRO_VIDEO = {"intro_video": {"id": "RTLFMt-ryOc", "title": "EUROSTAMP press brake tooling — introduction", "thumb": "video-RTLFMt-ryOc", "duration": "PT5M3S"},
               "intro_video_heading": "Inside the factory — where the tooling is made",
               "intro_video_text": "EUROSTAMP introduces its plant in Gragnano Trebbiense, Italy, where the punches, dies and adapters on these pages are made."}
VIDEO_TOOLING = {"id": "o5b-y1RibRM", "title": "EUROSTAMP press brake tooling — punches and dies", "thumb": "video-o5b-y1RibRM", "duration": "PT2M5S"}
VIDEO_ESA = {"id": "Oo5LJWY2o-g", "title": "ESA 630 press brake — punch and die drawing tutorial", "thumb": "video-Oo5LJWY2o-g", "duration": "PT17M52S"}

NOTE_TOOLS = ("Heights are the working height H of the tool; loads are the maker's maximum in tonnes per metre of tool length, shown as US "
              "tons per foot (1 t/m = 0.336 US t/ft) — the tonnage of the bend per foot must stay below it. Lengths: full lengths, "
              "sectioned (sect.) sets with horns, and single pieces. Profile: the tool's DXF, drawn in millimetres, for your CNC's "
              "tool library. Tools EUROSTAMP has taken out of production are not listed; ask us for them as special tools.")


# ------------------------------------------------------------------------------------------------ helpers
def drawing_keys(ts, n=6):
    """up to n drawing keys spread over a sorted tool list (only tools that have a maker's drawing)"""
    have = [t for t in ts if t["drawing"]]
    if len(have) <= n:
        pick = have
    else:
        step = (len(have) - 1) / (n - 1)
        pick = [have[round(i * step)] for i in range(n)]
    return [dkey(t["code"]) for t in pick]


def dkey(code):
    return "es-d-" + code.replace("/", "-").lower()


def tool_alt(t):
    k = D.kind(t)
    if k == "punch":
        kind = D.punch_type(t).lower() + " punch"
        bits = [f"{D.g(t['angle'])}°" if t["angle"] is not None else "", f"R {D.g(t['r'])} mm" if t["r"] is not None else "",
                f"H {D.g(t['h'])} mm" if t["h"] else ""]
    else:
        kind = {"1V": "1V die", "Insert": "insert die", "T die": "T die", "Hemming": "hemming die", "Pneumatic hemming": "pneumatic hemming die",
                "2V bolted": "2V die", "2V self-centring": "self-centring 2V die", "4V": "4V die", "U": "U die"}.get(D.die_type(t), "die")
        bits = [f"{D.g(t['angle'])}°" if t["angle"] is not None else "", ("V " + "/".join(D.g(v) for v in t["v"]) + " mm") if t["v"] else "",
                f"H {D.g(t['h'])} mm" if t["h"] else ""]
    return f"{t['code']} — {kind} {', '.join(b for b in bits if b)} (profile drawing)"


def tool_cap(t):
    """gallery caption line 1 for a drawing: '1011 · 88° · R .031″ · H 2.624″'"""
    bits = [f"{D.g(t['angle'])}°" if t["angle"] is not None else ""]
    if D.kind(t) == "punch" and t["r"] is not None:
        bits.append(f"R {D.inch(t['r'])}")
    if D.kind(t) == "die" and t["v"]:
        bits.append("V " + " / ".join(D.inch(v) for v in t["v"]))
    if t["h"]:
        bits.append(f"H {D.inch(t['h'])}")
    if t["load"]:
        bits.append(f"{t['load'] * D.US_T_FT:.1f} US t/ft")
    return " · ".join(b for b in bits if b)


ALL_FAMILIES = []
DRAWINGS = {}          # key → tool (for the photo script and the image_map alt text)


def family(fid, page, name, short, summary, features, tables, *, images=(), tools=(), ndraw=6, videos=(), headline="", models_label=None,
           family_row=None, note=NOTE_TOOLS, extra_caps=None, glance_tools=None, pdf=CATALOGUE):
    """a tooling family: tool tables (rows = tools), a gallery of photos + the maker's drawings of a spread of its tools"""
    ts = list(tools)
    dk = drawing_keys(ts, ndraw) if ndraw else []
    for t in ts:
        if t["drawing"] and dkey(t["code"]) in dk:
            DRAWINGS[dkey(t["code"])] = t
    gl = glance_tools if glance_tools is not None else ts
    codes = [t["code"] for t in gl]
    f = dict(id=fid, group=page, page=page, brand=BRAND, name=name, short=short, summary=summary, features=list(features),
             models_label=models_label or (f"{min(codes)} – {max(codes)} · {len(codes)} profiles" if codes else ""),
             images=list(images) + dk, videos=list(videos), tool_tables=tables, tool_note=note,
             pdf=pdf, pdf_cta="Download the catalogue (PDF)", headline=headline,
             model_caps={**{t["code"]: tool_cap(t) for t in gl}, **(extra_caps or {})},
             specs={"kind": "tools", "models": [{"name": t["code"], "glance": [tool_glance(t)[k] for k in GLANCE]} for t in gl],
                    "glance_keys": GLANCE, "family_row": family_row or [], "family_row_sub": "",
                    "headline": headline, "note": note})
    ALL_FAMILIES.append(f)
    return f


GLANCE = ["type", "angle", "height", "tip_radius_or_v", "max_load"]


def tool_glance(t):
    k = D.kind(t)
    return {"type": (D.punch_type(t) + " punch") if k == "punch" else (D.die_type(t) + " die") if k == "die" else (t.get("type_label") or ""),
            "angle": D.angle(t["angle"]) if t["angle"] is not None else "", "height": D.height(t["h"]) if t["h"] else "",
            "tip_radius_or_v": (D.radius(t["r"]) if k == "punch" and t["r"] is not None else D.vopen(t["v"]) if t["v"] else ""),
            "max_load": D.load(t["load"]) if t["load"] else ""}


def frow(ts, extra=""):
    """hub 'range at a glance' columns: profiles, angles, heights, max load"""
    s = D.summary_numbers(ts)
    return [str(s["n"]) + (f" · {extra}" if extra else ""), s["angles"] or "—", s["heights"], s["loads"]]


P, T = D.pick, D.tool_table
PUNCH_COLS = ["type", "angle", "h", "r", "load", "len", "mat", "dxf"]
DIE_COLS = ["type", "v", "angle", "h", "load", "len", "mat", "dxf"]


def ptyped(ts):
    return D.with_type(D.by_shape(ts), D.punch_type)


def dtyped(ts, labels=None):
    lab = labels or {"1V": "1V", "Insert": "Self-centring 1V", "T die": "T", "Hemming": "Hemming", "Pneumatic hemming": "Hemming, pneumatic",
                     "2V bolted": "2V, bolted", "2V self-centring": "2V, self-centring", "4V": "4V", "U": "3U"}
    return D.with_type(ts, lambda t: lab.get(D.die_type(t), D.die_type(t)))


def by_v(ts):
    return sorted(ts, key=lambda t: (-(t["angle"] or 0), t["h"] or 0, (t["v"] or [0])[0], t["code"]))


# ================================================================================================= European punches
eu_straight = ptyped(P("amada", "punch", ptype=["Straight", "Heavy-duty"]))
eu_acute = ptyped(P("amada", "punch", ptype=["Acute", "Hemming"]))
eu_goose = ptyped(P("amada", "punch", ptype=["Gooseneck", "Double gooseneck", "Reversed gooseneck", "Reversed", "Sash"]))
esh_p = ptyped(P("esh", "punch"))

family("es-eu-straight", P_EUP, "Straight and heavy-duty punches, 45° – 88°", "Straight punches",
       "The everyday punch for air bending to 90°: a straight body with an 88° or 85° tip — 85° leaves room to over-bend stainless and "
       "high-strength steel that springs back further — in working heights from 65 to 135 mm (2.56 – 5.31″), plus 75°, 60° and 45° "
       "punches for acute bends and deeper parts. Tip radii run from 0.25 mm for crisp corners in thin sheet to 3 mm, and the four "
       "heavy-duty punches carry R6 to R10 tips and up to 150 t/m (50 US t/ft) for plate, where a sharp tip would crack the outside of "
       "the bend.",
       ["Angles 88°, 85°, 75°, 60° and 45°; working heights 65 to 200 mm (2.56 – 7.87″)",
        "Tip radius R0.25 to R3 for sheet; heavy-duty profiles with R6 to R10 tips, rated to 150 t/m (50 US t/ft)",
        "835 mm (32.9″) and 415 mm (16.3″) full lengths; 805 mm (31.7″) sectioned set — 100 mm horns left and right plus 10, 15, 20, 40, 50, 200 and 270 mm pieces",
        "Moving horns for 1011, 1047 and 1065 (codes 1011S, 1047S, 1065S, pairs of 150 mm) to bend flanges at the end of a part",
        "C45 or 42CrMo4 steel, induction-hardened 55 – 60 HRC up to 3 mm (.118″) deep",
        "DXF profiles for the CNC's tool library"],
       [T("Straight punches", "85° – 88°", [t for t in eu_straight if t["angle"] >= 85 and D.punch_type(t) == "Straight"], PUNCH_COLS),
        T("Straight punches", "45° – 75°", [t for t in eu_straight if t["angle"] < 85 and D.punch_type(t) == "Straight"], PUNCH_COLS),
        T("Heavy-duty punches for plate", "large tip radius", [t for t in eu_straight if D.punch_type(t) == "Heavy-duty"], PUNCH_COLS)],
       images=["es-p-c077b", "es-std-eu-punch"], tools=eu_straight, videos=[VIDEO_TOOLING],
       headline="45° – 88°, H 2.56 – 7.87″, to 50 US t/ft", family_row=frow(eu_straight))

family("es-eu-acute", P_EUP, "Acute and hemming punches, 24° – 35°", "Acute punches",
       "Acute punches bend well past 90° — to 30° or 35° in a matching die — for the first stage of a hem, for acute flanges and to "
       "over-bend high-strength steel. The 26°, 30° and 35° punches come in working heights from 80 to 200 mm (3.15 – 7.87″) with tip "
       "radii from 0.5 to 5 mm; the slim-body 30° punch reaches into narrow profiles. The 24° and 28° hemming punches pre-bend the flange "
       "that a hemming die then closes flat in the second stroke.",
       ["Angles 35°, 30° and 26°; hemming punches 28° and 24°", "Working heights 80 to 200 mm (3.15 – 7.87″); tip radius R0.5 to R5",
        "Rated to 100 t/m (34 US t/ft) — check the rating of slim and tall profiles before bending plate",
        "835 and 415 mm (32.9 / 16.3″) lengths and the 805 mm (31.7″) sectioned set with horns",
        "Pairs with the 30° and 45° dies and the hemming dies on the European dies page"],
       [T("Acute punches", "26° – 35°", [t for t in eu_acute if D.punch_type(t) == "Acute"], PUNCH_COLS),
        T("Hemming punches", "24° – 28°", [t for t in eu_acute if D.punch_type(t) == "Hemming"], PUNCH_COLS)],
       images=["es-p-c077a"], tools=eu_acute, headline="26° – 35° acute, 24° – 28° hemming, H 3.15 – 7.87″", family_row=frow(eu_acute))

family("es-eu-goose", P_EUP, "Gooseneck and sash punches, 60° – 88°", "Gooseneck punches",
       "A gooseneck punch is relieved behind the tip so a returned flange clears the body: the punch for U-channels, pans and boxes with "
       "return flanges. Thirty-odd profiles from 66.6 to 200 mm (2.62 – 7.87″) high — single, double and reversed goosenecks, 60° and "
       "85° goosenecks for acute returns and springy materials, and sash punches with the slim nose for tight return flanges and window "
       "profiles. The tall 145, 165 and 200 mm punches reach into deep boxes; check the load rating, which falls as the neck gets deeper.",
       ["Single, double and reversed goosenecks, 88°, 85° and 60°; sash punches 88°",
        "Working heights 66.6 to 200 mm (2.62 – 7.87″); tip radius R0.25 to R3",
        "Rated to 100 t/m (34 US t/ft); deep-necked profiles lower — see the table",
        "835 and 415 mm (32.9 / 16.3″) lengths and the 805 mm (31.7″) sectioned set with horns; the 200 mm profiles in 505 mm and 805 mm sectioned",
        "C45 or 42CrMo4 steel, induction-hardened 55 – 60 HRC"],
       [T("Gooseneck punches", "single, double and reversed", [t for t in eu_goose if D.punch_type(t) != "Sash"], PUNCH_COLS),
        T("Sash punches", "slim nose for return flanges", [t for t in eu_goose if D.punch_type(t) == "Sash"], PUNCH_COLS)],
       images=["es-p-c015"], tools=eu_goose, headline="H 2.62 – 7.87″ — single, double, reversed and sash",
       family_row=frow(eu_goose))

family("es-esh-punch", P_EUP, "ESH same-height punches, 120 mm", "ESH punches",
       "ESH — EUROSTAMP Same Height — is a European-style series in which every punch has the same 120 mm (4.72″) working height, so "
       "straight, gooseneck and sash punches can stand side by side in stations and a complex part is bent in one setup without moving "
       "the ram. The punches are premium chrome-molybdenum steel with 950 – 1,050 N/mm² tensile strength, so slim sections still carry "
       "high tonnage, and the tips are induction-hardened to 55 – 58 HRC more than 3 mm deep. Angles 86°, 60°, 30° and 26°; the matching "
       "ESH insert dies are on the European dies page.",
       ["One working height for the whole series: 120 mm (4.72″) — staged bending without re-setting",
        "Straight, gooseneck and sash profiles at 86°, 60°, 30° and 26°; tip radius R0.6", "Rated to 100 t/m (34 US t/ft)",
        "835 and 415 mm (32.9 / 16.3″) lengths; 800 mm (31.5″) sectioned set: 100 mm horns, 10, 15, 15, 20, 40, 50, 150 and 300 mm",
        "Premium CrMo steel, 950 – 1,050 N/mm²; tips induction-hardened 55 – 58 HRC more than 3 mm deep; phosphate coating against corrosion on request"],
       [T("ESH punches", "working height 120 mm (4.72″)", esh_p, PUNCH_COLS)],
       images=["es-p-c078a"], tools=esh_p, headline="All 120 mm (4.72″) high, 26° – 86°", family_row=frow(esh_p))

# radius tooling: holders + round elements (price list items; no web drawings)
RADIUS_HOLDERS = [("1096", "Holder for round elements, straight", 100), ("1036", "Holder for round elements, straight", 67),
                  ("1091", "Holder for round elements, gooseneck", 87), ("1090", "Holder for round elements, gooseneck", 115),
                  ("1155", "Holder for small radius elements", None), ("1296", "Holder for small elements R3 – R4.5", 60),
                  ("1297", "Holder for small elements R5 – R6.5", 60), ("1239", "Holder, Bystronic type R / RF-A", 140),
                  ("1273", "Holder, Bystronic type RF-A", 140), ("1240", "Holder, Trumpf style", 140),
                  ("1305", "Holder, Weinbrenner style", 250), ("1306", "Holder, EHT style", 250)]
SMALL_R = ["1180", "1181", "1182", "1183", "1184", "1185", "1186", "1187"]
ROUND_R = ["1100", "1101", "1102", "1103", "1037", "1104", "1106", "1107", "1108", "1109", "1038", "1110", "1111", "1039", "1112", "1040", "1113",
           "1041", "1114", "1042", "1115", "1116", "1117", "1118"]


def _tool(code):
    return D.TOOLS.get(code) or {"code": code, "sizes": [], "len_web": None, "style": None}


def acc_table(title, sub, rows, cols, first_col="Code"):
    """hand-built table for accessories: rows = [code, cells…]; codes with a DXF get a link in the last column if 'Profile' is a
    col.  A 'Lengths' / 'Length' column is replaced by the lengths-and-weights columns (D.with_lengths)."""
    cols = list(cols)
    li = next((i for i, c in enumerate(cols) if c in ("Lengths", "Length")), None)
    out = []
    for r in rows:
        code, cells = r[0], list(r[1:])
        if li is not None:
            cells.pop(li)
        if "Profile" in cols:
            cells.append(D.dxf_cell(code))
        out.append([code] + cells)
    if li is not None:
        cols.pop(li)
    tab = {"title": title, "sub": sub, "cols": cols, "rows": out, "first_col": first_col, "desc": True}
    return D.with_lengths(tab, [_tool(r[0]) for r in rows]) if li is not None else tab


def roll_table(title, codes):
    """film and cloth come in rolls: the price list's sizes are roll lengths in metres, with the weight of each roll"""
    rows = []
    for c, d in codes:
        t = D.TOOLS.get(c) or {}
        rl = [(int(m.group(1)), D.num(w)) for sz, w in t.get("sizes", []) for m in [re.match(r"^(\d+)\s*m$", sz.strip())] if m]
        rows.append([c, d, " · ".join(f"{m * 3.2808:.0f} ft ({m} m)" for m, _ in rl) or "—",
                     " · ".join(f"{D.lb_s(w)} ({D.kg_s(w)})" for _, w in rl if w) or "—"])
    return {"title": title, "sub": "", "cols": ["Part", "Roll length", "Weight per roll"], "rows": rows, "first_col": "Code", "desc": True}


LEN_TEXT = {"4308": "roll of 33 m (108 ft)", "4314": "roll of 33 m (108 ft)", "4379": "5 or 10 m (16 / 33 ft)", "4380": "5 or 10 m (16 / 33 ft)"}


def lens(code):
    """the lengths a part is sold in; film and cloth come by the metre (the price list's sizes are roll lengths in m)"""
    if code in LEN_TEXT:
        return LEN_TEXT[code]
    t = D.TOOLS.get(code)
    return D.lengths_text(D.lengths(t)) if t else "—"


rad_el = [D.TOOLS[c] for c in SMALL_R + ROUND_R if c in D.TOOLS and not D.TOOLS[c]["discontinued"]]
family("es-eu-radius", P_EUP, "Radius punches: holders and round elements R3 – R50", "Radius punches",
       "For a large inside radius — cabinet and enclosure corners, tank shells, architectural trim, rolled-look profiles — a radius "
       "holder clamps in the European-style beam and takes a round element of the radius you need: small elements from R3 to R6.5 in an "
       "H60 holder, round elements from R7 to R50 in straight (H67 and H100) or gooseneck (H87 and H115) holders, and a flat element for "
       "flattening. Changing the radius means changing a bar, not buying a punch. Holders for Bystronic, Trumpf, Weinbrenner and EHT press "
       "brakes take the same elements.",
       ["Round elements R7 to R50 (.28 – 1.97″) in 24 sizes; small elements R3 to R6.5 (.12 – .26″)",
        "Straight holders H67 and H100, gooseneck holders H87 and H115, small-element holders H60 — European style",
        "Holders for Bystronic type R / RF-A, Trumpf, Weinbrenner and EHT press brakes",
        "Elements in 835 and 415 mm (32.9 / 16.3″) lengths; holders 830 and 410 mm", "Flat element (1043) for flattening hems"],
       [acc_table("Holders", "European style unless noted", [(c, d, D.height(h) if h else "—", lens(c)) for c, d, h in RADIUS_HOLDERS],
                  ["Holder", "Height H", "Lengths"]),
        acc_table("Round and flat elements", "bend radius = element radius", [(t["code"], ("Small element" if t["code"] in SMALL_R else "Round element"),
                                                                              D.radius(t["spec"].get("r") or t["r"] or 0).replace("R ", "R "), lens(t["code"])) for t in rad_el]
                  + [("1043", "Flat element", "flat, H 17 mm", lens("1043"))], ["Element", "Radius", "Lengths"])],
       images=["es-p-radius-press", "es-p-c013", "es-p-radius-hand", "es-w-1096", "es-w-1090", "es-w-1041", "es-w-1297", "es-w-1180"], tools=[], ndraw=0, glance_tools=[],
       models_label="holders 1036 – 1306 · round elements R3 – R50", headline="Round elements R3 – R50 (.12 – 1.97″) in 12 holders",
       family_row=[f"{len(RADIUS_HOLDERS) + len(rad_el) + 1} · holders + elements", "radius R3 – R50", "holders H 2.36 – 9.84″ (60 – 250 mm)", "—"])

JOGGLE = sorted([t for t in D.TOOLS.values() if t["spec"].get("z") is not None and not t["discontinued"]], key=lambda t: (t["spec"]["z"], t["code"]))
family("es-eu-joggle", P_EUP, "Offset (joggle) tools, Z 1 – 15 mm", "Offset tools",
       "An offset tool bends a Z — two opposite bends a short distance apart — in one stroke: for lap joints that sit flush, stepped "
       "flanges, frames and enclosure doors. A pair of inserts works in a pair of holders, upper and lower; the inserts set the offset "
       "height Z, from 1 to 15 mm (.04 – .59″), at 90° for most sizes and 140° to 160° for the shallow offsets in thin sheet. Holders "
       "in European style, Bystronic R / RF-A and Trumpf / Wila style take the same inserts.",
       ["Offset heights Z 1 to 15 mm (.04 – .59″); 90° inserts from Z 2, 140° – 160° inserts for Z 1 to 2.5",
        "Insert pairs in 835 and 415 mm (32.9 / 16.3″) lengths", "Holders: European style 1150, Bystronic type R and RF-A 1198, Trumpf / Wila style 1242",
        "Tell us the sheet thickness with the offset — we check the pair against EUROSTAMP's table before you order"],
       [acc_table("Holders", "a pair, upper and lower", [("1150", "Joggle insert holders, European style", lens("1150")),
                                                       ("1198", "Joggle insert holders, Bystronic type R and RF-A", lens("1198")),
                                                       ("1242", "Joggle insert holders, Trumpf / Wila style", lens("1242"))], ["Holder pair", "Lengths"]),
        acc_table("Offset inserts", "a pair, upper and lower", [(t["code"], f"Z {D.inch(t['spec']['z'])} ({D.g(t['spec']['z'])} mm)",
                                                               f"{D.g((t['spec'].get('angles') or [90])[0])}°", lens(t["code"])) for t in JOGGLE],
                  ["Offset Z", "Angle", "Lengths"])],
       images=["es-p-joggle-press", "es-p-joggle-press2", "es-p-joggle-insert", "es-p-joggle-holder", "es-w-1150", "es-w-1198", "es-w-1135", "es-w-1130"], tools=[], ndraw=0, glance_tools=[],
       models_label="insert pairs 1130 – 1280 · holders 1150, 1198, 1242", headline="Z 1 – 15 mm (.04 – .59″), 90° – 160°",
       family_row=[f"{len(JOGGLE) + 3} · inserts + holders", "90° – 160°", "Z .04 – .59″ (1 – 15 mm)", "—"])

# ================================================================================================= European dies
eu_1v = dtyped(by_v(P("amada", "die", dtype=["1V"])))
eu_multi = dtyped(sorted(P("amada", "die", dtype=["2V bolted", "2V self-centring", "4V", "U"]), key=lambda t: (D.die_type(t), -(t["angle"] or 0), t["v"][0] if t["v"] else 0)))
for _t in eu_multi:                    # a U die has no bend angle (the shop lists 10°)
    if D.die_type(_t) == "U":
        _t["angle"] = None
eu_ins = dtyped(by_v(P("amada", "die", dtype=["Insert"])))
eu_t = dtyped(by_v(P("amada", "die", dtype=["T die"])))
eu_hem = dtyped(sorted(P("amada", "die", dtype=["Hemming", "Pneumatic hemming"]), key=lambda t: (D.die_type(t), -(t["angle"] or 0), t["v"][0] if t["v"] else 0)))
esh_d = dtyped(by_v(P("esh", "die")), {"Insert": "ESH insert"})
holders = {c: D.TOOLS[c] for c in ["2018", "2039", "2019", "2035", "2058", "2059", "2060", "3173"]}
HOLDER_TXT = {"2018": ("Holder for bolted 2V dies", 34), "2039": ("Holder for bolted 2V dies", 39), "2019": ("Holder for bolted 2V dies", 55),
              "2035": ("Holder for bolted 2V dies", 75), "2058": ("Rail for self-centring dies, on a holder", 10),
              "2059": ("Rail for self-centring dies, on the lower beam", 20), "2060": ("Stopper for sectioned self-centring dies", None),
              "3173": ("ESH insert die holder, with urethane strip", 61.5)}

family("es-eu-1v", P_EUD, "1V dies, V 18 – 220 mm", "1V dies",
       "The solid one-V die: a 60 mm (2.36″) wide block, the standard European-style die for air bending sheet and plate. 85° dies with V "
       "openings from 32 to 80 mm (1.26 – 3.15″) cover 90° bends from about 5/32 to 3/8″ plate by the 8 × thickness rule; 80° dies with V100 "
       "to V160 take heavier plate, and the V220 die stands 190 mm (7.48″) tall for 1″ plate and up to 200 t/m (67 US t/ft). The 60°, "
       "45° and 30° dies are for acute bends and the first stage of a hem.",
       ["V openings 18 to 220 mm (.71 – 8.66″); angles 85°, 80°, 70°, 60°, 45° and 30°",
        "Working heights 60 to 190 mm (2.36 – 7.48″); rated 100 to 200 t/m (34 – 67 US t/ft)",
        "835 and 415 mm (32.9 / 16.3″) lengths; 805 mm (31.7″) sectioned set: 10, 15, 20, 40, 50, 100, 200 and 370 mm",
        "C45 steel, tempered; V and shoulders induction-hardened 55 – 60 HRC"],
       [T("1V dies", "solid, 60 mm (2.36″) wide", eu_1v, DIE_COLS)],
       images=["es-p-c055", "es-p-c041", "es-std-eu-die"], tools=eu_1v, videos=[VIDEO_ESA],
       headline="V .71 – 8.66″ (18 – 220 mm), to 67 US t/ft", family_row=frow(eu_1v))

family("es-eu-multiv", P_EUD, "2V, 4V and U dies with holders", "Multi-V dies",
       "Several openings in one die, for shops that change jobs often: turn the die and the next V is ready. The bolted 2V dies are 26 mm "
       "(1.02″) low and sit in a holder 34, 39, 55 or 75 mm high; the self-centring 2V dies are 46 mm (1.81″) high and reversible, "
       "centring themselves on their rail. The 4V dies are 60 mm (2.36″) square blocks with a V on each face — 16, 22, 35 and 50 mm at "
       "85° – 88°, or 10 to 35 mm at 60° — and the 3U die has U channels of 6, 10 and 18 mm for flanges and channels.",
       ["Bolted 2V dies, H26, V 6/10 to 16/25 mm, 88° and 60°, with holders H34, H39, H55 and H75",
        "Self-centring reversible 2V dies, H46, V 6/10 to 16/25 mm, 88°, 85° and 30°",
        "4V dies, 60 mm square: V16 / 22 / 35 / 50 at 85° – 88°, V10 / 16 / 22 / 35 at 60°",
        "3U die, 60 mm square, U 6, 10 and 18 mm", "835 and 415 mm (32.9 / 16.3″) lengths; 805 mm sectioned sets on the self-centring and 4V dies"],
       [T("2V, 4V and 3U dies", "", eu_multi, DIE_COLS),
        acc_table("Holders and rails", "for the bolted 2V and the self-centring dies",
                  [(c, HOLDER_TXT[c][0], D.height(HOLDER_TXT[c][1]) if HOLDER_TXT[c][1] else "—", lens(c)) for c in ["2018", "2039", "2019", "2035", "2058", "2059", "2060"]],
                  ["Part", "Height H", "Lengths", "Profile"])],
       images=["es-p-c047", "es-p-c067a"], tools=eu_multi, headline="2V, 4V and 3U, V .24 – 1.97″ (6 – 50 mm)", family_row=frow(eu_multi))

family("es-eu-insert", P_EUD, "Self-centring 1V dies, V 4 – 25 mm", "Self-centring dies",
       "Slim one-V dies, 14 mm (.55″) wide and 60 mm (2.36″) high, that centre themselves on a rail: narrow enough for short flanges and "
       "return bends close to the die, and quick to change because the rail lines them up under the punch. 88° dies from V4 to V25 for "
       "thin sheet, 60° and 30° dies for acute bends and pre-hemming. The rails come for the lower beam (2059) or for a holder (2058).",
       ["V openings 4 to 25 mm (.16 – .98″); angles 88°, 60° and 30°", "14 mm (.55″) wide, 60 – 65 mm (2.36 – 2.56″) high; rated to 100 t/m (34 US t/ft)",
        "835 and 415 mm (32.9 / 16.3″) lengths; 805 mm (31.7″) sectioned set", "Rails 2058 (on a holder) and 2059 (on the lower beam); stopper 2060 for sectioned dies"],
       [T("Self-centring 1V dies", "14 mm (.55″) wide", eu_ins, DIE_COLS)],
       images=["es-p-c066"], tools=eu_ins, headline="V .16 – .98″ (4 – 25 mm), 14 mm (.55″) wide", family_row=frow(eu_ins))

family("es-eu-tdie", P_EUD, "T dies, V 6 – 25 mm, 80 and 120 mm high", "T dies",
       "A slim die body on a 60 mm (2.36″) T-shaped foot: the foot clamps in the European-style lower beam like a block die, and the "
       "narrow body leaves room for return flanges, hems and closed profiles that would hit a solid die. Seventy profiles in two heights — "
       "80 and 120 mm (3.15 / 4.72″) — at 88°, 85°, 60°, 45° and 30°, with V openings from 6 to 25 mm (.24 – .98″).",
       ["Working heights 80 and 120 mm (3.15 / 4.72″) on a 60 mm (2.36″) foot", "V 6 to 25 mm (.24 – .98″); 88°, 85°, 60°, 45° and 30°",
        "Rated to 100 t/m (34 US t/ft)", "835 and 415 mm (32.9 / 16.3″) lengths; 805 mm (31.7″) sectioned set", "C45 steel, induction-hardened"],
       [T("T dies, 80 mm high", "", [t for t in eu_t if (t["h"] or 0) < 100], DIE_COLS),
        T("T dies, 120 mm high", "", [t for t in eu_t if (t["h"] or 0) >= 100], DIE_COLS)],
       images=["es-p-c039"], tools=eu_t, headline="H 3.15 / 4.72″, V .24 – .98″ (6 – 25 mm)", family_row=frow(eu_t))

family("es-eu-hem", P_EUD, "Hemming dies, mechanical and pneumatic", "Hemming dies",
       "A hemming (flattening) die pre-bends and closes a hem on one press brake with one punch: an acute V on top pre-bends the flange to "
       "about 30°, and the spring-loaded upper plate then flattens it in the second stroke. The 35°, 30° and 26° dies are 100 to 135 mm "
       "(3.96 – 5.31″) high with V6 to V12 for sheet to about 1/8″; the 24° and 28° dies are lower, 80 mm (3.15″). The pneumatic versions "
       "(PN) open and close with shop air — kit 4313 connects them.",
       ["Spring-loaded hemming dies, V 6 to 12 mm (.24 – .47″), 24° to 35°", "Pneumatic hemming dies 3038PN – 3041PN; connection kit 4313",
        "Working heights 80 to 135 mm (3.15 – 5.31″); rated 50 to 100 t/m (17 – 34 US t/ft)",
        "835 and 415 mm (32.9 / 16.3″) lengths; the 80 mm dies also as an 805 mm sectioned set", "Use with the 24° – 35° acute and hemming punches"],
       [T("Hemming dies", "", eu_hem, DIE_COLS)],
       images=["es-p-c071"], tools=eu_hem, headline="V .24 – .47″, mechanical and pneumatic", family_row=frow(eu_hem))

family("es-esh-die", P_EUD, "ESH insert dies and holder", "ESH insert dies",
       "The lower half of the ESH series: one-V inserts 14 mm (.55″) wide and 60 mm (2.36″) high in the 3173 holder, which clamps in the "
       "European-style lower beam and holds them on a urethane strip. The inserts are nitrided all over to 65 HRC — the walls of the V, "
       "not just the shoulders, so they resist scoring and pick-up — and phosphate-coated; wide shoulder radii mark the sheet less, and "
       "chamfered corners avoid collisions with flanges already bent. 86° inserts V6 to V25, 30° inserts V6 to V25.",
       ["ESH inserts 86° and 30°, V 6 to 25 mm (.24 – .98″); shoulder radius R1 to R4", "Holder 3173: H 61.5 mm (2.42″) with a urethane strip",
        "Nitrided all over to 65 HRC, phosphate-coated; rated to 100 t/m (34 US t/ft)",
        "835 and 415 mm (32.9 / 16.3″) lengths; 800 mm (31.5″) sectioned set: 100, 10, 15, 15, 20, 40, 50, 150 and 400 mm"],
       [T("ESH insert dies", "14 mm (.55″) wide, 60 mm (2.36″) high", esh_d, ["v", "angle", "rs", "load", "len", "dxf"]),
        acc_table("Holder", "", [("3173", "ESH insert die holder, with urethane strip", D.height(61.5), lens("3173"))], ["Part", "Height H", "Lengths", "Profile"])],
       images=["es-p-c078b", "es-p-c067b"], tools=esh_d, headline="V .24 – .98″, nitrided to 65 HRC", family_row=frow(esh_d))

# ================================================================================================= Trumpf & Wila
tr_p = ptyped(P("trumpf", "punch"))
tr_d = dtyped(by_v(P("trumpf", "die") + [D.TOOLS[c] for c in ("3157", "3174") if D.TOOLS[c]["style"] != "trumpf"]))
wi_p = ptyped(P("wila", "punch"))
wi_d = dtyped(by_v(P("wila", "die")))

family("es-tr-punch", P_TW, "Trumpf-style punches, 26° – 86°", "Trumpf punches",
       "Punches with the Trumpf tang, for Trumpf press brakes and the Darley, Safan and other brakes with Wila-style (New Standard) "
       "clamping. Tall bodies — 140 to 300 mm (5.51 – 11.81″) — for deep boxes: straight and acute 26° and 28° punches, 86° goosenecks "
       "to the 300 mm deep-box punch, sash punches, 28° hemming punches and two 60° heavy-duty punches with R4 tips rated to 250 t/m "
       "(84 US t/ft). Safety buttons that stop a released tool from falling are fitted as standard on every tool up to 13.5 kg (30 lb).",
       ["Angles 86°, 80°, 60°, 28° and 26°; working heights 140 to 300 mm (5.51 – 11.81″)", "Tip radius R0.5 to R4; rated up to 250 t/m (84 US t/ft)",
        "Safety buttons standard on tools up to 13.5 kg (30 lb)",
        "500 mm (19.7″) lengths, 100 – 300 mm pieces and the 550 mm (21.7″) sectioned set with horns", "42CrMo4 or C45 steel, induction-hardened"],
       [T("Trumpf-style punches", "", tr_p, PUNCH_COLS)],
       images=["es-p-c091", "es-p-c107", "es-std-tr-punch"], tools=tr_p, headline="H 5.51 – 11.81″, to 84 US t/ft", family_row=frow(tr_p))

family("es-tr-die", P_TW, "Trumpf-style dies, V 6 – 120 mm", "Trumpf dies",
       "One-V dies with the Trumpf tang in two heights, 100 and 150 mm (3.94 / 5.91″) — and 120 mm for the big V openings: 86° and 84° "
       "dies from V6 to V50 for sheet, 80° dies from V24 to V100 and a 60° V120 die for plate, and 30° dies for acute bends and the "
       "first stage of a hem. The 32xx series is 42CrMo4 steel; the hemming dies 3157, 3174 and 3175 (U 8.1 to 12.1 mm) close the hem "
       "after the acute pre-bend.",
       ["V openings 6 to 120 mm (.24 – 4.72″); 86°, 84°, 80°, 60°, 30° and 24° hemming", "Working heights 100, 120 and 150 mm (3.94 – 5.91″); rated to 160 t/m (54 US t/ft)",
        "500 mm (19.7″) lengths, 25 – 300 mm pieces and the 550 mm (21.7″) sectioned set", "Hemming dies with U 8.1, 10.1 and 12.1 mm",
        "Safety buttons standard on tools up to 13.5 kg (30 lb)"],
       [T("Trumpf-style 1V dies", "86° – 84°", [t for t in tr_d if D.die_type(t) == "1V" and (t["angle"] or 0) >= 84], DIE_COLS),
        T("Trumpf-style 1V dies", "80°, 60° and 30°", [t for t in tr_d if D.die_type(t) == "1V" and (t["angle"] or 0) < 84], DIE_COLS),
        T("Hemming dies", "Trumpf, Wila and Bystronic style", [t for t in tr_d if D.die_type(t) == "Hemming"], ["u", "h", "load", "len", "mat", "dxf"])],
       images=["es-p-c110", "es-std-tr-die", "es-std-tr-sets"], tools=tr_d, headline="V .24 – 4.72″ (6 – 120 mm), to 54 US t/ft", family_row=frow(tr_d))

family("es-wi-punch", P_TW, "Wila-style punches, 28° – 86°", "Wila punches",
       "Punches in Wila style (New Standard) for Wila clamping on Trumpf, Darley, RPC, Safan and other press brakes: straight 80° punches "
       "157 to 237 mm (6.18 – 9.33″) high, 28° acute punches from 135 mm, 86° goosenecks to 237 mm and 60° heavy-duty punches with R3 "
       "tips rated to 160 t/m (54 US t/ft). Safety buttons are fitted as standard on tools up to 12.5 kg (27.5 lb).",
       ["Angles 86°, 80°, 60° and 28°; working heights 135 to 237 mm (5.31 – 9.33″)", "Tip radius R1 and R3; rated up to 160 t/m (54 US t/ft)",
        "Safety buttons standard on tools up to 12.5 kg (27.5 lb)", "515 mm (20.3″) lengths, 100 and 200 mm pieces, 550 mm (21.7″) sectioned set",
        "42CrMo4 steel, tempered and induction-hardened"],
       [T("Wila-style punches", "", wi_p, PUNCH_COLS)],
       images=["es-p-c147"], tools=wi_p, headline="H 5.31 – 9.33″, to 54 US t/ft", family_row=frow(wi_p))

family("es-wi-die", P_TW, "Wila-style dies, V 6 – 24 mm", "Wila dies",
       "One-V dies in Wila style in two heights: the low 55 mm (2.17″) dies for maximum stroke and daylight, and 100 mm (3.94″) dies "
       "rated to 120 t/m (40 US t/ft). 86° dies from V6 to V24, 80° for heavier sheet and 30° dies for acute bends and pre-hemming. "
       "42CrMo4 steel, tempered and induction-hardened.",
       ["V 6 to 24 mm (.24 – .94″); 86°, 80° and 30°", "Heights 55 and 100 mm (2.17 / 3.94″); rated 35 to 120 t/m (12 – 40 US t/ft)",
        "515 mm (20.3″) lengths, 100 and 200 mm pieces, 550 mm (21.7″) sectioned set", "42CrMo4 steel"],
       [T("Wila-style dies, 55 mm high", "", [t for t in wi_d if (t["h"] or 0) < 80], DIE_COLS),
        T("Wila-style dies, 100 mm high", "", [t for t in wi_d if (t["h"] or 0) >= 80], DIE_COLS)],
       images=["es-p-c164"], tools=wi_d, headline="V .24 – .94″, H 2.17 / 3.94″", family_row=frow(wi_d))

# ================================================================================================= Bystronic & LVD
by_p = ptyped(P("bystronic", "punch"))
by_d = dtyped(by_v(P("bystronic", "die") + [D.TOOLS["3175"]]))
lvd_p = ptyped(P("lvd", "punch"))
lvd_d = dtyped(by_v(P("lvd", "die")))
for t in lvd_p + lvd_d:                    # the shop gives 510 mm on some LVD tools; it is the standard length of the series
    t["sizes"] = t["sizes"] or [("510", "")]

family("es-by-punch", P_BL, "Bystronic-style punches, type R and RF-A", "Bystronic punches",
       "Punches for Bystronic and Beyeler press brakes with type R, RF and RF-A clamping: straight and acute 28° and 30° punches 155 to "
       "250 mm (6.10 – 9.84″) high, 85° – 88° goosenecks, sash punches, and 24° flattening blades 8, 10 and 12 mm thick for hemming. The "
       "type R and RF-A tangs differ — tell us the clamping of your brake, or send a photo of a tool you already use.",
       ["Type R (155 mm) and RF-A (175 mm) punches; type R / RF-A punches 250 mm (9.84″) high", "Angles 88°, 86°, 85°, 30°, 28° and 24°; tip radius R0.6 to R3",
        "Rated to 140 t/m (47 US t/ft)", "500 mm (19.7″) and 1,000 mm lengths, 100 mm pieces, 550 and 1,100 mm sectioned sets with horns"],
       [T("Bystronic-style punches", "", by_p, PUNCH_COLS)],
       images=["es-p-c180", "es-p-c171", "es-std-by-punch"], tools=by_p, headline="Type R and RF-A, H 6.10 – 9.84″", family_row=frow(by_p))

family("es-by-die", P_BL, "Bystronic-style dies, V 6 – 60 mm", "Bystronic dies",
       "One-V dies for Bystronic and Beyeler lower beams, 55 to 65 mm (2.17 – 2.56″) high: 88° dies V6 to V24, 85° V32 and V40, 60° "
       "V40 to V60 and 30° dies V6 to V32 — plus the hemming dies with U 8.1, 10.1 and 12.1 mm that close the hem after the flattening "
       "blade's pre-bend.",
       ["V 6 to 60 mm (.24 – 2.36″); 88°, 85°, 60° and 30°", "Heights 55 to 65 mm (2.17 – 2.56″); rated to 100 t/m (34 US t/ft)",
        "Hemming dies 3157, 3174 and 3175", "500 and 1,000 mm (19.7 / 39.4″) lengths, 100 mm pieces, 550 and 1,100 mm sectioned sets"],
       [T("Bystronic-style 1V dies", "", [t for t in by_d if D.die_type(t) == "1V"], DIE_COLS),
        T("Hemming dies", "Bystronic, Trumpf and Wila style", [t for t in by_d if D.die_type(t) == "Hemming"], ["u", "h", "load", "len", "mat", "dxf"])],
       images=["es-std-by-die"], tools=by_d, headline="V .24 – 2.36″ (6 – 60 mm), H 2.17 – 2.56″", family_row=frow(by_d))

family("es-lvd-punch", P_BL, "LVD-style punches, 20° – 78°", "LVD punches",
       "Punches for LVD press brakes, 196 mm (7.72″) high: 78° straight punches with R1 and R2 tips rated to 75 t/m (25 US t/ft) for "
       "90° air bending, 26° acute punches to 80 t/m and a 20° hemming punch 206 mm (8.11″) high. 42CrMo4 steel, 510 mm (20.1″) long.",
       ["78° and 26° punches, 196 mm (7.72″) high; 20° hemming punch, 206 mm", "Tip radius R1 and R2; rated 40 to 80 t/m (13 – 27 US t/ft)",
        "510 mm (20.1″) lengths", "42CrMo4 steel"],
       [T("LVD-style punches", "", lvd_p, PUNCH_COLS)],
       images=[], tools=lvd_p, headline="H 7.72 – 8.11″, 20° – 78°", family_row=frow(lvd_p))

family("es-lvd-die", P_BL, "LVD-style dies, V 6 – 120 mm", "LVD dies",
       "One-V dies for LVD lower beams in two heights, 90 and 130 mm (3.54 / 5.12″): 78° dies from V6 to V120 for 90° air bending of "
       "sheet and plate — rated up to 340 t/m (114 US t/ft) on the V100 die — 30° dies from V6 to V60 for acute bends, and a 20° hemming "
       "die. 42CrMo4 steel, 510 mm (20.1″) long.",
       ["V 6 to 120 mm (.24 – 4.72″); 78°, 30° and 20° hemming", "Heights 90 and 130 mm (3.54 / 5.12″); rated 21 to 340 t/m (7 – 114 US t/ft)",
        "510 mm (20.1″) lengths", "42CrMo4 steel"],
       [T("LVD-style dies, 90 mm high", "", [t for t in lvd_d if (t["h"] or 0) < 110], DIE_COLS),
        T("LVD-style dies, 130 mm high", "", [t for t in lvd_d if (t["h"] or 0) >= 110], DIE_COLS)],
       images=[], tools=lvd_d, headline="V .24 – 4.72″, to 114 US t/ft", family_row=frow(lvd_d))

# ================================================================================================= American style (NovoTech's American-style brochure)
AM_P = [("S28932", "EP2-88", "Straight", 88, 95.98, 1.5, "36″ · 18″ · 35.75″ sect."),
        ("S28881", "EGPC 88", "Gooseneck", 88, 95.99, 0.8, "36″ · 18″ · 35.75″ sect."),
        ("S28880", "EGPC 85", "Gooseneck", 85, 95.99, 0.8, "36″ · 18″ · 35.75″ sect."),
        ("S28974", "EGP-7A-88", "Straight", 88, 95.97, 0.8, "36″ · 18″ · 35.75″ sect."),
        ("S29083", "EP30", "Acute", 30, 96.0, 1.5, "36″ · 18″ · 35.75″ sect."),
        ("S29252", "—", "Acute", 28, 96.01, 0.8, "on request"),
        ("S29084", "EGP28", "Acute gooseneck", 28, 130.18, 0.8, "36″ · 18″ · 35.75″ sect.")]
AM_D = [("S28946", "ELD88-3/8", "1V", 88, 9.53, 1.14, 25.4, "36″ · 18″ · 35.75″ sect."),
        ("S29269", "—", "1V", 88, 12.70, 0.99, 25.4, "on request"),
        ("S29145", "ELD88-5/8", "1V", 88, 15.90, 1.91, 25.4, "36″ · 18″ · 35.75″ sect."),
        ("S28947", "ELD88-3/4", "1V", 88, 19.05, 3.81, 38.1, "36″ · 18″ · 35.75″ sect."),
        ("S29142", "ELD30-3/8", "Acute 1V", 30, 9.53, 1.14, 25.4, "36″ · 18″ · 35.75″ sect."),
        ("S29141", "ELD30-1/2", "Acute 1V", 30, 12.70, 1.14, 25.4, "36″ · 18″ · 35.75″ sect."),
        ("S29143", "ELD30-5/8", "Acute 1V", 30, 16.13, 1.50, 38.1, "36″ · 18″ · 35.75″ sect."),
        ("S29144", "ELD34-7/8", "Acute 1V", 34, 22.23, 2.31, 50.8, "36″ · 18″ · 35.75″ sect.")]
AM_DRAW = {"S28932": "x40", "S28881": "x43", "S28880": "x45", "S29083": "x49", "S29252": "x51", "S29084": "x53",
           "S28946": "x57", "S29269": "x59", "S29145": "x61", "S28947": "x63", "S29142": "x67", "S29141": "x69", "S29143": "x71", "S29144": "x73"}


def am_in(mm):
    return f"{D.inch(mm)} ({mm:.2f} mm)"


am_p_tab = {"title": "American-style punches", "sub": "tang .500″ (12.7 mm) with safety lip", "first_col": "Part no.",
            "cols": ["Model", "Type", "Angle", "Height H", "Tip radius", "Lengths"],
            "rows": [[c, m, ty, f"{a}°", am_in(h), f"R {D.inch(r)} ({r:g} mm)", ln] for c, m, ty, a, h, r, ln in AM_P]}
am_d_tab = {"title": "American-style dies", "sub": "working height 1.937″ (49.2 mm), 2.563″ (65.1 mm) overall · tang .500″ (12.7 mm)", "first_col": "Part no.",
            "cols": ["Model", "Type", "V opening", "Angle", "Shoulder radius", "Body width", "Lengths"],
            "rows": [[c, m, ty, am_in(v), f"{a}°", f"R {D.inch(r)} ({r:g} mm)", am_in(w), ln] for c, m, ty, a, v, r, w, ln in AM_D]}
AM_NOTE = ("Part numbers are EUROSTAMP designations: add 091401 for the 36″ (914.4 mm) full length, 045701 for the 18″ (457.2 mm) half "
           "length and 090801 for the 35.75″ (908 mm) sectioned set — S28881 091401 is the 36″ gooseneck punch. Dimensions in decimal "
           "inches with the exact metric equivalent.")
family("es-am-punch", P_AM, "American-style punches, 28° – 88°", "American punches",
       "Punches with the .500″ (12.7 mm) American tang and safety lip, for the American-style clamping used on most North American press "
       "brakes: 88° straight punches and 88° and 85° goosenecks for 90° air bending, 30° and 28° acute punches for hemming and acute "
       "angles, and a 28° acute gooseneck 5.125″ (130.18 mm) tall. Working height 3.779″ (96 mm); 36″ full lengths, 18″ half lengths and "
       "35.75″ sectioned sets, each with its own part number.",
       ["Tang .500″ (12.7 mm), .626″ (15.9 mm) with the safety lip; tang height .752″ (19.1 mm)",
        "88°, 85°, 30° and 28°; working height 3.779″ (96 mm) — 5.125″ (130.18 mm) on the acute gooseneck",
        "Tip radius R .031″ (0.8 mm) and R .059″ (1.5 mm)", "36″ (914.4 mm), 18″ (457.2 mm) and 35.75″ (908 mm) sectioned"],
       [am_p_tab], images=["es-am-" + c.lower() for c, *_ in AM_P if c in AM_DRAW] + ["es-am-sect"], tools=[], ndraw=0, glance_tools=[], note=AM_NOTE, pdf=None,
       models_label="S28880 – S29252 · 7 profiles", headline="Tang .500″, H 3.779 – 5.125″",
       family_row=["7", "28° – 88°", "3.779 – 5.125″ (96 – 130.2 mm)", "—"],
       extra_caps={c: f"{a}° · R {D.inch(r)} · H {D.inch(h)}" for c, m, ty, a, h, r, ln in AM_P})
family("es-am-die", P_AM, "American-style dies, V .375 – .875″", "American dies",
       "One-V dies with the .500″ American tang, all with the same 1.937″ (49.2 mm) working height so punches and dies stay in step "
       "when you change V: 88° dies with V .375, .500, .626 and .750″ for 90° air bending of 16 gauge to 3/32″, and 30° and 34° acute dies "
       "from V .375 to .875″ for hemming and acute bends. Body widths 1.000, 1.500 and 2.000″.",
       ["V .375 to .875″ (9.53 – 22.23 mm); 88°, 34° and 30°", "Working height 1.937″ (49.2 mm), 2.563″ (65.1 mm) overall",
        "Body widths 1.000, 1.500 and 2.000″ (25.4 / 38.1 / 50.8 mm)", "36″, 18″ and 35.75″ sectioned"],
       [am_d_tab], images=["es-am-" + c.lower() for c, *_ in AM_D if c in AM_DRAW], tools=[], ndraw=0, glance_tools=[], note=AM_NOTE, pdf=None,
       models_label="S28946 – S29269 · 8 profiles", headline="V .375 – .875″, H 1.937″",
       family_row=["8", "30° – 88°", "1.937″ (49.2 mm)", "—"],
       extra_caps={c: f"{a}° · V {D.inch(v)} · H 1.937″" for c, m, ty, a, v, r, w, ln in AM_D})

am_i_tab = {"title": "American-style Z1 intermediate", "sub": "EUROSTAMP drawing in millimetres, here in decimal inches with the millimetres",
            "first_col": "Part no.",
            "cols": ["Fits", "Takes", "Height", "Body depth", "Bending axis", "Lengths"],
            "rows": [["On request", "Brakes built for Z1 intermediates", "American punches, .500″ (12.7 mm) tang",
                      "3.937″ (100 mm) + 1.181″ (30 mm) tang", "1.063″ (27 mm)", ".276″ (7 mm) from tang face", "on request"]]}
family("es-am-inter", P_AM, "American-style Z1 intermediate", "Z1 intermediate",
       "An upper intermediate that puts American-style punches on press brakes built for Z1 intermediates (Amada-Promecam European "
       "style). The body is a standard Z1 — 3.937″ (100 mm) high under a 1.181″ (30 mm) upper tang, 1.063″ (27 mm) deep, with the "
       "bending axis .276″ (7 mm) from the tang face — so it lines up with the machine's other Z1 intermediates; the lower slot takes "
       "the .500″ (12.7 mm) American tang, with a .650″ (16.5 mm) pocket for its safety lip.",
       ["Fits press brakes built for Z1 intermediates (Amada-Promecam European style)",
        "Takes American-style punches: .500″ (12.7 mm) tang with the safety lip",
        "Height 3.937″ (100 mm) under a 1.181″ (30 mm) tang; body 1.063″ (27 mm), axis .276″ (7 mm)",
        "Part number, lengths and price on request"],
       [am_i_tab], images=["es-am-intermediate", "es-am-intermediate-tang"], tools=[], ndraw=0, glance_tools=[],
       note="EUROSTAMP drew this intermediate in millimetres; the inch values are converted exactly (1″ = 25.4 mm). Catalogue page 278.",
       pdf=None, models_label="Z1 · part number on request", headline="Z1 beam → .500″ American punches",
       family_row=["1 · intermediate", "—", "3.937″ (100 mm) + 1.181″ tang", "—"])

# ================================================================================================= holders, adapters, clamps, accessories
def h_of(code, default=None):
    t = D.TOOLS.get(code)
    return (t and t["h"]) or default


UPPER = [("4221", "Adjustable intermediate Z1 — body 27 mm, axis 7 mm, wedge for crowning", 100), ("4222", "Adjustable intermediate Z1, 27 / 7 mm", 120),
         ("4223", "Adjustable intermediate Z1, 27 / 7 mm", 150), ("4224", "Adjustable intermediate", 100),
         ("4225", "Adjustable intermediate Z2 — body 40 mm, axis 20 mm", 120), ("4073", "Heavy-duty adjustable intermediate, all CrMo steel, body 40 mm, axis 7 mm", 120),
         ("4411", "Heavy-duty adjustable intermediate, all CrMo steel, body 40 mm, axis 20 mm — 160 t/m", 120),
         ("4282", "Intermediate without wedge (extension), 27 / 7 mm", 100), ("4226", "Short intermediate without wedge (extension), 27 / 7 mm", 100),
         ("4227", "Short intermediate without wedge (extension), 27 / 7 mm", 150), ("4228", "Short intermediate Z2, 40 / 20 mm, not adjustable", 120)]
ADAPT = [("4362", "Amada / European beam → Trumpf / Wila punches", 67), ("4361", "Trumpf / Wila extension with safety pins", 100),
         ("4191", "Trumpf / Wila beam → Amada / European punches", 80), ("4192", "Beyeler type R → Amada / European punches", 67),
         ("4193", "Beyeler type S → Amada / European punches", None), ("4214", "Beyeler type RF-A → Amada / European punches", None),
         ("4215", "Weinbrenner → Amada / European punches", None), ("4216", "CBC → Amada / European punches", None),
         ("4217", "EHT → Amada / European punches", None), ("4218", "Durmazlar → Amada / European punches", None),
         ("4229", "Darley → Amada / European punches", None), ("4272", "Baykal → Amada / European punches", None),
         ("4273", "Colgar → Amada / European punches", None), ("4143", "LVD (S) → Amada / European punches", 80),
         ("4144", "LVD (M) → Amada / European punches — minimum 5 pieces", 80), ("4145", "LVD (L) → Amada / European punches — minimum 5 pieces", 80),
         ("4146", "LVD (XL) → Amada / European punches — minimum 5 pieces", 80),
         ("4000", "Upper adapter with your machine's tang, H59 — minimum 5 pieces", 59), ("4001", "Upper adapter with your machine's tang, H67 — minimum 5 pieces", 67),
         ("4002", "Upper adapter with your machine's tang, H100 — minimum 5 pieces", 100)]
family("es-acc-upper", P_ACC, "Intermediates and upper adapters", "Upper adapters",
       "The intermediate is the holder between the ram and a European-style punch: it carries the clamp and, on the adjustable versions, "
       "a wedge that crowns each section so the angle stays true along the bend. Z1 intermediates have a 27 mm (1.06″) body with the "
       "bending axis 7 mm from the face; Z2 intermediates a 40 mm (1.57″) body with the axis at 20 mm; the heavy-duty versions are solid "
       "CrMo steel. The upper adapters go the other way: they let a press brake with Trumpf / Wila, Beyeler, LVD, Weinbrenner, CBC, EHT, "
       "Durmazlar, Darley, Baykal or Colgar clamping run European-style punches — or a European-style beam run Trumpf / Wila punches. "
       "The Z1 intermediate for American-style punches is on the American-style tooling page.",
       ["Adjustable intermediates Z1 (H100, H120, H150) and Z2 (H120); heavy-duty CrMo versions rated to 160 t/m (54 US t/ft)",
        "Fixed intermediates and short extensions, 75 and 150 mm long", "Upper adapters to European-style punches from 12 clamping systems; European → Trumpf / Wila adapter",
        "Custom-tang upper adapters H59, H67 and H100 (minimum 5 pieces)", "150 mm (5.9″) long sections unless noted"],
       [acc_table("Intermediates", "European style (Amada-Promecam)", [(c, d, D.height(h_of(c, h)), lens(c)) for c, d, h in UPPER], ["Intermediate", "Height H", "Length", "Profile"]),
        acc_table("Upper adapters", "between clamping systems", [(c, d, D.height(h_of(c, h)) if h_of(c, h) else "—", lens(c)) for c, d, h in ADAPT],
                  ["Adapter", "Height H", "Length", "Profile"])],
       images=["es-w-4221", "es-p-c157", "es-w-4411", "es-w-4228", "es-w-4362", "es-w-4191", "es-w-4193", "es-w-4143s"], tools=[], ndraw=0, glance_tools=[],
       models_label="intermediates 4073 – 4411 · adapters 4000 – 4362", headline="Z1 / Z2 intermediates, adapters between 12 clamping systems",
       family_row=[f"{len(UPPER) + len(ADAPT)} · intermediates + adapters", "—", "H 2.32 – 5.91″ (59 – 150 mm)", "to 54 US t/ft (160 t/m)"])

CLAMPS = [("4021", "Safety clamp, top handle, with fixing screws", 60, 150), ("4009", "Safety clamp, fold-away handle", 60, 150),
          ("4020", "Safety clamp, simple", 60, 150), ("4219", "Safety clamp, top lever, urethane insert", 60, 150),
          ("4220", "Safety clamp, fold-away lever, urethane insert", 60, 150), ("4199", "Safety clamp, simple, urethane insert", 60, 150),
          ("4016", "Clamp, simple", 50, 150), ("4007", "Short safety clamp, top handle, with fixing screws", 59, 75),
          ("4090", "Short safety clamp, simple", 59, 75), ("4008", "Short clamp, top handle", 50, 75),
          ("5011", "Clamp", 52, 150), ("5012", "Clamp", 52, 150), ("5013", "Clamp with front screws, without safety tang", 43, 150),
          ("4031", "Double clamping set with rear clamp 4016", None, 150), ("4032", "Double clamping set with rear safety clamp 4020", None, 150),
          ("4281", "Special screw with spring for clamps 4007, 4021, 4219, 5011", None, None), ("4349", "Urethane strip, spare for 4199, 4220, 4319", None, 150)]
EUROGRIP = [("4389", "M-EASY: front clamp to retrofit a Z1 intermediate (body 27, axis 7 mm), H100"),
            ("4409", "M-EASY: front clamp and plate to retrofit a Z2 intermediate (body 40, axis 20 mm), H120"),
            ("4390", "M-TOP: front clamp assembled on a Z1 intermediate, H100"), ("4400", "M-TOP: front clamp assembled on a Z2 intermediate, H120"),
            ("4415", "M-TOP: front and rear clamp on a Z1 intermediate, H150"), ("4414", "M-TOP: front and rear clamp on a Z2 intermediate, H120"),
            ("4393", "M-WDP: upper adapter European → Wila / Trumpf punches, Z1, H100"),
            ("4392", "P-EASY Z1: pneumatic clamp on a Z1 intermediate, H100"), ("4405", "P-EASY Z2: pneumatic clamp on a Z2 intermediate, H120"),
            ("4391", "P-TOP Z1: pneumatic clamp for the upper beam (4399) with Z1 intermediate clamp (4398)"),
            ("4412", "P-TOP Z2: pneumatic clamp for the upper beam (4399) with Z2 intermediate clamp (4410)"),
            ("4408", "Optional rear clamp for M-EASY 4389 and 4409"), ("4404", "Optional rear clamp for M-TOP, P-EASY and P-TOP"),
            ("4394", "P-DHOLD: pneumatic die holder for European-style dies, 60 mm wide, H55"),
            ("4395", "Pneumatic control unit, single line (upper or lower)"), ("4396", "Pneumatic control unit, double line (upper and lower)"),
            ("4397", "P-EASY connection kit"), ("4381", "P-TOP connection kit")]
family("es-acc-clamps", P_ACC, "Clamps and the EUROGRIP clamping system", "Clamps & EUROGRIP",
       "Manual clamps for European-style intermediates — simple, with a top handle or a fold-away handle, with the safety tooth that "
       "catches a punch as it is released, and with a urethane insert that holds the tool without marking it — and EUROGRIP, EUROSTAMP's "
       "own clamping system. Each EUROGRIP clamp is worked by a recessed handle on top, so nothing stands proud to hit the part; the "
       "M-EASY clamps retrofit existing Z1 and Z2 intermediates, the M-TOP clamps come assembled on new intermediates, and the P-EASY and "
       "P-TOP versions clamp a whole beam of punches pneumatically from one control unit.",
       ["Safety clamps 59 – 60 mm high, 75 and 150 mm long, with or without urethane insert", "EUROGRIP manual: M-EASY retrofit, M-TOP assembled, M-WDP adapter for Wila / Trumpf punches",
        "EUROGRIP pneumatic: P-EASY and P-TOP clamps, P-DHOLD pneumatic die holder, single- and double-line control units",
        "Fits Z1 (27 mm body, 7 mm axis) and Z2 (40 mm body, 20 mm axis) intermediates — we check yours against EUROSTAMP's drawing first"],
       [acc_table("Clamps", "for European-style intermediates", [(c, d, D.height(h) if h else "—", f"{L / 25.4:.1f}″ ({L} mm)" if L else "—") for c, d, h, L in CLAMPS],
                  ["Clamp", "Height H", "Length"]),
        acc_table("EUROGRIP", "150 mm (5.9″) sections", [(c, d) for c, d in EUROGRIP], ["System part"])],
       images=["es-p-eg-row", "es-p-eg-measy", "es-p-c218", "es-p-eg-pdhold", "es-w-4021", "es-w-4219", "es-w-4009"], tools=[], ndraw=0, glance_tools=[],
       models_label="clamps 4007 – 5013 · EUROGRIP 4381 – 4415", headline="Safety clamps, EUROGRIP manual and pneumatic",
       family_row=[f"{len(CLAMPS) + len(EUROGRIP)} · clamps + EUROGRIP", "—", "H 1.69 – 2.36″ (43 – 60 mm)", "—"])

LOWER = [("4301", "Lower adapter Beyeler / Trumpf beam → European dies", 30), ("4302", "Lower adapter Beyeler / Trumpf beam → European dies", 60),
         ("4303", "Lower adapter European beam → Beyeler / Trumpf dies", 40), ("4304", "Lower adapter European beam → LVD dies", 40),
         ("4305", "Lower adapter Beyeler / Trumpf beam → LVD dies", 30),
         ("9010", "Solid lower die holder, European style, 2,100 mm", None), ("9011", "Solid lower die holder, European style, 2,600 mm", None),
         ("9012", "Solid lower die holder, European style, 3,100 mm", None), ("9013", "Solid lower die holder, European style, 4,100 mm", None),
         ("9020", "Modular lower adapter", None), ("4033", "Filler block H55 with 6 short clamps", 55), ("4050", "Filler block H55 with 2 clamps 800 mm long", 55),
         ("4034", "Short clamp for the rear of the filler block", 50), ("4040", "Long clamp for the front of the filler block", None),
         ("4041", "Long clamp for the rear of the filler block", None), ("4015", "Lower tool clamp", None), ("4014", "Washer for the lower tool clamp", None)]
TANGS = [("8012", "Amada / Promecam tang (standard)"), ("8100", "Beyeler / Trumpf tang 13 × 20 mm"), ("8101", "LVD tang 12 × 19 mm"),
         ("8102", "Weinbrenner tang 35 × 45 mm, 832 / 412 mm"), ("8105", "Weinbrenner tang 35 × 45 mm, 1,000 / 500 mm"),
         ("8107", "American-style tang"), ("8010", "Barretta-style tang"), ("8011", "BMB-style tang"), ("8013", "Gasparini-style tang")]
family("es-acc-lower", P_ACC, "Lower adapters, die holders and tangs", "Lower adapters",
       "Lower adapters fit dies of one style on a lower beam of another: European dies on a Beyeler / Trumpf beam, Beyeler / Trumpf or LVD "
       "dies on a European beam, LVD dies on a Trumpf beam. The solid lower die holders, 2,100 to 4,100 mm (6.9 – 13.5 ft) long, give a "
       "European-style die seat on a press brake that has none; the filler blocks raise a die by 55 mm (2.17″) to match the punch "
       "height. And any EUROSTAMP tool can be made with the tang of your machine — Beyeler / Trumpf, LVD, Weinbrenner, American, "
       "Barretta, BMB or Gasparini — on request.",
       ["Lower adapters between European, Beyeler / Trumpf and LVD styles, H30 to H60, 415 – 1,000 mm long",
        "Solid lower die holders 2,100, 2,600, 3,100 and 4,100 mm; modular lower adapter", "Filler blocks H55 with short or long clamps",
        "Tangs on request for 9 clamping styles"],
       [acc_table("Lower adapters, die holders and filler blocks", "", [(c, d, D.height(h_of(c, h)) if h_of(c, h) else "—", lens(c)) for c, d, h in LOWER],
                  ["Part", "Height H", "Lengths", "Profile"]),
        acc_table("Tangs on request", "made on any EUROSTAMP tool", [(c, d, lens(c)) for c, d in TANGS], ["Tang", "Lengths"])],
       images=["es-p-holders", "es-w-4302", "es-w-4304", "es-w-4040", "es-w-4034", "es-w-8100", "es-w-8107"], tools=[], ndraw=0, glance_tools=[],
       models_label="4014 – 4305 · 9010 – 9020 · tangs 8010 – 8107", headline="Between styles, die holders to 13.5 ft, tangs on request",
       family_row=[f"{len(LOWER) + len(TANGS)} · adapters + tangs", "—", "H 1.18 – 2.36″ (30 – 60 mm)", "—"])

ADJ = [("3190", "V 24 – 124 mm (.94 – 4.88″)", "30°", 125, "1,050 · 1,000 · 550 · 500 · 250", "9015 European · 9018 Trumpf / Beyeler / Wila"),
       ("3191", "V 65 – 180 mm (2.56 – 7.09″)", "60°", 200, "1,050 · 1,000 · 550 · 500 · 250", "9016 European · 9019 Trumpf / Beyeler / Wila"),
       ("3192", "V 120 – 300 mm (4.72 – 11.81″)", "60°", 400, "700 · 600 · 500", "9014"),
       ("3243", "V 150 – 400 mm (5.91 – 15.75″)", "60°", 600, "600", "9017")]
family("es-acc-adjustable", P_ACC, "Adjustable dies, V 24 – 400 mm", "Adjustable dies",
       "For plate and for shops that bend many thicknesses: one adjustable die replaces a rack of 1V dies. Spacer bars set the V opening "
       "between the two halves, and case-hardened rollers on the shoulders let the plate slide in instead of dragging, so it is not "
       "marked and less force is needed. Four sizes from V24 to V400 mm (.94 – 15.75″), rated from 125 to 600 t/m (42 – 202 US t/ft) at "
       "90°; each comes with its spacer set and 5 m of protective film and needs its own lower adapter.",
       ["V 24 – 124, 65 – 180, 120 – 300 and 150 – 400 mm", "Case-hardened rollers on the shoulders; minimum bend angle 30° (3190) or 60°",
        "Rated 125, 200, 400 and 600 t/m (42 / 67 / 134 / 202 US t/ft) at 90°", "Spacer bars and 5 m (16 ft) of protective film included; adapter ordered separately"],
       [acc_table("Adjustable dies", "", [(c, v, a, D.load(f), L + " mm", ad) for c, v, a, f, L, ad in ADJ],
                  ["V range", "Min. angle", "Max. load at 90°", "Lengths", "Lower adapter"])],
       images=["es-w-3191", "es-w-3190", "es-w-3192", "es-w-3243", "es-w-9015"], tools=[], ndraw=0, glance_tools=[],
       models_label="3190 · 3191 · 3192 · 3243", headline="V .94 – 15.75″ (24 – 400 mm), to 202 US t/ft",
       family_row=["4 · adjustable dies", "30° – 60° min.", "V .94 – 15.75″ (24 – 400 mm)", "to 202 US t/ft (600 t/m)"])

URE = [("2036", "Holder for 25 × 25 mm urethane inserts"), ("2037", "Holder for 50 × 50 mm urethane inserts"), ("2038", "Holder for 75 × 50 mm urethane inserts"),
       ("2040", "Holder for 100 × 50 mm urethane inserts"), ("2101", "Urethane insert 25 × 25 mm"), ("2102", "Urethane insert 50 × 50 mm"),
       ("2103", "Urethane insert 75 × 50 mm"), ("2104", "Urethane insert 100 × 50 mm"), ("2105", "Urethane insert 25 × 25 mm with hole"),
       ("2106", "Urethane insert 50 × 50 mm with hole"), ("2107", "Urethane insert 75 × 50 mm with hole"), ("2108", "Urethane insert 100 × 50 mm with hole"),
       ("2119", "Triangular urethane insert 50 × 25 mm with hole"), ("2109", "Holder for 20 × 24 mm nylon inserts, H74"), ("2110", "Holder for 24 × 35 mm nylon inserts, H75"),
       ("2111", "Holder for 31 × 38 mm nylon inserts, H75"), ("2115", "Holder for 24 × 35 mm nylon inserts, H50, Beyeler / Trumpf / Wila"),
       ("2116", "Holder for 24 × 35 mm nylon inserts, H95, Beyeler / Trumpf / Wila"), ("2112", "Nylon insert 20 × 24 mm"), ("2113", "Nylon insert 24 × 35 mm"),
       ("2114", "Nylon insert 31 × 38 mm"), ("4308", "Urethane protective film 0.5 mm × 105 mm × 33 m"), ("4314", "Urethane protective film 0.8 mm × 90 mm × 33 m"),
       ("4379", "Protective cloth for sheet to 3 mm, 5 or 10 m"), ("4380", "Protective cloth for sheet to 6 mm, 5 or 10 m"), ("4309", "Pair of supports for protective film")]
family("es-acc-urethane", P_ACC, "Urethane and nylon dies, protective film", "Urethane & film",
       "For stainless, aluminum, painted and pre-finished sheet that must not be marked: a urethane insert in its holder works as a die "
       "that the punch presses the sheet into — no V, no shoulders, no marks — and nylon inserts replace the steel shoulders of a V. "
       "Where the steel die stays, a urethane film or a protective cloth over the V keeps the shoulders off the part.",
       ["Urethane inserts 25 × 25 to 100 × 50 mm, solid or with a hole, in holders", "Nylon inserts 20 × 24, 24 × 35 and 31 × 38 mm with holders, European and Beyeler / Trumpf / Wila",
        "Urethane film 0.5 and 0.8 mm × 33 m (108 ft); cloth for sheet to 3 or 6 mm", "Inserts and holders in 835 and 415 mm (32.9 / 16.3″) lengths"],
       [acc_table("Urethane and nylon inserts and holders", "", [(c, d, lens(c)) for c, d in URE if c not in LEN_TEXT and c != "4309"], ["Part", "Lengths", "Profile"]),
        roll_table("Protective film and cloth", [(c, d) for c, d in URE if c in LEN_TEXT]),
        acc_table("Film supports", "", [(c, d) for c, d in URE if c == "4309"], ["Part", "Profile"])],
       images=["es-w-4308", "es-p-c255", "es-w-4309", "es-w-4379", "es-w-4380", "es-w-2037", "es-w-2110", "es-w-2119"], tools=[], ndraw=0, glance_tools=[],
       models_label="2036 – 2119 · 4308 – 4380", headline="Urethane and nylon inserts, film and cloth",
       family_row=[f"{len(URE)} · inserts, holders, film", "—", "—", "—"])

SHOP = [("4384", "Digital gauge for 45° chamfers and radii — chamfer 0.01 – 15 mm, radius 0.01 – 25 mm"), ("4883", "Manual protractor"),
        ("4306", "Fixed reference square"), ("4307", "Adjustable reference square"), ("4318", "Magnetic squaring arm, left"),
        ("4319", "Magnetic squaring arm, right"), ("4010", "Front sheet-support arm, 1,000 mm"), ("4011", "Clamp for the front arm"),
        ("4012", "Trip stop with micrometric adjustment"), ("4013", "Trip stop"), ("8211", "Safety buttons"), ("8212", "Safety buttons"),
        ("8213", "Safety buttons"), ("8214", "Safety buttons"), ("8215", "Safety buttons"), ("8216", "Safety buttons"),
        ("8218", "Safety buttons"), ("8219", "Safety buttons"), ("2004", "Shear blades"), ("2005", "Shear blades"),
        ("ACARM0NE0005", "Tooling cabinet for Amada / European tools, 5 drawers"), ("ACARM1NE0005", "Tooling cabinet for Trumpf / Wila / Bystronic / LVD tools, 5 drawers"),
        ("ACARM2NE0005", "Tooling cabinet for Trumpf / Wila / Bystronic / LVD tools, 5 drawers"), ("CARRELLO0005", "Mobile tooling trolley for Amada tools, 5 shelves")]
family("es-acc-shop", P_ACC, "Gauges, squares, safety buttons and tool storage", "Gauges & storage",
       "The small things around the tooling: a digital gauge that reads 45° chamfers and radii on a bent part, a protractor for inside "
       "and outside angles, fixed and adjustable reference squares and magnetic squaring arms for setting up, front support arms with "
       "trip stops, spare safety buttons for Trumpf- and Wila-style tools, shear blades — and cabinets and a trolley that keep a set of "
       "punches and dies in order next to the press brake.",
       ["Digital chamfer and radius gauge: chamfer 0.01 – 15 mm, radius 0.01 – 25 mm", "Manual protractor; fixed and adjustable reference squares; magnetic squaring arms",
        "Front support arm with fixed or micrometric trip stop", "Safety buttons, shear blades",
        "Tooling cabinets with 5 drawers (European or Trumpf / Wila / Bystronic / LVD tools) and a 5-shelf trolley; black as standard, other colours on request"],
       [acc_table("Gauges, accessories and storage", "", [(c, d) for c, d in SHOP], ["Part"])],
       images=["es-w-4384", "es-p-gauge-hand", "es-w-4883", "es-w-4306", "es-w-4307", "es-p-magarm", "es-p-cabinet", "es-p-trolley"], tools=[], ndraw=0, glance_tools=[],
       models_label="gauges, squares, buttons, cabinets", headline="Digital gauge, squares, safety buttons, cabinets",
       family_row=[f"{len(SHOP)} · accessories", "—", "—", "—"])


# ================================================================================================= pages
def fams(page):
    return [f for f in ALL_FAMILIES if f["page"] == page]


def count(page):
    return sum(len(t["rows"]) for f in fams(page) for t in f["tool_tables"])


SUBPAGES = [
    (P_EUP, "European (Amada-Promecam) punches — straight, acute, gooseneck, ESH, radius and offset", "es-p-c077b",
     "Straight, acute, gooseneck and sash punches for the Amada-Promecam clamping used on most press brakes, the ESH same-height series, radius holders R3 – R50 and offset tools.",
     "European punches"),
    (P_EUD, "European (Amada-Promecam) dies — 1V, 2V / 4V, self-centring, T, hemming and ESH insert dies", "es-p-c041",
     "1V dies V18 – V220, multi-V and 3U dies with holders, self-centring dies on rails, slim T dies, mechanical and pneumatic hemming dies and ESH inserts.",
     "European dies"),
    (P_TW, "Trumpf and Wila-style tooling — New Standard punches and dies", "es-p-dies",
     "Trumpf-style punches to 300 mm high and dies V6 – V120; Wila-style punches and 55 / 100 mm dies — with safety buttons on the lighter tools.",
     "Trumpf & Wila"),
    (P_BL, "Bystronic and LVD-style tooling — punches and dies", "es-p-c180",
     "Bystronic / Beyeler type R and RF-A punches, flattening blades and dies; LVD-style punches and dies V6 – V120 rated to 340 t/m.",
     "Bystronic & LVD"),
    (P_AM, "American-style punches and dies — .500″ tang", "es-am-hero",
     "88° and 85° straight and gooseneck punches, 28° – 30° acute punches and 1V dies V .375 – .875″ with the American tang, in 36″, 18″ and sectioned lengths — and a Z1 intermediate that takes them on European-style brakes.",
     "American style"),
    (P_ACC, "Holders, adapters, clamps and accessories", "es-p-holders",
     "Intermediates and adapters between clamping styles, safety clamps and EUROGRIP, lower adapters, adjustable dies V24 – V400, urethane tooling and gauges.",
     "Holders & adapters"),
]


def hub_info():
    return {"slug": HUB, "label": "All press brake tooling", "image": "es-p-range",
            "blurb": "Every EUROSTAMP tooling family NovoTech sells — European, Trumpf, Wila, Bystronic, LVD and American styles, holders and adapters — with a guide to choosing the V opening and the tonnage chart."}


def siblings():
    return [(s, nav, t.split(" — ")[0]) for s, t, _, _, nav in SUBPAGES]


FAQ_COMMON = {"q": "Can we get the tools as DXF files for our CNC?",
              "a": "Yes — every tool in these tables that has a DXF link can be downloaded straight from the page: the profile drawn in millimetres, "
                   "ready to import into the tool library of a Delem, ESA or Cybelec control or into offline bending software. For the "
                   "few tools without one, ask us and we get the drawing from EUROSTAMP."}

PAGES = {
    P_EUP: dict(
        title="European Press Brake Punches, Amada-Style | NovoTech",
        meta="Straight, acute, gooseneck, sash, ESH same-height, radius and offset punches for Amada-Promecam clamping, made in Italy, with DXF profiles to download.",
        h1="European-style (Amada-Promecam) press brake punches — straight, acute, gooseneck, same-height, radius and offset tools",
        intro="EUROSTAMP punches for press brakes with European-style clamping — the Amada-Promecam standard used by Amada and Promecam and "
              "by dozens of other makers, from Accurpress, Baykal and Dener to Durmazlar, Ermaksan, Prima Power, Salvagnini and Yawei. Made "
              "in Italy from C45 and 42CrMo4 steel, induction-hardened to 55 – 60 HRC on the working surfaces, in 835 mm (32.9″) and 415 mm "
              "(16.3″) lengths and 805 mm (31.7″) sectioned sets with horns. Six families on this page: straight punches from 45° to 88° and "
              "heavy-duty punches with R6 – R10 tips for plate; acute 24° to 35° punches; gooseneck and sash punches for return flanges; the "
              "ESH series with one 120 mm working height for staged bending; radius holders with round elements R3 to R50; and offset "
              "(joggle) tools. The punches link to their DXF profiles for your CNC, and NovoTech quotes, ships and supports the tooling from Mississauga, ON, Canada.",
        points=["Straight 45° – 88°, acute 24° – 35°, gooseneck and sash punches 2.56 – 7.87″ (65 – 200 mm) high, rated to 50 US t/ft (150 t/m)",
                "ESH same-height series: every punch 120 mm (4.72″), for staged bending in one setup",
                "Radius holders with round elements R3 – R50 and offset tools Z 1 – 15 mm; DXF profiles to download"],
        hero="es-p-c077b", minis=["es-p-c077a-cut"],
        faq=[{"q": "Will these punches fit my press brake?",
              "a": "If your press brake clamps European-style (Amada-Promecam) tooling, yes. EUROSTAMP lists Amada, Promecam, Accurpress, Adira, "
                   "Baykal, Boschert, Bystronic-Beyeler Euro-B, Colgar, Dener, Durmazlar, Ermaksan, Gasparini, Haco, Prima Power, Salvagnini, "
                   "Yawei and many more as using this style. If you are not sure, send us a photo of the upper clamp and a punch you use now — or "
                   "the model of the brake — and we confirm before you order. Adapters let other press brakes take these punches."},
             {"q": "Straight or gooseneck punch?",
              "a": "A straight punch is stiffer and carries more load, so it is the first choice for open angles and plate. A gooseneck is "
                   "relieved behind the tip: use it when a flange you have already bent comes back towards the punch — U-channels, pans, boxes "
                   "with return flanges. The deeper the neck, the lower the load rating, so check the table before you bend thick plate on a "
                   "gooseneck."},
             {"q": "What tip radius should I choose?",
              "a": "In air bending the inside radius is set mostly by the V opening — about 1/6 of the V in mild steel — not by the punch. "
                   "Choose a punch radius at or below that natural radius: R0.6 to R0.8 for sheet up to about 10 gauge, R1.5 to R3 for 3/16 to "
                   "1/4″, and the heavy-duty R6 – R10 punches for plate thicker than about 3/8″, where a sharp tip would crack the outside of "
                   "the bend. A sharp R0.25 punch gives crisp corners in thin stainless and aluminum."},
             {"q": "What are horns and sectioned sets?",
              "a": "A sectioned set is a punch or die cut into pieces that add up to a standard length — for European-style punches 805 mm "
                   "(31.7″) made of 100 mm horns at each end and 10, 15, 20, 40, 50, 200 and 270 mm pieces. You assemble the exact length of a "
                   "bend, and the horns — the ends relieved on the outside — let you bend the sides of a box without hitting the flanges "
                   "already formed."},
             {"q": "What is the ESH series?",
              "a": "ESH stands for EUROSTAMP Same Height: every punch in the series — straight, gooseneck, sash, 86°, 60°, 30° and 26° — has "
                   "the same 120 mm working height, and the matching insert dies the same 60 mm. Several tools can be set up side by side in "
                   "stations and used without re-setting the ram, which saves set-up time on parts with several different bends."},
             FAQ_COMMON],
        faq_title="Questions we get asked about European-style punches",
        related=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "dener-cnc-press-brakes.html", "label": "Dener CNC press brakes"},
                 {"href": "panel-bender.html", "label": "Panel benders"}],
    ),
    P_EUD: dict(
        title="European Press Brake Dies, Amada-Style | NovoTech",
        meta="1V, 2V, 4V, self-centring, T, hemming and ESH insert dies for Amada-Promecam clamping, V 4 – 220 mm, made in Italy, with DXF profiles to download.",
        h1="European-style (Amada-Promecam) press brake dies — 1V, multi-V, self-centring, T, hemming and ESH insert dies",
        intro="EUROSTAMP dies for the European-style (Amada-Promecam) lower beam found on most press brakes sold in Canada. Six families: "
              "solid 1V dies from V18 to V220 mm (.71 – 8.66″) for sheet and plate; 2V, 4V and 3U dies that hold several openings in one "
              "block, with their holders; slim self-centring 1V dies on rails; T dies — a slim body on a 60 mm foot — for return flanges "
              "and closed profiles; mechanical and pneumatic hemming dies that pre-bend and close a hem with one punch; and the ESH insert "
              "dies, nitrided all over to 65 HRC. C45 and 42CrMo4 steel, induction-hardened on the V and shoulders, in 835 and 415 mm "
              "lengths and 805 mm sectioned sets — with DXF profiles for your CNC.",
        points=["1V dies V18 – V220 mm (.71 – 8.66″), rated to 67 US t/ft (200 t/m); 2V, 4V and 3U dies with holders",
                "Self-centring 1V dies, T dies 80 and 120 mm high, hemming dies — mechanical and pneumatic",
                "ESH insert dies nitrided to 65 HRC; 835 / 415 mm lengths and 805 mm sectioned sets; DXF profiles"],
        hero="es-p-c041", minis=["es-p-c067b"],
        faq=[{"q": "How do I choose the V opening?",
              "a": "For mild steel up to about 1/2″, start with a V of 8 times the thickness: V16 (5/8″) for 14 gauge, V24 for 1/8″, V50 for "
                   "1/4″. Thicker plate needs 10 to 12 times; aluminum can go to 6 times, stainless wants 8 to 10. A wider V needs less force and "
                   "gives a larger inside radius (about 1/6 of the V) but a longer minimum flange (about 0.7 × V). The tonnage chart and the "
                   "guide on the press brake tooling overview page work through it."},
             {"q": "1V or 4V die?",
              "a": "A 1V die gives the best support and the highest load rating for one thickness, and the solid 60 mm block is the most "
                   "rigid. A 4V die puts four openings on one 60 mm block — turn it to change the V — so one die covers a range of gauges, "
                   "which suits job shops that change thickness several times a day. The 2V dies do the same with two openings."},
             {"q": "What is the difference between a T die and a self-centring die?",
              "a": "Both are slim. A T die stands on a 60 mm (2.36″) foot and clamps in the lower beam like any European die; its narrow body "
                   "leaves room for return flanges. A self-centring die is 14 mm wide and sits on a rail (2058 or 2059) that lines it up under "
                   "the punch, so changing V openings is quick and needs no alignment."},
             {"q": "How does a hemming die work?",
              "a": "In the first stroke the acute V on top of the die pre-bends the flange to about 30° with an acute or hemming punch; in the "
                   "second stroke the punch closes on the spring-loaded upper plate and flattens the hem. One die and one punch do both steps "
                   "without a tool change. The pneumatic (PN) versions open and close on shop air."},
             FAQ_COMMON],
        faq_title="Questions we get asked about European-style dies",
        related=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "novotech-cnc-press-brakes.html", "label": "NovoTech CNC press brakes · value line"}],
    ),
    P_TW: dict(
        title="Trumpf & Wila-Style Press Brake Tooling | NovoTech",
        meta="Trumpf-style punches to 300 mm and dies V6 – V120, Wila-style (New Standard) punches and dies — safety buttons, made in Italy, DXF profiles.",
        h1="Trumpf and Wila-style (New Standard) press brake tooling — punches and dies",
        intro="EUROSTAMP tooling for press brakes with Trumpf and Wila (New Standard) clamping — Trumpf, Darley, Safan, RPC and the other "
              "makers that use this hydraulic clamping. Trumpf-style punches stand 140 to 300 mm (5.51 – 11.81″) tall for deep boxes, with "
              "dies from V6 to V120 in 100, 120 and 150 mm heights; Wila-style punches run from 135 to 237 mm and the dies are 55 or 100 mm "
              "high. Tools up to 13.5 kg (Trumpf style) and 12.5 kg (Wila style) come with safety buttons that stop a released tool from "
              "falling, so they load from the front. 42CrMo4 and C45 steel, induction-hardened, with a DXF profile of every tool.",
        points=["Trumpf-style punches 5.51 – 11.81″ (140 – 300 mm) high, rated to 84 US t/ft (250 t/m); dies V .24 – 4.72″",
                "Wila-style punches 5.31 – 9.33″ (135 – 237 mm); dies 55 and 100 mm (2.17 / 3.94″) high",
                "Safety buttons standard on the lighter tools; 500 / 515 mm lengths and 550 mm sectioned sets"],
        hero="es-p-dies", minis=[],
        faq=[{"q": "Are Trumpf-style and Wila-style tools interchangeable?",
              "a": "They share the New Standard clamping idea — a vertical tang with safety buttons that the hydraulic clamp pulls up and "
                   "seats — and EUROSTAMP lists Trumpf, Darley and Safan brakes for both. Check the tang and the heights of the tools you already "
                   "run before mixing them, and send us the clamp model if you are unsure; we confirm before you order."},
             {"q": "What do the safety buttons do?",
              "a": "The spring-loaded buttons in the tang catch the tool in the clamp while it is released, so it can be loaded and removed "
                   "from the front without falling. EUROSTAMP fits them as standard on Trumpf-style tools up to 13.5 kg (30 lb) and Wila-style "
                   "tools up to 12.5 kg (27.5 lb); heavier tools are loaded from the side."},
             {"q": "Which height should I order?",
              "a": "Match the height of the tools already in the machine so the punch tips and die shoulders stay on the same line — mixing "
                   "heights means re-setting the ram. Use the tall 220 – 300 mm punches only where the part needs the depth, as the load rating "
                   "falls with height."},
             FAQ_COMMON],
        faq_title="Questions we get asked about Trumpf and Wila-style tooling",
        related=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "panel-bender.html", "label": "Panel benders"}],
    ),
    P_BL: dict(
        title="Bystronic & LVD-Style Press Brake Tooling | NovoTech",
        meta="Bystronic / Beyeler type R and RF-A punches, flattening blades and dies; LVD-style punches and dies V6 – V120 to 340 t/m — made in Italy, DXF profiles.",
        h1="Bystronic and LVD-style press brake tooling — punches and dies",
        intro="EUROSTAMP tooling for two clamping systems with their own tangs. Bystronic and Beyeler press brakes with type R, RF and RF-A "
              "clamping take the punches here — straight and acute, gooseneck, sash and 24° flattening blades, 155 to 250 mm (6.10 – 9.84″) "
              "high — and the 55 – 65 mm dies from V6 to V60. LVD press brakes take the LVD-style punches 196 mm high and dies 90 or 130 mm "
              "high from V6 to V120, rated up to 340 t/m (114 US t/ft). Tell us the clamping of your brake and we confirm the tang; the DXF "
              "profiles are on the page.",
        points=["Bystronic type R and RF-A punches 6.10 – 9.84″ (155 – 250 mm), flattening blades, dies V .24 – 2.36″",
                "LVD-style punches 7.72″ (196 mm) and dies V .24 – 4.72″, 90 and 130 mm high, rated to 114 US t/ft",
                "500 / 1,000 mm and 510 mm lengths, sectioned sets for Bystronic; DXF profiles"],
        hero="es-p-c180", minis=[],
        faq=[{"q": "Type R or RF-A — which do I need?",
              "a": "They are two Bystronic / Beyeler clamping systems with different tangs and punch heights — type R punches here are 155 mm "
                   "high, RF-A punches 175 mm, and the 250 mm punches fit both. Look at the clamp or at the marking on a punch you already use, "
                   "or send us a photo, and we match it."},
             {"q": "Can I use European-style tooling on my Bystronic or LVD brake?",
              "a": "Yes, with adapters: the upper adapters 4192 (type R), 4193 (type S) and 4214 (RF-A) take European-style punches on a "
                   "Beyeler ram, 4143 – 4146 on an LVD ram, and the lower adapters 4301, 4302 and 4304 / 4305 do the same for dies. They are "
                   "on the holders and adapters page."},
             FAQ_COMMON],
        faq_title="Questions we get asked about Bystronic and LVD-style tooling",
        related=[{"href": "press-brake.html", "label": "Press brakes"}],
    ),
    P_AM: dict(
        title="American-Style Press Brake Punches & Dies | NovoTech",
        meta="American-style punches and dies with the .500″ tang — 88° straight and gooseneck, 28° – 30° acute punches, 1V dies V .375 – .875″, 36″ and 18″.",
        h1="American-style press brake tooling — punches and dies with the .500″ tang",
        intro="EUROSTAMP punches and dies with the American tang — .500″ (12.7 mm) wide with the safety lip — for the American-style "
              "clamping found on most press brakes built in North America. Punches stand 3.779″ (96 mm) high: 88° straight and 88° / 85° "
              "gooseneck punches for 90° air bending, 30° and 28° acute punches for hemming and acute angles, and a 5.125″ acute gooseneck. "
              "The dies all share a 1.937″ (49.2 mm) working height: 88° dies V .375 to .750″ and 30° – 34° acute dies V .375 to .875″. "
              "Every tool comes in 36″ and 18″ lengths and a 35.75″ sectioned set, each with its own part number. For press brakes "
              "with European-style (Amada-Promecam) clamping there is a Z1 intermediate that takes these punches.",
        points=["Punches 88°, 85°, 30° and 28°, 3.779″ (96 mm) high — tang .500″ with safety lip",
                "1V dies V .375 – .875″ (9.53 – 22.23 mm), 88°, 34° and 30°; working height 1.937″ (49.2 mm)",
                "36″ (914.4 mm), 18″ (457.2 mm) and 35.75″ (908 mm) sectioned lengths",
                "Z1 intermediate for American-style punches on European-style (Amada-Promecam) press brakes"],
        hero="es-am-hero", minis=[],
        faq=[{"q": "Will American-style tooling fit my press brake?",
              "a": "It fits press brakes with American-style clamping — a .500″ tang in a clamp bar, used on most press brakes built in North "
                   "America. Measure the tang slot of your upper clamp and lower die holder, or send us a photo of a tool you use now, and we "
                   "confirm. If your brake has European-style clamping, see the European punches and dies pages — or, to use "
                   "American-style punches on it, the Z1 intermediate on this page, for brakes built for Z1 intermediates."},
             {"q": "Why do the drawings say the dimensions are in inches?",
              "a": "American-style tooling is designed in inches. The tables give each dimension in decimal inches with the exact metric value, "
                   "and the part numbers carry the length in millimetres: 0914 for 36″, 0457 for 18″ and 0908 for the 35.75″ sectioned set."}],
        faq_title="Questions we get asked about American-style tooling",
        related=[{"href": "press-brake.html", "label": "Press brakes"}],
    ),
    P_ACC: dict(
        title="Press Brake Tool Holders, Adapters & Clamps | NovoTech",
        meta="Intermediates, adapters between clamping styles, safety clamps and EUROGRIP, lower die holders, adjustable dies V24 – V400, urethane tooling and gauges.",
        h1="Press brake tool holders, adapters, clamps and accessories",
        intro="Everything around the punches and dies: European-style intermediates (Z1 and Z2, adjustable or fixed, heavy-duty CrMo) and "
              "upper adapters that let one press brake run another style's tools; safety clamps and EUROSTAMP's own EUROGRIP clamping, "
              "manual and pneumatic; lower adapters, solid die holders to 4,100 mm and tangs made to your machine; adjustable dies from V24 to "
              "V400 mm for plate; urethane and nylon tooling, film and cloth for parts that must not be marked; and gauges, squares, safety "
              "buttons and tooling cabinets. Made in Italy by EUROSTAMP, quoted and shipped by NovoTech.",
        points=["Intermediates Z1 / Z2 and upper adapters between 12 clamping systems; heavy-duty versions to 54 US t/ft",
                "EUROGRIP manual and pneumatic clamping; safety clamps; lower adapters and die holders to 13.5 ft",
                "Adjustable dies V .94 – 15.75″ to 202 US t/ft; urethane tooling, film, gauges and cabinets"],
        hero="es-p-holders", minis=[],
        faq=[{"q": "What is an intermediate and why adjustable?",
              "a": "The intermediate is the block between the ram and a European-style punch that holds the clamp. The adjustable versions "
                   "have a wedge that lets you set each section a few hundredths of a millimetre lower — manual crowning — so the angle stays "
                   "the same along a long bend on a brake without automatic crowning. Z1 (27 mm body, axis 7 mm) and Z2 (40 mm body, axis 20 mm) "
                   "differ in size: match the ones on your machine."},
             {"q": "Can one press brake use tooling of another style?",
              "a": "Yes, through adapters: upper adapters take European-style punches on Trumpf / Wila, Beyeler, LVD, Weinbrenner, CBC, EHT, "
                   "Durmazlar, Darley, Baykal and Colgar rams, and 4362 takes Trumpf / Wila punches on a European ram; lower adapters do the same "
                   "for dies. An adapter adds height and costs some load capacity — check both before you buy."},
             {"q": "When is an adjustable die worth it?",
              "a": "When you bend plate in many thicknesses: one 3191 covers V65 to V180 mm — the job of eight or ten solid dies — and the "
                   "rollers on the shoulders reduce marking and force. For thin sheet and repeat work, solid 1V dies remain cheaper and more "
                   "precise."}],
        faq_title="Questions we get asked about holders, adapters and clamps",
        related=[{"href": "press-brake.html", "label": "Press brakes"}],
    ),
}

HUB_PAGE = dict(
    title="Press Brake Tooling Canada — Punches & Dies | NovoTech",
    meta="EUROSTAMP punches, dies, holders and adapters made in Italy, for Amada-Promecam, Trumpf, Wila, Bystronic, LVD and American-style press brakes.",
    h1="Press brake tooling — EUROSTAMP punches, dies and adapters for every clamping style, made in Italy",
    intro="NovoTech sells and supports EUROSTAMP press brake tooling in Canada: punches, dies, holders, adapters and clamping made in "
          "Italy by a company that has built nothing but press brake tooling since 1970. Six pages cover the range — European-style "
          "(Amada-Promecam) punches and dies for most press brakes in Canadian shops, Trumpf and Wila-style tooling, Bystronic and LVD-style "
          "tooling, American-style tooling with the .500″ tang, and the holders, adapters and accessories that let one press brake run "
          "another style's tools. Every table gives the angle, height, tip radius or V opening and load rating of each tool in inches and "
          "millimetres, with DXF profiles to load into your CNC. Below the range: how to choose a V opening and the tonnage chart for air "
          "bending.",
    points=["Over 700 punches, dies, holders and accessories, in full lengths and sectioned sets — European, Trumpf, Wila, Bystronic, LVD and American styles",
            "C45 and 42CrMo4 steel, induction-hardened 55 – 60 HRC up to 3 mm (.118″) deep; special tools to your drawing",
            "DXF profiles to download; adapters between clamping styles; quoted and shipped from Mississauga, ON, Canada"],
    hero="es-p-range", minis=["es-p-group", "es-p-dies"],
    range_cols=["Profiles", "Angles", "Height H", "Max. load"],
    range_lead="Every tooling family on one table: the number of profiles, the angles, the working heights and the highest load rating. Each row links to the family's tool table, with the full data and the DXF profiles.",
    range_caption="EUROSTAMP press brake tooling supplied by NovoTech — families by clamping style",
    range_note="Loads are the maker's maximum in tonnes per metre of tool length, shown as US tons per foot (1 t/m = 0.336 US t/ft). Heights are the working height H.",
    faq=[{"q": "Which tooling fits my press brake?",
          "a": "It depends on the clamping, not the brand of the machine. Most press brakes in Canadian shops — Amada, Accurpress, Baykal, "
               "Dener, Durmazlar, Ermaksan, Yawei and many more — clamp European-style (Amada-Promecam) tools. Trumpf, Darley and Safan use "
               "Trumpf or Wila (New Standard) clamping; Bystronic and Beyeler use type R, RF or RF-A; LVD has its own; and many older North "
               "American brakes take American-style tools with a .500″ tang. Send us the model of your brake or a photo of the clamp and a "
               "tool, and we confirm before you order."},
         {"q": "How do I choose the V opening?",
          "a": "Start with V = 8 × the sheet thickness for mild steel up to about 1/2″ — V24 (about 1″) for 1/8″, V50 (2″) for 1/4″ — and "
               "10 to 12 × for heavier plate. Aluminum works with 6 ×, stainless with 8 – 10 ×. The inside radius comes out at about 1/6 of "
               "the V and the shortest flange you can bend at about 0.7 × V. The guide and the tonnage chart below work through it."},
         {"q": "How much tonnage does a bend need?",
          "a": "For 90° air bending of mild steel, tons per foot ≈ 575 × t² ÷ V, with the thickness t and the V opening in inches: 1/4″ "
               "in a 2″ V needs about 18 US tons per foot of bend, so a 10 ft bend needs about 180 tons. Stainless needs about 1.5 times as "
               "much, soft aluminum about half. The tooling must be rated above the tonnage per foot, and the press brake above the total."},
         {"q": "What do the load ratings in the tables mean?",
          "a": "The maximum force the tool takes per unit of length — EUROSTAMP gives it in tonnes per metre, we add US tons per foot. If a "
               "bend needs 15 tons per foot, use a punch and a die rated above 15 US t/ft (45 t/m). Concentrated loads on a short piece of "
               "tool are the usual way tools crack: a 1 ft part bent with 30 tons puts 30 tons per foot on the tool."},
         {"q": "Do you make special tools?",
          "a": "Yes. EUROSTAMP's technical department designs special punches and dies — profiles, radii, offsets, combined tools — for "
               "parts standard tooling cannot bend. Send us the part drawing and the press brake model, and we come back with a proposal "
               "and a price."},
         {"q": "What steel is the tooling made of?",
          "a": "C45 medium-carbon steel, raw or tempered, and Italian 42CrMo4 chrome-molybdenum steel for the heavier and slimmer tools. "
               "The working surfaces are induction-hardened to 55 – 60 HRC up to 3 mm (.118″) deep, so the tip and shoulders resist wear "
               "while the body stays tough. The ESH insert dies are nitrided all over to 65 HRC."},
         FAQ_COMMON],
    faq_title="Questions we get asked about press brake tooling",
)


# ================================================================================================= the guide (hub)
GAUGES = [("20 ga", 0.036), ("18 ga", 0.048), ("16 ga", 0.060), ("14 ga", 0.075), ("12 ga", 0.105), ("11 ga", 0.120), ("10 ga", 0.135),
          ("3/16″", 0.1875), ("1/4″", 0.25), ("5/16″", 0.3125), ("3/8″", 0.375), ("1/2″", 0.5), ("5/8″", 0.625), ("3/4″", 0.75), ("1″", 1.0)]
VS = [("1/4″", 0.25), ("3/8″", 0.375), ("1/2″", 0.5), ("5/8″", 0.625), ("3/4″", 0.75), ("1″", 1.0), ("1-1/4″", 1.25), ("1-1/2″", 1.5), ("2″", 2.0),
      ("2-1/2″", 2.5), ("3″", 3.0), ("4″", 4.0), ("5″", 5.0), ("6″", 6.0), ("8″", 8.0)]


def tonnage_chart_html():
    head = "".join(f"<th scope=\"col\">{n}<small>{v * 25.4:.0f} mm</small></th>" for n, v in VS)
    rows = []
    for name, t in GAUGES:
        cells = []
        for _, v in VS:
            r = v / t
            if 5.5 <= r <= 12.5:
                val = 575 * t * t / v
                rec = abs(r - 8) == min(abs(vv / t - 8) for _, vv in VS)
                cells.append(f"<td{' class=\"rec\"' if rec else ''}>{val:.1f}</td>")
            else:
                cells.append("<td></td>")
        dec = f"{t:.3f}"
        dec = dec[1:] if dec.startswith("0.") else dec
        rows.append(f"<tr><th scope=\"row\">{name}<small>{dec}″ · {t * 25.4:.1f} mm</small></th>{''.join(cells)}</tr>")
    return ("<div class=\"table-scroll\" tabindex=\"0\" aria-label=\"Air bending tonnage chart\"><table class=\"spec-table guide-table tonnage-table\">"
            "<caption>Air bending at 90°, mild steel (60,000 psi): US tons per foot of bend <small>bold: the V nearest 8 × thickness</small></caption>"
            f"<thead><tr><th scope=\"col\" class=\"label-col\">Thickness \\ V</th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>")


def guide_html():
    return f"""<section class="guide-section" id="tooling-styles">
<h3>Which tooling style fits my press brake?</h3>
<p>Press brake tooling is made to the clamping of the press brake, not to its brand. Five systems cover almost every machine in Canadian shops:</p>
<ul>
<li><strong>European (Amada-Promecam)</strong> — the most common: Amada, Promecam, Accurpress, Baykal, Dener, Durmazlar, Ermaksan, Prima Power, Salvagnini, Yawei and many more. Punches hang in intermediates with clamps; dies sit in a 60 mm lower seat. See <a href="{P_EUP}.html">European punches</a> and <a href="{P_EUD}.html">European dies</a>.</li>
<li><strong>Trumpf and Wila (New Standard)</strong> — hydraulic clamping that pulls a vertical tang up and seats it; Trumpf, Darley, Safan, RPC. See <a href="{P_TW}.html">Trumpf and Wila-style tooling</a>.</li>
<li><strong>Bystronic / Beyeler</strong> type R, RF and RF-A, and <strong>LVD</strong>, each with its own tang. See <a href="{P_BL}.html">Bystronic and LVD-style tooling</a>.</li>
<li><strong>American style</strong> — a .500″ tang in a clamp bar, on most older North American brakes. See <a href="{P_AM}.html">American-style tooling</a>.</li>
</ul>
<p>Adapters let one system run another's tools — European punches on a Trumpf, Beyeler or LVD ram, Trumpf / Wila punches on a European ram — at the cost of some height and load capacity. They are on the <a href="{P_ACC}.html">holders and adapters</a> page.</p>
</section>
<section class="guide-section" id="choosing-the-v-opening">
<h3>Choosing the V opening — the 8 × thickness rule</h3>
<p>In air bending the punch pushes the sheet into the V without bottoming, and the V opening decides almost everything: the force, the inside radius and the shortest flange you can bend.</p>
<ul>
<li><strong>V opening</strong>: about 8 × the thickness for mild steel up to 1/2″; 10 – 12 × for heavier plate; 6 × for soft aluminum; 8 – 10 × for stainless.</li>
<li><strong>Inside radius</strong>: about 1/6 of the V (0.16 × V) in mild steel — a 1″ V gives roughly a 5/32″ radius. Choose a punch tip at or below this radius.</li>
<li><strong>Minimum flange</strong>: about 0.7 × V, measured to the outside of the bend — shorter flanges fall into the V.</li>
<li><strong>Force</strong>: halving the V doubles the force; doubling the thickness quadruples it.</li>
</ul>
</section>
<section class="guide-section" id="tonnage-chart">
<h3>Tonnage chart for air bending</h3>
<p>The force for a 90° air bend in mild steel is about <strong>575 × t² ÷ V</strong> US tons per foot of bend, with the thickness t and the V opening in inches. Multiply by the bend length in feet for the press brake, and compare the tons per foot with the load rating of the punch and the die. Stainless needs about 1.5 times the force, soft aluminum about half, hard aluminum alloys about the same as mild steel; bottoming and coining need three to five times more.</p>
{tonnage_chart_html()}
<p>Example: 3/16″ mild steel in a 1-1/2″ V needs 13.5 tons per foot; a 6 ft bend needs about 81 tons, and a punch and die rated above 13.5 US t/ft (40 t/m).</p>
</section>
<section class="guide-section" id="punch-shapes">
<h3>Punch shapes: straight, gooseneck, acute, sash</h3>
<p>A <strong>straight punch</strong> is the stiffest and carries the most load — the first choice for open angles and plate. A <strong>gooseneck</strong> is relieved behind the tip so a returned flange clears it: U-channels, pans, boxes. <strong>Acute</strong> punches (26° – 35°) bend past 90° for hems and springback; <strong>sash</strong> punches have a slim nose for tight returns. Large-radius bends use a radius holder with a round element, and Z-bends an offset tool.</p>
</section>
<section class="guide-section" id="sectioned-tooling">
<h3>Sectioned (segmented) tooling and horns</h3>
<p>Sectioned — or segmented — sets are cut into pieces — 10 to 270 mm on European-style punches — that add up to a standard length, so you assemble exactly the length of the bend and leave gaps for flanges already formed. Horns are end pieces relieved on the outside: put one at each end of the punch to bend the fourth side of a box. Full lengths (835 mm on European style, 500 – 515 mm on Trumpf, Wila and Bystronic) are stiffer and quicker to set for long, straight bends.</p>
<figure class="guide-figure" data-img="es-std-eu-punch" data-alt="European-style punches: 835 and 415 mm full lengths and the 805 mm sectioned set — 100 mm horns at both ends with 10 to 270 mm pieces between"></figure>
</section>
<section class="guide-section" id="steel-and-hardness">
<h3>Steel, hardness and load ratings</h3>
<p>EUROSTAMP makes its tools from C45 medium-carbon steel and Italian 42CrMo4 chrome-molybdenum steel, and induction-hardens the working surfaces to 55 – 60 HRC up to 3 mm (.118″) deep: the tip and the shoulders resist wear while the core stays tough enough not to crack. Every tool has a load rating per metre of length — never exceed it, and remember that a short part concentrates the whole press force on a short piece of tool.</p>
<p>On request EUROSTAMP adds a surface treatment: <strong>nitriding</strong> hardens the surface further against wear, fatigue and notches; <strong>phosphating</strong> protects against corrosion; or both together.</p>
<figure class="guide-figure" data-img="es-p-treat"></figure>
</section>
<section class="guide-section" id="dxf-profiles">
<h3>Loading the tools into your CNC</h3>
<p>Every tool with a DXF link in the tables can be downloaded as its profile, drawn in millimetres, and imported into the tool library of the press brake control (Delem, ESA, Cybelec) or into offline bending software, so the control can check collisions and calculate the bend. On an ESA 630 the profile can also be drawn on the control — NovoTech's tutorial video shows how.</p>
</section>"""


# ================================================================================================= write everything
def check_lengths():
    for slug, p in list(PAGES.items()) + [(HUB, HUB_PAGE)]:
        assert len(p["title"]) <= 60, (slug, len(p["title"]))
        assert len(p["meta"]) <= 160, (slug, len(p["meta"]))
        assert p["title"].endswith("| NovoTech")
        assert "EUROSTAMP" not in p["title"].upper()


def copy_files():
    """the DXF profiles (R12) under files/dxf and the EUROSTAMP catalogue at the old site's PDF URL"""
    dst = os.path.join(ROOT, "src", D.DXF_DIR)
    os.makedirs(dst, exist_ok=True)
    used = {c["href"].rsplit("/", 1)[1] for f in ALL_FAMILIES for t in f["tool_tables"] for r in t["rows"] for c in r
            if isinstance(c, dict) and "href" in c}
    for fn in used:
        src = os.path.join(D.ES, "dxf12", fn)
        out = os.path.join(dst, fn)
        if not os.path.exists(out) or os.path.getsize(out) != os.path.getsize(src):
            shutil.copy(src, out)
    for fn in os.listdir(dst):
        if fn not in used:
            os.remove(os.path.join(dst, fn))
    cat = os.path.join(ROOT, "src", CAT_FILE)
    if not os.path.exists(cat):
        raise SystemExit(f"{CAT_FILE} is missing: python3 tools/brochure/eurostamp_edition.py")
    CATALOGUE["size"] = CATALOGUE["size"].format(mb=round(os.path.getsize(cat) / 1e6))
    return len(used)


def register_images():
    import eurostamp_photos as PH
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    heroes = {"es-p-range", "es-p-c041", "es-p-dies", "es-p-c077b", "es-p-c180", "es-p-holders"}      # page heroes under 1,200 px
    for key, alt, src in PH.exports(DRAWINGS, tool_alt):
        imap[key] = {"src": os.path.relpath(src, ROOT), "alt": alt, "section": "tooling", "trim": src.endswith(".webp"), "quality": 82,
                     "cutout": False, **({"upscale": 1.5} if key in heroes else {}),
                     # the drawings are cropped to 800 px already: trimmed further they would lose their 800 px variant
                     **({"trim_white": False} if src.endswith(".png") else {})}
        keys.append(key)
    for k in [k for k in imap if (k.startswith("es-") and imap[k].get("section") == "tooling" and k not in PH.PHOTOS and k not in DRAWINGS)]:
        del imap[k]                                    # pictures no longer used (a drawing that left a family's spread)
    imap["eurostamp-logo"] = {"src": "tools/src-images/eurostamp-logo.png", "alt": "EUROSTAMP Tooling", "section": "site", "trim": True, "quality": 90, "cutout": False}
    keys.append("eurostamp-logo")
    for v in ("RTLFMt-ryOc", "o5b-y1RibRM", "Oo5LJWY2o-g"):
        keys.append("video-" + v)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "eurostamp_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    check_lengths()
    n_dxf = copy_files()                               # first: it also reads the catalogue's size for the download button
    write_families(SET, ALL_FAMILIES)
    common = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, "catalogue_pdf": CATALOGUE, **INTRO_VIDEO,
              "why_title": "Every EUROSTAMP tool from NovoTech", "why_features": WHY, "why_note": "", "quote": QUOTE,
              "youtube_playlist": "https://www.youtube.com/@NovoTechMachineTools/videos"}
    for slug, p in PAGES.items():
        fs = fams(slug)
        ndx = sum(1 for f in fs for t in f["tool_tables"] for r in t["rows"] if any(isinstance(c, dict) and "href" in c for c in r))
        lead = (f"{count(slug)} tools in {len(fs)} families, {ndx} of them with a DXF profile to download." if ndx else
                f"{count(slug)} tools in {len(fs)} families, with EUROSTAMP part numbers and profile drawings.")
        groups = [(slug, p["h1"].split(" — ")[0], lead, BRAND)]
        page = dict(p, groups=groups, related_pages=p.get("related", []), related_title="More from NovoTech")
        nav = next(n for s, _, _, _, n in SUBPAGES if s == slug)
        extra = dict(common, nav_label=nav,
                     breadcrumb=CRUMBS + [{"label": SECTION, "href": f"{HUB}.html"}, {"label": p["h1"].split(" — ")[0]}])
        if slug == P_AM:
            extra["catalogue_pdf"] = None
        write_category(slug, page, fs, SET, SECTION, hub=hub_info(), siblings=siblings(), extra=extra)
    hub_fams = [f for f in ALL_FAMILIES]
    h = dict(HUB_PAGE, nav_label="All press brake tooling", related_blurb=hub_info()["blurb"])
    write_hub(HUB, h, hub_fams, SET, SECTION, SUBPAGES, extra=dict(common, range_first_col="Tool family", range_second_col="Page",
                                                                     family_noun="tool", subpage_link="tool tables and drawings",
                                                                     article="press-brake-tooling-guide.html", article_title="Choosing press brake tooling",
                                                                     article_intro="The clamping styles, the V opening and the tonnage a bend needs — and how to load the tools into your CNC.",
                                                                     article_id="tooling-guide"))
    open(os.path.join(ROOT, "content", "articles", "press-brake-tooling-guide.html"), "w", encoding="utf-8").write(guide_html())
    keys = register_images()
    print(f"tooling: {len(ALL_FAMILIES)} families on {len(PAGES)} pages + hub · {sum(count(s) for s in PAGES)} table rows · "
          f"{n_dxf} DXF files · {len(keys)} images")


if __name__ == "__main__":
    build()
