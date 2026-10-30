#!/usr/bin/env python3
"""NovoTech value-line laser pages: novotech-fiber-lasers (ULF, ULE, ULFT, ULET — under the laser-cutting-machine hub) and
novotech-tube-lasers (ULT — under the tube-laser-cutting-machine hub).  The families live in the 'dener' family set, which
tools/dener_pages.py writes with them included (the laser hubs read every laser family from that set); photos from
tools/vl_laser_photos.py (section 'value-laser').

    python3 tools/vl_laser_photos.py                    # logo-free sources → tools/src-images/value-laser
    python3 tools/dener_pages.py                        # the 'dener' family set (with these families) + the Dener pages
    python3 tools/senfeng_pages.py
    python3 tools/vl_laser_pages.py                     # the two pages + image_map entries (tools/vl_laser_keys.txt) + brochure specs
    python3 tools/laser_hub.py
    python3 tools/make_images.py --only $(cat tools/vl_laser_keys.txt)
    python3 tools/brochure/build_brochure.py tools/brochure/specs/novotech-fiber-lasers.json   (and novotech-tube-lasers.json)
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category  # noqa: F401
import vl_laser_data as D
import vl_laser_photos as PH
import laser_nav as LN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "dener"
BRAND = D.BRAND
PDF_SHEET = "files/NovoTech-Fiber-Lasers-Value-Line-2026.pdf"
PDF_TUBE = "files/NovoTech-Tube-Lasers-Value-Line-2026.pdf"

BRAND_LINE = ("NovoTech's own value line: built in China to high North American quality standards, with Raycus, MAX or IPG sources, "
              "Cypcut controls, Hiwin guides and Schneider components, the same CSA-approved panel, 1-year warranty and Mississauga, ON, Canada "
              "parts and support as every machine we sell.")
ORIGIN = {"title": "Built in China to North American standards", "text": "NovoTech's own brand — Raycus or IPG sources, Raytools, BOCI or Precitec "
          "heads and Cypcut controls, inspected before shipping, with the same CSA panel, warranty and Mississauga, ON, Canada support as every machine we sell."}
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}


def pdf(file, label):
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": label, "size": size}


PAGE_SHEET = dict(
    title="NovoTech Fiber Laser Cutters, 1.5–60 kW · Value Line",
    meta="Open ULF lasers from 10 × 5 ft, enclosed ULE lasers with a 15 s exchange table, ULG ground-rail plate lasers to 85 × 14.8 ft and ULFT / ULET sheet + tube.",
    h1="NovoTech fiber laser cutters — open, enclosed exchange-table, ground-rail plate and sheet + tube lasers, 1.5 to 60 kW · value line",
    intro="These are NovoTech's own fiber lasers — the value line: built in China to our specification with Raycus, MAX or IPG sources, "
          "Raytools, BOCI or Precitec heads, Cypcut controls, Hiwin guides and Schneider electrics, inspected before they ship and sold "
          "under NovoTech's name. Five families on one page: the open-type ULF single-table lasers — the G build from 1.5 to 6 kW, the "
          "heavier E build to 12 kW and large-format plate tables from 20 × 8.5 to 85 × 10.5 ft with up to 60 kW; the enclosed ULE with "
          "an exchange table that swaps in 15 seconds, from 10 × 5 to 41 × 8.5 ft and 3 to 40 kW; the ULG ground-rail plate lasers, whose "
          "gantry runs on floor rails over a table 42.7 or 85.3 ft long and up to 14.8 ft wide, with 12 to 60 kW; and the ULFT and ULET, "
          "which cut sheet and tube to Ø13.8″ on one machine, open or enclosed. For the Turkish-built premium lasers see the Dener page; for 4 × 4 ft "
          "compact machines, 80 kW and coil-fed lines see Senfeng. Every machine is installed and supported from Mississauga, ON, Canada, with a "
          "CSA-approved panel and a 1-year warranty.",
    points=["ULF open-type: G build 1.5 – 6 kW, E build to 12 kW and 1.7 G on 10 × 5 to 20 × 7.2 ft; large-format plate tables to 85 × 10.5 ft and 60 kW",
            "ULE enclosed with exchange table, 15 s swap: 10 × 5 to 41 × 8.5 ft, 3 – 40 kW, Z travel to 16.5″, ready for a storage tower",
            "ULG ground-rail plate lasers: 42.7 or 85.3 ft × up to 14.8 ft, 12 – 60 kW, up to 202,000 lb of plate on the table",
            "ULFT and ULET sheet + tube: the laser table plus a pneumatic chuck for tube to Ø13.8″ and 39 ft, open or enclosed, 1.5 – 60 kW"],
    hero="vn-ule-1", minis=["vn-ulf-1", "vn-ulft-1"],
    groups=[("laser-novotech", "NovoTech fiber lasers — the value line", "Open single-table, enclosed exchange-table, ground-rail plate and sheet + tube lasers from 10 × 5 to 85 × 14.8 ft, 1.5 to 60 kW.", BRAND)],
    faq=[{"q": "Open ULF or enclosed ULE?",
          "a": "The ULF is the open machine: a single table loaded from three sides, the lowest price per kilowatt and the right choice for a shop that cuts a few hours a day and unloads by hand. The ULE puts the cutting area in a full enclosure — laser-safe windows, fumes extracted from inside the cabin, less noise — and adds an exchange table that swaps in 15 seconds, so the laser cuts while the operator loads the next sheet. Above 6 kW, for two shifts, or with a storage tower in mind, buy the ULE."},
         {"q": "ULF-G or ULF-E?",
          "a": "Both are open single-table lasers. The G build takes 1.5 to 6 kW and moves at 295 ft/min with 1.4 G — plenty for sheet and light plate. The E build has a heavier frame for 1.5 to 12 kW, 459 ft/min and 1.7 G, a 7.2 ft wide table option (4022E, 6022E) and higher table loads; the large-format E machines from 20 × 8.5 to 85 × 10.5 ft take 6 to 60 kW for plate. Choose the E if you plan to go above 6 kW later or cut thick plate every day."},
         {"q": "What thickness does each laser power cut?",
          "a": "As a guide for mild steel cut with oxygen: 3 kW cuts to 3/4″ (20 mm), 6 kW to 1″ (25 mm), 12 kW to 1-3/16″ (30 mm), and 20 to 30 kW to 2 – 2-3/8″ (50 – 60 mm). The production thickness — where the edge is clean and the speed pays — is about two-thirds of the maximum, and stainless and aluminum cut with nitrogen run thinner at the same power. Most Canadian job shops buying today choose 6 or 12 kW; we send the cutting-speed chart for your material with the quote."},
         {"q": "When does a ground-rail laser make sense?",
          "a": "When the plate is longer than about 40 ft, wider than 10 ft or heavier than a table machine carries. On the ULG the gantry runs on rails set in the floor and the plate lies on a separate support table, so the table takes up to 202,000 lb (91.8 t) — a 2″ plate the full 85 × 14.8 ft weighs about 103,000 lb — without loading the axes. Structural, bridge, tower, mining and heavy-equipment fabricators use it for thick plate that used to go to plasma or oxy-fuel. It needs a prepared foundation for the rails, crane access along the table and extraction sized to the cutting zones; we plan the layout with you. The ULG-A is the faster gantry (262 ft/min, 1.1 G); the ULG-C leaves 11.8″ under the beam with a 60 kW source."},
         {"q": "Sheet and tube on one machine — ULFT or ULET?",
          "a": "Both add a pneumatic rotary chuck and tube supports to the sheet laser: round, square and rectangular tube to Ø8.7″ or Ø13.8″ and 20, 29.5 or 39 ft long, cut with the same source and head. The ULFT is the open version on the ULF table, to 85 × 10.5 ft and 60 kW; the ULET is the enclosed version with the exchange table, to 41 × 8.5 ft and 40 kW. A shop that cuts tube every day is better served by a dedicated ULT tube laser with a loader."},
         {"q": "What does the laser need on site?",
          "a": "Three-phase power (600 V with the CSA panel, or 208 / 240 / 480 V on request), compressed air at 185 psi (13 bar) and 53 cfm (1.5 m³/min) for air cutting, oxygen and nitrogen of 99.96 % purity, a dust collector, and a shop between 41 and 86 °F (5 – 30 °C) with humidity under 70 % — the water chiller is included. We lay the machine out for your building and size the compressor and dust collector with the quote."},
         {"q": "How does the NovoTech value line compare with Dener and Senfeng?",
          "a": "Dener is the premium line: built in Turkey with Precitec heads, IPG or nLIGHT sources and parts stocked in Canada, for the shop that cuts two shifts a day for twenty years. Senfeng is a value line sold under its own brand, with the widest range — 4 × 4 ft compact machines, 80 kW, 3D and coil-fed lasers. The NovoTech lasers are our own brand, built in China to our specification with Raycus or IPG sources, Cypcut controls and Hiwin, YYC and Schneider components, at the lowest price of the three; all are installed, warranted and serviced by the same NovoTech technicians. We quote all three so you can compare."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about the NovoTech fiber lasers",
    related_pages=[{"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}, {"href": "hydraulic-press-brake.html", "label": "NovoTech CNC press brakes · value line"},
                   {"href": "hydraulic-shearing-machine.html", "label": "Value-line hydraulic shears"},
                   {"href": "sheet-metal-plate-deburring-edge-rounding-finishing-grinding.html", "label": "Deburring after laser cutting"},
                   {"href": "laser-welding-machine.html", "label": "Laser welding & cladding"}],
    related_title="Machinery that works alongside a laser",
)

PAGE_TUBE = dict(
    title="NovoTech Tube Laser Cutters, Ø0.4–14″ · Value Line",
    meta="ULT tube and pipe lasers with two or three pneumatic chucks: round Ø0.4–14.2″, square to 13.8″, 20–39 ft bars to 2,205 lb, loaders and ±45° bevel heads.",
    h1="NovoTech tube lasers — ULT two- and three-chuck tube and pipe lasers, Ø0.4″ to 14.2″ · value line",
    intro="A tube laser cuts round, square, rectangular and open profiles to length and cuts the holes, copes, slots and notches in them in one "
          "pass, straight from the 3D model. The ULT is NovoTech's own tube laser — the value line, built in China to our specification and "
          "sold under NovoTech's name: pneumatic self-centring chucks at both ends of the bar, servo-following supports, 1.5 to 40 kW sources "
          "and four chuck sizes for round tube from Ø0.4 to 14.2″ and square to 13.8″, on 20, 29.5 or 39 ft bars of up to 2,205 lb. The "
          "three-chuck version cuts the last part without a remnant; pneumatic loaders, bundle feeding to 5 tonnes, a ±45° five-axis bevel "
          "head and TubesT nesting are options. For sheet and tube on one machine see the ULFT and ULET on the NovoTech fiber laser page; "
          "for the premium Turkish tube lasers see Dener. Installed and supported from Mississauga, ON, Canada, with a CSA-approved panel and a "
          "1-year warranty.",
    points=["Four chuck sizes: Ø6.3, 9.4, 11 and 14.2″ round, square to 13.8″; 20, 29.5 or 39 ft bars to 2,205 lb",
            "1.5 – 40 kW; 328 ft/min and 1.2 G on the small chucks; ±0.04 mm/m positioning; double-acting pneumatic chucks",
            "Three-chuck zero-tail version; pneumatic loader, bundle feeding to 5 t, ±45° five-axis bevel head, TubesT nesting"],
    hero="vn-ult-1", minis=["vn-ult-chuck", "vn-ulft-1"],
    groups=[("tube-novotech", "NovoTech tube lasers — the value line", "Two- and three-chuck ULT tube lasers in four chuck sizes, Ø0.4 to 14.2″, 20 to 39 ft bars.", BRAND)],
    faq=[{"q": "Which ULT chuck size do I need?",
          "a": "Size the chuck to the largest tube you cut. The 016 takes round tube from Ø0.4 to 6.3″ and square to 6.3″ — furniture, fitness equipment, racking and railings; the 024 takes Ø9.4″ and square to 8.9″, the size most fabrication shops buy; the 028 takes Ø11″ and the 036 Ø14.2″ and square to 13.8″, with bars to 2,205 lb for structural tube and pipe. The smaller chucks turn faster — 53.5 rpm against 23 rpm on the 036 — and accelerate harder, so they are quicker on small tube."},
         {"q": "Two chucks or three?",
          "a": "With two chucks the rear chuck has to keep hold of the bar, so the last few inches of every bar are scrap. The three-chuck ULT adds a chuck that takes over the bar as it shortens and cuts the last part with no remnant — on 20 to 39 ft bars of stainless or heavy-wall tube that saves material on every bundle. It is built on the 024, 028 and 036 chucks."},
         {"q": "How is the tube loaded?",
          "a": "The pneumatic loader of the 016 and 024 machines separates one bar from the rack and feeds it to the rear chuck — round tube to Ø8.7″ and square to 8.7″ across the corners. The automatic feeding system takes bundles of up to 5 tonnes and bars up to 606 lb (275 kg), sorting and positioning each bar in a 19-second cycle. The heavy tube of the 028 and 036 machines is placed on the infeed supports by crane. Finished parts slide onto the unloading table."},
         {"q": "Can it cut bevels for welding?",
          "a": "Yes — the optional five-axis head tilts ±45°, so weld preparations, mitred corners and tube-to-tube copes are cut in the same pass as the holes and the parting cut. The standard head cuts square to the tube wall."},
         {"q": "What about software?",
          "a": "The Cypcut tube control holds the cutting database and adjusts the power to the speed through corners. TubesT, BOCHU's tube nesting software, imports the 3D parts, unfolds them onto the profile and nests them along the bar to use the remnant; it is an option and also runs on a PC in the office."},
         {"q": "How does the ULT compare with the Dener and Senfeng tube lasers?",
          "a": "Dener's E-FTL and FTL are the premium machines — built in Turkey with 1 G servo chucks and parts stocked in Canada — and the FTL goes to Ø25.2″. Senfeng's value line covers Ø0.5 to 25″ with three- and four-chuck machines and an H-beam line. The ULT is NovoTech's own tube laser for the sizes most shops cut, Ø0.4 to 14.2″, at the lowest price of the three; every model of the three lines is in one table on the tube laser cutters overview."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about the NovoTech tube lasers",
    related_pages=[{"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"},
                   {"href": "pipe-notcher.html", "label": "Tube notchers"}, {"href": "tube-end-forming-machines.html", "label": "Tube end formers"},
                   {"href": "band-saw.html", "label": "Band saws"}],
    related_title="More tube machinery from NovoTech",
)

ABOUT_NT = ("NovoTech Machine Tools sells, installs and supports sheet-metal and fabrication machinery across Canada from Mississauga, ON, Canada. "
            "The value line is our own brand: machines built in China to our specification with established components — Raycus, "
            "MAX or IPG sources, Raytools, BOCI or Precitec heads, Cypcut controls, Hiwin guides, YYC racks and Schneider electrics — inspected "
            "before they ship, with a CSA-approved panel, a 1-year warranty, operator training and parts and service from Mississauga, ON, Canada.")

BROCHURES = {
    "novotech-fiber-lasers": dict(
        title="Fiber laser cutting machines", subtitle="NovoTech value line · ULF open-type, ULE enclosed with exchange table, ULG ground-rail, ULFT and ULET sheet + tube · 10 × 5 to 85 × 14.8 ft · 1.5 – 60 kW",
        cover_line="NovoTech value line · built in China to North American standards · sold & serviced in Canada by NovoTech", range_label="NovoTech fiber lasers",
        about_for="NovoTech fiber lasers", about_kicker="NovoTech value line", about_title="Open, enclosed and sheet + tube fiber lasers at a price a small shop can justify",
        about_text=["A fiber laser cutting machine cuts sheet and plate from a DXF file with a focused beam — mild steel to 1″ with 6 kW and to 2″ and beyond "
                    "with 20 to 30 kW — at speeds no plasma or punch can match, with a clean edge and no tooling. The ULF is the open single-table laser: "
                    "the G build from 1.5 to 6 kW, the heavier E build to 12 kW and 1.7 G, and large-format plate tables to 85 × 10.5 ft with up to 60 kW. "
                    "The ULE puts the cutting area in a full enclosure and swaps two tables in 15 seconds, from 10 × 5 to 41 × 8.5 ft and 3 to 40 kW. The "
                    "ULG runs its gantry on floor rails over a plate table 42.7 or 85.3 ft long and up to 14.8 ft wide, with 12 to 60 kW. The "
                    "ULFT and ULET add a pneumatic chuck for tube to Ø13.8″ and 39 ft, so one machine cuts sheet and tube.", ABOUT_NT],
        country="China", made_in="Built in China to North American standards", families=[f["id"] for f in D.SHEET_FAMILIES], family_sets=["dener"],
        groups=[{"title": "Sheet lasers", "families": ["vn-ulf", "vn-ule"]}, {"title": "Ground-rail plate lasers", "families": ["vn-ulg"]},
                {"title": "Sheet + tube lasers", "families": ["vn-ulft", "vn-ulet"]}],
        cover_photos=["vn-ule-1", "vn-ulf-1", "vn-ulft-1"], out="src/" + PDF_SHEET),
    "novotech-tube-lasers": dict(
        title="Tube laser cutting machines", subtitle="NovoTech value line · ULT two- and three-chuck tube and pipe lasers · Ø0.4 to 14.2″ · 20 to 39 ft bars · 1.5 to 40 kW",
        cover_line="NovoTech value line · built in China to North American standards · sold & serviced in Canada by NovoTech", range_label="NovoTech tube lasers",
        about_for="NovoTech tube lasers", about_kicker="NovoTech value line", about_title="Round, square and profile tube cut to length with every hole, cope and notch in one pass",
        about_text=["A tube laser cuts round, square, rectangular and open profiles to length and cuts the holes, copes, slots and notches in them in one pass, "
                    "straight from the 3D model — no saw, no drill, no notcher, no layout. The ULT carries the bar in double-acting pneumatic chucks with "
                    "servo-following supports and cuts it with a 1.5 to 40 kW source: four chuck sizes for round tube from Ø0.4 to 14.2″ and square to 13.8″, "
                    "bars of 20, 29.5 or 39 ft and up to 2,205 lb. The three-chuck version cuts the last part without a remnant; pneumatic loaders, bundle "
                    "feeding to 5 tonnes, a ±45° five-axis bevel head and TubesT nesting are options.", ABOUT_NT],
        country="China", made_in="Built in China to North American standards", families=[f["id"] for f in D.TUBE_FAMILIES], family_sets=["dener"],
        groups=[{"title": "Tube lasers", "families": ["vn-ult"]}],
        cover_photos=["vn-ult-1", "vn-ult-chuck", "vn-ult-head"], out="src/" + PDF_TUBE),
}


def write_brochure_specs():
    d = os.path.join(ROOT, "tools", "brochure", "specs")
    for name, spec in BROCHURES.items():
        spec = dict(spec, single_phase=False, year="2026")
        json.dump(spec, open(os.path.join(d, name + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key, p in PH.PHOTOS.items():
        ext, _ = PH.export_kind(key)
        if not os.path.exists(os.path.join(PH.OUT, key + ext)):
            print("!! missing export for", key)
            continue
        imap[key] = {"src": f"tools/src-images/value-laser/{key}{ext}", "alt": p["alt"], "section": "value-laser", "trim": ext == ".webp", "quality": 82,
                     "cutout": False}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "vl_laser_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    pdf_sheet = pdf(PDF_SHEET, "Download the NovoTech fiber laser brochure")
    pdf_tube = pdf(PDF_TUBE, "Download the NovoTech tube laser brochure")
    common = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **NO_VIDEO}
    # the ULF / ULE / ULG / ULFT / ULET / ULT families live in the 'dener' family set (tools/dener_pages.py writes it) and are shown on
    # the pages per kind of laser (tools/laser_types.py), not on a NovoTech-line page
    keys = register_images()
    write_brochure_specs()
    used = {k for f in D.ALL for k in f["images"]}
    for p in (PAGE_SHEET, PAGE_TUBE):
        used |= {p["hero"]} | set(p["minis"])
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    print(f"value-laser: {len(D.ALL)} families on 2 pages · images: {len(keys)} · brochure specs: {len(BROCHURES)}")


if __name__ == "__main__":
    build()
