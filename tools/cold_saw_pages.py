#!/usr/bin/env python3
"""The cold saw section (the owner, Nov 7 2026): a hub at the old cold saw URL (circular-cold-saws.html, hub.html) over two
pages — cold-saws.html, the manual and semi-automatic cold saws (ISITAN SFC, NovoTech value-line CS / PDS saws, abrasive saws,
roller stands), and automatic-cold-saws.html, the production saws that feed, cut and count by themselves (CSM CT325, Bekamak
BMDO XS / CS, OPUS 300).

The families come from content/families/pipe-end-and-saws.json (tools/isitan_pipe_end_saws.py) and ttmc-more.json
(tools/ttmc_more_pages.py); this script merges them into content/families/all-cold-saws.json, so run it after both:

    python3 tools/isitan_pipe_end_saws.py && python3 tools/ttmc_more_pages.py && python3 tools/cold_saw_pages.py
"""
import json
import os

from isitan_lib import PDF, PDF_BK, VOLT_FAQ_GENERIC, write_category, write_families, write_hub, write_json
import csm_pages as CSM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "all-cold-saws"
SECTION = "Cold saws"
HUB = "circular-cold-saws"
P_COLD, P_AUTO = "cold-saws", "automatic-cold-saws"
NO_VIDEO = {"intro_video": None, "intro_video_heading": None, "intro_video_text": None}

# (page, group id, group title, family set, family ids) — display order
GROUPS = [
    (P_COLD, "semi", "ISITAN premium line — semi-automatic cold saw", "pipe-end-and-saws", ["isitan-sfc-350-vx"]),
    (P_COLD, "manual", "ISITAN premium line — pull-down cold saws", "pipe-end-and-saws", ["isitan-sfc-v"]),
    (P_COLD, "tt-cold", "Cold saws · value line", "ttmc-more", ["tt-cs", "tt-pds315h", "tt-pds400"]),
    (P_COLD, "tt-abrasive", "Abrasive cut-off saws · value line", "ttmc-more", ["tt-tv"]),
    (P_COLD, "tt-stands", "Roller stands, roller conveyors and roller tables", "ttmc-more", ["tt-stand"]),
    (P_AUTO, CSM.SAW_GROUP[0], CSM.SAW_GROUP[1], "pipe-end-and-saws", ["csm-ct325"]),
    (P_AUTO, "bekamak-circular", "Bekamak automatic circular saws — TCT carbide and HSS", "pipe-end-and-saws",
     ["bekamak-bmdo-xs", "bekamak-bmdo-cs", "bekamak-opus-300"]),
]
ACCESSORIES = {"tt-stand"}      # on the cold saw page, not in the hub's model table

SUBPAGES = [
    (P_COLD, "Cold saws — manual and semi-automatic circular cold saws, 9″ to 16″ blades", "is-sfc-350-vx",
     "For the fabrication shop: ISITAN SFC pull-down and semi-automatic cold saws with 10-3/4 – 13-3/4″ blades, NovoTech value-line CS, "
     "PDS-315H and PDS-400 saws with 9 – 16″ blades, abrasive cut-off saws and roller stands.", "Cold saws"),
    (P_AUTO, "Automatic cold saws — carbide and HSS production saws, tube and bar to Ø11-3/4″", "bk-bmdo-150xs-1",
     "Production saws that feed, cut and count by themselves: the CSM CT325 with servo feed, the Bekamak BMDO XS carbide and BMDO CS "
     "HSS saws, and the OPUS 300 for solid bar to Ø11-3/4″.", "Automatic cold saws"),
]


def hub():
    return {"slug": HUB, "label": "All cold saws", "image": "is-sfc-350-vx",
            "blurb": "Manual, semi-automatic or automatic? Every cold saw NovoTech sells in Canada on one page, with the two kinds compared."}


def siblings():
    return [(s, nav, t.split(" — ")[0]) for s, t, _, _, nav in SUBPAGES]


FAQ_ABRASIVE = {"q": "Cold saw or abrasive chop saw?",
                "a": "An abrasive chop saw grinds through the steel at high speed, leaving a hot, burred, slightly bevelled end and sparks. A cold saw cuts with a slow HSS blade (45–90 rpm) under coolant, so the cut is square, cool to the touch, burr-free and ready to weld or fit — and the blade is resharpened dozens of times instead of thrown away."}
FAQ_TCT = {"q": "TCT carbide or HSS cold saw?",
           "a": "A carbide (TCT) blade runs at 130–920 ft/min and is the fastest way to cut solid steel bar in production — the Bekamak BMDO XS saws and the Ø11-3/4″ OPUS 300 are built around it, with servo feeding and a magazine loader for unattended runs. HSS blades run slower (22–130 ft/min on the BMDO CS) and are the choice for tube, thin walls and mixed work; the XS saws accept HSS blades for tube as well."}

COLD = dict(
    title="Cold Saws for Sale in Canada — Manual & Semi-Automatic Circular Cold Saws, 9″ to 16″ Blades | NovoTech",
    meta="Manual and semi-automatic circular cold saws sold, installed and supported in Canada: ISITAN SFC saws with 10-3/4 – 13-3/4″ blades and mitre 45° both ways, NovoTech value-line CS, PDS-315H and PDS-400 saws with 9 – 16″ blades, abrasive cut-off saws and roller stands.",
    h1="Cold saws — manual and semi-automatic circular cold saws, 9″ to 16″ blades",
    intro="A cold saw cuts metal with a slow-turning, coolant-flooded circular blade instead of a hot abrasive disc, leaving a square, "
          "burr-free end that is cool to the touch and ready to weld. This page has the manual and semi-automatic cold saws for the "
          "fabrication shop: ISITAN's wet-type SFC 275 and 315 pull-down saws with a manual or pneumatic vise and the semi-automatic SFC "
          "350-VX with a hydro-pneumatic head, all mitring 45° both ways; NovoTech's value-line saws, built in China — gear-driven manual "
          "CS saws with 9 – 14″ blades, the PDS-315H semi-automatic hydraulic saw and the PDS-400 heavy-duty saw with a 16″ blade; "
          "abrasive cut-off saws with 12 – 16″ wheels; and roller stands, a roller conveyor with a digital length stop and a measuring "
          "roller table. Each family below has its full specification table and photos. For production saws that feed, cut and count by "
          "themselves, see the automatic cold saws. CSA-approved panels and support from Mississauga, ON, Canada.",
    points=["ISITAN SFC 275 / 315 pull-down saws and the SFC 350-VX semi-automatic: 10-3/4 – 13-3/4″ HSS blades, round to Ø4-1/2″, mitre 45° both ways",
            "NovoTech value line: CS cold saws 9 – 14″, PDS-315H semi-automatic hydraulic, PDS-400 heavy-duty 16″, TV abrasive saws 12 – 16″",
            "Roller stands, a roller conveyor with a digital length stop and a measuring roller table"],
    hero="is-sfc-350-vx", minis=["is-sfc-315-vp", "tm-pds400"],
    faq=[{"q": "Manual, pneumatic or semi-automatic?", "a": "The SFC V clamps with a hand vise — the simplest saw for occasional cuts. The SFC VP clamps with air at the pull of a lever, which saves time on every cut and holds short pieces better. The SFC 350-VX runs a semi-automatic cycle from a foot switch with a regulated head descent, for batches of the same part without an operator on the handle."},
         FAQ_ABRASIVE,
         {"q": "Which blade do I need?", "a": "A standard HSS blade cuts mild steel and aluminum. For medium-hard steel we fit TiN-coated blades, TiCN for high-strength steel and TiAlN for stainless. The blade bore is 32 mm with two Ø11 mm pin holes on all SFC models, so blades are readily available in Canada."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about cold saws",
    related_pages=[{"href": "band-saw.html", "label": "Band saws"}, {"href": "pipe-notcher.html", "label": "Tube notchers"},
                   {"href": "belt-grinder.html", "label": "Belt grinders and sanders"}],
    related_title="More cutting machinery from NovoTech",
)

AUTO = dict(
    title="Automatic Cold Saws for Sale in Canada — Carbide & HSS, Tube and Bar to Ø11-3/4″ | NovoTech",
    meta="Automatic circular cold saws sold, installed and supported in Canada: the CSM CT325 with servo feed for tube and bundles to Ø4″, Bekamak BMDO XS carbide saws for solid bar to Ø6-1/4″ from a 20 ft magazine, BMDO CS HSS saws and the OPUS 300 for solid bar to Ø11-3/4″.",
    h1="Automatic cold saws — carbide and HSS production saws, tube and bar to Ø11-3/4″",
    intro="An automatic cold saw feeds the bar, clamps it, cuts and counts by itself: the operator loads the bars, programs the lengths "
          "and quantities and the saw runs the batch. NovoTech sells two lines in Canada, all on this page: CSM's CT325 hydraulic circular "
          "saw with a servo carriage, cutting tube and bundles to Ø4″ in three spindle-speed ranges; and Bekamak's automatic production "
          "saws — the BMDO XS high-speed carbide (TCT) cold saws that cut solid bar to Ø6-1/4″ from a 20 ft magazine loader with servo "
          "feeding, the OPUS 300 with a Ø35-7/16″ (900 mm) carbide blade and a 50 HP spindle for solid bar to Ø11-3/4″, and the BMDO CS "
          "HSS saws for tube and bar to Ø4″ with a servo gripper feed and touch-screen control. Each family below has its full "
          "specification table and photos. For manual and semi-automatic saws, see the cold saws. CSA-approved panels and support from "
          "Mississauga, ON, Canada.",
    points=["CSM CT325: hydraulic down-feed, servo carriage to ±.004″, tube and bundles to Ø4″ in three spindle-speed ranges",
            "Bekamak BMDO XS carbide saws: solid bar Ø3/8″ – 6-1/4″ at up to 920 ft/min, servo feed, 20 ft magazine loader — and the OPUS 300 for bar to Ø11-3/4″",
            "Bekamak BMDO CS HSS saws: tube and bar to Ø4″, servo gripper feed to ±.004″, several lengths per bar"],
    hero="bk-bmdo-150xs-1", minis=["cs-ct325", "bk-opus-300-1"],
    faq=[{"q": "What does an automatic cold saw do by itself?", "a": "You load bars in the magazine (BMDO XS) or on the roller table (BMDO CS), program the lengths and quantities, and the saw feeds each bar with a servo gripper, clamps it hydraulically, cuts, counts and moves on to the next length — to ±.004″ on the CS and with a 60 mm remnant on the XS."},
         FAQ_TCT,
         {"q": "What is the CSM CT325 for?", "a": "Cutting tube to length in production, single or in bundles: the CT325 clamps hydraulically, feeds with a servo carriage to ±.004″ at 39 in/s and feeds the blade down hydraulically through planetary gears, with a PLC touch-screen and a pedestal with emergency stop. The L, M and H types differ only in spindle speed — steel, stainless and alloy, aluminum and non-ferrous. It is the saw CSM builds into its bending cells, and stands just as well on its own."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about automatic cold saws",
    related_pages=[{"href": "automatic-band-saws.html", "label": "Automatic band saws"}, {"href": "pipe-benders.html", "label": "Pipe & tube benders"},
                   {"href": "tube-end-forming-machines.html", "label": "Tube end forming machines"}],
    related_title="More cutting machinery from NovoTech",
)

HUB_PAGE = dict(
    title="Cold Saws for Sale in Canada — Manual, Semi-Automatic & Automatic Circular Cold Saws | NovoTech",
    meta="Every circular cold saw NovoTech sells in Canada, by kind: manual and semi-automatic cold saws with 9 – 16″ HSS blades, and automatic carbide and HSS cold saws with servo feed for tube and bar to Ø11-3/4″ — the two kinds compared, with a buying guide.",
    h1="Circular cold saws — manual, semi-automatic and automatic",
    intro="A cold saw cuts metal with a slow-turning, coolant-flooded circular blade instead of a hot abrasive disc, leaving a square, "
          "burr-free end that is cool to the touch and ready to weld. NovoTech sells two kinds in Canada, each on its own page: cold saws "
          "— the manual and semi-automatic circular saws of the fabrication shop: ISITAN SFC pull-down and semi-automatic saws with 10-3/4 "
          "to 13-3/4″ blades and NovoTech's value-line CS, PDS-315H and PDS-400 saws with 9 to 16″ blades, with abrasive cut-off saws and "
          "roller stands; and automatic cold saws — production saws that feed, cut and count by themselves: the CSM CT325 with servo feed "
          "for tube and bundles to Ø4″, the Bekamak BMDO XS carbide saws for solid bar to Ø6-1/4″, the BMDO CS HSS saws and the OPUS 300 "
          "for solid bar to Ø11-3/4″. Below, the two kinds compared, every model in one table, the buying guide and the questions we get "
          "asked; every machine comes with a CSA-approved panel and support from Mississauga, ON, Canada.",
    points=['<a href="cold-saws.html">Cold saws</a>: <a href="cold-saws.html#isitan-sfc-v">ISITAN SFC pull-down</a> and <a href="cold-saws.html#isitan-sfc-350-vx">semi-automatic</a> saws, 10-3/4 – 13-3/4″; value-line <a href="cold-saws.html#tt-cs">CS</a>, <a href="cold-saws.html#tt-pds315h">PDS-315H</a> and <a href="cold-saws.html#tt-pds400">PDS-400</a>, 9 – 16″',
            '<a href="automatic-cold-saws.html">Automatic cold saws</a>: <a href="automatic-cold-saws.html#csm-ct325">CSM CT325</a> with servo feed, <a href="automatic-cold-saws.html#bekamak-bmdo-xs">Bekamak BMDO XS</a> carbide, <a href="automatic-cold-saws.html#bekamak-bmdo-cs">BMDO CS</a> HSS and the <a href="automatic-cold-saws.html#bekamak-opus-300">OPUS 300</a> for bar to Ø11-3/4″'],
    hero="is-sfc-350-vx", minis=["bk-bmdo-150xs-1", "tm-pds400"],
    range_cols=["Blade", "Round capacity", "Motor", "Weight"],
    range_lead="Every cold saw NovoTech sells, in one table: blade, round capacity, motor and weight. Each row links to the full specification table on the cold saw or automatic cold saw page.",
    range_caption="Circular cold saws supplied by NovoTech — manual, semi-automatic and automatic",
    range_note="Capacities are the manufacturers' ratings for mild steel at 90°. Three-phase machines are supplied for 600 V as standard with a CSA-approved panel; 208, 240 and 480 V on request.",
    faq=[{"q": "Manual, semi-automatic or automatic — which do I need?",
          "a": "By the number of cuts. For a few cuts a day in a fabrication or maintenance shop, a manual cold saw — the operator pulls the head down — is the simplest machine; a semi-automatic saw runs the cut from a foot switch with a regulated head descent, for batches of the same part. When the same lengths are cut by the hundred, an automatic cold saw feeds the bar with a servo gripper, clamps, cuts and counts by itself. The manual and semi-automatic saws are on the cold saw page, the production saws on the automatic cold saw page."},
         FAQ_TCT, VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about cold saws",
    related_pages=[{"href": "band-saw.html", "label": "Band saws"}, {"href": "band-saw-blades.html", "label": "Band saw blades"},
                   {"href": "aluminum-and-pvc-upcut-saws.html", "label": "Aluminum & PVC saws"}],
    related_title="More cutting machinery from NovoTech",
)

COMPARE = {
    "title": "Which kind of cold saw?",
    "lead": "The two kinds NovoTech sells, side by side; each page lists every model of its kind.",
    "cols": ["", "Cold saws", "Automatic cold saws"],
    "rows": [
        ["Cycle", "The operator pulls the head down (manual) or starts the cut from a foot switch (semi-automatic)", "The saw feeds the bar, clamps, cuts and counts by itself"],
        ["Blades", "HSS, 9 – 16″", "HSS and carbide (TCT), Ø9-7/8″ to Ø35-7/16″"],
        ["Capacity", "Round to Ø4-3/4″", "Tube and bundles to Ø4″, solid bar to Ø6-1/4″ and Ø11-3/4″ (OPUS 300)"],
        ["Typical buyer", "Fabrication, welding and maintenance shops", "Production shops cutting tube and bar to length in batches"],
        ["Page", {"href": "cold-saws.html", "label": "Cold saws"}, {"href": "automatic-cold-saws.html", "label": "Automatic cold saws"}],
    ],
}

RANGE_PICK = [["blade", "blade_diameter_max", "wheel_diameter_max"], ["round", "round_90", "round_pipe_90_45", "round_pipe_90_45_60"],
              ["installed_power", "main_motor", "motor"], "weight"]


def build():
    sets = {}
    fams = []
    for page, gid, _, set_name, ids in GROUPS:
        if set_name not in sets:
            sets[set_name] = json.load(open(os.path.join(ROOT, "content", "families", f"{set_name}.json"), encoding="utf-8"))["families"]
        for fid in ids:
            fams.append(dict(sets[set_name][fid], id=fid, page=page, group=gid))
    write_families(SET, fams)
    for slug, page in ((P_COLD, COLD), (P_AUTO, AUTO)):
        members = [f for f in fams if f["page"] == slug]
        brands = {}
        for f in members:
            brands.setdefault(f["group"], set()).add(f.get("brand"))
        groups = []
        for pg, gid, title, _, _ in GROUPS:
            if pg != slug:
                continue
            if len(brands[gid]) != 1:
                raise SystemExit(f"{slug}: group {gid} has families of several brands")
            groups.append((gid, title, "", next(iter(brands[gid]))))
        pdfs = [PDF] if slug == P_COLD else [CSM.pdf("csm-ct325"), PDF_BK]
        extra = {"nav_label": next(nav for s, _, _, _, nav in SUBPAGES if s == slug), "catalogue_pdf": None, "catalogue_pdfs": pdfs}
        if slug == P_COLD:
            extra.update({"hero_brand_line": "ISITAN circular cold saws are made in Turkey by ISITAN Makine; NovoTech's value-line saws are built in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech.",
                          "origin_feature": {"title": "Made in Turkey, value line from China", "text": "ISITAN has built sheet-metal machinery in Bursa since 1959; NovoTech's value line is built in China to our specification — CSA-approved panels, a 1-year warranty and parts and support in Canada."}})
        else:
            extra.update({"hero_brand_line": "The CT325 is made in Taiwan by CSM and the automatic BMDO and OPUS saws by Bekamak Makina, Turkey. All sold, installed and supported in Canada by NovoTech.",
                          "origin_feature": {"title": "Made in Turkey and Taiwan", "text": "Bekamak has built saws since 1990 and CSM tube machinery in Tainan since 1982 — CE-certified machines with European components."},
                          **NO_VIDEO})
        write_category(slug, dict(page, groups=groups), members, SET, SECTION, hub=hub(), siblings=siblings(), extra=extra)
        print(f"{slug}: {len(members)} families, {sum(len(f['specs']['models']) for f in members)} models")
    in_range = [f for f in fams if f["id"] not in ACCESSORIES]
    write_hub(HUB, {**HUB_PAGE, "artifact_title": "Circular Cold Saws", "nav_label": "All cold saws", "related_blurb": hub()["blurb"]},
              in_range, SET, SECTION, [(s, t, im, b, nav) for s, t, im, b, nav in SUBPAGES],
              extra={"catalogue_pdf": None, "catalogue_pdfs": [PDF, CSM.pdf("csm-ct325"), PDF_BK], "range_pick": RANGE_PICK,
                     "hero_brand_line": "ISITAN and Bekamak saws are made in Turkey, the CT325 in Taiwan by CSM and NovoTech's value-line saws in China to NovoTech's specification. All sold, installed and supported in Canada by NovoTech.",
                     "origin_feature": {"title": "Two kinds, one supplier", "text": "Manual, semi-automatic and automatic cold saws from Turkey, Taiwan and NovoTech's value line — installed, trained and supported by the same NovoTech technicians in Canada."},
                     **NO_VIDEO, "related_pages": HUB_PAGE["related_pages"], "related_title": HUB_PAGE["related_title"],
                     "hub_compact": True, "compare": COMPARE, "subpage_link": "all models, specifications and photos"})
    path = os.path.join(ROOT, "content", "pages", f"{HUB}.json")
    page = json.load(open(path, encoding="utf-8"))
    for sp in page["subpages"]:
        sp["cards_title"] = sp["title"].split(" — ")[0] + " — every family"
    write_json(path, page)
    print(f"cold saw hub: {len(in_range)} families on {len(page['subpages'])} pages")


if __name__ == "__main__":
    build()
