#!/usr/bin/env python3
"""NovoTech edition of the ULE 3015 quotation sheet (double table fiber laser cutting machine, ULE3015-6000W) — the full
technical specification of the value-line ULE, every page, picture and detail of the original in NovoTech's catalogue format,
units in imperial (metric in brackets).  The owner, Nov 1 2026: "make a full technical specification PDF in NovoTech format from
this PDF, imperial units, and a 'Download full technical specifications' button next to 'Download PDF brochure'".

    python3 tools/brochure/ule_spec_edition.py [--html]     → src/files/NovoTech-ULE-Fiber-Laser-Technical-Specification-2026.pdf

The ULE is sold under NovoTech's name (value line, built in China to North American standards), so the supplier's name, logos and
address do not appear: its company profile is the manufacturing partner's, the "ADH" entries of the configuration table are
NovoTech's in-house parts, "Party B" is NovoTech, and the supplier's address page is NovoTech's back cover.  Logos on helmets,
jackets, the factory building and the console's model strip are filled (images: tools/src-images/ule-spec/, the site's
value-laser photos for the components).
Adapted, and why: the after-sales warranty line states NovoTech's 1-year warranty (the supplier's sheet says 1–3 years, which
NovoTech does not offer as standard); the factory's "delivery within 20 days" is its ship-from-factory time; the operating
voltage keeps the factory's 380 V / 50 Hz with NovoTech's 600 V CSA panel noted; the compressed-air line's dew point is blank in
the original (NovoTech confirms it); translation slips are corrected (Cpycut → CypCut, "megawatt-level" → 10 kW-class, Linear
Quide → Linear Guide) and one misprint in the copper table (3 mm at 1,000 W: "0.5-10" → 0.5 – 1.0 m/min).
Cutting speeds: inches per minute with the original metres per minute below; thicknesses in decimal inches with the millimetres.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dener_laser_editions as D   # noqa: E402

ROOT = D.ROOT
U = os.path.join(ROOT, "tools", "src-images", "ule-spec") + "/"
V = os.path.join(ROOT, "tools", "src-images", "value-laser") + "/"
OUT = os.path.join(ROOT, "src", "files", "NovoTech-ULE-Fiber-Laser-Technical-Specification-2026.pdf")
title, P, checks, h2, h3, fig, row, grid, card, kv, mtable = D.title, D.P, D.checks, D.h2, D.h3, D.fig, D.row, D.grid, D.card, D.kv, D.mtable

# the value line: NovoTech's own brand, built in China
D.INCLUDED[:] = [("Built in China to North American standards", False), ("CSA-approved electrical panel", False), ("1-year warranty", False),
                 ("<b>7-day money-back guarantee</b> (in-stock machines only)", False),
                 ("Spare parts &amp; technical support readily available in Canada", False),
                 ("<b>Order Today with Just 10% Down — 0% Down Financing Available</b>", False), ("<b>Installation and training available</b>", False)]
D.DISCLAIMER = ("Specifications subject to change without notice. Imperial values are converted from the manufacturer's metric data and "
                "rounded: sheet thicknesses in decimal inches, cutting speeds in inches per minute. Model numbers are manufacturer designations. "
                "Photos may show optional equipment.")
D.CSS += """
.mt.cut{font-size:8pt}
.mt.cut th,.mt.cut td{padding:3.1pt 3pt;line-height:1.12}
.mt.cut thead th{font-size:8pt;padding:5pt 3pt}
.mt.cut td small,.mt.cut th small{display:block;font-size:6.6pt;color:#8c8e91;margin-top:.6pt}
.mt.cut tbody th{text-align:center;font-weight:600}
.s2{display:grid;grid-template-columns:1fr 1fr;row-gap:9pt;padding:11pt 12pt}
.s2 b{font-size:18pt}
.s2 span{font-size:7.2pt;letter-spacing:.06em;text-transform:none}
.irow.sm{padding:6pt 10pt;margin-bottom:7pt;gap:11pt}
.irow.sm .ico{width:40pt;height:40pt;flex:0 0 40pt}
.irow.sm p{font-size:8.6pt;line-height:1.35}
.det{display:grid;grid-template-columns:1fr 218pt;gap:16pt;align-items:center;border-bottom:.8pt solid #e2e3e5;padding:0 0 9pt;margin:0 0 9pt}
.det:last-child{border-bottom:0}
.det h2{margin-top:0}
.det .checks li{font-size:8.9pt;line-height:1.38;margin-bottom:5pt}
.det .im{border:.6pt solid #e2e3e5}
.kv.cmp th,.kv.cmp td{padding:4.3pt 8pt;font-size:8.8pt}
.kv.cmp tbody th{font-size:8.8pt}
.req td,.req th{font-size:8.2pt;padding:3.6pt 7pt}
.req tbody th{width:122pt;font-size:8.2pt}
.req td:first-child{width:22pt;text-align:center}
.req ul{margin:0;padding-left:10pt}
.req li{margin:0 0 2pt}
.svc .cim{border:.6pt solid #e2e3e5}
.svc .cim img{width:100%;height:100%;object-fit:cover}
.svc .checks li{font-size:8.2pt;line-height:1.33}
"""

POWER = [1000, 1500, 2000, 3000, 4000, 6000, 8000, 10000]
# metres per minute, exactly as in the quotation's comparison tables (pages 10 and 11); "/" = not applicable
CUT = {
    "cs": ("Carbon steel", "oxygen", [
        (1, "8.0-10 15-26 24-30 30-40 33-43 35-44 35-42 35-42"), (2, "4.0-6.5 4.5-6.5 4.7-6.5 4.8-7.5 15-25 20-28 6.2-10 7.0-12"),
        (3, "2.4-3.0 2.6-4.0 3.0-4.8 3.3-5.0 7.0-12 13-17 4.0-7.0 4.2-7.5"), (4, "2.0-2.4 2.5-3.0 2.8-3.5 3.0-4.2 3.0-4.0 3.0-4.5 3.5-5.5 3.5-5.5"),
        (5, "1.5-2.0 2.0-2.5 2.2-3.0 2.6-3.5 2.7-3.6 3.0-4.2 3.3-4.5 3.3-4.5"), (6, "1.4-1.6 1.6-2.2 1.8-2.6 2.3-3.2 2.5-3.4 2.5-3.5 3.0-4.2 3.0-4.2"),
        (8, "0.8-1.2 1.0-1.4 1.2-1.8 1.8-2.6 2.0-3.0 2.2-3.2 2.5-3.5 2.5-3.5"), (10, "0.6-1.0 0.8-1.1 1.1-1.3 1.2-2.0 1.5-2.4 1.8-2.5 2.2-2.7 2.2-2.7"),
        (12, "0.5-0.8 0.7-1.0 0.9-1.2 1.0-1.6 1.2-1.8 1.2-2.0 1.2-2.1 1.2-2.1"), (14, "/ 0.5-0.7 0.7-0.8 0.9-1.4 0.9-1.2 1.2-1.8 1.7-1.9 1.7-1.9"),
        (16, "/ / 0.6-0.7 0.7-1.0 0.8-1.0 0.8-1.3 0.9-1.7 0.9-1.7"), (18, "/ / 0.4-0.6 0.6-0.8 0.6-0.9 0.6-0.9 0.65-0.9 0.65-0.9"),
        (20, "/ / / 0.5-0.8 0.5-0.8 0.5-0.8 0.6-0.9 0.6-0.9"), (22, "/ / / / 0.4-0.8 0.4-0.8 0.5-0.8 0.5-0.8"),
        (25, "/ / / / / 0.3-0.55 0.3-0.7 0.3-0.7")]),
    "ss": ("Stainless steel", "nitrogen", [
        (1, "15-25 20-27 24-30 30-35 32-45 42-52 50-66 60-75"), (2, "5-7.5 8.0-12 9.0-15 13-21 16-28 20-33 30-42 40-55"),
        (3, "1.8-2.5 3.0-5.0 4.0-6.5 6.0-10 7.0-15 15-22 20-30 27-38"), (4, "1.2-1.3 1.5-2.4 3.0-4.5 4.0-6.0 5.0-8.0 10.0-15.0 14-21 18-25"),
        (5, "0.6-0.7 0.7-1.3 1.8-2.5 3.0-5.0 3.5-5.0 8.0-12 12-17 15-22"), (6, "/ 0.7-1.0 1.2-2.0 2.0-4.0 2.5-4.5 4.8-8.0 8.0-14.0 12-15"),
        (8, "/ / 0.7-1.0 1.5-2.0 1.2-2.0 3.0-4.0 6.0-8.0 8.0-12.0"), (10, "/ / / 0.6-0.8 0.8-1.2 1.6-2.5 3.0-5.0 6.0-8.0"),
        (12, "/ / / 0.4-0.6 0.5-0.8 0.8-1.5 1.8-3.0 3.0-5.0"), (14, "/ / / / 0.4-0.6 0.6-0.8 1.2-1.8 1.8-3.0"),
        (20, "/ / / / / 0.3-0.55 0.6-0.7 1.2-1.8"), (25, "/ / / / / 0.2-0.4 0.5-0.6 0.6-0.7")]),
    "al": ("Aluminum sheet", "nitrogen", [
        (1, "6.0-10.0 10.0-20.0 15-25 25-38 35-45 42-55 50-65 60-75"), (2, "2.8-3.5 5.0-7.0 7-10.0 10.0-18.0 13-24 20-40 25-38 33-45"),
        (3, "0.7-1.5 2.0-4.0 4.0-6.0 6.5-8.0 7.0-13 15-25 20-30 25-35"), (4, "/ 1.0-1.5 2.0-3.0 3.5-5.0 4.0-5.5 9.5-12.0 13-18 21-30"),
        (5, "/ 0.7-1.0 1.2-1.8 2.5-3.5 3.0-4.5 5.0-8.0 9.0-12 13-20"), (6, "/ / 0.7-1.0 1.5-2.5 2.0-3.5 3.8-5.0 4.5-8.0 9.0-12"),
        (8, "/ / 0.6-0.8 0.7-1.0 0.9-1.6 2.0-2.5 4.0-6.0 4.5-8.0"), (10, "/ / / 0.4-0.7 0.6-1.2 1.0-1.5 2.2-3.0 4.0-6.0"),
        (12, "/ / / 0.3-0.45 0.4-0.6 0.8-1.0 1.5-2.0 2.2-3.0"), (16, "/ / / / 0.3-0.4 0.5-0.8 1.0-1.6 1.5-2.0"),
        (20, "/ / / / / 0.5-0.7 0.7-1.0 1.0-1.6"), (25, "/ / / / / 0.3-0.5 0.5-0.7 0.7-1.0"), (30, "/ / / / / / / 0.5-0.7"),
        (40, "/ / / / / / / /"), (50, "/ / / / / / / /")]),
    "cu": ("Copper sheet", "nitrogen", [
        (1, "6.0-10.0 8.0-13 10.0-16.0 20-35 25-35 35-45 55-65 65-75"), (2, "2.8-3.6 3.0-4.5 4.5-7.5 6.0-10 8.0-12 20-30 30-40 33-45"),
        (3, "0.5-1.0 1.5-2.5 2.5-4.0 4.0-6.0 5.0-8.0 12-18 20-30 25-40"), (4, "/ 1.0-1.6 1.5-2.0 3.0-5.0 3.2-5.5 5.0-8.0 10-18 14-24"),
        (5, "/ 0.5-0.7 0.9-1.2 1.5-2.0 2.0-3.0 4.5-6.0 7.0-9.0 9.0-15"), (6, "/ / 0.4-0.7 1.0-1.8 1.4-2.0 3.0-4.5 4.5-6.5 7.0-9.0"),
        (8, "/ / / 0.5-0.7 0.7-1.2 1.6-2.2 2.4-4.0 4.5-6.5"), (10, "/ / / / 0.2-0.5 0.8-1.2 1.5-2.2 2.4-4.0"),
        (12, "/ / / / / 0.3-0.5 0.8-1.5 1.5-2.2")]),
}


def thk(mm):
    return f"{mm / 25.4:.3f}″<small>{mm} mm</small>"


def speed(cell):
    if cell == "/":
        return "—"
    a, b = cell.split("-")
    lo, hi = round(float(a) * 39.3701), round(float(b) * 39.3701)
    return f"{lo:,} – {hi:,}<small>{a} – {b}</small>"


def cut_page(b, key, n):
    name, gas, rows = CUT[key]
    t = mtable([f"{w:,} W" for w in POWER], [(thk(mm), "", [speed(c) for c in vals.split()]) for mm, vals in rows], corner="Thickness", cls="cut")
    body = (title(f"Comparison table of cutting parameters · {n} of 4", f"{name} · {gas}")
            + P(f"Cutting speed by laser source power, in inches per minute; the metres per minute of the factory's table are given below "
                f"each value. {name}, {gas} assist gas. “—” = not cut at that power.", cls="sm")
            + t + D.included())
    b.page("Cutting parameters", body, key=key)


def det(name, items, img, h=150, sub=""):
    return (f'<div class="det"><div>{h2(name, sub)}{checks(items)}</div>'
            f'<div>{fig(img, h=h, fit="contain", px=1200)}</div></div>')


def book():
    b = D.Book("ule-spec", "ULE fiber laser — full technical specification", "Double table fiber laser cutting machine · ULE-3015 · 6,000 W", OUT)
    b.title = "NovoTech ULE Fiber Laser — Full Technical Specification — NovoTech Machine Tools"
    b.subject = "NovoTech ULE-3015 6,000 W double table fiber laser cutting machine — full technical specification, imperial edition"
    b.cover("Value line · full technical specification", "ULE-3015 · 6,000 W · double table fiber laser cutting machine", "ULE fiber laser",
            "Technical specification", "Built in China to North American standards", V + "vn-ule-machine-2026.webp",
            [("10 × 5 ft", "Cutting range"), ("6,000 W", "Raycus fiber laser"), ("492 ft/min", "Max. moving speed"), ("1.5 G", "Max. acceleration")],
            hero_h=330, minis=[V + "vn-ule-cutting.jpg", V + "vn-ule-console.jpg", V + "vn-ule-head.jpg", V + "vn-ule-chiller.jpg"])
    b.page("Contents", "@@TOC@@", sub="Contents")
    # company profile — the manufacturing partner (the original's "we": the factory)
    stats = ('<div class="stats s2">' + "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in [
        ("2002", "Founded in March 2002"), ("5000 +", "Annual production capacity of 5000+ sets"),
        ("120 +", "More than 120 R&amp;D personnel"), ("100 +", "Exported to over 100 countries")]) + "</div>")
    vmv = "".join(f'<div class="irow sm"><img class="ico" src="{D.im(U + i, 300)}"><div><div class="ittl">{t}</div><p>{x}</p></div></div>' for i, t, x in [
        ("icon-mission.png", "Mission", "Dedicated to research and development and to better product and service quality, in order to establish a "
         "globally renowned hub for sheet metal manufacturing machinery."),
        ("icon-vision.png", "Vision", "To be a respected provider of sheet metal support services, earning the trust of its customers and the "
         "pride of its staff."),
        ("icon-values.png", "Values", "Innovation, Lean, Integrity, Win-Win.")])
    body = (title("Company profile", "Our manufacturing partner")
            + P("The ULE is built for NovoTech in China, to North American standards, by NovoTech's value-line manufacturing partner — "
                "and sold, installed and serviced in Canada by NovoTech.", cls="sm")
            + row(fig(U + "factory-night.jpg", h=318, fit="cover", px=1000), stats + '<div style="height:10pt"></div>' + vmv, cols="1fr 1.25fr", gap=16)
            + '<div style="height:10pt"></div>'
            + P("Since its establishment the company has gone through 20 years of development. Through the joint efforts of two generations it "
                "has become the largest local machine tool manufacturer — its strength speaks for itself.",
                "An enterprise that does not prioritize technology and R&amp;D cannot sustain continuous development. Its leadership places "
                "technology first, allowing its machines to stay highly competitive in the current market environment — this sets it apart "
                "from many competitors in the industry.",
                "It has always prioritized giving customers the highest-quality machines. Customers feel excitement when they receive a machine "
                "of excellent quality, as it helps them in production and achieves career success — this is also its success.", cls="sm"))
    b.page("Company profile", body, key="profile")
    body = (title("Equipment", "Factory equipment")
            + P("Machining, welding and assembly equipment in the factory where the ULE is built.", cls="sm")
            + fig(U + "equipment.jpg", h=560, px=1400))
    b.page("Equipment", body, key="equipment")
    # product details (the original's order: top to bottom of each page)
    body = (title("Product details", "Bed · crossbeam · control")
            + det("Mechanical bed", ["High-quality steel structural materials and meticulous welding, tempering and aging treatments maintain the "
                                     "machine tool bed's undistorted rigidity, stability and long-term accuracy.",
                                     "Dust funnel structure with separate chambers, a tracking dust removal system and precision processing on "
                                     "imported large-scale CNC equipment ensure superior precision exceeding design standards, improving the "
                                     "working environment and the life of consumables."], V + "vn-ule-bed.jpg")
            + det("Crossbeam", ["The crossbeam undergoes annealing treatment and is machined as a whole in the machining center for long-term "
                                "stability during high-speed operation.",
                                "The crossbeam structure is lightweight yet impact-resistant, with high rigidity optimized by finite element "
                                "methods and precision machining, minimizing the load on the gantry for optimal dynamic performance."], U + "crossbeam.jpg")
            + det("Control system", ["It stands out for its user-friendly features, including easy installation, simple calibration and "
                                     "adjustable speed control through power settings, enhancing operational efficiency.",
                                     "The software provides advanced customization options, such as individual adjustments for imported linear "
                                     "speed, and a comprehensive cutting process database, ensuring precise and optimized cutting operations."],
                  V + "vn-ule-console.jpg"))
    b.page("Product details", body, key="details1")
    body = (title("Product details", "Cutting head · laser source · servo motor")
            + det("Cutting head", ["Auto-focusing laser cutting head adjusts the focus to the material thickness, reducing cutting time and "
                                   "enhancing cutting quality.",
                                   "Patented anti-collision protection structure and micro-joints in waste cutting prevent plate warping, ensuring "
                                   "high-speed and stable cutting operations."], V + "vn-ule-head.jpg")
            + det("Laser source", ["The laser allows direct control of all functions and supports synchronized laser source control, enhancing "
                                   "cutting capabilities and efficiency while delivering maintenance cost savings of 15% to 20%.",
                                   "With an independently developed core light source, this fiber laser offers convenient maintenance, lower "
                                   "procurement costs and reliable operation — a cost-effective, top-performing solution for industrial "
                                   "applications."], V + "vn-ule-source.jpg")
            + det("Servo motor", ["The machine features Delta servo motors from Taiwan, renowned for their high speed, precision, feedback and "
                                  "inertia capabilities, ensuring optimal performance in high-quality, high-productivity operation.",
                                  "The imported high-inertia servo system and amplifier offer exceptional responsiveness, significantly cutting "
                                  "down tuning time and enabling rapid acceleration and deceleration for improved mechanical stability."],
                  V + "vn-ule-servo.jpg"))
    b.page("Product details", body, key="details2")
    body = (title("Product details", "Gear, rack, linear guide · gearbox · lubrication")
            + det("Gear, rack, linear guide", ["The precision-ground gear and rack transmission system of this machine goes beyond the vibration "
                                               "limits of screw-driven systems, ensuring high-speed, high-precision transmission over long distances.",
                                               "The YYC gear and rack transmission system, an original imported component, guarantees accuracy and "
                                               "long life even under the intense high-speed operation of a 10 kW-class laser."], V + "vn-ule-rack.jpg")
            + det("Gearbox", ["The machine features DESBOER gearboxes from Japan, known for high torque, precision, stability and durability, "
                              "ensuring reliable performance.",
                              "The innovative technology integrated into the gearboxes enhances their performance and sets them apart in the "
                              "market for quality and longevity."], V + "vn-ule-drive.jpg")
            + det("Automatic lubrication", ["The timed automatic lubrication system starts and dispenses lubricating oil according to the "
                                            "machine's running time, ensuring swift and efficient service.",
                                            "By precisely timing the lubrication cycles, the system optimizes equipment performance and prolongs "
                                            "its life, saving maintenance costs and improving operational efficiency."], V + "vn-ule-lube.jpg"))
    b.page("Product details", body, key="details3")
    body = (title("Product details", "Water chiller · air cooler · electric components")
            + det("Water chiller", ["The water chiller comes with over-temperature alarms, flow protection, water level protection and further "
                                    "safety alarms to ensure operational safety and prevent potential hazards.",
                                    "These safety features provide comprehensive protection against overheating, flow issues and water level "
                                    "fluctuations, enhancing the reliability and life of the water chiller."], V + "vn-ule-chiller.jpg")
            + det("Air cooler", ["Air coolers regulate the temperature inside the electrical cabinet to ensure optimal performance of the components.",
                                 "Stable temperatures held by the air coolers prevent overheating and potential damage to electronic equipment.",
                                 "Effective cooling enhances the overall efficiency and life of the electrical cabinet systems."], V + "vn-ule-aircon.jpg")
            + det("Electric components", ["The machine is designed to meet European electrical standards and incorporates Schneider Electric "
                                          "components."], V + "vn-ule-cabinet.jpg"))
    b.page("Product details", body, key="details4")
    body = (title("Optional", "Precitec head · IPG laser · aluminum crossbeam")
            + det("Precitec cutting head — Germany", ["The PROCUTTER high-power fiber cutting head from PRECITEC, imported from Germany, offers "
                                                      "stable and reliable performance thanks to its electric focus position adjustment, "
                                                      "making automated machine setup and piercing easier.",
                                                      "Its compact and slim design, with fast acceleration and cutting speed, enhances efficiency "
                                                      "in a wide range of cutting applications."], U + "precitec.jpg", sub="option")
            + det("IPG laser", ["With a photoelectric conversion rate above 30%, the fiber laser operates at temperatures between 50 and 104 °F "
                                "(10 – 40 °C), with optional temperature control by air conditioning.",
                                "With a wavelength range of 1070 – 1090 nm, high beam quality in TEM00 mode and an M² value below 1.4, it "
                                "ensures precise cutting of highly reflective materials such as aluminum and copper."], V + "vn-ule-ipg.jpg", sub="option")
            + det("Aluminum crossbeam", ["Die-cast integrated aluminum crossbeam made from aerospace-grade aluminum alloy.",
                                         "CNC high-temperature annealing treatment for a lightweight design and resistance to deformation.",
                                         "Faster dynamic response and higher cutting accuracy thanks to minimal deformation, lower weight and "
                                         "higher strength."], V + "vn-ule-albeam.jpg", sub="option"))
    b.page("Optional", body, key="options")
    # specifications and configuration
    spec = kv([("Model", "ULE (ULE-3015)"), ("Laser power", "6,000 W"), ("Cutting range", "10 × 5 ft (3,000 × 1,500 mm)"),
               ("Maximum moving speed", "492 ft/min (150 m/min)"), ("Maximum acceleration", "1.5 G"),
               ("Positioning accuracy", "±0.002″ (±0.05 mm)"), ("Repeated positioning accuracy", "±0.0008″ (±0.02 mm)"),
               ("Operating voltage", "380 V / 50 Hz <small>— factory standard; supplied with a CSA-approved panel for 600 V 3-phase in Canada</small>"),
               ("Cooling method", "Water-cooled")], head=["Specifications", "ULE"])
    conf = kv([("Bed", "NovoTech (built in-house)"), ("Control system", "CypCut 4000E"), ("Laser", "Raycus"), ("Cutting head", "BOCI BLT421"),
               ("Servo motor", "Delta"), ("Gearbox", "DESBOER"), ("Gear, rack", "YYC"), ("Linear guide", "Hiwin"), ("Water chiller", "Hanli"),
               ("Electrical components", "NovoTech (built in-house)"), ("Automatic lubrication device", "NovoTech (built in-house)")],
              head=["Component function", "Brand / manufacturer"])
    spec, conf = (t.replace('<table class="kv">', '<table class="kv cmp">', 1) for t in (spec, conf))
    body = (title("Specifications", "Specifications · configuration") + spec + '<div style="height:10pt"></div>'
            + h2("Configuration") + conf + D.included())
    b.page("Specifications", body, key="spec")
    for i, k in enumerate(("cs", "ss", "al", "cu"), 1):
        cut_page(b, k, i)
    # installation conditions and consumables
    req = [("1", "Power supply capacity", ["Not less than 120 kVA"]),
           ("2", "Power supply quality", ["Three-phase voltage instability ≤ ±5%", "Three-phase power imbalance ≤ 2.5%",
                                          "Grounding resistance ≤ 3 ohms; the power supply voltage must not cut off suddenly"]),
           ("3", "Compressed air", ["For high-pressure air cutting, the pressure should be ≥ 185 psi (13 kgf/cm²) and the flow rate ≥ 53 cfm (1.5 m³/min)",
                                    "The dew point temperature must stay low — the limit is not given in the factory's sheet; NovoTech confirms it for your air dryer",
                                    "Oil content ≤ 0.01 ppm; solid particles ≤ 0.01 µm"]),
           ("4", "Auxiliary gases", ["The purity of oxygen and nitrogen should be ≥ 99.96%"]),
           ("5", "Cutting material", ["Smooth, flat, rust-free and uniformly rolled, meeting ISO standards"]),
           ("6", "Foundation requirements", ["The installation foundation must have no settlement and be built to the foundation drawings provided by NovoTech"]),
           ("7", "On-site conditions", ["The working environment should have a stable temperature of 41 – 86 °F (5 – 30 °C)", "Humidity below 70%",
                                        "After installation and commissioning, the laser should be isolated and an air conditioner installed"]),
           ("8", "Operators", ["Personnel with basic skills in electrical work, mechatronics and CNC machine tool operation"]),
           ("9", "Other supporting equipment", ["A computer for programming and monitoring the laser operation",
                                                "The cables needed for on-site installation of the equipment"])]
    trs = "".join(f"<tr><td>{n}</td><th>{c}</th><td><ul>{''.join(f'<li>{x}</li>' for x in r)}</ul></td></tr>" for n, c, r in req)
    reqt = f'<table class="kv req"><thead><tr><th>No.</th><th>Content</th><th>Requirements</th></tr></thead><tbody>{trs}</tbody></table>'
    cons = kv([("Focusing protective lens", "40 hours", "3 – 5 pieces"), ("Collimating protective lens", "500 hours", "1 – 3 pieces"),
               ("Focusing lens", "Approx. 3,000 hours", "2 sets"), ("Collimating lens", "Approx. 3,000 hours", "1 set"),
               ("Nozzle", "120 hours", "3 – 10 of each model needed, depending on the variety of sheet metal you cut")],
              head=["Name", "Lifespan", "Recommended stock quantity"])
    cons = cons.replace('<table class="kv">', '<table class="kv cmp">', 1)
    body = (title("Installation", "Conditions for on-site installation") + reqt + '<div style="height:8pt"></div>'
            + h2("Consumable supplies") + cons)
    b.page("Installation", body, key="install")
    body = (title("Quality · delivery", "Quality control · delivery")
            + fig(U + "building.jpg", h=170, fit="cover", px=1000)
            + '<div style="height:10pt"></div>'
            + row(fig(U + "testing.jpg", "Testing center", h=150, fit="cover", px=900), fig(U + "truck.jpg", "Container loading", h=150, fit="cover", px=900), gap=14)
            + '<div style="height:6pt"></div>'
            + row(h2("Quality control") + checks(["The factory's press brake manufacturing leads the industry in China, setting benchmarks for "
                                                 "quality and performance.",
                                                 "Its quality inspection rigorously follows industry standards, ensuring the reliability of the machines.",
                                                 "Testing machines run continuously, so every product meets the highest standards before it is dispatched."]),
                  h2("Delivery", "packaging") + checks(["Customizable packaging, including wooden cases, for sea transportation keeps the machine "
                                                       "intact on delivery.",
                                                       "Standard machines are ready to ship from the factory within 20 days.",
                                                       "An advanced fixing method keeps the machine stable and free of vibration in container transport."]),
                  gap=18))
    b.page("Quality · delivery", body, key="quality")
    svc = [(U + "training.jpg", "Pre sale", ["Custom-tailored selection of press brakes and tooling to match each customer's processing needs, "
                                            "optimizing bending quality and operational efficiency.",
                                            "A comprehensive engineering review recommends the most cost-effective solution for the user.",
                                            "A finalized, engineer-approved solution that best fits the user's requirements."]),
           (V + "vn-ule-cutting.jpg", "On sale", ["Commitment to customer satisfaction through strict adherence to the contract terms.",
                                                  "Rigorous quality assurance for all equipment delivered.",
                                                  "Continuous, proactive communication keeps the customer informed throughout the sale."]),
           (U + "support.jpg", "After sales", ["NovoTech's 1-year warranty with complimentary part replacements ensures long-term reliability "
                                              "and user satisfaction.",
                                              "Professional remote assistance and on-site service, for personalized and convenient support.",
                                              "Tracking services and a service file for each user streamline maintenance for regular customers."]),
           (V + "vn-ule-nozzles.jpg", "Parts", ["Prompt delivery of custom accessories to meet specific customer requirements.",
                                                "Focused on minimizing downtime and keeping the machine running."]),
           (U + "brands.jpg", "Generality", ["Components from globally recognized brands make replacement parts easy to find worldwide.",
                                             "Identical parts can be sourced locally, which makes maintenance and repair convenient."]),
           (U + "console-strip.jpg", "Customization", ["We specialize in tailored machinery and tooling solutions designed for the unique "
                                                       "specifications of each customer's workpieces.",
                                                       "Customization ensures optimal compatibility and efficiency for a wide range of workpieces."])]
    cards = [card(i, t, checks(x), h=118, cls="svc") for i, t, x in svc]
    body = title("Service", "Service") + grid(cards[:3], 3, 14) + '<div style="height:8pt"></div>' + grid(cards[3:], 3, 14)
    b.page("Service", body, key="service")
    # the ULE photos of the supplier's website, logos removed (the owner, Nov 1 2026: "add these photos to their PDF catalogue")
    pics = [("vn-ule-machine-2026.webp", "The ULE: the enclosed cutting cabin, its viewing windows and the shuttle table at the end"),
            ("vn-ule-exchange-2026.webp", "Exchange table — the second table runs out of the cabin, so the next sheet is loaded while the first is cut"),
            ("vn-ule-loading-2026.webp", "Sheets laid on the outside exchange table, ready to go into the cabin"),
            ("vn-ule-unloading-2026.webp", "Cut parts taken off the exchange table while the other table is in the cabin"),
            ("vn-ule-slats-2026.webp", "Sheet on the replaceable support slats of the table"),
            ("vn-ule-loader-2026.webp", "Automatic sheet loading beside an enclosed ULE (option)"),
            ("vn-ule-gantry-2026.webp", "Gantry with the cutting head, the cable carrier and the bellows over the guides"),
            ("vn-ule-frame-2026.webp", "Welded bed with the rails of the shuttle table"),
            ("vn-ule-heads-2026.webp", "Cutting heads matched to the laser power"),
            ("vn-ule-chillers-2026.webp", "Water chillers sized to the laser source"),
            ("vn-ule-screen-2026.webp", "CNC touchscreen with the camera view of the table and the cutting program")]
    for i, part in enumerate((pics[:6], pics[6:])):
        cells = [D.fig(V + f, cap, h=150, fit="contain", px=1200) for f, cap in part]
        b.page("Photos", title("Double table fiber laser cutting machine", "ULE in pictures" + (" (continued)" if i else ""))
               + D.grid(cells, 2, 14), key="photos" if i == 0 else None)
    b.back("Fiber laser for your shop.", [V + "vn-ule-machine-2026.webp", V + "vn-ule-cutting.jpg", V + "vn-ule-console.jpg", V + "vn-ule-bed.jpg"])
    toc = [("Company profile", "profile"), ("Equipment", "equipment"), ("Mechanical bed · crossbeam · control system", "details1"),
           ("Cutting head · laser source · servo motor", "details2"), ("Gear, rack, linear guide · gearbox · automatic lubrication", "details3"),
           ("Water chiller · air cooler · electric components", "details4"), ("Optional: Precitec head · IPG laser · aluminum crossbeam", "options"),
           ("Specifications · configuration", "spec"), ("Cutting parameters — carbon steel, oxygen", "cs"),
           ("Cutting parameters — stainless steel, nitrogen", "ss"), ("Cutting parameters — aluminum, nitrogen", "al"),
           ("Cutting parameters — copper, nitrogen", "cu"), ("Conditions for on-site installation · consumables", "install"),
           ("Quality control · delivery", "quality"), ("Service", "service"), ("ULE in pictures", "photos")]
    rows_ = "".join(f'<div><span>{t}</span><i></i><b>{b.num(k):02d}</b></div>' for t, k in toc)
    body = (title("Full technical specification · ULE-3015 · 6,000 W", "Contents")
            + f'<div class="toc" style="columns:1">{rows_}</div>'
            + row(D.included(two=True), '<div class="box"><div class="bt">Sold &amp; serviced in Canada</div>'
                  '<p>by NovoTech Machine Tools — Mississauga, ON</p></div>', cols="2.3fr 1fr", gap=14, cls="mt-auto"))
    for pg in b.pages:
        if pg.get("body") == "@@TOC@@":
            pg["body"] = body
    return b


if __name__ == "__main__":
    D.build(book(), "--html" in sys.argv)
