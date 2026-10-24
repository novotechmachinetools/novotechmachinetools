#!/usr/bin/env python3
"""Fill the BiRefNet cut-out cache (tools/cache/birefnet/) for every photo tools/make_images.py would cut out, so a
later full make_images.py run is fast.  Runs for hours on CPU; start it detached and watch tools/cache/precache.log:

    (setsid nohup python3 tools/birefnet_precache.py > tools/cache/precache.log 2>&1 < /dev/null &)
"""
import json, os, sys, time
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout2 import is_white_background  # noqa: E402
from birefnet_cut import cut_rgba  # noqa: E402
import torch
torch.set_num_threads(max(1, (os.cpu_count() or 2) - 1))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = json.load(open(os.path.join(ROOT, "tools", "image_map.json")))
todo = []
for name, spec in MAP.items():
    section = spec.get("section", "rebar")
    if section == "guide" or name.startswith("video-"):
        continue
    src = spec.get("orig") or spec["src"]
    if not os.path.isabs(src):
        src = os.path.join(ROOT, src)
    if not os.path.exists(src):
        continue
    im = Image.open(src)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    if has_alpha and not spec.get("orig"):
        continue
    want = spec.get("cutout")
    if want is False or want == "threshold":
        continue
    im = ImageOps.exif_transpose(im).convert("RGB")
    if spec.get("crop"):
        im = im.crop(tuple(spec["crop"]))
    white, _ = is_white_background(im)
    if want is not None:
        white = bool(want)
    if white or spec.get("orig"):
        todo.append((name, spec, im))
print(f"{len(todo)} photos to cut", flush=True)
t0 = time.time()
for i, (name, spec, im) in enumerate(todo, 1):
    t = time.time()
    cs = spec.get("cut_spec")
    cspec = json.load(open(os.path.join(ROOT, cs))) if cs else None
    cut_rgba(im, str(spec.get("cut_size", 1024)), spec=cspec, cache_key=name)
    print(f"{i}/{len(todo)} {name} {im.width}x{im.height} {time.time()-t:.0f}s  (total {(time.time()-t0)/60:.0f} min)", flush=True)
print("done", flush=True)
