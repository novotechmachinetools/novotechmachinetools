"""Cut a machine out of a photo with other machines behind it: rembg (IS-Net) plus hand-traced polygons in SOURCE
pixel coordinates (tools/cutout-specs/<photo>.json).  python3 tools/trace_cutout.py <src.jpg> <out.png> <spec.json>
spec = {"drop": [[poly],...], "keep": [[poly],...], "hole": [[poly],...]}  (drop/hole → alpha 0, keep → alpha 255)"""
import sys, json
from rembg import new_session, remove
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import numpy as np
src, out, specf = sys.argv[1:4]
spec = json.load(open(specf))
im = ImageOps.exif_transpose(Image.open(src)).convert('RGB'); W, H = im.size
res = remove(im, session=new_session("isnet-general-use"), post_process_mask=True)
a = np.asarray(res.getchannel('A')).astype(np.float32)
for poly in spec.get("keep", []):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255); m = m.filter(ImageFilter.GaussianBlur(1.0))
    a = np.maximum(a, np.asarray(m).astype(np.float32))
for poly in spec.get("drop", []) + spec.get("hole", []):
    m = Image.new('L', (W, H), 255); ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=0); m = m.filter(ImageFilter.GaussianBlur(1.0))
    a = a * (np.asarray(m).astype(np.float32) / 255)
res = Image.fromarray(np.dstack([np.asarray(im), a.astype(np.uint8)]), 'RGBA')
bbox = res.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); res = res.crop(bbox); res.save(out)
bg = Image.new('RGBA', res.size, (242, 138, 31, 255)); bg.alpha_composite(res)
chk = bg.convert('RGB'); chk.save(out.replace('.png', '-check.jpg'), quality=88)
print(out, res.size, 'bbox', bbox)
