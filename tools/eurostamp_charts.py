#!/usr/bin/env python3
"""EUROSTAMP air-bending force charts for the press brake buying guide (the owner's request of Oct 29 2026): the diagram
(F, S, Ri, B, V), the legend and the formula in English, then the mild-steel and the stainless-steel chart of the EUROSTAMP
catalogue, each in its original metric form and converted to inches — four charts.

The charts are transcribed from the catalogue page cell by cell (they are not the bare formula: EUROSTAMP rounds and corrects
the narrow-V cells).  One printed cell is corrected: stainless 8 mm in V 50 reads 208 in the catalogue, while the mild-steel
chart (85 × 1.5) and its neighbours (102 in V 63) give 128.  The inch charts convert every value: thickness, V, B and Ri to
inches, the force from tonnes per metre to US tons per foot (× 0.336).

    python3 tools/eurostamp_charts.py     → rewrites the block between <!-- force-charts --> markers in content/articles/press-brake-guide.html
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE = os.path.join(ROOT, "content", "articles", "press-brake-guide.html")
T_PER_M_TO_USTON_PER_FT = 1.1023113 / 3.2808399

# V opening (mm): (B shortest flange mm, Ri inside radius mm)
VBR = [(6, 4, 1), (8, 5.5, 1.3), (10, 7, 1.6), (12, 8.5, 2), (14, 10, 2.3), (16, 11, 2.6), (18, 13.5, 3), (20, 14, 3.3), (25, 17.5, 4),
       (32, 22, 5), (40, 28, 6.5), (50, 35, 8), (63, 45, 10), (80, 55, 13), (100, 71, 16), (125, 89, 20), (160, 113, 26), (200, 140, 33),
       (250, 175, 41)]

# force in t/m by V (mm) and thickness S (mm); "*" marks the catalogue's highlighted cell
MILD = {
    "cols": [0.5, 0.6, 0.8, 1, 1.2, 1.5, 2, 2.5, 3, 4, 4.5, 5, 6, 8, 10, 12, 15, 20, 25, 30],
    6: "0.5:3 0.6:4 0.8:7* 1:11", 8: "0.6:4 0.8:5 1:8* 1.2:12 1.5:20", 10: "0.8:4 1:7 1.2:10* 1.5:17", 12: "1:6 1.2:8 1.5:15* 2:22",
    14: "1.2:7 1.5:13* 2:19", 16: "1.2:6 1.5:11 2:17* 2.5:28", 18: "1.5:10 2:15 2.5:25* 3:34", 20: "1.5:9 2:13 2.5:22* 3:30",
    25: "2:11 2.5:18 3:24* 4:43", 32: "2.5:14 3:19 4:34* 4.5:44 5:52", 40: "3:15 4:27 4.5:34 5:42* 6:60 8:107",
    50: "4:21 4.5:27 5:33 6:48* 8:85", 63: "4:17 4.5:21 5:26 6:38 8:68* 10:105", 80: "5:21 6:30 8:53 10:85* 12:120",
    100: "6:24 8:43 10:67 12:96 15:150", 125: "10:53 12:78* 15:120 20:215", 160: "10:42 12:60 15:95* 20:170",
    200: "12:55 15:75 20:135* 25:210", 250: "20:108 25:170* 30:240",
}
STAINLESS = {
    "cols": [0.5, 0.6, 0.8, 0.9, 1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30],
    6: "0.5:5 0.6:6 0.8:11* 0.9:13 1:17", 8: "0.6:6 0.8:8 0.9:10 1:12* 1.2:18", 10: "0.8:7 0.9:8 1:11 1.2:15*", 12: "0.9:7 1:8 1.2:12 1.5:20* 2:33",
    14: "1.2:11 1.5:17* 2:29", 16: "1.2:9 1.5:15 2:26* 2.5:39", 18: "1.5:13 2:23 2.5:35* 3:51", 20: "1.5:12 2:20 2.5:30* 3:45",
    25: "2:17 2.5:25 3:36* 4:65", 32: "2.5:19 3:29 4:51* 5:78", 40: "3:23 4:41 5:63* 6:90",
    50: "4:32 5:50 6:72* 8:128", 63: "4:26 5:39 6:57 8:102* 10:163", 80: "5:32 6:45 8:81 10:129* 12:187",
    100: "6:36 8:65 10:101* 12:144", 125: "8:51 10:80 12:117* 15:180", 160: "10:63 12:90 15:141* 20:250",
    200: "12:83 15:114 20:208* 25:315", 250: "20:167 25:255* 30:360",
}


def parse(chart):
    rows = {}
    for v, _, _ in VBR:
        cells = {}
        for tok in chart[v].split():
            s, f = tok.split(":")
            cells[float(s)] = (int(f.rstrip("*")), f.endswith("*"))
        rows[v] = cells
    return rows


def num(x):
    """1 → '1', 1.5 → '1.5'"""
    return f"{x:g}"


def inch(mm, d=2):
    return f"{mm / 25.4:.{d}f}"


def us_t_ft(t_m):
    v = t_m * T_PER_M_TO_USTON_PER_FT
    return f"{v:.1f}" if v < 10 else f"{v:.0f}"


def chart_html(chart, title, imperial, note=""):
    rows = parse(chart)
    cols = chart["cols"]
    unit_s = "in" if imperial else "mm"
    unit_f = "US tons per foot" if imperial else "tonnes per metre (t/m)"
    head = "".join(f'<th scope="col">{inch(s, 3) if imperial else num(s)}</th>' for s in cols)
    body = []
    for v, b, ri in VBR:
        cells = rows[v]
        rec = [i for i, s in enumerate(cols) if s in cells and cells[s][1]]
        tds = []
        for i, s in enumerate(cols):
            if s not in cells:
                tds.append("<td></td>")
                continue
            f, star = cells[s]
            cls = "is-rec" if star else ("is-near" if rec and abs(i - rec[0]) == 1 else "")
            val = us_t_ft(f) if imperial else str(f)
            tds.append(f'<td class="{cls}">{val}</td>' if cls else f"<td>{val}</td>")
        vv, bb, rr = (inch(v), inch(b), inch(ri)) if imperial else (num(v), num(b), num(ri))
        body.append(f'<tr><th scope="row">{vv}</th><td class="fc-side">{bb}</td><td class="fc-side">{rr}</td>{"".join(tds)}</tr>')
    cap = (f'{title} <small>Thickness S across the top ({unit_s}); V opening, shortest flange B and inside radius Ri down the side ({unit_s}); '
           f'force F in {unit_f} in the cells.{(" " + note) if note else ""}</small>')
    return (f'<div class="table-scroll" tabindex="0" aria-label="{title}"><table class="force-chart{" is-inch" if imperial else ""}">'
            f'<caption>{cap}</caption><thead><tr><th scope="col" class="fc-key">V</th><th scope="col" class="fc-key">B</th>'
            f'<th scope="col" class="fc-key">Ri</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


DIAGRAM = """<svg class="bend-diagram" viewBox="0 0 360 445" role="img" aria-labelledby="bend-diagram-t">
<title id="bend-diagram-t">Air bending: the punch presses the sheet into the V opening of the die. F force, S sheet thickness, Ri inside radius, B shortest flange, V die opening.</title>
<line x1="180" y1="8" x2="180" y2="440" class="bd-axis"/>
<path class="bd-die" d="M92 300 H120 L180 382 L240 300 H268 V432 H92 Z"/>
<path class="bd-sheet" d="M50 230 L172.9 352.9 Q180 360 187.1 352.9 L262 278 L254.9 270.9 L185.7 340.2 Q180 345.9 174.3 340.2 L57.1 222.9 Z"/>
<path class="bd-punch" d="M136 72 H224 V210 L184.5 338 Q180 346.5 175.5 338 L136 210 Z"/>
<line x1="180" y1="14" x2="180" y2="54" class="bd-force"/><path class="bd-force-head" d="M170 50 H190 L180 68 Z"/>
<text x="194" y="40" class="bd-label">F</text>
<line x1="70" y1="290" x2="88" y2="272" class="bd-dim"/><path class="bd-head" d="M90.6 269.4 L80.5 274.1 L85.9 279.5 Z"/>
<line x1="117" y1="243" x2="99" y2="261" class="bd-dim"/><path class="bd-head" d="M96.4 263.6 L106.5 258.9 L101.1 253.5 Z"/>
<text x="112" y="236" class="bd-label">S</text>
<line x1="228" y1="268" x2="188" y2="336" class="bd-dim"/><path class="bd-head" d="M185.5 340.5 L187.4 329.6 L194 333.5 Z"/>
<text x="219" y="262" class="bd-label">Ri</text>
<line x1="180" y1="360" x2="199" y2="379" class="bd-ext"/><line x1="262" y1="278" x2="281" y2="297" class="bd-ext"/>
<line x1="198.5" y1="371.5" x2="273.5" y2="296.5" class="bd-dim"/>
<path class="bd-head" d="M194.6 375.4 L199.3 365.3 L204.7 370.7 Z"/><path class="bd-head" d="M277.4 292.6 L272.7 302.7 L267.3 297.3 Z"/>
<text x="246" y="352" class="bd-label">B</text>
<line x1="120" y1="300" x2="120" y2="418" class="bd-ext"/><line x1="240" y1="300" x2="240" y2="418" class="bd-ext"/>
<line x1="126" y1="410" x2="234" y2="410" class="bd-dim"/>
<path class="bd-head" d="M120 410 L131 404.5 V415.5 Z"/><path class="bd-head" d="M240 410 L229 404.5 V415.5 Z"/>
<text x="171" y="402" class="bd-label">V</text>
</svg>"""

LEGEND = """<dl class="bend-legend">
<div><dt>S</dt><dd>Sheet thickness</dd></div>
<div><dt>V</dt><dd>V opening of the die</dd></div>
<div><dt>F</dt><dd>Bending force — tonnes per metre or US tons per foot of bend</dd></div>
<div><dt>B</dt><dd>Shortest flange the V can hold</dd></div>
<div><dt>Ri</dt><dd>Inside radius of the bend</dd></div>
<div><dt>R</dt><dd>Tensile strength: aluminum 20 – 25 kg/mm² (28,000 – 36,000 psi) · mild steel 40 – 45 kg/mm² (57,000 – 64,000 psi) · stainless steel 65 – 70 kg/mm² (92,000 – 100,000 psi)</dd></div>
</dl>
<div class="bend-formula">
<p><span class="bf-f">F</span> = <span class="bf-frac"><span>S² × 2 × R</span><span>1.4 × V</span></span> = … t/m <small>S and V in mm, R in kg/mm²</small></p>
<p><span class="bf-f">F</span> = <span class="bf-frac"><span>575 × S²</span><span>V</span></span> = … US tons/ft <small>mild steel, S and V in inches; × 1.5 for stainless, × 0.55 for aluminum</small></p>
</div>"""


def block():
    note_ss = ("8 mm in V 50 is corrected to 128 t/m: the catalogue prints 208, while the mild-steel value × 1.5 and the "
               "neighbouring cells give 128.")
    note_ss_in = ("0.315″ in V 1.97″ is corrected to 43 US tons/ft: the catalogue prints 208 t/m, while the mild-steel value × 1.5 "
                  "and the neighbouring cells give 128 t/m (43 US tons/ft).")
    return "\n".join([
        '<h4 id="air-bending-force-charts">Air bending force — the EUROSTAMP charts</h4>',
        "<p>The charts below are EUROSTAMP's own tables for a 90° air bend: pick the V opening in the left column and the thickness across "
        "the top, and the cell gives the force per metre or per foot of bend. The highlighted cells mark the V that EUROSTAMP recommends "
        "for each thickness; the shaded cells beside them still work, with more force or a larger radius. Each chart is shown as printed "
        "in the catalogue (metric) and converted to inches.</p>",
        f'<div class="bend-diagram-row"><figure class="bend-figure">{DIAGRAM}<figcaption>Air bending: the punch pushes the sheet into the V '
        f'opening; the shoulders of the die carry it.</figcaption></figure><div class="bend-key">{LEGEND}</div></div>',
        chart_html(MILD, "Mild steel — metric (EUROSTAMP chart)", False),
        chart_html(MILD, "Mild steel — inch", True),
        chart_html(STAINLESS, "Stainless steel — metric (EUROSTAMP chart)", False, note_ss),
        chart_html(STAINLESS, "Stainless steel — inch", True, note_ss_in),
    ])


def main():
    html = open(GUIDE, encoding="utf-8").read()
    start, end = "<!-- force-charts -->", "<!-- /force-charts -->"
    if start not in html:
        raise SystemExit("markers not found in the guide")
    html = re.sub(re.escape(start) + ".*?" + re.escape(end), lambda m: start + "\n" + block() + "\n" + end, html, flags=re.S)
    open(GUIDE, "w", encoding="utf-8").write(html)
    print("force charts: 4 tables,", sum(len(MILD[v].split()) for v, _, _ in VBR) + sum(len(STAINLESS[v].split()) for v, _, _ in VBR), "cells")


if __name__ == "__main__":
    main()
