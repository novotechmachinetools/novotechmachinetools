#!/usr/bin/env python3
"""Şahinler-only category pages: angle rolls, ironworkers, punching machines, hydraulic presses, corner notchers and pipe
polishing (family set content/families/sahinler.json).  The Şahinler families that share İşitan pages (plate rolls, SPB draw
benders, SDK / EFM circle cutters) are written by the İşitan modules.

    python3 tools/sahinler_pages.py        # families + pages + image_map entries (tools/sahinler_keys.txt)
    python3 tools/make_images.py --only $(cat tools/sahinler_keys.txt)
"""
import importlib.util
import json
import os

from isitan_lib import CRUMBS, VOLT_FAQ_GENERIC, lower_keep_acronyms, write_json  # noqa: F401
from sahinler_families import *  # noqa: F401,F403
import sahinler_plate_rolls
import hidroliksan_data  # NovoTech premium-line production presses below the Şahinler group on hydraulic-press.html

SET = "sahinler"
PDF_PROD_FILE = "files/NovoTech-Production-Hydraulic-Presses-2026.pdf"


def pdf_prod():
    f = os.path.join(ROOT, "src", PDF_PROD_FILE)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": PDF_PROD_FILE, "label": "Download the production hydraulic presses brochure", "size": size}


PDF_PROD = pdf_prod()
PREMIUM_FAMILIES = [dict(f, pdf=PDF_PROD) for f in hidroliksan_data.FAMILIES]   # their brochure button: the NovoTech production-press brochure
FAMILIES = ANGLE_FAMILIES + IRON_FAMILIES + PUNCH_FAMILIES + PRESS_FAMILIES + PREMIUM_FAMILIES + NOTCH_FAMILIES + POLISH_FAMILIES
SECTION = {P_ANGLE: "Angle rolls", P_IRON: "Ironworkers & punching", P_PUNCH: "Ironworkers & punching", P_PRESS: "Hydraulic presses", P_NOTCH: "Corner notchers", P_POLISH: "Pipe polishing & sanding"}

PAGES = {
    P_ANGLE: dict(
        title="Angle Rolls, Tube Rollers & Section Benders | NovoTech",
        meta="Hydraulic angle rolls and tube rollers from a 2 HP bench bender to HEB 600 beam benders: angle, pipe, tube, flat bar and channel rolled to rings and spirals.",
        h1="Angle rolls, tube rollers and section benders",
        intro="An angle roll (also called a roll bender, section bender, profile bender, ring roller or tube roller) pushes a bar, angle, pipe, tube or beam between three rolls to bend it into an arc, a ring or a spiral — the machine behind curved handrails, tank stiffener rings, rolled flanges, arched trusses and coiled heating pipe. Şahinler builds the complete range: the motorized PK 30 and PK 35 for small flat bar, angle and tube, the hydraulic HPK 40 to HPK 120 section and pipe benders with digital readouts, hydraulic guides and optional NC control, the HPK DP heavy-duty beam benders for channel, I-beam and H-beam up to HEB 600, and the TC-42 NC coiling machine for variable-pitch tube coils. Every machine rolls horizontally or vertically, comes with a standard roll set and takes pipe, tube, angle and special profile rolls; capacity charts for each model are on this page. Sold with a CSA-approved panel, parts and support from Mississauga, ON.",
        points=["PK 30 / PK 35 motorized and HPK 40 – 120 hydraulic angle rolls — pipe to NPS 5, angle to L 4-3/4 × 4-3/4 × 1/2″", "HPK 160 – 360 DP heavy-duty beam benders — IPN 600, UPN 600, HEB 600, pipe to NPS 16", "Digital readouts standard; NC control, hydraulic lateral guides and spiral crane optional; capacity chart per model"],
        hero="sh-hpk100", minis=["sh-hpk60", "sh-hpk160dp"],
        groups=[("sahinler-angle", "Hydraulic section and pipe benders — angle rolls", "From the PK 30 bench bender to the HPK 360 DP beam bender, small to large, each with its section bending capacity chart.", "sahinler"),
                ("sahinler-coil", "Tube coiling machine", "The TC-42 NC for spiral and variable-pitch tube coils with straight ends.", "sahinler")],
        faq=[{"q": "Angle roll, roll bender, section bender, ring roller, tube roller — are these the same machine?", "a": "Yes. All describe the three-roll machine on this page: two driven rolls hold the section and the third roll pushes it into a curve, and a ring is finished by running the piece round again. Each profile — flat bar, angle, square bar, pipe, tube, channel, beam — has its own roll set; the capacity chart under each model lists the largest section it rolls and the smallest diameter it rolls it to."},
             {"q": "How do I read the capacity chart?", "a": "Find your profile in the left column and read the largest section the machine can roll and, after the arrow, the minimum outside diameter it can roll that section to. A second entry gives a smaller section with its tighter minimum diameter. 'Standard rolls' profiles are rolled with the roll set supplied with the machine; 'optional rolls' need the matching roll set. The chart is for mild steel of 37,700 psi yield; stainless, aluminum and high-strength sections need the next model up."},
             {"q": "Which angle roll do I need for 2″ pipe or 2 × 2 × 1/4″ angle?", "a": "The HPK 50 rolls NPS 2 pipe to a Ø39″ ring and L 2 × 2 × 1/4″ angle leg-out to Ø24″; the HPK 60 does the same with more margin and takes NPS 3 pipe and L 2-3/4 × 2-3/4 × 1/4″. For a smaller ring in the same section, or for daily production, step up one size — the minimum diameter shrinks and the rolls last longer."},
             {"q": "Horizontal or vertical — what is the difference?", "a": "The HPK 40 to HPK 120 and the PK 35 work in both positions. Vertical takes less floor space and suits short pieces and rings; horizontal lets long bars, pipe and beams run out over the floor on supports and is the only position on the HPK DP machines. Lateral guide rolls (manual or hydraulic) keep the section square to the rolls and stop twist on angle and channel."},
             {"q": "Can these machines roll spirals and coils?", "a": "Yes. Every HPK with the optional spiral bending crane rolls spiral staircases, stringers and heating coils; the TC-42 NC is the dedicated coiling machine that rolls variable-pitch coils with a straight elbow at each end in one automatic pass."},
             {"q": "Do you supply the rolls for my profile?", "a": "A standard roll set comes with every machine and rolls flat bar, square bar and tee. Pipe, tube, angle, channel and special profile rolls are quoted to your section drawing and shipped with the machine or added later; Delrin rolls are available for polished stainless and aluminum."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about angle rolls",
        related_pages=[{"href": "rotary-draw-tube-benders.html", "label": "Rotary draw tube benders"}, {"href": "hydraulic-3-roll-plate-rollers.html", "label": "Hydraulic 3-roll plate rollers"}, {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"}],
        related_title="More bending machinery from NovoTech",
    ),
    P_IRON: dict(
        title="Hydraulic Ironworker Machines 44–193 Ton | NovoTech",
        meta="Hydraulic ironworkers from 44 to 193 US tons that punch, shear bar, angle and flat and notch: single-piston HKM 40–65, double-piston HKM 55–175 for 2 operators.",
        h1="Hydraulic ironworker machines",
        intro="A hydraulic ironworker (also sold as a steelworker or universal punch and shear) puts the five jobs of the structural shop on one machine: punching, round and square bar shear, angle shear at 90° and 45°, flat-bar and sheet shear and rectangular notching, each with its own station and LED light. Şahinler's HKM range runs from the 44 US ton HKM 40 to the 193 US ton HKM 175 in two designs: single-piston machines in which one cylinder serves every station — compact and economical — and double-piston machines with two cylinders and two foot pedals so two operators punch and shear at the same time. Punches to Ø1-1/2″ are standard on every model; large-hole, section punching, beam and tee blades, V-notching, press-brake and keyway tools are optional. Sold with a CSA-approved panel and installed, tooled and supported from Mississauga, ON.",
        points=["Single-piston HKM 40 · 45 · 60 · 65 V — 44 to 72 US tons, 4 – 5 work stations", "Double-piston HKM 55 · 65 · 85 · 115 · 175 — 61 to 193 US tons, two operators at once", "Angle to L 7-7/8 × 7-7/8 × 13/16″, flat bar to 15 × 1-1/8″, holes to Ø2-1/4″ in 7/8″ plate"],
        hero="sh-hkm115", minis=["sh-hkm60", "sh-hkm175"],
        groups=[("sahinler-iron", "HKM hydraulic ironworkers", "Single-piston and double-piston steelworkers from 44 to 193 US tons, with the punching, shearing and notching capacities of every model.", "sahinler")],
        faq=[{"q": "Single-piston or double-piston ironworker?", "a": "A single-piston machine (HKM 40 – 65 V) uses one hydraulic cylinder for all stations, so one operator works one station at a time — the right choice for a fabrication shop that punches a few holes and cuts a few angles per job. A double-piston machine (HKM 55 – 175) has two cylinders and two foot pedals, so one operator can punch while another shears or notches: twice the output from one machine, plus an electrical back gauge as standard."},
             {"q": "What size ironworker do I need?", "a": "Size it by the thickest material you punch and the largest angle you shear. The punching capacity is quoted as a hole diameter × thickness at the machine's tonnage — a 66 US ton HKM 60 punches Ø1-1/8″ through 9/16″ plate and shears L 4-3/4 × 4-3/4 × 1/2″ angle; the HKM 115 punches Ø1-3/8″ × 1″ and shears L 5-7/8 × 5-7/8 × 5/8″. Tell us your plate thickness, largest angle and flat bar and we will point to the model on the capacity table."},
             {"q": "What tooling comes with the machine?", "a": "A Ø7/8″ punch and die (Ø1″ on the HKM 115), the round and square bar blade set, the angle blade set, the flat-bar shear blades and — except on the HKM 40 — the rectangular notching blade set. Punches and dies to Ø1-1/2″ in any diameter, oblong or square are stocked in Mississauga; large-hole punching sets go to Ø4-7/8″ with the optional tool."},
             {"q": "Can an ironworker cut channel, I-beam and tee?", "a": "Yes, with the optional section blades on the shear station — UPN and IPN sections up to 11-3/4 × 4-7/8″ and tee to 5-7/8 × 9/16″ on the HKM 175 — and the section punching tools punch the flanges and webs of IPN, UPN, flat bar and angle."},
             {"q": "Ironworker or band saw for cutting angle?", "a": "An ironworker shears a 4″ angle in one stroke and a few seconds, with no blade to wear and no chips; the cut is square with a slight deformation at the edge. A band saw takes a minute per cut but leaves a clean, mitre-capable cut on any section. Shops that cut hundreds of angles and flats a day keep both: the ironworker for brackets, clips and base plates, the saw for mitres and beams."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about ironworkers",
        related_pages=[{"href": "hydraulic-punching-machines.html", "label": "Hydraulic punching machines"}, {"href": "angle-rolls.html", "label": "Angle rolls & section benders"}, {"href": "corner-notcher.html", "label": "Corner notchers"}, {"href": "band-saw.html", "label": "Band saws"}],
        related_title="More cutting and punching machinery from NovoTech",
    ),
    P_PUNCH: dict(
        title="Hydraulic Punching Machines, 33 to 193 Ton | NovoTech",
        meta="Hydraulic punching machines for plate, angle and flat bar: single-head HPM 30–175, double-head HPM DP, Siemens CNC punches and NC lines, holes to Ø2-1/4″.",
        h1="Hydraulic punching machines",
        intro="A hydraulic punching machine (hydraulic punch press) makes round, oblong and shaped holes in plate, angle, flat bar and sections with a punch and die in one stroke — faster and cleaner than drilling, with no chips. Şahinler's HPM range starts with the 33 US ton HPM 30 and 44 US ton HPM 40 bench-height punches, continues with the 72 to 193 US ton HPM 65 – 175 with a 24.6″ throat for holes to Ø2-1/4″ in plate to 1-1/4″, and grows into the HPM DP double-head punches for two operators, the HPM CNC with a 120 × 20″ Siemens-controlled table for bolted steel-construction parts and the HPM / HKM NC punching and cutting lines that copy hole patterns along angles, flat bar and beams. Punches and dies interchange with the HKM ironworkers. Supplied with a CSA-approved panel and supported from Mississauga, ON.",
        points=["HPM 30 – 175 single-station punches — 33 to 193 US tons, holes Ø1/4″ to Ø2-1/4″, throat to 24.6″", "HPM DP double-head, HPM CNC with 120 × 20″ Siemens table, HPM / HKM NC feeding lines", "Hydraulic stripper, press-brake tool, large-hole and section punching tools optional"],
        hero="sh-hpm115", minis=["sh-hpm65", "sh-hpm115cnc"],
        groups=[("sahinler-punch", "HPM hydraulic punching machines", "Single-head, double-head, CNC-table and NC-line punches from 33 to 193 US tons.", "sahinler")],
        faq=[{"q": "Punching machine or ironworker?", "a": "If holes are most of the work — base plates, gussets, clips, flat-bar brackets — a dedicated HPM punch has a deeper 24.6″ throat, a free table and a working height set for punching, and it can be fitted with an NC or CNC table. If you also shear angle, bar and flat and notch corners, the HKM ironworker puts all of it on one machine; the punches and dies are the same on both."},
             {"q": "How thick can a hydraulic punch go?", "a": "Each model is rated for a hole diameter × thickness at its tonnage: Ø7/8″ × 3/8″ on the HPM 30, Ø1 × 13/16″ on the HPM 65, Ø1-5/8 × 1-1/4″ on the HPM 175. Larger holes in thinner plate are punched with the large-hole tool up to Ø4-7/8″ × 3/16″. The rule of thumb for mild steel is tonnage = hole circumference × thickness × 25 (US tons, inches)."},
             {"q": "What does the CNC table do?", "a": "The HPM CNC moves the plate under the punch on a 120 × 20″ table with X 63″ and Y 23.6″ travel at ±0.004″, so a hole pattern programmed once — by hand (MDI) or from a CAM file — repeats on every part. It is the machine for bolted steel-construction plates where every hole must line up with the mating member; an optional 3-head unit on the 115 and 175 keeps three tools ready."},
             {"q": "What is an NC punching and cutting line?", "a": "An HPM punch or HKM ironworker with a 307 × 31″ NC feeding table: angles, flat bar and IPN / UPN beams are fed along the X axis to 244″ and the control copies the hole pattern at ±0.004″; on the HKM NC version the shear station then cuts the punched bar to length. It is the economical alternative to a CNC angle line for bracing, towers and ladders."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about punching machines",
        related_pages=[{"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "corner-notcher.html", "label": "Corner notchers"}, {"href": "hydraulic-press.html", "label": "Hydraulic presses"}, {"href": "press-brake-tooling-punch-and-die.html", "label": "Press brake tooling"}],
        related_title="More cutting and punching machinery from NovoTech",
    ),
    P_PRESS: dict(
        title="Hydraulic Presses, Shop to Production 3,307 Ton | NovoTech",
        meta="Hydraulic shop presses from 33 US tons and production presses to 3,307 US tons: H-frame, column, C-frame, deep drawing, SMC hot plate and straightening presses.",
        h1="Hydraulic presses — shop presses, H-frame, C-frame and production presses",
        intro="A hydraulic press machine does the pressing, forming, drawing and straightening work of every repair shop, fabricator and production plant: a hydraulic shop press (H-frame press) presses bearings and pins, straightens shafts and bends plate, and a production press runs a die — forming, deep drawing, blanking, moulding — cycle after cycle under PLC control. Both lines are on this page, small to large. Şahinler's workshop presses come first: DPM shop presses from 33 to 220 US tons with two-speed joystick control, the DPM-K and DK with a cylinder that travels across the frame, the AT T-slot die presses, the AP garage press brake and the DK-S 3-axis straightening presses to 441 US tons. Below them, NovoTech's premium line of production hydraulic presses, built in Turkey with European components: HSA single action and HDD double action deep drawing H-frame presses to 3,307 US tons, HCFP column presses, CFS, CFSS and CFDD C-frame presses, SMC / HHRP hot plate presses for composites and rubber, HSPS portal straightening presses and the HDT Eco H-frame. Every press with a CSA-approved panel, pressure gauge and relief valve, parts and service in Canada.",
        points=["Şahinler shop presses 33 – 441 US tons: DPM, mobile-cylinder DPM-K / DK, T-slot AT, AP press brake, DK-S straightening", "NovoTech premium line production presses: H-frame, column and C-frame to 3,307 US tons, deep drawing with die cushion, hot plate SMC presses", "Siemens PLC, HMI touchscreen and light barriers on the production line; two-speed joystick control on the shop presses"],
        hero="sh-dpm", minis=["hk-hdd", "sh-dks400"],
        groups=[("sahinler-press", "Şahinler hydraulic shop presses", "DPM shop presses first, then the mobile-cylinder DPM-K / DK, the T-slot AT, the AP press brake and the DK-S straightening presses — small to large.", "sahinler"),
                ("novotech-production", "Production hydraulic presses — NovoTech premium line", "Built in Turkey to NovoTech's specification: H-frame single and double action presses to 3,307 US tons, column presses, C-frame and C-frame deep drawing presses, SMC hot plate presses, portal straightening presses and the HDT Eco H-frame — small to large.", "novotech-premium")],
        faq=[{"q": "What tonnage shop press do I need?", "a": "Most truck, equipment and fabrication shops run a 66 – 110 US ton press (DPM 1040-60 to DPM 1570-100): enough for pressing bearings and bushings, straightening shafts to Ø3″ and bending flat bar. Go to 165 – 220 US tons for large bearings, track pins, heavy shafts and forming plate; the DK-S straightening presses from 220 to 441 US tons are for plates, beams and bar that need a moving ram."},
             {"q": "What do the model numbers mean — DPM 1040-60?", "a": "The first number is the clear working width between the columns in millimetres (1040 mm = 40.9″) and the second the press force in metric tons (60 t = 66 US tons). A 1570-100 press is 61.8″ wide at 110 US tons."},
             {"q": "Why a mobile (sliding) cylinder?", "a": "On the DPM-K and DK the cylinder head travels across the frame on a hand wheel, so the ram comes to the work — a long shaft, a frame rail or a plate stays clamped while you straighten it point by point instead of shifting the part under a fixed ram. The DK series adds a wider 61.8″ – 74.8″ frame."},
             {"q": "Can a shop press bend plate?", "a": "The AP garage-type press brake is a hydraulic press delivered with a 5-face prism bottom die and hardened top blade for bending 1/4″ (110 US tons) or 3/8″ (165 US tons) mild steel over 40″ or 60″ — the economical way to bend brackets and short plate without a full press brake. The AT press has T-slot tables for bolting your own forming, blanking and coining dies."},
             {"q": "Hand pump, foot pedal or two-hand control?", "a": "The DPM and DPM-K presses come with two-speed joystick control; a hand pump for fine pressing, a foot pedal and a limit switch that stops the stroke at a set height are options. The AT and AP presses are two-hand controlled with stepless stroke adjustment by limit switch, as die and bending work requires."},
             {"q": "Shop press or production press?", "a": "A shop press is operated by hand — joystick or two-hand buttons — for one part at a time: pressing, straightening, bending. A production press runs a die under PLC control with programmed speeds, pressures, dwell and return, light barriers instead of guards, automatic lubrication and remote diagnostics, for thousands of cycles a shift. The NovoTech premium line starts at 33 US tons with the CFS C-frame and goes to 3,307 US tons on the H-frame presses."},
             {"q": "Single action or double action — what is a die cushion?", "a": "A single action press has one ram. A double action (deep drawing) press adds a die cushion in the lower table — a second cylinder that holds the blank holder with its own programmed force — so a flat blank can be drawn into a deep cup, pan or housing without wrinkling. The HDD H-frame and CFDD C-frame presses have the cushion built in; it is an option on the HCFP column press."},
             {"q": "H-frame, column or C-frame?", "a": "An H-frame (straight-side) press is the stiffest and takes the largest tables and tonnages — the choice for deep drawing and big dies. A column (four-post) press is open on all sides for die access and automation. A C-frame press is open on three sides, so small dies go in and out quickly and the press takes less floor space; its table size is limited because the C deflects, which is why the C-frame range stops at 276 US tons."},
             {"q": "Can the press be built to my die?", "a": "Yes — every series of the premium line is built to order in the table size, stroke, daylight and tonnage the die needs, from a 33 US ton C-frame to a 3,307 US ton H-frame, with quick die change, die loading arms, ejector, heated platens or a die cushion as required. Send us the die drawing and the cycle you need and we quote the press around it."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about hydraulic presses",
        related_pages=[{"href": "hydraulic-punching-machines.html", "label": "Hydraulic punching machines"}, {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "compact-hydraulic-press-brakes.html", "label": "Compact hydraulic press brakes"}, {"href": "horizontal-press-brake.html", "label": "Horizontal press brakes"}],
        related_title="More pressing and bending machinery from NovoTech",
    ),
    P_NOTCH: dict(
        title="Hydraulic Corner Notchers, Fixed & Variable Angle | NovoTech",
        meta="Hydraulic corner notchers that cut a 90° or 30°–140° corner out of sheet to 1/4″ in one stroke: HNM 4F, 6F and 6V with T-slot table and automatic blade gap.",
        h1="Hydraulic corner notchers",
        intro="A corner notcher (notching machine) cuts a square or V-shaped corner out of a sheet in one stroke so the four sides fold up into a box, pan, tray or enclosure on the press brake — the hand-cut, hand-ground corner of the sheet-metal shop done in a second. Şahinler's HNM range: the fixed 90° HNM 4F for 3/16″ and HNM 6F for 1/4″ mild steel with foot-pedal control and a small footprint, and the HNM 6V variable-angle notcher whose blades swing from 30° to 140° on a T-slot table with automatic blade-gap adjustment and four hydraulic hold-downs. Sold with a CSA-approved panel, blades and support from Mississauga, ON.",
        points=["HNM 4F and HNM 6F — fixed 90°, 3/16″ and 1/4″ mild steel, 20 – 25 cuts per minute", "HNM 6V — 30° to 140° variable angle, 1/4″ mild steel, automatic blade gap, T-slot table", "Stainless to 11 ga; blade lengths 7.8″ to 9.8″"],
        hero="sh-hnm6v", minis=["sh-hnm6f"],
        groups=[("sahinler-notch", "HNM hydraulic corner notchers", "Fixed 90° notchers and the variable-angle HNM 6V.", "sahinler")],
        faq=[{"q": "Fixed 90° or variable angle?", "a": "Boxes, pans, trays and enclosures are 90° corners, and the HNM 4F and 6F cut them fastest at 20 – 25 strokes per minute. Hoppers, cones, chutes, duct transitions and any part whose sides are not square need the HNM 6V, whose blades set to any angle from 30° to 140° and whose T-slot table takes stops for repeat positioning."},
             {"q": "What does automatic blade-gap adjustment do?", "a": "Shear blades need a gap that grows with the sheet thickness. On the HNM 6V the gap follows the thickness automatically, so the operator changes from 20 ga to 1/4″ without realigning the blades — and the cut edge stays clean on both."},
             {"q": "Can the notcher cut stainless and aluminum?", "a": "Yes — 14 ga (HNM 4F) or 11 ga (HNM 6F / 6V) stainless, and aluminum up to the mild-steel capacity. Blades are hardened tool steel and are resharpened and shimmed back to size."},
             {"q": "Corner notcher or ironworker notching station?", "a": "The ironworker's rectangular notching station cuts a slot into the edge of bar and plate; the corner notcher cuts the full square corner out of a large sheet laid on its table with a back gauge, at 20 – 30 strokes a minute. Sheet-metal shops that fold boxes daily want the notcher; structural shops are usually served by the ironworker."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about corner notchers",
        related_pages=[{"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "hydraulic-punching-machines.html", "label": "Hydraulic punching machines"}, {"href": "compact-hydraulic-press-brakes.html", "label": "Compact hydraulic press brakes"}, {"href": "folder-sheet-metal-brake.html", "label": "Roofing & pan brakes"}],
        related_title="More sheet-metal machinery from NovoTech",
    ),
    P_POLISH: dict(
        title="Pipe Sanders & Pipe Polishing Machines | NovoTech",
        meta="Pipe sander and polishing machine with automatic feeder: two abrasive belts finish, satin-brush or derust straight and bent pipe and tube, Ø3/8″ to Ø4-1/2″.",
        h1="Pipe sanders and pipe polishing machines",
        intro="A pipe sander (pipe polisher, tube polishing machine) runs abrasive belts around a round pipe or square tube to grind off rust and weld discolouration, give stainless a satin or brushed finish and prepare tube for painting or plating. The Şahinler BT 114-S is the automatic version: a separate feed motor pushes the tube through two 37 × 2″ belts at an inverter-set speed, so the operator loads the pipe and takes the finished length off the other side without turning or holding it — straight tube and bends up to 45°, Ø3/8″ to Ø4-1/2″. The belt speed is variable too, belts change through an opening cover and a holder is provided for manual feeding. Supplied with two belts, a CSA-approved panel and support from Mississauga, ON.",
        points=["Round pipe and square tube Ø3/8″ to Ø4-1/2″ (10 – 114 mm), straight or bent to 45°", "Automatic pipe feeder with its own motor; feeding and belt speed variable by inverter", "Two 37 × 2″ abrasive belts included; 6.4 HP total"],
        hero="sh-bt114s", minis=["sh-bt114s-rail", "sh-bt114s-tube"],
        groups=[("sahinler-polish", "Automatic pipe polishing and sanding machine", "The BT 114-S belt sander with automatic pipe feeder.", "sahinler")],
        faq=[{"q": "What finish does a belt pipe sander give?", "a": "The finish follows the belt: a coarse grit removes rust, scale and weld colour; 180 – 240 grit gives the brushed, satin finish of architectural stainless handrail; finer belts and non-woven belts prepare for mirror polishing. Two belts run at once on the BT 114-S, so a cutting belt and a finishing belt can be fitted together."},
             {"q": "Does it polish bent tube?", "a": "Yes — the belt head and feeder follow bends up to 45°, so handrail elbows and furniture frames are finished after bending instead of before. Tight 90° elbows are finished on the straight sections and blended by hand."},
             {"q": "Round and square tube on the same machine?", "a": "Yes. Round pipe from Ø3/8″ to Ø4-1/2″ is clamped by the manual adjustment and fed through; square tube is passed through flat side by side, two faces at a time. The feeder means the operator never turns the material by hand."},
             {"q": "What about centreless and planetary polishers?", "a": "For long runs of straight stainless tube to a mirror finish a centreless polisher with several heads is the production machine; for a fabrication shop that finishes handrail, furniture and short lengths in mixed sizes the belt sander with feeder is faster to set up and a fraction of the price. Ask us about both."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about pipe polishing",
        related_pages=[{"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Metal deburring & finishing"}, {"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "angle-rolls.html", "label": "Angle rolls & tube rollers"}],
        related_title="More tube machinery from NovoTech",
    ),
}
EXTRA = {"hero_brand_line": BRAND_LINE, "catalogue_pdf": PDF, "origin_feature": ORIGIN}


def load_photos():
    spec = importlib.util.spec_from_file_location("sahinler_photos", os.path.join(ROOT, "tools", "sahinler_photos.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.PHOTOS


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def register_images():
    """Every exported Şahinler / premium-line photo → tools/image_map.json (sections 'sahinler', 'premium-presses');
    the keys are written to tools/sahinler_keys.txt."""
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for section, photos in (("sahinler", load_photos()), ("premium-presses", load_module("hidroliksan_photos").PHOTOS)):
        d = os.path.join(ROOT, "tools", "src-images", section)
        for key, p in photos.items():
            f = [x for x in os.listdir(d) if x.startswith(key + ".")]
            if not f:
                print("!! missing export for", key)
                continue
            ext = os.path.splitext(f[0])[1]
            e = {"src": f"tools/src-images/{section}/{key}{ext}", "alt": p["alt"], "section": section, "trim": ext == ".png", "quality": 82}
            if p.get("cutout") is False:
                e["cutout"] = False
            imap[key] = e
            keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "sahinler_keys.txt"), "w").write(",".join(keys))
    return keys


def write_families_set():
    from isitan_lib import write_families
    write_families(SET, FAMILIES)


def build():
    from isitan_lib import write_category
    write_families_set()
    for slug, p in PAGES.items():
        extra = dict(EXTRA)
        if slug == P_PRESS:
            extra.update({"catalogue_pdf": None, "catalogue_pdfs": [PDF, PDF_PROD]})
            extra.update({"hero_brand_line": "Şahinler shop presses are made in Turkey by Şahinler Metal; the NovoTech premium-line production presses are built in Turkey with European components to NovoTech's specification. All sold, installed and supported in Canada by NovoTech.",
                          "origin_feature": {"title": "Made in Turkey", "text": "Şahinler Metal has built shop presses in Bursa since 1976; the NovoTech premium-line production presses come from a Turkish press builder with 50 years of hydraulic press manufacturing, CE-certified with Siemens controls and European hydraulics."}})
        write_category(slug, p, FAMILIES, SET, SECTION[slug], extra=extra)
    keys = register_images()
    used = {k for f in FAMILIES + sahinler_plate_rolls.FAMILIES + SPB_FAMILIES + CIRCLE_FAMILIES for k in f["images"]} | {p["hero"] for p in PAGES.values()} | {m for p in PAGES.values() for m in p["minis"]}
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on any page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    print(f"sahinler pages: {len(PAGES)} · families: {len(FAMILIES)} · models: {sum(len(f['specs']['models']) for f in FAMILIES)} · images: {len(keys)}")


if __name__ == "__main__":
    build()
