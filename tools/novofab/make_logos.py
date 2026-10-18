"""Draft 10 NovoFab Machinery logo options that share the NovoTech Machine Tools logo DNA
(split orange/grey ring with a two-letter monogram, heavy two-tone wordmark, grey tagline).
Writes novofab-01.svg … novofab-10.svg, a sheet.html and (via Playwright) sheet.png."""
import math, os, base64
OUT = os.path.dirname(os.path.abspath(__file__))
F = "/tmp/claude-0/-home-claude/c238f6cc-e8bd-5b1f-a645-cb18914b0540/scratchpad/fonts/"
FONTS = {
    "Archivo Black": F + "fontsource-archivo-black-5.3.0/package/files/archivo-black-latin-400-normal.woff2",
    "Oswald": F + "fontsource-oswald-5.3.0/package/files/oswald-latin-600-normal.woff2",
    "Barlow Condensed": F + "fontsource-barlow-condensed-5.3.0/package/files/barlow-condensed-latin-700-normal.woff2",
    "Barlow": F + "fontsource-barlow-5.3.0/package/files/barlow-latin-900-normal.woff2",
}
ORANGE, ORANGE_D, ORANGE_L = "#F28A1F", "#D4700E", "#FFB457"
GREY, GREY_D, GREY_L, CHAR = "#6E7176", "#45474B", "#A6A9AE", "#2D2E30"


def font_css():
    css = ""
    for name, path in FONTS.items():
        b = base64.b64encode(open(path, "rb").read()).decode()
        css += f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) format('woff2');}}\n"
    return css


def defs(flat=False):
    d = f"""<defs>
  <linearGradient id="gOr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ORANGE_L}"/><stop offset=".45" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_D}"/></linearGradient>
  <linearGradient id="gGr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREY_L}"/><stop offset=".5" stop-color="{GREY}"/><stop offset="1" stop-color="{GREY_D}"/></linearGradient>
  <linearGradient id="gCh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A5D62"/><stop offset="1" stop-color="{CHAR}"/></linearGradient>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="3" dy="5" stdDeviation="3" flood-color="#000" flood-opacity=".32"/></filter>
  <filter id="sh2" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="2" dy="3" stdDeviation="2" flood-color="#000" flood-opacity=".28"/></filter>
</defs>"""
    return d


def arc(cx, cy, r, a0, a1, w, fill, extra=""):
    """thick arc from angle a0 to a1 (degrees, clockwise from 12 o'clock)"""
    def pt(a, rr):
        t = math.radians(a - 90)
        return cx + rr * math.cos(t), cy + rr * math.sin(t)
    ro, ri = r + w / 2, r - w / 2
    x0, y0 = pt(a0, ro); x1, y1 = pt(a1, ro); x2, y2 = pt(a1, ri); x3, y3 = pt(a0, ri)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M{x0:.1f},{y0:.1f} A{ro},{ro} 0 {large} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} '
            f'A{ri},{ri} 0 {large} 0 {x3:.1f},{y3:.1f} Z" fill="{fill}" {extra}/>')


def ring(cx, cy, r=190, w=36, split=True, swap=False, gap=7, fx='filter="url(#sh)"', or_fill="url(#gOr)", gr_fill="url(#gGr)"):
    a, b = (gr_fill, or_fill) if swap else (or_fill, gr_fill)
    if not split:
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{a}" stroke-width="{w}" {fx}/>'
    # orange: left/bottom 150° → 345°, grey: top/right 345° → 150°  (like the NovoTech ring)
    return arc(cx, cy, r, 165 + gap, 345 - gap, w, a, fx) + arc(cx, cy, r, 345 + gap, 165 - gap + 360, w, b, fx)


def monogram(cx, cy, l1="N", l2="F", size=200, swap=False, font="Archivo Black", fx='filter="url(#sh2)"', a="url(#gOr)", b="url(#gGr)"):
    c1, c2 = (b, a) if swap else (a, b)
    return (f'<text x="{cx - size * 0.64:.0f}" y="{cy + size * 0.36:.0f}" font-family="{font}" font-size="{size}" fill="{c1}" {fx}>{l1}</text>'
            f'<text x="{cx + size * 0.2:.0f}" y="{cy + size * 0.36:.0f}" font-family="{font}" font-size="{size}" fill="{c2}" {fx}>{l2}</text>')


def wordmark(x, y, size=200, swap=False, font="Archivo Black", fx='filter="url(#sh)"', a="url(#gOr)", b="url(#gGr)", w1="Novo", w2="Fab", ls="-6"):
    c1, c2 = (b, a) if swap else (a, b)
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" letter-spacing="{ls}" {fx}>'
            f'<tspan fill="{c1}">{w1}</tspan><tspan fill="{c2}">{w2}</tspan></text>')


def tagline(x, y, text="MACHINERY", size=92, fill="url(#gGr)", font="Oswald", ls="6", fx='filter="url(#sh2)"', anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" letter-spacing="{ls}" fill="{fill}" text-anchor="{anchor}" {fx}>{text}</text>'


def svg(w, h, body, flat=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><style>{font_css()}</style>{defs(flat)}{body}</svg>'


logos = []
# 1 classic twin
logos.append(("01 Classic twin — same ring and colours as NovoTech", svg(1300, 454,
    ring(230, 227) + monogram(230, 227, size=165) + wordmark(480, 250) + tagline(486, 345))))
# 2 inverted colours
logos.append(("02 Inverted — grey Novo, orange Fab", svg(1300, 454,
    ring(230, 227, swap=True) + monogram(230, 227, size=180, swap=True) + wordmark(480, 250, swap=True) + tagline(486, 345))))
# 3 flat modern (no bevel)
logos.append(("03 Flat modern — solid colours, no 3D", svg(1300, 454,
    ring(230, 227, fx="", or_fill=ORANGE, gr_fill=GREY) + monogram(230, 227, size=180, fx="", a=ORANGE, b=CHAR) + wordmark(480, 250, fx="", a=ORANGE, b=CHAR) + tagline(486, 345, fill=GREY, fx=""))))
# 4 stacked
logos.append(("04 Stacked — ring above the wordmark", svg(900, 900,
    ring(450, 250, r=165, w=32) + monogram(450, 250, size=160) + wordmark(450, 640, size=170, ls="-5").replace('x="450"', 'x="450" text-anchor="middle"') + tagline(450, 740, size=78, anchor="middle"))))
# 5 hex badge
def hexagon(cx, cy, r, w, fx='filter="url(#sh)"'):
    pts = [(cx + r * math.cos(math.radians(60 * i - 30)), cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    # left half orange, right half grey via clip
    return (f'<defs><clipPath id="hl"><rect x="{cx - r - 40}" y="{cy - r - 40}" width="{r + 40}" height="{2 * r + 80}"/></clipPath><clipPath id="hr"><rect x="{cx}" y="{cy - r - 40}" width="{r + 40}" height="{2 * r + 80}"/></clipPath></defs>'
            f'<path d="{d}" fill="none" stroke="url(#gOr)" stroke-width="{w}" stroke-linejoin="round" clip-path="url(#hl)" {fx}/>'
            f'<path d="{d}" fill="none" stroke="url(#gGr)" stroke-width="{w}" stroke-linejoin="round" clip-path="url(#hr)" {fx}/>')
logos.append(("05 Hex badge — nut-shaped mark", svg(1300, 454,
    hexagon(230, 227, 200, 34) + monogram(230, 227, size=175) + wordmark(480, 250) + tagline(486, 345))))
# 6 gear ring
def gear(cx, cy, r=186, w=30, teeth=24, th=16, fx='filter="url(#sh)"'):
    out = ""
    for i in range(teeth):
        a = 360 / teeth * i
        col = "url(#gOr)" if 150 <= a < 345 else "url(#gGr)"
        t = math.radians(a - 90)
        x0, y0 = cx + (r + w / 2 - 2) * math.cos(t), cy + (r + w / 2 - 2) * math.sin(t)
        x1, y1 = cx + (r + w / 2 + th) * math.cos(t), cy + (r + w / 2 + th) * math.sin(t)
        out += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="16" stroke-linecap="butt"/>'
    return out + ring(cx, cy, r=r, w=w, fx=fx, gap=4)
logos.append(("06 Gear ring — toothed ring", svg(1300, 454,
    gear(230, 227) + monogram(230, 227, size=165) + wordmark(480, 250) + tagline(486, 345))))
# 7 full orange ring, charcoal wordmark, orange tagline
logos.append(("07 Orange ring — charcoal wordmark, orange tagline", svg(1300, 454,
    ring(230, 227, split=False, or_fill="url(#gOr)") + f'<circle cx="230" cy="227" r="160" fill="none" stroke="url(#gGr)" stroke-width="6"/>'
    + monogram(230, 227, size=170, a="url(#gCh)", b="url(#gOr)") + wordmark(480, 250, a="url(#gCh)", b="url(#gCh)") + tagline(486, 345, fill="url(#gOr)"))))
# 8 double ring
logos.append(("08 Double ring — thin grey outer, orange inner", svg(1300, 454,
    f'<circle cx="230" cy="227" r="205" fill="none" stroke="url(#gGr)" stroke-width="14" filter="url(#sh2)"/>' + ring(230, 227, r=168, w=26, gap=6)
    + monogram(230, 227, size=155) + wordmark(480, 250) + tagline(486, 345))))
# 9 rounded-square app mark
logos.append(("09 Square mark — orange tile with white NF", svg(1300, 454,
    f'<rect x="40" y="37" width="380" height="380" rx="70" fill="url(#gOr)" filter="url(#sh)"/><rect x="40" y="37" width="190" height="380" rx="70" fill="url(#gGr)" opacity=".0"/>'
    + f'<path d="M230,37 h120 a70,70 0 0 1 70,70 v240 a70,70 0 0 1 -70,70 h-120 z" fill="url(#gGr)" opacity=".92"/>'
    + monogram(230, 227, size=180, a="#fff", b="#fff", fx='filter="url(#sh2)"') + wordmark(480, 250) + tagline(486, 345))))
# 10 charcoal mono with orange accent, Barlow Condensed wordmark
logos.append(("10 Charcoal — condensed wordmark, orange Fab only", svg(1300, 454,
    ring(230, 227, or_fill="url(#gOr)", gr_fill="url(#gCh)") + monogram(230, 227, a="url(#gCh)", b="url(#gOr)", font="Barlow Condensed", size=250)
    + wordmark(480, 262, size=250, font="Barlow Condensed", a="url(#gCh)", b="url(#gOr)", ls="-2") + tagline(486, 350, fill="url(#gCh)", font="Barlow Condensed", size=96, ls="8"))))

cards = ""
for i, (title, s) in enumerate(logos, 1):
    open(os.path.join(OUT, f"novofab-{i:02d}.svg"), "w", encoding="utf-8").write(s)
    cards += f'<div class="card"><div class="t">{title}</div><div class="l">{s}</div></div>'
html = f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#eceef0;font-family:Arial,sans-serif}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:18px}}
.card{{background:#fff;border:1px solid #d7d9dc;border-radius:10px;padding:14px 18px}}
.t{{font:700 17px Arial;color:#2D2E30;margin-bottom:8px}}
.l svg{{width:100%;height:auto;max-height:230px}} .card:nth-child(4) .l svg{{max-height:330px}}
</style><div class="grid">{cards}</div>"""
open(os.path.join(OUT, "sheet.html"), "w", encoding="utf-8").write(html)
print("ok", len(logos))
