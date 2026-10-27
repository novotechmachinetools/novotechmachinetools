"""dev: run the line-by-line cleanup on catalogue pages, render them, print what was left"""
import sys, os
import fitz, pdfplumber
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cleanup import clean_page

CAT = "/home/claude/eurostamp/pdf/cat.pdf"
OUT = "/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad/es/cl/"
os.makedirs(OUT, exist_ok=True)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
pages = []
for a in args:
    if "-" in a:
        x, y = a.split("-"); pages += list(range(int(x), int(y) + 1))
    else:
        pages.append(int(a))
doc = fitz.open(CAT)
pl = pdfplumber.open(CAT)
rep = []
for p in pages:
    clean_page(doc[p - 1], pl.pages[p - 1], report=rep)
    if "--png" in sys.argv:
        doc[p - 1].get_pixmap(dpi=100).save(OUT + f"c{p:03d}.png")
for r in rep:
    print(r)
print(len(rep), "left")
if "--save" in sys.argv:
    doc.save(OUT + "clean.pdf", garbage=3, deflate=True)
