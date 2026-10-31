#!/usr/bin/env python3
"""The press-brake section: one hub (press-brake.html) over three pages — hydraulic press brakes (Dener XL and mild hybrid XL,
NovoTech's value-line CNC and NC brakes), electric press brakes (Dener DDM servo-electric and DDS ball-screw, NovoTech's
value-line electric brakes) and compact hydraulic press brakes (the Dener XL 1560, the value-line WAD-50T and WC67K-30T
compacts and, through content/extra_groups, the value-line HBV bending brakes — the ISITAN Edgebenders left the site Oct 28 2026).  The horizontal press brake is a different machine (bar, pipe and
busbar) with its own page outside this section.

Pages are split by what the buyer searches for (the kind of machine), not by supplier: the premium and value lines are
sections inside each page.  Shared by tools/press_brake_hub.py (the hub and the merged family set) and
tools/press_brake_types.py (the three pages); tools/dener_pages.py and tools/vl_sheet_pages.py only write the families now."""

HUB = "press-brake"
SECTION = "Press brakes"

# (page slug, [(family set, family id, group id)]) — display order within the page follows this list
PAGES = {
    "hydraulic-press-brake": [
        # the XH full hybrid is off the site (the owner, Oct 31 2026)
        ("dener", "dn-xl", "pb-premium"),
        ("value-sheet", "vl-wad", "pb-value"),
        ("value-sheet", "vl-nc", "pb-nc"),
        ("value-sheet", "vl-wad-heavy", "pb-heavy"),      # the last product on the page (the owner, Oct 31 2026)
    ],
    "electric-press-brake": [
        ("dener", "dn-ddm", "pb-servo"), ("dener", "dn-dds", "pb-servo"),
        ("value-sheet", "vl-wadg", "pb-value-electric"), ("value-sheet", "vl-wadg-mini", "pb-value-electric"),
    ],
    "compact-hydraulic-press-brakes": [
        ("dener", "dn-xl-1560", "pb-compact-dener"),
        ("value-sheet", "vl-wad-compact", "pb-compact-cnc"), ("value-sheet", "vl-nc-compact", "pb-compact-nc"),
    ],
}

# (slug, title, hero image, blurb, nav label, line)
SUBPAGES = [
    ("hydraulic-press-brake", "Hydraulic press brakes — CNC, hybrid and NC, 33 to 1,323 US tons", "dn-xl-1",
     "The workhorse for plate and production: Dener XL CNC brakes to 661 US tons and 20 ft, NovoTech's value-line CNC brakes to 1,323 tons and 26 ft, the mild hybrid XL, and NC torsion-bar brakes from 33 tons.",
     "Hydraulic press brakes", ""),
    ("electric-press-brake", "Electric press brakes — servo-electric and ball-screw, 3 to 220 US tons", "dn-ddm-2",
     "No hydraulic oil: Dener DDM servo-electric brakes to 220 US tons and 13 ft, the DDS ball-screw brake from 22 tons, and NovoTech's value-line electric brakes from 3 to 176 tons — ±0.01 mm, twice the speed, about 70 % less power.",
     "Electric press brakes", ""),
    ("compact-hydraulic-press-brakes", "Compact hydraulic press brakes — 16 to 66 US tons, 2 to 8 ft", "dn-xl1560-studio",
     "The press brakes for a sheet-metal shop: the Dener XL 1560 compact CNC brake, 66 US tons × 5 ft, NovoTech's value-line WAD-50T CNC and WC67K-30T NC compacts over 4.3 – 5.2 ft, and the HBV bending brakes from 16 tons for brackets and short parts in plate.",
     "Compact press brakes", ""),
]


def hub():
    return {"slug": HUB, "label": "All press brakes", "image": "dn-xl-1",
            "blurb": "Hydraulic, electric or compact? Every press brake NovoTech sells in Canada on one page, with the three kinds compared and the capacity table for the whole range."}


def siblings():
    return [(s, nav, title.split(" — ")[0]) for s, title, _, _, nav, _ in SUBPAGES]


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


def why_features():
    """The 'Included with every machine' block of the press-brake pages: the site's standard features with two offers that apply
    to press brakes only (Oct 2026) — installation and training in the Greater Toronto Area at no charge, and free delivery to
    the customer's door in the GTA for press brakes ordered from the factory (back-ordered, not in-stock machines)."""
    import json
    import os
    site = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "site.json"), encoding="utf-8"))
    out = []
    for f in site["standard_features"]:
        f = dict(f)
        if f["title"] == "Installation and training":
            f["title"] = "Installation and training — free in the GTA"
            f["text"] = ("On every press brake delivered in the Greater Toronto Area, NovoTech's technicians commission the machine and train your "
                         "operators at no charge. Elsewhere in Canada on request, at an additional charge.")
        elif f["title"].startswith("Shipping across Canada"):
            f["title"] = "Free delivery in the GTA on factory orders"
            f["text"] = ("A press brake ordered from the factory is delivered to your door anywhere in the Greater Toronto Area at no charge; "
                         "unloading at your plant is the buyer's. In-stock machines, and deliveries elsewhere in Canada and the United States, ship at freight rates quoted by NovoTech.")
        out.append(f)
    return out

