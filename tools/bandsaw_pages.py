#!/usr/bin/env python3
"""Generate the band saw section pages: the hub (band-saw.json) and eight category pages —
four for the Bekamak premium line and four for the NovoFab Machinery value line.
    python3 tools/bandsaw_pages.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "content", "pages")
FAM = json.load(open(os.path.join(ROOT, "content", "families", "bandsaw.json"), encoding="utf-8"))

PDF_BK = {"file": "files/NovoTech-Bekamak-Band-Saws-Catalogue-2026.pdf", "label": "Bekamak band saw catalogue", "size": "PDF · 7.5 MB · imperial units"}
PDF_NF = {"file": "files/NovoTech-Value-Line-Band-Saws-Catalogue-2026.pdf", "label": "NovoTech value line band saw catalogue", "size": "PDF · 5 MB · imperial units"}
PLAYLIST = "https://www.youtube.com/playlist?list=PLgtouQi-TePvLZjD0XkwpvL2pX1sAUuFG"
GUIDE = {"href": "band-saw.html#buying-guide", "label": "Band saw buying guide: sizes, feeds, blades and troubleshooting"}
CRUMB_BASE = [{"label": "Home", "href": "index.html"}, {"label": "Products", "href": "products.html"}, {"label": "Metal cutting band saws", "href": "band-saw.html"}]

CATS = ["manual", "semi-automatic", "automatic", "double-column", "vertical"]
CAT_TITLE = {"manual": "Manual band saws", "semi-automatic": "Semi-automatic band saws", "automatic": "Automatic band saws", "double-column": "Double-column band saws", "vertical": "Vertical band saws"}
CAT_SHORT = {"manual": "Manual", "semi-automatic": "Semi-automatic", "automatic": "Automatic", "double-column": "Double-column", "vertical": "Vertical"}


FACTORY_VIDEO = {"id": "6xEVXrP8h3k", "title": "Bekamak corporate introduction video", "thumb": "video-6xEVXrP8h3k", "duration": "PT3M4S"}
FIRST = {"novotech-bs-315gf": 0, "bekamak-bmso-ga": 0, "bekamak-bmso-gs": 2}   # rank within the group: 0 = top (BMSO 350GA = most popular automatic saw), 2 = after the others (320GS / GLS below the 270DGS)


def fams(brand, cat, sub=None):
    ks = [k for k in FAM["order"] if FAM["families"][k]["brand"] == brand and FAM["families"][k]["group"] == cat
          and (sub is None or FAM["families"][k].get("subgroup") == sub)]
    return sorted(ks, key=lambda k: (FIRST.get(k, 1), ks.index(k)))


VOLT_FAQ = {"q": "What voltage do these saws run on?",
            "a": "Three-phase machines are supplied for 600 V with a CSA-approved electrical panel; 208 V, 240 V or 480 V 3-phase are available on request."}

BK = {
    "manual": dict(
        title="Manual Metal Band Saws — Double-Miter Gravity-Feed Bandsaws | NovoTech",
        meta="Gravity-feed manual band saws BMS 230DG and 270DG: double-miter heads to 60°, hydraulic descent, Ø9″ to 10-5/8″. Specs in inches and mm, CSA panels.",
        h1="Bekamak manual band saws",
        intro="Gravity-feed pivot saws built by Bekamak in Turkey for maintenance shops, fabricators and anyone cutting a few pieces at a time: the operator positions the bar, closes the vise and lowers the bow; a hydraulic cylinder controls the descent and the double-miter head swivels both ways for angle cuts. Premium-line construction with CSA-approved panels and support from Mississauga, ON, Canada.",
        points=["Hydraulic-damped gravity feed with adjustable cutting pressure", "Double-miter head: +60° right, −45° left", "Round capacities Ø9″ (230 mm) and Ø10-5/8″ (270 mm)"],
        hero="bk-hero-manual", minis=["bk-bms-230dg-1-cut"],
        lead="European-style pivot saws with heavy castings, variable-speed motors and hydraulic descent control.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "What does “gravity feed” mean on a band saw?", "a": "The saw bow descends under its own weight; a hydraulic cylinder with an adjustable valve controls how fast it drops, so the operator sets the cutting pressure for the material. After the cut the operator lifts the bow back up by hand."},
            {"q": "Can a manual band saw cut miters?", "a": "Yes. The BMS 230DG and 270DG heads swivel to both sides — +60° to the right and −45° to the left — with an angle scale and fast stops at 30°, 45° and 60°, so one setup covers most structural miters."},
            {"q": "When should I move up to a semi-automatic saw?", "a": "When you cut more than a few dozen pieces a day, or when the operator is tied up holding the bow. A semi-automatic saw clamps hydraulically, cuts at a preset feed and lifts the bow by itself, so the operator only loads material. See the Bekamak semi-automatic band saws page."},
            VOLT_FAQ,
        ]),
    "semi-automatic": dict(
        title="Semi-Automatic Metal Band Saws — Hydraulic Miter Bandsaws | NovoTech",
        meta="Bekamak BMSY semi-automatic band saws: hydraulic vise, automatic bow return, miter heads to 60°, Ø9″ to Ø17-3/8″ (230–440 mm). Specs in inches and mm.",
        h1="Bekamak semi-automatic band saws",
        intro="The workhorse of most fabrication shops: the operator loads the bar and presses start; the hydraulic vise clamps, the bow cuts at the set feed rate and lifts clear when the cut is done. Bekamak's BMSY pivot saws come with single- or double-miter heads for structural steel, inverter blade speed and hydro-mechanical blade tension — from Ø9″ to Ø17-3/8″ (230–440 mm).",
        points=["Hydraulic vise, automatic bow return, inverter blade speed", "Single- or double-miter heads to 60°; DGH models add a hydraulic vise", "Round capacities from Ø9″ (230 mm) to Ø17-3/8″ (440 mm)"],
        hero="bk-hero-semi", minis=["bk-bmsy-320g-1-cut", "bk-bmsy-270dgh-1-cut"],
        lead="Pivot-type saws with inverter blade speed, hydro-mechanical blade tension and a hydraulic vise on the DGH models.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "What is the difference between a semi-automatic and a fully automatic band saw?", "a": "A semi-automatic saw makes one cut per start: it clamps, cuts and lifts the bow, then waits for the operator to feed the next piece. A fully automatic saw also feeds the material to length (by rollers or a shuttle vise) and repeats the cycle for the programmed quantity. See the Bekamak automatic band saws page."},
            {"q": "Single miter or double miter?", "a": "A single-miter head (BMSY 320G/GL) swivels to one side, so angled parts are cut by flipping the bar. A double-miter head (BMSY DG/DGH) swivels both ways — +60° right, −45° left — which saves handling on frames and trusses with opposite angles."},
            {"q": "What does the DGH suffix mean?", "a": "DGH models have a hydraulic vise — the DG versions clamp the material by hand. The rest of the saw is the same: double-miter head swung by hand on the angle scale, hydraulic feed cylinder and automatic bow return."},
            {"q": "Can these saws cut bundles?", "a": "Yes, with the optional hydraulic top clamping, which presses a bundle of tubes or bars down while the side vise holds it. Ask us about bundle sizes for the model you need."},
        ]),
    "automatic": dict(
        title="Automatic Band Saws — Auto-Feed NC Bandsaws for Metal | NovoTech",
        meta="Bekamak BMSO automatic feed band saws: roller-feed, encoder and servo shuttle-vise NC saws to Ø17-3/8″ (440 mm), plus automatic miter models. Specs in inches.",
        h1="Bekamak automatic band saws",
        intro="Set the length and the quantity, load the bar and walk away. Bekamak's BMSO saws feed the material — with driven rollers, an encoder-measured feed or a servo shuttle vise — clamp, cut and count until the job is done. From Ø9″ to Ø17-3/8″ (230–440 mm), including automatic single- and double-miter models with NC job lists.",
        points=["Roller feed, encoder feed or servo shuttle-vise feed", "NC job lists: length × quantity", "Automatic single- and double-miter models"],
        hero="bk-hero-auto-350ga", minis=["bk-bmso-270dgs-1", "bk-bmso-320gs-3-cut"], hero_large=True,
        lead="Roller-feed automatics for simple repeat cutting, encoder and servo versions for length accuracy, and automatic miter saws for angled parts.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "Roller feed or shuttle vise — which is better?", "a": "Roller feed (BMSO 230–440, BMSO E) is simple and fast for bar and tube in straight cuts; the encoder versions measure the fed length for better accuracy. A shuttle vise — servo-driven on the BMSO GS/GLS and all CS/CGS double-column saws, motorized on the compact 270DGS — grips the bar and moves it to the programmed length, giving ±0.1 mm repeatability on the servo models and reliable feeding of bundles and short remnants."},
            {"q": "How many lengths can I program?", "a": "The NC control on the servo-feed models stores a job list of several length-and-quantity pairs, so one bar can be cut into different parts without re-programming."},
            {"q": "What happens at the end of the bar?", "a": "The saw stops when the remaining length is shorter than the next part or the feed vise reaches its limit, and the counter shows how many pieces were cut. Remnant length depends on the model — typically 3–6 in (80–150 mm)."},
            {"q": "Do automatic saws need a roller table?", "a": "A short infeed roller table is included on the BMSO E models; a 10 ft (3 m) manual or motorized roller table is optional on the others and is strongly recommended for bars longer than about 6 ft."},
        ]),
    "double-column": dict(
        title="Double Column Band Saws — Heavy-Duty Industrial Bandsaws | NovoTech",
        meta="Heavy-duty double column band saws from Ø13″ to 87″ (330–2200 mm): BMSY C semi-automatics, CGH / DG NC miter saws, BMSO CS / CGS servo saws, the XS line and the GANTRY 2200XS.",
        h1="Bekamak double-column band saws",
        intro="For heavy bar, billets, beams and bundles the bow runs between two hardened columns instead of pivoting, so the blade enters the material squarely and stays square through the cut. Bekamak builds semi-automatic and fully automatic versions, miter heads to 60°, servo feeding with NC job lists, the enclosed high-tech XS production saws and the gantry-type GANTRY 2200XS — from Ø13″ to Ø87″ (330–2200 mm).",
        points=["Twin-column guidance for square cuts in heavy stock", "Semi-automatic, roller-feed and servo-feed NC models", "Round capacities from Ø13″ (330 mm) to Ø87″ (2200 mm) — the GANTRY 2200XS for 50,000 kg pieces"],
        hero="bk-hero-dc-570cs", minis=["bk-bmsy-460c-1-cut", "bk-bmso-570xs-1-cut"],
        lead="From the BMSY C semi-automatics to servo-feed CS NC production saws and the enclosed XS line.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "Why choose a double-column saw over a pivot saw?", "a": "Rigidity and capacity. The bow is guided on two columns, so there is no side load on the blade — cuts stay square in large solids and the blade lasts longer. Double-column saws also reach capacities a pivot bow cannot: Ø13″ (330 mm) up to Ø87″ (2200 mm) on the Bekamak range, with the GANTRY 2200XS at the top."},
            {"q": "Can a double-column saw cut miters?", "a": "Yes — the BMSY CGH (single miter) and BMSY DG NC (double miter) swivel the whole bow assembly up to 60° under hydraulic or NC control, and the automatic CGS/CDGS NC models do the same with servo feeding."},
            {"q": "What is a split vise (SV)?", "a": "The SV versions of the BMSY C saws have a second vise jaw close to the blade, so short pieces and remnants are clamped on both sides of the cut — useful for cutting slices from blocks and billets."},
            {"q": "What is the XS line?", "a": "Bekamak's high-tech production saws: servo-driven bow feed and material feed, full enclosure and CNC control, designed for carbide blades, the fastest cycle times and unattended running."},
            {"q": "How big is the GANTRY 2200XS?", "a": "It cuts rounds from Ø20″ to Ø87″ (500–2200 mm) and blocks up to 94-1/2″ × 87″, pieces up to 23 ft (7 m) long and 50,000 kg, on a gantry frame 49 ft long — a saw for forges, steel mills and service centres that cut ingots and large billets. Servo bow and material feed, a 40 HP main motor and MES production software are standard."},
        ]),
    "vertical": dict(
        title="Vertical Band Saws for Metal — Plate & Block Saws | NovoTech",
        meta="Bekamak vertical band saws for metal cutting: the tilting-frame BMSY 460VG, the BMSY 613VT and VB 0814-8 block saws and the fully automatic CROSS 0626VT plate saw.",
        h1="Bekamak vertical band saws",
        intro="A vertical band saw for metal cutting runs the blade vertically through the workpiece instead of swinging a bow down onto it, so plates, blocks and billets can be sliced along their length or cross-cut flat on a table. Bekamak builds four: the BMSY 460VG, a semi-automatic saw whose frame tilts 60° both ways for miter cuts in Ø18″ stock; the BMSY 613VT, which slices 23-5/8″ × 23-5/8″ sections up to 51″ long from blocks and plates on a servo cutting feed; the VB 0814-8 block-cutting machine for 32″ × 55″ blocks of 40,000 kg over a 26 ft cut; and the fully automatic CROSS 0626VT, which feeds and cuts plates up to 23-5/8″ × 102″ in tool steel, titanium and Inconel. CSA-approved panels, parts and support from Mississauga, ON, Canada.",
        points=["Semi-automatic: BMSY 460VG tilting-frame miter saw, BMSY 613VT and VB 0814-8 block saws", "Fully automatic: CROSS 0626VT plate saw with automatic feed, 23-5/8″ × 102″", "Sections from Ø18″ (460 mm) to 32″ × 55″ blocks and 102″ wide plate"],
        hero="bk-bmsy-613vt-3", minis=["bk-bmsy-460vg-1", "bk-cross-0626vt-1"],
        lead="Vertical blades for plate, blocks and billets: a tilting-frame miter saw, two block saws and an automatic plate saw.",
        subgroups=[("semi", "Bekamak semi-automatic vertical band saws", "The operator loads and clamps; the saw cuts on a controlled feed and stops — the BMSY 460VG with its tilting frame, the BMSY 613VT block saw and the VB 0814-8 block-cutting machine."),
                   ("auto", "Bekamak fully automatic vertical band saws", "Automatic feeding and cutting from a program: the CROSS 0626VT plate saw.")],
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "When is a vertical band saw better than a horizontal one?", "a": "When the workpiece is a plate, slab or block rather than a bar: a horizontal saw clamps a bar and drops the bow through it, while a vertical saw passes the blade along a workpiece lying flat on a table — slicing a block into plates, trimming a slab or cutting a long plate to width. Tool steel, titanium and nickel alloys are usually cut this way."},
            {"q": "What does the BMSY 460VG cut?", "a": "Round, square and rectangular stock up to Ø18″ / 28″ × 18″ (460 / 710 × 460 mm), straight or at a miter: the whole frame tilts up to 60° to either side under power, with the hydraulic vise and automatic return of a semi-automatic saw."},
            {"q": "How long a cut can the block saws make?", "a": "The BMSY 613VT travels 51″ (1300 mm) along a 23-5/8″ × 23-5/8″ block; the VB 0814-8 has 26 ft (8 m) of cutting travel on a table rated 40,000 kg for blocks up to 32″ × 55″ (820 × 1400 mm)."},
            {"q": "What is automatic on the CROSS 0626VT?", "a": "Feeding and cutting: a feeder and servo positioning move the plate to the programmed length for each cut, the vises clamp across the full 102″ (2600 mm) width and the blade cuts, piece after piece, down to a minimum cut of 1-3/16″ (30 mm) in automatic mode."},
            VOLT_FAQ,
        ]),
}

NF = {
    "semi-automatic": dict(
        title="Affordable Semi-Automatic Band Saws — Hydraulic Bandsaws | NovoTech",
        meta="Value-line hydraulic semi-automatic band saws: BS-315GF full-hydraulic double-miter, BS-460G dual-miter, BS-5030 single-column and the 18″ BS-650GA.",
        h1="NovoTech semi-automatic band saws",
        intro="Hydraulic saws for the production floor at value-line prices, led by our best seller — the BS-315GF, a 10-inch double-miter (mitre) saw with hydraulic vise, hydraulic down-feed and hydraulic bow up-lift. A hydraulic cylinder lowers the bow at a dialled-in rate, the bow lifts and the machine stops at the end of the cut. From the 10-inch saws to the 18-inch BS-650GA swivel-head saw, with a single-column touch-screen model (BS-5030) in between.",
        points=["BS-315GF: full-hydraulic 10″ double-miter saw — our most popular model", "Hydraulic descent, automatic bow return and shut-off on every model", "Round capacities from Ø10″ (250 mm) to Ø18″ (460 mm)"],
        hero="nt-bs315gf-hero", minis=["nt-h18-1-cut", "nt-h12sc-1-cut"],
        lead="Hydraulic descent, hydraulic vises and automatic bow return from Ø10″ to Ø18″ (250–460 mm), including a single-column saw with touch screen.",
        faq=[
            {"q": "What is the difference between a semi-automatic and a fully automatic band saw?", "a": "A semi-automatic saw makes one cut per start: it clamps, cuts and lifts the bow, then waits for the operator to feed the next piece. A fully automatic saw also feeds the material to length and repeats the cycle for the programmed quantity — see the value line automatic band saws."},
            {"q": "Which value-line saws cut miters on both sides?", "a": "The BS-315GF, BS-460G / 460G-JC and BS-650GA swivel to both sides (45° left and right, 60° right); the BS-2114TH cuts angles up to 60° on one side."},
            {"q": "What does \"full-hydraulic\" mean on the BS-315GF?", "a": "Hydraulic vise, hydraulic down-feed and hydraulic bow up-lift on one 10-inch machine: the operator loads the bar, presses start and the saw clamps, cuts, lifts the bow and switches off. The gear drive and a bow that swivels to both sides with fast stops at 30°, 45° and 60° complete it."},
            {"q": "What does SC mean?", "a": "Single column: the BS-5030 guides the bow vertically on a column instead of a pivot, for square straight cuts up to Ø11-3/4″ / 19-3/4″ × 11-3/4″ with a PLC touch screen. Its automatic sister is the BS-5040."},
            VOLT_FAQ,
        ]),
    "automatic": dict(
        title="Automatic Feed Band Saws — Value-Line CNC Bandsaws | NovoTech",
        meta="Value-line automatic feed band saws: BS300x370 roller-feed, BS-460GB swivel-head miter saw with 20 ft stand, BS-650G scissor-type NC saw and the BS-5040 single-column saw.",
        h1="NovoTech automatic band saws",
        intro="Automatic saws that feed, clamp, cut and count by themselves — roller feeders on the compact BS300x370, the swivel-head BS-460GB that miters to both sides, the scissor-type BS-650G with NC feeding and 60° miters and a hydraulic shuttle vise on the single-column BS-5040; the CNC double column BS-500G, 500GT and 850G are on the double-column page. Value-line pricing with CSA-approved panels, a 1-year warranty and support from Mississauga, ON, Canada.",
        points=["Roller feed, NC feeder or hydraulic shuttle vise", "Piece counters and PLC job lists", "Round capacities from Ø11-3/4″ (300 mm) to Ø18-1/8″ (460 mm)"],
        hero="nt-a12-1-hero", minis=["nt-a18-1-cut", "nt-a12sc-1-cut"],
        lead="Roller-feed, shuttle-vise and CNC servo automatics from Ø11-3/4″ to Ø23-5/8″ (300–600 mm): feed, clamp, cut and count without an operator at the saw.",
        faq=[
            {"q": "Roller feed or shuttle vise — which is better?", "a": "Roller feed (BS300x370) is simple and fast for bar and tube in straight cuts. A shuttle vise (BS-5040, BS-460GB) grips the bar and moves it a set distance per stroke, which is more accurate and handles bundles; the CNC saws (BS-500G to BS-850G) position the feeder with a servo motor for the best repeatability."},
            {"q": "Which automatic models cut miters?", "a": "The BS300x370H (0°–60° miter head), the BS-460GB (bow swivels both sides) and the scissor-type BS-650G (automatic swivel to 60° right)."},
            {"q": "Do automatic saws need a roller table?", "a": "The BS-460GB ships with a 20 ft material stand; for the other models a roller conveyor is optional and strongly recommended for bars longer than about 6 ft."},
            VOLT_FAQ,
        ]),
    "double-column": dict(
        title="Twin-Column Band Saws — Value-Line Double Column Bandsaws | NovoTech",
        meta="Value-line twin-column band saws: semi-automatic TBK-4228, TGK and GZ gantry saws, automatic TBK-4228B and CNC BS-500G / 500GT / 850G. Specs in inches.",
        h1="NovoTech double-column band saws",
        intro="Twin-column saws at value-line prices: the bow travels vertically on two columns, so the cut stays square in solid bar, blocks and bundles. The TBK-4228 and the 45° miter (mitre) TBK-4228A are the semi-automatics, the TBK-4228B the automatic; the TGK-4235 and 4240 add gear drive and hydraulic blade tension; the BS-500G, 500GT and 850G are CNC production saws with servo feeding and stepless blade speed; the GZ4250/70 and GZ4260/120 are gantry saws for plate up to 47-1/4″ wide.",
        points=["Twin-column guidance for square cuts in heavy stock", "Semi-automatic and fully automatic models listed separately, smallest to largest", "Round capacities from Ø11″ (280 mm) to Ø23-5/8″ (600 mm)"],
        hero="nt-dc11av-1-cut", minis=["nt-dc14-1-cut", "nt-dc11-1-cut"],
        lead="Twin-column saws from Ø11″ to Ø23-5/8″ (280–600 mm): hydraulic semi-automatics, a miter version, automatics with shuttle vise, CNC production saws and gantry saws for plate and bundles.",
        subgroups=[("auto", "NovoTech fully automatic double-column band saws", "Automatic feeding, clamping and cutting from a program, from Ø11″ to Ø23-5/8″ (280–600 mm) — smallest to largest."),
                   ("semi", "NovoTech semi-automatic double-column band saws", "Hydraulic down-feed and clamping with manual material feed, from Ø11″ to Ø23-5/8″ (280–600 mm) — smallest to largest.")],
        faq=[
            {"q": "Why choose a double-column saw over a pivot saw?", "a": "Rigidity and capacity. The bow is guided on two columns, so there is no side load on the blade — cuts stay square in large solids and the blade lasts longer. The GZ4250/70 and GZ4260/120 gantry saws also take plate and bundles a pivot bow cannot."},
            {"q": "Which value-line double-column saws are automatic?", "a": "The TBK-4228B feeds and cuts automatically with a shuttle vise, stepless blade speed and a chip conveyor; the BS-500G, BS-500GT and BS-850G are CNC production saws with servo feeding, hydraulic vises and stepless blade speed. The TBK-4228, TBK-4228A, TGK-4235, TGK-4240, GZ4250/70 and GZ4260/120 are hydraulic semi-automatics with manual material feed."},
            {"q": "Can a value-line double-column saw cut miters?", "a": "The TBK-4228A swivels for cuts at 30° and 45° (Ø10-1/4″ and Ø6-3/4″), and the CNC BS-500G and BS-500GT have an automatic rotary bow to 45°. The other value-line double-column models are straight-cut saws."},
            VOLT_FAQ,
        ]),
    "vertical": dict(
        title="Vertical Metal Band Saws with Blade Welder — 12″ to 23″ Throat | NovoTech",
        meta="Value-line vertical metal band saws VS-300 to VS-585: 12″ to 23″ throat, tilting table, inverter blade speed and a built-in blade welder for contour and internal cuts. Specs in inches, sold and supported in Canada.",
        h1="NovoTech vertical metal band saws",
        intro="Vertical band saws for the tool room, fabrication and maintenance shop: the blade runs vertically and the workpiece — sheet, plate, bar, profiles, plastics or wood — is pushed across the table, so the saw cuts contours, radii, slots and straight lines that a horizontal saw cannot. The VS series has four sizes from a 12-1/4″ to a 23″ throat, a table that tilts 45° right (30° on the two larger saws) and 15° left, stepless blade speed from an inverter, and a blade welder with annealer and grinder on the column: cut the blade, thread it through a drilled hole, weld it and saw an internal cut-out. For slicing blocks and plate on a production line see the premium vertical saws.",
        points=["Throat 12-1/4″ × 7-1/4″ to 23″ × 13-1/4″ (310 × 185 to 585 × 336 mm)", "Built-in blade welder, annealer and grinder for internal cut-outs", "Tilting table, inverter blade speed to 1,076 ft/min, table gauge and work light"],
        hero="nt-vs400-1", minis=["nt-vs300-1", "nt-vs500-1"],
        lead="Contour, slot and straight cuts on a tilting table, with a blade welder on every saw — four sizes from a 12″ to a 23″ throat.",
        faq=[
            {"q": "What is the throat of a vertical band saw?", "a": "The width from the blade to the column (how wide a part can pass beside the blade) and the height under the upper blade guide (how thick a part can be). The VS-300 takes 12-1/4″ × 7-1/4″ (310 × 185 mm), the VS-400 15-3/4″ × 11-1/4″, the VS-500 19-3/4″ × 12-1/4″ and the VS-585 23″ × 13-1/4″ (585 × 336 mm)."},
            {"q": "What is the blade welder for?", "a": "Internal cut-outs and blade repair. Drill a hole in the part, cut the blade, thread it through the hole and weld it on the saw's own butt welder, anneal the weld and grind it flush with the built-in grinder — then saw the inside contour. The same welder makes blades from coil stock and repairs a broken blade in a few minutes."},
            {"q": "Can these saws cut steel?", "a": "Yes — mild steel, stainless, tool steel in thin sections, aluminum, copper and brass, as well as plastics and wood: the inverter sets the blade speed from about 33 – 49 ft/min for steel to 590 – 1,076 ft/min for aluminum and non-metals. The chart on the saw gives the speed and tooth pitch for each material and thickness."},
            {"q": "Vertical band saw or horizontal band saw?", "a": "A horizontal saw clamps a bar and cuts it to length, unattended; a vertical saw is a hand-fed machine for shapes — curves, slots, angles, notches and internal cut-outs in sheet and plate. Most shops that cut both have one of each."},
            VOLT_FAQ,
        ]),
}

KW = {
    "manual": " Searching for a manual metal bandsaw, a gravity-feed horizontal band saw for metal or a small band saw machine for the shop? These are the ones NovoTech stocks and supports.",
    "semi-automatic": " If you are looking for a semi-automatic metal bandsaw, a hydraulic horizontal band saw for metal or an industrial band saw machine with a hydraulic vise, this is the page.",
    "automatic": " For buyers searching for an automatic metal cutting bandsaw, a CNC band saw machine or an industrial horizontal band saw for metal with automatic feeding, these are the models NovoTech sells and supports in Canada.",
    "double-column": " Known as double column, twin-column or dual column metal bandsaws, these horizontal band saw machines are the industrial choice for heavy solids, bundles and plate.",
    "vertical": " If you are looking for a vertical band saw for metal cutting or a vertical bandsaw for plate, blocks and contour work, these are the machines NovoTech sells and supports in Canada.",
}

ORIGIN = {
    "bekamak": {"title": "Made in Turkey by Bekamak", "text": "Bekamak has built band saws in Turkey since 1990 with European components — our premium line."},
    "novotech": {"title": "Built in China to North American standards", "text": "NovoTech's own brand — same CSA panel, warranty and Mississauga, ON, Canada support as every machine we sell."},
}

BRAND = {
    "bekamak": dict(key="bekamak", slug="bekamak", line="premium", name="Bekamak", pdf=PDF_BK, page_label="Bekamak",
                    brand_line="Bekamak band saws are made in Turkey by Bekamak Makina. Sold, installed and supported in Canada by NovoTech — the premium line of our band saw range.",
                    related_title="More Bekamak band saws from NovoTech"),
    "novotech": dict(key="novotech", slug="novotech", line="value", name="NovoTech", pdf=PDF_NF, page_label="NovoTech",
                    brand_line="NovoTech's own brand: manufactured in China to high North American quality standards, with the same CSA-approved panel, 1-year warranty and Mississauga, ON, Canada parts and support as every machine we sell.",
                    related_title="More NovoTech value line band saws"),
}


# URL slugs carry no brand (NovoTech, Oct 2026): a page's content or supplier may change later and the
# URL must keep its ranking.  Each slug is the category's own search phrase; the value-line pages take
# the next-best phrase for the same category so the two lines never share a URL keyword.
SLUGS = {
    ("bekamak", "manual"): "manual-band-saws",
    ("bekamak", "semi-automatic"): "semi-automatic-band-saws",
    ("bekamak", "automatic"): "automatic-band-saws",
    ("bekamak", "double-column"): "double-column-band-saws",
    ("bekamak", "vertical"): "vertical-band-saws",
    ("novotech", "semi-automatic"): "affordable-semi-automatic-band-saws",
    ("novotech", "automatic"): "automatic-feed-band-saws",
    ("novotech", "double-column"): "twin-column-band-saws",
    ("novotech", "vertical"): "vertical-metal-band-saw",
}


def page(brand, cat, spec):
    b = BRAND[brand]
    spec = dict(spec, intro=spec["intro"] + KW[cat])
    slug = SLUGS[(brand, cat)]
    other = "novotech" if brand == "bekamak" else "bekamak"
    p = {
        "slug": slug, "template": "category.html", "family_set": "bandsaw",
        "artifact_title": f"{b['name']} {CAT_TITLE[cat]}",
        "title": spec["title"], "meta_description": spec["meta"], "h1": spec["h1"], "intro": spec["intro"],
        "hero_points": spec["points"], "hero_image": spec["hero"], "hero_image_secondary": spec["minis"], "hero_large": spec.get("hero_large", False),
        "breadcrumb": CRUMB_BASE + [{"label": f"{b['name']} {CAT_TITLE[cat].lower()}"}],
        "hero_brand_line": b["brand_line"],
        "catalogue_pdfs": [b["pdf"]],
        "line_key": b["key"],
        "origin_feature": ORIGIN[brand],
        "groups": ([{"id": f"{b['slug']}-{cat}-{sid}", "brand": b["key"], "title": title, "lead": lead, "families": fams(brand, cat, sid)} for sid, title, lead in spec["subgroups"]]
                   if spec.get("subgroups") else
                   [{"id": f"{b['slug']}-{cat}", "brand": b["key"], "title": f"{b['name']} {CAT_TITLE[cat].lower()}", "lead": spec["lead"], "families": fams(brand, cat)}]),
        "alt_line": ({"href": f"{SLUGS[(other, cat)]}.html", "label": f"{BRAND[other]['name']} {CAT_TITLE[cat].lower()}",
                      "line": BRAND[other]["line"], "brand": other} if cat in (BK if other == "bekamak" else NF) else None),
        "faq_title": f"Questions we get asked about {b['name']} {CAT_TITLE[cat].lower()}",
        "faq": spec["faq"],
        "related_article": GUIDE,
        "youtube_playlist": PLAYLIST,
        "related_pages": [{"href": "circular-cold-saws.html", "label": "Cold saws — circular, carbide and automatic"}],
    }
    if spec.get("video"):
        p["intro_video"] = spec["video"]
        p["intro_video_heading"] = "Inside the factory — where the saws are built"
        p["intro_video_text"] = spec["video_text"]
    return p


def main():
    for old in ("manual-band-saws", "semi-automatic-band-saws", "automatic-band-saws", "double-column-band-saws", "vertical-band-saws",
                "affordable-semi-automatic-band-saws", "automatic-feed-band-saws", "twin-column-band-saws", "vertical-metal-band-saw"):
        fp = os.path.join(PAGES, old + ".json")
        if os.path.exists(fp):
            os.remove(fp)
    lines = []
    for brand, specs in (("bekamak", BK), ("novotech", NF)):
        b = BRAND[brand]
        subpages = []
        for cat in CATS:
            if cat not in specs:
                continue
            p = page(brand, cat, specs[cat])
            json.dump(p, open(os.path.join(PAGES, p["slug"] + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            subpages.append({"slug": p["slug"], "title": f"{b['page_label']} {CAT_TITLE[cat].lower()}", "nav_label": CAT_SHORT[cat], "cat": cat, "line": b["line"],
                             "image": p["hero_image"], "blurb": specs[cat]["lead"], "families": fams(brand, cat)})
        lines.append({"id": b["line"], "brand": b["key"], "label": f"{b['line'].title()} line", "name": b["name"], "short": b["page_label"], "pdf": b["pdf"],
                      "blurb": ("Built in Turkey since 1990 with European components and the heaviest construction in their class — the saws we recommend for production and heavy sections." if brand == "bekamak"
                                else "NovoTech's own brand: manufactured in China to high North American quality standards, with the same CSA-approved panel, 1-year warranty and Mississauga, ON, Canada parts and support as every machine we sell."),
                      "subpages": subpages})
    # ---- hub
    hp = os.path.join(PAGES, "band-saw.json")
    h = json.load(open(hp, encoding="utf-8"))
    h["lines"] = lines
    h["subpages"] = [sp for ln in lines for sp in ln["subpages"]]
    h["title"] = "Metal Cutting Band Saws & Bandsaws for Sale in Canada | NovoTech"
    h["meta_description"] = "Metal cutting band saws from Ø9″ to 87″: manual, semi-automatic, automatic, double column and vertical machines in a premium and a value line, plus a guide."
    h["intro"] = "Horizontal metal cutting band saws — metal bandsaws for steel, stainless, aluminum and other metals — for fabricators, machine shops and steel service centres across Canada, in two clearly separated lines: the premium Bekamak range built in Turkey, and NovoTech's own value line. Whether you are searching for a manual band saw for metal, a semi-automatic hydraulic bandsaw, an automatic CNC band saw machine or an industrial double column saw for heavy bar and bundles or a vertical band saw for contour cuts, blocks and plate, every machine is here with specifications in inches and millimetres, a CSA-approved panel, spare parts and technical support from Mississauga, ON, Canada."
    h["hero_image"] = "bk-hero-auto-350ga"
    h["hero_image_secondary"] = ["bk-hero-hub", "nt-bs315gf-1"]
    h["hero_points"] = ['<a href="#premium-line">Premium line: Bekamak</a>, Ø9″ to 87″ (230–2200 mm)',
                        '<a href="#value-line">Value line: NovoTech</a>, Ø10″ to 23-5/8″ (250–600 mm) — semi-automatic, automatic, double-column and vertical',
                        '<a href="#manual-band-saws-overview">Manual</a> (Bekamak), <a href="#semi-automatic-band-saws-overview">semi-automatic</a>, <a href="#automatic-band-saws-overview">automatic</a>, <a href="#double-column-band-saws-overview">double-column</a> and <a href="#vertical-band-saws-overview">vertical</a> saws',
                        '<a href="#buying-guide">Band saw buying guide</a>, blade selection and troubleshooting chart on this page']
    h["catalogue_pdfs"] = [PDF_BK, PDF_NF]
    h["range_lead"] = "Capacity at 0° for every model, one table per line. Each row links to the full specification table with miter capacities, blade sizes, motors and dimensions."
    h["section_label"] = "Band saws"
    h["related_blurb"] = "Both lines side by side: every Bekamak and NovoTech value-line band saw, the capacity tables and the band saw buying guide."
    h["origin_feature"] = {"title": "Two lines, one standard of support", "text": "Bekamak saws are built in Turkey with European components; value-line saws in China to North American standards."}
    json.dump(h, open(hp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("pages:", [sp["slug"] for ln in lines for sp in ln["subpages"]])


if __name__ == "__main__":
    main()
