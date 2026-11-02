#!/usr/bin/env python3
"""Cut-out of the ULT tube laser studio render (vn-ult-hero-2026.webp) for the NovoTech site.
1. Erase the supplier's logos (green ring logo on the blue cabin face, two embossed "ADH" on the white panel)
   by plane-fitting the flat surface around each spot.
2. Matte: plain white studio background -> transparent; floor haze and the floor seen through the mesh
   fences -> translucent black shadow; the white cutting cabin is protected from the white-background flood.
Usage: python3 -I tools/ult_render_cutout.py tools/src-images/value-laser/vn-ult-hero-2026.webp tools/src-images/cutouts/vn-ult-1-cut.png
(image_map key vn-ult-1 points at the PNG; the mesh fences defeat the automatic white cut)"""
import sys
import numpy as np
import cv2
from PIL import Image

src, out_path = sys.argv[1], sys.argv[2]
img = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W = img.shape[:2]


def plane_fill(a, box, ring=3, sel=None, feather=1.5):
    x0, y0, x1, y1 = box
    X0, Y0, X1, Y1 = x0 - ring, y0 - ring, x1 + ring, y1 + ring
    yy, xx = np.mgrid[Y0:Y1, X0:X1]
    rm = ~((xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1))
    if sel is not None:
        rm &= sel[Y0:Y1, X0:X1]
    A = np.c_[np.ones(rm.sum()), xx[rm], yy[rm]]
    by, bx = np.mgrid[y0:y1, x0:x1]
    fill = np.zeros((y1 - y0, x1 - x0, 3), np.float32)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, a[Y0:Y1, X0:X1, c][rm], rcond=None)
        fill[..., c] = coef[0] + coef[1] * bx + coef[2] * by
    d = np.minimum.reduce([bx - x0 + 1, x1 - bx, by - y0 + 1, y1 - by]).astype(np.float32)
    w = np.clip(d / feather, 0, 1)[..., None]
    a[y0:y1, x0:x1] = w * fill + (1 - w) * a[y0:y1, x0:x1]


mn0 = img.min(-1)
navy = (img[..., 2] > img[..., 0] + 25) & (mn0 < 110)
plane_fill(img, (489, 227, 519, 281), ring=4, sel=navy)          # green ring logo + "ADH MACHINE TOOL"
plane_fill(img, (689, 243, 727, 265), ring=3)                    # embossed ADH, front panel
plane_fill(img, (836, 228, 878, 250), ring=3)                    # embossed ADH, front panel right

mn, mx = img.min(-1), img.max(-1)
neutral = (mx - mn) <= 14


def poly_mask(pts):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.array(pts, np.int32)], 1)
    return m.astype(bool)


cabin = poly_mask([(480, 204), (888, 204), (893, 412), (712, 445), (636, 445), (486, 414)])
fences = poly_mask([(86, 268), (338, 252), (458, 372), (458, 512), (240, 562), (86, 502)]) | \
    poly_mask([(1058, 640), (1522, 466), (1528, 684), (1058, 866)])


def border_cc(mask):
    n, lab = cv2.connectedComponents(mask.astype(np.uint8), connectivity=8)
    b = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(b)) if b else np.zeros_like(mask)


bg = border_cc(neutral & (mn >= 251))                 # only the pure studio white is background
# pure-white openings anywhere outside the cabin (mesh cells, gaps between supports)
n, lab, st, _ = cv2.connectedComponentsWithStats((neutral & (mn >= 251) & ~cabin).astype(np.uint8), connectivity=4)
bg |= (lab > 0) & ~cabin
protect = poly_mask([(1215, 370), (1390, 370), (1390, 530), (1215, 530)]) | poly_mask([(315, 215), (410, 215), (410, 305), (315, 305)])
free = ~cabin & ~protect
# floor: light neutral haze touching the background, everything light inside the fences, blobby light patches low down
light = neutral & (mn >= 205) & ~bg & free
n, lab, st, _ = cv2.connectedComponentsWithStats(light.astype(np.uint8), connectivity=8)
grow = cv2.dilate(bg.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
touch = set(np.unique(lab[grow & light])) - {0}
shadow = np.isin(lab, [i for i in touch if st[i, cv2.CC_STAT_AREA] >= 200]) if touch else np.zeros_like(light)
shadow |= light & fences
for i in range(1, n):
    x, y, w, h, area = st[i]
    if area >= 300 and area / max(w, h) >= 6 and y + h / 2 >= 320:
        shadow |= lab == i
# contact shadows under the supports: smooth neutral grey connected to the floor
sm = cv2.GaussianBlur(mn, (0, 0), 1.5)
grad = np.hypot(cv2.Sobel(sm, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(sm, cv2.CV_32F, 0, 1, ksize=3))
for _ in range(3):
    cand = neutral & (mn >= 55) & (grad < 60) & free & ~bg & ~shadow
    n2, lab2 = cv2.connectedComponents(cand.astype(np.uint8), connectivity=8)
    near = cv2.dilate(shadow.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    t2 = set(np.unique(lab2[near & cand])) - {0}
    if not t2:
        break
    shadow |= np.isin(lab2, list(t2))
# grey rims left around feet and cable ends: neutral grey within 7 px of the floor shadow
dist = cv2.distanceTransform((~(shadow | bg)).astype(np.uint8), cv2.DIST_L2, 3)
shadow |= neutral & (mn >= 90) & (dist <= 7) & free & ~bg
# 2 px band next to the outside: light neutral = floor, the rest = machine edge
k = np.ones((5, 5), np.uint8)
band = (cv2.dilate((bg | shadow).astype(np.uint8), k) > 0) & ~(bg | shadow)
shadow |= band & neutral & (mn > 200) & free
edge = band & ~shadow
alpha = np.ones((H, W), np.float32)
alpha[edge] = np.clip((252.0 - mn[edge]) / (252.0 - 190.0), 0, 1)
op = np.clip((252.0 - mn) / 252.0, 0, 0.85)           # black at this opacity reproduces the floor tone on white
alpha[shadow] = op[shadow]
alpha[bg] = 0.0
alpha = np.clip(cv2.GaussianBlur(alpha, (0, 0), 0.6), 0, 1)
alpha[bg & ~(cv2.dilate((~bg).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)] = 0.0
rgb = img.copy()
sel = edge & (alpha > 0.02) & (alpha < 0.98)
aa = alpha[sel][:, None]
rgb[sel] = np.clip((img[sel] - (1 - aa) * 255.0) / np.maximum(aa, 0.05), 0, 255)
rgb[shadow] = 0.0
res = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
im = Image.fromarray(res, 'RGBA')
bbox = Image.fromarray((alpha * 255).astype(np.uint8)).point(lambda v: 255 if v > 10 else 0).getbbox()
m = 6
im = im.crop((max(0, bbox[0] - m), max(0, bbox[1] - m), min(W, bbox[2] + m), min(H, bbox[3] + m)))
im.save(out_path)
print(out_path, im.size)
