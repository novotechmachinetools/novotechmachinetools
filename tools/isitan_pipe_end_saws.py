"""İşitan section: pipe-end processing (PN notchers, TD deburring, SFF end formers; catalogue pages 50–51)
and SFC circular cold saws (pages 52–53) — two category pages."""
from isitan_lib import *  # noqa: F401,F403

SET = "pipe-end-and-saws"
SECTION = "Tube notchers, end formers & cold saws"
P_END, P_SAW = "tube-notchers-and-end-formers", "circular-cold-saws"

IMAGES = {
    "is-pn-17-90": ("img/ISITAN-PN-17-90.jpg", "İşitan PN 17/90 motorized belt-sander tube notcher, 11/16″ to 3-1/2″ OD"),
    "is-pn-20-76": ("img/ISITAN-PN20-76.jpg", "İşitan PN 20/76 compact tube notcher with movable clamp, 13/16″ to 3″ OD"),
    "is-td-01": ("img/ISITAN-TD-01.jpg", "İşitan TD-01 motorized tube-end deburring machine, inside and outside to Ø3-1/2″"),
    "is-sff-90-1": ("img/ISITAN-SFF-90.jpg", "İşitan SFF 90-1 single-station hydraulic pipe-end former, expand and reduce to Ø3-1/2″"),
    "is-sff-60-1": ("img/ISITAN-SFF-60-2.jpg", "İşitan SFF 60-1 single-station hydraulic pipe-end former, expand and reduce to Ø2-3/8″"),
    "is-sff-tooling": ("cut/p51-386.png", "SFF end former — easy tool-changing system with the end-forming tooling set"),
    "is-sfc-350-vx": ("img/VX-350.jpg", "İşitan SFC 350-VX semi-automatic circular cold saw, 13-3/4″ blade, Ø4-1/2″ round"),
    "is-sfc-315-vp": ("cut/p52-392.png", "İşitan SFC 315-VP circular cold saw with pneumatic vise, 12-1/2″ blade"),
    "is-sfc-275-v": ("cut/p52-394.png", "İşitan SFC 275-V manual circular cold saw, 10-3/4″ blade, Ø3-3/8″ round"),
}

GK_END = ["capacity", "detail", "motor", "weight"]
GK_SAW = ["blade", "round", "square", "installed_power", "weight"]


def t_pn():
    t = manual_table("PN — motorized pipe notching machines", "Belt-sander tube notchers · 10 dovetail drums standard", ["PN 17/90", "PN 20/76"], [
        ("Notching capacity", "tube OD", ["11/16″ – 3-1/2″ (Ø17 – 90 mm)", "13/16″ – 3″ (Ø20 – 76 mm)"]),
        ("Max. notching angle", ["50°", "50°"]),
        ("Sanding belt", ["4 × 47″ (100 × 1200 mm)", "4 × 79″ (100 × 2000 mm)"]),
        ("Dovetail drums included", ["10 · Ø3/4″, 13/16″, 1″, 1-1/4″, 1-1/2″, 1-5/8″, 1-7/8″, 2″, 2-3/8″, 3″", "10 · Ø3/4″, 13/16″, 1″, 1-1/4″, 1-1/2″, 1-5/8″, 1-7/8″, 2″, 2-3/8″, 3″"]),
        ("Motor power", ["3 HP (2.2 kW)", "3 HP (2.2 kW)"]),
        ("Dimensions L × W × H", ["43 × 33 × 47″ (1100 × 850 × 1200 mm)", "53 × 28 × 47″ (1350 × 700 × 1200 mm)"]),
        ("Weight", ["375 lb (170 kg)", "287 lb (130 kg)"]),
    ], key_labels=("Notching capacity",))
    glance = {"PN 17/90": ["Notches 11/16″ – 3-1/2″ OD", "Up to 50° · 4 × 47″ belt", "3 HP", "375 lb"],
              "PN 20/76": ["Notches 13/16″ – 3″ OD", "Up to 50° · 4 × 79″ belt · movable clamp", "3 HP", "287 lb"]}
    caps = {"PN 17/90": "Notches 11/16″ – 3-1/2″ OD tube, up to 50°", "PN 20/76": "Notches 13/16″ – 3″ OD tube, up to 50°"}
    return manual_spec([t], GK_END, glance, caps, "Notching capacity is the tube outside diameter; dovetail drums for other sizes are optional. Dimensions are overall L × W × H.")


def t_td():
    t = manual_table("TD-01 — motorized tube-end deburring machine", "Wire-brush deburring inside and out", ["TD-01"], [
        ("Deburring capacity", "inside and outside", ["Up to Ø3-1/2″ (Ø90 mm)"]),
        ("Wire brush", ["Ø10″ × 4″ (Ø250 × 100 mm)"]),
        ("Brush speed", ["1,500 rpm"]),
        ("Profiles", ["Round, rectangular, oval and other tube"]),
        ("Materials", ["Stainless steel, mild steel, aluminum and more"]),
        ("Motor power", ["3 HP (2.2 kW)"]),
        ("Dimensions L × W × H", ["18 × 18 × 14″ (450 × 450 × 350 mm)"]),
        ("Weight", ["88 lb (40 kg)"]),
    ], key_labels=("Deburring capacity",))
    glance = {"TD-01": ["Deburrs tube ends to Ø3-1/2″", "Ø10″ × 4″ wire brush · 1,500 rpm", "3 HP", "88 lb"]}
    caps = {"TD-01": "Wire-brush deburring of tube ends to Ø3-1/2″"}
    return manual_spec([t], GK_END, glance, caps, "Dimensions are overall L × W × H.")


def t_sff():
    t = manual_table("SFF — single-station hydraulic pipe-end forming machines", "Expand or reduce tube ends · 1 tooling set included", ["SFF 90-1", "SFF 60-1"], [
        ("Expanding capacity", "mild steel tube", ["Ø1-3/8″ – 3-1/2″ × 14 ga (Ø35 – 90 × 2 mm)", "Ø1-3/8″ – 2-3/8″ × 14 ga (Ø35 – 60 × 2 mm)"]),
        ("Reducing capacity", "mild steel tube", ["Ø5/16″ – 3-1/2″ × 14 ga (Ø8 – 90 × 2 mm)", "Ø5/16″ – 2-3/8″ × 14 ga (Ø8 – 60 × 2 mm)"]),
        ("Motor power", ["15 HP (11 kW)", "10 HP (7.5 kW)"]),
        ("Dimensions L × W × H", ["51 × 28 × 45″ (1300 × 700 × 1150 mm)", "51 × 28 × 45″ (1300 × 700 × 1150 mm)"]),
        ("Weight", ["1,301 lb (590 kg)", "992 lb (450 kg)"]),
    ], key_labels=("Expanding capacity", "Reducing capacity"))
    glance = {"SFF 90-1": ["Expands Ø1-3/8″ – 3-1/2″ · reduces Ø5/16″ – 3-1/2″ × 14 ga", "Single station · hydraulic · foot pedal", "15 HP", "1,301 lb"],
              "SFF 60-1": ["Expands Ø1-3/8″ – 2-3/8″ · reduces Ø5/16″ – 2-3/8″ × 14 ga", "Single station · hydraulic · foot pedal", "10 HP", "992 lb"]}
    caps = {"SFF 90-1": "Expands and reduces tube ends to Ø3-1/2″ × 14 ga", "SFF 60-1": "Expands and reduces tube ends to Ø2-3/8″ × 14 ga"}
    return manual_spec([t], GK_END, glance, caps, "Capacities are for mild steel tube at the wall thickness shown. Dimensions are overall L × W × H.")


def t_sfc(models):
    data = {
        "SFC 350-VX": ["13-3/4″ (350 mm)", "Ø4-1/2″ / Ø4-3/8″", "3-7/8″ × 3-7/8″", "3-1/2″ × 3-1/2″", "4-3/4″ × 3-1/8″", "3-1/2″ × 3-1/2″", "45 / 80 rpm", "2.4 – 3.0 HP (1.8 – 2.2 kW)", "7.8 HP (5.8 kW)", "43 × 24 × 55″ (1100 × 600 × 1400 mm)", "661 lb (300 kg)"],
        "SFC 275-VP": ["10-3/4″ (275 mm)", "Ø3-3/8″ / Ø2-3/4″", "2-3/4″ × 2-3/4″", "2-3/8″ × 2-3/8″", "3-3/4″ × 2-3/8″", "2-3/4″ × 2-1/8″", "45 / 90 rpm", "1.7 – 2.4 HP (1.3 – 1.8 kW)", "5.0 HP (3.7 kW)", "39 × 24 × 55″ (1000 × 600 × 1400 mm)", "463 lb (210 kg)"],
        "SFC 315-VP": ["12-1/2″ (315 mm)", "Ø4-1/8″ / Ø3-1/2″", "3-3/8″ × 3-3/8″", "3-1/8″ × 3-1/8″", "4-3/4″ × 2-3/8″", "3-1/2″ × 2-3/8″", "45 / 90 rpm", "1.7 – 2.4 HP (1.3 – 1.8 kW)", "6.3 HP (4.7 kW)", "39 × 24 × 55″ (1000 × 600 × 1400 mm)", "441 lb (200 kg)"],
        "SFC 275-V": ["10-3/4″ (275 mm)", "Ø3-3/8″ / Ø2-3/4″", "2-3/4″ × 2-3/4″", "2-3/8″ × 2-3/8″", "3-3/4″ × 2-3/8″", "2-3/4″ × 2-1/8″", "45 / 90 rpm", "1.7 – 2.4 HP (1.3 – 1.8 kW)", "5.0 HP (3.7 kW)", "39 × 24 × 55″ (1000 × 600 × 1400 mm)", "419 lb (190 kg)"],
        "SFC 315-V": ["12-1/2″ (315 mm)", "Ø4-1/8″ / Ø3-1/2″", "3-3/8″ × 3-3/8″", "3-1/8″ × 3-1/8″", "4-3/4″ × 2-3/8″", "3-1/2″ × 2-3/8″", "45 / 90 rpm", "1.7 – 2.4 HP (1.3 – 1.8 kW)", "6.3 HP (4.7 kW)", "39 × 24 × 55″ (1000 × 600 × 1400 mm)", "441 lb (200 kg)"],
    }
    labels = [("Blade Ø", ""), ("Round — 90° / 45°", "mild steel"), ("Square — 90°", ""), ("Square — 45°", ""), ("Rectangular — 90°", ""), ("Rectangular — 45°", ""),
              ("Blade speeds", "two-speed"), ("Saw motor", ""), ("Installed power", "incl. 0.08 HP coolant pump"), ("Dimensions L × W × H", ""), ("Net weight", "")]
    rows = [(lab, sub, [data[m][i] for m in models]) for i, (lab, sub) in enumerate(labels)]
    rows.insert(6, ("Mitre range", ["0 – 45° left and right"] * len(models)))
    rows.insert(10, ("Blade bore / pin holes", ["32 mm / 2 × Ø11 mm"] * len(models)))
    return manual_table("SFC circular cold saws", "Cutting capacities at 90° / 45°", models, rows, key_labels=("Blade", "Round", "Square", "Rectangular"))


SFC_GLANCE = {"SFC 350-VX": ["13-3/4″", "Ø4-1/2″ · Ø4-3/8″ at 45°", "3-7/8″", "7.8 HP", "661 lb"],
              "SFC 275-VP": ["10-3/4″", "Ø3-3/8″ · Ø2-3/4″ at 45°", "2-3/4″", "5.0 HP", "463 lb"],
              "SFC 315-VP": ["12-1/2″", "Ø4-1/8″ · Ø3-1/2″ at 45°", "3-3/8″", "6.3 HP", "441 lb"],
              "SFC 275-V": ["10-3/4″", "Ø3-3/8″ · Ø2-3/4″ at 45°", "2-3/4″", "5.0 HP", "419 lb"],
              "SFC 315-V": ["12-1/2″", "Ø4-1/8″ · Ø3-1/2″ at 45°", "3-3/8″", "6.3 HP", "441 lb"]}
SFC_CAPS = {"SFC 350-VX": "13-3/4″ blade · Ø4-1/2″ round · semi-automatic", "SFC 315-VP": "12-1/2″ blade · Ø4-1/8″ round · pneumatic vise", "SFC 275-VP": "10-3/4″ blade · Ø3-3/8″ round · pneumatic vise",
            "SFC 315-V": "12-1/2″ blade · Ø4-1/8″ round · manual vise", "SFC 275-V": "10-3/4″ blade · Ø3-3/8″ round · manual vise"}
SFC_NOTE = "Cutting capacities are for mild steel at 90° and 45°. Wet-type cold sawing with the standard coolant pump; TiN, TiCN and TiAlN-coated HSS blades are available for medium-hard, high-strength and stainless steel."


def t_sfc_vx():
    return manual_spec([t_sfc(["SFC 350-VX"])], GK_SAW, SFC_GLANCE, SFC_CAPS, SFC_NOTE + " Air supply for the SFC 350-VX: 85 psi, 8.5 cfm.")


def t_sfc_v():
    return manual_spec([t_sfc(["SFC 275-VP", "SFC 315-VP", "SFC 275-V", "SFC 315-V"])], GK_SAW, SFC_GLANCE, SFC_CAPS, SFC_NOTE)


FAMILIES = [
    dict(id="isitan-pn", group="notch", page=P_END,
         name="PN 17/90 · PN 20/76 — motorized pipe notching machines",
         short="PN tube notchers",
         models_label="PN 17/90 · PN 20/76",
         summary="Belt-sander tube notchers that cope a saddle on the end of a tube in seconds for welded handrail, roll-cage, "
                 "furniture and frame joints. Ten dovetail drums from Ø3/4″ to 3″ are standard — pick the drum for the tube "
                 "you are joining, clamp the workpiece in the moving clamp and notch square or at any angle up to 50°. The "
                 "PN 17/90 takes tube from 11/16″ to 3-1/2″ OD on a 4 × 47″ belt; the PN 20/76 is the compact notcher with "
                 "a movable clamp, 13/16″ to 3″ OD on a 4 × 79″ belt.",
         features=["10 dovetail drums standard: Ø3/4″, 13/16″, 1″, 1-1/4″, 1-1/2″, 1-5/8″, 1-7/8″, 2″, 2-3/8″, 3″ — quickly opens the right dovetail for each tube diameter",
                   "Fast clamping and release with the moving clamp; clamp moves left and right", "Notching at any angle up to 50° with the movable clamp",
                   "PN 17/90: basic centering and easy belt adjustment, 4 × 47″ belt", "PN 20/76: compact notcher with movable clamp, 4 × 79″ belt", "3 HP motor; CE certified"],
         optional=["Special dovetail drums for other tube sizes", "Sanding belts", VOLT],
         images=["is-pn-17-90", "is-pn-20-76"],
         videos=[], specs=t_pn(),
         headline="Tube 11/16″ to 3-1/2″ OD · notching to 50° · 10 dovetail drums included"),
    dict(id="isitan-td-01", group="notch", page=P_END,
         name="TD-01 — motorized tube-end deburring machine",
         short="TD-01",
         models_label="TD-01",
         summary="A bench deburring machine with a Ø10″ × 4″ wire brush at 1,500 rpm that cleans the inside and outside of a tube "
                 "end in one pass, up to Ø3-1/2″ — round, rectangular, oval and other profiles in stainless, mild steel or "
                 "aluminum. Sits beside the cold saw or the bender and takes the burr off before welding or bending, at very "
                 "low running cost.",
         features=["Inside and outside deburring up to Ø3-1/2″ in one pass", "Wire brush Ø10″ × 4″ at 1,500 rpm — fast, easy deburring at high speed",
                   "Round, rectangular, oval and other profiles; stainless steel, mild steel, aluminum and more", "Balanced, long-life construction; works alongside tube benders and saws", "3 HP motor; low running cost, high productivity"],
         optional=["Replacement wire brushes", VOLT],
         images=["is-td-01"],
         videos=[], specs=t_td(),
         headline="Tube ends to Ø3-1/2″ · inside and outside in one pass · Ø10″ wire brush"),
    dict(id="isitan-sff", group="form", page=P_END,
         name="SFF 90-1 · SFF 60-1 — single-station hydraulic pipe-end forming machines",
         short="SFF end formers",
         models_label="SFF 90-1 · SFF 60-1",
         summary="Hydraulic end formers that expand or reduce (collapse) a tube end with one tooling set, for exhaust slip joints, "
                 "handrail sleeves, telescoping tube and furniture connectors. The SFF 90-1 expands Ø1-3/8″ to 3-1/2″ and reduces "
                 "down from Ø5/16″ in 14 ga mild steel with a 15 HP power unit; the SFF 60-1 covers tube to Ø2-3/8″ with 10 HP. "
                 "An easy tool-changing system swaps the forming set in minutes.",
         features=["Expands or reduces (collapses) pipe ends in a single station", "1 set of end-forming tooling in requested size; easy tool-changing system",
                   "Hydraulic power unit — 15 HP on the SFF 90-1, 10 HP on the SFF 60-1", "Mobile foot pedal; CE certified"],
         optional=["Additional end-forming tooling sets", VOLT],
         images=["is-sff-90-1", "is-sff-60-1", "is-sff-tooling"],
         videos=[], specs=t_sff(),
         headline="Expand and reduce tube ends to Ø3-1/2″ × 14 ga · one tooling set included"),
    dict(id="isitan-sfc-350-vx", group="semi", page=P_SAW,
         name="SFC 350-VX — semi-automatic circular cold saw",
         short="SFC 350-VX",
         models_label="SFC 350-VX · 13-3/4″ blade",
         summary="A semi-automatic cold saw for short batch runs: foot-switch actuation, hydro-pneumatic head descent with a "
                 "cutting-speed regulator and head stroke set to the material, so the operator loads and the saw cuts. Heavy-duty "
                 "double gearbox, cast-iron base, two blade speeds and mitre cuts 45° each way — Ø4-1/2″ round and 3-7/8″ "
                 "square mild steel on a 13-3/4″ HSS blade, burr-free and ready to weld.",
         features=["Semi-automatic cycle: foot-switch actuation, hydro-pneumatic head descent with cutting-speed regulator; head stroke adjustable to material size",
                   "Heavy-duty double gearbox; cast-iron base; two blade speeds 45 / 80 rpm", "Mitre cuts 45° right to 45° left; self-centering double split vise grips both sides of the material",
                   "Wet-type cold sawing for clean, burr-free cuts; coolant pump and tank", "24 V control voltage; CSA-approved panel; air supply 85 psi (8.5 cfm)"],
         optional=["Saw blades for specific materials — TiN for medium-hard steel, TiCN for high-strength steel, TiAlN for stainless", VOLT],
         images=["is-sfc-350-vx"],
         videos=[], specs=t_sfc_vx(),
         headline="13-3/4″ blade · Ø4-1/2″ round · semi-automatic, 45 / 80 rpm"),
    dict(id="isitan-sfc-v", group="manual", page=P_SAW,
         name="SFC 275 / 315-VP · SFC 275 / 315-V — circular cold saws with pneumatic or manual vise",
         short="SFC VP · V",
         models_label="SFC 275-VP · 315-VP · 275-V · 315-V",
         summary="Pull-down circular cold saws with a 10-3/4″ or 12-1/2″ blade, two speeds and mitre cuts 45° left and right: "
                 "the VP models clamp with an air-operated vise, the V models with a manual vise. Low-voltage start/stop trigger "
                 "in the handle, a robust double-hinged pivot, a double split vise that grips both sides of the cut and a large "
                 "base for stability — the metal cutting saw for tube, bar and profile in the fabrication shop, with a clean, "
                 "burr-free cut the band saw cannot match.",
         features=["SFC VP: air-operated material vise; SFC V: manually operated vise", "Low-voltage start/stop trigger in the pull-down handle; robust double-hinged pivot",
                   "Mitre cuts 45° left and right; double split vise grips both sides of the material; self-centering vise optimizes the cutting position",
                   "Two blade speeds 45 / 90 rpm; wet-type cold sawing for burr-free cuts; coolant pump and tank", "Large base for stability; 24 V control voltage; CSA-approved panel"],
         optional=["Saw blades for specific materials — TiN for medium-hard steel, TiCN for high-strength steel, TiAlN for stainless", VOLT],
         images=["is-sfc-315-vp", "is-sfc-275-v"],
         videos=[], specs=t_sfc_v(),
         headline="10-3/4″ and 12-1/2″ blades · Ø3-3/8″ and Ø4-1/8″ round · pneumatic or manual vise"),
]

PAGES = {
    P_END: dict(
        title="Tube Notchers, Pipe End Formers & Tube Deburring Machines | NovoTech Canada",
        meta="İşitan tube notchers, pipe-end forming and deburring machines in Canada: PN belt-sander pipe notchers for 11/16″ to 3-1/2″ OD tube to 50°, SFF hydraulic end formers that expand and reduce tube ends to Ø3-1/2″, and the TD-01 wire-brush deburring machine. Specs in inches, CSA panels, parts in Mississauga, ON.",
        h1="Tube notchers, end formers and deburring machines",
        intro="The machines that finish a tube end: PN belt-sander tube notchers that cope a saddle for welded handrail, cage and frame joints at any angle to 50° with ten dovetail drums included; SFF single-station hydraulic end formers that expand or reduce tube ends to Ø3-1/2″ for exhaust slip joints and sleeves; and the TD-01 wire-brush deburring machine that cleans inside and out in one pass. They sit beside the cold saw and the tube bender and take the hand grinding out of tube fabrication — with CSA-approved panels and support from Mississauga, ON.",
        points=["Pipe notchers — tube 11/16″ to 3-1/2″ OD, notching to 50°, 10 dovetail drums standard", "Hydraulic end formers — expand and reduce tube ends to Ø3-1/2″ × 14 ga", "TD-01 deburring — inside and outside to Ø3-1/2″ in one pass"],
        hero="is-pn-17-90", minis=["is-sff-90-1", "is-td-01"],
        groups=[("notch", "Tube notchers and deburring", "PN belt-sander notchers and the TD-01 wire-brush deburring machine."),
                ("form", "Pipe-end forming", "SFF hydraulic end formers for expanding and reducing tube ends.")],
        faq=[{"q": "What is a tube notcher for?", "a": "When one tube meets another in a T or at an angle — handrail posts, roll cages, furniture and bike frames, trailer and gate frames — the end has to be coped to the curve of the tube it joins so the weld closes without gaps. The PN notcher grinds that saddle on a sanding belt against a drum of the mating tube's diameter in seconds, square or at any angle to 50°."},
             {"q": "Which notcher — PN 17/90 or PN 20/76?", "a": "The PN 17/90 takes the larger range, 11/16″ to 3-1/2″ OD, on a 4 × 47″ belt with easy belt adjustment. The PN 20/76 is the compact notcher for 13/16″ to 3″ OD with a longer 4 × 79″ belt and a movable clamp. Both come with the same ten dovetail drums and 3 HP motor."},
             {"q": "Expanding or reducing — what does the end former do?", "a": "An expander opens a tube end so the next tube slips inside (exhaust slip joints, telescoping handrail, sleeves); a reducer collapses the end to fit into the next tube. The SFF does both in one station with a hydraulic ram and interchangeable forming tools — one set is included, others are quoted to your tube size."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about tube notchers and end formers",
    ),
    P_SAW: dict(
        title="Circular Cold Saws — Manual & Semi-Automatic Metal Cutting Saws for Tube and Bar | NovoTech Canada",
        meta="İşitan SFC circular cold saws in Canada: 10-3/4″, 12-1/2″ and 13-3/4″ blade metal cutting saws with manual, pneumatic or semi-automatic vise, round to Ø4-1/2″, mitre 45° both ways, two speeds, wet cutting. Specs in inches, CSA panels, parts in Mississauga, ON.",
        h1="Circular cold saws",
        intro="Wet-type circular cold saws for burr-free cuts in tube, bar and profile: the SFC 275 and 315 pull-down saws with a manual or pneumatic vise and the semi-automatic SFC 350-VX with a hydro-pneumatic head for short batch runs. Two blade speeds, mitre cuts 45° left and right, a double split vise that grips both sides of the cut and a low-voltage trigger in the handle — the metal chop saw that leaves a square, cool, weld-ready end instead of an abrasive burr. HSS blades with TiN, TiCN and TiAlN coatings for mild, high-strength and stainless steel, CSA-approved panels and support from Mississauga, ON. For automatic production cold saws see our Bekamak range.",
        points=["Round to Ø4-1/2″ · square to 3-7/8″ · rectangular to 4-3/4″ × 3-1/8″ mild steel", "10-3/4″, 12-1/2″ and 13-3/4″ HSS blades · two speeds · mitre 45° both ways", "Manual vise, pneumatic vise or semi-automatic cycle"],
        hero="is-sfc-350-vx", minis=["is-sfc-315-vp", "is-sfc-275-v"],
        groups=[("semi", "Semi-automatic cold saw", "The SFC 350-VX with foot-switch cycle and hydro-pneumatic head descent."),
                ("manual", "Pull-down cold saws", "SFC VP with pneumatic vise and SFC V with manual vise, 10-3/4″ and 12-1/2″ blades.")],
        faq=[{"q": "Cold saw or abrasive chop saw?", "a": "An abrasive chop saw grinds through the steel at high speed, leaving a hot, burred, slightly bevelled end and sparks. A cold saw cuts with a slow HSS blade (45–90 rpm) under coolant, so the cut is square, cool to the touch, burr-free and ready to weld or fit — and the blade is resharpened dozens of times instead of thrown away."},
             {"q": "Manual, pneumatic or semi-automatic?", "a": "The SFC V clamps with a hand vise — the simplest saw for occasional cuts. The SFC VP clamps with air at the pull of a lever, which saves time on every cut and holds short pieces better. The SFC 350-VX runs a semi-automatic cycle from a foot switch with a regulated head descent, for batches of the same part without an operator on the handle."},
             {"q": "Which blade do I need?", "a": "A standard HSS blade cuts mild steel and aluminum. For medium-hard steel we fit TiN-coated blades, TiCN for high-strength steel and TiAlN for stainless. The blade bore is 32 mm with two Ø11 mm pin holes on all SFC models, so blades are readily available in Canada."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about cold saws",
    ),
}


def build():
    write_families(SET, FAMILIES)
    related_end = [{"href": f"{P_SAW}.html", "label": "Circular cold saws"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "nc-tube-benders.html", "label": "NC tube benders"}]
    related_saw = [{"href": f"{P_END}.html", "label": "Tube notchers & end formers"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "cold-saw-carbide-saw-cutting.html", "label": "Automatic cold saws"}, {"href": "band-saw.html", "label": "Band saws"}]
    write_category(P_END, {**PAGES[P_END], "related_pages": related_end, "related_title": "More tube machinery from NovoTech"}, FAMILIES, SET, SECTION, extra={"nav_label": "Tube notchers & end formers"})
    write_category(P_SAW, {**PAGES[P_SAW], "related_pages": related_saw, "related_title": "More cutting machinery from NovoTech"}, FAMILIES, SET, SECTION, extra={"nav_label": "Circular cold saws"})
    return IMAGES
