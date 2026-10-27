"""print the text lines of catalogue pages with position, font, size, colour and language (dev aid)"""
import sys
import fitz
from lang import text_lang

CAT = "/home/claude/eurostamp/pdf/cat.pdf"


def page_lines(page):
    out = []
    raw = page.get_text("rawdict")
    for b in raw["blocks"]:
        for l in b.get("lines", []):
            t = "".join(c["c"] for s in l["spans"] for c in s["chars"])
            if not t.strip():
                continue
            fonts = sorted({s["font"].split("+")[-1] for s in l["spans"] if "".join(c["c"] for c in s["chars"]).strip()})
            size = max(s["size"] for s in l["spans"])
            col = l["spans"][0]["color"]
            out.append(dict(t=t, bbox=fitz.Rect(l["bbox"]), dir=tuple(round(x, 3) for x in l["dir"]), fonts=fonts, size=size,
                            color=col, lang=text_lang(t), block=b["number"]))
    return out


if __name__ == "__main__":
    doc = fitz.open(CAT)
    only_it = "--it" in sys.argv
    for a in sys.argv[1:]:
        if a.startswith("--"):
            continue
        p = int(a)
        print(f"=== page {p}")
        for L in page_lines(doc[p - 1]):
            if only_it and L["lang"] not in ("it", "mixed"):
                continue
            r = L["bbox"]
            print(f"  [{L['lang'] or '-':5}] b{L['block']:<3} ({r.x0:5.1f},{r.y0:5.1f},{r.x1:5.1f},{r.y1:5.1f}) {L['size']:4.1f} {'/'.join(f.replace('Roboto', 'R') for f in L['fonts'])[:38]:38} {L['t'][:90]!r}")
