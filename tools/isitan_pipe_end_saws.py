"""İşitan section: pipe-end processing (PN notchers, TD deburring, SFF end formers; catalogue pages 50–51)
and SFC circular cold saws (pages 52–53) — three category pages: tube notchers (old-site URL pipe-notcher kept),
tube end forming machines, cold saws."""
from isitan_lib import *  # noqa: F401,F403
from bekamak_extra import CIRCULAR_FAMILIES, CIRCULAR_IMAGES  # noqa: E402  (Bekamak BMDO saws share the cold saw page)
import wecotech_data  # Wecotech (Switzerland) tube end formers share the tube end forming page
import importlib.util

SET = "pipe-end-and-saws"
SECTION = "Tube notchers, end formers & cold saws"
P_NOTCH, P_FORM, P_SAW = "pipe-notcher", "tube-end-forming-machines", "circular-cold-saws"
P_END = P_NOTCH   # kept for older imports

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
    dict(id="isitan-pn", group="notch", page=P_NOTCH,
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
    dict(id="isitan-td-01", group="deburr", page=P_NOTCH,
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
    dict(id="isitan-sff", group="form", page=P_FORM,
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
         videos=wecotech_data.vids(("QjR0oYrLpRs", "SFF 90 hydraulic pipe end forming machine — expander and shrinker"), ("wj2MHDKj9tk", "SFF 60 pipe end forming machine")), specs=t_sff(),
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
] + [dict(f, page=P_SAW) for f in CIRCULAR_FAMILIES]

PAGES = {
    P_NOTCH: dict(
        title="Tube Notchers & Pipe Notching Machines | NovoTech",
        meta="Belt-sander tube and pipe notchers for tube 11/16″ to 3-1/2″ OD at any angle to 50°, ten dovetail drums included, plus the TD-01 tube-end deburring machine.",
        h1="Tube notchers and pipe notching machines",
        intro="A tube notcher (pipe notcher or coping machine) grinds a saddle-shaped notch into the end of a tube so it fits tightly against the tube it joins — the joint of every welded handrail, roll cage, trailer, gate and furniture frame. İşitan's PN belt-sander notchers cope that saddle in seconds, square or at any angle up to 50°, with ten dovetail drums from Ø3/4″ to 3″ included so the notch matches the mating tube; the TD-01 wire-brush deburring machine cleans the cut end inside and out in one pass before it goes to the notcher or the bender. Both sit beside the cold saw and take the hand grinding out of tube fabrication — with CSA-approved panels and support from Mississauga, ON.",
        points=["Pipe notchers — tube 11/16″ to 3-1/2″ OD, notching to 50°, 10 dovetail drums standard", "PN 17/90 with 4 × 47″ belt; compact PN 20/76 with movable clamp and 4 × 79″ belt", "TD-01 deburring — inside and outside to Ø3-1/2″ in one pass"],
        hero="is-pn-17-90", minis=["is-pn-20-76", "is-td-01"],
        groups=[("notch", "Tube notchers", "PN belt-sander pipe notching machines with ten dovetail drums included."),
                ("deburr", "Tube-end deburring", "The TD-01 wire-brush machine that cleans the cut end inside and out before notching or bending.")],
        faq=[{"q": "What is a tube notcher for?", "a": "When one tube meets another in a T or at an angle — handrail posts, roll cages, furniture and bike frames, trailer and gate frames — the end has to be coped to the curve of the tube it joins so the weld closes without gaps. The PN notcher grinds that saddle on a sanding belt against a drum of the mating tube's diameter in seconds, square or at any angle to 50°."},
             {"q": "Which notcher — PN 17/90 or PN 20/76?", "a": "The PN 17/90 takes the larger range, 11/16″ to 3-1/2″ OD, on a 4 × 47″ belt with easy belt adjustment. The PN 20/76 is the compact notcher for 13/16″ to 3″ OD with a longer 4 × 79″ belt and a movable clamp. Both come with the same ten dovetail drums and 3 HP motor."},
             {"q": "Belt notcher or hole-saw notcher?", "a": "A hole-saw notcher cuts the cope with a hole saw of the mating tube's diameter — slow, and the saw dulls on stainless. The PN grinds the cope on a sanding belt wrapped around a dovetail drum, so it is faster, works on any material and leaves a clean, square-to-weld edge; the drum is swapped in seconds for the next tube size."},
             {"q": "Does the notcher deburr the tube as well?", "a": "No — the notcher shapes the cope. The TD-01 is the machine that removes the burr left by the saw: a Ø10″ wire brush cleans the inside and outside of the tube end in one pass, on round, square and rectangular tube to Ø3-1/2″, so the tube is ready to notch, bend or weld."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about tube notchers",
    ),
    P_FORM: dict(
        title="Tube End Forming Machines — Expand, Reduce, Bead | NovoTech",
        meta="Tube end formers from a Ø3-1/2″ hydraulic expander-reducer to Swiss CNC inner / outer machines for Ø23.6″: expanding, reducing, beading, flaring, flanging; tube cutting and deburring.",
        h1="Tube end forming machines — expanding, reducing, beading and flanging",
        intro="A tube end former (pipe end forming machine) expands or reduces the end of a tube so two tubes slip together, "
              "and the production versions bead, flare, flange, calibrate and emboss the end as well — the machines behind exhaust "
              "systems, ventilation and chimney tube, shock absorbers, handrail and furniture connectors. Two ranges on this page, "
              "small to large. İşitan's SFF single-station hydraulic end formers expand and reduce tube to Ø3-1/2″ × 14 ga with one "
              "tooling set, for the fabrication shop. Wecotech's Swiss tube end forming machines cover series production: the Easy "
              "line of compact expanders, reducers, a straightening press and a punching unit; the Universal line of modular "
              "production machines — expanders, reducers, axial and servo rotary formers, a multi-station forming centre and an "
              "automatic beading machine to Ø39.4″; the Traditional line built for the C and IO tooling that is standard in the "
              "exhaust trade; the Weco line of CNC inner / outer formers with programmable tool rotation for tube to Ø23.6″ and a "
              "flanging cell for bellows; and the shearing cutters, tube shear and deburring machine that complete an end-forming "
              "cell. Siemens controls, Bosch Rexroth hydraulics or servo drives, CSA-approved panels and support from Mississauga, ON.",
        points=["İşitan SFF hydraulic end formers — expand and reduce tube ends to Ø3-1/2″ × 14 ga, tooling set included",
                "Wecotech compact expanders and reducers from Ø3/8″ to Ø23.6″, 21 – 26 US tons, 2 – 4 s cycles, touchscreen programming",
                "Wecotech CNC inner / outer formers to Ø23.6″ with 8 – 24 radial pistons, Tubimatic machines for standard C and IO tools, beading, flanging, shearing and deburring"],
        hero="wt-wecomatic-200", minis=["is-sff-90-1", "wt-tubex"],
        groups=[("form", "İşitan hydraulic tube end formers", "SFF single-station end forming machines for expanding and reducing tube ends with one tooling set.", "isitan"),
                ("wt-easy", "Wecotech Easy line — compact expanders, reducers and auxiliaries", "Entry-level machines with the electrics and hydraulics in one compact housing: the Tubex expander, Tubin reducers, the Tubepress straightening press and the Tubepunch slot punching unit.", "wecotech"),
                ("wt-universal", "Wecotech Universal line — modular production machines", "The HW-Flex housing with touchscreen programming and a choice of options: Tubex-U and Tubin-U, the Tubax axial and rotary formers, the Tubax-Multi forming centre and the Tubiroll-2R beading machine — small to large.", "wecotech"),
                ("wt-traditional", "Wecotech Traditional line — for standard C and IO tooling", "Production end formers that take the commercially available C-tools and IO-tools of the exhaust trade, hydraulic or servo-electric (Electra), with one to three tool stations.", "wecotech"),
                ("wt-weco", "Wecotech Weco line — CNC inner / outer tube end formers", "The flagship machines: an inner mandrel and 8 to 24 radial outer pistons under CNC control, with programmable inner-tool rotation on the Wecomatic, for tube to Ø23.6″; plus the flanging cell for bellows and T-pieces.", "wecotech"),
                ("wt-cutting", "Wecotech tube cutting and deburring", "The shearing cutter, tube shear and deburring machine that cut and prepare the tube before and after forming.", "wecotech")],
        faq=[{"q": "Expanding or reducing — what does the end former do?", "a": "An expander opens a tube end so the next tube slips inside (exhaust slip joints, telescoping handrail, sleeves); a reducer collapses the end to fit into the next tube. The İşitan SFF does both in one station with a hydraulic ram and interchangeable forming tools; the Wecotech Tubex and Tubex-U expand with a cone-driven segmented tool, the Tubin and Tubin-U reduce with collet-type top jaws, and the Tubimatic and Weco-line machines do both — and bead, flare and flange — with inner and outer tools."},
             {"q": "What is an inner / outer (IO) tube end former?", "a": "A machine with two tools that work on the tube end at the same time: an inner mandrel or expansion tool inside the tube and an outer tool — closing jaws or, on the Weco line, 8 to 24 radial pistons — around it. Between them the end is expanded, reduced, beaded, flared, flanged or embossed to a defined shape in one stroke, in any position on round or shaped tube. The Tubimatic IO machines take the commercially available IO-tools; the Tubex IO-S and Wecomatic run Wecotech's own tooling under CNC."},
             {"q": "Which Wecotech line do I need?", "a": "The Easy line is for a shop that forms a few hundred ends a day beside a bender or saw: compact, foot-switch operated, 21 US tons. The Universal line is the modular production machine with touchscreen programming, 26 US tons and the options that a production cell needs — heat exchangers, remote maintenance, Profisafe, horizontal version. The Traditional line is the choice when you already own C or IO tooling. The Weco line is for complex, multi-step forming of exhaust, ventilation and chimney parts at 10 – 40 s a cycle, programmed on the machine."},
             {"q": "What tube sizes and wall thickness can the SFF form?", "a": "The SFF 90-1 expands tube from Ø1-3/8″ to Ø3-1/2″ and reduces ends down to Ø5/16″, in mild steel up to 14 ga; the SFF 60-1 covers tube to Ø2-3/8″. Stainless and thicker walls are quoted case by case — send us the tube OD, wall and the finished end size you need."},
             {"q": "Hydraulic or Electra?", "a": "Wecotech builds the Tubimatic IO, Tubax-Rotary, Tubax-Multi and Tubecut as Electra versions with Bosch Rexroth servo drives instead of a hydraulic power unit: no oil, no heat exchanger, lower energy use and quieter running, with the forming force and position under direct servo control. The hydraulic versions keep the higher force reserve (37 US tons on the IO 160) and the lower price."},
             {"q": "How long does a tool change take?", "a": "A few minutes on every machine on this page: the SFF holds its forming set in a quick-change holder; the Wecotech machines have quick-change flanges for the basic tool and the mandrel and quick-change interfaces for the outer jaws, and the Tubimatic C 80 TRE carries three tool stations so three forming steps run without a change at all."},
             {"q": "Can the end former do an exhaust slip joint?", "a": "Yes — that is the most common job: expand one end of the pipe so the next section slides in, or reduce it to slip into a muffler or flex pipe, then bead it for the clamp. The SFF does the expansion and reduction; a Tubimatic IO or Wecomatic adds the bead, flare and calibration in the same stroke."},
             {"q": "Where are these machines made and how are they supported?", "a": "The SFF is built by İşitan in Bursa, Turkey; the Wecotech machines by Wecotech AG in Switzerland, a 60-person company whose customers include 3M, ABB, Akrapovič and American Axle. NovoTech sells, installs and supports both in Canada from Mississauga, ON, with CSA-approved panels, remote maintenance on the Wecotech controls and tooling to your tube size."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about tube end formers",
    ),
    P_SAW: dict(
        title="Cold Saws — Circular & CNC Carbide Cold Saws | NovoTech",
        meta="Cold saw machines for metal from a 10-3/4″ manual circular saw to CNC carbide production saws: wet cutting, burr-free ends, tube and bar to Ø6-1/4″, servo feeding, loaders.",
        h1="Cold saws — circular cold saws, manual to CNC carbide",
        intro="A cold saw cuts metal with a slow-turning, coolant-flooded circular blade instead of a hot abrasive disc, leaving a square, burr-free end that is cool to the touch and ready to weld. Two families of cold saw machines: İşitan's wet-type circular cold saws for the fabrication shop — the SFC 275 and 315 pull-down saws with a manual or pneumatic vise and the semi-automatic SFC 350-VX with a hydro-pneumatic head — and Bekamak's automatic production saws: the BMDO XS high-speed carbide (TCT) cold saws that cut solid bar to Ø6-1/4″ from a 20 ft magazine loader with servo feeding, and the BMDO CS HSS saws for tube and bar to Ø4″ with a servo gripper feed and touch-screen control. Mitre cuts 45° both ways on the İşitan saws, blades for mild, high-strength and stainless steel, CSA-approved panels and support from Mississauga, ON.",
        points=["Manual and semi-automatic circular cold saws: round to Ø4-1/2″, mitre 45° both ways, 10-3/4″ – 13-3/4″ HSS blades", "Automatic carbide cold saws: solid bar Ø3/8″ – 6-1/4″ at up to 920 ft/min, servo feed, 20 ft magazine loader", "Automatic HSS cold saws: tube and bar to Ø4″, ±.004″ feed accuracy, several lengths per bar"],
        hero="is-sfc-350-vx", minis=["bk-bmdo-150xs-1", "bk-bmdo-80cs-1"],
        groups=[("semi", "İşitan semi-automatic cold saw", "The SFC 350-VX with foot-switch cycle and hydro-pneumatic head descent."),
                ("manual", "İşitan pull-down cold saws", "SFC VP with pneumatic vise and SFC V with manual vise, 10-3/4″ and 12-1/2″ blades."),
                ("bekamak-circular", "Bekamak automatic circular saws — TCT carbide and HSS", "Production cold saws that feed, cut and count by themselves: BMDO XS carbide saws for solid bar to Ø6-1/4″ and BMDO CS HSS saws for tube and bar to Ø4″.", "bekamak")],
        faq=[{"q": "Cold saw or abrasive chop saw?", "a": "An abrasive chop saw grinds through the steel at high speed, leaving a hot, burred, slightly bevelled end and sparks. A cold saw cuts with a slow HSS blade (45–90 rpm) under coolant, so the cut is square, cool to the touch, burr-free and ready to weld or fit — and the blade is resharpened dozens of times instead of thrown away."},
             {"q": "TCT carbide or HSS cold saw?", "a": "A carbide (TCT) blade runs at 130–920 ft/min and is the fastest way to cut solid steel bar in production — the Bekamak BMDO XS saws are built around it, with servo feeding and a magazine loader for unattended runs. HSS blades run slower (22–130 ft/min on the BMDO CS) and are the choice for tube, thin walls and mixed work; the XS saws accept HSS blades for tube as well."},
             {"q": "What does an automatic cold saw do by itself?", "a": "You load bars in the magazine (BMDO XS) or on the roller table (BMDO CS), program the lengths and quantities, and the saw feeds each bar with a servo gripper, clamps it hydraulically, cuts, counts and moves on to the next length — to ±.004″ on the CS and with a 60 mm remnant on the XS."},
             {"q": "Manual, pneumatic or semi-automatic?", "a": "The SFC V clamps with a hand vise — the simplest saw for occasional cuts. The SFC VP clamps with air at the pull of a lever, which saves time on every cut and holds short pieces better. The SFC 350-VX runs a semi-automatic cycle from a foot switch with a regulated head descent, for batches of the same part without an operator on the handle."},
             {"q": "Which blade do I need?", "a": "A standard HSS blade cuts mild steel and aluminum. For medium-hard steel we fit TiN-coated blades, TiCN for high-strength steel and TiAlN for stainless. The blade bore is 32 mm with two Ø11 mm pin holes on all SFC models, so blades are readily available in Canada."},
             VOLT_FAQ_GENERIC],
        faq_title="Questions we get asked about cold saws",
    ),
}


def register_bekamak_images():
    """bekamak.com photos of the BMDO saws → tools/image_map.json (white renders, cut out by the pipeline)."""
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    for key, (fn, alt) in CIRCULAR_IMAGES.items():
        imap[key] = {"src": os.path.join("/home/claude/bekamak/site/img", fn), "alt": alt, "section": "bandsaw", "trim": False, "quality": 82}
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return list(CIRCULAR_IMAGES)


def register_wecotech_images():
    """tools/src-images/wecotech/<key>.jpg (copied by tools/wecotech_photos.py) → tools/image_map.json, section 'wecotech'."""
    spec = importlib.util.spec_from_file_location("wecotech_photos", os.path.join(ROOT, "tools", "wecotech_photos.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key, p in m.PHOTOS.items():
        f = os.path.join(ROOT, "tools", "src-images", "wecotech", key + ".jpg")
        if not os.path.exists(f):
            print("!! missing export for", key); continue
        e = {"src": f"tools/src-images/wecotech/{key}.jpg", "alt": p["alt"], "section": "wecotech", "trim": False, "quality": 82}
        if p.get("cutout") is False:
            e["cutout"] = False
        imap[key] = e
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "wecotech_keys.txt"), "w").write(",".join(keys))
    return keys


PDF_WT_FILE = "files/NovoTech-Wecotech-Tube-End-Forming-2026.pdf"


def pdf_wt():
    f = os.path.join(ROOT, "src", PDF_WT_FILE)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": PDF_WT_FILE, "label": "Download the Wecotech tube end forming brochure", "size": size}


def build():
    register_bekamak_images()
    register_wecotech_images()
    PDF_WT = pdf_wt()
    WT_FAMILIES = [dict(f, pdf=PDF_WT) for f in wecotech_data.FAMILIES]
    write_families(SET, FAMILIES + WT_FAMILIES)
    related_notch = [{"href": f"{P_FORM}.html", "label": "Tube end forming machines"}, {"href": f"{P_SAW}.html", "label": "Circular cold saws"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "nc-tube-benders.html", "label": "NC tube benders"}]
    related_form = [{"href": f"{P_NOTCH}.html", "label": "Tube notchers"}, {"href": f"{P_SAW}.html", "label": "Circular cold saws"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "rotary-draw-tube-benders.html", "label": "Rotary draw tube benders"}]
    related_saw = [{"href": f"{P_NOTCH}.html", "label": "Tube notchers"}, {"href": f"{P_FORM}.html", "label": "Tube end forming machines"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"}, {"href": "band-saw.html", "label": "Band saws"}, {"href": "double-column-band-saws.html", "label": "Bekamak double-column band saws"}]
    write_category(P_NOTCH, {**PAGES[P_NOTCH], "related_pages": related_notch, "related_title": "More tube machinery from NovoTech"}, FAMILIES, SET, SECTION, extra={"nav_label": "Tube notchers"})
    write_category(P_FORM, {**PAGES[P_FORM], "related_pages": related_form, "related_title": "More tube machinery from NovoTech"}, FAMILIES + WT_FAMILIES, SET, SECTION,
                   extra={"nav_label": "Tube end formers", "catalogue_pdf": None, "catalogue_pdfs": [PDF, PDF_WT],
                          "hero_brand_line": "İşitan end formers are made in Turkey by İşitan Makine; the Wecotech machines in Switzerland by Wecotech AG. All sold, installed and supported in Canada by NovoTech.",
                          "origin_feature": {"title": "Made in Turkey and Switzerland", "text": "İşitan has built sheet-metal and tube machinery in Bursa since 1959; Wecotech AG builds tube end forming machines in Switzerland for the exhaust, ventilation and automotive industries — Siemens controls, Bosch Rexroth hydraulics and servo drives, CE-certified."}})
    write_category(P_SAW, {**PAGES[P_SAW], "related_pages": related_saw, "related_title": "More cutting machinery from NovoTech"}, FAMILIES, SET, SECTION,
                   extra={"nav_label": "Cold saws", "catalogue_pdf": None, "catalogue_pdfs": [PDF, PDF_BK],
                          "hero_brand_line": "İşitan circular cold saws are made in Turkey by İşitan Makine; the automatic BMDO saws by Bekamak Makina, Turkey. All sold, installed and supported in Canada by NovoTech.",
                          "origin_feature": {"title": "Made in Turkey by İşitan and Bekamak", "text": "İşitan has built sheet-metal machinery in Bursa since 1959; Bekamak has built saws since 1990 — CE-certified machines with European components."}})
    return IMAGES
