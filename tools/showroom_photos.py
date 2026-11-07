#!/usr/bin/env python3
"""NovoTech's own showroom and warehouse photos for the About Us page (the owner, Nov 7 2026: "work these photos into the
About Us page; wherever a machine carries the Şahinler brand, remove it; retouch them a little so they look nicer").

Every şahinler name plate is emptied: the lettering and the emblem are painted out with the plate's own colour and the plate
itself stays (the Şahinler-built machines are sold as the NovoTech premium line).  Then a light retouch: white balance from the
white walls, levels, a little local contrast and vibrance, and a fine sharpening.

    python3 tools/showroom_photos.py               → tools/src-images/site/showroom/<key>.jpg and the image_map entries
    python3 tools/make_images.py --only <keys>     (the keys are printed at the end)

Sources: the owner's photos, /home/claude/untrusted/2026-11-07-showroom/sr01–sr13.jpg (and dener-factory.png, a frame of
Dener's own factory video).
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/untrusted/2026-11-07-showroom/"
OUT = os.path.join(ROOT, "tools", "src-images", "site", "showroom")
MAP = os.path.join(ROOT, "tools", "image_map.json")

# key: (source, alt text, şahinler plates as search boxes x0, y0, x1, y1 in the source's pixels) — in the gallery's order
PHOTOS = {
    "nt-about-building": ("sr12.jpg", "NovoTech Machine Tools at 1365 Mid-Way Blvd, Unit 26, Mississauga, ON", []),
    "nt-about-ironworker-rebar": ("sr05.jpg", "HKM 85 ironworker, B 50 rebar bender, H 45S rebar cutters and more rebar machines in the "
                                  "NovoTech showroom, Mississauga, ON", [(310, 1072, 466, 1143)]),
    "nt-about-ironworkers": ("sr10.jpg", "A row of hydraulic ironworkers, HKM 115 and HKM 85 among them, ready to ship from "
                             "Mississauga, ON", [(922, 498, 1012, 561), (444, 377, 495, 422), (226, 318, 262, 353),
                                                 (103, 270, 119, 292), (16, 248, 33, 269)]),
    "nt-about-bender-plate-rollers": ("sr13.jpg", "HPK section bender, an ironworker and ISITAN plate rollers in the NovoTech "
                                      "showroom, Mississauga, ON", [{"poly": [(48.3, 1238.3), (200.7, 1208.3), (208.3, 1258.3), (56.0, 1291.7)], "inset": 3.5,
                                         "keep": [(52.7, 1240.7), (196.7, 1211.7), (203.3, 1256.7), (60.7, 1287.7)]},
                                        {"poly": [(781.7, 1063.0), (905.5, 1047.5), (905.5, 1118.5), (783.3, 1129.7)], "inset": 3.5,
                                         "keep": [(785.7, 1072.0), (787.3, 1125.3)]}]),
    "nt-about-ironworkers-benders": ("sr01.jpg", "HKM 115 ironworker, HPK 60 and HPK 50 section benders and more ironworkers in the "
                                     "NovoTech showroom, Mississauga, ON", [(136, 572, 220, 610), (566, 550, 622, 583),
                                                                            (760, 556, 794, 578), (951, 578, 976, 597),
                                                                            (1051, 585, 1076, 604)]),
    "nt-about-band-saws": ("sr11.jpg", "Bekamak BMSO 320E automatic band saws in stock at NovoTech, Mississauga, ON", []),
    "nt-about-pipe-polishers": ("sr09.jpg", "BT 114-S pipe polishing machines and a Gecam machine ready for delivery from "
                                "Mississauga, ON", [(471, 472, 533, 521), (260, 421, 301, 462), (112, 387, 146, 417)]),
    "nt-about-bt26": ("sr04.jpg", "BT 26 rebar benders, the most popular rebar bender, in stock at NovoTech, Mississauga, ON", []),
    "nt-about-rebar-machines": ("sr06.jpg", "MAX 40 combined rebar cutters and benders, BT 24x5, B 36 and B 45x1 rebar benders in "
                                "stock at NovoTech, Mississauga, ON", []),
    "nt-about-ironworkers-plate-rollers": ("sr08.jpg", "Ironworkers and ISITAN plate rollers in the NovoTech warehouse, "
                                           "Mississauga, ON", [(282, 534, 308, 558), (24, 738, 96, 828)]),
    "nt-about-rebar-cutters": ("sr07.jpg", "H 45S rebar cutters, BT 26 rebar benders and a POWER 24 portable rebar cutter in stock "
                               "at NovoTech, Mississauga, ON", []),
    "nt-about-warehouse": ("sr02.jpg", "New machines in the NovoTech warehouse, Mississauga, ON: folding brakes, plate rollers and "
                           "ironworkers ready to ship", []),
    "nt-about-showroom-stock": ("sr03.jpg", "The NovoTech showroom floor, Mississauga, ON: section benders, folding brakes and "
                                "plate rollers in stock", []),
}
FACTORY = {"nt-about-dener-factory": ("dener-factory.png", "Press brakes on the assembly line in Dener's factory in Kayseri, Turkey")}


def blank_plates(img, boxes):
    """img: RGB uint8.  In each box: the dark plate (largest dark area, its holes filled), the white lettering inside it, the
    lettering's hull (screws left out) painted out with the plate's own colour."""
    out = img.copy()
    for b in boxes:
        if isinstance(b, dict):                                  # a plate drawn by hand: its corners and its screws
            blank_polygon(out, b["poly"], b.get("inset", 3), b.get("keep", ()))
            continue
        x0, y0, x1, y1 = b
        crop = out[y0:y1, x0:x1]
        gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
        thr, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        dark = gray < thr
        k = max(3, min(crop.shape[:2]) // 6)
        closed = ndimage.binary_closing(dark, structure=np.ones((k, k)), iterations=1, border_value=0)
        # a cable across the plate would join the plate to the cabinet behind it: thin dark lines are opened away first
        ko = max(3, min(crop.shape[:2]) // 5)
        opened = ndimage.binary_opening(closed, structure=np.ones((ko, ko)))
        closed = opened if opened.any() else closed
        lab, n = ndimage.label(closed)
        if not n:
            print("  !! no plate found in", (x0, y0, x1, y1)); continue
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        plate = ndimage.binary_fill_holes(lab == (1 + int(np.argmax(sizes))))
        inner = ndimage.binary_erosion(plate, iterations=1)
        base = np.median(gray[plate & dark]) if (plate & dark).any() else 40
        # the lettering: brighter than halfway from the plate to the plate's brightest pixels (a small, soft logo is grey)
        top = np.percentile(gray[inner], 97) if inner.any() else 255
        text = inner & (gray > (base + top) / 2)
        if plate.sum() < 700:                                   # a plate a few pixels high: empty all of it
            mask = inner
        else:
            tl, tn = ndimage.label(text)
            if tn:
                ts = ndimage.sum(np.ones_like(tl), tl, range(1, tn + 1))
                # cabinet showing between a cable and the plate's edge touches the plate's border; the screws are tiny
                ys_, xs_ = np.nonzero(plate)
                big = min(np.ptp(ys_), np.ptp(xs_)) >= 60                 # on a small plate the letters run close to its edge
                band = plate & ~ndimage.binary_erosion(plate, iterations=3)
                edge = set(np.unique(tl[band & (tl > 0)]).tolist()) if big else set()
                keep = [i + 1 for i, s in enumerate(ts) if s >= max(4, 0.03 * ts.max()) and (i + 1) not in edge]
                text = np.isin(tl, keep)
            ys, xs = np.nonzero(text)
            mask = np.zeros_like(text)
            if len(xs) >= 3:
                hull = cv2.convexHull(np.stack([xs, ys], axis=1).astype(np.int32))
                m8 = np.zeros(text.shape, np.uint8)
                cv2.fillConvexPoly(m8, hull, 1)
                mask = ndimage.binary_dilation(m8.astype(bool), iterations=2) & inner
        door = plate.mean() > 0.55                               # the dark area is the door the logo sits on, not a plate
        if door:
            # lettering on a door panel: filled from the panel around it, so its sheen and gradient carry on
            filled = cv2.inpaint(cv2.cvtColor(crop, cv2.COLOR_RGB2BGR), mask.astype(np.uint8) * 255, 5, cv2.INPAINT_TELEA)
            fill = cv2.cvtColor(filled, cv2.COLOR_BGR2RGB).astype(np.float32)
            grain = 1.2
        else:
            # a name plate: its own colour, the median of the plate around the lettering (bright screws and edges left out)
            ring = ndimage.binary_dilation(mask, iterations=4) & ~mask & plate & (gray < (base + 255) / 2 - 10)
            if ring.sum() < 8:
                ring = plate & ~mask & dark
            ref = crop[ring].astype(np.float32)
            fill = np.broadcast_to(np.median(ref, axis=0), crop.shape).astype(np.float32)
            grain = float(np.clip(ref.std(axis=0).mean(), 0, 4)) * 0.4
        paint(out, (x0, y0, x1, y1), mask, fill, grain)
        print(f"  plate {(x0, y0, x1, y1)}: {int(mask.sum())} px painted out" + (" (door panel)" if door else ""))
    return out


def paint(out, box, mask, fill, grain):
    """the fill laid over the mask with a little grain, feathered at its edge"""
    x0, y0, x1, y1 = box
    crop = out[y0:y1, x0:x1].astype(np.float32)
    rng = np.random.default_rng(x0 * 7919 + y0)
    fill = fill + rng.normal(0, grain, crop.shape[:2] + (1,))
    alpha = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 0.8)[..., None]
    out[y0:y1, x0:x1] = np.clip(crop * (1 - alpha) + fill * alpha, 0, 255).astype(np.uint8)


def blank_polygon(out, poly, inset, keep):
    """a plate whose outline the automatic search cannot find (a cable runs along it): its corners given, the plate inside
    them (inset px from the edge, the screws kept) painted with the plate's colour taken from its rim"""
    pts = np.array(poly, np.float32)
    c = pts.mean(axis=0)
    inner_pts = pts + inset * (c - pts) / np.linalg.norm(c - pts, axis=1, keepdims=True)
    x0, y0 = np.floor(pts.min(axis=0)).astype(int) - 4
    x1, y1 = np.ceil(pts.max(axis=0)).astype(int) + 5
    h, w = y1 - y0, x1 - x0
    m8 = np.zeros((h, w), np.uint8)
    cv2.fillPoly(m8, [np.round(inner_pts - [x0, y0]).astype(np.int32)], 1)
    outer = np.zeros((h, w), np.uint8)
    cv2.fillPoly(outer, [np.round(pts - [x0, y0]).astype(np.int32)], 1)
    for (sx, sy) in keep:                                        # the screws stay
        cv2.circle(m8, (int(round(sx - x0)), int(round(sy - y0))), 4, 0, -1)
    mask, rim = m8.astype(bool), outer.astype(bool) & ~m8.astype(bool)
    crop = out[y0:y1, x0:x1]
    gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    ref = crop[rim & (gray < np.percentile(gray[rim], 70))].astype(np.float32)
    fill = np.broadcast_to(np.median(ref, axis=0), crop.shape).astype(np.float32)
    paint(out, (x0, y0, x1, y1), mask, fill, float(np.clip(ref.std(axis=0).mean(), 0, 4)) * 0.4)
    print(f"  plate {tuple(int(v) for v in (x0, y0, x1, y1))}: {int(mask.sum())} px painted out (outline given)")


def retouch(img):
    """img: RGB uint8 → RGB uint8, a light touch"""
    f = img.astype(np.float32) / 255
    # white balance from the bright, nearly grey pixels (white walls, ceiling, floor highlights)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    sel = (hsv[..., 2] > 140) & (hsv[..., 1] < 38) & (hsv[..., 2] < 252)
    if sel.sum() > 2000:
        means = f[sel].mean(axis=0)
        f *= np.clip(means.mean() / means, 0.92, 1.08)
    # levels on the luminance, never stretched hard
    lum = f @ np.array([0.299, 0.587, 0.114], np.float32)
    lo = min(float(np.percentile(lum, 0.3)), 0.06)
    hi = max(float(np.percentile(lum, 99.7)), 0.88)
    f = np.clip((f - lo) / (hi - lo), 0, 1)
    # a dim photo (a warehouse lit from one door) a little brighter: its middle tones lifted toward 0.5, never more than γ 0.8
    mid = float(np.median(f @ np.array([0.299, 0.587, 0.114], np.float32)))
    if mid < 0.45:
        f = f ** max(0.8, np.log(0.5) / np.log(max(mid, 0.05)))
    # local contrast: CLAHE on the lightness, a third of it
    u8 = (f * 255 + 0.5).astype(np.uint8)
    lab = cv2.cvtColor(u8, cv2.COLOR_RGB2LAB)
    cl = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8)).apply(lab[..., 0])
    lab[..., 0] = np.clip(0.67 * lab[..., 0] + 0.33 * cl, 0, 255).astype(np.uint8)
    u8 = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    # vibrance: the muted colours a little stronger, the strong ones left alone
    hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV).astype(np.float32)
    s = hsv[..., 1] / 255
    hsv[..., 1] = np.clip(s + 0.22 * s * (1 - s), 0, 1) * 255
    u8 = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    # fine sharpening
    r = max(0.8, img.shape[1] / 1600)
    blur = cv2.GaussianBlur(u8, (0, 0), r)
    sharp = cv2.addWeighted(u8, 1.55, blur, -0.55, 0)
    return sharp


def main():
    os.makedirs(OUT, exist_ok=True)
    imap = json.load(open(MAP, encoding="utf-8"))
    keys = []
    for key, (src, alt, boxes) in list(PHOTOS.items()) + [(k, (s, a, [])) for k, (s, a) in FACTORY.items()]:
        im = np.asarray(ImageOps.exif_transpose(Image.open(SRC + src)).convert("RGB"))
        print(key, src, im.shape[1], "x", im.shape[0])
        im = blank_plates(im, boxes)
        im = retouch(im) if key not in FACTORY else im          # Dener's own frame stays as it is
        dst = os.path.join(OUT, key + ".jpg")
        Image.fromarray(im).save(dst, quality=93, subsampling=0)
        imap[key] = {"src": os.path.relpath(dst, ROOT), "alt": alt, "section": "site", "trim": False, "quality": 84, "cutout": False}
        keys.append(key)
    json.dump(imap, open(MAP, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("python3 tools/make_images.py --only " + ",".join(keys))


if __name__ == "__main__":
    main()
