#!/usr/bin/env python3
"""NovoTech editions of Senfeng's two SF3015H "Technical Solutions" documents — every page, picture and detail of the originals in
NovoTech's catalogue format, units in imperial (metric in brackets).  The owner, Nov 1 2026: "convert these two Senfeng catalogues
to the NovoTech format too … a 'Download full technical specification' button for both series, medium and high power lasers".

    python3 tools/brochure/senfeng_h_editions.py [g3] [g4] [--html]

  g3  SF3015H medium and high power fiber laser cutting machine, third generation, 1.5 – 6 kW (SF3015H_solution, 22 pages)
        → src/files/NovoTech-Senfeng-SF3015H-Medium-High-Power-Laser-Technical-Specification-2026.pdf
  g4  SF3015H high-power laser cutting machine, fourth generation, 12 – 30 kW (SF3015H_fourth_generation_solution, 20 pages)
        → src/files/NovoTech-Senfeng-SF3015H-High-Power-Laser-Technical-Specification-2026.pdf

Senfeng is sold under its own brand, so its name and photos stay.  Cutting tables: tools/brochure/data-senfeng-sf3015h-g*-cutting.json
(values by power column and the shaded "sample cutting only" cells, read from the PDFs); speeds in inches per minute with the
original metres per minute below, thicknesses in decimal inches with the millimetres.
Adapted, and why: the warranty line states NovoTech's 1-year warranty (the third-generation sheet says 2 years, the fourth 1 year);
installation at the customer's site is by NovoTech with Senfeng; the operating voltage keeps Senfeng's 380 V with the transformer
NovoTech supplies for 208 / 240 / 480 / 600 V noted; the operating costs stay in RMB as Senfeng gives them (Chinese prices, for
reference); one misprint corrected (fourth generation, stainless 80 mm at 30 kW: "0.08-1.1" → 0.08 – 0.11 m/min).  The baked-in MPa
labels of the third generation's gas picture are replaced by imperial labels.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dener_laser_editions as D   # noqa: E402

ROOT = D.ROOT
S = os.path.join(ROOT, "tools", "src-images", "senfeng-h-spec") + "/"
SF = os.path.join(ROOT, "tools", "src-images", "senfeng") + "/"      # the site's own Senfeng product photos
title, P, checks, h2, h3, fig, row, grid, card, kv = D.title, D.P, D.checks, D.h2, D.h3, D.fig, D.row, D.grid, D.card, D.kv

D.INCLUDED[:] = [("Made in China by Senfeng Laser — CE, FDA and ETL certified and CSA approved", False), ("CSA-approved electrical panel", False),
                 ("1-year warranty", False), ("<b>7-day money-back guarantee</b> (in-stock machines only)", False),
                 ("Spare parts &amp; technical support readily available in Canada", False),
                 ("<b>Order Today with Just 10% Down — 0% Down Financing Available</b>", False), ("<b>Installation and training available</b>", False)]
D.DISCLAIMER = ("Specifications subject to change without notice. Imperial values are converted from Senfeng's metric data and rounded: "
                "sheet thicknesses in decimal inches, cutting speeds in inches per minute. Model numbers are manufacturer designations. "
                "Photos may show optional equipment.")
D.CSS += """
.ct{border-collapse:collapse;width:100%;font:400 7.6pt/1.1 Barlow,BarlowX;color:#2d2e30}
.ct th,.ct td{padding:2.6pt 2.5pt;text-align:center;vertical-align:middle;border-bottom:.6pt solid #e2e3e5}
.ct thead th{background:#2d2e30;color:#fff;font:500 7.8pt Oswald;letter-spacing:.03em;padding:4.4pt 2pt}
.ct thead th.corner{background:#f2a23b;color:#2d2e30}
.ct td small{display:block;font-size:6.3pt;color:#8c8e91;margin-top:.5pt}
.ct td.t{font-weight:600}
.ct td.m{background:#eeeff0;font:600 8pt Oswald;text-transform:uppercase;letter-spacing:.03em;width:58pt}
.ct td.sh{background:#fde3bf}
.ct td.g{font-size:7.2pt;color:#55575b}
.ct tbody tr:nth-child(even) td:not(.m):not(.sh){background:#f7f7f8}
.legend{display:flex;align-items:center;gap:6pt;font:400 7.6pt Barlow;color:#55575b;margin:5pt 0 0}
.legend i{display:inline-block;width:16pt;height:9pt;background:#fde3bf;border:.6pt solid #e8c48f}
.cb{border-collapse:collapse;width:100%;font:400 8pt/1.2 Barlow;color:#2d2e30}
.cb th,.cb td{border:.6pt solid #d9dadc;padding:4pt 2pt;text-align:center}
.cb thead th{background:#2d2e30;color:#fff;font:500 8pt Oswald;border-color:#55575b}
.cb thead th.corner{background:#f2a23b;color:#2d2e30}
.cb tbody th{text-align:left;font:600 8pt Barlow;background:#f4f4f5;padding-left:5pt}
.cb td.grp{writing-mode:vertical-rl;transform:rotate(180deg);font:600 7.6pt Oswald;text-transform:uppercase;background:#eeeff0;width:16pt}
.cf{border-collapse:collapse;width:100%;font:400 9pt/1.3 Barlow;color:#2d2e30}
.cf th,.cf td{padding:5.4pt 8pt;border-bottom:.8pt solid #d9dadc;text-align:left}
.cf thead th{background:#2d2e30;color:#fff;font:500 9pt Oswald;letter-spacing:.04em;text-transform:uppercase}
.cf thead th:first-child{background:#f2a23b;color:#2d2e30}
.cf td.sec{background:#eeeff0;font:600 9pt Oswald;text-transform:uppercase;letter-spacing:.04em;text-align:center}
.cf td.n{width:30pt;text-align:center}
.cf td.q{width:44pt;text-align:center}
.feat{display:grid;grid-template-columns:repeat(2,1fr);gap:8pt;margin-top:10pt}
.feat div{display:flex;align-items:center;gap:10pt;background:#f4f4f5;border-left:3.7pt solid #f2a23b;padding:8pt 10pt;font:500 10pt Oswald;color:#2d2e30;text-transform:uppercase;letter-spacing:.03em}
.feat b{font:700 16pt Oswald;color:#e08a1e}
.stp{display:grid;grid-template-columns:repeat(4,1fr);gap:10pt}
.stp>div{border-top:2pt solid #f2a23b;padding-top:5pt}
.stp b{display:block;font:700 15pt Oswald;color:#e08a1e}
.stp p{font-size:8.4pt;line-height:1.36;margin:2pt 0 0}
.gasl{position:absolute;transform:translate(-50%,-50%);background:#fff;border-left:3pt solid #f2a23b;box-shadow:0 .6pt 2.4pt rgba(0,0,0,.3);
 padding:3pt 7pt;text-align:left;white-space:nowrap}
.gasl b{display:block;font:600 8.6pt Oswald;color:#2d2e30;text-transform:uppercase;letter-spacing:.04em}
.gasl span{display:block;font:400 7.8pt Barlow;color:#55575b}
.pat{display:flex;gap:12pt}
.pat div{flex:1;background:#2d2e30;padding:10pt 12pt}
.pat b{display:block;font:700 26pt/1 Oswald;color:#f2a23b}
.pat span{display:block;font:400 8pt Barlow;color:#c9cbce;text-transform:uppercase;letter-spacing:.08em;margin-top:4pt}
.cust{display:grid;grid-template-columns:repeat(4,1fr);gap:7pt}
.cust img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
.num li{font-size:9pt}
.small-note{font:italic 400 7.6pt/1.35 Barlow;color:#6d6f73;margin:4pt 0 0}
.cf.tight th,.cf.tight td{padding:3.6pt 8pt;font-size:8.6pt}
"""


def ipm(v):
    return round(float(v) * 39.3701)


def thk(mm):
    return f"{float(mm) / 25.4:.3f}″<small>{mm} mm</small>"


def spd(cell):
    """'1.6-1.8(O2)*' → (html, shaded)"""
    if not cell:
        return "", False
    sh = cell.endswith("*")
    c = cell.rstrip("*")
    o2 = "(O2)" in c
    c = c.replace("(O2)", "").replace(" ", "")
    a, b = (c.split("-") + [None])[:2]
    imp = f"{ipm(a):,}" + (f" – {ipm(b):,}" if b else "")
    met = a + (f" – {b}" if b else "")
    return imp + (" O₂" if o2 else "") + f"<small>{met}</small>", sh


GAS = {"N2/Air": "N₂ / air", "N2/air": "N₂ / air", "O2": "O₂", "Air": "air"}


def cut_table(page, blocks):
    powers = page["powers"]
    th = "".join(f"<th>{p.replace('kW', ' kW')}</th>" for p in powers)
    body = ""
    for b in blocks:
        n = len(b["rows"])
        for i, (t, vals, gas) in enumerate(b["rows"]):
            tds = ""
            for v in vals:
                h, sh = spd(v)
                tds += f'<td class="{"sh" if sh else ""}">{h}</td>'
            m = f'<td class="m" rowspan="{n}">{b["material"]}</td>' if i == 0 else ""
            body += f'<tr>{m}<td class="t">{thk(t)}</td>{tds}<td class="g">{GAS.get(gas, gas)}</td></tr>'
    return (f'<table class="ct"><thead><tr><th class="corner">Material</th><th>Thickness</th>{th}<th>Gas</th></tr></thead>'
            f"<tbody>{body}</tbody></table>")


CUT_NOTES = ["Due to variations in material carbon content, the cutting parameters are for reference only; actual conditions prevail.",
             "Shaded cells: full-sheet processing is not possible and only sample cutting is allowed."]


def cut_page(b, data, pn, part, n, tab="Cutting parameters"):
    pg = data[str(pn)]
    blocks = pg["blocks"][part[0]:part[1]] if part else pg["blocks"]
    names = " · ".join(x["material"].lower() for x in blocks)
    body = (title(f"Cutting parameters · {n}", names.capitalize())
            + P("Cutting speed by laser source power in inches per minute; Senfeng's metres per minute below each value. "
                "“O₂” marks a value cut with oxygen where the row's gas is N₂ / air.", cls="xs")
            + cut_table(pg, blocks)
            + '<div class="legend"><i></i>Sample cutting only — full sheets cannot be processed at this power</div>'
            + "".join(f'<p class="small-note">{i}. {t}</p>' for i, t in enumerate(CUT_NOTES, 1))
            + (D.included() if sum(len(x["rows"]) for x in blocks) <= 18 else ""))
    b.page(tab, body, key=f"cut{n}")


def lb(kg):
    return f"{round(kg * 2.20462):,} lb ({kg:,} kg)"


def cost_table(powers, laser, chiller, comp, host, dust, cons, total, cons_h, cost, unit="CNY/h"):
    """Senfeng's cost-benefit table: three gas columns (air, O₂, N₂) per power"""
    gases = ["Air", "O₂", "N₂"]
    th1 = "".join(f'<th colspan="3">{p}</th>' for p in powers)
    th2 = "".join(f"<th>{g}</th>" for _ in powers for g in gases)

    def span3(vals):
        return "".join(f'<td colspan="3">{v}</td>' for v in vals)

    def each(vals):
        return "".join(f"<td>{v}</td>" for v in vals)
    k = len(powers)
    rows = (f'<tr><td class="grp" rowspan="5">Peak power consumption</td><th>Laser source (kW)</th>{span3(laser)}</tr>'
            f"<tr><th>Chiller (kW)</th>{span3(chiller)}</tr>"
            f"<tr><th>Air compressor (kW)</th>{each(comp)}</tr>"
            f"<tr><th>Machine tool host (kW)</th>{each([host] * 3 * k)}</tr>"
            f"<tr><th>Dust removal (kW)</th>{each([dust] * 3 * k)}</tr>"
            f'<tr><th colspan="2">Consumables and gas consumption ({unit})</th>{each(cons * k)}</tr>'
            f'<tr><th colspan="2">Total power (kW)</th>{each(total)}</tr>'
            f'<tr><th colspan="2">Total power consumption (kWh per hour)</th>{each(cons_h)}</tr>'
            f'<tr><th colspan="2">Total operating cost (RMB per hour, at 1 RMB/kWh)</th>{each(cost)}</tr>')
    return (f'<table class="cb"><thead><tr><th class="corner" colspan="2" rowspan="2">Item</th>{th1}</tr><tr>{th2}</tr></thead>'
            f"<tbody>{rows}</tbody></table>")


def conf_table(sections, notes):
    body = ""
    for sec, items in sections:
        body += f'<tr><td class="sec" colspan="4">{sec}</td></tr>'
        for n, it, q, br in items:
            body += f'<tr><td class="n">{n}</td><td>{it}</td><td class="q">{q}</td><td>{br}</td></tr>'
    t = f'<table class="cf"><thead><tr><th>No.</th><th>Item</th><th>Qty</th><th>Brand</th></tr></thead><tbody>{body}</tbody></table>'
    return t + "".join(f'<p class="small-note">{i}. {x}</p>' for i, x in enumerate(notes, 1))


def numbered(rows):
    """[(no, item, value)] parameter table"""
    body = "".join(f"<tr><td class='n'>{n}</td><th>{i}</th><td>{v}</td></tr>" for n, i, v in rows)
    return f'<table class="cf"><thead><tr><th>No.</th><th>Item</th><th>Parameter</th></tr></thead><tbody>{body}</tbody></table>'


VOLT_NOTE = "<small> — in Canada: 208 / 240 / 480 / 600 V 3-phase 60 Hz through the transformer NovoTech supplies</small>"
TRAINING = [("Before equipment delivery", "The buyer can arrange for 1 – 2 operators to attend a one-week training at the Senfeng factory. "
             "The dates are confirmed with Senfeng's customer service department."),
            ("During the warranty period", "The buyer can apply for one more session of free training for 1 – 2 operators at Senfeng."),
            ("Training", "Laser principles, equipment structure, process explanation, equipment maintenance, laser safety protection, "
             "operating procedures and basic troubleshooting."),
            ("Requirement", "Trainees must be mechanical, electrical or optical engineers and pass assessments on equipment operation, laser "
             "principles, safety and maintenance before starting work.")]
INSTALL = [("Installation", "NovoTech engineers, with Senfeng, install the equipment at the customer's site."),
           ("Equipment debugging", "After installation, the equipment is debugged for the customer's use."),
           ("Door-to-door training", "On-site training on equipment maintenance, safety, operating procedures and basic troubleshooting, "
            "with 7 days of guaranteed usage."),
           ("On-site acceptance", "After the steps above, the engineer leaves the site only after the customer's acceptance (the customer can veto).")]


def steps(items):
    return '<div class="stp">' + "".join(f"<div><b>{i:02d}</b><div class='ittl'>{t}</div><p>{x}</p></div>" for i, (t, x) in enumerate(items, 1)) + "</div>"


def toc_page(b, toc, line):
    rows_ = "".join(f'<div><span>{t}</span><i></i><b>{b.num(k):02d}</b></div>' for t, k in toc)
    body = (title(line, "Contents") + f'<div class="toc" style="columns:1">{rows_}</div>'
            + row(D.included(two=True), '<div class="box"><div class="bt">Sold &amp; serviced in Canada</div>'
                  '<p>by NovoTech Machine Tools — Mississauga, ON</p></div>', cols="2.3fr 1fr", gap=14, cls="mt-auto"))
    for pg in b.pages:
        if pg.get("body") == "@@TOC@@":
            pg["body"] = body


# ======================================================================================== third generation, 1.5 – 6 kW
def book_g3():
    data = json.load(open(os.path.join(HERE, "data-senfeng-sf3015h-g3-cutting.json")))
    b = D.Book("sf-h-g3", "SF3015H fiber laser — full technical specification", "Senfeng · medium and high power · third generation · 1.5 – 6 kW",
               os.path.join(ROOT, "src", "files", "NovoTech-Senfeng-SF3015H-Medium-High-Power-Laser-Technical-Specification-2026.pdf"))
    b.title = "Senfeng SF3015H Medium and High Power Fiber Laser — Full Technical Specification — NovoTech Machine Tools"
    b.subject = "Senfeng SF3015H medium and high power fiber laser cutting machine, 1.5 – 6 kW — full technical specification, imperial edition"
    b.cover("Senfeng · full technical specification", "SF3015H · third generation · 1.5 – 6 kW", "SF3015H fiber laser", "Technical specification",
            "Medium and high power fiber laser cutting machine", S + "h3-machine.jpg",
            [("10 × 5 ft", "Work area"), ("1.5 – 6 kW", "MAX fiber laser"), ("427 ft/min", "Maximum speed"), ("1.2 G", "Maximum acceleration")],
            hero_h=320, minis=[S + "h3-head-6kw.jpg", S + "h3-source-1.jpg", S + "h3-bed.jpg", S + "h3-door.jpg"])
    b.page("Contents", "@@TOC@@", sub="Contents")
    body = (title("Fiber laser cutting machine · contents", "Senfeng technical solutions")
            + row(P("Contents of Senfeng's SF3015H technical solution: the model and its technical and cutting parameters, a cost-benefit "
                    "analysis and the configuration list; the core components and systems — laser source and head, machine bed, automatic gas "
                    "distribution, CNC system and the optional loading automation; and Senfeng's after-sales service — automated metal "
                    "fabrication solutions, personnel training, packaging and transportation, installation and customization, five-star fast "
                    "service and customer testimonials.", cls="sm")
                  + checks(["Fiber laser cutting machine: model, technical parameters, cutting parameters, cost-benefit analysis, configuration list",
                            "Core components and systems: laser source and laser head, machine bed system, auto gas distribution system, CNC system, optional configuration",
                            "After-sales service: automated metal fabrication solutions, training, packaging and transportation, installation and customization, five-star fast service, customer testimonials"], cls="sm"),
                  fig(S + "campus.jpg", "Senfeng's campus in Jinan, China", h=330, px=900), cols="1.2fr 1fr", gap=18))
    b.page("Overview", body, key="overview")
    feats = ["High strength machine bed", "Intelligent spiral negative pressure dust removal", "Visual monitoring for safety protection",
             "Integrated temperature and humidity control"]
    body = (title("01 · Model · the third generation", "SF3015H")
            + P("Medium and high power fiber laser cutting machine.", cls="sm")
            + fig(S + "h3-machine.jpg", h=300, px=2000)
            + '<div class="feat">' + "".join(f"<div><b>{i}</b>{t}</div>" for i, t in enumerate(feats, 1)) + "</div>"
            + P("*The image is for reference only; the appearance and dimensions are subject to the actual product from the factory.", cls="note")
            + D.included())
    b.page("Model", body, key="model")
    pw = ["1.5 kW", "2 kW", "3 kW", "4 kW", "6 kW"]
    one = lambda v: [v] + [""] * 4      # noqa: E731
    rows = [("Work area (L × W)", ["10 × 5 ft (3,050 × 1,530 mm)"]), ("X-axis travel", ["60.2″ (1,530 mm)"]), ("Y-axis travel", ["120.1″ (3,050 mm)"]),
            ("Z-axis travel", ["8.7″ (220 mm)"]), ("X / Y axis positioning accuracy", ["±0.002″ (±0.05 mm)"]),
            ("X / Y axis repeated positioning accuracy", ["±0.0008″ (±0.02 mm)"]), ("Maximum speed", ["427 ft/min (130 m/min)"]),
            ("Maximum acceleration", ["1.2 G"]), ("Dimensions (L × W × H)", ["28.0 × 7.4 × 7.2 ft (8,520 × 2,270 × 2,180 mm)"]),
            ("Maximum load", ["2,425 lb (1,100 kg)"]), ("Weight", [lb(5240), lb(5240), lb(5260), lb(5320), lb(5320)]), ("Phase", ["Three-phase"]),
            ("Power supply rated voltage", ["380 V" + VOLT_NOTE]), ("Frequency", ["60 Hz"]), ("Overall power supply protection level", ["IP54"])]
    trs = "".join(f"<tr><th>{l}</th>" + (f'<td colspan="5">{v[0]}</td>' if len(v) == 1 else "".join(f"<td>{x}</td>" for x in v)) + "</tr>" for l, v in rows)
    body = (title("02 · Technical parameters", "Technical parameters · SF3015H")
            + f'<table class="kv spec3"><thead><tr><th>Item</th>{"".join(f"<th>{p}</th>" for p in pw)}</tr></thead><tbody>{trs}</tbody></table>'
            + '<p class="small-note">1. Workpiece accuracy depends on factors like type, pre-treatment, sheet size and position.</p>'
            + '<p class="small-note">2. Technical parameters are subject to change without notice. Final parameters are based on the order agreement.</p>'
            + D.included())
    b.page("Technical parameters", body, key="tech")
    cut_page(b, data, 5, (0, 1), "1 of 3")
    cut_page(b, data, 5, (1, 2), "2 of 3")
    cut_page(b, data, 6, None, "3 of 3")
    pw5 = ["1.5 kW", "2 kW", "3 kW", "4 kW", "6 kW"]
    body = (title("05 · Cost-benefit analysis", "Cost-benefit analysis · SF3015H")
            + P("If the cutting auxiliary gas is dried compressed air, the cost includes the air compressor's electricity, the machine's power "
                "consumption and the consumables (protective lenses, cutting nozzles).", cls="sm")
            + cost_table(pw5, [5, 6, 10, 16, 16], [3, 3, 3, 6, 6], ["15", "/", "/"] * 5, 10, 3, ["0.5", "4.5", "60.5"],
                         [36, 21, 21, 37, 22, 22, 41, 26, 26, 50, 35, 35, 50, 35, 35],
                         [21.6, 12.6, 12.6, 22.2, 13.2, 13.2, 24.6, 15.6, 15.6, 30, 21, 21, 30, 21, 21],
                         [22.1, 17.1, 73.1, 22.7, 17.7, 73.7, 25.1, 20.1, 76.1, 30.5, 25.5, 81.5, 30.5, 25.5, 81.5])
            + '<p class="small-note">1. The electricity and gas prices are Senfeng\'s reference values in China (RMB) and vary by region.</p>'
            + '<p class="small-note">2. Auxiliary gas consumption varies with plate thickness; the values are based on 0.630″ (16 mm) carbon steel for '
              "oxygen and 0.039″ (1 mm) stainless steel for nitrogen, for reference.</p>" + D.included())
    b.page("Cost-benefit analysis", body, key="cost")
    body = (title("06 · Configuration list", "Configuration list · SF3015H")
            + conf_table([("Laser source", [(1, "Laser source", 1, "Max")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "Raytools")]),
                          ("Machine tool &amp; host", [(1, "Transmission system", 4, "SENFENG"), (2, "Machine tool and accessory", 1, "SENFENG"),
                                                     (3, "Reducer", 3, "SHIMPO, Japan"), (4, "Electrical and pneumatic systems", 1, "SCHNEIDER, France · AVENTICS, Germany"),
                                                     (5, "AC servo motor and driver", 4, "Fuji, Japan"), (6, "Water chiller", 1, "Hanli")]),
                          ("CNC cutting system", [(1, "CNC laser cutting system", 1, "FSCUT")])],
                         ["This is Senfeng's optimized configuration. Changes in brand or configuration may cause irreversible effects.",
                          "Warranty: NovoTech's 1-year warranty on the entire machine (excluding consumables, force majeure natural disasters, war, "
                          "improper operation and human damage)."])
            + D.included())
    b.page("Configuration", body, key="config")
    heads = row(fig(S + "h3-head-3kw.jpg", "3 kW and below", h=210, px=600), fig(S + "h3-head-6kw.jpg", "4 – 6 kW", h=210, px=600), gap=14)
    body = (title("07 · Core components", "Laser source · laser cutting head")
            + h2("SF3015H laser source", "1.5 – 6 kW optional power")
            + row(row(fig(S + "h3-source-1.jpg", h=95, px=900), fig(S + "h3-source-2.jpg", h=95, px=900), gap=10),
                  '<ol class="num">' + "".join(f"<li>{x}</li>" for x in ["High-power and high-quality laser output", "Uniformly distributed beam energy",
                                                                         "Excellent performance and strong processing ability",
                                                                         "Compact structure and maintenance-free", "Wide range of applications"]) + "</ol>",
                  cols="1.3fr 1fr", gap=16, align="center")
            + h2("SF3015H laser cutting head")
            + row(heads, '<ol class="num">' + "".join(f"<li>{x}</li>" for x in [
                "<b>Efficient cooling:</b> the collimating and focusing lenses have cooling structures, and the nozzle has cooling airflow, "
                "protecting the nozzle and ceramic body and extending operation time.",
                "<b>Fast focusing:</b> collimated focusing allows faster movement and a larger adjustment range than traditional focusing.",
                "<b>Multiple protective lenses:</b> four protective lenses reduce contamination when the fiber and lower protective lenses are "
                "replaced, extending the life of the collimating and focusing lenses.",
                "<b>Optimized structure:</b> the integrated body design ensures sealing; improved QBH, QD and G5 fiber interfaces improve "
                "compatibility with the laser source and prevent jamming caused by rust or water leakage."]) + "</ol>",
                  cols="1fr 1.25fr", gap=16, align="center"))
    b.page("Laser source · head", body, key="source")
    bed = [("1", "High strength machine bed", S + "h3-bed.jpg", ["Welded with precision welding techniques; after stress-relief annealing it "
                                                                   "undergoes secondary vibration aging treatment and finishing.",
                                                                   "Finite element analysis gives the optimal stress points and support structure, "
                                                                   "greatly reducing resonance during movement and ensuring long-term stable operation."]),
           ("2", "Aerospace-grade high-strength aluminum beam", S + "h3-beam.jpg", [
               "The beam is aerospace-grade high-strength aluminum alloy, extruded, heat-treated and precision-machined for excellent rigidity "
               "and surface quality. Its corrosion resistance, light weight, high rigidity and toughness are ideal for high-speed laser cutting.",
               "The optimized internal structure ensures excellent dynamic performance, enabling high-speed cutting with accuracy."]),
           ("3", "Intelligent spiral negative pressure dust removal", S + "h3-dust.jpg", [
               "The dust extraction system controls the exhaust vents according to the current cutting position, with timed, zoned and "
               "sectional exhaust.", "Combined with the base's bottom return-seal design, it ensures smoke-free cutting."]),
           ("4", "Visual monitoring for safety protection", S + "h3-monitor.jpg", [
               "The all-around monitoring system minimizes blind spots, ensuring safe and stable cutting operations."])]
    cards = [card(img, f"{n} · {t}", checks(x, cls="sm"), h=112) for n, t, img, x in bed]
    body = title("08 · Machine bed system", "SF3015H machine bed system") + grid(cards[:2], 2, 18) + '<div style="height:10pt"></div>' + grid(cards[2:], 2, 18)
    b.page("Machine bed system", body, key="bed")
    bed2 = [("5", "Temperature-controlled electrical cabinet", S + "h3-cabinet.jpg", [
                "The H series has a newly added temperature-controlled electrical cabinet, so no additional air-conditioned room is needed.",
                "The internal environment is temperature and humidity controlled, for excellent environmental adaptability.",
                "Significantly extends the life of the control system's electronic components, ensuring more stable laser cutting performance."]),
            ("6", "Fully enclosed lift door", S + "h3-door.jpg", ["The fully enclosed lift door improves the machine's sealing, improving dust "
                                                                   "extraction and reducing smoke."]),
            ("7", "Modular Z axis", S + "h3-zaxis.jpg", ["The modular Z axis seals well, reducing contamination and lowering the failure rate.",
                                                      "Modular installation and replacement greatly reduce maintenance time and difficulty."])]
    cards = [card(img, f"{n} · {t}", checks(x, cls="sm"), h=150) for n, t, img, x in bed2]
    body = title("09 · Machine bed system", "SF3015H machine bed system") + grid(cards[:2], 2, 18) + '<div style="height:10pt"></div>' + grid(cards[2:] + [""], 2, 18)
    b.page("Machine bed system", body, key="bed2")
    labels = [("Nitrogen (300 psi)", "Adjustable 15 – 435 psi (0.1 – 3 MPa)", 23.3, 36.8), ("Oxygen", "Adjustable 7 – 131 psi (0.05 – 0.9 MPa)", 35.1, 69.3),
              ("Compressed air", "Adjustable 15 – 435 psi (0.1 – 3 MPa)", 83.3, 60.2)]
    gas = (f'<div class="lab" style="height:300pt"><img src="{D.im(S + "h3-gas.jpg", 1600)}">'
           + "".join(f'<div class="gasl" style="left:{x}%;top:{y}%"><b>{t}</b><span>{s}</span></div>' for t, s, x, y in labels) + "</div>")
    body = (title("10 · Auto gas distribution system", "Precise control of each gas flow") + gas
            + P("The CNC laser cutting machine has two separate gas lines: nitrogen (air) and oxygen. Each gas line can be independently "
                "controlled for flow rate and pressure.")
            + checks(["The equipment software terminal has an automatic auxiliary gas selection feature.",
                      "The type and pressure of the auxiliary gases are set and selected automatically through the CNC program — no manual operation.",
                      "The actual gas pressure at the cutting head outlet is read and displayed on the panel in real time."]) + D.included())
    b.page("Gas distribution", body, key="gas")
    body = (title("11 · CNC system", "Bus cutting system") + fig(S + "h3-cnc.jpg", "Quick operation &amp; efficient cutting", h=200, px=1400)
            + P("This intelligent bus system is designed specifically for fiber laser cutting. It integrates motion control, laser source control "
                "and cutting gas control, offering stability, reliability, easy deployment, simple debugging, production safety and a rich set of "
                "features with excellent performance. It offers modular, customizable, automated and informational solutions. The system has "
                "memory buffering and a comprehensive cutting process database with optimized parameters for various materials and thicknesses, "
                "for fast operation and efficient cutting — ideal for sheet metal, kitchenware and lighting.")
            + checks(["Supported file formats: direct processing of DXF files and high-speed reading and writing of LXDS and NRP files generated by CypNest.",
                      "A cutting database allows real-time adjustments during cutting for optimal processing quality.",
                      "Multi-stage piercing, sharp-corner entry and centering significantly improve high-power cutting efficiency and stability.",
                      "Optimized rapid travel modes, including the “LeapFrog” function."]) + D.included())
    b.page("CNC system", body, key="cnc")
    body = (title("12 · Optional configuration", "Servo swing arm loading system")
            + h2("1 · Composition") + fig(S + "h3-swingarm.jpg", h=170, px=1400)
            + P("The system consists of a 1,102 lb (500 kg) swing arm manipulator, a 1,102 lb (500 kg) loading vacuum suction cup, a 6,614 lb "
                "(3,000 kg) fixed raw material rack, a vacuum system, a safety protection system, a CNC control system, etc.", cls="sm")
            + h2("2 · Core technical parameters")
            + numbered([(1, "Maximum sheet size", "10 × 5 ft (3,000 × 1,500 mm)"), (2, "Minimum sheet size", "31.5 × 31.5″ (800 × 800 mm)"),
                        (3, "Sheet thickness", "0.04 – 0.55″ (1 – 14 mm)"), (4, "Maximum sheet weight", "1,102 lb (500 kg)"), (5, "Arm swing angle", "120°"),
                        (6, "Repeated positioning accuracy", "±0.04″ (±1 mm)"), (7, "Single load cycle", "&lt; 45 s"),
                        (8, "Gas supply pressure", "73 – 87 psi (0.5 – 0.6 MPa)"), (9, "Gas consumption", "7.1 cfm (0.2 m³/min)"),
                        (10, "Material rack load", "6,614 lb (3,000 kg)"), (11, "Power supply voltage", "220 / 380 V"), (12, "Operating current", "12 A")]))
    b.page("Optional", body, key="opt1")
    body = (title("13 · Optional configuration", "3015 automatic loading and unloading robot")
            + row(h2("1 · Composition") + P("This system consists of composite truss manipulators for loading and unloading, a double-layer "
                                            "electric material cart, a CNC control system and a vacuum control system, working with the laser "
                                            "cutter as an automated sheet metal production unit. It automates the loading and unloading of "
                                            "plates, improving efficiency and reducing costs.", cls="sm"),
                  fig(S + "h3-robot.jpg", h=210, px=1000), cols="1fr 1.1fr", gap=16, align="center")
            + h2("2 · Core technical parameters")
            + numbered([(1, "Maximum sheet size", "10 × 5 ft (3,000 × 1,500 mm)"), (2, "Minimum sheet size", "31.5 × 31.5″ (800 × 800 mm)"),
                        (3, "Maximum sheet thickness", "0.55″ (14 mm)"), (4, "Minimum sheet thickness", "0.031″ (0.8 mm)"),
                        (5, "Maximum sheet weight", "1,102 lb (500 kg)"), (6, "Single-layer loading weight of the exchange material cart", "6,614 lb (3 t)"),
                        (7, "Single-layer loading height of the exchange material cart", "9.4″ (240 mm), including the material tray"),
                        (8, "Manipulator translation speed", "33 – 98 ft/min (10 – 30 m/min)"), (9, "Manipulator lifting speed", "16 – 33 ft/min (5 – 10 m/min)"),
                        (10, "Cart exchange speed", "33 ft/min (10 m/min)"), (11, "Intake pipe", "0.47″ (12 mm)"),
                        (12, "Gas source", "87 – 102 psi (0.6 – 0.7 MPa)"), (13, "Power supply", "3-phase 5-wire 380 V")]))
    b.page("Optional", body, key="opt2")
    body = (title("14 · Optional configuration", "3015 warehouse + automatic loading and unloading robot")
            + row(h2("1 · Composition")
                  + P("This system consists of a 3015 vertical warehouse, a vacuum suction cup composite fork loading and unloading truss robot, "
                      "the robot's track frame, a CNC control system, a vacuum control system, etc., which together with the laser cutting "
                      "machine form an automated sheet metal production unit.", cls="sm"),
                  fig(S + "h3-warehouse.jpg", h=140, px=1000), cols="1fr 1.2fr", gap=16, align="center")
            + h2("2 · Core technical parameters")
            + numbered([(1, "Layers of warehouse", "10"), (2, "Sheet size", "10 × 5 ft (3,000 × 1,500 mm)"), (3, "Warehouse layer load capacity", "6,614 lb (3,000 kg)"),
                        (4, "Lifting speed", "33 ft/min (10 m/min)"), (5, "Warehouse in-and-out speed", "33 ft/min (10 m/min)"),
                        (6, "Maximum sheet size", "10 × 5 ft (3,000 × 1,500 mm)"), (7, "Minimum sheet size", "31.5 × 31.5″ (800 × 800 mm)"),
                        (8, "Sheet thickness", "0.04 – 0.55″ (1 – 14 mm)"), (9, "Maximum sheet weight", "1,102 lb (500 kg)"),
                        (10, "Translation speed", "33 – 98 ft/min (10 – 30 m/min)"), (11, "Lifting speed of the loading and unloading manipulator", "16 – 39 ft/min (5 – 12 m/min)"),
                        (12, "Single loading and unloading cycle", "&lt; 180 s"), (13, "Air supply pressure", "87 – 102 psi (0.6 – 0.7 MPa)"),
                        (14, "Load of the electric material cart", "6,614 lb (3,000 kg)"), (15, "Operation speed of the electric material cart", "33 ft/min (10 m/min)"),
                        (16, "Power supply voltage", "380 V"), (17, "Working current", "80 A")]).replace('class="cf"', 'class="cf tight"'))
    b.page("Optional", body, key="opt3")
    body = (title("15 · Shipping", "Shipping · SF3015H")
            + h2("1 · Packing") + P("Standard packaging is fixed with high-strength bolts. A 20 ft (20 GP) container is used for shipment, ensuring "
                                    "the safety of the equipment.")
            + fig(S + "h3-container-1.jpg", h=210, px=1300)
            + h2("2 · Shipping") + P("One SF3015H standard machine needs one 20 ft (20 GP) container, making sea transportation cheaper and safer.")
            + fig(S + "h3-container-2.jpg", h=210, px=1300))
    b.page("Shipping", body, key="ship")
    body = (title("16 · After-sales service", "Providing global users with automated metal fabrication solutions")
            + row(P("Senfeng provides automated metal fabrication solutions globally, integrating cutting, bending, welding, cladding, automation "
                    "and new energy. With core technologies in laser cutting, welding and cladding, the company also offers intelligent "
                    "manufacturing systems such as flexible laser processing lines and sheet metal bending centers. These solutions serve "
                    "industries including automotive, construction, energy and petrochemicals, and are used in over 100 countries."),
                  fig(S + "solutions.jpg", h=230, px=1000), cols="1fr 1fr", gap=18, align="center")
            + '<div class="pat"><div><b>03</b><span>International PCT patents</span></div><div><b>577</b><span>Chinese technology patents</span></div></div>'
            + '<div style="height:10pt"></div>'
            + P("Senfeng has developed key components such as laser generators, processing heads, the Feng Cloud system and CNC systems, used in "
                "cutting, welding, cladding and automation. The company offers a complete industry chain, including laser cutting, welding, "
                "cladding and cleaning machines, bending centers and flexible production lines. These solutions are used in sectors such as power "
                "towers, construction machinery, shipbuilding, bridges and aerospace, helping businesses accelerate production and reduce costs for "
                "greater economic benefit.") + D.included())
    b.page("After-sales service", body, key="solutions")
    pack = [("Packaging", "Standard packaging, suitable for long-distance transportation, moisture-proof, rust-proof and shock-resistant. Designed "
             "for full lifting, with marked lifting points and center of gravity."),
            ("Transportation", "Domestic transportation within China is fully handled by Senfeng, including freight and insurance."),
            ("Packing list &amp; certificate", "Each package includes a packing list and a certificate of conformity. The user manual and other "
             "documents are inside the box; the packing list is on the outside.")]
    body = (title("17 · After-sales service", "Training · packaging · installation")
            + h2("Technical training", "to enhance customer production efficiency") + steps(TRAINING)
            + h2("Packaging &amp; transportation", "to ensure equipment quality")
            + row(fig(S + "pack-1.jpg", h=62, fit="cover", px=700), fig(S + "pack-2.jpg", h=62, fit="cover", px=700), fig(S + "pack-3.jpg", h=62, fit="cover", px=700), gap=10)
            + '<div style="height:5pt"></div>' + steps(pack).replace("repeat(4,1fr)", "repeat(3,1fr)")
            + h2("Installation", "professional and high-quality") + steps(INSTALL))
    b.page("After-sales service", body, key="training")
    cust = [("custom-1.jpg", "Senfeng understands the client's industry status and specific production processes, identifies issues and assesses their needs."),
            ("custom-2.jpg", "Through in-depth on-site communication, metal fabrication automation solutions are customized to the client's pain points and needs."),
            ("custom-3.jpg", "A tailored solution, different from competitors' standardized models."),
            ("custom-4.jpg", "A one-stop R&amp;D and production service from design to final machine, with thorough quality checks until customer "
             "satisfaction and acceptance.")]
    body = (title("18 · After-sales service", "Premium customization")
            + P("In the digital era, intelligent transformation in metal processing is essential. Building unmanned factories is key to "
                "upgrading, with customized automation solutions a top priority.")
            + grid([fig(S + f, h=150, fit="cover", px=1000) + P(f"<b>{i:02d}</b> · {t}", cls="sm") for i, (f, t) in enumerate(cust, 1)], 2, 16)
            + D.included())
    b.page("Customization", body, key="custom")
    body = (title("19 · After-sales service", "Five-star fast service")
            + fig(S + "service-bg.jpg", h=150, fit="cover", px=1600)
            + row(h2("Efficient") + checks(["Senfeng's repair hotline is available 24/7.",
                                           "A professional engineer responds to customer inquiries within 10 minutes and provides a repair plan within 1 hour."], cls="sm"),
                  fig(S + "service-1.jpg", h=92, fit="cover", px=700), cols="1.6fr 1fr", gap=14, align="center")
            + row(h2("Professional") + checks(["<b>Custom service:</b> service plans tailored to the customer's specific needs.",
                                              "<b>Service engineer certification:</b> each service engineer is rigorously trained and assessed before being certified to work.",
                                              "<b>Common issues training:</b> a manual of common issues for each equipment model, with certified engineers training customers.",
                                              "<b>Online guidance:</b> experienced senior engineers support customers by phone or video call.",
                                              "<b>Professional technical support:</b> the equipment is properly calibrated at the first installation, and similar issues are resolved in one go."], cls="sm"),
                  row(fig(S + "service-2.jpg", h=70, fit="cover", px=700), fig(S + "service-3.jpg", h=70, fit="cover", px=700), cols="1fr", gap=6),
                  cols="1.6fr 1fr", gap=14, align="center")
            + row(h2("Comprehensive") + checks(["<b>Pre-service:</b> theoretical and hands-on operation training, common fault self-diagnosis training, "
                                               "quick repair guidance and usage reminders.",
                                               "<b>Regular service:</b> regular maintenance reminders, on-site services and periodic promotional activities.",
                                               "<b>Value-added service:</b> equipment software and hardware upgrades, financing lease services and extended warranty services."], cls="sm"),
                  fig(S + "service-4.jpg", h=92, fit="cover", px=700), cols="1.6fr 1fr", gap=14, align="center"))
    b.page("Five-star service", body, key="service")
    body = (title("20 · After-sales service", "Customer testimonials")
            + P("Senfeng machines and customers around the world.", cls="sm")
            + '<div class="cust">' + "".join(f'<img src="{D.im(S + f"cust-{i:02d}.jpg", 600)}">' for i in range(1, 17)) + "</div>")
    b.page("Testimonials", body, key="cust")
    b.back("Fiber laser for your shop.", [S + "h3-machine.jpg", S + "h3-door.jpg", S + "h3-head-6kw.jpg", S + "h3-bed.jpg"])
    toc_page(b, [("Fiber laser cutting machine · Senfeng technical solutions", "overview"), ("01 · Model", "model"), ("02 · Technical parameters", "tech"),
                 ("03 · Cutting parameters — stainless steel", "cut1 of 3"), ("03 · Cutting parameters — carbon steel", "cut2 of 3"),
                 ("04 · Cutting parameters — brass, aluminum", "cut3 of 3"),
                 ("05 · Cost-benefit analysis", "cost"), ("06 · Configuration list", "config"), ("07 · Laser source, laser head", "source"),
                 ("08 – 09 · Machine bed system", "bed"), ("10 · Auto gas distribution system", "gas"), ("11 · CNC system", "cnc"),
                 ("12 – 14 · Optional configuration: swing arm loading, loading robot, warehouse", "opt1"), ("15 · Shipping", "ship"),
                 ("16 · Automated metal fabrication solutions", "solutions"), ("17 · Personnel training, packaging and transportation, installation", "training"),
                 ("18 · Customization", "custom"), ("19 · Five-star fast service", "service"), ("20 · Customer testimonials", "cust")],
             "Full technical specification · SF3015H · 1.5 – 6 kW")
    return b


# ======================================================================================== fourth generation, 12 – 30 kW
def book_g4():
    data = json.load(open(os.path.join(HERE, "data-senfeng-sf3015h-g4-cutting.json")))
    b = D.Book("sf-h-g4", "SF3015H high-power laser — full technical specification", "Senfeng · fourth generation · 12 – 30 kW",
               os.path.join(ROOT, "src", "files", "NovoTech-Senfeng-SF3015H-High-Power-Laser-Technical-Specification-2026.pdf"))
    b.title = "Senfeng SF3015H High-Power Fiber Laser — Full Technical Specification — NovoTech Machine Tools"
    b.subject = "Senfeng SF3015H high-power laser cutting machine, fourth generation, 12 – 30 kW — full technical specification, imperial edition"
    b.cover("Senfeng · full technical specification", "SF3015H · fourth generation · 12 – 30 kW", "SF3015H high power", "Technical specification",
            "High-power laser cutting machine · versatile &amp; efficient", S + "h4-machine.jpg",
            [("10 × 5 ft", "Work area"), ("12 – 30 kW", "Raycus fiber laser"), ("656 ft/min", "Maximum speed"), ("2.8 G", "Maximum acceleration")],
            hero_h=320, minis=[S + "h4-head-30.jpg", S + "h4-source-30.jpg", S + "h4-bed.jpg", S + "sample-7.jpg"])
    b.page("Contents", "@@TOC@@", sub="Contents")
    feats = ["Heavy-duty and thermally isolated hollow bed", "Laser cutting process database", "Intelligent surrounding spiral negative pressure dust removal",
             "Storm cutting system"]
    body = (title("01 · Model · the fourth generation", "Versatile &amp; efficient")
            + P("SF3015H high power laser cutting machine.", cls="sm")
            + fig(S + "h4-machine.jpg", h=300, px=2000)
            + '<div class="feat">' + "".join(f"<div><b>{i}</b>{t}</div>" for i, t in enumerate(feats, 1)) + "</div>"
            + P("※The picture is for reference only; the actual appearance and size prevail.", cls="note") + D.included())
    b.page("Model", body, key="model")
    pw = ["12 kW", "15 kW", "20 kW", "30 kW"]
    rows = [("Work area (length × width)", ["10 × 5 ft (3,000 × 1,500 mm)"]), ("X-axis travel", ["60.2″ (1,530 mm)"]), ("Y-axis travel", ["120.1″ (3,050 mm)"]),
            ("Z-axis travel", ["15.4″ (390 mm)"]), ("X / Y-axis positioning accuracy", ["±0.002″ (±0.05 mm)"]),
            ("X / Y-axis repeated positioning accuracy", ["±0.0008″ (±0.02 mm)"]), ("Maximum speed", ["656 ft/min (200 m/min)"]),
            ("Maximum acceleration", ["2.8 G"]), ("Dimensions (length × width × height)", ["27.7 × 7.4 × 7.7 ft (8,440 × 2,270 × 2,340 mm)"]),
            ("Maximum load of workbench", ["6,614 lb (3,000 kg)"]), ("Total weight", [lb(6230), lb(6700), lb(6770), lb(7150)]), ("Phase", ["Three-phase"]),
            ("Rated voltage of power supply", ["380 V" + VOLT_NOTE]), ("Frequency", ["50 Hz"]), ("Power supply protection grade", ["IP54"])]
    trs = "".join(f"<tr><th>{l}</th>" + (f'<td colspan="4">{v[0]}</td>' if len(v) == 1 else "".join(f"<td>{x}</td>" for x in v)) + "</tr>" for l, v in rows)
    body = (title("02 · Technical parameters", "Technical parameters · SF3015H")
            + f'<table class="kv spec3"><thead><tr><th>Items</th>{"".join(f"<th>{p}</th>" for p in pw)}</tr></thead><tbody>{trs}</tbody></table>'
            + '<p class="small-note">1. The accuracy of the workpiece depends to some extent on factors such as workpiece type, preparation, sheet size and position.</p>'
            + '<p class="small-note">2. The technical parameters are subject to change without notice; the final technical parameters are subject to the order agreement.</p>'
            + D.included())
    b.page("Technical parameters", body, key="tech")
    cut_page(b, data, 5, (0, 1), "1 of 3")
    cut_page(b, data, 5, (1, 2), "2 of 3")
    cut_page(b, data, 6, None, "3 of 3")
    body = (title("05 · Cost-benefit analysis", "Cost-benefit analysis · SF3015H")
            + P("If the cutting auxiliary gas is dried compressed air, the cost is the air compressor's electricity consumption + the machine "
                "tool's electricity consumption + consumables (protective lenses and nozzles).", cls="sm")
            + cost_table(pw, [32, 45.5, 57, 90], [18, 27, 28, 35], ["22", "/", "/", "22", "/", "/", "37", "/", "/", "37", "/", "/"], 22, 3,
                         ["0.5", "4.5", "60.5"], [97, 75, 75, 119.5, 97.5, 97.5, 147, 110, 110, 187, 150, 150],
                         [58.2, 45, 45, 71.7, 58.5, 58.5, 88.2, 66, 66, 112.2, 90, 90],
                         [58.7, 49.5, 105.5, 72.2, 63, 119, 88.7, 70.5, 126.5, 112.7, 94.5, 150.5], unit="RMB/h")
            + '<p class="small-note">1. The electricity and gas prices are Senfeng\'s reference values in China (RMB) and may vary from region to region.</p>'
              '<p class="small-note">2. The auxiliary gas consumption differs with plate thickness. The oxygen column takes 0.984″ (25 mm) carbon steel as an '
              "example and the nitrogen column 0.039″ (1 mm) stainless steel; the values are for reference only and subject to actual use.</p>" + D.included())
    b.page("Cost-benefit analysis", body, key="cost")
    adv = [("Positioning accuracy", "0.016″ (0.4 mm) — especially a 33 ft (10 m) bed", "0.0055″ (0.14 mm) — especially a 33 ft (10 m) bed", "High precision"),
           ("Section taper", "0.20″ (5 mm) — especially 1.575″ (40 mm) thick", "0.016″ (0.4 mm) — especially 1.575″ (40 mm) thick, 20 kW and above",
            "No need for fine processing"),
           ("Kerf", "0.16 – 0.24″ (4 – 6.0 mm)", "0.008 – 0.063″ (0.2 – 1.6 mm)", "Saves 6 – 9% of material"),
           ("Bleed and co-edge", "0.39″ (10 mm)", "0.12 – 0.16″ (3 – 4 mm)", "Saves 6 – 9% of material"),
           ("Heat-affected zone", "0.020 – 0.079″ (0.5 – 2.0 mm)", "0.004 – 0.016″ (0.1 – 0.4 mm)", "Less heat absorption, less deformation"),
           ("Cutting effect", "Average", "Excellent, less slag", "No need for sanding"), ("Cutting speed", "Average", "Very fast", "High production efficiency"),
           ("Piercing", "Can't cut small holes", "Diameter-to-depth ratio of 10 – 20%", "Saves drilling and handling"),
           ("Working environment", "Smoky", "Clean", "Healthy and environmentally friendly")]
    trs = "".join(f"<tr><th>{a}</th><td>{p}</td><td>{l}</td><td><b>{v}</b></td></tr>" for a, p, l, v in adv)
    body = (title("06 · Advantages of laser cutting", "Laser cutting vs. plasma cutting · SF3015H")
            + f'<table class="kv"><thead><tr><th>Items</th><th>Plasma cutting</th><th>Laser cutting</th><th>Laser cutting advantages</th></tr></thead><tbody>{trs}</tbody></table>'
            + D.included())
    b.page("Laser cutting advantages", body, key="adv")
    body = (title("07 · Configuration list", "Configuration list · SF3015H")
            + conf_table([("Laser source", [(1, "Laser source", 1, "Raycus")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "BOCI")]),
                          ("Machine tool · host", [(1, "Transmission system", 4, "Taiwan LAPPING / SENFENG"), (2, "Machine tool and accessories", 1, "SENFENG"),
                                                   (3, "Machine bed burn-proof parts", 1, "Graphite (optional refractory bricks)"), (4, "Reducer", 3, "Japan SHIMPO"),
                                                   (5, "Electrical and pneumatic systems", 1, "France SCHNEIDER · Japan SMC &amp; Taiwan AirTAC"),
                                                   (6, "AC servo motor and driver", 4, "Japan Fuji Electric"), (7, "Water chiller", 1, "HANLI")]),
                          ("CNC system", [(1, "CNC system", 1, "FSCUT 8000")])],
                         ["This is the optimal configuration verified by Senfeng. Changing the brand or configuration may cause irreversible effects.",
                          "Warranty: NovoTech's 1-year warranty on the entire machine (excluding consumables, force majeure natural disasters, wars and "
                          "violations, human damage and other reasons)."]) + D.included())
    b.page("Configuration", body, key="config")
    body = (title("08 · Cutting samples", "Cutting samples · SF3015H")
            + grid([f'<div style="height:118pt;display:flex;align-items:center;justify-content:center"><img src="{D.im(S + f"sample-{i}.jpg", 900)}" '
                    f'style="max-width:100%;max-height:100%;object-fit:contain"></div>' for i in range(1, 9)], 2, 14))
    b.page("Cutting samples", body, key="samples")
    body = (title("09 · Laser device", "SF3015H laser source")
            + row(fig(S + "h4-source-12.jpg", "RFL-C12000", h=230, px=700), fig(S + "h4-source-20.jpg", "RFL-C20000", h=230, px=800),
                  fig(S + "h4-source-30.jpg", "RFL-C30000", h=230, px=800), gap=12)
            + '<div class="stats" style="margin:12pt 0"><div><b>12 – 30 kW optional</b><span>Raycus fiber laser sources</span></div></div>'
            + '<ol class="num">' + "".join(f"<li>{x}</li>" for x in ["Small core diameter (50 – 300 µm optional) and excellent beam quality", "Efficient cutting",
                                                                     "Power-saving: electro-optical conversion efficiency &gt; 40%", "Precise and controllable",
                                                                     "Lightweight", "Highly customizable", "Smooth operation, safe and durable"]) + "</ol>"
            + D.included())
    b.page("Laser source", body, key="source")
    head = ["<b>Cutting head anti-collision design.</b> Customers can replace the anti-collision components themselves without replacing the "
            "cutting head, reducing the probability of returning it to the factory.",
            "<b>Protective lens temperature monitoring.</b> If the lens is contaminated, the system immediately alarms and shuts down to avoid "
            "damage to the cutting head, lenses, etc.",
            "<b>Real-time monitoring of the air pressure.</b> If the air is insufficient or the pressure too low or unstable, the system alarms immediately.",
            "<b>Real-time detection of the stray-light value of the lower protective lens against explosion.</b> If the threshold is exceeded, it alarms in time.",
            "<b>Pan-seal failure detection.</b> Real-time detection of the gas pressure in the lower 1 and lower 2 protective lens cavities ensures stable production.",
            "<b>Process monitoring.</b> If a cut is not complete, the head automatically cuts back.",
            "<b>Intelligent piercing.</b> Cutting starts immediately after the hole is penetrated, improving efficiency and protecting the machine tool.",
            "<b>Intelligent retraction.</b> The sensor determines the retraction automatically to avoid cutting lumps and damage to the workpiece.",
            "<b>Co-edge piercing monitoring.</b> When thermal deformation or misalignment of the plate is detected, the piercing procedure runs "
            "automatically, increasing the service life of the lens."]
    body = (title("10 · Laser head", "SF3015H laser head")
            + row(fig(S + "h4-head-15.jpg", "12 – 15 kW", h=200, px=600), fig(S + "h4-head-20.jpg", "20 kW", h=200, px=600),
                  fig(S + "h4-head-30.jpg", "30 kW", h=200, px=600), gap=12)
            + '<ol class="num" style="margin-top:8pt">' + "".join(f"<li>{x}</li>" for x in head) + "</ol>")
    b.page("Laser head", body, key="head")
    body = (title("11 · Machine bed system", "SF3015H machine bed system")
            + row(h2("Heavy-duty heat-isolated hollow bed", "higher processing efficiency")
                  + P("<b>Technology</b> — welding is followed by stress-relief annealing, secondary aging treatment and precision machining on a "
                      "very large gantry milling machine, so the bed is stable and shock-resistant enough to withstand high acceleration.",
                      "<b>Feature</b> — the bed has no internal connections, which prevents heat transfer and loss of accuracy during cutting and "
                      "ensures long-term use without deformation, improving its service life.", cls="sm"),
                  fig(S + "h4-bed.jpg", h=200, px=1400), cols="1fr 1.1fr", gap=16, align="center")
            + row(fig(S + "h4-beam.jpg", h=170, px=1400),
                  h2("Aviation-grade high-strength aluminum beam", "strong structural stability · strong impact resistance")
                  + P("<b>Technology</b> — the beam is made of high-strength aviation-grade aluminum alloy and undergoes extrusion, quenching, heat "
                      "aging treatment and precision machining. It has excellent rigidity and surface quality and is corrosion-resistant, "
                      "lightweight, rigid and tough thanks to the properties of aluminum alloy.",
                      "<b>Feature</b> — the internal structure is optimized by finite element analysis for perfect dynamic performance during "
                      "high-speed laser cutting, so various shapes are cut at high speed while accuracy is kept.", cls="sm"),
                  cols="1.1fr 1fr", gap=16, align="center") + D.included())
    b.page("Machine bed system", body, key="bed")
    body = (title("12 · Machine bed system", "SF3015H machine bed system")
            + row(h2("Intelligent surrounding spiral negative pressure dust removal", "green and smart")
                  + P("<b>Core</b> — the dust removal system divides the cutting area into sections and exhausts in a time-sharing, zonal and "
                      "segmented manner according to the current cutting position.",
                      "<b>Feature</b> — it is also equipped with a sealed bottom structure to achieve smoke-free cutting.", cls="sm"),
                  fig(S + "h4-dust.jpg", h=230, px=1400), cols="1fr 1.1fr", gap=16, align="center")
            + h2("Pneumatic system", "precise control")
            + P("<b>Core</b> — the gas system is equipped with SMC and AirTAC control valves and proportional regulating valves from well-known "
                "brands, which control the pressure and flow of each gas electrically.",
                "<b>Feature</b> — auxiliary cutting gases: O₂, N₂, compressed air, etc.", cls="sm") + D.included())
    b.page("Machine bed system", body, key="dust")
    gases = [("Nitrogen (300 psi)", "Adjustable between 15 and 435 psi (0.1 – 3 MPa)"), ("Oxygen", "Adjustable between 7 and 131 psi (0.05 – 0.9 MPa)"),
             ("Compressed air", "Adjustable between 15 and 435 psi (0.1 – 3 MPa)")]
    body = (title("13 · Automatic gas distribution device", "Precise gas control")
            + fig(S + "h4-gas.jpg", "Automatic gas distribution device for the auxiliary gas", h=250, fit="cover", px=1240)
            + '<div class="chips" style="grid-template-columns:repeat(3,1fr)">' + "".join(f"<div>{t}<br><small style='text-transform:none;font:400 8pt Barlow'>{s}</small></div>" for t, s in gases) + "</div>"
            + '<div style="height:8pt"></div>'
            + P("Equipped with two different gases, nitrogen (air) and oxygen. Each gas circuit can be individually controlled for flow and pressure.")
            + checks(["The equipment software terminal selects the auxiliary gas automatically.",
                      "The type and pressure of the auxiliary gas are set and selected automatically through the numerical control program, without manual operation.",
                      "The actual pressure at the outlet of the cutting head is read and displayed on the panel instantly."]) + D.included())
    b.page("Gas distribution", body, key="gas")
    body = (title("14 · Numerical control system", "Storm cutting system — FSCUT8000")
            + fig(S + "h4-fscut.jpg", h=200, fit="cover", px=1600)
            + h2("Convenient operation and efficient cutting")
            + P("The FSCUT8000 high-end intelligent bus system is designed specifically for ultra-high-power laser cutting of 8 kW and above. It is "
                "stable, reliable, easy to deploy, simple to debug, safe to operate, well-featured and superior in performance. It supports "
                "modular, personalized, automated and digital solutions and is currently the most high-end bus laser cutting system on the "
                "market. It has a memory cache, a powerful cutting technology database and cutting parameters for various thicknesses and plate "
                "materials, for fast and efficient cutting.", cls="sm")
            + checks(["Native DXF, G-code and other drawing formats processed directly; high-speed reading, writing and processing of the LXDS and NRP files generated by CypNest.",
                      "A cutting process parameter database allows real-time adjustment of the parameters during cutting for optimal cutting quality.",
                      "Contactless piercing for thin sheets, lightning-fast piercing for thick plates, multi-stage piercing, slag removal, vibration "
                      "suppression, closed-loop gas pressure control and fine process control by layer segmentation greatly improve the efficiency "
                      "and stability of high-power cutting.",
                      "Optimized rapid movement modes, with the “Leap Frog” function and automatic closing of the auxiliary gas during non-cutting moves."], cls="sm"))
    b.page("CNC system", body, key="cnc")
    body = (title("15 · Numerical control system", "Nesting software — CypNest")
            + fig(S + "h4-cypnest.jpg", h=190, fit="cover", px=1600)
            + h2("Automatic programming to improve the utilization rate")
            + P("The SF3015H CNC laser cutting machine is equipped with CypNest, a professional nesting software with automatic programming, nesting, "
                "layout, text processing and process configuration, maximizing sheet metal management and utilization. Its features:", cls="sm")
            + checks(["Lead-in, piercing, micro-joints, cutting sequence, optimized cutting path and optimized speed, etc.",
                      "A fast, high-utilization nesting algorithm reduces material waste. No upper limit to the number of nested plates; automatic, "
                      "manual and mixed manual + automatic nesting; automatic and manual nesting of special-shaped plates.",
                      "Inter-part gap nesting, embedded nesting, symmetric-flip nesting, rotational nesting and avoidance of shape overlaps and "
                      "collisions improve material utilization.",
                      "Minimized tool travel, fast manual sorting options and several shared-edge toolpath modes for different scenarios.",
                      "Co-edge segment cutting optimizes cutting efficiency and improves sheet utilization.",
                      "Different cutting processes are applied automatically from user-defined material and thickness settings — compensation radius, "
                      "piercing time, cutting power, lead-in method, micro-joints and bridging.",
                      "Processing orders, quotation documents and other statistical reports; fully compatible with the HypCut / CypCut cutting processes."], cls="sm"))
    b.page("CypNest", body, key="cypnest")
    tr = [("Before the equipment is shipped", "The buyer can arrange 1 – 2 operators to Senfeng's factory or exhibition hall for a one-week "
           "training; the time is set by Senfeng's customer service department."),
          ("Equipment warranty", "The buyer can also send another 1 – 2 operators to Senfeng for free training."),
          ("Training", "Laser principle, equipment structure, process description, equipment maintenance, laser safety protection, operating "
           "procedures and simple troubleshooting."),
          ("Requirement", "Trainees are mechanical, electrical or optical assistant engineers or engineers, who operate the machine after passing "
           "the assessment of equipment operation, laser principles, laser safety and maintenance.")]
    pk = [("Packing", "Standard packaging, suitable for long-distance road transport, moisture-proof, rust-proof and shock-proof, with the lifting "
           "center of gravity and lifting points marked for lifting the whole."),
          ("Shipping", "Road transport within China: Senfeng is responsible for freight and insurance."),
          ("Packing list and certificate", "A detailed packing list and quality certificate are attached to each packing box, with the equipment "
           "instructions and all other documents. The packing list is outside the box and the certificate inside.")]
    inst = [("Equipment installation", "The delivery place is the installation site of your company; NovoTech engineers, with Senfeng, install the equipment."),
            ("Equipment test", "After installation, debugging ensures the normal function of the equipment."),
            ("On-site training", "Training on equipment maintenance, safety protection, operating procedures and simple troubleshooting at the "
             "customer's site for 7 days to ensure normal use."),
            ("On-site acceptance", "The engineer leaves after the customer's on-site acceptance (the customer can veto).")]
    body = (title("16 · After-sale service", "Training · packaging · installation")
            + h2("Personnel training", "to improve production efficiency") + steps(tr)
            + h2("Packaging and transportation", "to ensure the equipment quality")
            + row(fig(S + "pack-1.jpg", h=62, fit="cover", px=700), fig(S + "pack-2.jpg", h=62, fit="cover", px=700), fig(S + "pack-3.jpg", h=62, fit="cover", px=700), gap=10)
            + '<div style="height:5pt"></div>' + steps(pk).replace("repeat(4,1fr)", "repeat(3,1fr)")
            + h2("Equipment installation", "professional and high-quality") + steps(inst))
    b.page("After-sale service", body, key="training")
    body = (title("17 · Customization service", "Honour · enjoy · customized")
            + fig(S + "h4-custom.jpg", h=170, fit="cover", px=1240)
            + P("In the digital age, the intelligent transformation of the metal processing industry is imperative, and building a fully automatic "
                "factory is the only way to achieve it. Customized metal forming automation solutions become a top priority.", cls="sm")
            + '<div class="pat"><div><b>05</b><span>International PCT patents</span></div><div><b>520</b><span>Domestic technology patents</span></div></div>'
            + '<div style="height:8pt"></div>'
            + P("The core components — laser generator, laser processing head and laser numerical control system — have been developed by Senfeng "
                "and are widely used in cutting, welding, cladding and automation. Senfeng has built a whole industry chain integrating cutting, "
                "bending, welding, cladding and automation, covering laser cutting, welding, cladding and cleaning equipment, bending centers and "
                "flexible laser processing lines, widely used in power towers, construction machinery, shipbuilding, bridge formwork, aerospace "
                "and other industries. With these strengths, Jinan Senfeng Laser Technology helps enterprises shorten the production cycle and "
                "save manufacturing costs, for greater economic benefit in the competition.", cls="sm")
            + h2("Custom standards")
            + steps([("Understand", "Understand the customer's industry and specific production situation; identify problems and understand the customer's needs."),
                     ("Exchange", "In-depth exchanges with the customer on site, and metal forming automation solutions customized to their pain points and needs."),
                     ("Differ", "Significantly different from competitors' models — the most suitable solution is formulated."),
                     ("Deliver", "Following the customized plan, R&amp;D and production from drawings to complete machines, controlling every procedure until the customer is satisfied.")]))
    b.page("Customization", body, key="custom")
    body = (title("18 · Five star service", "5-star service in quick response")
            + fig(S + "h4-service.jpg", h=170, fit="cover", px=1240)
            + P("Jinan Senfeng Laser Technology adheres to the concept of “customer first” and provides high-quality global services with dedicated "
                "and professional quality. During the epidemic it did not back down and solved problems for customers in time, which won the "
                "favor and trust of customers at home and abroad.", cls="sm")
            + row(h2("Efficient") + checks(["24 hours a day, 7 days a week, 365 days a year to answer repair calls.",
                                           "Within 10 minutes a professional technical engineer replies; 1 hour to decide the maintenance plan; 1 working day to dispatch engineers."], cls="sm"),
                  h2("Professional") + checks(["Exclusive customized service: a service plan for each customer's specific situation.",
                                              "Service engineer certification: every service engineer works with a certificate after strict training and assessment.",
                                              "FAQ training: an FAQ for each equipment model, with certified engineers training customers.",
                                              "Online one-to-one guidance: experienced senior engineers guide customers by telephone, video and other network channels.",
                                              "Once is good: the equipment is debugged correctly once, and similar problems are repaired once."], cls="sm"),
                  h2("Reliable") + checks(["Pre-service: theory + practical operation training, self-diagnosis training for common faults, quick "
                                          "repair guidance for difficult faults, reminders of usage precautions.",
                                          "Regular service: regular maintenance reminders, regular door-to-door service, regular promotions.",
                                          "Value-added services: hardware and software upgrades, financial leasing and extended warranty."], cls="sm"),
                  gap=14))
    b.page("Five-star service", body, key="service")
    b.back("Fiber laser for your shop.", [S + "h4-machine.jpg", S + "h4-head-30.jpg", S + "h4-bed.jpg", S + "sample-7.jpg"])
    toc_page(b, [("01 · Model", "model"), ("02 · Technical parameters", "tech"), ("03 · Cutting parameters — stainless steel", "cut1 of 3"),
                 ("03 · Cutting parameters — carbon steel", "cut2 of 3"), ("04 · Cutting parameters — brass, aluminum", "cut3 of 3"),
                 ("05 · Cost-benefit analysis", "cost"), ("06 · Advantages of laser cutting", "adv"), ("07 · Configuration list", "config"),
                 ("08 · Cutting samples", "samples"), ("09 · Laser source", "source"), ("10 · Laser head", "head"), ("11 – 12 · Machine bed system", "bed"),
                 ("13 · Automatic gas distribution", "gas"), ("14 · CNC system — FSCUT8000", "cnc"), ("15 · Nesting software — CypNest", "cypnest"),
                 ("16 · Training, packing and shipping, installation", "training"), ("17 · Metal forming customization service", "custom"),
                 ("18 · Five-star service", "service")],
             "Full technical specification · SF3015H · 12 – 30 kW")
    return b



# ======================================================================================== SF1530NP, 3 – 6 kW (the owner, Nov 1 2026)
def after_sales(b, first_no, cust_prefix, n_cust=16):
    """the after-sales pages shared by Senfeng's technical solutions: automated fabrication solutions, training / packaging /
    installation, premium customization, five-star fast service, customer testimonials"""
    n = first_no
    body = (title(f"{n} · After-sales service", "Providing global users with automated metal fabrication solutions")
            + row(P("Senfeng provides automated metal fabrication solutions globally, integrating cutting, bending, welding, cladding, automation "
                    "and new energy. With core technologies in laser cutting, welding and cladding, the company also offers intelligent "
                    "manufacturing systems such as flexible laser processing lines and panel benders. These solutions serve industries including "
                    "automotive, construction, energy and petrochemicals, and are used in over 100 countries."),
                  fig(S + "solutions.jpg", h=230, px=1000), cols="1fr 1fr", gap=18, align="center")
            + '<div class="pat"><div><b>03</b><span>International PCT patents</span></div><div><b>577</b><span>Chinese technology patents</span></div></div>'
            + '<div style="height:10pt"></div>'
            + P("Senfeng has developed key components such as laser generators, processing heads, the Feng Cloud system and CNC systems, used in "
                "cutting, welding, cladding and automation. The company offers a complete industry chain, including laser cutting, welding, "
                "cladding and cleaning machines, bending centers and flexible production lines. These solutions are used in sectors such as power "
                "towers, construction machinery, shipbuilding, bridges and aerospace, helping businesses accelerate production and reduce costs for "
                "greater economic benefit.") + D.included())
    b.page("After-sales service", body, key="solutions")
    pack = [("Packaging", "Standard packaging, suitable for long-distance transportation, moisture-proof, rust-proof and shock-resistant. Designed "
             "for full lifting, with marked lifting points and center of gravity."),
            ("Transportation", "Domestic transportation within China is fully handled by Senfeng, including freight and insurance."),
            ("Packing list &amp; certificate", "Each package includes a packing list and a certificate of conformity. The user manual and other "
             "documents are inside the box; the packing list is on the outside.")]
    body = (title(f"{n + 1} · After-sales service", "Training · packaging · installation")
            + h2("Technical training", "to enhance customer production efficiency") + steps(TRAINING)
            + h2("Packaging &amp; transportation", "to ensure equipment quality")
            + row(fig(S + "pack-1.jpg", h=62, fit="cover", px=700), fig(S + "pack-2.jpg", h=62, fit="cover", px=700), fig(S + "pack-3.jpg", h=62, fit="cover", px=700), gap=10)
            + '<div style="height:5pt"></div>' + steps(pack).replace("repeat(4,1fr)", "repeat(3,1fr)")
            + h2("Installation", "professional and high-quality") + steps(INSTALL))
    b.page("After-sales service", body, key="training")
    cust = [("custom-1.jpg", "Senfeng understands the client's industry status and specific production processes, identifies issues and assesses their needs."),
            ("custom-2.jpg", "Through in-depth on-site communication, metal fabrication automation solutions are customized to the client's pain points and needs."),
            ("custom-3.jpg", "A tailored solution, different from competitors' standardized models."),
            ("custom-4.jpg", "A one-stop R&amp;D and production service from design to final machine, with thorough quality checks until customer "
             "satisfaction and acceptance.")]
    body = (title(f"{n + 2} · After-sales service", "Premium customization")
            + P("In the digital era, intelligent transformation in metal processing is essential. Building unmanned factories is key to "
                "upgrading, with customized automation solutions a top priority.")
            + grid([fig(S + f, h=150, fit="cover", px=1000) + P(f"<b>{i:02d}</b> · {t}", cls="sm") for i, (f, t) in enumerate(cust, 1)], 2, 16)
            + D.included())
    b.page("Customization", body, key="custom")
    body = (title(f"{n + 3} · After-sales service", "Five-star fast service")
            + fig(S + "service-bg.jpg", h=150, fit="cover", px=1600)
            + row(h2("Efficient") + checks(["Senfeng's repair hotline is available 24/7.",
                                           "A professional engineer responds to customer inquiries within 10 minutes and provides a repair plan within 1 hour."], cls="sm"),
                  fig(S + "service-1.jpg", h=92, fit="cover", px=700), cols="1.6fr 1fr", gap=14, align="center")
            + row(h2("Professional") + checks(["<b>Custom service:</b> service plans tailored to the customer's specific needs.",
                                              "<b>Service engineer certification:</b> each service engineer is rigorously trained and assessed before being certified to work.",
                                              "<b>Common issues training:</b> a manual of common issues for each equipment model, with certified engineers training customers.",
                                              "<b>Online guidance:</b> experienced senior engineers support customers by phone or video call.",
                                              "<b>Professional technical support:</b> the equipment is properly calibrated at the first installation, and similar issues are resolved in one go."], cls="sm"),
                  row(fig(S + "service-2.jpg", h=70, fit="cover", px=700), fig(S + "service-3.jpg", h=70, fit="cover", px=700), cols="1fr", gap=6),
                  cols="1.6fr 1fr", gap=14, align="center")
            + row(h2("Comprehensive") + checks(["<b>Pre-service:</b> theoretical and hands-on operation training, common fault self-diagnosis training, "
                                               "quick repair guidance and usage reminders.",
                                               "<b>Regular service:</b> regular maintenance reminders, on-site services and periodic promotional activities.",
                                               "<b>Value-added service:</b> equipment software and hardware upgrades, financing lease services and extended warranty services."], cls="sm"),
                  fig(S + "service-4.jpg", h=92, fit="cover", px=700), cols="1.6fr 1fr", gap=14, align="center"))
    b.page("Five-star service", body, key="service")
    body = (title(f"{n + 4} · After-sales service", "Customer testimonials")
            + P("Senfeng machines and customers around the world.", cls="sm")
            + '<div class="cust">' + "".join(f'<img src="{D.im(S + f"{cust_prefix}{i:02d}.jpg", 600)}">' for i in range(1, n_cust + 1)) + "</div>")
    b.page("Testimonials", body, key="cust")


def book_np():
    data = json.load(open(os.path.join(HERE, "data-senfeng-sf1530np-cutting.json")))
    b = D.Book("sf-np", "SF1530NP fiber laser — full technical specification", "Senfeng · the new-generation NP series · 3 &amp; 6 kW",
               os.path.join(ROOT, "src", "files", "NovoTech-Senfeng-SF1530NP-Fiber-Laser-Technical-Specification-2026.pdf"))
    b.title = "Senfeng SF1530NP Fiber Laser — Full Technical Specification — NovoTech Machine Tools"
    b.subject = "Senfeng SF1530NP compact fiber laser cutting machine, 3 and 6 kW — full technical specification, imperial edition"
    b.cover("Senfeng · full technical specification", "SF1530NP · the new-generation NP series · 3 &amp; 6 kW", "SF1530NP fiber laser",
            "Technical specification", "Fiber laser cutting machine", S + "np-cover.jpg",
            [("10 × 5 ft", "Working area"), ("3 &amp; 6 kW", "Maxphotonics source"), ("328 ft/min", "Maximum speed"), ("1 G", "Maximum acceleration")],
            hero_h=320, minis=[S + "np-head-6kw.jpg", S + "np-source-1.jpg", S + "np-bed.jpg", S + "np-builtin.jpg"])
    b.page("Contents", "@@TOC@@", sub="Contents")
    feats = ["High-strength machine tool bed", "High-strength aluminum alloy beam", "Fully automatic focusing technology", "Intelligent following system"]
    body = (title("01 · Model · the new-generation NP series", "SF1530NP")
            + P("Fiber laser cutting machine.", cls="sm")
            + row(fig(S + "np-machine.jpg", h=270, px=1600), fig(S + "campus.jpg", "Senfeng's campus in Jinan, China", h=270, px=900), cols="1.6fr 1fr", gap=14)
            + '<div class="feat">' + "".join(f"<div><b>{i}</b>{t}</div>" for i, t in enumerate(feats, 1)) + "</div>"
            + P("*The image is for reference only; the appearance and dimensions are subject to the actual product from the factory.", cls="note")
            + D.included())
    b.page("Model", body, key="model")
    pw = ["3 kW", "6 kW"]
    rows = [("Working area (L × W)", ["10 × 5 ft (3,000 × 1,500 mm)"]), ("X-axis travel", ["119.3″ (3,030 mm)"]), ("Y-axis travel", ["59.4″ (1,510 mm)"]),
            ("Z-axis travel", ["5.1″ (130 mm)"]), ("X / Y axis positioning accuracy", ["±0.002″ (±0.05 mm)"]),
            ("X / Y axis repeated positioning accuracy", ["±0.0008″ (±0.02 mm)"]), ("Maximum speed", ["328 ft/min (100 m/min)"]),
            ("Maximum acceleration", ["1 G"]), ("Dimensions (L × W × H)", ["16.1 × 7.3 × 7.6 ft (4,921 × 2,225 × 2,317 mm)"]),
            ("Maximum load", ["2,425 lb (1,100 kg)"]), ("Weight", [lb(4709), lb(5230) + "<br><small>including fire bricks</small>"]), ("Phase", ["Three-phase"]),
            ("Power supply rated voltage", ["380 V" + VOLT_NOTE]), ("Frequency", ["50 / 60 Hz"]), ("Overall power supply protection level", ["IP54"])]
    trs = "".join(f"<tr><th>{l}</th>" + (f'<td colspan="2">{v[0]}</td>' if len(v) == 1 else "".join(f"<td>{x}</td>" for x in v)) + "</tr>" for l, v in rows)
    body = (title("02 · Technical parameters", "Technical parameters · SF1530NP")
            + f'<table class="kv spec3"><thead><tr><th>Item</th>{"".join(f"<th>{p}</th>" for p in pw)}</tr></thead><tbody>{trs}</tbody></table>'
            + '<p class="small-note">1. Workpiece accuracy depends on factors like type, pre-treatment, sheet size and position.</p>'
            + '<p class="small-note">2. Technical parameters are subject to change without notice. Final parameters are based on the order agreement.</p>'
            + D.included())
    b.page("Technical parameters", body, key="tech")
    cut_page(b, data, 5, (0, 1), "1 of 3")     # Senfeng's page 03 (stainless + carbon) on two pages so the tables fit
    cut_page(b, data, 5, (1, 2), "2 of 3")
    cut_page(b, data, 6, None, "3 of 3")
    body = (title("05 · Cost-benefit analysis", "Cost-benefit analysis · SF1530NP")
            + P("If the cutting auxiliary gas is dried compressed air, the cost includes the air compressor's electricity, the machine's power "
                "consumption and the consumables (protective lenses, cutting nozzles).", cls="sm")
            + cost_table(pw, [10, 16], [3, 6], ["15", "/", "/"] * 2, 7, 1.5, ["0.5", "4.5", "60.5"], [37, 22, 22, 46, 31, 31],
                         [22.2, 13.2, 13.2, 27.6, 18.6, 18.6], [22.7, 17.7, 73.7, 28.1, 23.1, 79.1])
            + '<p class="small-note">1. The electricity and gas prices are Senfeng\'s reference values in China (RMB) and may vary by region.</p>'
            + '<p class="small-note">2. Auxiliary gas consumption varies with plate thickness; the values are based on 0.630″ (16 mm) carbon steel for '
              "oxygen and 0.039″ (1 mm) stainless steel for nitrogen, for reference.</p>" + D.included())
    b.page("Cost-benefit analysis", body, key="cost")
    body = (title("06 · Configuration list", "Configuration list · SF1530NP")
            + conf_table([("Laser source", [(1, "Laser source", 1, "Maxphotonics")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "RayTools")]),
                          ("Machine tool &amp; host", [(1, "Transmission system", 4, "SENFENG"), (2, "Machine tool and accessories", 1, "SENFENG"),
                                                     (3, "Reducer", 3, "SHIMPO, Japan"), (4, "Electrical and pneumatic systems", 1, "SCHNEIDER, France · XINGYU ELECTRON"),
                                                     (5, "AC servo motor and driver", 4, "SCHNEIDER, France"), (6, "Water chiller", 1, "HANLI")]),
                          ("CNC cutting system", [(1, "CNC laser system", 1, "FSCUT")])],
                         ["This is Senfeng's optimized configuration. Changes in brand or configuration may cause irreversible effects.",
                          "The warranty period for the entire machine (excluding consumables, force majeure natural disasters, war, improper operation "
                          "and human damage) is 1 year."]) + D.included())
    b.page("Configuration", body, key="config")
    heads = row(fig(S + "np-head-3kw.jpg", "3 kW and below", h=200, px=600), fig(S + "np-head-6kw.jpg", "4 – 6 kW", h=200, px=600), gap=14)
    body = (title("07 · Core components", "Laser source · laser head")
            + h2("SF1530NP laser source")
            + row(row(fig(S + "np-source-1.jpg", h=95, px=700), fig(S + "np-source-2.jpg", h=95, px=700), gap=10),
                  '<ol class="num">' + "".join(f"<li>{x}</li>" for x in ["High-power and high-quality laser output", "Uniformly distributed beam energy",
                                                                         "Excellent performance and strong processing ability",
                                                                         "Compact structure and maintenance-free", "Wide range of applications"]) + "</ol>",
                  cols="1.3fr 1fr", gap=16, align="center")
            + h2("SF1530NP laser head")
            + row(heads, '<ol class="num">' + "".join(f"<li>{x}</li>" for x in [
                "<b>Superior design:</b> optimized optical configuration and smooth, efficient airflow significantly improve cutting quality and efficiency.",
                "<b>Auto focus:</b> automatic focusing minimizes manual intervention, with a focus range of −0.47″ to +0.39″ (−12 to +10 mm) and a "
                "positioning accuracy of 0.002″ (0.05 mm).",
                "<b>Multiple protective lenses:</b> an additional protective lens safeguards the collimating lens, extending its service life.",
                "<b>Drawer-type lens holder:</b> fast and easy replacement of the protective lenses.",
                "<b>High compatibility:</b> multiple fiber interfaces, including QBH and QD, for a wide range of mainstream laser sources."]) + "</ol>",
                  cols="1fr 1.25fr", gap=16, align="center"))
    b.page("Laser source · head", body, key="source")
    body = (title("08 · Machine bed system", "SF1530NP machine bed system")
            + fig(S + "np-front.jpg", h=230, px=1400)
            + row(h2("1 · Brand-new appearance") + checks(["The machine has an integrated screen and a platform leg-support design; the platform "
                                                          "frame has transfer balls for easier loading."], cls="sm"),
                  h2("2 · Fully enclosed lift door") + checks(["Improves the main unit's sealing and the dust removal. CE protective acrylic laser "
                                                              "shields; the lift door has safety locks on both sides for personnel safety."], cls="sm"), gap=18)
            + D.included())
    b.page("Machine bed system", body, key="bed")
    bed = [("3", "Tube welding bed", "durable and non-deformable", S + "np-bed.jpg", [
                "The reinforced welded bed frame is designed for high-speed movement, with aging treatment for precision and stability in long-term operation.",
                "The bed frame is annealed to eliminate internal stress and increase rigidity, then given secondary vibration aging and precision machining.",
                "The semi-hollow bed frame reduces thermal deformation, extends service life and keeps the cutting accurate."]),
           ("4", "High-strength aluminum alloy beam", "light weight and good dynamic performance", S + "np-beam.jpg", [
                "The high-strength aluminum alloy beam is lightweight and has excellent dynamic performance.",
                "The beam is precision-machined after secondary vibration aging, ensuring its overall strength and stability."]),
           ("5", "Intelligent spiral negative pressure dust removal", "green and smart manufacturing", S + "np-dust.jpg", [
                "The dust removal system controls the exhaust vents from the current cutting position, with time-based, zoned and segmented ventilation.",
                "With the return-type sealing structure at the bottom of the base, it achieves smoke-free cutting."]),
           ("6", "Visual monitoring safety protection", "ensures personal safety", S + "np-monitor.jpg", [
                "The all-around monitoring system significantly reduces blind spots, so cutting runs safely and stably."])]
    cards = [card(img, f"{n} · {t}", checks(x, cls="sm"), sub=sb, h=100) for n, t, sb, img, x in bed]
    body = title("09 · Machine bed system", "SF1530NP machine bed system") + grid(cards[:2], 2, 18) + '<div style="height:8pt"></div>' + grid(cards[2:], 2, 18)
    b.page("Machine bed system", body, key="bed2")
    bed2 = [("7", "Thermostatic electric control cabinet", "makes laser cutting more stable", S + "np-cabinet.jpg", [
                 "The temperature-controlled electrical cabinet eliminates the need for an air-conditioned room.",
                 "The constant-temperature, constant-humidity interior adapts the equipment to various conditions.",
                 "It significantly extends the life of the control system's electronic components, ensuring stable cutting."]),
            ("8", "Fully enclosed lift door", "green and environmentally friendly", S + "np-builtin.jpg", ["Built-in laser source saves valuable floor space."]),
            ("9", "Modular Z axis", "safety protection, easy maintenance", S + "np-zaxis.jpg", [
                 "The Z axis is modular, with excellent sealing that resists contamination and lowers the failure rate.",
                 "Modular installation and replacement significantly reduce maintenance time and difficulty."]),
            ("10", "Internal material cart", "easy to clean", S + "np-cart.jpg", [
                 "The material cart has an internal compartment, which makes collecting waste material and cleaning more convenient."])]
    cards = [card(img, f"{n} · {t}", checks(x, cls="sm"), sub=sb, h=100) for n, t, sb, img, x in bed2]
    body = title("10 · Machine bed system", "SF1530NP machine bed system") + grid(cards[:2], 2, 18) + '<div style="height:8pt"></div>' + grid(cards[2:], 2, 18)
    b.page("Machine bed system", body, key="bed3")
    labels = [("Nitrogen (300 psi)", "Adjustable 15 – 435 psi (0.1 – 3 MPa)", 23.3, 36.8), ("Oxygen", "Adjustable 7 – 131 psi (0.05 – 0.9 MPa)", 35.1, 69.3),
              ("Compressed air", "Adjustable 15 – 435 psi (0.1 – 3 MPa)", 83.3, 60.2)]
    gas = (f'<div class="lab" style="height:300pt"><img src="{D.im(S + "h3-gas.jpg", 1600)}">'
           + "".join(f'<div class="gasl" style="left:{x}%;top:{y}%"><b>{t}</b><span>{s}</span></div>' for t, s, x, y in labels) + "</div>")
    body = (title("11 · Auto gas distribution system", "Precise control of each gas flow") + gas
            + P("The CNC laser cutting machine has two separate gas lines: nitrogen (air) and oxygen. Each gas line can be independently "
                "controlled for flow rate and pressure.")
            + checks(["The equipment software terminal has an automatic auxiliary gas selection feature.",
                      "The type and pressure of the auxiliary gases are set and selected automatically through the CNC program — no manual operation.",
                      "The actual gas pressure at the cutting head outlet is read and displayed on the panel in real time."]) + D.included())
    b.page("Gas distribution", body, key="gas")
    body = (title("12 · CNC system", "SF1530NP CNC system") + fig(S + "h3-cnc.jpg", "Bus cutting system — quick operation &amp; efficient cutting", h=200, px=1400)
            + P("This intelligent bus system is designed specifically for fiber laser cutting. It integrates motion control, laser source control "
                "and cutting gas control, offering stability, reliability, easy deployment, simple debugging, production safety and a rich set of "
                "features with excellent performance. It offers modular, customizable, automated and informational solutions. The system has "
                "memory buffering and a comprehensive cutting process database with optimized parameters for various materials and thicknesses, "
                "for fast operation and efficient cutting — ideal for sheet metal, kitchenware and lighting.")
            + checks(["Supported file formats: direct processing of DXF files and high-speed reading and writing of LXDS and NRP files generated by CypNest.",
                      "A cutting database allows real-time adjustments during cutting for optimal processing quality.",
                      "Multi-stage piercing, sharp-corner entry and centering significantly improve high-power cutting efficiency and stability.",
                      "Optimized rapid travel modes, including the “LeapFrog” function."]) + D.included())
    b.page("CNC system", body, key="cnc")
    after_sales(b, 13, "np-cust-")
    b.back("Fiber laser for your shop.", [S + "np-machine.jpg", S + "np-front.jpg", S + "np-head-6kw.jpg", S + "np-bed.jpg"])
    toc_page(b, [("01 · Model", "model"), ("02 · Technical parameters", "tech"), ("03 · Cutting parameters — stainless steel", "cut1 of 3"),
                 ("03 · Cutting parameters — carbon steel", "cut2 of 3"), ("04 · Cutting parameters — brass, aluminum", "cut3 of 3"), ("05 · Cost-benefit analysis", "cost"), ("06 · Configuration list", "config"),
                 ("07 · Laser source, laser head", "source"), ("08 – 10 · Machine bed system", "bed"), ("11 · Auto gas distribution system", "gas"),
                 ("12 · CNC system", "cnc"), ("13 · Automated metal fabrication solutions", "solutions"),
                 ("14 · Personnel training, packaging and transportation, installation", "training"), ("15 · Customization", "custom"),
                 ("16 · Five-star fast service", "service"), ("17 · Customer testimonials", "cust")],
             "Full technical specification · SF1530NP · 3 &amp; 6 kW")
    return b


# ======================================================================================== SF1313G catalogue (the owner, Nov 1 2026)
def book_g13():
    b = D.Book("sf-1313g", "SF1313G compact fiber laser", "Senfeng · 4 × 4 ft · 1.5 – 3 kW · compact-sized single-platform sheet laser",
               os.path.join(ROOT, "src", "files", "NovoTech-Senfeng-SF1313G-Fiber-Laser-2026.pdf"))
    b.title = "Senfeng SF1313G Compact Fiber Laser — NovoTech Machine Tools"
    b.subject = "Senfeng SF1313G compact-sized single-platform sheet laser cutting machine, 4 × 4 ft, 1.5 – 3 kW — imperial edition"
    b.cover("Senfeng · SF1313G", "Cutting · welding · cleaning · cladding · bending · milling · automation", "SF1313G · 1.5 – 3 kW",
            "Compact fiber laser", "Compact-sized single-platform sheet laser cutting machine", SF + "sf-1313g-2.jpg",
            [("4 × 4 ft", "Working area"), ("1.5 – 3 kW", "Laser power"), ("262 ft/min", "Max. no-load speed"), ("485 lb", "Max. platform load")],
            hero_h=330, minis=[SF + "sf-1313g-4.jpg", S + "g13-table.jpg", S + "g13-head.jpg", S + "g13-container.jpg"])
    body = (title("SF1313G · 1.5 – 3 kW", "Compact-sized single-platform sheet laser cutting machine")
            + row(P("This machine has a small body and fits to cut pony-size, relatively thin and light-weight sheet. With it, users enjoy small "
                    "metal workpieces at high precision.")
                  + '<div class="feat" style="grid-template-columns:1fr">' + "".join(f"<div><b>{i}</b>{t}</div>" for i, t in enumerate(
                      ["Fully-enclosed structure", "Sidewise push-pull platform", "Only needs a 20 ft (20GP) container", "Zoning smoke exhaust system"], 1)) + "</div>",
                  fig(S + "g13-scene.jpg", h=420, fit="cover", px=1400), cols="1fr 1fr", gap=18)
            + '<div class="chips">' + "".join(f"<div>{x}</div>" for x in ["Cutting", "Welding", "Cleaning", "Cladding", "Bending", "Milling · automation"]) + "</div>"
            + D.included())
    b.page("SF1313G", body)
    spec = kv([("Laser power", "1.5 – 3 kW"), ("Working area (L × W)", "4 × 4 ft (1,300 × 1,300 mm)"),
               ("X / Y-axis positioning accuracy", "±0.002″ (±0.05 mm)"), ("X / Y-axis repositioning accuracy", "±0.0008″ (±0.02 mm)"),
               ("Max. no-load speed", "262 ft/min (80 m/min)"), ("Max. load of platform", "485 lb (220 kg)"),
               ("Overall dimensions (L × W × H)", "117.5 × 85.0 × 78.7″ (2,985 × 2,160 × 2,000 mm)"),
               ("Power supply", "Three-phase 380 V, 50 / 60 Hz" + VOLT_NOTE)], head=["Model", "SF1313G"])
    body = title("Specifications", "SF1313G technical parameters") + fig(S + "g13-hero.jpg", h=200, fit="cover", px=1864) + '<div style="height:10pt"></div>' + spec + D.included()
    b.page("Specifications", body)
    head = (f'<div class="lab" style="height:190pt"><img src="{D.im(S + "g13-head.jpg", 900)}" style="object-fit:cover">'
            '<div class="gasl" style="left:70%;top:82%"><b>Cuts sheet up to 0.787″ (20 mm) thick</b></div></div>')
    body = (title("Precision · high-reflectivity metals", "Cut thin sheet at high precision")
            + row(P("Laser energy precise-control technology takes accurate control of the laser beam output, entirely based on the sheet "
                    "thickness. Thin sheet is free from overburning or burr, and the cut section is much smoother."), head, cols="1fr 1.2fr", gap=18, align="center")
            + h2("Also deals with high-reflectivity metals")
            + row(P("The custom-made laser generator is small, light and compactly designed. With the new generation of laser pumping source and "
                    "optical elements, it has a high anti-back-reflection ability while cutting aluminum, stainless steel, copper and other "
                    "high-reflectivity metals.")
                  + '<div class="stats" style="margin-top:8pt"><div><b>Anti-back-reflection</b><span>modules</span></div><div><b>&gt; 40%</b>'
                    '<span>electro-optical conversion rate</span></div></div>',
                  fig(S + "g13-samples.jpg", h=210, px=1000), cols="1.2fr 1fr", gap=18, align="center") + D.included())
    b.page("Precision", body)
    green = [("Fully-enclosed structure", "Equipped with a top cover to form a fully-enclosed structure and prevent laser radiation.", "g13-enclosed.jpg"),
             ("Keep the workshop clean", "Its zoning smoke exhaust system synchronizes smoke exhaust and cutting to prevent its diffusion.", "g13-table.jpg"),
             ("Make loading &amp; unloading easier", "Its sidewise push-pull platform not only saves space, but also makes loading and unloading "
              "easier for further efficiency gains.", "g13-loading.jpg")]
    body = (title("Shipping · safe and green production", "Make easy overseas shipment")
            + P("The mini model is much smaller than others of the same type. Thanks to its small footprint, the workshop is better used, and "
                "overseas transport is more flexible at lower freight cost.")
            + row('<div class="stp" style="grid-template-columns:1fr"><div><b>01</b><div class="ittl">Machine size</div><p>117.5 × 85.0 × 78.7″ '
                  "(2,985 × 2,160 × 2,000 mm) (L × W × H)</p></div><div><b>02</b><div class='ittl'>Easily packed in a 20 ft (20GP) container</div></div></div>",
                  fig(S + "g13-container.jpg", h=120, px=1000), cols="1fr 1.6fr", gap=16, align="center")
            + h2("Carry out safe and green production")
            + grid([card(S + f, t, P(x, cls="sm"), h=110) for t, x, f in green], 3, 14) + D.included())
    b.page("Shipping · production", body)
    body = (title("Company profile", "Senfeng Laser")
            + P("SENFENG Laser Technology Co., Ltd., founded in 2004 as a globe-spanning metal forming manufacturer, has devoted itself to laser "
                "cutting, welding, bending, cleaning, cladding, flexible automation and new energy for years.",
                "During production, all its machines go through natural aging, heat treatment, shot blasting, powder coating, finish machining, "
                "quality inspection and many other professional treatments so they keep working for a long time.")
            + fig(S + "g13-campus.jpg", "Senfeng's campus in Jinan, China", h=230, fit="cover", px=1000)
            + row(fig(S + "g13-building.jpg", h=130, fit="cover", px=700), fig(S + "g13-showroom.jpg", h=130, fit="cover", px=700), gap=12)
            + P("Note: the pictures and parameters are for reference only; the actual product prevails. Senfeng catalogue, January 2025. "
                "Sold, installed and serviced in Canada by NovoTech Machine Tools.", cls="note") + D.included())
    b.page("Company profile", body)
    b.back("Fiber laser for your shop.", [SF + "sf-1313g-front.jpg", S + "g13-enclosed.jpg", S + "g13-head.jpg", S + "g13-samples.jpg"])
    return b


# ======================================================================================== SF3015HM tube and plate, 1.5 – 6 kW (the owner, Nov 1 2026)
def book_hm():
    data = json.load(open(os.path.join(HERE, "data-senfeng-sf3015hm-cutting.json")))
    b = D.Book("sf-hm", "SF3015HM tube and plate fiber laser — full technical specification", "Senfeng · tube and plate laser cutting machine · 1.5 – 6 kW",
               os.path.join(ROOT, "src", "files", "NovoTech-Senfeng-SF3015HM-Tube-Plate-Laser-Technical-Specification-2026.pdf"))
    b.title = "Senfeng SF3015HM Tube and Plate Laser — Full Technical Specification — NovoTech Machine Tools"
    b.subject = "Senfeng SF3015HM tube and plate fiber laser cutting machine, 1.5 – 6 kW — full technical specification, imperial edition"
    b.cover("Senfeng · full technical specification", "SF3015HM · tube and plate laser cutting machine · 1.5 – 6 kW", "SF3015HM",
            "Technical specification", "Tube and plate laser cutting machine", S + "hm-machine.jpg",
            [("10 × 5 ft", "Working area"), ("Ø0.8 – 8.7″", "Tube diameter"), ("427 ft/min", "Maximum speed"), ("1 G", "Maximum acceleration")],
            hero_h=300, minis=[S + "hm-head-6kw.jpg", S + "hm-source-1.jpg", S + "hm-bed.jpg", S + "hm-zaxis.jpg"])
    b.page("Contents", "@@TOC@@", sub="Contents")
    feats = ["High-strength machine tool bed", "Aircraft-grade aluminum beam", "One machine, double the functionality, efficiency multiplied",
             "Automatic following technology"]
    body = (title("01 · Model · tube &amp; plate cutting", "SF3015HM")
            + P("Medium power laser cutting machine.", cls="sm")
            + row(fig(S + "hm-machine.jpg", h=250, px=1600), fig(S + "hm-campus.jpg", "Senfeng's campus in Jinan, China", h=250, px=900), cols="1.7fr 1fr", gap=14)
            + '<div class="feat">' + "".join(f"<div><b>{i}</b>{t}</div>" for i, t in enumerate(feats, 1)) + "</div>"
            + P("*The image is for reference only; the appearance and dimensions are subject to the actual product from the factory.", cls="note")
            + D.included())
    b.page("Model", body, key="model")
    pw = ["1.5 kW", "2 kW", "3 kW", "4 kW", "6 kW"]
    rows = [("Working area (L × W)", ["120.1 × 60.2″ (3,050 × 1,530 mm)"]), ("X-axis travel", ["60.2″ (1,530 mm)"]), ("Y-axis travel", ["120.1″ (3,050 mm)"]),
            ("Z-axis travel", ["13.0″ (330 mm)"]), ("Tube length", ["1.6 – 19.7 ft (500 – 6,000 mm)"]), ("Tube diameter", ["Ø0.8 – 8.7″ (Ø20 – 220 mm)"]),
            ("X / Y axis positioning accuracy", ["±0.002″ (±0.05 mm)"]), ("X / Y axis repeated positioning accuracy", ["±0.0008″ (±0.02 mm)"]),
            ("Maximum speed", ["427 ft/min (130 m/min)"]), ("Maximum acceleration", ["1 G"]),
            ("Dimensions (L × W × H)", ["30.5 × 11.4 × 7.2 ft (9,300 × 3,460 × 2,180 mm)"]), ("Maximum load", ["2,425 lb (1,100 kg)"]),
            ("Weight", [lb(7100), lb(7110), lb(7130), lb(7190), lb(7190)]), ("Phase", ["Three-phase"]),
            ("Power supply rated voltage", ["380 V" + VOLT_NOTE]), ("Frequency", ["50 Hz"]), ("Overall power supply protection level", ["IP54"])]
    trs = "".join(f"<tr><th>{l}</th>" + (f'<td colspan="5">{v[0]}</td>' if len(v) == 1 else "".join(f"<td>{x}</td>" for x in v)) + "</tr>" for l, v in rows)
    body = (title("02 · Technical parameters", "Technical parameters · SF3015HM")
            + f'<table class="kv spec3 spec5"><thead><tr><th>Item</th>{"".join(f"<th>{p}</th>" for p in pw)}</tr></thead><tbody>{trs}</tbody></table>'
            + '<p class="small-note">1. Workpiece accuracy depends on factors like type, pre-treatment, sheet size and position.</p>'
            + '<p class="small-note">2. Technical parameters are subject to change without notice. Final parameters are based on the order agreement.</p>'
            + D.included())
    b.page("Technical parameters", body, key="tech")
    cut_page(b, data, 5, (0, 1), "1 of 3")     # Senfeng's page 03 (stainless + carbon) on two pages so the tables fit
    cut_page(b, data, 5, (1, 2), "2 of 3")
    cut_page(b, data, 6, None, "3 of 3")
    body = (title("05 · Cost-benefit analysis", "Cost-benefit analysis · SF3015HM")
            + P("If the cutting auxiliary gas is dried compressed air, the cost includes the air compressor's electricity, the machine's power "
                "consumption and the consumables (protective lenses, cutting nozzles).", cls="sm")
            + cost_table(pw, [5, 6, 10, 16, 16], [3, 3, 3, 6, 6], ["15", "/", "/"] * 5, 12, 3, ["0.5", "4.5", "60.5"],
                         [38, 23, 23, 39, 24, 24, 43, 28, 28, 52, 37, 37, 52, 37, 37],
                         [22.8, 13.8, 13.8, 23.4, 14.4, 14.4, 25.8, 16.8, 16.8, 31.2, 22.2, 22.2, 31.2, 22.2, 22.2],
                         [23.3, 18.3, 74.3, 23.9, 18.9, 74.9, 26.3, 21.3, 77.3, 31.7, 26.7, 82.7, 31.7, 26.7, 82.7])
            + '<p class="small-note">1. The electricity and gas prices are Senfeng\'s reference values in China (RMB) and may vary by region.</p>'
            + '<p class="small-note">2. Auxiliary gas consumption varies with plate thickness; the values are based on 0.630″ (16 mm) carbon steel for '
              "oxygen and 0.039″ (1 mm) stainless steel for nitrogen, for reference.</p>" + D.included())
    b.page("Cost-benefit analysis", body, key="cost")
    body = (title("06 · Configuration list", "Configuration list · SF3015HM")
            + conf_table([("Laser source", [(1, "Laser source", 1, "Max")]), ("Laser cutting head", [(1, "Laser cutting head", 1, "Raytools")]),
                          ("Machine tool &amp; host", [(1, "Transmission system", 4, "SENFENG"), (2, "Machine tool and accessory", 1, "SENFENG"),
                                                     (3, "Reducer", 3, "SHIMPO, Japan"), (4, "Electrical and pneumatic systems", 1, "SCHNEIDER, France · AVENTICS, Germany"),
                                                     (5, "AC servo motor and driver", 4, "Fuji Electric, Japan"), (6, "Water chiller", 1, "Hanli")]),
                          ("CNC cutting system", [(1, "CNC laser cutting system", 1, "FSCUT")])],
                         ["This is Senfeng's optimized configuration. Changes in brand or configuration may cause irreversible effects.",
                          "The warranty period for the entire machine (excluding consumables, force majeure natural disasters, war, improper operation "
                          "and human damage) is 1 year."]) + D.included())
    b.page("Configuration", body, key="config")
    heads = row(fig(S + "hm-head-3kw.jpg", "1.5 – 3 kW", h=190, px=600), fig(S + "hm-head-6kw.jpg", "4 – 6 kW", h=190, px=600), gap=14)
    body = (title("07 · Core components", "Laser source · laser head")
            + h2("SF3015HM laser source")
            + row(row(fig(S + "hm-source-1.jpg", h=95, px=700), fig(S + "hm-source-2.jpg", h=95, px=700), gap=10),
                  '<ol class="num">' + "".join(f"<li>{x}</li>" for x in ["High-power and high-quality laser output", "Uniformly distributed beam energy",
                                                                         "Excellent performance and strong processing ability",
                                                                         "Compact structure and maintenance-free", "Wide range of applications"]) + "</ol>",
                  cols="1.3fr 1fr", gap=16, align="center")
            + h2("SF3015HM laser head")
            + row(heads, '<ol class="num">' + "".join(f"<li>{x}</li>" for x in [
                "<b>Efficient cooling:</b> the collimating and focusing lenses have cooling structures, and the nozzle has a cooling airflow that "
                "protects the nozzle and the ceramic body and extends operating time.",
                "<b>Fast focusing:</b> collimated focusing moves faster and over a larger adjustment range than traditional focusing.",
                "<b>Multiple protective lenses:</b> four protective lenses reduce contamination when the fiber and the lower protective lenses are "
                "changed, extending the life of the collimating and focusing lenses.",
                "<b>Optimized structure:</b> the integrated body is sealed; improved QBH, QD and G5 fiber interfaces fit more laser sources and "
                "prevent jamming from rust or water leaks."]) + "</ol>",
                  cols="1fr 1.25fr", gap=16, align="center"))
    b.page("Laser source · head", body, key="source")
    bed = [("1", "High-strength machine tool bed", S + "hm-bed.jpg", [
                "The high-strength machine bed is welded from high-quality steel plates and tubes.",
                "After welding it is stress-relief annealed, given a secondary aging treatment and precision-machined on a large milling machine, "
                "for structural stability and vibration resistance under high acceleration.",
                "The bed has no internal connections, which blocks heat transfer and keeps cutting heat from affecting the machining accuracy — "
                "long-term resistance to deformation and a longer service life."]),
           ("2", "Aircraft-grade high-strength aluminum beam", S + "hm-beam.jpg", [
                "The beam is made of aerospace-grade high-strength aluminum alloy — extruded, quenched and aged — for rigidity, surface quality, "
                "corrosion resistance and light, durable construction.",
                "The internally optimized structure gives excellent dynamic performance at high speed, keeping the precision for cutting all shapes."]),
           ("3", "Pneumatic system", S + "hm-pneumatic.jpg", [
                "Control valves and proportional regulators from AVENTICS control the pressure and flow of each gas path electrically.",
                "Cutting auxiliary gases: O₂, N₂, compressed air and others."]),
           ("4", "Plate and tube cutting in one machine", S + "hm-machine.jpg", [
                "The SF3015HM cuts both plate and tube, doubling efficiency."])]
    cards = [card(img, f"{n} · {t}", checks(x, cls="sm"), h=100) for n, t, img, x in bed]
    body = title("08 · Machine bed system", "SF3015HM machine bed system") + grid(cards[:2], 2, 18) + '<div style="height:8pt"></div>' + grid(cards[2:], 2, 18)
    b.page("Machine bed system", body, key="bed")
    bed2 = [("5", "Intelligent spiral negative-pressure dust removal system", S + "hm-dust.jpg", [
                 "Smart control of the exhaust vents from the cutting position, with timed, zoned and sectional ventilation.",
                 "The U-shaped sealed base at the bottom keeps the cutting smoke-free."]),
            ("6", "Modular Z-axis", S + "hm-zaxis.jpg", [
                 "The Z axis is modular, with good sealing that prevents contamination and lowers the failure rate.",
                 "Modular installation and replacement greatly reduce maintenance time and difficulty."])]
    cards = [card(img, f"{n} · {t}", checks(x, cls="sm"), h=150) for n, t, img, x in bed2]
    body = title("09 · Machine bed system", "SF3015HM machine bed system") + grid(cards, 2, 18) + D.included()
    b.page("Machine bed system", body, key="bed2")
    labels = [("Nitrogen (300 psi)", "Adjustable 15 – 435 psi (0.1 – 3 MPa)", 23.3, 36.8), ("Oxygen", "Adjustable 7 – 131 psi (0.05 – 0.9 MPa)", 35.1, 69.3),
              ("Compressed air", "Adjustable 15 – 435 psi (0.1 – 3 MPa)", 83.3, 60.2)]
    gas = (f'<div class="lab" style="height:300pt"><img src="{D.im(S + "h3-gas.jpg", 1600)}">'
           + "".join(f'<div class="gasl" style="left:{x}%;top:{y}%"><b>{t}</b><span>{s}</span></div>' for t, s, x, y in labels) + "</div>")
    body = (title("10 · Auto gas distribution system", "Precise control of each gas flow") + gas
            + P("The CNC laser cutting machine has two separate gas lines: nitrogen (air) and oxygen. Each gas line can be independently "
                "controlled for flow rate and pressure.")
            + checks(["The equipment software terminal has an automatic auxiliary gas selection feature.",
                      "The type and pressure of the auxiliary gases are set and selected automatically through the CNC program — no manual operation.",
                      "The actual gas pressure at the cutting head outlet is read and displayed on the panel in real time."]) + D.included())
    b.page("Gas distribution", body, key="gas")
    body = (title("11 · CNC system", "SF3015HM CNC system") + fig(S + "h3-cnc.jpg", "Bus cutting system — quick operation &amp; efficient cutting", h=200, px=1400)
            + P("This intelligent bus system is designed specifically for fiber laser cutting. It integrates motion control, laser source control "
                "and cutting gas control, offering stability, reliability, easy deployment, simple debugging, production safety and a rich set of "
                "features with excellent performance. It offers modular, customizable, automated and informational solutions. The system has "
                "memory buffering and a comprehensive cutting process database with optimized parameters for various materials and thicknesses, "
                "for fast operation and efficient cutting — ideal for sheet metal, kitchenware and lighting.")
            + checks(["Supported file formats: direct processing of DXF files and high-speed reading and writing of LXDS and NRP files generated by CypNest.",
                      "A cutting database allows real-time adjustments during cutting for optimal processing quality.",
                      "Multi-stage piercing, sharp-corner entry and centering significantly improve high-power cutting efficiency and stability.",
                      "Optimized rapid travel modes, including the “LeapFrog” function."]) + D.included())
    b.page("CNC system", body, key="cnc")
    after_sales(b, 12, "hm-cust-")
    b.back("Fiber laser for your shop.", [S + "hm-machine.jpg", S + "hm-head-6kw.jpg", S + "hm-bed.jpg", S + "hm-zaxis.jpg"])
    toc_page(b, [("01 · Model", "model"), ("02 · Technical parameters", "tech"), ("03 · Cutting parameters — stainless steel", "cut1 of 3"),
                 ("03 · Cutting parameters — carbon steel", "cut2 of 3"), ("04 · Cutting parameters — brass, aluminum", "cut3 of 3"),
                 ("05 · Cost-benefit analysis", "cost"), ("06 · Configuration list", "config"), ("07 · Laser source, laser head", "source"),
                 ("08 – 09 · Machine bed system", "bed"), ("10 · Auto gas distribution system", "gas"), ("11 · CNC system", "cnc"),
                 ("12 · Automated metal fabrication solutions", "solutions"), ("13 · Personnel training, packaging and transportation", "training"),
                 ("14 · Installation and customization", "custom"), ("15 · Five-star fast service", "service"), ("16 · Customer testimonials", "cust")],
             "Full technical specification · SF3015HM · 1.5 – 6 kW")
    return b

BOOKS = {"g3": book_g3, "g4": book_g4, "np": book_np, "g13": book_g13, "hm": book_hm}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")] or list(BOOKS)
    for k in args:
        D.build(BOOKS[k](), "--html" in sys.argv)
