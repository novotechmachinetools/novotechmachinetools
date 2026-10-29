#!/usr/bin/env python3
"""Photos of the HP horizontal presses, TB mandrel-less pipe benders and WP welding positioners (NovoTech premium line, made in
Turkey) from three sources outside the repo:

  /home/claude/tubend/img/      tubend.com.tr product images (Oct 24) — the machine PNGs are Tubend's own clean cut-outs
  /home/claude/tubend/pdfimg/   images of NovoTech's earlier Tubend brochure (NovoTech_Tubend_Presses_Benders_2026.pdf, pdfimages;
                                c-*.png = image + its soft mask)
  /home/claude/tubend/catimg/   images of the Tubend General Catalogue 2026 (pdfimages; c-005 + c-006 = back-gauge press + mask)

Cut-outs (RGBA) are matted on white, upscaled 2x with Real-ESRGAN when they are small (`up`), their alpha resized to match,
and written as PNG; photos as JPEG.  Written to tools/src-images/tubend/<key>.png|jpg; make_images keeps the alpha.

    python3 tools/tubend_photos.py [key ...]      then   python3 tools/make_images.py --only $(cat tools/tubend_keys.txt)
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "tubend")
WEB, PDF, CAT = "/home/claude/tubend/img/", "/home/claude/tubend/pdfimg/", "/home/claude/tubend/catimg/"
MAX_SIDE = 2600


def C(src, alt, mask=None, up=False, **kw):
    """a cut-out: an RGBA source, or an RGB source with a separate mask file"""
    return dict(src=src, mask=mask, alt=alt, up=up, cutout=True, **kw)


def P(src, alt, crop=None, **kw):
    """a photo, kept rectangular"""
    return dict(src=src, alt=alt, crop=crop, cutout=False, **kw)


def B(src, alt, **kw):
    """a machine on a white background, cut out by BiRefNet in make_images"""
    return dict(src=src, alt=alt, cutout=True, rect=True, **kw)


PHOTOS = {
    # ---- HP 10 – HP 100 -------------------------------------------------------------------------------------------
    "tb-hp10": C(WEB + "hp10.png", "NovoTech HP 10 NC hydraulic horizontal press with touch-screen control stand and foot pedal", up=True),
    "tb-hp80": C(WEB + "hp80.png", "NovoTech HP 80 hydraulic horizontal press with induction-hardened support pins, control stand and foot pedal", up=True),
    "tb-hp-backgauge": B(CAT + "c-005.png", "HP horizontal press with servo-driven NC back gauge, touch-screen control stand and foot pedal"),
    "tb-hp-screen-manual": P(PDF + "p06-000.png", "HP touch-screen in manual mode: the ram works between the minimum and maximum stroke set in mm"),
    "tb-hp-screen-recipe": P(PDF + "p07-002.png", "HP touch-screen in recipe mode: ram and back gauge positions for each step of a part"),
    "tb-hp-tool-vdie": P(PDF + "p09-001.png", "Press brake punch with multi-V die on the HP table"),
    "tb-hp-tool-pipe": P(PDF + "p09-006.png", "Mandrel-less pipe bending tool with a tube bent to an S"),
    "tb-hp-tool-pipe-end": P(PDF + "p09-008.png", "Pipe end reduction and expansion tool"),
    "tb-hp-tool-radius": P(PDF + "p10-001.png", "Wide-radius bending tool bending 13/16″ (20 mm) plate"),
    "tb-hp-tool-busbar": P(PDF + "p10-008.png", "Busbar precision bending tool bending copper busbar"),
    "tb-hp-parts": C(PDF + "c-p06-007.png", "Flat bar, angle, channel, pipe and round bar parts bent on the HP", clean=40),
    "tb-hp-busbar-parts": C(PDF + "c-p06-003.png", "Copper busbars bent and punched on the HP", clean=40, edge=12),
    # ---- HP 120 / HP 150 ------------------------------------------------------------------------------------------
    "tb-hp120": C(WEB + "hp120-2.png", "NovoTech HP 120 / HP 150 heavy-duty horizontal press with T-slot table, support columns and control stand", up=True),
    "tb-hp120-side": C(WEB + "hp120.png", "HP 120 / HP 150 from the side: hydraulic unit, control box, T-slot table and foot pedal", up=True),
    "tb-hp120-straighten": P(WEB + "hp120-2.jpg", "Straightening a plate between the hardened support columns of the HP 120 / HP 150"),
    # ---- TB 34 / TB 42 --------------------------------------------------------------------------------------------
    "tb-tb34": C(WEB + "tb34.png", "NovoTech TB 34 electric mandrel-less pipe bender with digital angle readout", up=True),
    "tb-tb34-parts": P(PDF + "p20-000.png", "Street furniture, bike racks and serpentine tube bent on the TB 34"),
    "tb-tb34-barrier": P(PDF + "p20-001.png", "Safety barrier bent from pipe on the TB 34"),
    "tb-tb42": C(WEB + "tb42.png", "NovoTech TB 42 hydraulic mandrel-less pipe bender", up=True),
    "tb-tb42-part": P(WEB + "tb42-1.jpg", "Pipe bent to a U on the TB 42"),
    "tb-tb42-dies": P(PDF + "p21-000.png", "TB 42 pipe bending dies on the top plate"),
    "tb-tb42-panel": P(PDF + "p21-001.png", "TB 42 control panel with digital readout, emergency stop and joystick"),
    # ---- WP 100 / WP 300 ------------------------------------------------------------------------------------------
    "tb-wp300": C(WEB + "wp300.png", "NovoTech WP 300 tilting welding positioner with slotted turntable and control box"),
    "tb-wp100": C(WEB + "wp100.png", "NovoTech WP 100 compact tilting welding positioner"),
    "tb-wp300-plate": C(PDF + "c-p28-002.png", "WP 300 with a custom perforated work plate for welding fixtures", clean=40),
}


def matte_rgba(im):
    """RGBA → (RGB matted on white, alpha)"""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB"), im.split()[-1]


# the maker's logo and name on the photos — every machine is sold as NovoTech's premium line (HP presses Oct 2026, TB benders and
# WP positioners Oct 28 2026): boxes (x0, y0, x1, y1) in the pixels of the finished photo, filled by LaMa (tools/lama_inpaint.py)
LOGO = {
    "tb-hp10": [(55, 82, 273, 217)], "tb-hp80": [(113, 158, 347, 275)], "tb-hp-backgauge": [(274, 90, 352, 172)],
    "tb-hp120-straighten": [(2235, 115, 2570, 255)],
    "tb-tb34": [(480, 705, 820, 938)],                                   # name plate on the front of the bender
    "tb-tb42": [(415, 402, 618, 538), (1135, 310, 1280, 392)],          # name plate on the door; name embossed on the side handle
    "tb-tb42-panel": [("tint", 335, 688, 556, 848), ("tint", 556, 700, 600, 828)],   # name printed on the control panel, under the STOP ring, beside the panel edge
    "tb-wp300": [(202, 728, 300, 828)], "tb-wp300-plate": [(275, 775, 392, 858)],   # name plate on the column
}
# the maker's name typed on a control screen: the cell is painted with its own background colour, sampled at (x, y)
SCREEN = {"tb-hp-screen-recipe": [((905, 168, 1040, 207), (1060, 186))]}


def delogo(im, boxes):
    """boxes: (x0, y0, x1, y1) fills the whole rectangle; ("tint", x0, y0, x1, y1) fills only the blue-tinted pixels (the maker's
    blue-grey lettering and its blue underline) inside the rectangle, dilated by a few pixels — for a logo printed next to
    other labels that must stay."""
    import numpy as np
    from lama_inpaint import inpaint
    from scipy import ndimage
    rgba = im.mode == "RGBA"
    rgb = np.asarray(im.convert("RGB")).copy()
    mask = np.zeros(rgb.shape[:2], np.uint8)
    for box in boxes:
        if box[0] == "tint":
            _, x0, y0, x1, y1 = box
            sub = rgb[y0:y1, x0:x1].astype(int)
            r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
            yellow = ndimage.binary_dilation((r > 170) & (g > 150) & (b < 130), iterations=5)       # the STOP ring and its black letters stay
            dark = (r < 130) & (g < 130) & (b < 150) & ~yellow
            tint = (((b > r + 8) & (r < 215) & (b > 60)) | dark) & ~yellow                           # lettering, its halo, dark specks
            tint = ndimage.binary_dilation(tint, iterations=9) & ~yellow
            mask[y0:y1, x0:x1][tint] = 255
        else:
            x0, y0, x1, y1 = box
            mask[y0:y1, x0:x1] = 255
    out = Image.fromarray(inpaint(rgb, mask))
    if rgba:
        out.putalpha(im.getchannel("A"))
    return out


def process(key, spec):
    path, size = _process(key, spec)
    if key in LOGO or key in SCREEN:
        im = Image.open(path)
        im = im.convert("RGBA") if path.endswith(".png") else im.convert("RGB")
        if key in LOGO:
            im = delogo(im, LOGO[key])
        for box, at in SCREEN.get(key, []):
            from PIL import ImageDraw
            ImageDraw.Draw(im).rectangle(box, fill=im.getpixel(at))
        im.save(path, **({"optimize": True} if path.endswith(".png") else {"quality": 92}))
    return path, size


def _process(key, spec):
    im = Image.open(spec["src"])
    if spec.get("cutout") and not spec.get("rect"):
        if spec.get("mask"):
            rgb, alpha = im.convert("RGB"), Image.open(spec["mask"]).convert("L")
        else:
            rgb, alpha = matte_rgba(im)
        if spec.get("clean"):        # the earlier brochure's cut-outs: a faint haze and an edge strip around the parts
            t, e = spec["clean"], spec.get("edge", 0)
            alpha = alpha.point(lambda v: 0 if v < t else v)
            if e:
                from PIL import ImageDraw
                d = ImageDraw.Draw(alpha); w, h = alpha.size
                d.rectangle((w - e, 0, w, h), fill=0); d.rectangle((0, 0, e, h), fill=0)
        bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
        rgb, alpha = rgb.crop(bb), alpha.crop(bb)
        if spec.get("up"):
            from esrgan import upscale
            big = upscale(rgb)
            alpha = alpha.resize(big.size, Image.LANCZOS)
            rgb = big
        s = MAX_SIDE / max(rgb.size)
        if s < 1:
            rgb = rgb.resize((round(rgb.width * s), round(rgb.height * s)), Image.LANCZOS)
            alpha = alpha.resize(rgb.size, Image.LANCZOS)
        out = rgb.convert("RGBA"); out.putalpha(alpha)
        path = os.path.join(DST, key + ".png")
        os.makedirs(DST, exist_ok=True)
        for old in (os.path.join(DST, key + ".jpg"),):
            if os.path.exists(old):
                os.remove(old)
        out.save(path, optimize=True)
        return path, out.size
    im = im.convert("RGB")
    for old in (os.path.join(DST, key + ".png"),):
        if os.path.exists(old):
            os.remove(old)
    if spec.get("crop"):
        im = im.crop(spec["crop"])
    s = MAX_SIDE / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    os.makedirs(DST, exist_ok=True)
    path = os.path.join(DST, key + ".jpg")
    im.save(path, quality=92)
    return path, im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for key in keys:
        path, size = process(key, PHOTOS[key])
        print(f"{key:22s} {size} -> {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
