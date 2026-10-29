#!/usr/bin/env python3
"""Photos of the Dener XL 1560 compact press brake (the owner's set of Oct 28 2026, 1600 × 1200, taken in a dealer's showroom).

Every photo carries the dealer's semi-transparent "Makinaalsat.com" watermark at the same place (x 636–964, y 586–617), the
three machine photos carry the dealer's name plate under the Dener logo, and the control pendant a Turkish warning sticker.
This tool cleans them without the smears a generic inpainter leaves on flat surfaces:

  * the watermark lettering is masked from the control photo (its blue / orange letters against the flat screen, dilated 3 px —
    tools/src-images/dener-xl1560/wm_mask_v2.png) and the mask is reused on every photo;
  * on flat surfaces (the white cover, the control screen) the masked pixels are replaced by a quadratic brightness surface fitted
    to the clean pixels around them plus the camera noise of that surface (`surface_fill`);
  * over structured parts (tool clamps, rails, the carbon bezel) LaMa fills the mask (`lama`);
  * the dealer's plate is covered by a patch of the same dark band copied from next to it (`patch_copy`);
  * the warning stickers on the cover are removed with the watermark (they sit inside it on the front photo);
  * the control pendant gets a hand-drawn alpha (polygons of the housing, the handle and the open area between them) instead
    of a BiRefNet cut, which blurred its edges; the three machine photos are cut by BiRefNet at 1536 px with keep / drop
    polygons (tools/cutout-specs/birefnet/dn-xl1560-*.json).

    python3 tools/dener_xl1560_photos.py [key …]      → tools/src-images/dener-xl1560/<key>.jpg|png   (raw photos in raw/)
    python3 tools/make_images.py --only $(cat tools/dener_xl1560_keys.txt)
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "tools", "src-images", "dener-xl1560")
RAW = os.path.join(D, "raw")
WM_MASK = os.path.join(D, "wm_mask_v2.png")       # the watermark lettering (dilated), same place in every photo

# ----------------------------------------------------------------------------------------------- building blocks

def load_mask(path):
    return np.asarray(Image.open(path).convert("L")) > 127


def box_mask(shape, boxes):
    m = np.zeros(shape[:2], bool)
    for x0, y0, x1, y1 in boxes:
        m[y0:y1, x0:x1] = True
    return m


def poly_mask(shape, polys):
    im = Image.new("L", (shape[1], shape[0]), 0)
    d = ImageDraw.Draw(im)
    for p in polys:
        d.polygon([tuple(q) for q in p], fill=255)
    return np.asarray(im) > 127


def sticker_mask(rgb, boxes, dil=4):
    """everything that is not the white cover inside the boxes (the yellow warning triangles, the grey labels), dilated"""
    L = rgb.mean(axis=2)
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    m = np.zeros(rgb.shape[:2], bool)
    for x0, y0, x1, y1 in boxes:
        sub = (L[y0:y1, x0:x1] < 200) | (sat[y0:y1, x0:x1] > 28)
        sub = ndimage.binary_closing(sub, structure=np.ones((5, 5)))
        m[y0:y1, x0:x1] = sub
    return ndimage.binary_dilation(m, iterations=dil)


def surface_fill(rgb, mask, region, degree=2, noise=True, seed=0, fit_on=None):
    """Replace the masked pixels inside `region` (x0, y0, x1, y1) with a polynomial surface (per channel) fitted to the
    unmasked pixels of the region (only those where `fit_on` is true, if given), plus Gaussian noise with the standard
    deviation of the photo's grain there (the high-pass residual).  For flat surfaces — a painted cover, a dark band, a
    switched-off screen."""
    import cv2
    x0, y0, x1, y1 = region
    sub = rgb[y0:y1, x0:x1].astype(np.float64)
    msub = mask[y0:y1, x0:x1]
    h, w = msub.shape
    yy, xx = np.mgrid[0:h, 0:w]
    xs = (xx - w / 2) / w; ys = (yy - h / 2) / h
    terms = [np.ones_like(xs)]                  # degree 0: the mean colour; 1: a plane; 2: a quadratic surface
    for dgr in range(1, degree + 1):
        for i in range(dgr + 1):
            terms.append(xs ** (dgr - i) * ys ** i)
    A = np.stack([t.ravel() for t in terms], axis=1)
    keep = ~msub
    if fit_on is not None:
        keep &= fit_on[y0:y1, x0:x1]
    keep = ndimage.binary_erosion(keep, iterations=2).ravel()      # stay clear of the mask's soft edge
    rng = np.random.default_rng(seed)
    out = sub.copy()
    for c in range(3):
        v = sub[..., c]
        coef, *_ = np.linalg.lstsq(A[keep], v.ravel()[keep], rcond=None)
        fit = A @ coef
        hp = v - cv2.GaussianBlur(v, (0, 0), 1.5)                   # the grain: what a 1.5 px blur removes
        sd = min(6.0, hp.ravel()[keep].std()) if noise else 0.0
        fill = fit + rng.normal(0, sd, fit.shape)
        ch = out[..., c].ravel()
        ch[~keep & msub.ravel()] = fill[~keep & msub.ravel()]
        ch[msub.ravel()] = fill[msub.ravel()]
        out[..., c] = ch.reshape(h, w)
    res = rgb.copy()
    res[y0:y1, x0:x1] = np.clip(out, 0, 255).astype(np.uint8)
    # soften the seam by a pixel (outside the mask; inside it the fill is used in full)
    soft = np.clip(cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.0) * 1.8, 0, 1)[..., None]
    blended = rgb.astype(np.float32) * (1 - soft) + res.astype(np.float32) * soft
    return np.clip(blended, 0, 255).astype(np.uint8)


def patch_copy(rgb, box, dx=0, dy=0, feather=5):
    """cover `box` with the pixels found `dx, dy` away (the same plain surface next to a plate), feathered at the edges"""
    import cv2
    x0, y0, x1, y1 = box
    res = rgb.copy()
    res[y0:y1, x0:x1] = rgb[y0 + dy:y1 + dy, x0 + dx:x1 + dx]
    m = np.zeros(rgb.shape[:2], np.float32); m[y0:y1, x0:x1] = 1
    soft = cv2.GaussianBlur(m, (0, 0), feather)[..., None]
    soft = np.clip(soft * 1.3, 0, 1)         # the centre stays fully copied
    return np.clip(rgb.astype(np.float32) * (1 - soft) + res.astype(np.float32) * soft, 0, 255).astype(np.uint8)


def lama(rgb, mask, context=1.0):
    from lama_inpaint import inpaint
    if not mask.any():
        return rgb
    return inpaint(rgb, (mask * 255).astype(np.uint8), context=context)


def jpeg_roundtrip(rgb, quality=95):
    import io
    b = io.BytesIO(); Image.fromarray(rgb).save(b, "JPEG", quality=quality)
    return np.asarray(Image.open(io.BytesIO(b.getvalue())).convert("RGB")).copy()


def telea(rgb, mask, r=4):
    import cv2
    if not mask.any():
        return rgb
    return cv2.inpaint(rgb, (mask * 255).astype(np.uint8), r, cv2.INPAINT_TELEA)


def alpha_from_polys(shape, keep, drop, ss=4):
    """an anti-aliased alpha: the keep polygons minus the drop polygons, rasterised at `ss` × and averaged down"""
    H, W = shape[:2]
    im = Image.new("L", (W * ss, H * ss), 0)
    d = ImageDraw.Draw(im)
    for p in keep:
        d.polygon([(x * ss, y * ss) for x, y in p], fill=255)
    for p in drop:
        d.polygon([(x * ss, y * ss) for x, y in p], fill=0)
    a = np.asarray(im).reshape(H, ss, W, ss).mean(axis=(1, 3))
    return a.astype(np.uint8)


# ----------------------------------------------------------------------------------------------- the photos

WM_ROWS = (583, 621)        # rows the dilated watermark mask occupies

# cover (white) stickers next to / inside the watermark on the three machine photos
STICKERS = {
    "front": [(608, 564, 672, 628), (760, 564, 824, 628), (890, 564, 954, 628), (696, 584, 764, 622), (826, 584, 910, 622)],
    "angle-left": [(670, 537, 728, 594), (790, 535, 848, 594), (903, 548, 949, 601)],
    "angle-right": [(592, 565, 636, 613), (691, 566, 736, 615), (804, 564, 852, 617)],
}

# key: dict(src, alt, cutout, steps)   — steps run in order on the RGB array
PHOTOS = {
    "dn-xl1560-front": dict(
        src="front.jpg", cutout=True, cut_size=1536,
        alt="Dener XL 1560 compact CNC press brake, 66 US tons × 5 ft, front view with the ESA control pendant",
        steps=[("plate", dict(poly=[(684, 293), (790, 293), (790, 329), (684, 329)], dx=110)),
               ("wm_cover", dict(faces=[[(660, 500), (905, 500), (930, 636), (625, 636)], [(958, 500), (1040, 500), (1040, 616), (958, 616)]], stickers="front"))]),
    "dn-xl1560-left": dict(
        src="angle-left.jpg", cutout=True, cut_size=1536,
        alt="Dener XL 1560 press brake from the left: Y1 / Y2 ram cylinders, DSP laser guards and the ESA control pendant",
        steps=[("plate", dict(poly=[(754, 266), (833, 278), (834, 315), (755, 303)], dx=95, dil=1, lama_dil=0, ctx=1.0, q=94,
                              protect=[[(700, 230), (850, 230), (850, 277), (820, 277), (762, 265), (700, 265)]])),
               ("wm_cover", dict(faces=[[(575, 500), (930, 500), (952, 606), (677, 606), (677, 580), (575, 580)],
                                       dict(poly=[(575, 579), (677, 579), (677, 607), (575, 607)], min_l=120, max_l=225, degree=0)],   # the Y1 cover's grey bevel
                                stickers="angle-left")),
               ("wm_lama", dict())]),
    "dn-xl1560-right": dict(
        src="angle-right.jpg", cutout=True, cut_size=1536,
        alt="Dener XL 1560 press brake from the right with the ESA control on its swing arm",
        steps=[("plate", dict(poly=[(638, 306), (718, 306), (718, 340), (638, 340)], dx=110)),
               ("wm_cover", dict(faces=[[(635, 500), (942, 500), (942, 613), (832, 613), (832, 632), (705, 632)],
                                       dict(poly=[(942, 560), (958, 560), (958, 613), (942, 613)], min_l=150, max_l=235, degree=1),   # the light-grey wall strip
                                       dict(poly=[(830, 613), (958, 613), (958, 640), (850, 640)], min_l=100, max_l=200)],         # the grey block under the cover
                                stickers="angle-right")),
               ("wm_lama", dict())]),
    "dn-xl1560-control": dict(
        src="control.jpg", cutout="polys",
        alt="ESA touch-screen control pendant of the Dener XL 1560 — start, stop, muting lamp and general reset",
        steps=[("copy_cols", dict(box=(414, 846, 614, 912), dx=250)),             # the warning sticker over the button panel
               ("frame_strip", dict(x=(378, 422), rows=(846, 1048), shift=-200)),  # … and over the left frame
               ("patch", dict(box=(798, 632, 874, 700), dx=154)),                   # the model mark under the screen: carbon weave copied
                                                                                   # from 154 px (22 weave periods) to the right
               ("wm_cover", dict(faces=[[(540, 540), (1130, 540), (1130, 615), (540, 615)]], min_l=0)),   # the watermark on the screen
               ("wm_telea", dict(rows=(615, 622)))],                               # its last rows on the bezel edge
        keep=[[(407, 111), (1259, 97), (1263, 500), (1267, 700), (1271, 850), (1279, 1000), (1287, 1100), (1289, 1147), (1283, 1156), (1268, 1157),
               (1262, 1146), (404, 1141), (398, 1149), (388, 1148), (383, 1140), (383, 1100), (391, 1000), (403, 850), (403, 700), (407, 500)],
              [(748, 0), (905, 0), (905, 115), (748, 115)]],                       # the swing arm
        drop=[[(414, 905), (1257, 910), (1271, 1086), (398, 1086)]]),              # the open area between panel and handle
    "dn-xl1560-tooling": dict(src="tooling-left.jpg", alt="EUROSTAMP punch 1281 in the segmented holders, 4-way die and DSP laser transmitter on the XL 1560",
                              steps=[("wm_lama", dict())]),
    "dn-xl1560-tooling-2": dict(src="tooling-right.jpg", alt="Segmented top-tool holders, EUROSTAMP tooling, front supports and the DSP laser receiver on the XL 1560",
                                steps=[("wm_lama", dict())]),
    "dn-xl1560-backgauge": dict(src="backgauge.jpg", alt="X-axis back gauge of the XL 1560 on its ball screw with two fingers and the servo drive",
                                steps=[("wm_lama", dict()), ("lama_box", (975, 948, 1115, 1092))]),
    "dn-xl1560-backgauge-2": dict(src="backgauge-side.jpg", alt="Back gauge beam, fingers and rear sheet support of the XL 1560 seen through the side frame",
                                  steps=[("wm_cover", dict(faces=[dict(poly=[(848, 572), (1010, 572), (1010, 648), (785, 648), (785, 606), (805, 604)], min_l=0, max_l=70)])),   # the dark background behind the beam
                                         ("wm_lama", dict())]),
}


def frame_outer(y):
    """x of the pendant's outer left edge (it flares out towards the handle)"""
    pts = [(111, 407), (500, 407), (700, 403), (850, 403), (1000, 391), (1080, 383), (1150, 383)]
    return float(np.interp(y, [p[0] for p in pts], [p[1] for p in pts]))


def process(key):
    p = PHOTOS[key]
    rgb = np.asarray(Image.open(os.path.join(RAW, p["src"])).convert("RGB")).copy()
    wm = load_mask(WM_MASK)
    done = np.zeros(wm.shape, bool)          # watermark pixels already filled by an earlier step
    for step in p.get("steps", []):
        kind, arg = step[0], step[1]
        if kind == "plate":                      # the dealer's plate on the dark band: the band's brightness surface plus the
            poly = arg["poly"]                   # band's own mottled texture copied from next to the plate, then LaMa over it
            m = poly_mask(rgb.shape, [poly])
            if arg.get("dil", 2):
                m = ndimage.binary_dilation(m, iterations=arg.get("dil", 2))   # a little wider, so the plate's edges go too
            protect = poly_mask(rgb.shape, arg["protect"]) if arg.get("protect") else None   # the maker's logo next to it
            if protect is not None:
                m &= ~protect
            ys, xs = np.where(m); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            L = rgb.mean(axis=2); sat = rgb.max(axis=2) - rgb.min(axis=2)
            band = (L > 35) & (L < 100) & (sat < 40)       # the grey band itself — not the logo, the red stripe or the shadow line
            filled = surface_fill(rgb, m, (max(0, x0 - 70), max(0, y0 - 30), min(rgb.shape[1], x1 + 70), min(rgb.shape[0], y1 + 20)), degree=2, fit_on=band, noise=False)
            dx = arg.get("dx", 110)                         # the band's own mottled texture, copied from next to the plate
            src = rgb[y0:y1, x0 + dx:x1 + dx].astype(np.float32)
            sb = band[y0:y1, x0 + dx:x1 + dx]               # (only where the source really is band; elsewhere no texture)
            detail = np.where(sb[..., None], src - src[sb].mean(axis=0), 0.0)
            patch = np.clip(filled[y0:y1, x0:x1].astype(np.float32) + detail, 0, 255)
            import cv2
            res = rgb.copy(); res[y0:y1, x0:x1] = patch.astype(np.uint8)
            soft = np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.0) * 1.8, 0, 1)[..., None]   # hard inside, feathered outside
            rgb = np.clip(rgb.astype(np.float32) * (1 - soft) + res.astype(np.float32) * soft, 0, 255).astype(np.uint8)
            rgb = jpeg_roundtrip(rgb, arg.get("q", 95))     # (LaMa's output depends on the input's fine grain: on the lossless array it
                                                            # paints a blotch here, on a JPEG-grained copy a seamless band — so grain it)
            mm = ndimage.binary_dilation(m, iterations=arg.get("lama_dil", 1)) if arg.get("lama_dil", 1) else m
            if protect is not None:
                mm &= ~protect
            rgb = lama(rgb, mm, context=arg.get("ctx", 2.0))   # LaMa then re-synthesises the patch from the band around it — with the
                                                            # plate already gone it continues the band's gradient and mottling seamlessly
        elif kind == "lama_box":
            rgb = lama(rgb, box_mask(rgb.shape, [arg]))
        elif kind == "telea_box":                # a small label on a plain dark panel: diffusion fill from its rim
            rgb = telea(rgb, box_mask(rgb.shape, [arg]), 6)
        elif kind == "patch":                    # a plain surface patch copied from the same texture next to it
            rgb = patch_copy(rgb, arg["box"], dx=arg.get("dx", 0), dy=arg.get("dy", 0), feather=arg.get("feather", 3))
        elif kind == "copy_cols":
            x0, y0, x1, y1 = arg["box"]; dx = arg["dx"]
            rgb[y0:y1, x0:x1] = rgb[y0:y1, x0 + dx:x1 + dx]
        elif kind == "frame_strip":
            xa, xb = arg["x"]; ya, yb = arg["rows"]; sh = arg["shift"]
            for y in range(ya, yb):
                dx = int(round(frame_outer(y) - frame_outer(y + sh)))
                rgb[y, xa:xb] = rgb[y + sh, xa - dx:xb - dx]
        elif kind == "wm_cover":                 # the watermark (and stickers) on flat faces: one fitted surface per face
            m = wm.copy()
            if arg.get("stickers"):
                m |= sticker_mask(rgb, STICKERS[arg["stickers"]])
            L = rgb.mean(axis=2)
            for face in arg["faces"]:            # each flat face as a polygon, with the brightness range of its own paint
                if isinstance(face, dict):       # (the structured parts beside them are LaMa's job)
                    poly, lo, hi, deg = face["poly"], face.get("min_l", 205), face.get("max_l", 256), face.get("degree", 2)
                else:
                    poly, lo, hi, deg = face, arg.get("min_l", 205), 256, 2
                inside = poly_mask(rgb.shape, [poly])
                mm = m & inside
                if mm.any():
                    xs, ys = [p_[0] for p_ in poly], [p_[1] for p_ in poly]
                    region = (max(0, min(xs) - 10), max(0, min(ys)), min(rgb.shape[1], max(xs) + 10), min(rgb.shape[0], max(ys)))
                    rgb = surface_fill(rgb, mm, region, degree=deg, fit_on=(L > lo) & (L < hi) & inside)
                    done |= mm
            wm_rest = m & ~done                  # over the recess walls, labels and edges: LaMa (3 px wider, so its feathered
            if wm_rest.any():                    # edge lies in the freshly filled face, not in the sticker it is removing)
                rgb = lama(rgb, ndimage.binary_dilation(wm_rest, iterations=3))
                done |= wm_rest
        elif kind == "wm_lama":
            m = wm & ~done
            if arg.get("rows"):
                r0, r1 = arg["rows"]; sel = np.zeros_like(m); sel[r0:r1] = True; m &= sel
            rgb = lama(rgb, ndimage.binary_dilation(m, iterations=4))    # 4 px wider: LaMa feathers its edge over ~3 px, and the
            done |= m                                                     # lettering's anti-aliased rim must not bleed through there
        elif kind == "wm_telea":
            m = wm & ~done
            r0, r1 = arg["rows"]; sel = np.zeros_like(m); sel[r0:r1] = True; m &= sel
            rgb = telea(rgb, m, 4)
            done |= m
        else:
            raise SystemExit(f"unknown step {kind}")
    os.makedirs(D, exist_ok=True)
    if p.get("cutout") == "polys":
        a = alpha_from_polys(rgb.shape, p["keep"], p.get("drop", []))
        rgba = np.dstack([rgb, a])
        ys, xs = np.where(a > 0)
        pad = 12
        box = (max(0, xs.min() - pad), max(0, ys.min() - pad), min(rgb.shape[1], xs.max() + pad), min(rgb.shape[0], ys.max() + pad))
        out = Image.fromarray(rgba, "RGBA").crop(box)
        path = os.path.join(D, key + ".png")
        out.save(path, optimize=True)
    else:
        out = Image.fromarray(rgb)
        path = os.path.join(D, key + ".jpg")
        out.save(path, quality=94)
    return path, out.size


def register():
    """image_map entries (section dener-xl1560) and the key list for make_images"""
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    keys = []
    for key, p in PHOTOS.items():
        ext = ".png" if p.get("cutout") == "polys" else ".jpg"
        if not os.path.exists(os.path.join(D, key + ext)):
            print("!! missing export for", key)
            continue
        e = {"src": f"tools/src-images/dener-xl1560/{key}{ext}", "alt": p["alt"], "section": "dener-xl1560", "trim": ext == ".png",
             "quality": 84, "cutout": p.get("cutout") is True}
        if os.path.exists(os.path.join(D, key + "-cut.png")):   # tools/xl1560_cut.py (SAM selection + BiRefNet edge): the alpha is final
            e = {"src": f"tools/src-images/dener-xl1560/{key}-cut.png", "alt": p["alt"], "section": "dener-xl1560", "trim": True, "quality": 84}
        elif p.get("cut_size"):
            e["cut_size"] = p["cut_size"]
        spec = os.path.join(ROOT, "tools", "cutout-specs", "birefnet", key + ".json")
        if e.get("cutout") and os.path.exists(spec):        # keep / drop polygons for a cut BiRefNet gets wrong
            e["cut_spec"] = f"tools/cutout-specs/birefnet/{key}.json"
        imap[key] = e
        keys.append(key)
    # Dener's own studio cut-out of the XL 1500 × 60 (supplied by NovoTech, Oct 2026): the lead photo of the gallery
    studio = os.path.join(D, "dn-xl1560-studio.png")
    if os.path.exists(studio):
        imap["dn-xl1560-studio"] = {"src": "tools/src-images/dener-xl1560/dn-xl1560-studio.png", "section": "dener-xl1560", "trim": True, "quality": 84,
                                    "alt": "Dener XL 1560 compact CNC press brake, 66 US tons × 5 ft, with the ESA S840 control pendant — studio photo"}
        keys.append("dn-xl1560-studio")
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "dener_xl1560_keys.txt"), "w").write(",".join(keys))
    return keys


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--register" not in sys.argv:
        for k in keys or list(PHOTOS):
            path, size = process(k)
            print(f"{k:24s} {size} -> {os.path.relpath(path, ROOT)}")
    print("registered:", len(register()))


if __name__ == "__main__":
    main()
