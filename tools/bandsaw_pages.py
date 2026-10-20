#!/usr/bin/env python3
"""Generate the band saw section pages: the hub (band-saw.json) and eight category pages —
four for the Bekamak premium line and four for the NovoFab Machinery value line.
    python3 tools/bandsaw_pages.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "content", "pages")
FAM = json.load(open(os.path.join(ROOT, "content", "families", "bandsaw.json"), encoding="utf-8"))

PDF_BK = {"file": "files/NovoTech-Bekamak-Band-Saws-Catalogue-2026.pdf", "label": "Bekamak band saw catalogue", "size": "PDF · 7.5 MB · imperial units"}
PDF_NF = {"file": "files/NovoTech-Value-Line-Band-Saws-Catalogue-2026.pdf", "label": "NovoTech value line band saw catalogue", "size": "PDF · 5 MB · imperial units"}
PLAYLIST = "https://www.youtube.com/playlist?list=PLgtouQi-TePvLZjD0XkwpvL2pX1sAUuFG"
GUIDE = {"href": "band-saw.html#buying-guide", "label": "Band saw buying guide: sizes, feeds, blades and troubleshooting"}
CRUMB_BASE = [{"label": "Home", "href": "index.html"}, {"label": "Products", "href": "products.html"}, {"label": "Metal cutting band saws", "href": "band-saw.html"}]

CATS = ["manual", "semi-automatic", "automatic", "double-column"]
CAT_TITLE = {"manual": "Manual band saws", "semi-automatic": "Semi-automatic band saws", "automatic": "Automatic band saws", "double-column": "Double-column band saws"}
CAT_SHORT = {"manual": "Manual", "semi-automatic": "Semi-automatic", "automatic": "Automatic", "double-column": "Double-column"}


FACTORY_VIDEO = {"id": "6xEVXrP8h3k", "title": "Bekamak corporate introduction video", "thumb": "video-6xEVXrP8h3k", "duration": "PT3M4S"}
FIRST = {"novotech-bs-315gf": 0}   # families pinned to the top of their group


def fams(brand, cat):
    ks = [k for k in FAM["order"] if FAM["families"][k]["brand"] == brand and FAM["families"][k]["group"] == cat]
    return sorted(ks, key=lambda k: (FIRST.get(k, 1), ks.index(k)))


VOLT_FAQ = {"q": "What voltage do these saws run on?",
            "a": "Three-phase machines are supplied for 600 V with a CSA-approved electrical panel; 208 V, 240 V or 480 V 3-phase are available on request."}

BK = {
    "manual": dict(
        title="Bekamak Manual Band Saws — BMS Double-Miter Bandsaws | NovoTech",
        meta="Bekamak BMS 230DG and 270DG manual metal cutting band saws (gravity-feed bandsaws) for sale in Canada: double-miter heads to 60°, hydraulic descent, Ø9″–10-5/8″. Specs in inches and mm, CSA panels, support in Mississauga, ON.",
        h1="Bekamak manual band saws",
        intro="Gravity-feed pivot saws built by Bekamak in Turkey for maintenance shops, fabricators and anyone cutting a few pieces at a time: the operator positions the bar, closes the vise and lowers the bow; a hydraulic cylinder controls the descent and the double-miter head swivels both ways for angle cuts. Premium-line construction with CSA-approved panels and support from Mississauga, ON.",
        points=["Hydraulic-damped gravity feed with adjustable cutting pressure", "Double-miter head: +60° right, −45° left", "Round capacities Ø9″ (230 mm) and Ø10-5/8″ (270 mm)"],
        hero="bk-hero-manual", minis=["bk-bms-230dg-1-cut"],
        lead="European-style pivot saws with heavy castings, variable-speed motors and hydraulic descent control.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "What does “gravity feed” mean on a band saw?", "a": "The saw bow descends under its own weight; a hydraulic cylinder with an adjustable valve controls how fast it drops, so the operator sets the cutting pressure for the material. After the cut the operator lifts the bow back up by hand."},
            {"q": "Can a manual band saw cut miters?", "a": "Yes. The BMS 230DG and 270DG heads swivel to both sides — +60° to the right and −45° to the left — with an angle scale and fast stops at 30°, 45° and 60°, so one setup covers most structural miters."},
            {"q": "When should I move up to a semi-automatic saw?", "a": "When you cut more than a few dozen pieces a day, or when the operator is tied up holding the bow. A semi-automatic saw clamps hydraulically, cuts at a preset feed and lifts the bow by itself, so the operator only loads material. See the Bekamak semi-automatic band saws page."},
            VOLT_FAQ,
        ]),
    "semi-automatic": dict(
        title="Bekamak Semi-Automatic Band Saws — BMSY Hydraulic Bandsaws | NovoTech",
        meta="Bekamak BMSY semi-automatic metal cutting band saws (hydraulic bandsaws) for sale in Canada: hydraulic vise, automatic bow return, miter heads to 60°, Ø9″ to Ø17-3/8″ (230–440 mm). Specs in inches and mm.",
        h1="Bekamak semi-automatic band saws",
        intro="The workhorse of most fabrication shops: the operator loads the bar and presses start; the hydraulic vise clamps, the bow cuts at the set feed rate and lifts clear when the cut is done. Bekamak's BMSY pivot saws come with single- or double-miter heads for structural steel, inverter blade speed and hydro-mechanical blade tension — from Ø9″ to Ø17-3/8″ (230–440 mm).",
        points=["Hydraulic vise, automatic bow return, inverter blade speed", "Single- or double-miter heads to 60°; DGH models position the head hydraulically", "Round capacities from Ø9″ (230 mm) to Ø17-3/8″ (440 mm)"],
        hero="bk-hero-semi", minis=["bk-bmsy-320g-1-cut", "bk-bmsy-350m-1-cut"],
        lead="Pivot-type saws with inverter blade speed, hydro-mechanical blade tension and hydraulic miter positioning on the DGH models.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "What is the difference between a semi-automatic and a fully automatic band saw?", "a": "A semi-automatic saw makes one cut per start: it clamps, cuts and lifts the bow, then waits for the operator to feed the next piece. A fully automatic saw also feeds the material to length (by rollers or a shuttle vise) and repeats the cycle for the programmed quantity. See the Bekamak automatic band saws page."},
            {"q": "Single miter or double miter?", "a": "A single-miter head (BMSY 320G/GL) swivels to one side, so angled parts are cut by flipping the bar. A double-miter head (BMSY DG/DGH) swivels both ways — +60° right, −45° left — which saves handling on frames and trusses with opposite angles."},
            {"q": "What does the DGH suffix mean?", "a": "DGH models position the saw head hydraulically for miter angles instead of by hand, and include hydraulic head lifting — useful on the larger 320–440 mm machines where the bow is heavy."},
            {"q": "Can these saws cut bundles?", "a": "Yes, with the optional hydraulic top clamping, which presses a bundle of tubes or bars down while the side vise holds it. Ask us about bundle sizes for the model you need."},
        ]),
    "automatic": dict(
        title="Bekamak Automatic Band Saws — BMSO NC Bandsaws | NovoTech",
        meta="Bekamak BMSO fully automatic metal cutting band saws (NC bandsaws) for sale in Canada: roller-feed, encoder and servo shuttle-vise saws to Ø17-3/8″ (440 mm), automatic miter models. Specs in inches and mm.",
        h1="Bekamak automatic band saws",
        intro="Set the length and the quantity, load the bar and walk away. Bekamak's BMSO saws feed the material — with driven rollers, an encoder-measured feed or a servo shuttle vise — clamp, cut and count until the job is done. From Ø9″ to Ø17-3/8″ (230–440 mm), including automatic single- and double-miter models with NC job lists.",
        points=["Roller feed, encoder feed or servo shuttle-vise feed", "NC job lists: length × quantity × angle", "Automatic single- and double-miter models"],
        hero="bk-hero-auto-350ga", minis=["bk-bmso-320e-1-cut", "bk-bmso-320gs-3-cut"],
        lead="Roller-feed automatics for simple repeat cutting, encoder and servo versions for length accuracy, and automatic miter saws for angled parts.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "Roller feed or shuttle vise — which is better?", "a": "Roller feed (BMSO 230–440, BMSO E) is simple and fast for bar and tube in straight cuts; the encoder versions measure the fed length for better accuracy. A shuttle vise — servo-driven on the BMSO GS/GLS and all CS/CGS double-column saws, motorized on the compact 270DGS — grips the bar and moves it to the programmed length, giving ±0.1 mm repeatability on the servo models and reliable feeding of bundles and short remnants."},
            {"q": "How many lengths can I program?", "a": "The NC control on the servo-feed models stores a job list of several length-and-quantity pairs (and the miter angle on GS/DGS models), so one bar can be cut into different parts without re-programming."},
            {"q": "What happens at the end of the bar?", "a": "The saw stops when the remaining length is shorter than the next part or the feed vise reaches its limit, and the counter shows how many pieces were cut. Remnant length depends on the model — typically 3–6 in (80–150 mm)."},
            {"q": "Do automatic saws need a roller table?", "a": "A short infeed roller table is included on the BMSO E models; a 10 ft (3 m) manual or motorized roller table is optional on the others and is strongly recommended for bars longer than about 6 ft."},
        ]),
    "double-column": dict(
        title="Bekamak Double Column Band Saws (Bandsaws), Ø13″–59″ | NovoTech",
        meta="Bekamak double column metal cutting band saws (twin-column bandsaws) for sale in Canada, Ø13″ to 59″ (330–1500 mm): BMSY C semi-automatics, CGH / DG NC miter saws, BMSO CS / CGS servo NC saws and the XS line.",
        h1="Bekamak double-column band saws",
        intro="For heavy bar, billets, beams and bundles the bow runs between two hardened columns instead of pivoting, so the blade enters the material squarely and stays square through the cut. Bekamak builds semi-automatic and fully automatic versions, miter heads to 60°, servo feeding with NC job lists and the enclosed high-tech XS production saws — from Ø13″ to 59″ (330–1500 mm).",
        points=["Twin-column guidance for square cuts in heavy stock", "Semi-automatic, roller-feed and servo-feed NC models", "Round capacities from Ø13″ (330 mm) to 59″ (1500 mm)"],
        hero="bk-hero-dc-570cs", minis=["bk-bmsy-460c-1-cut", "bk-bmso-440cgs-1-cut"],
        lead="From the BMSY C semi-automatics to servo-feed CS NC production saws and the enclosed XS line.",
        video=FACTORY_VIDEO,
        video_text="A tour of the Bekamak plant in Turkey, where the premium-line band saws on this page are engineered and built.",
        faq=[
            {"q": "Why choose a double-column saw over a pivot saw?", "a": "Rigidity and capacity. The bow is guided on two columns, so there is no side load on the blade — cuts stay square in large solids and the blade lasts longer. Double-column saws also reach capacities a pivot bow cannot: 330 mm up to 1500 mm on the Bekamak range."},
            {"q": "Can a double-column saw cut miters?", "a": "Yes — the BMSY CGH (single miter) and BMSY DG NC (double miter) swivel the whole bow assembly up to 60° under hydraulic or NC control, and the automatic CGS/CDGS NC models do the same with servo feeding."},
            {"q": "What is a split vise (SV)?", "a": "The SV versions of the BMSY C saws have a second vise jaw close to the blade, so short pieces and remnants are clamped on both sides of the cut — useful for cutting slices from blocks and billets."},
            {"q": "What is the XS line?", "a": "Bekamak's high-tech production saws: servo-driven bow feed and material feed, full enclosure and CNC control, designed for carbide blades, the fastest cycle times and unattended running."},
        ]),
}

NF = {
    "semi-automatic": dict(
        title="NovoTech Semi-Automatic Band Saws — Hydraulic Bandsaws | Canada",
        meta="NovoTech semi-automatic metal cutting band saws (hydraulic bandsaws) for sale in Canada: the full-hydraulic BS-315GF double-miter saw, BS-460G dual-miter, BS-2114TH, BS-5030 single-column and the 18″ BS-650GA. Specs in inches and mm.",
        h1="NovoTech semi-automatic band saws",
        intro="Hydraulic saws for the production floor at value-line prices, led by our best seller — the BS-315GF, a 10-inch double-miter (mitre) saw with hydraulic vise, hydraulic down-feed and hydraulic bow up-lift. A hydraulic cylinder lowers the bow at a dialled-in rate, the bow lifts and the machine stops at the end of the cut. From the 10-inch saws to the 18-inch BS-650GA swivel-head saw, with a single-column touch-screen model (BS-5030) in between.",
        points=["BS-315GF: full-hydraulic 10″ double-miter saw — our most popular model", "Hydraulic descent, automatic bow return and shut-off on every model", "Round capacities from Ø9-7/8″ (250 mm) to Ø18″ (460 mm)"],
        hero="nt-h10f-1-cut", minis=["nt-h18-1-cut", "nt-h12sc-1-cut"],
        lead="Hydraulic descent, hydraulic vises and automatic bow return from Ø10″ to Ø18″ (254–460 mm), including a single-column saw with touch screen.",
        faq=[
            {"q": "What is the difference between a semi-automatic and a fully automatic band saw?", "a": "A semi-automatic saw makes one cut per start: it clamps, cuts and lifts the bow, then waits for the operator to feed the next piece. A fully automatic saw also feeds the material to length and repeats the cycle for the programmed quantity — see the value line automatic band saws."},
            {"q": "Which value-line saws cut miters on both sides?", "a": "The BS-315GF, BS-460G / 460G-JC and BS-650GA swivel to both sides (45° left and right, 60° right); the BS-2114TH cuts angles up to 60° on one side."},
            {"q": "What does \"full-hydraulic\" mean on the BS-315GF?", "a": "Hydraulic vise, hydraulic down-feed and hydraulic bow up-lift on one 10-inch machine: the operator loads the bar, presses start and the saw clamps, cuts, lifts the bow and switches off. The gear drive and a bow that swivels to both sides with fast stops at 30°, 45° and 60° complete it."},
            {"q": "What does SC mean?", "a": "Single column: the BS-5030 guides the bow vertically on a column instead of a pivot, for square straight cuts up to Ø11-3/4″ / 19-3/4″ × 11-3/4″ with a PLC touch screen. Its automatic sister is the BS-5040."},
            VOLT_FAQ,
        ]),
    "automatic": dict(
        title="NovoTech Automatic Band Saws — CNC Bandsaws | Canada",
        meta="NovoTech automatic metal cutting band saws (CNC bandsaws) for sale in Canada: BS300x370 roller-feed, BS-5040 single-column, BS-460GB swivel-head miter saw with 20 ft stand, BS-500G to BS-850G CNC servo saws. Specs in inches and mm.",
        h1="NovoTech automatic band saws",
        intro="Automatic saws that feed, clamp, cut and count by themselves — roller feeders on the compact BS300x370, a hydraulic shuttle vise on the single-column BS-5040 and the swivel-head BS-460GB that miters to both sides, and CNC servo feeding with stepless blade speed on the BS-500G to BS-850G. Value-line pricing with CSA-approved panels, a 1-year warranty and support from Mississauga, ON.",
        points=["Roller feed, shuttle vise or CNC servo feeding", "Piece counters and PLC job lists", "Round capacities from Ø11-3/4″ (300 mm) to Ø23-5/8″ (600 mm)"],
        hero="nt-a12sc-1-cut", minis=["nt-a18-1-cut", "nt-a13-1-cut"],
        lead="Roller-feed, shuttle-vise and CNC servo automatics from Ø11-3/4″ to Ø23-5/8″ (300–600 mm): feed, clamp, cut and count without an operator at the saw.",
        faq=[
            {"q": "Roller feed or shuttle vise — which is better?", "a": "Roller feed (BS300x370) is simple and fast for bar and tube in straight cuts. A shuttle vise (BS-5040, BS-460GB) grips the bar and moves it a set distance per stroke, which is more accurate and handles bundles; the CNC saws (BS-500G to BS-850G) position the feeder with a servo motor for the best repeatability."},
            {"q": "Which automatic models cut miters?", "a": "The BS300x370H (0°–60° miter head), the BS-460GB (bow swivels both sides) and the BS-500G, 500GT and 650G with an automatic rotary bow (45°; 60° on the BS-650G)."},
            {"q": "Do automatic saws need a roller table?", "a": "The BS-460GB ships with a 20 ft material stand; for the other models a roller conveyor is optional and strongly recommended for bars longer than about 6 ft."},
            VOLT_FAQ,
        ]),
    "double-column": dict(
        title="NovoTech Double Column Band Saws — Twin-Column Bandsaws | Canada",
        meta="NovoTech double column metal cutting band saws (twin-column bandsaws) for sale in Canada: TBK-4228 series, gear-driven TGK-4235 / 4240 and GZ4250/70 / 24 gantry saws for plate and bundles. Specs in inches and mm.",
        h1="NovoTech double-column band saws",
        intro="Twin-column saws at value-line prices: the bow travels vertically on two columns, so the cut stays square in solid bar, blocks and bundles. The TBK-4228 series offers manual feed, a 45° miter (mitre) version and two automatics; the TGK-4235 and 4240 add gear drive and hydraulic blade tension; the GZ4250/70 and GZ4260/120 are gantry saws for plate up to 47-1/4″ wide.",
        points=["Twin-column guidance for square cuts in heavy stock", "Hydraulic down-feed and clamping on every model; automatic feed on the TBK-4228B / 4228B (improved)", "Round capacities from Ø11″ (280 mm) to Ø23-5/8″ (600 mm)"],
        hero="nt-dc11a-1-cut", minis=["nt-dc14-1-cut", "nt-dc11-1-cut"],
        lead="Twin-column saws from Ø11″ to Ø23-5/8″ (280–600 mm): hydraulic semi-automatics, a miter version, automatics with shuttle vise and gantry saws for plate and bundles.",
        faq=[
            {"q": "Why choose a double-column saw over a pivot saw?", "a": "Rigidity and capacity. The bow is guided on two columns, so there is no side load on the blade — cuts stay square in large solids and the blade lasts longer. The GZ4250/70 and GZ4260/120 gantry saws also take plate and bundles a pivot bow cannot."},
            {"q": "Which value-line double-column saws are automatic?", "a": "The TBK-4228B and TBK-4228B (improved) feed and cut automatically with a shuttle vise; the AV adds stepless blade speed and a chip conveyor. The TBK-4228, TBK-4228A, TGK-4235, TGK-4240, GZ4250/70 and GZ4260/120 are hydraulic semi-automatics with manual material feed."},
            {"q": "Can a value-line double-column saw cut miters?", "a": "The TBK-4228A swivels for cuts at 30° and 45° (Ø10-1/4″ and Ø6-3/4″). The other value-line double-column models are straight-cut saws."},
            VOLT_FAQ,
        ]),
}

KW = {
    "manual": " Searching for a manual metal bandsaw, a gravity-feed horizontal band saw for metal or a small band saw machine for the shop? These are the ones NovoTech stocks and supports.",
    "semi-automatic": " If you are looking for a semi-automatic metal bandsaw, a hydraulic horizontal band saw for metal or an industrial band saw machine with a hydraulic vise, this is the page.",
    "automatic": " For buyers searching for an automatic metal cutting bandsaw, a CNC band saw machine or an industrial horizontal band saw for metal with automatic feeding, these are the models NovoTech sells and supports in Canada.",
    "double-column": " Known as double column, twin-column or dual column metal bandsaws, these horizontal band saw machines are the industrial choice for heavy solids, bundles and plate."
}

ORIGIN = {
    "bekamak": {"title": "Made in Turkey by Bekamak", "text": "Bekamak has built band saws in Turkey since 1990 with European components — our premium line."},
    "novotech": {"title": "Built in China to North American standards", "text": "NovoTech's own brand — same CSA panel, warranty and Mississauga, ON support as every machine we sell."},
}

BRAND = {
    "bekamak": dict(key="bekamak", slug="bekamak", line="premium", name="Bekamak", pdf=PDF_BK, page_label="Bekamak",
                    brand_line="Bekamak band saws are made in Turkey by Bekamak Makina. Sold, installed and supported in Canada by NovoTech — the premium line of our band saw range.",
                    related_title="More Bekamak band saws from NovoTech"),
    "novotech": dict(key="novotech", slug="novotech", line="value", name="NovoTech", pdf=PDF_NF, page_label="NovoTech",
                    brand_line="NovoTech's own brand: manufactured in China to high North American quality standards, with the same CSA-approved panel, 1-year warranty and Mississauga, Ontario parts and support as every machine we sell.",
                    related_title="More NovoTech value line band saws"),
}


def page(brand, cat, spec):
    b = BRAND[brand]
    spec = dict(spec, intro=spec["intro"] + KW[cat])
    slug = f"{b['slug']}-{cat}-band-saws"
    other = "novotech" if brand == "bekamak" else "bekamak"
    p = {
        "slug": slug, "template": "category.html", "family_set": "bandsaw",
        "artifact_title": f"{b['name']} {CAT_TITLE[cat]}",
        "title": spec["title"], "meta_description": spec["meta"], "h1": spec["h1"], "intro": spec["intro"],
        "hero_points": spec["points"], "hero_image": spec["hero"], "hero_image_secondary": spec["minis"],
        "breadcrumb": CRUMB_BASE + [{"label": f"{b['name']} {CAT_TITLE[cat].lower()}"}],
        "hero_brand_line": b["brand_line"],
        "catalogue_pdfs": [b["pdf"]],
        "line_key": b["key"],
        "origin_feature": ORIGIN[brand],
        "groups": [{"id": f"{b['slug']}-{cat}", "brand": b["key"], "title": f"{b['name']} {CAT_TITLE[cat].lower()}", "lead": spec["lead"], "families": fams(brand, cat)}],
        "alt_line": ({"href": f"{BRAND[other]['slug']}-{cat}-band-saws.html", "label": f"{BRAND[other]['name']} {CAT_TITLE[cat].lower()}",
                      "line": BRAND[other]["line"], "brand": other} if cat in (BK if other == "bekamak" else NF) else None),
        "faq_title": f"Questions we get asked about {b['name']} {CAT_TITLE[cat].lower()}",
        "faq": spec["faq"],
        "related_article": GUIDE,
        "youtube_playlist": PLAYLIST,
        "related_pages": [{"href": "cold-saw-carbide-saw-cutting.html", "label": "Circular cold saws"}],
    }
    if spec.get("video"):
        p["intro_video"] = spec["video"]
        p["intro_video_heading"] = "Inside the factory — where the saws are built"
        p["intro_video_text"] = spec["video_text"]
    return p


def main():
    for old in ("manual-band-saws", "semi-automatic-band-saws", "automatic-band-saws", "double-column-band-saws"):
        fp = os.path.join(PAGES, old + ".json")
        if os.path.exists(fp):
            os.remove(fp)
    lines = []
    for brand, specs in (("bekamak", BK), ("novotech", NF)):
        b = BRAND[brand]
        subpages = []
        for cat in CATS:
            if cat not in specs:
                continue
            p = page(brand, cat, specs[cat])
            json.dump(p, open(os.path.join(PAGES, p["slug"] + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            subpages.append({"slug": p["slug"], "title": f"{b['page_label']} {CAT_TITLE[cat].lower()}", "nav_label": CAT_SHORT[cat], "cat": cat, "line": b["line"],
                             "image": p["hero_image"], "blurb": specs[cat]["lead"], "families": fams(brand, cat)})
        lines.append({"id": b["line"], "brand": b["key"], "label": f"{b['line'].title()} line", "name": b["name"], "short": b["page_label"], "pdf": b["pdf"],
                      "blurb": ("Built in Turkey since 1990 with European components and the heaviest construction in their class — the saws we recommend for production and heavy sections." if brand == "bekamak"
                                else "NovoTech's own brand: manufactured in China to high North American quality standards, with the same CSA-approved panel, 1-year warranty and Mississauga, Ontario parts and support as every machine we sell."),
                      "subpages": subpages})
    # ---- hub
    hp = os.path.join(PAGES, "band-saw.json")
    h = json.load(open(hp, encoding="utf-8"))
    h["lines"] = lines
    h["subpages"] = [sp for ln in lines for sp in ln["subpages"]]
    h["title"] = "Metal Cutting Band Saws & Bandsaws for Sale in Canada | NovoTech"
    h["meta_description"] = "Horizontal metal cutting band saws (bandsaws) for sale in Canada: manual, semi-automatic, automatic and double column band saw machines from Ø9″ to 59″ — Bekamak premium and NovoTech value line, specs in inches and mm, buying guide."
    h["intro"] = "Horizontal metal cutting band saws — metal bandsaws for steel, stainless, aluminum and other metals — for fabricators, machine shops and steel service centres across Canada, in two clearly separated lines: the premium Bekamak range built in Turkey, and NovoTech's own value line. Whether you are searching for a manual band saw for metal, a semi-automatic hydraulic bandsaw, an automatic CNC band saw machine or an industrial double column saw for heavy bar and bundles, every machine is here with specifications in inches and millimetres, a CSA-approved panel, spare parts and technical support from Mississauga, ON."
    h["hero_image"] = "bk-hero-auto-350ga"
    h["hero_image_secondary"] = ["bk-hero-hub", "nt-h10f-1-cut"]
    h["hero_points"] = ['<a href="#premium-line">Premium line: Bekamak</a>, Ø9″ to 59″ (230–1500 mm)',
                        '<a href="#value-line">Value line: NovoTech</a>, Ø9-7/8″ to 23-5/8″ (250–600 mm) — semi-automatic, automatic and double-column',
                        '<a href="#bekamak-manual-band-saws-overview">Manual</a> (Bekamak), <a href="#bekamak-semi-automatic-band-saws-overview">semi-automatic</a>, <a href="#bekamak-automatic-band-saws-overview">automatic</a> and <a href="#bekamak-double-column-band-saws-overview">double-column</a> saws',
                        '<a href="#buying-guide">Band saw buying guide</a>, blade selection and troubleshooting chart on this page']
    h["catalogue_pdfs"] = [PDF_BK, PDF_NF]
    h["range_lead"] = "Capacity at 0° for every model, one table per line. Each row links to the full specification table with miter capacities, blade sizes, motors and dimensions."
    h["section_label"] = "Band saws"
    h["related_blurb"] = "Both lines side by side: every Bekamak and NovoTech value-line band saw, the capacity tables and the band saw buying guide."
    h["origin_feature"] = {"title": "Two lines, one standard of support", "text": "Bekamak saws are built in Turkey with European components; value-line saws in China to North American standards."}
    json.dump(h, open(hp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("pages:", [sp["slug"] for ln in lines for sp in ln["subpages"]])


if __name__ == "__main__":
    main()
