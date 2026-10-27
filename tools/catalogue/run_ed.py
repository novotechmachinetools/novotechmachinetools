"""dev: cleanup + spec lines on pages; png renders; report"""
import sys, os
import fitz, pdfplumber
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cleanup import clean_page
from specblock import add_us_lines
import specblock
if os.environ.get("SB_DEBUG"):
    specblock.DEBUG.append(1)

CAT = "/home/claude/eurostamp/pdf/cat.pdf"
OUT = "/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad/es/cl/"
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
    add_us_lines(doc[p - 1], None, report=rep)
    if "--png" in sys.argv:
        doc[p - 1].get_pixmap(dpi=100).save(OUT + f"e{p:03d}.png")
for r in rep:
    print(r)
print(len(rep), "left")
if "--save" in sys.argv:
    doc.save(OUT + "ed.pdf", garbage=3, deflate=True)
