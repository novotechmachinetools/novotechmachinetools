#!/usr/bin/env python3
"""CSM (Chiao Sheng Machinery, Tainan, Taiwan) — sold under its own brand.  This module holds the CSM page texts, the image
registration (section 'csm'), the NovoTech-format brochure specs and the wire-bending page:

    python3 tools/csm_photos.py                      # website renders + catalogue crops → tools/src-images/csm
    python3 tools/csm_pages.py                       # image_map entries (tools/csm_keys.txt), wire-bending page, brochure specs
    python3 tools/isitan_data.py                     # writes csm-tube-benders (pipe-benders hub) and the CSM groups on the
                                                     # tube end forming and cold saw pages
    python3 tools/make_images.py --only $(cat tools/csm_keys.txt)
    for s in csm-electric csm-hydraulic; do python3 tools/brochure/build_brochure.py tools/brochure/specs/$s.json; done

The bending page (csm-tube-benders) lives in the 'tube-benders' family set so the pipe-benders hub can list it; the end former
and the saw live in 'pipe-end-and-saws'; the wire benders in 'csm'.  CSM's laser cutting and riveting machines are not sold.
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families  # noqa: F401
import csm_data as D
import csm_photos as PH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET_WIRE = "csm"
BRAND = D.BRAND
PDF_ELECTRIC = "files/NovoTech-CSM-Electric-Tube-Benders-2026.pdf"
PDF_HYDRAULIC = "files/NovoTech-CSM-Hydraulic-Tube-Benders-2026.pdf"
FAMILY_PDF = {"csm-emr": PDF_ELECTRIC, "csm-mbe": PDF_ELECTRIC, "csm-tbre": PDF_ELECTRIC, "csm-wb": PDF_ELECTRIC,
              "csm-tsr": PDF_HYDRAULIC, "csm-tsrj": PDF_HYDRAULIC, "csm-tncb": PDF_HYDRAULIC, "csm-f38": PDF_HYDRAULIC,
              "csm-ef": PDF_HYDRAULIC, "csm-ct325": PDF_HYDRAULIC}
PDF_LABEL = {PDF_ELECTRIC: "Download the CSM electric tube & wire bender brochure", PDF_HYDRAULIC: "Download the CSM hydraulic bender, end former & saw brochure"}

BRAND_LINE = ("CSM tube benders are made in Tainan, Taiwan, by Chiao Sheng Machinery — CNC benders since 1989, 24 international design "
              "patents, ISO 9001 and CE. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Taiwan by CSM", "text": "Chiao Sheng Machinery has built tube benders in Tainan since 1982 and CNC benders since 1989 — "
          "two plants in the Southern Taiwan Science Park, ISO 9001 since 2002, CE on every machine and two Taiwan Excellence awards."}
INTRO_VIDEO = {"intro_video": {"id": "bUnS5wPFYQE", "title": "CSM tube bender company introduction", "thumb": "video-bUnS5wPFYQE", "duration": "PT4M36S"},
               "intro_video_heading": "Inside the factory — CSM in Tainan, Taiwan",
               "intro_video_text": "A tour of the CSM plant in the Southern Taiwan Science Park, where the tube benders, end formers, saws and wire benders are built."}


def pdf(fid):
    file = FAMILY_PDF[fid]
    f = os.path.join(ROOT, "src", file)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": file, "label": PDF_LABEL[file], "size": size}


def families(page=None):
    """CSM families with their brochure attached, optionally only those of one page."""
    return [dict(f, pdf=pdf(f["id"])) for f in D.FAMILIES if page is None or f["page"] == page]


# ------------------------------------------------------------------------------------------------ csm-tube-benders
PAGE_BEND = dict(
    title="CSM Electric & Hydraulic Tube Benders, to Ø8-5/8″ | NovoTech",
    meta="CNC tube benders made in Taiwan: all-electric EMR left / right benders, MBE and TBRE hybrids with stacked tools, TSR hydraulic CNC, NC and symmetric benders.",
    h1="CSM tube benders — all-electric, electric-hybrid and hydraulic CNC, NC and symmetric benders, Ø15/32″ to Ø8-5/8″",
    intro="A CNC tube bender feeds, rotates and bends the tube from a program, so a part with ten bends in different planes comes off the "
          "machine the same every time; a mandrel inside the tube and a wiper die keep thin walls round at tight radii. CSM — Chiao Sheng "
          "Machinery of Tainan, Taiwan — has built tube benders since 1982 and CNC benders since 1989, holds 24 international design "
          "patents and CE-certifies every machine. The range on this page, small to large: the EMB / EMR all-electric benders that switch "
          "between left- and right-hand bending within one part, from Ø19/32″ brake and fuel line to Ø3″, and the all-electric MRE2-RBE to "
          "Ø4″; the MBE / MRE and TBRE / TMRE / TSRE / TDRE electric hybrids — servo bend arm, carriage and collet, hydraulic clamp and "
          "mandrel — from Ø15/32″ to Ø6″ with one to three stacked tools and roll-bending heads; the TSR / TDR hydraulic CNC pipe benders to "
          "Ø8-5/8″; the TSRJ / TDRJ, TNCPB and TNCB NC hydraulic benders; and the two-head F38 / F50 symmetric benders. Rear boosters, "
          "loaders, punching units, saws, end formers and robot cells turn any of them into an automated bending cell. Sold, installed and "
          "supported in Canada by NovoTech from Mississauga, ON, Canada, with a CSA-approved panel.",
    points=["All-electric EMB / EMR (left- and right-hand) Ø19/32″ – Ø3″ and MRE2-RBE to Ø4″ — no hydraulics, ±0.01° bend arm",
            "Electric hybrid MBE / MRE, TBRE / TMRE, TSRE / TDRE: Ø15/32″ – Ø6″, 1 – 3 stacked tools, roll bending, servo rear boosters",
            "Hydraulic CNC TSR / TDR to Ø8-5/8″ pipe; NC TSRJ / TDRJ, TNCPB and TNCB; F38 / F50 two-head symmetric benders"],
    hero="cs-tbre", minis=["cs-emr", "cs-tncb"],
    groups=[("csm-electric", "CSM all-electric and electric-hybrid CNC tube benders",
             "Servo bend arms with CSM's patented transmission gears, ±0.01°, from Ø15/32″ fuel line to Ø6″: the all-electric EMB / EMR and MRE2-RBE, and the MBE / MRE and T-series hybrids.", BRAND),
            ("csm-hydraulic", "CSM hydraulic CNC pipe benders",
             "TSR and TDR: hydraulic bend arm, clamp and booster with a servo carriage and collet — pipe to Ø8-5/8″ × 19/32″ on 20 ft mandrels.", BRAND),
            ("csm-nc", "CSM NC hydraulic tube and pipe benders",
             "PLC-controlled hydraulic benders: the TSRJ / TDRJ with servo feed and rotation, the TNCPB with manual feed and the single-axis TNCB to Ø8-5/8″.", BRAND),
            ("csm-symmetric", "CSM symmetric benders",
             "Two bending heads on one bed bend both ends of the tube in one cycle — towel rails, handles, chair and bed frames.", BRAND)],
    faq=[{"q": "All-electric, electric-hybrid or hydraulic?",
          "a": "All-electric (EMB / EMR, MRE2-RBE): every axis is a servo motor — no oil, no warm-up, lower energy use, quiet and the most repeatable; the choice for small tube in high volume — fuel and brake lines, HVAC, head-rest bars, furniture. Electric hybrid (MBE / MRE and the T series): servo bend arm, carriage and collet for accuracy, hydraulic clamp, pressure die and mandrel for force — the usual production bender from Ø1/2″ to Ø6″. Hydraulic CNC (TSR / TDR): a hydraulic bend arm for heavy wall and large pipe to Ø8-5/8″ — boiler, shipyard, construction and water-supply pipe. NC (TSRJ / TDRJ, TNCPB, TNCB): PLC control and a lower price where the parts are simpler or the batches smaller."},
         {"q": "How do I read a CSM model name?",
          "a": "The number is the largest round tube in millimetres: a 38 TDRE bends Ø1-1/2″ (38.1 mm), an 80 MBE Ø3-1/8″ (80 mm), a 220 TNCB Ø8-5/8″ pipe. The letters name the series — EMB / EMR all-electric, MBE / MRE and the TBRE / TMRE / TSRE / TDRE electric hybrids, TSR / TDR hydraulic CNC, TSRJ / TDRJ, TNCPB and TNCB NC — and in the T series S, D and M stand for one, two and three stacked tools. The suffix names the booster: -RBE a servo rear booster, -RBF, -RBH and -CBF hydraulic boosters."},
         {"q": "How many stacked tools do I need, and what is roll bending?",
          "a": "Each stacked tool is another bend die (radius) on the same head; the head shifts up / down and left / right between them, so a part with two or three radii is bent in one cycle without a die change. One tool (TSRE, TSR, TNCB) suits single-radius parts; two (TDRE, TDR, TBRE) or three (MBE / MRE, TMRE) furniture, automotive and exhaust parts with several radii; the EMB / EMR carry 3 + 3, for left- and right-hand bends. A roll-bending head (EMR, MRE, TBRE / TMRE, MRE2-RBE) rolls large and variable radii — arcs, coils and frames — without a die for every radius."},
         {"q": "What does a rear booster do?",
          "a": "It pushes the tube from behind while the bend arm draws it around the die, so the outside wall thins less and the inside wall does not wrinkle — the way to bend thin-wall tube and pipe to radii down to about 1 × D (boiler pipe on the 120 TNCB-RBF, for example). -RBE is a servo booster on the electric and hybrid benders; -RBF, -RBH and -CBF are hydraulic boosters on the hydraulic machines."},
         {"q": "Can the bender be automated?",
          "a": "Yes: bundle loaders that feed the tube to the carriage, punching units on the head for holes in furniture tube (the P versions), an integrated circular saw that cuts each part off the bar, end-forming stations, robot transfer and checking fixtures. The videos under each series show most of them in production, and we lay out the cell for your parts."},
         {"q": "CSM or ISITAN?",
          "a": "Both are mandrel benders sold, installed and supported by NovoTech. The ISITAN SFB benders (Turkey) cover Ø1-1/4″ to Ø3-1/2″ with NC and CNC models for the job shop and fabricator. CSM covers a far wider range — from Ø15/32″ brake line to Ø8-5/8″ pipe — with all-electric and hybrid machines, stacked tools, boosters and automation for series production. Send us the part drawing and the tube and we quote the right machine from either range; the capacity table for every bender is on the pipe and tube benders overview."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about CSM tube benders",
    related_pages=[{"href": "wire-bending-machines.html", "label": "CNC wire bending machines"}, {"href": "tube-end-forming-machines.html", "label": "Tube end formers"},
                   {"href": "circular-cold-saws.html", "label": "Cold saws"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                   {"href": "tube-laser-cutting-machine.html", "label": "Tube laser cutters"}],
    related_title="More tube machinery from NovoTech",
)


def bend_extra():
    """extra page fields for csm-tube-benders (written by tools/isitan_tube_benders.py under the pipe-benders hub)"""
    return {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **INTRO_VIDEO, "nav_label": "CSM tube benders", "catalogue_pdf": None,
            "catalogue_pdfs": [pdf("csm-emr"), pdf("csm-tsr")]}

# ------------------------------------------------------------------------------------------------ groups on the ISITAN pages
FORM_GROUP = ("csm-form", "CSM end formers, grooving and end-finishing machines",
              "Six-station EF end formers to Ø2″, REF grooving machines and the ER 30-5 that forms, chamfers and grooves in one cycle — the end-finishing stations of CSM's bending cells.", BRAND)
SAW_GROUP = ("csm-saw", "CSM automatic circular saw with servo feed",
             "The CT325 saws tube and bundles to Ø4″ with hydraulic down-feed, a servo carriage feeding to ±0.004″ and three spindle-speed ranges.", BRAND)

# ------------------------------------------------------------------------------------------------ wire-bending-machines
PAGE_WIRE = dict(
    title="CNC Wire Bending Machines, 3D, Ø5/32″ to Ø9/16″ | NovoTech",
    meta="3D CNC wire benders fed from the coil: decoiler, straightener, servo feed and a 1,000°/s bending head — baskets, racks, frames, hooks and exhaust hangers.",
    h1="CNC wire bending machines — 3D wire benders fed from the coil, Ø5/32″ to Ø9/16″",
    intro="A CNC wire bending machine turns wire from the coil into a finished part in one pass: the decoiler pays off the wire, the "
          "straightener takes out the coil set, a servo feeder pushes the programmed length through the bending head, the head bends, rotates "
          "to the next plane and bends again, and a cutter drops the part — baskets, display racks, shelf supports, chair and furniture frames, "
          "handles, hooks, springs and exhaust hangers, with no jigs and no bending by hand. NovoTech sells the CSM WB 10-A and WB 14-A, built in "
          "Tainan, Taiwan, by the tube-bender maker CSM: 3D benders for Ø5/32″ to Ø3/8″ and Ø1/4″ to Ø9/16″ wire, bending at up to 1,000°/s "
          "with ±0.01° repeatability, an IPC control with a 15″ touch-screen that simulates the part in 3D before the first bend, and a "
          "concentric tool design and customised work-head that keep complex shapes free of interference. With a CSM EF end former they make "
          "a complete exhaust-hanger line. Installed, trained and supported from Mississauga, ON, Canada, with a CSA-approved panel.",
    points=["WB 10-A: Ø5/32″ – 3/8″ wire at 1,000°/s · WB 14-A: Ø1/4″ – 9/16″ wire at 600°/s — ±0.01° bending repeatability",
            "From the coil: AC-driven decoiler, hydraulic straightener, servo feed at 164 ft/min (±0.004″), hydraulic cutter",
            "3D: servo work-head rotation at 440°/s, servo tool shift, concentric tools; IPC control with 15″ touch-screen and 3D simulation"],
    hero="cs-wb10", minis=["cs-wb-screen", "cs-wb-line"],
    groups=[("csm-wire", "CSM CNC wire benders", "Two sizes of 3D CNC wire bender with decoiler, straightener, servo feed, bending head and cutter on one base.", BRAND)],
    faq=[{"q": "What can a CNC wire bender make?",
          "a": "Any part bent from round wire or rod in the capacity range: wire baskets and racks, display and shelf hardware, chair, sofa and bed frames, handles and hooks, springs and clips, automotive seat and exhaust-hanger wire, fencing and agricultural parts. The machine bends in three dimensions, so a part with bends in several planes comes off finished and cut to length."},
         {"q": "WB 10-A or WB 14-A?",
          "a": "By the wire. The WB 10-A bends Ø5/32″ to Ø3/8″ (4 – 10 mm) at 1,000°/s — the faster machine for furniture, display and basket wire. The WB 14-A takes Ø1/4″ to Ø9/16″ (6 – 14 mm) at 600°/s — heavier frames, rod, seat and exhaust-hanger wire. Both feed at 164 ft/min, rotate the head at 440°/s and repeat to ±0.01°; base, power and footprint are the same."},
         {"q": "2D or 3D — what does the rotating work-head do?",
          "a": "A 2D bender bends in one plane only. On the WB the work-head itself rotates around the wire under servo control, so after one bend the next can be made in any other plane — the wire never has to be turned by hand, and three-dimensional parts come off in one cycle. The concentric tool design and the customised work-head keep the head clear of the part as it grows."},
         {"q": "How is a new part programmed?",
          "a": "On the IPC control with its 15″ touch-screen: enter the lengths, bend angles and rotation angles of the part, and the control shows it in 3D, checks the sequence for interference and runs it. Programs are stored and reloaded for the next batch; no jigs or fixtures have to be built for a new part."},
         {"q": "Can it work with an end former?",
          "a": "Yes — the WB 14-A with a CSM EF50 end former makes complete exhaust hangers: the wire is bent and cut and the ends are formed in one line. The videos below show the line in production; the EF end formers are on our tube end forming page."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about CNC wire benders",
    related_pages=[{"href": "csm-tube-benders.html", "label": "CSM tube benders"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"},
                   {"href": "tube-end-forming-machines.html", "label": "Tube end formers"}, {"href": "rebar-bender.html", "label": "Rebar benders"}],
    related_title="More bending machinery from NovoTech",
)

# ------------------------------------------------------------------------------------------------ brochures
ABOUT_CSM = ("Chiao Sheng Machinery (CSM) has built tube benders in Tainan, Taiwan, since 1982 and released its first CNC bender in 1989; the "
             "company works from two plants in the Southern Taiwan Science Park, holds 24 international design patents, has been ISO 9001 "
             "certified since 2002 and CE-certifies every machine. NovoTech sells, installs and supports CSM machines in Canada from "
             "Mississauga, Ontario, Canada — layout for your building, installation, operator training, a CSA-approved panel, a 1-year warranty and "
             "parts and technical support in Canada.")
BROCHURES = {
    "csm-electric": dict(
        title="Electric tube benders and wire benders",
        subtitle="CSM EMB / EMR and MRE2-RBE all-electric benders · MBE / MRE and TBRE / TMRE / TSRE / TDRE electric hybrids · WB CNC wire benders · Ø5/32″ wire to Ø6″ tube",
        cover_line="CSM · made in Taiwan · sold & serviced in Canada by NovoTech", range_label="CSM electric tube benders", about_for="CSM electric tube benders",
        about_kicker="CSM · Tainan, Taiwan", about_title="Servo-driven tube benders, from Ø15/32″ brake line to Ø6″ tube",
        about_text=["CSM's electric benders put a servo motor on the bend arm — through CSM's patented transmission gears, to ±0.01° — and on the "
                    "carriage, collet and tool shift. The EMB / EMR and MRE2-RBE are all-electric, with no hydraulic unit at all; the EMB / EMR switch "
                    "between left- and right-hand bending within one part. The MBE / MRE and the TBRE / TMRE / TSRE / TDRE are electric hybrids with "
                    "hydraulic clamp, pressure die and mandrel, one to three stacked tools, roll-bending heads and servo rear boosters, from Ø15/32″ "
                    "fuel line to Ø6″. The WB 10-A and WB 14-A bend wire from the coil in 3D at up to 1,000°/s.", ABOUT_CSM],
        country="Taiwan", families=["csm-emr", "csm-mbe", "csm-tbre", "csm-wb"], family_sets=["tube-benders", "csm"],
        groups=[{"title": "All-electric CNC tube benders", "families": ["csm-emr"]}, {"title": "Electric-hybrid CNC tube benders", "families": ["csm-mbe", "csm-tbre"]},
                {"title": "CNC wire benders", "families": ["csm-wb"]}],
        cover_photos=["cs-emr", "cs-tbre", "cs-wb10"], out="src/" + PDF_ELECTRIC),
    "csm-hydraulic": dict(
        title="Hydraulic tube benders, end formers and saws",
        subtitle="CSM TSR / TDR hydraulic CNC and TSRJ / TDRJ, TNCPB, TNCB NC pipe benders to Ø8-5/8″ · F38 / F50 symmetric benders · EF, REF and ER end formers · CT325 circular saw",
        cover_line="CSM · made in Taiwan · sold & serviced in Canada by NovoTech", range_label="CSM hydraulic tube benders", about_for="CSM hydraulic tube benders, end formers and saws",
        about_kicker="CSM · Tainan, Taiwan", about_title="Hydraulic pipe benders to Ø8-5/8″, and the machines around them",
        about_text=["CSM's hydraulic benders put the force of a hydraulic bend arm, clamp, pressure die and booster on heavy-wall tube and pipe: the "
                    "TSR / TDR CNC benders with a servo carriage and collet bend pipe to Ø8-5/8″ on 20 ft mandrels; the TSRJ / TDRJ and TNCPB are "
                    "the NC versions with servo or manual feed; the TNCB is the single-axis NC pipe bender to Ø8-5/8″; the F38 / F50 bend both ends "
                    "of a tube at once. The EF, REF and ER machines form, groove and chamfer the tube ends, and the CT325 saws tube and bundles to "
                    "Ø4″ with servo feed — the stations of a complete tube cell.", ABOUT_CSM],
        country="Taiwan", families=["csm-tsr", "csm-tsrj", "csm-tncb", "csm-f38", "csm-ef", "csm-ct325"], family_sets=["tube-benders", "pipe-end-and-saws"],
        groups=[{"title": "Hydraulic CNC pipe benders", "families": ["csm-tsr"]}, {"title": "NC hydraulic tube and pipe benders", "families": ["csm-tsrj", "csm-tncb"]},
                {"title": "Symmetric benders", "families": ["csm-f38"]}, {"title": "End forming and sawing", "families": ["csm-ef", "csm-ct325"]}],
        cover_photos=["cs-tsr", "cs-tncb", "cs-ef30"], out="src/" + PDF_HYDRAULIC),
}


def write_brochure_specs():
    d = os.path.join(ROOT, "tools", "brochure", "specs")
    for name, spec in BROCHURES.items():
        spec = dict(spec, single_phase=False, year="2026", made_in="Made in Taiwan by CSM (Chiao Sheng Machinery) — ISO 9001 and CE")
        json.dump(spec, open(os.path.join(d, name + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "csm")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")]
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/csm/{key}{ext}", "alt": p["alt"], "section": "csm", "trim": False, "quality": 82, "cutout": bool(p.get("cutout"))}
        keys.append(key)
    imap["csm-logo"] = {"src": "tools/src-images/csm-logo.png", "alt": "CSM", "section": "site", "trim": True, "quality": 90, "cutout": False}
    keys.append("csm-logo")
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "csm_keys.txt"), "w").write(",".join(keys))
    return keys


def video_ids():
    ids = [v["id"] for f in D.FAMILIES for v in f["videos"]] + [INTRO_VIDEO["intro_video"]["id"]]
    return list(dict.fromkeys(ids))


def build():
    wire = families(D.P_WIRE)
    write_families(SET_WIRE, wire)
    write_category(D.P_WIRE, PAGE_WIRE, wire, SET_WIRE, "Wire bending machines",
                   extra={"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **INTRO_VIDEO, "nav_label": "Wire bending machines", "catalogue_pdf": pdf("csm-wb")})
    keys = register_images()
    write_brochure_specs()
    used = {k for f in D.FAMILIES for k in f["images"]} | {PAGE_BEND["hero"], PAGE_WIRE["hero"]} | set(PAGE_BEND["minis"]) | set(PAGE_WIRE["minis"])
    for b in BROCHURES.values():
        used |= set(b["cover_photos"])
    unused = sorted(set(keys) - used - {"csm-logo"})
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        print("!! image keys without a photo (export still running?):", missing)
    open(os.path.join(ROOT, "tools", "csm_vids.txt"), "w").write(" ".join(video_ids()))
    print(f"csm: {len(D.FAMILIES)} families · {sum(len(f['specs']['models']) for f in D.FAMILIES)} models · images: {len(keys)} · videos: {len(video_ids())}")


if __name__ == "__main__":
    build()
