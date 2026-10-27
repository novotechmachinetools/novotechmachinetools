"""dev: cleanup + spec lines + inch annotation on pages; renders; report"""
import sys, os, time
import fitz, pdfplumber
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cleanup import clean_page
from specblock import add_us_lines
from annotate import annotate_page

CAT = "/home/claude/eurostamp/pdf/cat.pdf"
OUT = "/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad/es/cl/"
OCR_PAGES = {16, 17, 23, 27, 28, 61, 63, 64, 172, 195, 216, 228, 229, 231, 232, 237, 238, 239}
args = [a for a in sys.argv[1:] if not a.startswith("--")]
pages = []
for a in args:
    if "-" in a:
        x, y = a.split("-"); pages += list(range(int(x), int(y) + 1))
    else:
        pages.append(int(a))
doc = fitz.open(CAT)
pl = pdfplumber.open(CAT)
import eurostamp_codes
codes = eurostamp_codes.codes(doc)
rep = []
t0 = time.time()
for p in pages:
    page = doc[p - 1]
    clean_page(page, pl.pages[p - 1], report=rep)
    add_us_lines(page, None, report=rep)
    n = annotate_page(page, codes=codes, ocr=p in OCR_PAGES, report=rep)
    print(p, n, f"{time.time() - t0:.0f}s", flush=True)
    if "--png" in sys.argv:
        page.get_pixmap(dpi=100).save(OUT + f"a{p:03d}.png")
for r in rep:
    print(r)
print(len(rep), "left")
if "--save" in sys.argv:
    doc.save(OUT + "an.pdf", garbage=3, deflate=True)
