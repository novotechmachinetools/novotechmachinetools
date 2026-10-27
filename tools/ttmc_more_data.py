#!/usr/bin/env python3
"""NovoTech value-line machines built by TTMC (sold under NovoTech's name, TTMC model codes) — families of the NEW pages:
sheet metal brakes, lock formers, belt grinders, drill presses, milling machines, CNC machine tools, CNC plasma tables, metal
shaping machines, arbor presses and tube benders.  Spec tables in tools/ttmc_more_tables.py, photos in tools/ttmc_more_photos.py,
pages in tools/ttmc_more_pages.py; families of the existing pages in tools/ttmc_more_data2.py.
"""
from ttmc_conv import auto_spec, pick
import ttmc_more_tables as TT

T = TT.TAB
BRAND = "novotech"
NOTE = ("Metric values in brackets are the manufacturer's figures; thin sheet is given in gauge. Packing size is the shipping crate "
        "L × W × H and weight is the net weight of the machine.")
NOTE_HZ = (NOTE + " Speeds marked “rated at 50 Hz” are the manufacturer's 50 Hz figures — motors run about 20 % faster on 60 Hz power.")
MANUAL_TAG = ("NovoTech's own brand: manufactured in China to high North American quality standards, with a 1-year warranty and parts "
              "and support from Mississauga, ON, Canada")


def F(fid, page, group, name, short, tables, summary, features, images, optional=(), headline="", cap=None, note=NOTE, manual=False,
      models_label=None):
    models = [m for t in tables for m in t["models"]]
    label = models_label or ((" · ".join(models) if len(models) <= 3 else f"{models[0]} – {models[-1]}") + f" · {len(models)} model{'s' if len(models) > 1 else ''}")
    return dict(id=fid, page=page, group=group, brand=BRAND, name=name, short=short, models_label=label, summary=summary,
                features=list(features), optional=list(optional), images=list(images), videos=[], headline=headline,
                specs=auto_spec(tables, note, cap=cap), manual=manual, no_pdf=True)   # no value-line PDF for these yet


# =============================================================================================== sheet metal brakes
P_BRAKE = "folder-sheet-metal-brake"
BRAKES = [
    F("tt-eb", P_BRAKE, "mag", "EB magnetic sheet metal brakes, 16 ga × 2 – 8 ft and 18 ga × 10 ft", "EB magnetic brakes", T["tt-eb"],
      "The magnetic brake clamps the sheet electromagnetically instead of mechanically: an electromagnet in the bed pulls the steel clamp "
      "bar down on the sheet with 3.3 to 13.2 US tons, and the bending beam folds it around the front edge of the bar. With no clamping "
      "beam frame at the ends, a short clamp bar folds the side of a box of any depth, and closed and narrow shapes a box and pan brake "
      "cannot reach. Six models from 2 to 10 ft — 16 ga mild steel to 8 ft, 18 ga over 10 ft — each with a foot switch, a back gauge, a "
      "bending stop and four sets of clamp bars.",
      ["16 ga (1.6 mm) mild steel over 2, 3, 4, 6 and 8 ft; 18 ga (1.2 mm) over 10 ft",
       "Electromagnetic clamping, 3.3 – 13.2 US tons (3 – 12 t); thermal cut-out at 158 °F (70 °C), 30 % duty cycle",
       "Unlimited box depth; return flanges down to 3/4″ (19 mm)",
       "Four sets of clamping bars — full length, short set for boxes, narrow and slotted",
       "Foot switch, easy-raise clamp bar and bending stop standard; back gauge 15.4 – 25.2″ (390 – 640 mm)"],
      ["tm-eb2500", "tm-eb1250", "tm-eb-bars"], headline="16 ga × 2 – 8 ft, 18 ga × 10 ft", cap="[Capacity, length × mild steel]"),
    F("tt-hw", P_BRAKE, "hyd", "HW hydraulic folding machines, 10 ga × 4 – 10 ft and 3/16″ × 80 – 100″", "HW hydraulic folders", T["tt-hw"],
      "Hydraulic folding machines for the production sheet-metal shop. The HW…×3.5 models fold 10 ga (3.5 mm) mild steel and 12 ga "
      "stainless over 4, 6, 8 and 10 ft, with segmented upper tools for boxes up to 5.9″ deep, a bending angle stop from 0 to 135°, foot "
      "pedals and a 26″ manual back gauge. The HW…E models add a touch screen that shows the angle and the gauge position, a servo back "
      "gauge on a ball screw and a light curtain at the front, and fold 3/16″ (4.5 mm) structural steel over 80″ and 100″ or 10 ga over 120″.",
      ["HW…×3.5: 10 ga (3.5 mm) mild steel and 12 ga (2.5 mm) stainless × 48 – 120″; 5 – 10 HP",
       "HW…E: 3/16″ (4.5 mm) structural steel × 80″ and 100″, 10 ga × 120″; touch screen; servo back gauge with ball screw, 21.7 – 49.2″",
       "Boxes to 5.9″ (150 mm) deep with the segmented upper tools",
       "Bending angle setting 0 – 135°; hand wheels set the upper beam and the tool gap",
       "Foot pedal control; full protective covers; light curtain at the front on the E models"],
      ["tm-hwe", "tm-hw", "tm-hw2440", "tm-hw-box", "tm-hw-angle"], headline="10 ga × 4 – 10 ft, 3/16″ × 80 – 100″", cap="[Bending length] × [Capacity]"),
    F("tt-efm", P_BRAKE, "hyd", "EFM / EFMS electric folding machines, 16 – 20 ga × 80 – 120″", "EFM electric folders", [T["tt-pbb"][2]],
      "Motorized folding with the operator's hands free: one motor closes the clamping beam, a second swings the folding beam, both run "
      "from a foot pedal while the operator holds and positions the sheet. 16 ga (1.5 mm) mild steel over 80″, 20 ga (1 mm) over 100″ "
      "and 120″. The EFMS models have a segmented blade (25 to 400 mm segments) for boxes and pans, the EFM models a one-piece blade for "
      "long straight bends.",
      ["16 ga (1.5 mm) × 80″; 20 ga (1 mm) × 100″ and 120″; bending angle 0 – 135°",
       "Clamping motor 1/2 HP (0.37 kW) and folding motor 1 HP (0.75 kW); foot pedal control",
       "EFMS: segmented blade, segments 25 – 400 mm, for boxes and pans; EFM: one-piece blade",
       "4″ (100 mm) opening height"],
      ["tm-efms", "tm-efm"], headline="16 ga × 80″, 20 ga × 100 – 120″", cap="[Bending length] × [Capacity, mild steel]"),
    F("tt-pb", P_BRAKE, "panbox", "Box and pan brakes, 22 ga – 12 ga × 12 – 157″", "Box and pan brakes", T["tt-pb"],
      "Hand-operated box and pan brakes with removable fingers, from a 12″ bench brake to 13 ft floor brakes with counterweights. The "
      "bench and stand brakes take 20 to 16 ga over 12 to 50″; the BP-1650 and BP-1648H fold 16 ga over 48 – 50″ with 4″ deep boxes; "
      "the floor brakes with segment blades and counterweights fold 12 ga over 4 to 8 ft, 14 ga over 10 ft, 18 ga over 12 ft and 22 ga "
      "over 13 ft. Take the fingers out where the sides of the box come up and fold all four sides of a pan.",
      ["Segmented fingers that are taken out and repositioned for any box size",
       "Bench brakes 12 – 50″ in 20 – 16 ga; BP-1650 / BP-1648H 16 ga × 48 – 50″, boxes 4″ (100 mm) deep",
       "Floor brakes with counterweights: 12 ga × 48 – 100″, 14 ga × 80 – 120″, 18 ga × 146″, 22 ga × 157″",
       "Bending angle to 135°, 140° on the W1.5×1500 and W1.2×2000",
       "BP-1648H: all-steel welded, adjustable truss bars, bronze bushings, removable nose bar and stop rod for repeat bends"],
      ["tm-bp1650", "tm-pb1220", "tm-w2540a", "tm-pb1220z", "tm-bp1648h", "tm-w1220pb"], headline="22 ga – 12 ga × 12 – 157″",
      cap="[Bending length] × [Capacity, mild steel]", manual=True),
    F("tt-pb-heavy", P_BRAKE, "panbox", "Heavy box and pan brakes, 18 – 14 ga × 59 – 100″, pans to 5-1/8″ deep", "Heavy box and pan brakes",
      [T["tt-pb-heavy"][0]],
      "Heavy fabricated box and pan brakes for pans and boxes deeper than a standard brake allows. The W1.5×2540H folds 16 ga over 100″ "
      "with fingers for pans up to 5-1/8″ deep and a 6-1/4″ clamping-beam lift; the WU2.0×2500 folds 14 ga over 100″ with two "
      "counterweights; the W1830×1.5P folds 16 ga over 72″ with 2, 3 and 4″ fingers; the W1.2×1500H folds 18 ga over 59″ with 4-7/8″ "
      "fingers and a precision angle stop. The counterweights hold the beam in any position.",
      ["W1.5×2540H: 16 ga × 100″; pans to 5-1/8″ (130 mm) deep; fingers 60 – 305 mm; quick beam adjustment",
       "WU2.0×2500: 14 ga × 100″; fingers 75 mm (5) and 125 mm (17), easy to remove; two counterweights; stop rod",
       "W1830×1.5P: 16 ga × 72″; eight fingers each of 2, 3 and 4″",
       "W1.2×1500H: 18 ga × 59″; 4-7/8″ (125 mm) fingers; counterweight stops in any position; precision angle stop"],
      ["tm-w2540h", "tm-wu", "tm-w1830p", "tm-w1500h"], headline="18 – 14 ga × 59 – 100″", cap="[Bending length] × [Capacity, mild steel]", manual=True),
    F("tt-hb", P_BRAKE, "hand", "Hand brakes, 22 ga – 12 ga × 12″ – 13 ft", "Hand brakes", T["tt-hb"] + [T["tt-pb-heavy"][1]],
      "Straight brakes for HVAC, flashing and general sheet work: bench brakes from 12 to 48″, the HB brakes on stand for 22 ga and 16 ga "
      "over 48 – 50″, floor brakes for 18 – 16 ga over 40 – 51″ with a one-piece blade or sliding segments, and heavy floor brakes with "
      "counterweights and a stop rod for 12 ga over 48 – 100″, 14 ga over 120″ and up to 157″ in 22 ga.",
      ["HB-2248 / HB-2250: 22 ga × 48 – 50″; HB-1650: 16 ga × 50″ with 1-1/4″ beam lift",
       "W1.0 / W1.2 brakes 12 – 79″ in 20 – 18 ga, bending to 135 – 140°",
       "W1.2 / W1.5 floor brakes 40 – 51″ with a one-piece blade or sliding segments, bending to 150°",
       "Heavy floor brakes with counterweights and stop rod: 12 ga × 48 – 100″, 14 ga × 120″, 18 ga × 146″, 22 ga × 157″",
       "HB-2248: all-steel welded, adjustable truss bars and bronze bushings, removable nose bar, stop rod, folding stand"],
      ["tm-hb2250", "tm-w2040", "tm-w1500", "tm-hb2248", "tm-w1050", "tm-w1220"], headline="22 ga – 12 ga × 12″ – 13 ft",
      cap="[Bending length] × [Capacity, mild steel]", manual=True),
    F("tt-folder", P_BRAKE, "hand", "Foot-clamp folding machines, 20 – 12 ga × 40 – 119″", "Manual folding machines",
      [T["tt-pbb"][0], T["tt-pbb"][1], T["tt-pb-heavy"][2]],
      "Folding machines with a foot-operated clamping beam: press the pedal to clamp, swing the folding beam with the handle, both hands "
      "free to hold the sheet. The PBB machines fold 12 ga over 40″ down to 20 ga over 99″, with one-piece or segmented blades and "
      "quick-release clamp segments on the 3SH models; the TSB, TSBS, MFS and MF heavy folding machines take 14 ga over 80″ and 18 – 20 ga "
      "over 10 ft, with segments from 25 to 500 mm on the S models; the WF folders take 20 ga over 80 to 118″.",
      ["Foot-operated clamping beam; counterbalanced folding beam with angle stop on the 3SH models",
       "PBB: 12 ga × 40″, 14 ga × 40 – 50″, 16 ga × 60″, 18 ga × 80″, 20 ga × 99″",
       "TSBS / MFS: segments 25 – 400 / 500 mm for boxes; TSB 2060/2 cast-iron frame with counterweight",
       "Bending angle to 135°, 150° on the 3SH models",
       "Back gauge on pre-drilled points (3SH) and gas spring in the arm (PBB) as options"],
      ["tm-pbb", "tm-pbb3sh", "tm-tsbs", "tm-mfs", "tm-wf", "tm-pbb1020", "tm-tsb2060", "tm-tfs"], headline="20 – 12 ga × 40 – 119″",
      cap="[Bending length] × [Capacity, mild steel]", manual=True),
    F("tt-alb", P_BRAKE, "roof", "ALB portable roofing brakes with slitter, 24 ga × 7 – 12.5 ft", "ALB roofing brakes", T["tt-alb"],
      "Portable roofing brakes for flashing, drip edge, sills, cornices and trim on the job site: an anodized aluminum frame on folding "
      "legs that is set up in 10 to 15 minutes, bends painted and coated steel up to 24 ga, aluminum up to 0.032″, copper and brass to "
      "180° — the silicone insert in the bending beam does not mark the finish — and a roller knife slits the sheet to width. Bending "
      "lengths of 7.2, 8.5, 10.5 and 12.5 ft, from 132 lb.",
      ["24 ga (0.7 mm) steel and 0.032″ (0.8 mm) aluminum; copper and brass; painted and coated sheet",
       "Bends to 180°; silicone insert in the bending beam protects the finish",
       "Roller knife for slitting; infeed depth 19 – 23″ (485 – 580 mm)",
       "Anodized light-alloy frame, 132 – 234 lb; set up in 10 – 15 minutes"],
      ["tm-alb", "tm-alb-work"], headline="24 ga × 7 – 12.5 ft", cap="[Bending length]", manual=True),
    F("tt-bench-brake", P_BRAKE, "roof", "Bench, slitting and offset brakes, 22 – 18 ga × 14 – 100″", "Bench and slitting brakes", T["tt-bsm"] + T["tt-wb"],
      "Small brakes for the bench and the van: the BSM folding brakes on a fold-away steel stand bend and slit 20 – 22 ga over 40, 48 and "
      "100″, with a slitting device that comes off; the WB-14 and W1.2 bench brakes bend 20 – 18 ga over 14 to 39″ to 90° or 135°; the "
      "ZWJ offset brakes make accurate 1/2″ offsets (jogs) up to 90° in 20 ga steel and 18 ga aluminum.",
      ["BSM1016 / BSM1220 / BSM2540: bend and slit 20 – 22 ga over 40 – 100″, foldable steel stand",
       "W1.2 bench brakes 18 – 39″ in 18 ga; WB-14 14″ in 20 ga",
       "ZWJ-20 / ZWJ-36 offset brakes: 1/2″ jogs to 90° in 20 ga steel and 18 ga aluminum",
       "Aluminum, copper and steel"],
      ["tm-bsm1016", "tm-bsm2540", "tm-w1000", "tm-wb14", "tm-zwj"], headline="22 – 18 ga × 14 – 100″", cap="[Working length]", manual=True),
    F("tt-3in1", P_BRAKE, "combo", "3-in-1 shear, brake and roll machines, 20 – 16 ga × 8 – 52″", "3-in-1 machines", T["tt-3in1"] + T["tt-3in1a"],
      "Hand-operated combination machines that shear, bend and roll sheet on one frame: 20 ga (1 mm) mild steel over 8 to 52″ and 16 ga "
      "(1.5 mm) over 42 and 52″, folding to 90° and rolling down to 1-1/8″ diameter on the small models. The floor models have removable "
      "segmented fingers for boxes and pans, a back gauge and wire grooves in the rolls; the A models have a separate bending section "
      "that needs less effort.",
      ["20 ga (1 mm) × 8 – 52″; 16 ga (1.5 mm) × 42 and 52″ on the ×1.5 models",
       "Shear, brake to 90° and slip roll on one frame; minimum rolling diameter 1-1/8 – 2-3/4″",
       "Removable segmented upper dies (fingers) for boxes and pans; back gauge",
       "Wire grooves in the rolls; two handle positions",
       "A models: independent bending section; mini shear brake 8″ for copper, brass and aluminum"],
      ["tm-3in1", "tm-3in1-1016", "tm-3in1a", "tm-3in1-305", "tm-minibrake"], headline="20 – 16 ga × 8 – 52″", cap="[Working width] × [Shear / brake / roll capacity, mild steel]",
      manual=True),
    F("tt-e3in1", P_BRAKE, "combo", "E3-IN-1 motorized shear, brake and roll machines, 1/8″ × 52″ and 80″", "E3-IN-1 motorized", T["tt-e3in1"],
      "The motorized combination machine: a 4.7 or 5.5 HP motor drives a shear that cuts 1/8″ (3 mm) mild steel at 30 strokes a minute, "
      "a brake that folds 14 ga and rolls that roll 12 ga with cone rolling, over 52″ or 80″. A function selector switches between shear, "
      "brake and roll; shearing and bending run single-stroke or continuous; the back gauge has a digital readout.",
      ["Shear 1/8″ (3 mm) × 52″ / 80″, 2° shearing angle, 30 strokes a minute",
       "Brake 14 ga (2 mm); rolls 12 ga (2.5 mm) × 59″ / 83″ with cone rolling",
       "Back gauge 17.7″ (450 mm) with digital readout and hand wheel",
       "Function selector brake / shear / roll; single stroke or continuous; quick-release top roll"],
      ["tm-e3in1"], headline="1/8″ shear × 52 – 80″", cap="[Shearing capacity × width]"),
]

# =============================================================================================== lock formers & HVAC
P_LOCK = "lock-former"
LOCK = [
    F("tt-lock", P_LOCK, "lock", "PF20G · PF16G Pittsburgh lock formers and AX20G roll former, 26 – 16 ga", "Lock formers", T["tt-lock"],
      "Pittsburgh machines for HVAC duct. The PF20G forms the Pittsburgh lock, the flange attachment and a right angle in 26 – 20 ga at "
      "25 ft/min, with double seam and drive cleat rolls as options; the PF16G takes 25 – 16 ga and forms the Pittsburgh lock, flange "
      "attachment, right angle, double seam, drive cleat and Z shape as standard. The AX20G auxiliary roll former runs drive cleat, Acme "
      "double seam, button lock and a 6-in-1 set of flanges and standing seams at 40 ft/min — its hinged table top and square drive "
      "shafts change a complete roll set in under five minutes, without tools.",
      ["Pittsburgh lock uses about 1″ of material; adjustable auto-guides",
       "All-steel forming head; hardened, ground shafts; case-hardened rolls with matching cut gears and needle bearings",
       "PF16G: six standard roll forms — Pittsburgh, flange attachment, right angle, double seam, drive cleat, Z shape",
       "AX20G: roll sets change without tools; quick jam release; roll sets at extra cost",
       "Single-phase or 3-phase motors: 1 HP (PF20G), 3 HP (PF16G), 4 HP (AX20G)"],
      ["tm-pf16g", "tm-pf20g", "tm-ax20g", "tm-lock-forms"], headline="26 – 16 ga mild steel", cap="[Capacity, mild steel] · [Speed]"),
    F("tt-hvac", P_LOCK, "duct", "SL-10 seam closer, CHB / CB cleat benders and LB-2 letter bender", "Duct and sign tools", T["tt-hvac"],
      "The tools that finish the duct: the SL-10 electric seam closer runs along a Pittsburgh seam and closes it in three stages, "
      "adjusting itself to 26 – 20 ga sheet; the CHB hand brakes bend 1/4 to 1″ flanges 24 or 30″ long; the CB cleat benders form "
      "drive-cleat edges on rectangular duct in seconds, with no set-up. The LB-2 is a foot-operated channel letter bender for sign "
      "makers — Z, S and W bends in aluminum up to 0.079″.",
      ["SL-10: closes Pittsburgh seams in 3 stages (30°, 75°, 90°); 13 – 23 ft/min; 120 V or 230 V",
       "CHB-24 / CHB-30: hand brakes for 1/4 – 1″ flanges in 20 ga, bench mounted, two-way trunnion",
       "CB-24 / CB-30: drive-cleat edges in 20 ga; quick release with 3 handle positions; needle bearings",
       "LB-2: channel letter bender for aluminum to 0.079″ (2 mm), foot pedal and depth stop"],
      ["tm-sl10", "tm-chb", "tm-cb", "tm-lb2"], headline="26 – 20 ga duct", cap="[Job]", manual=True),
    F("tt-rtb", P_LOCK, "round", "RTB round duct rollers, 22 ga × 40 – 49″", "RTB duct rollers", T["tt-rtb"],
      "Hand rollers that roll 22 ga (0.8 mm) sheet into round duct and pipe, 40″ or 49″ long, with hardened rolls: light and portable for "
      "the bench, or on a welded stand at a 33.5″ working height (RTB-8AS).",
      ["22 ga (0.8 mm) × 40″ (RTB-8) and 49″ (RTB-8A, RTB-8AS)", "Hardened rolls; portable and compact",
       "RTB-8AS on a welded stand, roll height 33.5″ (850 mm)"],
      ["tm-rtb8as", "tm-rtb8"], headline="22 ga × 40 – 49″", cap="[Working length]", manual=True),
    F("tt-duct", P_LOCK, "round", "RM18E power beading machine and LQ15 slitting and bending machine", "Duct beading and slitting", [T["tt-etb"][1]],
      "Two powered machines for round duct: the RM18E puts single and offset beads on round duct — 15 ga (1.8 mm) with a 9-3/8″ throat, "
      "three standard roll sets and a foot pedal; the LQ15 slits 16 ga (1.5 mm) sheet up to 47″ wide and bends it for duct work.",
      ["RM18E: 15 ga (1.8 mm), 9-3/8″ (238 mm) throat, 3 standard roll sets (E1 – E3), 3 more to order, foot pedal",
       "LQ15: slits 16 ga (1.5 mm) sheet up to 47″ (1,200 mm) wide; 42 – 49 in/min",
       "2 HP (1.5 kW) motors"],
      ["tm-rm18e", "tm-lq15"], headline="15 – 16 ga duct", cap="[Capacity, mild steel]"),
]

# =============================================================================================== belt grinders & sanders
P_GRIND = "belt-grinder"
GRIND = [
    F("tt-s75", P_GRIND, "belt", "S-75 · S-150 pedestal belt grinders, 3″ and 6″ × 79″ belt", "S-75 / S-150 belt grinders", T["tt-s75"],
      "The everyday pedestal belt grinder for steel and stainless: a 79″ belt, 3″ wide on the S-75 and 6″ wide on the S-150, running up "
      "to 6,693 ft/min from a 4 HP motor — two speeds on the S-150 — with a quick-adjusting belt angle, a large flat grinding platen and "
      "a contact wheel for radius work. The L models are the lighter versions, 5,709 ft/min, 159 and 181 lb.",
      ["3 × 79″ (S-75) or 6 × 79″ (S-150) belt; contact wheel Ø7-7/8 – 9-7/8″",
       "4 HP; up to 6,693 ft/min — the S-150 has two speeds, 3,346 / 6,693 ft/min",
       "Quick-adjusting belt angle; large flat sanding surface; vibration-free running",
       "L models: lighter build, 5,709 ft/min"],
      ["tm-s75"], headline="3 – 6″ × 79″ belt, 4 HP", cap="[Belt size] belt · [Belt speed]"),
    F("tt-s75h", P_GRIND, "belt", "S-75H · S-150H heavy-duty belt grinders, 5.5 HP, with dust collector on the HB", "S-75H / S-150H heavy-duty", T["tt-s75h"],
      "The heavy-duty pedestal grinder for production deburring: a rigid welded steel base, a 5.5 HP motor driving a 79″ belt at "
      "6,496 ft/min, a 21″ flat grinding length for large parts and a grinding angle that is adjusted and locked. The HB models have a "
      "3/4 HP dust collector built into the base, the HA models a dust drawer.",
      ["5.5 HP (4 kW) at 2,800 rpm; 3 × 79″ or 6 × 79″ belt at 6,496 ft/min", "20.9″ (530 mm) flat grinding length",
       "Adjustable grinding angle with lock; adjustable height", "HB: built-in 3/4 HP dust collector; HA: dust drawer"],
      ["tm-s75h"], headline="3 – 6″ × 79″ belt, 5.5 HP", cap="[Belt size] belt"),
    F("tt-s100", P_GRIND, "belt", "S-100 · S-220 wide-belt grinders, 4″ and 8″ belt", "S-100 / S-220 wide belt", T["tt-s100"],
      "Wide belts for wide work: the S-100 runs a 4 × 48″ belt from 1.5 HP with a quick-adjusting belt angle and a large flat platen; "
      "the S-220 is a radius grinder and surface sander in one, with an 8 × 79″ belt, a Ø7-7/8″ contact wheel, a 19.7 × 8.7″ graphite "
      "platen and an adjustable working position, driven by 4 HP.",
      ["S-100: 4 × 48″ belt, 3,740 ft/min, 1.5 HP, 99 lb", "S-220: 8 × 79″ belt, 5,709 ft/min, 4 HP, 260 lb",
       "Graphite platen pads for flat sanding; contact wheels for radius grinding", "Adjustable belt angle and working position"],
      ["tm-s220", "tm-s100"], headline="4″ and 8″ belts", cap="[Belt size] belt"),
    F("tt-s75f", P_GRIND, "belt", "S-75F mobile floor belt grinder for weld seams, 3″ belt", "S-75F floor grinder", T["tt-s75f"],
      "The belt grinder that goes to the work: on wheels with a handle, it grinds and polishes weld seams on the floor and on parts too "
      "heavy to lift onto a bench machine, with an adjustable depth stop. 3 × 79″ belt at 6,693 ft/min, 4 HP, 165 lb.",
      ["3 × 79″ belt at 6,693 ft/min; 4 HP", "Adjustable depth stop", "On wheels with a handle — grinds weld seams on the floor"],
      ["tm-s75f"], headline="3 × 79″ belt, on wheels", cap="[Belt size] belt"),
    F("tt-s50", P_GRIND, "belt", "S-50 · S-50B compact belt grinders, 2″ and 3″ belt", "S-50 / S-50B compact", T["tt-s50"],
      "Compact belt grinders for the bench: the S-50 combines a 2 × 39″ belt with a sanding disc and is light enough to carry; the S-50B "
      "runs a 3 × 69″ belt from 1 HP and grinds, cleans, brushes and deburrs the edges of all kinds of parts, with a stand as an option.",
      ["S-50: 2 × 39″ belt and sanding disc, 55 lb", "S-50B: 3 × 69″ belt, 1 HP, 110 lb; stand optional", "1 HP (0.75 kW)"],
      ["tm-s50", "tm-s50b"], headline="2″ and 3″ belts, 1 HP", cap="[Belt size] belt"),
    F("tt-s50v", P_GRIND, "belt", "S-50V · S-75V vertical column belt grinders, 2″ and 3″ × 79″ belt", "S-50V / S-75V vertical", T["tt-s50v"],
      "Column belt grinders that take a third of the floor space of a conventional machine: ready to use without assembly, quick belt "
      "changes and sparks directed away from the operator. 2 or 3 × 79″ belt, 1 – 1.5 HP.",
      ["2 × 79″ (S-50V) or 3 × 79″ (S-75V) belt", "1 – 1.5 HP at 2,800 rpm", "Small footprint; quick belt changes; sparks directed for safe work"],
      ["tm-s50v"], headline="2 – 3″ × 79″ belt", cap="[Belt size] belt"),
    F("tt-sdd75", P_GRIND, "belt", "SDD75 multi-purpose belt grinder — flat, contact wheel and tube notching", "SDD75 multi-purpose", T["tt-sdd75"],
      "Three kinds of grinding on one arm and one 3 × 79″ belt: flat grinding on the platen, contact-wheel grinding like a normal belt "
      "grinder, and an adjustable wheel for knives — and, with the optional vise and Ø28 mm roller, notching tube from Ø3/4 to 3″. Two "
      "speeds from a 2 / 3 HP motor; easy belt change.",
      ["3 × 79″ belt, two speeds 2,953 / 5,906 ft/min", "Flat, contact-wheel and knife grinding on one arm",
       "Tube notching Ø3/4 – 3″ with the optional vise and Ø28 mm roller", "Easy belt change"],
      ["tm-sdd75"], headline="3 × 79″ belt, two speeds", cap="[Belt size] belt"),
    F("tt-bgm50", P_GRIND, "belt", "BGM-50HV · BGM-50 belt grinders for knives and tools, 2″ and 1-1/2″ belt", "BGM-50 knife grinders", T["tt-bgm50"],
      "Belt grinders for knife makers and tool rooms: the BGM-50HV runs a 2 × 48″ belt at variable speed up to 3,543 ft/min, works "
      "horizontal or vertical, comes with five contact wheels from 3/4 to 8″ and polyurethane wheels ground flat for precise finishing, "
      "and tilted on its side it works as a bobbin grinder or a pipe notcher. The BGM-50 is a cast-frame 1-1/2″ grinder with inverter "
      "speed control.",
      ["BGM-50HV: 2 × 48″ belt, variable speed to 3,543 ft/min, 2 HP; horizontal and vertical",
       "Five contact wheels 3/4, 1, 1-1/2, 3-1/2 and 8″; sanding disc available", "BGM-50: 1-1/2 × 60″ belt, inverter speed control, 1.5 HP",
       "Sealed bearings; quick belt change and tracking"],
      ["tm-bgm50", "tm-bgm50b"], headline="1-1/2″ and 2″ belts, variable speed", cap="[Belt size] belt"),
    F("tt-sp", P_GRIND, "combo", "SP-2 · SP-3 · SP-6 grinding and polishing machines — belt, disc and wheel on one motor", "SP combination grinders", T["tt-sp"],
      "Combination machines with two working ends on one motor: the SP-2 runs a 2 × 79″ belt and a 10 – 12-5/8″ disc at variable speed "
      "from 3 HP; the SP-6 combines a 2″ belt grinder that tilts from 0 to 90° with a 20″ disc sander and its tilting table; the SP-3 "
      "combines a 3″ belt with a grinding or cup wheel and a polishing wheel, on two speeds.",
      ["SP-2: variable speed 200 – 2,800 rpm; belt and disc; safety cover rotates 360°", "SP-6: 2 × 79″ belt (0 – 90°) and 20″ disc sander, variable speed",
       "SP-3: 3 × 59″ belt (0 – 90°), 10″ grinding wheel or cup wheel and 8″ polishing wheel, two speeds",
       "Accessories for the SP-2: polishing mandrel, keyless chuck, hook-and-loop sanding disc, clamping arbors"],
      ["tm-sp6", "tm-sp2", "tm-sp3"], headline="Belt, disc and wheel on one machine", cap="[Belt size] belt"),
    F("tt-btm250", P_GRIND, "combo", "BTM250 belt and disc sander · BKM-250 belt sander and edge beveller", "BTM250 / BKM-250", T["tt-btm250"],
      "6″ belt machines on a cabinet stand: the BTM250 combines a 6 × 48″ belt that works horizontal or vertical with a 10″ disc and "
      "support tables for both; the BKM-250 bevels steel and non-ferrous parts at 15 to 45°, up to 1/4″ at 45°, with an easy depth "
      "adjustment, a removable top cover for contours and a miter stop.",
      ["6 × 48″ belt; 1.5 HP (1.1 kW)", "BTM250: belt horizontal or vertical, 10″ disc at 2,100 rpm, quick-lock belt change",
       "BKM-250: bevels 15 – 45°, up to 1/4″ (6 mm) at 45°, parts from 3.5″ long", "Dust plates; exhaust connector optional"],
      ["tm-btm250", "tm-bkm250"], headline="6 × 48″ belt", cap="[Belt size] belt"),
    F("tt-ds20", P_GRIND, "disc", "DS-20 20″ disc sanders for metal and TSM300 12″ disc sander", "DS-20 disc sanders", T["tt-ds20"],
      "Disc sanders for metal: the 20″ DS-20 models smooth burrs, chamfer edges for welding and clean up castings on a heavy column, with "
      "a hand-wheel table tilt to 45° down; on the DS-20A the whole table rides up and down the column, the DS-20V has variable speed and "
      "a 25 × 12″ table on a cabinet base. The TSM300 is a 12″ disc sander on a cabinet stand with a tilting table and miter stop.",
      ["20″ (508 mm) disc, 2 HP; 1,100 rpm at 60 Hz, or 500 – 1,800 rpm variable on the DS-20V", "Table tilts 30° up and 45° down by hand wheel",
       "DS-20A: table raised and lowered on the column; dust port for a shop vacuum", "TSM300: 12″ disc, 1.5 HP, tilting table with miter stop"],
      ["tm-ds20", "tm-ds20v", "tm-tsm300"], headline="12″ and 20″ discs", cap="[Disc diameter] disc"),
    F("tt-ds12", P_GRIND, "disc", "DS12 12″ bench disc sanders", "DS12 disc sanders", T["tt-ds12"],
      "Bench disc sanders with a 12″ disc at 1,725 rpm: the DS12 with a 17.6 × 6.1″ table and 3/4 HP, the DS12A with two tables and the "
      "DS12B with a 15.7 × 8.9″ table, 1 HP.",
      ["12″ (304 mm) disc, 1,725 rpm at 60 Hz", "3/4 HP (DS12) or 1 HP (DS12A, DS12B)", "DS12A: two tables"],
      ["tm-ds12"], headline="12″ disc", cap="[Table size]"),
    F("tt-bg", P_GRIND, "bench", "BG-8 · BG-10 bench grinders and BG-60 wire-wheel deburring machines", "Bench grinders", T["tt-bg"],
      "Heavy cast-iron bench grinders with 8 × 1″ and 10 × 1″ wheels, and the BG-60 deburring and polishing machines with a 10″ steel "
      "wire wheel 2-3/8″ wide — two speeds (1,680 / 3,400 rpm at 60 Hz) on the BG-60, 3 HP on the BG-60A.",
      ["BG-8: 8 × 1″ wheels, 3/4 HP; BG-10: 10 × 1″ wheels, 1 HP", "Heavy-duty cast-iron construction",
       "BG-60 / BG-60A: Ø10 × 2-3/8″ wire wheel, 0.012″ wire, 2 – 3 HP"],
      ["tm-bg", "tm-bg60"], headline="8″ and 10″ wheels", cap="[Wheel size]"),
    F("tt-cmd", P_GRIND, "chamfer", "CMD-4 · CMD-80 edge chamfering machines and DM5 hand chamfering tools", "Chamfering machines", T["tt-cmd"],
      "Edge chamfering machines that put a 15 – 45° weld prep or a clean deburred edge on plate, strip and parts: the CMD-80 cuts chamfers "
      "up to 1/4″ (6 mm) from 1.5 HP, the CMD-4 up to 5/32″, and the compact DM5 units 3/16″ at 45°.",
      ["CMD-80: chamfers 0 – 1/4″ (6 mm) at 15 – 45°, 1.5 HP", "CMD-4: chamfers 0 – 5/32″ (4 mm) at 15 – 45°",
       "DM5 / DM5A: compact units, 45° chamfers to 3/16″ (5 mm), 20 lb"],
      ["tm-cmd", "tm-cmd4"], headline="Chamfers to 1/4″", cap="[Chamfer size]"),
    F("tt-md380", P_GRIND, "chamfer", "MD-380A · MD-380B end-surface grinders", "MD-380 end grinders", T["tt-md380"],
      "End-surface grinding machines of Italian design that grind the faces of parts flat: a Ø7-7/8″ wheel on a 4 HP electro-spindle, "
      "0.0004″ vertical increments, coolant, and either a fixed 15.2 × 7″ table (MD-380A) or a Ø15.7″ rotary table (MD-380B); parts up "
      "to 11″ high.",
      ["Ø7-7/8″ grinding wheel at 2,800 rpm on a 4 HP electro-spindle", "Grinding height to 11″ (280 mm); 0.0004″ (0.01 mm) increments",
       "MD-380A fixed table; MD-380B Ø15.7″ rotary table; magnetic chuck optional", "Coolant system; 68 dB"],
      ["tm-md380"], headline="Parts to 11″ high", cap="[Table]"),
    F("tt-dc", P_GRIND, "dust", "DVS14 · DC650 metal dust collectors", "Dust collectors", T["tt-dc"],
      "Dust collectors for grinding and sanding metal: the DVS14 moves 494 CFM through a cyclone and a panel filter with a pull-out tray; "
      "the DC650 filters 650 CFM in three stages down to 1 micron, connects two machines at once through two 4″ inlets and drops the "
      "dust into a removable drawer. For metal dust only — never mix wood dust with metal sparks.",
      ["DVS14: 494 CFM; cyclone separation and panel filter; pull-out tray; 3/4 HP", "DC650: 650 CFM; 30-, 5- and 1-micron filter stages; 1.5 HP single-phase",
       "Two Ø4″ inlets on the DC650 — two machines at a time", "Casters; removable clean-out drawer"],
      ["tm-dc650", "tm-dvs14"], headline="494 – 650 CFM", cap="[Airflow]"),
]

# =============================================================================================== drill presses
P_DRILL = "drill-press"
DRILL = [
    F("tt-t25", P_DRILL, "gear", "T-25 – T-40 gear-head drill presses, 1″ to 1-9/16″ in steel", "T-25 – T-40 gear-head", T["tt-t25"],
      "Gear-head drill presses for the fabrication and maintenance shop: eight spindle speeds through a gearbox — no belts to move — "
      "from 1″ (25 mm) in steel on the T-25 to 1-9/16″ (40 mm) on the T-40. Floor and bench models; the drilling head and table move up "
      "and down and the table swivels; the T-28, T-32, T-35 and T-40 add a mechanical or electric power feed; the C models a 24 V "
      "control and a spindle guard with micro-switch. Tapping is an option on most models.",
      ["Drilling capacity 1 – 1-9/16″ (25 – 40 mm) in steel; MT3 or MT4 spindle", "8 spindle speeds, about 90 – 3,600 rpm at 60 Hz",
       "Power feed 0.004 – 0.013″/rev on the T-28, T-32, T-35, T-40", "Two-speed motors 0.9 – 2.4 HP; 3 HP on the T-40",
       "Safety spindle guard; C models with 24 V control and guard micro-switch; T-25C-H with depth readout"],
      ["tm-t25", "tm-t28", "tm-t32", "tm-t40", "tm-t25c", "tm-t25b"], headline="1 – 1-9/16″ in steel", cap="drills [Drilling capacity in steel] in steel",
      optional=["Tapping (T-25, T-25A, T-25B, T-26, T-26B, T-28B, T-30, T-30B)"]),
    F("tt-t5025", P_DRILL, "gear", "T5025 · T4025 gear-head drill presses with tilting table, 1″", "T5025 / T4025", T["tt-t5025"],
      "Compact gear-head drill presses for 1″ (25 mm) in steel with eight speeds, a forward / reverse switch, preset drilling depth and a "
      "spindle cover with micro-switch: floor models with a round table or a table that tilts ±50°, and bench models; the H models "
      "have a 12.4″ deep throat.",
      ["1″ (25 mm) in steel; MT3; 5.5″ (140 mm) spindle travel", "8 speeds, 120 – 3,480 rpm at 60 Hz; two-speed 3/4 / 1 HP motor",
       "Tilting table ±50° (T5025-3A, T5025H); T-slotted base", "Forward / reverse switch; preset drilling depth; spindle cover micro-switch"],
      ["tm-t5025", "tm-t5025-1a", "tm-t4025"], headline="1″ in steel", cap="throat [Throat (spindle to column)]"),
    F("tt-t50", P_DRILL, "gear", "T-50 heavy gear-head drill presses, 2″, and TX530 inverter drill presses", "T-50 / TX530 heavy-duty", T["tt-t50"],
      "The heavy end of the range: the T-50 and T-50E drill 2″ (50 mm) in steel and tap M30, with twelve speeds, a three-step power feed, "
      "hardened gears and an MT4 spindle; the T-50E has a 15.7″ deep throat, a 23.6 × 21.7″ table that swivels and coolant built into "
      "the base. The TX530 drill presses run on a frequency inverter with a two-range gearbox — variable speed with full torque at low "
      "speed — for 1-1/4 and 1-9/16″ holes and 3/4 to 1″ taps, forward and reverse.",
      ["T-50 / T-50E: 2″ (50 mm) in steel, 2-1/4″ in cast iron; taps M30 in steel", "12 speeds 75 – 1,525 rpm at 60 Hz; power feed 0.004 / 0.008 / 0.012″/rev",
       "T-50E: 15.7″ (400 mm) throat, swivelling table, coolant in the base", "TX530 / TX530A: inverter speed control with high / low gear range; 3 HP; coolant; guard micro-switch",
       "TX530A: mechanical power feed"],
      ["tm-t50", "tm-t50e", "tm-tx530"], headline="To 2″ in steel", cap="[Drilling capacity]"),
    F("tt-tb", P_DRILL, "column", "TB24 · TB28 · TB36 column drills — belt drive or inverter", "TB column drills", T["tt-tb"],
      "Industrial column drills with a V-belt drive and a quality motor, a digital speed display, forward / reverse, a precisely finished "
      "table with cross T-slots, a large base plate, an adjustable chuck guard and a work light, for 15/16 to 1-5/16″ (24 – 34 mm) in steel. "
      "The V models run on a frequency converter for stepless speed control — up to 6,500 rpm — on single-phase power, with coolant on "
      "the TB28V and TB36V.",
      ["24, 28 and 34 mm (15/16, 1-1/8 and 1-5/16″) in steel; MT2, MT3, MT4", "TB: 7 – 16 belt speeds; TB…V: stepless 35 – 6,500 rpm by frequency converter, 1-phase",
       "Digital speed display; forward / reverse; easy tool change", "T-slotted table and base; adjustable chuck guard; work light",
       "Coolant on the TB28V and TB36V"],
      ["tm-tb", "tm-tbv"], headline="15/16 – 1-5/16″ in steel", cap="drills [Drilling capacity in steel] in steel"),
    F("tt-wtz", P_DRILL, "vs", "WTZ variable-speed drill presses, 1/2″ and 5/8″, and WTZ-16T drilling and tapping press", "WTZ variable-speed", T["tt-wtz"],
      "Variable-speed bench and floor drill presses with a digital speed display for 1/2″ and 5/8″ holes in steel, and the WTZ-16T, "
      "which drills 5/8″ and taps M12: switched to tapping, the spindle stops in 0.2 s and reverses to back the tap out, with a laser "
      "cross-hair and a digital depth readout in mm or inch.",
      ["1/2″ (13 mm) and 5/8″ (16 mm) in steel; MT2", "Variable speed 500 – 2,600 rpm with digital display",
       "Bench models and the WTZ-16JF floor model", "WTZ-16T: taps M12 with automatic reverse; spindle runout under 0.0004″; laser cross-hair; digital depth readout"],
      ["tm-wtz", "tm-wtz16q", "tm-wtz16t"], headline="1/2 – 5/8″ in steel", cap="drills [Drilling capacity in steel] in steel"),
    F("tt-vise", P_DRILL, "vise", "Drill press vises and welding angle clamps", "Vises and clamps", T["tt-vise"],
      "Vises for the drill press and the mill: the BSM-N drill press vises with changeable prismatic jaws, the TSL vises (Q models with a "
      "quick lock), the TMS vises with slotted bases, the TQ tilting, swivel and compound precision vises, and the AC welding angle clamps "
      "that hold tube and angle at 90° for welding.",
      ["BSM / TSL / TMS: jaw widths 3-1/8 – 7-7/8″ (80 – 200 mm)", "TQ: 4 – 6″ precision vises — tilting (TQA), swivel (TQB), compound (TQC)",
       "AC-60 / AC-100 / AC-100H welding angle clamps; AC-100H for box and round tubing"],
      ["tm-vise", "tm-vise-tq", "tm-ac100h"], headline="Vises 3 – 8″", cap="[Jaw width] jaws", manual=True),
]

# =============================================================================================== milling machines
P_MILL = "milling-machine"
MILL = [
    F("tt-mill-turret", P_MILL, "turret", "Turret milling machines, ISO40, with horizontal spindle on the W models", "Turret mills",
      [T["tt-mill"][0]],
      "Knee-type turret mills for the tool room and the maintenance shop: the 4H with a 50 × 10″ table, shown with power feed and a digital readout; the X6325W "
      "and X6332WA with a horizontal spindle as well as the vertical head, power feed on X and Y and a motorized knee; the X6336 and "
      "X6336WA with a high-speed head (70 – 7,200 rpm), power feed on all three axes and hardened square ways. The head swivels ±45° "
      "front to back and ±90° left to right; on the WA models the table swivels ±45° too.",
      ["Tables 50 × 10″ to 64.2 × 14.2″; X travel 23.6 – 39.4″", "Vertical head 80 – 5,440 or 70 – 7,200 rpm; horizontal spindle 40 – 1,800 rpm (W models)",
       "Power feed X, Y; motorized Z — or power feed on all three axes (X6336)", "3 – 5.5 HP; quill travel 5″ (127 mm)",
       "Table swivel ±45° (X6332WA, X6336WA)"],
      ["tm-x6332", "tm-4h", "tm-x6325", "tm-x6336"], headline="Tables to 64 × 14″", cap="[Table]"),
    F("tt-mill-univ", P_MILL, "univ", "XQ6226 · X6436 universal milling machines, ISO40 / ISO50", "XQ6226 / X6436 universal", [T["tt-mill"][1]],
      "Universal milling machines with a horizontal spindle and a vertical head that swivels through 360°: the XQ6226 range with a "
      "44 – 50″ table, hardened ways, an ISO40 spindle and power feed on X and Y (motorized knee on the B), and the X6436 with ISO40 "
      "vertical and ISO50 horizontal spindles, a 52″ table and servo feeds with rapid traverse on all three axes.",
      ["Horizontal milling to Ø5″ (125 mm); vertical milling to Ø1 – 1-1/8″", "XQ6226: 40 – 1,600 rpm; table 44 – 50″; power feed X, Y",
       "X6436: servo feed and rapid traverse X, Y, Z; 5.5 / 7.5 HP", "Hardened guideways; head swivels 360°"],
      ["tm-xq6226", "tm-xq6226w", "tm-x6436"], headline="Tables 44 – 52″", cap="[Table]"),
    F("tt-mill-heavy", P_MILL, "univ", "LM-1450 · X5750 heavy universal milling machines, ISO50", "LM-1450 / X5750 heavy", [T["tt-mill"][2]],
      "Heavy ISO50 universal mills for production and large parts: the LM-1450 range with power feed and rapid traverse on all three "
      "axes, a head that swivels 360°, hardened three-axis ways and a hardened and ground table — 64 to 79″ long, with up to 15 HP on "
      "the horizontal spindle; the X5750 and X5750A with ball screws and three separate servo feed motors, a mechanical speed change in "
      "the head, an extra column supporting the table and central lubrication.",
      ["Tables 63 – 79″ (1,600 – 2,000 mm); X travel 31.5 – 55.1″", "ISO50 spindles; horizontal 30 – 1,800 rpm, vertical 60 – 1,700 rpm",
       "Power feed and rapid traverse on X, Y, Z; servo feed on the LM-1450B; ball screws and servo motors on the X5750",
       "5.5 – 15 HP; 5,842 – 9,921 lb", "Digital readout at extra cost"],
      ["tm-lm1450", "tm-lm1450b", "tm-lm1450d", "tm-x5750"], headline="Tables 63 – 79″, ISO50", cap="[Table]", optional=["Digital readout (DRO)"]),
    F("tt-zx", P_MILL, "drill", "ZX drilling and milling machines, 2″ drilling", "ZX drill-mills", T["tt-zx"],
      "Drilling and milling machines that drill 2″ (50 mm), face-mill Ø4 – 5″ and tap M16 on one column: the ZX5325 with a rotary milling "
      "head and a table that swivels ±45°, belt drive (ZX5325) or gear head (ZX5325C); the ZX7550C, ZX7550CW, ZX6350C and ZX6350Z on a "
      "knee, the W and 6350 models with a horizontal spindle as well.",
      ["Drilling 2″ (50 mm); face milling Ø4 – 5″; tapping M16", "Tables 31.5 × 9.4″ to 49.2 × 12.6″",
       "Vertical spindle 90 – 2,400 rpm; horizontal spindle 38 – 1,335 rpm on the W and 6350 models", "1.5 – 3 HP"],
      ["tm-zx5325", "tm-zx7550", "tm-zx6350"], headline="2″ drilling", cap="[Table]", optional=["Power feed on Y and Z", "Digital readout (DRO)"]),
    F("tt-mill-small", P_MILL, "drill", "TX-20 mini mill-drill and DM-20 radial drill-mill", "TX-20 / DM-20", T["tt-mill-small"],
      "Small machines for the bench and the repair shop: the TX-20 mill-drill with a 27.6 × 7.1″ X-Y table and variable speed for "
      "recessing, surface and end milling, grooving and angled drilling; the DM-20 radial drill-mill with a 19.7″ arm reach, a cross "
      "table and a box table, for 3/4″ drilling and 5/8″ end milling.",
      ["3/4″ (20 mm) drilling", "TX-20: variable 50 – 2,250 rpm, MT2, cabinet stand", "DM-20: 5 speeds 210 – 2,000 rpm, MT3 / R8, arm reach 19.7″",
       "DM-20 options: vise, coolant pump, milling chuck set, lamp"],
      ["tm-tx20", "tm-dm20"], headline="3/4″ drilling", cap="[Drilling capacity] drilling"),
    F("tt-slot", P_MILL, "slot", "B5012 keyseater and B5013 slotting machine", "Keyseater and slotter", T["tt-slot"],
      "Machines for keyways and splines: the B5012 keyseater cuts keyways in single and small-batch work, especially in blind holes, "
      "and its column does not limit the size of the part; the B5013 slotting machine has a head that swivels 90° left and right, a "
      "5″ stroke and 60 – 350 strokes a minute in six steps.",
      ["B5012: 4.7″ (120 mm) stroke; parts Ø16-1/2″ × 4-3/4″ on the table, larger parts beyond it", "B5013: 5″ (125 mm) stroke, 60 – 350 strokes/min, head swivels ±90°",
       "Heavy cast-iron construction"],
      ["tm-b5013", "tm-b5012"], headline="Keyways and splines", cap="[Stroke, max] stroke"),
]

# =============================================================================================== CNC machine tools
P_CNC = "cnc-machine-tools"
CNC = [
    F("tt-vmc", P_CNC, "vmc", "VMC8046 · VMC10562 vertical machining centres, BT40, 8,000 rpm", "VMC vertical machining centres", [T["tt-vmc"][0]],
      "Vertical machining centres with a 39.4 × 21.7″ table that carries 1,764 lb: the VMC8046 with linear rolling guideways on X and Y, "
      "hardened box ways on Z, a 7.5 / 10 HP spindle and a 16-tool changer; the VMC10562 with a wide bed, a heavy column, roller linear "
      "guideways on all three axes, a 15 HP spindle, 945 ipm rapids and a 24-tool changer. Mitsubishi, Fanuc or Siemens CNC to order.",
      ["Travel 31.5 – 41.3 × 17.3 – 24.4 × 19.7 – 24″", "BT40 spindle to 8,000 rpm; 7.5 / 10 HP or 15 HP",
       "Positioning ±0.0006″, repeatability ±0.0001 – 0.0002″", "16- or 24-tool automatic tool changer",
       "VMC10562: floating-cushion tool unclamping protects the spindle bearings; oil separation keeps the coolant clean"],
      ["tm-vmc10562", "tm-vmc8046"], headline="BT40, 8,000 rpm", cap="[Tool changer]"),
    F("tt-boring", P_CNC, "boring", "TXK · TH-800 CNC boring and milling machines, BT50", "CNC boring mills", T["tt-boring"],
      "CNC boring and milling machines for large prismatic parts — drilling, reaming, tapping, milling and boring several faces in one "
      "set-up: the TXK68 with a worm-gear dividing table, the fixed-column TXK160 range with a 51.2 × 23.6″ table, heavy linear "
      "guideways and an optional rotary B axis, and the TH-800 horizontal machining centre with an 800 × 800 mm B-axis table and a "
      "40-tool chain magazine.",
      ["BT50 spindles; 7.5 / 10 HP; up to 3,000 rpm (TXK160)", "Travel to 59 × 31.5 × 19.7″ (TXK160) and 63″ Y (TXK160D)",
       "4-axis machining with the rotary table (TXK68, TXK160B, TH-800)", "TH-800: 40-tool chain magazine, 13 s tool change",
       "Mitsubishi or Fanuc CNC"],
      ["tm-th800", "tm-txk160", "tm-txk160d", "tm-txk68"], headline="BT50, 4-axis", cap="[Table]"),
    F("tt-cnc-lathe", P_CNC, "lathe", "CTK6416 slant-bed CNC lathe with gang tooling", "CTK6416 CNC lathe", T["tt-cnc-lathe"],
      "A compact 45° slant-bed CNC lathe for small turned parts in series: linear guides, gang (parallel) tooling for fast tool changes, "
      "a one-piece bed and base, a 3,000 rpm spindle on 7.5 HP and AC servo axes with 0.00004″ resolution. Mitsubishi or Fanuc control.",
      ["Swing over bed 11.8″ (300 mm), over cross slide 5.9″ (150 mm)", "X / Z travel 11.8 / 11.8″; 472 ipm rapids",
       "3,000 rpm spindle, 7.5 HP; MT5", "45° slant bed for chip clearing; small footprint"],
      ["tm-ctk6416"], headline="Swing 11.8″", cap="swing [Swing over bed]"),
    F("tt-cnc-slot", P_CNC, "vmc", "CNC100 · CNC120 slot machining centres for quartz and glass", "CNC100 / CNC120", [T["tt-vmc"][1]],
      "CNC machining centres built to cut grooves in quartz, glass and similar materials with Ø4 – 7″ saw discs — for the optoelectronic "
      "and photovoltaic industry — with a patented spindle structure, outboard slurry collection and 709 ipm rapids.",
      ["Saw discs Ø4 – 7″ (100 – 180 mm); spindle 200 – 4,500 rpm", "Tables 39.4 × 19.7″ and 47.2 × 23.6″",
       "Positioning ±0.0006″, repeatability ±0.0002″", "Mitsubishi or Fanuc CNC"],
      ["tm-cnc100"], headline="Saw discs Ø4 – 7″", cap="[Table]"),
]

# =============================================================================================== CNC plasma
P_PLASMA = "cnc-plasma-table"
PLASMA = [
    F("tt-plasma-servo", P_PLASMA, "table", "PC 4′×4′ · PC 5′×10′ CNC plasma tables with servo drives", "PC 4×4 / 5×10 plasma tables", [T["tt-plasma"][1]],
      "Industrial CNC plasma tables: servo motors on X and Y over precision guides, a Z axis with automatic torch height detection, a "
      "welded frame that carries plate up to 1″ thick and a control console with the programming software. The 4×4 cuts over water "
      "pans; the 5×10 has rack-and-gear drives and a downdraft dust-collection table. With a 45, 65 or 85 A plasma source they cut "
      "5/16″, 3/8″ or 1/2″ — Hypertherm and other sources on request.",
      ["Cutting area 48 × 48″ or 60 × 120″", "Servo drives; accuracy ±0.006″, repeatability ±0.004″",
       "Automatic torch height control; 5.9″ (150 mm) Z stroke", "Cutting thickness 5/16 – 1/2″ (8 – 12 mm) with 45 – 85 A sources",
       "4×4: water pans; 5×10: downdraft dust collection"],
      ["tm-pc510", "tm-pc-console"], headline="4 × 4 ft and 5 × 10 ft", cap="[Cutting area]", optional=["Plasma source of another brand (Hypertherm …)"]),
    F("tt-plasma-compact", P_PLASMA, "table", "PC 2′×2′ · PC 2′×4′ compact CNC plasma tables", "PC 2×2 / 2×4 plasma tables", [T["tt-plasma"][0]],
      "Compact CNC plasma tables for steel, aluminum, galvanized and coated sheet: a fully welded frame, hardened and ground slideways "
      "with wipers, stepper motors on X and Y, water-assisted cooling and a hand-held controller that runs programs from a USB stick — "
      "no computer needed — with easy programming software; supplied with the plasma source and torch.",
      ["Cutting area 24 × 24″ or 24 × 48″", "3/8″ (10 mm) with a 40 A source, 1″ (26 mm) with 100 A",
       "Stepper motors; ±0.04″ per 39″", "Hand-held USB controller; plasma source and torch included"],
      ["tm-pc24"], headline="2 × 2 ft and 2 × 4 ft", cap="[Cutting area]"),
    F("tt-pcp", P_PLASMA, "pipe", "PCP CNC plasma pipe cutting machines, Ø2 – 11-3/4″ × 10 – 20 ft", "PCP pipe cutters", T["tt-pcp"],
      "CNC plasma pipe cutting for pipe and tube from Ø2 to 11-3/4″ (50 – 300 mm) with walls to 1/2″: copes, saddles, holes and "
      "cut-offs for structural and process piping, programmed without special skills. The PCP 300×3000E holds the pipe in chucks at both "
      "ends with a dust exhaust on both sides; the 300×3000 and 300×6000 rotate the pipe on gas-spring chuck supports and ball-transfer "
      "cradles; modular bed extensions take longer pipe.",
      ["Pipe Ø2 – 11-3/4″ (50 – 300 mm), wall 0.04 – 1/2″ (1 – 12 mm)", "Pipe length 10 ft (3 m) or 20 ft (6 m); modular bed extensions",
       "Cutting 200 ipm; rotation up to 100 rpm", "Removable chip tray and dust exhaust (3000E); gas-spring supports and ball cradles (3000, 6000)"],
      ["tm-pcp3000e", "tm-pcp6000"], headline="Pipe Ø2 – 11-3/4″", cap="[Pipe length]"),
]

# =============================================================================================== metal shaping
P_SHAPE = "english-wheel"
SHAPE = [
    F("tt-ew", P_SHAPE, "wheel", "English wheels, 22 – 14 ga, 18 – 45″ throat", "English wheels", [T["tt-ew"][0], T["tt-ew2"][0]],
      "English wheels stretch sheet into compound curves — fenders, hoods, tanks, aircraft and boat panels — by rolling it between a "
      "flat upper wheel and a crowned lower anvil. Ten models from the F0.8×450 for 22 ga with an 18″ throat to the F1.5×1100 with a "
      "45″ throat and the heavy F2.0 wheels for 14 ga: rigid welded C-frames, hardened wheels, sets of lower anvils with radii from flat "
      "to 12″, quick-release lower anvils and foot pressure control on the F1.2×1000.",
      ["22 ga (0.8 mm) to 14 ga (2 mm) mild steel; aluminum and copper heavier", "Throat 18 – 45″ (450 – 1,145 mm)",
       "Upper wheel Ø7-5/8 – 8″; 5 – 10 lower anvils, flat to 12″ radius", "Quick-release lower anvil with locking cam; foot pressure control (F1.2×1000)",
       "Rigid welded C-frames on stands with anvil storage"],
      ["tm-f1570", "tm-f15110", "tm-f2076", "tm-f1210", "tm-f12100", "tm-f2063", "tm-f1256"], headline="22 – 14 ga, 18 – 45″ throat",
      cap="[Capacity, mild steel] · throat [Throat depth]", manual=True),
    F("tt-ph", P_SHAPE, "hammer", "Planishing hammers and power hammers, 18 – 16 ga, 12 – 30″ throat", "Planishing and power hammers",
      [T["tt-ph"][0], pick(T["tt-ph"][1], ["PH-20D", "PH-30D"], title="PH-20D · PH-30D", sub="Electric power hammers")],
      "Hammers that smooth and shape panels after the English wheel: the PPH pneumatic planishing hammers with 12″ and 24″ throats, nine "
      "radius anvils and a foot pedal; the PPH-610 that forms and beads 16 ga with quick-change upper dies; the UFP-2 that is a planishing "
      "hammer and an English wheel in one; and the PH-20D and PH-30D electric power hammers with 20″ and 30″ throats, variable speed up "
      "to 1,700 blows a minute and 16 ga steel or 12 ga aluminum capacity.",
      ["PPH-12 / PPH-24: 18 ga, 12 / 24″ throat, 9 radius anvils from 3/4″ to 12″ and flat, foot pedal", "PPH-610: 16 ga, 24″ throat, 90 – 120 psi, 3-position air flow",
       "PPH500: 1, 2 and 3″ radius anvils, 875 – 1,350 blows/min, 50 – 100 psi", "PH-20D / PH-30D: 2 HP electric, variable 0 – 1,700 / 0 – 1,400 blows/min, 16 ga steel, 12 ga aluminum",
       "UFP-2: planishing hammer and English wheel on one stand"],
      ["tm-ph20d", "tm-pph610", "tm-pph12", "tm-ph30d", "tm-ufp2", "tm-anvils"], headline="18 – 16 ga", cap="throat [Throat depth]"),
    F("tt-ss", P_SHAPE, "shrink", "Shrinker-stretchers, 18 – 16 ga — bench, hand and foot-operated", "Shrinker-stretchers", T["tt-ss"],
      "Shrinkers gather the edge of a flange to curve it inward, stretchers spread it to curve it outward — together they bend angle and "
      "flanged parts into curves and S-shapes without cutting and welding. Bench models with 1″, 2-3/4″ and 8″ throats, the industrial "
      "SM-16B, the SS-12P hand tool and foot-operated models on stands that leave both hands free.",
      ["18 ga (1.2 mm) and 16 ga (1.5 mm) mild steel", "Throat 1″, 2-3/4″, 6″ and 8″", "Shrinking and stretching jaws; aluminum jaws optional (FSM-16)",
       "Foot pedal models: SS-18FD (two heads), SS-16F, SG-18F, FSM-16 on a wheeled base"],
      ["tm-ss18fd", "tm-ss16f", "tm-fsm16", "tm-ss16", "tm-sm16b", "tm-ss-jaws"], headline="18 – 16 ga", cap="[Capacity] · throat [Throat depth]", manual=True),
    F("tt-pic50", P_SHAPE, "wheel", "PIC50 diamond roller former, 20 ga × 50″", "PIC50 diamond roller", [T["tt-ew2"][1]],
      "A motorized roller former that embosses a 2-3/4″ (70 mm) diamond pattern into 20 ga sheet up to 50″ wide — decorative panels for "
      "doors, cabinets, food trucks and restorations — on a welded frame with a 1 HP motor and 9 – 16 rpm adjustable speed.",
      ["20 ga mild steel × 50″ (1,270 mm)", "2-3/4 × 2-3/4″ (70 × 70 mm) diamonds", "1 HP; 9 – 16 rpm adjustable"],
      ["tm-pic50", "tm-pic50-sample"], headline="20 ga × 50″", cap="[Capacity]"),
    F("tt-hammer", P_SHAPE, "forge", "C41 self-contained pneumatic forging hammers, 35 – 165 lb ram", "C41 air forging hammers", T["tt-hammer"],
      "Self-contained air hammers for blacksmiths and forges: the motor drives a compressor cylinder in the hammer itself — no shop air "
      "needed — and the ram strikes 210 to 270 blows a minute. Drawing out, upsetting, punching, chiselling, forge welding, bending and "
      "twisting, or forging in bolster dies, from 3/4″ square stock on the C41-16KG to 2-1/2″ square and Ø3-3/8″ round on the C41-75KG.",
      ["Ram weight 35 – 165 lb (16 – 75 kg); 210 – 270 blows/min", "Blow energy 133 – 664 ft·lbf (180 – 900 J)",
       "Stock to 2-1/2″ (65 mm) square, Ø3-3/8″ (85 mm) round", "2 – 9.4 HP; separate anvil block 441 – 1,874 lb"],
      ["tm-c41-40", "tm-c41-16"], headline="35 – 165 lb ram", cap="[Ram (falling) weight] ram"),
]

# =============================================================================================== arbor & bench presses
P_ARBOR = "arbor-press"
ARBOR = [
    F("tt-arbor", P_ARBOR, "arbor", "Arbor presses, 1/2 to 8 tons, and hand presses", "Arbor presses", T["tt-arbor"],
      "Hand arbor presses for pressing bearings, bushings, pins and gears in and out, broaching keyways and staking: steel bodies, a "
      "four-position base plate and square rams from 3/4″ to 2-3/8″, from the 1/2-ton AP-1/2 to the 8-ton AP-8 with 17.7″ of height and "
      "a 10″ diameter capacity. The rack-and-pinion AP-1S and AP-2S, the ratchet RAP-2 and RAP-3 and the MP-800 flywheel press cover "
      "repeated small-part work.",
      ["1/2 – 8 tons; work height to 17.7″, diameter to 10.2″", "Four-position base plate; square rams 3/4 – 2-3/8″",
       "Rack-and-pinion AP-1S / AP-2S with 2,248 – 4,496 lbf", "Ratchet RAP-2 / RAP-3 for 2 – 3 tons with less effort"],
      ["tm-ap5", "tm-ap8", "tm-rap"], headline="1/2 – 8 tons", cap="[Capacity]", manual=True),
    F("tt-bench-press", P_ARBOR, "bench", "BP-3T · EBP-10T bench presses and BP3-F combination bench press", "Bench presses", T["tt-bench-press"],
      "Bench presses for the sheet-metal and HVAC shop: the BP-3T hand press with a 12″ throat takes industry-standard punches and dies "
      "for round, square and oblong holes, punch-and-flare and punch-and-bead tools and louver tooling, and works as an arbor press; the "
      "EBP-10T is a 10-ton hydraulic version with a 25″ throat and 6″ tool opening that takes all the BP-3T tooling; the BP3-F mounts "
      "four tools at once — bend, stretch, corner punch and shrink — for production.",
      ["BP-3T: 3 tons, 12″ throat, welded plate, bronze bushings", "EBP-10T: 10 tons hydraulic, 25″ throat, 4″ stroke",
       "BP3-F: four stations — two 12″ throats and two 3″ throats", "Tooling: shear 16 ga, 90° bend 3/8″, corner punch 16 ga, louver punches 1 – 5″, punch & flare and punch & bead 1 – 3″"],
      ["tm-bp3t", "tm-ebp10t", "tm-bp3f", "tm-louver"], headline="3 – 10 tons", cap="[Capacity]",
      optional=["Shear kit", "90° bend kit", "Corner punch and corner radius punch", "Louver punches", "Punch & flare and punch & bead kits", "Universal tool stand"]),
    F("tt-tpunch", P_ARBOR, "punch", "TP-12 · TP-24 manual turret punch presses, 12 stations", "TP turret punches", T["tt-tpunch"],
      "Manual turret punch presses with twelve round punches from 3/16 to 1-1/4″ on a rotating turret: 6,000 kg of punching force from "
      "a hand lever, 1/4″ capacity, a 12″ (TP-12) or 24″ (TP-24) throat, on an open stand (A) or a cabinet stand with a table (B). "
      "Square, oval, rectangular and other shaped punches and dies to order, up to 2-1/4″.",
      ["12 stations, round punches 3/16 – 1-1/4″ (metric 5 – 32 mm)", "6.6 US tons (6,000 kg) by hand lever; 1/4″ (6 mm) capacity",
       "12″ or 24″ throat; open stand or cabinet stand", "Shaped punches and dies to order, up to 2-1/4″"],
      ["tm-tp12b", "tm-tp12a"], headline="12 stations, 1/4″", cap="throat [Throat depth]", manual=True),
    F("tt-riveter", P_ARBOR, "rivet", "XM orbital riveting machines, rivets Ø3/16 – 1-3/16″", "XM orbital riveters", T["tt-riveter"],
      "Hydraulic orbital (rolling) riveters: the riveting head rolls the rivet end into shape instead of hammering it, with about a tenth "
      "of the force of punch riveting — the part keeps its fit, the head comes out smooth, without vibration or noise. Six sizes for "
      "solid rivets from 3/16 to 1-3/16″; with other tools the machine works as a normal press. Hinges, chain links, brake parts, "
      "appliances and hardware.",
      ["Rivets Ø3/16 – 1-3/16″ (5 – 30 mm); 1,911 – 22,481 lbf", "11 rivet head forms", "Tables Ø4.7″ to 19.7 × 14″",
       "Low noise, no vibration; replaces hammering, punching and hot riveting"],
      ["tm-xm8"], headline="Rivets to 1-3/16″", cap="rivets to [Rivet diameter, max]"),
]

# =============================================================================================== tube & pipe benders
P_TUBE = "tube-bender"
TB = T["tt-tb-manual"]
TUBE = [
    F("tt-jtb", P_TUBE, "power", "JTB-40 · JTB-50 · JTB-80 hydraulic PLC tube benders, to 3-1/8″", "JTB hydraulic tube benders", [TB[4]],
      "Hydraulic tube benders with a PLC: one-touch operation for single parts and programmed batches of round tube, stainless tube, "
      "square tube and round bar, bending to 180°. The JTB-40 takes Ø5/8 – 1-9/16″ tube, the JTB-50 Ø5/8 – 2″ round and 2″ square with "
      "walls to 0.2″, the JTB-80 Ø1-9/16 – 3-1/8″ round and 3-1/8″ square with walls to 0.35″ and a movable control pedal.",
      ["Round tube Ø5/8 – 3-1/8″ (16 – 80 mm); square tube to 3-1/8″; round bar", "Bends to 180°; PLC control for programmed batches",
       "JTB-50: dies 25, 32, 38, 48 mm; JTB-80: 76 × 265 mm and 60 × 210 mm CLR", "3 – 7.5 HP drive plus hydraulic motor"],
      ["tm-jtb50", "tm-jtb40", "tm-jtb80"], headline="Tube to Ø3-1/8″", cap="[Round tube]"),
    F("tt-tbm60", P_TUBE, "power", "TBM-60 electric bender and HTB-25T 25-ton hydraulic tubing bender", "TBM-60 / HTB-25T", [TB[2]],
      "Two benders for the fabrication shop and the roll-cage builder: the TBM-60 electric top bender bends tube, pipe, square, "
      "rectangular, solids and profiles from 1/4 to 2-1/2″ OD to 180° at two speeds, with a remote foot pedal, transport wheels and an "
      "optional two-axis positioner; the HTB-25T puts 25 tons of air-hydraulic force on round and square tube 3/4 – 2″ with walls to "
      "0.125″, portable, with an engraved reference scale for repeatable bends.",
      ["TBM-60: 1/4 – 2-1/2″ OD, 0 – 180°, 1.7 / 3.4 rpm, 2 HP, foot pedal", "HTB-25T: 25-ton hydraulic ram with air-hydraulic pump; 90° bends",
       "HTB-25T dies: 1″ × 4″ CLR standard; 3/4 – 2″ round and square dies optional; floor stand optional", "TBM-60: one 1″ tube kit standard; two-axis positioner optional"],
      ["tm-tbm60", "tm-htb25t", "tm-tbm60-pos", "tm-htb25t-stand"], headline="Tube to 2-1/2″", cap="[Capacity]"),
    F("tt-tb3", P_TUBE, "power", "TB-3 · HTB-1000 benders for 2″ schedule 40 pipe — hand, air and electric hydraulic", "TB-3 / HTB-1000 pipe benders", [TB[1]],
      "The bender family for 2″ schedule 40 pipe and roll-cage tube: the TB-500 ratchet bender for 2-1/2″ tube; the TB-3 hand bender; "
      "the TB-3A with a 10-ton air / hydraulic jack; the TB-3B and TB-3C with a 10-ton cylinder with 12″ stroke on a caster stand with "
      "die rack, air-hydraulic or electric-hydraulic; and the HTB-1000 electric-hydraulic bender, about three times faster than an "
      "air-hydraulic unit. Dies for 120°, 180° and 240°.",
      ["2″ schedule 40 pipe (0.154″ wall); TB-500: 2-1/2 × 0.120″ tube", "Standard dies 1″ × 3″, 1-1/2″ × 5″, 1-3/4″ × 6″ (120°)",
       "Optional round dies 3/4 – 2″ and square dies 3/4 – 1-1/2″; 120°, 180° and 240° dies", "HTB-1000: 1 HP electric-hydraulic, aluminum-bronze bushings at the pivots"],
      ["tm-htb1000", "tm-tb3b", "tm-tb3c", "tm-tb500", "tm-tb3"], headline="2″ schedule 40 pipe", cap="[Drive]"),
    F("tt-exhaust", P_TUBE, "power", "HTB-2000 exhaust tube bender and HTES-3000 expander-swager", "Exhaust benders", [TB[5]],
      "For the exhaust and muffler shop: the HTB-2000 hydraulic bender bends tube from 1 to 3″ with 58,000 lb of force, with a built-in "
      "swager / expander for end finishing, a knee-pad control, a depth-of-bend indicator and a complete tooling package; the HTES-3000 "
      "expands tube 1 – 3-1/2″ and swages 1 – 3″ on a portable cart.",
      ["HTB-2000: tube 1 – 3″ OD, 0.098 – 0.118″ wall; 58,000 lb; 4 – 5.5 HP", "Tooling package: radius dies 3 – 5″, back shoes, collets, ball and swage dies, flare tool",
       "HTES-3000: expands 1 – 3-1/2″, swages 1 – 3″; 3,000 psi; Ø3.5″ cylinder, 6.5″ stroke", "Swivel casters with brakes"],
      ["tm-htb2000", "tm-htes"], headline="Exhaust tube 1 – 3″", cap="[Capacity]"),
    F("tt-hb-pipe", P_TUBE, "pipe", "HB hydraulic pipe benders, 8 – 16 tons, 1/2 – 3″ pipe", "HB hydraulic pipe benders", [TB[3]],
      "Hydraulic pipe benders for plumbing, electrical and maintenance work: a hand pump (or, on the EHB-10, an electric pump) drives "
      "the ram that pushes the pipe into the bending die. 8 to 16 tons, with die sets from 1/2″ to 2″, and to 3″ on the HB-16.",
      ["8, 10, 12 and 16 tons; ram stroke 4.7 – 9.4″", "Dies 1/2 – 2″; 1/2 – 3″ on the HB-16", "EHB-10: electric pump, 1 HP 1-phase or 3/4 HP 3-phase",
       "HB-8: dies 3/4, 1, 1-1/2, 1-5/8, 1-3/4″"],
      ["tm-hb12", "tm-ehb10", "tm-hb10", "tm-hb8"], headline="1/2 – 3″ pipe", cap="[Force]"),
    F("tt-tb-hand", P_TUBE, "hand", "Hand tube benders, 1/4 – 1″", "Hand tube benders", [TB[0]],
      "Hand benders for small tube: the TB-180 bends 3/8 – 1″ tube to 180° in one pull in a bench vise, with an eccentric lock roll and "
      "an angle indicator; the RB-1 bends 1/2 – 1″ tube to 270° on a stand; the RB-2 bends 1/4 – 5/8″ tube with 3D and 5D dies; the "
      "MY-22 comes in a carry case with dies for 3/8 – 7/8″ round and 3/4 – 1″ square tube.",
      ["TB-180: 3/8 – 1″ OD, 0.049 – 0.095″ wall, 180° in one pull", "RB-1: 1/2 – 1″, 270°; RB-2: 1/4 – 5/8″, 3D and 5D dies",
       "MY-22: round 3/8 – 7/8″, square 3/4 and 1″, carry case", "Vise or stand mounting"],
      ["tm-tb180", "tm-rb1", "tm-my22"], headline="Tube 1/4 – 1″", cap="[Tube size]", manual=True),
]

NEW_FAMILIES = BRAKES + LOCK + GRIND + DRILL + MILL + CNC + PLASMA + SHAPE + ARBOR + TUBE
