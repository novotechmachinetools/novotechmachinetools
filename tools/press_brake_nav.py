#!/usr/bin/env python3
"""The press-brake section: one hub (press-brake.html) over two pages, one per kind of drive — hydraulic press brakes
(Dener XL and XH hybrid, NovoTech's value-line CNC and NC brakes, the ISITAN compact brakes) and electric press brakes
(Dener DDM servo-electric and DDS ball-screw, NovoTech's value-line electric brakes).  The horizontal press brake keeps
its own page (horizontal-press-brake.html) and is linked from the hub.

Pages are split by what the buyer searches for (the kind of machine), not by supplier: the premium and value lines are
sections inside each page.  Shared by tools/press_brake_hub.py (the hub and the merged family set) and
tools/press_brake_types.py (the two pages); tools/dener_pages.py, tools/vl_sheet_pages.py and tools/isitan_pressbrake.py
only write the families now."""

HUB = "press-brake"
SECTION = "Press brakes"

# (page slug, [(family set, family id, group id)]) — display order within the page follows this list
PAGES = {
    "hydraulic-press-brake": [
        ("dener", "dn-xl-small", "pb-premium"), ("dener", "dn-xl-large", "pb-premium"),
        ("value-sheet", "vl-wad-small", "pb-value"), ("value-sheet", "vl-wad-large", "pb-value"), ("value-sheet", "vl-wad-heavy", "pb-value"),
        ("dener", "dn-xh", "pb-hybrid"),
        ("value-sheet", "vl-nc-small", "pb-nc"), ("value-sheet", "vl-nc-large", "pb-nc"),
        ("edgebender", "isitan-edgebender-cnc", "pb-compact"), ("edgebender", "isitan-edgebender-nc", "pb-compact"),
    ],
    "electric-press-brake": [
        ("dener", "dn-ddm", "pb-servo"), ("dener", "dn-dds", "pb-servo"),
        ("value-sheet", "vl-wadg", "pb-value-electric"), ("value-sheet", "vl-wadg-mini", "pb-value-electric"),
    ],
}

# (slug, title, hero image, blurb, nav label, line)
SUBPAGES = [
    ("hydraulic-press-brake", "Hydraulic press brakes — CNC, hybrid, NC and compact, 33 to 1,323 US tons", "dn-xl-1",
     "The workhorse for plate and production: Dener XL CNC brakes to 661 US tons and 20 ft, NovoTech's value-line CNC brakes to 1,323 tons, the XH hybrid with a servo pump, NC torsion-bar brakes from 33 tons and the ISITAN compact 4 – 7 ft machines.",
     "Hydraulic press brakes", ""),
    ("electric-press-brake", "Electric press brakes — servo-electric and ball-screw, 3 to 220 US tons", "dn-ddm-2",
     "No hydraulic oil: Dener DDM servo-electric brakes to 220 US tons and 13 ft, the DDS ball-screw brake from 22 tons, and NovoTech's value-line electric brakes from 3 to 176 tons — ±0.01 mm, twice the speed, about 70 % less power.",
     "Electric press brakes", ""),
]


def hub():
    return {"slug": HUB, "label": "All press brakes", "image": "dn-xl-1",
            "blurb": "Hydraulic or electric? Every press brake NovoTech sells in Canada on one page, with the capacity table for the whole range and the horizontal press brakes."}


def siblings():
    return [(s, nav, title.split(" — ")[0]) for s, title, _, _, nav, _ in SUBPAGES] + [("horizontal-press-brake", "Horizontal press brakes", "Horizontal press brakes")]


def family_sources():
    """(family set, page slug, family ids) per page, for the hub's merged set"""
    out = []
    for slug, items in PAGES.items():
        for set_name in dict.fromkeys(s for s, _, _ in items):
            out.append((set_name, slug, [fid for s, fid, _ in items if s == set_name]))
    return out


def group_of(fid):
    for items in PAGES.values():
        for _, f, g in items:
            if f == fid:
                return g
    raise KeyError(fid)
