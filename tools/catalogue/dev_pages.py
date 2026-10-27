"""dev: run the full edition steps (handlers, cleanup, US t/ft, inch values, POST, logo) on some pages; PNG renders
python3 dev_pages.py 16 17 92-96 [--dpi 110] [--out DIR] [--save name.pdf]"""
import os
import sys
import time

import fitz
import pdfplumber

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edition as E                     # noqa: E402
import eurostamp_codes                  # noqa: E402

args = sys.argv[1:]
dpi, out, save = 110, "/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad/ed2", None
if "--dpi" in args:
    i = args.index("--dpi"); dpi = int(args[i + 1]); del args[i:i + 2]
if "--out" in args:
    i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
if "--save" in args:
    i = args.index("--save"); save = args[i + 1]; del args[i:i + 2]
pages = E.parse_pages(",".join(args))
os.makedirs(out, exist_ok=True)
doc = fitz.open(E.CAT)
pl = pdfplumber.open(E.CAT)
codes = eurostamp_codes.codes(doc)
rep = []
t0 = time.time()
for p in pages:
    n = E.process(doc[p - 1], pl.pages[p - 1], codes, rep)
    print(p, n, f"{time.time() - t0:.0f}s", flush=True)
    doc[p - 1].get_pixmap(dpi=dpi).save(os.path.join(out, f"p{p:03d}.png"))
for r in rep:
    print(r)
print(len(rep), "left")
if save:
    o = fitz.open()
    for p in pages:
        o.insert_pdf(doc, from_page=p - 1, to_page=p - 1)
    o.save(os.path.join(out, save), garbage=3, deflate=True)
