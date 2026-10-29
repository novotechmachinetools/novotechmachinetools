#!/usr/bin/env python3
"""Air-bending force: the EUROSTAMP formula and chart as the one source for every tonnage figure on the site.

    F (t/m) = S² × 2 × R ÷ (1.4 × V)        S sheet thickness mm, V die opening mm, R tensile strength kg/mm²

EUROSTAMP's printed mild-steel chart is this formula with R = 47 kg/mm² (every bold cell: 6 mm in V 50 = 48 t/m, 12 mm in
V 100 = 97, 25 mm in V 200 = 210); its stainless chart uses R = 70, aluminum 20 – 25.  In inches and US tons per foot the
same formula with R = 47 is 575 × t² ÷ V — the imperial rule the guide used before — so the figures agree; this module just
makes metric and imperial sit side by side and drives the calculator (src/js/site.js, #bend-calc).

The standard V opening follows EUROSTAMP's thickness / V ratio: 6 × S up to 2.5 mm, 8 × S from 3 to 8 mm, 10 × S at 9 – 10 mm,
12 × S from 12 mm, rounded to the nearest die in the EUROSTAMP range.  Minimum flange B ≈ 0.7 × V, inside radius Ri ≈ V ÷ 6.

    python3 tools/press_brake_tonnage.py        → rewrites the table between the markers in content/articles/press-brake-guide.html
"""
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE = os.path.join(ROOT, "content", "articles", "press-brake-guide.html")

R = {"mild": 47.0, "stainless": 70.0, "aluminum": 25.0}
DIES = [6, 8, 10, 12, 14, 16, 18, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320]
US_T_PER_FT = 1.1023113 / 3.2808399      # 1 t/m in US tons per foot
LEN_10FT = 3.048
RESERVE = 1.2                             # the machine is chosen 20 % above the heaviest bend


def ratio(s):
    return 6 if s <= 2.5 else 8 if s < 9 else 10 if s <= 10 else 12


def standard_v(s):
    want = ratio(s) * s
    return min(DIES, key=lambda d: (abs(d - want), d))


def force_tm(s, v, r=R["mild"]):
    return s * s * 2 * r / (1.4 * v)


def round_up(x, step):
    return int(math.ceil(x / step) * step)


# (label, thickness mm) — North American gauges and fractions with the metric sizes between them
ROWS = [("20 ga", 0.9), ("1 mm", 1.0), ("16 ga", 1.5), ("14 ga", 1.9), ("2 mm", 2.0), ("12 ga", 2.7), ("3 mm", 3.0), ("10 ga", 3.4),
        ("4 mm", 4.0), ("3/16″", 4.76), ("5 mm", 5.0), ("6 mm", 6.0), ("1/4″", 6.35), ("8 mm", 8.0), ("5/16″", 7.94), ("3/8″", 9.53),
        ("10 mm", 10.0), ("12 mm", 12.0), ("1/2″", 12.7), ("16 mm", 16.0), ("5/8″", 15.88), ("3/4″", 19.05), ("20 mm", 20.0), ("1″", 25.4)]
ROWS.sort(key=lambda r: r[1])


def inch(mm):
    return f"{mm / 25.4:.3f}″"


def row_html(label, s):
    v = standard_v(s)
    f = force_tm(s, v)
    ft = f * US_T_PER_FT
    total = f * LEN_10FT
    machine = round_up(total * RESERVE, 5)
    return (f'<tr><th scope="row">{label}<small>{s:g} mm · {inch(s)}</small></th>'
            f'<td>{v} mm<small>{v / 25.4:.2f}″</small></td>'
            f'<td>{f:.0f} t/m</td><td>{ft:.1f} US t/ft</td>'
            f'<td>{total:.0f} t<small>{total * 1.1023113:.0f} US tons</small></td>'
            f'<td><strong>{machine} t</strong><small>{machine * 1.1023113:.0f} US tons</small></td></tr>')


def table_html():
    head = ('<div class="table-scroll" tabindex="0" aria-label="Press brake tonnage, mild steel, 90° air bending">'
            '<table class="spec-table guide-table tonnage-guide"><caption>Air bending at 90°, mild steel (47 kg/mm², 67,000 psi) — EUROSTAMP formula and standard V '
            '<small>Force for the bend, then the press brake to choose for a 10 ft (3,050 mm) bend with 20 % in reserve. Stainless: × 1.5. Aluminum: × 0.55.</small></caption>'
            '<thead><tr><th scope="col" class="label-col">Thickness</th><th scope="col">V opening<small>≈ 8 × thickness</small></th><th scope="col">Force per metre</th>'
            '<th scope="col">Force per foot</th><th scope="col">10 ft bend<small>3,050 mm</small></th><th scope="col">Press brake to choose<small>+20 % reserve</small></th></tr></thead><tbody>')
    return head + "".join(row_html(l, s) for l, s in ROWS) + "</tbody></table></div>"


def main():
    html = open(GUIDE, encoding="utf-8").read()
    start, end = "<!-- tonnage-table -->", "<!-- /tonnage-table -->"
    if start not in html:
        raise SystemExit("markers not found in the guide")
    new = re.sub(re.escape(start) + ".*?" + re.escape(end), start + table_html() + end, html, flags=re.S)
    open(GUIDE, "w", encoding="utf-8").write(new)
    print(f"tonnage table: {len(ROWS)} rows")
    for s, v in ((6.0, 50), (6.35, 50.8), (12.0, 100), (25.0, 200)):
        print(f"  check S={s} V={v}: {force_tm(s, v):.1f} t/m · {force_tm(s, v) * US_T_PER_FT:.1f} US t/ft")


if __name__ == "__main__":
    main()
