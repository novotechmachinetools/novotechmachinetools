#!/usr/bin/env python3
"""The three shear pages, one per kind of machine — hydraulic-shearing-machine.html, mechanical-guillotine-shear.html and
sheet-metal-shears.html — under the shear hub.  Each page holds every family of that kind NovoTech sells, premium and value
lines as sections, with the spec tables, photos, videos and brochures of the families (family set content/families/all-shears.json,
merged by tools/shear_hub.py — run that first):

    python3 tools/shear_hub.py && python3 tools/shear_types.py

The pages replace the supplier pages dener-shears and novotech-mechanical-shears (301s in src/root/.htaccess) and take over
the hydraulic-shearing-machine and sheet-metal-shears URLs: buyers search for the kind of machine, not the supplier
(reports/ساختار صفحات محصول و سئو.md).  The FAQ answers of the former pages are kept in tools/shear_copy.json."""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category
import shear_nav as SN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "all-shears"
COPY = json.load(open(os.path.join(ROOT, "tools", "shear_copy.json"), encoding="utf-8"))

BRAND_LINE = ("The premium hydraulic shears are built by Dener Makina in Kayseri, Turkey, and the premium mechanical shears in Turkey with European motors and electrics; "
              "NovoTech's value-line shears are built in China to our specification with Estun controls and Rexroth hydraulics. All sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Premium and value lines, one supplier", "text": "Every shear comes with a CSA-approved panel, a 1-year warranty and blades, parts and technicians in Mississauga, ON, Canada — whichever line you choose."}
RANGE = {"range_pick": [["capacity", "capacity_mild_steel"], ["length", "working_width"], "strokes", ["motor", "operation"], "weight"],
         "range_cols": ["Capacity (mild steel)", "Shearing length", "Strokes / min", "Motor", "Weight"]}


def faq(page, *questions):
    """FAQ entries of a former page by (the start of) their question"""
    out = []
    for q in questions:
        hit = next((f for f in COPY[page]["faq"] if f["q"].startswith(q)), None)
        if not hit:
            raise SystemExit(f"FAQ not found on {page}: {q}")
        out.append(hit)
    return out


HYDRAULIC = dict(
    title="Hydraulic Shears for Sale in Canada — Swing Beam & Guillotine Plate Shears, 12 ga to 1-9/16″ | NovoTech",
    meta="Hydraulic shearing machines sold, installed and supported in Canada: swing beam shears 12 ga – 3/4″ × 4 – 20 ft, variable-rake guillotines 1/4″ – 1-9/16″ × 8 – 26 ft, CNC shears with ESA control — premium line made in Turkey and NovoTech's value line, CSA panels. Every model in one table.",
    h1="Hydraulic shears — swing beam and guillotine plate shears, 12 ga to 1-9/16″",
    intro="A hydraulic shear cuts sheet and plate to size in one stroke between a fixed lower blade and a moving upper blade driven by two "
          "hydraulic cylinders; the back gauge sets the width, hydraulic hold-downs keep the sheet flat and the control counts the strokes. "
          "It is the shear for plate — from 12 ga to 1-9/16″ and 26 ft here — where tonnage matters more than strokes per minute. NovoTech "
          "sells three kinds in Canada, all on this page: swing beam shears, the rugged everyday plate shear with the beam swung through the "
          "cut on two bearings — the premium BS / BSY to 5/8″ over 13.5 ft and the value-line QC12K from 5/32″ to 3/4″ over 20 ft; guillotine "
          "shears with a variable rake angle on a beam carried straight down on rollers, so thin sheet is cut flat and 3/4″ plate with less "
          "distortion — the premium DAS CNC to 3/4″ × 20 ft with the ESA 630 control and the value-line Q11K to 1-9/16″ × 26 ft; and light "
          "hydraulic shears from 12 ga to 1/4″ over 51 – 120″ for the sheet-metal shop. Every model is in the table below with its capacity, "
          "length, strokes, motor and weight, then each family with its full specification and photos. Every machine comes with a CSA-approved "
          "panel and a 1-year warranty, installed, trained and supported from Mississauga, ON, Canada. For sheet to 1/4″ all day with no "
          "hydraulics, see the mechanical guillotine shears; for 20 – 14 ga, the sheet metal shears.",
    points=["Swing beam: premium BS / BSY 1/4″ – 5/8″ × 6.8 – 13.5 ft with NC back gauge; value QC12K 5/32″ – 3/4″ × 8 – 20 ft with Estun E21S",
            "Guillotine: premium DAS CNC 1/4″ – 3/4″ × 10 – 20 ft, variable angle, ESA 630, 1 m ball-screw gauge; value Q11K 1/4″ – 1-9/16″ × 8 – 26 ft",
            "Light hydraulic shears 12 ga – 1/4″ × 51 – 120″, 12 – 20 strokes/min, quick-set blade clearance, electric or NC back gauge"],
    hero="dn-das-1", minis=["vl-qc12k-1", "tt-hq11"],
    groups=[("sh-premium-swing", "Swing beam shears · premium line", "BS / BSY: a beam on two bearings swung through the cut by two cylinders, 8 to 22 strokes a minute, NC back gauge, hydraulic hold-downs and single-point blade-gap adjustment — 1/4″ to 5/8″ over 6.8 to 13.5 ft."),
            ("sh-premium-cnc", "CNC guillotine shears · premium line", "DAS: a beam on linear rollers with a variable cutting angle set by the ESA 630 CNC from the thickness keyed in — 1/4″ to 3/4″ over 10, 13 and 20 ft, for production."),
            ("sh-value-swing", "Swing beam shears · value line", "QC12K: NovoTech's own everyday plate shear with Estun E21S control, Rexroth hydraulics and a motorised back gauge — 5/32″ to 3/4″ over 8 to 20 ft."),
            ("sh-value-guillotine", "Guillotine shears · value line", "Q11K: variable rake angle and blade gap from the control, 1/4″ to 1-9/16″ over 8 to 26 ft — the value-line machine for thick plate."),
            ("sh-light-hydraulic", "Light hydraulic shears · value line", "THS and HQ11: hydraulic shears from 12 ga to 1/4″ over 51 to 120″ with quick-set blade clearance and an electric or NC back gauge — for the sheet-metal shop.")],
    faq=[faq("hydraulic-shearing-machine", "Swing beam or guillotine shear?")[0],
         {"q": "Premium line or value line?",
          "a": "The premium BS / BSY and DAS shears are built by Dener in Turkey with Rexroth or Hoerbiger hydraulics, ESA or Delem controls, the heaviest frames and parts stocked in Canada — the machines for two shifts a day and the tightest, flattest cut, with the DAS CNC setting rake, gap and gauge from the material keyed in. NovoTech's value-line QC12K and Q11K are the same two designs — swing beam and variable-rake guillotine — built in China to our specification with Estun controls, Rexroth hydraulics and Siemens motors at about two-thirds of the price, in more sizes (to 1-9/16″ and 26 ft). Both lines are installed and supported by the same NovoTech technicians, and the light hydraulic shears below them are the value-line answer for 12 ga to 1/4″."},
         faq("hydraulic-shearing-machine", "What thickness and length do I need?")[0],
         faq("dener-shears", "Which control?")[0],
         faq("hydraulic-shearing-machine", "What does the Estun E21S control do?")[0],
         faq("dener-shears", "What is standard on a Dener shear?")[0],
         faq("hydraulic-shearing-machine", "How is the sheet supported?")[0],
         faq("dener-shears", "Floor space and power?")[0],
         faq("shear-cutting", "What about safety and the Ontario pre-start review?")[0],
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about hydraulic shears",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "laser-cutting-machine.html", "label": "Sheet laser cutters"},
                   {"href": "plate-rollers.html", "label": "Plate rollers"}, {"href": "ironworker-machines.html", "label": "Hydraulic ironworkers"}],
    related_title="More cutting and forming machinery from NovoTech",
)

MECHANICAL = dict(
    title="Mechanical Guillotine Shears for Sale in Canada — Direct-Gear & Flywheel, 1/8″ to 3/8″ | NovoTech",
    meta="Mechanical shearing machines sold, installed and supported in Canada: direct-gear SRGM guillotine shears, 1/8″ and 1/4″ from 43″ to 13.8 ft at 31 – 35 strokes a minute, return-to-sender and cut-to-length versions, and flywheel shears to 3/8″ — no hydraulics. Every model in one table.",
    h1="Mechanical guillotine shears — direct-gear and flywheel, 1/8″ to 3/8″",
    intro="A mechanical shear drives the cutting beam from a motor instead of hydraulic cylinders — through a gearbox and crank (direct gear) "
          "or a flywheel and clutch — so there is no hydraulic power pack to leak or warm up, the cut is the same on the first and the "
          "thousandth stroke, and the machine runs 31 to 55 strokes a minute: the shear for sheet and light plate all day. NovoTech sells two "
          "kinds in Canada, both on this page: the premium-line SRGM direct-gear guillotines, built in Turkey with European motors, gearboxes "
          "and electrics — the light-type SRGM-H for 1/8″ mild steel and the SRGM for 1/4″ from 43″ to 13.8 ft, the SRGM-HFR / FR with a "
          "return-to-sender sheet support that brings the cut piece back to the operator, and the SRGM-HCL / CL built into cut-to-length coil "
          "lines; and the value-line Q11 flywheel shears for medium and thick steel, 1/8″ to 3/8″ at 45 to 55 strokes a minute. Every model "
          "is in the table below with its capacity, length, strokes, motor and weight, then each family with its full specification and "
          "photos. Every machine comes with a CSA-approved panel and a 1-year warranty, installed, trained and supported from Mississauga, ON, "
          "Canada. For plate from 3/8″ up see the hydraulic shears; for 20 – 14 ga the sheet metal shears.",
    points=["SRGM-H light type, 1/8″ × 3.6 – 10 ft, 35 strokes/min · SRGM standard, 1/4″ × 3.6 – 13.8 ft, 31 strokes/min — premium line, made in Turkey",
            "SRGM-HFR / SRGM-FR with return-to-sender: the cut blank comes back to the front, off-cuts drop to the rear; SRGM-HCL / CL for cut-to-length coil lines",
            "Value-line Q11 flywheel mechanical shears, 1/8″ – 3/8″ × 49 – 100″, 45 – 55 strokes/min"],
    hero="sm-srgm", minis=["sm-srgm-fr", "tt-q11-6x2000"],
    groups=[("sh-srgm", "Direct-gear mechanical guillotine shears · premium line", "SRGM-H and SRGM: a 4 to 15 HP motor drives the cutting beam through a gearbox and crank — 1/8″ and 1/4″ from 43″ to 13.8 ft, welded frame, beam in teflon slideways."),
            ("sh-srgm-return", "Guillotine shears with return-to-sender · premium line", "SRGM-HFR and SRGM-FR: a sheet support behind the blade tilts and brings the cut blank back to the operator; off-cuts drop to the rear."),
            ("sh-srgm-line", "Shears for cut-to-length lines · premium line", "SRGM-HCL and SRGM-CL: the same shears built into coil cut-to-length lines, with the line control and sheet stacker."),
            ("sh-flywheel", "Flywheel mechanical shears · value line", "Q11: a flywheel and clutch drive the beam for medium and thick steel, 1/8″ to 3/8″ at 45 – 55 strokes a minute, built in China to our specification.")],
    faq=faq("novotech-mechanical-shears", "Mechanical or hydraulic shear", "What does direct-gear mean?", "How is the capacity rated", "Which length do I need", "What is the back gauge", "What does return-to-sender do?", "How long do the blades last", "Can it cut at an angle?")
        + faq("sheet-metal-shears", "Are the flywheel shears safe to run?") + [VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about mechanical shears",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                   {"href": "circle-cutters-and-seamers.html", "label": "Circle shears & flanging machines"}, {"href": "folder-sheet-metal-brake.html", "label": "Sheet metal brakes"}],
    related_title="More sheet-metal cutting and forming machinery from NovoTech",
)

SHEET = dict(
    title="Sheet Metal Shears for Sale in Canada — Pneumatic, Electric, Bench & Coil Machines, 20 to 14 ga | NovoTech",
    meta="Sheet metal shears sold, installed and supported in Canada: a pneumatic shear for 16 ga × 52″ on shop air, electric shears 14 ga – 5/32″ × 49 – 100″ with manual or NC back gauge, motorized bench shears and a 48″ coil slitting and cut-to-length machine. Every model in one table.",
    h1="Sheet metal shears — pneumatic, electric, bench and coil machines, 20 to 14 ga",
    intro="A sheet metal shear is the light shear for the HVAC, ductwork, signage, enclosure, roofing and repair shop — where a 10 ft × 1/4″ "
          "plate shear is more machine than the work needs — cutting 20 to 14 ga sheet to size between two blades from a pneumatic cylinder, "
          "an electric motor or a hand lever. NovoTech sells three kinds in Canada, all on this page: the PS pneumatic shear that cuts 16 ga "
          "over 52″ on 85 – 100 psi shop air, the HQ01 light hydraulic shears for 14 ga over 52″ and 16 ga over 98″, and the EBQ01 motorized "
          "bench shears for 18 ga × 26″ and 20 ga × 41″; the Q11 electric shears with a manual back gauge and counter or a PLC with motorised "
          "back gauge, 14 ga to 5/32″ over 49″ to 100″; and the PS-1220 coil slitting and cut-to-length machine that turns 16 ga × 48″ coil "
          "into blanks and strips. Every machine ships with front and back gauges, a foot pedal and two-edged blades, wired for Canadian voltage "
          "with a CSA-approved panel; installed, trained and supported from Mississauga, ON, Canada. For 1/8″ and 1/4″ all day see the "
          "mechanical guillotine shears; for plate, the hydraulic shears.",
    points=["PS pneumatic shear 16 ga × 52″ on 85 – 100 psi shop air · HQ01 light hydraulic shears 14 ga × 52″ and 16 ga × 98″, 3 HP · EBQ01 bench shears 18 ga × 26″, 20 ga × 41″",
            "Q11 electric shears 14 ga – 5/32″ × 49 – 100″ with manual or PLC / motorised back gauge, 25 strokes/min",
            "PS-1220×1.5GT coil slitting and cut-to-length machine, 16 ga × 48″ — blanks and strips straight from the coil"],
    hero="tt-q11a", minis=["tt-ps", "tm-ps1220"],
    groups=[("sh-light", "Pneumatic, light hydraulic and bench shears, 20 – 14 ga", "The PS pneumatic shear on shop air, the HQ01 light hydraulic shears and the EBQ01 motorized bench shears — the lowest-priced powered shears."),
            ("sh-electric", "Electric shears, 14 ga to 5/32″", "Q11 electric shears with a manual back gauge and counter, or a PLC with motorised back gauge on the NC models, 49 to 100″."),
            ("sh-slit", "Coil slitting and cut-to-length machine", "The PS-1220×1.5GT decoils, slits and cuts 16 ga × 48″ coil to length — blanks and strips for the duct and panel shop.")],
    faq=faq("sheet-metal-shears", "Pneumatic, hydraulic, electric or mechanical", "Which length — 52″", "How is the capacity rated", "What does the A model add", "Manual, electric or NC back gauge?", "When is a coil slitter worth it?") + [VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about sheet metal shears",
    related_pages=[{"href": "folder-sheet-metal-brake.html", "label": "Sheet metal brakes"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                   {"href": "lock-former.html", "label": "Lock formers and HVAC machines"}, {"href": "bead-rollers.html", "label": "Bead rollers"}],
    related_title="More sheet-metal machinery from NovoTech",
)

VIDEOS = {
    "hydraulic-shearing-machine": COPY["dener-shears"],
    "mechanical-guillotine-shear": COPY["novotech-mechanical-shears"],
    "sheet-metal-shears": COPY["sheet-metal-shears"],
}


def build():
    fs = json.load(open(os.path.join(ROOT, "content", "families", f"{SET}.json"), encoding="utf-8"))
    fams = {fid: dict(fs["families"][fid], id=fid) for fid in fs["order"]}
    manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
    for slug, page in (("hydraulic-shearing-machine", HYDRAULIC), ("mechanical-guillotine-shear", MECHANICAL), ("sheet-metal-shears", SHEET)):
        members = [dict(fams[fid], group=g) for _, fid, g in SN.PAGES[slug]]
        pdfs, seen = [], set()
        for f in members:
            pd = f.get("pdf")
            if pd and pd["file"] not in seen:
                seen.add(pd["file"]); pdfs.append(pd)
        n = sum(len(f["specs"]["models"]) for f in members)
        v = VIDEOS[slug]
        video = {k: v.get(k) for k in ("intro_video", "intro_video_heading", "intro_video_text")} if v.get("intro_video") and v["intro_video"]["thumb"] in manifest else {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}
        for k in ("hero", "minis"):
            keys = [page[k]] if k == "hero" else page[k]
            missing = [x for x in keys if x not in manifest]
            if missing:
                raise SystemExit(f"{slug}: image keys not in manifest: {missing}")
        write_category(slug, page, members, SET, SN.SECTION, hub=SN.hub(), siblings=SN.siblings(),
                       extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **video,
                              "nav_label": next(nav for s, _, _, _, nav, _ in SN.SUBPAGES if s == slug),
                              "catalogue_pdf": None, "catalogue_pdfs": pdfs, **RANGE,
                              "range_lead": f"Every model on this page in one table — {n} machines: mild-steel capacity, shearing length, strokes per minute, motor and weight. Each row links to the full specification below.",
                              "range_caption": f"{page['h1'].split(' — ')[0]} supplied by NovoTech — premium and value lines", "range_title": "Every model at a glance"})
        print(f"{slug}: {len(members)} families, {n} models, {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
