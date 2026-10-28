#!/usr/bin/env python3
"""The two laser sections, each a hub over one page per kind of machine — not per supplier.

Sheet lasers (laser-cutting-machine.html): enclosed fiber lasers with exchange table or pallet changer, open-type and
semi-closed single-table lasers, large-format plate lasers, sheet-and-tube combination lasers, 3D laser cells and coil-fed
lines.  Tube lasers (tube-laser-cutting-machine.html): tube laser cutters to Ø14″ with two or three chucks, and heavy-duty
three- and four-chuck tube and profile lasers to Ø25″ and 49 ft.  The premium (Dener) and value (NovoTech, Senfeng) lines are
sections inside each page.

Shared by tools/laser_hub.py (the hubs and the merged family sets) and tools/laser_types.py (the pages); tools/dener_pages.py,
tools/senfeng_pages.py and tools/vl_laser_pages.py only write the families."""

# kind → page slug → [(family id, group id)] in display order; family records come from content/families/dener.json
PAGES = {
    "sheet": {
        "enclosed-fiber-laser": [("dn-gfl", "ls-premium-gfl"), ("dn-smart-closed", "ls-premium-closed"),
                                 ("vn-ule", "ls-value-ule"), ("sf-h", "ls-value-h"), ("sf-compact", "ls-value-compact")],
        "open-type-fiber-laser": [("dn-smart-open", "ls-premium-open"), ("dn-smart-semi", "ls-premium-semi"),
                                  ("vn-ulf", "ls-value-ulf"), ("sf-np", "ls-value-np")],
        "large-format-plate-laser": [("vn-ulg", "ls-value-ulg"), ("sf-r", "ls-value-r")],
        "sheet-and-tube-laser": [("vn-ulft", "ls-value-ulft"), ("vn-ulet", "ls-value-ulet"), ("sf-hm", "ls-value-hm")],
        "3d-laser-and-coil-fed-line": [("sf-3d", "ls-value-3d"), ("sf-coil", "ls-value-coil")],
    },
    "tube": {
        "tube-laser-cutter": [("dn-eftl", "lt-premium-eftl"), ("vn-ult", "lt-value-ult"), ("sf-t", "lt-value-t"), ("sf-plus", "lt-value-plus")],
        "heavy-duty-tube-laser": [("dn-ftl", "lt-premium-ftl"), ("sf-heavy", "lt-value-heavy")],
    },
}

# kind: dict(hub slug, section label, hub label, hub image, hub blurb, subpages=[(slug, title, hero image, blurb, nav label, line)])
SECTIONS = {
    "sheet": dict(
        hub="laser-cutting-machine", section="Sheet laser cutters", label="All sheet lasers", image="dn-gfl-3",
        blurb="Enclosed, open-type, plate, sheet-and-tube or coil-fed? Every fiber laser NovoTech sells for sheet and plate on one page, with the kinds compared and the working area, power and speed of the whole range in one table.",
        subpages=[
            ("enclosed-fiber-laser", "Enclosed fiber laser cutting machines — exchange table and pallet changer, 4 × 4 ft to 8.5 × 41 ft, 1.5 to 80 kW", "dn-gfl-3",
             "The production laser: a laser-safe cabin and a double table or pallet changer that loads the next sheet while the first is cut — the premium GFL and Smart closed-type made in Turkey, NovoTech's value-line ULE with a 15-second exchange table, the H series to 80 kW and compact 4 × 4 ft machines.",
             "Enclosed lasers", ""),
            ("open-type-fiber-laser", "Open-type fiber lasers — single-table and semi-closed, 5 × 10 to 85 × 10.5 ft, 1.5 to 60 kW", "vn-ulf-1",
             "The entry and long-plate laser: an open single table loaded by hand or forklift from any side, from 5 × 10 ft to semi-closed machines of 13 × 82 ft and open tables to 85 ft — the premium Smart open and semi-closed, NovoTech's value-line ULF and the NP series.",
             "Open-type lasers", ""),
            ("large-format-plate-laser", "Large-format plate lasers — ground-rail and gantry machines to 10 × 164 ft, 6 to 60 kW", "vn-ulg-1",
             "For plate: ground-rail lasers that cut 42.7 or 85.3 ft × 14.8 ft beds and gantry plate lasers to 10 × 164 ft with ±45° bevel heads and oxy-fuel, 6 to 60 kW — the value line.",
             "Plate lasers", ""),
            ("sheet-and-tube-laser", "Sheet and tube combination lasers — one machine for plate and tube to Ø13.8″", "vn-ulft-1",
             "A sheet laser with a rotary chuck beside the table: the open ULFT and enclosed ULET to 85 ft sheet and Ø13.8″ tube, and the HM series to 8.3 × 20 ft sheet and Ø8.6″ × 20 ft tube — the value line.",
             "Sheet & tube lasers", ""),
            ("3d-laser-and-coil-fed-line", "3D laser cells and coil-fed laser cutting lines", "sf-3d-1",
             "Beyond the flat sheet: five-axis 3D lasers and robot cells for formed parts, and coil-fed lines that uncoil, level and laser-cut sheet to 9/16″ plate without a sheet in sight — the value line.",
             "3D & coil-fed lasers", ""),
        ]),
    "tube": dict(
        hub="tube-laser-cutting-machine", section="Tube laser cutters", label="All tube lasers", image="dn-tube-2",
        blurb="Standard or heavy-duty? Every tube and profile laser NovoTech sells on one page, with the two kinds compared and the tube range, power, speed and bar length of the whole range in one table.",
        subpages=[
            ("tube-laser-cutter", "Tube laser cutters — two- and three-chuck, Ø0.3″ to 14″, 20 to 39 ft bars, 1.5 to 40 kW", "dn-tube-2",
             "The tube laser for round, square and rectangular tube to Ø14″: the premium E-FTL with 1 G servo chucks made in Turkey, NovoTech's value-line ULT with two or three chucks, and the T series and high-speed PLUS / bevel-cutting GT — bundle loaders and ±45° bevel heads.",
             "Tube laser cutters", ""),
            ("heavy-duty-tube-laser", "Heavy-duty tube and profile lasers — three and four chucks, to Ø25″ and 49 ft", "dn-tube-6",
             "For structural tube, pipe, beams and heavy profiles: the premium FTL to Ø25.2″ and 12 m bars of 2,600 kg, the three- and four-chuck NT / ST / HT machines to Ø25″, 6,600 lb and 49 ft, and the H-beam profile line.",
             "Heavy-duty tube lasers", ""),
        ]),
}


def hub(kind):
    s = SECTIONS[kind]
    return {"slug": s["hub"], "label": s["label"], "image": s["image"], "blurb": s["blurb"]}


def siblings(kind):
    return [(slug, nav, title.split(" — ")[0]) for slug, title, _, _, nav, _ in SECTIONS[kind]["subpages"]]


def subpages(kind):
    """[(slug, title, image, blurb, nav_label)] for write_hub"""
    return [(s, t, im, b, nav) for s, t, im, b, nav, _ in SECTIONS[kind]["subpages"]]


def lines(kind):
    return [line for *_, line in SECTIONS[kind]["subpages"]]


def families(kind):
    """[(page slug, [family ids])] for the hub's merged set"""
    return [(slug, [fid for fid, _ in items]) for slug, items in PAGES[kind].items()]


def group_of(kind, fid):
    for items in PAGES[kind].values():
        for f, g in items:
            if f == fid:
                return g
    raise KeyError(fid)
