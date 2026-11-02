#!/usr/bin/env python3
"""NovoTech editions of Senfeng's four tube laser "Technical Solutions" — every page, picture and detail of the originals in
NovoTech's catalogue format, units in imperial (metric in brackets).  The owner, Nov 1 2026: "make their PDF files too … change
nothing, delete nothing, only the units become imperial".

    python3 tools/brochure/senfeng_tube_editions.py [t12] [t24] [nt] [plus] [--html]

  t12   SF6012T two-chuck tube laser (follow-up support), 1.5 – 3 kW (SF6012T, 20 pages)
          → src/files/NovoTech-Senfeng-SF6012T-Tube-Laser-Technical-Specification-2026.pdf
  t24   SF6024T two-chuck tube laser (follow-up support), 1.5 – 6 kW (SF6024T, 20 pages)
          → src/files/NovoTech-Senfeng-SF6024T-Tube-Laser-Technical-Specification-2026.pdf
  nt    SF6024NT three-chuck zero-tail tube laser, 1.5 – 6 kW (SF6024NT, 22 pages)
          → src/files/NovoTech-Senfeng-SF6024NT-Tube-Laser-Technical-Specification-2026.pdf
  plus  SF6012PLUS high-speed tube laser, 3 – 6 kW (SF6012PLUS, 20 pages)
          → src/files/NovoTech-Senfeng-SF6012PLUS-Tube-Laser-Technical-Specification-2026.pdf

Cutting tables: tools/brochure/data-senfeng-tube-cutting.json (read from the PDFs); speeds in inches per minute with Senfeng's metres
per minute below, wall thicknesses in decimal inches with the millimetres.  Images: tools/src-images/senfeng-tube-spec/ (from the
PDFs) and the shared after-sales pictures of tools/src-images/senfeng-h-spec/.
Adapted, and why: the warranty line states NovoTech's 1-year warranty (the PLUS sheet says 2 years); installation at the customer's
site is by NovoTech with Senfeng; the 380 V supply keeps the note on the transformer NovoTech supplies for 208 / 240 / 480 / 600 V;
the operating costs stay in RMB as Senfeng gives them (Chinese prices, for reference); Senfeng's document number and its China
contact page are left out (NovoTech's contact details are on every page).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dener_laser_editions as D   # noqa: E402
import senfeng_h_editions as H     # noqa: E402  (Senfeng's included box, the after-sales pages, the table styles)

ROOT = D.ROOT
T = os.path.join(ROOT, "tools", "src-images", "senfeng-tube-spec") + "/"
title, P, checks, h2, h3, fig, row, grid, card, kv = D.title, D.P, D.checks, D.h2, D.h3, D.fig, D.row, D.grid, D.card, D.kv
CUT = json.load(open(os.path.join(HERE, "data-senfeng-tube-cutting.json")))
D.CSS += """
.ctt{border-collapse:collapse;width:100%;font:400 7.6pt/1.12 Barlow,BarlowX;color:#2d2e30}
.ctt th,.ctt td{padding:2.4pt 2.5pt;text-align:center;vertical-align:middle;border-bottom:.6pt solid #e2e3e5}
.ctt thead th{background:#2d2e30;color:#fff;font:500 7.8pt Oswald;letter-spacing:.03em;padding:4.4pt 2pt}
.ctt thead th.corner{background:#f2a23b;color:#2d2e30}
.ctt td small{display:block;font-size:6.2pt;color:#8c8e91;margin-top:.5pt}
.ctt td.t{font-weight:600}
.ctt td.m{background:#eeeff0;font:600 8pt Oswald;text-transform:uppercase;letter-spacing:.03em;width:62pt}
.ctt tbody tr:nth-child(even) td:not(.m){background:#f7f7f8}
.clamp{border-collapse:collapse;width:100%;font:400 8.2pt/1.3 Barlow,BarlowX;color:#2d2e30}
.clamp th,.clamp td{padding:3.6pt 6pt;border-bottom:.8pt solid #d9dadc;text-align:left;vertical-align:middle}
.clamp thead th{background:#2d2e30;color:#fff;font:500 8.6pt Oswald;letter-spacing:.04em;text-transform:uppercase}
.clamp thead th:first-child{background:#f2a23b;color:#2d2e30}
.clamp td.d{width:66pt;text-align:center}
.clamp td.d img{max-height:40pt;max-width:62pt;object-fit:contain}
.clamp tbody th{font:600 8.6pt Barlow;width:92pt}
.clamp small{color:#6d6f73}
.pre{list-style:none;margin:0;counter-reset:p}
.pre li{counter-increment:p;position:relative;padding:0 0 0 22pt;margin:0 0 4.6pt;font:400 8.5pt/1.36 Barlow,BarlowX;color:#2d2e30}
.pre li::before{content:counter(p);position:absolute;left:0;top:0;width:15pt;height:13pt;background:#2d2e30;color:#fff;font:600 7.6pt/13pt Oswald;text-align:center}
.pre li ol{margin:3pt 0 0 14pt}
.pre li ol li{padding-left:0;margin-bottom:2pt;counter-increment:none;list-style:decimal}
.pre li ol li::before{content:none}
.u4{display:grid;grid-template-columns:1fr 1fr;gap:12pt 16pt}
.u4 .ut{font:600 10pt/1.2 Oswald;color:#2d2e30;text-transform:uppercase;letter-spacing:.03em;border-top:1.8pt solid #f2a23b;padding-top:4pt;margin-bottom:4pt}
.u4 .ut small{font:400 8pt Barlow;color:#e08a1e;text-transform:none;letter-spacing:0;margin-left:4pt}
.u4 .ui{height:92pt;display:flex;align-items:center;justify-content:center;margin-bottom:5pt}
.u4 .ui img{max-width:100%;max-height:100%;object-fit:contain}
.u4 table{border-collapse:collapse;width:100%;font:400 7.8pt/1.25 Barlow,BarlowX;color:#2d2e30}
.u4 td,.u4 th{padding:2.8pt 5pt;border-bottom:.6pt solid #e2e3e5;text-align:left;vertical-align:top}
.u4 th{font:600 7.8pt Barlow;width:46%}
.u4 tr:nth-child(odd){background:#f4f4f5}
.hl{font:500 9pt/1.3 Oswald;color:#e08a1e;text-transform:uppercase;letter-spacing:.04em;margin:-2pt 0 4pt}
.bul{list-style:none;margin:0}
.bul li{position:relative;padding-left:11pt;margin:0 0 3.4pt;font:400 8.6pt/1.36 Barlow,BarlowX;color:#2d2e30}
.bul li::before{content:"";position:absolute;left:0;top:4.6pt;width:5pt;height:5pt;background:#f2a23b}
"""

WARRANTY = ("The warranty period for the entire machine (excluding consumables, non-force majeure natural disasters, war, improper "
            "operation, and human damage) is 1 year.")
CONF_NOTES = ["This is Senfeng's optimized configuration. Changes in brand or configuration may cause irreversible effects.", WARRANTY]
VOLT = H.VOLT_NOTE


# ------------------------------------------------------------------------------------------------------------- units
def inch(mm, nd=1):
    return f"{mm / 25.4:.{nd}f}"


def lb(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


def ftmin(v):
    return f"{round(v * 3.281):,} ft/min ({v:g} m/min)"


def ft_mm(a, b=None):
    """tube length: 1000 → 3.3 ft (1,000 mm); a range when b is given"""
    if b is None:
        return f"{a / 304.8:.1f} ft ({a:,} mm)"
    return f"{a / 304.8:.1f} – {b / 304.8:.1f} ft ({a:,} – {b:,} mm)"


def dia(a, b):
    return f"Ø{inch(a)} – {inch(b)}″ (Ø{a} – {b} mm)"


def sq(a, b):
    return f"{inch(a)} – {inch(b)}″ ({a} – {b} mm)"


def dims_ft(l, w, h):
    return f"{l / 304.8:.1f} × {w / 304.8:.1f} × {h / 304.8:.1f} ft ({l:,} × {w:,} × {h:,} mm)"


# ------------------------------------------------------------------------------------------------------------- pieces
def ul(items, cls="bul"):
    return f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ol(items):
    return '<ol class="num">' + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


def tech_table(rows, head=("No.", "Item", "Parameter", "Remarks")):
    body = "".join(f"<tr><td class='n'>{i}</td><th>{a}</th><td>{b}</td><td>{c}</td></tr>" for i, (a, b, c) in enumerate(rows, 1))
    th = "".join(f"<th>{h}</th>" for h in head)
    return f'<table class="cf tight"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def notes(items):
    return "".join(f'<p class="small-note">{i}. {x}</p>' for i, x in enumerate(items, 1))


GAS = {"N2/Air": "N₂ / air", "O2": "O₂"}


def cell(c):
    if c == "/":
        return "/"
    v, g = c[:-1].split("(")
    a, b = (v.split("-") + [None])[:2]
    imp = f"{round(float(a) * 39.3701):,}" + (f" – {round(float(b) * 39.3701):,}" if b else "")
    return f"{imp}<small>{a}{' – ' + b if b else ''} · {GAS[g]}</small>"


def cut_table(powers, blocks):
    th = "".join(f"<th>{p}</th>" for p in powers)
    body = ""
    for b in blocks:
        n = len(b["rows"])
        for i, (t, vals) in enumerate(b["rows"]):
            m = f'<td class="m" rowspan="{n}">{b["material"]}</td>' if i == 0 else ""
            body += f'<tr>{m}<td class="t">{float(t) / 25.4:.3f}″<small>{t} mm</small></td>' + "".join(f"<td>{cell(v)}</td>" for v in vals) + "</tr>"
    return (f'<table class="ctt"><thead><tr><th class="corner">Material</th><th>Wall thickness</th>{th}</tr></thead>'
            f"<tbody>{body}</tbody></table>")


def cut_pages(b, model, no, notes_):
    data = CUT[model]
    pages = data["pages"]
    nums = [no + i for i in range(len(pages))]
    if len(pages) == 1 and sum(len(x["rows"]) for x in pages[0]) > 20:      # one long source page → two NovoTech pages, same number
        pages, nums = [pages[0][:1], pages[0][1:]], [no, no]
    for i, blocks in enumerate(pages):
        names = " · ".join(x["material"].lower() for x in blocks)
        body = (title(f"{nums[i]:02d} · Cutting parameters · {model}", names.capitalize())
                + P("Cutting speed by laser source power in inches per minute, with Senfeng's metres per minute and the assist gas below "
                    "each value.", cls="xs")
                + cut_table(data["powers"], blocks) + notes(notes_)
                + (D.included() if sum(len(x["rows"]) for x in blocks) <= 13 else ""))
        b.page("Cutting parameters", body, key=f"cut{i + 1}")


T_CUT_NOTES = ["When processing carbon steel tubes with a wall thickness over 0.197″ (5 mm) and a diameter or side length under 2″ "
               "(50 mm), oxygen is not recommended as the assist gas. For tubes of these dimensions, please consult the process "
               "engineering team.",
               "The parameters are for reference only. The values above are theoretical; tube dimensions, equipment speed and other "
               "factors will affect the cutting speed."]
N_CUT_NOTES = ["For carbon steel pipes with a wall thickness over 0.197″ (5 mm) and a diameter or side length under 2″ (50 mm), oxygen is not "
               "recommended as the assist gas. Contact us for such pipe sizes.",
               "There are two types of cutting heads: ① the standard cutting head cuts regular pipes such as square, round, elliptical and "
               "triangular pipes without concave angles; ② the PC cutting head makes a significant difference in cutting speed and quality "
               "on carbon steel pipes of 0.236″ (6 mm) and thicker — the speed is reduced by 20 – 40 %, but it can process pipes of any shape.",
               "Parameters are for reference only. The values above are theoretical; the actual cutting speed may vary with factors such as "
               "pipe dimensions and equipment speed."]


def cost_rows_table(powers, rows):
    """rows: (label, values, span) — span=True: one value per power across its three gas columns; group rows ('grp', label, n)"""
    gases = ["Air", "O₂", "N₂"]
    th1 = "".join(f'<th colspan="3">{p}</th>' for p in powers)
    th2 = "".join(f"<th>{g}</th>" for _ in powers for g in gases)
    body = ""
    for r in rows:
        if r[0] == "grp":
            continue
        lab, vals, span = r[0], r[1], r[2] if len(r) > 2 else False
        lead = r[3] if len(r) > 3 else ""
        cells = "".join(f'<td colspan="3">{v}</td>' for v in vals) if span else "".join(f"<td>{v}</td>" for v in vals)
        body += f"<tr>{lead}<th{'' if lead else ' colspan=2'}>{lab}</th>{cells}</tr>"
    return (f'<table class="cb"><thead><tr><th class="corner" colspan="2" rowspan="2">Item</th>{th1}</tr><tr>{th2}</tr></thead>'
            f"<tbody>{body}</tbody></table>")


def grp(label, n):
    return f'<td class="grp" rowspan="{n}">{label}</td>'


def cost_page(b, model, no, powers, rows, oxy_note=True):
    body = (title(f"{no:02d} · Cost-benefit analysis", f"Cost-benefit analysis · {model}")
            + P("If the cutting auxiliary gas is dried compressed air, the cost includes the air compressor's electricity, the machine's power "
                "consumption and the consumables (protective lenses, cutting nozzles).", cls="sm")
            + cost_rows_table(powers, rows)
            + notes(["The electricity and gas prices are Senfeng's reference values in China (RMB) and may vary by region.",
                     "Auxiliary gas consumption varies with plate thickness." + (" The oxygen data is based on cutting 0.315″ (8 mm) carbon steel "
                                                                                 "and nitrogen on 0.039″ (1 mm) stainless steel; for reference only, "
                                                                                 "actual usage may vary." if oxy_note else "")])
            + D.included())
    b.page("Cost-benefit analysis", body, key="cost")


PRECAUTIONS = [
    "Pipes being processed should be free from significant rust, as it can affect the cutting section quality.",
    "Pipes should not be stored in the open air and should be placed flat, preferably with a surface oil coating or packaging. Ensure that "
    "the front end is even and the burr height at both ends is ≤0.20″ (5 mm). Bundled pipes should have consistent lengths, with a deviation "
    "of less than 11.8″ (300 mm).",
    "For welded pipes, the external weld seam should be relatively flat, with a height of less than 0.012″ (0.3 mm). The internal weld seam "
    "should have a height of less than 0.08″ (2 mm).",
    "The distortion and bending of the pipe should be lower than the tolerances specified in “GB/T 6728-2002 Dimensions, Shape, Weight, and "
    "Permissible Deviations of Cold-formed Hollow Sections for Structural Use.”",
    "The pipe should be straight, with a bending curvature of less than 0.012″ per ft (1 mm/1 m; 3 mm over 6 m).",
    "For the lengthwise torsion of the pipe, the total torsion should be less than 0.02 % of the total length.",
    "The outer diameter tolerance of the profile should not exceed ±0.5 % of the outer diameter, with a minimum of 0.008″ (0.2 mm) "
    "(according to the standard deviation level D4 specified in GB/T 17395-1998 for standardized outer diameter deviations).",
    "When loading the pipes, ensure the safety of personnel and equipment. Bundle loading should be carried out using cranes operated by "
    "qualified and certified professionals. The crane should have both fast and slow speed functions, and slow speed should be used when "
    "approaching the loading platform.",
    "Considering material errors, the positional error should be within IT12, and the shape and profile error should be within IT12.",
    "The surface roughness of the pipe cross-section varies with the material and thickness.",
    "Users must perform regular maintenance of the machine as instructed in the manual. Failure to do so may result in damage to the "
    "machine, and the manufacturer reserves the right to refuse repairs in such cases.",
    "To ensure cutting effectiveness and minimize pipe deformation, the pipe wall thickness should meet the following criteria based on the "
    "pipe diameter:<ol><li>For pipe diameters greater than Ø2″ (Ø50 mm): 1/40 ≤ wall thickness ≤ 1/10 of the pipe diameter.</li>"
    "<li>For pipe diameters smaller than Ø2″ (Ø50 mm): 0.031″ (0.8 mm) ≤ wall thickness ≤ 1/10 of the pipe diameter.</li>"
    "<li>Where the bending deflection exceeds the relevant standards, the cutting quality cannot be guaranteed.</li></ol>",
    "Equipment temperature requirements: 32 – 104 °F (0 – 40 °C) (if the ambient temperature at the installation site exceeds this range, "
    "the buyer shall give written notice to the supplier at the time of purchase); the laser source should be placed in an environment of "
    "64 – 77 °F (18 – 25 °C). If the ambient temperature at the installation site exceeds this range, air conditioning is recommended.",
    "Equipment humidity requirements: ≤70 % (laser source only).",
    "Cutting gas purity requirements: nitrogen ≥99.7 %; oxygen ≥99.5 %."]


def precautions_page(b, model, no):
    body = (title(f"{no:02d} · Technical parameters", f"Precautions · {model}")
            + f'<ul class="pre">{"".join(f"<li>{x}</li>" for x in PRECAUTIONS)}</ul>')
    b.page("Precautions", body, key="pre")


def clamp_page(b, model, no, prefix, rows, note):
    """rows: (type, drawing index or None, html)"""
    trs = ""
    for t, d, x in rows:
        im = f'<img src="{D.im(T + f"{prefix}-draw-{d}.jpg", 400)}">' if d else ""
        trs += f'<tr><th>{t}</th><td class="d">{im}</td><td>{x}</td></tr>'
    body = (title(f"{no:02d} · Cutting parameters", f"Clamping range · {model}")
            + f'<table class="clamp"><thead><tr><th>Type</th><th>Cross-section</th><th>Clamping range</th></tr></thead><tbody>{trs}</tbody></table>'
            + P(note, cls="note"))
    b.page("Clamping range", body, key="clamp")


def unit_box(img, name, sub, rows, text=""):
    t = "".join(f"<tr><th>{a}</th><td>{v}</td></tr>" for a, v in rows)
    return (f'<div><div class="ut">{name}<small>{sub}</small></div>'
            + (f'<div class="ui"><img src="{D.im(T + img, 1000)}"></div>' if img else "")
            + (f"<table><tbody>{t}</tbody></table>" if rows else "") + (P(text, cls="xs") if text else "") + "</div>")


def model_page(b, model, line, image, campus, feats, slogan="Versatile &amp; efficient"):
    body = (title(f"01 · Model · {line}", model)
            + P(slogan, cls="sm")
            + row(fig(T + image, h=250, px=1800), fig(T + campus, "Senfeng's campus in Jinan, China", h=250, px=900), cols="1.7fr 1fr", gap=14)
            + '<div class="feat">' + "".join(f"<div><b>{i}</b>{t}</div>" for i, t in enumerate(feats, 1)) + "</div>"
            + P("*The picture is for reference; the actual appearance and size shall prevail.", cls="note")
            + D.included())
    b.page("Model", body, key="model")


def finish(b, model, kw, prefix_cust="tcust-", toc=None):
    H.after_sales(b, toc["after"], prefix_cust and ("../senfeng-tube-spec/" + prefix_cust))
    b.back("Tube laser for your shop.", [T + f"{b.pfx}-machine.jpg", T + f"{b.pfx}-chuck1.jpg", T + f"{b.pfx}-head1.jpg", T + f"{b.pfx}-cnc.jpg"])
    H.toc_page(b, toc["items"] + [(f"{toc['after']:02d} · Automated metal fabrication solutions", "solutions"),
                                  (f"{toc['after'] + 1:02d} · Personnel training, packaging and transportation", "training"),
                                  (f"{toc['after'] + 2:02d} · Installation and customization", "custom"),
                                  (f"{toc['after'] + 3:02d} · Five-star fast service", "service"),
                                  (f"{toc['after'] + 4:02d} · Customer testimonials", "cust")],
               f"Full technical specification · {model} · {kw}")


def new_book(pfx, model, line, kw, out, stats):
    b = D.Book("sf-" + pfx, f"{model} tube laser — full technical specification", f"Senfeng · {line} · {kw}",
               os.path.join(ROOT, "src", "files", out))
    b.pfx = pfx
    b.title = f"Senfeng {model} Tube Laser — Full Technical Specification — NovoTech Machine Tools"
    b.subject = f"Senfeng {model} {line}, {kw} — full technical specification, imperial edition"
    b.cover("Senfeng · full technical specification", f"{model} · {line} · {kw}", model, "Technical specification", line.capitalize(),
            T + f"{pfx}-machine.jpg", stats, hero_h=300, minis=[T + f"{pfx}-chuck1.jpg", T + f"{pfx}-head1.jpg", T + f"{pfx}-cnc.jpg"])
    b.page("Contents", "@@TOC@@", sub="Contents")
    return b


def host_bed_support(b, model, no, bed_text, support_title, support_text, cap_title, cap_text, dyn_title, dyn_text, imgs):
    cards1 = [card(T + imgs[0], "1 · Machine bed", '<div class="hl">Stability, vibration reduction and durability</div>' + ol(bed_text), h=96),
              card(T + imgs[1], f"2 · {support_title[0]}", f'<div class="hl">{support_title[1]}</div>' + ol(support_text), h=96)]
    cards2 = [card(T + imgs[2], f"3 · {cap_title[0]}", f'<div class="hl">{cap_title[1]}</div>' + ol(cap_text), h=72),
              card(T + imgs[3], f"4 · {dyn_title[0]}", f'<div class="hl">{dyn_title[1]}</div>' + P(dyn_text, cls="sm"), h=72)]
    body = title(f"{no:02d} · Host machine", f"{model} host machine") + grid(cards1, 2, 18) + '<div style="height:8pt"></div>' + grid(cards2, 2, 18)
    b.page("Host machine", body, key="host")


BED = ["The machine bed is welded from rectangular tubes, giving greater stability, a higher load-bearing capacity, significantly better "
       "vibration damping and better operational performance.",
       "The design is based on structural dynamic principles and variable analysis with the finite element method (FEM). After precise "
       "welding, the bed undergoes stress-relief annealing and secondary aging treatment, followed by precision machining on a large gantry "
       "milling machine — high rigidity and a long service life."]
T_CNC_COMMON = [
    "Real-time tube center deviation compensation reduces clamping requirements and improves efficiency, ensuring higher piercing accuracy "
    "and more precise cutting.",
    "Built on a real-time bus control system with integrated following control, it delivers faster corner cutting, smoother corner "
    "tracking and more reliable cutting quality.",
    "Supports the follow-up support function, ensuring consistent cutting quality for full-length tubes.",
    "Compatible with hollow chuck feeding and cutting, significantly reducing the overall machine length and enhancing automation.",
    "Supports automatic loading / unloading and cyclic processing, including standard automated feeding actions.",
    "Trajectory accuracy of 0.0008″ (0.02 mm), positioning accuracy of 0.00004″ (0.001 mm) and repeatability of 0.0001″ (0.003 mm).",
    "Supports real-time encoder feedback and error measurement tools to help optimize the machine's motion parameters.",
    "Supports a tube process library for convenient export and storage of cutting processes."]
LOADER_TEXT = ("1. Equipped with an automatic sorting system that separates scrap from finished tubes without manual intervention. The "
               "receiving cart and unloading rack have an integrated design — high system integration and a compact footprint.<br>"
               "2. A self-developed servo-following support system automatically adjusts to the tube surface, ensuring optimal support "
               "during processing. After processing, the flip plate discharges the finished tubes, which slide into the finished product cart.")


# ============================================================================================================ SF6012T
def book_t12():
    m, p = "SF6012T", "t12"
    b = new_book(p, m, "tube laser cutting machine (follow-up support)", "1.5 – 3 kW",
                 "NovoTech-Senfeng-SF6012T-Tube-Laser-Technical-Specification-2026.pdf",
                 [("Ø0.6 – 4.7″", "Round tube"), ("3.3 – 21.3 ft", "Tube length"), ("492 ft/min", "Rapid traverse"), ("1.5 G", "Acceleration")])
    model_page(b, m, "tube laser cutting machine (follow-up support)", f"{p}-model.jpg", f"{p}-campus.jpg",
               ["Superior cutting stability", "Powerful dynamic performance", "Automated system for greater efficiency", "Pneumatic self-centering chuck"])
    rows = [("Tube length range", ft_mm(1000, 6500), ""), ("Tube diameter range", dia(15, 120), "National standard tube"),
            ("Side length of square tube", "□" + sq(15, 120), "National standard tube"), ("X / Y axis positioning accuracy", "±0.002″ (±0.05 mm)", ""),
            ("X / Y axis repeated positioning accuracy", "±0.001″ (±0.03 mm)", ""),
            ("Maximum rapid traverse speed", ftmin(150), "As tube weight increases, processing speed and moving parameters decrease."),
            ("Maximum chuck rotation speed", "180 rpm", ""), ("Maximum acceleration", "1.5 G", ""), ("Weight", lb(2500), "Depends on actual factory delivery"),
            ("Maximum load", lb(120), "Tube weight ≤13.4 lb/ft (20 kg/m)"), ("Dimensions (L × W × H)", dims_ft(9100, 1800, 2100), "Depends on actual factory delivery"),
            ("Phase", "Three-phase", ""), ("Rated supply voltage", "380 V" + VOLT, ""), ("Frequency", "50 / 60 Hz", ""), ("Main power protection level", "IP54", "")]
    tech_notes = ["The achievable workpiece accuracy partly depends on factors such as the workpiece type, pretreatment condition, size and position.",
                  "The technical parameters above are subject to change without prior notice. The final technical parameters shall be as specified in the actual order agreement."]
    b.page("Technical parameters", title("02 · Technical parameters", f"Technical parameters · {m}") + tech_table(rows) + notes(tech_notes) + D.included(), key="tech")
    precautions_page(b, m, 3)
    clamp = [("Round tube", 1, f"{dia(10, 120)}<br><small>★ Ø10 – Ø120 mm</small>"), ("Square tube", 2, f"a: {sq(10, 120)}<br><small>★ □10 × 10 – □120 × 120 mm</small>"),
             ("Rectangular tube", 3, f"a: {sq(10, 120)} · b: {sq(10, 120)}<br><small>★ □10 × 10 – □120 × 120 mm</small>"),
             ("Oval tube", 4, "For a better clamping effect, please provide a detailed drawing so the jaws can be designed accordingly."),
             ("I-beam", 5, f"a: {sq(10, 80)} · b: {sq(10, 80)}<br><small>The minimum size, No. 10 to the GB standard, cannot be clamped.</small>"),
             ("U-beam (channel)", 6, f"a: {sq(10, 80)} · b: {sq(10, 80)}<br><small>GB No. 5 – 8</small>"), ("H-beam", 7, f"a: {sq(10, 80)} · b: {sq(10, 80)}"),
             ("Equal angle steel", 8, f"a: {sq(20, 80)}<br><small>GB No. 2.5 – 8</small>"),
             ("Unequal angle steel", 9, f"a: {sq(10, 80)} · b: {sq(20, 80)}<br><small>GB No. 2.5/1.6 – 8/5</small>")]
    clamp_page(b, m, 4, p, clamp, "To ensure better machining accuracy, the tube diameter must be ≥0.6″ (15 mm).")
    cut_pages(b, m, 5, T_CUT_NOTES)
    cost_page(b, m, 6, ["1.5 kW", "2 kW", "3 kW"],
              [("Laser source (kW)", [5, 5, 10], True, grp("Peak power consumption", 6)), ("Chiller (kW)", [3, 3, 3], True, " "),
               ("Air compressor (kW)", ["15", "/", "/"] * 3, False, " "), ("Host (kW)", ["10.45"] * 9, False, " "),
               ("Dust removal (kW)", ["1.5"] * 9, False, " "), ("Loading &amp; unloading (kW)", ["3.85"] * 9, False, " "),
               ("Consumables and gas consumption (CNY/h)", ["0.5", "4.5", "60.5"] * 3), ("Total power (kW)", [38.8, 23.8, 23.8, 38.8, 23.8, 23.8, 43.8, 28.8, 28.8]),
               ("Total power consumption (kWh per hour)", [23.28, 14.28, 14.28, 23.28, 14.28, 14.28, 26.28, 17.28, 17.28]),
               ("Total operating cost (RMB per hour, at 1 RMB/kWh)", [23.78, 18.78, 74.78, 23.78, 18.78, 74.78, 26.78, 21.78, 77.78])])
    conf = [("Laser source", [(1, "Fiber laser source", 1, "MAX")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "SENFENG TYRFING (optional BOCI auto-focus)")]),
            ("Machine tool · host", [(1, "Transmission system", 8, "SENFENG"), (2, "Machine tool and accessories", 1, "SENFENG"),
                                     (3, "Reducer", 6, "TECHMECH / MOTOREDUCER"), (4, "Cutting gas circuit system", 1, "AVENTICS (Germany)"),
                                     (5, "Main machine air circuit system", 1, "AIRTAC (Taiwan, China)"), (6, "AC servo motor and driver", 8, "SCHNEIDER (France) / INOVANCE"),
                                     (7, "Water chiller", 1, "HANLI")]),
            ("CNC cutting software system", [(1, "CNC system", 1, "FSCUT 3000DE-A"), (2, "Nesting software", 1, "Small-tube version of TubesT nesting software (free, no USB dongle required)")]),
            ("Automation system (optional)", [(1, "Loading system", 1, "Fully automatic / simplified fully automatic / semi-automatic (three options available)"),
                                              (2, "Unloading system", 1, "Standard: 6.6 ft (2 m) · optional: 10 ft (3 m) / 13 ft (4 m)")])]
    b.page("Configuration", title("07 · Configuration list", f"Configuration list · {m}") + H.conf_table(conf, CONF_NOTES), key="config")
    body = (title("08 · Core components", "Laser source · laser head")
            + h2(f"{m} laser source") + row(row(fig(T + f"{p}-src1.jpg", h=92, px=900), fig(T + f"{p}-src2.jpg", h=92, px=900), gap=10),
                                            ol(["High-quality laser output", "High power and high efficiency", "High reliability and long service life",
                                                "Compact and robust packaging", "Expandable programming interface"]), cols="1.3fr 1fr", gap=16, align="center")
            + h2(f"{m} laser head")
            + row(fig(T + f"{p}-head1.jpg", "SENFENG TYRFING cutting head (standard)", h=150, px=600),
                  ol(["<b>Efficient water cooling:</b> effectively resolves overheating issues.", "<b>High sealing:</b> dust protection rating of IP65.",
                      "<b>Optimized structure:</b> integrated body design.", "<b>Manual focus adjustment:</b> flexible focus scale adjustment for a uniform zero-focus position."]),
                  cols="0.7fr 1.3fr", gap=16, align="center")
            + row(fig(T + f"{p}-head2.jpg", "BOCI cutting head (optional)", h=150, px=600),
                  ol(["Closed-loop system with active feedback alarms for precise issue detection.",
                      "Protective lens temperature monitoring detects contamination during operation and triggers immediate alarms to stop the machine, preventing damage such as head burning or lens breakage.",
                      "Monitors cutting gas pressure in real time, triggering alarms for insufficient gas supply, low pressure or unstable pressure.",
                      "The anti-collision design of the cutting head enables easy replacement of components after an impact, reducing downtime.",
                      "This cutting head supports an upgrade to an automatic focusing system."]), cols="0.7fr 1.3fr", gap=16, align="center"))
    b.page("Laser source · head", body, key="source")
    body = (title("09 · Core components", f"{m} chuck") + row(fig(T + f"{p}-chuck1.jpg", h=260, px=900), fig(T + f"{p}-chuck2.jpg", h=200, px=1100), cols="0.9fr 1.1fr", gap=14, align="center")
            + ol(["<b>Pneumatic self-centering chuck:</b> fast clamping speed, high efficiency.", "<b>Low chuck inertia:</b> high speed and acceleration.",
                  "<b>Front chuck with double rollers:</b> increases the clamping surface, reduces vibration and ensures high-speed, high-precision cutting of small, low-rigidity pipes.",
                  "<b>Internal gears, external jaws:</b> better dust-proof performance, longer lifespan, higher precision, and easier adjustment and maintenance.",
                  "<b>Integrated chuck structure:</b> high-precision rotary bearings inside give higher equipment stability.",
                  "<b>Front chuck with a square-hole structure:</b> a larger clamping range and wider application in various industries."]) + D.included())
    b.page("Chuck", body, key="chuck")
    host_bed_support(b, m, 10, BED, ("Follow-up support", "Provides effective support for the tube"),
                     ["Servo control automatically adjusts the tube center to stay coaxial with the chuck center, ensuring constant contact with the tube surface and more precise lifting movements.",
                      "The intelligent segmented layout solves tube sagging, which reduces machining accuracy on long tubes."],
                     ("Exceptional tube processing capability", "Wide size range &amp; high single-tube load capacity"),
                     ["<b>Size range:</b> round tubes of Ø0.6 – 4.7″ (Ø15 – 120 mm); square tubes of 0.6 × 0.6 – 4.7 × 4.7″ (15 × 15 – 120 × 120 mm).",
                      "<b>Supported shapes:</b> round, square and rectangular tubes.", "<b>High single-tube load:</b> each tube can weigh up to 265 lb (120 kg), outstanding value in tube cutting."],
                     ("Powerful dynamic performance", "Ultra-high precision"),
                     "The all-new tube laser cutting machine combines exceptional performance with ultra-high precision, fully meeting the stringent requirements of the tube cutting industry.",
                     [f"{p}-bed.jpg", f"{p}-support.jpg", f"{p}-profiles.jpg", f"{p}-tubes.jpg"])
    cnc = T_CNC_COMMON + ["Enables sensorless piercing for smoother operation and greatly improved piercing efficiency.",
                          "Compatible with TubePro and TubesT nesting software (free download available).",
                          "Supports processing of special-shaped tubes within Ø4.7″ (120 mm) (excluding L-, C- and H-shaped profiles).",
                          "Compatible with manual-focus cutting heads, with an optional BOCI cutting head that allows a free upgrade to an auto-focus system."]
    body = (title("11 · CNC system", "FSCUT3000DE-A CNC system") + fig(T + f"{p}-cnc.jpg", "Quick operation &amp; efficient cutting", h=150, px=1400)
            + P("FSCUT3000DE-A is a bus control system specifically developed for processing small tubes with diameters up to 4.7″ (120 mm). It "
                "supports high-precision, high-efficiency cutting of square, round, racetrack-shaped, elliptical and other special-shaped tubes "
                "(excluding L-, C- and H-shaped profiles). Its key performance features are as follows:", cls="sm") + ul(cnc))
    b.page("CNC system", body, key="cnc")
    units = [unit_box(f"{p}-opt1.jpg", "1 · 6.6 ft (2 m) unloading unit", "optional", [("Dimensions", "76.8 × 41.7 × 30.3″ (1,950 × 1,060 × 770 mm)"),
                                                                                         ("Maximum tube length", "9.8 ft (3,000 mm)"), ("Unloading weight", lb(300))]),
             unit_box(f"{p}-opt2.jpg", "2 · Inclined semi-automatic loading unit", "optional", [("Minimum loading tube length", "17.1 ft (5,200 mm)"),
                                                                                                 ("Maximum loading tube length", "20.3 ft (6,200 mm)"),
                                                                                                 ("Tube section side length (or diameter)", "0.8 × 0.8 – 4.7 × 4.7″ (20 × 20 – 120 × 120 mm); Ø0.6 – 4.7″ (Ø15 – 120 mm)"),
                                                                                                 ("Maximum single tube weight", lb(120)), ("Tube type", "Round, square and rectangular tube, channel steel")]),
             unit_box(f"{p}-opt3.jpg", "3 · Fully automatic loading unit", "optional", [("Loading tube length", "11.5 – 20 ft (3,500 – 6,100 mm)"),
                                                                                        ("Tube section side length (or diameter)", "0.8 × 0.8 – 4.7 × 4.7″ (20 × 20 – 120 × 120 mm); Ø0.8 – 4.7″ (Ø20 – 120 mm)"),
                                                                                        ("Maximum single tube weight", lb(120)), ("Warehouse weight capacity", "6,614 lb (3 t)"), ("Tube type", "Round tube, square tube")]),
             unit_box(f"{p}-opt4.jpg", "4 · Simplified fully automatic loading unit", "optional", [("Loading tube length", "11.5 – 20 ft (3,500 – 6,100 mm)"),
                                                                                                  ("Tube section side length (or diameter)", "0.8 × 0.8 – 4.7 × 4.7″ (20 × 20 – 120 × 120 mm); Ø0.8 – 4.7″ (Ø20 – 120 mm)"),
                                                                                                  ("Maximum single tube weight", lb(120)), ("Warehouse weight capacity", "6,614 lb (3 t)"), ("Tube type", "Round tube, square tube")])]
    body = title("12 · Optional configuration", f"{m} optional configuration") + f'<div class="u4">{"".join(units)}</div>' + P(LOADER_TEXT, cls="xs")
    b.page("Optional configuration", body, key="opt")
    finish(b, m, "1.5 – 3 kW", toc={"after": 13, "items": [
        ("01 · Model", "model"), ("02 · Technical parameters", "tech"), ("03 · Precautions", "pre"), ("04 · Clamping range", "clamp"),
        ("05 · Cutting parameters", "cut1"), ("05 · Cutting parameters — stainless steel, aluminum alloy", "cut2"), ("06 · Cost-benefit analysis", "cost"),
        ("07 · Configuration list", "config"), ("08 · Laser source, laser head", "source"), ("09 · Chuck", "chuck"), ("10 · Host machine", "host"),
        ("11 · CNC system", "cnc"), ("12 · Optional configuration", "opt")]})
    return b


# ============================================================================================================ SF6024T
def book_t24():
    m, p = "SF6024T", "t24"
    b = new_book(p, m, "tube laser cutting machine (follow-up support)", "1.5 – 6 kW",
                 "NovoTech-Senfeng-SF6024T-Tube-Laser-Technical-Specification-2026.pdf",
                 [("Ø0.8 – 9.1″", "Round tube"), ("6.6 – 21.3 ft", "Tube length"), ("328 ft/min", "Rapid traverse"), ("1 G", "Acceleration")])
    model_page(b, m, "tube laser cutting machine (follow-up support)", f"{p}-model.jpg", f"{p}-campus.jpg",
               ["Superior cutting stability", "Powerful dynamic performance", "Automated system for greater efficiency", "Pneumatic self-centering chuck"])
    rows = [("Tube length range", ft_mm(2000, 6500), ""), ("Tube diameter range", dia(20, 230), "National standard tube"),
            ("Side length of square tube", "□" + sq(20, 230), "National standard tube"), ("X / Y axis positioning accuracy", "±0.002″ (±0.05 mm)", ""),
            ("X / Y axis repeated positioning accuracy", "±0.001″ (±0.03 mm)", ""),
            ("Maximum rapid traverse speed", ftmin(100), "As tube weight increases, processing speed and moving parameters decrease."),
            ("Maximum chuck rotation speed", "100 rpm", ""), ("Maximum acceleration", "1.0 G", ""), ("Weight", lb(3150), "Depends on actual factory delivery"),
            ("Maximum load", lb(260), "Tube weight ≤28.9 lb/ft (43 kg/m)"), ("Dimensions (L × W × H)", dims_ft(9530, 1950, 2200), "Depends on actual factory delivery"),
            ("Phase", "Three-phase", ""), ("Rated supply voltage", "380 V" + VOLT, ""), ("Frequency", "50 Hz", ""), ("Main power protection level", "IP54", "")]
    tech_notes = ["The achievable workpiece accuracy partly depends on factors such as the workpiece type, pretreatment condition, size and position.",
                  "The technical parameters above are subject to change without prior notice. The final technical parameters shall be as specified in the actual order agreement."]
    b.page("Technical parameters", title("02 · Technical parameters", f"Technical parameters · {m}") + tech_table(rows) + notes(tech_notes) + D.included(), key="tech")
    precautions_page(b, m, 3)
    clamp = [("Round tube", 1, f"{dia(10, 230)}<br><small>Ø10 – Ø230 mm</small>"), ("Square tube", 2, f"a: {sq(10, 230)}<br><small>□10 × 10 – □230 × 230 mm</small>"),
             ("Rectangular tube", 3, f"a: {sq(10, 230)} · b: {sq(10, 230)}<br><small>□10 × 10 – □230 × 230 mm</small>"),
             ("Oval tube", 4, "For a better clamping effect, please provide a detailed drawing so the jaws can be designed accordingly."),
             ("I-beam", 5, f"min. a: {inch(10)}″ (10 mm) · max. b: {inch(200)}″ (200 mm)<br><small>Standard configuration: GB No. 10 – 20 · optional accessory: No. 22</small>"),
             ("U-beam (channel)", 6, f"min. a: {inch(10)}″ (10 mm) · max. b: {inch(180)}″ (180 mm)<br><small>Standard configuration: GB No. 5 – 20 · optional accessory: No. 22</small>"),
             ("H-beam", 7, f"a: {sq(10, 200)} · b: {sq(10, 200)}"),
             ("Equal angle steel", 8, f"a: {sq(10, 110)} · max. b: {inch(140)}″ (140 mm)<br><small>GB No. 2 – 11</small>"),
             ("Unequal angle steel", 9, f"a: {sq(10, 75)} · b: {sq(10, 150)} · max. c: {inch(155)}″ (155 mm)<br><small>GB No. 2.5/1.6 – 14/9</small>")]
    clamp_page(b, m, 4, p, clamp, "To ensure better machining accuracy, the tube diameter must be ≥0.8″ (20 mm).")
    cut_pages(b, m, 5, T_CUT_NOTES)
    cost_page(b, m, 7, ["3 kW", "4 kW", "6 kW"],
              [("Laser source (kW)", [10, 16, 16], True, grp("Peak power consumption", 6)), ("Chiller (kW)", [3, 6, 6], True, " "),
               ("Air compressor (kW)", ["15", "/", "/"] * 3, False, " "), ("Host (kW)", ["12.5"] * 9, False, " "),
               ("Dust removal (kW)", ["1.5"] * 9, False, " "), ("Loading &amp; unloading (kW)", ["3.85"] * 9, False, " "),
               ("Consumables and gas consumption (CNY/h)", ["0.5", "4.5", "60.5"] * 3), ("Total power (kW)", [45.85, 30.85, 30.85, 54.85, 39.85, 39.85, 54.85, 39.85, 39.85]),
               ("Total power consumption (kWh per hour)", [27.51, 18.51, 18.51, 32.91, 23.91, 23.91, 32.91, 23.91, 23.91]),
               ("Total operating cost (RMB per hour, at 1 RMB/kWh)", [28.01, 23.01, 79.01, 33.41, 28.41, 84.41, 33.41, 28.41, 84.41])])
    conf = [("Laser source", [(1, "Fiber laser source", 1, "Maxphotonics")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "Raytools")]),
            ("Machine tool · host", [(1, "Transmission system", 8, "SENFENG"), (2, "Machine tool and accessories", 1, "SENFENG"),
                                     (3, "Reducer", 6, "TECHMECH / MOTOREDUCER"), (4, "Cutting gas circuit system", 1, "AVENTICS (Germany)"),
                                     (5, "Main machine air circuit system", 1, "AIRTAC (Taiwan, China)"), (6, "AC servo motor and driver", 8, "SCHNEIDER (France) / INOVANCE"),
                                     (7, "Water chiller", 1, "HANLI")]),
            ("CNC cutting software system", [(1, "CNC system", 1, "FSCUT 3000DE-G"), (2, "Nesting software", 1, "TubesT professional nesting software")]),
            ("Automation system (optional)", [(1, "Loading system", 1, "Fully automatic / simplified fully automatic / semi-automatic (three options available)"),
                                              (2, "Unloading system", 1, "Standard: 6.6 ft (2 m) · optional: 10 ft (3 m) / 13 ft (4 m)")])]
    b.page("Configuration", title("08 · Configuration list", f"Configuration list · {m}") + H.conf_table(conf, CONF_NOTES), key="config")
    src = ["<b>Small fiber core:</b> better beam quality.", "<b>Faster cutting speed:</b> enhanced cutting efficiency.",
           "<b>Improved high-reflection resistance:</b> new optical components with a multi-layer anti-reflection design.",
           "<b>Enhanced intelligence:</b> real-time dynamic monitoring of operating indicators.",
           "<b>High electrical-optical conversion:</b> over 40 % efficiency, reducing power consumption.",
           "<b>Upgraded components:</b> new-generation pump sources offer greater reliability and stability, with improved beam quality and 30 – 40 % more brightness thanks to patented nonlinear suppression technology.",
           "<b>Lightweight and compact:</b> small size and compact design for easier integration.", "<b>Enhanced safety:</b> improved safety features."]
    src2 = ["<b>Small fiber core:</b> better beam quality.", "More efficient cutting of medium and thin plates.",
            "<b>Improved high-reflection resistance:</b> new optical components with a multi-layer anti-reflection design.",
            "<b>Enhanced intelligence:</b> real-time dynamic monitoring of operating indicators.",
            "<b>High electrical-optical conversion:</b> over 40 % efficiency, reducing power consumption.",
            "<b>Versatile applications:</b> the modulation frequency range is upgraded to 1 – 20 kHz, suitable for a wide variety of processes.",
            "<b>Lightweight and compact:</b> small size and compact design for easier integration.",
            "<b>High sealing performance:</b> sealing and reliability further improved, with the protection rating upgraded to IP66."]
    body = (title("09 · Core components", f"{m} laser source") + fig(T + f"{p}-src1.jpg", "MAX fiber laser source", h=120, px=1000)
            + row(h3("Laser source") + ol(src), h3("Laser source — medium and thin plate") + ol(src2), gap=16) + D.included())
    b.page("Laser source", body, key="source")
    body = (title("09 · Core components", f"{m} laser head")
            + row(row(fig(T + f"{p}-head1.jpg", "3 kW", h=120, px=600), fig(T + f"{p}-head2.jpg", "6 kW", h=120, px=600), gap=8),
                  ol(["<b>Optimized design:</b> an enhanced optical configuration and streamlined airflow design significantly improve cutting quality and efficiency.",
                      "<b>Auto-focusing:</b> minimizes human intervention, with a focusing accuracy of 0.002″ (0.05 mm).",
                      "<b>Multiple protective lenses:</b> the collimation module includes additional protective lenses that safeguard the collimating lens.",
                      "<b>Drawer-style lens holder:</b> quick and easy replacement of the protective lenses.",
                      "<b>High compatibility:</b> equipped with QBH and QD fiber interfaces."]), cols="1fr 1.2fr", gap=16, align="center")
            + h2("Optional BOCI cutting head")
            + row(fig(T + f"{p}-head3.jpg", "BOCI cutting head (optional)", h=130, px=600),
                  ol(["Closed-loop system with active feedback alarms for precise issue detection.",
                      "Protective lens temperature monitoring detects contamination during operation and triggers immediate alarms to stop the machine, preventing damage such as head burning or lens breakage.",
                      "Monitors cutting gas pressure in real time, triggering alarms for insufficient gas supply, low pressure or unstable pressure.",
                      "The anti-collision design of the cutting head enables easy replacement of components after an impact, reducing downtime."]),
                  cols="0.8fr 1.2fr", gap=16, align="center") + D.included())
    b.page("Laser head", body, key="head")
    body = (title("10 · Core components", f"{m} chuck") + row(fig(T + f"{p}-chuck1.jpg", h=250, px=900), fig(T + f"{p}-chuck2.jpg", h=190, px=1100), cols="0.95fr 1.05fr", gap=14, align="center")
            + ol(["<b>Pneumatic self-centering chuck:</b> fast clamping speed and high efficiency.",
                  "<b>Low-inertia chuck:</b> made of aerospace-grade aluminum — lightweight, low inertia, high rotation speed, lower power consumption and lower operating costs.",
                  "<b>Fully enclosed chuck protection:</b> keeps dust and debris out, ensuring smooth operation without stoppages.",
                  "<b>Internal gears and external jaws:</b> better dust resistance, longer lifespan, high precision, and easier adjustment and maintenance.",
                  "<b>Integrated chuck structure:</b> superior dust protection and greater machine stability.",
                  "<b>Square-opening front chuck:</b> expands the clamping range and broadens industry applications."]) + D.included())
    b.page("Chuck", body, key="chuck")
    host_bed_support(b, m, 11, BED, ("Follower support", "Effectively supports tubes"),
                     ["The segmented special reducing-wheel auxiliary support structure adapts to pipes of different diameters and shapes.",
                      "It effectively addresses the reduced processing accuracy caused by the sagging of long pipes."],
                     ("Exceptional tube processing capability", "Wide size range &amp; high single-tube load capacity"),
                     ["<b>Size range:</b> round tubes of Ø0.8 – 9.1″ (Ø20 – 230 mm); square tubes of 0.8 × 0.8 – 9.1 × 9.1″ (20 × 20 – 230 × 230 mm).",
                      "<b>Supported shapes:</b> round, square and rectangular tubes.", "<b>High single-tube load:</b> each tube can weigh up to 441 lb (200 kg), outstanding value in tube cutting."],
                     ("Powerful dynamic performance", "Ultra-high precision"),
                     "The all-new tube laser cutting machine combines exceptional performance with ultra-high precision, fully meeting the stringent requirements of the tube cutting industry.",
                     [f"{p}-bed.jpg", f"{p}-support.jpg", f"{p}-profiles.jpg", f"{p}-tubes.jpg"])
    cnc = T_CNC_COMMON + ["Supports seamless piercing, for smoother operation and significantly improved piercing efficiency.",
                          "Compatible with the TubePro cutting software and the professional version of the TubesT nesting software — it can process all types of tubes."]
    body = (title("12 · CNC system", "FSCUT3000DE-G CNC system") + fig(T + f"{p}-cnc.jpg", "Quick operation &amp; efficient cutting", h=150, px=1400)
            + P("FSCUT3000DE-G is a bus control system specifically developed for tube cutting. It supports high-precision, high-efficiency cutting "
                "of square tubes, round tubes, racetrack-shaped and oval tubes, as well as angle steel and channel steel. Its performance features "
                "are as follows:", cls="sm") + ul(cnc))
    b.page("CNC system", body, key="cnc")
    units = [unit_box(f"{p}-opt1.jpg", "1 · 6.6 ft (2 m) unloading unit", "optional", [("Dimensions", "76.8 × 41.7 × 30.3″ (1,950 × 1,060 × 770 mm)"),
                                                                                         ("Maximum tube length", "9.8 ft (3,000 mm)"), ("Unloading weight", lb(300))]),
             unit_box(f"{p}-opt2.jpg", "2 · Dual-arm chain-type semi-automatic loading unit", "optional", [("Minimum loading tube length", "13.1 ft (4,000 mm)"),
                                                                                                         ("Maximum loading tube length", "20 ft (6,100 mm)"),
                                                                                                         ("Tube section side length (or diameter)", "0.8 × 0.8 – 8.7 × 8.7″ (20 × 20 – 220 × 220 mm); Ø0.8 – 8.7″ (Ø20 – 220 mm)"),
                                                                                                         ("Maximum single tube weight", lb(240)), ("Tube type", "Round, square and rectangular tube, angle steel, channel steel, I-beams, etc.")]),
             unit_box(f"{p}-opt3.jpg", "3 · Fully automatic loading unit", "optional", [("Loading tube length", "11.5 – 20 ft (3,500 – 6,100 mm)"),
                                                                                        ("Tube section side length (or diameter)", "0.8 × 0.8 – 9.1 × 9.1″ (20 × 20 – 230 × 230 mm); Ø0.8 – 9.1″ (Ø20 – 230 mm)"),
                                                                                        ("Maximum single tube weight", lb(260)), ("Warehouse weight capacity", "6,614 lb (3 t)"), ("Tube type", "Round tube, square tube")]),
             unit_box(f"{p}-opt4.jpg", "4 · Simplified fully automatic loading unit", "optional", [("Loading tube length", "11.5 – 20 ft (3,500 – 6,100 mm)"),
                                                                                                  ("Tube section side length (or diameter)", "0.8 × 0.8 – 9.1 × 9.1″ (20 × 20 – 230 × 230 mm); Ø0.8 – 9.1″ (Ø20 – 230 mm)"),
                                                                                                  ("Maximum single tube weight", lb(260)), ("Warehouse weight capacity", "6,614 lb (3 t)"), ("Tube type", "Round tube, square tube")])]
    body = title("13 · Optional configuration", f"{m} optional configuration") + f'<div class="u4">{"".join(units)}</div>' + P(LOADER_TEXT, cls="xs")
    b.page("Optional configuration", body, key="opt")
    finish(b, m, "1.5 – 6 kW", toc={"after": 14, "items": [
        ("01 · Model", "model"), ("02 · Technical parameters", "tech"), ("03 · Precautions", "pre"), ("04 · Clamping range", "clamp"),
        ("05 · Cutting parameters — carbon steel", "cut1"), ("06 · Cutting parameters — stainless steel, aluminum alloy", "cut2"),
        ("07 · Cost-benefit analysis", "cost"), ("08 · Configuration list", "config"), ("09 · Laser source, laser head", "source"), ("10 · Chuck", "chuck"),
        ("11 · Host machine", "host"), ("12 · CNC system", "cnc"), ("13 · Optional configuration", "opt")]})
    return b


# ============================================================================================================ SF6024NT
def book_nt():
    m, p = "SF6024NT", "nt"
    line = "three-chuck tube laser cutting machine (horizontal)"
    b = new_book(p, m, line, "1.5 – 6 kW", "NovoTech-Senfeng-SF6024NT-Tube-Laser-Technical-Specification-2026.pdf",
                 [("Ø0.8 – 9.1″", "Round tube"), ("20 ft", "Tube length"), ("Zero tail", "Three chucks"), ("0.8 G", "Acceleration")])
    model_page(b, m, line, f"{p}-model.jpg", f"{p}-campus.jpg",
               ["Superior cutting stability", "Powerful dynamic performance", "Three-chuck zero-tail system", "Pneumatic self-centering chuck"])
    th = "".join(f"<th>{h}</th>" for h in ("No.", "Item", "Standard 3 m unloading system", "Optional 6 m unloading system", "Note"))
    rows = [("Tube length", "19.7 ft (6,000 mm)", None, ""), ("Tube unloading length", "9.8 ft (3,000 mm)", "19.7 ft (6,000 mm)", ""),
            ("Tube diameter", f"{dia(20, 230)}<br><small>bevel: Ø2 – 9.1″ (Ø50 – 230 mm)</small>", None, "National standard pipe"),
            ("Side length of square tube", f"{sq(20, 230)}<br><small>bevel: 2 – 9.1″ (50 – 230 mm)</small>", None, "National standard pipe"),
            ("X / Y axis positioning accuracy", "±0.002″ (±0.05 mm)", None, ""), ("X / Y axis repeated positioning accuracy", "±0.001″ (±0.03 mm)", None, ""),
            ("Maximum feeding speed", ftmin(75), None, "Processing speed, idle movement and other factors decrease as pipe weight increases."),
            ("Maximum chuck speed", "100 rpm", None, ""), ("Maximum acceleration", "0.8 G", None, ""),
            ("Dimensions", dims_ft(13800, 2750, 3150), dims_ft(16470, 2750, 3150), "Subject to actual factory delivery"),
            ("Weight", "About " + lb(7500), "About " + lb(8450), "Subject to actual factory delivery"),
            ("Maximum load of chuck", lb(260), None, "Air pressure 44 – 102 psi (0.3 – 0.7 MPa)"), ("Phase", "Three-phase", None, ""),
            ("Power supply rated voltage", "380 V" + VOLT, None, ""), ("Frequency", "50 Hz", None, ""), ("Power supply protection grade", "IP54", None, "")]
    trs = ""
    for i, (a, s, o, n) in enumerate(rows, 1):
        mid = f'<td colspan="2">{s}</td>' if o is None else f"<td>{s}</td><td>{o}</td>"
        trs += f"<tr><td class='n'>{i}</td><th>{a}</th>{mid}<td>{n}</td></tr>"
    body = (title("02 · Technical parameters", f"Technical parameters · {m}") + f'<table class="cf tight"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'
            + notes(["The achievable accuracy of the workpiece depends to some extent on factors such as workpiece type, surface, tube specifications and straightness.",
                     "The technical parameters above are subject to change without notice; the final technical parameters are subject to the order agreement."]) + D.included())
    b.page("Technical parameters", body, key="tech")
    precautions_page(b, m, 3)
    clamp = [("Round tube", 1, f"{dia(20, 230)}<br><small>Ø20 – Ø230 mm</small>"), ("Square tube", 2, f"a: {sq(20, 230)}<br><small>□20 × 20 – □230 × 230 mm</small>"),
             ("Rectangular tube", 3, f"a: {sq(20, 230)} · b: {sq(20, 230)}<br><small>□20 × 20 – □230 × 230 mm</small>"),
             ("Elliptical tube", 4, "Please send the specific dimension drawing."),
             ("I-beam", 5, f"min. a: {inch(20)}″ (20 mm) · max. b: {inch(200)}″ (200 mm)<br><small>Standard configuration: GB No. 20</small>"),
             ("Channel steel", 6, f"min. a: {inch(20)}″ (20 mm) · max. b: {inch(200)}″ (200 mm)<br><small>Standard configuration: GB No. 20</small>"),
             ("Angle steel", 7, f"Equal angle steel: a {sq(20, 110)} · max. b {inch(155)}″ (155 mm) — GB No. 11<br>Unequal angle steel: a {sq(20, 90)} · "
                                f"b {sq(20, 140)} · max. c {inch(166)}″ (166 mm) — GB No. 14/9")]
    clamp_page(b, m, 4, p, clamp, "For bevel laser tube cutting, the minimum clamping size for pipes is 2″ (50 mm).")
    cut_pages(b, m, 5, N_CUT_NOTES)
    std, opt = '<small style="display:block;font-weight:400;color:#6d6f73">standard 3 m unloading</small>', '<small style="display:block;font-weight:400;color:#6d6f73">optional 6 m unloading</small>'
    cost_page(b, m, 7, ["3 kW", "4 kW", "6 kW"],
              [("Laser source (kW)", [10, 16, 16], True, grp("Peak power consumption", 7)), ("Chiller (kW)", [3, 6, 6], True, " "),
               ("Air compressor (kW)", ["15", "/", "/"] * 3, False, " "), ("Host" + std, ["23.9"] * 9, False, " "), ("Host" + opt, ["25.2"] * 9, False, " "),
               ("Dust removal (kW)", ["1.5"] * 9, False, " "), ("Semi-automatic loading (kW)", ["3"] * 9, False, " "),
               ("Consumables and gas consumption (CNY/h)", ["0.5", "4.5", "60.5"] * 3),
               ("Total power (kW)" + std, [56.4, 41.4, 41.4, 65.4, 50.4, 50.4, 65.4, 50.4, 50.4]),
               ("Total power (kW)" + opt, [57.7, 42.7, 42.7, 66.7, 51.7, 51.7, 66.7, 51.7, 51.7]),
               ("Total power consumption (kWh per hour)" + std, [33.84, 24.84, 24.84, 39.24, 30.24, 30.24, 39.24, 30.24, 30.24]),
               ("Total power consumption (kWh per hour)" + opt, [34.62, 25.62, 25.62, 40.02, 31.02, 31.02, 40.02, 31.02, 31.02]),
               ("Total operating cost (RMB per hour, at 1 RMB/kWh)" + std, [34.34, 29.34, 85.34, 39.74, 34.74, 90.74, 39.74, 34.74, 90.74]),
               ("Total operating cost (RMB per hour, at 1 RMB/kWh)" + opt, [35.12, 30.12, 86.12, 40.52, 35.52, 91.52, 40.52, 35.52, 91.52])], oxy_note=False)
    conf = [("Laser source", [(1, "Laser source", 1, "Maxphotonics")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "BOCI (optional bevel cutting head)")]),
            ("Machine tool · host", [(1, "Transmission system", 13, "SENFENG"), (2, "Machine tool and accessories", 1, "SENFENG"), (3, "Reducer", 9, "TECHMECH"),
                                     (4, "Electrical and pneumatic systems", 1, "AVENTICS"), (5, "AC servo motor and driver", 13, "INOVANCE"), (6, "Water chiller", 1, "TONGFEI")]),
            ("CNC system", [(1, "CNC system", 1, "FSCUT 5000A")]),
            ("Automation system (optional)", [(1, "Loading system", 1, "Fully automatic / simplified fully automatic / semi-automatic (three options available)"),
                                              (2, "Unloading system", 1, "Standard: 10 ft (3 m) · optional: 20 ft (6 m)")])]
    b.page("Configuration", title("08 · Configuration list", f"Configuration list · {m}") + H.conf_table(conf, CONF_NOTES), key="config")
    body = (title("09 · Core components", f"{m} laser head")
            + row(row(fig(T + f"{p}-head1.jpg", "Standard cutting head", h=130, px=700), fig(T + f"{p}-head2.jpg", "Tapered cutting head", h=130, px=900), gap=8),
                  ol(["<b>Integrated cooling:</b> uniform heat dissipation across the whole module allows long continuous cutting and extends the lens life 1.5 to 2 times.",
                      "<b>High sealing:</b> integrated body design with a dust protection rating of IP68.", "<b>Easy maintenance:</b> the drawer-style design allows a lens change within three minutes.",
                      "<b>Standard cutting head:</b> for conventional tubes such as square and round tubes, angle irons, channel steels and other non-recessed profiles.",
                      "<b>Tapered cutting head:</b> processes tubes of any shape, including recessed profiles such as H-beams and I-beams."]), cols="1fr 1.1fr", gap=16, align="center")
            + h2("Optional bevel cutting head")
            + row(fig(T + f"{p}-head3.jpg", "Bevel cutting head (optional)", h=130, px=900),
                  ol(["Supports ±45° bevel cutting.", "Right-angle cutting head.", "Full optical temperature and gas leakage monitoring.",
                      "Anti-collision bracket that protects the fiber interface and cables.", "High-speed servo collimation and focusing."]), cols="0.9fr 1.1fr", gap=16, align="center")
            + D.included())
    b.page("Laser head", body, key="head")
    src = ["<b>Small fiber core:</b> better beam quality.", "<b>Faster cutting speed:</b> enhanced cutting efficiency.",
           "<b>Improved high-reflection resistance:</b> new optical components with a multi-layer anti-reflection design for efficient processing of various metals.",
           "<b>Enhanced intelligence:</b> next-generation software with a smart app mode for real-time monitoring.",
           "<b>High electrical-optical conversion:</b> over 40 % efficiency, reducing power consumption.",
           "<b>Upgraded components:</b> new-generation pump sources offer greater reliability and stability, with improved beam quality and 30 – 40 % more brightness thanks to patented nonlinear suppression technology.",
           "<b>Lightweight and compact:</b> small size and compact design for easier integration.", "<b>Enhanced safety:</b> improved safety features."]
    src2 = ["Smaller core diameter, better beam quality.", "More efficient cutting of thin and medium-thick plates.",
            "Next-generation optics with a multi-layer anti-reflection design for better high-reflectivity resistance.",
            "Smarter system with real-time dynamic monitoring of the operating parameters.", "Electro-optical conversion efficiency over 40 %.",
            "Modulation frequency range upgraded to 1 – 20 kHz, adaptable to diverse processes.", "Compact size and reduced weight for easier integration.",
            "Improved sealing and reliability with an upgraded IP66 protection rating."]
    body = (title("09 · Core components", f"{m} laser source") + fig(T + f"{p}-src1.jpg", "Fiber laser sources — standard and optional", h=110, px=1400)
            + row(h3("Laser source") + ol(src), h3("Laser source — optional") + ol(src2), gap=16) + D.included())
    b.page("Laser source", body, key="source")
    body = (title("10 · Core components", f"{m} chuck")
            + row(fig(T + f"{p}-chuck1.jpg", "Rear chuck", h=150, px=900), fig(T + f"{p}-chuck2.jpg", "Middle chuck", h=170, px=900),
                  fig(T + f"{p}-chuck3.jpg", "Front chuck", h=170, px=900), gap=12, align="center")
            + ol(["Fully enclosed, integrated gear transmission structure for better dust protection and operational stability.",
                  "Two-front, one-rear chuck structure with high clamping precision, strong stability and a long service life.",
                  "The two front full-stroke chucks reduce jaw changes and boost production efficiency.",
                  "The front chuck has a square-opening design, allowing a wider clamping range of square and rectangular tubes.",
                  "The rear chuck has an extended barrel-type design that can insert into the front chuck, giving shorter tail material."]) + D.included())
    b.page("Chuck", body, key="chuck")
    cards1 = [card(T + f"{p}-bed.jpg", "1 · Machine bed", ol(["The segmented bed has lifting rings on each section, reducing transportation costs.",
                                                              "The independently developed tube-welded bed offers better stability, a higher load capacity, stronger shock absorption and improved operational performance.",
                                                              "The bed is designed on structural dynamics principles and finite element variable analysis. After precision welding it undergoes stress-relief annealing, secondary aging treatment and high-precision machining on a large gantry milling machine — high rigidity and a long service life."]), h=88),
              card(T + f"{p}-support.jpg", "2 · Follow support", ol(["The servo-controlled system automatically aligns the tube center with the chuck center, ensuring constant surface contact with the tube.",
                                                                    "The intelligent segmented layout keeps long tubes from sagging, ensuring high processing accuracy."]), h=88)]
    unload = card(T + f"{p}-unload.jpg", "3 · Automatic unloading system", ol(["An automatic material separation system separates scrap and finished tubes without manual intervention.",
                                                                               "The servo control system automatically aligns the tube's center with the chuck's center, preventing sagging under gravity and ensuring high processing accuracy.",
                                                                               "After processing the plate flips automatically, so the finished tubes slide into the receiving rack."]), h=100)
    body = title("11 · Host machine", f"{m} host machine") + grid(cards1, 2, 18) + '<div style="height:8pt"></div>' + unload
    b.page("Host machine", body, key="host")
    body = (title("12 · Host machine", "Three-chuck structure")
            + row(fig(T + f"{p}-rear.jpg", "Rear chuck", h=90, px=800), fig(T + f"{p}-front1.jpg", "Middle chuck", h=100, px=800), fig(T + f"{p}-front2.jpg", "Front chuck", h=100, px=800), gap=12, align="center")
            + h2("4 · Three-chuck structure")
            + ol(["The standard configuration is a 1 rear + 2 front chuck structure, with automatic unloading of tubes up to 9.8 ft (3 m). Tubes longer than 9.8 ft (3 m) are unloaded by hand (which needs additional space), so workpieces of varying lengths can be processed.",
                  "It cuts with zero tail material, improving material utilization and saving costs.",
                  "All three chucks are movable. The rear chuck can pull and support the material, helping to correct workpiece deformation and improving accuracy and stability for very long or small workpieces.",
                  "Innovative “seven-axis material pulling” dynamic cutting, with the front hollow clamping chuck, makes the most of the raw material."])
            + h2("5 · Powerful tube processing capability")
            + row(ol(["<b>Size:</b> round tube Ø0.8 – 9.1″ (Ø20 – 230 mm); square tube 0.8 × 0.8 – 9.1 × 9.1″ (20 × 20 – 230 × 230 mm).",
                      "<b>Pipe type:</b> round, square, rectangular and elliptical tube, angle steel, channel steel, I-beam, H-beam, etc.",
                      "<b>Single tube load-bearing capacity:</b> 573 lb (260 kg)."]), fig(T + f"{p}-tubes.jpg", h=90, px=1200), cols="1.2fr 1fr", gap=14, align="center"))
    b.page("Three-chuck structure", body, key="three")
    cnc = ["Real-time compensation of the pipe center deviation reduces pipe clamping requirements and is more efficient; piercing accuracy is higher and cutting more accurate.",
           "Based on the bus real-time system and integrated follow-up control, pipe corner cutting is faster, corner following more stable and cutting quality more reliable.",
           "Supports the support-bracket follow-up function, ensuring the cutting quality of the whole pipe.",
           "Supports hollow chuck feeding and cutting, greatly shortening the total length of the bed, with a high degree of automation.",
           "Supports three-chuck pulling cutting, ensuring the cutting accuracy of long parts and zero-tail cutting.",
           "Supports automatic loading and unloading and cycle processing, and the standard automatic feeding action.",
           "Supports the chuck avoidance / cutting head avoidance function for processing shorter tails.", "Supports the groove (bevel) processing function (optional).",
           "Supports the chuck anti-burning function, which solves chuck burning caused by grooving.", "Supports special-shaped steel cutting — a more powerful function.",
           "Track accuracy 0.0008″ (0.02 mm), positioning accuracy 0.00004″ (0.001 mm), repeat positioning accuracy 0.0001″ (0.003 mm).",
           "Supports real-time encoder feedback, with error measurement tools that help find the best motion parameters of the machine."]
    body = (title("13 · CNC system", "FSCUT5000A CNC system") + fig(T + f"{p}-cnc.jpg", h=130, px=1400)
            + P("FSCUT5000A is a bus control system specially developed for pipe processing and suitable for four-chuck pipe cutting. It supports "
                "high-precision, high-efficiency cutting of square, round, runway-shaped and oval stretched pipes, as well as angle steels, channel "
                "steels, I-beams and other special-shaped steels. Its main performance features are as follows:", cls="sm") + ul(cnc))
    b.page("CNC system", body, key="cnc")
    soft = ["Automatically supports editing the paths of special-shaped steel such as angle steel, channel steel, I-beam and H-beam for high-quality cutting.",
            "Centering function with real-time deviation compensation of the tube center.", "Built-in drawing function: fast drawing, and standard parts imported in batches.",
            "Common-edge nesting reduces the number of cuts — higher cutting efficiency and extreme material saving.",
            "A separate corner process can be set to improve the quality of pipe corner cutting.",
            "The Z axis also takes part in interpolation — 80 % control + 20 % follow-up, climbing and downhill — so the Z axis is no longer the weak link and corners are cut faster.",
            "Fast “frog jump”: intelligent judgment of the lifting height on a face change shortens empty moves in all directions and improves cutting efficiency.",
            "Weld compensation automatically avoids the convex corners of vertical cutting, for interference-free splicing and easy intersecting welding.",
            "A simple interface, convenient operation, easy to learn, with a high degree of intelligence.", "Supports multiple formats such as IGS / SAT / JHB."]
    body = (title("14 · CNC system", "TubePro cutting software + TubesT nesting software") + fig(T + f"{p}-soft.jpg", h=130, px=1400) + ul(soft) + D.included())
    b.page("Software", body, key="soft")
    units = [unit_box(f"{p}-opt1.jpg", "1 · Semi-automatic loading system", "optional", [("Minimum loading tube length", "13.1 ft (4,000 mm)"),
                                                                                         ("Maximum loading tube length", "19.7 ft (6,000 mm)"),
                                                                                         ("Tube section side length (or diameter)", "0.8 × 0.8 – 8.7 × 8.7″ (20 × 20 – 220 × 220 mm); Ø0.8 – 8.7″ (Ø20 – 220 mm)"),
                                                                                         ("Maximum single tube weight", lb(240)), ("Tube type", "Round, square and rectangular tube, angle steel, channel steel, I-beam, etc.")],
                      "After placing tubes on the rack, arrange them neatly by hand; tubes beyond the specified size or weight are loaded by hand."),
             unit_box(f"{p}-opt2.jpg", "2 · Fully automatic loading system", "optional", [("Loading tube length", "11.5 – 19.7 ft (3,500 – 6,000 mm)"),
                                                                                         ("Tube section side length (or diameter)", "0.8 × 0.8 – 9.4 × 9.1″ (20 × 20 – 240 × 230 mm); Ø0.8 – 9.1″ (Ø20 – 230 mm)"),
                                                                                         ("Maximum single tube weight", lb(260)), ("Warehouse weight capacity", "6,614 lb (3 t)"), ("Tube type", "Round tube, square tube")]),
             unit_box(f"{p}-opt3.jpg", "3 · Simple automatic loading system", "optional", [("Loading tube length", "11.5 – 19.7 ft (3,500 – 6,000 mm)"),
                                                                                          ("Tube section side length (or diameter)", "0.8 × 0.8 – 9.1 × 9.1″ (20 × 20 – 230 × 230 mm); Ø0.8 – 9.1″ (Ø20 – 230 mm)"),
                                                                                          ("Maximum single tube weight", lb(260)), ("Warehouse weight capacity", "6,614 lb (3 t)"), ("Tube type", "Round tube, square tube")])]
    body = title("15 · Optional configuration", f"{m} optional units") + f'<div class="u4">{"".join(units)}</div>'
    b.page("Optional units", body, key="opt")
    finish(b, m, "1.5 – 6 kW", prefix_cust="tcust-", toc={"after": 16, "items": [
        ("01 · Model", "model"), ("02 · Technical parameters", "tech"), ("03 · Precautions", "pre"), ("04 · Clamping range", "clamp"),
        ("05 · Cutting parameters — carbon steel", "cut1"), ("06 · Cutting parameters — stainless steel, aluminum alloy", "cut2"),
        ("07 · Cost-benefit analysis", "cost"), ("08 · Configuration list", "config"), ("09 · Laser head, laser source", "head"), ("10 · Chuck", "chuck"),
        ("11 · Host machine", "host"), ("12 · Three-chuck structure", "three"), ("13 · CNC system", "cnc"), ("14 · TubePro and TubesT software", "soft"),
        ("15 · Optional units", "opt")]})
    return b


# ============================================================================================================ SF6012PLUS
def book_plus():
    m, p = "SF6012PLUS", "plus"
    line = "laser tube cutting machine"
    b = new_book(p, m, line, "3 – 6 kW", "NovoTech-Senfeng-SF6012PLUS-Tube-Laser-Technical-Specification-2026.pdf",
                 [("Ø0.4 – 4.7″", "Round tube"), ("3.3 – 21.3 ft", "Tube length"), ("240 rpm", "Chuck speed"), ("1.5 G", "Acceleration")])
    model_page(b, m, line, f"{p}-model.jpg", f"{p}-campus.jpg",
               ["Superior cutting stability", "Ultra-high cutting speed", "Automated system, more efficient", "Precision pneumatic chuck",
                "Over-position cutting to minimize tail length"])
    rows = [("Tube length range", ft_mm(1000, 6500), ""), ("Tube diameter range", dia(10, 120), "National standard tube"),
            ("Side length of square tube", "□" + sq(10, 120), "National standard tube"), ("X / Y axis positioning accuracy", "±0.002″ (±0.05 mm)", ""),
            ("X / Y axis repeated positioning accuracy", "±0.001″ (±0.03 mm)", ""),
            ("Maximum rapid speed", ftmin(150), "As pipe weight increases, processing speed and moving parameters decrease."),
            ("Maximum chuck speed", "240 rpm", ""), ("Maximum acceleration", "1.5 G", ""), ("Weight", lb(3500), "Depends on actual factory delivery"),
            ("Maximum load", lb(120), ""), ("Dimensions", dims_ft(9100, 2230, 2300), ""), ("Phase", "Three-phase", ""),
            ("Power supply rated voltage", "380 V" + VOLT, ""), ("Frequency", "50 Hz", ""), ("Power supply protection grade", "IP54", "")]
    b.page("Technical parameters", title("02 · Technical parameters", f"Technical parameters · {m}") + tech_table(rows, ("No.", "Item", "Parameter", "Note"))
           + notes(["The achievable accuracy of the workpiece depends to some extent on factors such as workpiece type, surface, tube specifications and straightness.",
                    "The technical parameters above are subject to change without notice; the final technical parameters are subject to the order agreement."]) + D.included(), key="tech")
    precautions_page(b, m, 3)
    clamp = [("Round tube", 1, dia(10, 120)), ("Square tube", 2, "□" + sq(10, 120)), ("Rectangular tube", 3, f"0.4″ (10 mm) ≤ diagonal ≤ 4.7″ (120 mm)"),
             ("I-beam", 4, "≤ GB No. 8"), ("H-beam", 5, "≤ GB No. 8 (customized)"), ("Channel steel", 6, "≤ GB No. 8"),
             ("Equal angle steel", 7, "≤ GB No. 8"), ("Unequal angle steel", 8, "≤ GB No. 9/5"), ("Load capacity", None, lb(120))]
    clamp_page(b, m, 4, p, clamp, "Clamping ranges of the SF6012PLUS by section, as given in Senfeng's cutting parameters.")
    cut_pages(b, m, 4, N_CUT_NOTES)
    cost_page(b, m, 6, ["3 kW", "6 kW"],
              [("Laser source (kW)", [10, 18.5], True, grp("Peak power consumption", 6)), ("Chiller (kW)", [3.5, 8.4], True, " "),
               ("Air compressor (kW)", ["22", "/", "/"] * 2, False, " "), ("Host (kW)", ["16.7"] * 6, False, " "),
               ("Dust removal (kW)", ["1.5"] * 6, False, " "), ("Semi-automatic loading (kW)", ["1.5"] * 6, False, " "),
               ("Consumables and gas consumption (CNY/h)", ["0.5", "4.5", "60.5"] * 2), ("Total power (kW)", [55.2, 33.2, 33.2, 68.6, 46.6, 46.6]),
               ("Total power consumption (kWh per hour)", [33.12, 19.92, 19.92, 41.16, 27.96, 27.96]),
               ("Total operating cost (RMB per hour, at 1 RMB/kWh)", [33.62, 24.42, 80.42, 41.66, 32.46, 88.46])])
    conf = [("Laser source", [(1, "Laser source", 1, "Raycus")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "BOCI")]),
            ("Machine tool &amp; host", [(1, "Transmission system", 8, "SENFENG"), (2, "Machine tool and accessories", 1, "SENFENG"), (3, "Reducer", 6, "TECHMECH"),
                                         (4, "Electrical and pneumatic systems", 1, "SCHNEIDER (France) · SMC (Japan) &amp; AIRTAC (Taiwan)"),
                                         (5, "AC servo motor and driver", 8, "INOVANCE"), (6, "Water chiller", 1, "TONGFEI")]),
            ("CNC system", [(1, "CNC system", 1, "FSCUT 3000DE")]),
            ("Optional automation system", [(1, "Loading system", 1, "Optional: fully automatic / basic fully automatic / semi-automatic"),
                                            (2, "Unloading system", 1, "Standard: 6.6 ft (2 m) · customizable: 10 ft (3 m) / 13 ft (4 m)")])]
    b.page("Configuration", title("07 · Configuration list", f"Configuration list · {m}") + H.conf_table(conf, CONF_NOTES), key="config")
    src = ["<b>Small fiber core:</b> better beam quality.", "<b>Faster cutting speed:</b> enhanced cutting efficiency.",
           "<b>Improved high-reflection resistance:</b> new optical components with a multi-layer anti-reflection design for efficient processing of various metals.",
           "<b>Enhanced intelligence:</b> next-generation software with a smart app mode for real-time monitoring.",
           "<b>High electrical-optical conversion:</b> over 40 % efficiency, reducing power consumption.",
           "<b>Upgraded components:</b> new-generation pump sources offer greater reliability and stability, with improved beam quality and 30 – 40 % more brightness thanks to patented nonlinear suppression technology.",
           "<b>Lightweight and compact:</b> small size and compact design for easier integration.", "<b>Enhanced safety:</b> improved safety features."]
    head = ["<b>Collision protection for the cutting head:</b> the collision component is replaced directly, without replacing the cutting head, reducing the likelihood of returns.",
            "<b>Protective lens temperature monitoring:</b> if contamination is detected during operation, the system immediately raises an alarm and stops the machine to prevent damage to the head or lenses.",
            "<b>Cutting pressure monitoring:</b> gas pressure is monitored continuously; an alarm is raised at once if it is insufficient, too low or unstable.",
            "<b>Protective lens explosion detection:</b> the stray light on the protective lens is monitored continuously, with an alarm when it exceeds the threshold.",
            "<b>Pan seal failure detection:</b> the gas pressure in the lower 1 and lower 2 protective lens chambers is monitored continuously for stable production.",
            "<b>Process monitoring:</b> automatically re-cuts if the material isn't fully cut through."]
    body = (title("08 · Core components", "Laser source · laser head")
            + h2(f"{m} laser source") + row(fig(T + f"{p}-src1.jpg", "Raycus RFL-C3000 fiber laser source", h=120, px=900), ol(src), cols="0.8fr 1.2fr", gap=16, align="center")
            + h2(f"{m} laser head") + row(row(fig(T + f"{p}-head1.jpg", h=120, px=700), fig(T + f"{p}-head2.jpg", h=120, px=700), gap=8), ol(head), cols="0.8fr 1.2fr", gap=16, align="center"))
    b.page("Laser source · head", body, key="source")
    body = (title("09 · Core components", f"{m} chuck")
            + row(fig(T + f"{p}-chuck1.jpg", "Chuck for straight cutting", h=170, px=1200), fig(T + f"{p}-chuck2.jpg", "Bevel cutting chuck", h=170, px=1200), gap=14)
            + ol(["Pneumatic self-centering chuck with high clamping accuracy for more precise cutting.", "Fast clamping, with gear-driven self-centering for high efficiency.",
                  "High-precision chuck with good dust-proof performance and a low maintenance frequency.",
                  "The chuck's tube holding capacity reaches 265 lb (120 kg) — designed for ultra-high-precision cutting of small tubes.",
                  "The front chuck has a square structure, allowing a wider range of clamping sizes for square and rectangular tubes.",
                  "Dual-row roller configuration for more stable tube clamping."]) + D.included())
    b.page("Chuck", body, key="chuck")
    cards1 = [card(T + f"{p}-bed.jpg", "1 · Machine bed", ol(["The bed is welded from rectangular tubes, giving better stability, load capacity, vibration damping and performance.",
                                                              "The bed is designed with structural dynamic principles and finite-element variable analysis. After precise welding, stress-relief annealing, secondary aging treatment and precision machining on a large gantry milling machine, it has high rigidity and a long service life."]), h=92),
              card(T + f"{p}-support.jpg", "2 · Follow support", ol(["Servo control automatically aligns the tube center with the chuck center, ensuring constant contact with the tube surface for more precise lifting movements.",
                                                                    "The intelligent segmented layout keeps long tubes from sagging, ensuring higher machining accuracy."]), h=92)]
    cards2 = [card(T + f"{p}-tail.jpg", "3 · Ultra-short tail material", ol(["<b>Dimensions:</b> round tube Ø0.4 – 4.7″ (Ø10 – 120 mm); square tube 0.4 × 0.4 – 4.7 × 4.7″ (10 × 10 – 120 × 120 mm).",
                                                                             "<b>Tube types:</b> round, square and rectangular tubes.",
                                                                             "The “over-position” cutting process gives an ultra-short tail, making Senfeng one of the few makers of dual-chuck laser tube cutting machines that minimize tail material."]), h=80),
              card(T + f"{p}-profiles.jpg", "4 · Powerful dynamic performance", P("A brand-new laser tube cutting machine, offering ultra-high performance matched with high precision to meet customer needs.", cls="sm"), h=80)]
    body = title("10 · Host machine", f"{m} host") + grid(cards1, 2, 18) + '<div style="height:8pt"></div>' + grid(cards2, 2, 18)
    b.page("Host machine", body, key="host")
    cnc = ["Real-time tube center deviation compensation reduces clamping requirements, improves efficiency and enhances piercing accuracy.",
           "A bus-based real-time system with integrated follow control gives faster corner cutting, more stable following and more reliable cutting quality.",
           "The support-following function ensures the processing quality of the whole tube.",
           "Hollow chuck feeding and cutting significantly shortens the overall length of the tube cutting machine, with high automation.",
           "Supports automatic loading and unloading, continuous processing and standard automated feeding actions.",
           "Track accuracy 0.0008″ (0.02 mm), positioning accuracy 0.00004″ (0.001 mm), repeated positioning accuracy 0.0001″ (0.003 mm).",
           "Supports bevel cutting with automatic focusing.", "A pipe process library for easy process export and storage.",
           "Contactless piercing makes cutting smoother and improves efficiency.", "Compatible with the TubePro cutting software and the TubesT small-tube nesting software."]
    body = (title("11 · CNC system", "FSCUT3000DE CNC system") + fig(T + f"{p}-cnc.jpg", "Quick operation &amp; efficient cutting", h=150, px=1400)
            + P("FSCUT3000DE is a bus control system specifically designed for processing pipes with a diameter of 4.7″ (120 mm) or less. It supports "
                "cutting square, round, racetrack-shaped and elliptical tubes with high precision and efficiency. Its key features include:", cls="sm") + ul(cnc))
    b.page("CNC system", body, key="cnc")
    units = [unit_box(f"{p}-opt1.jpg", "1 · Unloading unit", "optional", [("Dimensions", "78.7 × 44.1 × 31.5″ (2,000 × 1,120 × 800 mm)"), ("Maximum tube length", "9.8 ft (3,000 mm)")],
                      "1. The material separation system automatically separates waste from finished tubes without manual intervention; the receiving cart and drop rack are one integrated structure — high integration and space saving.<br>"
                      "2. Servo control automatically aligns the tube center with the chuck center so tube sag does not affect machining accuracy. After processing, the plate flips and the finished product slides into the material cart."),
             unit_box(f"{p}-opt2.jpg", "2 · Fully automatic loading unit", "standard", [("Tube length", "14.8 – 21.3 ft (4,500 – 6,500 mm)"),
                                                                                       ("Side length (or diameter) of tube section", "0.8 × 0.8 – 4.7 × 4.7″ (20 × 20 – 120 × 120 mm); Ø0.8 – 4.7″ (Ø20 – 120 mm)"),
                                                                                       ("Max. load of a single tube", lb(120)), ("Warehouse load bearing", "4,409 lb (2 t)")])]
    body = title("12 · Optional units", f"{m} optional units") + f'<div class="u4">{"".join(units)}</div>' + D.included()
    b.page("Optional units", body, key="opt")
    units = [unit_box(f"{p}-opt3.jpg", "3 · Bevel cutting unit", "optional", [("Chuck diameter", "4.7″ (120 mm)"), ("Maximum swing angle", "±45°")],
                      "Suitable for precision bevel cutting of small-diameter tubes. Paired with a high-precision oscillating axis, it improves cutting stability and cuts bevels up to ±45°."),
             unit_box(f"{p}-opt4.jpg", "4 · Automatic slag removal unit", "optional", [("Maximum tube length", "19.7″ (500 mm)"),
                                                                                       ("Side length (or diameter) of pipe section", "0.8 × 0.8 – 4.7 × 4.7″ (20 × 20 – 120 × 120 mm); Ø0.8 – 4.7″ (Ø20 – 120 mm)")],
                      "This system effectively reduces the slag left inside the tube, eliminating secondary processing.")]
    body = title("13 · Optional units", f"{m} optional units") + f'<div class="u4">{"".join(units)}</div>' + D.included()
    b.page("Optional units", body, key="opt2")
    finish(b, m, "3 – 6 kW", prefix_cust="tcust-", toc={"after": 14, "items": [
        ("01 · Model", "model"), ("02 · Technical parameters", "tech"), ("03 · Precautions", "pre"), ("04 · Clamping range", "clamp"),
        ("04 · Cutting parameters — carbon steel", "cut1"), ("05 · Cutting parameters — stainless steel, aluminum alloy", "cut2"),
        ("06 · Cost-benefit analysis", "cost"), ("07 · Configuration list", "config"), ("08 · Laser source, laser head", "source"), ("09 · Chuck", "chuck"),
        ("10 · Host", "host"), ("11 · CNC system", "cnc"), ("12 – 13 · Optional units", "opt")]})
    return b


BOOKS = {"t12": book_t12, "t24": book_t24, "nt": book_nt, "plus": book_plus}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or list(BOOKS)
    for k in args:
        D.build(BOOKS[k](), "--html" in sys.argv)
