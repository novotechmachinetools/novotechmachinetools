#!/usr/bin/env python3
"""The sheet-metal brake section: one short hub (folder-sheet-metal-brake.html, hub.html template) over six pages, one per
kind of brake — box and pan brakes, hand brakes and folding machines, magnetic brakes, hydraulic / electric / CNC folding
machines, portable roofing and siding brakes, 3-in-1 shear-brake-roll machines — each with every model of that kind in one
table under the hero, then the families with their spec tables and photos.

The families are the NovoTech value-line brakes written by tools/ttmc_more_pages.py (family set content/families/ttmc-more.json),
so run that first:

    python3 tools/ttmc_more_pages.py && python3 tools/brake_hub.py

One page per kind of machine, not one page of 137 models: buyers search for the kind ("box and pan brake", "siding brake",
"magnetic sheet metal brake") and a long page can hold only one title (reports/ساختار صفحات محصول و سئو.md)."""
import json
import os

from isitan_lib import CRUMBS, VOLT_FAQ_GENERIC, write_category, write_json
import ttmc_more_data as D
import ttmc_more_pages as TP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "ttmc-more"
HUB = "folder-sheet-metal-brake"
SECTION = "Sheet metal brakes"
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}

LENGTH = ["bending_length", "working_length", "working_width", "capacity_length_mild_steel", "coil_width", "bending_capacity_width"]
CAPACITY = ["capacity_mild_steel", "capacity", "shear_brake_roll_capacity_mild_steel", "bending_and_shearing_capacity_mild_steel", "capacity_length_mild_steel"]
RANGE = {"range_pick": [LENGTH, CAPACITY, "weight"], "range_cols": ["Length", "Capacity (mild steel)", "Weight"]}

# the six pages: slug, nav label, hero, minis, groups [(gid, title, lead, manual, [family ids])]
PAGES = {
    "box-and-pan-brake": dict(
        nav="Box and pan brakes", hero="tm-bp1650", minis=["tm-w2540h2", "tm-hw2540h"],
        title="Box and Pan Brakes for Sale in Canada — 12″ to 13 ft, 22 to 12 Gauge | NovoTech",
        meta="Box and pan brakes (finger brakes) sold, installed and supported in Canada: hand-operated brakes from 12″ to 157″ in 22 – 12 ga, heavy brakes that fold 14 ga boxes 9″ deep, and hydraulic box and pan brakes. Every model in one table.",
        h1="Box and pan brakes — finger brakes from 12″ to 13 ft, 22 to 12 gauge",
        intro="A box and pan brake (finger brake) is a sheet metal brake whose upper clamping blade is made of removable fingers: take the fingers out "
              "where the sides of a box come up and the leaf folds all four sides of a box or a pan; with every finger in place it works as a "
              "straight brake. NovoTech sells three kinds in Canada, all on this page: hand-operated box and pan brakes from a 12″ bench model "
              "to 157″, in 22 to 12 ga; heavy box and pan brakes from 52 to 100″ with 2, 3 and 4″ fingers that fold 14 ga boxes 9″ deep; and "
              "hydraulic box and pan brakes that clamp and fold 14 ga over 52 and 100″ from a foot pedal. Every model is listed in one table "
              "below with its length, capacity and weight, then each family with its full specification, photos and the finger sets supplied. "
              "NovoTech's value-line brakes are built in China to our specification, with parts and support from Mississauga, ON, Canada.",
        points=["Hand-operated box and pan brakes 12 – 157″, 22 to 12 ga mild steel, removable fingers in 1 – 6″ widths",
                "Heavy brakes 52 – 100″ with 2, 3 and 4″ finger sets — boxes to 9″ deep in 14 ga; counterweighted leaf",
                "Hydraulic box and pan brakes 52″ and 100″: 14 ga, foot-pedal clamping and folding"],
        groups=[("pb", "Box and pan brakes", "Hand-operated brakes from the 12″ bench model to 157″: the standard brake of the HVAC and sheet-metal shop.", True, ["tt-pb"]),
                ("pb-heavy", "Heavy box and pan brakes", "Heavier beams and deeper fingers: 14 ga boxes up to 9″ deep over 52 – 100″.", True, ["tt-pb-heavy"]),
                ("pb-hyd", "Hydraulic box and pan brakes", "Powered clamping and folding on a box and pan frame — a 100″ fold in 14 ga from a foot pedal.", False, ["tt-hw-h"])],
        faq=[{"q": "Box and pan brake or straight hand brake?",
              "a": "A straight (hand) brake has a one-piece clamping blade: the best choice for long straight bends such as flashing, trim and duct panels, and a little stiffer for its length. A box and pan brake has a blade of removable fingers, so it also folds the four sides of a box or a pan; with all the fingers in place it does everything the straight brake does. Most shops that make boxes, pans, enclosures and ducts buy the box and pan brake; the straight brakes are on the hand brake page."},
             {"q": "How deep a box can I fold?",
              "a": "The box depth is limited by the height of the fingers and the clearance behind the clamping beam: the standard box and pan brakes fold boxes up to about the finger height (2 – 3″), the heavy brakes with 4″ fingers fold 14 ga boxes 9″ deep, and for boxes of any depth a magnetic brake — which has no beam frame at the ends — is the machine. The maximum depth per model is in the specification table."},
             {"q": "How are the capacities rated, and what about stainless and aluminum?",
              "a": "Capacities are given in gauge of mild steel over the full bending length. Stainless steel bends at about two gauges lighter (a 16 ga brake takes 20 ga stainless), aluminum at about two gauges heavier. Bending at less than full length lets a brake take somewhat heavier sheet; folding heavier material than rated bends the beams permanently."},
             {"q": "Which finger sets come with the machine?",
              "a": "A full set of fingers that adds up to the bending length is in the crate, in widths from 1″ to 6″ (2, 3 and 4″ on the heavy brakes), so any combination of box sides can be made; extra fingers and narrow 1/2″ fingers are available. Fingers are hardened and ground on the bending edge and can be reversed for a second edge."},
             {"q": "Can a brake fold painted or coated sheet without marking it?",
              "a": "Yes — that is one of the reasons to fold instead of press-brake bending. The sheet is clamped and the leaf swings around the clamp edge without sliding over a die; a strip of protective film on the sheet keeps pre-painted and stainless finishes perfect."},
             VOLT_FAQ_GENERIC],
        related=[{"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                 {"href": "lock-former.html", "label": "Lock formers and HVAC machines"}, {"href": "bead-rollers.html", "label": "Bead rollers"}],
    ),
    "sheet-metal-hand-brake": dict(
        nav="Hand brakes & folders", hero="tm-hb2250", minis=["tm-pbb", "tm-bsm3150"],
        title="Sheet Metal Hand Brakes for Sale in Canada — Straight Brakes, Foot-Clamp Folders & Bench Brakes | NovoTech",
        meta="Sheet metal hand brakes sold, installed and supported in Canada: straight brakes from 12″ to 13 ft in 22 – 12 ga, foot-clamp folding machines to 119″ in 12 ga, and bench, slitting and offset brakes. Every model in one table.",
        h1="Sheet metal hand brakes — straight brakes, foot-clamp folders and bench brakes",
        intro="A sheet metal hand brake clamps the sheet under a one-piece beam and swings a folding leaf up around the edge by hand — long, "
              "straight, clean bends in thin sheet with no punch and die and no marks on painted material. NovoTech sells three kinds in "
              "Canada, all on this page: straight hand brakes from a 12″ bench model to 13 ft, in 22 to 12 ga, for flashing, trim and duct "
              "panels; foot-clamp folding machines from 40 to 119″ whose clamping beam closes from a foot pedal so both hands guide the sheet, "
              "to 12 ga; and bench brakes, shear-and-brake machines, slitting brakes and offset tools for the bench and the job box. Every "
              "model is listed in one table below with its length, capacity and weight, then each family with its full specification and "
              "photos. NovoTech's value-line brakes are built in China to our specification, with parts and support from Mississauga, ON, Canada.",
        points=["Straight hand brakes 12″ – 13 ft, 22 to 12 ga mild steel; counterweighted leaf, adjustable clamping and radius",
                "Foot-clamp folding machines 40 – 119″, 20 to 12 ga: pedal clamping, both hands on the sheet, angle stop",
                "Bench brakes 14 – 124″, shear-and-brake machines, slitting brakes and offset brakes, 22 – 18 ga"],
        groups=[("hb", "Straight hand brakes", "One-piece clamping blade for long, clean bends — flashing, trim, duct panels — from 12″ to 13 ft.", True, ["tt-hb"]),
                ("folder", "Foot-clamp folding machines", "The clamping beam closes from a foot pedal, so both hands feed and hold the sheet; 20 to 12 ga over 40 – 119″.", True, ["tt-folder"]),
                ("bench", "Bench, slitting and offset brakes", "Light brakes for the bench and the job box: bench brakes, shear-and-brake machines, slitting brakes and offset tools.", True, ["tt-bench-brake"])],
        faq=[{"q": "Hand brake, box and pan brake or magnetic brake — which do I need?",
              "a": "A hand (straight) brake has a one-piece clamping blade: the best choice for long straight bends — flashing, trim, duct panels. A box and pan brake has a blade made of removable fingers, so it folds the four sides of a box or a pan; with all the fingers in it works as a straight brake too. A magnetic brake has no clamping beam at all — an electromagnet holds a loose steel bar on the sheet — so it folds boxes of any depth, closed and narrow shapes and short return flanges, at the cost of a lower capacity. For 14 ga and heavier, or for production, choose a hydraulic or electric folding machine. Each kind has its own page."},
             {"q": "What does a foot-clamp folding machine add over a hand brake?",
              "a": "The clamping beam is closed by a foot pedal through a linkage instead of a hand lever, so the operator keeps both hands on the sheet to position it against the back stop — faster for repeat parts and safer for long, floppy sheet. The folding leaf is still swung by hand, with an adjustable angle stop for repeat bends."},
             {"q": "How are the capacities rated, and what about stainless and aluminum?",
              "a": "Capacities are given in gauge of mild steel over the full bending length. Stainless steel bends at about two gauges lighter (a 16 ga brake takes 20 ga stainless), aluminum at about two gauges heavier. Bending at less than full length lets a brake take somewhat heavier sheet; folding heavier material than rated bends the beams permanently."},
             {"q": "Can a brake fold painted or coated sheet without marking it?",
              "a": "Yes — the sheet is clamped and the leaf swings around the clamp edge without sliding over a die, so pre-painted and stainless sheet stays clean; a strip of protective film keeps a mirror finish perfect."},
             {"q": "What is a slitting brake and an offset brake?",
              "a": "A slitting brake has a roller knife that runs along the clamping beam to cut a strip from a sheet before folding it — the tool for trim and flashing from coil. An offset brake makes the small Z-shaped step (offset) at the edge of a panel in one stroke, for lap joints and door panels."},
             VOLT_FAQ_GENERIC],
        related=[{"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}, {"href": "bead-rollers.html", "label": "Bead rollers"},
                 {"href": "lock-former.html", "label": "Lock formers and HVAC machines"}, {"href": "motorized-plate-rollers.html", "label": "Slip rolls"}],
    ),
    "magnetic-sheet-metal-brake": dict(
        nav="Magnetic brakes", hero="tm-eb2500", minis=["tm-eb1250", "tm-eb-bars"],
        title="Magnetic Sheet Metal Brakes for Sale in Canada — 2 to 10 ft, 16 Gauge | NovoTech",
        meta="Magnetic sheet metal brakes sold, installed and supported in Canada: EB625 to EB3200, 16 ga over 2 – 8 ft and 18 ga over 10 ft, 3.3 – 13.2 US tons of electromagnetic clamping — fold boxes of any depth, closed shapes and short return flanges.",
        h1="Magnetic sheet metal brakes — 2 to 10 ft, 16 gauge, boxes of any depth",
        intro="A magnetic sheet metal brake clamps the sheet with an electromagnet in the bed instead of a mechanical beam: a loose steel clamping "
              "bar is held down by 3.3 to 13.2 US tons of magnetic force, and because there is no beam frame at the ends, a short bar folds the "
              "side of a box of any depth, closed shapes, narrow channels and short return flanges that a box and pan brake cannot reach. "
              "NovoTech sells the EB range in Canada, all on this page: six models from the EB625 at 2 ft to the EB3200 at 10 ft, 16 ga mild "
              "steel over 2 to 8 ft and 18 ga over 10 ft, each with a set of clamping bars, a radius bar and a back stop, and the leaf angle "
              "read on a scale. Every model is in the table below with its length, clamping force and weight, then the family with its full "
              "specification and photos. NovoTech's value-line brakes are built in China to our specification, with parts and support from "
              "Mississauga, ON, Canada.",
        points=["Six models, 2 – 10 ft: 16 ga × 2 – 8 ft and 18 ga × 10 ft mild steel; 3.3 – 13.2 US tons of clamping",
                "No end frames: boxes of any depth, closed and narrow shapes, short return flanges; clamping bars from 1″ and a radius bar included",
                "Single-phase 120 / 240 V, foot switch, 180° leaf, two-stage clamping for positioning"],
        groups=[("mag", "Magnetic sheet metal brakes", "An electromagnet in the bed clamps the sheet under a steel bar — no beam frame at the ends, so a short bar folds the side of a box of any depth.", False, ["tt-eb"])],
        faq=[{"q": "What can a magnetic brake fold that a box and pan brake cannot?",
              "a": "Anything the end frames of a conventional brake would block: the fourth side of a deep box, a closed or narrow channel, a short return flange, a flange inside a panel, a box with a lip. The clamping bars are loose pieces from 1″ long up, placed wherever the fold is, and the magnet holds whatever is under them. The price is capacity — 16 ga mild steel on the short models, 18 ga on the 10 ft — so for 14 ga and heavier the box and pan or hydraulic brakes are the machines."},
             {"q": "How strong is the clamping, and does the sheet slip?",
              "a": "The EB brakes clamp with 3.3 to 13.2 US tons across the full length, two-stage: a light hold to position the sheet, full force to fold. The sheet does not slip in rated material; the clamping bar edge gives the bend radius, and a radius bar is supplied for larger radii. The magnet releases the instant the foot switch is let go."},
             {"q": "How are the capacities rated, and what about stainless and aluminum?",
              "a": "In gauge of mild steel over the full length: 16 ga on the EB625 to EB2500 and 18 ga on the EB3200. Stainless steel bends at about two gauges lighter, aluminum at about two gauges heavier; shorter folds with a short clamping bar take heavier material than the full-length rating."},
             {"q": "What power does a magnetic brake need?",
              "a": "Single-phase 120 or 240 V — a wall outlet: the electromagnet draws power only while the foot switch is pressed. No hydraulics, no three-phase, so the brake can go anywhere in the shop or on a trailer."},
             VOLT_FAQ_GENERIC],
        related=[{"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}, {"href": "bead-rollers.html", "label": "Bead rollers"},
                 {"href": "corner-notcher.html", "label": "Corner notchers"}, {"href": "motorized-plate-rollers.html", "label": "Slip rolls"}],
    ),
    "hydraulic-folding-machine": dict(
        nav="Hydraulic & CNC folders", hero="tm-hwe", minis=["tm-tfm3100", "tm-efms2540l"],
        title="Hydraulic, Electric & CNC Folding Machines for Sale in Canada — 10 ga × 10 ft, 14 ga × 12 ft | NovoTech",
        meta="Powered sheet metal folding machines sold, installed and supported in Canada: hydraulic folders 10 ga × 4 – 10 ft and 3/16″ × 80 – 100″, electric folders 16 – 20 ga to 120″, and TFM / TFMS CNC folders 14 ga × 122 – 145″ with a programmable back gauge. Every model in one table.",
        h1="Hydraulic, electric and CNC folding machines — 10 ga over 10 ft, 14 ga CNC over 12 ft",
        intro="A powered folding machine clamps and folds the sheet with hydraulic cylinders or electric drives, so a 10 ft bend in 10 ga takes "
              "a foot pedal instead of two people and a CNC folder runs a 99-bend program with its back gauge while the operator only turns "
              "and feeds the sheet. NovoTech sells three kinds in Canada, all on this page: HW hydraulic folding machines, 10 ga over 4 to 10 ft "
              "and 3/16″ over 80 – 100″, with a hydraulic clamping beam, a folding beam driven by cylinders and a segmented upper beam on the "
              "box models; EFM / EFMS electric folding machines, 16 to 20 ga over 80 – 120″, for the shop that wants power without hydraulics; "
              "and TFM / TFMS CNC electric folders, 14 ga over 122 and 145″, with a CNC back gauge to 48″ and ±0.004″ repeatability for "
              "production panels, cassettes and enclosures. Every model is in the table below with its length, capacity and weight, then each "
              "family with its full specification and photos. NovoTech's value-line machines are built in China to our specification, with "
              "parts and support from Mississauga, ON, Canada.",
        points=["HW hydraulic folders: 10 ga × 4 – 10 ft and 3/16″ × 80 – 100″; hydraulic clamping, foot pedal, segmented beam on the H models",
                "EFM / EFMS electric folders 16 – 20 ga × 80 – 120″: motor-driven clamping and folding, no hydraulics",
                "TFM / TFMS CNC folders 14 ga × 122 – 145″: CNC back gauge 1/2 – 48-3/8″, ±0.004″, 99-bend programs, segmented beam on the TFMS"],
        groups=[("hw", "Hydraulic folding machines", "Powered clamping and folding: a 10 ft bend in 10 ga takes a foot pedal instead of two people; the H models fold boxes with a segmented beam.", False, ["tt-hw"]),
                ("efm", "Electric folding machines", "Motor-driven clamping and folding for 16 – 20 ga sheet over 80 – 120″ — power without hydraulics.", False, ["tt-efm"]),
                ("tfm", "CNC electric folding machines", "The TFM and TFMS run a program of up to 99 bends with a CNC back gauge — the production folder for panels, cassettes and enclosures.", False, ["tt-tfm"])],
        faq=[{"q": "When should I buy a folding machine instead of a press brake?",
              "a": "When the work is long panels in thin and medium sheet — duct, enclosures, architectural cladding, flashing — up to 10 ga. A folder bends from one side with the sheet lying flat, so a long panel needs no support or second person, there are no punch and die to change, and painted sheet is not marked. A press brake is the better machine for short heavy parts, for thick plate, for many different bends in one part and for tight tolerances on small flanges."},
             {"q": "Hydraulic, electric or CNC?",
              "a": "Hydraulic for the heaviest work — 10 ga over 10 ft and 3/16″ over 8 ft — and the lowest price per foot of capacity. Electric for 16 – 20 ga sheet where the shop wants powered clamping and folding without a hydraulic unit, oil or a three-phase pump. CNC when the same panels are made every day: the back gauge positions each flange from the program, the angle is corrected for springback and radii are folded in small steps, so an unskilled operator makes the part right first time."},
             {"q": "What does a CNC folding machine add?",
              "a": "A CNC folder (TFM, TFMS) positions the back gauge for every flange and folds to a programmed angle, one bend after the other from a program of up to 99 bends — the operator only turns and feeds the sheet. Programs are stored for repeat parts, the control corrects the angle for springback and folds radii in small steps. It pays for itself on production panels — cladding, cassettes, enclosures, duct — where a hand-set folder needs a skilled operator for every part. The TFMS has a segmented upper beam for boxes."},
             {"q": "How are the capacities rated, and what about stainless and aluminum?",
              "a": "In gauge (or inches) of mild steel over the full bending length; the specification tables give the stainless rating separately — about two gauges lighter — and aluminum goes about two gauges heavier. Folding at less than full length lets the machine take somewhat heavier sheet."},
             {"q": "Can a folding machine fold painted or coated sheet without marking it?",
              "a": "Yes — that is one of the reasons to fold instead of press-brake bending: the sheet is clamped and the beam swings around the clamp edge without sliding over a die. Protective film on the sheet keeps pre-painted and brushed stainless perfect."},
             VOLT_FAQ_GENERIC],
        related=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "hydraulic-shearing-machine.html", "label": "Hydraulic shears"},
                 {"href": "corner-notcher.html", "label": "Corner notchers"}, {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring machines"}],
    ),
    "roofing-siding-brake": dict(
        nav="Roofing & siding brakes", hero="tm-alb", minis=["tm-cd24", "tm-alb-work"],
        title="Portable Roofing & Siding Brakes for Sale in Canada — 7 to 12.5 ft, 24 Gauge | NovoTech",
        meta="Portable aluminum roofing and siding brakes sold, installed and supported in Canada: ALB brakes with roller slitter, 24 ga steel and 0.032″ aluminum over 7.2 – 12.5 ft, bend to 180°, set up in minutes, plus a 24″ trim coil dispenser.",
        h1="Portable roofing and siding brakes — aluminum brakes with slitter, 7 to 12.5 ft",
        intro="A portable roofing and siding brake folds flashing, trim, drip edge and fascia on site: an aluminum frame on folding legs, set up "
              "in 10 to 15 minutes, that clamps 24 ga steel or 0.032″ aluminum coil, bends it to 180° and slits the coil with a roller knife. "
              "NovoTech sells the ALB brakes in Canada, all on this page: six models from 7.2 to 12.5 ft with a silicone insert in the bending "
              "beam for pre-painted coil and copper, a slitter on a track and a carrying stand; and the CD-24 coil dispenser that feeds 24″ "
              "trim coil to the brake. Every model is in the table below with its length, capacity and weight, then the family with its full "
              "specification and photos. NovoTech's value-line brakes are built in China to our specification, with parts and support from "
              "Mississauga, ON, Canada.",
        points=["ALB brakes 7.2 – 12.5 ft: 24 ga steel, 0.032″ aluminum, 0.024″ copper; bend to 180°, 22.8″ throat",
                "Roller slitter on a track cuts the coil to width on the brake; silicone insert protects painted and copper coil",
                "Aluminum frame on folding legs, 132 – 220 lb, carried on the truck; CD-24 trim coil dispenser"],
        groups=[("alb", "Portable roofing and siding brakes", "Light brakes that go to the job: aluminum roofing brakes for flashing and trim with a roller slitter.", True, ["tt-alb"]),
                ("cd", "Trim coil dispenser", "The CD-24 holds a 24″ trim coil on two non-marring rollers and feeds it to the brake.", True, ["tt-cd24"])],
        faq=[{"q": "What do I need to bend roofing flashing on site?",
              "a": "A portable roofing brake: the ALB brakes have an aluminum frame on folding legs, set up in 10 – 15 minutes, take 24 ga steel and 0.032″ aluminum over 7.2 – 12.5 ft, bend to 180° and slit the coil with a roller knife. Add the CD-24 dispenser for trim coil. For the shop, a box and pan brake or a magnetic brake does the same work in heavier gauges."},
             {"q": "Which length should I buy?",
              "a": "Long enough for the longest piece you make in one bend — 10 ft for fascia and drip edge is the common choice, 12.5 ft for commercial trim — and no longer, because the brake is carried: the 7.2 ft model weighs 132 lb, the 12.5 ft model about 220 lb. Longer pieces are made in two overlapping bends."},
             {"q": "Does the slitter come with the brake?",
              "a": "Yes: a roller slitter on a track cuts the coil to width on the brake before folding, so a 24″ coil becomes drip edge, J-channel and fascia without a separate shear. Replacement cutting wheels are stocked in Mississauga, ON, Canada."},
             {"q": "Will it mark painted coil?",
              "a": "No — the bending beam has a silicone insert and the clamping surfaces are smooth aluminum, made for pre-painted steel and aluminum coil and for copper. Keep the protective film on the coil for a flawless finish."},
             VOLT_FAQ_GENERIC],
        related=[{"href": "sheet-metal-hand-brake.html", "label": "Hand brakes and bench brakes"}, {"href": "bead-rollers.html", "label": "Bead rollers"},
                 {"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}],
    ),
    "shear-brake-roll-3-in-1": dict(
        nav="3-in-1 machines", hero="tm-3in1", minis=["tm-e3in1", "tm-3in1-1016"],
        title="3-in-1 Shear, Brake & Roll Machines for Sale in Canada — 8″ to 80″ | NovoTech",
        meta="3-in-1 sheet metal machines sold, installed and supported in Canada: combination shear, brake and slip roll on one frame from 8″ to 52″ in 20 – 16 ga, and the motorized E3-IN-1 for 1/8″ × 52″ and 80″. Every model in one table.",
        h1="3-in-1 shear, brake and roll machines — 8″ to 80″",
        intro="A 3-in-1 machine puts a shear, a brake and a slip roll on one frame: the starter machine for the small sheet-metal, HVAC and "
              "hobby shop, and the compact machine for a maintenance department that cuts, folds and rolls a few parts a day. NovoTech sells "
              "two kinds in Canada, both on this page: hand-operated 3-in-1 machines from 8″ to 52″, 20 to 16 ga, with a guillotine shear, a "
              "finger brake and three rolls on one bench frame; and the motorized E3-IN-1 that shears 1/8″, bends 14 ga and rolls 12 ga over 52 "
              "and 80″ with a 4.7 HP motor. Every model is in the table below with its width, capacity and weight, then each family with its "
              "full specification and photos. NovoTech's value-line machines are built in China to our specification, with parts and support "
              "from Mississauga, ON, Canada.",
        points=["Hand-operated 3-in-1 machines 8 – 52″: shear, finger brake and slip roll, 20 – 16 ga mild steel on one bench frame",
                "Motorized E3-IN-1, 52″ and 80″: shears 1/8″, bends 14 ga, rolls 12 ga, 4.7 HP",
                "Minimum rolling diameters per model; removable fingers for boxes; back gauge for the shear"],
        groups=[("3in1", "3-in-1 shear, brake and roll machines", "Three machines on one frame — the starter machine for the small sheet-metal and HVAC shop.", False, ["tt-3in1"]),
                ("e3in1", "Motorized E3-IN-1 machines", "The powered combination machine: 1/8″ shearing, 14 ga bending and 12 ga rolling over 52 and 80″.", False, ["tt-e3in1"])],
        faq=[{"q": "Is a 3-in-1 machine as good as three separate machines?",
              "a": "No — it is as good as the three machines a small shop would otherwise not have. The shear, brake and roll share one frame and one capacity rating, so each is lighter than a dedicated machine of the same width, and changing from one function to another takes a minute. For a shop that cuts, folds and rolls a few parts a day in 20 – 16 ga it is the right buy; for production, buy the dedicated shear, box and pan brake and slip roll."},
             {"q": "Which size do I need?",
              "a": "By the widest sheet you cut or fold in one piece: the 12″ and 24″ models for enclosures and small parts, 40″ and 52″ for duct and panel work, 80″ (E3-IN-1) for full sheets. The capacity — 20 to 16 ga on the hand-operated models, 1/8″ shear and 14 ga brake on the motorized — is the same across the width."},
             {"q": "How small a cylinder can it roll?",
              "a": "The minimum rolling diameter is set by the roll diameter and is listed per model in the table; the slip roll section also has grooves for wire and the top roll lifts to slip the finished cylinder off."},
             {"q": "How are the capacities rated, and what about stainless and aluminum?",
              "a": "In gauge of mild steel over the full width; stainless about two gauges lighter, aluminum about two gauges heavier. The hand-operated models rate copper, brass and aluminum separately in the specification table."},
             VOLT_FAQ_GENERIC],
        related=[{"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}, {"href": "box-and-pan-brake.html", "label": "Box and pan brakes"},
                 {"href": "motorized-plate-rollers.html", "label": "Slip rolls"}, {"href": "bead-rollers.html", "label": "Bead rollers"}],
    ),
}

HUB_PAGE = dict(
    title="Sheet Metal Brakes & Folding Machines for Sale in Canada — Box & Pan, Hand, Magnetic, Hydraulic & CNC | NovoTech",
    meta="Every sheet metal brake and folding machine NovoTech sells in Canada, by kind: box and pan brakes, hand brakes and foot-clamp folders, magnetic brakes, hydraulic / electric / CNC folding machines, portable roofing and siding brakes and 3-in-1 machines — 137 models in one table, with a buying guide.",
    h1="Sheet metal brakes and folding machines — box and pan, hand, magnetic, hydraulic, roofing and 3-in-1",
    intro="A sheet metal brake (folder) bends sheet by clamping it under a straight beam and swinging a folding leaf up around the edge — no punch "
          "and die, no marks on painted sheet, and long, straight bends in thin material that a press brake cannot hold flat. NovoTech sells six "
          "kinds in Canada, each on its own page: box and pan brakes with removable fingers for boxes and pans; straight hand brakes, foot-clamp "
          "folding machines and bench brakes for flashing, trim and duct; magnetic brakes that fold boxes of any depth; hydraulic, electric and "
          "CNC folding machines for 10 ga over 10 ft and production panels; portable roofing and siding brakes for the job site; and 3-in-1 "
          "shear, brake and roll machines for the small shop. Below, the six kinds compared, every one of the {n} models in one table, the "
          "questions we get asked and the buying guide. NovoTech's value-line brakes are built in China to our specification, with parts and "
          "support from Mississauga, ON, Canada.",
    points=['<a href="box-and-pan-brake.html">Box and pan brakes</a> 12 – 157″ to 12 ga and 14 ga boxes 9″ deep; <a href="sheet-metal-hand-brake.html">hand brakes and foot-clamp folders</a> to 13 ft; <a href="sheet-metal-hand-brake.html#tt-bench-brake">bench brakes</a>',
            '<a href="magnetic-sheet-metal-brake.html">Magnetic brakes</a> 2 – 10 ft, 16 ga, boxes of any depth; <a href="hydraulic-folding-machine.html">hydraulic folders</a> 10 ga × 10 ft; <a href="hydraulic-folding-machine.html#tt-tfm">TFM / TFMS CNC folders</a> 14 ga × 12 ft',
            '<a href="roofing-siding-brake.html">Portable roofing and siding brakes</a> 7 – 12.5 ft with slitter; <a href="shear-brake-roll-3-in-1.html">3-in-1 shear, brake and roll machines</a> 8 – 80″'],
    hero="tm-eb2500", minis=["tm-hwe", "tm-bp1650"],
    range_cols=RANGE["range_cols"],
    range_lead="Every brake and folding machine NovoTech sells — all {n} models in one table: bending length, capacity in mild steel and weight. Each row links to the model's full specification on its page.",
    range_caption="Sheet metal brakes and folding machines supplied by NovoTech — value line, built to our specification",
    range_note="Capacities are rated in gauge of mild steel over the full bending length; stainless about two gauges lighter, aluminum about two gauges heavier. Single-phase and three-phase machines are supplied with a CSA-approved panel; voltages on request.",
    faq_title="Questions we get asked about sheet metal brakes",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "sheet-metal-shears.html", "label": "Sheet metal shears"},
                   {"href": "lock-former.html", "label": "Lock formers and HVAC machines"}, {"href": "bead-rollers.html", "label": "Bead rollers"},
                   {"href": "motorized-plate-rollers.html", "label": "Plate rollers and slip rolls"}, {"href": "corner-notcher.html", "label": "Corner notchers"}],
    related_title="Machinery that works alongside a sheet metal brake",
)

COMPARE = {
    "title": "Which kind of sheet metal brake?",
    "lead": "The six kinds NovoTech sells, side by side. The parts you make — boxes, long flashing, deep enclosures, production panels, site work — decide the kind; the pages list every model of each.",
    "cols": ["Kind", "What it folds", "Capacity and length", "Best for", "Page"],
    "rows": [
        ["Box and pan brakes", "Boxes, pans and straight bends; removable fingers", "22 – 12 ga × 12 – 157″; 14 ga boxes 9″ deep", "HVAC, enclosures, sheet-metal shops", {"href": "box-and-pan-brake.html", "label": "Box and pan brakes"}],
        ["Hand brakes and folders", "Long straight bends; foot-clamp folders; bench brakes", "22 – 12 ga × 12″ – 13 ft", "Flashing, trim, duct panels, job boxes", {"href": "sheet-metal-hand-brake.html", "label": "Hand brakes and folders"}],
        ["Magnetic brakes", "Boxes of any depth, closed shapes, return flanges", "16 ga × 2 – 8 ft, 18 ga × 10 ft", "Enclosures, signage, prototypes, mobile shops", {"href": "magnetic-sheet-metal-brake.html", "label": "Magnetic brakes"}],
        ["Hydraulic, electric and CNC folders", "Heavy and long panels, powered; programs on the CNC", "10 ga × 10 ft, 3/16″ × 8 ft; CNC 14 ga × 12 ft", "Cladding, cassettes, enclosures, production duct", {"href": "hydraulic-folding-machine.html", "label": "Hydraulic and CNC folders"}],
        ["Roofing and siding brakes", "Flashing, drip edge, fascia from coil, on site", "24 ga steel, 0.032″ aluminum × 7 – 12.5 ft", "Roofers, siding and eavestrough contractors", {"href": "roofing-siding-brake.html", "label": "Roofing and siding brakes"}],
        ["3-in-1 machines", "Shear, fold and roll on one frame", "20 – 16 ga × 8 – 52″; motorized 1/8″ × 52 – 80″", "Small shops, maintenance, schools", {"href": "shear-brake-roll-3-in-1.html", "label": "3-in-1 machines"}],
    ],
}


def hub():
    return {"slug": HUB, "label": "All sheet metal brakes", "image": "tm-eb2500",
            "blurb": "Every sheet metal brake and folding machine NovoTech sells, by kind — the six kinds compared, all 137 models in one table and the buying guide."}


def siblings():
    return [(s, p["nav"], p["h1"].split(" — ")[0]) for s, p in PAGES.items()]


def build():
    fs = json.load(open(os.path.join(ROOT, "content", "families", f"{SET}.json"), encoding="utf-8"))["families"]
    all_fams, subpages = [], []
    for slug, p in PAGES.items():
        members = []
        for gid, title, lead, manual, fids in p["groups"]:
            for fid in fids:
                members.append(dict(fs[fid], id=fid, group=gid, page=slug))
        n = sum(len(f["specs"]["models"]) for f in members)
        groups = [(gid, title, lead) for gid, title, lead, _, _ in p["groups"]]
        page = {"title": p["title"], "meta": p["meta"], "h1": p["h1"], "intro": p["intro"].replace("{n}", f"{n:,}"), "points": p["points"],
                "hero": p["hero"], "minis": p["minis"], "groups": groups, "faq": p["faq"], "related_pages": p["related"],
                "related_title": "More sheet-metal machinery from NovoTech"}
        write_category(slug, page, members, SET, SECTION, hub=hub(), siblings=siblings(),
                       extra={"hero_brand_line": TP.BRAND_LINE, "origin_feature": TP.ORIGIN, **NO_VIDEO, "nav_label": p["nav"], "catalogue_pdf": None,
                              **RANGE, "range_lead": f"Every model on this page in one table — {n} machines: bending length, capacity in mild steel and weight. Each row links to the full specification below.",
                              "range_caption": f"{p['h1'].split(' — ')[0]} supplied by NovoTech — value line", "range_title": "Every model at a glance"})
        # the manual-machine tagline the TTMC generator puts on hand-operated groups
        path = os.path.join(ROOT, "content", "pages", f"{slug}.json")
        d = json.load(open(path, encoding="utf-8"))
        for g, (gid, _, _, manual, _) in zip(d["groups"], p["groups"]):
            if manual:
                g["tagline"] = TP.MANUAL_TAG
        write_json(path, d)
        all_fams += members
        blurb = p["meta"].split(": ", 1)[-1].split(" Every model")[0].strip()
        subpages.append({"slug": slug, "title": p["h1"], "image": p["hero"], "blurb": blurb[0].upper() + blurb[1:], "families": [f["id"] for f in members], "nav_label": p["nav"],
                         "cards_title": p["h1"].split(" — ")[0] + " — every family"})
        print(f"{slug}: {len(members)} families, {n} models")
    n_all = sum(len(f["specs"]["models"]) for f in all_fams)
    h = HUB_PAGE
    page = {
        "slug": HUB, "template": "hub.html", "family_set": SET, "nav_label": "All sheet metal brakes",
        "title": h["title"], "artifact_title": "Sheet metal brakes", "meta_description": h["meta"], "h1": h["h1"], "intro": h["intro"].replace("{n}", f"{n_all:,}"),
        "hero_points": h["points"], "hero_image": h["hero"], "hero_image_secondary": h["minis"],
        "breadcrumb": CRUMBS + [{"label": SECTION}], "hero_brand_line": TP.BRAND_LINE,
        "subpages": subpages,
        "range_kind": "table", "range_cols": h["range_cols"], "range_lead": h["range_lead"].replace("{n}", f"{n_all:,}"), "range_caption": h["range_caption"], "range_note": h["range_note"],
        "range_pick": RANGE["range_pick"],
        "faq": TP.PAGES[D.P_BRAKE]["faq"], "faq_title": h["faq_title"],
        "catalogue_pdf": None, "origin_feature": TP.ORIGIN, "section_label": SECTION,
        "related_blurb": hub()["blurb"], "related_pages": h["related_pages"], "related_title": h["related_title"],
        "hub_compact": True, "compare": COMPARE, "subpage_link": "all models, specifications and photos", "family_noun": "machine",
        **NO_VIDEO,
    }
    write_json(os.path.join(ROOT, "content", "pages", f"{HUB}.json"), page)
    print(f"sheet metal brake hub: {len(all_fams)} families, {n_all} models on {len(PAGES)} pages")


if __name__ == "__main__":
    build()
