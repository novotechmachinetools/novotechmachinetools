"""dev: the distinct text lines (not bare numbers) of catalogue pages, normalised as it_en.norm() sees them"""
import re, sys
import fitz
from survey import page_lines
from it_en import norm
doc = fitz.open("/home/claude/eurostamp/pdf/cat.pdf")
pages = []
for a in sys.argv[1:]:
    if "-" in a:
        x, y = a.split("-"); pages += list(range(int(x), int(y) + 1))
    else:
        pages.append(int(a))
for p in pages:
    seen = []
    for L in page_lines(doc[p - 1]):
        t = norm(L["t"])
        if re.fullmatch(r"[\d\s.,x×/=RØ°-]*(mm|kg)?", t) or t in seen:
            continue
        seen.append(t)
    print(f"--- {p}: " + " | ".join(seen))
