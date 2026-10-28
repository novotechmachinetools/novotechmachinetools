#!/usr/bin/env python3
"""Dener pages: press-brake, laser-cutting-machine (sheet lasers), tube-laser-cutting-machine, panel-bender — family set
content/families/dener.json, photos from tools/dener_photos.py (section 'dener').  The Dener shears are appended to the
shears page by tools/saymak_pages.py (set 'shears').

    python3 tools/dener_photos.py                       # export the renders / frames to tools/src-images/dener
    python3 tools/dener_pages.py                        # families + pages + image_map entries (tools/dener_keys.txt)
    python3 tools/yt_thumbs.py $(cat tools/dener_vids.txt)
    python3 tools/make_images.py --only $(cat tools/dener_keys.txt)
"""
import json
import os
import shutil

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import dener_data as D
import dener_photos as PH
import vl_sheet_data as VL   # NovoTech value-line panel benders below the Dener machine on panel-bender.html
import senfeng_data as SF    # Senfeng lasers, tube lasers and panel benders: the value line below Dener, under the Senfeng brand
import senfeng_pages as SFP
import vl_laser_data as VLL   # NovoTech value-line lasers (ULF / ULE / ULFT / ULET, ULT): their own pages, families kept in this set for the hubs
import vl_laser_pages as VLP
import laser_nav as LN
import press_brake_nav as PBN
import shear_nav as SN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "dener"
BRAND = D.BRAND
SRC_PDF = "/home/claude/dener/"
PDF_PB_FILE = "files/NovoTech-Dener-Hydraulic-Press-Brakes-2026.pdf"
PDF_SERVO_FILE = "files/NovoTech-Dener-Servo-Press-Brakes-2026.pdf"
PDF_LASER_FILE = "files/NovoTech-Dener-Fiber-Lasers-2026.pdf"
PDF_TUBE_FILE = "files/NovoTech-Dener-Tube-Lasers-2026.pdf"
PDF_PANEL_FILE = "files/NovoTech-Dener-Panel-Bender-2026.pdf"
PDF_SHEAR_FILE = "files/NovoTech-Dener-Hydraulic-Shears-2026.pdf"
PDF_VL_PANEL_FILE = "files/NovoTech-Panel-Benders-Value-Line-2026.pdf"
COPY_PDFS = {PDF_PB_FILE: "nt-hydraulic-pb.pdf", PDF_SERVO_FILE: "pdf2/NovoTech_Dener_Servo_Press_Brakes (1).pdf", PDF_LASER_FILE: "nt-fiber-laser.pdf"}

BRAND_LINE = ("Dener Makina builds press brakes, shears and fiber lasers in Kayseri, Turkey — 52 years, exports to more than 100 countries, "
              "Dener Canada in Mississauga, ON, Canada. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Turkey by Dener Makina", "text": "Dener has built sheet-metal machinery in Kayseri since 1974 — a 1.3 million m² campus, "
          "its own design awards (Good Design, European Product Design, Design Turkey) and offices in the USA, Canada, Germany and India."}
INTRO_VIDEO = {"intro_video": {"id": "A1i_NljuVQo", "title": "DENER Group introduction video", "thumb": "video-A1i_NljuVQo", "duration": "PT2M52S"},
               "intro_video_heading": "Inside the factory — where the machines are built",
               "intro_video_text": "A tour of Dener Makina in Kayseri, Turkey, where the press brakes, shears and fiber lasers on this page are designed and built."}
CRUMBS_TAIL = []


def pdf(file, label):
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": label, "size": size}


PAGE_PB = dict(
    title="Dener CNC Press Brakes, 22–661 Tons | NovoTech",
    meta="XL hydraulic CNC press brakes to 661 US tons × 20 ft, XH hybrid servo-pump brakes, DDM / DDS servo-electric brakes from 22 tons. Made in Turkey; sold in Canada.",
    h1="Dener CNC press brakes — hydraulic, hybrid, servo-electric and ball-screw",
    intro="A press brake bends sheet and plate between a punch and a V-die; the CNC positions the back gauge and controls the ram depth, "
          "crowning and angle, so the operator loads the sheet and presses the pedal. NovoTech sells Dener press brakes in Canada — the "
          "XL hydraulic press brake in 18 models from 66 to 661 US tons and 5 to 20 ft, the XH hybrid that puts a servo pump on the same "
          "frame for 42 – 58 % less energy, the DDM servo-electric press brake with no hydraulic oil from 44 to 220 US tons, and the DDS "
          "ball-screw press brake from 22 US tons for small parts. ESA S640 / S875 or Delem DA-66S / 69S controls, European-style tooling, "
          "back gauges to 6 axes, crowning, angle measurement, sheet followers and robot cells. This is the premium line; NovoTech's own "
          "value-line CNC press brakes and the ISITAN compact press brakes have pages of their own. Installed and supported from Mississauga, ON, Canada, "
          "with a CSA-approved panel and Dener Canada parts.",
    points=["XL hydraulic: 18 models, 66 – 661 US tons × 5 – 20 ft; tandem to 60 ft and 1,800 tons",
            "XH hybrid: servo pump on the XL frame — 42 – 58 % less energy, faster approach and return",
            "DDM servo-electric 44 – 220 tons and DDS ball-screw 22 / 44 tons — no hydraulic oil"],
    hero="dn-xl-1", minis=["dn-ddm-2", "dn-xh-1"],
    groups=[("pb-hydraulic", "XL hydraulic CNC press brakes", "The standard: a monoblock frame, Hawe hydraulics and an ESA 2D control, 5 to 20 ft and 66 to 661 US tons.", BRAND),
            ("pb-hybrid", "XH hybrid press brakes", "The XL with a servo-driven pump — the same frame and cylinders, less energy, more speed, less noise.", BRAND),
            ("pb-servo", "Servo-electric and ball-screw press brakes", "No hydraulic oil: the DDM servo-electric brake for production to 220 tons and the DDS ball-screw brake for small parts.", BRAND)],
    faq=[{"q": "Hydraulic, hybrid or servo-electric — which press brake should I buy?",
          "a": "A hydraulic XL is the lowest price per ton and bends anything from 5 ft brackets to 20 ft, 1/2″ plate; it is the right machine when tonnage and length matter more than cycle time. The XH hybrid is the same machine with a servo pump: it costs a little more and pays it back in power (42 – 58 % less), speed and noise — the right choice for a shop that runs the brake all day. The DDM servo-electric brake has no oil at all, bends at twice the speed with 0.01 mm repeatability and draws power only while the ram moves — the choice for high-mix job shops and clean environments up to 220 US tons × 13 ft. Below 44 tons the DDS ball-screw brake is the compact, plug-in electric machine for boxes and brackets."},
         {"q": "How much tonnage do I need?",
          "a": "Air bending mild steel takes about 575 × t² ÷ V US tons per foot, with the thickness t and the V opening in inches: in the standard V = 8 × thickness die that is about 4 tons per foot for 16 ga, 9 for 1/8″, 13.5 for 3/16″, 18 for 1/4″ and 36 for 1/2″ (29 in a 10 × t die); stainless needs about 50 % more, aluminum about half. With about 20 % headroom, a 10 ft × 1/4″ job is therefore a 175 – 220 ton machine, and 10 ft × 1/2″, bent in a 5 – 6″ V, a 300 – 400 ton machine. Tell us the thickest and longest bend you make and we size the brake and the tooling."},
         {"q": "Which control comes with the machine?",
          "a": "The XL and DDS come with the 15″ ESA S640 2D graphic control: draw the profile, the control calculates the bend sequence, tonnage, back-gauge positions and crowning. The DDM comes with the 21″ ESA S875 W 3D control with 3D simulation and offline programming. Delem DA-66S (2D) and DA-69S (3D) are options on every machine, as is the ESA S875 W on the XL. All of them program in inches or millimetres and import DXF files."},
         {"q": "What is a hybrid press brake?",
          "a": "On a conventional hydraulic brake the motor and pump run at full speed all day, whether the ram moves or not. The XH hybrid replaces the AC motor and fixed pump with a servo motor driving an inverter pump: the pump turns only while the ram moves, at the speed the ram needs. Dener measures 42 – 58 % energy saving and 17 – 75 % faster approach and return against the XL of the same tonnage, with less heat in the oil and a quieter shop. Everything else — frame, cylinders, valves, tooling, controls — is the XL."},
         {"q": "What back gauge and axes are available?",
          "a": "Every machine has the Y1 and Y2 ram axes and an X back-gauge axis on a ball screw and linear guides; the DDM adds R (height) as standard. Options go up to the 6-axis ATF gauge with X1, X2, R1, R2, Z1 and Z2 — two independently positioned fingers for angled flanges — plus a CNC crowning axis and the Dual X-Prime fingers. The back gauge is set by the control for every bend of the program."},
         {"q": "Which tooling fits?",
          "a": "European-style (Promecam / Amada) segmented punches and dies with European-style holders are standard; Wila mechanical or hydraulic clamping, quick-release and pneumatic clamping are options, and American-style tooling can be fitted with an adapter. NovoTech stocks Eurostamp press brake tooling in Canada — punches, dies, radius tools, hemming and joggle tools — and sizes it to your machine."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes. Machines ship from Kayseri to Mississauga, ON, Canada; we unload, level, commission and train your operators, and Dener Canada stocks parts here. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request), a 1-year warranty and remote diagnostics through the control."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about press brakes",
    related_pages=[{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "horizontal-press-brake.html", "label": "Horizontal press brakes"}],
    related_title="More bending and cutting machinery from NovoTech",
)

PAGE_LASER = dict(
    title="Dener Fiber Laser Cutting Machines, 3–40 kW | NovoTech",
    meta="GFL production lasers with 1.5 G gantry and pallet changer, 5 × 10 to 6.6 × 20 ft; Smart series closed, semi-closed to 13 × 82 ft and open-type. Made in Turkey.",
    h1="Dener fiber lasers — GFL production lasers and the Smart series, 5 × 10 to 13 × 82 ft, 3 to 40 kW",
    intro="Dener's sheet lasers are the premium line of NovoTech's laser section: built in Kayseri, Turkey, on stress-relieved frames with IPG, "
          "Raycus or nLIGHT sources, Precitec autofocus heads and nesting software, and backed by Dener Canada parts in Mississauga, ON, Canada. The GFL is "
          "the production machine — a space-frame gantry rated for 1.5 G and 394 ft/min, a pallet changer that loads the next sheet while the "
          "first is cut, in 5 × 10, 6.6 × 13 and 6.6 × 20 ft with 3 to 40 kW. The Smart series comes from the same factory at a lower price: "
          "the closed-type with laser-safe cabin and double exchange table in six sizes to a 41 ft bed, the semi-closed single-table machines "
          "from 8.2 × 20 to 13 × 82 ft for long plate, and the open-type 3 – 6 kW entry laser. Loading towers, sheet storage, bevel heads and "
          "air-cutting packages are available for all of them. A 6 kW machine cuts 3/4″ mild steel; 12 kW cuts 1″, 20 – 40 kW 1-1/2″ and beyond. "
          "Installed, trained and supported from Mississauga, ON, Canada.",
    points=["GFL: 1.5 G, 394 ft/min, ±0.03 mm, pallet changer — 5 × 10 to 6.6 × 20 ft, 3 – 40 kW",
            "Smart closed-type: double table, 1 G, 459 ft/min, six sizes to 8.5 × 41 ft; semi-closed single table to 13 × 82 ft",
            "Smart open-type: 3 or 6 kW, 5 × 10 to 6.6 × 20 ft — the lowest-priced Dener laser; towers, storage and bevel heads optional"],
    hero="dn-gfl-3", minis=["dn-smart-1", "dn-gfl-2"],
    groups=[("laser-gfl", "GFL production fiber lasers", "Dener's premium sheet laser: 1.5 G, pallet changer, 3 – 40 kW — built for a job shop that cuts all day.", BRAND),
            ("laser-smart", "Smart fiber lasers", "The economy line from the same factory: closed, semi-closed and open machines in table sizes to 13 × 82 ft.", BRAND)],
    faq=[{"q": "GFL or Smart — what is the difference?",
          "a": "Both come from Dener's Kayseri plant with the same sources, heads and software. The GFL is the production machine: a heavier stress-relieved frame and space-frame bridge rated for 1.5 G, a pallet changer and the full option list — the machine for two shifts a day. The Smart series is built to a lower price: the closed-type still has a double exchange table and 1 G, the semi-closed machines offer very large single tables, and the open-type is the entry-level 3 – 6 kW laser. Same cut quality; the GFL is faster between parts and lasts longer at high duty."},
         {"q": "Which Smart — closed, semi-closed or open?",
          "a": "Closed-type when you cut all day: the double exchange table keeps the laser cutting while you load, and the cabin keeps fumes and the beam inside. Semi-closed when the parts are long — 20 to 82 ft single tables for beams, ship sections and plate that no standard laser takes. Open-type when the budget comes first and the sheets are loaded by hand or forklift from any side: 3 or 6 kW, 5 × 10 to 6.6 × 20 ft, the lowest-priced Dener laser."},
         {"q": "What is in a Dener laser as standard?",
          "a": "An IPG, Raycus or nLIGHT fiber source, a Precitec or Raytools autofocus cutting head with capacitive height sensing and collision protection, a stress-relieved welded frame, pneumatic fume-extraction compartments under the table and scrap boxes on wheels, a chiller, a CNC with nesting software, cutting database and production reports, and a remote handset. Cutting gas regulators, dust collector connections and the CSA-approved panel with a 600 V transformer are included in the NovoTech package."},
         {"q": "What can be added later?",
          "a": "A loading / unloading tower that feeds the pallet changer, sheet storage with several shelves for lights-out production, part sorting, a bevel head for weld preparation, a marking head, and the intelligent air-cutting package that replaces nitrogen on sheet to about 1/4″. The GFL and the closed-type Smart are prepared for the tower from the factory."},
         {"q": "How does Dener compare with the Senfeng value line?",
          "a": "Dener is the premium line — heavier frame rated for 1.5 G, Precitec heads, IPG / nLIGHT sources, longer life at high duty and Dener Canada parts in Mississauga, ON, Canada. Senfeng builds its own sources and heads and sells for less, with a range Dener does not cover (4 × 4 ft compact machines, 60 kW plate gantries, sheet-and-tube combos, coil-fed lines). The comparison, the laser power guide and the capacity table for both lines are on the sheet laser cutters overview."},
         {"q": "What does the machine need on site?",
          "a": "A level floor, 600 V 3-phase (with the transformer we supply) or 480 V, a chiller (included), assist gas — oxygen for mild steel, nitrogen or compressed air for stainless and aluminum — a dust collector and a compressed-air supply. A 6 kW GFL 3015 draws about 30 kW in total and needs roughly 33 × 20 ft with the pallet changer. Delivery, installation and operator training are done by NovoTech from Mississauga, ON, Canada."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about Dener fiber lasers",
    related_pages=[{"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}, {"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "panel-bender.html", "label": "CNC panel bender"}],
    related_title="Machinery that works alongside a laser",
)

PAGE_TUBE = dict(
    title="Dener Tube Laser Cutting Machines, Ø0.3–25″ | NovoTech",
    meta="E-FTL tube lasers with 1 G servo chucks for Ø0.3″ to 13.8″; heavy FTL for pipe, tube and beams to Ø25.2″ and 12 m bars. Bundle loaders, bevel heads, 3 – 20 kW.",
    h1="Dener tube lasers — E-FTL and FTL, Ø0.3″ to 25.2″, bars to 39.4 ft, 3 to 20 kW",
    intro="Dener's tube lasers are the premium line of NovoTech's tube laser section: built in Kayseri, Turkey, with servo chucks, Precitec "
          "heads and 3 to 20 kW sources, and backed by Dener Canada parts in Mississauga, ON, Canada. The E-FTL is the fast machine for the sizes most "
          "fabricators use — railings, frames, furniture, trailers, exhaust: four chuck sizes from Ø0.3″ to 13.8″, servo axes accelerating at "
          "1 G to 394 ft/min and ±0.05 mm repeatability on 7, 9 or 12 m bars. The FTL is built for weight: structural tube, pipe and beams to "
          "Ø25.2″ and 12 m bars of 2,600 kg — 12,000 kg on the long-bed 250 — with ±0.1 mm on the large chucks and a 5-axis bevel head for weld "
          "preparations. Both load from a bundle automatically, support the tube as it is cut, nest parts along the bar from STEP / IGES models "
          "and unload finished pieces. Installed, trained and supported from Mississauga, ON, Canada.",
    points=["E-FTL 120 / 180 / 250 / 350: Ø0.3″ – 13.8″, 1 G, 394 ft/min, ±0.05 mm, bars to 39.4 ft",
            "FTL 250 / 350 / 500 / 640: Ø0.6″ – 25.2″, bars to 39.4 ft and 5,732 lb (12,000 kg on the long-bed 250), 5-axis bevel head",
            "3 – 20 kW sources, bundle loaders, following supports, STEP / IGES tube nesting; made in Turkey, Dener Canada parts in Mississauga, ON, Canada"],
    hero="dn-tube-2", minis=["dn-tube-6", "dn-tube-1"],
    groups=[("tube-eftl", "E-FTL tube lasers", "The fast tube laser for Ø0.3″ to 13.8″: 1 G servo axes, 394 ft/min, four chuck sizes.", BRAND),
            ("tube-ftl", "FTL heavy tube lasers", "For structural tube, pipe and profile to Ø25.2″ and 12 m bars of 2,600 kg.", BRAND)],
    faq=[{"q": "E-FTL or FTL?",
          "a": "The E-FTL is the fast machine for the sizes most fabricators use — railings, frames, furniture, trailers, exhaust — Ø0.3″ to 13.8″, accelerating at 1 G and running 394 ft/min on the small chucks. The FTL is built for weight: structural tube and pipe to Ø25.2″ and 12 m bars of 2,600 kg, with ±0.1 mm repeatability on the large chucks. Both take the same 3 – 20 kW sources and bundle loaders."},
         {"q": "Which chuck size?",
          "a": "The number is the largest round tube in millimetres: E-FTL 120 takes Ø0.3 – 4.7″, 180 to 7.1″, 250 to 9.8″ and 350 to 13.8″; FTL 250, 350, 500 and 640 take Ø0.6″ to 9.8, 13.8, 19.7 and 25.2″. Square and rectangular tube is limited by the diagonal, so a 350 chuck takes about 9.8″ square. Buy the chuck for the largest tube you cut regularly — a smaller chuck is faster and holds thin tube better — and the bar length (7, 9 or 12 m) for the stock you buy."},
         {"q": "Can it cut bevels and weld preparations?",
          "a": "Yes — the 5-axis head on the FTL (optional on the E-FTL) tilts to ±45° so mitred corners, chamfers and weld preparations are cut in the same pass as the holes and copes; the tube arrives at the welding table ready to fit. The seam detector orients welded tube so the seam sits where the drawing puts it."},
         {"q": "How does Dener compare with the Senfeng value line?",
          "a": "Dener's E-FTL and FTL are the premium machines — Turkish-built, 1 G servo chucks, Precitec heads, Dener Canada parts in Mississauga, ON, Canada. Senfeng's tube lasers are the value line: a 6 m two-chuck machine with a 1.5 kW source costs a fraction of a premium tube laser, and the range goes to zero-tailing three-chuck and four-chuck machines for 49 ft stock. The comparison and the capacity table for both lines are on the tube laser cutters overview."},
         {"q": "Floor space and power?",
          "a": "A 7 m E-FTL needs about 20 m (65 ft) of length including the loader and unloader; a 12 m FTL about 30 m. 600 V 3-phase with the supplied transformer or 480 V, a chiller (included), assist gas and a dust collector. We lay the machine out for your building before you order."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about Dener tube lasers",
    related_pages=[{"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"},
                   {"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "tube-end-forming-machines.html", "label": "Tube end formers"},
                   {"href": "band-saw.html", "label": "Band saws"}],
    related_title="More tube machinery from NovoTech",
)

PAGE_SHEAR = dict(
    title="Dener Hydraulic Shears, 1/4″ to 3/4″ × 20 ft | NovoTech",
    meta="BS / BSY hydraulic swing beam shears with NC back gauge, 1/4″ – 5/8″ × 6.8 – 13.5 ft; DAS CNC guillotines with variable angle, 1/4″ – 3/4″ × 10 – 20 ft.",
    h1="Dener hydraulic shears — BS / BSY swing beam to 5/8″ and DAS CNC guillotine to 3/4″ × 20 ft",
    intro="Dener's shears are the premium plate shears of NovoTech's shear section: built in Kayseri, Turkey, with Rexroth or Hoerbiger hydraulics, "
          "ESA or Delem controls and Dener Canada parts in Mississauga, ON, Canada. The BS / BSY swing beam shears are the rugged everyday plate shear: a beam "
          "on two bearings swung through the cut by two cylinders, 8 to 22 strokes a minute, with an NC back gauge, hydraulic hold-downs and "
          "single-point blade-gap adjustment — the light BSY 2006 – 3006 for 1/4″ over 6.8 to 10 ft and the BS 3006 – 4016 to 5/8″ (16 mm) over "
          "10 and 13.5 ft. The DAS CNC guillotines are the production machines: a beam on linear rollers with a variable cutting angle, so thin "
          "sheet is cut fast and flat at 0.5° and 3/4″ plate at 3° with less distortion, back gauge, blade gap and angle set by the ESA 630 CNC "
          "from the thickness and material keyed in — 1/4″ to 3/4″ over 10, 13 and 20 ft. Installed, trained and supported from Mississauga, ON, Canada.",
    points=["BS / BSY swing beam: 11 models, 1/4″ – 5/8″ × 6.8 – 13.5 ft, 8 – 22 strokes/min, NC back gauge, hydraulic hold-downs",
            "DAS CNC guillotine: 13 models, 1/4″ – 3/4″ × 10 – 20 ft, variable cutting angle, ESA 630 CNC, 1 m ball-screw back gauge",
            "Made in Turkey by Dener Makina; Dener Canada parts in Mississauga, ON, Canada; CSA-approved panel, 600 V standard"],
    hero="dn-das-1", minis=["dn-bs-2", "dn-das-3"],
    groups=[("shear-swing", "BS / BSY hydraulic swing beam shears", "Plate from 1/4″ to 5/8″: two cylinders swing the beam through the cut, NC back gauge, 8 – 22 strokes a minute.", BRAND),
            ("shear-cnc", "DAS CNC hydraulic guillotine shears", "The production plate shear to 3/4″ × 20 ft: variable cutting angle, blade gap and back gauge set by the CNC.", BRAND)],
    faq=[{"q": "BS or DAS — swing beam or guillotine?",
          "a": "On the BS the beam pivots on two bearings and the cylinders swing it through the cut — few parts, a low price and a rake angle fixed by the design, which is fine for plate from 1/4″ to 5/8″. The DAS carries the beam straight down on linear rollers with a variable rake angle, so the same machine cuts thin sheet flat and fast at 0.5° and 3/4″ plate at 3° with less twist, and the CNC sets the blade gap and the back gauge from the thickness keyed in. For a plate shop cutting mostly 3/8″ and up, the BS; for a job shop that cuts everything from 16 ga to 3/4″, the DAS."},
         {"q": "Which control?",
          "a": "The BS / BSY come with an NC control for the back gauge and the stroke counter; the DAS with the ESA 630 CNC — back gauge, blade gap, cutting angle and stroke length programmed per material, with a parts memory and a 1 m ball-screw back gauge with retract. Delem controls are available on request."},
         {"q": "What is standard on a Dener shear?",
          "a": "Hydraulic hold-downs (16 – 33 on the DAS), a squaring arm with scale, front support arms, a ball-transfer table, a shadow-line light, a photocell rear guard, a front finger guard, high-carbon high-chrome four-edged blades and the CSA-approved panel with a 600 V transformer. Pneumatic sheet supports with return-to-front, conveyors and longer arms are options."},
         {"q": "How do the Dener shears compare with the NovoTech value line?",
          "a": "Same architecture — welded frame, swing beam or roller-guided guillotine beam, motorised back gauge, hydraulic hold-downs — and the same NovoTech installation, warranty and support. The Dener machines are built in Turkey with the ESA 630 CNC, the 1 m back gauge and Dener Canada parts; the NovoTech value-line shears are built in China with Estun controls at a lower price and in a wider range of sizes, to 1-9/16″ and 26 ft. The capacity table for all four lines is on the shears overview."},
         {"q": "Floor space and power?",
          "a": "A 10 ft shear needs about 16 × 10 ft of floor with the back gauge travel; a 20 ft DAS about 27 × 12 ft. 600 V 3-phase with the supplied transformer or 480 V; the motors run from 15 to 60 HP. We lay the machine out for your building before you order."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about Dener shears",
    related_pages=[{"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"}, {"href": "dener-fiber-lasers.html", "label": "Dener fiber lasers"},
                   {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "corner-notcher.html", "label": "Corner notchers"}],
    related_title="More cutting machinery from NovoTech",
)

PAGE_PANEL = dict(
    title="CNC Panel Benders, 47–165″ Wide, 0.2 s per Bend | NovoTech",
    meta="CNC panel benders sold in Canada: the Dener 79″ machine, Senfeng BDC push-down and suction-cup benders 47 – 126″, NovoTech value-line PB-M and PB-A to 165″.",
    h1="CNC panel benders — four-side bending with no tooling changes, 47 to 165″ bend width",
    intro="A panel bender is the machine that replaces a press brake for boxes, doors, enclosures, panels and HVAC parts: the blank is clamped "
          "by a blank-holder and a bending blade folds the flange up or down, hems it or forms a box corner in 0.2 s, while the manipulator "
          "turns the part to bend the next side — all four sides in one setup, no tooling changes, no skilled operator. NovoTech sells the "
          "Dener panel bender in Canada: blanks to 78.7 × 49.2″ (2,000 × 1,250 mm), flanges to 6.7″, 14 ga mild steel, 16 ga stainless and "
          "1/8″ aluminum, 15 servo axes with 0.001 mm positioning, 100 % electric at about 2.8 kW average draw. Automatic loading and "
          "unloading arms turn it into an unattended cell. Below it is NovoTech's own value line: the PB-M press-arm panel benders in nine sizes "
          "from 63 to 165″ and the PB-A with automatic tool change in four sizes to 126″, built in China to our specification with the same "
          "0.2 s bends and 14 ga capacity, and the Senfeng BDC panel benders under their own brand — push-down machines from 59 to 126″ with 13 "
          "to 16 servo axes and the suction-cup BDC1200 / 1500 for thin door and appliance panels. All installed and supported from Mississauga, ON, Canada.",
    points=["Blanks to 78.7 × 49.2″, flanges to 6.7″ (11.8″ on request), 1 mm minimum radius, boxes from 5.5 × 7.5″ inside",
            "14 ga mild steel, 16 ga stainless, 1/8″ aluminum — 0.2 s per bend, 295 ft/min feeding",
            "Senfeng BDC: push-down 59 – 126″ with 13 – 16 axes, suction-cup 47 – 59″ for 20 ga panels, robot loading cells",
            "Value line: PB-M 63 – 165″ in nine sizes, PB-A with 0.5 s automatic tool change to 126″"],
    hero="dn-panel-1", minis=["dn-panel-2", "dn-panel-5"],
    groups=[("panel", "Dener CNC panel bender", "Fully servo-driven four-side bending cell with a 3D control — one model, 79 × 49″ blanks, made in Turkey.", BRAND),
            ("panel-senfeng", "Senfeng BDC panel benders", "Senfeng's own-brand panel benders from Jinan: push-down machines to 126″ with up to 16 servo axes, and the light suction-cup models to 59″.", SF.BRAND),
            ("panel-value", "NovoTech value-line panel benders", "The PB-M press-arm machines in nine sizes and the PB-A with automatic tool change — 63 to 165″ bend width at a value-line price.", VL.BRAND)],
    faq=[{"q": "Panel bender or press brake?",
          "a": "A press brake bends one line at a time and the operator handles the part between bends; a panel bender clamps the blank once and forms every side — up, down, hems, box corners — automatically, in 0.2 s per bend and with the same accuracy on the first and the thousandth part. For boxes, doors, cabinets, enclosures, appliance and HVAC panels in sheet to 14 ga it is five to ten times faster than a brake and needs no skilled operator or tooling changes. For plate, long single bends, deep boxes or small batches of unusual parts the press brake stays the better machine — most shops run both."},
         {"q": "What sheet can it bend?",
          "a": "Mild steel to 14 ga (2.0 mm), stainless to 16 ga (1.5 mm), aluminum to 1/8″ (3.0 mm); blanks to 78.7 × 49.2″ (2,000 × 1,250 mm) and flange heights to 6.7″ (170 mm), 11.8″ on request; minimum bend radius 1 mm, minimum four-side box 5.5 × 7.5″ inside. Pre-painted and film-covered sheet is bent without marking thanks to the brush table and blade geometry."},
         {"q": "How is it programmed?",
          "a": "From the 3D model or a DXF on the 3D control: the software unfolds the part, sets the bending sequence and simulates it, with automatic compensation for springback. A new part is programmed in minutes and runs without test bends; programs can be prepared offline on a PC."},
         {"q": "Can it run unattended?",
          "a": "With the optional loading and unloading arms the machine takes blanks from a stack and places finished parts on a pallet, so it runs lights-out behind a laser. The 15-axis servo drive and the 2.8 kW average consumption make it the cheapest machine on the floor to keep running."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about panel benders",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "corner-notcher.html", "label": "Corner notchers"}],
    related_title="More sheet-metal machinery from NovoTech",
)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "dener")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/dener/{key}{ext}", "alt": p["alt"], "section": "dener", "trim": p.get("trim", False), "quality": 82, "cutout": False}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "dener_keys.txt"), "w").write(",".join(keys))
    return keys


def copy_pdfs():
    for dst, src in COPY_PDFS.items():
        d = os.path.join(ROOT, "src", dst)
        if not os.path.exists(d):
            shutil.copy(SRC_PDF + src, d)


def build():
    copy_pdfs()
    pdf_pb = pdf(PDF_PB_FILE, "Download the hydraulic & hybrid press brake brochure")
    pdf_servo = pdf(PDF_SERVO_FILE, "Download the servo-electric press brake brochure")
    pdf_laser = pdf(PDF_LASER_FILE, "Download the fiber laser brochure")
    pdf_tube = pdf(PDF_TUBE_FILE, "Download the tube laser brochure")
    pdf_panel = pdf(PDF_PANEL_FILE, "Download the panel bender brochure")
    fams = []
    for f in D.PB_FAMILIES:
        fams.append(dict(f, pdf=pdf_servo if f["group"] == "pb-servo" else pdf_pb))
    fams += [dict(f, pdf=pdf_laser) for f in D.LASER_FAMILIES]
    fams += [dict(f, pdf=pdf_tube) for f in D.TUBE_FAMILIES]
    fams += [dict(f, pdf=pdf_panel) for f in D.PANEL_FAMILIES]
    pdf_vl_panel = pdf(PDF_VL_PANEL_FILE, "Download the value-line panel bender brochure")
    fams += [dict(f, pdf=pdf_vl_panel) for f in VL.PANEL_FAMILIES]
    pdf_sf_laser = SFP.pdf(SFP.PDF_LASER, "Download the Senfeng fiber laser brochure")
    pdf_sf_tube = SFP.pdf(SFP.PDF_TUBE, "Download the Senfeng tube laser brochure")
    pdf_sf_panel = SFP.pdf(SFP.PDF_PANEL, "Download the Senfeng panel bender brochure")
    fams += [dict(f, pdf=pdf_sf_laser) for f in SF.LASER_FAMILIES]
    fams += [dict(f, pdf=pdf_sf_tube) for f in SF.TUBE_FAMILIES]
    fams += [dict(f, pdf=pdf_sf_panel) for f in SF.PANEL_FAMILIES]
    pdf_vl_sheet = VLP.pdf(VLP.PDF_SHEET, "Download the NovoTech fiber laser brochure")
    pdf_vl_tube = VLP.pdf(VLP.PDF_TUBE, "Download the NovoTech tube laser brochure")
    fams += [dict(f, pdf=pdf_vl_sheet) for f in VLL.SHEET_FAMILIES]
    fams += [dict(f, pdf=pdf_vl_tube) for f in VLL.TUBE_FAMILIES]
    write_families(SET, fams)
    common = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **INTRO_VIDEO}
    # the press-brake families are shown on the hydraulic / electric press brake pages (tools/press_brake_types.py), not on a Dener page;
    # the laser families on the pages per kind of laser (tools/laser_types.py — enclosed, open-type, tube laser cutters …), not on a Dener page
    pdf_shear = pdf(PDF_SHEAR_FILE, "Download the Dener hydraulic shears brochure")
    # the shear families are shown on the hydraulic / mechanical / sheet metal shear pages (tools/shear_types.py), not on a supplier page
    write_category(D.P_PANEL, PAGE_PANEL, fams, SET, "Panel benders", extra={**common, "nav_label": "Panel benders", "catalogue_pdf": None, "catalogue_pdfs": [pdf_panel, pdf_sf_panel, pdf_vl_panel],
                                                                                "hero_brand_line": "The Dener panel bender is made in Turkey by Dener Makina; the BDC machines by Senfeng Laser in Jinan, China; the PB-M and PB-A carry the NovoTech name — built in China to North American standards. All sold, installed and supported in Canada by NovoTech."})
    keys = register_images()
    vl_keys = {k for f in VL.PANEL_FAMILIES + SF.ALL + VLL.ALL for k in f["images"]}
    used = {k for f in fams + D.SHEAR_FAMILIES for k in f["images"]} - vl_keys
    for p in (PAGE_PB, PAGE_LASER, PAGE_TUBE, PAGE_PANEL, PAGE_SHEAR):
        used |= {p["hero"]} | set(p["minis"])
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    vids = sorted({v["id"] for f in fams + D.SHEAR_FAMILIES for v in f["videos"] if f["id"] not in {x["id"] for x in VL.PANEL_FAMILIES + SF.ALL + VLL.ALL}} | {INTRO_VIDEO["intro_video"]["id"]})
    open(os.path.join(ROOT, "tools", "dener_vids.txt"), "w").write(" ".join(vids))
    print(f"dener: {len(fams)} families on 4 Dener pages (+ Senfeng families for the Senfeng pages) + {len(D.SHEAR_FAMILIES)} shear families · images: {len(keys)} · videos: {len(vids)}")


if __name__ == "__main__":
    build()
