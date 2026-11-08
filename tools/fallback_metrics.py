#!/usr/bin/env python3
"""Metric-matched fallback fonts: measure how wide the site's text renders in Barlow / Barlow Condensed versus the local
fonts the browser shows while the woff2 files load (Arial = Liberation Sans on Linux, Roboto on Android, DejaVu Sans on
bare Linux), and print the @font-face lines for src/css/site.css.

    python3 tools/fallback_metrics.py            # needs dist/*.html (python3 build.py first), fontTools and Pillow

size-adjust = total Barlow advance width / total fallback advance width over every heading, paragraph, list item,
button and table cell of the built site, per weight — so a line of fallback text is as long as the same line in
Barlow and wraps at the same word.  ascent/descent overrides = Barlow's 1000 / -200 metrics divided by size-adjust.
Why not `ch` widths: Barlow's "0" is wider than its average glyph, so a max-width in ch is ~6 % narrower while the
fallback shows; the CSS therefore uses em (Barlow zero advance: 0.565em at 400, 0.453em condensed 700)."""
import glob, io, os, re, sys
from html.parser import HTMLParser
from fontTools.ttLib import TTFont
from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FONTS = os.path.join(ROOT, "src", "fonts")
SYS = {"lib_r": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
       "lib_b": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
       "dv_r": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
       "dv_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
       "rob_r": os.path.join(ROOT, "tools", "fonts", "Roboto-Regular.ttf"),
       "rob_b": os.path.join(ROOT, "tools", "fonts", "Roboto-Bold.ttf")}

def barlow(name):
    """woff2 from src/fonts -> TTF bytes Pillow can read."""
    t = TTFont(os.path.join(SRC_FONTS, name + ".woff2")); t.flavor = None
    buf = io.BytesIO(); t.save(buf); buf.seek(0); return buf

class Corpus(HTMLParser):
    KEYS = ("h1", "h2", "h3", "p", "li", "th", "td", "strong", "summary", "a", "button")
    def __init__(self):
        super().__init__(); self.open = []; self.skip = 0; self.out = {k: [] for k in self.KEYS}
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "template"): self.skip += 1
        self.open.append((tag, [] if tag in self.KEYS else None))
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "template"): self.skip = max(0, self.skip - 1)
        while self.open:
            t, parts = self.open.pop()
            if parts is not None:
                txt = re.sub(r"\s+", " ", "".join(parts)).strip()
                if txt: self.out[t].append(txt)
                for _, up in reversed(self.open):
                    if up is not None: up.append(" " + "".join(parts) + " "); break
            if t == tag: break
    def handle_data(self, d):
        if self.skip: return
        for _, parts in reversed(self.open):
            if parts is not None: parts.append(d); break

def corpus():
    c = Corpus()
    files = glob.glob(os.path.join(ROOT, "dist", "*.html"))
    if not files: sys.exit("dist/*.html missing — run python3 build.py first")
    for f in files: c.feed(open(f, encoding="utf-8").read())
    return {k: sorted(set(v)) for k, v in c.out.items()}

def ratio(web, local, items):
    fw, fl = ImageFont.truetype(web, 100), ImageFont.truetype(local, 100)
    pairs = [(fw.getlength(t), fl.getlength(t)) for t in items]
    return sum(a for a, _ in pairs) / sum(b for _, b in pairs)

def main():
    C = corpus()
    body = C["p"] + C["li"] + C["td"]                       # Barlow 400 (and 500-700 for strong/labels)
    cond6 = C["h3"] + C["th"] + C["summary"] + C["a"] + C["button"]   # Barlow Condensed 600: nav, chips, buttons, table heads, h3
    cond7 = C["h1"] + C["h2"]                                # Barlow Condensed 700: headings
    print(f"corpus: {len(body)} body strings, {len(cond6)} condensed-600 strings, {len(cond7)} headings\n")
    faces = [  # (css family, weight, [local() names], web font, local file, corpus)
        ("Barlow Fallback", "400", ['Arial', 'ArialMT', 'Helvetica', 'Liberation Sans'], "barlow-latin-400-normal", "lib_r", body),
        ("Barlow Fallback", "500", ['Arial Bold', 'Arial-BoldMT', 'Arial', 'Helvetica', 'Liberation Sans Bold'], "barlow-latin-500-normal", "lib_b", body),
        ("Barlow Fallback", "600", ['Arial Bold', 'Arial-BoldMT', 'Arial', 'Helvetica', 'Liberation Sans Bold'], "barlow-latin-600-normal", "lib_b", body),
        ("Barlow Fallback", "700", ['Arial Bold', 'Arial-BoldMT', 'Arial', 'Helvetica', 'Liberation Sans Bold'], "barlow-latin-700-normal", "lib_b", C["strong"] + body),
        ("Barlow Condensed Fallback", "500", ['Arial Bold', 'Arial-BoldMT', 'Arial', 'Helvetica', 'Liberation Sans Bold'], "barlow-condensed-latin-500-normal", "lib_b", cond6),
        ("Barlow Condensed Fallback", "600", ['Arial Bold', 'Arial-BoldMT', 'Arial', 'Helvetica', 'Liberation Sans Bold'], "barlow-condensed-latin-600-normal", "lib_b", cond6),
        ("Barlow Condensed Fallback", "700", ['Arial Bold', 'Arial-BoldMT', 'Arial', 'Helvetica', 'Liberation Sans Bold'], "barlow-condensed-latin-700-normal", "lib_b", cond7),
        ("Barlow Fallback R", "400", ['Roboto', 'Roboto-Regular'], "barlow-latin-400-normal", "rob_r", body),
        ("Barlow Fallback R", "500 700", ['Roboto Bold', 'Roboto-Bold'], "barlow-latin-600-normal", "rob_b", body),
        ("Barlow Condensed Fallback R", "500 600", ['Roboto Bold', 'Roboto-Bold'], "barlow-condensed-latin-600-normal", "rob_b", cond6),
        ("Barlow Condensed Fallback R", "700", ['Roboto Bold', 'Roboto-Bold'], "barlow-condensed-latin-700-normal", "rob_b", cond7),
        ("Barlow Fallback D", "400", ['DejaVu Sans'], "barlow-latin-400-normal", "dv_r", body),
        ("Barlow Fallback D", "500 700", ['DejaVu Sans Bold'], "barlow-latin-600-normal", "dv_b", body),
        ("Barlow Condensed Fallback D", "500 600", ['DejaVu Sans Bold'], "barlow-condensed-latin-600-normal", "dv_b", cond6),
        ("Barlow Condensed Fallback D", "700", ['DejaVu Sans Bold'], "barlow-condensed-latin-700-normal", "dv_b", cond7),
    ]
    for fam, w, locals_, web, loc, items in faces:
        if not os.path.exists(SYS[loc]): print(f"/* {fam} {w}: {SYS[loc]} not installed */"); continue
        sa = round(ratio(barlow(web), SYS[loc], items) * 100, 2)
        src = ", ".join(f'local("{n}")' for n in locals_)
        print(f'@font-face {{ font-family: "{fam}"; font-weight: {w}; src: {src}; size-adjust: {sa:g}%; '
              f'ascent-override: {100 / sa * 100:.2f}%; descent-override: {20 / sa * 100:.2f}%; line-gap-override: 0%; }}')
    print("\nBarlow zero advance (for em measures):")
    for n in ("barlow-latin-400-normal", "barlow-latin-500-normal", "barlow-condensed-latin-700-normal"):
        t = TTFont(os.path.join(SRC_FONTS, n + ".woff2")); adv = t["hmtx"][t.getBestCmap()[ord("0")]][0]
        print(f"  {n}: {adv / t['head'].unitsPerEm:.3f}em per ch")

if __name__ == "__main__":
    main()
