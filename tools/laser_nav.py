#!/usr/bin/env python3
"""The two laser sections — not per supplier.

Sheet lasers (laser-cutting-machine.html): a hub over one page per kind — fiber lasers with shuttle table or pallet changer,
sheet-and-tube combination lasers, large-format plate lasers (semi-closed, ground-rail, gantry), 3D laser cells, and coil-fed
lines.  Tube lasers (tube-laser-cutting-machine.html): ONE page, no hub — the tube laser cutters to Ø14″ and the heavy-duty
three- and four-chuck machines to Ø25″ and 49 ft together, with the tube laser buying guide (the owner, Nov 1 2026).  The
premium (Dener) and value (NovoTech, Senfeng) lines are sections inside each page.

Shared by tools/laser_hub.py (the hubs and the merged family sets) and tools/laser_types.py (the pages); tools/dener_pages.py,
tools/senfeng_pages.py and tools/vl_laser_pages.py only write the families."""

# kind → page slug → [(family id, group id)] in display order; family records come from content/families/dener.json
PAGES = {
    # four groups on the sheet-laser hub (the owner, Oct 31 2026): lasers with shuttle table / pallet changer, sheet-and-tube
    # combinations, large-format plate lasers (semi-closed, ground-rail, gantry), and 3D cells and coil-fed lines on two pages.
    # No fully open machines: the Smart open-type, ULF and ULFT are gone; the NP has a cover on its gantry.
    "sheet": {
        "fiber-laser-cutting-machine": [("dn-gfl", "ls-premium-gfl"), ("dn-smart-closed", "ls-premium-closed"),
                                        ("vn-ule", "ls-value-ule"), ("sf-h", "ls-value-h"), ("sf-compact", "ls-value-compact"), ("sf-np", "ls-value-np"),
                                        ("sf-1313g", "ls-value-1313g")],     # compact G / N / NP above the NP, SF1313G last (the owner, Nov 1 2026)
        "sheet-and-tube-laser": [("vn-ulet", "ls-value-ulet"), ("sf-hm", "ls-value-hm")],
        "large-format-plate-laser": [("dn-smart-semi", "ls-premium-semi"), ("vn-ulg", "ls-value-ulg"), ("sf-r", "ls-value-r")],
        "3d-laser-cutting-machine": [("sf-3d", "ls-value-3d")],
        "coil-fed-laser-cutting-line": [("sf-coil", "ls-value-coil"), ("sf-coil-c", "ls-value-coil-c"), ("sf-top", "ls-value-top"),
                                        ("sf-coil-clh", "ls-value-clh"), ("sf-coil-2012", "ls-value-coil-heavy")],   # five lines (the owner, Nov 1 2026)
    },
    # one page for every tube laser, standard and heavy-duty (the owner, Nov 1 2026: no hub, no split)
    "tube": {
        "tube-laser-cutting-machine": [("dn-eftl", "lt-premium-eftl"), ("dn-ftl", "lt-premium-ftl"), ("vn-ult", "lt-value-ult"),
                                       ("sf-t", "lt-value-t"), ("sf-plus", "lt-value-plus"), ("sf-gt", "lt-value-gt"),
                                       ("sf-nt", "lt-value-nt"), ("sf-st", "lt-value-st")],
    },
}

# kind: dict(hub slug, section label, hub label, hub image, hub blurb, subpages=[(slug, title, hero image, blurb, nav label, line)])
SECTIONS = {
    "sheet": dict(
        hub="laser-cutting-machine", section="Sheet laser cutters", label="All sheet lasers", image="dn-gfl-1",
        blurb="Shuttle table, sheet and tube, large-format plate, 3D or coil-fed? Every fiber laser NovoTech sells for sheet and plate on one page, with the kinds compared and the working area, power and speed of the whole range in one table.",
        subpages=[
            ("fiber-laser-cutting-machine", "Fiber laser cutting machines — shuttle table or pallet changer, 4 × 4 ft to 8.5 × 41 ft, 1.5 to 80 kW", "dn-gfl-1",
             "The production laser: a shuttle table or pallet changer loads the next sheet while the first is cut — the premium GFL and Smart made in Turkey, NovoTech's value-line ULE with a 15-second shuttle table, the Senfeng H series to 80 kW, the NP with a cover on its gantry and compact 4 × 4 ft machines.",
             "Fiber laser cutters", ""),
            ("sheet-and-tube-laser", "Sheet and tube combination lasers — one machine for sheet and tube to Ø13.8″", "sf-hm-1",
             "A sheet laser with a rotary chuck beside the table: the ULET with shuttle table to 41 × 8.5 ft sheet and Ø13.8″ tube, and the HM series to 8.3 × 20 ft sheet and Ø8.6″ × 20 ft tube — the value line.",
             "Sheet & tube lasers", ""),
            ("large-format-plate-laser", "Large-format plate lasers — semi-closed, ground-rail and gantry machines to 13 × 82 ft and 10 × 164 ft, 3 to 60 kW", "vn-ulg-1",
             "For long and heavy plate: the premium Smart semi-closed single tables to 13 × 82 ft, ground-rail lasers with 42.7 or 85.3 ft beds and gantry plate lasers to 10 × 164 ft with ±45° bevel heads, 3 to 60 kW.",
             "Large-format lasers", ""),      # was "Plate lasers" (the owner, Nov 1 2026)
            ("3d-laser-cutting-machine", "3D laser cutting machines — five-axis SF3015TD, 5 × 10 ft, 3 to 20 kW", "sf-3d-1",
             "For formed parts: the five-axis SF3015TD trims and cuts stamped, drawn and bent parts and pipe fittings after forming, 3 to 20 kW — the value line.",
             "3D laser cells", ""),
            ("coil-fed-laser-cutting-line", "Coil-fed laser cutting lines — uncoil, level and cut coil to 9/16″ plate, 1.5 to 80 kW", "sf-coil-1",
             "Cut blanks straight from the coil: five lines for thin, aluminum and 5/16 – 9/16″ coil from 1.5 to 80 kW, and the TOP line with robot sorting, panel bending and welding — the value line.",
             "Coil-fed laser lines", ""),
        ]),
    # a single page: no hub, no section bar of sibling pages
    "tube": dict(
        hub=None, section="Tube laser cutters", label="Tube laser cutters", image="dn-tube-2", blurb="",
        subpages=[
            ("tube-laser-cutting-machine", "Tube and profile laser cutting machines — Ø0.3″ to 25.2″, 20 to 49 ft tubes, 1.5 to 40 kW", "dn-tube-2",
             "Every tube and profile laser NovoTech sells: two- and three-chuck tube laser cutters to Ø14″ and heavy-duty three- and four-chuck machines to Ø25″ and 49 ft.",
             "Tube laser cutters", ""),
        ]),
}


def hub(kind):
    s = SECTIONS[kind]
    if not s["hub"]:
        return None
    return {"slug": s["hub"], "label": s["label"], "image": s["image"], "blurb": s["blurb"]}


def siblings(kind):
    if not SECTIONS[kind]["hub"]:
        return None
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
