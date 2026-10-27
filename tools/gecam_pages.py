#!/usr/bin/env python3
"""Gecam (Parma, Italy) and its Eurofintec division — deburring & finishing hub and pages, the pipe sanding page (with the NovoTech
premium-line BT 114-S) and the corner welding page; image registration (section 'gecam') and the NovoTech-format brochure spec.

    Metal deburring & finishing     sheet-metal-plate-deburring-edge-rounding-finishing-grinding (one page, the old site's URL):
                                    wide-belt deburring G15 · G30 · G65 · G135 · GM65 · GM110 · G30 WET · G65/135 WET,
                                    edge rounding & deslagging G135RB8 · GT06 · GT13 · G65DCC,
                                    brush machines & benches CUB 30 · CUB 65BB · CUB 30B1B2 · EASY T · GCB 25 / 30 / 40
    Corner grinders                 corner-grinding-machines                  135 · 136 · 131 · special corner grinders
    Pipe sanding & polishing        pipe-sanding-polishing-machines           BT 114-S (NovoTech premium line, first) · Eurofintec 141 · 144 ·
                                                                              128 S / SL / DL · 228 · 728 · 143 — a menu item of its own, no hub
    Corner welders                  corner-welding-machines                   CWS 200 · CWS 300

    python3 tools/gecam_photos.py                    # gecam.com, catalogue and brochure images → tools/src-images/gecam
    python3 tools/gecam_pages.py                     # families, pages, image_map entries (tools/gecam_keys.txt), brochure spec
    python3 tools/make_images.py --only $(cat tools/gecam_keys.txt)
    python3 tools/brochure/build_brochure.py tools/brochure/specs/gecam.json

All families live in the 'gecam' family set (the BT 114-S is copied in from the NovoTech premium line so the pipe page and the hub
can show it; tools/sahinler_pages.py no longer writes the pipe page).
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families, write_hub
from sahinler_families import POLISH_FAMILIES
from sahinler_lib import premium_pdf
import gecam_data as D
import gecam_photos as PH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "gecam"
SECTION = "Deburring & finishing"
PDF_FILE = "files/NovoTech-Gecam-Deburring-Finishing-Pipe-Sanding-2026.pdf"
PDF_LABEL = "Download the Gecam & Eurofintec deburring and finishing brochure"


def pdf(fid=None):
    f = os.path.join(ROOT, "src", PDF_FILE)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": PDF_FILE, "label": PDF_LABEL, "size": size}


def families(page=None):
    return [dict(f, pdf=pdf(f["id"])) for f in D.FAMILIES if page is None or f["page"] == page]


BT114 = [dict(f, page=D.P_PIPE) for f in POLISH_FAMILIES]          # its own premium-line brochure is attached in write_families
ALL = families(D.P_SHEET) + families(D.P_EDGE) + families(D.P_BRUSH) + families(D.P_CORNER) + BT114 + families(D.P_PIPE) + families(D.P_WELD)

BRAND_LINE = ("Gecam machines are designed and built in Parma, Italy, by GECAM — deburring, grinding and finishing machines made 100 % in "
              "Italy, with components from Italian suppliers within 125 miles of the plant. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Italy by Gecam", "text": "Gecam designs and builds deburring, grinding and finishing machines at Vicofertile, Parma — "
          "100 % made in Italy, with components from Italian suppliers within 125 miles (200 km) of the plant. In 2005 it took over Eurofintec, "
          "the abrasive-belt machine builder whose name its pipe and belt machines still carry."}
GECAM_VIDEO = {"intro_video": {"id": "nnEMwdcC5kQ", "title": "Gecam corporate introduction", "thumb": "video-nnEMwdcC5kQ", "duration": "PT2M27S"},
               "intro_video_heading": "Inside the factory — Gecam in Parma, Italy",
               "intro_video_text": "A tour of Gecam at Vicofertile, Parma, where the machines on this page are designed and built."}
SHARED = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **GECAM_VIDEO, "catalogue_pdf": pdf(), "catalogue_pdfs": None}
RELATED_TITLE = "More finishing and fabrication machinery from NovoTech"

# ------------------------------------------------------------------------------------------------ sheet metal deburring machines
PAGE_SHEET = dict(
    title="Sheet Metal Deburring Machines, 6″ – 53″ Wide | NovoTech",
    meta="Wide-belt deburring and satin finishing machines for laser-, punch- and plasma-cut parts: belt, top-brush and Scotch-Brite groups, dry or wet.",
    h1="Sheet metal deburring machines — wide-belt deburring and finishing, 5-7/8″ to 53-1/8″ wide",
    intro="A sheet metal deburring machine feeds flat parts on a conveyor under one to four working groups: an abrasive belt that "
          "takes the burr off laser-, punch- and plasma-cut edges, rotating and oscillating top brushes that round the edges, inside "
          "the holes too, and cylindrical Scotch-Brite brushes that leave an even satin finish — all in one pass, with no hand "
          "grinding. NovoTech sells the deburring machines of Gecam, built in Parma, Italy, small to large: the G15 (5-7/8″) and G30 "
          "(11-13/16″) for small parts and job shops; the G65 (25-9/16″) and G135 (53-1/8″) production machines with up to four "
          "groups, touch screen and electronic grit set as standard; the single-belt GM65 and GM110 for plain deburring and satin "
          "finishing; and the G30 WET and G65/135 WET for parts that must not get hot. Parts from .020″ to 4-3/4″ thick (5-1/2″ wet). "
          "Supplied with a CSA-approved panel, installed and supported from Mississauga, ON.",
    points=["Working width 5-7/8″ to 53-1/8″ · parts .020″ to 4-3/4″ thick (5-1/2″ on the wet machines)",
            "Abrasive belt, top brushes, four-brush carousel and Scotch-Brite brushes — up to 4 groups in one pass",
            "Touch screen, electronic grit set and ±.004″ thickness setting on the G65 and G135 · wet machines for heat-sensitive parts"],
    hero="gc-g65", minis=["gc-g15", "gc-g30-wet"],
    groups=[("gc-belt", "Dry deburring and satin finishing machines",
             "Belt and brush machines from 5-7/8″ to 53-1/8″ wide, small to large, with dust extraction at every working group.", D.GECAM),
            ("gc-wet", "Wet deburring machines",
             "Water sprayed at every tool and the sludge collected in a tank — for parts that would deform from the heat of dry grinding.", D.GECAM)],
    faq=[{"q": "What do the letters R, X, B, b, B4 and T stand for?",
          "a": "They are Gecam's working groups, named in the order the part meets them. R is an abrasive belt on a rubber contact roller — "
               "it takes off the burr and levels the surface. X is a double row of rotating, oscillating top brushes that round the edges, "
               "inside holes and slots too, and T a single row of them. B is a cylindrical Scotch-Brite brush for the finish and b an "
               "external one below the outfeed. B4 is a carousel of four abrasive brushes for heavier edge rounding. A G65 RXB, for "
               "example, deburrs, rounds and satin-finishes in one pass."},
         {"q": "Which width do I need?",
          "a": "Take the widest part you cut and add a little margin: 5-7/8″ (G15) and 11-13/16″ (G30) for small laser and punched parts, "
               "25-9/16″ (G65, GM65) for most job-shop work, 43-5/16″ (GM110) and 53-1/8″ (G135) when you deburr nested parts or full "
               "sheets. Thickness is not the limit — every machine takes parts up to 4-1/8″ or 4-3/4″ — but the groups are: plain "
               "deburring needs a belt, edge rounding needs brushes."},
         {"q": "How much dust extraction does a deburring machine need?",
          "a": "Each machine has a hood at every working group and needs a dust collector of the airflow in its table: 1,177 CFM "
               "(2,000 m³/h) for the G15, G30, GM65 and GM110, 2,354 CFM for the G65 and 3,531 CFM for the G135. We quote a matching "
               "collector with the machine. Wet machines need no dust collector — the water takes the dust to the sludge tank."},
         {"q": "Can it handle small parts?",
          "a": "Yes, with the right options: a vacuum table holds small parts of any material on the conveyor, and a magnetic track holds "
               "small steel parts. The rubberized pressure rollers before and after each group keep parts flat as they pass. Very small "
               "or awkward parts are better finished on a brush workstation such as the EASY T."},
         {"q": "Dry or wet?",
          "a": "Dry machines with dust extraction suit most steel and stainless work. Choose a wet machine when the heat of dry grinding "
               "would deform the parts, or when you want no grinding dust in the shop: the G30 WET and G65/135 WET spray water directly "
               "on every tool and collect the sludge in an external tank."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about sheet metal deburring machines",
    related_pages=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "corner-welding-machines.html", "label": "Corner welders"},
                   {"href": "press-brake.html", "label": "Press brakes"}],
)

# ------------------------------------------------------------------------------------------------ edge rounding & deslagging
PAGE_EDGE = dict(
    title="Edge Rounding & Deslagging Machines to 53″ | NovoTech",
    meta="Round laser-cut edges to 5/64″ inside the holes, both sides in one pass, and strip plasma and oxy-fuel slag: brush-carousel, cross-belt and deslagging machines.",
    h1="Edge rounding and deslagging machines — radius to 5/64″, both sides in one pass, slag off plasma parts",
    intro="An edge rounding machine turns the sharp edges of laser-, plasma- and punch-cut parts into an even radius, so they are safe to "
          "handle and paint or powder coating covers the edge instead of thinning out on it; a deslagging machine takes the dross off "
          "the bottom edge of thick plasma and oxy-fuel parts. NovoTech sells three Gecam machines for this work, built in Parma, Italy: "
          "the G135RB8, whose carousel of eight counter-rotating abrasive brushes rounds every edge — inside holes too — to a 5/64″ "
          "(2 mm) radius across 53-1/8″; the GT06 and GT13, which run strip brushes on cross belts above and below the part and round "
          "both sides in one pass without touching the faces, 23-5/8″ and 51-3/16″ wide; and the G65DCC, which breaks the slag off "
          "parts 3/8″ to 4-3/4″ thick and rounds their edges. Supplied with a CSA-approved panel, installed and supported from "
          "Mississauga, ON.",
    points=["G135RB8: 8-brush carousel, edge radius to 5/64″ (2 mm), 53-1/8″ wide",
            "GT06 · GT13: both sides of the part in one pass, faces untouched, 23-5/8″ and 51-3/16″ wide",
            "G65DCC: plasma and oxy-fuel slag off parts 3/8″ – 4-3/4″ thick, edges rounded in the same pass"],
    hero="gc-g135rb8", minis=["gc-gt13", "gc-g65dcc"],
    groups=[("gc-round", "Edge rounding machines",
             "A brush carousel for the largest radius on one side, and cross-belt strip brushes for both sides at once.", D.GECAM),
            ("gc-slag", "Deslagging machine", "For the dross under thick plasma- and oxy-fuel-cut parts.", D.GECAM)],
    faq=[{"q": "Why round the edges of laser-cut parts?",
          "a": "A laser or punch leaves a sharp, square edge that cuts hands and gloves and on which paint and powder coating pull thin — "
               "the edge is the first place a coated part rusts. A rounded edge is safe to handle and takes an even coat. The G135RB8 "
               "rounds edges to a 5/64″ (2 mm) radius; the GT06 and GT13 round the edges evenly on both sides at once."},
         {"q": "One side or both sides?",
          "a": "The G135RB8 works the top of the part, with the deepest radius and a belt for heavy burrs. The GT06 and GT13 work the edges "
               "from above and below in the same pass, so parts are not turned over and fed twice, and they leave the faces untouched — "
               "the choice for galvanized, brushed or pre-painted sheet."},
         {"q": "What is deslagging?",
          "a": "Removing the dross — re-solidified metal — that plasma and oxy-fuel cutting leave on the bottom edge of thick parts. Ground "
               "off by hand it takes minutes per part; the G65DCC presses an abrasive belt on a soft rubber roller against the edges, "
               "breaks the slag away and then rounds the edges with strip brushes, on parts 3/8″ to 4-3/4″ thick."},
         {"q": "Do the brushes mark coated or brushed sheet?",
          "a": "The strip brushes of the GT06 and GT13 work the edges and leave the faces as they were, so galvanized, brushed and "
               "pre-painted surfaces are kept. The G135RB8 is also suitable for surface-treated material; set its belt group off when "
               "the face must not be touched."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about edge rounding and deslagging machines",
    related_pages=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "plate-beveler.html", "label": "Plate bevelers"}],
)

# ------------------------------------------------------------------------------------------------ brush deburring & benches
PAGE_BRUSH = dict(
    title="Brush Deburring Machines & Deburring Benches | NovoTech",
    meta="Lower-cost deburring for flat, shaped and heavy parts: conveyor brush machines 12″ and 26″ wide, a vacuum-table brushing workstation and crossed-belt benches.",
    h1="Brush deburring machines and deburring benches — conveyor brush machines, a brushing workstation and crossed-belt benches",
    intro="Not every shop needs a wide-belt line. A brush deburring machine passes flat parts under cylindrical brushes on a conveyor "
          "and gives them a deburred, satin-finished surface at a fraction of the cost; a deburring workstation or bench lets the "
          "operator finish the parts no conveyor takes — heavy, thick, shaped, long or one-off. NovoTech sells three Gecam lines, built "
          "in Parma, Italy: the CUB 30, CUB 65BB and CUB 30B1B2 brush machines, 11-13/16″ and 25-9/16″ wide, with motorized pressure "
          "on every brush; the EASY T workstation, with a vacuum table and a two-tool brush arm that tilts through 180°; and the GCB "
          "25, 30 and 40 benches, where two long crossed abrasive belts run over a motorized table up to 157-1/2″ long. Supplied with "
          "a CSA-approved panel, installed and supported from Mississauga, ON.",
    points=["CUB brush machines: 11-13/16″ and 25-9/16″ wide, parts to 9-13/16″ thick, conveyor 3.3 – 23 ft/min",
            "EASY T: 31-1/2 × 51-3/16″ vacuum table, two tools on a 180° tilting arm, parts to 5-7/8″",
            "GCB 25 / 30 / 40: two crossed belts over tables 98-7/16″ to 157-1/2″ long, suction-cup manipulator for shaped parts"],
    hero="gc-cub", minis=["gc-easy-t", "gc-gcb"],
    groups=[("gc-brush", "Conveyor brush deburring machines", "Cylindrical brushes over a conveyor, each with its own motor and pressure setting.", D.GECAM),
            ("gc-bench", "Deburring workstation and crossed-belt benches", "For heavy, thick, long and shaped parts finished by the operator.", D.GECAM)],
    faq=[{"q": "Brush machine or wide-belt deburring machine?",
          "a": "A CUB brush machine deburrs and satin-finishes flat parts with cylindrical brushes — a clean, even finish and light "
               "deburring at a much lower price. Heavy burrs, edge rounding to a set radius and high volumes call for a wide-belt "
               "machine with an abrasive belt and top brushes, on the sheet metal deburring page."},
         {"q": "Which parts suit the EASY T?",
          "a": "Parts a conveyor cannot carry or would not finish evenly: thick plates up to 5-7/8″, heavy brackets, shaped and bent "
               "parts, and single pieces. The vacuum table holds the part while the operator guides the brush; the second tool on the "
               "arm is a quick tilt away."},
         {"q": "What is a crossed-belt bench used for?",
          "a": "Long and shaped parts — profiles, frames, panels, parts with flanges — that the operator deburrs, rounds and "
               "satin-finishes against the belt, choosing a roller, shoe or brush and its position along the belt for each job. The "
               "motorized table carries parts up to 220 lb, and the optional suction-cup manipulator holds shaped parts in any position."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about brush deburring machines",
    related_pages=[{"href": "sheet-metal-deburring-machines.html", "label": "Wide-belt deburring machines"}],
)

# ------------------------------------------------------------------------------------------------ corner grinders
PAGE_CORNER = dict(
    title="Corner Grinders — Corner Grinding Machines to 59″ | NovoTech",
    meta="Corner grinders (corner grinding machines, corner sanders) that grind the welds on box, cabinet and door corners flush or to a radius: hand-fed, automatic and PLC.",
    h1="Corner grinders — corner grinding machines for the weld seams of boxes, cabinets, doors and tube frames",
    intro="A corner grinder (corner grinding machine, also called a corner sander or weld seam sander) grinds the weld on the corner of a welded box, cabinet, door or "
          "tray flush with the sheet, or to a neat radius, ready for paint or polishing — work that takes long minutes with a hand "
          "grinder and never looks the same twice. NovoTech sells the corner grinders of Gecam, built in Parma, Italy: the hand-fed 131 "
          "and 136, where an abrasive belt on an oscillating fork grinds corners up to 5-7/8″ and 11-13/16″ high to a radius of 3/64″ to "
          "3/8″; the 135, whose head travels the full length of the edge by itself on boxes with edges up to 59″; and PLC-controlled "
          "machines for series work — an upper-corner grinder, a six-head grinder and a grinder for the welds of 90° tube frames. "
          "Supplied with a CSA-approved panel, installed and supported from Mississauga, ON.",
    points=["131 · 136: hand-fed, corners to 5-7/8″ and 11-13/16″ high, radius 3/64″ – 3/8″ or sharp",
            "135: automatic head travel along edges up to 31-1/2″ or 59″, one or two heads",
            "Special PLC grinders for upper corners, two corners at once and 90° tube frames"],
    hero="gc-135", minis=["gc-136", "gc-131"],
    groups=[("gc-corner", "Corner grinders for boxes, cabinets and doors",
             "The hand-fed 136 and 131 and the automatic 135, each grinding the corner weld with a belt pressed on by rollers or a pad.", D.GECAM),
            ("gc-corner-special", "Special corner grinders for series work",
             "PLC machines that run from a stored recipe: the operator places the part and starts the cycle.", D.GECAM)],
    faq=[{"q": "What does a corner grinder do?",
          "a": "It grinds the weld bead on an outside corner of a welded box, cabinet, door or tray flush with the sheet — or to a radius — "
               "so the corner can be painted, powder-coated or polished without visible weld. The belt runs over rollers or a pad shaped "
               "for the corner, so the result is the same on every part, unlike hand grinding."},
         {"q": "Hand-fed or automatic?",
          "a": "The 131 and 136 are hand-fed: the operator moves the corner along the belt — quick to set up for mixed boxes and doors. "
               "The 135 clamps the box and runs the head along the whole edge by itself, which suits long edges and repeat work, and a "
               "second head doubles its output. For high volumes of one part, the PLC machines grind two corners or a whole tube-frame "
               "corner per cycle."},
         {"q": "What radius can it make?",
          "a": "The oscillating fork of the 131 and 136 grinds a radius from 3/64″ to 3/8″ (R1 – R10 mm), or a sharp corner. The 135 "
               "grinds the weld flush; its PLUS version adds vertical, horizontal and oscillating head movement for radiusing."},
         {"q": "How high a box can it take?",
          "a": "Corner height up to 5-7/8″ on the 131 and 7-7/8″ or 11-13/16″ on the 136 (19-11/16″ on request). The 135 is limited by "
               "edge length — 31-1/2″ or 59″ — and the six-head grinder takes boxes up to 5-7/8″ high."},
         {"q": "Can you build a machine for my part?",
          "a": "Yes. Gecam designs special corner grinders around the part — the upper-corner, six-head and tube-frame machines on this "
               "page are examples. Send us a drawing or photo of the part and the weld, and the number of parts a shift."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about corner grinders",
    related_pages=[{"href": "corner-welding-machines.html", "label": "Corner welders"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                   {"href": "press-brake.html", "label": "Press brakes"}],
)

# ------------------------------------------------------------------------------------------------ pipe sanding & polishing
PAGE_PIPE = dict(
    title="Pipe Sanders & Polishing Machines to Ø15-3/4″ | NovoTech",
    meta="Tube sanders and pipe polishers for straight and bent tube: BT 114-S with automatic feeder, orbital, centreless and large-pipe sanders, tube-end deburring.",
    h1="Pipe sanders and pipe polishing machines — automatic, orbital and centreless tube sanders, Ø3/16″ to Ø15-3/4″",
    intro="A pipe sander (pipe polisher, tube polishing machine) runs abrasive belts or brushes over round or square tube to grind off "
          "rust, scale and weld discolouration, give stainless steel a satin or brushed finish and prepare tube for painting or "
          "plating. NovoTech has four kinds: the BT 114-S, NovoTech's premium-line sander with two belts and an automatic feeder for "
          "straight and bent tube Ø3/8″ to Ø4-1/2″; the Eurofintec 141 and 144 orbital sanders, whose belts orbit the tube so straight "
          "and bent round and oval tube is finished all round without turning, Ø3/8″ to Ø5-7/8″; the Eurofintec 128 S, 128 SL and 128 DL "
          "centreless sanders for bar and tube Ø3/16″ to Ø5-7/8″ and the 228 for pipe up to Ø15-3/4″; and the 728 tube brushing machine "
          "and 143 tube-end deburring machine. Eurofintec machines are built in Parma, Italy, by Gecam. Supplied with a CSA-approved "
          "panel and supported from Mississauga, ON.",
    points=["BT 114-S: automatic feeder, two 37 × 2″ belts, straight and bent tube Ø3/8″ – 4-1/2″",
            "141 · 144 orbital sanders for bent tube Ø3/8″ – 5-7/8″ · 128 centreless Ø3/16″ – 5-7/8″ · 228 to Ø15-3/4″",
            "728 tube brushing · 143 tube-end deburring, inside and outside, ends cut at 90° and 45°"],
    hero="sh-bt114s", minis=["ef-144", "ef-128sl"],
    groups=[("sahinler-polish", "Automatic pipe polishing and sanding machine", "The BT 114-S belt sander with automatic pipe feeder — NovoTech premium line, made in Turkey.", "sahinler"),
            ("ef-orbital", "Orbital pipe sanders", "Two belts orbit the tube in the head: straight and bent tube finished all round without turning.", D.EURO),
            ("ef-centreless", "Centreless and large-pipe sanders", "Round bar and tube turned against the belt as it passes — Ø3/16″ to Ø15-3/4″.", D.EURO),
            ("ef-brush", "Tube brushing and tube-end deburring", "A heavy brushing machine for tube and a deburring machine for cut tube ends.", D.EURO)],
    faq=[{"q": "Which pipe sander do I need?",
          "a": "For handrail, furniture and fabrication work in mixed sizes, straight and bent: the BT 114-S with its automatic feeder "
               "(Ø3/8″ – 4-1/2″) or the 141 / 144 orbital sanders (Ø3/8″ – 5-7/8″, round and oval). For long runs of straight bar and "
               "tube to an even satin or polished finish: a 128 centreless sander, two heads on the 128 DL for two grits in one pass. "
               "For pipe over Ø5-7/8″: the 228, to Ø15-3/4″. Tube ends go on the 143."},
         {"q": "What finish does a belt pipe sander give?",
          "a": "The finish follows the belt: a coarse grit removes rust, scale and weld colour; 180 – 240 grit gives the brushed, satin "
               "finish of architectural stainless handrail; finer belts and non-woven belts prepare for mirror polishing. Two belts run "
               "at once on the BT 114-S, so a cutting belt and a finishing belt can be fitted together."},
         {"q": "Does it polish bent tube?",
          "a": "The BT 114-S and the 141 and 144 orbital sanders do: the BT 114-S head and feeder follow bends up to 45°, and on the "
               "orbital sanders the belts orbit the tube as it is pushed through the head, so elbows and frames are finished after "
               "bending. Centreless machines finish straight bar and tube only."},
         {"q": "Round and square tube on the same machine?",
          "a": "The BT 114-S takes round pipe from Ø3/8″ to Ø4-1/2″ and square tube, passed through flat side by side, two faces at a "
               "time. The orbital and centreless sanders are for round tube (the orbital sanders oval too); the 143 deburrs the ends of "
               "round and square tube."},
         {"q": "How are cut tube ends deburred?",
          "a": "On the 143: the tube end is pushed into a prism against a wire brush that turns while its own axis rotates, deburring "
               "the inside and the outside of the end in one cycle — ends cut at 90° or 45°, round Ø13/16″ to Ø4-3/4″ and square to 4-3/4″."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about pipe polishing",
    related_pages=[{"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"},
                   {"href": "circular-cold-saws.html", "label": "Circular cold saws"}, {"href": "angle-rolls.html", "label": "Angle rolls & tube rollers"}],
)

# ------------------------------------------------------------------------------------------------ corner welders
PAGE_WELD = dict(
    title="Corner Welding Machines for Boxes, to 59 × 59″ | NovoTech",
    meta="TIG and plasma corner welders for bent boxes, cabinets and enclosures in steel, stainless and aluminum: copper clamping, guided torch, CNC touch screen.",
    h1="Corner welding machines — TIG and plasma corner welders for bent boxes, cabinets and enclosures",
    intro="A corner welding machine welds the corners of bent sheet-metal parts — boxes, cabinets, trays, enclosures, hoods — with the "
          "torch carried by the machine at a set speed instead of by hand, so every corner is the same and the welder is free while it "
          "runs. NovoTech sells the CWS 200 and CWS 300 of Gecam, built in Parma, Italy: the part is clamped from inside against copper "
          "blocks that hold the corner square and draw off the heat, the TIG or plasma torch runs along a guide at 0 to 118 in/min, and "
          "the CNC touch screen stores the parameters of every part. Mild steel, stainless steel and aluminum; corners 7-7/8″ or "
          "11-13/16″ high, parts from 3-15/16″ to 59″ square. The welded corner then goes to a corner grinder. Supplied with a "
          "CSA-approved panel, installed and supported from Mississauga, ON.",
    points=["Corners 7-7/8″ (CWS 200) or 11-13/16″ (CWS 300) high · parts 3-15/16″ to 59″ square",
            "TIG or plasma · guided torch, 0 – 118 in/min · two-axis torch movement available",
            "Pneumatic clamping on copper blocks · CNC touch screen with stored parameters"],
    hero="gc-cws", minis=["gc-cws-welding", "gc-cws-welded"],
    groups=[("gc-weld", "CWS corner welding machines", "Two corner heights, the same machine: clamp, start, and the torch welds the corner.", D.GECAM)],
    faq=[{"q": "What does a corner welding machine do?",
          "a": "It welds the corner seam of a bent part with the torch on a guide, moved by the machine at a set speed: the operator "
               "places the part, clamps it with a button and presses start. The result is a straight, even weld on every corner, made in "
               "the flat position whatever the operator's skill, and the welder can prepare the next part while it runs."},
         {"q": "What do the copper blocks do?",
          "a": "The part is pressed from inside against copper blocks — an external guide 7-7/8″ or 11-13/16″ high and an internal unit "
               "matched to the corner height. They hold the corner square during welding and draw the heat away, keeping the part cool "
               "and the weld zone clean; a cooling unit for the copper is available and recommended against discoloration."},
         {"q": "TIG or plasma — and is the power source included?",
          "a": "The CWS works with a TIG or a plasma welding power source, which carries the torch on the machine's guide. Tell us the "
               "material, thickness and corner you weld and we will quote the CWS with a matching power source, or connect yours."},
         {"q": "Which parts fit?",
          "a": "Bent parts from 3-15/16 × 3-15/16″ to 59 × 59″ with corners up to 7-7/8″ high (CWS 200) or 11-13/16″ (CWS 300), on a "
               "32-5/16 × 32-5/16″ table. Mild steel, stainless steel and aluminum."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about corner welding machines",
    related_pages=[{"href": "corner-grinding-machines.html", "label": "Corner grinders"}, {"href": "welding-positioners.html", "label": "Welding positioners"},
                   {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                   {"href": "press-brake.html", "label": "Press brakes"}],
    related_title="More welding and fabrication machinery from NovoTech",
)

# ------------------------------------------------------------------------------------------------ hub
HUB_PAGE = dict(
    title="Metal Deburring & Finishing Machines, 6″ – 53″ | NovoTech",
    meta="Deburring, edge rounding, deslagging, brush and corner grinding machines for laser-, plasma- and punch-cut parts and welded boxes.",
    h1="Deburring and finishing machines — for laser-cut parts and welded boxes",
    intro="A deburring machine takes the burr, slag and sharp edges off cut metal parts and gives them an even finish, so they can be "
          "handled safely, painted evenly and assembled without hand grinding. NovoTech supplies the machines of Gecam, built in Parma, "
          "Italy: wide-belt deburring machines from the 5-7/8″ G15 to the 53-1/8″ G135, dry or wet; edge rounding machines that round "
          "edges to 5/64″, inside holes and on both sides at once; a deslagging machine for plasma and oxy-fuel parts; brush deburring "
          "machines and benches for shops that do not need a wide-belt line; and corner grinders for the welds of boxes, cabinets and "
          "tube frames. Pipe sanders and polishers have a page of their own. Every machine is supplied with a CSA-approved panel, "
          "installed, and supported from Mississauga, ON. "
          "Below, each page in brief and every model in one table.",
    points=[f"<a href=\"{D.P_SHEET}\">Sheet metal deburring machines</a> — wide-belt deburring and satin finishing, 5-7/8″ to 53-1/8″, dry or wet",
            f"<a href=\"{D.P_EDGE}\">Edge rounding & deslagging</a> — radius to 5/64″, both sides in one pass · <a href=\"{D.P_BRUSH}\">brush deburring machines & benches</a>",
            f"<a href=\"{D.P_CORNER}\">Corner grinders</a> for the welds of boxes, cabinets, doors and tube frames"],
    hero="gc-g135", minis=["gc-135", "gc-g65"],
    faq=[{"q": "What does a deburring machine do?",
          "a": "It removes the burr that laser cutting, punching, shearing and plasma cutting leave on a part's edges, rounds the sharp "
               "edges and evens out the surface — in one pass on a conveyor, where hand grinding takes minutes per part and never comes "
               "out the same twice. Deburred parts are safe to handle, bend and weld cleanly, and take paint and powder coating evenly "
               "right to the edge."},
         {"q": "Belt, brushes or both?",
          "a": "The abrasive belt (R) cuts the burr off and levels the surface; top brushes (X, T) and brush carousels (B4, B8) round the "
               "edges, inside holes too; cylindrical Scotch-Brite brushes (B) give a satin finish. Most shops combine them — a belt and "
               "top brushes deburr and round in one pass, and a Scotch-Brite brush at the end leaves an even grain."},
         {"q": "Which machine for plasma and oxy-fuel parts?",
          "a": "The G65DCC: its D belt on a soft rubber roller breaks the slag off the bottom edge of parts 3/8″ to 4-3/4″ thick and "
               "strip brushes on two transverse belts round the edges in the same pass. For thinner plasma parts with light dross a G65 with belt and top "
               "brushes is usually enough."},
         {"q": "Can it round edges on both sides at once?",
          "a": "Yes — the GT06 and GT13 run strip brushes on cross belts above and below the part and round every edge on both sides in "
               "one pass, leaving the faces as they were. The G135RB8 works from the top with the deepest radius, 5/64″ (2 mm)."},
         {"q": "Do you install the machines and train operators?",
          "a": "Yes. Our technicians install and commission the machine anywhere in Canada, set up the groups and abrasives for your "
               "parts and train the operators; abrasives, brushes and parts are supplied from Mississauga, ON, and we support every "
               "machine by video call."},
         VOLT_FAQ_GENERIC],
    range_lead="Capacity, part thickness, feed, working groups and weight for every model on the four pages. Each row links to the full specification table of its machine.",
    range_cols=["Capacity", "Part thickness", "Feed", "Working groups / tools", "Weight"],
    range_caption="Deburring, edge rounding, brush and corner grinding machines supplied by NovoTech — Gecam, built in Parma, Italy",
    range_note="Working width is the widest part the machine takes; tube capacities are outside diameters. Feed is the conveyor or part speed. Weights are approximate and depend on the groups fitted.",
)
# ------------------------------------------------------------------------------------------------ the one deburring page
DEBUR_FAQ = HUB_PAGE["faq"][:4] + [q for q in PAGE_SHEET["faq"] if q is not VOLT_FAQ_GENERIC] + \
    [q for q in PAGE_EDGE["faq"] if q is not VOLT_FAQ_GENERIC and q["q"] != "What is deslagging?"] + \
    [q for q in PAGE_BRUSH["faq"] if q is not VOLT_FAQ_GENERIC] + [HUB_PAGE["faq"][4], VOLT_FAQ_GENERIC]
for _q in DEBUR_FAQ:                                     # the answers now point into this page, not to another one
    _q["a"] = _q["a"].replace(", on the sheet metal deburring page.", ", further up this page.")
PAGE_DEBUR = dict(
    title="Metal Deburring & Finishing Machines, 6″ – 53″ | NovoTech",
    meta="Gecam wide-belt deburring, edge rounding, deslagging and brush deburring machines and benches for laser-, punch- and plasma-cut parts, dry or wet.",
    h1="Metal deburring and finishing machines, 5-7/8″ to 53-1/8″ wide",
    intro="A metal deburring machine takes the burr, slag and sharp edges off laser-, punch- and plasma-cut parts and gives them an even "
          "finish — in one pass on a conveyor, where hand grinding takes minutes per part and never comes out the same twice. NovoTech "
          "sells the machines of Gecam, built in Parma, Italy, small to large: wide-belt deburring and satin-finishing machines from the "
          "5-7/8″ G15 to the 53-1/8″ G135, dry or wet, with an abrasive belt, top brushes and Scotch-Brite brushes in one pass; edge "
          "rounding machines that round every edge to 5/64″ (2 mm), inside holes too, or both sides of the part at once; the G65DCC, "
          "which breaks the slag off thick plasma and oxy-fuel parts; and, for shops that do not need a wide-belt line, CUB brush "
          "machines, the EASY T brushing workstation and GCB crossed-belt benches for heavy, long and shaped parts. Supplied with a "
          "CSA-approved panel, installed and supported from Mississauga, ON.",
    points=["Wide-belt deburring and satin finishing, 5-7/8″ to 53-1/8″ wide · parts .020″ to 4-3/4″ thick, dry or wet",
            "Edge rounding to 5/64″ (2 mm), both sides in one pass on the GT06 and GT13 · G65DCC deslagging for plasma parts 3/8″ – 4-3/4″",
            "CUB conveyor brush machines, the EASY T vacuum-table workstation and GCB crossed-belt benches for heavy and shaped parts"],
    hero="gc-g135", minis=["gc-g135rb8", "gc-cub"],
    groups=PAGE_SHEET["groups"] + PAGE_EDGE["groups"] + PAGE_BRUSH["groups"],
    faq=DEBUR_FAQ,
    faq_title="Questions we get asked about metal deburring machines",
    related_pages=[{"href": f"{D.P_CORNER}.html", "label": "Corner grinders"}, {"href": f"{D.P_PIPE}.html", "label": "Pipe sanding & polishing machines"},
                   {"href": "corner-welding-machines.html", "label": "Corner welders"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "plate-beveler.html", "label": "Plate bevelers"}, {"href": "press-brake.html", "label": "Press brakes"}],
)

SUBPAGES = [  # slug, title, image, blurb, nav label
    (D.P_SHEET, "Sheet metal deburring machines", "gc-g65", "Gecam G15, G30, G65, G135 and GM wide-belt deburring and satin finishing machines, 5-7/8″ to 53-1/8″ wide, dry or wet.", "Sheet metal deburring"),
    (D.P_EDGE, "Edge rounding & deslagging machines", "gc-g135rb8", "G135RB8 brush-carousel edge rounding to 5/64″, GT06 and GT13 double-sided edge rounding, G65DCC deslagging for plasma parts.", "Edge rounding & deslagging"),
    (D.P_BRUSH, "Brush deburring machines & benches", "gc-cub", "CUB conveyor brush machines, the EASY T vacuum-table workstation and GCB crossed-belt benches for heavy and shaped parts.", "Brush deburring & benches"),
    (D.P_CORNER, "Corner grinders", "gc-135", "Hand-fed 131 and 136, automatic 135 and PLC corner grinders for the welds of boxes, cabinets, doors and tube frames.", "Corner grinders"),
]
PAGES = {D.P_SHEET: PAGE_SHEET, D.P_EDGE: PAGE_EDGE, D.P_BRUSH: PAGE_BRUSH, D.P_CORNER: PAGE_CORNER}

PIPE_EXTRA = {
    "hero_brand_line": "Eurofintec pipe sanders are built in Parma, Italy, by Gecam; the BT 114-S is NovoTech's premium line, built in Turkey to "
                       "NovoTech's specification with European components. All sold, installed and supported in Canada by NovoTech.",
    "origin_feature": {"title": "Made in Italy and Turkey", "text": "The Eurofintec orbital, centreless and brushing machines are built by Gecam at Vicofertile, "
                       "Parma — 100 % made in Italy; the BT 114-S is built in Turkey for NovoTech's premium line, inspected before shipping."},
    **GECAM_VIDEO,
    "intro_video_text": "A tour of Gecam at Vicofertile, Parma, where the Eurofintec pipe sanders on this page are built (the BT 114-S is built in Turkey).",
    "catalogue_pdf": None, "catalogue_pdfs": [pdf(), premium_pdf("premium-sheet-metal")],
}

# ------------------------------------------------------------------------------------------------ brochure
ABOUT_NT = ("NovoTech sells, installs and supports Gecam and Eurofintec machines in Canada from Mississauga, Ontario — groups and abrasives "
            "chosen for your parts, installation, operator training, a CSA-approved panel, a 1-year warranty and parts and technical support "
            "in Canada.")
BROCHURE = dict(
    title="Deburring, finishing and pipe sanding machines",
    subtitle="Gecam wide-belt deburring, edge rounding, deslagging and brush machines · corner grinders and CWS corner welders · Eurofintec orbital, centreless and large-pipe sanders, tube brushing and tube-end deburring",
    cover_line="Gecam · Eurofintec · made in Italy · sold & serviced in Canada by NovoTech", range_label="Gecam & Eurofintec machinery",
    about_for="Gecam and Eurofintec machinery", about_kicker="Gecam · Parma, Italy", about_title="Deburring and finishing, made in Italy",
    about_text=["Gecam designs and builds machines for deburring, grinding and finishing metal at Vicofertile, Parma — 100 % made in Italy, "
                "with components from Italian suppliers within 125 miles of the plant. Its wide-belt machines deburr, round and satin-finish "
                "laser-, punch- and plasma-cut parts from 5-7/8″ to 53-1/8″ wide, dry or wet; its corner grinders and corner welders "
                "build and finish metal boxes; and since 2005 its Eurofintec division has built the orbital, centreless and brushing "
                "machines that finish tube and pipe.", ABOUT_NT],
    country="Italy", families=[f["id"] for f in D.FAMILIES], family_sets=["gecam"],
    groups=[{"title": "Sheet metal deburring machines", "families": [f["id"] for f in D.families(D.P_SHEET)]},
            {"title": "Edge rounding & deslagging machines", "families": [f["id"] for f in D.families(D.P_EDGE)]},
            {"title": "Brush deburring machines & benches", "families": [f["id"] for f in D.families(D.P_BRUSH)]},
            {"title": "Corner grinders", "families": [f["id"] for f in D.families(D.P_CORNER)]},
            {"title": "Corner welding machines", "families": [f["id"] for f in D.families(D.P_WELD)]},
            {"title": "Pipe sanding & polishing — Eurofintec", "families": [f["id"] for f in D.families(D.P_PIPE)]}],
    cover_photos=["gc-g135", "gc-135", "ef-144"], out="src/" + PDF_FILE)


def write_brochure_specs():
    d = os.path.join(ROOT, "tools", "brochure", "specs")
    spec = dict(BROCHURE, single_phase=False, year="2026", made_in="Made in Italy by Gecam — 100 % Italian")
    json.dump(spec, open(os.path.join(d, "gecam.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "gecam")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")] if os.path.isdir(d) else []
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/gecam/{key}{ext}", "alt": p["alt"], "section": "gecam", "trim": False, "quality": 82,
                     "cutout": bool(p.get("cutout"))}
        keys.append(key)
    for logo, alt in (("gecam-logo", "Gecam"), ("eurofintec-logo", "Eurofintec")):
        imap[logo] = {"src": f"tools/src-images/{logo}.png", "alt": alt, "section": "site", "trim": True, "quality": 90, "cutout": False}
        keys.append(logo)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "gecam_keys.txt"), "w").write(",".join(keys))
    return keys


def video_ids():
    return list(dict.fromkeys([v["id"] for f in D.FAMILIES for v in f["videos"]] + [GECAM_VIDEO["intro_video"]["id"]]))


def build():
    for f in ALL:                                          # the three deburring pages are one page now
        if f["page"] in (D.P_SHEET, D.P_EDGE, D.P_BRUSH):
            f["page"] = D.P_HUB
    write_families(SET, ALL)
    pipe_related = [{"href": f"{D.P_HUB}.html", "label": "Metal deburring & finishing machines"},
                    {"href": f"{D.P_CORNER}.html", "label": "Corner grinders"},
                    {"href": "tube-end-forming-machines.html", "label": "Tube end formers"}, {"href": "pipe-notcher.html", "label": "Tube notchers"}]
    # the wide-belt, edge rounding / deslagging and brush machines on one page (the old site's URL); corner grinders and pipe
    # sanders are menu items of their own — no hub
    write_category(D.P_HUB, {**PAGE_DEBUR, "related_title": RELATED_TITLE}, ALL, SET, "Metal deburring & finishing machines",
                   extra={**SHARED, "nav_label": "Metal deburring & finishing machines"})
    write_category(D.P_CORNER, {**PAGE_CORNER, "related_title": RELATED_TITLE,
                                "related_pages": [{"href": f"{D.P_HUB}.html", "label": "Metal deburring & finishing machines"},
                                                  {"href": f"{D.P_PIPE}.html", "label": "Pipe sanding & polishing machines"},
                                                  {"href": "corner-welding-machines.html", "label": "Corner welders"}]},
                   ALL, SET, "Corner grinders", extra={**SHARED, "nav_label": "Corner grinders"})
    write_category(D.P_PIPE, {**PAGE_PIPE, "related_title": RELATED_TITLE, "related_pages": pipe_related},
                   ALL, SET, "Pipe sanding & polishing machines", extra={**SHARED, **PIPE_EXTRA, "nav_label": "Pipe sanding & polishing machines"})
    write_category(D.P_WELD, PAGE_WELD, ALL, SET, "Corner welders", extra={**SHARED, "nav_label": "Corner welders"})
    for old in (D.P_SHEET, D.P_EDGE, D.P_BRUSH):          # merged into the deburring page
        fp = os.path.join(ROOT, "content", "pages", f"{old}.json")
        if os.path.exists(fp):
            os.remove(fp)
    keys = register_images()
    write_brochure_specs()
    pages = [PAGE_DEBUR, PAGE_CORNER, PAGE_PIPE, PAGE_WELD]
    used = {k for f in D.FAMILIES for k in f["images"]} | {p["hero"] for p in pages} | {m for p in pages for m in p["minis"]}
    used |= set(BROCHURE["cover_photos"])
    used -= {k for f in BT114 for k in f["images"]} | {"sh-bt114s"}          # registered by tools/sahinler_pages.py
    unused = sorted(set(keys) - used - {"gecam-logo", "eurofintec-logo"})
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        print("!! image keys without a photo (export still running?):", missing)
    open(os.path.join(ROOT, "tools", "gecam_vids.txt"), "w").write(" ".join(video_ids()))
    for name, p in [("deburring", PAGE_DEBUR), ("corner", PAGE_CORNER), ("pipe", PAGE_PIPE), ("weld", PAGE_WELD)]:
        print(f"{name:42s} title {len(p['title'])} · meta {len(p['meta'])}")
    print(f"gecam: {len(D.FAMILIES)} families · {sum(len(f['specs']['models']) for f in D.FAMILIES)} models · images: {len(keys)} · videos: {len(video_ids())}")


if __name__ == "__main__":
    build()
