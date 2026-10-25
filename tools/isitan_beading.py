"""ISITAN section: bead rollers / beading machines (catalogue pages 28–31) — one category page."""
from isitan_lib import *  # noqa: F401,F403

SET = "beading"
SECTION = "Bead rollers"
SLUG = "bead-rollers"

IMAGES = {
    "is-hibks-4": ("img/ISITAN-HIBKS-4.jpg", "ISITAN HIBKS 4.0 hydraulic bead roller for sheet up to 8 ga"),
    "is-ibks-4": ("img/ISITAN-IBKS-4.jpg", "ISITAN IBKS 4.0 motorized bead roller with manual top-roll setting"),
    "is-hibks-25": ("img/ISITAN-HIBKS-25.jpg", "ISITAN HIBKS 2.5 hydraulic bead roller for sheet up to 12 ga"),
    "is-ibks-25": ("img/ISITAN-IBKS-25.jpg", "ISITAN IBKS 2.5 motorized bead roller"),
    "is-hibks-rolls-4": ("cut/p28-155.png", "HIBKS / IBKS 4.0 — standard roll sets S1–S4 and extra roll sets E1–E8"),
    "is-hibks-rolls-25": ("cut/p29-162.png", "HIBKS / IBKS 2.5 — standard roll sets S1–S4 and extra roll sets E1–E8"),
    "is-ibks-18": ("img/ISITAN-IBKS-18.jpg", "ISITAN IBKS 1.8 motorized bead roller — 3 sets of standard rolls"),
    "is-ikm-12": ("img/ISITAN-IKM-12.jpg", "ISITAN IKM 1.2 motorized bead roller with 8 sets of standard rolls"),
    "is-ikmp-12": ("img/ISITAN-IKMP-12.jpg", "ISITAN IKMP 1.2 motorized bead roller on floor stand"),
    "is-ikmp-12p": ("img/ISITAN-IKMP-12P.jpg", "ISITAN IKMP 1.2 P bead roller with pneumatic top shaft"),
    "is-ikm-rolls-extra": ("cut/p30-173.png", "Extra roll sets for IKMP and IKM bead rollers"),
    "is-ikm-rolls-std": ("cut/p30-174.png", "Standard roll sets for IKMP and IKM bead rollers"),
}

NOTE = "Beading capacity is for mild steel; thin sheet is given in gauge with the manufacturer's nominal metric value in brackets. Dimensions are overall L × W × H."
GK = ["shaft_length", "beading_capacity", "roll_diameter", "throat_depth", "motor"]


def t_hibks():
    t1 = manual_table("HIBKS 4.0 · IBKS 4.0", "sheet up to 8 ga · hydraulic / motorized", ["HIBKS 4.0 · hydraulic", "IBKS 4.0 · motorized"], [
        ("Shaft length", ["11.8″ (300 mm)", "11.8″ (300 mm)"]),
        ("Beading capacity", "mild steel", ["8 ga (4 mm)", "8 ga (4 mm)"]),
        ("Roll Ø", ["4.96″ (126 mm)", "4.96″ (126 mm)"]),
        ("Throat depth", ["7.9″ (200 mm)", "7.9″ (200 mm)"]),
        ("Spindle speed", ["10 rpm", "10 rpm"]),
        ("Motor power", ["3 + 1 HP (2.2 + 0.75 kW)", "3 HP (2.2 kW)"]),
        ("Hydraulic oil tank", ["6 L", "—"]),
        ("Dimensions L × W × H", ["68 × 23 × 50″ (1730 × 580 × 1270 mm)", "58 × 22 × 47″ (1470 × 560 × 1190 mm)"]),
        ("Weight", ["1,213 lb (550 kg)", "1,014 lb (460 kg)"]),
    ], key_labels=("Beading capacity", "Shaft length"))
    t2 = manual_table("HIBKS 2.5 · IBKS 2.5", "sheet up to 12 ga · hydraulic / motorized", ["HIBKS 2.5 · hydraulic", "IBKS 2.5 · motorized"], [
        ("Shaft length", ["9.8″ (250 mm)", "9.8″ (250 mm)"]),
        ("Beading capacity", "mild steel", ["12 ga (2.5 mm)", "12 ga (2.5 mm)"]),
        ("Roll Ø", ["3.78″ (96 mm)", "3.78″ (96 mm)"]),
        ("Throat depth", ["6.3″ (160 mm)", "6.3″ (160 mm)"]),
        ("Spindle speed", ["13 rpm", "13 rpm"]),
        ("Motor power", ["2 + 0.75 HP (1.5 + 0.55 kW)", "2 HP (1.5 kW)"]),
        ("Hydraulic oil tank", ["6 L", "—"]),
        ("Dimensions L × W × H", ["68 × 23 × 50″ (1730 × 580 × 1270 mm)", "58 × 22 × 47″ (1470 × 560 × 1190 mm)"]),
        ("Weight", ["838 lb (380 kg)", "705 lb (320 kg)"]),
    ], key_labels=("Beading capacity", "Shaft length"))
    glance = {"HIBKS 4.0 · hydraulic": ["11.8″ (300 mm)", "8 ga (4 mm)", "4.96″ (126 mm)", "7.9″ (200 mm)", "3 + 1 HP"],
              "IBKS 4.0 · motorized": ["11.8″ (300 mm)", "8 ga (4 mm)", "4.96″ (126 mm)", "7.9″ (200 mm)", "3 HP"],
              "HIBKS 2.5 · hydraulic": ["9.8″ (250 mm)", "12 ga (2.5 mm)", "3.78″ (96 mm)", "6.3″ (160 mm)", "2 + 0.75 HP"],
              "IBKS 2.5 · motorized": ["9.8″ (250 mm)", "12 ga (2.5 mm)", "3.78″ (96 mm)", "6.3″ (160 mm)", "2 HP"]}
    caps = {"HIBKS 4.0": "beads up to 8 ga (4 mm) · 11.8″ shafts · hydraulic top roll", "IBKS 4.0": "beads up to 8 ga (4 mm) · 11.8″ shafts · motorized",
            "HIBKS 2.5": "beads up to 12 ga (2.5 mm) · 9.8″ shafts · hydraulic top roll", "IBKS 2.5": "beads up to 12 ga (2.5 mm) · 9.8″ shafts · motorized"}
    return manual_spec([t1, t2], GK, glance, caps, NOTE)


def t_motorized():
    t1 = manual_table("IBKS 1.8 · IKM 1.2", "motorized bead rollers", ["IBKS 1.8", "IKM 1.2"], [
        ("Shaft length", ["4.7″ (120 mm)", "5.5″ (140 mm)"]),
        ("Beading capacity", "mild steel", ["14 ga (1.8 mm)", "18 ga (1.2 mm)"]),
        ("Roll Ø", ["3.23″ (82 mm)", "2.44″ (62 mm)"]),
        ("Throat depth", ["11.0″ (280 mm)", "3.9″ (100 mm)"]),
        ("Spindle speed", ["48 rpm", "30 / 60 / 90 / 120 rpm"]),
        ("Motor power", ["2 HP (1.5 kW)", "1 HP (0.75 kW)"]),
        ("Dimensions L × W × H", ["33 × 16 × 48″ (840 × 410 × 1220 mm)", "35 × 18 × 53″ (890 × 460 × 1350 mm)"]),
        ("Weight", ["309 lb (140 kg)", "298 lb (135 kg)"]),
    ], key_labels=("Beading capacity", "Shaft length"))
    t2 = manual_table("IKMP 1.2 · IKMP 1.2 P", "motorized · pneumatic top shaft", ["IKMP 1.2", "IKMP 1.2 P"], [
        ("Shaft length", ["5.5″ (140 mm)", "5.5″ (140 mm)"]),
        ("Beading capacity", "mild steel", ["18 ga (1.2 mm)", "18 ga (1.2 mm)"]),
        ("Roll Ø", ["2.44″ (62 mm)", "2.44″ (62 mm)"]),
        ("Throat depth", ["3.9″ (100 mm)", "3.9″ (100 mm)"]),
        ("Spindle speed", ["32 rpm", "32 rpm"]),
        ("Motor power", ["1 HP (0.75 kW)", "1 HP (0.75 kW)"]),
        ("Dimensions L × W × H", ["39 × 18 × 53″ (990 × 460 × 1350 mm)", "35 × 18 × 65″ (890 × 460 × 1650 mm)"]),
        ("Weight", ["287 lb (130 kg)", "331 lb (150 kg)"]),
    ], key_labels=("Beading capacity", "Shaft length"))
    glance = {"IBKS 1.8": ["4.7″ (120 mm)", "14 ga (1.8 mm)", "3.23″ (82 mm)", "11.0″ (280 mm)", "2 HP"],
              "IKM 1.2": ["5.5″ (140 mm)", "18 ga (1.2 mm)", "2.44″ (62 mm)", "3.9″ (100 mm)", "1 HP"],
              "IKMP 1.2": ["5.5″ (140 mm)", "18 ga (1.2 mm)", "2.44″ (62 mm)", "3.9″ (100 mm)", "1 HP"],
              "IKMP 1.2 P": ["5.5″ (140 mm)", "18 ga (1.2 mm)", "2.44″ (62 mm)", "3.9″ (100 mm)", "1 HP"]}
    caps = {"IBKS 1.8": "beads up to 14 ga (1.8 mm) · 11″ throat · motorized", "IKM 1.2": "beads up to 18 ga (1.2 mm) · 4 speeds · 8 roll sets",
            "IKMP 1.2 P": "beads up to 18 ga (1.2 mm) · pneumatic top shaft", "IKMP 1.2": "beads up to 18 ga (1.2 mm) · motorized on floor stand"}
    return manual_spec([t1, t2], GK, glance, caps, NOTE)


FAMILIES = [
    dict(id="isitan-hibks", group="beading", page=SLUG,
         name="HIBKS / IBKS hydraulic and motorized bead rollers",
         short="HIBKS / IBKS heavy-duty",
         models_label="HIBKS 4.0 · IBKS 4.0 · HIBKS 2.5 · IBKS 2.5",
         summary="Heavy-duty beading and trimming machines for sheet up to 8 ga (4.0 models) or 12 ga (2.5 models): a welded steel frame, "
                 "a gearbox motor with brake, foot-pedal control and shafts in tapered roller bearings. The HIBKS moves the top roll "
                 "hydraulically — the bead is formed under constant pressure without the operator cranking — while the IBKS has a "
                 "manual top-roll setting at a lower price. Four sets of standard rolls and the roll spanner key are included; the "
                 "bottom roll and the sheet support adjust forward and backward for ducts, drums, tanks and HVAC fittings.",
         features=["Welded steel construction frame; complete with floor stand", "HIBKS: hydraulic up/down top roll · IBKS: manual top-roll setting",
                   "Forward-backward adjustable bottom roll and sheet support", "Special-steel shafts in tapered roller bearings; low-maintenance ball-bearing design",
                   "Gearbox motor with brake; foot-pedal control", "4 sets of standard rolls (S1–S4) and roll spanner key included; built to EC safety directives (CE)"],
         optional=["Extra roll sets E1–E8; rolls for special jobs made to order", "Digital readout (HIBKS)", VOLT],
         images=["is-hibks-4", "is-ibks-4", "is-hibks-25", "is-ibks-25", "is-hibks-rolls-4", "is-hibks-rolls-25"],
         videos=[], specs=t_hibks(),
         headline="Beads sheet up to 8 ga (4 mm) · shafts 9.8″ and 11.8″ · hydraulic or motorized"),
    dict(id="isitan-ikm", group="beading", page=SLUG,
         name="IBKS 1.8 / IKM / IKMP motorized and pneumatic bead rollers",
         short="IKM / IKMP motorized",
         models_label="IBKS 1.8 · IKM 1.2 · IKMP 1.2 · IKMP 1.2 P",
         summary="Motorized bead rollers for 14–18 ga sheet, each complete with a floor stand and foot-pedal control. The IBKS 1.8 has a "
                 "welded steel-plate frame with an 11″ throat and a gearbox motor with brake; the IKM 1.2 and IKMP 1.2 are cast-iron "
                 "machines with 8 sets of standard rolls — the IKM with four pulley speeds, the IKMP 1.2 P with a pneumatic top shaft "
                 "that closes the rolls at the press of the pedal for repeat work.",
         features=["IBKS 1.8: welded steel-plate frame, 11″ (280 mm) throat, 3 sets of standard rolls, easy to move around the shop",
                   "IKM 1.2: heavy-duty cast-iron frame, 8 sets of standard rolls, tooling cupboard, 4 working speeds (30 / 60 / 90 / 120 rpm)",
                   "IKMP 1.2 / 1.2 P: cast-iron frame, 8 sets of standard rolls, adjustable bottom roll; the P version with pneumatic top shaft",
                   "Forward-backward adjustable sheet support; special-steel roll shafts", "Foot-pedal control; complete with floor stand; built to EC safety directives (CE)"],
         optional=["Extra roll sets; rolls for special jobs made to order", VOLT],
         images=["is-ibks-18", "is-ikm-12", "is-ikmp-12", "is-ikmp-12p", "is-ikm-rolls-std", "is-ikm-rolls-extra"],
         videos=[], specs=t_motorized(),
         headline="Beads sheet up to 14 ga (1.8 mm) · motorized · pneumatic top shaft on the IKMP 1.2 P"),
]

PAGE = dict(
    title="Bead Roller Machines for Sheet Metal & HVAC | NovoTech",
    meta="Hydraulic and motorized bead roller machines for sheet to 8 ga — HIBKS, IBKS, IKM and IKMP with beading, swaging and flanging roll sets. CSA panels, parts in Mississauga, ON.",
    h1="Bead rollers and beading machines",
    intro="Bead rollers — also called beading machines, rotary machines or swagers — form stiffening beads, wired edges, flanges, crimps and seams in sheet metal for HVAC ducts, drums, tanks, buckets and architectural work. ISITAN builds them motorized and hydraulic — from the IKM and IKMP cast-iron bead rollers with foot-pedal control to the HIBKS 4.0, whose hydraulic top roll beads 8 ga steel under constant pressure. Every machine comes with its sets of standard rolls, a CSA-approved panel and support from Mississauga, ON.",
    points=["Hydraulic HIBKS and motorized IBKS for sheet to 8 ga (4 mm)", "Motorized IKM / IKMP with 4 speeds or pneumatic top shaft", "Standard roll sets (4 to 8 per machine) and the roll spanner key included; extra sets made to order"],
    hero="is-hibks-4", minis=["is-ikmp-12p", "is-ibks-18"],
    groups=[("beading", "Bead rollers line-up", "From the IKM motorized bead roller to the hydraulic HIBKS 4.0 — all with standard roll sets included.", "isitan")],
    faq=[{"q": "Bead roller, beading machine, rotary machine or swager — what is the difference?", "a": "They are the same machine under different names: two shaft-mounted rolls that form a profile in sheet metal as it is turned through them. \"Bead roller\" is the common North American term, \"swager\" the older sheet-metal trade word, \"rotary machine\" the HVAC term. The roll sets decide what it does — beading, wiring, crimping, flanging, burring or trimming."},
         {"q": "Which rolls are included?", "a": "Every ISITAN bead roller ships with its standard roll sets — 4 sets (S1–S4) on the HIBKS / IBKS 4.0 and 2.5, 3 on the IBKS 1.8, 8 sets on the IKM 1.2 and IKMP 1.2 — plus the roll spanner key. Extra sets (E1–E8) and rolls for special jobs are made to order; tell us the profile you need."},
         {"q": "Hydraulic or motorized top roll?", "a": "On the IBKS the operator sets the gap between the rolls by hand and the motor turns them. On the HIBKS the top roll is moved hydraulically, so the pressure stays constant through the bead and deep beads in 8 ga steel are formed in one pass with the foot pedal — the choice for production work and heavier sheet."},
         {"q": "What is throat depth?", "a": "The distance from the rolls to the frame: it sets how far from the sheet edge a bead can be formed. The IBKS 1.8 has an 11″ throat for beads deep into a panel; the HIBKS / IBKS 4.0 7.9″."},
         {"q": "What voltage do bead rollers run on?", "a": "Motorized models are supplied for 600 V 3-phase with a CSA-approved panel; 208 V, 240 V and 480 V 3-phase are available on request and 240 V single-phase on the 1–2 HP models."}],
)


def build():
    write_families(SET, FAMILIES)
    write_category(SLUG, PAGE, FAMILIES, SET, SECTION,
                   extra={"nav_label": "Bead rollers", "related_pages": [{"href": "circle-cutters-and-seamers.html", "label": "Circle cutters & lock seamers"}, {"href": "plate-rollers.html", "label": "Plate rollers & slip rolls"}]})
    return IMAGES
