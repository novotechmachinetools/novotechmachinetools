"""dev: contact sheets of PDF pages.  python3 sheet.py <pdf> <out.png> <pages…> [--dpi N]"""
import sys
import fitz
from PIL import Image
args = sys.argv[1:]
dpi = 60
if "--dpi" in args:
    i = args.index("--dpi"); dpi = int(args[i + 1]); del args[i:i + 2]
pdf, out, pages = args[0], args[1], []
for a in args[2:]:
    if "-" in a:
        x, y = a.split("-"); pages += list(range(int(x), int(y) + 1))
    else:
        pages.append(int(a))
doc = fitz.open(pdf)
ims = []
for p in pages:
    pix = doc[p - 1].get_pixmap(dpi=dpi)
    ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
w, h = ims[0].size
s = Image.new("RGB", (w * len(ims), h), "white")
for i, im in enumerate(ims):
    s.paste(im, (i * w, 0))
s.save(out)
