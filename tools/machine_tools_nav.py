#!/usr/bin/env python3
"""The CNC machine-tool section: one hub (cnc-machine-tools.html) over four product pages, one per line — the three Dener
pages (premium line, made in Turkey) and NovoTech's value-line CNC machine tools (built in China).  Shared by
tools/dener_mt_pages.py, tools/ttmc_more_pages.py (section nav + related links) and tools/machine_tools_hub.py (the hub)."""

HUB = "cnc-machine-tools"
SECTION = "CNC machine tools"
RELATED_TITLE = "More CNC machine tools from NovoTech"
# (slug, title, hero image, blurb, nav label, line)
SUBPAGES = [
    ("dener-cnc-lathes", "Dener CNC lathes — TTC and TTH slant-bed lathes, 6″ to 12″ chucks", "dn-ttc-1",
     "The premium line, made in Turkey: 45° slant-bed CNC lathes with Fanuc control, 12-station servo turrets and hydraulic tailstocks — the "
     "compact TTC-6 and TTC-8 and the TTH-8, TTH-10 and TTH-12 with a Ø27.6″ swing, a 12″ chuck and 4.65″ spindle bore on the largest. "
     "C-axis turrets with live tools to order.",
     "Dener CNC lathes", "premium"),
    ("dener-machining-centres", "Dener machining centres — TMC vertical and TDC double-column, BBT40 and BBT50", "dn-tmc-1",
     "The premium line, made in Turkey: TMC vertical machining centres from 33.5 to 63″ X travel with a 10,000 rpm BBT40 spindle and 24 tools, "
     "and TDC double-column machining centres from 82.7 to 161.4″ with a BBT50 spindle and tables for 26,455 lb.",
     "Dener machining centres", "premium"),
    ("dener-surface-grinders", "Dener surface grinder — TGH-B 450 NC surface grinding machine", "dn-tgh-1",
     "The premium line, made in Turkey: a precision NC surface grinder with a 17.7 × 35.4″ table, a 15.7 × 31.5″ electromagnetic chuck, "
     "hydraulic table drive and Mitsubishi NC down and cross feed in 0.00004″ steps.",
     "Dener surface grinders", "premium"),
    ("novotech-cnc-machine-tools", "NovoTech CNC machine tools — CNC lathe, vertical machining centres and boring mills · value line", "tm-vmc10562",
     "NovoTech's own brand, built in China to our specification with Mitsubishi, Fanuc or Siemens controls: the CTK6416 slant-bed lathe, "
     "VMC8046 and VMC10562 vertical machining centres, BT50 CNC boring and milling machines, the TH-800 horizontal machining centre and "
     "slot machining centres.",
     "NovoTech CNC machine tools", "value"),
]


def hub():
    return {"slug": HUB, "label": "All CNC machine tools", "image": "dn-tmc-1",
            "blurb": "Every CNC lathe, machining centre and surface grinder NovoTech sells — Dener premium and NovoTech value lines — on one "
                     "page, with the whole range in one table."}


def siblings():
    return [(s, nav, title.split(" — ")[0]) for s, title, _, _, nav, _ in SUBPAGES]


def subpages():
    return [(s, t, im, b, nav) for s, t, im, b, nav, _ in SUBPAGES]


def lines():
    return [line for *_, line in SUBPAGES]
