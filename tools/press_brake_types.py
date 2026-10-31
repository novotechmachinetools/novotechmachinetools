#!/usr/bin/env python3
"""The three press-brake pages — hydraulic-press-brake.html, electric-press-brake.html and compact-hydraulic-press-brakes.html —
under the press-brake hub.  Each page holds every family of that kind NovoTech sells, premium and value lines as sections, with the
spec tables, photos, videos and brochures of the families (family set content/families/press-brakes.json, merged by
tools/press_brake_hub.py — run that first):

    python3 tools/press_brake_hub.py && python3 tools/press_brake_types.py

The pages replace the supplier pages dener-cnc-press-brakes and novotech-cnc-press-brakes (301s in src/root/.htaccess): buyers search for the kind of machine, not the supplier, and one URL per kind is what the
search engines rank (reports/ساختار صفحات محصول و سئو.md)."""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category
import press_brake_nav as PBN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "press-brakes"

BRAND_LINE = ("The premium line is built by Dener Makina in Kayseri, Turkey (press brakes since 1974); NovoTech's value line is built in China to our "
              "specification with Delem controls and Estun servo drives. All sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Premium and value lines, one supplier", "text": "Every press brake comes with a CSA-approved panel, a 1-year warranty and parts and technicians in Mississauga, ON, Canada — whichever line you choose."}

TONNAGE_FAQ = {"q": "How much tonnage and length do I need?",
               "a": "Air bending takes F = S² × 2 × R ÷ (1.4 × V) tonnes per metre of bend — the sheet thickness S and the V opening V in millimetres, the tensile strength R = 47 kg/mm² for mild steel (70 for stainless, 25 for aluminum), the formula behind the EUROSTAMP and Dener bending charts; in inches and US tons per foot it reads 575 × t² ÷ V. With the standard V of about 8 × the thickness, 3 mm needs about 24 t/m (8 US tons per foot), 6 mm 48 t/m (16), 1/4″ 54 t/m (18), 3/8″ in a 3″ V 80 t/m (27) and 1/2″ in a 5″ V 85 t/m (29). Multiply by the bend length and add about 20 % in reserve: 3 m × 6 mm is a 175-ton press brake, 10 ft × 1/4″ a 200 – 220 US ton machine, 10 ft × 3/8″ a 300 – 320 ton machine and 13 ft × 1/2″ a 400 – 450 ton machine. The tonnage calculator in the buying guide on the press brake page does the arithmetic for your thickness and length; tell us your thickest and longest bend and we size the brake and the tooling."}
TOOLING_FAQ = {"q": "What tooling fits, and do you stock it?",
               "a": "European-style (Promecam / Amada) segmented tooling fits every line: the premium Dener brakes carry European-style top-tool holders, the value-line brakes their own clamping, and a sectioned punch set with a 2-V or 4-V die ships with every machine (a 4-V die with the Dener brakes, a 2-V die with the value line) — tell us which tooling standard your shop already has and we fit the holders to match. NovoTech stocks Eurostamp press brake tooling in Canada — punches, dies, radius, hemming and joggle tools, gooseneck and special profiles — and sizes it to your machine; quick-release, pneumatic and Wila hydraulic clamping and American-style adapters are options, not standard equipment."}
SAFETY_FAQ = {"q": "What about safety and the Ontario pre-start review?",
              "a": "Side guards, an enclosed rear guard, interlocked doors and an anti-panic foot pedal with emergency stop are standard; DSP laser finger protection is standard on the WAD CNC press brakes and the Dener XL, and on the other machines DSP or Fiessler laser protection and light curtains are options we recommend for every CNC press brake. In Ontario a new press brake needs a pre-start health and safety review (PSR) under Regulation 851 before it runs."}
SERVICE_FAQ = {"q": "Do you deliver, install and service in Canada?",
               "a": "Yes — NovoTech sells, installs and supports press brakes across Canada and the United States. Installation, commissioning and operator training are free of charge in the Greater Toronto Area; outside the GTA our technicians do the same work at an additional charge. Parts are stocked in Canada. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request), a 1-year warranty and remote diagnostics through the control."}
DELIVERY_FAQ = {"q": "What does delivery cost, and who unloads the machine?", "a": "A press brake ordered from the factory (back-ordered) travels in its container straight from the port, customs and the rail yard to your plant door: in the Greater Toronto Area that delivery is free; outside the GTA the freight is quoted and charged. A machine from NovoTech's stock is loaded, shipped and unloaded at the buyer's cost. In every case unloading is the buyer's responsibility and expense — the crane or forklift, the rigging and moving the machine onto its foundation — so book a rigger for the delivery day; we are glad to recommend riggers who know press brakes and to tell you the weight and lifting points."}
OIL_FAQ = {"q": "Is the hydraulic oil included?", "a": "No — the hydraulic oil is bought by the customer. Before commissioning, fill the tank with ISO VG 46 anti-wear hydraulic oil (AW 46) in the quantity shown in the specification table for your model; our technician checks the level and bleeds the system during installation. Electric press brakes have no hydraulic oil at all."}

HYDRAULIC = dict(
    title="Hydraulic Press Brakes for Sale in Canada — CNC, Hybrid & NC, 33–1,323 Tons | NovoTech",
    meta="Hydraulic press brakes sold, installed and supported in Canada: CNC brakes 55 – 1,323 US tons, the mild hybrid XL, and NC torsion-bar brakes from 33 tons — premium and value lines, CSA panels, Delem and ESA controls.",
    h1="Hydraulic press brakes — CNC, hybrid and NC, 33 to 1,323 US tons",
    intro="A hydraulic press brake bends sheet and plate between a punch and a V-die with two hydraulic cylinders, giving full force over the whole "
          "stroke at the lowest price per ton — the machine for plate, long parts and production. NovoTech sells three kinds in Canada, all on this "
          "page: CNC hydraulic press brakes with linear scales, servo valves, crowning and a graphic control — the premium Dener XL in 18 models "
          "from 66 to 661 US tons and 5 to 20 ft, and NovoTech's own value line from 55 to 331 tons, heavy-duty and tandem to 1,323 tons and 26 ft; "
          "hybrid press brakes — the mild hybrid servo motor and pump, an option on every XL that cuts energy by 42 – 58 %; and NC torsion-bar press brakes from 33 to 441 tons for "
          "repeat parts in one material. Every machine comes with a CSA-approved panel and a 1-year warranty, and is "
          "installed, trained and supported from Mississauga, ON, Canada. For a brake with no hydraulic oil see the electric press brakes; for "
          "33 – 66 ton machines over 4 – 5 ft, the compact press brakes.",
    # the hero bullets link to the products further down the page (the owner, Oct 30 2026)
    points=['CNC hydraulic: <a href="#dn-xl">premium line 66 – 661 US tons × 5 – 20 ft</a> (ESA / Delem, 6-axis gauges); '
            '<a href="#vl-wad">value line 55 – 331 tons</a>, <a href="#vl-wad-heavy">heavy-duty to 1,323 tons × 26 ft</a>',
            'Hybrid: the <a href="#dn-xl">mild hybrid servo pump on any XL</a> — 42 – 58 % less energy, 17 – 75 % faster approach and return, '
            'quieter — and standard on every <a href="#vl-wad">value-line WAD</a>',
            '<a href="#vl-nc">NC torsion-bar 33 – 441 tons</a> with Estun control for repeat parts in one material — the simplest hydraulic brake to run and maintain'],
    hero="dn-xl-1", minis=["vl-wad-1", "vl-nc-1"],
    groups=[("pb-premium", "CNC hydraulic press brakes · premium line", "", "dener"),   # no lead line (the owner, Oct 31 2026)
            ("pb-value", "CNC hydraulic press brakes · value line", "", "novotech"),   # no lead line (the owner, Oct 31 2026)
            ("pb-nc", "NC hydraulic press brakes — torsion bar · value line", "", "novotech"),   # no lead line (the owner, Oct 31 2026)
            # the heavy-duty and tandem machines are the last product on the page (the owner, Oct 31 2026)
            ("pb-heavy", "Heavy-duty and tandem CNC press brakes · value line", "", "novotech")],
    faq=[{"q": "CNC, hybrid or NC — which hydraulic press brake do I need?",
          "a": "A CNC brake measures the ram on linear scales and corrects it through servo valves, calculates the bend from the drawing, crowns the bed and changes material in the program — the machine for mixed work, tight angles and multi-bend parts, and the one most Canadian shops buy. The hybrid is a CNC brake with a servo pump: it costs a little more and pays it back in power, speed and noise when the brake runs all day. An NC brake positions the back gauge and the ram depth from a stored program with the cylinders kept in step by a torsion bar — rigid, cheap to maintain, right for the same parts in one material every day. For 4 – 7 ft work in sheet up to 8 ga, where a 100-ton machine is more than you need, see the compact press brakes."},
         {"q": "Premium line or value line?",
          "a": "The premium Dener XL is built in Turkey on the heaviest frame, with ESA or Delem controls, back gauges to 6 axes, sheet followers, robot cells and parts stocked in Canada — the machines for plate, 3/8″ and 1/2″ over 10 to 20 ft, two shifts, a long options list. NovoTech's value line is the same architecture — monoblock frame, servo valves, linear scales, Delem control — built in China to our specification at about two-thirds of the price: the right buy for a job shop that needs a 100 – 300 ton CNC brake or an NC brake for repeat parts, and the only line that goes to 1,323 tons and 26 ft. Both are installed and supported by the same NovoTech technicians."},
         TONNAGE_FAQ,
         {"q": "What is a hybrid press brake?",
          "a": "On a conventional hydraulic brake the motor and pump run at full speed all day, whether the ram moves or not. A hybrid drives the hydraulics with servo motors, so the pump turns only while the ram moves, at the speed the ram needs. Dener builds it two ways. The mild hybrid, an option on every XL, keeps the XL's hydraulic circuit and replaces only the AC motor and fixed pump with a servo motor and servo pump: Dener measures 42 – 58 % energy saving and 17 – 75 % faster approach and return against the standard XL, with less heat in the oil and a quieter shop, and everything else — frame, cylinders, valves, tooling, controls — is the XL. On NovoTech's value line, every WAD CNC brake has the mild hybrid drive as standard."},
         {"q": "Which control comes with the machine?",
          "a": "The premium XL comes with the 15.6″ ESA S840 2D graphic touch-screen control (Delem DA-66S / 69S and the ESA S875 W 3D control are options): draw the profile, the control calculates the bend sequence, tonnage, back-gauge positions and crowning and checks the part for collisions with the tools and the machine. The value-line CNC brakes come with the 15″ Delem DA-53Tx — the 18.5″ DA-58Tx (2D graphic), the 24″ DA-66S and DA-69S, the ESA S840 and S875 W and the Cybelec CybTouch 12 are options; the NC brakes with the Estun E21PS (E315PS, Delem DA-41T or ESA S630 as options). All program in inches or millimetres, and the buying guide on the press brake page compares every one of them."},
         {"q": "What back gauge and axes are available?",
          "a": "Every CNC machine has the Y1 and Y2 ram axes and an X back-gauge axis on a ball screw and linear guides. Options go up to the 6-axis gauge with X1, X2, R1, R2, Z1 and Z2 — two independently positioned fingers for angled flanges — plus a CNC crowning axis; the NC brakes have X and the depth stop. The back gauge is set by the control for every bend of the program."},
         TOOLING_FAQ, SAFETY_FAQ, SERVICE_FAQ, DELIVERY_FAQ, OIL_FAQ, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about hydraulic press brakes",
    related_pages=[{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "v-grooving-machine.html", "label": "V-grooving machines"}],
    related_title="More bending and cutting machinery from NovoTech",
)

ELECTRIC = dict(
    title="Electric Press Brakes for Sale in Canada — Servo-Electric & Ball-Screw, 3–220 Tons | NovoTech",
    meta="Servo-electric and ball-screw press brakes sold, installed and supported in Canada: 3 to 220 US tons, no hydraulic oil, ±0.01 mm repeatability, about twice the speed and 70 % less power — premium and value lines with CSA panels.",
    h1="Electric press brakes — servo-electric and ball-screw, 3 to 220 US tons",
    intro="An electric press brake drives the ram with servo motors and ball screws or belts instead of hydraulic cylinders: no oil, no pump "
          "running idle, ±0.01 mm repeatability, bending speeds to 30 mm/s and about 70 % less power — usually the better buy for 20 ga to 1/4″ "
          "sheet in a job shop, an enclosure or HVAC plant, or anywhere clean and quiet matters. NovoTech sells two lines in Canada, both on this "
          "page: the premium Dener DDM servo-electric press brakes from 44 to 220 US tons and 5 to 13 ft with the ESA S875 3D control, and the "
          "DDS ball-screw brakes of 22 and 44 tons for small parts; and NovoTech's own value-line electric press brakes, ball-screw driven, from "
          "11 to 176 US tons and 1.6 to 10.5 ft with Delem control, plus 3 to 13 ton bench machines. Every machine comes with a CSA-approved "
          "panel and a 1-year warranty, installed, trained and supported from Mississauga, ON, Canada. For 3/8″ plate, "
          "tonnage above 220 tons or the lowest price per ton, see the hydraulic press brakes.",
    points=['Premium line: <a href="#dn-ddm">DDM servo-electric 44 – 220 US tons × 5 – 13 ft</a>, ESA S875 W 3D control; '
            '<a href="#dn-dds">DDS ball-screw 22 and 44 tons</a>',
            'Value line: <a href="#vl-wadg">electric ball-screw brakes 11 – 176 US tons × 1.6 – 10.5 ft</a> with Delem control; '
            '<a href="#vl-wadg-mini">3 – 13 ton bench brakes</a>',
            "±0.01 mm, power only while the ram moves, no hydraulic oil or filters — about twice the speed of a hydraulic brake on sheet"],
    hero="dn-ddm-2", minis=["vl-wadg-1", "dn-dds-1"],
    groups=[("pb-servo", "Servo-electric and ball-screw press brakes · premium line", "", "dener"),   # no lead line (the owner, Oct 31 2026)
            ("pb-value-electric", "Electric press brakes · value line", "", "novotech")],   # no lead line (the owner, Oct 31 2026)
    faq=[{"q": "Electric or hydraulic — which press brake should I buy?",
          "a": "Electric when the work is sheet — 20 ga to 1/4″, brackets, enclosures, panels, stainless and aluminum — and when accuracy, speed, energy and a clean floor matter: the servo drive repeats to ±0.01 mm, bends at about twice the speed of a hydraulic brake and draws power only while the ram moves. Hydraulic when the work is plate, 3/8″ and up, long parts over 13 ft, or tonnage above 220 US tons, and when the lowest price per ton decides. Many shops run one of each; the hydraulic press brakes have their own page."},
         {"q": "Servo-electric or ball-screw — what is the difference?",
          "a": "Both are electric. The DDM servo-electric brake drives the ram through servo motors and a belt-and-pulley system across the whole bending length, which is how it reaches 220 US tons and 13 ft with the force distributed evenly along the beam. The DDS and the value-line brakes drive the ram with two ball screws, one per side, each on its own servo motor — simpler, very accurate, and the right construction up to about 176 tons and 10 ft."},
         {"q": "Premium line or value line?",
          "a": "The premium DDM is built in Turkey by Dener with the 21.5″ ESA S875 W 3D control, 6-axis back gauges, laser angle measurement and robot cells as options, and parts stocked in Canada — the production electric brake. NovoTech's value-line electric brakes are built in China to our specification with Delem control and the same Estun servo components, at about two-thirds of the price — the electric brake for a job shop or a second machine for small parts. Both are installed and supported by the same NovoTech technicians."},
         TONNAGE_FAQ,
         {"q": "What does an electric press brake cost to run?",
          "a": "There is no hydraulic oil to buy, filter, cool or dispose of, no pump motor idling between bends, and the servo motors regenerate on the return stroke: Dener measures about 70 % less energy than a hydraulic brake of the same tonnage on sheet work, and the maintenance schedule is lubrication of the ball screws and guides. The machines are also quieter, which matters in a shop that runs the brake all day."},
         TOOLING_FAQ, SAFETY_FAQ, SERVICE_FAQ, DELIVERY_FAQ, OIL_FAQ, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about electric press brakes",
    related_pages=[{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring before bending"}],
    related_title="More bending and cutting machinery from NovoTech",
)

COMPACT = dict(
    title="Compact Hydraulic Press Brakes for Sale in Canada — 16 to 66 Tons, 2 to 8 ft | NovoTech",
    meta="Small hydraulic press brakes sold, installed and supported in Canada: the Dener XL 1560 compact CNC brake, 66 US tons × 5 ft with ESA S840 control, NovoTech value-line WAD-50T CNC and WC67K-30T NC compacts over 4.3 – 5.2 ft, and HBV bending brakes 16 – 35 tons.",
    h1="Compact hydraulic press brakes — 16 to 66 US tons, 2 to 8 ft",
    intro="A compact hydraulic press brake bends sheet between a punch and a V-die like its big brothers, at the size that fits a sheet-metal "
          "shop rather than a steel-fabrication plant: 2 to 8 ft of bending length and 16 to 66 US tons, on a footprint that goes through a "
          "door and runs on a 600 V or 208 V supply. NovoTech sells three on this page: the Dener XL 1560 — the smallest machine of the "
          "premium line, 66 US tons over 5 ft with the 15.6″ ESA S840 2D control, Y1-Y2 ram on linear scales, a ball-screw X back gauge and "
          "EUROSTAMP tooling in the crate, built in Turkey; NovoTech's own value-line compacts, built to our specification — the WAD-50T "
          "CNC brakes, 55 US tons over 4.3 and 5.2 ft with servo valves and a Delem DA-53Tx, and the WC67K-30T torsion-bar NC brake, "
          "33 US tons over 5.2 ft with an Estun E21PS; and the value-line HBV bending brakes, 16 to 35 tons, with a four-way V-block "
          "(HBV24 / 48) or two cylinders (HBV-1250 / 2540) for brackets, clips and short parts in plate to 3/16″. For HVAC fittings, "
          "enclosures, signage, brackets and job-shop work where a 100-ton machine is more than you need. Every machine comes with a "
          "CSA-approved panel and a 1-year warranty, installed, trained and supported from Mississauga, ON, Canada. For 10 ft and longer, or "
          "1/4″ plate and up, see the hydraulic press brakes; for a brake with no hydraulic oil the electric press brakes.",
    points=['<a href="#dn-xl-1560">Dener XL 1560: 66 US tons × 5 ft</a>, 15.7″ throat, ESA S840 2D control, Y1-Y2-X axes on linear scales, '
            'EUROSTAMP 1281 punch and 2067 4-way die included — premium line, made in Turkey',
            'Value line: <a href="#vl-wad-compact">WAD-50T/1300 and 1600 CNC brakes</a>, 55 US tons × 4.3 – 5.2 ft, 4 axes with Delem DA-53Tx; '
            '<a href="#vl-nc-compact">WC67K-30T/1600 NC torsion-bar brake</a>, 33 US tons × 5.2 ft with Estun E21PS',
            'Value-line <a href="#tt-hbv">HBV bending brakes</a>: 16.5 – 35 US tons, 5/32″ × 24 – 48″, 3/16″ × 49″ and 1/8″ × 100″, four-way V-block or two cylinders'],
    hero="dn-xl1560-studio", minis=["vl-cp-wad1600", "vl-cp-nc-adh"],
    groups=[("pb-compact-dener", "Compact CNC press brake · Dener premium line", "", "dener"),   # no lead line (the owner, Oct 31 2026)
            ("pb-compact-cnc", "Compact CNC press brakes · NovoTech value line", "", "novotech"),   # no lead line (the owner, Oct 31 2026)
            ("pb-compact-nc", "Compact NC press brake · NovoTech value line", "", "novotech")],   # no lead line (the owner, Oct 31 2026)
    faq=[{"q": "What tonnage do I need?",
          "a": "Bending force depends on the sheet thickness, the bend length and the V-die opening: F = S² × 2 × R ÷ (1.4 × V) tonnes per metre with S and V in millimetres and R = 47 kg/mm² for mild steel — in inches and US tons per foot about 575 × t² ÷ V. In a V of 8 × the thickness, a 4 ft bend takes about 16 US tons in 16 ga, 39 tons in 10 ga and 47 tons in 8 ga (0.16″); a wider die lowers the force — 8 ga in a 2″ V takes about 31 tons over 4 ft — at the cost of a larger inside radius. The control calculates the exact force for the tool and material you enter; send us your thickest and longest bend and we size the machine."},
         {"q": "Dener XL 1560 or a value-line compact?",
          "a": "The XL 1560 is the premium machine: the heaviest frame, servo-valve hydraulics, an ESA 2D control with collision control, the DSP-AP laser finger guard as standard, every Dener option open to it — 3D controls, 4- to 6-axis back gauges, CNC crowning, Wila clamping, robot cells — and parts stocked in Canada; it bends 3/16″ over the full 5 ft and 1/4″ over 4 ft. The value-line WAD-50T is the same electro-hydraulic servo architecture (servo valves, linear scales, Delem control) built to our specification at a lower price, for 1/8″ over 5.2 ft; the WC67K-30T is the simple torsion-bar NC brake for one material and repeat parts. If the brake runs all day or you program from CAD, the XL; if it bends brackets and enclosures a few hours a day, the value line."},
         {"q": "NC or CNC?",
          "a": "An NC brake (the WC67K-30T) sets the ram depth and the back gauge from a stored program, with the two cylinders kept in step by a torsion bar — enough for the same parts in one material. A CNC brake (the XL 1560 and the WAD-50T) measures the ram on linear scales and corrects it through servo valves, calculates tonnage, bend sequence and gauge positions from the drawing, and changes material and tool in the program — the machine for mixed work, tight angles and multi-bend parts. The buying guide on the press brake page compares every control these machines are sold with."},
         {"q": "Press brake or HBV bending brake?",
          "a": "The XL 1560, WAD-50T and WC67K-30T are press brakes: a programmable ram, a motorised back gauge, segmented tooling and a guard, for sheet work all day. The HBV is a hydraulic bending brake for short parts in plate — brackets, clips, tabs — bent on a four-way V-block (HBV24 / 48) or between two cylinders (HBV-1250 / 2540) with a hand-wheel back gauge, at a fraction of the price. If you bend panels and enclosures, a press brake; if you bend 3/16″ plate brackets a few at a time, the HBV."},
         TOOLING_FAQ,
         {"q": "Are they safe to run without a separate guarding system?",
          "a": "Every compact press brake carries side guards, an enclosed rear guard with interlocked doors and a foot pedal with emergency stop; the Dener XL 1560 comes with the DSP-AP laser finger guard and an MCS safety PLC as standard, and on the value-line machines a laser guard — DSP, Fiessler AKAS or a light curtain — is an option we recommend. In Ontario a new press brake needs a pre-start health and safety review (PSR) under Regulation 851 before it runs."},
         SERVICE_FAQ, DELIVERY_FAQ, OIL_FAQ, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about compact press brakes",
    related_pages=[{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "folder-sheet-metal-brake.html", "label": "Sheet metal brakes & folders"},
                   {"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}, {"href": "corner-notcher.html", "label": "Corner notchers"}],
    related_title="More sheet-metal machinery from NovoTech",
)

VIDEOS = {
    # Dener's introduction film from NovoTech's channel in place of the XL 4000 × 220 clip (the owner, Oct 31 2026)
    "hydraulic-press-brake": {"intro_video": {"id": "A1i_NljuVQo", "title": "Dener introduction film — the plant in Kayseri, Turkey, where the XL press brakes are built", "thumb": "video-A1i_NljuVQo", "duration": "PT2M52S"},
                              "intro_video_heading": "Inside the factory where the machines are built",
                              "intro_video_text": "Dener Makina's introduction film: the plant in Kayseri, Turkey, where Dener has built press brakes since 1974 — the premium-line machines NovoTech sells, installs and supports in Canada."},
    "electric-press-brake": {"intro_video": {"id": "ZujRJUhckG4", "title": "DDM 10030 — 10 ft × 100 ton servo-electric CNC press brake", "thumb": "video-ZujRJUhckG4", "duration": "PT0M51S"},
                             "intro_video_heading": "The servo-electric press brake at work",
                             "intro_video_text": "A 10 ft × 100 ton DDM bending sheet: no hydraulic oil, servo drive, ±0.01 mm repeatability."},
}


def build():
    fs = json.load(open(os.path.join(ROOT, "content", "families", f"{SET}.json"), encoding="utf-8"))
    fams = {fid: dict(fs["families"][fid], id=fid) for fid in fs["order"]}
    manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
    for slug, page in (("hydraulic-press-brake", HYDRAULIC), ("electric-press-brake", ELECTRIC), ("compact-hydraulic-press-brakes", COMPACT)):
        members = [dict(fams[fid], group=g) for _, fid, g in PBN.PAGES[slug]]
        pdfs, seen = [], set()
        for f in members:
            pd = f.get("pdf")
            if pd and pd["file"] not in seen:
                seen.add(pd["file"]); pdfs.append(pd)
        video = VIDEOS[slug] if slug in VIDEOS and VIDEOS[slug]["intro_video"]["thumb"] in manifest else {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}
        write_category(slug, page, members, SET, PBN.SECTION, hub=PBN.hub(), siblings=PBN.siblings(),
                       extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **video,
                              "why_title": "Included with every press brake from NovoTech", "why_features": PBN.why_features(),
                              "nav_label": next(nav for s, _, _, _, nav, _ in PBN.SUBPAGES if s == slug),
                              "catalogue_pdf": None, "catalogue_pdfs": pdfs})
        print(f"{slug}: {len(members)} families, {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
