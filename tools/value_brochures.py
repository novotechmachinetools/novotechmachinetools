#!/usr/bin/env python3
"""NovoTech-format brochures for every product that had none (the owner, Nov 7 2026: "no product without a PDF brochure").

Eight new value-line brochures, each made of the families of a few product pages that had no brochure, in the order of the
pages and their groups; the stray value-line families added to the brochure of their kind (ironworkers, hydraulic press brakes,
sheet metal shears); and the EUROSTAMP catalogue (which has the American-style tools) on the American-style tooling page.

    python3 tools/value_brochures.py      → tools/brochure/specs/value-*.json and content/family_pdfs.json
    python3 tools/brochure/build_brochure.py tools/brochure/specs/<spec>.json      (each spec printed at the end)
    python3 build.py                      → the brochure on every family, and on every page that had none

content/family_pdfs.json: {"families": {id: {file, label}}, "pages": {slug: {file, label}}} — build.py gives a family its brochure
only when it has none of its own, and a page only when it shows none.
"""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS = os.path.join(ROOT, "tools", "brochure", "specs")

VALUE_ABOUT = ("NovoTech's value line is our own brand: machines built in China to our specification by a maker that exports metalworking "
               "machinery to more than 70 countries, inspected before they ship and sold under NovoTech's name with a CSA-approved panel on "
               "every 3-phase machine, a 1-year warranty and parts and technical support from Mississauga, Ontario, Canada.")
VALUE_COMMON = dict(cover_line="NovoTech value line · built in China to North American standards · sold & serviced in Canada by NovoTech",
                    about_kicker="NovoTech value line", country="China", made_in="Built in China to North American standards",
                    single_phase=False, year="2026")

# spec file: (pages in order, output, label, texts)
NEW = {
    "value-sheet-metal-brakes.json": (
        ["hydraulic-folding-machine", "box-and-pan-brake", "sheet-metal-hand-brake", "magnetic-sheet-metal-brake", "roofing-siding-brake",
         "shear-brake-roll-3-in-1"],
        "NovoTech-Sheet-Metal-Brakes-Folders-Value-Line-2026.pdf", "Download the value-line sheet metal brake brochure",
        dict(title="Sheet metal brakes and folding machines",
             subtitle="Hydraulic, electric and CNC folders · box and pan brakes · straight brakes and foot-clamp folders · magnetic brakes · "
                      "roofing and siding brakes · 3-in-1 machines",
             range_label="Value-line sheet metal brakes", about_for="value-line sheet metal brakes and folding machines",
             about_title="Sheet metal brakes for the HVAC, roofing and fabrication shop",
             text="A sheet metal brake bends sheet by clamping it under a straight beam and swinging a folding leaf up around the edge: no "
                  "punch and die, no marks on painted sheet, and long, straight bends in thin material. From the largest machines to the "
                  "smallest: hydraulic, electric and CNC folding machines for 10 ga over 10 ft and production panels, box and pan brakes "
                  "with removable fingers, straight brakes and foot-clamp folders, magnetic brakes that fold boxes of any depth, portable "
                  "roofing and siding brakes for the job site and 3-in-1 shear, brake and roll machines.")),
    "value-grinding-finishing.json": (
        ["belt-grinder", "sheet-metal-plate-deburring-edge-rounding-finishing-grinding", "corner-grinding-machines", "plate-beveler"],
        "NovoTech-Grinders-Finishing-Machines-Value-Line-2026.pdf", "Download the value-line grinding and finishing brochure",
        dict(title="Grinding and finishing machines",
             subtitle="Belt grinders and sanders · disc sanders and bench grinders · end-surface grinders · dust collectors · deburring "
                      "and finishing machines · corner grinders · edge chamfering machines",
             range_label="Value-line grinding and finishing machines", about_for="value-line grinding and finishing machines",
             about_title="Grinding, deburring and finishing for the fabrication shop",
             text="Belt grinders take the burr off a cut, blend a weld and square an end faster than a hand grinder: pedestal, floor and "
                  "wide-belt grinders with 2 to 8″ belts, combination belt and disc machines, disc sanders, bench grinders and wire-wheel "
                  "machines, end-surface grinders and metal dust collectors; wide-belt deburring and finishing machines for laser-cut and "
                  "punched parts; corner grinders for welded boxes and frames; and edge chamfering machines for weld preps.")),
    "value-woodworking.json": (
        ["woodworking-machinery"],
        "NovoTech-Woodworking-Machinery-Value-Line-2026.pdf", "Download the value-line woodworking machinery brochure",
        dict(title="Woodworking machinery",
             subtitle="Jointers, thickness planers and jointer-planers · table saws and band saws · slot boring machines · wood lathe · "
                      "dust collector",
             range_label="Value-line woodworking machinery", about_for="value-line woodworking machinery",
             about_title="Machines for the cabinet, furniture and millwork shop",
             text="Rough lumber is milled in a fixed order: the jointer flattens a face and squares an edge, the thickness planer brings "
                  "the board to thickness, the table saw rips and crosscuts it and the band saw cuts curves and resaws. Slot boring "
                  "machines cut the joinery, the wood lathe turns, and the dust collector keeps the shop clean.")),
    "value-welding-automation.json": (
        ["welding-positioners", "welding-turning-rolls", "column-and-boom-welding-manipulators", "welding-tables"],
        "NovoTech-Welding-Automation-Value-Line-2026.pdf", "Download the value-line welding automation brochure",
        dict(title="Welding automation",
             subtitle="Welding positioners · rotary tables and lift positioners · welding turning rolls and pipe rotators · column and "
                      "boom manipulators · welding tables and downdraft tables",
             range_label="Value-line welding automation", about_for="value-line welding automation",
             about_title="Positioners, rolls and manipulators for the welding shop",
             text="Welding automation brings the seam to the welder: positioners tilt and turn the part so every weld is made flat, "
                  "turning rolls rotate vessels, tanks and pipe under the torch, column and boom manipulators carry the welding head along "
                  "the seam, and welding tables hold the parts square while downdraft tables draw off grinding dust and fumes.")),
    "value-presses-riveters.json": (
        ["hydraulic-shop-press", "h-frame-hydraulic-press", "c-frame-hydraulic-press", "hydraulic-straightening-press", "riveting-machine"],
        "NovoTech-Hydraulic-Presses-Riveting-Machines-Value-Line-2026.pdf", "Download the value-line press and riveting machine brochure",
        dict(title="Hydraulic presses and riveting machines",
             subtitle="Bench and workshop presses · four-column presses · C-frame presses · presses with sliding table · orbital "
                      "riveting machines",
             range_label="Value-line presses and riveting machines", about_for="value-line hydraulic presses and riveting machines",
             about_title="Presses for the repair shop and light production",
             text="A hydraulic press presses bearings and bushings, straightens shafts and bends flat bar one part at a time, or runs dies "
                  "cycle after cycle: bench presses for sheet-metal tooling, workshop and H-frame presses with a brake function, four-column "
                  "and C-frame presses for dies, presses with a sliding table for straightening, and orbital riveting machines that form "
                  "rivet heads with a tenth of a press's force.")),
    "value-saws.json": (
        ["cold-saws", "aluminum-and-pvc-upcut-saws"],
        "NovoTech-Cold-Saws-Cut-Off-Saws-Value-Line-2026.pdf", "Download the value-line cold saw brochure",
        dict(title="Cold saws and cut-off saws",
             subtitle="Cold saws 9 – 14″ · PDS semi-automatic and heavy-duty saws · abrasive cut-off saws · aluminum cut-off saws · "
                      "roller stands and conveyors",
             range_label="Value-line saws", about_for="value-line cold saws and cut-off saws",
             about_title="Saws for the fabrication shop",
             text="A cold saw cuts metal with a slow-turning, coolant-flooded blade and leaves a square, burr-free end that is cool to "
                  "the touch: gear-driven manual cold saws, a semi-automatic hydraulic saw and a heavy-duty 16″ saw, abrasive cut-off saws, "
                  "aluminum cut-off saws with pneumatic clamping, and the roller stands and conveyors that carry long bar to the saw.")),
    "value-hvac-sheet-metal.json": (
        ["bead-rollers", "lock-former", "circle-cutters-and-seamers", "corner-notcher"],
        "NovoTech-HVAC-Sheet-Metal-Machines-Value-Line-2026.pdf", "Download the value-line HVAC and sheet metal machine brochure",
        dict(title="HVAC and sheet metal machines",
             subtitle="Bead rollers and beading machines · lock formers and roll formers · circle cutters and flanging · corner notchers",
             range_label="Value-line HVAC and sheet metal machines", about_for="value-line HVAC and sheet metal machines",
             about_title="Machines for the HVAC and sheet-metal shop",
             text="The machines that turn flat sheet into duct and fittings: bead rollers and beading machines that stiffen panels and "
                  "roll the beads of round duct, lock formers and roll formers for the seams, circle cutters and flanging machines for "
                  "discs and end caps, and corner notchers that cut the corners of panels and boxes before they are folded.")),
    "value-rolls-benders.json": (
        ["angle-rolls", "hydraulic-3-roll-plate-rollers", "motorized-plate-rollers", "rotary-draw-tube-benders", "pipe-notcher",
         "horizontal-press-brake"],
        "NovoTech-Rolls-Benders-Tube-Machines-Value-Line-2026.pdf", "Download the value-line roll, bender and tube machine brochure",
        dict(title="Rolls, benders and tube machines",
             subtitle="Profile and ring benders · plate rolls and slip rolls · tube and pipe benders · tube notchers and end grinders · "
                      "horizontal benders",
             range_label="Value-line rolls, benders and tube machines", about_for="value-line rolls, benders and tube machines",
             about_title="Bending and tube machines for the fabrication shop",
             text="Machines that bend and shape bar, sections, plate and tube: profile and ring benders that roll angle, flat bar and "
                  "tube into rings, plate rolls and slip rolls, hydraulic and manual tube and pipe benders, tube notchers and belt tube-end "
                  "grinders that cope tube for welding, and hydraulic horizontal benders for flat bar.")),
}

# stray value-line families into the brochure of their kind: spec → (families, family set, groups to add)
ADD = {
    "value-ironworkers.json": (["tt-m55"], "ttmc-more", [{"title": "Compact single-cylinder ironworkers", "families": ["tt-m55"]}],
                               "files/NovoTech-Ironworkers-Value-Line-2026.pdf", "Download the value-line ironworker brochure"),
    "value-hydraulic-press-brakes.json": (["tt-hbv"], "ttmc-more", [{"title": "Hydraulic bending brakes", "families": ["tt-hbv"]}],
                                          "files/NovoTech-Hydraulic-Press-Brakes-2026.pdf", "Download the value-line press brake brochure"),
    "value-sheet-metal-shears.json": (["tt-bq01", "tt-ps1220"], "ttmc", [{"title": "Bench shears", "families": ["tt-bq01"]},
                                                                         {"title": "Coil slitting and cut-to-length machine", "families": ["tt-ps1220"]}],
                                      "files/NovoTech-Sheet-Metal-Shears-2026.pdf", "Download the value-line sheet metal shear brochure"),
}
TOOLING = ("files/NovoTech-Press-Brake-Tooling-Catalogue-2026.pdf", "Download the EUROSTAMP catalogue — inch edition")

# Bekamak models on bekamak.com that the Bekamak catalogue 2025/2026 does not have (the PDF check, Nov 7 2026): a NovoTech-format
# supplement, the families' brochure button; the Bekamak catalogue stays on the pages
BEKAMAK_SPEC = "bekamak-saws-supplement.json"
BEKAMAK_PDF = ("files/NovoTech-Bekamak-Saws-Supplement-2026.pdf", "Download the Bekamak supplement brochure")
BEKAMAK = dict(
    title="Bekamak saws — catalogue supplement 2026",
    subtitle="BMSO 320S servo-feed automatic band saw · BMSO CS NC double column band saws · TERRA 6 high-speed band saw · "
             "OPUS 300 carbide circular saw",
    cover_line="Bekamak · made in Turkey · sold & serviced in Canada by NovoTech",
    about_kicker="Bekamak · made in Turkey", country="Turkey", made_in="Made in Turkey by Bekamak with European components",
    range_label="Bekamak saws · supplement", about_for="Bekamak saws",
    about_title="The Bekamak models the 2025/2026 catalogue does not show",
    about_text=["Bekamak has built band saws in Turkey since 1990 with European components — NovoTech's premium line of band saws and "
                "circular saws, sold, installed and supported in Canada by NovoTech Machine Tools from Mississauga, Ontario.",
                "This supplement carries the Bekamak machines that are not in the Bekamak catalogue 2025/2026: the BMSO 320S servo-feed "
                "automatic band saw, the full BMSO CS NC double column range with the BMSO 460CS and the BMSO 1313CS for 51″ blocks, the "
                "TERRA 6 that runs its blade at up to 1,970 ft/min (600 m/min) and the OPUS 300 "
                "carbide circular saw for solid bar to Ø11-3/4″."],
    single_phase=False, year="2026",
    family_sets=["bandsaw", "all-cold-saws"],
    families=["bekamak-bmso-s", "bekamak-bmso-cs", "bekamak-terra-6", "bekamak-opus-300"],  # BMH 170 power hacksaw: taken off the site and out of the brochure (the owner, Nov 12 2026)
    groups=[{"title": "Automatic band saws", "families": ["bekamak-bmso-s"]},
            {"title": "Double column band saws", "families": ["bekamak-bmso-cs", "bekamak-terra-6"]},
            {"title": "Carbide circular saws", "families": ["bekamak-opus-300"]}],
    cover_photos=["bk-bmso-320s-1", "bk-terra-6-1", "bk-opus-300-1", "bk-bmso-820cs-1"],
    out="src/" + BEKAMAK_PDF[0])


def load_sets():
    sets = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "families", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if isinstance(d, dict) and isinstance(d.get("families"), dict):
            sets[os.path.basename(f)[:-5]] = d["families"]
    return sets


def page_groups(slug):
    """the page's groups with those other generators add (content/extra_groups), in the order the page shows them"""
    p = json.load(open(os.path.join(ROOT, "content", "pages", slug + ".json"), encoding="utf-8"))
    groups = [dict(g) for g in p.get("groups") or []]
    for fn in sorted(glob.glob(os.path.join(ROOT, "content", "extra_groups", "*.json"))):
        x = json.load(open(fn, encoding="utf-8"))
        if x.get("slug") != slug:
            continue
        for g in x.get("groups") or []:
            g = dict(g)
            after = g.get("after")
            i = next((k + 1 for k, h in enumerate(groups) if after and h.get("id") in (after, after + "-group")), len(groups))
            groups.insert(i, g)
    return p, groups


def clean_title(t):
    for s in (" · value line, built to order", " · value line", " · premium line"):
        t = t.replace(s, "")
    return t


def main():
    sets = load_sets()
    where = {}
    for name, fams in sets.items():
        for fid in fams:
            where.setdefault(fid, []).append(name)
    has_pdf = {fid for fams in sets.values() for fid, f in fams.items() if f.get("pdf")}
    out = {"families": {}, "pages": {}}
    built = []
    for spec_name, (pages, pdf_name, label, t) in NEW.items():
        file = "files/" + pdf_name
        fams, groups, used_sets, cover = [], [], [], []
        for slug in pages:
            page, gs = page_groups(slug)
            shows_pdf = bool(page.get("catalogue_pdf") or page.get("catalogue_pdfs"))
            mine = []
            for g in gs:
                # the value line only (tt- / dt-): the other brands show their maker's catalogue on every family
                ids = [fid for fid in g["families"] if isinstance(fid, str) and fid.startswith(("tt-", "dt-")) and fid not in has_pdf
                       and fid not in fams and fid in where]
                if ids:
                    groups.append({"title": clean_title(g["title"]), "families": ids})
                    fams += ids
                    mine += ids
            if mine and not shows_pdf:
                out["pages"][slug] = {"file": file, "label": label}
        if "sheet-metal-hand-brake" in pages:                 # the brake hub too
            out["pages"]["folder-sheet-metal-brake"] = {"file": file, "label": label}
        for fid in fams:
            for s in where[fid]:
                if s not in used_sets:
                    used_sets.append(s)
            out["families"][fid] = {"file": file, "label": label}
        # the cover: the first photo of the first three groups' first families, the first group's photo large in the middle
        for g in groups:
            f = next(sets[s][g["families"][0]] for s in where[g["families"][0]])
            if f.get("images") and f["images"][0] not in cover:
                cover.append(f["images"][0])
            if len(cover) == 3:
                break
        if len(cover) >= 2:
            cover[0], cover[1] = cover[1], cover[0]
        # the set that holds the families' latest data last (ttmc-more over the copies in the page sets)
        used_sets.sort(key=lambda s: s == "ttmc-more")
        spec = dict(VALUE_COMMON, title=t["title"], subtitle=t["subtitle"], range_label=t["range_label"], about_for=t["about_for"],
                    about_title=t["about_title"], about_text=[VALUE_ABOUT, t["text"]], family_sets=used_sets, families=fams,
                    groups=groups, cover_photos=cover, out="src/" + file)
        json.dump(spec, open(os.path.join(SPECS, spec_name), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        built.append(spec_name)
        print(f"{spec_name:34s} {len(fams):2d} families in {len(groups):2d} groups from {len(pages)} pages · sets {used_sets}")
    for spec_name, (ids, set_name, add_groups, file, label) in ADD.items():
        path = os.path.join(SPECS, spec_name)
        spec = json.load(open(path, encoding="utf-8"))
        for fid in ids:
            if fid not in spec["families"]:
                spec["families"].append(fid)
            out["families"][fid] = {"file": file, "label": label}
        if set_name not in spec["family_sets"]:
            spec["family_sets"].append(set_name)
        if spec.get("groups"):
            have = {f for g in spec["groups"] for f in g["families"]}
            spec["groups"] += [g for g in add_groups if not set(g["families"]) & have]
        json.dump(spec, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        built.append(spec_name)
        print(f"{spec_name:34s} + {ids}")
    json.dump(BEKAMAK, open(os.path.join(SPECS, BEKAMAK_SPEC), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for fid in BEKAMAK["families"]:
        out["families"][fid] = {"file": BEKAMAK_PDF[0], "label": BEKAMAK_PDF[1]}
    built.append(BEKAMAK_SPEC)
    print(f"{BEKAMAK_SPEC:34s} {len(BEKAMAK['families'])} Bekamak families")
    tooling = json.load(open(os.path.join(ROOT, "content", "pages", "american-style-press-brake-tooling.json"), encoding="utf-8"))
    for g in tooling["groups"]:
        for fid in g["families"]:
            out["families"][fid] = {"file": TOOLING[0], "label": TOOLING[1]}
    out["pages"]["american-style-press-brake-tooling"] = {"file": TOOLING[0], "label": TOOLING[1]}
    json.dump(out, open(os.path.join(ROOT, "content", "family_pdfs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"content/family_pdfs.json: {len(out['families'])} families, {len(out['pages'])} pages")
    print(" ".join(os.path.join("tools", "brochure", "specs", s) for s in built))


if __name__ == "__main__":
    main()
