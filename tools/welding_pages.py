#!/usr/bin/env python3
"""The welding automation section (the owner, Nov 7 2026): a hub, welding-automation.html (hub.html), over four pages —
welding-positioners.html (every positioner), welding-turning-rolls.html (turning rolls, pipe and fit-up rotators and pipe stands),
column-and-boom-welding-manipulators.html and welding-tables.html (the fixture welding table and the downdraft tables).  On every
page the families run from the smallest model at the top to the largest at the bottom, the premium line in its place by size.

The families come from content/families/tubend.json (tools/tubend_pages.py: the premium-line WP 100 / WP 300), ttmc-more.json
(tools/ttmc_more_pages.py: the value-line positioners, turning rolls, stands and tables) and tools/datang_data.py (the value-line
positioners, turning rolls and column & boom manipulators added Nov 7 2026); this script merges them into
content/families/welding-automation.json, so run it after the other two:

    python3 tools/tubend_pages.py && python3 tools/ttmc_more_pages.py && python3 tools/welding_pages.py && python3 tools/guides.py
"""
import json
import os

import datang_data as DT
from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families, write_hub, write_json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "welding-automation"
SECTION = "Welding automation"
HUB = "welding-automation"
P_POS, P_ROLL, P_CAB, P_TAB = DT.P_POS, DT.P_ROLL, DT.P_CAB, "welding-tables"
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}
SOURCES = ("ttmc-more", "tubend")
PDF_WP = {"file": "files/NovoTech-Pipe-Benders-Welding-Positioners-2026.pdf", "label": "Download the NovoTech pipe bender & welding positioner brochure",
          "size": "PDF · imperial units"}

# (page, group id, group title, brand, family ids) — display order: small to large on every page (the owner, Nov 7 2026)
GROUPS = [
    (P_POS, "vl-light", "Light and benchtop welding positioners · value line", "novotech", ["dt-hb-light", "tt-wp-bench", "tt-wp-chuck"]),
    (P_POS, "pl-tilt", "WP tilting welding positioners · premium line", "novotech-premium", ["tubend-wp"]),
    (P_POS, "vl-tilt", "Tilting welding positioners · value line", "novotech", ["tt-wp-tilt", "dt-hb"]),
    (P_POS, "vl-tables", "Rotary welding tables and lift positioners · value line", "novotech", ["dt-hbt", "dt-hbj"]),
    (P_POS, "vl-heavy", "Heavy welding positioners · value line", "novotech", ["tt-wp-heavy", "dt-hb-heavy"]),
    (P_POS, "vl-order", "Headstock, tailstock and special positioners · value line, built to order", "novotech", ["dt-headtail", "dt-special-pos"]),
    (P_POS, "vl-acc", "Welding chucks and torch holders · value line", "novotech", ["tt-wp-acc"]),
    (P_ROLL, "vl-light-rolls", "Light welding turning rolls · value line", "novotech", ["dt-dzg-light", "tt-trs"]),
    (P_ROLL, "vl-adjust", "Adjustable welding turning rolls · value line", "novotech", ["dt-dkg", "dt-dsk"]),
    (P_ROLL, "vl-self", "Self-aligning welding turning rolls · value line", "novotech", ["dt-dzg"]),
    (P_ROLL, "vl-pipe", "Pipe rotators and fit-up rotators · value line, built to order", "novotech", ["dt-pipe-rot"]),
    (P_ROLL, "vl-stands", "Pipe stands and supports · value line", "novotech", ["tt-wtr"]),
    (P_CAB, "vl-cab", "Column and boom welding manipulators · value line", "novotech", ["dt-dlh-small", "dt-dlh-medium", "dt-dlh-heavy"]),
    (P_TAB, "vl-weld-table", "Welding tables · value line", "novotech", ["tt-wt3624"]),
    (P_TAB, "vl-downdraft", "Downdraft tables · value line", "novotech", ["tt-mdt"]),
]
PREMIUM = {"sahinler", "novotech-premium"}

# photos and models small to large (the owner, Nov 7 2026); the same photos and table columns, only reordered
IMAGE_ORDER = {
    "tt-wp-bench": ["tm-mrt15", "tm-mrt15-v", "tm-wp30t", "tm-wp30t-chuck", "tm-wp50", "tm-wp50-gas"],
    "tt-wp-chuck": ["tm-wp100t", "tm-wp100t-h", "tm-wp110", "tm-wp110-panel", "tm-wp110t"],
    "tt-wp-tilt": ["tm-wp220", "tm-wp350", "tm-wp500", "tm-wp500-panel", "tm-wp500t", "tm-wp-sample"],
    "tt-wp-heavy": ["tm-wp1000", "tm-wp2000", "tm-wp3000", "tm-wp-heavy-box"],
    "tubend-wp": ["tb-wp100", "tb-wp300", "tb-wp300-plate"],
}
MODEL_ORDER = {"tt-wp-bench": ["MRT-15", "WP-30T", "WP-50"]}       # 33 / 66 / 110 lb

SUBPAGES = [
    (P_POS, "Welding positioners — benchtop, tilting, heavy, rotary-table and lift positioners, 22 to 44,092 lb", "dt-hb",
     "Every positioner on one page, small to large: light and benchtop positioners from 22 lb, premium-line WP tilting positioners, "
     "tilting and heavy positioners to 44,092 lb, rotary welding tables, lift and headstock positioners.", "Welding positioners"),
    (P_ROLL, "Welding turning rolls — welding rotators and pipe turning rolls, 2,205 to 220,462 lb per set", "dt-dzg",
     "Light, bolt- and lead-screw adjustable and self-aligning turning rolls for pipe, tanks and vessels to Ø216.5″, pipe and fit-up "
     "rotators, and pipe stands and supports.", "Welding turning rolls"),
    (P_CAB, "Column and boom welding manipulators — 31.5 to 275.6″ lift, 39.4 to 315″ boom", "dt-dlh-medium",
     "Small, medium and heavy manipulators that carry the welding head over the seams of tanks and vessels — fixed, rotating or "
     "travelling.", "Column & boom manipulators"),
    (P_TAB, "Welding tables and downdraft tables — fixture welding table and downdraft grinding tables", "tm-wt3624",
     "The WT-36X24 mobile fixture table with a 2″ hole grid, and MDT downdraft tables that draw dust and fumes down at 1,350 – 3,700 CFM.",
     "Welding tables"),
]


def hub():
    return {"slug": HUB, "label": "All welding automation", "image": "dt-hb",
            "blurb": "Positioner, turning rolls, column and boom or welding table? Every machine NovoTech sells for moving the work under the torch, with the four kinds compared."}


def siblings():
    return [(s, nav, t.split(" — ")[0]) for s, t, _, _, nav in SUBPAGES]


# ------------------------------------------------------------------------------------------------ shared answers
FAQ_POS_OR_ROLLS = {"q": "Positioner or turning rolls?",
                    "a": "A positioner holds the part on a turntable or in a chuck and turns it about its own axis, tilted to bring the joint to the flat position: the machine for flanges, short pipe spools, hubs and parts up to about the size of the table. Turning rolls carry a long round part — pipe, a tank shell, a pressure vessel — on wheels and turn it under the torch: the machine for long and heavy work. Long pipe in a positioner chuck needs an outboard support stand at the far end."}
FAQ_SIZE = {"q": "How do I size a positioner for my part?",
            "a": "By the weight and where its centre of gravity sits. The rating is for the centre of gravity close to the table centre and face: the further it is from the axis (an off-centre bracket) or from the table (a tall part), the more torque the drive and the tilt need. The tables give the limits — the HB positioners up to 3.9 – 9.8″ off the axis and 5.9 – 23.6″ above the table, the heavy WP positioners 12″ and 12″. For off-centre or tall parts choose the next size up, and send us a sketch with the weight."}
FAQ_LINES = {"q": "Premium-line or value-line?",
             "a": "The WP 100 and WP 300 tilting positioners are built in Turkey for NovoTech's premium line and run on single-phase 220 V with a foot pedal. The other positioners, the turning rolls, the column and boom manipulators, the pipe stands and the tables are NovoTech's value line, built in China to NovoTech's specification — with the same CSA-approved panel, 1-year warranty and parts and support in Canada."}
LINE_VALUE = "NovoTech's value-line welding equipment is built in China to NovoTech's specification and sold, installed and supported in Canada by NovoTech."
ORIGIN_VALUE = {"title": "Value line from China", "text": "Built in China to NovoTech's specification — CSA-approved panels, a 1-year warranty and parts and support in Canada."}
ORIGIN_TR_CN = {"title": "Made in Turkey, value line from China",
                "text": "The WP tilting positioners are built in Turkey for NovoTech's premium line with European components; NovoTech's value line is built in China to our specification. CSA-approved panels, a 1-year warranty and parts and support in Canada."}

# ------------------------------------------------------------------------------------------------ pages
POS = dict(
    title="Welding Positioners for Sale in Canada — Tilting, Rotary & Lift Positioners, 22 to 44,092 lb | NovoTech",
    meta="Welding positioners from 22 to 44,092 lb — benchtop, tilting, heavy, rotary-table, lift and headstock positioners, sold and supported in Canada.",
    h1="Welding positioners — benchtop, tilting, heavy, rotary-table and lift positioners, 22 to 44,092 lb",
    intro="A welding positioner holds the part on a turntable and turns it under the torch at a steady, adjustable speed, so a round weld "
          "on a flange, pipe-to-plate joint, hub, tank head or wheel is laid in one continuous pass in the flat position — no stopping, "
          "repositioning and restarting around the part, and a more even bead whether the torch is held by hand or clamped in a holder. "
          "Tilting the table brings the joint to the best angle for the torch. NovoTech has positioners for every size of part, all on "
          "this page, small to large: light and benchtop positioners from 22 to 247 lb, with chucks, hollow bores and foot pedals; the "
          "premium-line WP 100 and WP 300 tilting positioners, built in Turkey, 220 and 661 lb on single-phase power; value-line tilting "
          "positioners from 485 to 2,646 lb; HBT rotary welding tables and HBJ lift positioners that also adjust in height, to 44,092 lb; "
          "heavy tilting positioners from 3,307 to 44,092 lb with motorized tilt; headstock and tailstock, L-type and hydraulic "
          "positioners built to order; and the chucks and torch holders that go on them. Each family below has its full specification "
          "table and photos. Parts, installation and service from Mississauga, ON, Canada.",
    points=["Light and benchtop positioners 22 – 247 lb · premium-line WP 100 and WP 300 tilting positioners, 220 and 661 lb, single-phase",
            "Tilting positioners to 2,646 lb · heavy HB and WP positioners to 44,092 lb with motorized tilt",
            "HBT rotary welding tables and HBJ lift positioners to 44,092 lb · headstock and tailstock positioners built to order"],
    hero="dt-hb", minis=[],
    faq=[{"q": "What does a welding positioner do?",
          "a": "It turns the part under a stationary torch at a set speed, so a circumferential weld is made in one pass in the flat "
               "position — the easiest position to weld and the one that gives the most even bead. The welder no longer walks around the "
               "part or stops to reposition it; with the torch in a holder the travel speed is as steady as the table, which makes repeat "
               "parts faster and more uniform."},
         FAQ_SIZE,
         {"q": "How fast should the table turn?",
          "a": "Table speed (rpm) = travel speed ÷ (π × weld diameter). A MIG weld at 20 in/min around a Ø6″ flange needs about 1.1 rpm; "
               "a submerged-arc weld at 20 in/min on a Ø60″ tank head about 0.1 rpm. Check that the positioner's speed range covers your "
               "smallest and largest weld diameters: the light positioners turn up to 8 – 18 rpm, the heavy ones as slowly as 0.03 rpm."},
         {"q": "Tilting positioner, rotary table, lift or headstock positioner?",
          "a": "A tilting positioner turns and tilts the part on a table — the most versatile. A rotary welding table (HBT) only turns, for "
               "parts that stand upright: tanks, drums, rings and hubs. A lift positioner (HBJ) also adjusts the table height, so the work "
               "comes to the welder or the welding head. Headstock and tailstock positioners turn long parts — beams, columns, frames and "
               "shafts — about their own length."},
         {"q": "What can be mounted on the turntable?",
          "a": "The tables are T-slotted for clamps, angle plates and fixtures. A self-centring 3-jaw welding chuck holds pipe, shafts and "
               "round parts on centre — the WPC chucks on this page grip from Ø0.4″ inside to Ø15″ outside — and a torch holder on an "
               "adjustable arm keeps the torch in one place while the part turns."},
         FAQ_LINES, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about welding positioners",
    related_pages=[{"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "plate-beveler.html", "label": "Plate bevelers"},
                   {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}],
    related_title="More welding and fabrication machinery from NovoTech",
)

ROLL = dict(
    title="Welding Turning Rolls for Sale in Canada — Welding Rotators & Pipe Rotators to 220,462 lb | NovoTech",
    meta="Welding turning rolls from 2,205 to 220,462 lb per set — light, adjustable and self-aligning rotators, pipe and fit-up rotators and pipe stands, in Canada.",
    h1="Welding turning rolls — welding rotators and pipe turning rolls, 2,205 to 220,462 lb per set",
    intro="Welding turning rolls (welding rotators, tank turning rolls) carry a long round part — pipe, a tank shell, a pressure vessel — "
          "on two sets of wheels and turn it under a fixed torch at the welding speed: one section has the motor and the control, the "
          "other is an idler placed to suit the length of the part. NovoTech has them all on this page, small to large: light turning "
          "rolls from 2,205 lb per set for pipe and small vessels; DKG bolt-adjustable and DSK lead-screw adjustable rolls from 4,409 to "
          "220,462 lb, whose wheel spacing is set to the diameter; DZG self-aligning rolls from 11,023 to 220,462 lb, whose wheel pairs "
          "swing to the vessel by themselves; GGLJ pinch-type pipe rotators for pipe segments and flanges and hydraulic fit-up rotators "
          "that line up two shell sections for the joint; and pipe stands and supports for fit-up and outboard support. Polyurethane "
          "wheels; surface speeds of 3.9 – 39.4 in/min set by VFD on the larger rolls. Each family below has its full specification table "
          "and photos. Parts, installation and service from Mississauga, ON, Canada.",
    points=["Light DZG and TRS turning rolls, 2,205 – 11,023 lb per set, work from Ø0.8″",
            "DKG bolt-adjustable and DSK lead-screw rolls 4,409 – 220,462 lb · DZG self-aligning rolls 11,023 – 220,462 lb, work to Ø216.5″",
            "GGLJ pinch-type pipe rotators, hydraulic fit-up rotators and pipe stands to 19,800 lb"],
    hero="dt-dzg", minis=[],
    faq=[{"q": "Self-aligning or adjustable turning rolls?",
          "a": "Self-aligning rolls (DZG) swing their wheel pairs to the diameter by themselves, so vessels of different diameters go on "
               "without resetting — the choice when diameters change often. Adjustable (conventional) rolls hold their wheels at a set "
               "spacing: the DKG moves the wheel blocks to bolt positions, the DSK sets them with a lead screw and hand wheel. They cost "
               "less and suit work that stays in one diameter range for a while."},
         {"q": "How are turning rolls rated?",
          "a": "By the weight per set — one drive and one idler section — and by the diameter range the wheels carry. Add the weight of "
               "the part and any fixtures, and leave a margin for out-of-round shells and off-centre nozzles; very long work can rest on "
               "two idler sections beside the drive."},
         {"q": "How fast do the rolls turn the work?",
          "a": "Turning rolls are set by the surface speed of the work, which is the travel speed of the weld: the adjustable and "
               "self-aligning rolls run 3.9 – 39.4 in/min (6 – 60 m/h) by VFD, for manual welding and submerged-arc heads; the light DZG "
               "rolls reach 43 – 75 in/min and the TRS rolls 56 – 143 in/min."},
         {"q": "What does a fit-up rotator do?",
          "a": "It brings two shell sections into line before they are welded: two hydraulic swing-arm lifting rollers raise, lower and "
               "shift each section slightly until the edges meet evenly, then the drive roller turns both for welding. The rollers move "
               "on rails to suit the diameter."},
         FAQ_POS_OR_ROLLS, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about welding turning rolls",
    related_pages=[{"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "plate-beveler.html", "label": "Plate bevelers"},
                   {"href": "pipe-notcher.html", "label": "Tube notchers"}],
    related_title="More welding and fabrication machinery from NovoTech",
)

CAB = dict(
    title="Column and Boom Welding Manipulators for Sale in Canada — 31.5 to 275.6″ Lift | NovoTech",
    meta="Column and boom welding manipulators for tank and vessel seams — 31.5 to 275.6″ lift, 39.4 to 315″ boom, fixed, rotating or travelling, sold in Canada.",
    h1="Column and boom welding manipulators — 31.5 to 275.6″ lift, 39.4 to 315″ boom",
    intro="A column and boom (welding manipulator) holds the welding head — submerged arc, MIG or TIG — on a horizontal boom that "
          "travels up and down a column and in and out over the part, and feeds it along the seam at the welding speed: longitudinal "
          "seams of tanks and pipe, and, with turning rolls or a positioner turning the part beneath it, circumferential seams inside and "
          "outside. NovoTech's value-line manipulators, built in China, come in three sizes, all on this page, small to large: small "
          "manipulators with 31.5 to 78.7″ of lift and 39.4 to 78.7″ of boom travel, the column turned by hand; medium ones with 78.7 to "
          "157.5″ of lift and 118.1 to 196.9″ of boom; and heavy ones with 196.9 to 275.6″ of lift and 236.2 to 315″ of boom, with "
          "motorized column rotation and carriage travel. Every model is available fixed, fixed with rotation or travelling with rotation, "
          "with arc auto-tracking, a TV monitor and flux recovery as options. Parts, installation and service from Mississauga, ON, Canada.",
    points=["Small DLH0810 – DLH2020: 31.5 – 78.7″ lift, 39.4 – 78.7″ boom, column turned by hand",
            "Medium DLH2030 – DLH4050 and heavy DLH5060 – DLH7080: to 275.6″ lift and 315″ boom, motorized rotation and carriage",
            "Boom feed 4.7 – 47.2 in/min · fixed, rotating or travelling · arc tracking, TV monitor, flux recovery"],
    hero="dt-dlh-medium", minis=[],
    faq=[{"q": "What is a column and boom used for?",
          "a": "Welding long and circumferential seams by machine: the boom puts the welding head over the seam and feeds it at the "
               "welding speed while the operator watches the arc. With the vessel on turning rolls the head stays still and the vessel "
               "turns for circumferential seams; with the boom feeding, it welds longitudinal seams — inside and outside of small tanks, "
               "longitudinal and transverse seams of large ones."},
         {"q": "Fixed, rotating or travelling?",
          "a": "A fixed column suits a cell where the part comes to the machine. A fixed column with rotation swings the boom up to ±180° "
               "between two stations — weld one part while the next is loaded. A travelling column runs on rails along the work, for long "
               "vessels and several stations."},
         {"q": "Which size do I need?",
          "a": "By the largest part: the lift has to put the head at the top of the largest vessel on its rolls, and the boom has to reach "
               "the far end of the longest seam — or inside the vessel for internal seams. Send us the diameters and lengths of your vessels "
               "and the welding process and we size the manipulator and the rolls under it."},
         {"q": "What options are there?",
          "a": "Arc auto-tracking that keeps the head on the seam, a TV monitor for watching the arc from the control station, and a flux "
               "recovery and conveying system for submerged-arc welding. The welding power source and head are chosen for the process."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about column and boom manipulators",
    related_pages=[{"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "plate-beveler.html", "label": "Plate bevelers"},
                   {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}],
    related_title="More welding and fabrication machinery from NovoTech",
)

TAB = dict(
    title="Welding Tables & Downdraft Tables for Sale in Canada — Fixture Table and Grinding Tables | NovoTech",
    meta="A mobile 36 × 24″ fixture welding table with a 2″ hole grid, and MDT downdraft tables that draw grinding dust and welding fumes down at 1,350 – 3,700 CFM.",
    h1="Welding tables and downdraft tables — fixture welding table and downdraft grinding tables",
    intro="A welding table holds the parts square and flat for fit-up, tacking and welding; a downdraft table draws grinding dust, "
          "sanding dust and welding fumes down through its perforated top before they reach the operator. NovoTech's value line, built in "
          "China, has both on this page: the WT-36X24 mobile fixture table — a 36 × 24 × 5/8″ top flat to 0.006″ with 216 holes of 5/8″ on "
          "a 2″ grid for clamps and fixtures, reversible and nitrided against spatter, on casters with a tube and pipe notcher — and the "
          "MDT downdraft tables: the MDT-4840 and MDT-6137 drawing 1,350 CFM through three filter stages to HEPA, and the MDT-6022 "
          "grinding table moving 3,700 CFM through four panel filters. Each has its full specification table and photos. Parts and "
          "service from Mississauga, ON, Canada.",
    points=["WT-36X24 fixture table: 36 × 24 × 5/8″, flat to 0.006″, 216 holes of 5/8″ on a 2″ grid, 1,500 lb",
            "MDT-4840 and MDT-6137 downdraft tables: 1,350 CFM, three-stage filtration to HEPA H13",
            "MDT-6022 grinding table: 61 × 20″, 3,700 CFM through four panel filters"],
    hero="tm-mdt4840", minis=[],   # the downdraft table large, the welding table under it (the owner, Nov 7 2026)
    faq=[{"q": "What is a downdraft table for?",
          "a": "Grinding, sanding and welding small parts without the dust and fumes rising past the operator's face: a fan under the "
               "perforated top pulls the air down through the filters. The MDT-4840 and MDT-6137 filter it in three stages to HEPA H13, "
               "the MDT-4840 with compressed-air cleaning of its cartridges; the MDT-6022 moves 3,700 CFM for heavy grinding."},
         {"q": "Why a fixture table with a hole grid?",
          "a": "The 5/8″ holes on a 2″ grid take standard clamps, stops and squares, so a part is set up square and repeatable in minutes "
               "and the setup can be rebuilt for the next batch. The top is flat to 0.006″, reversible and nitrided, so spatter does not "
               "stick and the surface stays true."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about welding and downdraft tables",
    related_pages=[{"href": "belt-grinder.html", "label": "Belt grinders"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                   {"href": "corner-grinding-machines.html", "label": "Corner grinders"}],
    related_title="More welding and fabrication machinery from NovoTech",
)

HUB_PAGE = dict(
    title="Welding Automation for Sale in Canada — Positioners, Turning Rolls, Column & Boom, Welding Tables | NovoTech",
    meta="Welding positioners 22 – 44,092 lb, turning rolls to 220,462 lb, column and boom manipulators and welding tables — sold, installed and supported in Canada.",
    h1="Welding automation — welding positioners, turning rolls, column and boom manipulators and welding tables",
    intro="Welding automation moves the work, not the welder: the part turns under a fixed torch at the welding speed, so round and long "
          "welds are laid in one continuous pass in the flat position, by hand or with an automatic welding head. NovoTech sells four "
          "kinds in Canada, each on its own page: welding positioners — tilting turntables, rotary tables, lift positioners and headstock "
          "and tailstock positioners from 22 to 44,092 lb; welding turning rolls — light, adjustable and self-aligning rolls for pipe, "
          "tanks and vessels from Ø0.8 to 216.5″ and 2,205 to 220,462 lb per set, with pipe and fit-up rotators and pipe stands; column "
          "and boom manipulators that carry the welding head over the seam, 31.5 to 275.6″ of lift; and welding tables and downdraft "
          "tables. The premium-line WP positioners are built in Turkey, the value line in China. Below, the four kinds compared, every "
          "family by line, the buying guide and the questions we get asked; every machine comes with a CSA-approved panel and support "
          "from Mississauga, ON, Canada.",
    points=['<a href="welding-positioners.html">Welding positioners</a>: <a href="welding-positioners.html#dt-hb-light">light</a>, '
            '<a href="welding-positioners.html#tubend-wp">premium-line WP</a>, <a href="welding-positioners.html#dt-hb-heavy">heavy</a>, '
            '<a href="welding-positioners.html#dt-hbt">rotary-table</a> and <a href="welding-positioners.html#dt-hbj">lift</a> positioners, 22 – 44,092 lb',
            '<a href="welding-turning-rolls.html">Welding turning rolls</a>: <a href="welding-turning-rolls.html#dt-dzg">self-aligning</a> and '
            '<a href="welding-turning-rolls.html#dt-dkg">adjustable</a> rolls to 220,462 lb per set, <a href="welding-turning-rolls.html#dt-pipe-rot">pipe and fit-up rotators</a>, '
            '<a href="welding-turning-rolls.html#tt-wtr">pipe stands</a>',
            '<a href="column-and-boom-welding-manipulators.html">Column and boom manipulators</a> 31.5 – 275.6″ lift · '
            '<a href="welding-tables.html">welding and downdraft tables</a>'],
    hero="dt-hb", minis=["dt-dzg", "dt-dlh-medium"],
    range_cols=["Load", "Table or work Ø", "Speed", "Tilt or travel", "Motor"],
    range_lead="Every machine of the section in one table. Each row links to the full specification table on its page.",
    range_caption="Welding automation supplied by NovoTech — positioners, turning rolls, column and boom manipulators and welding tables",
    range_note="Loads in lb with kg in brackets.",
    faq=[{"q": "Which welding automation do I need?",
          "a": "By the part. Round parts that fit on a table — flanges, hubs, pipe spools, tank heads — go on a positioner, tilted to bring "
               "the joint flat. Long round parts — pipe, tank shells, pressure vessels — turn on turning rolls. Long seams and "
               "circumferential seams welded by an automatic head need a column and boom over the part, usually with turning rolls under "
               "it. Fit-up, tacking and small parts go on a welding table. Send us the part and the welds and we size the set."},
         FAQ_POS_OR_ROLLS,
         {"q": "What does a column and boom do?",
          "a": "It holds the welding head on a boom that moves up and down the column and in and out over the part, and feeds it along "
               "the seam at the welding speed: longitudinal seams of tanks and pipe and, with turning rolls under the part, "
               "circumferential seams inside and outside. The column turns ±180° and, on the travelling versions, the carriage runs on "
               "rails along the work."},
         FAQ_SIZE, FAQ_LINES, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about welding automation",
    related_pages=[{"href": "corner-welding-machines.html", "label": "Corner welders"}, {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"},
                   {"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "plate-beveler.html", "label": "Plate bevelers"}],
    related_title="More welding and fabrication machinery from NovoTech",
)

COMPARE = {
    "title": "Which kind of welding automation?",
    "lead": "The four kinds NovoTech sells, side by side; each page lists every model of its kind.",
    "cols": ["", "Welding positioners", "Turning rolls", "Column & boom", "Welding tables"],
    "rows": [
        ["What it does", "Turns and tilts the part on a table, or between a headstock and tailstock", "Turns round work on wheels under the torch",
         "Carries the welding head over the seam on a boom", "Holds parts for fit-up and welding; downdraft tables draw off dust and fumes"],
        ["Typical work", "Flanges, hubs, pipe spools, tank heads, weldments", "Pipe, tank shells, pressure vessels",
         "Longitudinal and circumferential seams of tanks and vessels", "Fit-up, tacking, grinding and welding small parts"],
        ["Range", "22 – 44,092 lb", "2,205 – 220,462 lb per set · Ø0.8 – 216.5″", "31.5 – 275.6″ lift · 39.4 – 315″ boom", "36 × 24″ table · 1,350 – 3,700 CFM"],
        ["Page", {"href": "welding-positioners.html", "label": "Welding positioners"}, {"href": "welding-turning-rolls.html", "label": "Welding turning rolls"},
         {"href": "column-and-boom-welding-manipulators.html", "label": "Column & boom manipulators"}, {"href": "welding-tables.html", "label": "Welding tables"}],
    ],
}

RANGE_PICK = [["rated_load", "load_horizontal_vertical", "nominal_load_capacity", "load_per_set", "load_max", "vertical_travel"],
              ["worktable_diameter", "table_diameter", "table_chuck", "work_diameter", "table", "boom_travel"],
              ["rotation_speed", "table_rotation", "surface_speed", "linear_speed", "column_rotation_speed", "air_flow"],
              ["tilt", "boom_feed_speed", "holes", "filtration"], ["rotation_motor", "motor", "turntable_motor", "weight"]]

POS_LINE = ("The WP tilting positioners are built in Turkey for NovoTech's premium line with European components; NovoTech's value-line "
            "positioners are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech.")
PAGE_EXTRA = {
    P_POS: {"catalogue_pdfs": [PDF_WP], "hero_brand_line": POS_LINE, "origin_feature": ORIGIN_TR_CN},
    P_ROLL: {"catalogue_pdfs": [], "hero_brand_line": LINE_VALUE, "origin_feature": ORIGIN_VALUE},
    P_CAB: {"catalogue_pdfs": [], "hero_brand_line": LINE_VALUE, "origin_feature": ORIGIN_VALUE},
    P_TAB: {"catalogue_pdfs": [], "hero_brand_line": LINE_VALUE, "origin_feature": ORIGIN_VALUE},
}


def reorder_models(f, order):
    """the family's table columns (and glance rows) in the given model order"""
    sp = f["specs"]
    for t in sp["tables"]:
        if sorted(t["models"]) != sorted(order):
            raise SystemExit(f"welding_pages: MODEL_ORDER {f['id']} is not the table's models {t['models']}")
        idx = [t["models"].index(m) for m in order]
        t["models"] = list(order)
        for r in t["rows"]:
            r["cells"] = [r["cells"][i] for i in idx]
    by = {m["name"]: m for m in sp["models"]}
    sp["models"] = [by[m] for m in order]
    t0 = sp["tables"][0]
    old = " · ".join(t0["title"].split(" · "))
    t0["title"] = new = " · ".join(order)
    for k in ("name", "models_label"):
        f[k] = f[k].replace(old, new)


def families():
    sets = {s: json.load(open(os.path.join(ROOT, "content", "families", f"{s}.json"), encoding="utf-8"))["families"] for s in SOURCES}
    dt = {f["id"]: f for f in DT.FAMILIES}
    out, seen = [], set()
    for page, gid, _, brand, ids in GROUPS:
        for fid in ids:
            src = dt.get(fid) or next((sets[s][fid] for s in SOURCES if fid in sets[s]), None)
            if src is None:
                raise SystemExit(f"welding_pages: no family {fid}")
            if (src.get("brand") in PREMIUM) != (brand in PREMIUM):
                raise SystemExit(f"welding_pages: {fid} ({src.get('brand')}) in group {gid} ({brand})")
            f = json.loads(json.dumps(dict(src, id=fid, page=page, group=gid)))
            if f.get("brand") in PREMIUM:
                f["brand"] = "novotech-premium"
            if fid in IMAGE_ORDER:
                if sorted(IMAGE_ORDER[fid]) != sorted(f["images"]):
                    raise SystemExit(f"welding_pages: IMAGE_ORDER {fid} is not the family's photos {f['images']}")
                f["images"] = IMAGE_ORDER[fid]
            if fid in MODEL_ORDER:
                reorder_models(f, MODEL_ORDER[fid])
            out.append(f)
            seen.add(fid)
    missing = [f["id"] for f in DT.FAMILIES if f["id"] not in seen]
    if missing:
        raise SystemExit(f"welding_pages: Datang families not on a page: {missing}")
    return out


def build():
    fams = families()
    write_families(SET, fams)
    for slug, page in ((P_POS, POS), (P_ROLL, ROLL), (P_CAB, CAB), (P_TAB, TAB)):
        members = [f for f in fams if f["page"] == slug]
        groups = [(gid, title, "", brand) for pg, gid, title, brand, _ in GROUPS if pg == slug]
        extra = {"catalogue_pdf": None, **NO_VIDEO, **PAGE_EXTRA[slug],
                 "nav_label": next(nav for s, _, _, _, nav in SUBPAGES if s == slug)}
        write_category(slug, dict(page, groups=groups), members, SET, SECTION, hub=hub(), siblings=siblings(), extra=extra)
        print(f"{slug}: {len(members)} families, {sum(len(f['specs']['models']) for f in members)} models")
    write_hub(HUB, {**HUB_PAGE, "artifact_title": "Welding Automation", "nav_label": "All welding automation", "related_blurb": hub()["blurb"]},
              fams, SET, SECTION, [(s, t, im, b, nav) for s, t, im, b, nav in SUBPAGES],
              extra={"catalogue_pdf": None, "catalogue_pdfs": [PDF_WP], "range_pick": RANGE_PICK, **NO_VIDEO,
                     "hero_brand_line": "The premium-line WP positioners are built in Turkey with European components; the value-line positioners, turning rolls, manipulators, stands and tables are built in China — all to NovoTech's specification and sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Four kinds, two lines, one supplier", "text": "Positioners, turning rolls, column and boom manipulators and welding tables from NovoTech's premium line, built in Turkey, and its value line, built in China — installed, trained and supported by the same NovoTech technicians in Canada."},
                     "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"],
                     "hub_compact": True, "compare": COMPARE, "subpage_link": "all models, specifications and photos",
                     "lineup_noun": "welding automation equipment",
                     "related_title_": "More welding automation from NovoTech"})      # the section pages' related heading (build.py)
    path = os.path.join(ROOT, "content", "pages", f"{HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp in page["subpages"]:
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — every family"
    write_json(path, page)
    for name, p in [("hub", HUB_PAGE), ("positioners", POS), ("rolls", ROLL), ("column & boom", CAB), ("tables", TAB)]:
        print(f"{name:16s} title {len(p['title'])} · meta {len(p['meta'])}")
    print(f"welding automation hub: {len(fams)} families on {len(page['subpages'])} pages")


if __name__ == "__main__":
    build()
