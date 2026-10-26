#!/usr/bin/env python3
"""NovoTech value-line fiber lasers (ULF, ULE, ULFT, ULET sheet lasers and ULT tube lasers) — supplier brochure renders,
quotation photos and automation photos → logo-free sources in tools/src-images/value-laser/.

The machines are sold under NovoTech's name, so the supplier's badges, the model labels painted on the enclosures and the
Chinese warning stickers are boxed by hand (page pixels, located on 50 px grid views) and filled with LaMa
(tools/delogo.py, mode "lama") before anything else.  Sources (outside the repository, /home/claude/adhlaser/):

  src/<SERIES>-00N.png   the pages of the supplier's series brochures (3366 × 1241) and of its 2025 general brochure
                         (GEN-00N, 2481 × 1684), rendered from the PDFs
  q/q-PP-NN.png          the images inside the ULE 3015 quotation: the render with its own mask (q-01-27) and real photos
                         of the console, bed, drives, chiller and cabinet

Kinds:
  R()   render on the page's white / lavender background → crop, delogo, Real-ESRGAN x2 when the crop is small (twice when
        tiny), BiRefNet cut-out (cached), specks dropped → WebP with lossless alpha
  A()   render that already has an alpha channel (q-01-27) → delogo on a white matte, the soft floor shadow removed from
        the alpha → WebP
  P()   photo or diagram → crop, delogo, ESRGAN when small → JPEG (stays a rectangle on the site)

    python3 tools/vl_laser_photos.py [keys]           export
    python3 tools/vl_laser_photos.py --check [pages]  page overviews with the crops (green) and boxes (red) drawn
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/adhlaser/src/"
QD = "/home/claude/adhlaser/q/"
UG = "/home/claude/adhlaser/ulg/s/"          # ULG photos from the supplier's website (October 2026), see the ULG block below
WORK = "/home/claude/adhlaser/work/"
OUT = os.path.join(ROOT, "tools", "src-images", "value-laser")
MAX_SIDE = 1800
Image.MAX_IMAGE_PIXELS = None


def R(page, crop, alt, boxes=(), **kw):
    src = page if page.startswith("/") else SRC + page + ".png"
    return dict(kind="render", src=src, page=os.path.basename(page), crop=crop, alt=alt, boxes=list(boxes), **kw)


def A(path, alt, boxes=(), floor=90, **kw):
    src = path if path.startswith("/") else QD + path
    return dict(kind="alpha", src=src, page=os.path.basename(path), crop=None, alt=alt, boxes=list(boxes), floor=floor, **kw)


def P(page, crop, alt, boxes=(), **kw):
    src = page if page.startswith("/") else (QD + page if page.startswith("q-") else SRC + page + ".png")
    return dict(kind="photo", src=src, page=os.path.basename(page), crop=crop, alt=alt, boxes=list(boxes), **kw)


PHOTOS = {
    # ---------------------------------------------------------------- ULF open-type single-table lasers
    "vn-ulf-1": R("ULF-000", (985, 255, 2600, 1060), "NovoTech ULF 3015 open-type fiber laser — 10 × 5 ft single table, Cypcut console on its arm",
                  boxes=[(1250, 600, 1372, 810), (1485, 655, 1552, 785), (2540, 645, 2588, 700)]),
    "vn-ulf-frame": R("ULF-001", (110, 470, 1166, 1150), "Welded bed of the ULF — internal stiffeners, annealed and shot-blasted to relieve the welding stress",
                      boxes=[(824, 465, 850, 608), (1098, 832, 1170, 1110)]),
    "vn-ulf-beam": R("ULF-001", (2515, 125, 3245, 505), "Cast-aluminum crossbeam of the ULF with the cutting-head carriage and cable chain"),
    "vn-ulf-console": R("ULF-001", (1945, 575, 2485, 1145), "Cypcut CNC console — monitor, keyboard and hand pendant on a swing arm"),
    "vn-ulf-head": R("ULF-002", (105, 268, 375, 760), "Raytools autofocus cutting head with anti-collision protection"),
    "vn-ulf-source": R("ULF-002", (115, 828, 695, 1120), "Raycus fiber laser source — Raycus, MAX or IPG chosen at order"),
    "vn-ulf-chiller": R("ULF-003", (125, 255, 485, 805), "Hanli water chiller for the laser source and the cutting head"),
    "vn-ulf-skyeye": R("ULF-003", (2945, 295, 3205, 705), "Camera nesting over the table — scan the remnant, nest the parts on it (optional)"),
    "vn-ipg": R("ULE-004", (655, 450, 1015, 805), "IPG fiber laser source (optional)"),
    # ---------------------------------------------------------------- ULE enclosed exchange-table lasers
    "vn-ule-1": A("q-01-27.png", "NovoTech ULE enclosed fiber laser with exchange table — 20 × 8.5 ft working area, full enclosure, front console",
                  boxes=[(235, 265, 350, 365), (1040, 365, 1095, 395), (1178, 262, 1222, 668), (950, 474, 1004, 502, "all"), (578, 322, 628, 535),
                         (1690, 420, 1880, 535), (2108, 332, 2150, 402), (1525, 340, 1568, 500)]),
    "vn-ule-console": P("q-04-58.png", None, "ULE operator station — touchscreen CNC with the cutting database, emergency stop and hand pendant"),
    "vn-ule-bed": P("q-04-61.png", None, "Inside the ULE bed — zoned extraction chambers under the table, rack and linear guide"),
    "vn-ule-frame": R("ULE-001", (130, 380, 1600, 1030), "Welded bed of the ULE — precision-welded and heat-treated, flat to 0.05 mm per square metre",
                      boxes=[(110, 360, 475, 458), (1060, 945, 1225, 1010)]),
    "vn-ule-servo": P("q-05-67.png", None, "Servo motor and reducer driving the gantry"),
    "vn-ule-rack": P("q-06-73.png", None, "Precision-ground rack beside the linear guide rail"),
    "vn-ule-chiller": P("q-07-77.png", None, "Hanli 12000 water chiller, sized for a 12 kW source"),
    "vn-ule-cabinet": P("q-07-78.png", None, "Electrical cabinet — Schneider components, servo drives and the CNC, two cooling fans"),
    "vn-fms-tower": P("GEN-006", (140, 560, 1150, 1080), "Sheet storage tower feeding an exchange-table laser — flexible manufacturing system (optional)"),
    "vn-fms-gantry": P("GEN-006", (1360, 880, 2380, 1280), "Gantry loading and unloading with suction cups (optional)"),
    "vn-precitec": R("ULE-004", (245, 435, 415, 820), "Precitec ProCutter autofocus cutting head (optional)"),
    # ---------------------------------------------------------------- ULG ground-rail plate lasers (photos from the supplier's website)
    "vn-ulg-1": R(UG + "ulg-hero.webp", None, "NovoTech ULG ground-rail plate laser — enclosed gantry cabin running on floor rails, plate table behind, console in front",
                  boxes=[(332, 286, 416, 390), (1278, 278, 1312, 470)]),
    "vn-ulg-beam": P(UG + "ulg-beam.webp", None, "ULG gantry and cutting head over the slat table — the gantry runs on its own ground rails"),
    "vn-ulg-rails": P(UG + "ulg-bed.webp", None, "Ground rails and plate-support table set side by side — the motion axis never carries the plate load"),
    "vn-ulg-table": P(UG + "ulg-table.webp", None, "Long plate-support table with replaceable slats, sources and chillers along the wall"),
    "vn-ulg-cutting": P(UG + "ulg-cutting.webp", None, "Cutting head piercing plate — 12 to 60 kW source chosen at order"),
    "vn-ulg-parts": P(UG + "ulg-parts.webp", None, "Heavy-plate parts and flanges cut on the ULG table, gantry carriage overhead", boxes=[(846, 138, 937, 170)]),
    "vn-ulg-installed": P(UG + "ulg-installed.webp", None, "ULG with a 59 × 14.8 ft (18 × 4.5 m) table and a 30 kW source installed in a heavy-equipment plant",
                          boxes=[(8, 698, 532, 845)]),
    "vn-ulg-extraction": P(UG + "ulg-extraction.webp", None, "Zoned fume-extraction duct along the plate table"),
    "vn-ulg-console": A(UG + "ulg-console.webp", "ULG operator console with the touchscreen CNC, nesting and remnant functions", floor=0, up=True),
    "vn-ulg-flanges": P(UG + "ulg-flanges.webp", None, "Tower flanges and baseplates cut from thick plate on a ground-rail laser"),
    # ---------------------------------------------------------------- ULFT open-type sheet + tube lasers
    "vn-ulft-1": R("ULFT-000", (982, 190, 2562, 1005), "NovoTech ULFT open-type sheet-and-tube fiber laser — 10 × 5 ft table and a rotary chuck for tube on one machine",
                   boxes=[(1310, 632, 1400, 705), (1760, 370, 1815, 398), (1470, 650, 1618, 708), (2058, 662, 2110, 722)]),
    "vn-ulft-frame": R("ULFT-001", (235, 470, 1440, 1110), "ULFT bed — hollow welded frame with fish-scale stiffeners, stress-relieved",
                       boxes=[(1098, 905, 1445, 1115)]),
    "vn-ulft-beam": R("ULFT-001", (2490, 140, 3250, 478), "Crossbeam and cutting-head carriage of the ULFT", boxes=[(2765, 288, 2820, 310)]),
    "vn-ulft-chuck": R("ULFT-002", (1175, 128, 1705, 660), "Pneumatic chuck of the tube unit — one-key self-centring, three times faster than an electric chuck"),
    "vn-ulft-head": R("ULFT-002", (155, 218, 365, 670), "Autofocus cutting head — anti-collision, micro-joints so parts stay in the sheet"),
    "vn-ulft-sources": R("ULFT-002", (155, 728, 605, 1100), "MAX and Raycus fiber laser sources — chosen at order"),
    # ---------------------------------------------------------------- ULET enclosed sheet + tube lasers
    "vn-ulet-1": R("ULET-000", (1055, 262, 2590, 1050), "NovoTech ULET enclosed sheet-and-tube fiber laser — full enclosure with the tube chuck at the end",
                   boxes=[(1072, 370, 1135, 432), (1825, 322, 2035, 428)]),
    "vn-ulet-beam": R("ULET-001", (2515, 135, 3160, 525), "Crossbeam and Z axis of the ULET — manganese steel, heat-treated"),
    "vn-ulet-chuck": P("ULET-002", (1350, 115, 1800, 575), "Pneumatic chuck clamping a square tube"),
    "vn-ulet-head": R("ULET-002", (185, 228, 365, 770), "Autofocus cutting head with anti-collision protection"),
    "vn-ulet-source": R("ULET-002", (145, 850, 645, 1140), "Raycus fiber laser source, 1.5 to 40 kW"),
    # ---------------------------------------------------------------- ULT tube lasers
    "vn-ult-1": R("TUBE-000", (735, 225, 2545, 960), "NovoTech ULT tube laser — two pneumatic chucks, bundle loader on the left, unloading table in front",
                  boxes=[(720, 400, 990, 505), (1365, 420, 1435, 510), (738, 655, 756, 712), (888, 676, 906, 732), (1010, 685, 1028, 742), (1133, 700, 1152, 760)]),
    "vn-ult-frame": R("TUBE-001", (535, 255, 1575, 955), "ULT bed with the cutting cabin, chuck carriage rails and following supports"),
    "vn-ult-beam": R("TUBE-001", (2485, 255, 3268, 515), "Stress-relieved crossbeam carrying the chuck carriage"),
    "vn-ult-console": R("TUBE-001", (1895, 625, 2435, 1185), "CNC console with Cypcut tube software"),
    "vn-ult-chuck": R("TUBE-002", (1655, 708, 2055, 1120), "Double-acting pneumatic chuck — clamps tube from Ø0.6 to 8.7″ without changing jaws", floor=60),
    "vn-ult-head": R("TUBE-002", (145, 228, 325, 770), "Autofocus cutting head for tube"),
    "vn-ult-tubest": P("TUBE-002", (2685, 124, 3264, 524), "TubesT tube nesting — parts unfolded and nested along the bar (optional)"),
    "vn-ult-dualy": P("TUBE-003", (695, 235, 1355, 695), "Dual Y-axis cutting — a short Y axis on the head for fast cutting of small tube (optional)",
                      boxes=[(1115, 280, 1360, 395)]),
    "vn-ult-loader": P("TUBE-003", (1765, 395, 2225, 735), "Automatic bundle loader (optional)"),
    "vn-ult-zero": P("TUBE-003", (2272, 395, 2735, 735), "Zero-tail cutting and five-axis ±45° bevel head (optional)"),
    "vn-ult-feeder": P("TUBE-003", (2780, 395, 3240, 735), "Automatic feeding system — up to 606 lb (275 kg) per tube, 19 s cycle (optional)"),
}


# ------------------------------------------------------------------------------------------------ helpers
def clean_alpha(alpha, keep=0.004):
    """drop the specks a mask leaves around the machine: alpha components under `keep` × the largest one"""
    a = np.array(alpha)
    lab, n = ndimage.label(a > 24)
    if n <= 1:
        return alpha
    sizes = ndimage.sum(np.ones_like(a), lab, range(1, n + 1))
    drop = [i + 1 for i, s in enumerate(sizes) if s < keep * sizes.max()]
    if drop:
        a[np.isin(lab, drop)] = 0
    return Image.fromarray(a)


def fit(im):
    """at most MAX_SIDE; a picture 560 – 800 px wide is brought to 800 px so the site gets its 800 px variant"""
    s = MAX_SIDE / max(im.size)
    if s >= 1:                                   # never blown up past the source, except the 560 – 800 px band
        s = 800 / im.width if 560 <= im.width < 800 else 1
    elif 560 <= im.width * s < 800:              # a tall picture capped by its height still gets an 800 px wide variant
        s = 800 / im.width
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS) if s != 1 else im


def page_boxes(p):
    """the spec's boxes (page pixels) shifted into the crop and clipped to it"""
    boxes = [tuple(b) + (("lama",) if len(b) == 4 else ()) for b in p["boxes"]]       # a 5th element picks the delogo mode
    if not p["crop"]:
        return boxes
    cx0, cy0, cx1, cy1 = p["crop"]
    out = []
    for x0, y0, x1, y1, mode in boxes:
        x0, y0, x1, y1 = max(x0, cx0) - cx0, max(y0, cy0) - cy0, min(x1, cx1) - cx0, min(y1, cy1) - cy0
        if x1 - x0 > 3 and y1 - y0 > 3:
            out.append((x0, y0, x1, y1, mode))
    return out


def upscale_small(im):
    if max(im.size) >= 900:
        return im
    from esrgan import upscale
    im = upscale(im)
    if max(im.size) < 700:
        im = upscale(im)
    return im


def remove_old(key):
    for e in (".png", ".jpg", ".webp"):
        f = os.path.join(OUT, key + e)
        if os.path.exists(f):
            os.remove(f)


def save_rgba(key, rgb, alpha):
    bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    rgb, alpha = rgb.crop(bb), alpha.crop(bb)
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    out = fit(out)
    remove_old(key)
    path = os.path.join(OUT, key + ".webp")
    out.save(path, quality=95, alpha_quality=100, method=6)
    return path, out.size


def outside_circle(cx, cy, r, ymax, skip_x0, skip_x1):
    """post-fix for a round chuck render: clear what lies outside the chuck's disc in its upper part (a white haze BiRefNet
    keeps), except the columns of the top bracket that stand above the disc"""
    def fix(im):
        a = np.array(im.getchannel("A"))
        yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
        out = ((xx - cx) ** 2 + (yy - cy) ** 2 > r * r) & (yy < ymax) & ((xx < skip_x0) | (xx > skip_x1))
        a[out] = 0
        im.putalpha(Image.fromarray(a))
        return im
    return fix


POST = {"vn-ult-chuck": outside_circle(402, 416, 390, 208, 265, 535)}     # output pixels (800 × 839)


def process(key):
    from delogo import delogo
    p = PHOTOS[key]
    im = Image.open(p["src"])
    os.makedirs(OUT, exist_ok=True)
    if p["kind"] == "alpha":
        im = im.convert("RGBA")
        alpha = im.getchannel("A")
        white = Image.new("RGBA", im.size, (255, 255, 255, 255))
        white.alpha_composite(im)
        rgb = delogo(white.convert("RGB"), page_boxes(p))
        a = np.asarray(alpha).astype(np.float32)
        a = np.clip((a - p["floor"]) * 255.0 / (250 - p["floor"]), 0, 255).astype(np.uint8)   # soft floor shadow out
        alpha = Image.fromarray(a)
        if p.get("up"):                                  # a narrow cut-out: Real-ESRGAN x2 on the white matte, the mask resized to match
            bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
            rgb, alpha = rgb.crop(bb), alpha.crop(bb)
            if min(rgb.size) < 560:
                from esrgan import upscale
                rgb = upscale(rgb)
                alpha = alpha.resize(rgb.size, Image.LANCZOS)
        path, size = save_rgba(key, rgb, clean_alpha(alpha))
    else:
        im = im.convert("RGB")
        if p["crop"]:
            im = im.crop(p["crop"])
        boxes = page_boxes(p)
        if boxes:
            im = delogo(im, boxes)
        im = upscale_small(im)
        if p["kind"] == "render":
            from birefnet_cut import cut_rgba
            cut = cut_rgba(im, p.get("size", "1024"), cache_key=f"vlaser-{key}")
            alpha = cut.getchannel("A")
            if p.get("floor"):                     # a haze BiRefNet leaves around a render: semi-transparent pixels below `floor` out
                a = np.asarray(alpha).astype(np.float32)
                alpha = Image.fromarray(np.clip((a - p["floor"]) * 255.0 / (255 - p["floor"]), 0, 255).astype(np.uint8))
            path, size = save_rgba(key, im, clean_alpha(alpha))
        else:
            im = fit(im)
            remove_old(key)
            path = os.path.join(OUT, key + ".jpg")
            im.save(path, quality=90)
            size = im.size
    if key in POST:
        im = POST[key](Image.open(path).convert("RGBA"))
        im.save(path, quality=95, alpha_quality=100, method=6)
    print(f"{key:18s} {p['kind']:6s} {size[0]}x{size[1]} -> {os.path.basename(path)}", flush=True)


def check(pages):
    """one overview per source page: crops green, logo boxes red, key names in the corner of each crop"""
    by_page = {}
    for k, p in PHOTOS.items():
        by_page.setdefault(p["src"], []).append((k, p))
    for src, items in by_page.items():
        name = os.path.splitext(os.path.basename(src))[0]
        if pages and name not in pages:
            continue
        im = Image.open(src).convert("RGB")
        d = ImageDraw.Draw(im)
        for k, p in items:
            if p["crop"]:
                d.rectangle(p["crop"], outline=(0, 200, 0), width=5)
                d.text((p["crop"][0] + 8, p["crop"][1] + 8), k, fill=(0, 140, 0))
            for b in p["boxes"]:
                d.rectangle(b[:4], outline=(255, 0, 0), width=3)
        s = 1800 / im.width
        im = im.resize((1800, round(im.height * s)), Image.LANCZOS)
        im.save(os.path.join(WORK, f"check-{name}.jpg"), quality=82)
        print("check", name, [k for k, _ in items])


def export_kind(key):
    """(ext, cutout) for image_map: the cut-outs are WebP with alpha, the photos JPEG kept as rectangles"""
    f = [x for x in os.listdir(OUT) if x.startswith(key + ".")]
    ext = os.path.splitext(f[0])[1] if f else ".jpg"
    return ext, False


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--check" in sys.argv:
        check(args)
    else:
        for k in (args or list(PHOTOS)):
            process(k)
