#!/usr/bin/env python3
"""Photos of the NovoTech value-line machines from TTMC's 2026 new-item sheets and catalogues (tools/ttmc_new_tables.py) —
crops from the owner's attachments in /home/claude/ttmc-new (sheet rasters 1,900 – 2,500 px wide, and the photos embedded in
the welding and woodworking PDFs).  The supplier's logo on a machine is painted over with the colour around it, captions and
leader lines are painted white or removed with ttmc_more_photos.clean_marks; product photos are cut out later by
tools/make_images.py (BiRefNet), detail photos (DETAIL) keep their background.

    python3 tools/ttmc_new_photos.py [key …]      → tools/src-images/ttmc-more/<key>.jpg
"""
import io
import os
import sys

import numpy as np
from PIL import Image

import ttmc_more_photos as P

SRC = "/home/claude/ttmc-new/"
NI, BR = SRC + "new_items_rar/", SRC + "brochure_rar/"
BEND, SAW, WELD = NI + "折弯类/", NI + "锯床类/", NI + "焊接变位机或旋转台/"
PDF_A, PDF_B = SRC + "pdf_a/a.pdf", SRC + "pdf_b/b.pdf"
TFM_PDF = BR + "TFM3100x2E TFMS3100X2E.pdf"
DST = P.DST


def S(src, box=None, alt="", white=(), logo=(), clean=False, detail=False, xref=None, logo_out=(), lines=()):
    """src: an image file, or a PDF with xref; box: crop (x0, y0, x1, y1) in source pixels, None = whole image;
    white / logo: boxes (x0, y0, x1, y1) in source pixels painted white / filled from the surface around the badge;
    logo_out: badge boxes in the pixels of the finished (cropped and trimmed) photo, padded by PAD;
    lines: thin frame or dash lines of the catalogue layout on the finished photo, ("h", y0, y1) or ("v", x0, x1) —
    erased wherever there is white on both sides of the line (not where the machine crosses it)"""
    return dict(src=src, xref=xref, box=box, alt=alt, white=list(white), logo=list(logo), clean=clean, detail=detail,
                logo_out=list(logo_out), lines=list(lines))


def erase_lines(im, lines):
    a = np.asarray(im).copy()
    h, w = a.shape[:2]
    white = a.min(axis=2) > 235
    for kind, u0, u1 in lines:
        if kind == "h":
            side = white[max(0, u0 - 3)] & white[min(h - 1, u1 + 3)]
            a[u0:u1 + 1, side] = 255
        else:
            side = white[:, max(0, u0 - 3)] & white[:, min(w - 1, u1 + 3)]
            a[side, u0:u1 + 1] = 255
    return Image.fromarray(a)


PAD = 4
SMALL = 520         # px, longest side: below it the finished photo is upscaled (the gallery shows photos ~560 px wide)


PHOTOS = {
    # ------------------------------------------------------------------------------------------- sheet metal brakes
    "tm-w2540h2": S(BEND + "W2.0x2540H.jpg", (185, 290, 2335, 1705), "W2.0×2540H heavy pan and box brake with extended fingers and counterweight",
                    white=[(140, 1650, 1450, 1710)], clean=True),
    "tm-w2540h2-gauge": S(BEND + "W2.0x2540H.jpg", (1851, 2125, 2392, 2483), "Digital angle gauge on the bending leaf", detail=True,
                          logo_out=[(178, 95, 314, 118)]),
    "tm-w2540h2-fingers": S(BEND + "W2.0x2540H.jpg", (707, 2126, 1249, 2482), "Ground segmented fingers of the heavy pan and box brake", detail=True),
    "tm-hw2540h": S(BEND + "HW2.0x2540H.jpg", (140, 280, 2390, 1436), "HW2.0×2540H hydraulic pan and box brake with NC control pedestal and foot pedal",
                    clean=True),
    "tm-hw2540h-panel": S(BEND + "HW2.0x2540H.jpg", (710, 1868, 1251, 2224), "NC control panel: open height, bending angle and dwell time", detail=True),
    "tm-bsm3150": S(BEND + "BSM3150.jpg", (150, 380, 2330, 1095), "BSM3150 shear and brake machine on its mobile stand", clean=True,
                    white=[(370, 770, 732, 800), (370, 770, 412, 1100)]),
    "tm-bsm3150-head": S(BEND + "BSM3150.jpg", (767, 1160, 1522, 1703), "Slitter head of the shear and brake machine", detail=True),
    "tm-efms2540l": S(BEND + "EFMS-2540X1.5L.png", (40, 320, 1860, 965), "EFMS-2540×1.5L electric folding machine with segmented beams and foot pedals",
                      clean=True),
    "tm-efms2540l-angle": S(BEND + "EFMS-2540X1.5L.png", (1436, 1081, 1840, 1414), "Bending angle setting dial", detail=True),
    "tm-tfm3100": S(BR + "TFM3100X2E.jpg", (125, 265, 2362, 1360), "TFM 3100×2E CNC electric folding machine with touch-screen control",
                    white=[(380, 1180, 1060, 1290)], logo=[(780, 555, 1065, 652)], clean=True),
    "tm-tfm-screen": S(BR + "TFM3100X2E.jpg", (1834, 1629, 2365, 1989), "Touch-screen CNC of the folding machine", detail=True),
    "tm-tfm-table": S(BR + "TFM3100X2E.jpg", (110, 1630, 909, 1989), "CNC back gauge table with fingers", detail=True),
    "tm-tfms3100": S(TFM_PDF, (130, 300, 2426, 1298), "TFMS 3100×2E CNC electric folding machine with segmented upper beam", xref=53, clean=True, logo_out=[(838, 285, 1022, 338)]),
    "tm-tfms-box": S(TFM_PDF, (1815, 1361, 2403, 1773), "Box folded on the segmented folding machine", xref=53, detail=True),
    "tm-tfms-segments": S(TFM_PDF, (1192, 1361, 1798, 1773), "Segmented upper beam", xref=53, detail=True),
    "tm-hbv1250": S(BEND + "HBV-1250.jpg", (255, 335, 2272, 1536), "HBV-1250 hydraulic press brake with two cylinders and foot pedal",
                    white=[(360, 1420, 880, 1545)], clean=True),
    "tm-hbv1250-gauge": S(BEND + "HBV-1250.jpg", (1876, 1610, 2392, 2117), "Back gauge hand wheel with counter", detail=True),
    "tm-cd24": S(BR + "WhatsApp Image 2026-07-20 at 5.20.20 AM.jpeg", (488, 147, 1133, 867), "CD-24 coil dispenser on its folding stand", clean=True),
    "tm-cd24-coil": S(BR + "WhatsApp Image 2026-07-20 at 5.20.20 AM.jpeg", (50, 460, 384, 720), "Trim coil on the CD-24 next to a portable brake",
                      detail=True),
    # ------------------------------------------------------------------------------------------- shears, saws, stands
    "tm-ps1220": S(BR + "WhatsApp Image 2026-01-26 at 7.24.57 PM.jpeg", (40, 130, 755, 620), "PS-1220×1.5GT coil slitting and cut-to-length machine",
                   white=[(70, 515, 370, 575)], clean=True),
    "tm-ps1220-line": S(BR + "WhatsApp Image 2026-01-26 at 7.24.57 PM.jpeg", (855, 98, 1530, 437), "Slitting machine with the decoiler and the outfeed table",
                        clean=True),
    "tm-ps1220-slit": S(BR + "WhatsApp Image 2026-01-26 at 7.24.57 PM.jpeg", (1085, 453, 1314, 612), "Coil slit into strips", detail=True),
    "tm-qcs500a": S(SAW + "QCS-500A.jpg", (1240, 388, 2358, 1978), "QCS-500A aluminum cut-off saw with 20″ blade and pneumatic clamping", clean=True),
    "tm-qcs500a-vise": S(SAW + "QCS-500A.jpg", (161, 390, 934, 1137), "Pneumatic vise, swivel scale and control panel of the QCS-500A", detail=True),
    "tm-rb3653000d": S(SAW + "RB365x3000D.jpg", (100, 320, 1798, 1106), "RB365×3000D roller conveyor with digital length stop",
                       white=[(585, 1030, 1045, 1095), (1160, 950, 1680, 1010)], clean=True),
    "tm-rb3653000d-stop": S(SAW + "RB365x3000D.jpg", (1104, 1226, 1715, 1624), "Length stop with digital display", detail=True),
    "tm-srb3202000d": S(SAW + "SRB-320X2000D.jpg", (128, 332, 2404, 1750), "SRB-320×2000D roller stand with vertical side rollers", clean=True, logo_out=[(1318, 485, 1468, 560)]),
    # ------------------------------------------------------------------------------------------- deburring, milling, presses
    "tm-mgm300": S(NI + "MGM300.jpg", (112, 250, 1032, 1592), "MGM-300 finishing and deburring machine, 12″ working width", clean=True),
    "tm-mgm300-conveyor": S(NI + "MGM300.jpg", (1231, 1218, 1799, 1592), "Conveyor drive and abrasive belt of the MGM-300", detail=True),
    "tm-ksm850": S(NI + "KSM-850.jpg", (590, 295, 1900, 1478), "KSM-850 cylinder head and block resurfacing machine", clean=True, logo_out=[(690, 573, 811, 626)]),
    "tm-ksm850-panel": S(NI + "KSM-850.jpg", (133, 1939, 674, 2295), "Control panel with variable head and table speeds", detail=True),
    "tm-x6336b": S(NI + "X6336.jpg", (1100, 318, 2264, 1696), "X6336 turret milling machine with power feed and digital readout", clean=True),
    "tm-x6336-dro": S(NI + "X6336.jpg", (277, 407, 945, 1185), "Three-axis digital readout and feed controls of the X6336", detail=True),
    "tm-hp150f1plc": S(NI + "HP-150F1-PLC.jpg", (535, 310, 1921, 2271), "HP-150F1/PLC four-column hydraulic press with PLC cabinet",
                       white=[(1600, 650, 2270, 770)], clean=True, logo_out=[(257, 275, 393, 333)]),
    "tm-hp63c2": S(NI + "C type hydraulic press.jpg", (394, 334, 1341, 2036), "HP-63C C-frame hydraulic press with guard doors", clean=True),
    "tm-hp30c2": S(NI + "C type hydraulic press.jpg", (1516, 489, 2310, 2033), "HP-30C C-frame hydraulic press with foot pedal", clean=True),
    # ------------------------------------------------------------------------------------------- welding positioners (2026 sheets)
    "tm-mrt15": S(WELD + "MRT-15.jpg", (108, 382, 1729, 1345), "MRT-15 multi-function rotary table with control box and foot pedal", clean=True),
    "tm-mrt15-v": S(WELD + "MRT-15.jpg", (1784, 475, 2369, 1252), "MRT-15 in the vertical position", clean=True),
    "tm-wp30t": S(WELD + "WP-30T.jpg", (362, 239, 1631, 1223), "WP-30T benchtop welding positioner with foot pedal", clean=True),
    "tm-wp30t-chuck": S(WELD + "WP-30T.jpg", (1396, 1232, 1829, 1545), "Chuck on the WP-30T table (optional)", detail=True),
    "tm-wp50": S(WELD + "WP-50.jpg", (76, 238, 1099, 1098), "WP-50 benchtop welding positioner with 3-jaw chuck and digital speed display", clean=True),
    "tm-wp50-gas": S(WELD + "WP-50.jpg", (989, 1102, 1400, 1415), "Gas inlet port for purging through the centre", detail=True),
    "tm-wp100t": S(BR + "WP-100T.jpg", (166, 310, 1722, 1380), "WP-100T benchtop welding positioner with 8″ chuck", clean=True),
    "tm-wp100t-h": S(BR + "WP-100T.jpg", (1635, 1429, 2326, 1977), "WP-100T in the horizontal position", clean=True),
    "tm-wp110": S(BR + "WP110T.jpg", (95, 413, 1145, 1306), "WP-110 welding positioner with 8″ chuck and foot pedal", clean=True),
    "tm-wp110t": S(BR + "WP110T.jpg", (1257, 414, 2373, 1226), "WP-110T welding positioner with hollow chuck", clean=True),
    "tm-wp110-panel": S(BR + "WP110T.jpg", (1396, 1514, 2333, 2045), "Control panel: speed, foot pedal and auto mode, forward and reverse", detail=True),
    "tm-wp1000": S(BR + "WP-1000 2000 3000.jpg", (275, 240, 1009, 860), "WP-1000 welding positioner with power tilt", clean=True, logo_out=[(439, 272, 521, 305)]),
    "tm-wp2000": S(BR + "WP-1000 2000 3000.jpg", (291, 988, 971, 1647), "WP-2000 welding positioner with power tilt", clean=True, logo_out=[(119, 236, 159, 271)]),
    "tm-wp3000": S(BR + "WP-1000 2000 3000.jpg", (1413, 227, 2264, 884), "WP-3000 welding positioner, 8,818 lb", clean=True, logo_out=[(300, 338, 388, 372)]),
    "tm-wp-heavy-box": S(BR + "WP-1000 2000 3000.jpg", (1995, 936, 2384, 1218), "Control box of the heavy positioners", detail=True),
    # ------------------------------------------------------------------------------------------- welding positioners and supports (pdf_a)
    "tm-wp220": S(PDF_A, None, "WP-220 tilting welding positioner with foot pedal", xref=47, clean=True),
    "tm-wp350": S(PDF_A, None, "WP-350 tilting welding positioner", xref=51, clean=True),
    "tm-wp-sample": S(PDF_A, None, "Pipe welded on a positioner", xref=43, detail=True),
    "tm-wp500": S(PDF_A, None, "WP-500 welding positioner with motorized tilt", xref=68, clean=True),
    "tm-wp500t": S(PDF_A, None, "WP-500T welding positioner with Ø6-11/16″ hollow chuck", xref=58, clean=True),
    "tm-wp500-panel": S(PDF_A, None, "Control panel: table rotation, tilt and speed", xref=62, detail=True),
    "tm-wpc": S(PDF_A, None, "WPC 3-jaw welding chuck", xref=313, clean=True),
    "tm-wgs": S(PDF_A, None, "Welding torch holder on a positioner", xref=334, clean=True),
    "tm-trs1000": S(PDF_A, None, "TRS1000 welding turning rolls — drive and idler with control box and foot pedal", xref=133, clean=True),
    "tm-trs-pipe": S(PDF_A, None, "Pipe on welding turning rolls", xref=141, clean=True),
    "tm-trs2200": S(PDF_A, None, "TRS2200 welding turning rolls", xref=145, clean=True),
    "tm-trs5000": S(PDF_A, None, "TRS5000 welding turning rolls with steel base", xref=149, clean=True),
    "tm-wtr": S(PDF_A, None, "Outboard support stand with screw height adjustment", xref=159, clean=True),
    "tm-mr3000a": S(PDF_A, None, "MR3000A pipe stand with double height adjustment", xref=178, clean=True),
    "tm-mr7000d": S(PDF_A, None, "MR7000D pipe stand with three-point legs", xref=194, clean=True),
    "tm-mh5500": S(PDF_A, None, "MH5500 pipe support", xref=182, clean=True),
    "tm-pjv": S(PDF_A, None, "Folding pipe jack with V-head", xref=240, clean=True, lines=[("v", 9, 11), ("h", 53, 56), ("h", 460, 463)]),
    "tm-ptr185": S(PDF_A, None, "PTR-185 low pipe roller stand", xref=295, clean=True),
    "tm-wt3624": S(PDF_A, None, "WT-36X24 mobile welding table with CNC hole pattern and drop-down tray", xref=446, clean=True),
    "tm-wt-notcher": S(PDF_A, None, "Tube notcher and fixtures on the welding table", xref=434, detail=True),
    "tm-mdt4840": S(PDF_A, None, "MDT-4840 downdraft table with three-stage filtration", xref=393, clean=True),
    "tm-mdt6137": S(PDF_A, None, "MDT-6137 downdraft table", xref=405, clean=True),
    "tm-mdt6022": S(PDF_A, None, "MDT-6022 downdraft grinding table", xref=422, clean=True),
    "tm-mdt-filter": S(PDF_A, None, "Cartridge filter of the downdraft table", xref=399, detail=True),
    # ------------------------------------------------------------------------------------------- woodworking (pdf_b)
    "tm-wm2000": S(PDF_B, None, "WM2000 multifunction woodworking machine — planer and saw", xref=11, clean=True),
    "tm-wm2500e": S(PDF_B, None, "WM2500E multifunction woodworking machine", xref=23, clean=True),
    "tm-wm2200": S(PDF_B, None, "WM2200 multifunction woodworking machine set up as a table saw", xref=34, clean=True),
    "tm-wm2200r": S(PDF_B, None, "WM2200R multifunction machine with thicknesser on its legs", xref=38, clean=True),
    "tm-wm-planing": S(PDF_B, None, "Edge planing with the clamping device", xref=316, detail=True),
    "tm-wm-drilling": S(PDF_B, None, "Drilling on the milling and drilling table", xref=325, detail=True),
    "tm-wj876": S(PDF_B, None, "WJ-8x76 8″ jointer with spiral cutterhead on cabinet stand", xref=47, clean=True),
    "tm-wj-cutterhead": S(PDF_B, None, "Spiral cutterhead with indexable carbide inserts", xref=55, detail=True),
    "tm-wj1040": S(PDF_B, None, "WJ10X40 10″ surface planer", xref=59, clean=True),
    "tm-tdm260": S(PDF_B, None, "TDM-260 surface planer and thicknesser", xref=144, clean=True),
    "tm-tdm320": S(PDF_B, None, "TDM-320 surface planer and thicknesser", xref=148, clean=True),
    "tm-tdm-thick": S(PDF_B, None, "Planer-thicknesser opened for thicknessing", xref=152, clean=True),
    "tm-tdm-roller": S(PDF_B, None, "Spiral-toothed infeed roller and cutterblock", xref=160, detail=True),
    "tm-wjp15": S(PDF_B, None, "WJP-15 15″ thickness planer with spiral cutterhead", xref=76, clean=True, logo_out=[(249, 94, 333, 134)]),
    "tm-wjp20": S(PDF_B, None, "WJP-20 20″ thickness planer with spiral cutterhead", xref=80, clean=True),
    "tm-wjp15b": S(PDF_B, None, "WJP-15B benchtop thickness planer", xref=133, clean=True, logo_out=[(261, 228, 368, 270)]),
    "tm-wjp-cutterhead": S(PDF_B, None, "Spiral cutterhead of the thickness planer", xref=84, detail=True),
    "tm-wts1050": S(PDF_B, None, "WTS10-50 10″ cabinet table saw with 52″ rip fence", xref=181, clean=True, logo_out=[(295, 317, 381, 362)]),
    "tm-wts1050s": S(PDF_B, None, "WTS10-50S table saw with touch-screen blade height and angle", xref=189, clean=True, logo_out=[(297, 274, 378, 298)]),
    "tm-wts-screen": S(PDF_B, None, "Touch screen for blade height and angle", xref=201, detail=True),
    "tm-wts-mortise": S(PDF_B, None, "Mortising attachment on the table saw (optional)", xref=197, detail=True),
    "tm-tbs356": S(PDF_B, None, "TBS-356 14″ band saw for wood", xref=208, clean=True),
    "tm-tbs457": S(PDF_B, None, "TBS-457 18″ band saw for wood", xref=230, clean=True),
    "tm-tl406": S(PDF_B, None, "TL-406 12 × 16″ wood lathe", xref=99, clean=True),
    "tm-tl406-bed": S(PDF_B, None, "TL-406 with the extension bed (optional)", xref=101, clean=True),
    "tm-mgx16": S(PDF_B, None, "MGX16 slot boring machine", xref=241, clean=True),
    "tm-mgx20r": S(PDF_B, None, "MGX20R slot boring machine with swivelling head", xref=245, clean=True),
    "tm-ms38": S(PDF_B, None, "MS 3-8 benchtop mortiser", xref=254, clean=True),
    "tm-ms48": S(PDF_B, None, "MS 4-8 benchtop mortiser", xref=258, clean=True),
    "tm-wm01": S(PDF_B, None, "WM-01 horizontal boring machine on stand", xref=262, clean=True),
    "tm-dc900": S(PDF_B, None, "DC900 dust collector", xref=280, clean=True, logo_out=[(103, 458, 139, 483)]),
    "tm-ws25": S(PDF_B, None, "WS25-200 belt and disc combination sander", xref=288, clean=True),
}
DETAIL = {k for k, v in PHOTOS.items() if v["detail"]}


def pdf_image(path, xref):
    import pymupdf as fitz
    d = fitz.open(path)
    pix = fitz.Pixmap(d, xref)
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    im = Image.open(io.BytesIO(pix.tobytes("png")))
    smask = next((i[1] for p in d for i in p.get_images(full=True) if i[0] == xref), 0)
    if smask:
        m = Image.open(io.BytesIO(fitz.Pixmap(d, smask).tobytes("png"))).convert("L")
        if m.size != im.size:
            m = m.resize(im.size, Image.LANCZOS)
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im.convert("RGB"), mask=m)
        im = bg
    return im.convert("RGB")


def paint(im, boxes, mode):
    """mode "white": paint the boxes white (captions, leader lines on the white sheet);
    mode "logo": remove the maker's badge or lettering inside each box and fill it from the surface around it (OpenCV
    inpainting).  Only the badge is replaced: the surface — every smooth area that reaches the edge of the box without
    crossing an edge, whether machine paint, a second colour band or the white background past the edge of the part —
    is kept, so nothing is smeared across a colour boundary."""
    a = np.asarray(im).copy()
    if mode == "white":
        for x0, y0, x1, y1 in boxes:
            a[y0:y1, x0:x1] = 255
        return Image.fromarray(a)
    import cv2
    from scipy import ndimage
    f = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.0)
    g = np.max([np.hypot(cv2.Sobel(f[:, :, c], cv2.CV_32F, 1, 0), cv2.Sobel(f[:, :, c], cv2.CV_32F, 0, 1)) for c in range(3)], axis=0) / 4
    for x0, y0, x1, y1 in boxes:
        lab, n = ndimage.label(g[y0:y1, x0:x1] < 20)
        edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        surface = np.isin(lab, list(edge))
        # the badge: the islands of edges and colour that do not reach the box edge; the edges that run out of the box (the
        # boundary between two paint bands, the edge of the part against the background) are kept, so they stay straight
        lab2, _ = ndimage.label(~surface)
        through = np.isin(lab2, list(set(np.unique(np.concatenate([lab2[0], lab2[-1], lab2[:, 0], lab2[:, -1]]))) - {0}))
        island = ~surface & ~through
        badge = ndimage.binary_dilation(island, iterations=2) & ~through if island.any() else ndimage.binary_dilation(~surface, iterations=2)
        badge[[0, -1], :] = False                       # the box edge stays: it is what the fill is taken from
        badge[:, [0, -1]] = False
        sub = np.ascontiguousarray(a[y0:y1, x0:x1, ::-1])
        # the surface the badge sits on: the smooth area with the most pixels along the badge; any other colour in the box
        # (a second paint band, the background past the edge of the part) is set to that surface's colour while filling,
        # then put back — the fill is taken from the badge's own surface only
        ring = ndimage.binary_dilation(badge, iterations=3) & ~badge
        ids, counts = np.unique(lab[ring & (lab > 0)], return_counts=True)
        tmp, other = sub.copy(), np.zeros_like(badge)
        if len(ids):
            main = ids[counts.argmax()]
            other = ~badge & (lab != main)
            tmp[other] = np.median(sub[lab == main], axis=0).astype(np.uint8)
        out = cv2.inpaint(tmp, badge.astype(np.uint8) * 255, 4, cv2.INPAINT_TELEA)
        out[other] = sub[other]
        a[y0:y1, x0:x1] = out[:, :, ::-1]
    return Image.fromarray(a)


def process(key):
    p = PHOTOS[key]
    im = pdf_image(p["src"], p["xref"]) if p["xref"] else Image.open(p["src"]).convert("RGB")
    im = paint(im, p["white"], "white")
    im = paint(im, p["logo"], "logo")
    if p["box"]:
        im = im.crop(p["box"])
    if p["clean"]:
        im = P.clean_marks(im)
    im = P.trim(im)
    if p["lines"]:
        im = P.trim(erase_lines(im, p["lines"]))
    if p["logo_out"]:                                   # the maker's badge on the machine, located on the finished photo
        im = paint(im, [(max(0, x0 - PAD), max(0, y0 - PAD), min(im.width, x1 + PAD), min(im.height, y1 + PAD))
                        for x0, y0, x1, y1 in p["logo_out"]], "logo")
    while max(im.size) < SMALL:                         # small catalogue photos: Real-ESRGAN 2x (twice under 260 px), not a blurred zoom
        from esrgan import upscale
        im = upscale(im)
    os.makedirs(DST, exist_ok=True)
    im.save(os.path.join(DST, key + ".jpg"), quality=92)
    return im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PHOTOS)
    for k in keys:
        print(f"{k:22s} {process(k)}")


if __name__ == "__main__":
    main()
