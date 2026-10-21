"""Build content/families/bandsaw.json (Bekamak premium line) from the catalogue extractions in
/home/claude/bekamak/data/*.json and the website crawl /home/claude/bekamak/site/products.json,
and register the website photos in tools/image_map.json (section "bandsaw").

    python3 -I tools/bandsaw_data.py
"""
import json, os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = "/home/claude/bekamak/data"
SITE = json.load(open("/home/claude/bekamak/site/products.json", encoding="utf-8"))
IMG_DIR = "/home/claude/bekamak/site/img"

# ---- catalogue models by name ----------------------------------------------------------------
cat = {}
for fn in ("pivot-a.json", "pivot-b.json", "dc-a.json", "dc-b.json"):
    for fam in json.load(open(os.path.join(DATA, fn)))["families"]:
        for m in fam["models"]:
            cat[m["name"].replace(" NC", "")] = m

def norm(t):
    return t.upper().replace("-", "").replace(" ", "")
site_by_name = {norm(v["title"]): (k, v) for k, v in SITE.items()}

def site_rec(model):
    key = norm(model)
    for cand in (key, key.replace("ECO", "ECO"), key + "NC", key.replace("NC", "")):
        if cand in site_by_name:
            return site_by_name[cand]
    return None, None

def dedupe(items):
    out = []
    for i in items:
        i = i.strip()
        if i and i not in out:
            out.append(i)
    return out

# ---- family definitions (copy written for the website) ------------------------------------------
FAMILIES = [
 dict(id="bekamak-bms-dg", group="manual", name="BMS DG manual double-miter band saws", short="BMS manual saws",
      models=["BMS 230DG", "BMS 270DG"],
      summary="Gravity-feed pivot band saws for the maintenance shop and light fabrication: the operator swings the bow, a hydraulic cylinder controls the descent and the head swivels both ways for miter cuts up to 60°. Two-speed motor, mechanical blade tensioner with microswitch, electric coolant system.",
      features=["Bow swivels left and right: miter cuts to +60° / −45°", "Hydraulic cylinder for controlled, adjustable descent", "Variable blade speed: two-speed motor on the BMS 230DG (inverter optional), stepless 15–120 m/min inverter standard on the BMS 270DG", "Manual vise with quick-approach; cutting-length stop", "Safety switches on the wheel cover and blade guard", "Electric coolant pump and blade brush", "Options: 10 ft (3 m) roller table, micro-spray lubrication"],
      summary="The most popular Bekamak pivot saws: automatic bow lift after every cut, with the head swivelling both ways for miters — right to 60°, left to 45°. DGH versions have a hydraulic vise; the DG versions clamp by hand. Sizes from Ø9″ (230 mm) to Ø17-3/8″ (440 mm).",
      features=["Semi-automatic cycle: the bow descends at the set feed and returns after the cut; hydraulic vise on the DGH models (manual vise on the 230DG / 270DG)", "Double miter: +60° right and −45° left, head swung by hand on the angle scale", "Inverter drive for stepless blade speed 15–120 m/min (standard from the 270 up; optional on the 230DG / 230DGH)", "Hydro-mechanical blade tension with safety switch; blade brush; coolant pump", "Bow height-adjustment switch; cutting-pressure control on the 440DGH", "Heavy-duty gearbox from the 270 up; control panel", "Options: 10 ft (3 m) roller table, micro-spray lubrication; hydraulic top clamp, laser line pointer and motorized roller table on the 440DGH"]),
 dict(id="bekamak-bmsy-g", group="semi-automatic", name="BMSY 320G / 320GL semi-automatic single-miter band saws", short="BMSY 320G/GL",
      models=["BMSY 320G", "BMSY 320GL"],
      summary="Semi-automatic Ø12-5/8″ (320 mm) saws that miter to one side up to 60°; the 320GL has a longer bow for 24″ (610 mm) wide stock at 0°.",
      features=["Hydraulic vise and automatic bow return", "Miter cutting to one side: 0° to 60°", "Inverter drive, 15–120 m/min blade speed", "Hydro-mechanical blade tension with safety switch", "Blade brush, coolant pump, 2° inclined blade for faster cutting", "Optional hydraulic top clamping and 10 ft roller table"]),
 dict(id="bekamak-bmsy-straight", group="semi-automatic", name="BMSY 280–440 semi-automatic band saws", short="BMSY straight-cut",
      models=["BMSY 280", "BMSY 320", "BMSY 320L", "BMSY 350M", "BMSY 440"],
      summary="Straight-cutting pivot saws with hydraulic vise and automatic head lift, from Ø11″ (280 mm) to Ø17-3/8″ (440 mm); the 320L bow passes 24″ (610 mm) wide flats and the 350M bundles tube.",
      features=["Semi-automatic cycle with hydraulic vise", "Inverter drive, blade speed 15–120 m/min", "Hydro-mechanical blade tension, blade brush, coolant pump", "Adjustable cutting-length stop and material roller", "Options: hydraulic top clamping, chip conveyor, turn table, 10 ft motorized roller table"]),
 dict(id="bekamak-bmso-roller", group="automatic", name="BMSO 230–440 automatic roller-feed band saws", short="BMSO roller-feed",
      models=["BMSO 230", "BMSO 320", "BMSO 320L", "BMSO 440"],
      summary="Fully automatic pivot saws with roller material feed: set the length and quantity and the machine feeds, clamps, cuts and counts. Ø9″ (230 mm) to Ø17-3/8″ (440 mm), 24″ (610 mm) wide on the 320L.",
      features=["Automatic feeding by driven rollers; hydraulic vise on the 320 / 320L", "Piece counter and length setting on the control panel", "Automatic bow return; inverter blade speed (standard on the 320 / 320L, optional on the BMSO 230)", "Hydro-mechanical blade tension, blade brush, coolant pump, mechanical top clamp, 4 ft (1.2 m) roller table", "Options: hydraulic blade tension and chip conveyor (320 / 320L), micro-spray lubrication, 10 ft (3 m) roller table"]),
 dict(id="bekamak-bmso-e", group="automatic", name="BMSO E automatic band saws with encoder feed", short="BMSO E encoder-feed",
      models=["BMSO 230E", "BMSO 320E", "BMSO 350E"],
      summary="Roller-feed automatic saws with an encoder measuring the fed length for accurate repeat cuts, Ø9″ (230 mm) to Ø13-3/4″ (350 mm).",
      features=["Encoder-controlled roller feed for precise length", "Automatic cycle with piece counter", "Hydraulic vise; heavy-duty gearbox; 4 ft (1.2 m) roller table standard", "Inverter blade speed 15–120 m/min; blade brush; coolant pump", "Options: hydraulic blade tension, chip conveyor, microspray"]),
 dict(id="bekamak-bmso-ga", group="automatic", name="BMSO 350GA automatic single-miter band saw", short="BMSO 350GA",
      models=["BMSO 350GA"],
      summary="Roller-feed automatic saw that also miters to one side up to 60° — automatic repeat cutting of angled structural parts up to Ø13-3/4″ (350 mm).",
      features=["Encoder-measured roller feed with hydraulic feed vise; NC controller for length and quantity", "Single miter 0°–60°: the head is swung by hand and locked at the set angle", "Inverter blade speed, hydro-mechanical blade tension, heavy-duty gearbox", "Blade brush, coolant pump, mechanical top clamp, 4 ft (1.2 m) roller table standard", "Options: chip conveyor, micro-spray lubrication, 10 ft (3 m) roller table"],
      summary="NC automatic saws with servo-driven shuttle vise feeding and a single-miter head to 60° (set by hand on the angle scale); the GLS bow takes 24″ (610 mm) wide material.",
      features=["Servo shuttle-vise feed with ball screw: ±0.1 mm length accuracy", "NC control with multi-program job list (length × quantity)", "Single miter to 60°: the head is swung by hand on the angle scale", "Hydraulic vise, inverter blade speed, hydro-mechanical blade tension", "Options: hydraulic top clamp, hydraulic blade tension, multi-segment vise jaws, micro-spray lubrication, 10 ft (3 m) roller table"]),
 dict(id="bekamak-bmso-dgs", group="automatic", name="BMSO 270DGS servo-feed double-miter band saw", short="BMSO 270DGS",
      models=["BMSO 270DGS"],
      summary="Compact NC automatic saw that feeds with a servo shuttle vise and miters both ways — automatic production of angled parts up to Ø10-5/8″ (270 mm).",
      features=["Motorized shuttle-vise feeding (39″ / 1000 mm stroke); touch-screen control with a 10-step program", "Double miter +60° / −45°, head swung by hand", "Hydraulic vise, hydro-mechanical blade tension, coolant pump", "Options: hydraulic top clamp, micro-spray lubrication, 10 ft (3 m) roller table"],
      summary="Twin-column saws for straight cutting of heavy bar, billet and bundles from Ø13″ (330 mm) to Ø40-1/8″ (1020 mm). The bow runs on two hardened columns for a rigid, square cut; hydraulic vise, automatic bow return and a 2° inclined blade are standard. SV versions have a split vise for cutting short pieces.",
      features=["Double-column guidance with hydraulic vise and automatic bow return", "2° inclined blade and heavy-duty gearbox for fast, square cuts", "Inverter drive, blade speed 15–120 m/min; hydro-mechanical blade tension", "Cutting-width adjustment lever, blade brush, coolant pump", "Options: split vise (SV), hydraulic top clamping, chip conveyor, roller tables"]),
 dict(id="bekamak-bmsy-cgh", group="double-column", name="BMSY CGH semi-automatic single-miter double-column band saws", short="BMSY CGH miter",
      models=["BMSY 325CGH", "BMSY 440CGH", "BMSY 540CGH", "BMSY 810CGH"],
      summary="Double-column rigidity with a head that rotates up to 60° for miter cuts on beams and heavy sections, from Ø12-3/4″ (325 mm) to Ø31-7/8″ (810 mm).",
      features=["Single miter 0°–60°: the head is swung by hand on the angle scale; digital angle display and hydraulic angle clamping on the 540CGH / 810CGH", "Twin-column bow guidance; hydraulic vise; automatic bow return", "Inverter blade speed, hydro-mechanical blade tension, 3° inclined blade, optical bow height adjustment", "Blade brush, coolant pump, cutting-pressure control", "Options: hydraulic top clamp, hydraulic blade tension, chip conveyor, laser line pointer, micro-spray lubrication, 10 ft (3 m) roller tables (plain or motorized)"]),
 dict(id="bekamak-bmsy-dg-nc", group="double-column", name="BMSY DG NC semi-automatic double-miter double-column band saws", short="BMSY DG NC double-miter",
      models=["BMSY 360CDGH", "BMSY 440CDGH", "BMSY 560DG", "BMSY 650DG", "BMSY 750DG"],
      summary="Heavy double-column miter saws whose head swivels both ways; on the 650DG and 750DG NC versions the operator enters the angle and the saw positions itself. Ø14-1/8″ (360 mm) to Ø29-1/2″ (750 mm).",
      features=["Double-miter head: NC-controlled rotation on the 650DG / 750DG NC, hand-swung turntable on the 440CDGH / 560DG", "Twin-column guidance, hydraulic vise, automatic bow return", "Inverter blade speed; hydraulic blade tension on the 650DG / 750DG, hydro-mechanical on the 440CDGH / 560DG", "Chip conveyor standard on the 650DG / 750DG (optional on the 560DG); options: hydraulic top clamp, laser line pointer, micro-spray lubrication, 10 ft (3 m) roller tables"]),
 dict(id="bekamak-bmso-c", group="double-column", name="BMSO C automatic roller-feed double-column band saws", short="BMSO C automatic",
      models=["BMSO 330C", "BMSO 460C", "BMSO 560C", "BMSO 825C"],
      summary="Automatic straight-cutting double-column saws with roller material feed and piece counting, from Ø13″ (330 mm) up to the 825C.",
      features=["Automatic roller feed with hydraulic feed vise", "Piece counter and length setting", "Twin-column guidance, hydraulic vise, inverter blade speed", "Hydro-mechanical blade tension, blade brush, coolant pump, 4 ft (1.2 m) roller table", "Options: hydraulic blade tension, chip conveyor, split vise (330C), laser line pointer, micro-spray lubrication, 10 ft (3 m) roller tables"]),
 dict(id="bekamak-bmso-cs", group="double-column", name="BMSO CS NC fully automatic servo-feed double-column band saws", short="BMSO CS NC servo",
      models=["BMSO 330CS", "BMSO 420CS", "BMSO 560CS", "BMSO 570CS", "BMSO 820CS", "BMSO 1110CS"],
      summary="Production saws with ball-screw servo shuttle-vise feeding and PLC touch-screen control: job lists of length and quantity run unattended with ±0.1 mm repeatability. Ø13″ (330 mm) to Ø43-3/4″ (1110 mm).",
      features=["Servo shuttle-vise feed on ball screw; multi-program PLC touch screen", "Twin-column guidance; hydraulic vise on feed and cutting side", "Inverter blade speed; blade-slippage sensor; hydro-mechanical blade tension (hydraulic blade tension standard on the 570CS / 820CS, optional below)", "Chip conveyor on most sizes, blade brush, coolant pump", "Options: hydraulic top clamp, multi-segment (bundle) vise jaws, hexagonal vise jaws, micro-spray lubrication, 15 kW (20 HP) main motor, roller tables"]),
 dict(id="bekamak-bmso-cgs", group="double-column", name="BMSO CGS / CDGS NC automatic miter double-column band saws", short="BMSO CGS/CDGS miter NC",
      models=["BMSO 325CGS", "BMSO 440CGS", "BMSO 540CGS", "BMSO 440CDGS"],
      summary="Servo-feed automatic double-column saws with a miter head and digital angle display — single miter on the CGS, both sides on the CDGS — for unattended cutting of angled parts up to Ø21-1/4″ (540 mm).",
      features=["Servo shuttle-vise feeding with NC job programming", "Miter head 0°–60° (CGS) or +60° / −45° (CDGS), swung by hand with digital angle display; hydraulic angle clamping on the 440CGS / 540CGS", "Twin-column guidance, hydraulic vise, inverter blade speed", "Hydro-mechanical blade tension, blade brush, coolant pump, 3° inclined blade", "Options: hydraulic blade tension, hydraulic top clamp, chip conveyor, laser line pointer, micro-spray lubrication, 10 ft (3 m) roller table"]),
 dict(id="bekamak-bmso-xs", group="double-column", name="BMSO XS high-tech production band saws", short="BMSO XS high-tech",
      models=["BMSO 335XS", "BMSO 420XS", "BMSO 570XS", "BMSO 660XS", "BMSO 825XS"],
      summary="Bekamak's top production line: servo bow feed and servo material feed, full enclosure and CNC control for carbide blades and the shortest cycle times. Ø13-1/4″ (335 mm) to Ø32-1/2″ (825 mm).",
      features=["Servo-driven bow feed and servo shuttle-vise material feed", "CNC control with cutting database and remote diagnostics", "Enclosed cabin design, carbide-blade capable, high blade speeds", "Hydraulic vises on both sides, hydraulic blade tension, LED work light", "Options: pallet-type chip conveyor, hydraulic top clamp, hexagonal vise jaws, 15 kW (20 HP) main motor, micro-spray lubrication"]),
 dict(id="bekamak-bmsy-heavy", group="double-column", name="BMSY 1110C–1515C heavy-duty band saws", short="BMSY heavy-duty",
      models=["BMSY 1110C", "BMSY 1113C", "BMSY 1122C", "BMSY 1313C", "BMSY 1515C"],
      summary="Large semi-automatic saws for forging shops, steel service centres and mould makers — blocks and bundles up to 59″ (1500 mm) wide on a massive welded body with a reinforced bow.",
      features=["Capacities from Ø43-3/4″ (1110 mm) to 59″ × 59″ (1500 × 1500 mm)", "Twin-column guidance with hydraulic vise and automatic bow return", "Heavy-duty gearbox and high-power main motor; inverter blade speed", "Hydraulic blade tension, chip conveyor, motorized swarf brush", "Options: second vise (standard on the 1515C), hydraulic top clamp, laser line pointer, micro-spray lubrication, 10–13 ft (3–4 m) motorized roller tables"]),
]

def alt_for(model, i, n):
    return f"Bekamak {model} band saw" + ("" if i == 0 else f" — photo {i + 1} of {n}")

imap_path = os.path.join(ROOT, "tools", "image_map.json")
imap = json.load(open(imap_path, encoding="utf-8"))
fam_out = {}
order = []
for F in FAMILIES:
    fid = F["id"]; order.append(fid)
    models = []
    images = []
    std, opt = [], []
    for name in F["models"]:
        m = cat.get(name)
        if not m:
            print("!! no catalogue data for", name)
            continue
        models.append(dict(m, name=name))
        slug, rec = site_rec(name)
        if rec:
            std += rec["standard"]; opt += rec["optional"]
            n = len(rec["images"])
            for i, fn in enumerate(rec["images"]):
                key = "bk-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + f"-{i + 1}"
                if key not in imap:
                    imap[key] = {"src": os.path.join(IMG_DIR, fn), "alt": alt_for(name, i, n), "section": "bandsaw", "trim": False, "quality": 82}
                images.append(key)
        else:
            print("   (no website page for", name, ")")
    fam_out[fid] = {
        "id": fid, "brand": "bekamak", "line": "premium", "group": F["group"],
        "name": F["name"], "short": F["short"], "models_label": " · ".join(F["models"]),
        "summary": F["summary"], "features": F["features"],
        "optional": dedupe(opt)[:10],
        "images": images, "videos": [],
        "specs": {"kind": "bandsaw", "models": models},
    }
    print(f"{fid:24s} models={len(models)} images={len(images)}")

json.dump({"order": order, "families": fam_out}, open(os.path.join(ROOT, "content", "families", "bandsaw.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("families:", len(fam_out), "| image map entries:", len(imap))
