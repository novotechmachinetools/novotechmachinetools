#!/usr/bin/env python3
"""NovoTech value-line machines built by TTMC — families added as value-line groups to EXISTING pages (cold saws, aluminum saws,
corner notchers, ironworkers, angle rolls, bead rollers, tube notchers, hydraulic presses, circle shears, compact press brakes,
horizontal press brakes, plate rollers, deburring machines) and the manual shears on sheet-metal-shears.html.
"""
from ttmc_conv import pick
from ttmc_more_data import F, MANUAL_TAG, NOTE, NOTE_HZ  # noqa: F401
import ttmc_more_tables as TT

T = TT.TAB

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
      ["tm-cs"], headline="Ø2-3/8 – 4-3/4″ round", cap="[Blade diameter, max] blade · cuts [Round, 90°] round", note=NOTE_HZ),
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
    F("tt-stand", P_COLD, "tt-stands", "Roller stands, roller conveyors and RA785 measuring roller table", "Roller stands and tables", T["tt-stand"],
      "Material support for saws, shears, brakes and drills: V-roller and flat roller stands, a tripod stand, roller conveyors in 41″ "
      "sections with 79″ and 118″ extensions, and the RA785 roller table with a measuring feed system that positions the bar to "
      "±0.012″ at 40 – 140 in/min.",
      ["Height-adjustable stands 23 – 43″; loads to 728 lb", "Roller conveyors 1,323 – 1,543 lb; extensions of 79″, 118″ and more",
       "RA785: 79″ roller table with measuring feed, ±0.012″ (0.3 mm)", "RS018 stand for the SS-18 shrinker-stretcher"],
      ["tm-stand-ra785", "tm-stand-rb365", "tm-stand-rv"], headline="Stands, conveyors and roller tables", cap="[Type]", manual=True),
]

P_ALU = "aluminum-and-pvc-upcut-saws"
ALU = [
    F("tt-qcs400", P_ALU, "tt-alu", "QCS-400 aluminum cut-off saws, 16″ blade, pneumatic clamping", "QCS-400 aluminum saw", T["tt-qcs400"],
      "A 16″ saw for aluminum profiles at 2,800 rpm: fast pneumatic clamping, a pneumatic cylinder that brings the blade down at a "
      "controlled speed, and a blade that swivels 45° left and right for miter cuts in profiles up to 7-7/8 × 3-1/8″.",
      ["Ø4-1/8″ (105 mm) round, 7-7/8 × 3-1/8″ (200 × 80 mm) profile at 90° and 45°", "Blade swivels ±45°", "Pneumatic clamping vise; pneumatic feed cylinder",
       "1.5 HP belt drive, 2,800 rpm"],
      ["tm-qcs400"], headline="Profiles 7-7/8 × 3-1/8″", cap="[Rectangular, 90° and 45° left and right]", note=NOTE_HZ),
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
    F("tt-notch-hand", P_CORNER, "tt-notch", "HN hand corner notchers and FN foot notcher", "Hand and foot notchers", T["tt-notch-hand"],
      "Manual 90° corner notchers for sheet and plate in the HVAC and sheet-metal shop: the HN-3 and HN-4 notch 16 ga with 5 and 6″ "
      "blades, the HN-3/102 notches 1/8″ with 4″ blades, and the FN1.5×80 works from a foot pedal on its own stand.",
      ["HN-3 / HN-4: 16 ga (1.5 mm), 4.9 × 4.9″ and 6 × 6″ notches", "HN-3/102: 1/8″ (3 mm), 3.9 × 3.9″", "FN1.5×80: 16 ga, foot pedal, on stand",
       "Stand optional for the HN-4"],
      ["tm-hn3", "tm-hn4", "tm-fn"], headline="16 ga – 1/8″, 90°", cap="[Capacity, mild steel]", manual=True),
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
    F("tt-pn-hand", P_PIPE_NOTCH, "tt-tube-notch", "Hole-saw pipe notchers for the drill and hand tube notchers", "Hole-saw and hand notchers",
      [T["tt-notcher"][1]],
      "Inexpensive notchers for the occasional saddle: the PNM 1-1/2 bolts to the bench and runs a bi-metal hole saw from an ordinary "
      "1/2″ drill on 3/4 to 3″ tube at up to 50°, with offset notches up to 1-1/2″; the PN-1/2 notchers fit the drill press for "
      "compound-angle notches up to 2″; the RA hand notchers punch 90° notches in thin-wall tube by lever.",
      ["PNM 1-1/2: 3/4 – 3″ OD, to 50°, CNC-machined 1-1/4″ steel frame, 2-axis clamp", "PN-1/2A / H (aluminum) and PN-1/2S (steel): to 2″ tube, 0 – 45 / 50 / 60°",
       "RA-1 – RA-10: hand lever, 90° notches", "RAB: vent notcher"],
      ["tm-pnm15", "tm-pn12", "tm-ra"], headline="Tube to 3″", cap="[Capacity]", manual=True),
    F("tt-prs", P_PIPE_NOTCH, "tt-prs", "PRS tube and profile end grinders — belt notchers, Ø3/4 – 5-3/4″", "PRS tube end grinders", T["tt-prs"],
      "Belt grinders built to notch tube ends: the tube sits in the adjustable slide and is fed against a contact roller the size of the "
      "mating tube, at any angle from 30 to 90° — a clean, burr-free saddle in steel, stainless and aluminum tube and profiles without "
      "saws or tooling. The PRS-76 models take Ø3/4 – 3″ tube with a 4″ belt, two speeds and forward / reverse on the C; the PRS-150 "
      "takes Ø1-3/8 – 5-3/4″ with a 6″ belt and 7.5 HP and grinds flat and on a contact wheel as well.",
      ["PRS-76A / 76C / 76: tube Ø3/4 – 3″, 4 × 79″ belt, 4 HP or two-speed 3 / 3.75 HP", "PRS-150: tube Ø1-3/8 – 5-3/4″, 6 × 79″ belt, 7.5 HP two-speed, forward and reverse",
       "Notching angle 30 – 90°; contact rollers for 1/2 to 2-1/2″ pipe sizes", "Dust collector connection; flat and contact-wheel grinding too"],
      ["tm-prs", "tm-prs150"], headline="Tube Ø3/4 – 5-3/4″", cap="[Belt size] belt", optional=["Contact rollers Ø20, 26, 32, 42, 48, 60 and 76 mm (1/2 – 2-1/2″ pipe)"]),
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
      ["tm-hrbm50", "tm-rbm40", "tm-hrbm65", "tm-hrbm40", "tm-rbm50"], headline="Shafts Ø1-9/16 – 2-1/2″", cap="[Shaft diameter] shafts"),
    F("tt-rbm-small", P_ANGLE, "tt-ring", "RBM10 – RBM30HV ring rollers, Ø3/4 – 1-3/16″ shafts", "RBM10 – RBM30 ring rollers", [RB[0]],
      "Small ring rollers for flat bar, square bar and light sections: the RBM10 by hand crank, the ERBM10HV, RBM30 and RBM30HV with a "
      "motor and foot pedal — the HV models horizontal and vertical — and the RBM20 with two driven rolls, an LED readout for the top "
      "roll and single-phase or 3-phase power.",
      ["Shafts Ø3/4 – 1-3/16″ (20 – 30 mm)", "Flat bar on edge to 1-3/16 × 3/8″, the easy way to 2 × 9/16″", "Motorized models with foot pedal; RBM10 by hand",
       "RBM20: LED top-roll readout, two driven rolls, 1-phase or 3-phase"],
      ["tm-rbm30hv", "tm-rbm20", "tm-erbm10", "tm-rbm30", "tm-rbm10", "tm-rbm-rolls"], headline="Shafts Ø3/4 – 1-3/16″", cap="[Shaft diameter] shafts"),
    F("tt-tr", P_ANGLE, "tt-ring", "TR tube rollers, CRB-76 decorative ring roller and PR ring rollers", "Tube and ring rollers",
      T["tt-tr"] + [RB[2], pick(T["tt-ub"][1], ["PR-3", "PR-5"], title="PR-3 · PR-5", sub="Bench ring rollers for flat bar and rod")],
      "Rollers that bend tube, pipe and bar into arcs and rings: the TR-40 for square and rectangular tube, the TR-50 and electric ETR-50 "
      "for 1/2 – 2″ round tube and 1/4 – 1-1/2″ pipe with CNC-machined dies, the TR-60 with a quick-change lower roll for round, square "
      "and rectangular tube, flat bar and channel; the CRB-76 rolls decorative rings and scrolls in round and square tube and flat bar; "
      "the PR-3 and PR-5 bench rollers roll flat bar and rod.",
      ["TR-50 / ETR-50: round tube 1/2 – 2″, pipe 1/4 – 1-1/2″, square tube 1/2 – 1″ with optional rolls", "TR-60: round tube 2″, pipe 1-1/2″, square 2″, rectangular and channel 1 × 2″",
       "ETR-50: 1/2 HP motor with foot pedal; CRB-76: 1.5 HP, formers Ø5/8 – 3″", "PR-5: three driven rolls, flat bar 1 × 1/4″ the easy way, on a heavy stand"],
      ["tm-tr60", "tm-etr50", "tm-tr50", "tm-crb76", "tm-pr5", "tm-tr40", "tm-pr5-stand", "tm-pr3", "tm-crb-rolls"], headline="Tube to 2″", cap="[Capacity]", manual=True),
]

# =============================================================================================== bead rollers
P_BEAD = "bead-rollers"
BEAD = [
    F("tt-etb", P_BEAD, "tt-bead", "ETB-12 · ETB-25 · ETB-40 beading machines, 18 – 8 ga", "ETB beading machines", [T["tt-etb"][0]],
      "Beading machines for stiffening beads, steps, flanges and offsets in sheet and in the ends of ducts and tanks: the TB-12 by hand "
      "and the ETB-12 with a self-braking motor and foot pedal for 18 ga with an 8″ throat; the ETB-25 and ETB-40 on welded steel frames "
      "with brake motors, foot pedals and adjustable idle rolls for 12 ga and 8 ga with 11 and 12″ throats. Four standard roll sets and "
      "eight extra profiles.",
      ["18 ga (TB-12, ETB-12), 12 ga (ETB-25), 8 ga (ETB-40) mild steel", "Throat 8 – 12″", "Brake motor and foot pedal on the ETB models",
       "4 standard roll sets; 8 extra profiles to order"],
      ["tm-etb25", "tm-etb12", "tm-tb12"], headline="18 – 8 ga", cap="[Capacity, mild steel] · throat [Throat depth]"),
    F("tt-rm-deep", P_BEAD, "tt-bead", "RM24 · RM36 · RM42 deep-throat bead rollers, 24 – 42″", "RM deep-throat bead rollers", [T["tt-etb"][2]],
      "Deep-throat bead rollers for auto body panels, floor pans, doors and HVAC panels: 20 ga steel and 18 ga aluminum with a 24, 36 "
      "or 42″ throat, by hand crank (M models) or with a variable-speed motor, foot pedal and forward / reverse. The H models have a 4″ "
      "high throat for formed panels and drive both shafts. Round, flat, step and spoiler bead rolls; the bead depth is adjustable.",
      ["20 ga (1 mm) mild steel, 18 ga (1.2 mm) aluminum", "Throat 24″, 36″ or 42″; 4″ throat height on the H models",
       "Variable-speed foot pedal, forward / reverse; both shafts driven (H)", "Rolls: round bead 1/8 – 1″, flat bead, step 1/16 – 1/4″, 45° step, spoiler 1-1/4″ radius"],
      ["tm-rm36", "tm-rm42h", "tm-rm24m"], headline="24 – 42″ throat", cap="throat [Throat depth]"),
    F("tt-bead", P_BEAD, "tt-bead", "RM bench bead rollers and rotary machines, 22 – 18 ga", "RM bench bead rollers", T["tt-bead"],
      "Hand bead rollers and rotary machines for the bench and the vise: the RM-A and RM-B with hardened rolls, the RM08 with six roll "
      "sets for turning, burring, wiring, crimping and ogee beads, the RM12 and RM18 with 12 and 18″ throats, and the heavy-duty RM-8H and "
      "RM-27 with 22 mm shafts and gear drive for 18 ga steel and 16 ga aluminum.",
      ["22 – 18 ga mild steel; RM-8H / RM-27: 20 ga stainless, 16 ga aluminum", "Throat 4.5″ (RM-B) to 18″ (RM18)",
       "RM08: six standard roll sets; RM-8H: 3/8″ bead and offset die sets", "Bench, vise or stand mounting; stands optional"],
      ["tm-rm08", "tm-rm18", "tm-rm8h", "tm-rm27", "tm-rmb"], headline="22 – 18 ga", cap="[Capacity]", manual=True),
]

# =============================================================================================== hydraulic presses
P_PRESS = "hydraulic-press"
SP = T["tt-shop-press"]
HP = T["tt-hp"]
PRESS = [
    F("tt-shop-hs", P_PRESS, "tt-shop", "HP-S workshop presses 22 – 110 US tons and HPP motorized presses 66 – 176 US tons", "HP-S / HPP workshop presses",
      [SP[3], SP[4]],
      "H-frame workshop presses for repair, assembly and straightening: the HP-S presses from 22 to 110 US tons with hand pumps, in a "
      "European (S) and a standard (S-A) design, and the HPP motorized presses from 66 to 176 US tons with a two-step hydraulic unit, a "
      "cylinder that moves across the frame, V-block worktables and 16″ of stroke.",
      ["HP-S: 22, 33, 55, 88 and 110 US tons; hand pump; travel to 7.9 + 17.7″", "HPP: 66, 110 and 176 US tons; 3 – 4 HP; 16.1″ (410 mm) stroke",
       "Moving cylinder and V-block worktable (HPP)", "Working width to 43.3″ (HPP-160)"],
      ["tm-hpp100", "tm-hp30s", "tm-hp30sa"], headline="22 – 176 US tons", cap="[Force]"),
    F("tt-shop-small", P_PRESS, "tt-shop", "Shop presses 10 – 30 tons and BP-16T / EBP-25T workshop presses", "Shop presses 10 – 30 tons",
      [SP[1], SP[2]],
      "Shop presses for the garage, the farm and the maintenance shop: H-frame presses from 10 to 30 tons with hand pumps and adjustable "
      "tables for pressing bearings, bushings and shafts and straightening parts; the BP-16T workshop press with a two-speed hand pump "
      "and the EBP-25T with a motorized pump and infinitely variable pressure and speed, both with two V-blocks for straightening.",
      ["H-frame 10, 12, 20 and 30 tons; working space to 39″", "BP-16T: 18 US tons, hand pump with low and high pressure; 6.3″ stroke",
       "EBP-25T: 28 US tons, motorized pump, 7.9″ stroke; pressure gauge", "Two V-blocks for straightening"],
      ["tm-ebp25t", "tm-bp16t", "tm-hframe"], headline="10 – 30 tons", cap="[Capacity]"),
    F("tt-shop-brake", P_PRESS, "tt-shop", "HP-12N · HP-24N shop press brakes, 12″ × 3/16″ and 24″ × 14 ga", "HP-12N / HP-24N press brakes", [SP[0]],
      "Compact hydraulic bending brakes driven by a bottle jack: the HP-12N bends 3/16″ mild steel over 12″ with two V-blocks on a "
      "frame with four wheels — its 12-ton ram and pump come off for other pressing jobs — and the HP-24N bends 14 ga over 24″ with 20 "
      "tons, with return springs that bring the bending bar back after every bend.",
      ["HP-12N: 12 tons; 3/16″ (5 mm) × 12″; 0 – 90°", "HP-24N: 20 tons; 14 ga half width, 16 ga full width, 12 ga aluminum, 18 ga stainless × 24″",
       "Return springs bring the bending bar back (HP-24N)", "HP-12N on four wheels; ram and pump removable"],
      ["tm-hp12n", "tm-hp24n"], headline="12″ × 3/16″, 24″ × 14 ga", cap="[Bending width × thickness]", manual=True),
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
      ["tm-hp63c", "tm-hp30c"], headline="22 – 110 US tons", cap="[Force]"),
    F("tt-hp-f", P_PRESS, "tt-hp", "HP-F four-column hydraulic presses, 55 – 347 US tons", "HP-F four-column presses", [HP[4]],
      "Four-column presses for forming and pressing with an evenly guided slide: 55 to 220 US tons on the HP-F, and the heavier F1 "
      "models to 347 US tons with tables up to 42.9 × 31.5″; the HP-315FK has a PLC touch-screen control cabinet.",
      ["55 – 347 US tons", "Tables 15.7 × 23.6″ to 42.9 × 31.5″", "Stroke 11.8 – 15.7″", "Separate pump unit; PLC touch screen on the HP-315FK"],
      ["tm-hp315fk", "tm-hp50f"], headline="55 – 347 US tons", cap="[Force]"),
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
    F("tt-hcs", P_CIRCLE, "tt-circle", "HCS · ECS circle shears and flanging machines and MCS manual circle shear", "HCS / ECS circle shears", T["tt-hcs"],
      "Circle shears that also flange: the HCS10/10 by hand crank and the ECS10/10 with a two-speed motor and foot pedal cut discs from "
      "Ø5-7/8 to 19-3/4″ in 16 ga and turn a rim up to 5/16″ high with the second roll set; the MCS1.0×1000 is a manual circle shear "
      "for discs up to Ø39-3/8″ in 20 ga.",
      ["HCS10/10 / ECS10/10: discs Ø5-7/8 – 19-3/4″, 16 ga; flanging to 5/16″", "Two roll sets: cutting and flanging", "ECS10/10: 1/2 / 3/4 HP two-speed motor, foot pedal",
       "MCS1.0×1000: discs Ø4 – 39-3/8″ in 20 ga, hand crank"],
      ["tm-ecs", "tm-hcs", "tm-mcs1000"], headline="Discs to Ø39″", cap="[Disc diameter]", manual=True),
]

# =============================================================================================== press brakes, horizontal benders
P_COMPACT = "compact-hydraulic-press-brakes"
COMPACT = [
    F("tt-hbv", P_COMPACT, "tt-hbv", "HBV24 · HBV48 hydraulic bending brakes, 5/32″ × 24″ and 48″", "HBV hydraulic brakes", T["tt-hbv"],
      "Small hydraulic brakes for brackets, clips and short parts in plate: 16.5 or 33 US tons push the top beam into a four-way V-block "
      "for 5/32″ (4 mm) plate over 24″ or 48″, controlled by a hydraulic foot valve; the beam unpins for closed bends and easy removal of "
      "the part, and a back gauge sets the flange from 4.1 to 21.7″.",
      ["5/32″ (4 mm) mild steel × 24″ (HBV24) or 48″ (HBV48)", "16.5 / 33 US tons; 5.9″ (150 mm) stroke", "Four-way V-block; hydraulic pull-up press beam",
       "Hydraulic foot valve; back gauge 4.1 – 21.7″"],
      ["tm-hbv"], headline="5/32″ × 24 – 48″", cap="[Bending width × thickness]"),
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
    F("tt-ub", P_HORIZ, "tt-ub", "UB universal benders, SBG / YP / UBM bench benders and ornamental iron tools", "Universal and bench benders",
      [T["tt-ub"][0], pick(T["tt-ub"][1], ["YP-9", "YP-38", "UBM-30"], title="YP-9 · YP-38 · UBM-30", sub="Bench benders for flat bar, 0 – 200°"),
       pick(T["tt-ub"][2], ["W-1", "W-2", "W-10", "Mini universal bender", "SBG-20", "JTR-20", "JTR-30"])],
      "Hand benders for flat bar, round and square bar and angle — gates, railings, brackets, scrolls and ornamental iron: the UB-70, "
      "UB-100 and UB-100A universal benders bend angles to 120° and radius bends in flat bar up to 4 × 3/8″ hot; the SBG and YP benders "
      "bend angles, rings, hoops and scrolls; the W-1 and W-2 tool sets form scrolls, bend, twist, shear and punch strip; the W-10 makes "
      "180° rod bends in a vise.",
      ["UB-70 / UB-100: flat bar 2-3/4 – 4 × 3/8″, round Ø3/4″, square 11/16″ (hot); angle 2-3/8 × 5/16″", "SBG-30 / SBG-40, YP-9 / YP-38 / UBM-30: flat bar to 2 × 5/16″, 0 – 200°",
       "W-1 / W-2: scroll former, bender, twister, shear and punch", "W-10: 180° bends in rod to 3/8″, ID 1/2 – 1-1/2″"],
      ["tm-ub100a", "tm-ub70", "tm-sbg30", "tm-yp38", "tm-ubm30", "tm-w1", "tm-w10", "tm-mini-ub", "tm-jtr30"], headline="Flat bar to 4 × 3/8″", cap="[Flat bar]", manual=True),
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
      ["tm-her"], headline="12 ga – 1/2″ × 4 – 10 ft", cap="[Working width] × [Capacity, mild steel]", note=NOTE_HZ),
    F("tt-esr", P_ROLL, "tt-slip", "ESR electric slip rolls, 22 ga – 1/4″ × 3.3 – 10 ft", "ESR electric slip rolls", [SL[2]],
      "Motorized three-roll slip rolls for HVAC, duct and sheet-metal work: a fixed top roll, adjustable lower and rear rolls of "
      "high-strength steel, wire grooves, a top roll that swings out over a cam lock and cone rolling. From the ESR-1020×2 for 14 ga over "
      "40″ to 1/4″ over 51″, 3/16″ over 61″ and 10 ga over 80″ and 10 ft; the E models have a motorized rear roll with a digital "
      "position readout.",
      ["Rolling capacity 22 ga to 1/4″ (0.8 – 6.5 mm) × 40 – 118″", "Fixed top roll, adjustable lower and rear rolls; wire grooves; cone rolling",
       "Foot pedal; 1 – 7.5 HP", "ESR2550 / ESR3050 E: motorized rear roll with digital position readout",
       "Options: hand-wheel adjustment of the rear roll, fast lower-roll adjustment"],
      ["tm-esr", "tm-esr1300e", "tm-esr1020"], headline="22 ga – 1/4″ × 3.3 – 10 ft", cap="[Working width] × [Capacity, mild steel]", note=NOTE_HZ),
    F("tt-slip-hand", P_ROLL, "tt-slip", "Manual slip rolls, 22 – 14 ga × 12 – 81″", "Manual slip rolls", [SL[0], SL[1]],
      "Hand-crank slip rolls for HVAC, flashing and small tanks: precision-ground rolls of high-strength steel, hardened gears, an "
      "eccentric clamp, a lower roll set by lever and cam and a top roll that swings out to remove the part — 22 ga to 16 ga on the "
      "bench from 12 to 51″, the KW01 on its own stand, and the W01-2 floor rolls for 14 ga over 24 to 49″.",
      ["22 – 14 ga (0.8 – 2 mm) × 12 – 81″", "Precision-ground high-strength rolls; hardened gears", "Quick-release top roll; lever-and-cam lower roll adjustment",
       "Bench models, KW01 on stand, W01-2 on floor stand; stand type A optional"],
      ["tm-slip-1300", "tm-slip-kw01", "tm-w01-2", "tm-slip-w01", "tm-slip-sj"], headline="22 – 14 ga × 12 – 81″", cap="[Working width] × [Capacity, mild steel]",
      manual=True),
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
]

# =============================================================================================== manual shears (sheet-metal-shears.html, family set "ttmc")
P_SHEAR = "sheet-metal-shears"
SHEAR = [
    F("tt-q01", P_SHEAR, "sh-manual", "Q01 foot shears, 20 – 14 ga × 40 – 98″", "Q01 foot shears", T["tt-q01"],
      "Foot-operated shears for HVAC, roofing and light sheet: cast frames for 20 ga and 14 ga over 40″ and 16 ga over 52″, welded "
      "steel frames (A) with an adjustable-length pedal, and the light-duty B models with a spring-loaded hold-down for 16 ga over 52″ "
      "and 18 ga over 98″. High-carbon chromium-steel blades; front and back gauges; mild steel, aluminum, copper, brass, zinc and plastic.",
      ["20 ga × 40″, 14 ga × 40″, 16 ga × 52″, 18 ga × 98″", "Cast or welded steel frames; spring-loaded hold-down beam (B)", "Back gauge 0 – 27.6 / 31.5″ (700 / 800 mm)",
       "High-carbon chromium-steel blades; adjustable blade gap (B)", "Rear safety cage optional (A)"],
      ["tm-q01", "tm-q01a", "tm-q01b", "tm-q01b-gauge"], headline="20 – 14 ga × 40 – 98″", cap="[Working width] × [Capacity, mild steel]", manual=True),
    F("tt-bq01", P_SHEAR, "sh-manual", "BQ01 bench shears, BQF01 foot and EBQ01 motorized bench shears, Q01 hand shears", "Bench shears", T["tt-bq01"],
      "Bench shears for 18 – 20 ga over 26″ and 41″, by hand lever (BQ01), foot pedal (BQF01) or a 1 HP motor and foot switch (EBQ01), "
      "with a working light and a 19.7″ back gauge; and the Q01 two-handle shears on stands for 16 ga over 41 and 59″, 18 ga over 79″ "
      "and 22 ga over 98″.",
      ["Bench shears 18 ga × 26″ and 20 ga × 41″; back gauge 0 – 19.7″", "Hand lever, foot pedal or motorized (EBQ01, 1 HP, foot switch)",
       "Q01 hand shears: 16 ga × 41 – 59″, 18 ga × 79″, 22 ga × 98″", "Working light; front angle stop (EBQ01); rear safety cage optional (BQF01)"],
      ["tm-ebq01", "tm-bqf01", "tm-bq01", "tm-q01h"], headline="22 – 16 ga × 26 – 98″", cap="[Working width] × [Capacity, mild steel]", manual=True),
    F("tt-hs300", P_SHEAR, "sh-manual", "Hand guillotine shears, 20 – 16 ga × 12 – 51″", "Hand guillotine shears", T["tt-hs300"],
      "Lever guillotine shears for thin sheet and plastic: the HS-300 for 20 ga over 12″, the HS-500 to HS-1300 for 16 ga over 20 to "
      "51″, and the GS, KHS and TSC shears on stands with fast clamping, a hand-wheel back gauge and a counterweight on the lever, for 20 "
      "ga over 40 – 49″ and 16 ga over 40″.",
      ["HS-300: 20 ga × 12″ with back gauge 0 – 7″", "HS-500 – HS-1300: 16 ga × 20 – 51″", "GS / KHS / TSC: 20 – 16 ga × 40 – 49″; cast-iron frame on the GS-1000I",
       "Fast clamping; back gauge by hand wheel; counterweight (spring on the GS-1000)"],
      ["tm-khs", "tm-gs1000", "tm-hs800", "tm-hs300", "tm-tsc"], headline="20 – 16 ga × 12 – 51″", cap="[Working width] × [Capacity, mild steel]", manual=True),
    F("tt-hs", P_SHEAR, "sh-manual", "Lever shears, bar cutters and bar and section shears", "Lever shears and bar cutters", T["tt-hs"],
      "Hand shears for plate, flat bar and bar: the HS and HSG lever shears cut 1/4″ plate and 2-3/4 × 1/4″ flat with 5 – 12″ blades; "
      "the MS bar cutters cut round bar from Ø3/4 to 1-1/4″, square and flat; the PBS bar and section shears cut flat bar up to 4 × 3/8″, "
      "angle, tee, round and square bar, and the PBS-9 punches holes in sheet as well.",
      ["HS / HSG: 1/4″ (6 mm) plate, flat bar 2-3/4 × 1/4″, round Ø7/16 – 1/2″", "MS-20 – MS-32: round Ø3/4 – 1-1/4″, square 11/16 – 1-1/8″",
       "PBS-7 / PBS-9: flat 3-1/2 × 9/16″, angle 2-3/8 × 1/4″, round Ø7/8″; PBS-9 punches 14 ga", "Hold-down adjustable for height (PBS)"],
      ["tm-hs", "tm-ms", "tm-pbs9", "tm-pbs7"], headline="1/4″ plate, Ø1-1/4″ bar", cap="[Round bar] round", manual=True),
    F("tt-mms", P_SHEAR, "sh-manual", "MMS bench shears and throatless rack-and-pinion shears, 16 ga – 5/32″", "MMS bench shears", T["tt-mms"],
      "Bench shears for sheet, strip and wire: the MMS-1 to MMS-3 for 16 ga to 1/8″, and the MMS-4 to MMS-6 throatless shears with an "
      "alloy-steel rack and pinion that cut straight lines, curves and shapes in mild steel to 5/32″ and stainless to 1/8″ — the work turns "
      "freely around the blade.",
      ["MMS-1 – MMS-3: 16 ga – 1/8″ mild steel", "MMS-4 – MMS-6: 14 ga – 5/32″ mild steel, 16 ga – 1/8″ stainless; cuts curves",
       "Rack-and-pinion drive; removable handle; adjustable hold-down (MMS-6)", "Bolts to a bench or a stand"],
      ["tm-mms6", "tm-mms3"], headline="16 ga – 5/32″", manual=True),
]

GROUP_FAMILIES = COLD + ALU + CORNER + PIPE_NOTCH + IRON + ANGLE + BEAD + PRESS + CIRCLE + COMPACT + HORIZ + ROLL + DEBURR
