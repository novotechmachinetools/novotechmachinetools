#!/usr/bin/env python3
"""The two press-brake pages, one per kind of drive — hydraulic-press-brake.html and electric-press-brake.html — under the
press-brake hub.  Each page holds every family of that kind NovoTech sells, premium and value lines as sections, with the
spec tables, photos, videos and brochures of the families (family set content/families/press-brakes.json, merged by
tools/press_brake_hub.py — run that first):

    python3 tools/press_brake_hub.py && python3 tools/press_brake_types.py

The pages replace the supplier pages dener-cnc-press-brakes, novotech-cnc-press-brakes and compact-hydraulic-press-brakes
(301s in src/root/.htaccess): buyers search for the kind of machine, not the supplier, and one URL per kind is what the
search engines rank (reports/ساختار صفحات محصول و سئو.md)."""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category
import press_brake_nav as PBN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "press-brakes"

BRAND_LINE = ("The premium line is built by Dener Makina in Kayseri, Turkey (press brakes since 1974); NovoTech's value line is built in China to our "
              "specification with Delem, Hawe and Estun components; the compact brakes by ISITAN in Bursa, Turkey. All sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Premium and value lines, one supplier", "text": "Every press brake comes with a CSA-approved panel, European-style tooling, a 1-year warranty and parts and technicians in Mississauga, ON, Canada — whichever line you choose."}

TONNAGE_FAQ = {"q": "How much tonnage and length do I need?",
               "a": "Air bending mild steel takes about 575 × t² ÷ V US tons per foot, with the thickness t and the V opening in inches: in the standard V = 8 × thickness die that is about 4 tons per foot for 16 ga, 9 for 1/8″, 13.5 for 3/16″, 18 for 1/4″ and 36 for 1/2″ (29 in a 10 × t die); stainless needs about 50 % more, aluminum about half. Add a foot of length to the longest part you bend and about 20 % headroom. A 10 ft × 1/4″ shop is a 175 – 220 ton machine; 10 ft × 3/8″ a 250 – 320 ton machine; 13 ft × 1/2″, bent in a 5 – 6″ V, a 400 – 450 ton machine. Tell us your thickest and longest bend and we size the brake and the tooling."}
TOOLING_FAQ = {"q": "What tooling fits, and do you stock it?",
               "a": "European-style (Promecam / Amada) segmented punches and dies with quick-release clamping are standard on every line, and a sectioned punch set with a 2-V die ships with each machine. NovoTech stocks Eurostamp press brake tooling in Canada — punches, dies, radius, hemming and joggle tools, gooseneck and special profiles — and sizes it to your machine; Wila hydraulic clamping and American-style adapters are options."}
SAFETY_FAQ = {"q": "What about safety and the Ontario pre-start review?",
              "a": "Side guards, an enclosed rear guard, interlocked doors and an anti-panic foot pedal with emergency stop are standard; DSP or Fiessler laser finger protection and light curtains are options we recommend for every CNC machine. In Ontario a new press brake needs a pre-start health and safety review (PSR) under Regulation 851 before it runs; NovoTech prepares the documentation for it."}
SERVICE_FAQ = {"q": "Do you deliver, install and service in Canada?",
               "a": "Yes — every press brake is shipped to Mississauga, ON, Canada, unloaded, levelled, commissioned and the operators trained by NovoTech; Dener Canada and NovoTech stock the parts here. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request), a 1-year warranty and remote diagnostics through the control."}

HYDRAULIC = dict(
    title="Hydraulic Press Brakes for Sale in Canada — CNC, Hybrid & NC, 33–1,323 Tons | NovoTech",
    meta="Hydraulic press brakes sold, installed and supported in Canada: CNC brakes 55 – 1,323 US tons, XH hybrid with servo pump, NC torsion-bar brakes from 33 tons and compact 33 – 66 ton machines — premium and value lines, CSA panels, Delem and ESA controls.",
    h1="Hydraulic press brakes — CNC, hybrid, NC and compact, 33 to 1,323 US tons",
    intro="A hydraulic press brake bends sheet and plate between a punch and a V-die with two hydraulic cylinders, giving full force over the whole "
          "stroke at the lowest price per ton — the machine for plate, long parts and production. NovoTech sells four kinds in Canada, all on this "
          "page: CNC hydraulic press brakes with linear scales, servo valves, crowning and a graphic control — the premium Dener XL in 18 models "
          "from 66 to 661 US tons and 5 to 20 ft, and NovoTech's own value line from 55 to 331 tons, heavy-duty and tandem to 1,323 tons and 26 ft; "
          "the XH hybrid, an XL with a servo-driven pump that cuts energy by 42 – 58 %; NC torsion-bar press brakes from 33 to 441 tons for repeat "
          "parts in one material; and the compact ISITAN brakes, 33 to 66 tons over 4 to 7 ft, for HVAC, enclosures and brackets. Every machine "
          "comes with a CSA-approved panel, European-style tooling and a 1-year warranty, and is installed, trained and supported from Mississauga, "
          "ON, Canada. For a brake with no hydraulic oil see the electric press brakes; for bar, pipe and busbar the horizontal press brakes.",
    points=["CNC hydraulic: premium line 66 – 661 US tons × 5 – 20 ft (ESA / Delem, 6-axis gauges); value line 55 – 331 tons, heavy-duty to 1,323 tons × 26 ft",
            "XH hybrid: servo pump on the premium frame — 42 – 58 % less energy, 17 – 75 % faster approach and return, quieter",
            "NC torsion-bar 33 – 441 tons for repeat parts; compact 33 – 66 ton × 4 – 7 ft brakes with Cybelec control for the sheet-metal shop"],
    hero="dn-xl-1", minis=["vl-wad-1", "is-eb-1240-cnc"],
    groups=[("pb-premium", "CNC hydraulic press brakes · premium line", "The Dener XL: a monoblock frame, Hawe hydraulics and an ESA 2D control, 5 to 20 ft and 66 to 661 US tons — the standard for plate and production."),
            ("pb-value", "CNC hydraulic press brakes · value line", "NovoTech's own brakes: the same architecture — servo valves, linear scales, Delem control — from 55 to 331 US tons, heavy-duty and tandem machines to 1,323 tons."),
            ("pb-hybrid", "Hybrid press brakes · premium line", "The XL with a servo-driven pump — the same frame and cylinders, less energy, more speed, less noise."),
            ("pb-nc", "NC hydraulic press brakes — torsion bar · value line", "The simple machine: torsion-bar synchronised ram, mechanical stops and an Estun NC control for the back gauge and depth, 33 to 441 US tons."),
            ("pb-compact", "Compact hydraulic press brakes, 33 – 66 tons", "The ISITAN Edgebender: 4.2 to 6.9 ft, 2-axis NC or 3-axis CNC with Cybelec control, made in Turkey — the press brake for a sheet-metal shop.")],
    faq=[{"q": "CNC, hybrid, NC or compact — which hydraulic press brake do I need?",
          "a": "A CNC brake measures the ram on linear scales and corrects it through servo valves, calculates the bend from the drawing, crowns the bed and changes material in the program — the machine for mixed work, tight angles and multi-bend parts, and the one most Canadian shops buy. The hybrid is a CNC brake with a servo pump: it costs a little more and pays it back in power, speed and noise when the brake runs all day. An NC brake positions the back gauge and the ram depth from a stored program with the cylinders kept in step by a torsion bar — rigid, cheap to maintain, right for the same parts in one material every day. The compact 33 – 66 ton brakes are for 4 – 7 ft work in sheet up to 8 ga where a 100-ton machine is more than you need."},
         {"q": "Premium line or value line?",
          "a": "The premium Dener XL and XH are built in Turkey on the heaviest frame, with ESA or Delem controls, back gauges to 6 axes, sheet followers, robot cells and Dener Canada parts in Mississauga, ON, Canada — the machines for plate, 3/8″ and 1/2″ over 10 to 20 ft, two shifts, a long options list. NovoTech's value line is the same architecture — monoblock frame, Hawe servo valves, linear scales, Delem control — built in China to our specification at about two-thirds of the price: the right buy for a job shop that needs a 100 – 300 ton CNC brake or an NC brake for repeat parts, and the only line that goes to 1,323 tons and 26 ft. Both are installed and supported by the same NovoTech technicians."},
         TONNAGE_FAQ,
         {"q": "What is a hybrid press brake?",
          "a": "On a conventional hydraulic brake the motor and pump run at full speed all day, whether the ram moves or not. The XH hybrid replaces the AC motor and fixed pump with a servo motor driving an inverter pump: the pump turns only while the ram moves, at the speed the ram needs. Dener measures 42 – 58 % energy saving and 17 – 75 % faster approach and return against the XL of the same tonnage, with less heat in the oil and a quieter shop. Everything else — frame, cylinders, valves, tooling, controls — is the XL."},
         {"q": "Which control comes with the machine?",
          "a": "The premium XL comes with the 15″ ESA S640 2D graphic control (Delem DA-66S / 69S and the ESA S875 W 3D control are options): draw the profile, the control calculates the bend sequence, tonnage, back-gauge positions and crowning. The value-line CNC brakes come with Delem DA-53T or DA-58T and the heavy-duty machines with DA-66T; the NC brakes with an Estun E21; the compact CNC with a Cybelec Cybtouch 12. All program in inches or millimetres."},
         {"q": "What back gauge and axes are available?",
          "a": "Every CNC machine has the Y1 and Y2 ram axes and an X back-gauge axis on a ball screw and linear guides. Options go up to the 6-axis gauge with X1, X2, R1, R2, Z1 and Z2 — two independently positioned fingers for angled flanges — plus a CNC crowning axis; the NC brakes have X and the depth stop. The back gauge is set by the control for every bend of the program."},
         TOOLING_FAQ, SAFETY_FAQ, SERVICE_FAQ, VOLT_FAQ_GENERIC],
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
          "panel, European-style tooling and a 1-year warranty, installed, trained and supported from Mississauga, ON, Canada. For 3/8″ plate, "
          "tonnage above 220 tons or the lowest price per ton, see the hydraulic press brakes.",
    points=["Premium line: DDM servo-electric 44 – 220 US tons × 5 – 13 ft, ESA S875 W 3D control; DDS ball-screw 22 and 44 tons",
            "Value line: electric ball-screw brakes 11 – 176 US tons × 1.6 – 10.5 ft with Delem control; 3 – 13 ton bench brakes",
            "±0.01 mm, power only while the ram moves, no hydraulic oil or filters — about twice the speed of a hydraulic brake on sheet"],
    hero="dn-ddm-2", minis=["vl-wadg-1", "dn-dds-1"],
    groups=[("pb-servo", "Servo-electric and ball-screw press brakes · premium line", "No hydraulic oil: the Dener DDM servo-electric brake for production to 220 tons and the DDS ball-screw brake for small parts."),
            ("pb-value-electric", "Electric press brakes · value line", "NovoTech's own electric brakes: ball-screw servo drive from 3 to 176 US tons — the clean, quiet, accurate brake for sheet work at a value-line price.")],
    faq=[{"q": "Electric or hydraulic — which press brake should I buy?",
          "a": "Electric when the work is sheet — 20 ga to 1/4″, brackets, enclosures, panels, stainless and aluminum — and when accuracy, speed, energy and a clean floor matter: the servo drive repeats to ±0.01 mm, bends at about twice the speed of a hydraulic brake and draws power only while the ram moves. Hydraulic when the work is plate, 3/8″ and up, long parts over 13 ft, or tonnage above 220 US tons, and when the lowest price per ton decides. Many shops run one of each; the hydraulic press brakes have their own page."},
         {"q": "Servo-electric or ball-screw — what is the difference?",
          "a": "Both are electric. The DDM servo-electric brake drives the ram through servo motors and a belt-and-pulley system across the whole bending length, which is how it reaches 220 US tons and 13 ft with the force distributed evenly along the beam. The DDS and the value-line brakes drive the ram with two ball screws, one per side, each on its own servo motor — simpler, very accurate, and the right construction up to about 176 tons and 10 ft."},
         {"q": "Premium line or value line?",
          "a": "The premium DDM is built in Turkey by Dener with the 21″ ESA S875 W 3D control, 6-axis back gauges, laser angle measurement and robot cells as options, and Dener Canada parts in Mississauga, ON, Canada — the production electric brake. NovoTech's value-line electric brakes are built in China to our specification with Delem control and the same Estun servo components, at about two-thirds of the price — the electric brake for a job shop or a second machine for small parts. Both are installed and supported by the same NovoTech technicians."},
         TONNAGE_FAQ,
         {"q": "What does an electric press brake cost to run?",
          "a": "There is no hydraulic oil to buy, filter, cool or dispose of, no pump motor idling between bends, and the servo motors regenerate on the return stroke: Dener measures about 70 % less energy than a hydraulic brake of the same tonnage on sheet work, and the maintenance schedule is lubrication of the ball screws and guides. The machines are also quieter, which matters in a shop that runs the brake all day."},
         TOOLING_FAQ, SAFETY_FAQ, SERVICE_FAQ, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about electric press brakes",
    related_pages=[{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "shear-cutting.html", "label": "Metal shears"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring before bending"}],
    related_title="More bending and cutting machinery from NovoTech",
)

VIDEOS = {
    "hydraulic-press-brake": {"intro_video": {"id": "pRxr7CB2pDQ", "title": "XL 13 ft × 220 ton CNC hydraulic press brake with laser angle measurement and sheet follower", "thumb": "video-pRxr7CB2pDQ", "duration": "PT1M30S"},
                              "intro_video_heading": "The CNC hydraulic press brake at work",
                              "intro_video_text": "A 13 ft × 220 ton XL bending plate with laser angle measurement and a sheet follower — the premium hydraulic brake in production."},
    "electric-press-brake": {"intro_video": {"id": "ZujRJUhckG4", "title": "DDM 10030 — 10 ft × 100 ton servo-electric CNC press brake", "thumb": "video-ZujRJUhckG4", "duration": "PT0M51S"},
                             "intro_video_heading": "The servo-electric press brake at work",
                             "intro_video_text": "A 10 ft × 100 ton DDM bending sheet: no hydraulic oil, servo drive, ±0.01 mm repeatability."},
}


def build():
    fs = json.load(open(os.path.join(ROOT, "content", "families", f"{SET}.json"), encoding="utf-8"))
    fams = {fid: dict(fs["families"][fid], id=fid) for fid in fs["order"]}
    manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
    for slug, page in (("hydraulic-press-brake", HYDRAULIC), ("electric-press-brake", ELECTRIC)):
        members = [dict(fams[fid], group=g) for _, fid, g in PBN.PAGES[slug]]
        pdfs, seen = [], set()
        for f in members:
            pd = f.get("pdf")
            if pd and pd["file"] not in seen:
                seen.add(pd["file"]); pdfs.append(pd)
        video = VIDEOS[slug] if VIDEOS[slug]["intro_video"]["thumb"] in manifest else {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}
        write_category(slug, page, members, SET, PBN.SECTION, hub=PBN.hub(), siblings=PBN.siblings(),
                       extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **video,
                              "nav_label": next(nav for s, _, _, _, nav, _ in PBN.SUBPAGES if s == slug),
                              "catalogue_pdf": None, "catalogue_pdfs": pdfs})
        print(f"{slug}: {len(members)} families, {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
