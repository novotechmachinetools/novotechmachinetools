#!/usr/bin/env python3
"""NovoTech value-line machines built by TTMC — families added as value-line groups to EXISTING pages (cold saws, aluminum saws,
corner notchers, ironworkers, angle rolls, bead rollers, tube notchers, hydraulic presses, circle shears, compact press brakes,
horizontal press brakes, plate rollers, deburring machines, welding positioners) and the EBQ01 motorized bench shears and the
PS-1220 coil slitter on sheet-metal-shears.html.
Manual machines are not sold (see the scope note in ttmc_more_data.py): the families pick only the powered models.
"""
from ttmc_conv import pick
from ttmc_more_data import F, MANUAL_TAG, NOTE, NOTE_HZ  # noqa: F401
import ttmc_more_tables as TT
import ttmc_new_tables as TN

T = TT.TAB
NT = TN.TAB          # 2026 new items, welding positioners and supports

# =============================================================================================== cold saws & abrasive saws
P_COLD = "circular-cold-saws"
COLD = [
    F("tt-cs", P_COLD, "tt-cold", "CS cold saws, 9 – 14″ blade, cut Ø2-3/8 – 4-3/4″", "CS cold saws", T["tt-cs"],
      "Gear-driven cold saws for clean, burr-free cuts in tube, bar and profiles. The CS-225, CS-250 and CS-275 run a 9 – 11″ blade at "
      "42 – 46 rpm through a gearbox in an oil bath, with a 24 V hold-to-run control and a vise with an anti-burr device, and swivel 45° "
      "left and right; the CS-315 and CS-350 on stands take 12-1/2 and 14″ blades, cut Ø3-7/8 and 4-3/4″ round, run at two speeds "
      "(18 / 36 rpm) and clamp in a quick-adjusting double vise.",
      ["Round capacity at 90°: Ø2-3/8″ (CS-225, CS-250) to Ø4-3/4″ (CS-350); rectangular to 5-1/2 × 3-7/8″",
       "Head swivels 45° left and right; angle cuts at 45° to Ø4-1/8″", "Gear drive; reduction unit in an oil bath (CS-225 – 275); two blade speeds (CS-315, 350)",
       "24 V low-voltage hold-to-run control; vise with anti-burr device; double vise on the CS-315 and 350",
       "CS-315 / 350: 1 / 1.7 HP two-speed 3-phase or 1.5 HP single-phase motor"],
      ["tm-cs", "tm-cs-250", "tm-cs-225"], headline="Ø2-3/8 – 4-3/4″ round", cap="[Blade diameter, max] blade · cuts [Round, 90°] round", note=NOTE_HZ),
    F("tt-pds315h", P_COLD, "tt-cold", "PDS-315H semi-automatic hydraulic cold saw, 12-1/2″ blade", "PDS-315H semi-automatic", T["tt-pds315h"],
      "The semi-automatic cold saw: hydraulic clamping and a hydraulic feed cylinder make the cut — the operator loads the bar and "
      "presses start. A 12-1/2″ blade at 60 or 120 rpm, a saw frame that swivels ±45°, a double vise, coolant and 24 V DC controls; "
      "Ø3-1/2″ round and 3-1/8″ square tube at 90°.",
      ["Ø3-1/2″ (90 mm) round and 3-1/8 × 3-1/8″ tube at 90°; Ø3-1/8″ at 45°", "Automatic cutting cycle: hydraulic feed and hydraulic clamping",
       "Two-speed 3 / 4 HP motor, 60 / 120 rpm", "Saw frame swivels ±45°; double vise; coolant system"],
      ["tm-pds315h"], headline="Ø3-1/2″ round", cap="[Blade diameter, max] blade", note=NOTE_HZ),
    F("tt-pds400", P_COLD, "tt-cold", "PDS-400 heavy-duty cold saw, 16″ blade", "PDS-400 heavy-duty", T["tt-pds400"],
      "The heavy-duty manual cold saw for structural sections: a 16″ blade at 20 or 40 rpm on a compact cabinet stand, a head that "
      "swivels 60° right and 45° left, and capacities up to Ø4-3/4″ round tube, 5-7/8 × 3″ channel and 4-1/2 × 4-1/2″ angle at 90°.",
      ["Ø4-3/4″ round tube, 4-3/8″ square tube, 5-7/8 × 3″ channel and flat bar, 4-1/2″ angle at 90°", "Miter cuts 45° left and 60° right",
       "Two-speed 3 / 3.75 HP motor, 20 / 40 rpm", "Electric power control; manual vise feed"],
      ["tm-pds400"], headline="Ø4-3/4″ round tube", cap="[Blade diameter, max] blade", note=NOTE_HZ),
    F("tt-tv", P_COLD, "tt-abrasive", "TV abrasive cut-off saws, 12 – 16″ wheel, and SQ-40-1 portable saw", "TV abrasive saws", T["tt-tv"],
      "Abrasive cut-off saws on stands for fast square and miter cuts in tube, pipe, angle, flat and solid steel — construction, plumbing, "
      "electrical and petrochemical work: 12, 14 and 16″ wheels on belt drives with 5.5 – 7.5 HP, a vise with an anti-burr device and a "
      "24 V hold-to-run control. The SQ-40-1 is a portable 16″ saw on wheels.",
      ["Ø3-7/8″ (TV-300) to Ø5-1/2″ (TV-400, SQ-40-1) round at 90°", "Miter cuts to 45°; vise opening 7.5 – 8.7″",
       "Belt drive; 5.5 – 7.5 HP; wheel speed 3,200 – 5,400 rpm", "24 V low-voltage hold-to-run control; anti-burr vise"],
      ["tm-tv", "tm-tv-sq"], headline="Ø3-7/8 – 5-1/2″ round", cap="[Wheel diameter, max] wheel · [Round, 90°] round", note=NOTE_HZ),
    F("tt-stand", P_COLD, "tt-stands", "Roller stands, roller conveyors and measuring roller tables", "Roller stands and tables",
      [pick(T["tt-stand"][0], ["RV1100", "RB1100", "RB1000", "RB365", "RB2000", "RA785"])] + NT["tt-stand2"],
      "Material support for saws, shears, brakes and drills: V-roller and flat roller stands, a tripod stand, roller conveyors in 41″ "
      "sections with 79″ and 118″ extensions, the RB365×3000D — a 120″ roller conveyor on a closed steel frame with a length stop that "
      "reads out digitally — the SRB-320 roller stands, 39″ and 79″ long, with adjustable vertical side rollers that guide the bar, and "
      "the RA785 roller table with a measuring feed system that positions the bar to ±0.012″ at 40 – 140 in/min.",
      ["Height-adjustable stands 23 – 43″; loads to 728 lb", "Roller conveyors 1,323 – 1,543 lb; extensions of 79″, 118″ and more",
       "RB365×3000D: 120″ conveyor with a digital length stop, 882 lb", "SRB-320×1000D / 2000D: 39″ and 79″ stands with vertical side rollers, 1,323 lb",
       "RA785: 79″ roller table with measuring feed, ±0.012″ (0.3 mm)"],
      ["tm-stand-ra785", "tm-rb3653000d", "tm-srb3202000d", "tm-stand-rb365", "tm-stand-rv", "tm-rb3653000d-stop"],
      headline="Stands, conveyors and roller tables", cap="[Type]", manual=True),
]

P_ALU = "aluminum-and-pvc-upcut-saws"
ALU = [
    F("tt-qcs400", P_ALU, "tt-alu", "QCS-400 · QCS-500A aluminum cut-off saws, 16″ and 20″ blade, pneumatic clamping", "QCS aluminum saws",
      T["tt-qcs400"] + NT["tt-qcs500a"],
      "Saws for aluminum profiles at 2,800 rpm with fast pneumatic clamping and a pneumatic cylinder that brings the blade down at a "
      "controlled speed: the QCS-400 and QCS-400A have a 16″ blade that swivels 45° left and right for miter cuts in profiles up to "
      "7-7/8 × 3-1/8″; the QCS-500A has a 20″ blade on a head that swivels from 0 to 180° and a 3 HP motor, and cuts profiles up to "
      "10-1/4 × 5-1/8″ at 90° and 9-1/2 × 4″ at 45°.",
      ["QCS-400 / 400A: 16″ blade; Ø4-1/8″ round, 7-7/8 × 3-1/8″ (200 × 80 mm) profiles at 90° and 45°; 1.5 HP",
       "QCS-500A: 20″ blade; Ø6-11/16″ round; 10-1/4 × 5-1/8″ at 90°, 9-1/2 × 4″ at 45°; 3 HP",
       "Blade swivels ±45° (QCS-400) or 0 – 180° (QCS-500A)", "Pneumatic clamping vise; pneumatic feed cylinder; belt drive, 2,800 rpm"],
      ["tm-qcs500a", "tm-qcs400a", "tm-qcs400", "tm-qcs500a-vise"], headline="Profiles to 10-1/4 × 5-1/8″", cap="[Rectangular, 90° and 45° left and right]", note=NOTE_HZ),
]

# =============================================================================================== notchers
P_CORNER = "corner-notcher"
CORNER = [
    F("tt-hnm", P_CORNER, "tt-notch", "HNM-6 · HNM-6A hydraulic corner notchers, 1/4″", "HNM-6 hydraulic notchers", T["tt-hnm"],
      "Hydraulic corner notchers for 1/4″ plate: the HNM-6 cuts a fixed 90° notch 9.8 × 9.8″ in 6.5 mm at 24 strokes a minute, with "
      "automatic blade clearance, a sheet hold-down and a chute that takes the drop away; the HNM-6A sets any angle from 30 to 135° by "
      "hand wheels, punches holes up to Ø1-9/16″ and has gauges for locating the sheet.",
      ["1/4″ (6 – 6.5 mm) mild steel; 5.5 HP", "HNM-6: fixed 90°, 9.8 × 9.8″ (250 × 250 mm) notch, 24 strokes/min",
       "HNM-6A: adjustable 30 – 135°, 7.9″ (200 mm) blades, punching to Ø1-9/16″ (40 mm)", "Automatic blade clearance; sheet hold-down"],
      ["tm-hnm6", "tm-hnm6a"], headline="1/4″ plate", cap="[Notch angle]"),
    F("tt-pnm", P_CORNER, "tt-notch", "PNM-130 · PNM-150 pneumatic corner notchers", "PNM pneumatic notchers", T["tt-pnm"],
      "Free-standing notchers that run on shop air: 90° notches 5-1/8 × 5-1/8″ in 1/8″ mild steel (PNM-130) or 5-7/8″ in 14 ga "
      "(PNM-150), a transparent blade guard that lets the operator line up scribed marks, adjustable stops and guides on both sides of "
      "the blade, a pressure regulator and water trap, a heavy cast-iron table and a roving foot pedal.",
      ["PNM-130: 1/8″ (3 mm) × 5-1/8″; PNM-150: 14 ga (2 mm) × 5-7/8″", "Cast-iron table 23.6 × 18.1″", "Roving foot pedal; regulator and water trap",
       "Transparent blade guard; adjustable stops and guides"],
      ["tm-pnm"], headline="To 1/8″, 90°", cap="[Notch size]"),
]

P_PIPE_NOTCH = "pipe-notcher"
PIPE_NOTCH = [
    F("tt-ptn", P_PIPE_NOTCH, "tt-tube-notch", "PTN-30 hole-saw notcher, UTN40 end-mill notchers and PTN-12U", "PTN / UTN tube notchers",
      [T["tt-notcher"][0]],
      "Motorized notchers that cut the saddle on the end of a tube or pipe so it fits against another for a T or angled joint. The "
      "PTN-30 drives a bi-metal hole saw through a gearbox — 1/2 to 3″ tube and 1/2 to 2-1/2″ schedule 40 pipe at any angle from 0 to "
      "90° with a quick-release cam vise, a taper lock and a large degree wheel; the UTN40 and UTN40V cut with an end mill — fast, without "
      "coolant, dust or noise — on 1/2 to 2″ tube with a swivel vise in 1° steps; the PTN-12U is an electric notcher for 1/4 to 2″ pipe.",
      ["PTN-30: tube 1/2 – 3″ OD, pipe 1/2 – 2-1/2″ schedule 40; 0 – 90°; 3/4 HP; hole-saw arbors 1/2″-20 and 5/8″-18",
       "UTN40: end mill, 1-1/2 HP, 280 rpm; UTN40V: 1 HP DC, 75 – 250 rpm variable", "V-block vise, swivels in 1° steps (UTN40)",
       "PTN-12U: pipe 1/4 – 2″, electric"],
      ["tm-ptn30", "tm-utn40", "tm-utn40v", "tm-ptn12u", "tm-ptn-work"], headline="Tube to 3″", cap="[Capacity]"),
    F("tt-prs", P_PIPE_NOTCH, "tt-prs", "PRS tube and profile end grinders — belt notchers, Ø3/4 – 5-3/4″", "PRS tube end grinders", T["tt-prs"],
      "Belt grinders built to notch tube ends: the tube sits in the adjustable slide and is fed against a contact roller the size of the "
      "mating tube, at any angle from 30 to 90° — a clean, burr-free saddle in steel, stainless and aluminum tube and profiles without "
      "saws or tooling. The PRS-76 models take Ø3/4 – 3″ tube with a 4″ belt, two speeds and forward / reverse on the C; the PRS-150 "
      "takes Ø1-3/8 – 5-3/4″ with a 6″ belt and 7.5 HP and grinds flat and on a contact wheel as well.",
      ["PRS-76A / 76C / 76: tube Ø3/4 – 3″, 4 × 79″ belt, 4 HP or two-speed 3 / 3.75 HP", "PRS-150: tube Ø1-3/8 – 5-3/4″, 6 × 79″ belt, 7.5 HP two-speed, forward and reverse",
       "Notching angle 30 – 90°; contact rollers for 1/2 to 2-1/2″ pipe sizes", "Dust collector connection; flat and contact-wheel grinding too"],
      ["tm-prs", "tm-prs76", "tm-prs76a", "tm-prs150"], headline="Tube Ø3/4 – 5-3/4″", cap="[Belt size] belt", optional=["Contact rollers Ø20, 26, 32, 42, 48, 60 and 76 mm (1/2 – 2-1/2″ pipe)"]),
]

# =============================================================================================== ironworkers
P_IRON = "ironworker-machines"
IRON = [
    F("tt-m55", P_IRON, "tt-iron", "M50 · M55 · M60 compact single-cylinder ironworkers, 50 – 60 tons", "M50 – M60 ironworkers", T["tt-m55"],
      "Compact ironworkers for the small fabrication and repair shop: one cylinder punches, shears flat bar and angle, notches and — with "
      "the optional tooling — brakes, shears round and square bar, notches pipe and punches shaped holes. 50 to 60 tons: a 1″ to "
      "1-1/16″ hole through 5/8″ plate, 12 × 5/8″ flat bar and 4 × 4 × 3/8″ angle on the M60, with a 7-1/2″ throat.",
      ["Punching: 1″ hole in 5/8″ plate (M50), 1-1/16″ in 5/8″ (M55, M60)", "Flat bar: 10 × 1/2″ (M50), 12 × 5/8″ or 14 × 3/8″ (M55, M60)",
       "Angle: 4 × 4 × 1/4″ (M50, M55), 4 × 4 × 3/8″ (M60)", "Standard tooling: 15/16″ punch and die, flat bar shear, angle shear",
       "5.5 – 7 HP; 7-1/2″ throat; 1-1/4″ stroke"],
      ["tm-m55"], headline="50 – 60 tons", cap="[Rated force]",
      optional=["Punch and die sets 3/16 – 1-1/16″", "Right-angle notcher", "Press brake die", "Slot die", "Pipe notcher 3/4 – 2″", "Round pipe shear die",
                "Bar shear die for round, square and angle", "Gauging table kit and fabricator's guard"]),
]

# =============================================================================================== angle rolls / ring rollers
P_ANGLE = "angle-rolls"
RB = T["tt-rbm"]
ANGLE = [
    F("tt-rbm", P_ANGLE, "tt-ring", "RBM40HV – HRBM65 profile benders, Ø1-9/16 – 2-1/2″ shafts", "RBM / HRBM profile benders", [RB[1]],
      "Motorized three-roll profile benders that roll flat bar, square and round bar, angle, channel, tee and square and rectangular "
      "tube into rings and arcs, horizontally or vertically: one combination roll set does every profile in the table. The H models "
      "move the top roll hydraulically; the HRBM65 has Ø2-1/2″ shafts, a hydraulic drive and a mobile control panel and rolls 4-3/4 × "
      "1″ flat bar the easy way and 3-1/8 × 1″ on edge. Rolls for round tube and special profiles — also in nylon — are made to order.",
      ["Shafts Ø1-9/16″ (40 mm), Ø2″ (50 mm) and Ø2-1/2″ (65 mm); 2 – 3 HP; 9 – 9.3 rpm", "Horizontal and vertical operation (HV models)",
       "Hydraulic top roll on the HRBM models", "One standard combination roll set for all listed profiles", "Foot pedal; special rolls (also nylon) to order"],
      ["tm-hrbm50", "tm-rbm40", "tm-hrbm65", "tm-hrbm40", "tm-rbm50", "tm-hrbm-work"], headline="Shafts Ø1-9/16 – 2-1/2″", cap="[Shaft diameter] shafts"),
    F("tt-rbm-small", P_ANGLE, "tt-ring", "ERBM10HV – RBM30HV motorized ring rollers, Ø13/16 – 1-3/16″ shafts", "RBM motorized ring rollers",
      [pick(RB[0], ["ERBM10HV", "RBM20", "RBM30", "RBM30HV"], title="ERBM10HV · RBM20 · RBM30 · RBM30HV", sub="Motorized ring rollers with Ø13/16 – 1-3/16″ shafts")],
      "Small motorized ring rollers for flat bar, square and round bar, light angle, channel and tube — railings, gates, frames and "
      "ornamental work: the ERBM10HV, RBM30 and RBM30HV with a motor and foot pedal — the HV models horizontal and vertical — and the "
      "RBM20 with two driven rolls, an LED readout for the top roll and single-phase or 3-phase power.",
      ["Shafts Ø13/16″ (20 mm) and Ø1-3/16″ (30 mm); 3/4 – 1.5 HP; 8 – 12 rpm", "Flat bar on edge to 1-3/16 × 3/8″, the easy way to 2 × 9/16″",
       "Foot pedal; horizontal and vertical working position on the HV models", "RBM20: LED top-roll readout, two driven rolls, 1-phase or 3-phase"],
      ["tm-rbm30hv", "tm-rbm20", "tm-erbm10", "tm-rbm30", "tm-rbm-rolls"], headline="Shafts Ø13/16 – 1-3/16″", cap="[Shaft diameter] shafts"),
    F("tt-tr", P_ANGLE, "tt-ring", "ETR-50 electric tube roller and CRB-76 decorative ring roller", "ETR-50 / CRB-76 tube rollers",
      [pick(T["tt-tr"][0], ["ETR-50"], title="ETR-50", sub="Electric tube and pipe roller — rings and arcs in round tube, pipe and square tube"), RB[2]],
      "Two motorized rollers for tube and pipe: the ETR-50 rolls 1/2 – 2″ round tube, 1/4 – 1-1/2″ pipe and 1/2 – 1″ square tube into "
      "arcs and rings with CNC-machined dies, a 1/2 HP motor and a foot pedal; the CRB-76 rolls decorative rings and scrolls in round "
      "and square tube and flat bar on formers from Ø5/8 to 3″ — the metal-craft machine for gates, railings and furniture.",
      ["ETR-50: round tube 1/2 – 2″, pipe 1/4 – 1-1/2″, square tube 1/2 – 1″ with optional rolls", "ETR-50: 1/2 HP (0.37 kW) motor, foot pedal, 1- or 3-phase",
       "CRB-76: round tube formers Ø5/8 – 3″, square tube formers 5/8 – 2″, walls 0.02 – 0.08″", "CRB-76: 1.5 HP (1.1 kW)"],
      ["tm-etr50", "tm-crb76", "tm-crb-rolls"], headline="Tube to Ø3″", cap="[Capacity] · [Round tube formers]"),
]

# =============================================================================================== bead rollers
P_BEAD = "bead-rollers"
BEAD = [
    F("tt-etb", P_BEAD, "tt-bead", "ETB-12 · ETB-25 · ETB-40 beading machines, 18 – 8 ga", "ETB beading machines",
      [pick(T["tt-etb"][0], ["ETB-12", "ETB-25", "ETB-40"], title="ETB-12 · ETB-25 · ETB-40", sub="Motorized beading machines with 8 – 12″ throat, 18 ga to 8 ga")],
      "Beading machines for stiffening beads, steps, flanges and offsets in sheet and in the ends of ducts and tanks: the ETB-12 with a "
      "self-braking motor and foot pedal for 18 ga with an 8″ throat; the ETB-25 and ETB-40 on welded steel frames with brake motors, "
      "foot pedals and adjustable idle rolls for 12 ga and 8 ga with 11 and 12″ throats. Four standard roll sets and eight extra profiles.",
      ["18 ga (ETB-12), 12 ga (ETB-25), 8 ga (ETB-40) mild steel", "Throat 8 – 12″", "Brake motor and foot pedal; 1 – 3 HP",
       "4 standard roll sets; 8 extra profiles to order"],
      ["tm-etb25", "tm-etb12"], headline="18 – 8 ga", cap="[Capacity, mild steel] · throat [Throat depth]"),
    F("tt-rm-deep", P_BEAD, "tt-bead", "RM24 · RM36 · RM42 motorized deep-throat bead rollers, 24 – 42″", "RM deep-throat bead rollers",
      [pick(T["tt-etb"][2], ["RM24", "RM-24H", "RM36", "RM-36H", "RM42", "RM-42H"], title="RM24 · RM36 · RM42 · RM-24H · RM-36H · RM-42H",
            sub="Motorized deep-throat bead rollers, 24 – 42″, 20 ga — H models with a 4″ high throat and both shafts driven")],
      "Deep-throat bead rollers for auto body panels, floor pans, doors and HVAC panels: 20 ga steel and 18 ga aluminum with a 24, 36 "
      "or 42″ throat, a variable-speed motor, a foot pedal and forward / reverse. The H models have a 4″ high throat for formed panels "
      "and drive both shafts. Round, flat, step and spoiler bead rolls; the bead depth is adjustable.",
      ["20 ga (1 mm) mild steel, 18 ga (1.2 mm) aluminum", "Throat 24″, 36″ or 42″; 4″ throat height on the H models",
       "Variable-speed motor, foot pedal, forward / reverse; both shafts driven (H)", "Rolls: round bead 1/8 – 1″, flat bead, step 1/16 – 1/4″, 45° step, spoiler 1-1/4″ radius"],
      ["tm-rm36", "tm-rm42h"], headline="24 – 42″ throat", cap="throat [Throat depth]"),
]

# =============================================================================================== hydraulic presses
P_PRESS = "hydraulic-press"
SP = T["tt-shop-press"]
HP = T["tt-hp"]
PRESS = [
    F("tt-shop-hs", P_PRESS, "tt-shop", "HPP-60 · HPP-100 · HPP-160 motorized workshop presses, 66 – 176 US tons", "HPP motorized workshop presses",
      [SP[4]],
      "Motorized H-frame workshop presses for repair, assembly and straightening: a two-step hydraulic unit with a 3 – 4 HP motor and a "
      "double-acting hand pump for fine positioning, a cylinder that moves across the frame, V-block worktables and 16″ of stroke, from "
      "66 to 176 US tons with working widths to 43.3″.",
      ["HPP-60 / 100 / 160: 66, 110 and 176 US tons", "3 – 4 HP; two-step hydraulic unit; 16.1″ (410 mm) stroke",
       "Cylinder moves across the frame; V-block worktable", "Working width 29.5 – 43.3″ (750 – 1,100 mm)"],
      ["tm-hpp100"], headline="66 – 176 US tons", cap="[Force]"),
    F("tt-shop-small", P_PRESS, "tt-shop", "EBP-25T motorized workshop press, 28 US tons", "EBP-25T workshop press",
      [pick(SP[2], ["EBP-25T"], title="EBP-25T", sub="Motorized workshop press with two V-blocks")],
      "A compact workshop press with a motorized pump and infinitely variable pressure and speed — pressing bearings, bushings and "
      "shafts, and straightening on the two V-blocks — for the garage, the farm and the maintenance shop.",
      ["28 US tons (250 kN); 7.9″ (200 mm) stroke", "Motorized pump; infinitely variable pressure and speed; pressure gauge", "Two V-blocks for straightening"],
      ["tm-ebp25t"], headline="28 US tons", cap="[Force]"),
    F("tt-ebp10t", P_PRESS, "tt-shop", "EBP-10T hydraulic bench press for sheet-metal tooling, 10 tons, 25″ throat", "EBP-10T bench press",
      [pick(T["tt-bench-press"][0], ["EBP-10T"], title="EBP-10T", sub="Hydraulic bench press for punch, flare, bead, louver and bend tooling")],
      "A 10-ton hydraulic bench press for the sheet-metal and HVAC shop: a 25″ throat and a 6″ tool opening take the industry-standard "
      "bench and louver press tooling — punch round, square and oblong holes, punch and flare or punch and bead, cut louvers, notch "
      "corners, bend 90° in 3/8″ mild steel and shear 16 ga — and it works as a hydraulic arbor press as well.",
      ["10 tons hydraulic; 4″ stroke; 25″ throat; 6″ tool opening", "Takes all standard bench press and louver press tooling",
       "Tooling: shear 16 ga, 90° bend 3/8″, corner punch 16 ga, louver punches 1 – 5″, punch & flare and punch & bead 1 – 3″"],
      ["tm-ebp10t", "tm-louver"], headline="10 tons, 25″ throat", cap="[Capacity]",
      optional=["Shear kit", "90° bend kit", "Corner punch and corner radius punch", "Louver punches", "Punch & flare and punch & bead kits", "Universal tool stand"]),
    F("tt-riveter", P_PRESS, "tt-rivet", "XM orbital riveting machines, rivets Ø3/16 – 1-3/16″", "XM orbital riveters", T["tt-riveter"],
      "Hydraulic orbital (rolling) riveters: the riveting head rolls the rivet end into shape instead of hammering it, with about a tenth "
      "of the force of punch riveting — the part keeps its fit, the head comes out smooth, without vibration or noise. Six sizes for "
      "solid rivets from 3/16 to 1-3/16″; with other tools the machine works as a normal press. Hinges, chain links, brake parts, "
      "appliances and hardware.",
      ["Rivets Ø3/16 – 1-3/16″ (5 – 30 mm); 1,911 – 22,481 lbf", "11 rivet head forms", "Tables Ø4.7″ to 19.7 × 14″",
       "Low noise, no vibration; replaces hammering, punching and hot riveting"],
      ["tm-xm8"], headline="Rivets to 1-3/16″", cap="rivets to [Rivet diameter, max]"),
    F("tt-hp-h", P_PRESS, "tt-hp", "HP-30 – HP-500 motorized H-frame hydraulic presses, 33 – 551 US tons", "HP H-frame presses", [HP[0]],
      "Motorized H-frame hydraulic presses for production pressing, forming, straightening and assembly, from 33 to 551 US tons: a "
      "piston stroke of 7.9 – 11.8″ plus 10.6 – 25.6″ of table travel, tables up to 35.4 × 47.2″, the hydraulic unit built on to 88 US "
      "tons and a separate hydraulic station from 110 US tons up. CE equipment, complete guarding, a foot pedal and travel limit switches "
      "are available.",
      ["33, 55, 69, 88, 110, 165, 220, 331, 441 and 551 US tons", "Pressure 3,626 – 4,569 psi (25 – 31.5 MPa)", "Tables 11.8 × 15.7″ to 35.4 × 47.2″",
       "Hydraulic unit built on (HP-30 – HP-80) or separate (HP-100 and up)"],
      ["tm-hp100", "tm-hp30"], headline="33 – 551 US tons", cap="[Force]",
      optional=["CE equipment", "Complete guarding", "Foot pedal switch", "Travel limit switch", "Table lift device (HP-30, 50, 63, 80)"]),
    F("tt-hpb", P_PRESS, "tt-hp", "HPB presses with brake function, 33 – 331 US tons — single and twin cylinder", "HPB brake presses", [HP[1]],
      "H-frame presses set up as press brakes: replaceable top tools, a V-block and a support table with stops, a worktable lifted by a "
      "chain from the main cylinder, on a torsion-proof steel weldment. The HPB models have one cylinder; the D models two cylinders for "
      "bending widths of 47 – 71″, with a synchronizing device as an option and fine adjustment of the angle.",
      ["33 – 220 US tons single cylinder; 33 – 331 US tons twin cylinder (D)", "Tables 11.8 × 15.7″ to 70.9 × 27.6″", "Replaceable top tools, V-block, support table with stops",
       "Angle fine adjustment; synchronizing device optional (D models)"],
      ["tm-hpb1500", "tm-hpb1500d", "tm-hpb580d", "tm-hpb580"], headline="33 – 331 US tons", cap="[Force]"),
    F("tt-hp-m1", P_PRESS, "tt-hp", "HP-M1 hydraulic presses with sliding table, 22 – 220 US tons", "HP-M1 sliding-table presses", [HP[2]],
      "Two-column presses whose table slides out of the frame — load and unload large, heavy parts outside the press and roll them in "
      "for press-fitting or dismantling. 22 to 220 US tons, 11.8 – 15.7″ stroke, tables to 31.5 × 27.6″ with 23.6″ of travel.",
      ["22, 44, 69, 110, 165 and 220 US tons", "Table slides 23.6″ (600 mm) out of the frame", "Daylight 27.6 – 43.3″", "Stroke 11.8 – 15.7″"],
      ["tm-hp150m1", "tm-hp200m1", "tm-hp20m1"], headline="22 – 220 US tons", cap="[Force]"),
    F("tt-hp-c", P_PRESS, "tt-hp", "HP-C C-frame hydraulic presses, 22 – 110 US tons", "HP-C C-frame presses", [HP[3]],
      "Open C-frame presses with access from three sides, for assembling and dismantling complex structures and large parts: 22 to 110 "
      "US tons, 11.8 – 15.7″ stroke, tables to 31.5 × 23.6″.",
      ["22, 33, 55, 69 and 110 US tons", "Open on three sides", "Tables 15.7 × 11.8″ to 31.5 × 23.6″", "Stroke 11.8 – 15.7″"],
      ["tm-hp63c2", "tm-hp30c2"], headline="22 – 110 US tons", cap="[Force]"),
    F("tt-hp-f", P_PRESS, "tt-hp", "HP-F four-column hydraulic presses, 55 – 347 US tons, and HP-F1/PLC presses with touch-screen control",
      "HP-F four-column presses", [HP[4]] + NT["tt-hp-f1plc"],
      "Four-column presses for forming and pressing with an evenly guided slide: 55 to 220 US tons on the HP-F, the heavier F1 models to "
      "347 US tons with tables up to 42.9 × 31.5″, and the HP-F1/PLC presses from 110 to 347 US tons with a PLC touch-screen cabinet, a "
      "foot pedal and a separate hydraulic station; the HP-315FK has a PLC touch-screen control cabinet too.",
      ["55 – 347 US tons", "Tables 15.7 × 23.6″ to 42.9 × 31.5″", "Stroke 11.8 – 15.7″",
       "HP-F1/PLC: PLC touch screen, foot pedal and separate hydraulic station, 110 – 347 US tons", "Separate pump unit; PLC touch screen on the HP-315FK"],
      ["tm-hp315fk", "tm-hp150f1plc", "tm-hp50f"], headline="55 – 347 US tons", cap="[Force]"),
]

# =============================================================================================== circle shears
P_CIRCLE = "circle-cutters-and-seamers"
CIRCLE = [
    F("tt-mcs", P_CIRCLE, "tt-circle", "MCS-1250E motorized circle shear, Ø8 – 49″, 10 ga", "MCS-1250E circle shear", T["tt-mcs"],
      "A motorized circle shear on a solid cast-iron frame that cuts discs from Ø7-7/8 to 49-1/4″ in 10 ga (3.5 mm) sheet: hardened, "
      "regrindable special-steel blades running in bronze bearings, a ball screw that sets the radius with an encoder readout, and "
      "pneumatic clamping of the blank.",
      ["Discs Ø7-7/8 – 49-1/4″ (200 – 1,250 mm) in 10 ga (3.5 mm)", "3 HP main motor and 1.5 HP feed motor", "Ball-screw radius setting with encoder readout",
       "Pneumatic blank clamping; regrindable blades in bronze bearings"],
      ["tm-mcs1250e"], headline="Ø8 – 49″ discs", cap="[Disc diameter]"),
    F("tt-hcs", P_CIRCLE, "tt-circle", "ECS10/10 motorized circle shear and flanging machine, 16 ga, Ø6 – 19-3/4″ discs", "ECS10/10 circle shear",
      [pick(T["tt-hcs"][0], ["ECS10/10"], title="ECS10/10", sub="Motorized circle shear that cuts discs and flanges rims")],
      "A circle shear that also flanges: the ECS10/10 cuts discs from Ø5-7/8 to 19-3/4″ in 16 ga with a two-speed motor and a foot "
      "pedal, then turns a rim up to 5/16″ high with the second roll set — ends for ducts, tanks, lights and dust collectors.",
      ["Discs Ø5-7/8 – 19-3/4″ (150 – 500 mm) in 16 ga (1.5 mm)", "Flanging height to 5/16″ (8 mm); two roll sets: cutting and flanging",
       "1/2 / 3/4 HP (0.37 / 0.55 kW) two-speed motor, foot pedal", "Throat 19.7″ (500 mm)"],
      ["tm-ecs"], headline="Discs Ø6 – 19-3/4″", cap="[Disc diameter]"),
]

# =============================================================================================== press brakes, horizontal benders
P_COMPACT = "compact-hydraulic-press-brakes"     # the compact press brake page under the press-brake hub (Oct 2026)
COMPACT = [
    F("tt-hbv", P_COMPACT, "tt-hbv", "HBV hydraulic bending brakes, 5/32″ × 24 – 48″, 3/16″ × 49″ and 1/8″ × 100″", "HBV hydraulic brakes",
      T["tt-hbv"] + NT["tt-hbv-l"],
      "Small hydraulic brakes for brackets, clips and short parts in plate. The HBV24 and HBV48 push the top beam into a four-way "
      "V-block with 16.5 or 33 US tons for 5/32″ (4 mm) plate over 24″ or 48″, controlled by a hydraulic foot valve; the beam unpins for "
      "closed bends and easy removal of the part, and a back gauge sets the flange from 4.1 to 21.7″. The HBV-1250 and HBV-2540 are "
      "two-cylinder press brakes of 35 US tons for 3/16″ over 49″ and 1/8″ over 100″, with a 5.1″ stroke, an 8.3″ open height, a foot "
      "pedal and a back gauge set by hand wheel with a counter.",
      ["HBV24 / HBV48: 5/32″ (4 mm) × 24″ or 48″; 16.5 / 33 US tons; four-way V-block; hydraulic foot valve",
       "HBV-1250: 3/16″ (5 mm) × 49-1/4″; HBV-2540: 1/8″ (3 mm) × 100″; 35 US tons on two cylinders",
       "Back gauge 4.1 – 21.7″ (HBV24 / 48) or 24-3/8″ with hand wheel and counter (HBV-1250 / 2540)", "Stroke 5.1 – 5.9″"],
      ["tm-hbv1250", "tm-hbv", "tm-hbv1250-gauge"], headline="To 3/16″ × 49″, 1/8″ × 100″", cap="[Bending width × thickness]"),
]

P_HORIZ = "horizontal-press-brake"
HORIZ = [
    F("tt-hb-horizontal", P_HORIZ, "tt-horiz", "HB-10T · HB-25T · HB-40T hydraulic horizontal benders", "HB horizontal benders", T["tt-hb-horizontal"],
      "Hydraulic horizontal benders for flat bar and plate strip: hooks, U-bolts, loops, eyes, brackets and clamps. The HB-10T works by "
      "hand lever on a mobile stand and bends flat bar up to 4-1/2 × 5/16″; the HB-25T and HB-40T bend up to 6-1/4 × 1/2″, with a foot "
      "pedal, a PLC touch screen, a manual back gauge of 33.5″ and a massive ground-steel table. Special tools for pipe and flat bar at any "
      "angle are made to order.",
      ["HB-10T: 11 US tons, flat bar 4-1/2 × 5/16″; hand control; mobile", "HB-25T / HB-40T: 27.6 / 44 US tons, flat bar to 6-1/4 × 1/2″; PLC touch screen; foot pedal",
       "Adjustable pressure with gauge; adjustable stroke", "33.5″ (850 mm) manual back gauge; ground-steel table"],
      ["tm-hb40t", "tm-hb10t", "tm-hb-vee"], headline="11 – 44 US tons", cap="[Bending force]", optional=["Special dies for pipe and flat bar"]),
]

# =============================================================================================== slip rolls
P_ROLL = "motorized-plate-rollers"
SL = T["tt-slip"]
ROLL = [
    F("tt-her", P_ROLL, "tt-slip", "HER hydraulic slip rolls, 12 ga – 1/2″ × 4 – 10 ft", "HER hydraulic slip rolls", [SL[3]],
      "Three-roll slip rolls with all three rolls driven hydraulically: the pinch-roll cylinders move in sync, a digital counter shows "
      "the pinch-roll position, the rolls are alloy steel hardened to HRC 55, the top roll swings out to take off a closed cylinder, and a "
      "foot pedal runs forward and reverse. 1/4″ over 4′3″ to 8′2″, 3/16″ over 5′1″ and 6′8″, 5/16″ over 8′2″, 1/2″ over 6′7″, and "
      "12 – 10 ga over 8′3″ and 9′11″.",
      ["Rolling capacity 12 ga to 1/2″ (2.5 – 12 mm) × 4′3″ – 9′11″", "All three rolls driven hydraulically; pinch rolls synchronized",
       "Digital pinch-roll position counter", "Rolls HRC 55; top roll swings out; forward / reverse foot pedal", "3 – 7.5 HP"],
      ["tm-her", "tm-her2070"], headline="12 ga – 1/2″ × 4 – 10 ft", cap="[Working width] × [Capacity, mild steel]", note=NOTE_HZ),
    F("tt-esr", P_ROLL, "tt-slip", "ESR electric slip rolls, 22 ga – 1/4″ × 3.3 – 10 ft", "ESR electric slip rolls", [SL[2]],
      "Motorized three-roll slip rolls for HVAC, duct and sheet-metal work: a fixed top roll, adjustable lower and rear rolls of "
      "high-strength steel, wire grooves, a top roll that swings out over a cam lock and cone rolling. From the ESR-1020×2 for 14 ga over "
      "40″ to 1/4″ over 51″, 3/16″ over 61″ and 10 ga over 80″ and 10 ft; the E models have a motorized rear roll with a digital "
      "position readout.",
      ["Rolling capacity 22 ga to 1/4″ (0.8 – 6.5 mm) × 40 – 118″", "Fixed top roll, adjustable lower and rear rolls; wire grooves; cone rolling",
       "Foot pedal; 1 – 7.5 HP", "ESR2550 / ESR3050 E: motorized rear roll with digital position readout",
       "Options: hand-wheel adjustment of the rear roll, fast lower-roll adjustment"],
      ["tm-esr", "tm-esr1300e", "tm-esr1020", "tm-esr1300-15e", "tm-esr1300-45", "tm-esr1550", "tm-esr2550e"], headline="22 ga – 1/4″ × 3.3 – 10 ft", cap="[Working width] × [Capacity, mild steel]", note=NOTE_HZ),
]

# =============================================================================================== deburring
P_DEBURR = "sheet-metal-plate-deburring-edge-rounding-finishing-grinding"
DEBURR = [
    F("tt-bfm2560", P_DEBURR, "tt-bfm", "BFM-2560 wide-belt deburring machine, 24″, and WD-1800 wet dust collector", "BFM-2560 wide-belt deburring",
      T["tt-bfm2560"],
      "An entry-level wide-belt machine for deburring and finishing laser-cut, punched and sheared parts: a 25 × 60″ abrasive belt over "
      "a 24″ working width, parts from 0.04 to 6″ thick on a heat-resistant conveyor with variable speed, the table height set digitally "
      "in mm or inch on four synchronized posts, electric-eye belt tracking and a 6″ dust hood. The WD-1800 stainless-steel wet collector "
      "keeps the grinding dust from becoming a fire hazard.",
      ["24″ (600 mm) working width; parts 0.04 – 6″ thick, from 12″ long", "25 × 60″ abrasive belt; 10 HP main motor", "Conveyor 6.6 – 30 ft/min, variable",
       "Digital table height; four-post synchronous lifting; electric-eye belt tracking", "WD-1800: 2,100 CFM stainless-steel wet dust collector, 5 HP"],
      ["tm-bfm2560", "tm-wd1800"], headline="24″ working width", cap="[Working width, max]"),
    F("tt-mgm300", P_DEBURR, "tt-bfm", "MGM-300 finishing and deburring machine, 12″ working width", "MGM-300 deburring machine", NT["tt-mgm300"],
      "A compact finishing machine for small laser-cut, punched and machined parts: a 12 × 41″ abrasive belt over a 12″ working width, "
      "parts from 0.04 to 7-7/8″ thick on a conveyor with variable speed from 4.9 to 23 ft/min, the table height set digitally in mm or "
      "inch on four synchronized posts, electric-eye belt tracking and a 4″ dust extraction port.",
      ["12″ (300 mm) working width; parts 0.04 – 7-7/8″ (1 – 200 mm) thick", "Abrasive belt 12 × 41″ (310 × 1,040 mm); rubber contact roller",
       "Conveyor 4.9 – 23 ft/min (1.5 – 7 m/min), variable", "Digital table height; four-post synchronous lifting; electric-eye belt tracking",
       "4″ dust port; 5.4 HP (4 kW); 1,190 lb"],
      ["tm-mgm300", "tm-mgm300-conveyor"], headline="12″ working width", cap="[Working width, max]"),
]

# =============================================================================================== motorized bench shears (sheet-metal-shears.html, family set "ttmc")
P_SHEAR = "sheet-metal-shears"
SHEAR = [
    F("tt-bq01", P_SHEAR, "sh-light", "EBQ01 motorized bench shears, 18 ga × 26″ and 20 ga × 41″", "EBQ01 bench shears",
      [pick(T["tt-bq01"][0], ["EBQ01-1.25x650", "EBQ01-1.0x1050"], title="EBQ01-1.25x650 · EBQ01-1.0x1050", sub="Motorized bench shears, 18 ga × 26″ and 20 ga × 41″")],
      "Compact motorized shears for the bench: a 1 HP motor drives the blade from a foot switch, so both hands hold the sheet — 18 ga "
      "over 26″ and 20 ga over 41″, with a 19.7″ back gauge, a front angle stop and a working light. For duct parts, flashing, signs "
      "and small panels where a floor shear is more machine than the work needs.",
      ["18 ga (1.25 mm) × 26″ (650 mm); 20 ga (1 mm) × 41″ (1,050 mm)", "1 HP (0.75 kW) motor; foot switch",
       "Back gauge 0 – 19.7″ (0 – 500 mm); front angle stop", "Working light"],
      ["tm-ebq01"], headline="18 – 20 ga × 26 – 41″", cap="[Working width] × [Capacity, mild steel]"),
    F("tt-ps1220", P_SHEAR, "sh-slit", "PS-1220×1.5GT coil slitting and cut-to-length machine, 16 ga × 48″", "PS-1220 coil slitter", NT["tt-ps1220"],
      "A coil line in one machine: the decoiler pays off coil up to 48″ wide and 4,409 lb, the machine feeds it automatically at up to "
      "56 ft/min, rotary knives slit it into strips — two strips in 16 ga, up to seven in thin sheet — and the shear cuts the strips to "
      "length at 35 strokes a minute onto the 120″ outfeed table. For roofing, siding and trim shops, HVAC and duct, and any shop that "
      "buys coil and cuts its own blanks.",
      ["16 ga (1.5 mm) mild steel × 48″ (1,220 mm) wide", "Slits 2 strips in 16 ga, 3 in 20 ga, 5 in 22 ga, up to 7 in 0.5 – 0.6 mm",
       "Automatic feed 0 – 56 ft/min (0 – 17 m/min); shear 35 strokes/min", "Decoiler for 20″ coil ID, 4,409 lb (2,000 kg); outfeed table 120 × 49″",
       "3 HP slitter + 3 HP shear; 4,630 lb"],
      ["tm-ps1220", "tm-ps1220-line", "tm-ps1220-slit"], headline="16 ga × 48″", cap="[Length]"),
]

# =============================================================================================== welding positioners, turning rolls, supports, tables
P_WELD = "welding-positioners"
WT = NT["tt-wtable"]
WELD = [
    F("tt-wp-bench", P_WELD, "tt-wp-small", "MRT-15 · WP-50 · WP-30T benchtop welding positioners, 33 – 110 lb", "Benchtop positioners",
      [NT["tt-wp-bench"][0]],
      "Small positioners for the bench that turn tube, flanges and small parts under the torch at a steady speed, started and stopped "
      "with the foot pedal. The MRT-15 is a rotary table with a 4″ 3-jaw chuck that works horizontal or vertical — for welding, grinding "
      "and cutting — at up to 18 rpm; the WP-50 has an 8″ table with a 3-jaw chuck, a digital speed display and gas purge through the "
      "centre for back-purging stainless tube; the WP-30T a 12-3/8″ table with a 2-9/16″ hollow bore and a hand-wheel tilt.",
      ["Loads 33 lb (MRT-15), 66 lb (WP-30T) and 110 lb (WP-50) horizontal", "MRT-15: 4″ 3-jaw chuck, 0 – 18 rpm, horizontal or vertical",
       "WP-50: Ø8″ table with 3-jaw chuck, 0 – 6 rpm with digital display, gas purge through the centre",
       "WP-30T: Ø12-3/8″ table, 2-9/16″ hollow bore, 0 – 6.5 rpm, hand-wheel tilt 0 – 90°", "Foot pedal on every model"],
      ["tm-wp50", "tm-wp30t", "tm-mrt15", "tm-mrt15-v", "tm-wp50-gas", "tm-wp30t-chuck"], headline="33 – 110 lb", cap="[Load, horizontal / vertical]",
      optional=["3-jaw chuck and torch holder (WP-30T)"]),
    F("tt-wp-chuck", P_WELD, "tt-wp-small", "WP-100T · WP-110 · WP-110T chuck welding positioners, 220 – 247 lb", "Chuck positioners",
      [NT["tt-wp-bench"][1]],
      "Positioners built around an 8″ 3-jaw chuck for tube, pipe, flanges and shafts: 220 – 247 lb on the chuck, 0 – 6 or 0 – 8 rpm, foot "
      "pedal. The WP-100T is a benchtop positioner with a 2-3/8″ hollow bore that tilts 0 – 90° by hand; the WP-110 and WP-110T stand on a "
      "pedestal base, lock at 0, 30, 60 or 90° and run forward, reverse and in auto mode — the WP-110T with a 2-9/16″ hollow bore so long "
      "tube passes through the chuck.",
      ["220 – 247 lb (100 – 112 kg) horizontal, 110 – 121 lb vertical", "8″ (200 mm) 3-jaw chuck; hollow bore 2-3/8″ (WP-100T) and 2-9/16″ (WP-110T)",
       "0 – 6 rpm (WP-100T), 0 – 8 rpm (WP-110, WP-110T)", "WP-110 / WP-110T: tilt locked at 0, 30, 60 or 90°; forward / reverse; auto mode",
       "Foot pedal standard"],
      ["tm-wp110", "tm-wp110t", "tm-wp100t", "tm-wp100t-h", "tm-wp110-panel"], headline="220 – 247 lb", cap="[Load, horizontal / vertical]"),
    F("tt-wp-tilt", P_WELD, "tt-wp-big", "WP-220 · WP-350 · WP-500 · WP-500T tilting welding positioners, 485 – 1,102 lb", "Tilting positioners",
      NT["tt-wp-tilt"],
      "Tilting turntable positioners for flanges, pipe-to-plate joints, hubs, tank heads and wheels: 0 – 5 rpm variable, a table that "
      "tilts from 0 to 135°, foot pedal. The WP-220 and WP-350 carry 485 and 772 lb on a Ø13″ T-slotted table and tilt by hand; the "
      "WP-500 and WP-500T carry 1,102 lb on a Ø21.7″ table with a motorized tilt, the WP-500T with a Ø6-11/16″ hollow chuck for pipe.",
      ["485 – 1,102 lb (220 – 500 kg) horizontal, 220 – 551 lb vertical", "Ø13″ (WP-220, WP-350) and Ø21.7″ (WP-500, WP-500T) tables",
       "0 – 5 rpm, variable; foot pedal", "Tilt 0 – 135°: by hand (WP-220, WP-350), motorized (WP-500, WP-500T)", "WP-500T: Ø6-11/16″ (170 mm) hollow chuck"],
      ["tm-wp500", "tm-wp220", "tm-wp350", "tm-wp500t", "tm-wp500-panel", "tm-wp-sample"], headline="485 – 1,102 lb", cap="[Load, horizontal / vertical]"),
    F("tt-wp-heavy", P_WELD, "tt-wp-big", "WP-1000 · WP-2000 · WP-3000 heavy welding positioners, 3,307 – 8,818 lb", "Heavy positioners",
      NT["tt-wp-heavy"],
      "Heavy positioners for pressure vessels, large flanges, rings and weldments: 3,307 to 8,818 lb on tables of Ø39.4 to 47.2″, "
      "0.1 – 1.2 rpm rotation and a motorized tilt through 135° in 57 seconds, run from a hand pendant and a foot pedal, with "
      "high-frequency protection for TIG welding. Rated with the load's centre of gravity up to 12″ from the table centre and 12″ above "
      "the table.",
      ["3,307 / 5,512 / 8,818 lb (1,500 / 2,500 / 4,000 kg) horizontal", "Tables Ø39.4″, Ø43.3″ and Ø47.2″",
       "Rotation 0.1 – 1.2 rpm; tilt 0 – 135°, motorized, 57 s", "Hand pendant and foot pedal; high-frequency protected", "1 – 2 HP (0.75 – 1.5 kW)"],
      ["tm-wp3000", "tm-wp1000", "tm-wp2000", "tm-wp-heavy-box"], headline="3,307 – 8,818 lb", cap="[Load, horizontal / vertical]"),
    F("tt-wp-acc", P_WELD, "tt-wp-big", "WPC welding chucks and WGS torch holders for the positioners", "Chucks and torch holders", NT["tt-wp-acc"],
      "Accessories for the positioners: WPC self-centring 3-jaw welding chucks that grip parts from Ø0.4″ inside to Ø15″ outside, and "
      "WGS torch holders that clamp the torch on an arm 8.5 to 21.3″ long and a post up to 59″ high, so the bead stays in one place "
      "while the part turns.",
      ["WPC-200 / 300 / 400: outside clamping Ø4.3 – 15″, inside Ø0.4 – 9.8″; centre holes Ø3.1 – 6.7″",
       "Clamping force 441 – 772 lb; part weight to 529 lb", "WGS215 / 370 / 540: arms 8.5, 14.6 and 21.3″; posts 11.8 – 59″"],
      ["tm-wpc", "tm-wgs"], headline="Chucks and torch holders"),
    F("tt-trs", P_WELD, "tt-rolls", "TRS welding turning rolls, 2,205 – 11,023 lb per set", "TRS turning rolls", NT["tt-trs"],
      "Turning rolls (welding rotators) turn pipe, tanks and vessels under a fixed torch for circumferential welds, and for cutting, "
      "grinding and painting: each set is a drive section with a variable-speed motor, a control box and a foot pedal, and an idler "
      "section placed to suit the length of the part. Four sizes carry 2,205 to 11,023 lb per set and work from Ø1-1/2 to 96″, at "
      "surface speeds up to 56 – 143 in/min.",
      ["2,205 / 2,646 / 4,850 / 11,023 lb (1,000 – 5,000 kg) per set", "Work Ø1-1/2 – 24″ (TRS1000) to Ø12 – 96″ (TRS5000)",
       "Surface speed variable, up to 56 – 143 in/min", "One drive and one idler section per set; control box and foot pedal", "Wheels Ø8 – 12″; 150 – 500 W motors"],
      ["tm-trs1000", "tm-trs-pipe", "tm-trs2200", "tm-trs5000"], headline="2,205 – 11,023 lb", cap="[Load per set] per set"),
    F("tt-wtr", P_WELD, "tt-supports", "Pipe stands, pipe supports and pipe jacks for welding, to 19,800 lb", "Pipe stands and supports", NT["tt-wtr"],
      "Supports that hold the far end of a long pipe or vessel while it turns on a positioner or on turning rolls, and stands for fit-up "
      "and cutting: WTR outboard support stands with screw height adjustment for 992 – 9,921 lb; MR pipe stands with roller heads for "
      "6,600 – 15,400 lb and Ø4 – 60″ pipe, the MR3000A with double height adjustment and the MR7000D on three-point legs; MH5500 and "
      "MH9000 pipe supports; and folding pipe jacks with V, ball-transfer or roller heads and low PTR roller stands.",
      ["WTR450 / 2250 / 4500 outboard supports: 992 – 9,921 lb, Ø2 – 48″, 8″ screw height travel",
       "MR pipe stands: 6,600 – 15,400 lb, Ø4 – 60″ pipe, polyurethane-covered steel wheels",
       "MH5500 / MH9000 pipe supports: 12,100 and 19,800 lb, 60″ and 72″ wide",
       "Folding pipe jacks: V-head 2,400 lb, ball-transfer and roller heads 1,000 lb, 28 – 51″ high",
       "PTR roller stands for Ø1/2 – 36″ pipe, 7-1/4 – 43″ high, 1,100 lb"],
      ["tm-mr3000a", "tm-wtr", "tm-mr7000d", "tm-mh5500", "tm-pjv", "tm-ptr185"], headline="To 19,800 lb", cap="[Load, max]", manual=True),
    F("tt-wt3624", P_WELD, "tt-weld-tables", "WT-36X24 mobile welding table with CNC hole pattern", "WT-36X24 welding table", [WT[0]],
      "A mobile fixture table for the fabrication shop: a 36 × 24 × 5/8″ top, flat to 0.006″, with 216 holes of 5/8″ on a 2″ grid for "
      "clamps and fixtures, reversible and nitrided with a black-oxide finish against spatter and rust. It carries 1,500 lb and comes "
      "with a tube and pipe notcher, a drop-down working tray, shelves, leveling feet and casters.",
      ["Top 36 × 24 × 5/8″ (910 × 610 × 16 mm), flat to 0.006″ (0.15 mm)", "216 holes Ø5/8″ (16 mm) on a 2″ (50 mm) grid",
       "Reversible top; nitrided black-oxide finish", "1,500 lb (680 kg) load; leveling feet and casters", "Tube and pipe notcher, drop-down tray and shelves standard"],
      ["tm-wt3624", "tm-wt-notcher"], headline="36 × 24″ top", cap="[Load, max] load", manual=True),
    F("tt-mdt", P_WELD, "tt-weld-tables", "MDT downdraft tables for grinding, sanding and welding fumes, 1,350 – 3,700 CFM", "MDT downdraft tables", [WT[1]],
      "Downdraft tables pull grinding dust, sanding dust and welding fumes down through the perforated top before they reach the "
      "operator. The MDT-4840 and MDT-6137 draw 1,350 CFM through three filter stages — an aluminum pre-filter, a cartridge filter and a "
      "HEPA filter — with compressed-air cleaning of the cartridges on the MDT-4840; the MDT-6022 is a 61 × 20″ grinding table with two "
      "fans moving 3,700 CFM through four panel filters.",
      ["MDT-4840: 46 × 38.7″ table; MDT-6137: 61 × 36.8″; MDT-6022: 61-3/16 × 20″", "1,350 CFM with 3-stage filtration G2 / F7 / H13 (MDT-4840, MDT-6137)",
       "MDT-6022: 3,700 CFM through four panel filters; 1/8″ steel inserts; 78 dB or less", "Table loads 441 – 1,543 lb", "Motors 3/4 – 4 HP (0.55 – 3 kW)"],
      ["tm-mdt4840", "tm-mdt6137", "tm-mdt6022", "tm-mdt-filter"], headline="1,350 – 3,700 CFM", cap="[Air flow]"),
]

GROUP_FAMILIES = COLD + ALU + CORNER + PIPE_NOTCH + IRON + ANGLE + BEAD + PRESS + CIRCLE + COMPACT + HORIZ + ROLL + DEBURR + WELD
