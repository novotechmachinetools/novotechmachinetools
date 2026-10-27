#!/usr/bin/env python3
"""NovoTech sheet metal shears page (sheet-metal-shears.html) — the value-line shears for the sheet-metal shop, built in China
by TTMC and sold under NovoTech's name without the supplier's brand — under the shear-cutting hub.  Families in
content/families/ttmc.json, photos from tools/ttmc_photos.py (section 'shears').

    python3 tools/ttmc_photos.py                   # crops from the catalogue page rasters → tools/src-images/ttmc
    python3 tools/ttmc_pages.py                    # families + page + image_map entries (tools/ttmc_keys.txt)
    python3 tools/make_images.py --only $(cat tools/ttmc_keys.txt)
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import shear_nav as SN
import ttmc_data as D
import ttmc_photos as PH
import ttmc_more_data2 as D2   # foot, bench and hand shears (value line, sample photos in section 'ttmc-more')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "ttmc"
BRAND = D.BRAND
PDF_FILE = "files/NovoTech-Sheet-Metal-Shears-2026.pdf"
BRAND_LINE = ("NovoTech's value-line sheet metal shears are built in China to NovoTech's specification and sold under NovoTech's name — "
              "with a CSA-approved panel, a 1-year warranty and parts and service from Mississauga, ON, Canada.")
ORIGIN = {"title": "NovoTech value line — built in China", "text": "Built by a sheet-metal machinery maker that exports shears, press brakes and notchers worldwide; "
          "inspected before shipping, wired for Canadian voltage with a CSA-approved panel, and supported by NovoTech's technicians in Mississauga, ON, Canada."}
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}

PAGE = dict(
    title="NovoTech Sheet Metal Shears, 16 ga to 3/8″ · Value Line",
    meta="Pneumatic shear for 16 ga, hydraulic shears to 1/4″, electric shears with manual or NC back gauge, flywheel mechanical shears to 3/8″, foot, bench and hand shears — 12 to 120″.",
    h1="NovoTech sheet metal shears — pneumatic, hydraulic, electric and mechanical, 16 ga to 3/8″, the value line",
    intro="The shears for the sheet-metal shop — HVAC, ductwork, signage, enclosures, roofing and the general repair shop — where a 10 ft × 1/4″ "
          "plate shear is more machine than the work needs. NovoTech's value-line sheet metal shears are built in China to our specification "
          "and sold under our name: the PS pneumatic shear that cuts 16 ga over 52″ on shop air, the HQ01 light hydraulic shears for 14 ga over "
          "52″ and 16 ga over 98″, the THS and HQ11 hydraulic shears from 12 ga to 1/4″ over 51″ to 120″, the Q11 electric shears with a manual "
          "back gauge and counter or a PLC with motorised back gauge, 14 ga to 5/32″ over 49″ to 100″, and the Q11 flywheel mechanical shears "
          "for medium and thick steel, 1/8″ to 3/8″ at 45 to 55 strokes a minute. Every machine ships with front and back gauges, a foot pedal "
          "and two-edged blades, wired for Canadian voltage with a CSA-approved panel; installed, trained and supported from Mississauga, ON, Canada. "
          "For the shop without power at the shear there are foot shears to 98″, bench shears, lever guillotines, lever shears and bar "
          "cutters for plate and bar, and throatless shears that cut curves. "
          "For plate shears from 5/32″ to 1-9/16″ see the NovoTech hydraulic shears, for the premium direct-gear mechanical shears the "
          "NovoTech mechanical shears, and for every line in one table the shears overview.",
    points=["PS pneumatic shear 16 ga × 52″ on 85 – 100 psi shop air · HQ01 light hydraulic shears 14 ga × 52″ and 16 ga × 98″, 3 HP",
            "THS and HQ11 hydraulic shears 12 ga – 1/4″ × 51 – 120″, 12 – 20 strokes/min, quick-set blade clearance, electric or NC back gauge",
            "Q11 electric shears 14 ga – 5/32″ × 49 – 100″ with manual or PLC / motorised back gauge · Q11 mechanical shears 1/8″ – 3/8″, 45 – 55 strokes/min",
            "Foot shears 20 – 14 ga × 40 – 98″, bench shears, lever guillotines, lever shears and bar cutters to 1/4″ plate and Ø1-1/4″ bar"],
    hero="tt-q11a", minis=["tt-hq11", "tt-ps"],
    groups=[("sh-light", "Pneumatic and light hydraulic shears, 16 – 14 ga", "The lightest powered shears in the range: the PS on shop air and the HQ01 with a 3 HP power pack — for ductwork, signage and light sheet.", BRAND),
            ("sh-hydraulic", "Hydraulic shears, 12 ga to 1/4″", "The THS with front and back gauges and the HQ11 with quick-set blade clearance and an electric or NC back gauge — 51″ to 120″.", BRAND),
            ("sh-electric", "Electric shears, 14 ga to 5/32″", "A motor and gearbox drive the beam — no hydraulics: the Q11 with manual back gauge and counter, and the Q11 NC with a PLC touch-screen and motorised back gauge.", BRAND),
            ("sh-mechanical", "Mechanical shears to 3/8″", "The classic flywheel shear for medium and thick steel: 45 to 55 strokes a minute, 1/8″ to 3/8″ over 39″ to 98″.", BRAND),
            ("sh-manual", "Foot, bench and hand shears", "No motor needed: foot shears to 98″, bench shears, lever guillotines, lever shears for plate and bar, bar cutters and throatless shears.", BRAND)],
    faq=[{"q": "Pneumatic, hydraulic, electric or mechanical — which shear for a small shop?",
          "a": "By the sheet you cut and what you already have. If the shop runs compressed air and cuts 16 ga and lighter — ductwork, flashing, signage — the PS pneumatic shear is the simplest machine: no motor, no oil, 40 strokes a minute. For 14 ga to 1/4″ the hydraulic shears (HQ01, THS, HQ11) give a smooth, quiet cut with hydraulic hold-downs and the lowest price per inch of blade. The electric Q11 cuts the same 14 ga to 5/32″ through a gearbox with nothing to warm up and 30 strokes a minute, and the NC version adds a PLC and motorised back gauge for repeat parts. The flywheel mechanical shears are the fastest — 45 to 55 strokes a minute — and go to 3/8″ for the shop that cuts heavier bar and plate."},
         {"q": "Which length — 52″, 79″, 98″ or 120″?",
          "a": "The model number is the maximum shearing width in millimetres: 1250 / 1300 / 1320 = 49 – 52″ (a 4 ft sheet cut across), 1500 / 1520 = 59 – 60″, 2000 / 2050 = 79 – 81″, 2500 / 2550 = 98 – 100″ (a 4 × 8 sheet cut lengthwise), 3050 = 120″ (5 × 10 sheet). Most HVAC and signage shops are well served by a 52″ or 98″ machine; buy the 120″ if you cut 5 × 10 sheet."},
         {"q": "How is the capacity rated, and what about stainless and aluminum?",
          "a": "Capacities are the manufacturer's ratings for mild steel over the full blade length: 16 ga (1.5 – 1.6 mm) on the PS and the HQ01-1.6x2500B, 14 ga (2 mm) on the HQ01-2x1320B and the Q11-2x…, 12 ga on the THS-1320X2.5, 1/8″ (3 mm) and 5/32″ (4 mm) on the THS X4, Q11 and Q11 NC, 3/16″ and 1/4″ on the HQ11, 3/8″ on the Q11-10x…. Stainless steel shears at about 60 % of the mild-steel thickness — 16 ga stainless on a 14 ga machine, 11 ga on a 1/4″ machine; aluminum to the full rated thickness and more."},
         {"q": "What does the A model add — Q11-3x1250A?",
          "a": "A light-curtain rear guard instead of a fence, so nobody reaches into the rear of the shear while it cycles, a pneumatic sheet catcher behind the blade and a front sheet pallet for stacking the cut blanks — the Q11 set up for a production station rather than a cut-now-and-then shear. The light curtain and catcher are options on the other Q11 models; the NC machines have an interlocked rear guard and the pneumatic catcher as standard."},
         {"q": "Manual, electric or NC back gauge?",
          "a": "The back gauge is the stop behind the blade that sets the width of the cut strip. A manual gauge with a millimetre counter (Q11, THS, HQ01) is wound to the dimension by hand — fine for a few set-ups a day. An electric back gauge (HQ11-6.5x1300 and 3050, optional on the Q11) moves under power from a switch. The NC machines (Q11 NC, optional on the HQ11) take the dimension from a touch-screen PLC and position the gauge themselves, with programs for the parts you cut every week; 24.8″ (630 mm) of travel is standard, 36.2″ (920 mm) on the HQ11-6.5x3050."},
         {"q": "Are the flywheel shears safe to run?",
          "a": "The Q11 mechanical shears make one stroke per pedal press — the clutch engages for one revolution and the beam stops at the top — and are supplied with mechanical hold-downs, a finger guard along the blade and the CSA-approved panel; a rear guard with photocell and front sheet supports are options we recommend for every machine. In Ontario a new shear needs a pre-start health and safety review (PSR) under Regulation 851 before it runs; NovoTech prepares the documentation for it."},
         {"q": "How do these compare with the premium SRGM shears and the hydraulic value line?",
          "a": "The NovoTech mechanical shears (SRGM) are the premium direct-gear machines from Turkey — heavier, 31 to 35 strokes a minute, NC back gauge and photocell guard as standard — for the shop that shears all day. The NovoTech hydraulic shears (QC12K / Q11K) are plate shears from 5/32″ to 1-9/16″ over 8 to 26 ft with Estun controls. The sheet metal shears on this page are the smaller, lower-priced machines for sheet to 1/4″ and widths to 120″ — the same NovoTech installation, warranty and support. The comparison and the capacity table for every line are on the shears overview."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about sheet metal shears",
    related_pages=[{"href": "compact-hydraulic-press-brakes.html", "label": "Compact hydraulic press brakes"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                   {"href": "bead-rollers.html", "label": "Bead rollers"}, {"href": "circle-cutters-and-seamers.html", "label": "Circle shears & flanging machines"},
                   {"href": "plate-rollers.html", "label": "Plate rollers"}],
    related_title="More sheet-metal machinery from NovoTech",
)


def pdf_entry(file=PDF_FILE, label="Download the sheet metal shears brochure"):
    f = os.path.join(ROOT, "src", file)
    if not os.path.exists(f):
        return None
    return {"file": file, "label": label, "size": f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units"}


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "ttmc")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/ttmc/{key}{ext}", "alt": p["alt"], "section": "shears", "trim": False, "quality": 82, "cutout": bool(p.get("cutout"))}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "ttmc_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    pdf = pdf_entry()
    fams = [dict(f, pdf=pdf) for f in D.FAMILIES] + [dict(f) for f in D2.SHEAR]
    write_families(SET, fams)
    write_category(D.P_SHEAR, PAGE, fams, SET, SN.SECTION, hub=SN.hub(), siblings=SN.siblings(),
                   extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, "catalogue_pdf": pdf, "nav_label": "NovoTech sheet metal shears", **NO_VIDEO})
    path = os.path.join(ROOT, "content", "pages", f"{D.P_SHEAR}.json")
    page = json.load(open(path, encoding="utf-8"))
    for g in page["groups"]:
        if g["id"] == "sh-manual-group":
            g["tagline"] = D2.MANUAL_TAG if hasattr(D2, "MANUAL_TAG") else None
    json.dump(page, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    keys = register_images()
    used = {k for f in FAMILIES_IMAGES() for k in f} | {PAGE["hero"]} | set(PAGE["minis"])     # the manual shears' photos are registered by ttmc_more_pages.py
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on the page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    print(f"sheet metal shears page · families: {len(fams)} · models: {sum(len(f['specs']['models']) for f in fams)} · images: {len(keys)}")


def FAMILIES_IMAGES():
    return [f["images"] for f in D.FAMILIES]


if __name__ == "__main__":
    build()
