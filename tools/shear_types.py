#!/usr/bin/env python3
"""The two shear pages, one per kind of machine — hydraulic-shearing-machine.html and mechanical-guillotine-shear.html — under
the shear hub.  Each page holds every family of that kind NovoTech sells, premium and value lines as sections, with the spec
tables, photos, videos and brochures of the families (family set content/families/all-shears.json, merged by tools/shear_hub.py
— run that first):

    python3 tools/shear_hub.py && python3 tools/shear_types.py

The pages replace the supplier pages dener-shears and novotech-mechanical-shears (301s in src/root/.htaccess) and take over
the hydraulic-shearing-machine URL: buyers search for the kind of machine, not the supplier (reports/ساختار صفحات محصول و
سئو.md).  The sheet-metal-shears page was merged into the two (the owner, Nov 7 2026): the HQ01 light hydraulic shears at the
bottom of the hydraulic page; the electric, NC electric and bench shears and the coil slitter on the mechanical page; the
pneumatic shear dropped.  The FAQ answers of the former pages are kept in tools/shear_copy.json."""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category
import shear_nav as SN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "all-shears"
COPY = json.load(open(os.path.join(ROOT, "tools", "shear_copy.json"), encoding="utf-8"))

BRAND_LINE = ("The premium hydraulic shears are built by Dener Makina in Kayseri, Turkey, and the premium mechanical shears in Turkey with European motors and electrics; "
              "NovoTech's value-line shears are built in China to our specification with Estun controls. All sold, installed and supported in Canada by NovoTech.")
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
    title="Hydraulic Shears for Sale in Canada — Swing Beam & Guillotine Plate Shears, 16 ga to 1-9/16″ | NovoTech",
    meta="Hydraulic shearing machines sold, installed and supported in Canada: swing beam shears 5/32″ – 3/4″ × 6.8 – 20 ft, variable-rake guillotines 1/4″ – 1-9/16″ × 8 – 26 ft, CNC shears with ESA control and light hydraulic shears 16 ga – 1/4″ — premium line made in Turkey and NovoTech's value line, CSA panels.",
    h1="Hydraulic shears — swing beam and guillotine plate shears, 16 ga to 1-9/16″",
    intro="A hydraulic shear cuts sheet and plate to size in one stroke between a fixed lower blade and a moving upper blade driven by two "
          "hydraulic cylinders; the back gauge sets the width, hydraulic hold-downs keep the sheet flat and the control counts the strokes. "
          "It is the shear for plate — from 16 ga to 1-9/16″ and 26 ft here — where tonnage matters more than strokes per minute. NovoTech "
          "sells three kinds in Canada, all on this page: swing beam shears, the rugged everyday plate shear with the beam swung through the "
          "cut on two bearings — the premium BS / BSY to 5/8″ over 13.5 ft and the value-line QC12K from 5/32″ to 3/4″ over 20 ft; guillotine "
          "shears with a variable rake angle on a beam carried straight down on rollers, so thin sheet is cut flat and 3/4″ plate with less "
          "distortion — the premium DAS CNC to 3/4″ × 20 ft with the ESA 630 control and the value-line Q11K to 1-9/16″ × 26 ft; and the THS, "
          "HQ11 and HQ01 light hydraulic shears from 16 ga to 1/4″ over 51 – 120″ for the sheet-metal shop. Each family below has its full specification table and photos. Every machine comes with a CSA-approved "
          "panel and a 1-year warranty, installed, trained and supported from Mississauga, ON, Canada. For sheet to 1/4″ all day with no "
          "hydraulics — guillotine, electric, bench and coil machines — see the mechanical shears.",
    points=["Swing beam: premium BS / BSY 1/4″ – 5/8″ × 6.8 – 13.5 ft with NC back gauge; value QC12K 5/32″ – 3/4″ × 8 – 20 ft with Estun E21S",
            "Guillotine: premium DAS CNC 1/4″ – 3/4″ × 10 – 20 ft, variable angle, ESA 630, 1 m ball-screw gauge; value Q11K 1/4″ – 1-9/16″ × 8 – 26 ft",
            "Light hydraulic shears 16 ga – 1/4″ × 51 – 120″: THS, HQ11 and HQ01, quick-set blade clearance, manual, electric or NC back gauge"],
    hero="dn-das-1", minis=["vl-qc12k-1", "tt-hq11"],
    groups=[("sh-premium-swing", "Swing beam shears · premium line", "BS / BSY: a beam on two bearings swung through the cut by two cylinders, 8 to 22 strokes a minute, NC back gauge, hydraulic hold-downs and single-point blade-gap adjustment — 1/4″ to 5/8″ over 6.8 to 13.5 ft."),
            ("sh-premium-cnc", "CNC guillotine shears · premium line", "DAS: a beam on linear rollers with a variable cutting angle set by the ESA 630 CNC from the thickness keyed in — 1/4″ to 3/4″ over 10, 13 and 20 ft, for production."),
            ("sh-value-swing", "Swing beam shears · value line", "QC12K: NovoTech's own everyday plate shear with Estun E21S control and a motorised back gauge — 5/32″ to 3/4″ over 8 to 20 ft."),
            ("sh-value-guillotine", "Guillotine shears · value line", "Q11K: variable rake angle and blade gap from the control, 1/4″ to 1-9/16″ over 8 to 26 ft — the value-line machine for thick plate."),
            ("sh-light-hydraulic", "Light hydraulic shears · value line", "THS, HQ11 and HQ01: hydraulic shears from 16 ga to 1/4″ over 51 to 120″ with quick-set blade clearance and a manual, electric or NC back gauge — for the sheet-metal shop.")],
    faq=[faq("hydraulic-shearing-machine", "Swing beam or guillotine shear?")[0],
         {"q": "Premium line or value line?",
          "a": "The premium BS / BSY and DAS shears are built by Dener in Turkey with European hydraulics, ESA or Delem controls, the heaviest frames and parts stocked in Canada — the machines for two shifts a day and the tightest, flattest cut, with the DAS CNC setting rake, gap and gauge from the material keyed in. NovoTech's value-line QC12K and Q11K are the same two designs — swing beam and variable-rake guillotine — built in China to our specification with Estun controls and Siemens motors at about two-thirds of the price, in more sizes (to 1-9/16″ and 26 ft). Both lines are installed and supported by the same NovoTech technicians, and the light hydraulic shears below them are the value-line answer for 16 ga to 1/4″."},
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
    title="Mechanical Shears for Sale in Canada — Guillotine, Electric, Bench & Coil Shears, 20 ga to 3/8″ | NovoTech",
    meta="Mechanical shears sold, installed and supported in Canada: direct-gear SRGM guillotines, 1/8″ and 1/4″ to 13.8 ft with return-to-sender and cut-to-length versions, flywheel shears to 3/8″, electric and NC electric shears 14 ga – 5/32″, motorized bench shears and a 48″ coil slitter — no hydraulics.",
    h1="Mechanical shears — guillotine, electric, bench and coil machines, 20 ga to 3/8″",
    intro="A mechanical shear drives the cutting beam from an electric motor instead of hydraulic cylinders — through a gearbox and crank "
          "(direct gear) or a flywheel and clutch — so there is no hydraulic power pack to leak or warm up, the cut is the same on the first "
          "and the thousandth stroke, and the machine runs up to 55 strokes a minute: the shear for sheet and light plate all day. NovoTech "
          "sells them in Canada in two lines, all on this page: the premium-line SRGM direct-gear guillotines, built in Turkey with European "
          "motors, gearboxes and electrics — the light-type SRGM-H for 1/8″ mild steel and the SRGM for 1/4″ from 43″ to 13.8 ft, the "
          "SRGM-HFR / FR with a return-to-sender sheet support that brings the cut piece back to the operator, and the SRGM-HCL / CL built "
          "into cut-to-length coil lines; and NovoTech's value line — the Q11 flywheel shears for medium and thick steel, 1/8″ to 3/8″ at 45 "
          "to 55 strokes a minute, the Q11 electric shears for 14 ga to 5/32″ over 49″ to 100″ with a manual back gauge and counter or, on the "
          "Q11 NC, a PLC and motorised back gauge, the EBQ01 motorized bench shears for 18 ga over 26″ and 20 ga over 41″, and the "
          "PS-1220×1.5GT that slits 16 ga × 48″ coil into strips and cuts them to length. Each family below has its full specification table "
          "and photos. Every machine comes with a CSA-approved panel and a 1-year warranty, installed, trained and supported from "
          "Mississauga, ON, Canada. For plate from 3/8″ up, and for the light hydraulic shears, see the hydraulic shears.",
    points=["SRGM-H light type, 1/8″ × 3.6 – 10 ft, 35 strokes/min · SRGM standard, 1/4″ × 3.6 – 13.8 ft, 31 strokes/min — premium line, made in Turkey",
            "SRGM-HFR / SRGM-FR with return-to-sender: the cut blank comes back to the front, off-cuts drop to the rear; SRGM-HCL / CL for cut-to-length coil lines",
            "Value-line Q11 flywheel mechanical shears, 1/8″ – 3/8″ × 39 – 98″, 45 – 55 strokes/min · Q11 electric shears 14 ga – 5/32″ × 49 – 100″ with manual or NC back gauge",
            "EBQ01 motorized bench shears, 18 ga × 26″ and 20 ga × 41″ · PS-1220×1.5GT coil slitting and cut-to-length machine, 16 ga × 48″"],
    hero="sm-srgm", minis=["sm-srgm-fr", "tt-q11-6x2000"],
    groups=[("sh-srgm", "Direct-gear mechanical guillotine shears · premium line", "SRGM-H and SRGM: a 4 to 15 HP motor drives the cutting beam through a gearbox and crank — 1/8″ and 1/4″ from 43″ to 13.8 ft, welded frame, beam in teflon slideways."),
            ("sh-srgm-return", "Guillotine shears with return-to-sender · premium line", "SRGM-HFR and SRGM-FR: a sheet support behind the blade tilts and brings the cut blank back to the operator; off-cuts drop to the rear."),
            ("sh-srgm-line", "Shears for cut-to-length lines · premium line", "SRGM-HCL and SRGM-CL: the same shears built into coil cut-to-length lines, with the line control and sheet stacker."),
            ("sh-flywheel", "Flywheel mechanical shears · value line", "Q11: a flywheel and clutch drive the beam for medium and thick steel, 1/8″ to 3/8″ at 45 – 55 strokes a minute, built in China to our specification."),
            ("sh-electric", "Electric and NC electric shears · value line", "Q11 and Q11 NC: a motor and gearbox drive the beam — 14 ga to 5/32″ over 49 to 100″, with a manual back gauge and counter, or a PLC touch-screen and motorised back gauge on the NC models."),
            ("sh-bench", "Motorized bench shears · value line", "EBQ01: a 1 HP motor and a foot switch drive the blade — 18 ga over 26″ and 20 ga over 41″, for small parts on the bench."),
            ("sh-slit", "Coil slitting and cut-to-length machine · value line", "PS-1220×1.5GT: decoils, slits and cuts 16 ga × 48″ coil to length — blanks and strips for the duct and panel shop.")],
    faq=faq("novotech-mechanical-shears", "Mechanical or hydraulic shear", "What does direct-gear mean?")
        + [dict(q, a=q["a"] + " On the value line: 3/8″ on the Q11-10 flywheel shears, 5/32″ on the Q11-4 electric and NC shears, 14 ga on the Q11-2 models, 18 ga and 20 ga on the EBQ01 bench shears and 16 ga on the PS-1220 coil slitter.")
           for q in faq("novotech-mechanical-shears", "How is the capacity rated")]
        + faq("novotech-mechanical-shears", "Which length do I need")
        + [dict(q, a=q["a"] + " On the value line, the Q11 electric shears have a manual back gauge with a millimetre counter, wound to the dimension by hand, with an electric gauge as an option; the Q11 NC takes the dimension from a touch-screen PLC and positions the gauge itself, with programs for the parts you cut every week (24.8″ of travel); the EBQ01 bench shears have a 0 – 19.7″ back gauge.")
           for q in faq("novotech-mechanical-shears", "What is the back gauge")]
        + faq("novotech-mechanical-shears", "What does return-to-sender do?", "How long do the blades last", "Can it cut at an angle?")
        + faq("sheet-metal-shears", "What does the A model add", "Are the flywheel shears safe to run?", "When is a coil slitter worth it?") + [VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about mechanical shears",
    related_pages=[{"href": "press-brake.html", "label": "Press brakes"}, {"href": "corner-notcher.html", "label": "Corner notchers"},
                   {"href": "circle-cutters-and-seamers.html", "label": "Circle shears & flanging machines"}, {"href": "folder-sheet-metal-brake.html", "label": "Sheet metal brakes"}],
    related_title="More sheet-metal cutting and forming machinery from NovoTech",
)

VIDEOS = {
    "hydraulic-shearing-machine": COPY["dener-shears"],
    "mechanical-guillotine-shear": COPY["novotech-mechanical-shears"],
}


def build():
    fs = json.load(open(os.path.join(ROOT, "content", "families", f"{SET}.json"), encoding="utf-8"))
    fams = {fid: dict(fs["families"][fid], id=fid) for fid in fs["order"]}
    manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
    for slug, page in (("hydraulic-shearing-machine", HYDRAULIC), ("mechanical-guillotine-shear", MECHANICAL)):
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
        # the press brake page format (the owner, Nov 1 2026): every group under its brand's line header with no lead line, and
        # no page-level "every model" table — that table is on the hub
        brand_of = {}
        for f in members:
            brand_of.setdefault(f["group"], set()).add(f.get("brand"))
        page = dict(page, groups=[(g[0], g[1], "", next(iter(brand_of[g[0]]))) for g in page["groups"]])
        if any(len(brand_of[g[0]]) != 1 or None in brand_of[g[0]] for g in page["groups"]):
            raise SystemExit(f"{slug}: a group has families of several brands or none")
        write_category(slug, page, members, SET, SN.SECTION, hub=SN.hub(), siblings=SN.siblings(),
                       extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **video,
                              "nav_label": next(nav for s, _, _, _, nav, _ in SN.SUBPAGES if s == slug),
                              "catalogue_pdf": None, "catalogue_pdfs": pdfs})
        print(f"{slug}: {len(members)} families, {n} models, {len(pdfs)} brochures")


if __name__ == "__main__":
    build()
