#!/usr/bin/env python3
"""Senfeng Laser pages: the laser-welding-machine page (family set content/families/senfeng.json) and the image_map entries for
every Senfeng photo (section 'senfeng').  The Senfeng sheet lasers, tube lasers and panel benders are appended BELOW the Dener
groups on laser-cutting-machine.html, tube-laser-cutting-machine.html and panel-bender.html by tools/dener_pages.py (which
imports senfeng_data).  Senfeng is sold under its own brand — the value line of the laser section — so the logo stays.

    python3 tools/senfeng_photos.py                     # renders / masked cut-outs → tools/src-images/senfeng
    python3 tools/senfeng_pages.py                      # welding page + image_map entries (tools/senfeng_keys.txt); brochure specs
    python3 tools/dener_pages.py                        # laser / tube / panel pages with the Senfeng groups
    python3 tools/make_images.py --only $(cat tools/senfeng_keys.txt)
    for s in senfeng-sheet-lasers senfeng-tube-lasers senfeng-welding senfeng-panel-benders; do python3 tools/brochure/build_brochure.py tools/brochure/specs/$s.json; done
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import senfeng_data as D
import senfeng_photos as PH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "senfeng"
BRAND = D.BRAND
PDF_LASER = "files/NovoTech-Senfeng-Fiber-Lasers-2026.pdf"
PDF_TUBE = "files/NovoTech-Senfeng-Tube-Lasers-2026.pdf"
PDF_WELD = "files/NovoTech-Senfeng-Laser-Welding-Cladding-2026.pdf"
PDF_PANEL = "files/NovoTech-Senfeng-Panel-Benders-2026.pdf"

BRAND_LINE = ("Senfeng Laser builds fiber laser cutting, welding and cladding machines in Jinan, China — 20 years, 15,000 machines a year, "
              "CE / FDA / ETL certified, with Senfeng Laser USA. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in China by Senfeng Laser", "text": "Senfeng has built fiber laser machines in Jinan since 2004 — a 1.8 million ft² campus, its own laser "
          "sources and cutting heads, 20 overseas branches and a USA warehouse — with NovoTech's CSA panel, warranty and Mississauga, ON support."}
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}


def pdf(file, label):
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": label, "size": size}


PAGE_WELD = dict(
    title="Laser Welding Machines, Handheld & Robotic | NovoTech",
    meta="Senfeng laser welders sold in Canada: portable air-cooled and handheld welders to 3 kW, robotic laser welding cells to 20 kW, cobot MIG welders, laser cladding.",
    h1="Laser welding machines — handheld welders from 0.8 kW, robotic cells to 20 kW, laser cladding",
    intro="A fiber laser welder joins stainless, aluminum, galvanized and mild steel sheet with a narrow, deep seam at five times the speed of TIG, "
          "with almost no heat distortion and no grinding afterwards; handheld, it takes a day to learn, and on a robot it runs the same weld "
          "all shift. NovoTech sells Senfeng laser welding equipment in Canada: the portable air-cooled S series at 0.8 to 1.5 kW on wheels, "
          "the HWM handheld welders at 1.5 to 3 kW with wire feed for joints to 9/32″, robotic laser welding cells from 1.5 to 20 kW with "
          "positioners and tracks, teaching-free and collaborative MIG robots, and the laser cladding machines that rebuild shafts, rolls and "
          "bores with a metallurgically bonded wear layer. Senfeng makes its own sources and heads in Jinan, China; CE / FDA / ETL certified. "
          "Installed and supported from Mississauga, ON.",
    points=["Handheld: S series 0.8 – 1.5 kW air-cooled, 99 – 121 lb · HWM 1.5 – 3 kW, welds to 9/32″, 4-in-1 head",
            "Robotic: RW laser cells 1.5 – 20 kW · RMW teaching-free and CMW cobot MIG welders 350 / 500 A",
            "Cladding: 6 / 12 kW robot cells, lathe-type machines to 20 ft and a portable system for on-site repair"],
    hero="sf-hwm-1", minis=["sf-rw-1", "sf-clad-1"],
    groups=[("weld-handheld", "Handheld laser welders", "The portable S series and the HWM series — one gun that welds, cleans, cuts and seam-welds.", BRAND),
            ("weld-robot", "Robotic welding", "Laser welding cells on 6-axis robots, and MIG robots that program themselves or are hand-guided.", BRAND),
            ("weld-cladding", "Laser cladding", "Wear and corrosion layers on shafts, rolls, cylinders and bores — in the cell, on the lathe or on site.", BRAND)],
    faq=[{"q": "What can a handheld laser welder do that TIG cannot?",
          "a": "Speed and heat. A 1.5 kW laser welds 16 ga stainless at 10 – 15 in/min with a seam that needs no grinding, puts a fraction of the heat into the part — thin sheet, boxes, cabinets and railings stay flat — and welds dissimilar thicknesses, galvanized and aluminum that TIG struggles with. An operator who has never welded produces clean seams after a day of training. It does not replace MIG on heavy plate: the 3 kW HWM welds 9/32″ mild steel in a single pass and the robotic 6 – 20 kW cells go to 9/16″."},
         {"q": "S series or HWM — which handheld welder?",
          "a": "The S series is the portable machine: 0.8, 1.2 or 1.5 kW, air-cooled with no chiller, 99 – 121 lb on wheels and a 220 V single-phase plug — for a shop that moves it between jobs or takes it on site. The HWM is the production welder: 1.5, 2 or 3 kW with a water chiller, a 33 ft cable, a wire feeder and the 4-in-1 head that welds, cleans the weld, cuts sheet and seam-welds — for a station that welds all day and for joints to 9/32″."},
         {"q": "Is it safe to use in a shop?",
          "a": "A class 4 laser needs a controlled area: the welders ship with a CE face shield, laser-resistant gloves and clothing, and the gun fires only with the safety clamp on the workpiece. We recommend the welding booth with laser-protective glass for a fixed station, and fume extraction as for any welding. Operator training is part of the installation."},
         {"q": "When does a robot make sense?",
          "a": "When the same joint is welded hundreds of times a day: tanks, frames, boxes, exhaust, furniture. The RW laser cells run 1.5 to 20 kW on a 6-axis robot with a positioner so the seam is always in position; the CMW cobot is the simplest entry — a 350 or 500 A MIG torch on a collaborative arm, programmed by guiding it by hand over the part, on a cart you wheel to the job; the RMW scans the part with a camera and writes its own program, for batches of one."},
         {"q": "What is laser cladding used for?",
          "a": "Repairing and hardening: worn shafts, hydraulic cylinder rods, rolls, valve seats, pump housings and dies get a new wear- or corrosion-resistant surface — stainless, nickel, cobalt or carbide alloys from powder — fused to the base metal with a thin heat-affected zone, far stronger than thermal spray and with less distortion than overlay welding. Layers to 25/64″ (10 mm), machined afterwards. Mining, oil and gas, hydro, pulp and paper and steel mills are the usual customers."},
         {"q": "What does the machine need on site?",
          "a": "The S series plugs into a 220 V outlet; the HWM, robots and cladding machines run on 3-phase — we supply the transformer for 600 V. Shielding gas (argon or nitrogen), compressed air for the cutting and cleaning modes, a fume extractor, and for the cladding machines a powder supply. Delivery, installation and training by NovoTech from Mississauga."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about laser welders",
    related_pages=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"},
                   {"href": "press-brake.html", "label": "CNC press brakes"}, {"href": "panel-bender.html", "label": "CNC panel benders"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring and edge rounding"}],
    related_title="Machinery that works alongside a laser welder",
)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "senfeng")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/senfeng/{key}{ext}", "alt": p["alt"], "section": "senfeng", "trim": p.get("trim", False), "quality": 82,
                     "cutout": bool(p.get("cutout"))}
        keys.append(key)
    imap["senfeng-logo"] = {"src": "tools/src-images/senfeng-logo.png", "alt": "Senfeng", "section": "site", "trim": False, "quality": 90, "cutout": False}
    keys.append("senfeng-logo")
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "senfeng_keys.txt"), "w").write(",".join(keys))
    return keys


ABOUT_SENFENG = ("Senfeng Laser has built fiber laser machines in Jinan, Shandong, since 2004: a 1.8 million ft² campus, its own laser sources, "
                 "cutting heads and welding guns, around 15,000 machines a year, 20 overseas branches and Senfeng Laser USA with a warehouse "
                 "and service team. CE, FDA and ETL certified. NovoTech sells, installs and supports the machines in Canada from Mississauga, "
                 "Ontario — layout for your building, installation, operator training, a CSA-approved panel, a 1-year warranty and parts and "
                 "technical support in Canada.")
BROCHURES = {
    "senfeng-sheet-lasers": dict(
        title="Fiber laser cutting machines", subtitle="Senfeng sheet lasers · compact, NP open-type, H series with pallet changer, sheet + tube, large-format plate, 3D and coil-fed · 1.5 – 80 kW",
        cover_line="Senfeng Laser · made in China · sold & serviced in Canada by NovoTech", range_label="Senfeng fiber lasers", about_for="Senfeng fiber lasers",
        about_kicker="Senfeng Laser · Jinan, China", about_title="A fiber laser for every shop, from the first 4 × 4 ft machine to 60 kW plate gantries",
        about_text=["A fiber laser cutting machine cuts sheet and plate from a DXF file with a focused beam — mild steel to 2″ and beyond with the high-power sources — at "
                    "speeds no plasma or punch can match, with a clean edge and no tooling. Senfeng's range starts with single-table enclosed machines that ship in one "
                    "container and plug in the day they arrive, and the NP open-type laser that is the lowest-priced 12 kW machine in the catalogue; the H series adds a "
                    "full enclosure and a 20-second pallet changer for production, in 1.5 to 80 kW; the HM cuts sheet and tube on one machine; the R and TX gantries take "
                    "plate to 10 × 164 ft with ±45° bevels; the TD five-axis machine and RC robot cells trim formed parts; and the coil-fed lines cut straight from the "
                    "coil with no sheet handling.", ABOUT_SENFENG],
        country="China", families=[f["id"] for f in D.LASER_FAMILIES], family_sets=["dener"],
        groups=[{"title": "Sheet lasers", "families": ["sf-compact", "sf-np", "sf-h", "sf-hm"]}, {"title": "Plate, 3D and coil-fed lasers", "families": ["sf-r", "sf-3d", "sf-coil"]}],
        cover_photos=["sf-h-1", "sf-np-1", "sf-r-1"], out="src/" + PDF_LASER),
    "senfeng-tube-lasers": dict(
        title="Tube laser cutting machines", subtitle="Senfeng T, PLUS, GT, NT, ST and HT tube and profile fiber lasers · Ø0.5″ to 25″ · 20 to 49 ft · 1.5 to 20 kW",
        cover_line="Senfeng Laser · made in China · sold & serviced in Canada by NovoTech", range_label="Senfeng tube lasers", about_for="Senfeng tube lasers",
        about_kicker="Senfeng Laser · Jinan, China", about_title="Round, square and profile tube cut to length with every hole, cope and notch in one pass",
        about_text=["A tube laser cuts round, square, rectangular and open profiles to length and cuts the holes, copes, slots and notches in them in one pass, straight from "
                    "the 3D model — no saw, no drill, no notcher, no layout. The T series two-chuck machines cover Ø0.5 to 14″ and 20 to 39 ft with 1.5 to 6 kW; the PLUS "
                    "series runs to 492 ft/min on small tube and the GPLUS / GT add a 45° bevel head; the NT three-chuck machines cut the last part without a tail; and the "
                    "ST and HT three- and four-chuck machines carry tube to Ø25″ and 6,600 lb over 29 to 49 ft with 6 to 20 kW sources, for structural steel, towers and "
                    "trailers. Automatic bundle loaders and unloading conveyors are available for every model.", ABOUT_SENFENG],
        country="China", families=[f["id"] for f in D.TUBE_FAMILIES], family_sets=["dener"],
        groups=[{"title": "Two-chuck tube lasers", "families": ["sf-t", "sf-plus"]}, {"title": "Three- and four-chuck tube lasers", "families": ["sf-heavy"]}],
        cover_photos=["sf-t-1", "sf-plus-1", "sf-st-1"], out="src/" + PDF_TUBE),
    "senfeng-welding": dict(
        title="Laser welding and cladding machines", subtitle="Senfeng handheld laser welders 0.8 – 3 kW · robotic laser welding cells 1.5 – 20 kW · cobot MIG welders · laser cladding 6 / 12 kW",
        cover_line="Senfeng Laser · made in China · sold & serviced in Canada by NovoTech", range_label="Senfeng laser welding", about_for="Senfeng laser welding and cladding machines",
        about_kicker="Senfeng Laser · Jinan, China", about_title="Five times faster than TIG, with almost no heat in the part",
        about_text=["A fiber laser welder joins stainless, aluminum, galvanized and mild steel sheet with a narrow, deep seam at five times the speed of TIG, with almost no "
                    "distortion and no grinding afterwards; an operator learns the handheld gun in a day. The portable S series runs 0.8 to 1.5 kW air-cooled from a 220 V "
                    "outlet; the HWM welds to 9/32″ with 1.5 to 3 kW, a wire feeder and a 4-in-1 head; the RW cells put 1.5 to 20 kW on a 6-axis robot with positioners "
                    "and tracks; the CMW cobot and the teaching-free RMW bring MIG robots to shops that have never programmed one. The laser cladding machines rebuild "
                    "shafts, rolls, cylinders and bores with a metallurgically bonded wear layer — in a robot cell, on a lathe bed, or on site.", ABOUT_SENFENG],
        country="China", families=[f["id"] for f in D.WELD_FAMILIES], family_sets=["senfeng"],
        groups=[{"title": "Handheld laser welders", "families": ["sf-handheld"]}, {"title": "Robotic welding", "families": ["sf-robot-weld"]}, {"title": "Laser cladding", "families": ["sf-cladding"]}],
        cover_photos=["sf-hwm-1", "sf-rw-1", "sf-clad-1"], out="src/" + PDF_WELD),
    "senfeng-panel-benders": dict(
        title="Automatic panel benders", subtitle="Senfeng BDC push-down panel benders 59 – 126″ · suction-cup panel benders 47 – 59″ · 0.2 s per bend · robot cells",
        cover_line="Senfeng Laser · made in China · sold & serviced in Canada by NovoTech", range_label="Senfeng panel benders", about_for="Senfeng panel benders",
        about_kicker="Senfeng Laser · Jinan, China", about_title="Four-side bending with no tooling changes",
        about_text=["A panel bender clamps the blank once and forms every side — up, down, hems, box corners — in 0.2 s per bend while a manipulator turns the part: boxes, "
                    "doors, enclosures, cabinets and HVAC panels in sheet to 14 ga, five to ten times faster than a press brake and without a skilled operator. The "
                    "push-down BDC series bends 59 to 126″ with 13 to 16 servo axes, a 7.9″ bending height (11.8″ optional) and automatic thickness compensation; the "
                    "suction-cup BDC1200 and 1500 are the light machines for door and appliance panels to 20 ga. Robot loading and unloading cells are available.",
                    ABOUT_SENFENG],
        country="China", families=[f["id"] for f in D.PANEL_FAMILIES], family_sets=["dener"],
        groups=[{"title": "BDC panel benders", "families": ["sf-bdc"]}], cover_photos=["sf-bdc-1", "sf-bdc-2", "sf-bdc-robot"], out="src/" + PDF_PANEL),
}


def write_brochure_specs():
    d = os.path.join(ROOT, "tools", "brochure", "specs")
    for name, spec in BROCHURES.items():
        spec = dict(spec, single_phase=False, year="2026", made_in="Made in China by Senfeng Laser — CE, FDA and ETL certified")
        json.dump(spec, open(os.path.join(d, name + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def build():
    pdf_weld = pdf(PDF_WELD, "Download the laser welding & cladding brochure")
    fams = [dict(f, pdf=pdf_weld) for f in D.WELD_FAMILIES]
    write_families(SET, fams)
    common = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **NO_VIDEO}
    write_category(D.P_WELD, PAGE_WELD, fams, SET, "Laser welding", extra={**common, "nav_label": "Laser welding & cladding", "catalogue_pdf": pdf_weld})
    keys = register_images()
    write_brochure_specs()
    used = {k for f in D.ALL for k in f["images"]} | {PAGE_WELD["hero"]} | set(PAGE_WELD["minis"])
    unused = sorted(set(keys) - used - {"senfeng-logo"})
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    print(f"senfeng: {len(D.ALL)} families ({len(fams)} on the welding page) · images: {len(keys)} · brochure specs: {len(BROCHURES)}")


if __name__ == "__main__":
    build()
