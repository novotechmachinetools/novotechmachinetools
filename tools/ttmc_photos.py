#!/usr/bin/env python3
"""Photos for the NovoTech sheet metal shears (built by TTMC, sold without the supplier's brand): crops from the catalogue page
rasters (the TTMC Vol. 23 catalogue is a PDF of full-page JPEGs at 1240 × 1683 px, with the watermark on a separate layer —
so `pdfimages` gives clean pages).  The crops are taken from /home/claude/ttmc/img/p<page>-<n>.png (not in the repo), the
captions and model names printed next to the machines are painted white, every crop is upscaled 2x (Real-ESRGAN)
and written to tools/src-images/ttmc/<key>.jpg; the site pipeline (tools/make_images.py) cuts them out (BiRefNet).

    pdfimages -f 56 -l 59 -png /mnt/user-data/uploads/Catalog_TTMC_Vol23.pdf /home/claude/ttmc/img/p56   (per page)
    python3 tools/ttmc_photos.py [key ...]      then   python3 tools/make_images.py --only $(cat tools/ttmc_keys.txt)
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "ttmc")
P = "/home/claude/ttmc/img/"

# key: dict(src, crop=(x0,y0,x1,y1), fill=[(x0,y0,x1,y1)…] painted white (printed captions), alt, cutout, up)
PHOTOS = {
    # pneumatic shear
    "tt-ps": dict(src=P + "p56-000.png", crop=(165, 105, 1195, 795), fill=[(95, 440, 325, 492), (55, 598, 665, 835)], cutout=True, up=True,
                  alt="PS-1.5x1320 pneumatic shear, 52″ × 16 ga, with front gauge arms and the mobile foot pedal"),
    "tt-ps-gauge": dict(src=P + "p56-000.png", crop=(115, 878, 472, 1108), cutout=False, alt="Back gauge with indicator on the pneumatic shear"),
    "tt-ps-control": dict(src=P + "p56-000.png", crop=(497, 878, 848, 1108), cutout=False, alt="Pneumatic control unit — filter, regulator and lubricator"),
    "tt-ps-cylinder": dict(src=P + "p56-000.png", crop=(873, 878, 1215, 1108), cutout=False, alt="Pneumatic cylinder driving the cutting beam"),
    # THS hydraulic shears
    "tt-ths": dict(src=P + "p56-001.png", crop=(195, 105, 1165, 765), cutout=True, up=True,
                   alt="THS-1320X4 hydraulic shear, 52″ × 8 ga, with front gauge arms and the mobile foot pedal"),
    "tt-ths-gauge": dict(src=P + "p56-001.png", crop=(75, 755, 445, 995), cutout=False, alt="Hand-wheel back gauge of the THS hydraulic shear"),
    # Q11 electric shears
    "tt-q11a": dict(src=P + "p57-000.png", crop=(55, 95, 835, 645), fill=[(655, 588, 848, 625)], cutout=True, up=True,
                    alt="Q11-3x1250A electric shear with light curtain, pneumatic sheet catcher and the mobile foot pedal"),
    "tt-q11a-rear": dict(src=P + "p57-000.png", crop=(845, 305, 1185, 565), cutout=True, up=True,
                         alt="Q11-3x1250A from the rear — light curtain and sheet catcher"),
    "tt-q11": dict(src=P + "p57-000.png", crop=(55, 775, 795, 1202), fill=[(465, 1138, 645, 1202)], cutout=True, up=True,
                   alt="Q11-3x2050 electric shear, 81″ × 1/8″, with front gauge arms and the foot pedal"),
    "tt-q11-gauge": dict(src=P + "p57-000.png", crop=(895, 835, 1165, 1055), cutout=False, alt="Manual back gauge with millimetre counter"),
    "tt-q11-stop": dict(src=P + "p57-000.png", crop=(895, 1085, 1165, 1290), cutout=False, alt="Bench angle stop on the shear table"),
    "tt-q11nc": dict(src=P + "p57-001.png", crop=(95, 635, 885, 1125), fill=[(525, 1078, 735, 1118)], cutout=True, up=True,
                     alt="Q11-2x2550NC electric shear with PLC control and motorised back gauge, 100″ × 14 ga"),
    "tt-q11nc-rear": dict(src=P + "p57-001.png", crop=(795, 1045, 1195, 1315), cutout=True, up=True,
                          alt="Q11-2x2550NC from the rear — interlocked rear guard and pneumatic sheet catcher"),
    "tt-q11nc-screen": dict(src=P + "p57-001.png", crop=(525, 170, 725, 365), cutout=False, alt="Touch-screen PLC control of the NC shear"),
    "tt-q11nc-light": dict(src=P + "p57-001.png", crop=(730, 170, 960, 365), cutout=False, alt="Cutting line lighting over the blade"),
    "tt-q11nc-balls": dict(src=P + "p57-001.png", crop=(525, 380, 725, 565), cutout=False, alt="Sheet hold-downs with rolling balls"),
    "tt-q11nc-gauge": dict(src=P + "p57-001.png", crop=(970, 380, 1185, 565), cutout=False, alt="Motorised back gauge with manual fine adjustment"),
    # Q11 mechanical shears
    "tt-q11-4x2000": dict(src=P + "p58-000.png", crop=(135, 235, 1065, 655), cutout=True, up=True,
                          alt="Q11-4x2000 mechanical shear, 79″ × 5/32″, with the foot pedal"),
    "tt-q11-3x1300": dict(src=P + "p58-000.png", crop=(455, 775, 1175, 1185), cutout=True, up=True,
                          alt="Q11-3x1300 mechanical shear, 51″ × 1/8″"),
    "tt-q11-6x2000": dict(src=P + "p58-001.png", crop=(85, 295, 1195, 965), cutout=True, up=True,
                          alt="Q11-6x2000 mechanical shear, 79″ × 1/4″, with hold-down cylinders"),
    # HQ hydraulic shears
    "tt-hq01": dict(src=P + "p59-000.png", crop=(165, 205, 1135, 905), fill=[(55, 800, 545, 968)], cutout=True, up=True,
                    alt="HQ01-2x1320B hydraulic shear, 52″ × 14 ga, with rear guard and the foot pedal"),
    "tt-hq01-photocell": dict(src=P + "p59-000.png", crop=(75, 1005, 425, 1270), cutout=False, alt="Optional photoelectric rear protection"),
    "tt-hq01-gauge": dict(src=P + "p59-000.png", crop=(445, 1005, 795, 1270), cutout=False, alt="Adjustable back gauge with scale"),
    "tt-hq01-switch": dict(src=P + "p59-000.png", crop=(815, 1005, 1165, 1270), cutout=False, alt="Control panel — automatic and single-stroke switching"),
    "tt-hq11": dict(src=P + "p59-001.png", crop=(145, 185, 1105, 825), fill=[(865, 775, 1105, 825)], cutout=True, up=True,
                    alt="HQ11-4.5x2000 hydraulic shear, 79″ × 3/16″, with hold-downs and the mobile foot pedal"),
    "tt-hq11-table": dict(src=P + "p59-001.png", crop=(65, 895, 335, 1105), cutout=False, alt="Ball-transfer table of the HQ11 shear"),
    "tt-hq11-egauge": dict(src=P + "p59-001.png", crop=(340, 895, 605, 1105), cutout=False, alt="Electric back gauge drive"),
    "tt-hq11-mgauge": dict(src=P + "p59-001.png", crop=(615, 895, 885, 1105), cutout=False, alt="Manual back gauge with hand wheel"),
    "tt-hq11-pump": dict(src=P + "p59-001.png", crop=(895, 895, 1165, 1105), cutout=False, alt="Lubrication pump"),
}


def process(key, spec):
    im = Image.open(spec["src"]).convert("RGB")
    if spec.get("fill"):
        d = ImageDraw.Draw(im)
        for r in spec["fill"]:
            d.rectangle(r, fill=(255, 255, 255))
    im = im.crop(spec["crop"])
    if spec.get("up", True):      # the page rasters are ~150 dpi: every crop is upscaled 2x (Real-ESRGAN)
        from esrgan import upscale
        im = upscale(im)
    os.makedirs(DST, exist_ok=True)
    out = os.path.join(DST, key + ".jpg")
    im.save(out, quality=92)
    return out, im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for key in keys:
        out, size = process(key, PHOTOS[key])
        print(f"{key:18s} {size} -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
