#!/usr/bin/env python3
"""Detail photos for the press brake pages and the buying guide (Oct 28 2026):

  * tools/src-images/dener-detail/src/  — images of Dener's XL and DDM quotation documents (pdfimages): back gauges, front
    supports, rear gates, tool holders, quick clamps, the EUROSTAMP punch 1281 / 4-way die 2067, sheet followers, oil cooler,
    tandem; and the two EUROSTAMP tool profiles as DXF (the owner's files) → clean line drawings.
  * tools/src-images/controls/src/      — press brake controls: Delem's own cut-outs (DA-69S, DA-66S, DA-53Tx, DA-58Tx, DA-41T),
    Cybelec's CybTouch 12 photo, ESA cards and brochure images (S630, S840, S875 W), the value-line supplier's
    controller page (SCS920, Estun E21PS / E315PS crops).

Small images are upscaled 2x with Real-ESRGAN (tools/esrgan.py); a PDF image with a soft mask keeps its alpha.
Registered by tools/press_brake_hub.py (register_detail_images) — section "dener-detail" / "controls".

    python3 tools/dener_detail_photos.py [key …]
"""
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DET = os.path.join(ROOT, "tools", "src-images", "dener-detail")
CTL = os.path.join(ROOT, "tools", "src-images", "controls")
SMALL = 900            # px: a source whose longest side is under this is upscaled 2x


def D(src, alt, mask=None, up=True, cutout=False, crop=None, up2=False, arrows=False, upscale=None, rotate=0, min_width=0):
    """arrows=True: the figure is drawn with its axis arrows by tools/dener_bg_arrows.py (from the PDF page), not here"""
    return dict(src=src, alt=alt, mask=mask, up=up, cutout=cutout, crop=crop, up2=up2, arrows=arrows, upscale=upscale, rotate=rotate,
                min_width=min_width)


DETAIL = {
    # ---- machine details from the XL quotation (tools/src-images/dener-detail/src/xl-*.png)
    "dn-det-backgauge-std": D("xl-backgauge-std.png", "Standard back gauge of the Dener XL: CNC X axis on ball screw and linear guides, finger with manual R and Z adjustment and micro vernier"),
    "dn-det-cylinder-pivot": D("xl-cylinder-pivot.png", "Hydraulic cylinder of the XL attached to the ram by a rotational pivot pin — no side thrust on the piston seals"),
    "dn-det-frame-fea": D("xl-frame-fea.png", "Finite-element analysis of the XL welded frame: a high-strength frame with minimal distortion under load"),
    "dn-det-punch-holder": D("xl-punch-holder-drawing.png", "Euro / American segmented upper punch holder — takes European and American upper tools"),
    "dn-det-front-supports": D("xl-front-supports.png", "Two linear-guided front sheet supports with T-slots, ball transfers, disappearing stops and inch / mm scales"),
    "dn-det-foot-pedal": D("xl-foot-pedal.png", "Foot pedal stand with emergency stop at the operator's position"),
    "dn-det-rear-gates": D("xl-rear-gates.png", "Rear interlocked gates: the back gauge area cannot be entered while the machine runs"),
    "dn-det-esa-2d": D("xl-esa-640.png", "ESA 2D touch design on a 15″ touch screen: the profile is drawn and the control calculates the bend sequence — the programming of the S840"),
    "dn-det-esa-875": D("xl-esa-875.png", "ESA S875 W control: 21″ 3D touch screen with EsaBend 3D simulation"),
    "dn-det-bg-xr": D("xl-bg-xr.png", "2-axis (X, R) and 4-axis (X, R, Z1, Z2) back gauge on linear guides and ball screw"),
    "dn-det-bg-2axis": D("xl-bg-xr.png", "2-axis CNC back gauge (X, R): the arrows show the X axis moving the fingers to and from the die and the R axis raising and lowering them", arrows=True),
    "dn-det-bg-4axis": D("xl-bg-xr.png", "4-axis CNC back gauge (X, R, Z1, Z2): the arrows show X, R and the two fingers travelling sideways along the beam (Z1, Z2)", arrows=True),
    "dn-det-bg-5axis": D("xl-bg-5axis.png", "5-axis back gauge (X, X′, R, Z1, Z2) for lengths to 26 ft and presses to 800 tons — the arrows show each axis, X′ moving one finger in depth on its own", arrows=True),
    "dn-det-bg-6axis-atf": D("xl-bg-6axis-atf.png", "6-axis ATF back gauge (X1, X2, R1, R2, Z1, Z2): each finger tower moves in depth, height and sideways on its own — one flat and one crab-claw finger on each tower", mask="xl-bg-6axis-atf-mask.png", cutout=True, arrows=True),
    "dn-det-crowning-motor": D("xl-crowning-motor.jpg", "CNC motorised crowning on a Dener press brake: a gear motor at the end of the bed drives the crowning wedges, set by the control for every bend", up=False),
    "dn-det-eurostamp-tools": D("xl-eurostamp-tools.png", "The standard tooling delivered with a Dener press brake: EUROSTAMP 85° punch 1281 (R 0.8 mm, 100 t/m) and 4-way die 2067 with 16, 22, 35 and 50 mm openings"),
    "dn-det-quick-release-plate": D("xl-quick-release-plate.png", "Dener quick-release punch holder front clamp plates with lever bar action, for European and American punches"),
    # photographed lying on a table; turned 90° so the punch hangs from the clamp as it does on the ram (the owner's request)
    "dn-det-eurostamp-quick-clamp": D("xl-eurostamp-quick-clamp.png", "EUROSTAMP quick clamp (Z1 / Z2 models) as mounted on the ram: the European punch is inserted from below and self-seats when the lever closes", rotate=90, min_width=820),
    "dn-det-eurostamp-quick-clamp-2": D("xl-eurostamp-quick-clamp-2.png", "EUROSTAMP quick clamp on the ram — European tools only, lever action"),
    "dn-det-sheet-followers": D("xl-sheet-followers.png", "AP 01 CNC mechanical sheet followers: 0 – 60° inclination, 150 kg (330 lb) each, for long and heavy sheets"),
    "dn-det-oil-cooler": D("xl-oil-cooler.png", "Hydraulic oil cooler: the fan starts at 60 °C oil temperature and stops at 55 °C"),
    "dn-det-tandem": D("xl-tandem.png", "Tandem press brakes: two machines on one control for long parts, cheaper than one large machine and more versatile for small jobs"),
    # ---- from the DDM quotation (ddm-*.png)
    "dn-det-ddm-rear": D("ddm-rear.png", "Dener DDM servo-electric press brake from the rear: belt-and-pulley ram drive, no hydraulic oil"),
    "dn-det-bg-2axis-ddm": D("ddm-bg-2axis.png", "Standard 2-axis back gauge (X, R) of the DDM on linear guides, ball-screw X axis with 500 mm reach"),
    "dn-det-finger-steps": D("ddm-finger-steps.png", "Multi-step finger design: three X-axis stops extend the gauging range to 764 mm (30.1″) and ease long flanges"),
    "dn-det-front-support-single": D("ddm-front-support.png", "Linear-guided front sheet support with hardened rod, T-slot, ball transfers and inch / mm scale"),
    "dn-det-cabinet-cooling": D("ddm-cabinet-cooling.png", "Electrical cabinet cooling system — a sealed cabinet with air conditioning"),
    "dn-det-esa-875-ddm": D("ddm-esa-875.png", "ESA S875 W 21″ widescreen 3D control of the Dener DDM servo-electric press brake"),
    "dn-det-esabend-3d": D("ddm-esabend-3d.png", "EsaBend 3D: the part is imported or drawn, the bend sequence calculated and simulated with the tools in 3D"),
    "dn-det-bg-5axis-ddm": D("ddm-bg-5axis.png", "5-axis back gauge (X, X′, R, Z1, Z2) with ±100 mm X′ for parts that are not square to the die"),
    "dn-det-wila-clamp": D("ddm-wila-clamp.png", "Wila hydraulic tool clamping with CNC crowning — option on every Dener press brake"),
    "dn-det-wila-tools": D("ddm-wila-tools.png", "Wila New Standard tooling and hydraulic clamping for fast tool changes"),
    "dn-det-wilson-clamp": D("ddm-wilson-clamp.png", "Wilson Express Clamp: manual quick-release clamping for European punches"),
}
DXF = {   # EUROSTAMP tool profiles drawn from the DXF files: (file, alt)
    "dn-det-tool-1281": ("eurostamp-1281.dxf", "EUROSTAMP punch 1281 — the 85° gooseneck-free straight punch, R 0.8 mm, H 104.65 mm, 100 t/m, supplied with Dener press brakes"),
    "dn-det-tool-2067": ("eurostamp-2067.dxf", "EUROSTAMP 4-way die 2067 — four V openings (16, 22, 35 and 50 mm) in one 60 mm block, supplied with Dener press brakes"),
}
CONTROLS = {
    "ctl-delem-da69s": D("delem-da-69s.webp", "Delem DA-69S: 24″ multi-touch 3D control — 3D and 2D programming, 3D simulation, Profile-S3D offline software", up=False, cutout=True),
    "ctl-delem-da66s": D("delem-da-66s.webp", "Delem DA-66S: 24″ multi-touch 2D graphical control with 3D machine view, Profile-S2D offline software", up=False, cutout=True),
    "ctl-delem-da58tx": D("delem-da-58tx.webp", "Delem DA-58Tx: 18.5″ touch 2D graphical control with automatic bend sequence and collision detection", up=False, cutout=True),
    "ctl-delem-da53tx": D("delem-da-53tx.webp", "Delem DA-53Tx: 15″ touch numerical control with 2D product and tool programming, up to 4 axes", up=False, cutout=True),
    # the owner's photo of a DA-41T on a press brake pendant (Oct 29 2026), background removed with Pixelcut and approved as it is —
    # the mounting tube runs to the top edge; it replaced Delem's product cut-out delem-da-41t.webp
    "ctl-delem-da41t": D("delem-da41t-pendant.png", "Delem DA-41T 7″ touch NC control on a press brake pendant, with the emergency stop and handle — Y and X axes, 100 programs, for torsion-bar press brakes", up=True),
    "ctl-cybelec-ct12": D("cybelec-ct12.webp", "Cybelec CybTouch 12 PS: 12″ touch control for synchronised press brakes with TouchProfile 2D programming", up=False),
    # ESA's own product photos of the S875 W and S840 on their swing-arm stands (the owner's choice, Oct 29 2026; the earlier
    # cards were esa-s875w-card.webp / esa-s840-card.webp)
    "ctl-esa-s875w-card": D("esa-s875w-stand.png", "ESA S875 W: 21.5″ Full HD multi-touch 3D control on its stand — EsaBend 3D shows the tools, the gauge and the part", up=False, cutout=True, upscale=1.6),
    "ctl-esa-s840-card": D("esa-s840-stand.png", "ESA S840: 15.6″ HD touch control on its stand — up to 6 axes, numeric and 2D programming with automatic bend sequence", up=True, cutout=True, upscale=1.1),
    # ESA's own front view of the S630 pendant, already cut out (the owner's choice, Oct 29 2026; earlier a crop of esa-006-020.png)
    "ctl-esa-s630": D("esa-s630-pendant.png", "ESA S630: 10″ resistive touch control on its pendant with the handle — up to 4 axes, numeric and 2D programming, the bend calculation on screen", up=True),
    "ctl-esa-pendant": D("xl1560-esa-s640.jpg", "ESA touch-screen control pendant on the Dener XL 1560", up=False, cutout=True, crop=(340, 80, 1300, 1150)),
    # the value-line supplier's controller page (a scan): crops of the controls that have no maker's photo
    "ctl-scs920": D("adh-controllers-page.png", "SCS920: 21.5″ capacitive touch CNC, 6+1 axes standard (8+1 optional), for hydraulic, electric and dual-pump press brakes", crop=(30, 290, 340, 680), up=True, up2=True, cutout=True),
    "ctl-estun-e21ps": D("adh-controllers-page.png", "Estun E21PS: NC control for torsion-bar press brakes — back gauge and ram positioning, one-way / two-way positioning, 2D graphic programming", crop=(1850, 320, 2080, 640), up=True, up2=True, cutout=True),
    # Estun's product photo of the E315PS on its pendant arm, background removed with Pixelcut (the owner's choice, Oct 29 2026;
    # earlier a crop of the supplier's controller page)
    "ctl-estun-e315ps": D("estun-e315ps-pendant.png", "Estun E315PS: 15.6″ capacitive touch NC control on its pendant arm — angle programming, tool and material databases, 6+1 axes", up=True),
}


def upscale2(im):
    from esrgan import upscale
    return upscale(im)


def process_image(spec, srcdir, dst, key):
    im = Image.open(os.path.join(srcdir, spec["src"]))
    im = im.convert("RGBA") if (im.mode in ("RGBA", "LA", "P") or spec.get("mask")) else im.convert("RGB")
    if spec.get("crop"):
        im = im.crop(spec["crop"])
    if spec.get("rotate"):                              # degrees counter-clockwise (a tool photographed lying down, shown as mounted)
        im = im.rotate(spec["rotate"], expand=True, resample=Image.BICUBIC)
    if spec.get("mask"):
        m = Image.open(os.path.join(srcdir, spec["mask"])).convert("L")
        im = im.convert("RGBA")
        im.putalpha(m)
        if spec.get("cutout"):                          # matte on white; make_images cuts it out again with BiRefNet
            bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
            bg.alpha_composite(im)
            im = bg.convert("RGB")
    if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] == 255:
        im = im.convert("RGB")
    if spec.get("up") and max(im.size) < SMALL:
        im = upscale2(im)
        if spec.get("up2") and max(im.size) < SMALL:
            im = upscale2(im)
    if spec.get("min_width") and im.width < spec["min_width"]:     # a portrait photo shown half-width: enough pixels for the 800 px variant
        f = spec["min_width"] / im.width
        im = im.resize((spec["min_width"], round(im.height * f)), Image.LANCZOS)
    os.makedirs(dst, exist_ok=True)
    if im.mode == "RGBA":
        path = os.path.join(dst, key + ".png")
        im.save(path, optimize=True)
    else:
        path = os.path.join(dst, key + ".jpg")
        im.convert("RGB").save(path, quality=92)
    return path, im.size


def render_dxf(file, out, size=1400):
    """black line drawing of the LINE / ARC entities (the centre lines and the code text are left out)"""
    import ezdxf
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Arc
    doc = ezdxf.readfile(file)
    msp = doc.modelspace()
    xs, ys = [], []
    fig = plt.figure(figsize=(size / 250, size / 250), dpi=250)
    ax = fig.add_axes([0.04, 0.04, 0.92, 0.92])
    ax.set_axis_off()
    ax.set_aspect("equal")
    lines = [(e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1]) for e in msp if e.dxftype() == "LINE"]
    bw = max(max(l[0], l[2]) for l in lines) - min(min(l[0], l[2]) for l in lines)
    bh = max(max(l[1], l[3]) for l in lines) - min(min(l[1], l[3]) for l in lines)
    for x1, y1, x2, y2 in lines:
        if (abs(x1 - x2) < 0.01 and abs(y1 - y2) > 0.9 * bh) or (abs(y1 - y2) < 0.01 and abs(x1 - x2) > 0.9 * bw):
            continue                                   # centre lines
        ax.plot([x1, x2], [y1, y2], color="#1d1d1b", lw=2.2, solid_capstyle="round")
        xs += [x1, x2]
        ys += [y1, y2]
    for e in msp:
        t = e.dxftype()
        if t == "LINE":
            continue
        elif t == "ARC":
            cx, cy, _ = e.dxf.center
            r, a0, a1 = e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle
            if a1 < a0:
                a1 += 360
            ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, angle=0, theta1=a0, theta2=a1, color="#1d1d1b", lw=2.2))
            for a in (a0, a1):
                xs.append(cx + r * math.cos(math.radians(a)))
                ys.append(cy + r * math.sin(math.radians(a)))
    pad = max(max(xs) - min(xs), max(ys) - min(ys)) * 0.06
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    im = Image.open(out).convert("RGB")
    bb = Image.eval(im.convert("L"), lambda v: 255 if v < 250 else 0).getbbox()
    if bb:
        p = 40
        im = im.crop((max(0, bb[0] - p), max(0, bb[1] - p), min(im.width, bb[2] + p), min(im.height, bb[3] + p)))
    im.save(out, optimize=True)
    return out, im.size


def register():
    """image_map entries (sections dener-detail / controls) and the key list for make_images"""
    import json
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    sets = [(DETAIL, DET, "dener-detail"), ({k: dict(alt=v[1], cutout=False) for k, v in DXF.items()}, DET, "dener-detail"), (CONTROLS, CTL, "controls")]
    for specs, folder, section in sets:
        for key, p in specs.items():
            f = [x for x in os.listdir(folder) if x.startswith(key + ".")]
            if not f:
                print("!! missing export for", key)
                continue
            ext = os.path.splitext(f[0])[1]
            imap[key] = {"src": f"tools/src-images/{os.path.basename(folder)}/{key}{ext}", "alt": p["alt"], "section": section, "trim": ext == ".jpg" and section == "dener-detail",
                         "quality": 84, "cutout": bool(p.get("cutout")) and not p.get("arrows")}   # arrows and letters would be cut away
            if p.get("upscale"):                     # make_images: Lanczos upscale after the cut, so the 800 px variant exists
                imap[key]["upscale"] = p["upscale"]
            keys.append(key)
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "dener_detail_keys.txt"), "w").write(",".join(keys))
    return keys


def main():
    if "--register" in sys.argv:
        print("registered:", len(register()))
        return
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(DETAIL) + list(DXF) + list(CONTROLS)
    for k in keys:
        if k in DETAIL and DETAIL[k].get("arrows"):
            print(f"{k:32s} (drawn with its axis arrows by tools/dener_bg_arrows.py)")
            continue
        if k in DETAIL:
            path, size = process_image(DETAIL[k], os.path.join(DET, "src"), DET, k)
        elif k in DXF:
            os.makedirs(DET, exist_ok=True)
            path, size = render_dxf(os.path.join(DET, "src", DXF[k][0]), os.path.join(DET, k + ".png"))
        elif k in CONTROLS:
            path, size = process_image(CONTROLS[k], os.path.join(CTL, "src"), CTL, k)
        else:
            raise SystemExit(f"unknown key {k}")
        print(f"{k:32s} {size} -> {os.path.relpath(path, ROOT)}")
    print("registered:", len(register()))


if __name__ == "__main__":
    main()
