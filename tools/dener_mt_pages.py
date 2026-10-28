#!/usr/bin/env python3
"""Dener machine-tool pages: cnc-lathe (TTC / TTH), vertical-machining-center (TMC vertical, TDC double-column) and
surface-grinder (TGH-B 450), under the cnc-machine-tools hub — family set content/families/dener-mt.json, photos from
tools/dener_mt_photos.py (section 'dener').

    python3 tools/dener_mt_photos.py                      # frames of NovoTech's videos → tools/src-images/dener, Shorts thumbnails
    python3 tools/dener_mt_pages.py                       # families + pages + image_map entries (tools/dener_mt_keys.txt)
    python3 tools/yt_thumbs.py $(cat tools/dener_mt_vids.txt)
    python3 tools/make_images.py --only $(cat tools/dener_mt_keys.txt)
    python3 tools/brochure/build_brochure.py tools/brochure/specs/cnc-lathe.json   (… machining-centres, surface-grinder)
    python3 tools/machine_tools_hub.py                    # the hub, after this and tools/ttmc_more_pages.py
"""
import json
import os

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families
import dener_mt_data as D
import dener_mt_photos as PH
import dener_pages as DP
import machine_tools_nav as MTN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "dener-mt"
BRAND = D.BRAND
PDF_LATHE = "files/NovoTech-Dener-CNC-Lathes-2026.pdf"
PDF_MC = "files/NovoTech-Dener-Machining-Centres-2026.pdf"
PDF_GRIND = "files/NovoTech-Dener-Surface-Grinder-2026.pdf"

BRAND_LINE = ("Dener builds its CNC lathes, machining centres and grinders in Kayseri, Turkey, in the machine-tool plant it took over "
              "from Taksan in 2016. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Turkey by Dener Makina",
          "text": "Dener has built machinery in Kayseri since 1974 — press brakes, shears and lasers first, and since 2016 CNC machine tools "
                  "in the Taksan plant: 155,000 m² of factory buildings on a 1.3 million m² site, with castings machined and machines "
                  "assembled in-house."}
INTRO_VIDEO = {"intro_video": {"id": "_bkvwzuOYW0", "title": "DENER machining centre and turning centre assembly line", "thumb": "video-_bkvwzuOYW0",
                               "duration": "PT0M25S"},
               "intro_video_heading": "Inside the factory — where the machines are built",
               "intro_video_text": "The assembly hall in Kayseri, Turkey, where Dener's machining centres and lathes are built up from their own castings."}
COMMON_RELATED = [{"href": "milling-machine.html", "label": "Milling machines"}, {"href": "drill-press.html", "label": "Drill presses"},
                  {"href": "band-saw.html", "label": "Band saws"}, {"href": "belt-grinder.html", "label": "Belt grinders and sanders"}]
INSTALL_FAQ = {"q": "Do you deliver, install and train in Canada?",
               "a": "Yes. Machines ship from Kayseri to Mississauga, ON, Canada; NovoTech unloads, levels and commissions the machine, checks "
                    "the geometry, trains your operators and programmers on the control and helps with the first parts. Every machine comes "
                    "with a CSA-approved panel, a 1-year warranty and parts and service from Mississauga. Ask for the foundation drawing and "
                    "the power and air requirements before the machine ships."}

PAGE_LATHE = dict(
    title="CNC Lathes for Sale — Slant-Bed, 6″–12″ Chucks | NovoTech",
    meta="CNC lathes for sale in Canada: Dener TTC and TTH slant-bed CNC lathes with Fanuc control, 12-station servo turret, 6″ to 12″ "
         "chucks, Ø27.6″ swing and C-axis live tooling. Made in Turkey.",
    h1="Dener CNC lathes — TTC and TTH slant-bed lathes, 6″ to 12″ chucks",
    intro="A CNC lathe turns, faces, bores, grooves and threads round parts from bar stock or chucked blanks, with its tools on a turret that "
          "brings the next one into position in a fraction of a second. NovoTech sells Dener's CNC lathes in Canada, built in Kayseri, "
          "Turkey, in the machine-tool plant Dener took over from Taksan in 2016. Both families share one design: a one-piece cast bed "
          "inclined at 45°, roller linear guides with C1 and C3 ballscrews coupled straight to the servo motors, a 12-station servo turret "
          "that indexes in 0.2 s, a hydraulic chuck and a hydraulic tailstock, under a Fanuc 0i-TF Plus control (Mitsubishi M80 to order). "
          "The compact TTC-6 and TTC-8 swing Ø22″ (560 mm) with 6″ and 8″ chucks; the TTH-8, TTH-10 and TTH-12 swing Ø27.6″ (700 mm), turn "
          "parts to Ø20.8″ × 26.8″ and go up to a 12″ chuck, 3.74″ (95 mm) bar and 602 lb·ft of spindle torque. A BMT55 C-axis turret with "
          "12 live tools turns any of them into a turn-mill centre. Installed, programmed with you and supported from Mississauga, ON, Canada.",
    points=["TTC-6 / TTC-8: Ø22″ swing, turning Ø12″ × 17″, 6″ or 8″ chuck, 6,000 / 4,500 rpm",
            "TTH-8 / 10 / 12: Ø27.6″ swing, turning Ø20.8″ × 26.8″, 8″ to 12″ chucks, bar to Ø3.74″ (95 mm)",
            "Fanuc 0i-TF Plus, 12-station servo turret, hydraulic tailstock; C-axis live tooling, bar feeder and probes to order"],
    hero="dn-ttc-1", minis=["dn-tth-1", "dn-ttc-2"],
    groups=[("lathe-ttc", "TTC compact CNC lathes", "Ø22″ swing with 6″ and 8″ chucks — the compact slant-bed lathe for shafts, flanges and bushings in series.", BRAND),
            ("lathe-tth", "TTH CNC lathes", "Ø27.6″ swing with 8″ to 12″ chucks — longer and heavier work, up to Ø20.8″ × 26.8″, and a 4.65″ spindle bore on the TTH-12.", BRAND)],
    faq=[{"q": "TTC or TTH — which lathe do I need?",
          "a": "Choose by the largest part and the bar you feed. The TTC turns parts up to Ø12″ × 17″ (305 × 433 mm) from a 6″ or 8″ chuck and "
               "takes bar to 1.77″ (TTC-6) or 2.05″ (TTC-8): the machine for shafts, pins, flanges and bushings in series. The TTH swings "
               "Ø27.6″, turns to Ø20.8″ × 26.8″ (528 × 680 mm) and has 8″, 10″ and 12″ chucks with bar to 2.05″, 2.95″ and 3.74″; the "
               "TTH-12's A2-11 spindle, 4.65″ bore and 602 lb·ft of torque are for large diameters, pipe and heavy roughing. Send us a drawing "
               "of your largest part and we check it against the working range."},
         {"q": "Why a 45° slant bed?",
          "a": "On a slant bed the chips fall away from the tools and the guideways straight into the chip conveyor, the turret sits behind "
               "the spindle where the cutting force pushes into the casting, and the operator reaches the chuck easily over the low front. "
               "Dener casts the bed in one piece, stress-relieves it and lays it out by finite-element analysis, so it damps vibration in "
               "interrupted and heavy cuts."},
         {"q": "Fanuc or Mitsubishi?",
          "a": "Dener lathes for North America come with the Fanuc 0i-TF Plus as standard, the control most Canadian programmers and service "
               "technicians already know; the Mitsubishi M80 is available instead. Both run ISO G-code with canned turning, grooving and "
               "threading cycles and take programs from any CAM system. The spindle motor differs slightly between the two (see the table)."},
         {"q": "What does the C-axis option add?",
          "a": "A BMT55 turret with 12 live (driven) tools at up to 6,000 rpm and a spindle that indexes and holds position: cross holes, "
               "tapped holes, flats, slots, hex and keyways are machined in the same setup instead of on a mill. The largest turning "
               "diameter and length are a little smaller with the live-tool turret — both are in the table."},
         {"q": "Can it run unattended?",
          "a": "With the automatic bar feeder and a parts catcher a lathe runs through a bar without the operator; the tool-setting arm and "
               "workpiece probe measure offsets and parts in the cycle, and the automatic door opens and closes for a robot. All are "
               "options on both families."},
         INSTALL_FAQ, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about CNC lathes",
    related_pages=COMMON_RELATED,
    related_title="More metalworking machinery from NovoTech",
)

PAGE_MC = dict(
    title="Vertical Machining Center, BT40 & Double-Column BT50 | NovoTech",
    meta="Vertical machining centers (VMC) for sale in Canada: Dener TMC, BBT40, 10,000 rpm, 24 tools, X 33.5 – 63″, and TDC double-column "
         "machining centers, BBT50, X to 161.4″. Made in Turkey.",
    h1="Dener vertical machining centers — TMC VMCs and TDC double-column, BBT40 and BBT50",
    intro="A machining centre mills, drills, bores and taps prismatic parts under CNC and changes its own tools from a magazine, so a part "
          "that once went from the mill to the drill press to the tapping arm is finished in one setup. NovoTech sells Dener's machining "
          "centres in Canada, built in Kayseri, Turkey: the TMC vertical machining centres (VMC) in five sizes, from the TMC 850 with 33.5 × 20.1 × "
          "22″ (850 × 510 × 560 mm) travels to the TMC 1600 with 63 × 27.6 × 27.6″ (1,600 × 700 × 700 mm), all with a direct-drive BBT40 "
          "spindle at 10,000 rpm, a 24-tool arm changer and rapids of 1,417 in/min (36 m/min); and the TDC double-column (gantry) machining "
          "centres for long, wide and heavy parts — 82.7 to 161.4″ (2,100 – 4,100 mm) of X travel, 55 to 82.7″ between the columns, tables "
          "to 157.5 × 70.9″ for 26,455 lb (12,000 kg) and a BBT50 spindle with through-spindle coolant. Mitsubishi M80A control with Navi-Mill "
          "conversational programming as standard, Fanuc to order. Installed and supported from Mississauga, ON, Canada.",
    points=["TMC 850 – 1600: X 33.5 – 63″, tables to 68.9 × 27.6″ and 2,646 lb, BBT40 10,000 rpm (12,000 / 15,000 optional), 24 tools",
            "TDC 2112 – 4120: X 82.7 – 161.4″, 55 – 82.7″ between the columns, tables to 157.5 × 70.9″ and 26,455 lb, BBT50, 24 or 40 tools",
            "Mitsubishi M80A with Navi-Mill (Fanuc optional); C3 ballscrews, roller guides, ±0.00016″ positioning on the TMC"],
    hero="dn-tmc-1", minis=["dn-tdc-1", "dn-tmc-2"],
    groups=[("mc-vertical", "TMC vertical machining centres", "Five sizes from 33.5 to 63″ of X travel — BBT40, 10,000 rpm, 24 tools, fully enclosed.", BRAND),
            ("mc-double", "TDC double-column machining centres", "Gantry machines for long, wide and heavy parts — 82.7 to 161.4″ of X travel, BBT50, tables to 26,455 lb.", BRAND)],
    faq=[{"q": "Vertical or double-column machining centre?",
          "a": "A vertical machining centre carries the part on a table that moves in X and Y under a spindle on a single column — the "
               "standard machine for brackets, housings, plates and moulds up to the size of its table — 39 × 20″ to 69 × 28″ on the TMC. A double-column "
               "machine puts the spindle on a cross rail between two columns over a long table: it takes parts far wider and heavier than a "
               "vertical's single column could, keeps its rigidity over the whole width, and machines machine bases, plates, frames and large "
               "moulds. The TMC runs to 63 × 27.6″ of travel and 2,646 lb on the table; the TDC starts at 82.7 × 48″ and carries up to 26,455 lb."},
         {"q": "BBT40, BBT50 — will my CAT40 holders fit?",
          "a": "BBT is BT with the BIG-PLUS dual-contact face: the holder seats on the taper and on the spindle face at once, which stiffens "
               "the tool. Standard BT holders fit a BBT spindle too. CAT40 holders do not: the taper is the same 7/24 but the flange and the "
               "pull stud are different, so plan for BT or BBT holders — we quote a starter set with the machine. BBT50 carries larger face "
               "mills and boring bars and takes heavier cuts than BBT40."},
         {"q": "How accurate are they?",
          "a": "Dener specifies ±0.004 mm (±0.00016″) positioning and ±0.002 mm repeatability per 300 mm on the TMC (±0.005 mm on the "
               "TMC 1600), and ±0.008 / ±0.004 mm on the TDC. Double-nut C3 ballscrews coupled directly to the servo motors, roller linear "
               "guides, spindle cooling and stress-relieved Meehanite castings keep it there; linear scales are an option for closed-loop "
               "positioning."},
         {"q": "Which control, and how are they programmed?",
          "a": "The Mitsubishi M80A with a 15″ touchscreen is standard, with Navi-Mill conversational programming for simple parts at the "
               "machine; Fanuc 0i-MF is an option. Both run ISO G-code from any CAM system, with rigid tapping, canned cycles and 4th-axis "
               "control for the optional rotary table."},
         {"q": "Which options are worth it?",
          "a": "Through-spindle coolant at 435 psi (30 bar) for deep drilling and pocketing (standard on the TDC); a 12,000 or 15,000 rpm "
               "spindle if you cut mostly aluminum; a tool setter and workpiece probe to cut setup time; a CNC rotary table for four-sided work; "
               "and linear scales for the tightest work. The chip conveyor, chip wash-down, oil skimmer and spindle cooling are standard."},
         {"q": "What foundation, power and air do they need?",
          "a": "The TMC machines need 32 kVA (43 kVA for the 1300 and 1600), 73 – 87 psi of shop air and a level reinforced-concrete floor; "
               "the TDC machines, at 21 to 40 tonnes, sit on a foundation built to Dener's drawing. We send the drawings and the floor-space "
               "plan with the quote."},
         INSTALL_FAQ, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about machining centres",
    related_pages=COMMON_RELATED,
    related_title="More metalworking machinery from NovoTech",
)

PAGE_GRIND = dict(
    title="Precision NC Surface Grinder, 18 × 35″ Table | NovoTech",
    meta="Surface grinder for sale in Canada: the Dener TGH-B 450 precision NC surface grinder, 17.7 × 35.4″ table, 15.7 × 31.5″ magnetic "
         "chuck, Ø13.8″ wheel, Mitsubishi NC down feed in 0.00004″ steps. Made in Turkey.",
    h1="Dener NC surface grinder — TGH-B 450, 17.7 × 35.4″ table",
    intro="A surface grinder finishes flat, parallel and square faces to tenths: the part sits on a magnetic chuck on a table that runs back "
          "and forth under a grinding wheel, the wheel steps across at each stroke and comes down a few tenths at a time until the face is "
          "true. NovoTech sells the Dener TGH-B 450 in Canada, built in Kayseri, Turkey: a 17.7 × 35.4″ (450 × 900 mm) table on scraped, "
          "Turcite-B coated V and flat guideways, driven hydraulically at 16 – 82 ft/min, a Ø13.8″ (350 mm) wheel on a direct-drive spindle "
          "with 21.7″ (550 mm) under the wheel centre, and AC servo motors on ballscrews for the cross and vertical axes under a Mitsubishi NC "
          "with a 10″ touchscreen — the operator sets the stock to remove, and the machine down-feeds in 0.00004″ (0.001 mm) steps and "
          "cross-feeds 0.002 – 0.79″ per stroke by itself. Installed and supported from Mississauga, ON, Canada.",
    points=["17.7 × 35.4″ table, 15.7 × 31.5″ electromagnetic chuck, 882 lb table load, 3 – 21.7″ under the wheel centre",
            "Mitsubishi NC with 10″ touchscreen: automatic down feed in 0.00004″ steps and cross feed 0.002 – 0.79″ per stroke",
            "Direct-drive spindle 100 – 1,450 rpm, Ø13.8″ wheel; hydraulic table 16 – 82 ft/min on scraped V and flat ways"],
    hero="dn-tgh-1", minis=["dn-tgh-4", "dn-tgh-6"],
    groups=[("grind", "TGH NC surface grinder", "A 450 × 900 mm precision surface grinder with NC cross and down feed and a hydraulic table.", BRAND)],
    faq=[{"q": "What does the NC do on a surface grinder?",
          "a": "On a manual grinder the operator turns the handwheels for every pass. On the TGH-B 450 the cross and vertical axes are AC servo "
               "axes under the Mitsubishi NC: the operator enters the stock to remove, the down feed per pass and the cross feed, and the "
               "machine grinds the face — roughing, finishing and spark-out passes — while the hydraulic table runs back and forth. The "
               "handwheel stays for touching off and setup."},
         {"q": "How large a part can it grind?",
          "a": "Faces up to 35.4 × 17.7″ (900 × 450 mm) on the 15.7 × 31.5″ (400 × 800 mm) electromagnetic chuck, parts up to 882 lb (400 kg), "
               "and up to 21.7″ (550 mm) from the table to the wheel centre — about 14.8″ of part height under a new Ø13.8″ wheel."},
         {"q": "Which accessories are worth adding?",
          "a": "A magnetic sine plate and sine bar for angled faces, a precision toolmaker's vise for non-magnetic parts, a magnetic separator "
               "with the paper filter for long coolant life, a wheel-head diamond dresser and a profile dressing attachment for formed "
               "wheels, and a demagnetizer for finished parts. A second wheel flange makes wheel changes quick."},
         INSTALL_FAQ, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about surface grinders",
    related_pages=[{"href": "belt-grinder.html", "label": "Belt grinders and sanders"}] + COMMON_RELATED[:3],
    related_title="More metalworking machinery from NovoTech",
)


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "dener")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if os.path.splitext(x)[0] == key]
        if not f:
            raise SystemExit(f"missing export for {key} — run tools/dener_mt_photos.py")
        imap[key] = {"src": f"tools/src-images/dener/{f[0]}", "alt": p["alt"], "section": "dener", **PH.image_map_spec(key)}
        keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "dener_mt_keys.txt"), "w").write(",".join(keys))
    return keys


def build():
    pdfs = {D.P_LATHE: DP.pdf(PDF_LATHE, "Download the Dener CNC lathe brochure"),
            D.P_MC: DP.pdf(PDF_MC, "Download the Dener machining centre brochure"),
            D.P_GRIND: DP.pdf(PDF_GRIND, "Download the Dener surface grinder brochure")}
    fams = [dict(f, pdf=pdfs[f["page"]]) for f in D.FAMILIES]
    write_families(SET, fams)
    common = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, **INTRO_VIDEO}
    nav = {s: n for s, n, _ in MTN.siblings()}
    for slug, page in ((D.P_LATHE, PAGE_LATHE), (D.P_MC, PAGE_MC), (D.P_GRIND, PAGE_GRIND)):
        write_category(slug, page, [f for f in fams if f["page"] == slug], SET, MTN.SECTION, hub=MTN.hub(), siblings=MTN.siblings(),
                       extra={**common, "nav_label": nav[slug], "catalogue_pdf": pdfs[slug]})
        path = os.path.join(ROOT, "content", "pages", f"{slug}.json")
        pj = json.load(open(path, encoding="utf-8"))
        pj["section"]["related_title"] = MTN.RELATED_TITLE              # 'CNC', not 'cnc' (the template lower-cases the label)
        json.dump(pj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    keys = register_images()
    used = {k for f in fams for k in f["images"]} | {p["hero"] for p in (PAGE_LATHE, PAGE_MC, PAGE_GRIND)} | \
           {m for p in (PAGE_LATHE, PAGE_MC, PAGE_GRIND) for m in p["minis"]}
    missing = sorted(used - set(keys))
    if missing:
        raise SystemExit(f"image keys without a photo: {missing}")
    unused = sorted(set(keys) - used)
    if unused:
        print("photos not used on a page:", unused)
    vids = sorted({v["id"] for f in fams for v in f["videos"]} | {INTRO_VIDEO["intro_video"]["id"]})
    open(os.path.join(ROOT, "tools", "dener_mt_vids.txt"), "w").write(" ".join(vids))
    print(f"dener-mt: {len(fams)} families ({sum(len(f['specs']['models']) for f in fams)} models) on 3 pages · images: {len(keys)} · videos: {len(vids)}")


if __name__ == "__main__":
    build()
