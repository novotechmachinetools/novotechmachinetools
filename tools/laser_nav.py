#!/usr/bin/env python3
"""The two laser sections, each a hub over one page per line: sheet lasers (laser-cutting-machine.html → Dener fiber lasers,
Senfeng fiber lasers) and tube lasers (tube-laser-cutting-machine.html → Dener tube lasers, Senfeng tube lasers).  Shared by
tools/dener_pages.py and tools/senfeng_pages.py (section nav + related links) and tools/laser_hub.py (the hubs)."""

# kind: dict(hub slug, section label, hub label, hub image, hub blurb, subpages=[(slug, title, hero image, blurb, nav label, line)])
SECTIONS = {
    "sheet": dict(
        hub="laser-cutting-machine", section="Sheet laser cutters", label="All sheet lasers", image="dn-gfl-3",
        blurb="Every fiber laser NovoTech sells for sheet and plate — Dener and Senfeng — on one page, with the working area, power and speed of the whole range in one table.",
        subpages=[
            ("dener-fiber-lasers", "Dener fiber lasers — GFL production lasers and the Smart series, 3 to 40 kW", "dn-gfl-3",
             "The premium line, made in Turkey: the GFL with a 1.5 G gantry and pallet changer in 5 × 10 to 6.6 × 20 ft, and the Smart series — closed-type with double table to 41 ft, semi-closed single tables to 13 × 82 ft and the open-type entry machine — with IPG, Raycus or nLIGHT sources and Precitec heads.",
             "Dener fiber lasers", "premium"),
            ("senfeng-fiber-lasers", "Senfeng fiber lasers — compact, open-type, H series, plate, 3D and coil-fed · value line", "sf-h-1",
             "The value line under its own brand: single-table compact lasers from 4 × 4 ft, the NP open-type to 12 kW, the enclosed H series with pallet changer to 80 kW, sheet-and-tube combination lasers, plate gantries to 10 × 164 ft with bevel heads, 3D lasers and coil-fed lines.",
             "Senfeng fiber lasers", "value"),
        ]),
    "tube": dict(
        hub="tube-laser-cutting-machine", section="Tube laser cutters", label="All tube lasers", image="dn-tube-2",
        blurb="Every tube and profile laser NovoTech sells — Dener and Senfeng — on one page, with the tube range, power, speed and bar length of the whole range in one table.",
        subpages=[
            ("dener-tube-lasers", "Dener tube lasers — E-FTL and FTL, Ø0.3″ to 25.2″, 3 to 20 kW", "dn-tube-2",
             "The premium line, made in Turkey: the E-FTL with 1 G servo chucks for tube from Ø0.3″ to 13.8″ and the heavy FTL for structural tube, pipe and beams to Ø25.2″ and 12 m bars of 2,600 kg — bundle loaders, following supports and bevel heads.",
             "Dener tube lasers", "premium"),
            ("senfeng-tube-lasers", "Senfeng tube lasers — T, PLUS, GT, NT, ST and HT, Ø0.5″ to 25″ · value line", "sf-t-1",
             "The value line under its own brand: two-chuck T series lasers from Ø0.5″ and 1.5 kW, the high-speed PLUS and 45° bevel GT, the zero-tailing NT and the three- and four-chuck ST / HT machines to Ø25″, 6,600 lb and 49 ft, plus the H-beam profile line.",
             "Senfeng tube lasers", "value"),
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
