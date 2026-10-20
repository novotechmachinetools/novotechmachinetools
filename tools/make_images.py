"""Build optimized WebP product images for the site from source photos.

Usage: python3 -I tools/make_images.py
Reads tools/image_map.json: { "<out-name>": {"src": "<path>", "alt": "...", "trim": true/false} }
Writes src/img/<section>/<out-name>-{1200,800,480}.webp (only sizes <= source width, always at least one)
and tools/image_manifest.json with the real dimensions of each variant (used by the templates).
"""
import json, os, sys
from PIL import Image, ImageOps
try:
    import pillow_avif  # noqa: F401  (AVIF sources)
except ImportError:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = json.load(open(os.path.join(ROOT, "tools", "image_map.json")))
SIZES = [1200, 800, 480]
only = None
if "--only" in sys.argv:
    only = set(sys.argv[sys.argv.index("--only")+1].split(","))
mpath = os.path.join(ROOT, "tools", "image_manifest.json")
manifest = json.load(open(mpath)) if (only and os.path.exists(mpath)) else {}

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

for name, spec in MAP.items():
    if only and name not in only:
        continue
    src = spec["src"]
    if not os.path.isabs(src):
        src = os.path.join(ROOT, src)
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if has_alpha else "RGB")
    if spec.get("trim") and has_alpha:
        im = trim_alpha(im)
    if spec.get("crop"):
        im = im.crop(tuple(spec["crop"]))
    if spec.get("trim_white", True) and not has_alpha and spec.get("section", "rebar") != "guide" and not name.startswith("video-"):
        im = trim_white(im)
    section = spec.get("section", "rebar")
    outdir = os.path.join(ROOT, "src", "img", section)
    os.makedirs(outdir, exist_ok=True)
    variants = []
    widths = [w for w in SIZES if w <= im.width] or [im.width]
    if im.width < SIZES[-1] and im.width not in widths:
        widths = [im.width]
    # small square-ish thumbnail for gallery strips
    t = im.copy(); t.thumbnail((160, 160), Image.LANCZOS)
    tout = os.path.join(outdir, f"{name}-thumb.webp"); t.save(tout, "WEBP", quality=78, method=6)
    thumb = {"w": t.width, "h": t.height, "file": f"img/{section}/{name}-thumb.webp", "bytes": os.path.getsize(tout)}
    for w in widths:
        if w == im.width:
            v = im.copy()
        else:
            v = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out = os.path.join(outdir, f"{name}-{w}.webp")
        q = spec.get("quality", 82)
        v.save(out, "WEBP", quality=q, method=6)
        variants.append({"w": v.width, "h": v.height, "file": f"img/{section}/{name}-{w}.webp", "bytes": os.path.getsize(out)})
    manifest[name] = {"alt": spec.get("alt", ""), "variants": variants, "alpha": has_alpha, "thumb": thumb}
    print(f"{name:34s} {im.width}x{im.height} -> " + ", ".join(f"{v['w']}w {v['bytes']//1024}KB" for v in variants))

json.dump(manifest, open(os.path.join(ROOT, "tools", "image_manifest.json"), "w"), indent=1)
print("manifest entries:", len(manifest))
