#!/usr/bin/env python3
"""The shear section: one hub (shear-cutting.html) over four product pages, one per line.  Shared by tools/dener_pages.py,
tools/saymak_pages.py, tools/vl_sheet_pages.py, tools/ttmc_pages.py (section nav + related links) and tools/shear_hub.py."""

HUB = "shear-cutting"
SECTION = "Shears"
# (slug, title, hero image, blurb, nav label, line)
SUBPAGES = [
    ("dener-shears", "Dener hydraulic shears — BS / BSY swing beam and DAS CNC guillotine, 1/4″ to 3/4″", "dn-das-1",
     "The premium line, made in Turkey: BS / BSY hydraulic swing beam shears with NC back gauge, 1/4″ to 5/8″ over 6.8 to 13.5 ft, and the DAS CNC guillotine shears with variable cutting angle, 1/4″ to 3/4″ over 10 to 20 ft, with Dener Canada parts in Mississauga, ON, Canada.",
     "Dener hydraulic shears", "premium"),
    ("novotech-mechanical-shears", "NovoTech mechanical guillotine shears — direct-gear SRGM, 1/8″ and 1/4″ · premium line", "sm-srgm",
     "NovoTech's premium-line mechanical shears, built in Turkey: a motor and gearbox drive the beam — no hydraulics, no flywheel clutch — for 31 to 35 strokes a minute in 1/8″ sheet to 10 ft and 1/4″ plate to 13.8 ft, with return-to-sender and cut-to-length versions.",
     "NovoTech mechanical shears", "premium"),
    ("hydraulic-shearing-machine", "NovoTech hydraulic shears — QC12K swing beam and Q11K guillotine, 5/32″ to 1-9/16″ · value line", "vl-qc12k-1",
     "NovoTech's own value-line plate shears, built in China with Estun controls and Rexroth hydraulics: QC12K swing beam shears from 5/32″ to 3/4″ over 8 to 20 ft and Q11K variable-rake guillotines from 1/4″ to 1-9/16″ over 8 to 26 ft.",
     "NovoTech hydraulic shears", "value"),
    ("sheet-metal-shears", "NovoTech sheet metal shears — pneumatic, hydraulic, electric and mechanical, 16 ga to 3/8″ · value line", "tt-q11a",
     "The value-line shears for the sheet-metal shop, built in China to NovoTech's specification: a pneumatic shear for 16 ga, light and production hydraulic shears to 1/4″, electric shears with manual or NC back gauge, flywheel mechanical shears to 3/8″, motorized bench shears and a 48″ coil slitting and cut-to-length machine.",
     "NovoTech sheet metal shears", "value"),
]


def hub():
    return {"slug": HUB, "label": "All shears", "image": "sm-srgm",
            "blurb": "Every metal shear NovoTech sells — Dener, NovoTech premium and value lines — on one page, with the capacity table for the whole range."}


def siblings():
    return [(s, nav, title.split(" — ")[0]) for s, title, _, _, nav, _ in SUBPAGES]


def subpages():
    return [(s, t, im, b, nav) for s, t, im, b, nav, _ in SUBPAGES]


def lines():
    return [line for *_, line in SUBPAGES]
