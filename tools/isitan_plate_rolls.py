"""İşitan section: plate rollers and slip rolls (catalogue pages 4–27)."""
from isitan_lib import *  # noqa: F401,F403

SET = "plate-rolls"
SECTION = "Plate rollers & slip rolls"
# ------------------------------------------------------------------ images
# key -> (source file, alt) ; sources: isitan.com photo (img/…) or catalogue cut-out (cut/…)
IMAGES = {
    # 4R HMS
    "is-4rhms-3100-250": ("img/ISITAN-4RHMS-3100-250.jpg", "İşitan 4R HMS 3100x250 hydraulic 4-roll plate roller, 10.2 ft"),
    "is-4rhms-2050-180": ("img/ISITAN-4RHMS-2050-180.jpg", "İşitan 4R HMS 2050x180 hydraulic 4-roll plate roller with NC control and plate ejector"),
    "is-4rhms-1550-220": ("img/ISITAN-4RHMS-1550-220-1.jpg", "İşitan 4R HMS 1550x220 4-roll plate roller with overhead crane and side supports"),
    "is-4rhms-1270-100": ("img/ISITAN-4RHMS-1270-100-1.jpg", "İşitan 4R HMS 1270x100 4-roll plate roller with NC control, ejector and mechanical overhead crane"),
    "is-4rhms-2050-130": ("img/ISITAN-4RHMS-2050-130-2.jpg", "İşitan 4R HMS 2050x130 4-roll plate roller — full automation with vacuum sheet feeder and ejector"),
    "is-4rhms-650-80": ("img/ISITAN-4RHMS-650-80-1.jpg", "İşitan 4R HMS 650x80 compact hydraulic 4-roll plate roller, 2.1 ft"),
    "is-4rhms-automation-line": ("cut/p05-009.png", "4R HMS — full automation line with sheet feeder, NC control and part ejector"),
    "is-4rhms-ejector": ("cut/p05-007.png", "4R HMS — hydraulic plate ejector system"),
    "is-4rhms-safety-switch": ("cut/p06-027.png", "4R HMS — safety switch on the drop-end"),
    "is-4rhms-pressure": ("cut/p06-028.png", "4R HMS — pressure adjustment on the bottom roll"),
    "is-4rhms-cone": ("cut/p06-029.png", "4R HMS — standard cone-bending device"),
    # corrugated / special
    "is-4rom-1550-220": ("img/ISITAN-4ROM-1550-220-2.jpg", "İşitan 4R OM 1550x220 4-roll corrugated sheet bending machine"),
    "is-4rhom-corrugated": ("img/ISITAN-4RHOM-ONDULIN.jpg", "İşitan 4R HOM corrugated sheet bending machine rolling galvanized sheet"),
    "is-4rhom-1270-220": ("cut/p09-039.png", "İşitan 4R HOM 1270x220 special-production corrugated sheet bending machine"),
    "is-4rhom-2050-250": ("cut/p09-041.png", "İşitan 4R HOM 2050x250 4-roll corrugated sheet bending machine"),
    "is-4rh-10x90": ("cut/p09-043.png", "İşitan 4RH 10x90 NC-controlled special sheet bending machine"),
    "is-4rom-rings": ("cut/p09-048.png", "4R OM 1550x220 with rolled corrugated rings"),
    # MRM-H
    "is-mrmh-3100-250": ("img/ISITAN-MRM-H-3100-250.jpg", "İşitan MRM-H 3100x250 hydraulic 3-roll plate roller, 10 ft"),
    "is-mrmh-2050-180": ("img/ISITAN-MRM-H-2050-180-1.jpg", "İşitan MRM-H 2050x180 hydraulic 3-roll plate roller — motor + planetary reducer drive"),
    "is-mrmh-2550-180": ("img/ISITAN-MRM-H-2550-180-1.jpg", "İşitan MRM-H 2550x180 hydraulic 3-roll plate roller, 8.4 ft"),
    "is-mrmh-1550-150": ("img/ISITAN-MRM-H-1550-150-1.jpg", "İşitan MRM-H 1550x150 hydraulic 3-roll plate roller with digital readouts"),
    "is-mrmh-1270-180": ("img/ISITAN-MRM-H1270-180.jpg", "İşitan MRM-H 1270x180 hydraulic 3-roll plate roller, 4.2 ft"),
    "is-mrmh-1050-100": ("img/ISITAN-MRM-H-1050-100-1.jpg", "İşitan MRM-H 1050x100 hydraulic 3-roll plate roller, 3.4 ft"),
    "is-mrmh-wire-grooves": ("cut/p11-055.png", "MRM-H — optional wire grooves on the roll ends"),
    "is-mrmh-drop-end": ("cut/p11-058.png", "MRM-H — hydraulic drop-end and roll-end detail"),
    # 3R HMD
    "is-3rhmd-1270-90": ("img/ISITAN-ISITAN-3RHMD-1270-90.jpg", "İşitan 3R HMD 1270x90 mechanical-hydraulic 3-roll plate roller"),
    # MRM-S
    "is-mrms-2050-190": ("img/ISITAN-MRM-S-2050-190.jpg", "İşitan MRM-S 2050x190 motorized 3-roll plate roller, 6.7 ft"),
    "is-mrms-1050-150": ("img/ISITAN-MRM-S-1050-150-1.jpg", "İşitan MRM-S 1050x150 motorized 3-roll plate roller, 3.4 ft"),
    "is-mrms-1550-150": ("img/ISITAN-MRM-S-1550-150.jpg", "İşitan MRM-S 1550x150 motorized 3-roll plate roller, 5.1 ft"),
    "is-mrms-2550-190": ("img/ISITAN-MRM-S-2550-190.jpg", "İşitan MRM-S 2550x190 motorized 3-roll plate roller, 8.4 ft"),
    "is-mrms-3050-190": ("img/ISITAN-MRM-S-3050-190.jpg", "İşitan MRM-S 3050x190 motorized 3-roll plate roller, 10 ft"),
    "is-mrms-composite": ("img/ISITAN-OZELMODEL-2.jpg", "İşitan MRM-S special model with segmented plastic-coated top roll for aluminum composite panels"),
    "is-mrms-panel": ("cut/p15-070.png", "MRM-S — optional control panel with digital readout"),
    "is-mrms-section-rolls": ("cut/p15-072.png", "MRM-S — optional extended roll shafts and section bending roll set"),
    "is-mrms-cone": ("cut/p15-074.png", "MRM-S — standard cone-bending device"),
    "is-mrms-drop-end": ("cut/p15-076.png", "MRM-S — manual drop-end with safety switch"),
    "is-mrms-delrin": ("cut/p15-078.png", "MRM-S — segmented plastic (Delrin) top roll for composite panels"),
    # IRM
    "is-irm-1550-140": ("img/ISITAN-IRM-1550-140-1.jpg", "İşitan IRM 1550x140 motorized 3-roll plate roller, 5.1 ft"),
    "is-irm-1050-130": ("img/ISITAN-IRM-1050-130-1.jpg", "İşitan IRM 1050x130 motorized 3-roll plate roller — compact cast-frame model"),
    "is-irm-1270-140": ("img/ISITAN-IRM-1270-140.jpg", "İşitan IRM 1270x140 motorized 3-roll plate roller, 4.2 ft"),
    "is-irm-2050-130": ("img/ISITAN-IRM-2050-130.jpg", "İşitan IRM 2050x130 motorized 3-roll plate roller, 6.7 ft"),
    "is-irm-2550-130": ("img/ISITAN-IRM-2550-130.jpg", "İşitan IRM 2550x140 motorized 3-roll plate roller, 8.4 ft"),
    "is-irm-drop-end": ("cut/p18-095.png", "IRM — standard manual drop-end"),
    # RM / RS
    "is-rm-1270-90": ("img/ISITAN-RM-1270-90.jpg", "İşitan RM 1270x90 motorized 3-roll plate roller with foot-pedal control"),
    "is-rm-1050-90": ("img/ISITAN-RM-1050-90-1.jpg", "İşitan RM 1050x90 motorized 3-roll plate roller, 3.4 ft"),
    "is-rm-1550-90": ("img/ISITAN-RM-1550-90.jpg", "İşitan RM 1550x90 motorized 3-roll plate roller, 5.1 ft"),
    "is-rm-2050-95": ("img/ISITAN-RM-2050-95.jpg", "İşitan RM 2050x95 motorized 3-roll plate roller, 6.7 ft"),
    "is-rm-drop-end": ("cut/p20-105.png", "RM — standard manual drop-end"),
    "is-rm-safety-switch": ("cut/p20-106.png", "RM — standard drop-end safety switch"),
    "is-rs-1270-90": ("img/ISITAN-RS1270-90-1.jpg", "İşitan RS 1270x90 manual 3-roll plate roller — hand-crank operation"),
    "is-rs-1050-90": ("img/ISITAN-RS1050-90.jpg", "İşitan RS 1050x90 manual plate roller, 3.4 ft"),
    "is-rs-1550-90": ("img/ISITAN-RS1550-90-1.jpg", "İşitan RS 1550x90 manual plate roller, 5.1 ft"),
    "is-rs-2050-95": ("img/ISITAN-RS2050-95-1.jpg", "İşitan RS 2050x95 manual plate roller, 6.7 ft"),
    # IR
    "is-ir-1270-75": ("img/ISITAN-IR1270-75.jpg", "İşitan IR 1270x75 motorized slip roll with foot pedal"),
    "is-ir-1050-56": ("img/ISITAN-IR1050-56-1.jpg", "İşitan IR 1050x56 motorized slip roll — reinforced steel frame"),
    "is-ir-1550-75": ("img/ISITAN-IR-1550-75.jpg", "İşitan IR 1550x75 motorized slip roll, 5.1 ft"),
    "is-ir-2050-75": ("img/ISITAN-IR-2050-75-1.jpg", "İşitan IR 2050x75 motorized slip roll, 6.7 ft"),
    "is-ir-drop-end": ("cut/p22-118.png", "IR — standard manual drop-end"),
    "is-ir-geared-lock": ("cut/p22-120.png", "IR — geared lock for quick back-roll adjustment"),
    "is-ir-safety-switch": ("cut/p22-122.png", "IR — optional drop-end safety switch"),
    # R
    "is-r-1050-56": ("img/ISITAN-R-1050-56-1.jpg", "İşitan R 1050x56 manual slip roll on stand — hand-crank operation"),
    "is-r-1270-75": ("img/ISITAN-R-1270-75.jpg", "İşitan R 1270x75 manual slip roll, 4.2 ft"),
    "is-r-1550-68": ("img/ISITAN-R-1550-68-1.jpg", "İşitan R 1550x68 manual slip roll, 5.1 ft"),
    "is-r-2050-75": ("img/ISITAN-R-2050-75.jpg", "İşitan R 2050x75 manual slip roll, 6.7 ft"),
    "is-r-1270-46": ("img/ISITAN-R-1270-46-1.jpg", "İşitan R 1270x46 bench slip roll with geared lock for quick back-roll adjustment"),
    "is-r-610-46": ("cut/p24-132.png", "İşitan R 610x46 bench slip roll without stand, 2 ft"),
    "is-r-pinch-lever": ("cut/p24-131.png", "R series — easy bottom-roll pinching lever"),
    "is-r-wire-grooves": ("cut/p24-134.png", "R series — wire grooves as standard"),
    # RST
    "is-rstm-1270-86": ("img/ISITAN-RST-M-1270-86.jpg", "İşitan RST-M 1270x86 motorized economical plate roller with foot pedal"),
    "is-rst-1270-86": ("img/ISITAN-RST-1270-86-1.jpg", "İşitan RST 1270x86 manual economical plate roller"),
    "is-rst-screws": ("cut/p26-142.png", "RST — manual up/down setting of the bottom and back rolls by screws"),
}

# ------------------------------------------------------------------ families
FAMILIES = [
    dict(id="isitan-4r-hms", group="4-roll", page="hydraulic-4-roll-plate-rollers",
         name="4R HMS hydraulic 4-roll plate rollers",
         short="4R HMS 4-roll",
         models_label="4R HMS 650x80 – 4R HMS 3100x250 · 36 models",
         summary="İşitan's main line of 4-roll plate rolling machines, from a 2.1 ft bench-size roll to 10.2 ft machines that roll "
                 "3/8″ plate. The pinch roll and both side rolls move on a pyramid-style linear path driven by hydraulic cylinders, "
                 "while the top roll is powered by an electric motor through a planetary gearbox — so the sheet is pinched, pre-bent "
                 "at both ends and rolled into a full cylinder without being removed from the machine. Cone bending, hydraulic "
                 "drop-end and three digital readouts are standard; NC control with programmed roll positions, overhead crane and "
                 "side supports turn it into a semi- or fully automatic production line.",
         features=["Pinch and side rolls moved linearly by hydraulic cylinders; top roll driven by motor and planetary gearbox, bottom roll through a cardan joint",
                   "Three digital readouts for easy roll positioning; mobile control panel",
                   "Hydraulic drop-end for easy removal of finished cylinders; hydraulic balancing system",
                   "Induction-hardened forged or rolled SAE 1050 (CK45) steel rolls; welded steel frames",
                   "Cone-bending device and overload protection standard",
                   "Remote technical support via Wi-Fi; built to EC safety directives (CE marked)"],
         optional=["NC control with remote assistance — teach mode, stored programs, 4 axes expandable to 7", "Overhead crane and hydraulic side supports for large diameters",
                   "Vacuum sheet feeder and part ejector for full automation", "Ground and polished rolls; two-speed or infinitely variable speed; hydraulic motor for rotation", VOLT],
         images=["is-4rhms-3100-250", "is-4rhms-2050-180", "is-4rhms-1550-220", "is-4rhms-1270-100", "is-4rhms-2050-130", "is-4rhms-650-80",
                 "is-4rhms-automation-line", "is-4rhms-ejector", "is-4rhms-cone", "is-4rhms-pressure", "is-4rhms-safety-switch"],
         videos=[],
         specs=spec([(7, 0, "4R HMS 650 – 1050", "2.1–3.4 ft · 4 models"), (7, 1, "4R HMS 1270", "4.2 ft · 6 models"), (7, 2, "4R HMS 1550", "5.1 ft · 7 models"),
                     (8, 0, "4R HMS 2050", "6.7 ft · 6 models"), (8, 1, "4R HMS 2550", "8.4 ft · 5 models"), (8, 2, "4R HMS 3100", "10.2 ft · 4 models")],
                    NOTE_ROLLS + " 4R HMS 4100 models are available on request."),
         headline="Working lengths 2.1–10.2 ft (650–3100 mm) · rolls up to 1/2″ (12 mm)"),
    dict(id="isitan-4r-corrugated", group="4-roll", page="hydraulic-4-roll-plate-rollers",
         name="4R OM / 4R HOM / 4RH corrugated sheet and special 4-roll machines",
         short="4R corrugated & special",
         models_label="4R OM · 4R HOM · 4RH 10x90",
         summary="Purpose-built 4-roll machines for corrugated galvanized sheet up to 11 ga — the material of tanks, roofs and silos. "
                 "The rolls carry a corrugation profile that can be custom made to the customer's sheet, with motor + reducer drive "
                 "and motorized (4R OM, 4R HOM) or hydraulic (4RH) linear roll movement. İşitan also builds special plate rolls to "
                 "order for widths, profiles and automation that the standard range does not cover.",
         features=["Rolls machined to the customer's corrugation profile", "Motor + reducer drive; motorized or hydraulic linear roll movement",
                   "4RH 10x90: standard NC control, motor + planetary reducer and hydraulic linear movement", "Built to EC safety directives (CE marked)"],
         optional=[VOLT],
         images=["is-4rom-1550-220", "is-4rhom-corrugated", "is-4rom-rings", "is-4rhom-1270-220", "is-4rhom-2050-250", "is-4rh-10x90"],
         videos=[],
         specs=spec([(9, 0, "4RH 10x90", "3.4 ft special sheet bending machine")], NOTE_SIMPLE + " 4R OM and 4R HOM machines are built to order — ask for the data sheet of your profile."),
         headline="Corrugated sheet to 11 ga (3 mm) · widths to 6.7 ft (2050 mm) · special builds to order"),
    dict(id="isitan-mrm-h", group="3-roll-hydraulic", page="hydraulic-3-roll-plate-rollers",
         name="MRM-H hydraulic asymmetrical 3-roll plate rollers",
         short="MRM-H hydraulic 3-roll",
         models_label="MRM-H 650x80 – MRM-H 3100x250 · 32 models",
         summary="Initial-pinch 3-roll plate rolls with hydraulic movement of the back and bottom rolls and motor-driven rolls through "
                 "planetary gearboxes — the hydraulic version of the MRM-S. The sheet is pinched between the top and bottom roll, "
                 "pre-bent against the back roll, then rolled; the back roll runs on ball bearings for thin-sheet work and a hydraulic "
                 "drop-end releases the finished cylinder. Cone bending and two digital readouts are standard; NC control, overhead "
                 "crane and side supports are available for larger diameters.",
         features=["Hydraulic movement of back and bottom rolls; motor-driven centralized rolls with planetary gearbox drive on two rolls",
                   "Hydraulic drop-end; mobile control panel with 2 digital readouts", "Main motor with brake system for precise positioning",
                   "Cone bending and pre-bending; back roll on ball bearings for thin-sheet work",
                   "Certified SAE 1050 (CK45) forged steel rolls, hardened; welded steel main frames", "Built to EC safety directives (CE marked)"],
         optional=["Overhead crane and hydraulic side supports for large diameters", "Ground and polished rolls; wire grooves on roll ends", "NC control",
                   "Two-speed operation or adjustable stepless speed; hydraulic motor drive", VOLT],
         images=["is-mrmh-3100-250", "is-mrmh-2050-180", "is-mrmh-2550-180", "is-mrmh-1550-150", "is-mrmh-1270-180", "is-mrmh-1050-100", "is-mrmh-drop-end", "is-mrmh-wire-grooves"],
         videos=[],
         specs=spec([(12, 0, "MRM-H 650 – 1050", "2.1–3.4 ft · 4 models"), (12, 1, "MRM-H 1270", "4.2 ft · 6 models"), (12, 2, "MRM-H 1550", "5.1 ft · 7 models"),
                     (13, 0, "MRM-H 2050", "6.7 ft · 6 models"), (13, 1, "MRM-H 2550", "8.4 ft · 5 models"), (13, 2, "MRM-H 3100", "10 ft · 4 models")], NOTE_ROLLS),
         headline="Working lengths 2.1–10 ft (650–3100 mm) · rolls up to 1/2″ (12 mm)"),
    dict(id="isitan-3r-hmd", group="3-roll-hydraulic", page="hydraulic-3-roll-plate-rollers",
         name="3R HMD mechanical-hydraulic 3-roll plate rollers",
         short="3R HMD",
         models_label="3R HMD 1270x90 · 1550x90 · 2050x95",
         summary="A new compact series in which all three rolls are powered by one motor and planetary reducer, with a hydraulic "
                 "piston moving the back roll: joystick positioning with a digital readout makes cone bending and repeat radii easy. "
                 "Cast-iron frames, induction-hardened SAE 1050 rolls and wire grooves as standard — a step up from a slip roll for "
                 "HVAC ducting, signage and light fabrication up to 12 ga.",
         features=["All three rolls driven by a single gearbox and gear system", "Hydraulic back-roll piston with digital readout and joystick control",
                   "Cone bending with easy joystick positioning; manual drop-end", "Certified SAE 1050 induction-hardened steel rolls with wire grooves Ø3/16″, 1/4″, 3/8″",
                   "Cast-iron main frames; mobile control panel with foot pedal; brake motor for precision bending", "Built to EC safety directives (CE marked)"],
         optional=[VOLT],
         images=["is-3rhmd-1270-90"],
         videos=[],
         specs=spec([(27, 0, "3R HMD", "4.2–6.7 ft · 3 models")], NOTE_SIMPLE),
         headline="Working lengths 4.2–6.7 ft (1270–2050 mm) · rolls up to 12 ga (2.5 mm)"),
    dict(id="isitan-mrm-s", group="3-roll-motorized", page="motorized-plate-rollers",
         name="MRM-S mechanical asymmetrical 3-roll plate rollers",
         short="MRM-S motorized 3-roll",
         models_label="MRM-S 1050x130 – MRM-S 3050x220 · 21 models",
         summary="Motorized initial-pinch plate rolls for light to medium-duty work up to 3/8″ plate: a planetary gearbox drives the rolls, "
                 "the back roll moves linearly on a motorized adjustment and a manual drop-end with safety switch releases the finished "
                 "cylinder. Ideal for aluminum forming, HVAC and ventilation ducting, signage panels, machine guards and sheet-metal "
                 "enclosures. A special version carries a top roll of segmented hard-plastic (Delrin) rings for rolling aluminum "
                 "composite panels (Alucobond / ACM) without marking the surface.",
         features=["Planetary gearbox drive on all models; precision rolling with brake motor", "Motorized back-roll adjustment; manual drop-end top roll with safety switch",
                   "Cone-bending device, top-roll support system and central lubrication", "High-tensile rolls in certified SAE 1050 (CK45) steel; fabricated welded-steel main frames",
                   "Mobile pendant control panel", "Built to EC safety directives (CE certified)"],
         optional=["Digital readout (DRO) for the back roll; NC control", "Induction-hardened rolls; variable stepless speed; motorized bottom roll",
                   "Extended roll shafts and profile & section bending roll set", "Plastic-coated segmented top roll for Alucobond / ACM composite panels", VOLT],
         images=["is-mrms-2050-190", "is-mrms-1050-150", "is-mrms-1550-150", "is-mrms-2550-190", "is-mrms-3050-190", "is-mrms-composite", "is-mrms-delrin",
                 "is-mrms-panel", "is-mrms-section-rolls", "is-mrms-cone", "is-mrms-drop-end"],
         videos=[],
         specs=spec([(16, 0, "MRM-S 1050", "3.4 ft · 4 models"), (16, 1, "MRM-S 1550", "5.1 ft · 4 models"), (16, 2, "MRM-S 2050", "6.7 ft · 5 models"),
                     (17, 0, "MRM-S 2550", "8.4 ft · 4 models"), (17, 1, "MRM-S 3050", "10 ft · 4 models")], NOTE_SIMPLE + " Capacity pairs are as published by the manufacturer."),
         headline="Working lengths 3.4–10 ft (1050–3050 mm) · rolls up to 3/8″ (10 mm)"),
    dict(id="isitan-irm", group="3-roll-motorized", page="motorized-plate-rollers",
         name="IRM mechanical asymmetrical 3-roll plate rollers",
         short="IRM motorized 3-roll",
         models_label="IRM 1050x110 – IRM 2550x140 · 10 models",
         summary="Value-priced motorized plate rolls, a favourite of small workshops: top and bottom rolls driven by a single gearbox "
                 "and gear system, spheroidal cast-iron frames, wire grooves at the roll ends and a cone-bending device, with a mobile "
                 "control panel and foot pedal. Designed for light to medium work up to 3/16″ — aluminum forming, HVAC ducting, signage "
                 "panels and sheet-metal enclosures.",
         features=["Top and bottom rolls driven by a single gearbox and gear system", "Certified SAE 1050 steel rolls with high tensile strength; spheroidal cast-iron frames",
                   "Mobile control panel with foot pedal; precision bending with brake motor", "Cone-bending device, manual drop-end, top-roll support with bearing",
                   "Wire grooves at the roll ends; IRM 2550x140 with motorized back roll as standard", "Built to EC safety directives (CE certified)"],
         optional=["Motorized back-roll adjustment with digital readout", "Induction-hardened rolls; adjustable stepless speed", VOLT],
         images=["is-irm-1550-140", "is-irm-1050-130", "is-irm-1270-140", "is-irm-2050-130", "is-irm-2550-130", "is-irm-drop-end"],
         videos=[],
         specs=spec([(19, 0, "IRM 1050 – 1550", "3.4–5.1 ft · 5 models"), (19, 1, "IRM 1550 – 2550", "5.1–8.4 ft · 5 models")], NOTE_SIMPLE),
         headline="Working lengths 3.4–8.4 ft (1050–2550 mm) · rolls up to 3/16″ (5 mm)"),
    dict(id="isitan-rm", group="3-roll-motorized", page="motorized-plate-rollers",
         name="RM motorized 3-roll asymmetrical plate rollers",
         short="RM motorized",
         models_label="RM 1050x90 · 1270x90 · 1550x90 · 2050x95",
         summary="Motorized 3-roll plate rolls on a reinforced steel frame with a single gearbox and chain/gear drive, foot-pedal control "
                 "and a brake motor for precise stops. Rolls up to 11 ga, with wire grooves and a cone-bending device as standard — "
                 "the motorized sister of the RS manual roll for ducting, cylinders and light sheet-metal work.",
         features=["Top and bottom rolls driven by a single gearbox and chain/gear system", "Certified SAE 1050 steel rolls; reinforced steel main frame",
                   "Mobile control panel with foot pedal; precision bending with brake motor", "Cone-bending device, manual drop-end and wire grooves at the roll ends",
                   "Built to EC safety directives (CE)"],
         optional=["Motorized back-roll adjustment with digital readout", "Induction-hardened or coated rolls; variable speed", VOLT],
         images=["is-rm-1270-90", "is-rm-1050-90", "is-rm-1550-90", "is-rm-2050-95", "is-rm-drop-end", "is-rm-safety-switch"],
         videos=[],
         specs=spec([(21, 0, "RM — motorized", "3.4–6.7 ft · 4 models")], NOTE_SIMPLE),
         headline="Working lengths 3.4–6.7 ft (1050–2050 mm) · rolls up to 11 ga (3 mm)"),
    dict(id="isitan-ir", group="slip-rolls", page="slip-rolls",
         name="IR motorized 3-roll slip rolls",
         short="IR motorized slip rolls",
         models_label="IR 1050x46 – IR 2050x75 · 10 models",
         summary="Motorized slip rolls with foot-pedal control for sheet up to 14 ga: top and bottom rolls driven by a single gearbox "
                 "and chain/gear system, a reinforced steel frame, manual drop-end and wire grooves at the roll ends. A geared lock "
                 "gives quick back-roll adjustment and a brake motor stops the rolls exactly where the operator wants them — the "
                 "everyday roll of HVAC and sheet-metal shops.",
         features=["Top and bottom rolls driven by a single gearbox and chain/gear system", "Certified SAE 1050 steel rolls with high tensile strength; steel frame",
                   "Mobile control panel with foot pedal; precision bending with brake motor", "Manual drop-end; geared lock for quick back-roll adjustment",
                   "Wire grooves at the roll ends", "Built to EC safety directives (CE certified)"],
         optional=["Induction-hardened rolls", "Drop-end safety switch", VOLT],
         images=["is-ir-1270-75", "is-ir-1050-56", "is-ir-1550-75", "is-ir-2050-75", "is-ir-geared-lock", "is-ir-drop-end", "is-ir-safety-switch"],
         videos=[],
         specs=spec([(23, 0, "IR 1050 – 1270", "3.4–4.2 ft · 5 models"), (23, 1, "IR 1270 – 2050", "4.2–6.7 ft · 5 models")], NOTE_SIMPLE),
         headline="Working lengths 3.4–6.7 ft (1050–2050 mm) · rolls up to 14 ga (2 mm)"),
    dict(id="isitan-r", group="slip-rolls", page="slip-rolls",
         name="R manual 3-roll slip rolls — floor-standing and bench models",
         short="R manual slip rolls",
         models_label="R 610x46 – R 2050x75 · 13 models",
         summary="Hand-crank slip rolls from a 2 ft bench roll to a 6.7 ft floor-standing machine: certified SAE 1050 steel rolls, "
                 "a steel frame on the 68 and 75 mm roll models, manual drop-end and wire grooves at the roll ends. An easy "
                 "bottom-roll pinching lever sets the sheet thickness; bench models are supplied without a stand for mounting on a "
                 "workbench.",
         features=["Certified SAE 1050 steel rolls with high tensile strength", "Steel frame (68 and 75 mm roll models); bench models without stand",
                   "Manual drop-end; easy bottom-roll pinching lever", "Wire grooves at the roll ends as standard",
                   "R 1270x46 bench roll with geared lock for quick back-roll adjustment"],
         optional=["Induction-hardened rolls"],
         images=["is-r-1050-56", "is-r-1270-75", "is-r-1550-68", "is-r-2050-75", "is-r-1270-46", "is-r-610-46", "is-r-pinch-lever", "is-r-wire-grooves"],
         videos=[],
         specs=spec([(25, 0, "R 1050 – 1270 · floor-standing", "3.4–4.2 ft · 5 models"), (25, 1, "R 1270 – 2050 · floor-standing", "4.2–6.7 ft · 5 models"),
                     (25, 2, "R bench models · without stand", "2–4.2 ft · 3 models")], NOTE_SIMPLE + " Manual machines carry the NovoTech warranty and support; electrical items do not apply."),
         headline="Working lengths 2–6.7 ft (610–2050 mm) · rolls up to 14 ga (2 mm)"),
    dict(id="isitan-rs", group="slip-rolls", page="slip-rolls",
         name="RS manual 3-roll asymmetrical plate rollers",
         short="RS manual",
         models_label="RS 1050x90 · 1270x90 · 1550x90 · 2050x95",
         summary="The manual version of the RM: the same reinforced steel frame, certified SAE 1050 rolls, cone-bending device and "
                 "wire grooves, turned by a hand crank instead of a motor. Rolls up to 11 ga on the shortest model — a sturdy, "
                 "no-electrics roll for shops that bend a few cylinders a day.",
         features=["Hand-crank operation; reinforced steel main frame", "Certified SAE 1050 steel rolls with high tensile strength",
                   "Cone-bending device, manual drop-end and wire grooves at the roll ends", "Built to EC safety directives (CE)"],
         optional=["Induction-hardened or coated rolls", "Fully enclosed sheet covers"],
         images=["is-rs-1270-90", "is-rs-1050-90", "is-rs-1550-90", "is-rs-2050-95"],
         videos=[],
         specs=spec([(21, 1, "RS — manual", "3.4–6.7 ft · 4 models")], NOTE_SIMPLE + " Manual machines carry the NovoTech warranty and support; electrical items do not apply."),
         headline="Working lengths 3.4–6.7 ft (1050–2050 mm) · rolls up to 11 ga (3 mm)"),
    dict(id="isitan-rst", group="slip-rolls", page="slip-rolls",
         name="RST / RST-M economical manual and motorized plate rollers",
         short="RST economical",
         models_label="RST 1270x86 · RST-M 1270x86 · RST 1550x86 · RST-M 1550x86",
         summary="Reinforced, value-priced plate rolls for light work up to 12 ga — ventilation ducting, signage panels, machine guards "
                 "and sheet-metal parts. Cast main frames, a manual drop-end top roll and back and bottom rolls adjusted up and down by "
                 "screws on both sides; the RST-M adds a geared motor with electrical box and foot pedal.",
         features=["Cast main frames; certified SAE 1050 steel rolls", "Manual drop-end top roll", "Back and bottom rolls adjusted up/down by screws on both sides",
                   "Motor- (RST-M) or hand-driven centre rolls; foot-pedal control on the RST-M"],
         optional=["Hardened rolls", VOLT],
         images=["is-rstm-1270-86", "is-rst-1270-86", "is-rst-screws"],
         videos=[],
         specs=spec([(26, 0, "RST · RST-M", "4.1–5.1 ft · 4 models")], NOTE_SIMPLE),
         headline="Working lengths 4.1–5.1 ft (1270–1550 mm) · rolls up to 12 ga (2.5 mm)"),
]

# ------------------------------------------------------------------ pages
HUB = "plate-rollers"
GUIDE = {"href": "plate-rollers.html#buying-guide", "label": "Plate roller buying guide: 3-roll vs 4-roll, capacities, cones and controls"}
VOLT_FAQ = {"q": "What voltage do İşitan plate rollers run on?",
            "a": "Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208 V, 240 V and 480 V 3-phase are available on request, and 240 V single-phase on models with a small enough motor. Manual slip rolls have no electrics."}

PAGES = {
    "hydraulic-4-roll-plate-rollers": dict(
        title="Hydraulic 4-Roll Plate Rollers — 4 Roll Plate Rolling Machines in Canada | NovoTech",
        meta="İşitan 4-roll plate rollers for sale in Canada: hydraulic 4 roll plate rolling machines from 2.1 ft to 10.2 ft, up to 1/2″ plate, NC control and full automation, corrugated sheet rolls. Specs in inches, CSA panels, parts in Mississauga, ON.",
        h1="Hydraulic 4-roll plate rollers",
        intro="Four-roll plate rolling machines pinch the sheet between the top and bottom roll and bend it with two side rolls, so the plate is pre-bent at both ends and rolled into a full cylinder in one pass without flipping it. İşitan's 4R HMS hydraulic plate rollers run from a 2.1 ft bench-size roll to 10.2 ft machines for 3/8″ plate, with NC control, overhead crane and sheet feeder for production work; the 4R OM and 4R HOM roll corrugated galvanized sheet for tanks, roofs and silos. Every 4 roll plate roller is sold with a CSA-approved panel and supported from Mississauga, ON.",
        points=["36 models from 2.1 ft to 10.2 ft (650–3100 mm)", "Rolls up to 1/2″ (12 mm) plate; pre-bends both ends in one pass", "NC control, overhead crane, sheet feeder and ejector for automation"],
        hero="is-4rhms-3100-250", minis=["is-4rhms-2050-180", "is-4rom-1550-220"],
        groups=[("4-roll", "Hydraulic 4-roll plate rollers", "The 4R HMS range with hydraulic roll positioning and motor-driven rolls, plus the corrugated-sheet and special-build 4-roll machines.")],
        faq=[{"q": "3-roll or 4-roll plate roller — which one do I need?", "a": "A 4-roll machine holds the sheet pinched between the top and bottom roll while the side rolls pre-bend and roll it, so both ends are pre-bent without turning the plate around and the operator never loses alignment — the better choice for production, thin or polished material and cones. A 3-roll initial-pinch machine does the same job with one more handling step at a lower price, which is why most job shops start with an MRM-H or MRM-S."},
             {"q": "What does \"capacity at 1.5× / 5× top roll Ø\" mean?", "a": "Plate rolls are rated for a given diameter: the thicker the plate, the larger the minimum cylinder it can form. The manufacturer states two figures — the thickness the machine rolls into a tight cylinder of 1.5 times the top roll diameter, and the thickness it rolls at 5 times the top roll diameter. Tell us your plate thickness and the smallest diameter you make and we will size the machine from the capacity chart."},
             {"q": "Can a 4R HMS roll cones?", "a": "Yes — a cone-bending device is standard on every 4R HMS, and the NC control stores the roll positions for repeat cones. Hydraulic side supports and the overhead crane keep large cones and thin material in shape while rolling."},
             {"q": "How automatic can a plate roller be?", "a": "With the NC control the operator programs the roll positions once; the machine then bends to the stored program. Adding the vacuum sheet feeder, the hydraulic overhead crane and the part ejector turns the 4R HMS into a full automation line where the operator only loads blanks and removes finished cylinders at the welding station."},
             VOLT_FAQ]),
    "hydraulic-3-roll-plate-rollers": dict(
        title="Hydraulic 3-Roll Plate Rollers — Initial-Pinch Plate Rolling Machines in Canada | NovoTech",
        meta="İşitan MRM-H hydraulic 3-roll plate rollers in Canada: initial-pinch plate rolling machines from 2.1 ft to 10 ft, up to 1/2″ plate, hydraulic drop-end and digital readouts; 3R HMD joystick rolls. Specs in inches, CSA panels, parts in Mississauga, ON.",
        h1="Hydraulic 3-roll plate rollers",
        intro="Initial-pinch 3-roll plate rolling machines with hydraulic positioning of the back and bottom rolls and motor-driven rolls: the operator pinches the sheet, pre-bends the leading edge against the back roll, rolls the cylinder and opens the hydraulic drop-end to take it off. İşitan's MRM-H covers 2.1 ft to 10 ft and plate to 1/2″ with two digital readouts and cone bending as standard; the compact 3R HMD puts hydraulic back-roll positioning with a joystick on a cast-iron frame for ducting and light fabrication. Hydraulic plate rollers with CSA-approved panels, sold and supported from Mississauga, ON.",
        points=["MRM-H: 32 models from 2.1 ft to 10 ft (650–3100 mm), up to 1/2″ (12 mm)", "Hydraulic back and bottom rolls, hydraulic drop-end, 2 digital readouts", "3R HMD: all-roll drive with hydraulic joystick back roll from 4.2 ft"],
        hero="is-mrmh-3100-250", minis=["is-mrmh-2050-180", "is-3rhmd-1270-90"],
        groups=[("3-roll-hydraulic", "Hydraulic 3-roll plate rollers", "MRM-H initial-pinch plate rolls and the compact 3R HMD with hydraulic back-roll positioning.")],
        faq=[{"q": "How does an initial-pinch 3-roll plate roller work?", "a": "The sheet is clamped (pinched) between the top and bottom roll, the back roll is raised to pre-bend the leading edge, the sheet is fed through and rolled to the radius set by the back roll, and the drop-end is opened to remove the cylinder. The trailing edge is pre-bent by turning the sheet around — the one extra step compared with a 4-roll machine."},
             {"q": "MRM-H or MRM-S — hydraulic or mechanical?", "a": "Both are initial-pinch rolls with the same roll sizes. The MRM-H moves its back and bottom rolls hydraulically and opens the drop-end hydraulically, which is faster, takes thicker plate at the same roll diameter and suits daily production; the MRM-S moves the back roll with a motor and opens the drop-end by hand at a lower price."},
             {"q": "What thickness can the MRM-H roll?", "a": "From 20 ga sheet on the 1270x80 up to 1/2″ plate on the 250 mm roll models — see the capacity tables, which give the thickness at 1.5× and at 5× the top roll diameter. Capacities are for mild steel; stainless and high-strength plate need the next roll size up."},
             VOLT_FAQ]),
    "motorized-plate-rollers": dict(
        title="Motorized 3-Roll Plate Rollers — Mechanical Plate Rolling Machines in Canada | NovoTech",
        meta="İşitan motorized plate rollers in Canada: MRM-S, IRM and RM mechanical 3-roll plate rolling machines from 3.4 ft to 10 ft, up to 3/8″ plate, cone bending, composite-panel rolls. Specs in inches, CSA panels, parts in Mississauga, ON.",
        h1="Motorized 3-roll plate rollers",
        intro="Mechanical plate rolling machines for aluminum, HVAC ducting, signage panels, machine guards and sheet-metal enclosures: a planetary gearbox or gear train drives the rolls, the back roll is adjusted by motor or hand wheel and a manual drop-end releases the cylinder. The MRM-S rolls up to 3/8″ plate on working lengths to 10 ft and has a composite-panel version with a Delrin-coated top roll; the IRM and RM are the value-priced motorized plate rollers small workshops ask for. All with CSA-approved panels, parts and support from Mississauga, ON.",
        points=["MRM-S: 21 models to 10 ft (3050 mm) and 3/8″ (10 mm) plate", "IRM and RM: value-priced motorized rolls from 3.4 ft, up to 3/16″", "Cone bending, wire grooves and brake motor standard"],
        hero="is-mrms-2050-190", minis=["is-irm-1550-140", "is-rm-1270-90"],
        groups=[("3-roll-motorized", "Motorized 3-roll plate rollers", "MRM-S, IRM and RM: mechanical initial-pinch plate rolls from 3.4 ft to 10 ft.")],
        faq=[{"q": "MRM-S, IRM or RM — what is the difference?", "a": "Roll diameter and construction. The MRM-S has 130–220 mm rolls on a welded frame with planetary drive and motorized back roll and takes plate to 3/8″; the IRM has 110–140 mm rolls on cast-iron frames for sheet to 3/16″; the RM has 90–95 mm rolls on a reinforced steel frame for sheet to 11 ga. Choose by the thickest sheet and the smallest diameter you roll."},
             {"q": "Can I roll aluminum composite panels (Alucobond) without marking them?", "a": "Yes — the MRM-S composite-panel version has a top roll covered in segmented hard-plastic (Delrin) rings so the painted panel is not marked. It is used for curved signage, architectural cladding and outdoor design work."},
             {"q": "Do motorized plate rollers bend cones?", "a": "Every MRM-S, IRM and RM has a cone-bending device: one end of the top roll is lowered so the sheet travels faster on the wide end. The optional digital readout on the back roll makes repeat cones easier."},
             VOLT_FAQ]),
    "slip-rolls": dict(
        title="Slip Rolls — Manual & Motorized Sheet Metal Slip Rollers in Canada | NovoTech",
        meta="İşitan slip rolls in Canada: manual hand-crank slip rollers from 2 ft bench models to 6.7 ft, motorized IR slip rolls with foot pedal, RS and RST economical plate rolls. Sheet to 14 ga, wire grooves standard, parts in Mississauga, ON.",
        h1="Slip rolls — manual and motorized sheet metal rollers",
        intro="Slip rollers for HVAC, sign, ducting and general sheet-metal shops: three rolls, a drop-end to slip the finished cylinder off and wire grooves at the roll ends for wired edges. İşitan's R series is the hand-crank slip roll — 2 ft bench models to 6.7 ft floor-standing machines up to 14 ga — the IR adds a motor, foot pedal and brake for daily use, and the RS and RST are the reinforced economical rolls. Sold with CSA-approved panels on motorized models and supported from Mississauga, ON.",
        points=["Manual R series: bench and floor models from 2 ft to 6.7 ft", "Motorized IR series with foot pedal, up to 14 ga (2 mm)", "Wire grooves, manual drop-end and SAE 1050 rolls on every model"],
        hero="is-ir-1270-75", minis=["is-r-1050-56", "is-rst-1270-86"],
        groups=[("slip-rolls", "Slip rolls and economical plate rollers", "Motorized IR, manual R and RS, and the economical RST — the light-gauge rolls of the sheet-metal shop.")],
        faq=[{"q": "What is the difference between a slip roll and a plate roller?", "a": "They work the same way — three rolls that pinch and bend the sheet — but a slip roll is built for thin sheet (up to about 14 ga) and the top roll \"slips\" out of its bearing so the finished cylinder can be removed; its wire grooves also form wired edges. Plate rollers have larger rolls, heavier frames and powered or hydraulic roll positioning for plate from 11 ga up to 1/2″ and beyond."},
             {"q": "Manual or motorized slip roll?", "a": "A hand-crank R or RS roll is enough for occasional cylinders and short lengths; once you roll ducting daily or work with 5 ft and longer sheets, the IR motorized roll with foot pedal and brake motor pays for itself in time and consistent diameters."},
             {"q": "What do the wire grooves do?", "a": "The grooves at the end of the rolls (3/16″, 1/4″ and 3/8″ on most models) close a hemmed edge around a wire to make a stiff, safe wired edge on ducts, buckets and tanks."},
             VOLT_FAQ]),
}
HUB_PAGE = dict(
    title="Plate Rollers & Slip Rolls for Sale in Canada — Plate Rolling Machines | NovoTech",
    meta="Plate rollers and slip rolls in Canada: İşitan hydraulic 4-roll and 3-roll plate rolling machines, motorized plate rollers and manual slip rollers from 2 ft to 10 ft, sheet to 1/2″ plate. Specs in inches, CSA panels, parts and service in Mississauga, ON.",
    h1="Plate rollers and slip rolls",
    intro="Every İşitan plate roller and slip roll NovoTech sells in Canada: hydraulic 4-roll plate rolling machines with NC control for production, hydraulic and motorized 3-roll plate rollers for the fabrication shop, and manual and motorized slip rolls for HVAC and sheet-metal work — from a 2 ft bench slip roll to 10.2 ft machines that roll 1/2″ plate. Built in Turkey by İşitan since 1959, supplied with CSA-approved panels and supported from NovoTech's warehouse in Mississauga, ON. Looking for a plate roller machine, sheet metal roller, slip roller or plate bending rolls? These are the ones we stock and service.",
    points=["<a href=\"hydraulic-4-roll-plate-rollers\">Hydraulic 4-roll plate rollers</a> — 2.1 to 10.2 ft, up to 1/2″ plate, NC and automation",
            "<a href=\"hydraulic-3-roll-plate-rollers\">Hydraulic</a> and <a href=\"motorized-plate-rollers\">motorized 3-roll plate rollers</a> — initial pinch, cone bending",
            "<a href=\"slip-rolls\">Slip rolls</a> — manual and motorized, 2 to 6.7 ft, wire grooves standard"],
    hero="is-4rhms-3100-250", minis=["is-mrms-2050-190", "is-r-1050-56"],
    faq=[{"q": "Plate roller, plate roll, slip roll, bending rolls — are these the same machine?", "a": "Largely yes. \"Plate roller\", \"plate rolling machine\" and \"plate bending rolls\" all describe the three- or four-roll machine that rolls flat plate into cylinders and cones; \"slip roll\" or \"sheet metal roller\" is the light-gauge version for sheet up to about 14 ga, whose top roll slips open to remove the part. We use the manufacturer's terms on each page so you can match them to the capacity tables."},
         {"q": "How do I choose the size of a plate roller?", "a": "Three numbers: the longest cylinder you roll (working length), the thickest plate you roll at that length, and the smallest diameter you need. Plate rolls are rated at 1.5× and 5× the top roll diameter — a machine that rolls 1/4″ plate into a 20″ cylinder will not roll 1/4″ into a 10″ cylinder. Send us those three numbers and we will point to the models on the capacity tables."},
         {"q": "Which plate rollers does NovoTech keep in stock?", "a": "We stock the popular MRM-S motorized rolls and the IR and R slip rolls in Mississauga, ON, and bring 4R HMS and MRM-H hydraulic machines in to order with their options. In-stock machines carry the 7-day money-back guarantee."},
         {"q": "Do you install plate rollers and train operators?", "a": "Yes — our technicians commission the machine anywhere in Canada, level it, check the roll parallelism and train your operators on pre-bending, cones and the NC control where fitted."},
         VOLT_FAQ],
    range_lead="Working length, rolling capacity, top roll diameter, motor and weight for every model. Each row links to the full specification table of its series.",
    range_cols=["Working length", "Rolling capacity", "Top roll Ø", "Motor", "Weight"],
    range_caption="İşitan plate rollers and slip rolls supplied by NovoTech — capacities for mild steel",
    range_note="Rolling capacity is for mild steel (34,100 psi yield); where two values are given they apply at 1.5× / 5× the top roll diameter. Manual machines have no motor.",
)
SUBPAGE_META = {
    "hydraulic-4-roll-plate-rollers": ("Hydraulic 4-roll plate rollers", "is-4rhms-2050-180", "4R HMS from 2.1 ft to 10.2 ft with NC control and automation, plus corrugated-sheet and special 4-roll machines.", "4-roll plate rollers"),
    "hydraulic-3-roll-plate-rollers": ("Hydraulic 3-roll plate rollers", "is-mrmh-2050-180", "MRM-H initial-pinch plate rolls to 10 ft and 1/2″ plate, and the compact 3R HMD with joystick back-roll control.", "Hydraulic 3-roll"),
    "motorized-plate-rollers": ("Motorized 3-roll plate rollers", "is-mrms-2050-190", "MRM-S, IRM and RM mechanical plate rolls from 3.4 ft to 10 ft — the shop's everyday rolls, with a composite-panel version.", "Motorized 3-roll"),
    "slip-rolls": ("Slip rolls", "is-ir-1270-75", "Manual R and RS, motorized IR and economical RST slip rolls from 2 ft bench models to 6.7 ft.", "Slip rolls"),
}
ORDER = ["hydraulic-4-roll-plate-rollers", "hydraulic-3-roll-plate-rollers", "motorized-plate-rollers", "slip-rolls"]




def build():
    write_families(SET, FAMILIES)
    sib = [(s, SUBPAGE_META[s][3], SUBPAGE_META[s][0]) for s in ORDER]
    hub = {"slug": HUB, "label": "All plate rollers & slip rolls", "image": "is-4rhms-3100-250", "blurb": "Every İşitan plate roller and slip roll NovoTech supplies, with the capacity table for the whole range."}
    for slug in ORDER:
        write_category(slug, PAGES[slug], FAMILIES, SET, SECTION, hub=hub, siblings=sib, guide=GUIDE)
    write_hub(HUB, {**HUB_PAGE, "artifact_title": "Plate Rollers & Slip Rolls", "faq_title": "Questions we get asked about plate rollers", "nav_label": "All plate rollers & slip rolls", "related_blurb": hub["blurb"]},
              FAMILIES, SET, SECTION, [(s, SUBPAGE_META[s][0], SUBPAGE_META[s][1], SUBPAGE_META[s][2], SUBPAGE_META[s][3]) for s in ORDER],
              extra={"article": "plate-roller-guide.html", "article_id": "buying-guide", "article_title": "Plate roller buying guide",
                     "article_intro": "What we explain to customers before they buy a plate roller: 3-roll and 4-roll machines, initial-pinch and double-pinch, how capacity is rated, cone bending, crowning, controls and automation. Written by NovoTech's technicians from years of installing plate rolls in Canada."})
    return IMAGES
