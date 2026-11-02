#!/usr/bin/env python3
"""NovoTech editions of Dener's machine-tool catalogues (Turkish, R-2404-TR) — every page, picture and figure, translated into
English, in NovoTech's catalogue format, with the units in imperial (metric in brackets).  The owner, Nov 1 2026: "change nothing,
delete nothing, only the units become imperial — every PDF converted to the NovoTech format is converted completely".

    python3 tools/brochure/dener_mt_editions.py [lathe] [--html]

  lathe  TTC-TTH CNC Torna Tezgahı (R-2404-TR)            → src/files/NovoTech-Dener-CNC-Lathes-2026.pdf
  mc     CNC Dikey İşleme Merkezi (TMC) and Çift Kolonlu İşleme Merkezi (TDC), R-2404-TR
                                                            → src/files/NovoTech-Dener-Machining-Centres-2026.pdf

Drawings, working ranges, tool interference and the power / torque charts are the catalogue's own, dimensioned in millimetres
(a note on each page gives the conversion).  Left out, and why: Dener's addresses, phone numbers and QR code (NovoTech's contact
details are on every page) and the catalogue's "free installation and training in Turkey" (Dener's terms at home; NovoTech's
installation and training are in the included-with-every-machine box).

Images: tools/src-images/dener-brochure/lathe/ (rasters of the catalogue and renders of its drawing pages).  Helpers and layout:
tools/brochure/dener_laser_editions.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dener_laser_editions as D   # noqa: E402
from dener_laser_editions import Book, title, P, checks, h2, h3, fig, row, grid, im, included, stats, ORANGE, OR2, CHAR  # noqa: E402

ROOT = D.ROOT


# ----------------------------------------------------------------------------------------------------------------- units
def num(v, nd=1):
    s = f"{v:,.{nd}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def two(main, metric):
    return f"{main} <small>({metric})</small>"


def mm(v, nd=1):
    return two(f"{num(v / 25.4, nd)}″", f"{v:,} mm" if isinstance(v, int) else f"{num(v, 3)} mm")


def mm_pair(a, b, nd=1):
    return two(f"{num(a / 25.4, nd)} / {num(b / 25.4, nd)}″", f"{num(a, 3)} / {num(b, 3)} mm")


def kw(v):
    return two(f"{num(v * 1.341)} HP", f"{num(v)} kW")


def kw_pair(a, b):
    return two(f"{num(a * 1.341)} / {num(b * 1.341)} HP", f"{num(a)} / {num(b)} kW")


def nm(v):
    return two(f"{num(v * 0.7376)} lbf·ft", f"{num(v)} N·m")


def nm_pair(a, b):
    return two(f"{num(a * 0.7376)} / {num(b * 0.7376)} lbf·ft", f"{num(a)} / {num(b)} N·m")


def mmin(v):
    return two(f"{num(v * 3.281, 0)} ft/min", f"{num(v)} m/min")


def mmin_range(a, b):
    return two(f"{num(a * 3.281)} – {num(b * 3.281)} ft/min", f"{a} – {b} m/min")


def litre(v):
    return two(f"{num(v / 3.785, 0)} US gal", f"{v} L")


def kg(v):
    return two(f"{v * 2.20462:,.0f} lb", f"{v:,} kg")


DRAW_NOTE = "Dimensions on the drawings are in millimetres (1″ = 25.4 mm)."
CHART_NOTE = ("Torque in N·m (1 N·m = 0.738 lbf·ft), power in kW (1 kW = 1.341 HP), spindle speed in rpm. Max. torque, S1 continuous "
              "nominal torque, continuous power and max. power of the main spindle motor.")
VOLT = "Custom voltage available: 208 V, 240 V, 480 V or 600 V 3-phase. CSA-approved electrical panel."

CSS = ("<style>.lt{font-size:7.3pt}.lt th,.lt td{padding:2.1pt 3.5pt;line-height:1.18}.lt tbody th{width:146pt;font-size:7.3pt}"
       ".lt tr.grp th{background:#e3e4e6;font:600 7.4pt Oswald;color:%s;text-transform:uppercase;letter-spacing:.07em;padding:3pt 5pt}"
       ".lt td small{font-size:6.4pt;white-space:nowrap}.lt tbody th small{display:block}.cap2{font:500 7.6pt Oswald;color:%s;text-transform:uppercase;letter-spacing:.05em}"
       ".ovl.la{transform:translate(0,-50%%)}.ovl{position:absolute;font:600 6.6pt/1 Barlow;color:%s;background:rgba(255,255,255,.92);padding:1pt 2pt;transform:translate(-50%%,-50%%);white-space:nowrap}"
       ".cd{background:#f4f4f5;border-left:3.7pt solid %s;padding:8pt 10pt}.cd p{margin:3pt 0 0}</style>"
       % (CHAR, CHAR, CHAR, ORANGE))


def ttable(models, rows, corner="Model"):
    """the specification table with group rows: rows [("#group", None) | (label, [cells])]"""
    th = f'<th class="corner">{corner}</th>' + "".join(f"<th>{m}</th>" for m in models)
    body = ""
    for lab, cells in rows:
        if cells is None:
            body += f'<tr class="grp"><th colspan="{len(models) + 1}">{lab}</th></tr>'
            continue
        if isinstance(cells, str):
            cells = [cells] * len(models)
        body += f"<tr><th>{lab}</th>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    return f'<table class="mt lt"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def campus(book, img):
    D.campus_page(book)
    p = book.pages[-1]
    p["body"] = p["body"].replace(im("gfl/campus.jpg", 2400), im(img, 2400))


def drawing_page(book, tab, eyebrow, head, img, note, toc=None, h=560):
    book.page(tab, title(eyebrow, head) + fig(img, h=h, px=2200) + P(note, cls="note"), toc=toc)


# --------------------------------------------------------------------------------------------------------------- lathes
MODELS = ["TTC-6", "TTC-8", "TTH-8", "TTH-10", "TTH-12"]
FEATURES = ["Specially manufactured precision, backlash-free double-nut ball screws",
            "Powerful, fast serial automatic tool-changer turret",
            "Rigid spindles supported by super-precision bearings",
            "Stable travel on linear guides supported at many points",
            "Very precise positioning and repeatability",
            "Quiet, vibration-free, high cutting capability",
            "One-piece 45° slant, robust cast body",
            "Fast service and spare parts support"]
STD = ["Mitsubishi M80A-8A", "Roller linear guides", "C1 – C3 precision ball screws", "BMT / slot type powerful turret", "Fully enclosed cabin",
       "Chip conveyor", "Automatic fill-and-drain lubrication system", "Automatic coolant system", "Oil and water separator unit",
       "3-phase 380 / 200 V – 50 / 60 Hz external transformer", "Foot pedal", "Front door safety switch", "Hydraulic power unit",
       "6″ – 8″ – 10″ – 12″ hydraulic chuck, soft and hard jaws", "Tool holders", "In-cabin lighting and alarm / warning lamps",
       "Electrical cabinet cooling system", "Portable handwheel", "Levelling bolts and plates", "Tailstock", "Air and water gun",
       "Tool bag &amp; tools", "CE"]
OPT = ["FANUC 0i TFP", "C axis", "Tool measuring system", "Workpiece measuring system", "Automatic bar feeder unit",
       "Air conditioner for the electrical cabinet", "Automatic door", "Chip cart", "Mist extraction unit", "Linear encoder",
       "Programmable tailstock", "Parts catcher"]
# the catalogue's technical table: Fanuc (option) and Mitsubishi (standard) columns, TTC-6, TTC-8, TTH-8, TTH-10, TTH-12
FAN = dict(fx=[1.8, 1.8, 3, 3, 3], fz=[1.8] * 5, tx=[(11, 27)] * 2 + [(20, 45)] * 3, tz=[(11, 27)] * 5,
           sp=[(11, 20.4), (11, 20.4), (15, 24.2), (11, 16.5), (15, 20.4)], st=[171.6, 195, 231, 315, 815.9],
           smt=[(52.5, 130), (52.5, 130), (71.6, 154), (105, 210), (143, 259)], cnc="FANUC 0i-TFP", kva=[25, 25, 32, 25, 32],
           L=[4123, 4123, 4345, 4345, 4545], W=[1709, 1709, 1924, 1924, 2073], lp=(3.7, 8.3), lt=(17.7, 52.5))
MIT = dict(fx=[2.2, 2.2, 3, 3, 3], fz=[2.2] * 5, tx=[(12, 32)] * 2 + [(22.5, 64)] * 3, tz=[(12, 32)] * 5,
           sp=[(11, 18), (11, 18), (11, 22.2), (11, 18), (15, 22.2)], st=[151.3, 171.9, 212, 343.8, 890.5],
           smt=[(52.5, 114.6), (52.5, 114.6), (70, 141.3), (116.7, 229.2), (143.2, 282.7)], cnc="M80 (FCA80H-8A)", kva=[32] * 5,
           L=[4118, 4123, 4346, 4346, 4546], W=[1709, 1709, 2073, 2073, 1924], lp=(3.7, 6.6), lt=(23.6, 42))


def lathe_rows(c):
    return [("Axis movements", None),
            ("Travel — X axis", [mm(v) for v in (190, 190, 300, 300, 300)]),
            ("Travel — Z axis", [mm(v) for v in (450, 450, 760, 760, 760)]),
            ("Axis motors", None),
            ("Feed motor power — X axis", [kw(v) for v in c["fx"]]),
            ("Feed motor power — Z axis", [kw(v) for v in c["fz"]]),
            ("Feed motor torque — X axis<br><small>continuous / holding / max.</small>", [nm_pair(*v) for v in c["tx"]]),
            ("Feed motor torque — Z axis<br><small>continuous / holding / max.</small>", [nm_pair(*v) for v in c["tz"]]),
            ("Main spindle", None),
            ("Max. spindle speed", [f"{v:,} rpm" for v in (6000, 4500, 4500, 3500, 2450)]),
            ("Main spindle motor power", [kw_pair(*v) for v in c["sp"]]),
            ("Max. spindle torque", [nm(v) for v in c["st"]]),
            ("Max. spindle motor torque<br><small>30 min / continuous</small>", [nm_pair(*v) for v in c["smt"]]),
            ("Spindle nose", [f"ASA {v}" for v in ("A2-5", "A2-6", "A2-6", "A2-8", "A2-11")]),
            ("Spindle bearing diameter (front)<br><small>inner / outer</small>", [mm_pair(*v) for v in ((80, 125), (100, 150), (100, 150), (130, 200), (160, 240))]),
            ("Spindle bore", [mm(v) for v in (56, 66, 66, 92, 118)]),
            ("Turret", None),
            ("Number of tool stations", "12"),
            ("Tool shank size", two("1 × 1″", "25 × 25 mm")),
            ("Max. boring bar diameter", mm(40)),
            ("Type", "Slot type"),
            ("Turret indexing time (1 station)", "0.20 – 0.34 s"),
            ("Turret drive type", "Servo mechanical"),
            ("Control system", None),
            ("CNC control unit", c["cnc"]),
            ("Screen", "10.4″ colour LCD"),
            ("Capacity", None),
            ("Swing", [mm(v) for v in (560, 560, 700, 700, 700)]),
            ("Recommended turning diameter", [mm(v) for v in (170, 210, 210, 254, 315)]),
            ("Max. turning diameter", [mm(v) for v in (305, 305, 528, 528, 488)]),
            ("Max. turning length", [mm(v) for v in (433, 406, 680, 660, 614)]),
            ("Chuck size", [f"{v}″" for v in (6, 8, 8, 10, 12)]),
            ("Bar capacity", [mm(v) for v in (45, 52, 52, 75, 95)]),
            ("Bed angle", "45°"),
            ("Ball screw diameter × pitch and tolerance class — Z axis", "C1"),
            ("Ball screw diameter × pitch and tolerance class — X axis", "C3"),
            ("Guideway size — Z axis", [mm(v, 2) for v in (30, 30, 45, 45, 45)]),
            ("Guideway size — tailstock", [mm(v, 2) for v in (35, 35, 45, 45, 45)]),
            ("Guideway size — X axis", [mm(v, 2) for v in (30, 30, 45, 45, 45)]),
            ("Guideway type [linear]", "Roller type"),
            ("Axis feeds", None),
            ("Rapid traverse — X axis", mmin(30)),
            ("Rapid traverse — Z axis", mmin(30)),
            ("Cutting feed — X axis", [mmin_range(1, 5)] * 2 + [mmin_range(1, 10)] * 3),
            ("Cutting feed — Z axis", [mmin_range(1, 5)] * 2 + [mmin_range(1, 10)] * 3),
            ("Accuracy", None),
            ("Positioning accuracy X / Z", two("0.0003 / 0.00016″", "0.008 / 0.004 mm")),
            ("Repeatability X / Z", two("0.00016 / 0.00008″", "0.004 / 0.002 mm")),
            ("Tailstock", None),
            ("Tailstock body travel", [mm(v) for v in (450, 450, 650, 650, 650)]),
            ("Quill diameter", two("Ø2.68″", "Ø68 mm")),
            ("Quill inner taper", [f"MK {v}" for v in (4, 4, 4, 4, 5)]),
            ("Power and coolant", None),
            ("Electrical power connection", [f"{v} kVA" for v in c["kva"]]),
            ("Coolant pump", two("1 HP (58 psi)", "0.75 kW (4 bar)")),
            ("Coolant tank capacity", [litre(v) for v in (140, 140, 160, 160, 160)]),
            ("Machine dimensions", None),
            ("Length", [mm(v) for v in c["L"]]),
            ("Width", [mm(v) for v in c["W"]]),
            ("Height", [mm(v) for v in (1778, 1778, 2008, 2008, 2008)]),
            ("Weight (approx.)", [kg(v) for v in (3260, 3306, 5389, 5439, 5886)]),
            ("C axis (option)", None),
            ("Max. live tool speed", [f"{v:,} rpm" for v in (6000, 6000, 6000, 6000, 5000)]),
            ("Live tool motor power<br><small>continuous / max.</small>", kw_pair(*c["lp"])),
            ("Live tool motor torque<br><small>continuous / max.</small>", nm_pair(*c["lt"])),
            ("Turret type", ["BMT55"] * 4 + ["BMT65"]),
            ("Max. turning diameter", [mm(v) for v in (275, 275, 438, 438, 373)]),
            ("Max. turning length", [mm(v) for v in (362, 335, 627, 607, 537)])]


def book_lathe():
    b = Book("lathe", "CNC lathes", "Dener TTC and TTH series CNC lathes", os.path.join(ROOT, "src", "files", "NovoTech-Dener-CNC-Lathes-2026.pdf"))
    b.title = "Dener TTC and TTH CNC Lathes — NovoTech Machine Tools"
    b.subject = "Dener TTC-TTH series CNC lathe catalogue, English imperial edition"
    b.cover("Dener · CNC lathes", "“The future is here” · sold &amp; serviced in Canada by NovoTech", "CNC lathes", "TTC · TTH series",
            "Turning · threading · drilling · C-axis milling", "lathe/ttc.png",
            [("Since 1974", "Manufacturing experience"), ("6 – 12″", "Hydraulic chuck"), ("45°", "Slant bed"), ("Canada", "Parts &amp; technical support")],
            hero_h=300, minis=("lathe/cut-1.png", "lathe/turret.png", "lathe/cover-a.png"))
    D.about_page(b)
    campus(b, "lathe/campus.jpg")
    # catalogue p3 — overview
    body = (CSS + title("TTC-TTH series CNC lathes", "Overview")
            + fig("lathe/ttc.png", "TTC CNC lathe", h=250, px=1600)
            + P("With the CNC lathe, precise internal and external diameter turning, internal and external threading and drilling are "
                "carried out. With the C-axis option, milling operations can also be performed.")
            + row(checks(FEATURES), fig("lathe/cutting.png", h=170, fit="cover", px=1000), cols="1.15fr 1fr", gap=16, align="start"))
    b.page("Overview", body, toc="Overview")
    # catalogue p4 — standard and optional equipment
    body = (CSS + title("TTC-TTH series CNC lathes", "Standard / optional equipment")
            + row(h2("Standard equipment") + checks(STD, cls="sm"),
                  h2("Optional equipment") + checks(OPT, cls="sm") + '<div style="height:8pt"></div>'
                  + fig("lathe/tool.png", h=150, px=700) + fig("lathe/cut-2.png", h=150, px=600), gap=20))
    b.page("Equipment", body, toc="Standard / Optional Equipment")
    # catalogue p5 — body structure, working area, part loading
    tbl_area = ttable(MODELS, [("Travel — X axis", [mm(v) for v in (190, 190, 300, 300, 300)]),
                               ("Travel — Z axis", [mm(v) for v in (450, 450, 760, 760, 760)])], corner="Working area")
    tbl_door = ttable(MODELS, [("Door opening", [mm(v) for v in (690, 690, 740, 740, 745)])], corner="Part loading")
    body = (CSS + title("TTC-TTH series CNC lathe", "Body structure and working area")
            + row(fig("lathe/body.png", "The 45° slant cast body with the turret, spindle and tailstock", h=230, px=1200),
                  h3("Body structure") + checks(["High speed", "Precision", "Long life", "High durability", "Vibration damping"]),
                  cols="1.3fr 1fr", gap=18, align="center")
            + h2("Working area") + tbl_area
            + h2("Part loading") + tbl_door
            + fig("lathe/loading.png", "Loading a heavy part by crane through the door", h=165, px=1000))
    b.page("Body · working area", body, toc="Body Structure and Working Area")
    # catalogue p5-6 — machining capacity, rigid structure, FEM, linear equipment, direct-drive servo motors
    cap_rows = [("Ød — recommended turning diameter", [mm(v) for v in (170, 210, 210, 254, 304)]),
                ("Ød<sub>1</sub> — max. turning diameter", [mm(v) for v in (305, 305, 528, 528, 488)]),
                ("Ød<sub>2</sub> — swing over bed", [mm(v) for v in (560, 560, 700, 700, 700)]),
                ("L — max. turning length", [mm(v) for v in (433, 406, 680, 660, 614)])]

    def cd(img, ttl, text, h=112):
        return (f'<div>{fig(img, h=h, px=900)}<div class="cd" style="margin-top:5pt"><div class="ittl">{ttl}</div>'
                f'<p class="sm" style="font-size:8.6pt">{text}</p></div></div>')
    body = (CSS + title("TTC-TTH series CNC lathe", "Machining capacity and structure")
            + row(ttable(MODELS, cap_rows, corner="Machining capacity"), fig("lathe/capacity.png", h=120, px=900), cols="1.6fr 1fr", gap=14, align="center")
            + '<div style="height:10pt"></div>'
            + grid([cd("lathe/rigid.png", "Rigid structure", "Effective damping of the cutting forces generated during machining, thanks to the "
                       "massive 45° main body structure."),
                    cd("lathe/fem.png", "Finite element method", "The optimum body structure obtained using the finite element method."),
                    cd("lathe/linear.png", "Ultra-precise linear equipment", "Ultra-precise, ground, preloaded and backlash-free ball screws and "
                       "linear bearing elements for precise positioning, repeatability, minimum friction, rigid support and quiet operation."),
                    cd("lathe/servo.png", "Direct-drive servo motors", "Direct connection between the motor and the ball screw for backlash-free, "
                       "precise motion.")], 2, 14))
    b.page("Capacity · structure", body)
    # catalogue p7 — turret, C-axis turret, spindle, tailstock
    body = (CSS + title("TTC-TTH series CNC lathes", "Turret, spindle and tailstock")
            + row(fig("lathe/turret.png", h=130, px=800) + h3("Turret")
                  + P("Fast tool change, high machining performance, precise positioning and powerful hydraulic clamping with the "
                      "12-station, electro-mechanical, servo-controlled slot type turret.", cls="sm"),
                  fig("lathe/turret-c.png", h=130, px=800) + h3("C-axis turret (option)")
                  + P("Machining on the C axis, fast tool change, high machining performance, precise positioning and powerful hydraulic "
                      "clamping with the new-generation BMT type, 12-station (all 12 live tools) electro-mechanical servo turret.", cls="sm"), gap=18)
            + h2("Spindle") + P("Reinforced with roller bearings, with high heat dissipation, low vibration and quiet operation: high durability "
                               "and excellent machining.", cls="sm")
            + row(fig("lathe/spindle-1.png", h=118, fit="cover", px=900), fig("lathe/spindle-2.png", h=118, fit="cover", px=900), gap=14)
            + h2("Tailstock") + P("Easy positioning with hydraulically controlled movement independent of the turret axis, and powerful braking.", cls="sm")
            + row(fig("lathe/tailstock-1.png", h=118, fit="cover", px=900), fig("lathe/tailstock-2.png", "Tailstock axis", h=118, fit="cover", px=900), gap=14))
    b.page("Turret · spindle", body, toc="Tool Change System · Spindle · Tailstock")
    # catalogue p8 — chip conveyor, coolant tank, chip cart, control unit
    labels = [("Coolant pump", 10.9, 31.8), ("Oil separator", 29.2, 23.8), ("Chip filter", 64.8, 29.2), ("Pallet", 80.1, 36.2), ("Tank", 75.9, 93.8)]
    tank = ('<div style="position:relative"><img src="%s" style="width:100%%;display:block">' % im("lathe/coolant.png", 1000)
            + "".join(f'<span class="ovl" style="left:{x}%;top:{y}%">{t}</span>' for t, x, y in labels) + "</div>")
    body = (CSS + title("TTC-TTH series CNC lathes", "Chip conveyor, coolant and control unit")
            + h2("Chip conveyor") + P("Trouble-free transport and discharge of the long, coarse and spiral chips of metal, fiber, teflon, delrin and "
                                     "similar materials.", cls="sm")
            + row(fig("lathe/conveyor-1.png", h=60, fit="cover", px=700) + '<div style="height:6pt"></div>' + fig("lathe/conveyor-2.png", h=60, fit="cover", px=700),
                  fig("lathe/conveyor-3.png", h=126, fit="cover", px=1000), cols="1fr 2fr", gap=10)
            + row(h2("Coolant tank") + P("Optimum cooling and easy maintenance with a 37 – 53 US gal (140 – 200 L), self-filtering, functional "
                                         "tank design.", cls="sm") + tank,
                  h2("Chip cart (option)") + P("Easy storage and discharge of all kinds of chips, with its tilting and braking features.", cls="sm")
                  + fig("lathe/cart.png", h=118, px=900), gap=16)
            + h2("Control unit") + P("Easy to use, with up-to-date technological modules, an operator-friendly interface and an ergonomic design.", cls="sm")
            + row(fig("lathe/control-1.png", h=112, fit="cover", px=900), fig("lathe/control-2.png", h=112, fit="cover", px=900), gap=14))
    b.page("Conveyor · control", body, toc="Chip Conveyor · Coolant · Control Unit")
    # catalogue p9-13 — working ranges of the tool holders
    note = DRAW_NOTE + " A: Z-axis travel · B: X-axis travel · C: tailstock travel. C Opt. = with the C-axis turret (option); Std. = standard turret."
    for i, (k, m) in enumerate((("ttc6", "TTC 6"), ("ttc8", "TTC 8"), ("tth8", "TTH 8"), ("tth10", "TTH 10"), ("tth12", "TTH 12"))):
        drawing_page(b, "Working range", "TTC-TTH series · machining distances", f"{m} working range", f"lathe/range-{k}.png", note,
                     toc=("TTC Series Working Range" if k == "ttc6" else "TTH Series Working Range" if k == "tth8" else None))
    drawing_page(b, "Tool interference", "TTC-TTH series · tool interface", "Tool interference", "lathe/interference.png",
                 DRAW_NOTE + " C Opt. = with the C-axis turret (option); Std. = standard turret.", toc="TTC/TTH Tool Interference")
    drawing_page(b, "Power · torque", "TTC-TTH series · power | torque", "Power and torque — Fanuc", "lathe/power-fanuc.png", CHART_NOTE,
                 toc="TTC/TTH Power and Torque")
    drawing_page(b, "Power · torque", "TTC-TTH series · power | torque", "Power and torque — Mitsubishi", "lathe/power-mitsubishi.png", CHART_NOTE)
    body = (title("TTC-TTH series · outline drawings", "TTH and TTH 12 outline")
            + h3("TTH") + fig("lathe/outline-tth.png", h=245, px=1800) + h3("TTH 12") + fig("lathe/outline-tth12.png", h=255, px=1800)
            + P(DRAW_NOTE, cls="note"))
    b.page("Outline drawings", body, toc="Outline Drawings")
    b.page("Outline drawings", title("TTC-TTH series · outline drawings", "TTC outline") + fig("lathe/outline-ttc.png", h=420, px=1800)
           + P(DRAW_NOTE, cls="note"))
    # catalogue p21-22 — technical data: the Mitsubishi (standard) and Fanuc (option) columns in one table, both values where they differ
    rm, rf = lathe_rows(MIT), lathe_rows(FAN)
    rows = []
    for (lab, cm), (_, cf) in zip(rm, rf):
        if cm == cf:
            rows.append((lab, cm))
        else:
            def tag(t):
                return lab.replace("</small>", f" · {t}</small>") if "<small>" in lab else f"{lab}<br><small>{t}</small>"
            rows += [(tag("Mitsubishi M80 (std.)"), cm), (tag("Fanuc 0i-TFP (opt.)"), cf)]
    groups = [i for i, r in enumerate(rows) if r[1] is None]
    cut1 = next(i for i in groups if rows[i][0] == "Turret")
    cut2 = next(i for i in groups if rows[i][0] == "Tailstock")
    parts = (rows[:cut1], rows[cut1:cut2], rows[cut2:])
    for n, rr in enumerate(parts):
        body = (CSS + title("TTC-TTH series CNC lathes", f"Technical data · {n + 1} of 3")
                + (P("Mitsubishi M80 control as standard, Fanuc 0i-TFP as an option: where the two differ, both values are given.", cls="note")
                   if n == 0 else "")
                + ttable(MODELS, rr, corner="Model")
                + (P("Specifications from Dener's catalogue. " + VOLT, cls="note") + included() if n == 2 else ""))
        b.page("Technical data", body, toc="Technical Data" if n == 0 else None)
    D.range_page(b)
    b.back("Lathe for your shop.", ["lathe/ttc.png", "lathe/turret.png", "lathe/body.png", "lathe/cutting.png"])
    D.fill_about(b)
    return b


# ----------------------------------------------------------------------------------------------------- machining centres
TMC = ["TMC 850", "TMC 1000", "TMC 1200", "TMC 1300", "TMC 1600"]
MC_FEATURES = ["Specially manufactured precision, backlash-free double-nut ball screws", "Fast, serial automatic tool changer",
               "Precise, rigid direct-drive or belt-and-pulley driven spindles", "High-precision, economical linear motion",
               "Stable travel on linear or friction guideways", "Above-standard positioning and repeatability accuracy",
               "Stress-relieved Meehanite cast body", "Quiet, vibration-free, high cutting capability", "Fast service and spare parts support"]
MC_STD = ["Mitsubishi M80A-8A (15″ touchscreen panel)", "Dialog programming (Navi-Mill)", "BT 40 / 10,000 rpm direct-drive spindle",
          "BT 40 arm-type 24-tool ATC", "C3 class double-nut ball screws", "Ball or roller linear guides", "Fully enclosed cabin",
          "Steel belt chip conveyor (with its bucket)", "Automatic lubrication system", "Spindle air blow system",
          "Coolant through nozzles around the spindle", "Oil and water separator unit", "Rigid tapping", "In-cabin chip washing system",
          "Electrical cabinet cooling system", "3-phase 380 / 200 V – 50 / 60 Hz external transformer",
          "In-cabin lighting and alarm / warning lamps", "Front door safety switch", "Air and water gun", "Coolant system",
          "Portable handwheel", "4th axis preparation", "Automatic power on / off", "Levelling bolts and plates", "Tool bag &amp; tools", "CE"]
MC_OPT = ["FANUC 0i MF (15″ LCD colour screen panel)", "BT 40 / 12,000 rpm and BT 40 / 15,000 rpm direct-drive spindles",
          "Through-tool coolant (435 psi, 30 bar)", "Air conditioner for the electrical cabinet", "CNC rotary table with the 4th axis",
          "Tool measuring system", "Workpiece measuring system", "Automatic door"]


def pm(v, per=300):
    return two(f"±{num(v / 25.4, 5)}″ / {num(per / 25.4)}″", f"±{num(v, 3)} / {per} mm")


def pump(k, bar):
    return two(f"{num(k * 1.341, 2)} HP ({num(bar * 14.504, 0)} psi)", f"{num(k, 2)} kW ({num(bar)} bar)")


def tmc_rows():
    return [("Movements", None),
            ("X-axis travel", [mm(v) for v in (850, 1020, 1200, 1300, 1600)]),
            ("Y-axis travel", [mm(v) for v in (510, 510, 600, 700, 700)]),
            ("Z-axis travel", [mm(v) for v in (560, 560, 600, 700, 700)]),
            ("Ball screws X / Y", "C3"),
            ("Distance from the column face to the spindle centre", [mm_pair(150, 710), mm_pair(150, 710), mm_pair(150, 750), mm_pair(130, 830), mm_pair(130, 830)]),
            ("Guideway type", "Roller type"),
            ("Guideway size X / Y / Z", [two(f"{num(a / 25.4, 2)} / {num(b / 25.4, 2)} / {num(c / 25.4, 2)}″", f"{a} / {b} / {c} mm")
                                         for a, b, c in ((30, 35, 35), (30, 35, 35), (35, 45, 45), (35, 45, 45), (35, 45, 45))]),
            ("Work table", None),
            ("Table size (X direction)", [mm(v) for v in (1000, 1200, 1300, 1450, 1750)]),
            ("Table size (Y direction)", [mm(v) for v in (500, 500, 600, 700, 700)]),
            ("T-slot size", mm(18, 2)),
            ("Number of T-slots", "5"),
            ("T-slot spacing", [mm(v) for v in (100, 100, 100, 125, 125)]),
            ("Table load capacity", [kg(v) for v in (500, 500, 1000, 1200, 1200)]),
            ("Spindle", None),
            ("Spindle taper (7/24 taper)", "BBT40"),
            ("Spindle drive", "Direct"),
            ("Feeds", None),
            ("Rapid traverse X / Y", mmin(36)),
            ("Rapid traverse Z", mmin(36)),
            ("Cutting feed", mmin_range(1, 15)),
            ("Tool magazine capacity", "24"),
            ("Tool magazine", None),
            ("Tool change method", "Arm type"),
            ("Tool shank type", "BBT"),
            ("Tool change time (tool to tool)", "1.3 s"),
            ("Tool change time (chip to chip)", ["3.1 s", "3.1 s", "3.7 s", "3.7 s", "3.7 s"]),
            ("Pull stud angle", "45°"),
            ("Max. tool diameter", two("Ø3.9 / Ø5.9″", "Ø100 / Ø150 mm")),
            ("Max. tool length", mm(300)),
            ("Max. tool weight", kg(7)),
            ("Accuracy", None),
            ("Positioning accuracy", [pm(0.004)] * 4 + [pm(0.005)]),
            ("Repeatability", pm(0.002)),
            ("Coolant — capacity, motor, pressure", None),
            ("Coolant pump", pump(0.55, 3)),
            ("Coolant pump for the gun", pump(0.37, 2)),
            ("Coolant pump for chip cleaning", pump(1.10, 2.5)),
            ("Coolant tank capacity", [litre(v) for v in (350, 350, 400, 400, 400)]),
            ("Machine dimensions (machine working area)", None),
            ("Length", [mm(v) for v in (3965, 4300, 4685, 4945, 5690)]),
            ("Width", [mm(v) for v in (2200, 2200, 2400, 2370, 2400)]),
            ("Height", [mm(v) for v in (3185, 3185, 3145, 3280, 3280)]),
            ("Weight (approx.)", [kg(v) for v in (6500, 7500, 8000, 9500, 10000)])]


def tmc_ctl_rows(c):
    return [("Screen", c["scr"]),
            ("Spindle motor", None),
            ("Code", c["sm"]), ("Speed", [f"{v:,} rpm" for v in c["rpm"]]), ("CTS readiness", c["cts"]),
            ("Torque (continuous / max.)", [nm_pair(*v) for v in c["st"]]), ("Power (continuous / max.)", [kw_pair(*v) for v in c["sp"]]),
            ("Axis motors", None),
            ("Code X / Y", c["axy"]), ("Torque X / Y (continuous / max.)", [nm_pair(*v) for v in c["txy"]]), ("Power X / Y", [kw(v) for v in c["pxy"]]),
            ("Code Z", c["az"]), ("Torque Z (continuous / max.)", [nm_pair(*v) for v in c["tz"]]), ("Power Z", [kw(v) for v in c["pz"]]),
            ("Air and power connection", None),
            ("Air pressure", two("73 / 87 psi", "5.0 / 6.0 bar")), ("Power connection", [f"{v} kVA" for v in c["kva"]])]


TMC_M = dict(scr=["10.4″ / 15″", "10.4″ / 15″", "15″", "15″", "15″"],
             sm=["SJ-DG11/100-03T", "SJ-DG11/100-03T", "SJ-DG11/120-03T", "SJ-DG15/120-02T-K-S", "SJ-DG15/120-02T-K-S"],
             rpm=[10000, 10000, 12000, 12000, 12000], cts=["–*", "–*", "+", "+", "+"],
             st=[(47.7, 115)] * 3 + [(77.8, 191)] * 2, sp=[(7.5, 18)] * 3 + [(11, 30)] * 2,
             axy=["HG224S-D48", "HG224S-D48", "HG354S-D48", "HG354S-D48", "HG354S-D48"],
             txy=[(7, 46.5), (7, 46.5), (11.1, 75), (11.1, 75), (14.3, 122)], pxy=[2.2, 2.2, 3.5, 3.5, 3.5],
             az=["HG354BS-D48"] * 3 + ["HG453BS-D48"] * 2, tz=[(11.1, 75)] * 3 + [(14.3, 122)] * 2, pz=[3.5, 3.5, 3.5, 4.5, 4.5],
             kva=[32, 32, 32, 43, 43])
TMC_F = dict(scr=["10.4″", "10.4″", "15″", "15″", "15″"],
             sm=["βiI 8/12000-B", "βiI 8/12000-B", "βiIT 12/10000-B", "βiIT 12/10000-B", "βiIT 12/10000-B"],
             rpm=[12000, 12000, 10000, 10000, 10000], cts=["–**", "–**", "+", "+", "+"],
             st=[(35.8, 105)] * 2 + [(52.5, 130)] * 3, sp=[(7.5, 16.5)] * 2 + [(11, 20.4)] * 3,
             axy=["βiS 22/3000-B"] * 5, txy=[(20, 45)] * 5, pxy=[3] * 5,
             az=["βiS 22/3000-B"] * 3 + ["βiS 40/2000-B"] * 2, tz=[(20, 45)] * 3 + [(36, 90)] * 2, pz=[3] * 5, kva=[32] * 5)

TDC = ["TDC 2112", "TDC 3116", "TDC 4120"]


def tdc_rows():
    return [("X axis", [mm(v) for v in (2100, 3100, 4100)]),
            ("Y axis", [mm(v) for v in (1220, 1600, 2020)]),
            ("Z axis", [two("23.6″ (opt. 31.5″)", "600 mm, opt. 800 mm"), mm(1020), mm(1020)]),
            ("Distance between the two columns", [mm(v) for v in (1400, 1700, 2100)]),
            ("Table size", [two(f"{num(a / 25.4)} × {num(b / 25.4)}″", f"{a:,} × {b:,} mm") for a, b in ((2000, 1200), (3000, 1500), (4000, 1800))]),
            ("T-slots (number × slot width × distance)", [two(f"{n} × 0.87″ × 5.9″", f"{n} × 22 × 150 mm") for n in (7, 9, 9)]),
            ("Max. table load", [kg(v) for v in (4000, 10000, 12000)]),
            ("Spindle taper", "BBT50"),
            ("Spindle speed", "10,000 rpm"),
            ("Spindle motor", kw_pair(22, 26)),
            ("Rapid traverse X / Y / Z", two("39 / 39 / 39 ft/min", "12 / 12 / 12 m/min")),
            ("Cutting feed", mmin_range(1, 10)),
            ("Axis motors X, Y, Z", [two("12.1 / 6 / 6 HP", "9 / 4.5 / 4.5 kW"), two("12.1 / 9.4 / 9.4 HP", "9 / 7 / 7 kW"), two("12.1 / 9.4 / 9.4 HP", "9 / 7 / 7 kW")]),
            ("Tool capacity", ["Arm type, 24 tools", "Chain type, 40 tools", "Chain type, 40 tools"]),
            ("Coolant tank capacity", [litre(v) for v in (300, 800, 800)]),
            ("Guideway types", "X, Y, Z roller linear guides"),
            ("Control unit", "Mitsubishi (Fanuc option)"),
            ("Positioning accuracy X / Y / Z", two("±0.0003″", "±0.008 mm")),
            ("Repeatability X / Y / Z", two("±0.00016″", "±0.004 mm")),
            ("Guarding", "Semi-open enclosure"),
            ("Width", [mm(v) for v in (3640, 4340, 4740)]),
            ("Length", [mm(v) for v in (5965, 8315, 10315)]),
            ("Height", [mm(v) for v in (3372, 4390, 4390)]),
            ("Weight (approx.)", [kg(v) for v in (21000, 32000, 40000)])]


def book_mc():
    b = Book("mc", "CNC machining centres", "Dener TMC vertical and TDC double-column machining centres",
             os.path.join(ROOT, "src", "files", "NovoTech-Dener-Machining-Centres-2026.pdf"))
    b.title = "Dener TMC Vertical and TDC Double-Column Machining Centres — NovoTech Machine Tools"
    b.subject = "Dener TMC vertical and TDC double-column CNC machining centre catalogues, English imperial edition"
    b.cover("Dener · Machining centres", "“The future is here” · sold &amp; serviced in Canada by NovoTech", "Machining centres",
            "TMC · TDC series", "Vertical and double-column CNC machining centres", "mc/tmc.png",
            [("Since 1974", "Manufacturing experience"), ("33.5 – 161″", "X-axis travel"), ("BBT40 · BBT50", "Spindle taper"),
             ("Canada", "Parts &amp; technical support")], hero_h=290, minis=("mc/tdc-a.png", "mc/cover-b.png", "mc/spindle.png"))
    D.about_page(b)
    campus(b, "mc/campus.jpg")
    head = "TMC series CNC vertical machining centres"
    # vertical catalogue p3 — overview
    body = (CSS + title(head, "Overview") + fig("mc/tmc.png", "TMC CNC vertical machining centre", h=250, px=1600)
            + P("With CNC vertical machining centres, precision milling, drilling, pocketing and synchronized tapping without an adapter are "
                "possible, as well as the machining of forms defined by free-hand drawing.")
            + row(checks(MC_FEATURES), fig("mc/machining.png", h=190, fit="cover", px=900), cols="1.15fr 1fr", gap=16, align="start"))
    b.page("Overview", body, toc="TMC — Overview")
    # p4 — standard / optional equipment
    body = (CSS + title(head, "Standard / optional equipment")
            + row(h2("Standard equipment") + checks(MC_STD, cls="sm"),
                  h2("Optional equipment") + checks(MC_OPT, cls="sm") + '<div style="height:8pt"></div>'
                  + fig("mc/cover-a.png", h=150, fit="cover", px=700) + '<div style="height:8pt"></div>' + fig("mc/cover-d.png", h=150, fit="cover", px=600), gap=20))
    b.page("Equipment", body, toc="TMC — Standard / Optional Equipment")
    # p5 — body structure, working area, idle axis speeds
    xyz = lambda a, b_, c: two(f"{num(a / 25.4)} / {num(b_ / 25.4)} / {num(c / 25.4)}″", f"{a:,} / {b_:,} / {c:,} mm")
    body = (CSS + title(head, "Body structure and working area")
            + row(D.diagram("Rigid and<br>optimized<br>massive cast<br>body", [("tl", "High speed"), ("tr", "High durability"), ("l", "Precision"),
                                                                            ("r", "Long life"), ("b", "Vibration damping")]),
                  fig("mc/body.png", "The cast column, base and table", h=240, px=1200), cols="1fr 1fr", gap=16, align="center")
            + h2("Working area") + ttable(TMC, [("Stroke X / Y / Z", [xyz(*v) for v in ((850, 510, 560), (1020, 510, 560), (1200, 600, 600),
                                                                                        (1300, 700, 700), (1600, 700, 700))])], corner="Stroke")
            + h2("Idle axis speeds") + ttable(TMC, [("Rapid X / Y / Z", two("118 / 118 / 118 ft/min", "36 / 36 / 36 m/min"))], corner="Rapid"))
    b.page("Body · working area", body, toc="TMC — Body Structure and Working Area")
    # p6 — part loading and table dimensions
    body = (CSS + title(head, "Part loading and table dimensions")
            + h2("Part loading") + ttable(TMC, [("Load capacity", [kg(v) for v in (500, 500, 1000, 1200, 1200)])], corner="Capacity")
            + fig("mc/loading.png", "Loading a part by crane", h=210, px=1200)
            + h2("Table dimensions") + ttable(TMC, [("Table L × W", [two(f"{num(a / 25.4)} × {num(c / 25.4)}″", f"{a:,} × {c} mm")
                                                                     for a, c in ((1000, 500), (1200, 500), (1300, 600), (1450, 700), (1750, 700))])], corner="Table")
            + fig("mc/table-dims.png", "Table length L and width W", h=170, px=1100))
    b.page("Loading · table", body, toc="TMC — Part Loading and Table Dimensions")

    def cd(img, ttl, text, h=112):
        return (f'<div>{fig(img, h=h, px=900)}<div class="cd" style="margin-top:5pt"><div class="ittl">{ttl}</div>'
                f'<p class="sm" style="font-size:8.6pt">{text}</p></div></div>')
    body = (CSS + title(head, "Structure")
            + grid([cd("mc/rigid.png", "Rigid structure", "Excellent vibration damping and cutting-load distribution thanks to the combined "
                       "design of the deltoid column and the main body.", h=190),
                    cd("mc/fem.png", "Finite element method", "The optimum body structure obtained using the finite element method.", h=190),
                    cd("mc/linear.png", "Ultra-precise linear equipment", "Ultra-precise, ground, preloaded and backlash-free ball screws and "
                       "linear bearing elements for precise positioning, repeatability, minimum friction, rigid support and quiet operation.", h=150),
                    cd("mc/servo.png", "Direct-drive servo motors", "Direct connection between the motor and the ball screw for backlash-free, "
                       "precise motion.", h=150)], 2, 14))
    b.page("Structure", body)
    # p7 — tool change, spindle, spindle cooling, through-tool coolant
    body = (CSS + title(head, "Tool change and spindle")
            + h2("Tool change system") + P("Fast, stable and functional tool change with the 24-tool, cam-type, inverter-controlled ATC.", cls="sm")
            + row(fig("mc/atc-1.png", h=140, fit="cover", px=900), fig("mc/atc-2.png", h=140, fit="cover", px=900), gap=14)
            + h2("Direct-drive spindle") + row(P("Powerful machining capability with high heat dissipation, low vibration, quiet operation and easy "
                                                "maintenance.", cls="sm"), fig("mc/spindle.png", h=130, px=1000), cols="1fr 1.3fr", gap=14, align="center")
            + row(h2("Spindle cooling system") + P("Automatically controlled cooling system to prevent thermal deformation and extend the spindle's "
                                                    "life.", cls="sm") + row(fig("mc/spcool-1.png", h=120, px=400), fig("mc/spcool-2.png", h=120, px=400), gap=8),
                  h2("Through-tool coolant (option)") + P("Excellent cutting capability and long tool life with coolant through the tool.", cls="sm")
                  + fig("mc/tsc.png", h=120, px=500), gap=18))
    b.page("Tool change · spindle", body, toc="TMC — Tool Change System and Spindle")
    # p8 — chip conveyor, coolant tank, chip cart, control unit
    labels = [("Tool coolant pump", 6.5, 10.3), ("Chip washing pump", 6.5, 17.2), ("Hand gun pump", 6.5, 24.1), ("Oil separator", 32.7, 36.7),
              ("Chip filter", 50.1, 87.4), ("Level indicator", 71.8, 87.6), ("Electronic level control", 24.2, 95.4)]
    tank = ('<div style="position:relative"><img src="%s" style="width:100%%;display:block">' % im("mc/coolant.png", 1100)
            + "".join(f'<span class="ovl la" style="left:{x}%;top:{y}%">{t}</span>' for t, x, y in labels) + "</div>")
    body = (CSS + title(head, "Chip conveyor, coolant and control unit")
            + h2("Chip conveyor") + P("Trouble-free transport and discharge of the long, coarse and spiral chips of metal, fiber, teflon, delrin and "
                                     "similar materials.", cls="sm")
            + row(fig("mc/conveyor-1.png", h=62, fit="cover", px=700) + '<div style="height:6pt"></div>' + fig("mc/conveyor-2.png", h=62, fit="cover", px=700),
                  fig("mc/conveyor-3.png", h=130, px=1000), cols="1fr 2fr", gap=10)
            + row(h2("Coolant tank") + P("Optimum cooling and easy maintenance with a 132 US gal (500 L), self-filtering, functional tank "
                                         "design.", cls="sm") + tank,
                  h2("Chip cart") + P("Easy storage and discharge of all kinds of chips, with its tilting and braking features.", cls="sm")
                  + fig("mc/cart.png", h=110, px=900), gap=16)
            + h2("Control unit") + P("Easy to use, with up-to-date technological modules, an operator-friendly interface and an ergonomic design.", cls="sm")
            + row(fig("mc/control-1.png", h=110, fit="cover", px=900), fig("mc/control-2.png", h=110, fit="cover", px=900), gap=14))
    b.page("Conveyor · control", body, toc="TMC — Chip Conveyor, Coolant and Control Unit")
    # p9-10 — technical data
    rows = tmc_rows()
    cut = next(i for i, r in enumerate(rows) if r[0] == "Tool magazine")
    for n, rr in enumerate((rows[:cut], rows[cut:])):
        b.page("Technical data", CSS + title(head, f"Technical data · {n + 1} of 4") + ttable(TMC, rr, corner="Model")
               + (P("The values in the table may change with renewals and revisions of the machines.", cls="note") if n else ""),
               toc="TMC — Technical Data" if n == 0 else None)
    b.page("Technical data", CSS + title(head, "Technical data · 3 of 4") + h3("Mitsubishi control unit (standard)")
           + ttable([m + " (M)" for m in TMC], tmc_ctl_rows(TMC_M), corner="Model") + P("* CTS = SJ-DG11/120-03T-S (12,000 rpm).", cls="note"))
    b.page("Technical data", CSS + title(head, "Technical data · 4 of 4") + h3("Fanuc control unit (option)")
           + ttable([m + " (F)" for m in TMC], tmc_ctl_rows(TMC_F), corner="Model")
           + P("** CTS = βiIT 12/10000-B (10,000 rpm). The values in the table may change with renewals and revisions of the machines. " + VOLT,
               cls="note") + included())
    # double-column catalogue — cover and inner spread
    hd = "TDC series double-column CNC machining centres"
    body = (CSS + title("Dener · CNC machining centre", "Double-column machining centre")
            + fig("mc/tdc-b.png", "TDC double-column machining centre", h=270, px=1800)
            + stats([("2×", "Motor power compared to competitors"), ("Long", "Distance between the two columns")])
            + '<div style="height:10pt"></div>'
            + P("The Dener double-column CNC machining centre increases the competitiveness of your business by combining creative design, "
                "technological superiority and productivity. With this machine, which meets your precision machining needs at the highest "
                "level, you can produce quickly and efficiently without compromising on quality."))
    b.page("Double column", body, toc="TDC — Double-Column Machining Centre")
    body = (CSS + title(hd, "Control unit, chip conveyor and tool change")
            + row(fig("mc/tdc-control.png", h=150, px=900),
                  h3("Control unit") + P("The Mitsubishi control unit makes your production and machining processes more efficient and flexible "
                                         "with its powerful performance, advanced features and reliability.", cls="sm")
                  + checks(["Advanced control capabilities", "Fast response time", "Comprehensive connection options", "User-friendly interface"], cls="sm"),
                  cols="1fr 1.4fr", gap=16, align="center")
            + row(fig("mc/tdc-conveyor.png", h=150, px=900),
                  h3("Chip conveyor") + P("The chip conveyor controls your machining processes and keeps them running steadily, increasing your "
                                          "machining efficiency. Thanks to this solution, the preparation time for complex operations is shorter, "
                                          "and your ability to handle a wide variety of workpieces grows.", cls="sm"), cols="1fr 1.4fr", gap=16, align="center")
            + row(fig("mc/tdc-atc.png", h=150, px=900),
                  h3("Tool change") + P("The tool change system optimizes efficiency with fast, automatic tool change. Fast, automatic tool change "
                                        "shortens machining times and raises productivity while keeping the quality.", cls="sm"),
                  cols="1fr 1.4fr", gap=16, align="center"))
    b.page("Double column", body)
    rpm = ('<table class="mt lt" style="width:auto"><thead><tr><th class="corner">RPM</th><th>BBT-50</th><th>CTS</th></tr></thead><tbody>'
           '<tr><th>6,000 rpm</th><td>○</td><td>○</td></tr><tr><th>8,000 rpm</th><td>○</td><td>○</td></tr>'
           '<tr><th>10,000 rpm</th><td>●</td><td>●</td></tr></tbody></table><p class="note">std. ● · opt. ○</p>')
    body = (CSS + title(hd, "Linear equipment, coolant and spindle")
            + row(fig("mc/tdc-linear.png", h=135, px=900),
                  h3("Precise linear equipment") + P("Precise linear equipment offers excellent accuracy, smooth movement and long life. It keeps the "
                                                     "precision of your machining processes stable and so gives higher-quality workpieces.", cls="sm"),
                  cols="1fr 1.4fr", gap=16, align="center")
            + row(fig("mc/tdc-coolant.png", h=110, px=900),
                  h3("Coolant tank") + P("The coolant tank optimizes your machining processes while extending tool life, keeping the machining "
                                         "conditions efficient and contributing to excellent results.", cls="sm"), cols="1fr 1.4fr", gap=16, align="center")
            + row(fig("mc/tdc-spindle.png", h=105, px=900),
                  h3("Direct-drive spindle") + P("High torque, fast acceleration and excellent precision: this advanced spindle technology takes "
                                                 "the performance of your CNC machining centre to new levels, bringing speed and precision together "
                                                 "for outstanding machining results.", cls="sm") + rpm, cols="1fr 1.4fr", gap=16, align="center")
            + row(row(fig("mc/tdc-spcool.png", h=110, px=400), h3("Spindle cooling system") + P("Extends tool life by controlling the "
                      "temperature, and keeps the machining process stable. This cooling solution maximizes the performance of your CNC "
                      "machining centre.", cls="xs"), cols="54pt 1fr", gap=10, align="center"),
                  row(fig("mc/tdc-tsc.png", h=110, px=500), h3("Through-tool coolant") + P("Automatically controlled cooling system to prevent "
                      "thermal deformation and extend the spindle's life.", cls="xs"), cols="80pt 1fr", gap=10, align="center"), gap=16))
    b.page("Double column", body)
    body = (CSS + title(hd, "Technical data") + ttable(TDC, tdc_rows(), corner="TDC double column") + P(VOLT, cls="note") + included())
    b.page("Technical data", body, toc="TDC — Technical Data")
    D.range_page(b)
    b.back("Machining centre for your shop.", ["mc/tmc.png", "mc/tdc-a.png", "mc/spindle.png", "mc/machining.png"])
    D.fill_about(b)
    return b


BOOKS = {"lathe": book_lathe, "mc": book_mc}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or list(BOOKS)
    for k in args:
        D.build(BOOKS[k](), "--html" in sys.argv)


if __name__ == "__main__":
    main()
