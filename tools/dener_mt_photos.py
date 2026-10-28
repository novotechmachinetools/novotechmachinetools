#!/usr/bin/env python3
"""Dener machine-tool photos → tools/src-images/dener/<key>.(png|jpg) (section 'dener', like tools/dener_photos.py).

Every photo comes from Dener's own websites:
  * the product catalogues linked from the product pages (en.dener.com/urun/11, 13, 14, 15 and denerusa.com/urun/…) and
    downloaded from https://dener.com/katalog/ — dener_dikey_isleme_merkezi.pdf (TMC), dener_ck_isleme_merkezi.pdf (TDC),
    TTC-TTH_CNC_Torna_Tezgahi_TR.pdf (TTC / TTH) and dener_taslama_tezgahi.pdf (TGH).  The photos and renders are taken out of
    the PDFs at their full embedded resolution, with Dener's own transparency masks (the renders are already cut out);
  * the product images on dener.com's home page (transparent PNG renders, 800 × 450) and its lathe slider photo.
Both were read in the built-in browser and saved to /home/claude/dener-mt/catalogues/ and /home/claude/dener-mt/web/
(dener.com and denerusa.com are outside this workspace's network allowlist).

Kinds:  png   — a cut-out render with its own alpha: exported as PNG, trimmed by make_images (trim: true);
        photo — a real scene (machining, a control, the tool changer): exported as JPG and kept rectangular (cutout: false);
        cut   — an object on a white or light-grey studio background: exported as JPG and cut out by make_images (BiRefNet).

Also writes 16:9 thumbnails for NovoTech's Shorts (the vertical frame on a blurred copy of itself) into
/home/claude/gms-site/yt/, where tools/yt_thumbs.py picks them up instead of YouTube's own (a three-frame strip for Shorts).

    python3 tools/dener_mt_photos.py
"""
import io
import os
import re

import fitz
from PIL import Image, ImageEnhance, ImageFilter

fitz.TOOLS.mupdf_display_errors(False)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = "/home/claude/dener-mt/catalogues/"
WEB = "/home/claude/dener-mt/web/"
YT = "/home/claude/dener-mt/yt/"
OUT = os.path.join(ROOT, "tools", "src-images", "dener")
THUMBS = "/home/claude/gms-site/yt"
SHORTS = {"gUYhBOqIP3M": "oardefault", "XhIVx8rzqnY": "oardefault", "dim9DA1TmoQ": "oardefault", "_bkvwzuOYW0": "oardefault"}

PDF = {"tmc": "dener_dikey_isleme_merkezi.pdf", "tdc": "dener_ck_isleme_merkezi.pdf",
       "ttc": "TTC-TTH_CNC_Torna_Tezgahi_TR.pdf", "tgh": "dener_taslama_tezgahi.pdf"}


def P(cat, xref, kind, alt, **spec):
    """an image of a Dener catalogue: the PDF (key of PDF) and the image object's xref"""
    return dict(pdf=cat, xref=xref, kind=kind, alt=alt, spec=spec)


def W(name, kind, alt, **spec):
    """an image of dener.com / denerusa.com"""
    return dict(web=name, kind=kind, alt=alt, spec=spec)


PHOTOS = {
    # TTC compact lathes (TTC-TTH catalogue, pages 3 – 5)
    "dn-ttc-1": P("ttc", 22, "png", "Dener TTC CNC lathe — fully enclosed 45° slant-bed lathe with the control on the front and the chip "
                                    "conveyor at the end", upscale=1.5),
    "dn-ttc-2": P("ttc", 66, "cut", "12-station servo turret of the Dener TTC and TTH CNC lathes — slot type, hydraulically clamped"),
    "dn-ttc-3": P("ttc", 19, "photo", "A shaft being turned on a Dener CNC lathe — the turret tool cutting the taper"),
    "dn-ttc-4": P("ttc", 38, "png", "One-piece 45° slant-bed casting with the headstock, turret slide and tailstock — the structure of the "
                                    "Dener TTC and TTH lathes"),
    # TTH lathes (dener.com home page; TTC-TTH catalogue, page 5)
    "dn-tth-1": W("web_dener_6946518400241349076.png", "png", "Dener TTH CNC lathe — Ø27.6″ swing, 8″ to 12″ chucks, chip conveyor at the end"),
    "dn-tth-2": P("ttc", 68, "cut", "BMT55 C-axis turret with 12 live-tool stations for drilling, tapping and milling (optional) — Dener TTH"),
    "dn-tth-3": P("ttc", 60, "cut", "Hydraulic tailstock on its own linear guides, moved independently of the turret — Dener TTH"),
    "dn-tth-5": W("web_dener_20276876237744754988.jpg", "photo", "Turning a part on a Dener CNC lathe — chuck, turret and tool at work"),
    # TMC vertical machining centres (TMC catalogue, pages 1 and 3 – 5)
    "dn-tmc-1": P("tmc", 20, "png", "Dener TMC vertical machining centre — fully enclosed, with the swivelling control pendant and the chip "
                                    "conveyor and cart", upscale=1.5),
    "dn-tmc-2": P("tmc", 38, "photo", "24-tool arm-type automatic tool changer of the Dener TMC — BBT40 tool holders"),
    "dn-tmc-3": P("tmc", 272, "photo", "Milling a pocket in an aluminium block with flood coolant on a Dener TMC vertical machining centre"),
    "dn-tmc-4": P("tmc", 41, "photo", "Mitsubishi M80 control with a 15″ touchscreen on the Dener TMC"),
    "dn-tmc-5": P("tmc", 269, "photo", "Dener TMC — the swivelling control pendant beside the front door"),
    "dn-tmc-6": P("tmc", 29, "cut", "Stress-relieved Meehanite castings — base, saddle, table and column of the Dener TMC"),
    "dn-tmc-7": P("tmc", 31, "photo", "Servo motor coupled directly to the C3 ballscrew between the roller linear guides — Dener TMC axis drive"),
    # TDC double-column machining centres (TDC catalogue; the machined part from the TMC catalogue, page 3)
    "dn-tdc-1": P("tdc", 85, "png", "Dener TDC double-column machining centre — semi-enclosed gantry, the cross rail on two columns"),
    "dn-tdc-2": P("tdc", 81, "png", "Dener TDC double-column machining centre — front view with the control on its swing arm"),
    "dn-tdc-3": P("tdc", 22, "cut", "BBT50 direct-drive spindle of the Dener TDC — 10,000 rpm, through-spindle coolant"),
    "dn-tdc-4": P("tdc", 23, "photo", "Roller linear guides and ballscrew on a Dener TDC axis"),
    "dn-tdc-5": P("tmc", 17, "photo", "A 3-D contoured aluminium part machined on a Dener machining centre"),
    # TGH surface grinder (TGH catalogue, pages 1, 3 – 5; dener.com home page)
    "dn-tgh-1": P("tgh", 17, "png", "Dener TGH-B 450 NC surface grinder — 17.7 × 35.4″ table, wheel head on the column, 10″ touchscreen "
                                    "control", upscale=1.5),
    "dn-tgh-2": P("tgh", 229, "png", "Dener TGH-B 450 surface grinder — three-quarter view with the control panel on the right"),
    "dn-tgh-4": P("tgh", 240, "photo", "Grinding a block on the magnetic chuck — wheel guard and coolant nozzle of the Dener TGH-B 450"),
    "dn-tgh-5": P("tgh", 231, "photo", "Mitsubishi NC with a 10″ touchscreen on the Dener TGH-B 450"),
    "dn-tgh-6": P("tgh", 55, "png", "15.7 × 31.5″ (400 × 800 mm) electromagnetic chuck of the Dener TGH-B 450"),
    "dn-tgh-7": P("tgh", 76, "cut", "Hydraulic unit with a 100 L tank — drives the table of the Dener TGH-B 450"),
}


def _final_width(key):
    """the width make_images will work from — after its trim (alpha box + 12 px, or the white margin of a photo) and upscale;
    None for a 'cut' photo (BiRefNet decides)"""
    p = PHOTOS[key]
    f = [x for x in os.listdir(OUT) if os.path.splitext(x)[0] == key]
    if not f or p["kind"] == "cut":
        return None
    im = Image.open(os.path.join(OUT, f[0]))
    if p["kind"] == "png":
        bb = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        w = (min(im.width, bb[2] + 12) - max(0, bb[0] - 12)) if bb else im.width
        return round(w * p["spec"].get("upscale", 1))
    bb = im.convert("L").point(lambda v: 0 if v >= 236 else 255).getbbox()
    if bb:
        px = round(max(bb[2] - bb[0], bb[3] - bb[1]) * 0.025)
        w = min(im.width, bb[2] + px) - max(0, bb[0] - px)
        if w >= im.width * 0.35:
            return w
    return im.width


def image_map_spec(key):
    """the tools/image_map.json fields of a photo (used by tools/dener_mt_pages.py).  Dener's catalogue photos are 480 – 1,200 px
    wide, so each keeps its own width as the largest variant instead of dropping to the next standard size."""
    p = PHOTOS[key]
    spec = {"trim": p["kind"] == "png", "quality": 82,
            "cutout": {"png": False, "photo": False, "cut": "birefnet"}[p["kind"]]}
    if p["kind"] == "png":
        spec["trim_white"] = False
    spec.update(p["spec"])
    w = _final_width(key)
    if w and 530 < w < 800:                               # below 800 the largest standard variant would be 480 px
        spec["sizes"] = [w, 480]
    elif w and 860 <= w < 1200:
        spec["sizes"] = [w, 800, 480]
    return spec


_docs = {}


def _doc(cat):
    if cat not in _docs:
        _docs[cat] = fitz.open(CAT + PDF[cat])
    return _docs[cat]


def _ref(doc, xref, key):
    t, v = doc.xref_get_key(xref, key)
    return int(v.split()[0]) if t == "xref" else 0


def pdf_image(cat, xref):
    """the image object at its embedded resolution: RGB, or RGBA when it carries a soft mask.  An Indexed image (a JPEG 2000
    palette image, which MuPDF hands back as raw palette indices) is decoded with its lookup table."""
    doc = _doc(cat)
    cs = doc.xref_get_key(xref, "ColorSpace")
    cs_obj = doc.xref_object(int(cs[1].split()[0])) if cs[0] == "xref" else cs[1]
    if "/Indexed" in cs_obj:
        lut_ref = re.findall(r"(\d+) 0 R", cs_obj)[-1]
        lut = doc.xref_stream(int(lut_ref))
        idx = Image.open(io.BytesIO(doc.xref_stream_raw(xref)))
        im = Image.frombytes("L", idx.size, idx.tobytes()).convert("P")
        im.putpalette(list(lut) + [0] * (768 - len(lut)))
        im = im.convert("RGB")
    else:
        pix = fitz.Pixmap(doc, xref)
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        if pix.n >= 4 or pix.colorspace is None or pix.colorspace.n != 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    sm = _ref(doc, xref, "SMask")
    if sm:
        m = fitz.Pixmap(doc, sm)
        mask = Image.frombytes("L", (m.width, m.height), m.samples)
        if mask.size != im.size:                  # Dener's masks are often drawn at twice the colour resolution
            mask = mask.resize(im.size, Image.LANCZOS)
        im = im.convert("RGBA")
        im.putalpha(mask)
    return im


def source(p):
    if "pdf" in p:
        return pdf_image(p["pdf"], p["xref"])
    im = Image.open(WEB + p["web"])
    return im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")


def flat(im, bg=(255, 255, 255)):
    if im.mode != "RGBA":
        return im.convert("RGB")
    base = Image.new("RGB", im.size, bg)
    base.paste(im, mask=im.getchannel("A"))
    return base


def export_one(key):
    p = PHOTOS[key]
    im = source(p)
    for old in (".png", ".jpg"):
        f = os.path.join(OUT, key + old)
        if os.path.exists(f):
            os.remove(f)
    if p["kind"] == "png":
        im = im.convert("RGBA")
        path = os.path.join(OUT, key + ".png")
        im.save(path, optimize=True)
    else:
        im = flat(im)
        if p["kind"] == "photo":
            im = ImageEnhance.Sharpness(im).enhance(1.15)
        path = os.path.join(OUT, key + ".jpg")
        im.save(path, quality=94)
    return path


def short_thumb(vid, which):
    """1280 × 720 for the video card: the vertical frame centred on a darkened, blurred copy of itself"""
    src = Image.open(YT + f"{vid}_{which}.jpg").convert("RGB")
    top = (round(1280 * src.height / src.width) - 720) // 2
    bg = src.resize((1280, round(1280 * src.height / src.width))).crop((0, top, 1280, top + 720))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(30))).enhance(0.55)
    fg = src.resize((round(720 * src.width / src.height), 720), Image.LANCZOS)
    bg.paste(fg, ((1280 - fg.width) // 2, 0))
    os.makedirs(THUMBS, exist_ok=True)
    path = os.path.join(THUMBS, vid + ".jpg")
    bg.save(path, quality=88)
    return path


def export():
    os.makedirs(OUT, exist_ok=True)
    for key in PHOTOS:
        path = export_one(key)
        im = Image.open(path)
        print(f"{key:12s} {PHOTOS[key]['kind']:5s} {im.size[0]}x{im.size[1]} {im.mode}")
    for vid, which in SHORTS.items():
        print("thumb", short_thumb(vid, which))


if __name__ == "__main__":
    export()
