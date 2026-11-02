#!/usr/bin/env python3
"""NovoTech editions of Dener's machine-tool catalogues (Turkish, R-2404-TR) — every page, picture and figure, translated into
English, in NovoTech's catalogue format, with the units in imperial (metric in brackets).  The owner, Nov 1 2026: "change nothing,
delete nothing, only the units become imperial — every PDF converted to the NovoTech format is converted completely".

    python3 tools/brochure/dener_mt_editions.py [lathe] [--html]

  lathe  TTC-TTH CNC Torna Tezgahı (R-2404-TR)            → src/files/NovoTech-Dener-CNC-Lathes-2026.pdf

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
from dener_laser_editions import Book, title, P, checks, h2, h3, fig, row, grid, im, included, ORANGE, OR2, CHAR  # noqa: E402

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
       ".ovl{position:absolute;font:600 6.6pt/1 Barlow;color:%s;background:rgba(255,255,255,.92);padding:1pt 2pt;transform:translate(-50%%,-50%%);white-space:nowrap}"
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


BOOKS = {"lathe": book_lathe}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or list(BOOKS)
    for k in args:
        D.build(BOOKS[k](), "--html" in sys.argv)


if __name__ == "__main__":
    main()
