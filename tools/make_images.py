"""Build optimized WebP product images for the site from source photos.

Usage: python3 tools/make_images.py [--only key,key] [--engine birefnet|threshold]
Reads tools/image_map.json: { "<out-name>": {"src": "<path>", "alt": "...", "trim": true/false, "sizes": [w…] (optional, overrides 1200/800/480),
                                             "cutout": true/false (optional override),
                                             "orig": "<original photo>"  (cut it out again from this, ignoring a hand-made src),
                                             "cut_size": 1024|1280, "cut_spec": "tools/cutout-specs/x.json", "upscale": 1.5} }
Writes src/img/<section>/<out-name>-{1200,800,480}.webp (only sizes <= source width, always at least one; a photo 15 % or more
wider than the largest of those, under 1200 px, also gets <out-name>-<its width>.webp)
and tools/image_manifest.json with the real dimensions of each variant (used by the templates).

House rule (docs/images.md): a product photo shot on a white studio background is never shown as a
white rectangle on a coloured surface.  Every such photo is cut out automatically here (transparent
WebP, floor shadow kept translucent) so the machine sits directly on the card / gallery background.
Photos of real scenes (factory floor, showroom renders) stay rectangular unless "cutout": true is set or a
cut-out PNG is supplied as the source.  "cutout": true/false in image_map.json forces or prevents the cut-out.

Cut-out engine: BiRefNet (tools/birefnet_cut.py, cached in tools/cache/birefnet/) is the default — it keeps
hoses, handles, white covers on white and clears neighbouring machines, walls and pallets; the old white-threshold
cut (tools/cutout2.py) is kept as --engine threshold or "cutout": "threshold" per photo (fast, keeps the floor
shadow of studio renders).  A photo with "orig" is cut again from that original every time, so hand-made
cut-out PNGs are superseded without editing the map.
"""
import json, os, sys
from PIL import Image, ImageOps
try:
    import pillow_avif  # noqa: F401  (AVIF sources)
except ImportError:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout2 import auto_cutout, cutout, is_white_background  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = json.load(open(os.path.join(ROOT, "tools", "image_map.json")))
SIZES = [1200, 800, 480]
ENGINE = os.environ.get("CUTOUT_ENGINE", "birefnet")
if "--engine" in sys.argv:
    ENGINE = sys.argv[sys.argv.index("--engine") + 1]
only = None
if "--only" in sys.argv:
    only = set(sys.argv[sys.argv.index("--only")+1].split(","))
mpath = os.path.join(ROOT, "tools", "image_manifest.json")
manifest = json.load(open(mpath)) if (only and os.path.exists(mpath)) else {}
if "--manifest-out" in sys.argv:        # parallel runs: each chunk writes its own partial manifest, merged afterwards
    mpath = sys.argv[sys.argv.index("--manifest-out") + 1]
    manifest = {}

def trim_white(im, thr=236, pad=0.025):
    """Crop the white studio margin around a photo so the machine fills the frame (keeps a small
    margin). Only near-white rows/columns at the edges are removed; photos without a white border
    come back unchanged."""
    if im.mode != "RGB":
        return im
    g = im.convert("L")
    bbox = g.point(lambda v: 0 if v >= thr else 255).getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    px = round(max(r - l, b - t) * pad)
    box = (max(0, l - px), max(0, t - px), min(im.width, r + px), min(im.height, b + px))
    if box[2] - box[0] < im.width * 0.35 or box[3] - box[1] < im.height * 0.35:
        return im   # something odd (mostly white image) — leave it
    return im.crop(box)


def trim_alpha(im, pad=12):
    """Crop a transparent cut-out to its content box, leaving a small margin."""
    if im.mode != "RGBA":
        return im
    bbox = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    l = max(0, l - pad); t = max(0, t - pad); r = min(im.width, r + pad); b = min(im.height, b + pad)
    return im.crop((l, t, r, b))

def birefnet_cut(im, name, spec):
    from birefnet_cut import cut_rgba  # noqa: E402  (torch import is slow; only when needed)
    cs = spec.get("cut_spec")
    cspec = json.load(open(os.path.join(ROOT, cs))) if cs else None
    return cut_rgba(im, str(spec.get("cut_size", 1024)), spec=cspec, cache_key=name)


for name, spec in MAP.items():
    if only and name not in only:
        continue
    src = spec.get("orig") if (spec.get("orig") and ENGINE == "birefnet") else spec["src"]
    if not os.path.isabs(src):
        src = os.path.join(ROOT, src)
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if has_alpha else "RGB")
    if has_alpha:
        hist = im.getchannel("A").histogram()
        if sum(hist[:128]) < 0.005 * im.width * im.height:
            im = im.convert("RGB")      # an alpha channel that is (practically) fully opaque is just a photo
            has_alpha = False
    if spec.get("trim") and has_alpha:
        im = trim_alpha(im)
    if spec.get("crop"):
        im = im.crop(tuple(spec["crop"]))
    section = spec.get("section", "rebar")
    product_photo = section != "guide" and not name.startswith("video-")
    cut = ""
    if not has_alpha and product_photo:
        want = spec.get("cutout")
        white, level = is_white_background(im)
        if want is not None:
            white = bool(want)
        engine = spec.get("cutout") if spec.get("cutout") in ("birefnet", "threshold") else ENGINE
        if white or spec.get("orig"):
            if engine == "birefnet":
                im = trim_alpha(birefnet_cut(im, name, spec))
                cut = "birefnet"
            elif spec.get("cut_params"):        # hand-set thresholds for a photo the auto pass gets wrong (floor glow, cream covers)
                im = trim_alpha(cutout(im, **spec["cut_params"]))
                cut = "params"
            else:
                im = trim_alpha(auto_cutout(im, level))
                cut = "auto"
            has_alpha = True
        elif spec.get("trim_white", True):
            im = trim_white(im)
    if spec.get("upscale") and has_alpha:       # page heroes: a 1.5x Lanczos upscale so the 1200 px variant exists
        f = float(spec["upscale"]); im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    outdir = os.path.join(ROOT, "src", "img", section)
    os.makedirs(outdir, exist_ok=True)
    variants = []
    widths = [w for w in SIZES if w <= im.width] or [im.width]
    if im.width < SIZES[-1] and im.width not in widths:
        widths = [im.width]
    # a photo well between two standard widths keeps its own width as the largest variant too (a 644 px cut-out had only the
    # 480 px file, a 1,091 px one 800 px), so the gallery and the photo viewer get every pixel the photo has (Oct 30 2026)
    if im.width < SIZES[0] and im.width not in widths and im.width >= max(widths) * 1.15:
        widths = [im.width] + widths
    if spec.get("sizes"):        # e.g. the site logo: shown at 178 px, so 360 / 180 px variants instead of 1200 / 800 / 480
        widths = [w for w in spec["sizes"] if w <= im.width] or [im.width]
    # small square-ish thumbnail for gallery strips
    t = im.copy(); t.thumbnail((160, 160), Image.LANCZOS)
    tout = os.path.join(outdir, f"{name}-thumb.webp"); t.save(tout, "WEBP", quality=78, method=4)
    thumb = {"w": t.width, "h": t.height, "file": f"img/{section}/{name}-thumb.webp", "bytes": os.path.getsize(tout)}
    for w in widths:
        if w == im.width:
            v = im.copy()
        else:
            v = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out = os.path.join(outdir, f"{name}-{w}.webp")
        q = spec.get("quality", 82)
        v.save(out, "WEBP", quality=q, method=4)   # method 6 is ~30x slower for ~5% smaller files
        variants.append({"w": v.width, "h": v.height, "file": f"img/{section}/{name}-{w}.webp", "bytes": os.path.getsize(out)})
    manifest[name] = {"alt": spec.get("alt", ""), "variants": variants, "alpha": has_alpha, "thumb": thumb}
    if cut:
        manifest[name]["cut"] = cut
    print(f"{name:34s} {im.width}x{im.height}{' cut' if cut else ''} -> " + ", ".join(f"{v['w']}w {v['bytes']//1024}KB" for v in variants))

json.dump(manifest, open(mpath, "w"), indent=1)
print("manifest entries:", len(manifest))
