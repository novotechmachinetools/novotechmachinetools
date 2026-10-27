"""dev: process one page and render a zoomed clip.  python3 zoom.py PAGE x0 y0 x1 y1 [dpi] [name]"""
import os, sys
import fitz, pdfplumber
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edition as E, eurostamp_codes
p = int(sys.argv[1]); r = fitz.Rect(*map(float, sys.argv[2:6]))
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 250
name = sys.argv[7] if len(sys.argv) > 7 else f"z{p:03d}"
doc = fitz.open(E.CAT); pl = pdfplumber.open(E.CAT)
rep = []
E.process(doc[p - 1], pl.pages[p - 1], eurostamp_codes.codes(doc), rep)
doc[p - 1].get_pixmap(dpi=dpi, clip=r).save(f"/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad/ed2/{name}.png")
for x in rep: print(x)
