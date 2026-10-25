#!/usr/bin/env python3
"""Direct-gear guillotine shear photos (NovoTech premium line, made in Turkey) → logo-free sources in
tools/src-images/saymak/.

Sources: the maker's 2025 catalogue (page extracts and 300-dpi page crops in /home/claude/saymak/img) and the per-model
gallery PNGs of the maker's site (/home/claude/saymak/web, real cut-outs with alpha).  The maker's lettering on the top
beam, the badge sticker beside it and the logo on the control screen are boxed by hand (source pixels) and filled with
LaMa (tools/delogo.py, mode "lama"); the alpha channel of the gallery PNGs is kept.  `--check` writes
/home/claude/saymak/work/check-<key>.jpg with the boxes drawn.

    python3 tools/saymak_photos.py [keys]          export
    python3 tools/saymak_photos.py --check [keys]  contact sheets only
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delogo import delogo  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/saymak/"
WORK = "/home/claude/saymak/work/"
OUT = os.path.join(ROOT, "tools", "src-images", "saymak")
MAX_SIDE = 2600
A = "lama"

# key: source file (relative to SRC), boxes (source px), alt; cutout False for detail shots; imap: extra image_map options
PHOTOS = {
    "sm-srgm": dict(src="img/p-004.png", boxes=[(600, 400, 840, 475)],
                    alt="SRGM direct-gear motorized guillotine shear, 1/4″ capacity — NovoTech premium line, with NC back gauge and front sheet support arms"),
    "sm-srgm-table": dict(src="web/SRGMi4.png", boxes=[(700, 0, 850, 45)], cutout=False, alt="SRGM shear — ball-transfer table, front sheet holding arms and finger guard"),
    "sm-srgm-rear": dict(src="web/SRGMi3.png", cutout=False, alt="SRGM shear — rear view with the NC back gauge and the sheet supports"),
    "sm-srgm-h": dict(src="img/p-023.png", boxes=[(860, 650, 1150, 730)],
                      alt="SRGM-H light type direct-gear guillotine shear, 1/8″ capacity — NovoTech premium line"),
    "sm-srgm-h-panel": dict(src="web/SRGM_Hi2.png", boxes=[(220, 265, 420, 340)], cutout=False, alt="SRGM-H shear — control panel with the back gauge position controller"),
    "sm-srgm-h-rear": dict(src="web/SRGM_Hi3.png", cutout=False, alt="SRGM-H shear — rear doors open: drive motor, gearbox and back gauge"),
    "sm-srgm-h-gauge": dict(src="web/SRGM_Hi4.png", cutout=False, alt="SRGM-H shear — back gauge and sheet supports behind the blade"),
    "sm-srgm-fr": dict(src="img/p-030.png", boxes=[(415, 148, 635, 215)], imap={"upscale": 1.5},
                       alt="SRGM-FR direct-gear guillotine shear with return-to-sender, 1/4″ capacity — NovoTech premium line"),
    "sm-srgm-fr-panel": dict(src="web/SRGM_FRi2.png", boxes=[(1005, 165, 1280, 255)], cutout=False, alt="SRGM-FR shear — NC control panel and front holding arm"),
    "sm-srgm-fr-rear": dict(src="web/SRGM_FRi3.png", cutout=False, alt="SRGM-FR shear — return-to-sender sheet support behind the blade"),
    "sm-srgm-fr-open": dict(src="web/SRGM_FRi4.png", cutout=False, alt="SRGM-FR shear — rear doors open, back gauge and return-to-sender supports"),
    "sm-srgm-hfr": dict(src="img/p-045.png", boxes=[(405, 75, 545, 125), (295, 104, 352, 134)], imap={"upscale": 1.5},
                        alt="SRGM-HFR light type guillotine shear with return-to-sender, 1/8″ capacity — NovoTech premium line"),
    "sm-srgm-hfr-blade": dict(src="web/SRGM_HFRi2.png", cutout=False, alt="SRGM-HFR shear — top and bottom blades and the sheet clamps"),
    "sm-srgm-cl": dict(src="img/cl-hero.png", boxes=[(370, 220, 810, 325)],
                       alt="SRGM-CL direct-gear guillotine shear for cut-to-length lines, 1/4″ capacity — NovoTech premium line"),
    "sm-srgm-hcl": dict(src="img/hcl-hero.png", boxes=[(290, 160, 665, 255)],
                        alt="SRGM-HCL light type guillotine shear for cut-to-length lines, 1/8″ capacity — NovoTech premium line"),
    "sm-srgm-hcl-rear": dict(src="web/SRGM_HCL_i3.png", cutout=False, alt="SRGM-HCL shear — rear view, open for the line's sheet feed"),
    "sm-elgo-p40t": dict(src="web/ELGO_P40T_DOKUNMATK_KONTROL_NTES.jpg", cutout=False, alt="ELGO P40T touch-screen NC control unit — optional on every SRGM shear"),
}


def process(key, check_only=False):
    p = PHOTOS[key]
    im = Image.open(SRC + p["src"])
    alpha = im.split()[-1] if im.mode in ("RGBA", "LA") else None
    rgb = im.convert("RGB")
    if alpha is not None:                      # inpaint on the photo composited over white, keep the cut-out alpha
        bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(rgb, mask=alpha); rgb = bg
    boxes = [(x0, y0, x1, y1, A) for x0, y0, x1, y1 in p.get("boxes", [])]
    s = min(1.0, MAX_SIDE / max(im.size))
    if check_only:
        d = ImageDraw.Draw(rgb)
        for x0, y0, x1, y1, _ in boxes:
            d.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=max(3, int(im.width / 400)))
        rgb.resize((int(im.width * s * 0.6), int(im.height * s * 0.6))).save(WORK + f"check-{key}.jpg", quality=80)
        print(f"{key:20s} {im.size} boxes={boxes}")
        return
    if boxes:
        rgb = delogo(rgb, boxes, report=[])
    out_im = rgb
    if alpha is not None:
        out_im = rgb.convert("RGBA"); out_im.putalpha(alpha)
    if s < 1:
        out_im = out_im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, key + (".png" if alpha is not None else ".jpg"))
    if alpha is not None:
        out_im.save(out, optimize=True)
    else:
        out_im.save(out, quality=92)
    print(f"{key:20s} {out_im.size} boxes={len(boxes)} -> {out}")


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for k in args or list(PHOTOS):
        process(k, check_only="--check" in sys.argv)
