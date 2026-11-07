#!/usr/bin/env python3
"""The hydraulic press section (the owner, Nov 7 2026): a hub at the old press URL (hydraulic-press.html, hub.html) over four pages —
hydraulic-shop-press.html, h-frame-hydraulic-press.html (H-frame and four-column presses), c-frame-hydraulic-press.html and
hydraulic-straightening-press.html — and riveting-machine.html, a page of its own outside the hub.  On every page the premium line
comes first and the value line below it; families and photos run small to large.

Page names from Search Console (Oct 2026 export): "hydraulic press" 3,166 impressions against "hydraulic presses" 2,626, "hydraulic
shop press" 2,869 against "hydraulic shop presses" 993.  The H-frame, C-frame, straightening and riveting names follow the way
press builders and dealers name these machines; no volume tool was available on the day.

The families come from content/families/sahinler.json (tools/sahinler_pages.py: the premium-line shop presses and, through
tools/hidroliksan_data.py, the premium-line production presses) and ttmc-more.json (tools/ttmc_more_pages.py: the value line); this
script merges them into content/families/all-presses.json, so run it after both:

    python3 tools/sahinler_pages.py && python3 tools/ttmc_more_pages.py && python3 tools/press_pages.py
"""
import json
import os

from isitan_lib import SAHINLER_INTRO_VIDEO, VOLT_FAQ_GENERIC, write_category, write_families, write_hub, write_json
from sahinler_lib import premium_pdf
import sahinler_pages as SP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "all-presses"
SECTION = "Hydraulic press"
HUB = "hydraulic-press"
P_SHOP, P_H, P_C, P_STR = "hydraulic-shop-press", "h-frame-hydraulic-press", "c-frame-hydraulic-press", "hydraulic-straightening-press"
P_RIV = "riveting-machine"            # its own page, not one of the hub's kinds (the owner, Nov 7 2026)
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}
PDF_SHOP = premium_pdf("premium-shop-presses")
PDF_PROD = SP.PDF_PROD
SOURCES = ("sahinler", "ttmc-more")

# (page, group id, group title, brand, family ids) — display order: premium line first, then the value line, small to large
GROUPS = [
    # the AT, AP, HPB and HP presses moved from the H-frame page to the shop presses, the HP-M1 sliding-table presses to the
    # straightening presses (the owner, Nov 7 2026)
    (P_SHOP, "pl-shop", "Hydraulic shop presses · premium line", "novotech-premium", ["sahinler-dpm", "sahinler-dpm-k", "sahinler-at", "sahinler-ap"]),
    (P_SHOP, "vl-shop", "Bench and workshop presses · value line", "novotech", ["tt-ebp10t", "tt-shop-small", "tt-hpb", "tt-hp-h", "tt-shop-hs"]),
    (P_H, "pl-h", "H-frame presses · premium line", "novotech-premium", ["nt-press-hdt", "nt-press-hsa", "nt-press-hdd", "nt-press-hhrp"]),
    (P_H, "pl-column", "Four-column presses · premium line", "novotech-premium", ["nt-press-hcfp"]),
    (P_H, "vl-column", "Four-column presses · value line", "novotech", ["tt-hp-f"]),
    (P_C, "pl-c", "C-frame presses · premium line", "novotech-premium", ["nt-press-cfs", "nt-press-cfss", "nt-press-cfdd"]),
    (P_C, "vl-c", "C-frame presses · value line", "novotech", ["tt-hp-c"]),
    (P_STR, "pl-str", "Straightening presses · premium line", "novotech-premium", ["nt-press-hsps", "sahinler-dk-s"]),
    (P_STR, "vl-str", "Presses with sliding table · value line", "novotech", ["tt-hp-m1"]),
    (P_RIV, "vl-rivet", "Orbital riveting machines · value line", "novotech", ["tt-riveter"]),
]
PREMIUM = {"sahinler", "novotech-premium"}      # both NovoTech premium line, built in Turkey: one brand here, so the hub lists them as one line

# photos small to large (the owner, Nov 7 2026); the same photos as the family's own list, only reordered
IMAGE_ORDER = {
    "sahinler-dk-s": ["sh-dks200", "sh-dks400", "sh-dks-remote", "shd-dks-side", "shd-dks-table", "shd-dks-piston"],
    "nt-press-hsps": ["hk-hsps-100", "hk-hsps", "hk-hsps-300", "hk-hsps-detail"],
    "tt-hp-h": ["tm-hp30", "tm-hp100"],
    "tt-hpb": ["tm-hpb580", "tm-hpb580d", "tm-hpb1500", "tm-hpb1500d"],
    "tt-hp-m1": ["tm-hp20m1", "tm-hp150m1", "tm-hp200m1"],
    "tt-hp-c": ["tm-hp30c2", "tm-hp63c2"],
    "tt-hp-f": ["tm-hp50f", "tm-hp150f1plc", "tm-hp315fk"],
}

SUBPAGES = [
    (P_SHOP, "Hydraulic shop presses — H-frame workshop and bench presses, 10 to 551 US tons", "sh-dpm",
     "For the repair shop, dealer and fabricator: premium-line DPM and mobile-cylinder DPM-K / DK presses from 33 to 220 US tons, AT "
     "T-slot presses and AP press brakes, and value-line bench, workshop, brake and H-frame presses from 10 to 551 tons.", "Hydraulic shop presses"),
    (P_H, "H-frame hydraulic presses — H-frame and four-column production presses, 55 to 661 US tons", "hk-hsa",
     "For dies and production: premium-line HDT, HSA, HDD deep drawing, SMC hot plate and HCFP four-column presses to 661 US "
     "tons (3,307 to order), and value-line HP-F four-column presses.", "H-frame presses"),
    (P_C, "C-frame hydraulic presses — open-gap presses, 22 to 276 US tons", "hk-cfss",
     "Open on three sides for small dies, punching and assembly: premium-line CFS, enclosed CFSS and CFDD deep drawing presses from 33 "
     "to 276 US tons, and value-line HP-C presses from 22 to 110 US tons.", "C-frame presses"),
    (P_STR, "Hydraulic straightening presses — portal, 3-axis and sliding-table presses, 22 to 441 US tons", "sh-dks400",
     "For beams, plate, rails and shafts that stay on the bed: premium-line HSPS portal straightening presses from 110 to 441 US tons "
     "and DK-S 3-axis moving straightening presses from 220 to 441 US tons, and value-line HP-M1 presses with a sliding table from "
     "22 to 220 US tons.", "Straightening presses"),
]


def hub():
    return {"slug": HUB, "label": "All hydraulic presses", "image": "sh-dpm",
            "blurb": "Shop, H-frame, C-frame or straightening press? Every hydraulic press NovoTech sells in Canada on one page, with the four kinds compared."}


def siblings():
    return [(s, nav, t.split(" — ")[0]) for s, t, _, _, nav in SUBPAGES]


# ------------------------------------------------------------------------------------------------ shared answers
FAQ_LINES = {"q": "Premium-line or value-line press?",
             "a": "The premium-line shop and production presses are built in Turkey with European hydraulics and Siemens controls, for daily production work, straightening lines and custom sizes. The value-line presses are built in China for the repair shop, the maintenance department and lighter production — the same tonnages at a lower price, with built-on or separate power units."}
FAQ_SHOP_OR_PROD = {"q": "Shop press or production press?",
                    "a": "A shop press is operated by hand — joystick or two-hand buttons — for one part at a time: pressing, straightening, bending. A production press runs a die under PLC control with programmed speeds, pressures, dwell and return, light barriers instead of guards, automatic lubrication and remote diagnostics, for thousands of cycles a shift. The NovoTech premium line starts at 33 US tons with the CFS C-frame and goes to 3,307 US tons on the H-frame presses."}
FAQ_CUSHION = {"q": "Single action or double action — what is a die cushion?",
               "a": "A single action press has one ram. A double action (deep drawing) press adds a die cushion in the lower table — a second cylinder that holds the blank holder with its own programmed force — so a flat blank can be drawn into a deep cup, pan or housing without wrinkling. The HDD H-frame and CFDD C-frame presses have the cushion built in; it is an option on the HCFP column press."}
FAQ_FRAMES = {"q": "H-frame, four-column or C-frame?",
              "a": "An H-frame (straight-side) press is the stiffest and takes the largest tables and tonnages — the choice for deep drawing and big dies. A four-column (column) press is open on all sides for die access and automation. A C-frame press is open on three sides, so small dies go in and out quickly and the press takes less floor space; its table size is limited because the C deflects, which is why the premium-line C-frame range stops at 276 US tons."}
FAQ_TO_ORDER = {"q": "Can the press be built to my die?",
                "a": "Yes — every series of the premium line is built to order in the table size, stroke, daylight and tonnage the die needs, from a 33 US ton C-frame to a 3,307 US ton H-frame, with quick die change, die loading arms, ejector, heated platens or a die cushion as required. Send us the die drawing and the cycle you need and we quote the press around it."}
FAQ_TONNAGE = {"q": "What tonnage shop press do I need?",
               "a": "Most truck, equipment and fabrication shops run a 66 – 110 US ton press (DPM 1040-60 to DPM 1570-100, or the value-line HPP-60 and HPP-100): enough for pressing bearings and bushings, straightening shafts to Ø3″ and bending flat bar. Go to 165 – 220 US tons for large bearings, track pins, heavy shafts and forming plate. Beams and plate that need a moving ram are on the straightening press page."}

ORIGIN_TR_CN = {"title": "Made in Turkey, value line from China",
                "text": "The premium-line presses are built in Turkey — the shop presses for NovoTech's premium line, the production presses by a Turkish press builder with 50 years of hydraulic press manufacturing, CE-certified with Siemens controls and European hydraulics; NovoTech's value line is built in China to our specification. CSA-approved panels, a 1-year warranty and parts and support in Canada."}
LINE_TR_CN = ("The premium-line presses are built in Turkey with European components; the value-line presses are built in China — all to "
              "NovoTech's specification and sold, installed and supported in Canada by NovoTech.")

# ------------------------------------------------------------------------------------------------ pages
SHOP = dict(
    title="Hydraulic Shop Press for Sale in Canada — Shop & Workshop Presses, 10 to 551 US Tons | NovoTech",
    meta="Hydraulic shop presses sold, installed and supported in Canada: premium-line DPM, DPM-K / DK, AT T-slot presses and AP press brakes from 33 to 220 US tons, and value-line bench, workshop, brake and H-frame presses from 10 to 551 tons.",
    h1="Hydraulic shop presses — H-frame workshop and bench presses, 10 to 551 US tons",
    intro="A hydraulic shop press is the machine every repair shop, truck and equipment dealer and fabricator reaches for several times "
          "a day: pressing bearings, bushings and pins, straightening shafts and bar, bending flat bar and short plate, pushing a die for "
          "the odd forming job. NovoTech sells two lines in Canada, all on this page, small to large: the premium line, built in Turkey — "
          "DPM H-frame shop presses from 33 to 220 US tons with two-speed joystick control, a pressure gauge and a relief valve against "
          "overload, and the DPM-K and DK presses whose cylinder travels across the frame on a hand wheel, so the ram meets the work "
          "instead of the work being shifted under the ram, the AT presses with T-slot tables for your own dies and the AP garage-type "
          "press brake for 1/4″ and 3/8″ plate, 110 to 165 US tons; and the value line, built in China — the EBP-10T hydraulic bench press for "
          "sheet-metal and louver tooling, the EBP-25T motorized workshop press of 28 US tons, the HPB presses with a brake function from "
          "33 to 331 US tons, the HP motorized H-frame presses from 33 to 551 US tons and the HPP-60 to HPP-160 motorized "
          "workshop presses with a moving cylinder, 66 to 176 US tons. Each family below has its full specification table and photos. "
          "For die work and production, see the H-frame and C-frame presses; for beams and plate, the straightening presses. Parts, "
          "installation and service from Mississauga, ON, Canada.",
    points=["Premium-line DPM shop presses 33 – 220 US tons: working widths 30.5″ to 61.8″, two-speed joystick, gauge and relief valve",
            "DPM-K and DK with a mobile cylinder on a hand wheel; AT T-slot presses and AP press brakes 110 – 165 US tons",
            "NovoTech value line: EBP-10T bench press, EBP-25T workshop press, HPB brake presses, HP H-frame presses, HPP-60 – HPP-160 motorized workshop presses"],
    hero="sh-dpm", minis=["sh-dk", "tm-hpp100"],
    faq=[FAQ_TONNAGE,
         {"q": "What do the model numbers mean — DPM 1040-60?", "a": "The first number is the clear working width between the columns in millimetres (1040 mm = 40.9″) and the second the press force in metric tons (60 t = 66 US tons). A 1570-100 press is 61.8″ wide at 110 US tons."},
         {"q": "Why a mobile (sliding) cylinder?", "a": "On the DPM-K and DK the cylinder head travels across the frame on a hand wheel, so the ram comes to the work — a long shaft, a frame rail or a plate stays clamped while you straighten it point by point instead of shifting the part under a fixed ram. The DK series adds a wider 61.8″ – 74.8″ frame. The value-line HPP presses also have a cylinder that moves across the frame."},
         {"q": "Hand pump, foot pedal or joystick?", "a": "The DPM and DPM-K presses come with two-speed joystick control; a hand pump for fine pressing, a foot pedal and a limit switch that stops the stroke at a set height are options. The value-line HPP presses pair the motorized two-step unit with a double-acting hand pump for fine positioning, and the EBP-25T has infinitely variable pressure and speed."},
         {"q": "Can a press bend plate?", "a": "The AP garage-type press brake is a hydraulic press delivered with a 5-face prism bottom die and hardened top blade for bending 1/4″ (110 US tons) or 3/8″ (165 US tons) mild steel over 40″ or 60″ — the economical way to bend brackets and short plate without a full press brake. The value-line HPB presses are set up the same way, with replaceable top tools, a V-block and a support table with stops; the twin-cylinder D models bend widths of 47 – 71″. The AT press has T-slot tables for bolting your own forming, blanking and coining dies."},
         {"q": "What is the EBP-10T bench press for?", "a": "The sheet-metal and HVAC shop: its 25″ throat and 6″ tool opening take the industry-standard bench and louver press tooling, so it punches round, square and oblong holes, punches and flares or beads, cuts louvers, notches corners, bends 90° in 3/8″ mild steel and shears 16 ga — and it works as a hydraulic arbor press as well."},
         FAQ_LINES, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about hydraulic shop presses",
    related_pages=[{"href": "riveting-machine.html", "label": "Orbital riveting machines"}, {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"},
                   {"href": "lock-former.html", "label": "Lock formers and HVAC machines"}],
    related_title="More pressing and bending machinery from NovoTech",
)

HFRAME = dict(
    title="H-Frame Hydraulic Press for Sale in Canada — H-Frame & Four-Column Presses, 55 to 661 US Tons | NovoTech",
    meta="H-frame hydraulic presses sold, installed and supported in Canada: premium-line HDT, HSA single action and HDD deep drawing presses, SMC hot plate and HCFP four-column presses to 661 US tons (3,307 to order), and value-line HP-F four-column presses from 55 to 347 US tons.",
    h1="H-frame hydraulic presses — H-frame and four-column production presses, 55 to 661 US tons",
    intro="An H-frame (straight-side) hydraulic press carries the cylinder in a crown between two side frames, so the frame stays square "
          "under load and takes the largest tables and tonnages — the press for dies: forming, blanking, coining, deep drawing and "
          "composite moulding, cycle after cycle. A four-column press does the same on four guide posts, open to the die from every side. "
          "NovoTech sells two lines in Canada, all on this page, small to large: the premium line, built in Turkey — the HDT Eco "
          "H-frame to 276 US tons and the production presses on a welded, machined monoblock frame with Siemens PLC, HMI touchscreen and "
          "light barriers — HSA single action, HDD double action deep drawing with a die cushion, SMC / HHRP hot plate presses and HCFP "
          "four-column presses, 110 to 661 US tons as standard, the H-frames to 3,307 US tons and the HCFP to 1,102 US tons to order; and "
          "the value line, built in China — HP-F four-column presses from 55 to 347 US tons, the F1/PLC models with a touchscreen. "
          "Each family below has its full specification table and photos. Parts, installation and service from Mississauga, ON, Canada.",
    points=["Premium line: HDT Eco H-frame presses 110 – 276 US tons with a T-slotted table and two-hand control",
            "Premium-line production presses: HSA single action, HDD deep drawing, SMC / HHRP hot plate and HCFP four-column, 110 – 661 US tons, Siemens PLC and light barriers",
            "NovoTech value line: HP-F four-column presses 55 – 347 US tons, F1/PLC models with touch-screen control"],
    hero="hk-hsa", minis=["hk-hdt", "tm-hp50f"],
    faq=[FAQ_SHOP_OR_PROD, FAQ_CUSHION,
         {"q": "H-frame or four-column?", "a": "An H-frame press is the stiffest for its size and takes the widest tables — the choice for deep drawing, long dies and the largest tonnages. A four-column press guides the slide on four posts and is open to the die from all four sides, which suits automation, die loading from the side and parts that overhang the table. The HCFP and HP-F are four-column presses; the HSA, HDD, HHRP and HDT are H-frames."},
         FAQ_TO_ORDER, FAQ_LINES, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about H-frame hydraulic presses",
    related_pages=[{"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"}, {"href": "hydraulic-punching-machines.html", "label": "Hydraulic punching machines"},
                   {"href": "horizontal-press-brake.html", "label": "Horizontal press brakes"}],
    related_title="More pressing and bending machinery from NovoTech",
)

CFRAME = dict(
    title="C-Frame Hydraulic Press for Sale in Canada — Open-Gap C-Frame Presses, 22 to 276 US Tons | NovoTech",
    meta="C-frame hydraulic presses sold, installed and supported in Canada: premium-line CFS, enclosed CFSS and CFDD deep drawing C-frame presses from 33 to 276 US tons, and value-line HP-C C-frame presses from 22 to 110 US tons.",
    h1="C-frame hydraulic presses — open-gap presses, 22 to 276 US tons",
    intro="A C-frame (gap-frame) hydraulic press is open on three sides: small dies go in and out quickly, the operator reaches the part "
          "from the front and both sides, and the press takes less floor space than an H-frame of the same force — the press for punching, "
          "blanking and forming with small dies, press-fitting and assembly. NovoTech sells two lines in Canada, all on this page: the "
          "premium line, built in Turkey on a welded monoblock frame with a chrome-plated cylinder and a T-slotted table, 33 to 276 US tons "
          "— the CFS with a pressure transmitter, light barrier and two-hand control, the CFSS with the work area enclosed by guards and a "
          "light barrier, and the CFDD for deep drawing, with a die cushion of 11 to 110 US tons and an ejector that lifts the drawn part "
          "out; and the value line, built in China — the HP-C presses from 22 to 110 US tons, open on three sides for assembling and "
          "dismantling large parts. Each family below has its full specification table and photos. For larger tables and tonnages, see the "
          "H-frame presses. Parts, installation and service from Mississauga, ON, Canada.",
    points=["Premium line: CFS single action, CFSS enclosed and CFDD deep drawing C-frame presses, 33 – 276 US tons, 15.7″ stroke",
            "T-slotted tables to 43.3 × 23.6″; two-hand control and light barriers; die cushion 11 – 110 US tons with ejector on the CFDD",
            "NovoTech value line: HP-C C-frame presses 22 – 110 US tons, tables 15.7 × 11.8″ to 31.5 × 23.6″"],
    hero="hk-cfss", minis=["hk-cfdd", "tm-hp30c2"],
    faq=[{"q": "C-frame or H-frame?", "a": "A C-frame press is open on three sides, so small dies go in and out quickly, the part is easy to reach and the press takes less floor space. The open throat deflects slightly under load, which limits the table size and the force — the premium-line C-frame range stops at 276 US tons. For deep drawing large parts, long dies or more force, an H-frame press is stiffer and takes larger tables."},
         {"q": "CFS, CFSS or CFDD?", "a": "All three share the welded monoblock frame, chrome-plated cylinder and T-slotted table, from 33 to 276 US tons with a 15.7″ stroke. The CFS is the simpler press with a pressure transmitter, light barrier and two-hand control. The CFSS encloses the work area with guards and a light barrier for production with smaller dies. The CFDD adds a die cushion of 11 to 110 US tons in the lower table and an ejector, for deep drawing on a C-frame."},
         FAQ_CUSHION, FAQ_TO_ORDER, FAQ_LINES, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about C-frame hydraulic presses",
    related_pages=[{"href": "hydraulic-punching-machines.html", "label": "Hydraulic punching machines"}, {"href": "riveting-machine.html", "label": "Orbital riveting machines"},
                   {"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"}],
    related_title="More pressing and bending machinery from NovoTech",
)

STRAIGHT = dict(
    title="Hydraulic Straightening Press for Sale in Canada — Portal, 3-Axis & Sliding-Table Presses, 22 to 441 US Tons | NovoTech",
    meta="Hydraulic straightening presses sold, installed and supported in Canada: premium-line HSPS portal presses 110 – 441 US tons, DK-S 3-axis moving presses 220 – 441 US tons, and value-line HP-M1 sliding-table presses 22 – 220 US tons.",
    h1="Hydraulic straightening presses — portal, 3-axis and sliding-table presses, 22 to 441 US tons",
    intro="A straightening press leaves the workpiece lying still on the bed and brings the ram to the bend: the cylinder travels along "
          "a gantry and the gantry along the bed, or the press head moves on three axes, so a long beam, a plate, a rail, a shaft or a "
          "pipe is straightened point by point without craning it under a fixed ram. NovoTech's premium line, built in Turkey, has two "
          "families, small to large: the HSPS portal (gantry) straightening presses from 110 to 441 US tons, with beds from 39.4 × 78.7″ "
          "to 59.1 × 137.8″, the cylinder travelling along the gantry on a rack drive and the gantry along the bed; and the DK-S 3-axis "
          "moving straightening presses from 220 to 441 US tons, whose cylinder moves on X, Y and Z by motorized gear drive over a 100″ "
          "bed, with a remote control as an option; and NovoTech's value line, built in China — the HP-M1 presses from 22 to 220 US tons, "
          "whose table slides out of the frame, so large and heavy parts are loaded outside the press and rolled in. "
          "Each family below has its full specification table and photos. For shafts and bar in "
          "a repair shop, a shop press with a mobile cylinder is often enough. Parts, installation and service from Mississauga, ON, Canada.",
    points=["HSPS portal straightening presses 110 – 441 US tons: beds 39.4 × 78.7″ to 59.1 × 137.8″, stroke 15.7 – 23.6″",
            "DK-S 3-axis moving straightening presses 220 – 441 US tons: the head travels over a 100″ bed, 11.8″ stroke, remote control optional",
            "Value-line HP-M1 presses with a sliding table, 22 – 220 US tons: parts loaded outside the press and rolled in"],
    hero="sh-dks400", minis=["hk-hsps", "sh-dks-remote"],
    faq=[{"q": "Portal (HSPS) or 3-axis (DK-S)?", "a": "Both leave the workpiece on the bed and move the ram to the bend. The HSPS is a gantry that runs along the bed on a rack drive, with beds to 59.1 × 137.8″ — the choice for long beams, rails and plate. The DK-S carries its cylinder on X, Y and Z over a 100″ bed with motorized gear drives, from 220 to 441 US tons, for heavy plate, beams, profiles and round bar."},
         {"q": "Which press for my parts?", "a": "It depends on the section, the material and the distance between the supports: the press has to bend the part slightly past straight. Send us the profile or the shaft diameter, the material grade, the length and how far it is out of straight, and we size the press, the bed and the supports."},
         {"q": "Can a shop press straighten too?", "a": "Yes, for shafts, bar and smaller sections that can be moved under the ram. The DPM-K and DK shop presses carry the cylinder across the frame on a hand wheel, so a shaft or a frame rail stays clamped while it is straightened point by point. For beams, plate and parts too heavy or too long to move, a straightening press brings the ram to the work."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about hydraulic straightening presses",
    related_pages=[{"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"},
                   {"href": "angle-rolls.html", "label": "Angle rolls"}],
    related_title="More heavy fabrication machinery from NovoTech",
)

RIVET = dict(
    title="Riveting Machines for Sale in Canada — Hydraulic Orbital Riveting Machines, Rivets to Ø1-3/16″ | NovoTech",
    meta="Orbital riveting machines sold, installed and supported in Canada: NovoTech value-line XM-5 to XM-30 hydraulic orbital riveters for solid rivets from Ø3/16″ to Ø1-3/16″, 1,911 to 22,481 lbf.",
    h1="Riveting machines — hydraulic orbital riveters for solid rivets Ø3/16″ to Ø1-3/16″",
    intro="An orbital (rolling) riveting machine forms the head of a solid rivet by rolling the rivet end into shape instead of hammering "
          "it, with about a tenth of the force of punch riveting: the part keeps its fit and the head comes out smooth, without vibration "
          "or noise. It replaces hammering, punching and hot riveting on hinges, chain links, brake parts, appliances and hardware, and with "
          "other tools the machine works as a normal press. NovoTech's value-line XM riveters, built in China, come in six sizes, small to "
          "large, for solid rivets from Ø3/16″ (XM-5, 1,911 lbf) to Ø1-3/16″ (XM-30, 22,481 lbf), with 11 rivet head forms and tables from "
          "Ø4.7″ to 19.7 × 14″. The specification table and photo are below. Parts, installation and service from Mississauga, ON, Canada.",
    points=["XM-5 to XM-30 orbital riveters: solid rivets Ø3/16″ to Ø1-3/16″, 1,911 – 22,481 lbf",
            "11 rivet head forms; tables Ø4.7″ to 19.7 × 14″; works as a normal press with other tools",
            "Low noise, no vibration — replaces hammering, punching and hot riveting"],
    hero="tm-xm8", minis=[],
    faq=[{"q": "Which XM riveter for my rivet?", "a": "Choose by the largest solid rivet you set: XM-5 to Ø3/16″, XM-8 to Ø5/16″, XM-10 to Ø3/8″, XM-16 to Ø5/8″, XM-20 to Ø13/16″ and XM-30 to Ø1-3/16″. Send us a drawing of the part and the rivet and we confirm the size and the head form."},
         {"q": "Orbital riveting or pressing the rivet?", "a": "Pressing or punching sets the whole head at once and needs about ten times the force, which can distort the part and loosen the fit. The orbital head rolls the rivet end outward a little at a time, so the force stays low, the head comes out smooth and the part keeps its fit — the reason it is used for hinges, chain links and brake parts."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about riveting machines",
    related_pages=[{"href": "hydraulic-press.html", "label": "Hydraulic press"}, {"href": "hydraulic-shop-press.html", "label": "Hydraulic shop presses"},
                   {"href": "c-frame-hydraulic-press.html", "label": "C-frame hydraulic presses"}, {"href": "drill-press.html", "label": "Drill presses"}],
    related_title="More machinery from NovoTech",
)

HUB_PAGE = dict(
    title="Hydraulic Press for Sale in Canada — Hydraulic Presses: Shop, H-Frame, C-Frame & Straightening | NovoTech",
    meta="Every hydraulic press NovoTech sells in Canada, by kind: shop and bench presses from 10 to 551 US tons, H-frame and four-column production presses to 661 US tons (3,307 to order), C-frame presses to 276 US tons and straightening presses to 441 US tons — every model in one table.",
    h1="Hydraulic press — shop, H-frame, C-frame and straightening hydraulic presses",
    intro="A hydraulic press drives its ram with an oil cylinder — slowly, with the full force available anywhere in the stroke and a "
          "pressure you set — which is why the same kind of machine presses bearings, straightens shafts, bends plate and punches, forms "
          "and deep-draws sheet in a die. NovoTech sells four kinds in Canada, each on its own page: hydraulic shop presses — the H-frame "
          "workshop press of every repair shop, dealer and fabricator, from a 10-ton bench press to 551 US tons; H-frame hydraulic presses "
          "— straight-side and four-column production presses for dies, deep drawing and composite moulding, from 55 to 661 US tons and "
          "to 3,307 US tons to order; C-frame hydraulic presses — open on three sides for small dies, punching and assembly, from 22 to "
          "276 US tons; and hydraulic straightening presses — portal and 3-axis presses whose cylinder travels to the bend over beams, "
          "plate and shafts, from 22 to 441 US tons. The premium line is built in Turkey with European hydraulics and Siemens controls, "
          "the value line in China for the repair shop and lighter production. Below, "
          "the four kinds compared, every model in one table, the buying guide and the questions we get asked; every press comes with a "
          "CSA-approved panel and support from Mississauga, ON, Canada.",
    points=['<a href="hydraulic-shop-press.html">Hydraulic shop presses</a>: premium-line <a href="hydraulic-shop-press.html#sahinler-dpm">DPM</a> , <a href="hydraulic-shop-press.html#sahinler-dpm-k">mobile-cylinder DPM-K / DK</a>, <a href="hydraulic-shop-press.html#sahinler-at">AT</a> and <a href="hydraulic-shop-press.html#sahinler-ap">AP</a>, 33 – 220 US tons; value-line <a href="hydraulic-shop-press.html#tt-ebp10t">bench</a> and <a href="hydraulic-shop-press.html#tt-shop-hs">workshop presses</a>',
            '<a href="h-frame-hydraulic-press.html">H-frame hydraulic presses</a>: premium-line <a href="h-frame-hydraulic-press.html#nt-press-hsa">HSA</a>, <a href="h-frame-hydraulic-press.html#nt-press-hdd">HDD deep drawing</a> and <a href="h-frame-hydraulic-press.html#nt-press-hcfp">HCFP four-column</a> to 661 US tons; value-line <a href="h-frame-hydraulic-press.html#tt-hp-f">HP-F four-column</a>',
            '<a href="c-frame-hydraulic-press.html">C-frame presses</a> 22 – 276 US tons · <a href="hydraulic-straightening-press.html">straightening presses</a> 22 – 441 US tons'],
    hero="sh-dpm", minis=["hk-hsa", "hk-cfss"],
    range_cols=["Force", "Stroke", "Table / working width", "Motor", "Weight"],
    range_lead="Every hydraulic press NovoTech sells, in one table: force, stroke, table or working width, motor and weight. Each row links to the full specification table on its page.",
    range_caption="Hydraulic presses supplied by NovoTech — shop, H-frame, four-column, C-frame and straightening presses",
    range_note="Forces in US tons with metric tons in brackets. Three-phase presses are supplied for 600 V as standard with a CSA-approved panel; 208, 240 and 480 V on request. Larger tables, strokes and tonnages to order on the premium line.",
    faq=[{"q": "Which kind of hydraulic press do I need?",
          "a": "By the work. For pressing bearings, bushings and pins, straightening shafts and bending flat bar one part at a time, a shop press. For dies — forming, blanking, coining, deep drawing — run cycle after cycle under PLC control, an H-frame or four-column press, or a C-frame press when the dies are small and quick access matters more than table size. For beams, plate and long parts straightened where they lie, a straightening press with a moving cylinder. Send us the part and the force and we size the press."},
         FAQ_TONNAGE, FAQ_FRAMES, FAQ_LINES, FAQ_TO_ORDER, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about hydraulic presses",
    related_pages=[{"href": "riveting-machine.html", "label": "Orbital riveting machines"}, {"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"},
                   {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "hydraulic-punching-machines.html", "label": "Hydraulic punching machines"}],
    related_title="More pressing and bending machinery from NovoTech",
)

COMPARE = {
    "title": "Which kind of hydraulic press?",
    "lead": "The four kinds NovoTech sells, side by side; each page lists every model of its kind.",
    "cols": ["", "Shop presses", "H-frame presses", "C-frame presses", "Straightening presses"],
    "rows": [
        ["Frame", "Welded H-frame, open front; the table set at height", "Straight-side H-frame or four columns, machined monoblock",
         "Open on three sides — a C-shaped gap", "Portal (gantry) or 3-axis head; the cylinder travels over the bed"],
        ["Control", "Joystick or hand pump, one part at a time", "PLC with programmed speed, pressure and dwell; light barriers",
         "Two-hand control or PLC; light barrier", "At the bend, by pendant or remote control"],
        ["Force", "10 – 551 US tons", "55 – 661 US tons, to 3,307 to order", "22 – 276 US tons", "22 – 441 US tons"],
        ["Typical work", "Bearings, bushings and pins; straightening shafts; bending flat bar",
         "Dies: forming, blanking, coining, deep drawing; composite moulding", "Small dies, punching, assembly and press-fitting",
         "Beams, plate, rails, shafts and pipe straightened where they lie"],
        ["Page", {"href": "hydraulic-shop-press.html", "label": "Hydraulic shop presses"}, {"href": "h-frame-hydraulic-press.html", "label": "H-frame presses"},
         {"href": "c-frame-hydraulic-press.html", "label": "C-frame presses"}, {"href": "hydraulic-straightening-press.html", "label": "Straightening presses"}],
    ],
}

RANGE_PICK = [["force", "capacity"], ["stroke", "travel", "piston_travel_table_travel"],
              ["table", "width", "working_width_max", "table_table_travel", "throat_depth"], "motor", "weight"]

PAGE_EXTRA = {
    P_SHOP: {"catalogue_pdfs": [PDF_SHOP], **SAHINLER_INTRO_VIDEO,
             "hero_brand_line": "Premium-line shop presses are built in Turkey for NovoTech's premium line; the value-line presses are built in China — all to NovoTech's specification and sold, installed and supported in Canada by NovoTech."},
    P_H: {"catalogue_pdfs": [PDF_PROD, PDF_SHOP], **SAHINLER_INTRO_VIDEO, "hero_brand_line": LINE_TR_CN},
    P_C: {"catalogue_pdfs": [PDF_PROD], **NO_VIDEO, "hero_brand_line": LINE_TR_CN},
    P_STR: {"catalogue_pdfs": [PDF_PROD, PDF_SHOP], **SAHINLER_INTRO_VIDEO,
            "hero_brand_line": LINE_TR_CN, "origin_feature": ORIGIN_TR_CN},
    P_RIV: {"catalogue_pdfs": [], **NO_VIDEO,
            "hero_brand_line": "NovoTech's value-line riveting machines are built in China to NovoTech's specification and sold, installed and supported in Canada by NovoTech.",
            "origin_feature": {"title": "Value line from China", "text": "Built in China to NovoTech's specification — CSA-approved panels, a 1-year warranty and parts and support in Canada."}},
}


def families():
    sets = {s: json.load(open(os.path.join(ROOT, "content", "families", f"{s}.json"), encoding="utf-8"))["families"] for s in SOURCES}
    out = []
    for page, gid, _, brand, ids in GROUPS:
        for fid in ids:
            src = next((sets[s][fid] for s in SOURCES if fid in sets[s]), None)
            if src is None:
                raise SystemExit(f"press_pages: no family {fid}")
            if (src.get("brand") in PREMIUM) != (brand in PREMIUM):
                raise SystemExit(f"press_pages: {fid} ({src.get('brand')}) in group {gid} ({brand})")
            f = dict(src, id=fid, page=page, group=gid)
            if f.get("brand") in PREMIUM:
                f["brand"] = "novotech-premium"
            if fid in IMAGE_ORDER:
                if sorted(IMAGE_ORDER[fid]) != sorted(f["images"]):
                    raise SystemExit(f"press_pages: IMAGE_ORDER {fid} is not the family's photos {f['images']}")
                f["images"] = IMAGE_ORDER[fid]
            out.append(f)
    return out


def build():
    fams = families()
    write_families(SET, fams)
    for slug, page in ((P_SHOP, SHOP), (P_H, HFRAME), (P_C, CFRAME), (P_STR, STRAIGHT), (P_RIV, RIVET)):
        members = [f for f in fams if f["page"] == slug]
        groups = [(gid, title, "", brand) for pg, gid, title, brand, _ in GROUPS if pg == slug]
        extra = {"catalogue_pdf": None, "origin_feature": ORIGIN_TR_CN, **PAGE_EXTRA[slug]}
        if slug == P_RIV:
            extra["nav_label"] = "Riveting machines"
            write_category(slug, dict(page, groups=groups), members, SET, "Riveting machines", extra=extra)
        else:
            extra["nav_label"] = next(nav for s, _, _, _, nav in SUBPAGES if s == slug)
            write_category(slug, dict(page, groups=groups), members, SET, SECTION, hub=hub(), siblings=siblings(), extra=extra)
        print(f"{slug}: {len(members)} families, {sum(len(f['specs']['models']) for f in members)} models")
    in_range = [f for f in fams if f["page"] != P_RIV]
    write_hub(HUB, {**HUB_PAGE, "artifact_title": "Hydraulic Press", "nav_label": "All hydraulic presses", "related_blurb": hub()["blurb"]},
              in_range, SET, SECTION, [(s, t, im, b, nav) for s, t, im, b, nav in SUBPAGES],
              extra={"catalogue_pdf": None, "catalogue_pdfs": [PDF_SHOP, PDF_PROD], "range_pick": RANGE_PICK,
                     "hero_brand_line": "The premium-line presses are built in Turkey with European hydraulics and Siemens controls; the value-line presses and riveters are built in China — all to NovoTech's specification and sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Four kinds, two lines, one supplier", "text": "Shop, H-frame, C-frame and straightening presses from NovoTech's premium line, built in Turkey, and its value line, built in China — installed, trained and supported by the same NovoTech technicians in Canada."},
                     **SAHINLER_INTRO_VIDEO, "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"],
                     "hub_compact": True, "compare": COMPARE, "subpage_link": "all models, specifications and photos",
                     "related_title_": "More hydraulic presses from NovoTech"})      # the section pages' related heading (build.py)
    path = os.path.join(ROOT, "content", "pages", f"{HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp in page["subpages"]:
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — every family"
    write_json(path, page)
    print(f"hydraulic press hub: {len(in_range)} families on {len(page['subpages'])} pages · riveting page: {sum(1 for f in fams if f['page'] == P_RIV)} family")


if __name__ == "__main__":
    build()
