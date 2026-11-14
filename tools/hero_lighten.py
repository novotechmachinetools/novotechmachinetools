#!/usr/bin/env python3
"""Lighter files for the page heroes — the photo PageSpeed waits for (Largest Contentful Paint).

    python3 tools/hero_lighten.py            # every hero-main photo of the built pages (run build.py first)
    python3 tools/hero_lighten.py NAME …     # only these image names (e.g. wt-wecomatic-200)

The 480 / 680 / 800 px variants are re-encoded from the photo's largest variant (1200 px, else the largest there is) at
WebP quality 72, cut-out edges (alpha) at quality 70, method 6: 35 – 45 % fewer bytes, no visible difference at the size
they are shown (checked side by side on the orange band, Nov 14 2026). The largest variant itself is left as it is, so
nothing is re-compressed twice at full size. A file is replaced only when the new one is at least 10 % smaller, and
tools/image_manifest.json gets the new byte counts. Phones load the 680 px file in PageSpeed's test (412 px × 1.75).
"""
import io, json, os, re, sys, glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "tools", "image_manifest.json")
WIDTHS = (480, 680, 800)
Q, ALPHA_Q = 72, 70

manifest = json.load(open(MANIFEST, encoding="utf-8"))
names = sys.argv[1:]
if not names:
    found = set()
    for page in glob.glob(os.path.join(ROOT, "dist", "*.html")):
        h = open(page, encoding="utf-8").read()
        for src in re.findall(r'<img class="hero-main" src="img/[^"/]+/([^"]+?)-\d+\.webp"', h):
            found.add(src)
    names = sorted(found)

saved = 0
done = 0
for name in names:
    entry = manifest.get(name)
    if not entry or not entry.get("variants"):
        print(f"skip {name}: not in the manifest")
        continue
    variants = entry["variants"]
    big = max(variants, key=lambda v: v["w"])
    src_path = os.path.join(ROOT, "src", big["file"])
    if not os.path.exists(src_path):
        print(f"skip {name}: {big['file']} missing")
        continue
    im = Image.open(src_path)
    im.load()
    alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if alpha else "RGB")
    for v in variants:
        if v["w"] not in WIDTHS or v["w"] >= big["w"]:
            continue
        path = os.path.join(ROOT, "src", v["file"])
        if not os.path.exists(path):
            continue
        old = os.path.getsize(path)
        small = im.resize((v["w"], v["h"]), Image.LANCZOS)          # the same pixel size as before: the page's width/height stay
        buf = io.BytesIO()
        if alpha:
            small.save(buf, "WEBP", quality=Q, alpha_quality=ALPHA_Q, method=6)
        else:
            small.save(buf, "WEBP", quality=Q, method=6)
        new = len(buf.getvalue())
        if new > old * 0.9:
            continue
        open(path, "wb").write(buf.getvalue())
        v["bytes"] = new
        saved += old - new
        done += 1
        print(f"{v['file']}: {old // 1024} → {new // 1024} KB")

open(MANIFEST, "w", encoding="utf-8").write(json.dumps(manifest, indent=1))
print(f"{done} files lighter, {saved // 1024} KB less in all, {len(names)} hero photos looked at")
