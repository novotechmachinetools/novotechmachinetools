#!/usr/bin/env python3
"""EUROSTAMP press brake tooling — photos, the maker's drawings and the standard-length diagrams → tools/src-images/eurostamp/
(image_map section 'tooling'; registered by tools/eurostamp_pages.py).

Sources (outside the repository, /home/claude/eurostamp/):
  img/<code>-….jpg      the web shop's drawing of each tool (1100 × 1422, often RGBA) and its standard-lengths picture
  web/                  photos from eurostampsrl.it (hero, range, gooseneck and die groups)
  web2/                 the shop's pictures of the accessories, radius and joggle tools, adjustable dies and EUROGRIP (October 2026)
  pdf/ext, pdf/ext2     photos extracted from the IT-EN catalogue (≈ 600 px: Real-ESRGAN x2 before use)
  am/                   NovoTech's American-style brochure: the profile drawings (white on black) and larger copies of
                        catalogue photos

Kinds:
  draw    a drawing on white (or transparent) → composited on white, cropped to the drawing → PNG
  std     a standard-lengths diagram → the Italian line of each bilingual label (or a whole label) removed with LaMa → PNG
  photo   a photo → crop, a duotone page photo turned grey (the catalogue tints some pages red, blue, purple or orange),
          Real-ESRGAN x2 when small (twice when tiny) → JPEG, stays a rectangle on the site
  cut     a product photo cut out with BiRefNet (cached) → WebP with alpha — the page heroes and their minis
  mask    a catalogue image that comes with its own soft mask → WebP with alpha
  am      an American-style drawing (white on black) → steel-grey body, charcoal lines, on white → PNG
  amhero  the American page hero: a line-up of profiles (bodies only, outlined) on transparent → WebP

    python3 tools/eurostamp_photos.py [keys] [--force]     process (missing outputs only, unless --force)
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ES = "/home/claude/eurostamp/"
IMG, WEB, WEB2, EXT, EXT2, EXT3, AM = (ES + d for d in ("img/", "web/", "web2/", "pdf/ext/", "pdf/ext2/", "pdf/ext3/", "am/"))
OUT = os.path.join(ROOT, "tools", "src-images", "eurostamp")
MAX_SIDE = 1800
Image.MAX_IMAGE_PIXELS = None


def draw(src, alt, **kw):
    return dict(kind="draw", src=src, alt=alt, **kw)


def std(src, alt, labels=(), **kw):
    return dict(kind="std", src=IMG + src, alt=alt, labels=list(labels), **kw)


def photo(src, alt, crop=None, gray=False, **kw):
    return dict(kind="photo", src=src, alt=alt, crop=crop, gray=gray, **kw)


def cut(src, alt, crop=None, gray=False, **kw):
    return dict(kind="cut", src=src, alt=alt, crop=crop, gray=gray, **kw)


# the American-style drawings of NovoTech's brochure: part number → (image, description)
AM_DRAW = {"S28932": ("x40", "88° straight punch, tip R .059″, 3.779″ high"), "S28881": ("x43", "88° gooseneck punch, tip R .031″, 3.779″ high"),
           "S28880": ("x45", "85° gooseneck punch, tip R .031″, 3.779″ high"), "S29083": ("x49", "30° acute punch, tip R .059″, 3.779″ high"),
           "S29252": ("x51", "28° acute punch, tip R .031″, 3.779″ high"), "S29084": ("x53", "28° acute gooseneck punch, 5.125″ high"),
           "S28946": ("x57", "88° 1V die, V .375″, 1.000″ wide"), "S29269": ("x59", "88° 1V die, V .500″, 1.000″ wide"),
           "S29145": ("x61", "88° 1V die, V .626″, 1.000″ wide"), "S28947": ("x63", "88° 1V die, V .750″, 1.500″ wide"),
           "S29142": ("x67", "30° acute die, V .375″, 1.000″ wide"), "S29141": ("x69", "30° acute die, V .500″, 1.000″ wide"),
           "S29143": ("x71", "30° acute die, V .635″, 1.500″ wide"), "S29144": ("x73", "34° acute die, V .875″, 2.000″ wide")}

PHOTOS = {
    # ---------------------------------------------------------------- hub
    "es-p-range": cut(WEB + "es-hero_mob.jpg", "EUROSTAMP press brake tooling — punches, dies, holders and adapters made in Italy"),
    "es-p-group": cut(WEB + "es-02.jpg", "Straight, gooseneck and acute punches from EUROSTAMP"),
    # ---------------------------------------------------------------- European punches
    # every photo of a style page comes from that style's own pages of the EUROSTAMP catalogue (red pages = Amada-Promecam,
    # blue = Trumpf, purple = Wila, orange = Bystronic) or shows a part number of that style
    "es-p-c077a": photo(EXT + "p077-x309.png", "Sectioned European-style acute punch 1311 (26°), 805 mm set — horns at both ends and short sections between"),
    "es-p-c077a-cut": cut(EXT + "p077-x309.png", "European-style (Amada-Promecam) sectioned punch, 805 mm set with horns"),
    "es-p-c077b": cut(EXT + "p077-x311.png", "European-style (Amada-Promecam) punch sections — the narrow 13 mm tang with its safety groove"),
    "es-p-c107": cut(EXT + "p107-x452.png", "Trumpf-style gooseneck punches with the safety button in the tang"),
    "es-p-c015": photo(EXT + "p015-x51.png", "Gooseneck punches standing in a row, sections and full lengths", gray=True),
    "es-p-c078a": photo(EXT + "p078-x315.png", "ESH punches — every profile 120 mm (4.72″) high", crop=(0, 95, 597, 455), gray=True),
    "es-p-radius-press": photo(EXT2 + "p192-x806.png", "Radius holder with a round element in the press brake beam"),
    "es-p-c013": photo(AM + "x15.png", "Round radius elements on their bars"),
    "es-p-radius-hand": photo(EXT2 + "p193-x810.png", "Finishing round radius elements in the EUROSTAMP plant"),
    "es-w-1096": draw(WEB2 + "1096.jpg", "1096 — straight holder for round radius elements, 100 mm high (drawing)"),
    "es-w-1090": draw(WEB2 + "1090.jpg", "1090 — gooseneck holder for round radius elements, 115 mm high (drawing)"),
    "es-w-1041": draw(WEB2 + "1041.jpg", "1041 — round radius element R25 in its holder (drawing)"),
    "es-w-1297": draw(WEB2 + "1297.jpg", "1297 — holder for the small radius elements R5 – R6.5 (drawing)"),
    "es-w-1180": draw(WEB2 + "1180.jpg", "1180 — small radius element R3 (drawing)"),
    "es-p-joggle-press": photo(EXT2 + "p207-x889.png", "Offset tool in the press brake bending a Z in one stroke"),
    "es-p-joggle-press2": photo(EXT2 + "p209-x896.png", "Offset insert pair closed on the sheet — upper and lower holders"),
    "es-p-joggle-insert": dict(kind="mask", src=EXT2 + "p204-x876.png", mask=EXT2 + "p204-x874.png", alt="Offset insert marked Z = 5 / 90°"),
    "es-p-joggle-holder": photo(EXT2 + "p205-x881.png", "1150 offset insert holder, European style"),
    "es-w-1150": draw(WEB2 + "1150.jpg", "1150 — offset insert holders, European style, upper and lower (drawing)"),
    "es-w-1198": draw(WEB2 + "1198.jpg", "1198 — offset insert holders, Bystronic type R and RF-A (drawing)"),
    "es-w-1135": draw(WEB2 + "1135.jpg", "1135 — offset insert pair Z 3.5 mm at 90° (drawing)"),
    "es-w-1130": draw(WEB2 + "1130.jpg", "1130 — offset insert pair Z 1 mm at 140° for thin sheet (drawing)"),
    # ---------------------------------------------------------------- European dies
    "es-p-dies": cut(WEB + "es-01.jpg", "Trumpf-style dies — the 3228 1V die with its sections"),
    "es-p-c055": photo(EXT + "p055-x196.png", "European-style 1V dies in the lower beam, punch above"),
    "es-p-c041": cut(EXT3 + "p041-x135.png", "European-style (Amada-Promecam) 1V die 2081, 45°, sectioned to the length of the bend", fade_right=0.16),
    "es-p-c047": photo(EXT3 + "p047-x170.png", "European-style two-V self-centring dies"),
    "es-p-c066": photo(EXT3 + "p066-x242.png", "Rail with a self-centring die insert, bolted in the European-style lower beam"),
    "es-p-c039": photo(EXT3 + "p039-x128.png", "European-style T dies taken from the tooling rack"),
    "es-p-treat": photo(AM + "x18.png", "Tools finished with nitriding and phosphating — surface treatments EUROSTAMP applies on request"),
    "es-p-c067a": photo(EXT + "p067-x247.png", "Rail for self-centring dies"),
    "es-p-c067b": cut(EXT + "p067-x249.png", "3173 holder for ESH insert dies, with its urethane strip"),
    "es-p-c071": photo(EXT + "p071-x264.png", "Hemming die with the spring-loaded flattening plate"),
    "es-p-c078b": photo(EXT + "p078-x315.png", "ESH insert dies in the 3173 holder", crop=(0, 450, 597, 790), gray=True),
    # ---------------------------------------------------------------- Trumpf & Wila
    "es-p-c110": cut(EXT + "p110-x466.png", "Trumpf-style dies — the 3244 1V die with sections and pieces"),
    "es-p-c091": photo(EXT + "p091-x381.png", "Trumpf-style punches with safety buttons in the tang", gray=True),
    "es-p-c147": cut(EXT + "p147-x603.png", "Wila-style punch with safety button", gray=True),
    "es-p-c164": photo(EXT + "p164-x672.png", "Wila-style dies and punch"),
    # ---------------------------------------------------------------- Bystronic & LVD
    "es-p-c180": cut(EXT + "p180-x739.png", "Bystronic-style punches, type R and RF-A"),
    "es-p-c171": cut(EXT + "p171-x699.png", "Bystronic-style gooseneck and sash punches", gray=True),
    # ---------------------------------------------------------------- holders, adapters, clamps, accessories
    "es-p-holders": cut(WEB + "es-header-video.jpg", "Lower die holders and adapters with a punch, EUROSTAMP"),
    "es-p-c157": photo(EXT + "p157-x643.png", "Extension for Trumpf / Wila-style punches, with safety pins"),
    "es-w-4221": draw(WEB2 + "4221.jpg", "4221 — adjustable intermediate Z1, H100, with the crowning wedge (drawing)"),
    "es-w-4411": draw(WEB2 + "4411.jpg", "4411 — heavy-duty adjustable intermediate Z2, H120, 160 t/m (drawing)"),
    "es-w-4228": draw(WEB2 + "4228.jpg", "4228 — short fixed intermediate Z2, H120, 75 mm long (drawing)"),
    "es-w-4362": draw(WEB2 + "4362.jpg", "4362 — adapter from a European ram to Trumpf / Wila punches (drawing)"),
    "es-w-4191": draw(WEB2 + "4191.jpg", "4191 — adapter from a Trumpf / Wila ram to European punches (drawing)"),
    "es-w-4193": draw(WEB2 + "4193.jpg", "4193 — adapter from a Beyeler type S ram to European punches (drawing)"),
    "es-w-4143s": draw(WEB2 + "4143S.jpg", "4143 — adapter from an LVD ram to European punches, size S (drawing)"),
    "es-p-eg-row": draw(WEB2 + "eg-mwdp.jpg", "EUROGRIP clamps along the upper beam of a press brake"),
    "es-p-eg-measy": draw(WEB2 + "eg-measy.jpg", "EUROGRIP M-EASY clamp on an intermediate, recessed handle on top"),
    "es-p-eg-pdhold": draw(WEB2 + "eg-pdhold.jpg", "EUROGRIP P-DHOLD pneumatic die holder for European-style dies"),
    "es-p-c218": photo(AM + "x16.png", "EUROGRIP clamp — the handle sits flush in the body"),
    "es-w-4021": draw(WEB2 + "4021.jpg", "4021 — safety clamp with top handle and fixing screws, H60 (drawing)"),
    "es-w-4219": draw(WEB2 + "4219.jpg", "4219 — safety clamp with top lever and urethane insert (drawing)"),
    "es-w-4009": draw(WEB2 + "4009.jpg", "4009 — safety clamp with fold-away handle (drawing)"),
    "es-w-4302": draw(WEB2 + "4302.jpg", "4302 — lower adapter from a Beyeler / Trumpf beam to European dies, H60 (drawing)"),
    "es-w-4304": draw(WEB2 + "4304.jpg", "4304 — lower adapter from a European beam to LVD dies, H40 (drawing)"),
    "es-w-4040": draw(WEB2 + "4040.jpg", "Filler block with its long clamps (drawing)"),
    "es-w-4034": draw(WEB2 + "4034.jpg", "4034 — short clamp for the rear of the filler block (drawing)"),
    "es-w-8100": draw(WEB2 + "8100.jpg", "Tang on request: Beyeler / Trumpf style 13 × 20 mm (drawing)"),
    "es-w-8107": draw(WEB2 + "8107.jpg", "Tang on request: American style, 12.7 mm (.500″) (drawing)"),
    "es-w-3191": draw(WEB2 + "3191.jpg", "3191 — adjustable die V 65 – 180 mm, closed and open (drawing)"),
    "es-w-3190": draw(WEB2 + "3190.jpg", "3190 — adjustable die V 24 – 124 mm, closed and open (drawing)"),
    "es-w-3192": draw(WEB2 + "3192.jpg", "3192 — adjustable die V 120 – 300 mm, closed and open (drawing)"),
    "es-w-3243": draw(WEB2 + "3243.jpg", "3243 — adjustable die V 150 – 400 mm, closed and open (drawing)"),
    "es-w-9015": draw(WEB2 + "9015.jpg", "9015 — lower adapter for the 3190 adjustable die, European style (drawing)"),
    "es-w-4308": draw(WEB2 + "4308.jpg", "Urethane protective film unrolled over a die"),
    "es-w-4309": draw(WEB2 + "4309.webp", "Film tighteners holding the protective film over the die"),
    "es-p-c255": photo(EXT2 + "p255-x1154.png", "Protective film stretched over the V by its supports"),
    "es-w-4379": draw(WEB2 + "4379.jpg", "Protective cloth for sheet up to 3 mm (1/8″)"),
    "es-w-4380": draw(WEB2 + "4380.jpg", "Protective cloth for sheet up to 6 mm (1/4″)"),
    "es-w-2037": draw(WEB2 + "2037.jpg", "2037 — holder for 50 × 50 mm urethane inserts (drawing)"),
    "es-w-2110": draw(WEB2 + "2110.jpg", "2110 — holder for 24 × 35 mm nylon inserts, H75 (drawing)"),
    "es-w-2119": draw(WEB2 + "2119.jpg", "2119 — triangular urethane insert 50 × 25 mm with hole (drawing)"),
    "es-w-4384": draw(WEB2 + "4384.jpg", "Digital gauge for 45° chamfers and radii"),
    "es-p-gauge-hand": photo(EXT2 + "p258-x1173.png", "Reading a bend radius with the digital gauge"),
    "es-w-4883": draw(WEB2 + "4883.jpg", "Manual protractor"),
    "es-w-4306": draw(WEB2 + "4306.webp", "Reference squares on the press brake table"),
    "es-w-4307": draw(WEB2 + "4307.webp", "Adjustable reference square with its scale"),
    "es-p-magarm": photo(EXT2 + "p257-x1169.png", "Magnetic squaring arms"),
    "es-p-cabinet": photo(EXT2 + "p260-x1182.png", "Tooling cabinet with five drawers"),
    "es-p-trolley": photo(EXT2 + "p260-x1183.png", "Mobile tooling trolley with five shelves"),
    # ---------------------------------------------------------------- standard-length diagrams (the maker's, labels in English only)
    "es-std-eu-punch": std("504-1338-punches-75.jpg", "Standard lengths of European-style punches: 835 and 415 mm, and the 805 mm sectioned set with horns",
                           labels=[((140, 330, 372, 452), "first"), ((88, 755, 352, 880), "first"), ((125, 1124, 352, 1172), "first")]),
    "es-std-eu-die": std("502-2091-die-85.jpg", "Standard lengths of European-style dies: 835 and 415 mm, and the 805 mm sectioned set",
                         labels=[((152, 482, 382, 588), "first"), ((594, 645, 856, 762), "first")]),
    "es-std-tr-die": std("1052-3224-1v-dies-60.jpg", "Standard lengths of Trumpf-style dies: 100, 200, 300 and 500 mm, and the 550 mm sectioned set",
                         labels=[((380, 185, 600, 285), "first"), ((490, 1060, 752, 1208), "first")]),
    "es-std-tr-sets": std("1059-3156-1v-dies-30.jpg", "Trumpf-style dies made up to bed lengths of 550 to 4050 mm from sectioned sets and pieces"),
    "es-std-tr-punch": std("1002-1251-flattening-hemming-tools-24.jpg", "Standard lengths of Trumpf-style punches: 100 to 500 mm, and the 550 mm sectioned set",
                           labels=[((630, 262, 872, 300), "first")]),
    "es-std-by-punch": std("1006-1218-r-punches-85.jpg", "Standard lengths of Bystronic-style punches: 500 mm and the 550 mm sectioned set with horns; type R and RF-A tangs",
                           boxes=[(902, 528, 956, 547), (908, 740, 960, 759)]),
    "es-std-by-die": std("1000-3174-flattening-hemming-tools-24.jpg", "Standard lengths of Bystronic-style dies: 500 and 1000 mm, and the 550 and 1100 mm sectioned sets",
                         labels=[((262, 465, 485, 565), "all")]),
    # ---------------------------------------------------------------- American style
    "es-am-sect": photo(AM + "x35.png", "American-style sectioned sets: punch and die sections in inches, 35.75″ in all"),
    "es-am-hero": dict(kind="amhero", src=AM, alt="American-style punches and dies with the .500″ tang — gooseneck, straight and acute profiles",
                       codes=["S29084", "S28881", "S28932", "S29083", "S28946", "S28947", "S29144"]),
    **{f"es-am-{c.lower()}": dict(kind="am", src=AM + f"{x}.png", alt=f"{c} — American-style {d} (drawing, inches)") for c, (x, d) in AM_DRAW.items()},
}


# ------------------------------------------------------------------------------------------------ helpers
def fit(im, cap=MAX_SIDE):
    """at most `cap`; a picture 560 – 800 px wide is brought to 800 px so the site gets its 800 px variant"""
    s = cap / max(im.size)
    if s >= 1:
        s = 800 / im.width if 560 <= im.width < 800 else 1
    elif 560 <= im.width * s < 800:
        s = 800 / im.width
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS) if s != 1 else im


def on_white(im):
    im = im.convert("RGBA")
    w = Image.new("RGBA", im.size, (255, 255, 255, 255))
    w.alpha_composite(im)
    return w.convert("RGB")


def content_box(rgb, thr=242, pad=0.04):
    """bounding box of everything darker than `thr`, padded by `pad` × its longer side"""
    g = np.asarray(rgb.convert("L"))
    ys, xs = np.nonzero(g < thr)
    if not len(xs):
        return (0, 0) + rgb.size
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    p = round(max(x1 - x0, y1 - y0) * pad)
    return (max(0, x0 - p), max(0, y0 - p), min(rgb.width, x1 + p), min(rgb.height, y1 + p))


def duotone_gray(rgb):
    """a catalogue page tinted red / blue / purple / orange → neutral grey: the HSV value channel carries the tone ramp"""
    a = np.asarray(rgb).astype(np.float32)
    v = a.max(axis=2)
    g = Image.fromarray(v.clip(0, 255).astype(np.uint8), "L")
    g = ImageOps.autocontrast(g, cutoff=0.5)
    return Image.merge("RGB", (g, g, g))


def upscale_small(im, target=760):
    from esrgan import upscale
    while max(im.size) < target:
        im = upscale(im)
    return im


def remove_old(key):
    for e in (".png", ".jpg", ".webp"):
        f = os.path.join(OUT, key + e)
        if os.path.exists(f):
            os.remove(f)


def clean_alpha(alpha, keep=0.004):
    a = np.array(alpha)
    lab, n = ndimage.label(a > 24)
    if n <= 1:
        return alpha
    sizes = ndimage.sum(np.ones_like(a), lab, range(1, n + 1))
    drop = [i + 1 for i, s in enumerate(sizes) if s < keep * sizes.max()]
    if drop:
        a[np.isin(lab, drop)] = 0
    return Image.fromarray(a)


def save_rgba(key, rgba):
    a = rgba.getchannel("A")
    bb = a.point(lambda v: 255 if v > 8 else 0).getbbox()
    rgba = fit(rgba.crop(bb))
    remove_old(key)
    path = os.path.join(OUT, key + ".webp")
    rgba.save(path, quality=95, alpha_quality=100, method=6)
    return path, rgba.size


# ------------------------------------------------------------------------------------------------ label removal (std diagrams)
def label_mask(rgb, box, which):
    """the blue label text inside `box`, letter by letter: the letters (connected components of strong blue) are grouped
    into text lines by the position of their centres across the text direction (PCA of the blue pixels); dimension lines
    (long components) and numbers (few letters) are skipped.  The picked letters grow 2 px into their anti-aliased edge.
    `which`: 'first' = the upper line (the Italian one of a bilingual label), 'all' = every text line in the box"""
    x0, y0, x1, y1 = box
    a = np.asarray(rgb).astype(np.int16)[y0:y1, x0:x1]
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    core = (B - R > 45) & (B >= G)
    m = np.zeros(rgb.size[::-1], bool)
    lab, n = ndimage.label(core, structure=np.ones((3, 3)))
    if n == 0:
        return m
    ys, xs = np.nonzero(core)
    pts = np.stack([xs, ys], 1).astype(np.float64)
    c = pts.mean(0)
    _, _, vt = np.linalg.svd(pts - c, full_matrices=False)
    d = vt[0] if vt[0][0] >= 0 else -vt[0]
    nrm = np.array([-d[1], d[0]])
    if nrm[1] < 0:
        nrm = -nrm
    objs = ndimage.find_objects(lab)
    cents = ndimage.center_of_mass(core, lab, range(1, n + 1))
    comps = []
    for i, (cy, cx) in enumerate(cents):
        sl = objs[i]
        if max(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start) > 70:
            continue
        q = np.array([cx, cy]) - c
        comps.append((i + 1, float(q @ nrm), float(q @ d)))
    if not comps:
        return m
    comps.sort(key=lambda t: t[1])
    clusters, cur = [], [comps[0]]
    for t in comps[1:]:
        if t[1] - cur[-1][1] > 6:
            clusters.append(cur)
            cur = [t]
        else:
            cur.append(t)
    clusters.append(cur)
    lines = [cl for cl in clusters if len(cl) >= 6 and max(t[2] for t in cl) - min(t[2] for t in cl) > 60]
    pick = lines[:1] if which == "first" else lines
    if not pick:
        return m
    sel = np.isin(lab, [t[0] for cl in pick for t in cl])
    # grow 4 px over the soft halo of the letters, but not past the middle of the gap to the next text line
    H, W = core.shape
    Y, X = np.mgrid[0:H, 0:W]
    P = (X - c[0]) * nrm[0] + (Y - c[1]) * nrm[1]
    span = lambda cl: (P[np.isin(lab, [t[0] for t in cl])].min(), P[np.isin(lab, [t[0] for t in cl])].max())
    lo, hi = span(pick[0])[0] - 5, span(pick[-1])[1] + 5
    rest = [cl for cl in lines if cl not in pick]
    below = [span(cl)[0] for cl in rest if span(cl)[0] > span(pick[-1])[1]]
    if below:
        hi = min(hi, (span(pick[-1])[1] + min(below)) / 2)
    sel = ndimage.binary_dilation(sel, iterations=4) & (P >= lo) & (P <= hi)
    m[y0:y1, x0:x1] = sel
    return m


def remove_labels(rgb, labels, boxes=()):
    from lama_inpaint import inpaint
    mask = np.zeros(rgb.size[::-1], bool)
    for box, which in labels:
        mask |= label_mask(rgb, box, which)
    for x0, y0, x1, y1 in boxes:                      # small grey text on white: the whole box
        mask[y0:y1, x0:x1] = True
    if not mask.any():
        return rgb
    return Image.fromarray(inpaint(np.asarray(rgb), (mask * 255).astype(np.uint8)))


# ------------------------------------------------------------------------------------------------ American drawings
CHARCOAL = np.array([44, 46, 50], np.float32)


def am_layers(path):
    """(value 0..1, body mask, filled body) of a white-on-black profile drawing"""
    v = np.asarray(Image.open(path).convert("L")).astype(np.float32) / 255.0
    if path.endswith("x57.png"):
        v[:, :40] = 0                                  # fragments of the neighbouring drawing at the left edge
    white = v > 0.5
    lab, n = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, n + 1))
    body = lab == (int(np.argmax(sizes)) + 1)
    holes = ndimage.binary_fill_holes(body) & ~body
    hl, hn = ndimage.label(holes)
    hs = ndimage.sum(holes, hl, range(1, hn + 1)) if hn else []
    big = [i + 1 for i, s in enumerate(hs) if s > 0.004 * body.sum()]          # notches, not strokes
    filled = body | (holes & ~np.isin(hl, big))
    return v, body, filled


def steel(shape, filled):
    H, W = shape
    ys, xs = np.nonzero(filled)
    t = np.clip((np.arange(W) - xs.min()) / max(1, xs.max() - xs.min()), 0, 1)[None, :] * np.ones((H, 1))
    s1, s2 = np.array([236, 238, 241], np.float32), np.array([190, 195, 203], np.float32)
    return s1[None, None] * (1 - t[..., None]) + s2[None, None] * t[..., None]


def am_drawing(path):
    """the full drawing (dimensions included) on white: steel body, charcoal lines and text"""
    v, body, filled = am_layers(path)
    st = steel(v.shape, filled)
    vv = v[..., None]
    inside = CHARCOAL[None, None] * (1 - vv) + st * vv
    outside = CHARCOAL[None, None] * vv + 255 * (1 - vv)
    rgb = np.where(filled[..., None], inside, outside)
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8), "RGB")


def am_profile(path):
    """the tool's body only, steel-filled with a charcoal outline, on transparent"""
    v, body, filled = am_layers(path)
    solid = ndimage.binary_fill_holes(body)
    st = steel(v.shape, solid)
    ring = ndimage.binary_dilation(solid, iterations=3) & ~solid
    H, W = v.shape
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.where(solid[..., None], st, CHARCOAL[None, None])
    out[..., 3] = np.where(solid | ring, 255, 0)
    im = Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")
    return im.crop(im.getchannel("A").getbbox()), solid


def am_hero(codes):
    """profiles side by side on one baseline at one scale (pixels per inch from each drawing's known height)"""
    heights = {"S29084": 5.125 + 0.752, "S28881": 4.531, "S28880": 4.531, "S28932": 4.531, "S29083": 4.531, "S29252": 4.531}
    parts = []
    for c in codes:
        im, solid = am_profile(AM + AM_DRAW[c][0] + ".png")
        h_in = heights.get(c, 2.563)
        parts.append((im, im.height / h_in))
    ppi = min(p for _, p in parts)
    parts = [im.resize((round(im.width * ppi / p), round(im.height * ppi / p)), Image.LANCZOS) for im, p in parts]
    gap = round(0.32 * ppi)
    W = sum(p.width for p in parts) + gap * (len(parts) - 1)
    H = max(p.height for p in parts)
    can = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 0
    for p in parts:
        can.alpha_composite(p, (x, H - p.height))
        x += p.width + gap
    return can


# ------------------------------------------------------------------------------------------------ processing
def process(key, force=False):
    p = PHOTOS[key]
    os.makedirs(OUT, exist_ok=True)
    have = [f for f in os.listdir(OUT) if os.path.splitext(f)[0] == key]
    if have and not force:
        return os.path.join(OUT, have[0])
    k = p["kind"]
    if k == "draw":
        im = on_white(Image.open(p["src"]))
        im = im.crop(content_box(im))
        im = fit(im)
        remove_old(key)
        path = os.path.join(OUT, key + (".png" if "(drawing" in p["alt"] else ".jpg"))
        im.save(path, **({} if path.endswith(".png") else {"quality": 92}))
    elif k == "std":
        im = on_white(Image.open(p["src"]))
        im = remove_labels(im, p.get("labels", []), p.get("boxes", []))
        im = fit(im.crop(content_box(im, pad=0.03)))
        remove_old(key)
        path = os.path.join(OUT, key + ".png")
        im.save(path)
    elif k in ("photo", "cut"):
        im = Image.open(p["src"]).convert("RGB")
        if p.get("crop"):
            im = im.crop(p["crop"])
        if p.get("gray"):
            im = duotone_gray(im)
        im = upscale_small(im, 1700 if p.get("up") else 760)
        if k == "cut":
            from birefnet_cut import cut_rgba
            rgba = cut_rgba(im, "1024", cache_key=f"eurostamp-{key}")
            if p.get("keep"):                   # only the part of the picture inside the polygon (source pixels)
                from PIL import ImageDraw
                src_w = Image.open(p["src"]).width
                s = im.width / src_w
                m = Image.new("L", im.size, 0)
                ImageDraw.Draw(m).polygon([(x * s, y * s) for x, y in p["keep"]], fill=255)
                rgba.putalpha(Image.fromarray(np.minimum(np.asarray(rgba.getchannel("A")), np.asarray(m))))
            rgba.putalpha(clean_alpha(rgba.getchannel("A")))
            if p.get("fade_right"):            # the photo cuts the part at its right edge: fade it out instead of a hard cut
                A = np.asarray(rgba.getchannel("A")).astype(np.float32)
                xs = np.nonzero(A.max(axis=0) > 8)[0]
                x1 = xs.max() if len(xs) else A.shape[1] - 1
                x0 = int(x1 - p["fade_right"] * (x1 - xs.min()))
                ramp = np.ones(A.shape[1], np.float32)
                ramp[x0:x1 + 1] = np.linspace(1, 0, x1 + 1 - x0) ** 1.4
                rgba.putalpha(Image.fromarray((A * ramp[None, :]).astype(np.uint8)))
            path, _ = save_rgba(key, rgba)
        else:
            im = fit(im)
            remove_old(key)
            path = os.path.join(OUT, key + ".jpg")
            im.save(path, quality=90)
    elif k == "mask":
        im = Image.open(p["src"]).convert("RGB")
        a = Image.open(p["mask"]).convert("L")
        im = upscale_small(im)
        a = a.resize(im.size, Image.LANCZOS)
        rgba = im.convert("RGBA")
        rgba.putalpha(a)
        path, _ = save_rgba(key, rgba)
    elif k == "am":
        im = am_drawing(p["src"])
        im = fit(im.crop(content_box(im, pad=0.03)))
        remove_old(key)
        path = os.path.join(OUT, key + ".png")
        im.save(path)
    elif k == "amhero":
        path, _ = save_rgba(key, am_hero(p["codes"]))
    else:
        raise ValueError(k)
    print(f"{key:22s} {k:6s} -> {os.path.basename(path)} {Image.open(path).size}", flush=True)
    return path


def drawing(key, t, force=False):
    """the maker's drawing of a tool (es-d-<code>), cropped on white → PNG"""
    path = os.path.join(OUT, key + ".png")
    if os.path.exists(path) and not force:
        return path
    os.makedirs(OUT, exist_ok=True)
    im = on_white(Image.open(t["drawing"]))
    im = fit(im.crop(content_box(im, pad=0.03)))
    im.save(path)
    return path


def exports(drawings, tool_alt, force=False):
    """(key, alt, source path) for every picture of the tooling pages: the photos, diagrams and drawings above and the maker's
    drawing of each tool in `drawings` (key → tool, from tools/eurostamp_pages.py), processed when missing"""
    for key, p in PHOTOS.items():
        yield key, p["alt"], process(key, force)
    for key, t in drawings.items():
        yield key, tool_alt(t), drawing(key, t, force)


if __name__ == "__main__":
    force = "--force" in sys.argv
    keys = [a for a in sys.argv[1:] if not a.startswith("--")]
    for k in keys or list(PHOTOS):
        process(k, force)
