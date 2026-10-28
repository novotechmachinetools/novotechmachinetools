#!/usr/bin/env python3
"""The shear section: one hub (shear-cutting.html) over three pages, one per kind of shear — hydraulic shears (swing beam and
guillotine plate shears, premium and value lines), mechanical guillotine shears (direct-gear SRGM, flywheel shears) and sheet
metal shears (pneumatic, light hydraulic, electric, bench and coil machines for the sheet-metal shop).

Pages are split by the kind of machine the buyer searches for, not by supplier: the premium and value lines are sections
inside each page.  Shared by tools/shear_hub.py (the hub and the merged family set) and tools/shear_types.py (the three
pages); tools/dener_pages.py, tools/saymak_pages.py, tools/vl_sheet_pages.py and tools/ttmc_pages.py only write the families."""

HUB = "shear-cutting"
SECTION = "Shears"

# (page slug, [(family set, family id, group id)]) — display order within the page follows this list
PAGES = {
    "hydraulic-shearing-machine": [
        ("shears", "dn-bs", "sh-premium-swing"), ("shears", "dn-das", "sh-premium-cnc"),
        ("value-sheet", "vl-qc12k", "sh-value-swing"), ("value-sheet", "vl-q11k", "sh-value-guillotine"),
        ("ttmc", "tt-ths", "sh-light-hydraulic"), ("ttmc", "tt-hq11", "sh-light-hydraulic"),
    ],
    "mechanical-guillotine-shear": [
        ("shears", "nt-shear-srgm-h", "sh-srgm"), ("shears", "nt-shear-srgm", "sh-srgm"),
        ("shears", "nt-shear-srgm-hfr", "sh-srgm-return"), ("shears", "nt-shear-srgm-fr", "sh-srgm-return"),
        ("shears", "nt-shear-srgm-hcl", "sh-srgm-line"), ("shears", "nt-shear-srgm-cl", "sh-srgm-line"),
        ("ttmc", "tt-q11-mech", "sh-flywheel"),
    ],
    "sheet-metal-shears": [
        ("ttmc", "tt-ps", "sh-light"), ("ttmc", "tt-hq01", "sh-light"), ("ttmc", "tt-bq01", "sh-light"),
        ("ttmc", "tt-q11", "sh-electric"), ("ttmc", "tt-q11nc", "sh-electric"),
        ("ttmc", "tt-ps1220", "sh-slit"),
    ],
}

# (slug, title, hero image, blurb, nav label, line)
SUBPAGES = [
    ("hydraulic-shearing-machine", "Hydraulic shears — swing beam and guillotine plate shears, 12 ga to 1-9/16″", "dn-das-1",
     "The plate shears: swing beam shears from 12 ga to 3/4″ and variable-rake guillotines to 1-9/16″ over 26 ft, in a premium line made in Turkey (BS / BSY, DAS CNC) and NovoTech's value line (QC12K, Q11K) with Estun controls, plus light hydraulic shears for the sheet-metal shop.",
     "Hydraulic shears", ""),
    ("mechanical-guillotine-shear", "Mechanical guillotine shears — direct-gear and flywheel, 1/8″ to 3/8″", "sm-srgm",
     "No hydraulics: the premium-line SRGM direct-gear guillotines, 1/8″ and 1/4″ to 13.8 ft at 31 – 35 strokes a minute, with return-to-sender and cut-to-length versions, and the value-line flywheel shears to 3/8″.",
     "Mechanical shears", ""),
    ("sheet-metal-shears", "Sheet metal shears — pneumatic, electric, bench and coil machines, 20 to 14 ga", "tt-q11a",
     "The shears for the HVAC, signage and sheet-metal shop: a pneumatic shear on shop air, electric shears with manual or NC back gauge, motorized bench shears and a 48″ coil slitting and cut-to-length machine.",
     "Sheet metal shears", ""),
]


def hub():
    return {"slug": HUB, "label": "All shears", "image": "sm-srgm",
            "blurb": "Hydraulic, mechanical or sheet metal shear? Every shear NovoTech sells in Canada on one page, with the three kinds compared and the capacity table for the whole range."}


def siblings():
    return [(s, nav, title.split(" — ")[0]) for s, title, _, _, nav, _ in SUBPAGES]


def subpages():
    return [(s, t, im, b, nav) for s, t, im, b, nav, _ in SUBPAGES]


def lines():
    return [line for *_, line in SUBPAGES]


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
