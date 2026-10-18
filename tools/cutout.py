"""Remove a plain white studio background from a product photo (flood fill from the edges) → PNG with alpha.
    python3 -I tools/cutout.py <src.jpg> <out.png> [threshold=235]
"""
import sys
from PIL import Image, ImageFilter
from collections import deque
src, out = sys.argv[1], sys.argv[2]
thr = int(sys.argv[3]) if len(sys.argv) > 3 else 235
im = Image.open(src).convert("RGB")
w, h = im.size
px = im.load()
mask = bytearray(w * h)        # 1 = background
def is_bg(x, y):
    r, g, b = px[x, y]
    return r >= thr and g >= thr and b >= thr and max(r, g, b) - min(r, g, b) < 18
q = deque()
for x in range(w):
    for y in (0, h - 1):
        if is_bg(x, y) and not mask[y * w + x]:
            mask[y * w + x] = 1; q.append((x, y))
for y in range(h):
    for x in (0, w - 1):
        if is_bg(x, y) and not mask[y * w + x]:
            mask[y * w + x] = 1; q.append((x, y))
while q:
    x, y = q.popleft()
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < w and 0 <= ny < h and not mask[ny * w + nx] and is_bg(nx, ny):
            mask[ny * w + nx] = 1; q.append((nx, ny))
alpha = Image.frombytes("L", (w, h), bytes(255 - 255 * m for m in mask))
alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))
rgba = im.convert("RGBA"); rgba.putalpha(alpha)
bbox = alpha.point(lambda a: 255 if a > 8 else 0).getbbox()
if bbox:
    rgba = rgba.crop((max(0, bbox[0] - 6), max(0, bbox[1] - 6), min(w, bbox[2] + 6), min(h, bbox[3] + 6)))
rgba.save(out, "PNG")
print(out, rgba.size)
