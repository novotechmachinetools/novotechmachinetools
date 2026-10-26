#!/usr/bin/env python3
"""Cevisa (Vitoria, Spain) plate bevelling machines — photos from two sources outside the repo:

  /home/claude/cevisa/img/      cevisa.net product images (Oct 24): the shearing bevellers are Cevisa's own clean RGBA cut-outs
                                (47-…chp7, 49-…chp12, …); the milling bevellers are JPEGs on white (cut out by BiRefNet)
  /home/claude/cevisa/catimg/   images of the Cevisa catalogue (CATALOGO_CEVISA_EN-ES.pdf, pdfimages): bevelled plate samples,
                                machines at work and details — kept rectangular

Cut-outs are matted on white, upscaled 2x with Real-ESRGAN when small (`up`), their alpha resized to match, and written as
PNG; machines on white and photos as JPEG.  Written to tools/src-images/cevisa/<key>.png|jpg.

    python3 tools/cevisa_photos.py [key ...]      then   python3 tools/make_images.py --only $(cat tools/cevisa_keys.txt)
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "cevisa")
WEB, CAT = "/home/claude/cevisa/img/", "/home/claude/cevisa/catimg/"
MAX_SIDE = 2600


def C(src, alt, up=False, **kw):
    """an RGBA cut-out"""
    return dict(src=src, alt=alt, up=up, cutout=True, **kw)


def B(src, alt, up=False, crop=None, **kw):
    """a machine on a white background, cut out by BiRefNet in make_images"""
    return dict(src=src, alt=alt, up=up, crop=crop, cutout=True, rect=True, **kw)


def P(src, alt, crop=None, up=False, **kw):
    """a photo, kept rectangular"""
    return dict(src=src, alt=alt, crop=crop, up=up, cutout=False, **kw)


PHOTOS = {
    # ---- standard shearing: CHP 7 · CHP 12 · CHP 12 INV -----------------------------------------------------------
    "cv-chp7": C(WEB + "47-biseladora-achaflanadora-cizallado-estandar-chp7-cevisa.png", "Cevisa CHP 7 portable plate beveller with tube frame and handle"),
    "cv-chp12": C(WEB + "49-biseladora-achaflanadora-cizallado-estandar-chp12-cevisa.png", "Cevisa CHP 12 plate and tube bevelling machine", up=True),
    "cv-chp12-inv": C(WEB + "45-biseladora-achaflanadora-cizallado-gradual-chp12-inv-cevisa.png", "Cevisa CHP 12 INV inverted beveller on its stand, for lower bevels"),
    "cv-bevel-samples": P(CAT + "c-042.png", "Plate edges bevelled cold for welding by a Cevisa shearing beveller"),
    "cv-chp12-plate": P(CAT + "c-043.png", "CHP 12 feeding itself along a plate edge"),
    "cv-chp7-shell": P(CAT + "c-076.png", "CHP 7 bevelling the edge of a rolled shell"),
    "cv-chp12-bench": P(CAT + "c-096.png", "CHP 12 bevelling a plate on the bench"),
    "cv-chp12-crane": P(CAT + "c-070.png", "CHP 12 hung from a crane hook to bevel large plates"),
    "cv-cutters": P(WEB + "herramientas-de-corte-cevisa.jpg", "Sharpenable shear cutter of the CHP shearing bevellers"),
    # ---- adjustable shearing: CHP 12G · CHP 21G · CHP 21G INV ------------------------------------------------------
    "cv-chp12g": C(WEB + "52-biseladora-achaflanadora-cizallado-gradual-chp12g-cevisa.png", "Cevisa CHP 12G adjustable-angle beveller on its trolley"),
    "cv-chp21g": C(WEB + "54-biseladora-achaflanadora-cizallado-gradual-chp21g-cevisa.png", "Cevisa CHP 21G heavy-duty adjustable-angle beveller with built-in trolley", up=True),
    "cv-chp21g-inv": C(WEB + "56-biseladora-achaflanadora-cizallado-gradual-chp21g-inv-cevisa.png", "Cevisa CHP 21G INV inverted beveller for lower bevels on heavy plates", up=True),
    "cv-bevel-sample-v": P(CAT + "c-045.png", "V bevel on plate, cut cold — no heat-affected zone and no slag to grind"),
    "cv-bevel-cutting": P(CAT + "c-000.png", "A Cevisa shearing beveller cutting a bevel along a plate edge"),
    "cv-chp21g-inv-yard": P(CAT + "c-123.png", "CHP 21G INV with its plate support"),
    # ---- reversible shearing: CHP 12G REV · CHP 21G REV ------------------------------------------------------------
    "cv-chp21g-rev": C(WEB + "60-biseladora-achaflanadora-cizallado-reversible-chp21g-rev-cevisa.png", "Cevisa CHP 21G REV reversible beveller on its frame"),
    "cv-chp12g-rev": C(WEB + "58-biseladora-achaflanadora-cizallado-reversible-chp12g-rev-cevisa.png", "Cevisa CHP 12G REV reversible beveller", up=True),
    "cv-chp21g-rev-turned": B(CAT + "c-127.png", "CHP 21G REV turned over on its frame to bevel the lower edge", crop=(800, 90, 1925, 1360)),
    "cv-chp21g-rev-plate": P(CAT + "c-135.png", "CHP 21G REV with a plate in the bevelling head", up=True),
    "cv-chp12g-rev-detail": P(CAT + "c-147.png", "Pivot and locking handle the CHP 12G REV turns over on"),
    # ---- milling: CHP 30G · CHP 60G · CHP 60G INV · CHP 100G -----------------------------------------------------
    "cv-chp60g": B(WEB + "67-chp-60g.jpg", "Cevisa CHP 60G milling beveller with pneumatic height adjustment and built-in trolley"),
    "cv-chp30g": B(WEB + "64-chp-30g.jpg", "Cevisa CHP 30G milling beveller with control box and display", up=True),
    "cv-chp60g-inv": B(WEB + "71-chp-60ginv_1.jpg", "Cevisa CHP 60G INV inverted milling beveller for lower bevels", up=True),
    "cv-chp100g": B(WEB + "73-chp-100g_0.jpg", "Cevisa CHP 100G heavy milling beveller for bevels to 3-15/16″"),
    "cv-milled-bevel": P(WEB + "20200521_113624peq.jpg", "Machined bevel left by the CHP 60G milling head — no grinding needed before welding"),
    "cv-chp30g-plate": P(CAT + "c-164.png", "CHP 30G bevelling a plate"),
    "cv-chp100g-chips": P(WEB + "1.14_-_chp-100g_soplado_viruta.jpg", "CHP 100G milling a wide bevel — chips blown clear of the cut"),
    "cv-chp100g-panel": P(WEB + "chp-100g_caja_electrica_-_c.jpg", "CHP 100G control cabinet"),
    "cv-chp60g-pendant": P(CAT + "c-191.png", "CHP 60G control pendant, feed handwheel and 400 V supply"),
    "cv-milling-head": P(WEB + "herramienta-corte.jpg", "Milling head with indexable inserts of the CHP milling bevellers"),
}


def matte_rgba(im):
    """RGBA → (RGB matted on white, alpha)"""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB"), im.split()[-1]


def fit(im, alpha=None):
    s = MAX_SIDE / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        if alpha is not None:
            alpha = alpha.resize(im.size, Image.LANCZOS)
    return im, alpha


def process(key, spec):
    im = Image.open(spec["src"])
    os.makedirs(DST, exist_ok=True)
    if spec.get("cutout") and not spec.get("rect"):
        rgb, alpha = matte_rgba(im)
        bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
        rgb, alpha = rgb.crop(bb), alpha.crop(bb)
        if spec.get("up"):
            from esrgan import upscale
            big = upscale(rgb)
            alpha = alpha.resize(big.size, Image.LANCZOS)
            rgb = big
        rgb, alpha = fit(rgb, alpha)
        out = rgb.convert("RGBA"); out.putalpha(alpha)
        path = os.path.join(DST, key + ".png")
        if os.path.exists(os.path.join(DST, key + ".jpg")):
            os.remove(os.path.join(DST, key + ".jpg"))
        out.save(path, optimize=True)
        return path, out.size
    im = im.convert("RGB")
    if spec.get("crop"):
        im = im.crop(spec["crop"])
    if spec.get("up"):
        from esrgan import upscale
        im = upscale(im)
    im, _ = fit(im)
    path = os.path.join(DST, key + ".jpg")
    if os.path.exists(os.path.join(DST, key + ".png")):
        os.remove(os.path.join(DST, key + ".png"))
    im.save(path, quality=92)
    return path, im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for key in keys:
        path, size = process(key, PHOTOS[key])
        print(f"{key:24s} {size} -> {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
