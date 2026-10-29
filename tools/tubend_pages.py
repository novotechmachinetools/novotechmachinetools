#!/usr/bin/env python3
"""HP horizontal presses, TB pipe benders and WP welding positioners made in Bursa, Turkey — all sold as NovoTech's premium line,
made in Turkey, with the maker's logo removed from the photos (tools/tubend_photos.LOGO), the
texts and their own brochure (Oct 2026).  Page texts for horizontal-press-brake (HP 10 – HP 150) and
welding-positioners (WP 100 / WP 300), the TB group for the rotary draw page, image registration (section 'tubend'), and the
NovoTech-format brochure spec:

    python3 tools/tubend_photos.py                   # tubend.com.tr cut-outs, brochure / catalogue images → tools/src-images/tubend
    python3 tools/tubend_pages.py                    # image_map entries (tools/tubend_keys.txt), the two pages, brochure spec
    python3 tools/isitan_data.py                     # writes rotary-draw-tube-benders with the TB group (pipe-benders hub)
    python3 tools/make_images.py --only $(cat tools/tubend_keys.txt)
    python3 tools/brochure/build_brochure.py tools/brochure/specs/pipe-benders-welding-positioners.json

The HP and WP families live in the 'tubend' family set; TB 34 / TB 42 in 'tube-benders' (tools/isitan_tube_benders.py).
"""
import json
import os

from isitan_lib import write_category, write_families
import tubend_data as D
import tubend_photos as PH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "tubend"
BRAND = D.BRAND
PDF_FILE = "files/NovoTech-Pipe-Benders-Welding-Positioners-2026.pdf"          # TB / WP: NovoTech premium line, no maker's name (Oct 28 2026)
PDF_LABEL = "Download the NovoTech pipe bender & welding positioner brochure"
PDF_HP_FILE = "files/NovoTech-Horizontal-Press-Brakes-2026.pdf"          # the HP presses: NovoTech premium line, no maker's name (Oct 2026)
PDF_HP_LABEL = "Download the NovoTech horizontal press brake brochure"
HP_BRAND_LINE = ("The HP horizontal presses are built in Turkey for NovoTech's premium line, with European hydraulics and controls. Sold, "
                 "installed and supported in Canada by NovoTech.")
HP_ORIGIN = {"title": "Made in Turkey for NovoTech", "text": "NovoTech's premium-line horizontal presses are built in Turkey to our specification — welded "
             "steel frames, hardened tools and touch-screen controls — with a CSA-approved panel, a 1-year warranty and parts and technicians in Mississauga, ON, Canada."}

BRAND_LINE = ("The TB pipe benders and WP welding positioners are built in Turkey for NovoTech's premium line, with European components. Sold, "
              "installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Turkey for NovoTech", "text": "NovoTech's premium-line pipe benders and welding positioners are built in Turkey to our "
          "specification — welded steel frames, hardened dies and simple, robust controls — with a 1-year warranty and parts and technicians in Mississauga, ON, Canada."}
NO_FACTORY_VIDEO = {"intro_video": None}


def pdf(fid=None):
    file, label = (PDF_HP_FILE, PDF_HP_LABEL) if fid in ("tubend-hp", "tubend-hp-heavy") else (PDF_FILE, PDF_LABEL)
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": label, "size": size}


def families(page=None):
    """Tubend families with the brochure attached, optionally only those of one page."""
    return [dict(f, pdf=pdf(f["id"])) for f in D.FAMILIES if page is None or f["page"] == page]


VOLT_FAQ_HP = {"q": "What power supply does an HP press need?",
               "a": "Three-phase: the HP presses are supplied for 600 V with a CSA-approved panel as standard, and for 208 V, 240 V or 480 V "
                    "3-phase on request. Motors run from 1.5 HP on the HP 10 to 15 HP on the HP 100 and 10 HP on the HP 150."}

# ------------------------------------------------------------------------------------------------ horizontal-press-brake
PAGE_HP = dict(
    title="Horizontal Press Brakes, Hydraulic, 11 – 165 Ton | NovoTech",
    meta="NC hydraulic horizontal presses that bend, punch, shear and straighten flat bar, pipe, bar and busbar: NovoTech premium-line HP 10 to HP 150, made in Turkey, with touch-screen recipes.",
    h1="Horizontal press brakes — NC hydraulic horizontal presses, 11 to 165 US tons",
    intro="A horizontal press brake is a hydraulic press laid on its side: the ram pushes the tool across a heavy steel table at bench "
          "height, so flat bar, angle, channel, pipe, solid bar and busbar lie flat in front of the operator while they are bent, "
          "punched, sheared, notched or straightened. With the right tooling one machine does the work of a small press brake, a bar "
          "bender, a heavy-wall pipe bender, a punch and a straightening press — the workhorse of maintenance and repair shops, gate, "
          "railing and fence makers, trailer and agricultural fabricators and the switchgear builders who bend copper busbar. NovoTech "
          "sells the HP series, built in Turkey for its premium line: six NC-controlled models from the 11-ton HP 10 to the 110-ton HP 100, "
          "and the 132- and 165-ton HP 120 and HP 150 with a T-slot table and hardened support columns for straightening heavy "
          "sections. Every HP has a touch-screen control stand with manual, automatic and recipe modes and a foot pedal; a servo NC "
          "back gauge, a library of bending, punching, shearing, pipe and busbar tools and dies made for your part are available. "
          "Installed, trained and supported from Mississauga, ON, Canada.",
    points=["HP 10 – HP 100: 11 – 110 US tons · flat bar from 5-7/8″ × 1/4″ to 11-13/16″ × 15/16″",
            "HP 120 · HP 150: 132 – 165 US tons · 19.7″ stroke · T-slot table and hardened support columns",
            "Touch-screen NC with manual, automatic and recipe modes · servo NC back gauge · bending, punching, pipe and busbar tools"],
    hero="tb-hp80", minis=["tb-hp10", "tb-hp120"],
    groups=[("tubend-hp", "HP hydraulic horizontal presses · premium line",
             "NC-controlled horizontal presses from 11 to 165 US tons, small to large: the HP 10 – HP 100 on one frame design, and the "
             "HP 120 and HP 150 with a T-slot table and support columns for heavy bending and straightening.", "novotech-premium")],
    faq=[{"q": "What is a horizontal press brake used for?",
          "a": "Bending, punching, shearing, notching and straightening bar stock with the part lying flat on a table at bench height. "
               "The ram moves horizontally, so long parts rest on the table and the operator watches the bend from the side. With its "
               "tooling one HP replaces a small press brake for flat bar, a bar and pipe bender, a punch and a straightening press: "
               "brackets and clamps, U-bolts and hooks, gate and railing parts, pipe saddles and offsets, reduced and expanded pipe ends, "
               "bent and punched copper busbar."},
         {"q": "Which HP size do I need?",
          "a": "Size the press by the heaviest flat bar you bend the hard way in mild steel: HP 10 – 5-7/8″ × 1/4″, HP 20 – 7-7/8″ × 3/8″, "
               "HP 40 – 9-7/8″ × 5/8″, HP 60 – 11-13/16″ × 5/8″, HP 80 – 11-13/16″ × 13/16″, HP 100 – 11-13/16″ × 15/16″, HP 120 and "
               "HP 150 – 19-11/16″ × 1-3/16″ and 1-9/16″. Punching takes the most force: a Ø13/16″ hole in 1/2″ mild steel needs about "
               "32 US tons, so an HP 40 or larger. Stainless steel needs about 1.5 times the force of mild steel."},
         {"q": "How does the NC control work?",
          "a": "On the touch-screen of the control stand. In manual mode the ram works between the minimum and maximum stroke you set, "
               "while the pedal is pressed — for setting up and single parts. The automatic modes repeat the stroke cycle by cycle for "
               "series parts. In recipe mode a part with several operations is stored as a list of positions and run step by step; "
               "recipes are saved and reloaded for the next batch."},
         {"q": "What does the automatic back gauge add?",
          "a": "A servo-driven NC back gauge, 3.3, 6.6 or 9.8 ft (1, 2 or 3 m) long, positions the part for every step of a recipe, so "
               "parts with several bends or holes at set distances come off faster and more repeatably than with a manual stop. Its "
               "pull-back retracts the stop while the part bends, so a part that swings against the gauge during the bend is not "
               "pushed off position."},
         {"q": "Which tools are available?",
          "a": "Bending tools — radius punch with V-die, press brake punch and bolt punch with multi-V dies, narrow V-die, two-sided V and "
               "spring-loaded U-bending tools, profile and round bar bending tools; pipe tools — mandrel-less pipe bending, solid bar and "
               "thick-wall pipe bending, pipe end reduction and expansion, pipe clamping and pipe notching; wide-radius bending, "
               "straightening, punching and shearing tools; and busbar tools for shearing, punching, precision, vertical and Z-bending, "
               "corner notching and twisting. Dies are also designed and made for your part — send us the drawing."},
         {"q": "Can an HP bend busbar?",
          "a": "Yes — with the busbar tools the HP shears, punches, bends flat and on edge, Z-bends, corner-notches and twists copper and "
               "aluminum busbar for switchgear, panel and battery builders, and the recipe mode repeats a busbar with several operations "
               "the same way every time."},
         VOLT_FAQ_HP],
    faq_title="Questions we get asked about horizontal press brakes",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "hydraulic-press-brake.html", "label": "Hydraulic press brakes"},
                   {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}, {"href": "hydraulic-press.html", "label": "Hydraulic presses"},
                   {"href": "pipe-benders.html", "label": "Pipe & tube benders"}],
    related_title="More bending and forming machinery from NovoTech",
)

# ------------------------------------------------------------------------------------------------ welding-positioners
PAGE_WP = dict(
    title="Welding Positioners, Tilting, 220 – 661 lb | NovoTech",
    meta="Tilting welding positioners that turn the part under the torch at 1 – 5.5 rpm: NovoTech premium-line WP 100 and WP 300, 120° or 90° tilt, foot pedal, single-phase power.",
    h1="Welding positioners — tilting turntables for round welds, 220 to 661 lb",
    intro="A welding positioner holds the part on a turntable and turns it under the torch at a steady, adjustable speed, so a round "
          "weld on a flange, pipe-to-plate joint, hub, tank head or wheel is laid in one continuous pass in the flat position — no "
          "stopping, repositioning and restarting around the part, and a more even bead whether the torch is held by hand or clamped "
          "in a holder. Tilting the table brings the joint to the best angle for the torch. NovoTech's premium-line WP 100 and WP 300 are "
          "built in Turkey: the WP 100 carries 220 lb on a Ø13-3/4″ table that tilts 120°, the WP 300 661 lb on a Ø18-7/8″ table "
          "that tilts 90°. Both turn 360° at 1 to 5.5 rpm, set on the control box and run from the standard foot pedal, with T-slots for "
          "clamps and fixtures, an optional 3-jaw lathe chuck and, on the WP 300, a custom fixture plate. They run on single-phase "
          "220 V. Supplied and supported from Mississauga, ON, Canada.",
    points=["WP 100: 220 lb on a Ø13-3/4″ table, 120° tilt · WP 300: 661 lb on a Ø18-7/8″ table, 90° tilt",
            "360° rotation at 1 – 5.5 rpm, variable · foot pedal standard · single-phase 220 V",
            "T-slotted turntable · optional Ø6-1/4″ or Ø7-7/8″ 3-jaw chuck · custom fixture plate (WP 300)"],
    hero="tb-wp300", minis=["tb-wp100", "tb-wp300-plate"],
    groups=[("tubend-wp", "WP tilting welding positioners · premium line",
             "Two tilting positioners with variable-speed rotation for MIG, TIG and stick welding of round joints — on the bench or the floor.", "novotech-premium")],
    faq=[{"q": "What does a welding positioner do?",
          "a": "It turns the part under a stationary torch at a set speed, so a circumferential weld is made in one pass in the flat "
               "position — the easiest position to weld and the one that gives the most even bead. The welder no longer walks around "
               "the part or stops to reposition it; with the torch in a holder the travel speed is as steady as the table, which makes "
               "repeat parts faster and more uniform."},
         {"q": "WP 100 or WP 300?",
          "a": "By the weight and size of the part. The WP 100 carries 220 lb on its Ø13-3/4″ table (110 lb with the table tilted) and "
               "tilts to 120°; the WP 300 carries 661 lb on a Ø18-7/8″ table (331 lb tilted) and tilts to 90°. The ratings are for a "
               "part centred on the table: a part whose centre of gravity sits off the table or far above it loads the drive more, so "
               "leave margin for long or overhanging parts."},
         {"q": "How fast should the table turn?",
          "a": "Table speed (rpm) = travel speed ÷ (π × weld diameter). Across the WP's 1 – 5.5 rpm, a weld on Ø4″ pipe passes the torch at "
               "about 12.6 to 69 in/min and one on a Ø8″ flange at 25 to 138 in/min; set the speed on the control box for the process, "
               "wire and joint, and run the table from the foot pedal."},
         {"q": "What can be mounted on the turntable?",
          "a": "The table is T-slotted (M10) for clamps, angle plates and fixtures. A 3-jaw lathe chuck of Ø6-1/4″ or Ø7-7/8″ (160 or "
               "200 mm) holds pipe, shafts and round parts; the WP 300 also takes a custom perforated work plate for welding fixtures."},
         {"q": "What power do they need?",
          "a": "Single-phase 220 V — no three-phase supply is needed. The turntable motors are 0.33 HP (WP 100) and 0.5 HP (WP 300), and "
               "the foot pedal is standard."}],
    faq_title="Questions we get asked about welding positioners",
    related_pages=[{"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "plate-beveler.html", "label": "Plate bevelers"},
                   {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}, {"href": "horizontal-press-brake.html", "label": "Horizontal press brakes"},
                   {"href": "pipe-benders.html", "label": "Pipe & tube benders"}],
    related_title="More fabrication machinery from NovoTech",
)

# ------------------------------------------------------------------------------------------------ group on the rotary draw page
TB_GROUP = ("tubend-tb", "TB mandrel-less pipe benders · premium line",
            "An electric bench bender for 1″ NPS pipe and a 17-ton hydraulic bender for 1-1/4″ NPS — simple, low-cost benders for railing, "
            "barrier, furniture and repair work, built in Turkey for NovoTech's premium line.", "novotech-premium")

# ------------------------------------------------------------------------------------------------ brochure
ABOUT_TB = ("NovoTech sells, installs and supports its premium-line pipe benders and welding positioners in Canada from Mississauga, Ontario, Canada — "
            "dies chosen for your parts, installation, operator training, a CSA-approved panel on three-phase machines, a 1-year warranty and parts "
            "and technical support in Canada.")
BROCHURE = dict(
    title="Pipe benders and welding positioners",
    subtitle="TB 34 / TB 42 mandrel-less pipe benders · WP 100 / WP 300 tilting welding positioners",
    cover_line="NovoTech premium line · made in Turkey · sold & serviced in Canada by NovoTech", range_label="Pipe benders and welding positioners", about_for="pipe benders and welding positioners",
    about_kicker="NovoTech premium line · made in Turkey", about_title="Simple, solid machines for the pipe and welding shop",
    about_text=["NovoTech's premium-line pipe benders and welding positioners are built in Turkey to our specification. The TB 34 and TB 42 are simple "
                "mandrel-less pipe benders with a digital angle readout and a brake motor that holds the bend, and the WP 100 and WP 300 tilting "
                "welding positioners turn round parts under the torch at 1 – 5.5 rpm, foot-pedal controlled.", ABOUT_TB],
    country="Turkey", families=["tubend-tb34", "tubend-tb42", "tubend-wp"], family_sets=["tubend", "tube-benders"],
    groups=[{"title": "Mandrel-less pipe benders", "families": ["tubend-tb34", "tubend-tb42"]},
            {"title": "Welding positioners", "families": ["tubend-wp"]}],
    cover_photos=["tb-tb42", "tb-wp300"], out="src/" + PDF_FILE)

ABOUT_HP = ("NovoTech sells, installs and supports the HP presses in Canada from Mississauga, Ontario, Canada — tooling chosen for your parts, "
            "installation, operator training, a CSA-approved panel, a 1-year warranty and parts and technical support in Canada.")
BROCHURE_HP = dict(
    title="Horizontal press brakes",
    subtitle="HP 10 – HP 150 NC hydraulic horizontal presses, 11 – 165 US tons — bend, punch, shear and straighten flat bar, pipe, bar and busbar",
    cover_line="NovoTech premium line · made in Turkey · sold & serviced in Canada by NovoTech", range_label="Horizontal press brakes", about_for="horizontal press brakes",
    about_kicker="NovoTech premium line · made in Turkey", about_title="Horizontal presses with a tool for every bend",
    about_text=["NovoTech's premium-line HP horizontal presses are built in Turkey to our specification. They bend, punch, shear, notch "
                "and straighten flat bar, pipe, solid bar and busbar with the part lying flat on the table — NC-controlled from 11 to 165 "
                "US tons, with a touch-screen recipe control, an optional servo back gauge and an extensive library of bending, punching, "
                "shearing, pipe and busbar tools; the HP 120 and HP 150 add a T-slot table and hardened support columns for straightening "
                "heavy sections.", ABOUT_HP],
    country="Turkey", families=["tubend-hp", "tubend-hp-heavy"], family_sets=["tubend"],
    groups=[{"title": "NC hydraulic horizontal presses", "families": ["tubend-hp"]},
            {"title": "Heavy-duty horizontal presses", "families": ["tubend-hp-heavy"]}],
    cover_photos=["tb-hp80", "tb-hp10", "tb-hp120"], out="src/" + PDF_HP_FILE)


def write_brochure_specs():
    d = os.path.join(ROOT, "tools", "brochure", "specs")
    spec = dict(BROCHURE, single_phase=False, year="2026", made_in="Made in Turkey for NovoTech's premium line — with European components")
    json.dump(spec, open(os.path.join(d, "pipe-benders-welding-positioners.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    old = os.path.join(d, "tubend.json")
    if os.path.exists(old):
        os.remove(old)
    spec = dict(BROCHURE_HP, single_phase=False, year="2026", made_in="Made in Turkey for NovoTech's premium line — with European hydraulics and controls")
    json.dump(spec, open(os.path.join(d, "horizontal-press-brakes.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "tubend")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/tubend/{key}{ext}", "alt": p["alt"], "section": "tubend", "trim": False, "quality": 82,
                     "cutout": bool(p.get("cutout"))}
        keys.append(key)
    imap.pop("tubend-logo", None)        # the maker's logo is no longer shown anywhere (Oct 28 2026)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "tubend_keys.txt"), "w").write(",".join(keys))
    return keys


def video_ids():
    return list(dict.fromkeys(v["id"] for f in D.FAMILIES for v in f["videos"]))


def build():
    fams = families(D.P_HP) + families(D.P_WP)
    write_families(SET, fams)
    shared = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **NO_FACTORY_VIDEO, "catalogue_pdf": pdf(), "catalogue_pdfs": None}
    write_category(D.P_HP, PAGE_HP, fams, SET, "Horizontal press brakes", extra={**shared, "hero_brand_line": HP_BRAND_LINE, "origin_feature": HP_ORIGIN,
                                                                                   "catalogue_pdf": pdf("tubend-hp"), "nav_label": "Horizontal press brakes"})
    write_category(D.P_WP, PAGE_WP, fams, SET, "Welding positioners", extra={**shared, "nav_label": "Welding positioners"})
    keys = register_images()
    write_brochure_specs()
    used = {k for f in D.FAMILIES for k in f["images"]} | {PAGE_HP["hero"], PAGE_WP["hero"]} | set(PAGE_HP["minis"]) | set(PAGE_WP["minis"])
    used |= set(BROCHURE["cover_photos"]) | set(BROCHURE_HP["cover_photos"])
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        print("!! image keys without a photo:", missing)
    for t, p in (("hp", PAGE_HP), ("wp", PAGE_WP)):
        print(f"{t}: title {len(p['title'])} · meta {len(p['meta'])}")
    print(f"tubend: {len(D.FAMILIES)} families · {sum(len(f['specs']['models']) for f in D.FAMILIES)} models · images: {len(keys)} · videos: {len(video_ids())}")


if __name__ == "__main__":
    build()
