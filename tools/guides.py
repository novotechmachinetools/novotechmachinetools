"""Buying guides — one short guide per product category, embedded at the bottom of the category or hub page (before the FAQ)
and listed on the Articles page.

Each guide is an HTML fragment in content/articles/<file> made of <section class="guide-section" id=…><h3>…</h3>…</section>
blocks, with <figure class="guide-figure" data-img="image key"></figure> placeholders for photos.  This script writes
content/extra_groups/guide-<page>.json, which build.py applies to the page (article, article_id, article_title, article_intro),
so the generators that write the pages need not change.  The Articles page (tools/site_pages.py) lists every guide from GUIDES.

    python3 tools/guides.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Articles page sections, in order
TOPICS = [
    ("bending", "Bending and forming"),
    ("cutting", "Cutting and sawing"),
    ("punching", "Punching, shearing and notching"),
    ("tube", "Tube, pipe and wire"),
    ("sheet", "Sheet metal, HVAC and metal shaping"),
    ("finishing", "Deburring, grinding and finishing"),
    ("welding", "Welding"),
    ("presses", "Presses"),
    ("machining", "Drilling, milling and CNC machining"),
    ("rebar", "Rebar"),
    ("windows", "Window and door machinery"),
]

BY = "Written by NovoTech's sales engineers and technicians from years of installing machines in Canada."


def G(page, file, title, topic, intro, card, image=None, featured=False):
    return dict(page=page, file=file, title=title, topic=topic, intro=intro, card=card, image=image, featured=featured)


GUIDES = [
    # ------------------------------------------------------------------------------------------- bending and forming
    G("press-brake", "press-brake-guide.html", "Press brake buying guide", "bending",
      "What we go through with customers before they buy a press brake: air bending and the V-die, the tonnage and length a part "
      "needs, hydraulic, hybrid or electric drives, CNC axes and crowning, tooling, and the safety review. " + BY,
      "Air bending and the V-die, the tonnage formula with a quick chart, hydraulic, hybrid and electric drives, back gauge axes, "
      "crowning, tooling and the Ontario pre-start review.", featured=True),
    G("panel-bender", "panel-bender-guide.html", "Panel bender buying guide", "bending",
      "What we explain to customers before they buy a panel bender: how it bends, which parts it pays for, how capacity is rated, "
      "manual or automatic tooling, programming and automation. " + BY,
      "How a panel bender folds four sides in one set-up, when it beats a press brake, how capacity is rated, and what automatic "
      "tool change and robot loading add."),
    G("v-grooving-machine", "v-grooving-guide.html", "V-grooving machine buying guide", "bending",
      "What we explain to customers before they buy a V-grooving machine: why groove before bending, horizontal or vertical "
      "machines, groove depth and angle, bending the grooved panel, and what to compare. " + BY,
      "Sharp corners in stainless and aluminum panels: why groove, horizontal or vertical machines, groove depth and angle, and how "
      "grooved panels are bent."),
    G("folder-sheet-metal-brake", "sheet-metal-brake-guide.html", "Sheet metal brake buying guide", "bending",
      "What we explain to customers before they buy a sheet metal brake: hand, box and pan, magnetic and hydraulic folders, how "
      "capacity is rated in gauges, bend radius, short flanges and box depth, and what to check. " + BY,
      "Hand, box and pan, magnetic and hydraulic brakes compared, how capacity is rated in gauges of steel, stainless and aluminum, "
      "and folder or press brake."),
    G("horizontal-press-brake", "horizontal-press-brake-guide.html", "Horizontal press brake buying guide", "bending",
      "What we explain to customers before they buy a horizontal press brake: what it does that a vertical brake cannot, how to "
      "size it, which tools you need, and how the NC and back gauge speed up repeat parts. " + BY,
      "Bending, punching, shearing and straightening bar on one machine: sizing by flat bar and holes, the tools to order, and the "
      "NC recipes and back gauge."),
    G("angle-rolls", "angle-roll-guide.html", "Angle roll buying guide", "bending",
      "What we explain to customers before they buy an angle roll or section bender: how it works, why the section and its "
      "orientation set the capacity, twist and roll sets, horizontal or vertical working, NC and spirals. " + BY,
      "How three rolls bend sections into rings, why the section matters more than its size, twist and roll sets, and NC and "
      "spiral bending."),
    # ------------------------------------------------------------------------------------------- tube, pipe and wire
    G("pipe-benders", "tube-bender-guide.html", "Tube and pipe bender buying guide", "tube",
      "What we go through with customers before they buy a tube or pipe bender: CLR, D of bend and wall factor, push-type, rotary "
      "draw or mandrel bending, when a mandrel is needed, manual, NC or CNC, and tooling. " + BY,
      "Tube or pipe, CLR, D of bend and wall factor, which bending method, when you need a mandrel, NC or CNC, and the tooling to "
      "order."),
    G("tube-end-forming-machines", "tube-end-forming-guide.html", "Tube end forming buying guide", "tube",
      "What we explain to customers before they buy a tube end former: expanding, reducing, beading and flaring, ram, IO or "
      "rotary forming, how to size the machine, tooling and change-over, hydraulic or electric. " + BY,
      "Expanding, reducing, beading and flaring, ram, inner/outer or rotary forming, sizing by tube and wall, tooling and "
      "change-over."),
    G("wire-bending-machines", "wire-bender-guide.html", "CNC wire bender buying guide", "tube",
      "What we explain to customers before they buy a CNC wire bending machine: what it makes, wire size and material, why "
      "straightening decides the accuracy, 2D or 3D, programming and lines. " + BY,
      "From coil to finished part: wire size and strength, straightening and accuracy, 2D or 3D heads, programming and end-forming "
      "lines."),
    # ------------------------------------------------------------------------------------------- cutting
    G("laser-cutting-machine", "fiber-laser-guide.html", "Fiber laser cutting machine buying guide", "cutting",
      "What we go through with customers before they buy a fiber laser: the power for your thicknesses, bed size and exchange "
      "tables, oxygen, nitrogen or air, open or enclosed machines, the source and head, and what the laser needs on site. " + BY,
      "Laser power and thickness at a glance, single or exchange table, oxygen, nitrogen or air assist, open or enclosed machines "
      "and the running costs.", featured=True),
    G("tube-laser-cutting-machine", "tube-laser-guide.html", "Tube laser buying guide", "cutting",
      "What we explain to customers before they buy a tube laser: what it replaces, the chuck size, bar length and power you need, "
      "two or three chucks and the tail, loading, bevels, software and floor space. " + BY,
      "What a tube laser replaces, how to size the chucks, bar length and power, two or three chucks and the tail, loading, bevels "
      "and floor space."),
    G("cnc-plasma-table", "cnc-plasma-guide.html", "CNC plasma table buying guide", "cutting",
      "What we explain to customers before they buy a CNC plasma table: plasma, laser or oxy-fuel, the plasma source for your plate, "
      "drives and torch height control, water or downdraft tables, software and pipe cutting. " + BY,
      "Plasma, laser or oxy-fuel, the source for your plate, piercing and consumables, torch height control, water or downdraft "
      "tables and pipe cutting."),
    G("circular-cold-saws", "cold-saw-guide.html", "Cold saw buying guide", "cutting",
      "What we explain to customers before they buy a cold saw: cold saw, abrasive saw or band saw, HSS or carbide blades, "
      "capacity at 90° and on the miter, manual to automatic saws, and speed and coolant. " + BY,
      "Cold saw, abrasive saw or band saw, HSS or carbide blades and tooth pitch, capacity on the miter, and manual, semi-automatic "
      "or automatic saws."),
    G("band-saw-blades", "band-saw-blade-guide.html", "Band saw blade guide", "cutting",
      "How to order the right band saw blade and make it last: width, thickness, length, pitch and tooth material, choosing the "
      "pitch from the contact length, breaking in a new blade, and tension, guides and coolant. " + BY,
      "The five things that define a blade, choosing the pitch from the contact length, breaking in a new blade and the habits "
      "that make blades last."),
    G("aluminum-and-pvc-upcut-saws", "upcut-saw-guide.html", "Upcut saw buying guide", "cutting",
      "What we explain to customers before they buy a saw for aluminum and PVC profiles: upcut, double-head or top-down saws, "
      "blade size and the profile chart, blades, feed and cooling for each material, and measuring. " + BY,
      "Upcut, double-head or top-down saw, the blade size for your largest profile, aluminum or PVC blades, feeds and cooling, "
      "and measuring conveyors."),
    G("plate-beveler", "plate-beveler-guide.html", "Plate beveller buying guide", "cutting",
      "What we explain to customers before they buy a plate bevelling machine: why bevel cold, shearing or milling bevellers, how "
      "to size the machine by the bevel face, bevelling both sides, pipe and discs, and running costs. " + BY,
      "Cold bevelling for weld preparation, shearing or milling bevellers, sizing by the bevel face, INV and REV machines, pipe and "
      "discs."),
    G("circle-cutters-and-seamers", "circle-cutter-guide.html", "Circle cutting machine buying guide", "cutting",
      "What we explain to customers before they buy a circle cutting or flanging machine: how circle shears work, size and "
      "thickness, clamping and drive, and cutting and flanging tank heads on one machine. " + BY,
      "How a circle shear cuts blanks and rings, choosing the diameter and thickness, clamping and drive, and cutting and flanging "
      "tank heads."),
    # ------------------------------------------------------------------------------------------- punching and shearing
    G("shear-cutting", "shear-guide.html", "Metal shear buying guide", "punching",
      "What we go through with customers before they buy a shear: mechanical, hydraulic, swing beam or guillotine, how capacity "
      "and length are rated, rake angle and blade gap, back gauges, sheet support and safety. " + BY,
      "Which kind of shear, how capacity is rated in mild steel, stainless and aluminum, rake angle and blade gap, back gauges "
      "and sheet support.", featured=True),
    G("hydraulic-punching-machines", "punching-machine-guide.html", "Hydraulic punching machine buying guide", "punching",
      "What we explain to customers before they buy a hydraulic punch: the tonnage a hole takes, the smallest hole a punch can "
      "make, throat depth and die clearance, manual, NC or CNC tables, and punch or ironworker. " + BY,
      "The tonnage formula for round and shaped holes, the smallest hole you can punch, throat depth, die clearance and CNC "
      "tables."),
    G("pipe-notcher", "tube-notcher-guide.html", "Tube notcher buying guide", "tube",
      "What we explain to customers before they buy a tube notcher: why cope tube ends, belt, hole-saw or end-mill notchers, size "
      "and angle range, and belts, dust and safety. " + BY,
      "Why a good cope makes a better weld, belt, hole-saw or end-mill notchers, size and angle range, belts and dust collection."),
    # ------------------------------------------------------------------------------------------- sheet metal, HVAC, shaping
    G("bead-rollers", "bead-roller-guide.html", "Bead roller buying guide", "sheet",
      "What we explain to customers before they buy a bead roller: what beads and roll sets do, capacity and throat depth, "
      "hand-crank, motorized or hydraulic machines, and tips for straight, clean beads. " + BY,
      "What bead rollers make, capacity and throat depth, hand-crank, motorized or hydraulic top rolls, roll sets and tips for "
      "clean beads."),
    G("lock-former", "lock-former-guide.html", "Lock former buying guide", "sheet",
      "What we explain to HVAC shops before they buy a lock former: the seams and connectors it makes, which gauge range, material "
      "allowance and set-up, and the machines of a duct shop. " + BY,
      "Pittsburgh locks, snap locks, seams and cleats, choosing the gauge range, material allowance, and the machines of a duct "
      "line."),
    G("power-hammer", "power-hammer-guide.html", "Power and planishing hammer buying guide", "sheet",
      "What we explain to customers before they buy a power hammer or a planishing hammer: what each hammer does, throat, frame "
      "and dies, air and power, and sizing an air forging hammer. " + BY,
      "Planishing hammer, power hammer or air forging hammer: what each does, throat and frame stiffness, dies and anvils, and "
      "ram weight for forging."),
    # ------------------------------------------------------------------------------------------- finishing
    G("sheet-metal-plate-deburring-edge-rounding-finishing-grinding", "deburring-machine-guide.html", "Deburring machine buying guide",
      "finishing",
      "What we explain to customers before they buy a deburring machine: why deburr and round edges, belts and brushes, which "
      "machine for laser, plasma and coated parts, width and small parts, and dust and wet machines. " + BY,
      "Why burrs and sharp edges matter for coating, belts and brushes, the right machine for laser, plasma and coated parts, and "
      "dust and wet machines."),
    G("belt-grinder", "belt-grinder-guide.html", "Belt grinder buying guide", "finishing",
      "What we explain to customers before they buy a belt grinder: platen, contact wheel and slack belt, belt width and motor "
      "power, speeds and abrasives, disc sanders and chamfering machines, and dust and safety. " + BY,
      "Belt width and motor power, belt speeds for steel, stainless and aluminum, abrasives and grits, and dust and safety."),
    G("corner-grinding-machines", "corner-grinder-guide.html", "Corner grinder buying guide", "finishing",
      "What we explain to customers before they buy a corner grinder: what it does, hand-fed or automatic machines, radius, box "
      "height and edge length, abrasives and finish, and special machines. " + BY,
      "Grinding the welded corners of boxes and doors: hand-fed or automatic, radius and box height, and abrasives for a finish "
      "that disappears."),
    G("pipe-sanding-polishing-machines", "pipe-sander-guide.html", "Pipe sander buying guide", "finishing",
      "What we explain to customers before they buy a pipe sander: which machine for which tube, straight or bent, finish and "
      "grit, and keeping stainless clean. " + BY,
      "Belt, orbital, centreless and large-pipe sanders, straight or bent tube, grits for a satin or mirror finish, and keeping "
      "stainless clean."),
    # ------------------------------------------------------------------------------------------- welding
    G("laser-welding-machine", "laser-welding-guide.html", "Laser welding machine buying guide", "welding",
      "What we explain to customers before they buy a laser welder: when laser welding beats TIG and MIG, the power you need, "
      "portable or production welders, laser safety in the shop, and robots and cladding. " + BY,
      "When a laser welder beats TIG and MIG, the power for your thickness, air-cooled or water-cooled welders, laser safety and "
      "robotic cells."),
    G("welding-positioners", "welding-positioner-guide.html", "Welding positioner buying guide", "welding",
      "What we explain to customers before they buy a welding positioner: what it does, the weight and off-centre load it takes, "
      "the table speed formula, fixtures, chucks and grounding. " + BY,
      "What a positioner does for round welds, rating for weight and off-centre loads, the table speed formula, and fixtures and "
      "grounding."),
    G("corner-welding-machines", "corner-welding-guide.html", "Corner welding machine buying guide", "welding",
      "What we explain to customers before they buy a corner welding machine: what it does, why the copper blocks matter, which "
      "parts fit, and TIG or plasma. " + BY,
      "Welding the corners of bent boxes by machine: the copper blocks, part sizes, and TIG or plasma with the right power "
      "source."),
    # ------------------------------------------------------------------------------------------- presses
    G("hydraulic-press", "hydraulic-press-guide.html", "Hydraulic press buying guide", "presses",
      "What we explain to customers before they buy a hydraulic press: the tonnage for pressing, straightening and bending, "
      "H-frame, C-frame or column presses, working space and controls, and shop or production presses. " + BY,
      "Sizing the tonnage for press fits, straightening and bending, H-frame, C-frame or column, working space, controls and "
      "safety."),
    # ------------------------------------------------------------------------------------------- machining
    G("drill-press", "drill-press-guide.html", "Drill press buying guide", "machining",
      "What we explain to customers before they buy a drill press: the drilling capacity you need, gear-head, belt or inverter "
      "drives, the spindle speed formula, tapping, and work holding and power. " + BY,
      "Choosing the capacity, gear-head, belt or inverter drive, the rpm formula for steel, stainless and aluminum, tapping and "
      "work holding."),
    G("milling-machine", "milling-machine-guide.html", "Milling machine buying guide", "machining",
      "What we explain to customers before they buy a milling machine: turret, universal or drill-mill, table, travels and "
      "rigidity, spindle taper and power, power feed and DRO, and the tooling to start with. " + BY,
      "Turret, universal or drill-mill, table and travels, ISO40 or ISO50, power feed and DRO, and the tooling to budget for."),
    G("cnc-machine-tools", "cnc-machine-tools-guide.html", "CNC machine tool buying guide", "machining",
      "What we explain to customers before they buy a CNC lathe or machining centre: which machine for which parts, travels and "
      "swing, spindle taper and power, the control, tool changers and options, and the foundation. " + BY,
      "CNC lathe, vertical machining centre or boring mill, sizing the travels, BT40 or BT50, choosing the control, options and "
      "installation."),
    # ------------------------------------------------------------------------------------------- rebar
    G("rebar-bender-and-cutter", "rebar-guide.html", "Rebar bender and cutter buying guide", "rebar",
      "What we explain to customers before they buy a rebar bender or cutter: Canadian bar sizes and grades, how to read the "
      "capacity tables, bend diameters and pins, output per shift, and power and winter work. " + BY,
      "Canadian bar sizes and grades in one table, reading the 45 / 65 / 85 kg/mm² capacity columns, bend diameters and pins, and "
      "output per shift."),
    # ------------------------------------------------------------------------------------------- windows
    G("pvc-aluminum-window-machines", "window-machinery-guide.html", "Window and door machinery buying guide", "windows",
      "What we explain to customers before they set up a window and door shop: the steps and their machines, sizing the line by "
      "output, PVC or aluminum, profile systems and tooling, and air, power and layout. " + BY,
      "The steps of a window shop and the machine for each, sizing the line by windows a shift, PVC or aluminum, and air, power and "
      "layout."),
    G("corner-notcher", "corner-notcher-guide.html", "Corner notcher buying guide", "punching",
      "What we explain to customers before they buy a corner notcher: what it does, fixed or variable angle, thickness, notch "
      "size and material, hydraulic, pneumatic or manual drive, and how to size the notch. " + BY,
      "What a corner notcher does, fixed 90° or variable angle, capacity in mild steel, stainless and aluminum, and getting the "
      "notch right."),
]


def build():
    out_dir = os.path.join(ROOT, "content", "extra_groups")
    pages_dir = os.path.join(ROOT, "content", "pages")
    seen, done = set(), 0
    for fn in os.listdir(out_dir):                       # clear the guide files of an earlier run
        if fn.startswith("guide-") and fn.endswith(".json"):
            os.remove(os.path.join(out_dir, fn))
    for g in GUIDES:
        if g["page"] in seen:
            raise SystemExit(f"two guides for {g['page']}")
        seen.add(g["page"])
        if not os.path.exists(os.path.join(ROOT, "content", "articles", g["file"])):
            raise SystemExit(f"missing content/articles/{g['file']}")
        page = json.load(open(os.path.join(pages_dir, g["page"] + ".json"), encoding="utf-8"))
        if page.get("article"):
            raise SystemExit(f"{g['page']} already has a guide ({page['article']})")
        x = {"slug": g["page"], "set": {"article": g["file"], "article_id": "buying-guide", "article_title": g["title"],
                                        "article_intro": g["intro"]}}
        with open(os.path.join(out_dir, f"guide-{g['page']}.json"), "w", encoding="utf-8") as fh:
            json.dump(x, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        done += 1
    print(f"guides: {done} pages")


def update_llms():
    """the '## Buying guides' section of src/root/llms.txt: one line per guide (rewritten on every run)"""
    path = os.path.join(ROOT, "src", "root", "llms.txt")
    text = open(path, encoding="utf-8").read()
    head = "## Buying guides"
    if head in text:
        before, rest = text.split(head, 1)
        nxt = rest.find("\n## ")
        after = rest[nxt + 1:] if nxt >= 0 else ""
    else:
        before, after = text.rstrip("\n") + "\n\n", ""
    domain = "https://novotechmachinetools.com/"
    lines = [head, "", "Short buying guides written by NovoTech's technicians; each sits at the bottom of its product page, "
                       "before the FAQ.", ""]
    older = [("Band saw buying guide", "band-saw#buying-guide", "pivot or double-column, manual to automatic, blades, speeds and "
                                                                "feeds, troubleshooting."),
             ("Plate roller buying guide", "plate-rollers#buying-guide", "3-roll or 4-roll, initial or double pinch, capacity ratings, "
                                                                         "cones, crowning, automation."),
             ("Ironworker buying guide", "ironworker-machines#buying-guide", "sizing by punching tonnage, stations, shears, safety, "
                                                                             "build quality."),
             ("Press brake tooling guide", "press-brake-tooling-punch-and-die#tooling-guide", "clamping styles, V opening, tonnage chart, "
                                                                                             "sectioned tools.")]
    for t, href, d in older:
        lines.append(f"- [{t}]({domain}{href}): {d}")
    for g in GUIDES:
        lines.append(f"- [{g['title']}]({domain}{g['page']}#buying-guide): {g['card']}")
    open(path, "w", encoding="utf-8").write(before + "\n".join(lines) + "\n" + (("\n" + after) if after else ""))


def cards():
    """the Articles page cards for the guides: href, title, image, topic, text"""
    out = []
    for g in GUIDES:
        image = g["image"]
        if not image:
            page = json.load(open(os.path.join(ROOT, "content", "pages", g["page"] + ".json"), encoding="utf-8"))
            image = page.get("hero_image")
        out.append({"href": f"{g['page']}.html#buying-guide", "title": g["title"], "image": image,
                    "topic": dict(TOPICS)[g["topic"]], "group": g["topic"], "text": g["card"], "featured": g["featured"]})
    return out


if __name__ == "__main__":
    build()
    update_llms()
