#!/usr/bin/env python3
"""The press-brake section: one hub (press-brake.html) over three product pages, each with its own line.  Shared by
tools/dener_pages.py, tools/vl_sheet_pages.py, tools/isitan_pressbrake.py (section nav + related links) and
tools/press_brake_hub.py (the hub itself)."""

HUB = "press-brake"
SECTION = "Press brakes"
# (slug, title, hero image, blurb, nav label, line)
SUBPAGES = [
    ("dener-cnc-press-brakes", "Dener CNC press brakes — hydraulic, hybrid and servo-electric", "dn-xl-1",
     "The premium line, made in Turkey: XL hydraulic brakes in 18 models to 661 US tons and 20 ft, the XH hybrid with a servo pump, the DDM servo-electric to 220 tons and the DDS ball-screw brake from 22 tons.",
     "Dener CNC press brakes", "premium"),
    ("novotech-cnc-press-brakes", "NovoTech CNC press brakes — hydraulic and electric · value line", "vl-wad-1",
     "NovoTech's own brand, built in China to our specification with Delem, Hawe and Estun: hydraulic CNC brakes 55 – 331 tons, heavy-duty to 1,323 tons, electric servo brakes 3 – 176 tons and NC torsion-bar brakes from 33 tons.",
     "NovoTech CNC press brakes", "value"),
    ("compact-hydraulic-press-brakes", "Compact hydraulic press brakes — İşitan Edgebender, 33 to 66 tons", "is-eb-1240-cnc",
     "The press brake for a sheet-metal shop rather than a steel-fabrication plant: 4.2 to 6.9 ft, 33 to 66 US tons, 2-axis NC or 3-axis CNC with Cybelec control, made in Turkey.",
     "Compact hydraulic press brakes", ""),
]


def hub():
    return {"slug": HUB, "label": "All press brakes", "image": "dn-xl-1",
            "blurb": "Every press brake NovoTech sells — Dener, NovoTech value line and İşitan — on one page, with the capacity table for the whole range."}


def siblings():
    return [(s, nav, title.split(" — ")[0]) for s, title, _, _, nav, _ in SUBPAGES]
