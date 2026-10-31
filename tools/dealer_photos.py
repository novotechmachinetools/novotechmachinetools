#!/usr/bin/env python3
"""Machine and accessory photos from the Polish Dener / Şahinler / Bekamak distributor's website, used with the
distributor's permission (the owner, Oct 31 2026: machine photos and accessory close-ups only — no photos taken at
customers' plants — and the distributor's marks removed).

The chosen files were downloaded once through the owner's browser and copied under their site keys to
/home/claude/dealer-pl/<key>.<ext>.  The distributor's name plates on the machines, the badge on the sample-part photos
and on-screen marks are filled with LaMa (tools/lama_inpaint.py); renders on white are cut out later by
tools/make_images.py (BiRefNet), accessory close-ups keep their background.

    python3 tools/dealer_photos.py [key …]     → tools/src-images/dealer-pl/<key>.jpg and the tools/image_map.json entries
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/dealer-pl/"
DST = os.path.join(ROOT, "tools", "src-images", "dealer-pl")
BIG = 1800

PLATE_DDM = [(424, 109, 486, 158)]


def P(alt, boxes=(), cut=True, section="dener", clone=()):
    return dict(alt=alt, boxes=list(boxes), cut=cut, section=section, clone=list(clone))


# key: alt / caption, boxes (x0, y0, x1, y1 in source pixels) filled by LaMa, cut = BiRefNet cut-out (False: keep the scene);
# clone (x0, y0, x1, y1, dx, dy): a plate on a plain panel is covered with the panel next to it (offset dx, dy), feathered —
# for spots where LaMa invents a badge from the logo above
PHOTOS = {
    # ---- Dener XL hydraulic press brakes and tandem
    "dn-xl-4000x600": P("Dener XL 4000 × 600: 661 US tons (600 t) × 13 ft hydraulic CNC press brake, with the CNC control on its swing arm "
                        "and the foot pedal", [(550, 348, 590, 380)]),
    "dn-xl-4000x320": P("Dener XL 4000 × 320: 353 US tons (320 t) × 13 ft, front view with the front sheet supports, the foot pedal and "
                        "the CNC control on its swing arm", [(634, 362, 697, 412)]),
    "dn-tandem-6000x600": P("Tandem of two XL 6000 × 600 press brakes: 40 ft and 1,323 US tons (1,200 t) bent from one control",
                            [(402, 342, 434, 364), (1050, 337, 1083, 357)]),
    "dn-xl-wila": P("Wila New Standard upper tool holder on the ram — Wila mechanical or hydraulic tool clamping is optional on the XL",
                    cut=False),
    # the owner's set (sent in the chat, Oct 31 2026): the distributor's plate on each ram and its logo on the control screens filled
    "dn-xl-3000x220": P("Dener XL 3000 × 220: 243 US tons (220 t) × 10 ft hydraulic CNC press brake, with the CNC control on its swing arm, "
                        "the front sheet supports and the foot pedal", [(432, 251, 480, 290)]),
    "dn-xl-tandem-3000x320": P("Tandem of two XL 3000 × 320 press brakes: 20 ft and 706 US tons (640 t) bent from one control, or each "
                               "machine on its own", [(424, 271, 471, 307), (122, 441, 155, 455), (1305, 443, 1338, 456)],
                               clone=[(1015, 268, 1076, 316, 70, 0)]),
    "dn-xl-tandem-4000x320": P("Tandem of two XL 4000 × 320 press brakes: 26 ft and 706 US tons (640 t) bent from one control, with a CNC "
                               "control at each end", [(1405, 397, 1434, 411)],
                               clone=[(403, 317, 454, 358, 60, 0), (1007, 317, 1057, 358, 60, 0)]),
    "dn-xl-tandem-4000x320-shop": P("Tandem XL 4000 × 320 press brakes in the shop: two 13 ft machines that bend 26 ft parts together or work "
                                    "apart", cut=False, clone=[(247, 317, 278, 346, 40, 0), (611, 310, 649, 343, 45, 0)]),
    "dn-xl-throat-frames": P("Deep throats in the XL side frames, seen along the machine: tall flanges on long parts pass into the frames",
                             cut=False),
    "dn-xl-bg-fingers": P("Back gauge fingers of the XL, sliding along the beam on its linear guide", cut=False),
    "dn-sheet-followers": P("Two CNC sheet followers in front of a Dener press brake: they rise with the sheet through the bend, so large, "
                            "thin sheets do not sag or whip back", [(580, 82, 642, 125)], cut=False),
    # ---- Dener DDM servo-electric and DDS ball-screw press brakes
    "dn-ddm-5020": P("Dener DDM 5020 servo-electric press brake: 55 US tons (50 t) × 6.7 ft, front view", PLATE_DDM),
    "dn-ddm-5020-side": P("Dener DDM 5020 servo-electric press brake — three-quarter view with the front supports and the foot pedal",
                          [(670, 176, 719, 231)]),
    "dn-dds-4013": P("Dener DDS 4013 ball-screw electric press brake: 44 US tons (40 t) × 4.3 ft, with the CNC control on its swing arm "
                     "and the foot pedal", [(462, 180, 514, 222)]),
    "dn-dds-ballscrew": P("DDS ram drive: the servo motor turns a ball screw that moves the ram — no cylinders, no hydraulic oil", cut=False),
    # ---- Dener DAS guillotine and BS swing beam shears
    "dn-das-3006": P("Dener DAS 3006 CNC hydraulic guillotine shear: 1/4″ (6 mm) × 10 ft, with the CNC control on its arm"),
    "dn-das-6006": P("Dener DAS 6006 CNC hydraulic guillotine shear: 1/4″ (6 mm) × 20 ft, with the front support arms",
                     [(482, 288, 515, 321)]),
    "dn-bs-3013": P("Dener BS 3013 hydraulic swing beam shear: 1/2″ (13 mm) × 10 ft, with the NC control and the foot pedal",
                    [(572, 138, 616, 176)]),
    "dn-bs-3010": P("Dener BS 3010 hydraulic swing beam shear: 3/8″ (10 mm) × 10 ft", [(624, 178, 653, 213)]),
    "dn-bs-3006": P("Dener BS 3006 hydraulic swing beam shear: 1/4″ (6 mm) × 10 ft, with the rear guard fence", [(569, 263, 629, 318)]),
    "dn-bs-panel": P("HT 071 NC control on the BS: back gauge position, programs and stroke counter, with the mode switches below",
                     cut=False),
    # ---- Dener GFL fiber laser
    "dn-gfl-3015": P("Dener GFL 3015 fiber laser cutting machine: 5 × 10 ft table, enclosed cabin and pallet changer"),
    "dn-gfl-6020": P("Dener GFL 6020 fiber laser cutting machine: 6.6 × 20 ft table with the pallet changer",
                     clone=[(254, 238, 292, 272, 0, 44)]),
    "dn-gfl-open": P("GFL with the cabin door open: the cutting head on the gantry, and the CNC control on its arm"),
    "dn-gfl-frame": P("GFL frame: stress-relieved welded bed, the gantry with the cutting head, and the pallet changer"),
    "dn-gfl-head": P("GFL cutting head on the Z axis, with the status light strips", cut=False),
    "dn-gfl-part": P("Sample part cut from thick steel plate on a GFL fiber laser", [(455, 695, 545, 730)], cut=False),
    "dn-gfl-sheet": P("Sample nest: S-shaped parts cut from one steel sheet on a GFL fiber laser", [(455, 695, 545, 730)], cut=False),
}


def fill_boxes(im, boxes):
    """LaMa, one box at a time: lama_inpaint works on a window around the whole mask, so boxes far apart (the plates on two
    machines of a tandem) would share one big, downscaled window."""
    import numpy as np
    from lama_inpaint import inpaint
    rgb = np.asarray(im.convert("RGB")).copy()
    for x0, y0, x1, y1 in boxes:
        mask = np.zeros(rgb.shape[:2], np.uint8)
        mask[y0:y1, x0:x1] = 255
        rgb = inpaint(rgb, mask)
    return Image.fromarray(rgb)


def trim(im, thr=242, pad=14):
    g = im.convert("L").point(lambda v: 255 if v < thr else 0)
    bb = g.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def source(key):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if os.path.exists(SRC + key + ext):
            return SRC + key + ext
    raise SystemExit(f"no source for {key} in {SRC}")


def process(key):
    p = PHOTOS[key]
    im = Image.open(source(key))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
    im = im.convert("RGB")
    for x0, y0, x1, y1, dx, dy in p.get("clone", []):
        from PIL import ImageFilter
        patch = im.crop((x0 + dx, y0 + dy, x1 + dx, y1 + dy))
        mask = Image.new("L", patch.size, 0)
        mask.paste(255, (3, 3, patch.width - 3, patch.height - 3))
        im.paste(patch, (x0, y0), mask.filter(ImageFilter.GaussianBlur(2)))
    if p["boxes"]:
        im = fill_boxes(im, p["boxes"])
    if p["cut"]:
        im = trim(im)
    if max(im.size) > BIG:
        f = BIG / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    os.makedirs(DST, exist_ok=True)
    im.save(os.path.join(DST, key + ".jpg"), quality=92)
    return im.size


def register(keys):
    path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(path, encoding="utf-8"))
    for k in keys:
        p = PHOTOS[k]
        imap[k] = {"src": f"tools/src-images/dealer-pl/{k}.jpg", "alt": p["alt"], "section": p["section"], "trim": p["cut"],
                   "quality": 82, "cutout": p["cut"], "cut_size": 1024}
    json.dump(imap, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for k in keys:
        print(f"{k:22s} {process(k)}")
    register(keys)


if __name__ == "__main__":
    main()
