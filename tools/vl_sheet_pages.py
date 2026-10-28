#!/usr/bin/env python3
"""NovoTech value-line sheet-metal pages: novotech-cnc-press-brakes (hydraulic CNC + NC + electric, one page under the
press-brake hub), hydraulic-shearing-machine (swing beam + guillotine), v-grooving-machine — family set content/families/value-sheet.json, photos from
tools/vl_sheet_photos.py (section 'value-sheet').  The value-line panel benders are appended to panel-bender.html by
tools/dener_pages.py and the ironworker to ironworker-machines.html by tools/sahinler_pages.py (both import
vl_sheet_data).

    python3 tools/vl_sheet_photos.py                    # logo-free sources → tools/src-images/value-sheet
    python3 tools/vl_sheet_pages.py                     # families + pages + image_map entries (tools/vl_sheet_keys.txt)
    python3 tools/yt_thumbs.py $(cat tools/vl_sheet_vids.txt)
    python3 tools/make_images.py --only $(cat tools/vl_sheet_keys.txt)
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import vl_sheet_data as D
import vl_sheet_photos as PH
import press_brake_nav as PBN
import shear_nav as SN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "value-sheet"
BRAND = D.BRAND
PDF_HPB = "files/NovoTech-Hydraulic-Press-Brakes-2026.pdf"
PDF_EPB = "files/NovoTech-Electric-Press-Brakes-2026.pdf"
PDF_SHEAR = "files/NovoTech-Hydraulic-Shearing-Machines-2026.pdf"
PDF_VG = "files/NovoTech-V-Grooving-Machines-2026.pdf"
PDF_PANEL = "files/NovoTech-Panel-Benders-Value-Line-2026.pdf"
PDF_IRON = "files/NovoTech-Ironworkers-Value-Line-2026.pdf"

BRAND_LINE = ("NovoTech's own value line: manufactured in China to high North American quality standards, with Delem, Estun, Hawe, Rexroth and "
              "Schneider components, the same CSA-approved panel, 1-year warranty and Mississauga, ON, Canada parts and support as every machine we sell.")
ORIGIN = {"title": "Built in China to North American standards", "text": "NovoTech's own brand — European controls and hydraulics, inspected before shipping, "
          "same CSA panel, warranty and Mississauga, ON, Canada support as every machine we sell."}
WADE_VIDEO = {"intro_video": {"id": "-rFs4TdGvds", "title": "10 ft × 110 ton CNC press brake with Delem DA-53T control", "thumb": "video--rFs4TdGvds", "duration": "PT2M23S"},
              "intro_video_heading": "In our showroom — the 10 ft × 110 ton CNC press brake",
              "intro_video_text": "A walk around the value-line CNC press brake in Mississauga, ON, Canada: Delem DA-53T control, servo back gauge, quick clamps and the hydraulic system."}
SHEAR_VIDEO = {"intro_video": {"id": "WKmfgruGOWI", "title": "10 ft × 1/4″ swing beam shear with Estun E200P control", "thumb": "video-WKmfgruGOWI", "duration": "PT45S"},
               "intro_video_heading": "In our showroom — the 10 ft × 1/4″ swing beam shear",
               "intro_video_text": "The value-line swing beam shear cutting 1/4″ plate in Mississauga, ON, Canada, with the Estun control and the motorised back gauge."}
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}
# WADE_VIDEO / SHEAR_VIDEO are not used: both clips were filmed at the supplier's factory with its badges in view (Oct 2026).


def pdf(file, label):
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": label, "size": size}


PAGE_PB = dict(
    title="NovoTech CNC Press Brakes, Hydraulic & Electric · Value Line",
    meta="NovoTech's own CNC press brakes sold in Canada: hydraulic CNC 55 – 331 US tons with Delem control, heavy-duty and tandem to 1,323 tons, NC brakes from 33 tons, servo-electric 3 – 176 tons.",
    h1="NovoTech CNC press brakes — hydraulic and electric · value line, 3 to 1,323 US tons",
    intro="These are NovoTech's own press brakes — the value line: built in China to our specification with Delem controls, Hawe and Rexroth "
          "hydraulics, Estun servos and Schneider electrics, inspected before they ship and sold under NovoTech's name at a price a small shop "
          "can justify. Three families on one page: the hydraulic CNC press brakes from 55 to 331 US tons over 4 to 20 ft, with heavy-duty and "
          "tandem machines to 1,323 tons and 26 ft; the NC torsion-bar brakes from 33 to 441 tons for shops that bend the same parts every day; and "
          "the electric servo press brakes — no hydraulic oil, ball-screw drive, ±0.01 mm — from 11 to 176 US tons, plus 3 to 12 ton bench "
          "machines. For the Turkish-built premium machines see the Dener CNC press brakes; for the compact 4 – 7 ft shop brakes see the ISITAN "
          "page. Every machine is installed and supported from Mississauga, ON, Canada, with a CSA-approved panel and a 1-year warranty.",
    points=["Hydraulic CNC: Delem DA-53T, Hawe servo valves, servo back gauge, 4+1 axes — 55 – 331 US tons × 4 – 20 ft; heavy-duty to 1,323 tons",
            "Electric: servo motors, belts and ball screws, ±0.01 mm, 70 % less energy — 11 – 176 US tons × 20″ – 10.5 ft, 3 – 12 t bench",
            "NC torsion-bar brakes with Estun E21 control — 33 – 441 tons × 5 – 20 ft; robot bending cells on hydraulic and electric"],
    hero="vl-wad-1", minis=["vl-wadg-1", "vl-nc-1"],
    groups=[("pb-cnc", "Hydraulic CNC press brakes", "Electro-hydraulic servo synchronisation, Delem control and a servo back gauge — the full CNC package from 55 to 1,323 US tons.", BRAND),
            ("pb-electric", "Electric servo press brakes", "Ball-screw servo drive from 3 to 176 US tons — the clean, quiet, accurate brake for sheet work.", BRAND),
            ("pb-nc", "NC hydraulic press brakes — torsion bar", "The simple machine: torsion-bar synchronised ram, mechanical stops and an Estun NC control for the back gauge and depth.", BRAND)],
    faq=[{"q": "Hydraulic, electric or NC — which press brake do I need?",
          "a": "Hydraulic CNC is the all-rounder: full tonnage over the whole stroke, the lowest price per ton above about 150 tons and the right machine for 3/8″ and 1/2″ plate. Electric wins on accuracy, speed on thin material, energy and cleanliness — ±0.01 mm from the first part, bending speeds to 30 mm/s, about 70 % less power, no oil — and is usually the better buy for a shop bending 16 ga to 1/4″ sheet all day: enclosures, brackets, HVAC, electrical. The NC torsion-bar brake is the budget machine for a shop that bends the same parts from the same stock every day: rigid, cheap to maintain, a third less than the CNC. Tell us your material mix and we quote the right one."},
         {"q": "CNC or NC press brake — what is the difference?",
          "a": "An NC press brake positions the back gauge and the ram depth from a stored program, but the two cylinders are kept in step by a torsion bar and the depth is set by mechanical stops: accurate enough for brackets, boxes, channels and roofing in one material. A CNC press brake measures the ram on linear scales and corrects it through servo valves, calculates the bend from the drawing, crowns the bed automatically and changes material and thickness in the program — the machine for mixed work, tight angles and multi-bend parts."},
         {"q": "How does the value line differ from the Dener press brakes?",
          "a": "The architecture is the same — monoblock frame, Hawe servo valves, linear scales, servo back gauge, Delem control, European tooling — and both are installed and supported by the same NovoTech technicians in Mississauga, ON, Canada. The Dener XL is built in Turkey on a heavier frame with a longer options list (ESA controls, 6-axis ATF gauge, hybrid drive, 20 ft and 661 tons in the catalogue) and carries the Dener name and Dener Canada parts; the value-line machine is built in China to our specification, sold under NovoTech's name and inspected before it ships, at about two-thirds of the price. Both come with the CSA panel and the same warranty."},
         {"q": "How much tonnage do I need?",
          "a": "Air bending mild steel takes about 575 × t² ÷ V US tons per foot, with the thickness t and the V opening in inches: in the standard V = 8 × thickness die that is about 4 tons per foot for 16 ga, 9 for 1/8″, 13.5 for 3/16″, 18 for 1/4″ and 36 for 1/2″ (29 in a 10 × t die); stainless needs about 50 % more, aluminum about half. With about 20 % headroom, a 10 ft × 1/4″ job is therefore a 175 – 220 ton machine, 10 ft × 3/8″ a 250 – 320 ton machine and 13 ft × 1/2″, bent in a 5 – 6″ V, a 400 – 450 ton machine. Tell us the thickest and longest bend you make and we size the brake and the tooling."},
         {"q": "How does the electric ball-screw drive work?",
          "a": "Two servo motors (three on the 160 t) on top of the frame drive lead ball screws through timing belts; the screws move the ram, and magnetic scales on each side feed the position back to the control so the two sides stay in step to 0.01 mm. Because the screws hold position without power, the ram can dwell at the bottom for coining or hemming with no energy drawn. The screws are preloaded and lubricated automatically; there is nothing to bleed or change. The 3 – 12 ton bench machines are the same drive in a cabinet that plugs into a wall outlet."},
         {"q": "Which control comes with the machine?",
          "a": "The Delem DA-53T: a 10″ touchscreen numerical control for Y1, Y2, X and R (plus the V crowning axis on the hydraulic brakes from 110 t) that stores programs with the angle, depth and gauge positions and runs in inches or millimetres. The DA-58T adds a 15″ screen with 2D graphic programming and automatic bend sequencing, the DA-66T a 17″ screen with 3D part view, and the DA-69T full 3D programming and simulation; ESA S875 and Cybelec controls are available too. All of them import DXF files and take offline programs from Delem's Profile software. The NC brakes carry the Estun E21."},
         {"q": "What tooling fits?",
          "a": "European-style (Promecam / Amada) segmented punches and dies with quick clamps are standard and a sectioned punch set with a 2-V die is in the crate; Wila hydraulic clamping, double-sided quick clamps and Rolleri pneumatic clamps are options, and American-style tooling can be fitted with an adapter. NovoTech stocks Eurostamp press brake tooling in Canada — punches, dies, radius, hemming and joggle tools — and sizes it to your machine."},
         {"q": "What safety equipment is included?",
          "a": "Side guards, an enclosed rear guard, interlocked doors and an anti-panic foot pedal with emergency stop are standard. DSP laser finger protection (EN 12622 CAT 4 / SIL 3), which watches the zone under the punch and stops the ram if a finger enters it, and light curtains are options we recommend for every CNC machine; in Ontario the machine also needs the pre-start health and safety review, which we prepare the documentation for."},
         {"q": "Can the press brake be automated?",
          "a": "Yes — the 40 and 50 ton electric machines and the 110 – 220 ton hydraulic brakes are sold as complete robot bending cells with an Estun robot, gripper, loading table and unloading stack, and every CNC model has the robot interface; CNC sheet followers support large blanks through the bend on the hydraulic machines."},
         {"q": "Do you deliver, install and service in Canada?",
          "a": "Yes. Machines are inspected before they leave the factory, shipped to Mississauga, ON, Canada, unloaded, levelled, commissioned and the operators trained by NovoTech; parts for the Delem, Hawe, Rexroth, Estun and Schneider components are standard items and the machine-specific parts are stocked here. Every machine comes with a CSA-approved panel, 600 V standard (208 / 240 / 480 V on request), a 1-year warranty and remote diagnostics through the control."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about the NovoTech press brakes",
    related_pages=[{"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}, {"href": "hydraulic-shearing-machine.html", "label": "Hydraulic shears"},
                   {"href": "panel-bender.html", "label": "CNC panel benders"}, {"href": "v-grooving-machine.html", "label": "V-grooving machines"}],
    related_title="More bending and cutting machinery from NovoTech",
)

PAGE_SHEAR = dict(
    title="NovoTech Hydraulic Shears, 5/32″ to 1-9/16″ · Value Line",
    meta="QC12K swing beam shears 5/32″ – 3/4″ × 8 – 20 ft and Q11K variable-rake guillotine shears 1/4″ – 1-9/16″ × 8 – 26 ft with Estun NC control, 66 models.",
    h1="NovoTech hydraulic shears — QC12K swing beam to 3/4″, Q11K guillotine to 1-9/16″ plate, the value line",
    intro="A hydraulic shear cuts sheet and plate to size in one stroke between a fixed lower blade and a moving upper blade; the back gauge sets the "
          "width, hydraulic hold-downs keep the sheet flat and the control counts the strokes. NovoTech's value-line hydraulic shears are our own "
          "brand, built in China with Estun controls, Rexroth hydraulics and Siemens motors: the swing beam shears from 5/32″ to 3/4″ over 8 to "
          "20 ft — the rugged everyday plate shear — and the guillotine shears with a variable rake angle from 1/4″ to 1-9/16″ over 8 to 26 ft for "
          "production and thick plate. The Dener premium plate shears, the premium-line mechanical shears and the value-line sheet metal shears "
          "have their own pages, and the shears overview puts every line in one table. Installed and supported from Mississauga, ON, Canada, with a "
          "CSA-approved panel.",
    points=["Swing beam: 32 models, 5/32″ – 3/4″ × 8 – 20 ft, Estun E21S control, motorised back gauge",
            "Guillotine: 34 models, 1/4″ – 1-9/16″ × 8 – 26 ft, variable rake angle and blade gap from the control",
            "Hydraulic hold-downs, ball-transfer tables, shadow line, light-barrier guards — all standard"],
    hero="vl-qc12k-1", minis=["vl-q11k-1", "vl-q11k-feed"],
    groups=[("sh-swing", "Hydraulic swing beam shears", "The everyday plate shear: a swing beam on two cylinders, NC back gauge and hydraulic hold-downs, 5/32″ to 3/4″.", BRAND),
            ("sh-guillotine", "Hydraulic guillotine shears", "The production shear with a variable rake angle — flat cuts in thin sheet, less twist in thick plate, 1/4″ to 1-9/16″.", BRAND)],
    faq=[{"q": "Swing beam or guillotine shear?",
          "a": "A swing beam shear pivots the upper blade on two bearings and drives it down with two cylinders: a simple, rigid machine with few moving parts, a fixed cutting angle and a slightly curved blade path — the right shear for most fabrication shops cutting 5/32″ to 1/2″ sheet. A guillotine shear carries the blade beam on linear rollers so it comes straight down, and the rake angle is set by the control: thin sheet is cut at 0.5° fast and flat, thick plate at 3° or 4° with less twist and less force — the production machine, and the only choice above 3/4″."},
         {"q": "What thickness and length do I need?",
          "a": "Capacities are rated for mild steel of 65,000 psi; stainless cuts about 60 % of the rated thickness and aluminum about 150 %. Choose the length from the sheet you buy: 8 ft (2,500 mm) for 4 × 8 sheet cut across, 10 ft (3,200 mm) for 5 × 10 sheet, 13 ft and up for plate. The 1/4″ × 10 ft swing beam shear (QC12K-6×3200) is the Canadian standard; a shop cutting 3/8″ and 1/2″ plate daily should look at the 10 or 13 mm guillotine."},
         {"q": "What does the Estun E21S control do?",
          "a": "It positions the motorised back gauge (0.8 – 25.6″, 31.5″ on the long machines) with a servo, sets the cutting angle and displays the blade clearance from an encoder, counts strokes and stores 40 programs of 25 steps, in inches or millimetres; a retract function pulls the gauge back after the cut so the strip falls free. The E200PS and the Delem DAC-360T add programmable blade-gap adjustment."},
         {"q": "How is the sheet supported?",
          "a": "Ball-transfer front tables, a squaring arm with scale and front support arms are standard; the back gauge carries support fingers and the cut strip drops onto the rear slide. A pneumatic sheet support that holds the piece during the cut and returns it to the front, a conveyor for strips and longer front arms are options for thin, large or finished sheet."},
         {"q": "How does the value line compare with the Dener shears?",
          "a": "Same architecture — welded frame, swing beam or roller-guided guillotine beam, motorised ball-screw back gauge, hydraulic hold-downs — and the same NovoTech installation, warranty and support. The Dener machines are built in Turkey with the ESA 630 CNC, 1 m back gauge and Dener Canada parts; the value-line shears are built in China to our specification with Estun controls and Rexroth valves, sold under NovoTech's name at a lower price and in a wider range of sizes, to 1-9/16″ and 26 ft. The capacity table for all four lines is on the shears overview."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about hydraulic shears",
    related_pages=[{"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"},
                   {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                   {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}],
    related_title="More cutting machinery from NovoTech",
)

PAGE_VG = dict(
    title="V-Grooving Machines, CNC Horizontal & Vertical | NovoTech",
    meta="CNC V-grooving machines sold in Canada: horizontal 10.5–20 ft tables for sheet to 5/32″, vertical to 13 ft for plate to 1/4″ — sharp zero-radius bends.",
    h1="CNC V-grooving machines — horizontal to 20 ft, vertical to 1/4″ plate",
    intro="A V-grooving machine (sheet grooving or slotting machine) planes a V-shaped channel along the bend line of a sheet, leaving a thin web; "
          "the sheet then folds to a sharp, zero-radius outside corner with no springback and no cracking or orange-peel of the finish — the way "
          "stainless elevator and door panels, column cladding, signage, appliance fronts and architectural trim are made, and the way thick "
          "sheet is bent on a small press brake. NovoTech sells its own value-line CNC V-grooving machines in Canada: the horizontal machines lay "
          "the sheet flat on a 10.5 to 20 ft table, the vertical machines stand it against a fixed beam in half the floor space and groove plate "
          "to 1/4″. Four-tool servo heads on ball screws, ± 0.01 mm, Taiwan CNC and servos, hydraulic clamping that does not mark the sheet. "
          "Installed and supported from Mississauga, ON, Canada, with a CSA-approved panel.",
    points=["Horizontal: 7 sizes, 10.5 – 20 ft × 49 – 59″, sheet 0.016″ – 5/32″, four-tool head at 295 ft/min",
            "Vertical: 4 sizes, 10.5 – 13 ft × 49 – 59″, plate to 1/4″, rear feeding, half the footprint",
            "± 0.01 mm positioning, 0.001 mm resolution; hydraulic blank holder; CNC with touchscreen"],
    hero="vl-vg-h-1", minis=["vl-vg-v-1", "vl-vg-corner"],
    groups=[("vg-h", "Horizontal CNC V-grooving machines", "The sheet lies flat on the table: the longest sheets, the four-tool head and the fastest grooving.", BRAND),
            ("vg-v", "Vertical CNC V-grooving machines", "The sheet stands against the beam: half the floor space, no bed sag, plate to 1/4″.", BRAND)],
    faq=[{"q": "What is V-grooving for?",
          "a": "Three things. Sharp corners: a press brake leaves an inside radius about equal to the thickness, a grooved sheet folds to a radius near zero, which is what architects, elevator and furniture makers want in stainless and aluminum. Finish: the groove removes most of the thickness so the outer skin bends without stretching — no cracking, no orange peel, no marking of brushed or mirror stainless and pre-painted sheet. Force: a grooved 1/4″ plate bends on a 40-ton brake, and long panels bend by hand on a folder."},
         {"q": "Horizontal or vertical machine?",
          "a": "The horizontal machine lays the sheet on a table with pneumatic clamps along the edge and the head travels the length — the machine for long panels (to 20 ft), thin sheet and the highest speed, and the one most sign and cladding shops buy. The vertical machine clamps the sheet upright against a fixed beam and feeds it from the rear: the bed cannot deflect, it grooves plate to 1/4″ and it takes half the floor space, at the cost of the 13 ft maximum length."},
         {"q": "What sheet can it groove?",
          "a": "Stainless, mild steel, aluminum, copper and brass from 0.016″ to 5/32″ on the horizontal machines and to 1/4″ on the vertical; sheet widths of 49 or 59″ and lengths of 10.5, 13, 16 and 20 ft. The groove depth is programmed in the control — typically 60 – 70 % of the thickness for a 90° bend — with the first groove no closer than 5/16″ to the edge."},
         {"q": "How is it programmed?",
          "a": "On the touchscreen CNC: enter the sheet thickness, the groove positions (or a pitch and count), the depth and the number of passes, and the machine runs the sheet automatically; the four-tool head takes the groove in several light cuts for a clean V. Programs are stored and recalled; the control runs in inches or millimetres."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about V-grooving machines",
    related_pages=[{"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "folder-sheet-metal-brake.html", "label": "Roofing & pan brakes"}, {"href": "hydraulic-shearing-machine.html", "label": "Hydraulic shears"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring & finishing"}],
    related_title="More sheet-metal machinery from NovoTech",
)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key, p in PH.PHOTOS.items():
        ext, cut = PH.export_kind(key)
        if not os.path.exists(os.path.join(PH.OUT, key + ext)):
            print("!! missing export for", key)
            continue
        imap[key] = {"src": f"tools/src-images/value-sheet/{key}{ext}", "alt": p["alt"], "section": "value-sheet", "trim": ext == ".png", "quality": 82, "cutout": cut}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "vl_sheet_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    pdf_hpb = pdf(PDF_HPB, "Download the hydraulic press brake brochure")
    pdf_epb = pdf(PDF_EPB, "Download the electric press brake brochure")
    pdf_shear = pdf(PDF_SHEAR, "Download the value-line hydraulic shears brochure")
    pdf_vg = pdf(PDF_VG, "Download the V-grooving machine brochure")
    fams = [dict(f, pdf=pdf_hpb) for f in D.HPB_FAMILIES] + [dict(f, pdf=pdf_epb) for f in D.EPB_FAMILIES]
    fams += [dict(f, pdf=pdf_shear) for f in D.SHEAR_FAMILIES] + [dict(f, pdf=pdf_vg) for f in D.VG_FAMILIES]
    write_families(SET, fams)
    common = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN}
    # the press-brake families are shown on the hydraulic / electric press brake pages (tools/press_brake_types.py), not on a value-line page
    # the shear families are shown on the hydraulic / mechanical / sheet metal shear pages (tools/shear_types.py), not on a supplier page
    write_category(D.P_VG, PAGE_VG, fams, SET, "V-grooving machines", extra={**common, **NO_VIDEO, "nav_label": "V-grooving machines", "catalogue_pdf": pdf_vg})
    keys = register_images()
    used = {k for f in D.ALL for k in f["images"]}
    for p in (PAGE_PB, PAGE_SHEAR, PAGE_VG):
        used |= {p["hero"]} | set(p["minis"])
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    vids = sorted({v["id"] for f in D.ALL for v in f["videos"]})
    open(os.path.join(ROOT, "tools", "vl_sheet_vids.txt"), "w").write(" ".join(vids))
    print(f"value-sheet: {len(fams)} families on 4 pages (+ {len(D.PANEL_FAMILIES)} panel, {len(D.IRON_FAMILIES)} ironworker) · images: {len(keys)} · videos: {len(vids)}")


if __name__ == "__main__":
    build()
