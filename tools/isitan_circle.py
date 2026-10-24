"""İşitan section: circle cutting machines and lock seamer (catalogue pages 32–34) — one category page."""
from isitan_lib import *  # noqa: F401,F403
from sahinler_families import CIRCLE_FAMILIES  # Şahinler SDK / EFM tank-head machines below the İşitan group
from sahinler_lib import PDF as PDF_SH

SET = "circle-cutting"
SECTION = "Circle cutters & seamers"
SLUG = "circle-cutters-and-seamers"

IMAGES = {
    "is-idk-5": ("img/ISITAN-IDK-5.jpg", "İşitan IDK-5 hydraulic circle cutting and flanging machine — discs up to 78.7″ in 3/16″ sheet"),
    "is-idk-5-clamp": ("cut/p32-190.png", "IDK-5 — hydraulic clamping and cutting system"),
    "is-idk-5-flanging": ("cut/p32-192.png", "IDK-5 — optional flanging attachment for edge flanging up to 3/8″"),
    "is-idk-35": ("img/ISITAN-IDK-35.jpg", "İşitan IDK-3.5 motorized circle cutting shear with pneumatic centre clamp"),
    "is-idk-2": ("img/ISITAN-IDK-2.jpg", "İşitan IDK-2 heavy-duty motorized circle cutting machine"),
    "is-idk-18": ("img/ISITAN-IDK-18.jpg", "İşitan IDK-1.8 motorized circle cutter with foot pedal"),
    "is-idk-1": ("img/ISITAN-IDK-1.jpg", "İşitan IDK-1 manual circle cutting machine"),
    "is-ls-13p": ("cut/p34-207.png", "İşitan LS-13P pneumatic heavy-duty lock seaming machine"),
    "is-ls-13p-profile": ("cut/p34-209.png", "LS-13P — lock-seam profile"),
    "is-ls-13p-seam": ("cut/p34-210.png", "LS-13P — finished lock seam"),
}

NOTE = "Cutting capacities are for mild steel; thin sheet is given in gauge with the manufacturer's nominal metric value in brackets. Dimensions are overall L × W × H."


def t_idk():
    t = manual_table("IDK series", "5 models · circles Ø4.3″ – 78.7″", ["IDK-5", "IDK-3.5", "IDK-2", "IDK-1.8", "IDK-1"], [
        ("Min. cutting Ø", ["9.8″ (250 mm)", "7.9″ (200 mm)", "4.7″ (120 mm)", "4.3″ (110 mm)", "5.9″ (150 mm)"]),
        ("Max. cutting Ø", ["78.7″ (2000 mm)", "47.2″ (1200 mm)", "39.4″ (1000 mm)", "39.4″ (1000 mm)", "39.4″ (1000 mm)"]),
        ("Cutting capacity", "mild steel", ["3/16″ (5 mm)", "10 ga (3.5 mm)", "14 ga (2 mm)", "14 ga (2 mm)", "20 ga (1 mm)"]),
        ("Cutting speed", ["13 ft/min (4 m/min)", "20 ft/min (6 m/min)", "25 ft/min (7.5 m/min)", "25 ft/min (7.5 m/min)", "manual"]),
        ("Blade material", ["1.2379 tool steel", "1.2379 tool steel", "1.2379 tool steel", "1.2379 tool steel", "1.2379 tool steel"]),
        ("Motor power", ["3 + 1 HP (2.2 + 0.75 kW)", "3 HP (2.2 kW)", "1.5 HP (1.1 kW)", "1.5 HP (1.1 kW)", "—"]),
        ("Hump depth", ["47.2″ (1200 mm)", "29.5″ (750 mm)", "27.6″ (700 mm)", "24.0″ (610 mm)", "23.6″ (600 mm)"]),
        ("Throat depth", ["11.8″ (300 mm)", "9.8″ (250 mm)", "11.0″ (280 mm)", "8.5″ (215 mm)", "7.9″ (200 mm)"]),
        ("Inside-diameter cutting", ["Yes", "Yes", "Yes", "No", "No"]),
        ("Centre clamp", ["Hydraulic", "Pneumatic (116 psi air)", "Manual", "Manual", "Manual"]),
        ("Dimensions L × W × H", ["118 × 30 × 55″ (3000 × 760 × 1400 mm)", "79 × 24 × 55″ (2000 × 610 × 1400 mm)", "55 × 16 × 51″ (1400 × 410 × 1300 mm)", "59 × 16 × 51″ (1500 × 410 × 1300 mm)", "47 × 8 × 18″ (1200 × 200 × 460 mm)"]),
        ("Weight", ["2,976 lb (1,350 kg)", "1,653 lb (750 kg)", "772 lb (350 kg)", "529 lb (240 kg)", "132 lb (60 kg)"]),
    ], key_labels=("Cutting capacity", "Max. cutting"))
    glance = {"IDK-5": ["9.8″ – 78.7″ (250–2000 mm)", "3/16″ (5 mm)", "Yes", "3 + 1 HP", "2,976 lb"],
              "IDK-3.5": ["7.9″ – 47.2″ (200–1200 mm)", "10 ga (3.5 mm)", "Yes", "3 HP", "1,653 lb"],
              "IDK-2": ["4.7″ – 39.4″ (120–1000 mm)", "14 ga (2 mm)", "Yes", "1.5 HP", "772 lb"],
              "IDK-1.8": ["4.3″ – 39.4″ (110–1000 mm)", "14 ga (2 mm)", "No", "1.5 HP", "529 lb"],
              "IDK-1": ["5.9″ – 39.4″ (150–1000 mm)", "20 ga (1 mm)", "No", "manual", "132 lb"]}
    caps = {"IDK-5": "cuts discs to Ø78.7″ (2000 mm) in 3/16″ (5 mm) · hydraulic clamp", "IDK-3.5": "cuts discs to Ø47.2″ (1200 mm) in 10 ga · pneumatic clamp",
            "IDK-2": "cuts discs to Ø39.4″ (1000 mm) in 14 ga · heavy-duty cast frame", "IDK-1.8": "cuts discs to Ø39.4″ (1000 mm) in 14 ga · foot pedal",
            "IDK-1": "cuts discs to Ø39.4″ (1000 mm) in 20 ga · manual"}
    return manual_spec([t], ["cutting_diameter", "cutting_capacity", "inside_diameter_cutting", "motor", "weight"], glance, caps, NOTE)


def t_ls():
    t = manual_table("LS-13P", "pneumatic heavy-duty lock seamer", ["LS-13P"], [
        ("Seaming capacity", "mild steel", ["18 ga (1.2 mm)"]),
        ("Seaming length", ["4.3 ft · 51.2″ (1300 mm)"]),
        ("Seaming Ø (min – max)", ["3.9″ – 5.1″ (100–130 mm)"]),
        ("Working pressure (pneumatic)", ["120 psi (8 bar)"]),
        ("Press force", ["220 lbf (100 kgf)"]),
        ("Motor power", ["0.5 HP (0.37 kW)"]),
        ("Dimensions L × W × H", ["68 × 35 × 65″ (1730 × 890 × 1650 mm)"]),
        ("Weight", ["661 lb (300 kg)"]),
    ], key_labels=("Seaming capacity", "Seaming length"))
    glance = {"LS-13P": ["seams to 51.2″ (1300 mm)", "18 ga (1.2 mm)", "—", "0.5 HP", "661 lb"]}
    caps = {"LS-13P": "closes lock seams to 18 ga (1.2 mm) · 51.2″ (1300 mm) long · Ø3.9–5.1″ pipe"}
    return manual_spec([t], ["cutting_diameter", "cutting_capacity", "inside_diameter_cutting", "motor", "weight"], glance, caps,
                       "Seaming capacity is for mild steel; the metric values in brackets are the manufacturer's nominal figures.")


FAMILIES = [
    dict(id="isitan-idk", group="circle", page=SLUG,
         name="IDK circle cutting machines — hydraulic, motorized and manual circle shears",
         short="IDK circle cutters",
         models_label="IDK-5 · IDK-3.5 · IDK-2 · IDK-1.8 · IDK-1",
         summary="Circle cutting shears cut round blanks — and on the IDK-5, 3.5 and 2 also inside diameters (rings) — from sheet clamped at "
                 "its centre and rotated between two circular blades. The IDK-5 is the production machine: hydraulic centre clamp, "
                 "motorized cutting-diameter adjustment, discs up to 78.7″ in 3/16″ steel and an optional flanging attachment that turns "
                 "the edge of the disc up to 3/8″ for tank heads. The IDK-3.5 adds a pneumatic clamp to a 47″ machine, the IDK-2 and "
                 "IDK-1.8 are rigid cast-frame motorized cutters for 14 ga, and the IDK-1 is the hand-operated bench model.",
         features=["IDK-5: welded steel frame, hydraulic centre clamp, motorized cutting-diameter adjustment, inside-diameter cutting, mobile control panel",
                   "IDK-3.5: pneumatic centre clamp (116 psi air supply), motorized diameter adjustment, inside-diameter cutting",
                   "IDK-2: rigid cast frame, blades in bearings, foot pedal, inside-diameter cutting", "IDK-1.8: rigid cast frame, blades in bronze bushings, foot pedal",
                   "Special-steel (1.2379) blades; shafts on conical bearings for long blade life; gearbox motor with brake", "Built to EC safety directives (CE)"],
         optional=["IDK-5: flanging attachment for edge flanging up to 3/8″; digital readout", "IDK-2: pneumatic sheet-centring device", VOLT],
         images=["is-idk-5", "is-idk-35", "is-idk-2", "is-idk-18", "is-idk-1", "is-idk-5-clamp", "is-idk-5-flanging"],
         videos=[], specs=t_idk(),
         headline="Discs Ø4.3″ – 78.7″ (110–2000 mm) · sheet to 3/16″ (5 mm) · inside-diameter cutting"),
    dict(id="isitan-ls-13p", group="circle", page=SLUG,
         name="LS-13P pneumatic heavy-duty lock seaming machine",
         short="LS-13P lock seamer",
         models_label="LS-13P",
         summary="A motorized lock seamer that closes the longitudinal lock seam of round ducts and pipes: a gearbox-driven pinching system "
                 "with pneumatic pressing, hardened seaming rolls on a ball-bearing slide, and pinching and rotation controlled from the "
                 "foot pedal. Seams up to 51″ long in 18 ga sheet on pipes of 3.9″ to 5.1″ diameter — the companion to the slip roll and "
                 "the bead roller in the HVAC shop.",
         features=["Gearbox-driven pinching system; pneumatic pressing for easy operation", "Pinching and rotation controlled by the standard foot pedal",
                   "Hardened seaming rolls; sliding system on ball bearings", "Pneumatic system protected by air filter", "Operator's manual"],
         optional=[VOLT],
         images=["is-ls-13p", "is-ls-13p-profile", "is-ls-13p-seam"],
         videos=[], specs=t_ls(),
         headline="Lock seams to 51.2″ (1300 mm) in 18 ga (1.2 mm) · pipe Ø3.9–5.1″"),
]

PAGE = dict(
    title="Circle Shears, Flanging Machines & Lock Seamers | NovoTech",
    meta="Circle shears cutting discs and rings to Ø78.7″ in 3/16″ plate, tank-head cutting and flanging machines for dished and elliptical heads to Ø15 ft, and a pneumatic lock seamer.",
    h1="Circle cutting machines, flanging machines and lock seamers",
    intro="Circle cutting machines (circle shears, circle cutters) cut round blanks and rings from sheet for tank heads, fan housings, flanges, lids and gaskets; a flanging machine then turns the edge of the disc up for a dished or flat tank head. İşitan's IDK series runs from the hand-operated IDK-1 to the hydraulic IDK-5 cutting 78.7″ discs in 3/16″ steel, and the LS-13P lock seaming machine closes the longitudinal seam of round ducts. Şahinler's SDK 6 and SDK 8 cut and flange dished heads up to Ø15 ft in 5/16″ plate on the same head, and the EFM 6 does the same for elliptical heads. Sold with CSA-approved panels and supported from Mississauga, ON.",
    points=["IDK-5: discs to Ø78.7″ (2000 mm) in 3/16″ steel, hydraulic clamp, flanging option", "SDK 6 / SDK 8: cut and flange tank heads Ø21.7″ to Ø15 ft in 5/16″ plate; EFM 6 for elliptical heads", "LS-13P pneumatic lock seamer — 51″ seams in 18 ga"],
    hero="is-idk-5", minis=["sh-sdk8", "is-ls-13p"],
    groups=[("circle", "İşitan circle cutters and lock seamer", "Five circle cutting shears from manual to hydraulic, and the pneumatic lock seaming machine.", "isitan"),
            ("sahinler-circle", "Şahinler tank-head cutting and flanging machines", "SDK 6 and SDK 8 circular cutting and flanging machines to Ø15 ft, and the EFM 6 elliptical machine.", "sahinler")],
    faq=[{"q": "How does a circle cutting machine work?", "a": "The sheet is clamped at its centre on a spindle and turned by hand or motor while two rotary blades shear a circle at the radius set on the arm. On the IDK-5, 3.5 and 2 a second pass at a smaller radius cuts the inside diameter, leaving a ring; the blank can then be flanged on the IDK-5's optional attachment."},
         {"q": "What size and thickness can be cut?", "a": "From Ø4.3″ up to Ø78.7″ (2 m) depending on the model, in mild steel from 20 ga on the manual IDK-1 to 3/16″ on the hydraulic IDK-5. Stainless steel reduces the capacity by roughly one gauge; ask us for the model that suits your material."},
         {"q": "Hydraulic, pneumatic or manual clamp?", "a": "The centre clamp holds the sheet on the spindle while it rotates. The IDK-5 clamps hydraulically and the IDK-3.5 pneumatically (116 psi shop air) — fast and consistent for production; the IDK-2, 1.8 and 1 clamp by hand screw, which is fine for a few parts at a time."},
         {"q": "How does a tank-head flanging machine work?", "a": "The plate disc is clamped on the part carrier and rotated while a top and bottom flanging roll, driven through planetary gearboxes, turn its edge up to the radius of the roll set — R1″ as supplied, other radii optional. On the SDK 6 and SDK 8 the same head first cuts the disc from the square plate with rotary blades, so a dished or flat head is cut and flanged without moving it; hydraulic lateral supports hold large heads and the LCD touchscreen runs the cycle."},
         {"q": "What does the LS-13P lock seamer do?", "a": "After a sheet is rolled into a pipe on a slip roll with a Pittsburgh or snap lock profile, the LS-13P closes the longitudinal seam: the pneumatic rolls pinch the lock over the full 51″ length while the pipe is rotated with the foot pedal, giving a tight, straight seam on 3.9–5.1″ ducts in 18 ga."},
         VOLT_FAQ_GENERIC],
)


ALL_FAMILIES = FAMILIES + CIRCLE_FAMILIES


def build():
    write_families(SET, ALL_FAMILIES)
    write_category(SLUG, PAGE, ALL_FAMILIES, SET, SECTION,
                   extra={"nav_label": "Circle cutters & flangers", "catalogue_pdf": None, "catalogue_pdfs": [PDF, PDF_SH],
                          "hero_brand_line": "İşitan circle cutters and Şahinler flanging machines are made in Turkey — İşitan Makine since 1959, Şahinler Metal since 1976 — with European components. Sold, installed and supported in Canada by NovoTech.",
                          "origin_feature": {"title": "Made in Turkey by İşitan and Şahinler", "text": "İşitan has built sheet-metal machinery in Bursa since 1959 and Şahinler Metal tank-head machinery since 1976 — CE-certified machines with European components."},
                          "related_pages": [{"href": "hydraulic-4-roll-plate-rollers.html", "label": "Hydraulic 4-roll plate rollers"}, {"href": "bead-rollers.html", "label": "Bead rollers"}, {"href": "slip-rolls.html", "label": "Slip rolls"}, {"href": "plate-rollers.html", "label": "Plate rollers & slip rolls"}]})
    return IMAGES
