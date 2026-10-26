#!/usr/bin/env python3
"""CSM (Chiao Sheng Machinery, Taiwan) photos: the website renders (/home/claude/csm/img/*.jpg, downloaded Oct 24 from
tubebender.com.tw — numbered callout bubbles are painted out) and crops from the two catalogue PDFs, which are full-page
JPEG rasters at 180 dpi (/home/claude/csm/img/E-nnn.png = electric catalogue, H-nnn.png = hydraulic catalogue; pdfimages).
Written to tools/src-images/csm/<key>.jpg; the site pipeline (tools/make_images.py) cuts the machine photos out (BiRefNet).

    pdfimages -png /mnt/user-data/attachments/…/0fe06f93-electric.pdf /home/claude/csm/img/E
    pdfimages -png /mnt/user-data/attachments/…/06fd971f-hydraulic.pdf /home/claude/csm/img/H
    python3 tools/csm_photos.py [key ...]      then   python3 tools/make_images.py --only $(cat tools/csm_keys.txt)
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "csm")
P = "/home/claude/csm/img/"
MAX_SIDE = 2600


def W(name, alt, **kw):
    """website photo (machine on white) — cut out; callouts=True erases the numbered bubbles"""
    return dict(src=P + name, alt=alt, **{"cutout": True, **kw})


def C(page, crop, alt, **kw):
    """crop from a catalogue page raster (1822 × 1290 px); up=True → Real-ESRGAN 2x"""
    return dict(src=P + page + ".png", crop=crop, alt=alt, **{"cutout": True, "up": True, **kw})


# key: dict(src, alt, crop, fill=[boxes painted white], inpaint=[boxes LaMa-filled], callouts=True | "inpaint", trace, cutout, up)
PHOTOS = {
    # ---- CNC all-electric (website renders: the Small_ versions carry no callout bubbles) ---------------------------
    "cs-emr": W("Small_EMR.jpg", "CSM 45 EMR all-electric CNC tube bender with left- and right-hand bending head"),
    "cs-emr-15": C("E-004", (130, 430, 500, 720), "15 EMB all-electric CNC bender for brake and fuel line to Ø19/32″", fill=[(420, 425, 500, 515)]),
    "cs-emr-45": C("E-004", (130, 720, 500, 940), "30 – 45 EMR all-electric CNC bender with roll-bending head"),
    "cs-emr-75": C("E-004", (90, 955, 536, 1195), "75 EMR all-electric CNC bender for Ø3″ automotive and transportation tube", fill=[(526, 1100, 560, 1195)]),
    "cs-emr-parts-small": C("E-004", (530, 508, 830, 700), "Brake lines, fuel lines and air-conditioning tube bent on the 15 – 20 EMB", cutout=False),
    "cs-emr-parts-mid": C("E-004", (550, 798, 830, 940), "Furniture and health-care tube frame bent on the 30 – 45 EMR", cutout=False),
    "cs-emr-parts-large": C("E-004", (540, 1015, 860, 1170), "Automotive exhaust tube bent on the 75 EMR", cutout=False),
    "cs-mre2": W("Small_80MRE2-RBE-1.jpg", "CSM 80 MRE2-RBE all-electric CNC tube bender with servo rear booster"),
    "cs-mre2-50": C("E-005", (95, 415, 615, 745), "50 MRE2-RBE all-electric CNC bender"),
    "cs-mre2-100": C("E-005", (95, 820, 615, 1150), "100 MRE2-RBE all-electric CNC bender for Ø4″ tube"),
    "cs-mre2-parts": C("E-005", (680, 495, 875, 760), "Multi-plane furniture and health-care tube bent on the 50 MRE2-RBE", cutout=False),
    "cs-mre2-parts-large": C("E-005", (636, 910, 912, 1145), "Automotive tube bent on the 80 – 100 MRE2-RBE", cutout=False),
    # ---- CNC electric hybrid ---------------------------------------------------------------------------------------
    "cs-mbe": W("Small_MBE.jpg", "CSM MBE electric-hybrid CNC tube bender with three stacked tools"),
    "cs-mbe-parts": C("E-006", (585, 960, 825, 1215), "Stainless exhaust manifold bent on the 80 – 150 MBE / MRE", cutout=False),
    "cs-mbe-parts-2": C("E-006", (85, 940, 330, 1185), "HVAC and fuel-line tube bent on the 18 – 25 MBE", fill=[(205, 932, 300, 957), (288, 1122, 340, 1155)], cutout=False),
    "cs-tbre": W("Small_TBRE_TMRE-1.jpg", "CSM TMRE electric-hybrid CNC tube bender with three stacked tools and roll-bending head"),
    "cs-tbre-parts": C("E-007", (100, 836, 382, 966), "Serpentine HVAC tube bent on the 18 – 25 TBRE", inpaint=[(334, 838, 382, 874), (300, 946, 382, 966)],
                       inpaint_mode="telea", cutout=False),
    "cs-tbre-parts-2": C("E-007", (470, 866, 905, 1156), "Automotive tube frame bent on the 80 – 130 TBRE",
                         inpaint=[(540, 968, 772, 996), (650, 994, 806, 1022), (455, 1022, 492, 1090), (470, 1098, 562, 1156), (466, 866, 525, 898)], cutout=False),
    "cs-tdre": W("Small_65TDRE-1.jpg", "CSM 65 TDRE electric-hybrid CNC tube bender with two stacked tools"),
    "cs-tdre-parts": C("E-008", (515, 990, 906, 1230), "Rounded automotive frame bent on the 80 – 130 TDRE",
                       fill=[(515, 990, 612, 1010), (515, 1005, 552, 1024), (570, 1073, 836, 1135)], cutout=False),
    "cs-tdre-parts-2": C("E-008", (265, 822, 612, 1020), "Rectangular frame with handle bent on the 12 – 25 TDRE",
                         fill=[(538, 822, 612, 858), (262, 958, 300, 1022), (560, 1006, 612, 1022)], cutout=False),
    # ---- CNC hydraulic / NC hydraulic ------------------------------------------------------------------------------
    "cs-tsr": W("Small_TSR_TDR.jpg", "CSM TSR hydraulic CNC pipe bender"),
    "cs-tsr-parts": C("H-004", (650, 1000, 905, 1240), "Large pipe elbows bent on the 150 – 220 TSR for shipyard, oil-rig and water-supply work",
                      fill=[(648, 1060, 685, 1116)], cutout=False),
    "cs-tsr-parts-2": C("H-004", (100, 905, 428, 1112), "Furniture and automotive U-bends bent on the 38 – 65 TSR",
                        fill=[(354, 926, 430, 958), (390, 1033, 430, 1070), (338, 1084, 430, 1114)], cutout=False),
    "cs-tsr-parts-3": C("H-004", (82, 1078, 524, 1252), "Boiler and construction tube bent on the 80 – 120 TSR",
                        fill=[(140, 1076, 292, 1113), (503, 1062, 526, 1122)], cutout=False),
    "cs-tsrj": C("H-005", (880, 650, 1630, 1230), "CSM TSRJ NC hydraulic tube bender with servo carriage", callouts=True,
                 trace=[[(1426, 902), (1531, 902)]]),
    "cs-tsrj-carriage": C("H-005", (855, 297, 1121, 450), "Servo carriage of the TSRJ / TDRJ", cutout=False),
    "cs-tncpb": W("Small_TNCPB.jpg", "CSM 100 TNCPB NC hydraulic tube bender with manual feeding"),
    "cs-tncb": W("Small_TNCB.jpg", "CSM TNCB single-axis NC hydraulic pipe bender"),
    "cs-tncb-parts": C("H-006", (508, 760, 878, 1066), "Large pipe elbows bent on the 150 – 220 TNCB", fill=[(795, 1004, 880, 1068)], cutout=False),
    "cs-tncb-parts-2": C("H-006", (100, 632, 345, 790), "Exhaust pipes with flex sections bent on the 38 – 50 TNCB", fill=[(254, 755, 470, 810)], cutout=False),
    # ---- symmetric benders -----------------------------------------------------------------------------------------
    "cs-f38": C("H-008", (150, 445, 790, 960), "F38 single-axis symmetric bender — two heads bend both ends of the tube at once", callouts=True),
    "cs-f38h": W("Symmetric-1.jpg", "CSM F38H-5A multi-axis symmetric tube bender with servo feeding", callouts=True),
    # ---- end forming -----------------------------------------------------------------------------------------------
    "cs-ef30": W("EF30-6-01.jpg", "CSM EF 30-6 six-station tube end forming machine"),
    "cs-ef30-tools": W("EF30-6-02.jpg", "Six forming stations of the EF end former", cutout=False),
    "cs-ref40": W("REF40-2.jpg", "CSM REF 40 tube grooving machine"),
    "cs-ref20": W("REF20.jpg", "Rotary grooving head of the CSM REF machine", cutout=False),
    "cs-er30": W("ER30-5.jpg", "CSM ER 30-5 complex end-finishing machine: end forming, chamfering and grooving in one"),
    "cs-end-finishing": W("end-finishing.jpg", "ER 30-5 head forming, chamfering and grooving a tube end", crop=(0, 90, 1140, 841), cutout=False),
    "cs-ref-part": C("H-009", (825, 830, 1125, 1105), "Tube end formed, chamfered and grooved on the ER 30-5", callouts="inpaint", cutout=False),
    # ---- circular sawing -------------------------------------------------------------------------------------------
    "cs-ct325": C("H-010", (125, 600, 712, 1190), "CT325 hydraulic circular saw with servo feed, PLC and pedestal control", callouts=True,
                  trace=[[(544, 688), (544, 818)], [(620, 792), (712, 792)]]),
    "cs-ct325-bundle": W("9V001.jpg", "Bundle-cutting vise of the CT325 — nine tubes cut at once", cutout=False),
    "cs-ct325-parts": W("001.jpg", "Round, square, rectangular and angle sections cut on the CT325", cutout=False),
    # ---- wire bending ----------------------------------------------------------------------------------------------
    "cs-wb10": W("WB10-A.jpg", "CSM WB 10-A CNC wire bending machine with decoiler, straightener and servo bending head", callouts=True, fill=[(60, 690, 350, 965)]),
    "cs-wb-line": C("E-009", (760, 985, 1710, 1185), "WB wire bending line layout — decoiler, straightener, feeder and bending head", cutout=False),
    "cs-wb-screen": C("E-009", (280, 960, 585, 1195), "IPC control with 3D simulation of the wire bending machine", cutout=False),
}


CATALOGUE_CALLOUT = dict(color=(0, 155, 228), tol=40, bubble=(12, 26), ink="cyan")   # cyan bubbles ~18 px, dots every 10 px


def callout_masks(im, color=(73, 143, 228), tol=22, bubble=None, ink="tint"):
    """Masks of the numbered callout bubbles, their dotted / dashed leader lines and arrow heads.

    bg  = callout pixels over the white background (painted white),
    inp = callout pixels over the machine (LaMa-inpainted).
    A bubble is a flat disc of the callout colour with a white digit inside; its size range defaults to 0.8 – 5 % of
    the image width (website renders) or is given in px (catalogue crops).  Leader lines are the callout-coloured
    pixels connected to a bubble; arrow heads / end dots are compact blobs just beyond a leader's end.  Anything not
    connected to a bubble is left alone, so the machines' own blue paint, stickers and reflections are never touched."""
    import numpy as np
    from scipy import ndimage
    a = np.asarray(im).astype(int)
    W_ = a.shape[1]
    lo, hi = bubble or (0.008 * W_, 0.05 * W_)
    k = 1 if bubble else max(1.0, W_ / 1440)                    # drawing scale (dot spacing, line width)
    win = max(15, round(15 * k)); link = max(3, round((5 if bubble else 3) * k)); grow = max(2, round(2 * k))
    hsv = np.asarray(im.convert("HSV")).astype(int)
    flat = np.abs(a - np.array(color)).max(axis=2) <= tol
    for c in ((62, 122, 198), (33, 98, 188)):                                # arrow heads and the dashes next to them
        flat |= np.abs(a - np.array(c)).max(axis=2) <= 28
    bluish = (hsv[..., 0] >= 120) & (hsv[..., 0] <= 185) & (hsv[..., 1] >= 35) & (hsv[..., 2] >= 120)
    bluish_wide = ndimage.uniform_filter(bluish.astype(float), win)
    if ink == "cyan":      # catalogue: cyan dots, blended with whatever they are printed over (white, yellow, black)
        tint = ((a[..., 1] - a[..., 0]) >= 50) & ((a[..., 2] - a[..., 0]) >= 40) & (a[..., 2] >= 100)
    else:                  # website renders: semi-transparent blue dashes over white
        tint = ((a[..., 2] - a[..., 0]) >= 18) & (a[..., 2] >= 160)
    white = a.min(axis=2) >= 238
    bub_bg = np.zeros(flat.shape, bool); bub_inp = bub_bg.copy(); dots = bub_bg.copy()
    lab, n = ndimage.label(flat); objs = ndimage.find_objects(lab)
    pad = max(3, round(0.12 * lo))
    for i, sl in enumerate(objs, 1):
        blob = lab[sl] == i; h, w = blob.shape; sz = blob.sum()
        box = (slice(max(0, sl[0].start - pad), sl[0].stop + pad), slice(max(0, sl[1].start - pad), sl[1].stop + pad))
        if lo <= w <= hi and lo <= h <= hi and abs(w - h) <= 0.15 * max(w, h) and sz >= 0.55 * w * h:
            c = max(1, round(0.16 * w))
            corners = np.concatenate([blob[:c, :c].ravel(), blob[:c, -c:].ravel(), blob[-c:, :c].ravel(), blob[-c:, -c:].ravel()])
            inner = a[sl][round(0.25 * h):round(0.75 * h), round(0.25 * w):round(0.75 * w)]
            digit = (inner.min(axis=2) >= 190).mean()
            if corners.mean() < 0.2 and 0.04 <= digit <= 0.6:                 # a numbered bubble
                ring = np.ones(white[box].shape, bool); ring[pad:-pad, pad:-pad] = False
                (bub_bg if white[box][ring].mean() > 0.5 else bub_inp)[box] = True
                continue
        if max(w, h) <= 3 * lo and sz <= 1.2 * lo * lo:                       # dot / arrow head: an isolated blue mark
            r = max(4, round(0.4 * lo))
            Y0, X0 = max(0, sl[0].start - r), max(0, sl[1].start - r)
            loc = lab[Y0:sl[0].stop + r, X0:sl[1].stop + r] == i
            ring = ndimage.binary_dilation(loc, iterations=r) & ~ndimage.binary_dilation(loc, iterations=1)
            # the catalogue's cyan is unlike any machine paint, so a cyan end dot may sit on a blue part
            if bubble or bluish[Y0:sl[0].stop + r, X0:sl[1].stop + r][ring].mean() < 0.15:
                dots[Y0:sl[0].stop + r, X0:sl[1].stop + r] |= loc
    bub = bub_bg | bub_inp
    bluish_wide = ndimage.uniform_filter((bluish & ~bub).astype(float), win)   # a bubble does not shield its own leader
    raw = (tint | flat) & (bluish_wide < 0.25)
    lab, n = ndimage.label(ndimage.binary_dilation(raw, iterations=link) | ndimage.binary_dilation(bub, iterations=max(2, round(0.5 * lo))))
    keep = np.unique(lab[bub]); keep = keep[keep > 0]
    lines_raw = raw & np.isin(lab, keep) & ~bub
    near = ndimage.binary_dilation(lines_raw | bub, iterations=max(3, round(1.2 * lo)))
    dl, _ = ndimage.label(dots)
    ends = np.isin(dl, np.unique(dl[near & dots])) & dots & (dl > 0) & ~bub
    marks = lines_raw | ends
    lines = ndimage.binary_dilation(marks, iterations=grow) & ~bub
    cl = ndimage.binary_dilation(marks | bub, iterations=grow)
    num = ndimage.uniform_filter((white & ~cl).astype(float), win)      # white share of what surrounds the callout
    den = ndimage.uniform_filter((~cl).astype(float), win)
    wfrac = np.where(den > 0.05, num / np.maximum(den, 1e-6), 1.0)
    bg = bub_bg | (lines & (wfrac >= 0.6))
    inp = bub_inp | (lines & (wfrac < 0.6))
    bg = ndimage.binary_dilation(bg, iterations=1)
    inp &= ~bg
    return bg, inp


def decallout(im, paint=True, trace=(), **kw):
    """Erase the callouts found by callout_masks: white over the background, LaMa over the machine.
    paint=False inpaints everything (photos on a tinted background); trace = extra polylines [(x, y), ...] to inpaint
    (leader lines the colour test cannot follow, e.g. cyan dots printed over yellow)."""
    import numpy as np
    bg, inp = callout_masks(im, **kw)
    if not paint:
        inp |= bg; bg[:] = False
    if trace:
        m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
        for line in trace:
            d.line(line, fill=255, width=9)
            for x, y in line[:1] + line[-1:]:
                d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=255)
        inp |= np.asarray(m) > 0
        inp &= ~bg
    out = np.asarray(im).copy(); out[bg] = 255
    if inp.any():
        from lama_inpaint import inpaint
        out = inpaint(out, (inp * 255).astype(np.uint8))
    return Image.fromarray(out)


def inpaint_boxes(im, boxes, mode="lama"):
    """Fill boxes (catalogue labels printed over a tinted background): LaMa, or mode="telea" (OpenCV) for a plain gradient
    at the image border, where LaMa tends to invent texture"""
    import numpy as np
    m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
    for r in boxes:
        d.rectangle(r, fill=255)
    if mode == "telea":
        import cv2
        return Image.fromarray(cv2.inpaint(np.asarray(im), np.asarray(m), 9, cv2.INPAINT_TELEA))
    from lama_inpaint import inpaint
    return Image.fromarray(inpaint(np.asarray(im), np.asarray(m)))


def process(key, spec):
    im = Image.open(spec["src"]).convert("RGB")
    catalogue = spec["src"].endswith(".png")
    if spec.get("fill"):
        d = ImageDraw.Draw(im)
        for r in spec["fill"]:
            d.rectangle(r, fill=(255, 255, 255))
    if spec.get("inpaint") and not spec.get("crop"):
        im = inpaint_boxes(im, spec["inpaint"])
    co = spec.get("callouts")
    opts = dict(paint=co != "inpaint")
    if co and not catalogue:
        im = decallout(im, trace=spec.get("trace", ()), **opts)
        if spec.get("crop"):
            im = im.crop(spec["crop"])
    elif co:          # catalogue page: detect on the crop plus a margin, so bubbles just outside it seed their leaders
        x0, y0, x1, y1 = spec["crop"]; m = 80
        X0, Y0, X1, Y1 = max(0, x0 - m), max(0, y0 - m), min(im.width, x1 + m), min(im.height, y1 + m)
        trace = [[(x - X0, y - Y0) for x, y in line] for line in spec.get("trace", ())]
        im = decallout(im.crop((X0, Y0, X1, Y1)), trace=trace, **opts, **CATALOGUE_CALLOUT)
        im = im.crop((x0 - X0, y0 - Y0, x1 - X0, y1 - Y0))
    elif spec.get("crop"):
        im = im.crop(spec["crop"])
    if spec.get("inpaint") and spec.get("crop"):
        # LaMa on the crop only: on the full page it would continue the label text / the neighbouring part into the hole
        x0, y0 = spec["crop"][:2]
        im = inpaint_boxes(im, [(a - x0, b - y0, c - x0, d - y0) for a, b, c, d in spec["inpaint"]], spec.get("inpaint_mode", "lama"))
    if spec.get("up"):
        from esrgan import upscale
        im = upscale(im)
    s = MAX_SIDE / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    os.makedirs(DST, exist_ok=True)
    out = os.path.join(DST, key + ".jpg")
    im.save(out, quality=92)
    return out, im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for key in keys:
        out, size = process(key, PHOTOS[key])
        print(f"{key:22s} {size} -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
