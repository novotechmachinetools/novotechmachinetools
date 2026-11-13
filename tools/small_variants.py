"""240 px and 320 px WebP variants for the small photos under the page heroes (PageSpeed, Nov 13 2026).

A small hero photo is about 100 - 200 px wide on a phone and on a desktop, while the smallest file make_images.py writes is
480 px wide (about 30 KB): PageSpeed Insights counted 160 - 290 KB of oversized images on the busy pages.  This adds
<name>-240.webp and <name>-320.webp beside the other variants (made from the largest one, same WebP quality) and lists them
in tools/image_manifest.json, so the srcset of every <img> of those photos offers them too.

Also a 680 px variant of each page's large hero photo (a phone shows it about 380 px wide: 665 px at PageSpeed's 1.75 pixel
ratio, where the browser took the 800 px file) and a 240 px header logo (about 105 - 130 px wide on a phone, where the
browser took the 360 px file).

Run it after `python3 build.py` (it reads the small hero photos from dist/*.html), then build again:
    python3 tools/small_variants.py && python3 build.py
Safe to run again: a photo that already has its 240 / 320 px files is skipped.  A photo re-made by make_images.py loses the
two small variants from the manifest until this is run again (the page then simply offers the 480 px file, as before).
"""
import glob
import json
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MPATH = os.path.join(ROOT, "tools", "image_manifest.json")
WIDTHS = (320, 240)

manifest = json.load(open(MPATH))
image_map = json.load(open(os.path.join(ROOT, "tools", "image_map.json"), encoding="utf-8"))
by_file = {v["file"]: name for name, e in manifest.items() for v in e["variants"]}

want = {"novotech-logo": (240,)}
for f in glob.glob(os.path.join(ROOT, "dist", "*.html")):
    s = open(f, encoding="utf-8").read()
    for block in re.findall(r'<(?:ul|div) class="hero-minis.*?</(?:ul|div)>', s, re.S):
        for src in re.findall(r'<img src="([^"?]+)', block):
            if src in by_file:
                want[by_file[src]] = tuple(sorted(set(want.get(by_file[src], ())) | set(WIDTHS)))
    for src in re.findall(r'<img class="hero-main" src="([^"?]+)', s):
        if src in by_file:
            want[by_file[src]] = tuple(sorted(set(want.get(by_file[src], ())) | {680}))
names = [n for n in want if n != "novotech-logo"]

added = 0
for name in sorted(want):
    e = manifest[name]
    have = {v["w"] for v in e["variants"]}
    largest = max(e["variants"], key=lambda v: v["w"])
    todo = [w for w in want[name] if w not in have and largest["w"] >= w * 1.15]
    if not todo:
        continue
    src = Image.open(os.path.join(ROOT, "src", largest["file"]))
    src.load()
    q = image_map.get(name, {}).get("quality", 82)
    for w in todo:
        v = src.resize((w, round(src.height * w / src.width)), Image.LANCZOS)
        rel = re.sub(r"-\d+\.webp$", f"-{w}.webp", largest["file"])
        out = os.path.join(ROOT, "src", rel)
        v.save(out, "WEBP", quality=q, method=4)
        e["variants"].append({"w": v.width, "h": v.height, "file": rel, "bytes": os.path.getsize(out)})
        added += 1
    e["variants"].sort(key=lambda v: -v["w"])   # widest first, as make_images.py writes them

open(MPATH, "w").write(json.dumps(manifest, indent=1))
print(f"photos: {len(want)}, new files: {added}")
