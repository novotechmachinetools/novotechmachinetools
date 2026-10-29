#!/usr/bin/env python3
"""NovoTech value-line machines built by TTMC (sold under NovoTech's name with TTMC model codes, no supplier brand) — writes
  content/families/ttmc-more.json            every family of tools/ttmc_more_data.py (new pages) and ttmc_more_data2.py (groups)
  content/pages/<slug>.json                  the new pages (category.html), woodworking machinery among them
  content/extra_groups/ttmc-<slug>.json      value-line groups on pages other generators write (build.py apply_extra_groups)
  tools/image_map.json, tools/ttmc_more_keys.txt   the photos (tools/ttmc_more_photos.py — Vol. 23 catalogue, and
                                             tools/ttmc_new_photos.py — 2026 sheets and catalogues), section 'ttmc-more'
The EBQ01 bench shears and the PS-1220 coil slitter (ttmc_more_data2.SHEAR) go on sheet-metal-shears.html through
tools/ttmc_pages.py (family set 'ttmc').

    python3 tools/ttmc_more_photos.py && python3 tools/ttmc_new_photos.py && python3 tools/ttmc_more_pages.py && python3 tools/ttmc_pages.py
    python3 tools/make_images.py --only $(cat tools/ttmc_more_keys.txt) && python3 build.py
"""
import json
import os

from PIL import Image

from isitan_lib import CRUMBS, VOLT_FAQ_GENERIC, lower_keep_acronyms, write_families, write_json
import ttmc_more_data as D
import ttmc_more_data2 as D2
import ttmc_more_photos as PH
import ttmc_new_photos as NP
import ttmc_hires_photos as HP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "ttmc-more"
BRAND = "novotech"
BRAND_LINE = ("NovoTech value line — NovoTech's own brand, manufactured in China to high North American quality standards and sold with a "
              "1-year warranty, a CSA-approved panel on every 3-phase machine and parts and support from Mississauga, ON, Canada.")
ORIGIN = {"title": "NovoTech value line — built in China",
          "text": "Built in China to NovoTech's specification by a maker that exports metalworking machinery to more than 70 countries; inspected "
                  "before shipping, wired for Canadian power and supported by NovoTech's technicians in Mississauga, ON, Canada."}
MANUAL_TAG = D.MANUAL_TAG
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}
VOLT = VOLT_FAQ_GENERIC

# ---------------------------------------------------------------------------------------------------------------- new pages
# groups: (group id, title, lead, manual?) — every group is NovoTech value line
PAGES = {
    D.P_BRAKE: dict(
        title="Sheet Metal Brakes — Box & Pan, Magnetic & Hydraulic | NovoTech",
        meta="Sheet metal brakes in Canada: magnetic, box and pan brakes for 9″ deep boxes, hand brakes, hydraulic, electric and CNC folders, roofing brakes and 3-in-1s.",
        h1="Sheet metal brakes — box and pan, magnetic, hand and hydraulic folding machines",
        nav="Sheet metal brakes",
        intro="A sheet metal brake (folder) bends sheet by clamping it under a straight beam and swinging a folding leaf up around the edge — "
              "no punch and die, no marks on painted sheet, and long, straight bends in thin material that a press brake cannot hold flat. "
              "NovoTech's value-line brakes are built in China to our specification: magnetic brakes from 2 to 10 ft that clamp the sheet "
              "with an electromagnet and fold boxes of any depth, box and pan brakes with removable fingers — the heaviest fold 14 ga boxes "
              "9″ deep, by hand or with hydraulic power — hand brakes and foot-clamp folding machines for the HVAC, roofing and sheet-metal "
              "shop, hydraulic, electric and CNC folding machines for 10 ga over 10 ft, 3/16″ over 8 ft and 14 ga over 12 ft, portable "
              "roofing brakes and a coil dispenser for the job site, and combination shear, brake and roll machines — {n} models, with parts "
              "and support from Mississauga, ON, Canada.",
        points=["Magnetic brakes EB625 – EB3200: 16 ga × 2 – 8 ft and 18 ga × 10 ft, 3.3 – 13.2 US tons of clamping, boxes of any depth",
                "Box and pan brakes 12 – 157″ with removable fingers, 22 to 12 ga, boxes to 9″ deep in 14 ga; hand brakes and foot-clamp folders to 13 ft",
                "Hydraulic folding machines 10 ga × 4 – 10 ft and 3/16″ × 80 – 100″; TFM / TFMS CNC electric folders 14 ga × 122 – 145″"],
        hero="tm-eb2500", minis=["tm-hwe", "tm-bp1650"],
        groups=[("mag", "Magnetic sheet metal brakes", "An electromagnet in the bed clamps the sheet under a steel bar — no beam frame at the ends, so a short bar folds the side of a box of any depth.", False),
                ("hyd", "Hydraulic, electric and CNC folding machines", "Powered clamping and folding: a 10 ft bend in 10 ga takes a foot pedal instead of two people, and the CNC folders run a 99-bend program with their back gauge.", False),
                ("panbox", "Box and pan brakes", "The upper blade is made of removable fingers: take them out where the sides of the box come up and fold all four sides of a pan.", True),
                ("hand", "Hand brakes and foot-clamp folding machines", "Straight brakes with a one-piece blade for long, clean bends, and folders whose clamping beam closes from a foot pedal.", True),
                ("roof", "Portable roofing brakes and bench brakes", "Light brakes that go to the job: aluminum roofing brakes for flashing and trim, a coil dispenser, bench brakes, shear and brake machines, slitting brakes and offset tools.", True),
                ("combo", "Combination shear, brake and roll machines", "Three machines on one frame — the starter machine for the small sheet-metal and HVAC shop.", False)],
        faq=[{"q": "Box and pan brake, hand brake or magnetic brake — which do I need?",
              "a": "A hand (straight) brake has a one-piece clamping blade: the best choice for long straight bends — flashing, trim, duct panels. A box and pan brake has a blade made of removable fingers, so it folds the four sides of a box or a pan; with all the fingers in it works as a straight brake too. A magnetic brake has no clamping beam at all — an electromagnet holds a loose steel bar on the sheet — so it folds boxes of any depth, closed and narrow shapes and short return flanges that a box and pan brake cannot reach, at the cost of a lower capacity (16 ga to 8 ft). For 14 ga and heavier, or for production, choose a hydraulic or electric folding machine."},
             {"q": "How are the capacities rated, and what about stainless and aluminum?",
              "a": "Brake capacities are given in gauge of mild steel over the full bending length. Stainless steel bends at about two gauges lighter (a 16 ga brake takes 20 ga stainless), aluminum at about two gauges heavier. Bending at less than full length lets a brake take somewhat heavier sheet; folding heavier material than rated bends the beams permanently."},
             {"q": "Can a brake fold painted or coated sheet without marking it?",
              "a": "Yes — that is one of the reasons to fold instead of press-brake bending. The sheet is clamped and the leaf swings around the clamp edge without sliding over a die. The ALB roofing brakes have a silicone insert in the bending beam for pre-painted coil and copper; on the other brakes a strip of protective film on the sheet keeps the finish perfect."},
             {"q": "When should I buy a hydraulic folding machine instead of a press brake?",
              "a": "When the work is long panels in thin and medium sheet — duct, enclosures, architectural cladding, flashing — up to 10 ga. A folder bends from one side with the sheet lying flat, so a long panel needs no support or second person, there are no punch and die to change, and painted sheet is not marked. A press brake is the better machine for short heavy parts, for thick plate, for many different bends in one part and for tight tolerances on small flanges."},
             {"q": "What does a CNC folding machine add?",
              "a": "A CNC folder (TFM, TFMS) positions the back gauge for every flange and folds to a programmed angle, one bend after the other from a program of up to 99 bends — the operator only turns and feeds the sheet. Programs are stored for repeat parts, the control corrects the angle for springback and folds radii in small steps. It pays for itself on production panels — cladding, cassettes, enclosures, duct — where a hand-set folder needs a skilled operator for every part. The TFMS has a segmented upper beam for boxes."},
             {"q": "What do I need to bend roofing flashing on site?",
              "a": "A portable roofing brake: the ALB brakes have an aluminum frame on folding legs, set up in 10 – 15 minutes, take 24 ga steel and 0.032″ aluminum over 7.2 – 12.5 ft, bend to 180° and slit the coil with a roller knife. For the shop, a box and pan brake or a magnetic brake does the same work in heavier gauges."},
             {"q": "Do you still sell the brakes from the old website?",
              "a": "The brakes on this page replace the earlier roofing and box and pan brakes. If you need parts or service for a brake you bought from NovoTech before, call us at 647-526-5510 with the model and serial number."},
             VOLT],
        related=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "sheet-metal-shears.html", "label": "Sheet metal shears"},
                 {"href": "lock-former.html", "label": "Lock formers and HVAC machines"}, {"href": "bead-rollers.html", "label": "Bead rollers"},
                 {"href": "motorized-plate-rollers.html", "label": "Plate rollers and slip rolls"}, {"href": "corner-notcher.html", "label": "Corner notchers"}],
    ),
    D.P_LOCK: dict(
        title="Lock Formers — Pittsburgh Machines & HVAC Duct Tools | NovoTech",
        meta="Pittsburgh lock formers for 26 – 16 ga duct, an auxiliary roll former for button lock and drive cleat, an electric seam closer, a power beading machine and a slitting machine.",
        h1="Lock formers and HVAC duct machines — Pittsburgh lock formers, roll formers and duct tools",
        nav="Lock formers & HVAC",
        intro="A lock former (Pittsburgh machine) rolls the edge of a duct panel into the Pittsburgh lock — the pocket the matching flange is "
              "hammered into to close a rectangular duct — and, with other roll sets, double seams, drive cleats, button locks and flanges. "
              "NovoTech's value-line HVAC machines are built in China to our specification: the PF20G lock former for 26 – 20 ga, the PF16G "
              "for 25 – 16 ga with six roll forms as standard, and the AX20G auxiliary roll former whose roll sets change in under five "
              "minutes; and the machines that finish the duct — the SL-10 electric seam closer, the RM18E power beading machine for round "
              "duct and the LQ15 slitting and bending machine. Parts and support from Mississauga, ON, Canada.",
        points=["PF20G and PF16G Pittsburgh lock formers, 26 – 16 ga; AX20G roll former with button lock, drive cleat and 6-in-1 flange rolls",
                "SL-10 electric seam closer: closes Pittsburgh seams in three stages, 26 – 20 ga, 13 – 23 ft/min",
                "RM18E power beading machine for round duct, 15 ga; LQ15 slitting and bending machine, 16 ga × 47″"],
        hero="tm-pf16g", minis=["tm-ax20g", "tm-sl10"],
        groups=[("lock", "Lock formers and roll formers", "The machines that roll the joints of rectangular duct: Pittsburgh locks, double seams, drive cleats, button locks and flanges.", False),
                ("duct", "Electric seam closer", "The SL-10 closes the Pittsburgh seam after the lock former — faster and neater than a hammer.", False),
                ("round", "Power beading and slitting machines", "For round duct and pipe: a power beading machine and a slitting and bending machine.", False)],
        faq=[{"q": "What is a Pittsburgh lock, and what gauge can a lock former take?",
              "a": "The Pittsburgh lock is the standard longitudinal seam of rectangular duct: the lock former rolls a pocket on one edge of the panel, the other edge is bent to a 90° flange, the flange goes into the pocket and the lip is hammered (or closed with a seam closer) over it. The PF20G forms it in 26 to 20 ga, the PF16G in 25 to 16 ga mild steel; galvanized steel is the usual material."},
             {"q": "PF20G, PF16G or AX20G?",
              "a": "The PF20G is the compact lock former for light duct — Pittsburgh, flange attachment and right angle in 26 – 20 ga, with double seam and drive cleat rolls as options. The PF16G takes duct to 16 ga and has six roll forms as standard — Pittsburgh, flange attachment, right angle, double seam, drive cleat and Z — on one machine. The AX20G is an auxiliary roll former for the joints a lock former does not make: button locks, Acme double seams, drive cleats and a 6-in-1 set of flanges and standing seams, with roll sets that change in five minutes."},
             {"q": "How much material does a Pittsburgh lock use?",
              "a": "About 1″ of sheet for the pocket; the adjustable auto-guides set the edge so the pocket depth is consistent and material waste stays at a minimum. Allow for it when you lay out the blanks."},
             {"q": "Do I need a seam closer?",
              "a": "For a few ducts a week the lip is closed with a hammer. For production the SL-10 runs along the seam and closes it in three stages — 30°, 75°, 90° — adjusting itself to the sheet thickness: faster, quieter and a neater seam than hammering."},
             VOLT],
        related=[{"href": "folder-sheet-metal-brake.html", "label": "Sheet metal brakes"}, {"href": "bead-rollers.html", "label": "Bead rollers and beading machines"},
                 {"href": "sheet-metal-shears.html", "label": "Sheet metal shears"}, {"href": "circle-cutters-and-seamers.html", "label": "Circle shears and flanging"},
                 {"href": "motorized-plate-rollers.html", "label": "Plate rollers and slip rolls"}, {"href": "corner-notcher.html", "label": "Corner notchers"}],
    ),
    D.P_GRIND: dict(
        title="Metal Belt Grinders, Disc Sanders & Bench Grinders | NovoTech",
        meta="Belt grinders for metal with 2 – 8″ belts: pedestal, floor and wide-belt models, knife grinders, combination grinders, 12 – 20″ disc sanders, bench grinders, chamfering machines and dust collectors.",
        h1="Metal belt grinders, disc sanders and bench grinders",
        nav="Belt grinders & sanders",
        intro="Belt grinders are the finishing machines of the fabrication shop: they take the burr off a cut, blend a weld, square an end "
              "and put a chamfer on an edge faster than a hand grinder and with a flatter result. NovoTech's value-line grinders are built in "
              "China to our specification: pedestal belt grinders with 3″ and 6″ belts up to 5.5 HP, a mobile floor grinder for weld seams, "
              "wide-belt grinders with 4″ and 8″ belts, knife and tool grinders, combination machines with a belt, a disc and a wheel on one "
              "motor, disc sanders to 20″, bench grinders and wire-wheel machines, edge chamfering machines, end-surface grinders and the "
              "dust collectors that keep metal dust out of the shop. Parts and belts from Mississauga, ON, Canada.",
        points=["Pedestal belt grinders 3 × 79″ and 6 × 79″, 4 – 5.5 HP, to 6,693 ft/min; dust collector built in on the HB models",
                "Wide-belt grinders 4″ and 8″, mobile floor grinder, knife grinders, combination belt / disc / wheel machines",
                "Disc sanders 12″ and 20″, bench grinders 8 – 10″, chamfering machines to 1/4″, metal dust collectors 494 – 650 CFM"],
        hero="tm-s75h", minis=["tm-s220", "tm-sp6"],
        groups=[("belt", "Belt grinders", "Pedestal, floor, column and wide-belt grinders for deburring, blending welds and squaring ends — 1-1/2″ to 8″ belts.", False),
                ("combo", "Combination grinders and sanders", "Two working ends on one motor: belt and disc, belt and wheel, belt sander and edge beveller.", False),
                ("disc", "Disc sanders", "12″ and 20″ disc sanders for flat sanding, deburring and chamfering weld edges.", False),
                ("bench", "Bench grinders and wire-wheel machines", "Cast-iron bench grinders and wire-wheel deburring and polishing machines.", False),
                ("chamfer", "Chamfering machines and end grinders", "Weld preps and clean edges on plate and parts, and flat end faces on round work.", False),
                ("dust", "Dust collectors", "Collectors for grinding and sanding dust — metal only.", False)],
        faq=[{"q": "Which belt width — 2″, 3″, 4″, 6″ or 8″?",
              "a": "2″ belts (2 × 72″, 2 × 79″) are for knives, tools and detail work; 3″ is the all-round width for deburring and blending in the fabrication shop; 4″ and 6″ belts grind wider parts flat and last longer; 8″ belts are for flat sanding of wide parts and for radius grinding. Most shops start with a 3″ or 6″ pedestal grinder and add a disc sander for flat faces."},
             {"q": "What belt speed for steel, stainless and aluminum?",
              "a": "Around 5,000 – 6,500 ft/min for steel and stainless with zirconia or ceramic belts; slower — 2,500 – 4,000 ft/min — for aluminum, for heat-sensitive parts and for fine finishing. The two-speed and variable-speed grinders (S-150, SDD75, BGM-50, SP-2) cover both."},
             {"q": "Belt grinder or disc sander?",
              "a": "A belt grinder removes metal faster, grinds radii on the contact wheel and runs cooler because the belt is long; a disc sander gives a flat face and an accurate angle against its table — chamfers for welding, squaring ends, deburring flat parts. The combination machines (SP-6, BTM250) put both on one stand."},
             {"q": "Do I need a dust collector for metal grinding?",
              "a": "Grinding dust settles everywhere and is a health and housekeeping problem; a collector at the machine keeps it out of the air. Use a collector made for metal — sparks reach the filter — and never connect the same collector to a woodworking machine: wood dust and hot metal sparks are a fire hazard. The DVS14 and DC650 are metal-only collectors; for heavy production the WD-1800 wet collector is on the deburring machines page."},
             VOLT],
        related=[{"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring and finishing machines"},
                 {"href": "pipe-notcher.html", "label": "Tube notchers and tube end grinders"}, {"href": "corner-grinding-machines.html", "label": "Corner grinders"},
                 {"href": "pipe-sanding-polishing-machines.html", "label": "Pipe sanding and polishing machines"}, {"href": "plate-beveler.html", "label": "Plate bevelers"},
                 {"href": "drill-press.html", "label": "Drill presses"}],
    ),
    D.P_DRILL: dict(
        title="Drill Presses — Gear-Head, Floor & Bench, to 2″ | NovoTech",
        meta="Industrial drill presses: gear-head drill presses 1 – 2″ in steel with power feed and tapping, belt and inverter column drills, variable-speed bench and floor drill presses, vises.",
        h1="Drill presses — gear-head, column, floor and bench drill presses",
        nav="Drill presses",
        intro="A drill press holds the drill square to the work and feeds it with the force and control a hand drill cannot give — the "
              "first machine tool in most fabrication and maintenance shops. NovoTech's value-line drill presses are built in China to our "
              "specification: gear-head drill presses from 1″ to 2″ in steel with eight or twelve speeds, power feed and tapping, inverter "
              "drill presses that keep full torque at low speed, belt-drive and stepless column drills, variable-speed bench and floor drill "
              "presses with a digital speed display, a drilling and tapping press with automatic reverse, and the vises to go with them. "
              "Parts and support from Mississauga, ON, Canada.",
        points=["Gear-head drill presses T-25 – T-50: 1″ to 2″ in steel, 8 – 12 speeds, power feed, tapping to M30",
                "TX530 inverter drill presses with two-range gearbox; TB column drills, belt drive or stepless by frequency converter",
                "WTZ variable-speed bench and floor drill presses, 1/2 – 5/8″; WTZ-16T drilling and tapping with automatic reverse"],
        hero="tm-t50e", minis=["tm-t25", "tm-tbv"],
        groups=[("gear", "Gear-head drill presses", "Speeds through a gearbox — no belts to move — with the torque for large holes and tapping, from 1″ to 2″ in steel.", False),
                ("column", "Column drills — belt drive and inverter", "Industrial column drills with a digital speed display; the V models with stepless speed on single-phase power.", False),
                ("vs", "Variable-speed bench and floor drill presses", "Light drill presses with variable speed for holes to 5/8″, and a drilling and tapping press.", False),
                ("vise", "Drill press vises and welding clamps", "Vises for the drill press and the mill, and angle clamps for welding.", True)],
        faq=[{"q": "Gear-head or belt-drive drill press?",
              "a": "A gear-head drill press changes speed with levers on a gearbox and transmits more torque at low speed — the speeds you need for 1″ and larger holes and for tapping — and it does not slip. A belt-drive drill press is quieter and smoother at high speed for small holes but needs the belts moved to change speed. Inverter (V) machines change speed steplessly from the panel and keep their torque at low speed with a two-range gearbox (TX530)."},
             {"q": "What drilling capacity do I need?",
              "a": "The rated capacity is the largest hole drilled in mild steel in one pass with a twist drill. Choose a machine one size above your largest everyday hole: a 1″ machine for general fabrication, 1-1/4 to 1-9/16″ for structural work and tapping, 2″ for heavy plates and flanges. Larger holes are faster and safer with an annular cutter on a magnetic drill or on the drill press."},
             {"q": "Which drill presses tap?",
              "a": "The WTZ-16T taps M12 with automatic reverse; the TX530 range taps 3/4 – 1″ with forward and reverse; the T-50 and T-50E tap M30 in steel; tapping is an option on most T-25, T-26, T-28 and T-30 models. Tapping needs a reversing spindle and low speed — tell us the largest tap and the material."},
             {"q": "Single-phase or 3-phase?",
              "a": "The WTZ bench and floor drill presses and the TB…V inverter column drills run on single-phase power; the gear-head drill presses have 3-phase two-speed motors, supplied for 600 V with a CSA-approved panel or for 208 / 240 / 480 V on request."},
             VOLT],
        related=[{"href": "milling-machine.html", "label": "Milling machines"}, {"href": "cnc-machine-tools.html", "label": "CNC lathes, machining centres and grinders"},
                 {"href": "belt-grinder.html", "label": "Belt grinders and sanders"}, {"href": "band-saw.html", "label": "Band saws"},
                 {"href": "ironworker-machines.html", "label": "Ironworkers"}, {"href": "hydraulic-press.html", "label": "Hydraulic presses and shop presses"}],
    ),
    D.P_MILL: dict(
        title="Milling Machines — Turret, Universal & Mill-Drills | NovoTech",
        meta="Milling machines: turret mills with horizontal spindle, universal and ISO50 mills, drill-mills, keyseaters and a cylinder head resurfacing machine.",
        h1="Milling machines — turret, universal and drilling-milling machines",
        nav="Milling machines",
        intro="Milling machines cut flat faces, slots, steps, pockets and keyways with rotating cutters while the table moves the work under "
              "them. NovoTech's value-line milling machines are built in China to our specification: knee-type turret mills with a "
              "horizontal spindle as well as the vertical head, universal mills with a head that swivels through 360°, heavy ISO50 universal "
              "mills with power feed and rapid traverse on all axes and tables up to 79″, drilling-milling machines that drill 2″, a mini "
              "mill-drill and a radial drill-mill, a keyseater and a slotting machine for keyways and splines, and the KSM-850 resurfacing "
              "machine for cylinder heads and blocks. Parts and support from Mississauga, ON, Canada.",
        points=["Turret mills X6325W – X6336WA: vertical head to 7,200 rpm, horizontal spindle, power feed, tables to 64 × 14″",
                "Universal mills XQ6226, X6436 and heavy ISO50 LM-1450 / X5750 with tables to 79″ and servo feeds",
                "ZX drilling-milling machines for 2″ drilling; TX-20 and DM-20; B5012 keyseater and B5013 slotter; KSM-850 head resurfacer"],
        hero="tm-x6332", minis=["tm-lm1450", "tm-zx5325"],
        groups=[("turret", "Turret milling machines", "Knee-type mills with a turret head — the tool-room machine — and on the W models a horizontal spindle too.", False),
                ("univ", "Universal milling machines", "Horizontal and vertical milling on one machine, with a head that swivels through 360°.", False),
                ("drill", "Drilling-milling machines and mini mills", "Mill-drills for the job shop and the repair shop: 2″ drilling and face milling on one column.", False),
                ("slot", "Keyseaters and slotting machines", "Keyways and splines in hubs, gears and pulleys.", False),
                ("resurf", "Cylinder head resurfacing machine", "Flat, smooth gasket faces on cylinder heads and engine blocks for the engine rebuilder.", False)],
        faq=[{"q": "Turret mill, universal mill or drill-mill?",
              "a": "A turret (Bridgeport-type) mill has a vertical head that tilts and a knee that moves the table up and down — the most flexible machine for one-off parts, slots and pockets. A universal mill adds a horizontal spindle and arbor for side and slab milling and gang cutters, and swivels its head through 360°. A drill-mill drills and mills on one column without a knee: the lower-cost choice when most of the work is drilling with some face milling."},
             {"q": "What do ISO40 and ISO50 mean?",
              "a": "They are the sizes of the spindle taper that holds the tool holder: ISO40 (NT40, the same size as CAT40 and BT40) for general milling, ISO50 for heavier cuts and larger face mills. R8 and MT tapers are found on small mills. Tell us what tooling you already have — adapters are available."},
             {"q": "Power feed and DRO?",
              "a": "Power feed moves the table at a steady rate for a better finish and less operator fatigue; a digital readout (DRO) shows the table position to 0.0002″ and replaces the dials for most work. The X6336 and LM-1450 have power feed on all three axes, the X6336 with rapid traverse and a three-axis DRO; DROs are available on most models — ask us when you quote."},
             {"q": "What does a cylinder head resurfacing machine do?",
              "a": "It mills the gasket face of a cylinder head or an engine block flat and smooth again after warping or corrosion, so the new head gasket seals. The KSM-850 feeds the part under a Ø13″ cutter head with CBN inserts for cast iron and PCD for aluminum, with variable head speed and table feed for the finish the gasket needs, on heads and blocks up to 33.5″ long."},
             VOLT],
        related=[{"href": "drill-press.html", "label": "Drill presses"}, {"href": "cnc-machine-tools.html", "label": "CNC lathes, machining centres and grinders"},
                 {"href": "belt-grinder.html", "label": "Belt grinders and sanders"}, {"href": "band-saw.html", "label": "Band saws"}],
    ),
    D.P_CNC: dict(
        title="NovoTech CNC Lathes, VMCs & Boring Mills · Value Line | NovoTech",
        meta="NovoTech value-line CNC machine tools: a slant-bed CNC lathe, BT40 vertical machining centres with 16 – 24 tool changers, BT50 CNC boring and milling machines and a horizontal machining centre.",
        h1="NovoTech CNC machine tools — CNC lathe, vertical machining centres and CNC boring mills, the value line",
        nav="NovoTech CNC machine tools",
        intro="CNC machine tools for the job shop and the production line, built in China to NovoTech's specification with Mitsubishi, Fanuc "
              "or Siemens controls to order: the CTK6416 slant-bed CNC lathe with gang tooling, the VMC8046 and VMC10562 vertical machining "
              "centres with BT40 spindles to 8,000 rpm and 16- and 24-tool changers, CNC boring and milling machines with BT50 spindles and "
              "rotary B axes for large prismatic parts, the TH-800 horizontal machining centre with a 40-tool magazine, and slot machining "
              "centres for quartz and glass. Installed, programmed with you and supported from Mississauga, ON, Canada.",
        points=["VMC8046 and VMC10562 vertical machining centres: 39.4 × 21.7″ table, BT40, 8,000 rpm, 16 / 24 tools",
                "TXK68 – TXK160D CNC boring and milling machines and TH-800 horizontal machining centre, BT50, 4-axis",
                "CTK6416 slant-bed CNC lathe with gang tooling; CNC100 / CNC120 slot machining centres"],
        hero="tm-vmc10562", minis=["tm-th800", "tm-ctk6416"],
        groups=[("vmc", "Vertical machining centres", "Three-axis CNC milling, drilling and tapping with an automatic tool changer.", False),
                ("boring", "CNC boring and milling machines", "Large parts machined on several faces in one set-up, with a rotary B axis.", False),
                ("lathe", "CNC lathe", "A compact slant-bed lathe for small turned parts in series.", False)],
        faq=[{"q": "Which CNC control do the machines have?",
              "a": "Mitsubishi or Fanuc on every machine, Siemens on the machining centres — chosen when you order. All three are supported in North America, with programmers and spare parts available locally; we recommend the control your programmers already know."},
             {"q": "BT40 or BT50?",
              "a": "BT40 spindles (the same size as CAT40) are the standard for vertical machining centres up to about 15 HP — fast tool changes and a wide choice of holders. BT50 spindles carry larger face mills and boring bars and take heavier cuts: the boring and milling machines have them."},
             {"q": "Do you install and train?",
              "a": "Yes — NovoTech delivers, levels and commissions the machine, checks the geometry, and trains your operator on the control; we help with the first programs and the post-processor for your CAM software. Ask us for the foundation drawing and the power requirements before the machine ships."},
             VOLT],
        related=[{"href": "milling-machine.html", "label": "Milling machines"}, {"href": "drill-press.html", "label": "Drill presses"},
                 {"href": "laser-cutting-machine.html", "label": "Fiber laser cutting machines"}, {"href": "cnc-plasma-table.html", "label": "CNC plasma tables"}],
    ),
    D.P_PLASMA: dict(
        title="CNC Plasma Tables & Plasma Pipe Cutting Machines | NovoTech",
        meta="CNC plasma tables 2 × 2 ft to 5 × 10 ft with servo drives and torch height control, compact plasma tables with USB control and CNC plasma pipe cutters for Ø2 – 11-3/4″ pipe.",
        h1="CNC plasma tables and CNC plasma pipe cutting machines",
        nav="CNC plasma tables",
        intro="A CNC plasma table cuts steel, stainless and aluminum plate to any shape from a drawing — brackets, gussets, base plates, signs "
              "and art — at a fraction of the price of a laser, and cuts thicker plate than a small laser. NovoTech's value-line plasma "
              "machines are built in China to our specification: industrial 4 × 4 and 5 × 10 ft tables with servo drives, automatic torch "
              "height control and water or downdraft tables, compact 2 × 2 and 2 × 4 ft tables that run from a USB stick, and CNC plasma pipe "
              "cutters that cope and saddle pipe from Ø2 to 11-3/4″. Supplied with the plasma source or ready for a Hypertherm; installed and "
              "supported from Mississauga, ON, Canada.",
        points=["PC 4×4 and 5×10 CNC plasma tables: servo drives, torch height control, plate to 1″ on the table, cuts to 1/2″ with 85 A",
                "PC 2×2 and 2×4 compact plasma tables with stepper drives and USB hand-held control",
                "PCP CNC plasma pipe cutters for pipe Ø2 – 11-3/4″, 10 and 20 ft"],
        hero="tm-pc510", minis=["tm-pcp3000e", "tm-pc24"],
        groups=[("table", "CNC plasma tables", "Cut plate to shape from a drawing — 2 × 2 ft to 5 × 10 ft.", False),
                ("pipe", "CNC plasma pipe cutting machines", "Copes, saddles, holes and cut-offs in round pipe.", False)],
        faq=[{"q": "Plasma or fiber laser?",
              "a": "A plasma table costs much less, cuts thicker plate for the money and is simple to run; its cut is wider with a slight bevel and some dross, which is fine for structural, agricultural and repair work. A fiber laser cuts thin and medium sheet faster with a narrow, square, clean edge and small holes — the choice for sheet-metal parts and enclosures. See the fiber laser cutting machines page for the laser line-up."},
             {"q": "How thick does it cut?",
              "a": "The plasma source sets the thickness, not the table: a 45 A source cuts about 5/16″ cleanly, 65 A 3/8″, 85 A 1/2″, 100 A 1″ (severance). The 4×4 and 5×10 tables carry plate up to 1″ thick. Tell us your usual and thickest plate and we will match the source."},
             {"q": "Water table or downdraft table?",
              "a": "A water table catches the sparks and most of the fumes in water under the plate — simple and quiet; a downdraft table draws the fumes down through the slats into a dust collector and keeps the plate dry. The 4×4 table cuts over water pans, the 5×10 has downdraft collection."},
             VOLT],
        related=[{"href": "laser-cutting-machine.html", "label": "Fiber laser cutting machines"}, {"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutting machines"},
                 {"href": "plate-beveler.html", "label": "Plate bevelers"}, {"href": "shear-cutting.html", "label": "Metal shears"},
                 {"href": "belt-grinder.html", "label": "Belt grinders and sanders"}],
    ),
    D.P_SHAPE: dict(
        title="Power Hammers & Planishing Hammers for Metal | NovoTech",
        meta="Pneumatic planishing hammers with 12 – 24″ throats, electric power hammers to 1,700 blows/min, a diamond roller former and C41 air forging hammers, 35 – 165 lb ram.",
        h1="Power hammers and planishing hammers — pneumatic, electric and air forging hammers",
        nav="Power & planishing hammers",
        intro="Hammers for the metal shaper and the blacksmith. Auto body, hot-rod, motorcycle and aircraft panel builders smooth and "
              "shape sheet with a planishing hammer — fast, light blows between an upper die and a crowned lower anvil — and with an "
              "electric power hammer that has the force to shape, bead and shrink as well; blacksmiths and forges draw out, upset, punch "
              "and forge-weld hot stock under a self-contained air hammer that needs no compressor. NovoTech's value-line hammers are "
              "built in China to our specification: PPH pneumatic planishing hammers with 12″ and 24″ throats, the UFP-2 planishing hammer "
              "and wheel on one stand, the PH-20D and PH-30D electric power hammers with 20″ and 30″ throats, the PIC50 diamond roller "
              "former for embossed panels and the C41 air forging hammers from 35 to 165 lb ram. Parts and support from Mississauga, ON, Canada.",
        points=["Pneumatic planishing hammers PPH-12 / PPH-24 / PPH500 / PPH-610: 18 – 16 ga, 12 – 24″ throats, radius anvils",
                "PH-20D and PH-30D electric power hammers: 2 HP, 0 – 1,700 blows/min, 16 ga steel and 12 ga aluminum",
                "C41 self-contained air forging hammers, 35 – 165 lb ram, 210 – 270 blows/min; PIC50 diamond roller former, 20 ga × 50″"],
        hero="tm-ph20d", minis=["tm-pph610", "tm-c41-40"],
        groups=[("hammer", "Planishing hammers and power hammers", "Smoothing, shaping and beading panels with fast, light blows — on shop air or with an electric drive.", False),
                ("former", "Diamond roller former", "A motorized roller that embosses a diamond pattern into sheet for decorative panels.", False),
                ("forge", "Air forging hammers", "Self-contained pneumatic hammers for blacksmiths and forges.", False)],
        faq=[{"q": "Planishing hammer or power hammer?",
              "a": "A pneumatic planishing hammer (PPH) runs on shop air and delivers fast, light blows that smooth a panel and take out the marks of earlier shaping — the finishing tool of the auto body and restoration shop. An electric power hammer (PH-20D / PH-30D) has variable speed and more force: it shapes as well as planishes, and with shaping dies it shrinks, stretches and beads. Many shops have both."},
             {"q": "Which throat depth do I need?",
              "a": "The throat is the distance from the dies to the frame — it limits how far into a panel you can reach. A 12″ throat suits brackets, patch panels and motorcycle parts; 20 – 24″ most car panels; the 30″ throat of the PH-30D reaches the middle of hoods, roofs and large aircraft and boat skins."},
             {"q": "What does a planishing hammer need from the compressor?",
              "a": "The PPH500 runs at 50 – 100 psi and the PPH-610 at 90 – 120 psi; the foot pedal or the 3-position air flow valve sets the blow rate. Use clean, dry air — a filter, regulator and lubricator at the hammer keep the valve and the piston working."},
             {"q": "Does an air forging hammer need shop air?",
              "a": "No — the C41 hammers are self-contained: a 2 – 9.4 HP motor drives a compressor cylinder in the hammer itself, and that air drives the ram. They stand on a solid concrete foundation — the larger hammers on a separate anvil block of 441 to 1,874 lb — and forge stock heated in a forge. Choose the ram by the largest stock: the 35 – 55 lb rams for blades, tools and ornamental work up to about 1-1/2″ square, the 88 and 165 lb rams for 2 – 2-1/2″ square bar."},
             VOLT],
        related=[{"href": "bead-rollers.html", "label": "Bead rollers"}, {"href": "folder-sheet-metal-brake.html", "label": "Sheet metal brakes"},
                 {"href": "angle-rolls.html", "label": "Angle rolls and ring rollers"}, {"href": "tube-bender.html", "label": "Tube and pipe benders"},
                 {"href": "belt-grinder.html", "label": "Belt grinders"}],
    ),
    D.P_TUBE: dict(
        title="Tube & Pipe Benders — Hydraulic & Electric | NovoTech",
        meta="Tube and pipe benders: hydraulic PLC tube benders to 3-1/8″, an electric top bender to 2-1/2″, a 25-ton tubing bender, air and electric benders for 2″ schedule 40 pipe, exhaust benders and an electric pipe bender.",
        h1="Tube and pipe benders — hydraulic, electric and air-hydraulic, value line",
        nav="Tube & pipe benders · value line",
        intro="Benders for the fabrication shop, the roll-cage and chassis builder, the exhaust shop and the plumber and electrician — lower in "
              "price than the CNC and NC rotary-draw benders on the other pages of this section, for the shop that bends tube and pipe every "
              "week but does not need mandrel bending or programmed 3-D parts. NovoTech's value-line benders are built in China to our "
              "specification: JTB hydraulic PLC tube benders to 3-1/8″, the TBM-60 electric top bender to 2-1/2″, the HTB-25T 25-ton tubing "
              "bender, the air- and electric-hydraulic TB-3 benders and the HTB-1000 for 2″ schedule 40 pipe, the HTB-2000 exhaust bender "
              "with swager and expander and the EHB-10 electric hydraulic pipe bender. Dies, parts and support from Mississauga, ON, Canada.",
        points=["JTB-40 / 50 / 80 hydraulic PLC tube benders: round tube to Ø3-1/8″, square tube to 3-1/8″, bending to 180°",
                "TBM-60 electric top bender 1/4 – 2-1/2″; HTB-25T 25-ton tubing bender; TB-3 and HTB-1000 for 2″ schedule 40 pipe",
                "HTB-2000 exhaust bender and HTES-3000 expander-swager; EHB-10 electric hydraulic pipe bender, 11 US tons, 1/2 – 2″ pipe"],
        hero="tm-jtb50", minis=["tm-tbm60", "tm-htb1000"],
        groups=[("power", "Hydraulic and electric tube benders", "Powered benders for tube, pipe, square tube and bar — from the PLC bender to the 25-ton tubing bender.", False),
                ("pipe", "Electric hydraulic pipe bender", "A push-type bender with an electric pump for plumbing, electrical and maintenance pipe work.", False)],
        faq=[{"q": "Rotary-draw, push-type or roll bending?",
              "a": "A rotary-draw bender (JTB, TBM-60, HTB-25T, TB-3, HTB-1000) pulls the tube around a die with a clamp and a follower — a tight, accurate bend with little flattening, the method for roll cages, railings, frames and exhaust. A push-type hydraulic pipe bender (EHB-10) pushes the pipe into a die between two supports — simple and fast for plumbing and electrical pipe, where some ovality is acceptable. For large radii, rings and spirals, see the tube rollers on the angle rolls page."},
             {"q": "What do I need to tell you to choose the dies?",
              "a": "The outside diameter (or the square size), the wall thickness, the material and the centre-line radius (CLR) of the bend — usually 2 to 4 times the tube diameter. Tube and pipe sizes differ: 1-1/2″ schedule 40 pipe is 1.900″ OD, while 1-1/2″ tube is 1.500″ OD — the die must fit the OD exactly."},
             {"q": "When do I need a CNC or mandrel bender instead?",
              "a": "When the wall is thin for its diameter (thin-wall stainless, aluminum, exhaust tube on tight radii) a mandrel inside the tube prevents wrinkling and flattening; when parts have several bends in different planes, a CNC bender positions length and rotation automatically. The ISITAN CNC and NC tube benders on the other pages of this section do both."},
             VOLT],
        crumb={"label": "Pipe & tube benders", "href": "pipe-benders.html"},
        related=[{"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "angle-rolls.html", "label": "Angle rolls, tube rollers and ring rollers"},
                 {"href": "tube-end-forming-machines.html", "label": "Tube end forming machines"}, {"href": "horizontal-press-brake.html", "label": "Horizontal benders"}],
    ),
    D.P_WOOD: dict(
        # keyword research (Ubersuggest, Canada, Oct 2026): "woodworking machinery" 320/mo, CPC $1.47; "woodworking machines" 320/mo, CPC $1.08
        title="Woodworking Machinery — Planers, Jointers & Saws | NovoTech",
        meta="Woodworking machines in Canada: jointers, thickness planers, jointer-planers, 10″ table saws, band saws, multifunction machines, mortisers and a lathe.",
        h1="Woodworking machinery — jointers, planers, table saws, band saws and multifunction machines",
        nav="Woodworking machinery",
        intro="Woodworking machines for the cabinet shop, the joinery, the school shop and the serious home workshop. NovoTech's value-line "
              "woodworking machinery is built in China to our specification: multifunction machines that plane, saw, mortise and drill on "
              "one motor; 6″ and 8″ jointers and 15″ and 20″ thickness planers with spiral carbide cutterheads, and jointer-planers to 16″; "
              "10″ cabinet table saws with 30″ and 52″ of rip, with touch-screen blade height and angle on the S models; 14″ and 18″ band "
              "saws for resawing; hollow-chisel mortisers, slot boring and horizontal boring machines; a 12 × 16″ wood lathe; a belt and "
              "disc sander and a dust collector — {n} models, with parts and support from Mississauga, ON, Canada.",
        points=["Jointers 6 – 8″ and thickness planers 15 – 20″ with spiral carbide cutterheads; jointer-planers 10 – 16″",
                "WTS10 10″ cabinet table saws, 30″ and 52″ rip, touch-screen S models; TBS 14″ and 18″ band saws",
                "WM multifunction machines, MS mortisers, MGX slot boring machines, TL-406 lathe, DC900 dust collector"],
        hero="tm-tdm320", minis=["tm-wts1050", "tm-tbs457"],
        groups=[("planing", "Jointers, thickness planers and jointer-planers", "Flat, square and to thickness: the machines that turn rough lumber into stock.", False),
                ("sawing", "Table saws and band saws", "Rip and crosscut on the table saw, resaw and cut curves on the band saw.", False),
                ("combo", "Multifunction woodworking machines", "Planer, table saw, mortiser and drill on one motor — for the shop with room for one machine.", False),
                ("boring", "Mortisers and boring machines", "Mortises, slots and dowel holes for joinery, doors and furniture.", False),
                ("turning", "Wood lathe", "Bowls, spindles, pens and furniture parts.", False),
                ("finish", "Sander and dust collector", "Sand small parts and edges, and keep the chips and dust off the floor and out of the air.", False)],
        faq=[{"q": "Jointer, thickness planer or jointer-planer — what do I need?",
              "a": "A jointer flattens one face of a rough board and squares an edge to it; a thickness planer then makes the other face parallel and brings the board to thickness. You need both to mill rough lumber. A jointer-planer (TDM) does both jobs with one cutterblock in the space of one machine — the tables lift for thicknessing — at the cost of a changeover between the two; separate machines are faster when both run all day."},
             {"q": "Spiral carbide cutterhead or straight knives?",
              "a": "A spiral (helical) cutterhead has many small carbide inserts set in a spiral: it cuts with a shearing action, so it is quieter, leaves a cleaner surface on figured and interlocked grain and tears out less, and a chipped insert is turned to a fresh edge in a minute instead of a set of knives reground and reset. Straight knives cost less to buy and are fine for softwood and general work. The WJ jointers and WJP planers have spiral carbide heads; the WJ10X40 and the multifunction machines have straight knives."},
             {"q": "Which table saw — 30″ or 52″ rip, hand wheels or touch screen?",
              "a": "The rip capacity is the widest cut to the right of the blade: 30″ is enough for solid wood and for cutting a sheet of plywood to 30″ parts; 52″ cuts a 4 × 8 sheet to any width, which a cabinet shop needs. All WTS10 saws take a 10″ blade with 3-3/8″ of cut at 90°; on the S models the blade height and angle are typed on a touch screen and shown digitally — faster and repeatable set-ups for production."},
             {"q": "Do I need a dust collector?",
              "a": "Yes for every planer, jointer and table saw: they make chips faster than a shop vacuum can take them, and fine dust is a health risk. A single-stage collector like the DC900 — 940 CFM, two 4″ inlets — serves one or two machines at a time; keep the hose runs short and connect the machine that is running."},
             VOLT],
        related=[{"href": "drill-press.html", "label": "Drill presses"}, {"href": "belt-grinder.html", "label": "Belt grinders and sanders"},
                 {"href": "vertical-band-saws.html", "label": "Vertical band saws"}, {"href": "aluminum-and-pvc-upcut-saws.html", "label": "Aluminum & PVC saws"}],
    ),
}

# ---------------------------------------------------------------------------------------------------------------- groups on existing pages
# groups: (group id, title, lead, manual?, after group id or None)
VL = "NovoTech value line"
EXTRA = {
    D2.P_COLD: dict(
        groups=[("tt-cold", "Cold saws · value line", "NovoTech's value-line cold saws, built in China: manual gear-driven cold saws with 9 – 14″ blades, a semi-automatic hydraulic saw and a 16″ heavy-duty saw.", False, None),
                ("tt-abrasive", "Abrasive cut-off saws · value line", "Fast square and miter cuts in steel tube, pipe and profiles with 12 – 16″ abrasive wheels.", False, None),
                ("tt-stands", "Roller stands, roller conveyors and roller tables", "Material support for every saw, shear and brake — stands with side rollers, a conveyor with a digital length stop and a measuring roller table.", True, None)],
        intro_add="NovoTech's value-line cold saws, built in China, add gear-driven manual saws with 9 – 14″ blades, a semi-automatic hydraulic "
                  "saw, a 16″ heavy-duty saw and abrasive cut-off saws, plus roller stands, a roller conveyor with a digital length stop and a "
                  "measuring roller table.",
        points_add=["NovoTech value line: CS cold saws 9 – 14″, PDS-315H semi-automatic hydraulic, PDS-400 heavy-duty 16″, TV abrasive saws 12 – 16″"],
        faq_add=[{"q": "Cold saw or abrasive cut-off saw?",
                  "a": "A cold saw cuts with a toothed HSS or carbide blade at low speed: a square, burr-free cut that is ready to weld, no sparks and no heat in the part, but the blade must suit the material. An abrasive saw grinds through with a 12 – 16″ wheel at high speed: a lower price, any steel including hardened, but a hot part, sparks, a burr and wheels that wear quickly. For production cutting of tube and profiles choose a cold saw; for occasional cutting of mixed steel the abrasive saw."}],
        related_add=[{"href": "band-saw.html", "label": "Band saws"}, {"href": "belt-grinder.html", "label": "Belt grinders and sanders"}],
        set={"hero_brand_line": "ISITAN circular cold saws are made in Turkey by ISITAN Makine, the CT325 in Taiwan by CSM and the automatic BMDO saws by Bekamak Makina, Turkey; NovoTech's value-line cold saws are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech."},
    ),
    D2.P_ALU: dict(
        groups=[("tt-alu", "Aluminum cut-off saws · value line", "16″ and 20″ pneumatic-clamping saws for aluminum profiles — NovoTech value line, built in China.", False, None)],
        intro_add="For the shop that cuts aluminum profiles now and then, the NovoTech value-line QCS-400 is a 16″ saw with pneumatic clamping "
                  "and feed, and the QCS-500A a 20″ saw whose head swivels from 0 to 180° for profiles up to 10-1/4 × 5-1/8″.",
        related_add=[{"href": "circular-cold-saws.html", "label": "Cold saws"}],
    ),
    D2.P_CORNER: dict(
        groups=[("tt-notch", "Corner notchers · value line", "Hydraulic and pneumatic corner notchers — NovoTech value line, built in China.", False, None)],
        intro_add="NovoTech's value-line notchers, built in China, add the HNM-6 and HNM-6A hydraulic notchers for 1/4″ and the PNM-130 and "
                  "PNM-150 pneumatic notchers for sheet to 1/8″.",
        points_add=["NovoTech value line: HNM-6 / HNM-6A hydraulic 1/4″, PNM-130 / PNM-150 pneumatic"],
        faq_add=[{"q": "Hydraulic or pneumatic notcher?",
                  "a": "A hydraulic notcher cuts 3/16 – 1/4″ plate quickly and is the choice for a production shop or for heavier plate; a pneumatic notcher runs on shop air and cuts up to 1/8″ in sheet — quieter, no hydraulic oil, a lower price. The premium-line HNM notchers and the value-line HNM-6 / HNM-6A differ in build and price; both have adjustable stops and a sheet hold-down."}],
        set={"hero_brand_line": "Premium-line corner notchers are built in Turkey to NovoTech's specification with European hydraulic and electrical components; the value-line notchers are built in China to NovoTech's specification. All sold with a 1-year warranty and supported from Mississauga, ON, Canada."},
    ),
    D2.P_PIPE_NOTCH: dict(
        groups=[("tt-tube-notch", "Tube and pipe notchers · value line", "Motorized hole-saw and end-mill notchers — NovoTech value line, built in China.", False, None),
                ("tt-prs", "Tube end grinders · value line", "Belt grinders that notch tube ends at any angle with a contact roller the size of the mating tube.", False, None)],
        intro_add="NovoTech's value-line notchers, built in China, add the motorized PTN-30 hole-saw notcher, the UTN40 end-mill notchers, "
                  "the PTN-12U and the PRS tube end grinders that notch tube from Ø3/4 to 5-3/4″ with a belt.",
        points_add=["NovoTech value line: PTN-30 hole-saw notcher, UTN40 end-mill notchers, PRS belt tube-end grinders to Ø5-3/4″"],
        faq_add=[{"q": "Hole saw, end mill or belt — which notching method?",
                  "a": "A hole-saw notcher (PTN-30) is the lowest-cost way to cut a saddle: one inexpensive bi-metal hole saw per tube size, any angle, clean enough for most welding. An end-mill notcher (UTN40) cuts faster and more precisely, without coolant, and one cutter covers several sizes. A belt notcher (PRS) grinds the saddle against a contact roller: no burr, no sharp tooling, works on thin-wall stainless and aluminum and also finishes and deburrs. The premium-line PN machines are motorized notchers for production."}],
        related_add=[{"href": "tube-bender.html", "label": "Tube and pipe benders · value line"}, {"href": "belt-grinder.html", "label": "Belt grinders"}],
        set={"hero_brand_line": "ISITAN machines are made in Turkey by ISITAN Makine — sheet-metal forming machinery since 1959, with European components; NovoTech's value-line notchers are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech."},
    ),
    D2.P_IRON: dict(
        groups=[("tt-iron", "Compact ironworkers · value line", "Single-cylinder 50 – 60 ton ironworkers for the small shop — NovoTech value line, built in China.", False, "iron-value-group")],
        intro_add="The value line also has the compact M50, M55 and M60 ironworkers — 50 to 60 tons on one cylinder.",
        points_add=["NovoTech value line: M50 – M60 compact ironworkers, 50 – 60 tons"],
    ),
    D2.P_ANGLE: dict(
        groups=[("tt-ring", "Ring rollers, profile benders and tube rollers · value line", "Motorized profile benders with Ø13/16 to 2-1/2″ shafts, ring rollers and tube rollers — NovoTech value line, built in China.", False, None)],
        intro_add="NovoTech's value-line ring rollers, built in China, add motorized RBM and HRBM profile benders with Ø13/16 to 2-1/2″ "
                  "shafts — the H models with a hydraulic top roll — the ETR-50 electric tube roller and the CRB-76 decorative ring roller.",
        points_add=["NovoTech value line: RBM / HRBM motorized profile benders Ø13/16 – 2-1/2″ shafts, ETR-50 tube roller, CRB-76 decorative roller"],
        faq_add=[{"q": "Premium-line angle roll or value-line ring roller?",
                  "a": "The premium-line PK and HPK angle rolls are built in Turkey for daily structural work — heavier frames, larger shafts, NC options and capacities to 6″ angle. The value-line RBM and HRBM ring rollers are lighter and lower in price for the fabrication, railing and ornamental shop: flat bar, angle, channel, tee and tube to 4-3/4 × 1″ flat on the HRBM65, with one combination roll set for every profile."}],
        set={"hero_brand_line": "Premium-line angle rolls are built in Turkey to NovoTech's specification with European hydraulic and electrical components; the value-line ring rollers and tube rollers are built in China to NovoTech's specification. All sold with a 1-year warranty and supported from Mississauga, ON, Canada."},
    ),
    D2.P_BEAD: dict(
        groups=[("tt-bead", "Beading machines and bead rollers · value line", "Motorized beading machines to 8 ga and motorized deep-throat bead rollers to 42″ — NovoTech value line, built in China.", False, None)],
        intro_add="NovoTech's value-line bead rollers, built in China, add ETB beading machines to 8 ga and RM24 – RM42 deep-throat bead "
                  "rollers with variable-speed drive for auto body panels.",
        points_add=["NovoTech value line: ETB beading machines 18 – 8 ga, RM24 / 36 / 42 motorized deep-throat bead rollers"],
        faq_add=[{"q": "Which throat depth for auto body panels?",
                  "a": "The throat is how far from the edge of the panel the bead can go: 24″ reaches the centre of a 48″ panel, 36″ and 42″ reach into floor pans, hoods and truck beds. The RM-H models also have a 4″ high throat so formed panels clear the frame. For duct, ends of tanks and edge beads, the 8 – 12″ throat of the ETB beading machines is enough."}],
        related_add=[{"href": "power-hammer.html", "label": "Power and planishing hammers"}, {"href": "lock-former.html", "label": "Lock formers and HVAC machines"}],
        set={"hero_brand_line": "ISITAN machines are made in Turkey by ISITAN Makine — sheet-metal forming machinery since 1959, with European components; NovoTech's value-line bead rollers are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech."},
    ),
    D2.P_PRESS: dict(
        groups=[("tt-shop", "Shop presses · value line", "Motorized workshop presses from 28 to 176 US tons and a hydraulic bench press for sheet-metal tooling — NovoTech value line, built in China.", False, None),
                ("tt-hp", "Hydraulic presses · value line", "Motorized H-frame, brake, sliding-table, C-frame and four-column presses from 22 to 551 US tons — NovoTech value line, built in China.", False, None),
                ("tt-rivet", "Orbital riveting machines · value line", "Hydraulic orbital riveters that roll solid rivets from 3/16 to 1-3/16″ — NovoTech value line, built in China.", False, None)],
        intro_add="NovoTech's value-line presses, built in China, add motorized workshop presses from 28 to 176 US tons, the EBP-10T hydraulic "
                  "bench press, motorized H-frame presses to 551 US tons, presses with a brake function, sliding-table, C-frame and four-column "
                  "presses — the HP-F1/PLC with a PLC touch screen — and XM orbital riveting machines.",
        points_add=["NovoTech value line: workshop presses 28 – 176 US tons, H-frame presses 33 – 551 US tons, brake, sliding-table, C-frame and four-column presses, orbital riveters"],
        faq_add=[{"q": "Premium-line or value-line press?",
                  "a": "The premium-line shop and production presses are built in Turkey with European hydraulics and Siemens controls, for daily production work, straightening lines and custom sizes. The value-line presses are built in China for the repair shop, the maintenance department and lighter production — the same tonnages at a lower price, with built-on or separate power units."}],
        related_add=[{"href": "lock-former.html", "label": "Lock formers and HVAC machines"}],
        set={"hero_brand_line": "Premium-line shop presses are built in Turkey for NovoTech's premium line; the NovoTech premium-line production presses are built in Turkey with European components; the value-line presses are built in China — all to NovoTech's specification and sold, installed and supported in Canada by NovoTech."},
    ),
    D2.P_CIRCLE: dict(
        groups=[("tt-circle", "Circle shears · value line", "Motorized circle shears, one with flanging rolls — NovoTech value line, built in China.", False, None)],
        intro_add="NovoTech's value-line circle shears, built in China, add the MCS-1250E motorized circle shear for discs to Ø49″ in 10 ga and "
                  "the ECS10/10 motorized circle shear with flanging rolls.",
        points_add=["NovoTech value line: MCS-1250E motorized circle shear Ø8 – 49″, ECS10/10 circle shear with flanging"],
    ),
    D2.P_COMPACT: dict(     # the compact page's own intro (tools/press_brake_types.py) already introduces the HBV brakes
        groups=[("tt-hbv", "Hydraulic bending brakes · value line", "Small hydraulic brakes for plate to 3/16″, with a four-way V-block or two cylinders — NovoTech value line, built in China.", False, None)],
    ),
    D2.P_HORIZ: dict(
        groups=[("tt-horiz", "Hydraulic horizontal benders · value line", "Horizontal benders for flat bar from 11 to 44 US tons — NovoTech value line, built in China.", False, None)],
        intro_add="NovoTech's value-line HB-10T, HB-25T and HB-40T hydraulic benders, built in China, bend flat bar to 6-1/4 × 1/2″.",
        points_add=["NovoTech value line: HB-10T / 25T / 40T hydraulic horizontal benders, 11 – 44 US tons"],
        related_add=[{"href": "tube-bender.html", "label": "Tube and pipe benders · value line"}],
        set={"hero_brand_line": "The HP horizontal presses are built in Turkey for NovoTech's premium line, with European hydraulics and controls; NovoTech's value-line benders are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech."},
    ),
    D2.P_ROLL: dict(
        groups=[("tt-slip", "Slip rolls · value line", "Hydraulic and electric slip rolls for sheet to 1/2″ — NovoTech value line, built in China.", False, None)],
        intro_add="For sheet and light plate, NovoTech's value-line slip rolls, built in China, roll 22 ga to 1/2″: HER hydraulic slip rolls with "
                  "all three rolls driven and ESR electric slip rolls with cone rolling for the HVAC and sheet-metal shop.",
        points_add=["NovoTech value line: HER hydraulic slip rolls to 1/2″, ESR electric slip rolls 22 ga – 1/4″"],
        faq_add=[{"q": "Plate roller or slip roll?",
                  "a": "A slip roll is a light three-roll machine for sheet — duct, flues, tanks, hoppers, signage — in 22 ga to 1/4″, with a top roll that swings out to slip the finished cylinder off. A plate roller rolls heavier plate and pre-bends the edges so the cylinder closes round. The HER hydraulic slip rolls bridge the two, to 1/2″ over 6′7″."}],
        set={"hero_brand_line": "ISITAN machines are made in Turkey by ISITAN Makine — sheet-metal forming machinery since 1959, with European components; NovoTech's value-line slip rolls are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech."},
    ),
    D2.P_DEBURR: dict(
        groups=[("tt-bfm", "Wide-belt deburring machines · value line", "Entry-level wide-belt deburring and finishing machines, 12″ and 24″ — NovoTech value line, built in China.", False, None)],
        intro_add="For the shop that starts deburring by machine, the NovoTech value-line MGM-300 (12″) and BFM-2560 (24″, with a wet dust "
                  "collector) are wide-belt machines for laser-cut and punched parts.",
        related_add=[{"href": "belt-grinder.html", "label": "Belt grinders and sanders"}],
    ),
    D2.P_WELD: dict(
        groups=[("tt-wp-small", "Benchtop and chuck positioners · value line", "Positioners for tube, pipe and small parts from 33 to 247 lb, with chucks, hollow bores and foot pedals — NovoTech value line, built in China.", False, None),
                ("tt-wp-big", "Tilting and heavy welding positioners · value line", "Turntable positioners from 485 to 8,818 lb with tilt by hand or motor, and the chucks and torch holders that go on them — NovoTech value line, built in China.", False, None),
                ("tt-rolls", "Welding turning rolls · value line", "Turning rolls that turn pipe, tanks and vessels from Ø1-1/2 to 96″ under the torch — NovoTech value line, built in China.", False, None),
                ("tt-supports", "Pipe stands and supports", "Outboard supports, pipe stands, pipe jacks and roller stands for fit-up and welding.", True, None),
                ("tt-weld-tables", "Welding table and downdraft tables", "A fixture table with a 2″ hole grid, and downdraft tables that take grinding dust and welding fumes away from the operator.", True, None)],
        intro_add="NovoTech's value-line welding equipment, built in China, adds benchtop and chuck positioners from 33 lb, tilting positioners "
                  "to 1,102 lb and heavy positioners with motorized tilt to 8,818 lb, welding chucks and torch holders, TRS turning rolls for "
                  "pipe and vessels to 11,023 lb per set, pipe stands, supports and pipe jacks, a fixture welding table and downdraft tables.",
        points_add=["NovoTech value line: positioners 33 – 8,818 lb with chucks, hollow bores and motorized tilt; TRS turning rolls 2,205 – 11,023 lb",
                    "Pipe stands and supports to 19,800 lb, the WT-36X24 fixture table and MDT downdraft tables 1,350 – 3,700 CFM"],
        faq_add=[{"q": "Positioner or turning rolls?",
                  "a": "A positioner holds the part on a turntable or in a chuck and turns it about its own axis, tilted to bring the joint to the flat position: the machine for flanges, short pipe spools, hubs and parts up to about the size of the table. Turning rolls carry a long round part — pipe, a tank shell, a pressure vessel — on wheels and turn it under the torch: the machine for long and heavy work. Long pipe in a positioner chuck needs an outboard support stand at the far end."},
                 {"q": "How do I size a positioner for my part?",
                  "a": "By the weight and where its centre of gravity sits. The rating is for the centre of gravity close to the table centre and face: the further it is from the axis (an off-centre bracket) or from the table (a tall part), the more torque the drive and the tilt need. The heavy WP positioners are rated with the centre of gravity up to 12″ from the table centre and 12″ above it. For off-centre or tall parts choose the next size up, and send us a sketch with the weight."}],
        related_add=[{"href": "pipe-sanding-polishing-machines.html", "label": "Pipe sanding & polishing"}],
        set={"title": "Welding Positioners, Turning Rolls & Pipe Stands | NovoTech",
             "meta_description": "Welding positioners 33 – 8,818 lb, turning rolls to 11,023 lb, pipe stands and supports, a welding table and downdraft tables — NovoTech premium and value lines.",
             "h1": "Welding positioners, turning rolls, pipe stands and welding tables",
             "artifact_title": "Welding positioners, turning rolls, pipe stands and welding tables",
             "faq_title": "Questions we get asked about welding positioners and turning rolls",
             "breadcrumb": CRUMBS + [{"label": "Welding positioners & turning rolls"}],
             "hero_brand_line": "The WP tilting positioners are built in Turkey for NovoTech's premium line, with European components; NovoTech's value-line positioners, turning rolls, stands and tables are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech."},
    ),
}

# ---------------------------------------------------------------------------------------------------------------- tube-bender page in the pipe-benders hub
TUBE_SUBPAGE = {"slug": D.P_TUBE, "title": "Tube and pipe benders — hydraulic, electric and air-hydraulic · value line", "image": "tm-jtb50",
                "blurb": "NovoTech's value-line benders, built in China: JTB hydraulic PLC tube benders to 3-1/8″, the TBM-60 electric bender, a 25-ton tubing bender, air and electric benders for 2″ schedule 40 pipe, exhaust benders and an electric hydraulic pipe bender.",
                "nav_label": "Value-line tube & pipe benders", "families": [f["id"] for f in D.TUBE], "in_range": False}


def group_entry(page_slug, gid, title, lead, manual, fams):
    g = {"id": f"{gid}-group", "title": title, "lead": lead, "brand": BRAND, "families": [f["id"] for f in fams if f["group"] == gid]}
    if manual:
        g["tagline"] = MANUAL_TAG
    if not g["families"]:
        raise SystemExit(f"{page_slug}: group {gid} has no families")
    return g


def write_page(slug, p, fams):
    groups = [group_entry(slug, gid, t, lead, manual, fams) for gid, t, lead, manual in p["groups"]]
    crumbs = CRUMBS + ([p["crumb"]] if p.get("crumb") else []) + [{"label": p["h1"].split(" — ")[0]}]
    section = None
    if slug == D.P_CNC:                               # the value line's page under the CNC machine-tool hub, beside the Dener pages
        import machine_tools_nav as MTN
        h = MTN.hub()
        crumbs = CRUMBS + [{"label": MTN.SECTION, "href": f"{h['slug']}.html"}, {"label": p["h1"].split(" — ")[0]}]
        section = {"label": MTN.SECTION, "related_title": MTN.RELATED_TITLE,
                   "hub": {"href": f"{h['slug']}.html", "label": h["label"], "image": h["image"], "blurb": h["blurb"]},
                   "pages": [{"href": f"{s}.html", "label": nav, "current": s == slug} for s, nav, _ in MTN.siblings()]}
        p = dict(p, related=[{"href": f"{s}.html", "label": lab} for s, _, lab in MTN.siblings() if s != slug]
                 + [{"href": f"{h['slug']}.html", "label": h["label"]}] + [r for r in p["related"] if r["href"] != f"{h['slug']}.html"])
    n_models = sum(len(f["specs"]["models"]) for f in fams)
    page = {
        "slug": slug, "template": "category.html", "family_set": SET,
        "title": p["title"], "artifact_title": p["h1"], "meta_description": p["meta"], "h1": p["h1"], "intro": p["intro"].replace("{n}", f"{n_models:,}"),
        "hero_points": p["points"], "hero_image": p["hero"], "hero_image_secondary": p["minis"],
        "breadcrumb": crumbs, "hero_brand_line": BRAND_LINE, "nav_label": p["nav"],
        "groups": groups, "faq": p["faq"], "faq_title": p.get("faq_title") or f"Questions we get asked about {lower_keep_acronyms(p['h1'].split(' — ')[0])}",
        "catalogue_pdf": None, "origin_feature": ORIGIN, "section_label": p["nav"],
        "related_pages": p["related"], "related_title": "More machinery from NovoTech", **NO_VIDEO,
    }
    if section:
        page["section"] = section
        page["section_label"] = section["label"]
    write_json(os.path.join(ROOT, "content", "pages", f"{slug}.json"), page)
    return page


def write_extra(slug, x, fams):
    groups = []
    for gid, t, lead, manual, after in x["groups"]:
        g = group_entry(slug, gid, t, lead, manual, fams)
        if after:
            g["after"] = after
        groups.append(g)
    out = {"slug": slug, "family_set": SET, "groups": groups}
    for k in ("intro_add", "points_add", "faq_add", "related_add", "set"):
        if x.get(k):
            out[k] = x[k]
    d = os.path.join(ROOT, "content", "extra_groups")
    os.makedirs(d, exist_ok=True)
    write_json(os.path.join(d, f"ttmc-{slug}.json"), out)


def register_images(used):
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key in sorted(used):
        if key in HP.PHOTOS:                     # the supplier's high-resolution photos (Oct 2026) replace the catalogue crops
            alt, detail, size, tool = HP.PHOTOS[key]["alt"], bool(HP.PHOTOS[key].get("detail")), 1024, "ttmc_hires_photos.py"
        elif key in PH.PLAN:                     # Vol. 23 catalogue crops, under 1,000 px: the 768 px matte is as sharp and twice as fast
            alt, detail, size, tool = PH.PLAN[key][3], key in PH.DETAIL, 768, "ttmc_more_photos.py"
        elif key in NP.PHOTOS:                   # 2026 sheets (up to 2,300 px): 1024 px matte; catalogue photos under 1,300 px: 768
            alt, detail, tool = NP.PHOTOS[key]["alt"], key in NP.DETAIL, "ttmc_new_photos.py"
            with Image.open(os.path.join(ROOT, "tools", "src-images", "ttmc-more", f"{key}.jpg")) as im:
                size = 1024 if max(im.size) >= 1300 else 768
        else:
            raise SystemExit(f"no photo for {key} in ttmc_more_photos.PLAN or ttmc_new_photos.PHOTOS")
        src = f"tools/src-images/ttmc-more/{key}.jpg"
        if not os.path.exists(os.path.join(ROOT, src)):
            raise SystemExit(f"missing crop for {key} — run tools/{tool}")
        imap[key] = {"src": src, "alt": alt, "section": "ttmc-more", "trim": True, "quality": 82, "cutout": not detail, "cut_size": size}
        spec = f"tools/cutout-specs/birefnet/{key}.json"       # keep / drop polygons for a photo BiRefNet gets wrong (smeared stand, floor shadow)
        if os.path.exists(os.path.join(ROOT, spec)):
            imap[key]["cut_spec"] = spec
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "ttmc_more_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    fams = D.NEW_FAMILIES + D2.GROUP_FAMILIES
    write_families(SET, fams)
    for slug, p in PAGES.items():
        if slug == D.P_BRAKE:     # the brakes are a hub with one page per kind now — tools/brake_hub.py writes them (after this script)
            continue
        write_page(slug, p, [f for f in fams if f["page"] == slug])
    for slug, x in EXTRA.items():
        write_extra(slug, x, [f for f in fams if f["page"] == slug])
    write_json(os.path.join(ROOT, "content", "extra_groups", "ttmc-pipe-benders.json"),
               {"slug": "pipe-benders", "family_set": SET, "subpages": [TUBE_SUBPAGE],
                "related_add": [{"href": "tube-bender.html", "label": "Tube and pipe benders · value line"}]})
    used = {k for f in fams + D2.SHEAR for k in f["images"]} | {p["hero"] for p in PAGES.values()} | {m for p in PAGES.values() for m in p["minis"]}
    keys = register_images(used)
    print(f"ttmc-more: {len(fams)} families ({sum(len(f['specs']['models']) for f in fams)} models) · {len(PAGES)} new pages · "
          f"{len(EXTRA)} pages with value-line groups · {len(keys)} photos")


if __name__ == "__main__":
    build()
