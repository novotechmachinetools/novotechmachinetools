"""ISITAN section: circle cutting machines (catalogue pages 32–33) — one category page; the LS-13P lock seamer moved to the bead-roller page (Oct 2026)."""
from isitan_lib import *  # noqa: F401,F403
from sahinler_families import CIRCLE_FAMILIES  # SDK / EFM tank-head machines below the ISITAN group
from sahinler_lib import PDF as PDF_SH

SET = "circle-cutting"
SECTION = "Circle cutters & flangers"
SLUG = "circle-cutters-and-seamers"

IMAGES = {
    "is-idk-5": ("img/ISITAN-IDK-5.jpg", "ISITAN IDK-5 hydraulic circle cutting and flanging machine — discs up to 78.7″ in 3/16″ sheet"),
    "is-idk-5-clamp": ("cut/p32-190.png", "IDK-5 — hydraulic clamping and cutting system"),
    "is-idk-5-flanging": ("cut/p32-192.png", "IDK-5 — optional flanging attachment for edge flanging up to 3/8″"),
    "is-idk-35": ("img/ISITAN-IDK-35.jpg", "ISITAN IDK-3.5 motorized circle cutting shear with pneumatic centre clamp"),
    "is-idk-2": ("img/ISITAN-IDK-2.jpg", "ISITAN IDK-2 heavy-duty motorized circle cutting machine"),
    "is-idk-18": ("img/ISITAN-IDK-18.jpg", "ISITAN IDK-1.8 motorized circle cutter with foot pedal"),
}

NOTE = "Cutting capacities are for mild steel; thin sheet is given in gauge with the manufacturer's nominal metric value in brackets. Dimensions are overall L × W × H."


def t_idk():
    t = manual_table("IDK series", "4 models · circles Ø4.3″ – 78.7″", ["IDK-5", "IDK-3.5", "IDK-2", "IDK-1.8"], [
        ("Min. cutting Ø", ["9.8″ (250 mm)", "7.9″ (200 mm)", "4.7″ (120 mm)", "4.3″ (110 mm)"]),
        ("Max. cutting Ø", ["78.7″ (2000 mm)", "47.2″ (1200 mm)", "39.4″ (1000 mm)", "39.4″ (1000 mm)"]),
        ("Cutting capacity", "mild steel", ["3/16″ (5 mm)", "10 ga (3.5 mm)", "14 ga (2 mm)", "14 ga (2 mm)"]),
        ("Cutting speed", ["13 ft/min (4 m/min)", "20 ft/min (6 m/min)", "25 ft/min (7.5 m/min)", "25 ft/min (7.5 m/min)"]),
        ("Blade material", ["1.2379 tool steel", "1.2379 tool steel", "1.2379 tool steel", "1.2379 tool steel"]),
        ("Motor power", ["3 + 1 HP (2.2 + 0.75 kW)", "3 HP (2.2 kW)", "1.5 HP (1.1 kW)", "1.5 HP (1.1 kW)"]),
        ("Hump depth", ["47.2″ (1200 mm)", "29.5″ (750 mm)", "27.6″ (700 mm)", "24.0″ (610 mm)"]),
        ("Throat depth", ["11.8″ (300 mm)", "9.8″ (250 mm)", "11.0″ (280 mm)", "8.5″ (215 mm)"]),
        ("Inside-diameter cutting", ["Yes", "Yes", "Yes", "No"]),
        ("Centre clamp", ["Hydraulic", "Pneumatic (116 psi air)", "Manual", "Manual"]),
        ("Dimensions L × W × H", ["118 × 30 × 55″ (3000 × 760 × 1400 mm)", "79 × 24 × 55″ (2000 × 610 × 1400 mm)", "55 × 16 × 51″ (1400 × 410 × 1300 mm)", "59 × 16 × 51″ (1500 × 410 × 1300 mm)"]),
        ("Weight", ["2,976 lb (1,350 kg)", "1,653 lb (750 kg)", "772 lb (350 kg)", "529 lb (240 kg)"]),
    ], key_labels=("Cutting capacity", "Max. cutting"))
    glance = {"IDK-5": ["9.8″ – 78.7″ (250–2000 mm)", "3/16″ (5 mm)", "Yes", "3 + 1 HP", "2,976 lb"],
              "IDK-3.5": ["7.9″ – 47.2″ (200–1200 mm)", "10 ga (3.5 mm)", "Yes", "3 HP", "1,653 lb"],
              "IDK-2": ["4.7″ – 39.4″ (120–1000 mm)", "14 ga (2 mm)", "Yes", "1.5 HP", "772 lb"],
              "IDK-1.8": ["4.3″ – 39.4″ (110–1000 mm)", "14 ga (2 mm)", "No", "1.5 HP", "529 lb"]}
    caps = {"IDK-5": "cuts discs to Ø78.7″ (2000 mm) in 3/16″ (5 mm) · hydraulic clamp", "IDK-3.5": "cuts discs to Ø47.2″ (1200 mm) in 10 ga · pneumatic clamp",
            "IDK-2": "cuts discs to Ø39.4″ (1000 mm) in 14 ga · heavy-duty cast frame", "IDK-1.8": "cuts discs to Ø39.4″ (1000 mm) in 14 ga · foot pedal"}
    return manual_spec([t], ["cutting_diameter", "cutting_capacity", "inside_diameter_cutting", "motor", "weight"], glance, caps, NOTE)


FAMILIES = [
    dict(id="isitan-idk", group="circle", page=SLUG,
         name="IDK circle cutting machines — hydraulic and motorized circle shears",
         short="IDK circle cutters",
         models_label="IDK-5 · IDK-3.5 · IDK-2 · IDK-1.8",
         summary="Circle cutting shears cut round blanks — and on the IDK-5, 3.5 and 2 also inside diameters (rings) — from sheet clamped at "
                 "its centre and rotated between two circular blades. The IDK-5 is the production machine: hydraulic centre clamp, "
                 "motorized cutting-diameter adjustment, discs up to 78.7″ in 3/16″ steel and an optional flanging attachment that turns "
                 "the edge of the disc up to 3/8″ for tank heads. The IDK-3.5 adds a pneumatic clamp to a 47″ machine, the IDK-2 and "
                 "IDK-1.8 are rigid cast-frame motorized cutters for 14 ga sheet with foot-pedal control.",
         features=["IDK-5: welded steel frame, hydraulic centre clamp, motorized cutting-diameter adjustment, inside-diameter cutting, mobile control panel",
                   "IDK-3.5: pneumatic centre clamp (116 psi air supply), motorized diameter adjustment, inside-diameter cutting",
                   "IDK-2: rigid cast frame, blades in bearings, foot pedal, inside-diameter cutting", "IDK-1.8: rigid cast frame, blades in bronze bushings, foot pedal",
                   "Special-steel (1.2379) blades; shafts on conical bearings for long blade life; gearbox motor with brake", "Built to EC safety directives (CE)"],
         optional=["IDK-5: flanging attachment for edge flanging up to 3/8″; digital readout", "IDK-2: pneumatic sheet-centring device", VOLT],
         images=["is-idk-5", "is-idk-35", "is-idk-2", "is-idk-18", "is-idk-5-clamp", "is-idk-5-flanging"],
         videos=[], specs=t_idk(),
         headline="Discs Ø4.3″ – 78.7″ (110–2000 mm) · sheet to 3/16″ (5 mm) · inside-diameter cutting"),

]

PAGE = dict(
    title="Circle Shears & Flanging Machines | NovoTech",
    meta="Circle shears cutting discs and rings to Ø78.7″ in 3/16″ plate, and tank-head cutting and flanging machines for dished and elliptical heads to Ø15 ft. Made in Turkey, sold and supported in Canada.",
    h1="Circle cutting machines and flanging machines",
    intro="Circle cutting machines (circle shears, circle cutters) cut round blanks and rings from sheet for tank heads, fan housings, flanges, lids and gaskets; a flanging machine then turns the edge of the disc up for a dished or flat tank head. ISITAN's IDK series runs from the motorized IDK-1.8 to the hydraulic IDK-5 cutting 78.7″ discs in 3/16″ steel. The SDK 6 and SDK 8 cut and flange dished heads up to Ø15 ft in 5/16″ plate on the same head, and the EFM 6 does the same for elliptical heads. Sold with CSA-approved panels and supported from Mississauga, ON.",
    points=["IDK-5: discs to Ø78.7″ (2000 mm) in 3/16″ steel, hydraulic clamp, flanging option", "SDK 6 / SDK 8: cut and flange tank heads Ø21.7″ to Ø15 ft in 5/16″ plate; EFM 6 for elliptical heads"],
    hero="is-idk-5", minis=["sh-sdk8", "is-idk-35"],
    groups=[("circle", "ISITAN premium line — circle cutters", "Four circle cutting shears from motorized to hydraulic.", "isitan"),
            ("sahinler-circle", "NovoTech premium line tank-head cutting and flanging machines", "SDK 6 and SDK 8 circular cutting and flanging machines to Ø15 ft, and the EFM 6 elliptical machine.", "sahinler")],
    faq=[{"q": "How does a circle cutting machine work?", "a": "The sheet is clamped at its centre on a spindle and turned by hand or motor while two rotary blades shear a circle at the radius set on the arm. On the IDK-5, 3.5 and 2 a second pass at a smaller radius cuts the inside diameter, leaving a ring; the blank can then be flanged on the IDK-5's optional attachment."},
         {"q": "What size and thickness can be cut?", "a": "From Ø4.3″ up to Ø78.7″ (2 m) depending on the model, in mild steel from 14 ga on the IDK-1.8 and IDK-2 to 3/16″ on the hydraulic IDK-5. Stainless steel reduces the capacity by roughly one gauge; ask us for the model that suits your material."},
         {"q": "Hydraulic, pneumatic or manual clamp?", "a": "The centre clamp holds the sheet on the spindle while it rotates. The IDK-5 clamps hydraulically and the IDK-3.5 pneumatically (116 psi shop air) — fast and consistent for production; the IDK-2 and IDK-1.8 clamp by hand screw, which is fine for a few parts at a time."},
         {"q": "How does a tank-head flanging machine work?", "a": "The plate disc is clamped on the part carrier and rotated while a top and bottom flanging roll, driven through planetary gearboxes, turn its edge up to the radius of the roll set — R1″ as supplied, other radii optional. On the SDK 6 and SDK 8 the same head first cuts the disc from the square plate with rotary blades, so a dished or flat head is cut and flanged without moving it; hydraulic lateral supports hold large heads and the LCD touchscreen runs the cycle."},
         VOLT_FAQ_GENERIC],
)


ALL_FAMILIES = FAMILIES + CIRCLE_FAMILIES


def build():
    write_families(SET, ALL_FAMILIES)
    write_category(SLUG, PAGE, ALL_FAMILIES, SET, SECTION,
                   extra={"nav_label": "Circle cutters & flangers", "catalogue_pdf": None, "catalogue_pdfs": [p for p in (PDF, PDF_SH) if p],
                          "hero_brand_line": "ISITAN circle cutters and NovoTech premium-line flanging machines are made in Turkey — ISITAN Makine since 1959, the NovoTech premium line built to NovoTech's specification — with European components. Sold, installed and supported in Canada by NovoTech.",
                          "origin_feature": {"title": "Made in Turkey — ISITAN and the NovoTech premium line", "text": "ISITAN has built sheet-metal machinery in Bursa since 1959 and the NovoTech premium line tank-head machinery since 1976 — CE-certified machines with European components."},
                          "related_pages": [{"href": "hydraulic-4-roll-plate-rollers.html", "label": "Hydraulic 4-roll plate rollers"}, {"href": "bead-rollers.html", "label": "Bead rollers"}, {"href": "plate-rollers.html", "label": "Plate rollers & slip rolls"}]})
    return IMAGES
