"""Ten variations on option 01 (classic twin of the NovoTech logo). Canvas widened so the wordmark never clips."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_logos import *   # ring, monogram, wordmark, tagline, svg, colours, font_css
OUT = os.path.dirname(os.path.abspath(__file__))
W = 1420

def classic(mono_size=180, word_size=200, word_font="Archivo Black", tag_fill="url(#gGr)", tag_font="Oswald", tag_ls="6",
            ring_w=36, ring_r=190, gap=7, word_x=480, extra="", swap=False, a="url(#gOr)", b="url(#gGr)", tag_size=92, tag_y=345, word_y=250, ring_kw=None, ls="-6"):
    rk = dict(r=ring_r, w=ring_w, gap=gap, swap=swap); rk.update(ring_kw or {})
    return (ring(230, 227, **rk) + monogram(230, 227, size=mono_size, swap=swap, a=a, b=b)
            + wordmark(word_x, word_y, size=word_size, font=word_font, swap=swap, a=a, b=b, ls=ls)
            + tagline(word_x + 6, tag_y, size=tag_size, fill=tag_fill, font=tag_font, ls=tag_ls) + extra)

L = []
L.append(("1A Baseline — option 01, complete wordmark", svg(W, 454, classic())))
L.append(("1B Metallic — stronger bevel with highlight edges", svg(W, 454, classic().replace('filter="url(#sh)"', 'filter="url(#sh)" stroke="#fff" stroke-opacity=".35" stroke-width="2" paint-order="stroke"'))))
L.append(("1C Orange tagline — MACHINERY in orange", svg(W, 454, classic(tag_fill="url(#gOr)"))))
L.append(("1D Rule — thin orange rule between wordmark and tagline", svg(W, 454, classic(tag_y=352, extra='<rect x="486" y="276" width="880" height="7" fill="url(#gOr)" filter="url(#sh2)"/>'))))
L.append(("1E Condensed — Barlow Condensed wordmark (narrower letters)", svg(W, 454, classic(word_font="Barlow Condensed", word_size=265, word_y=262, ls="-2", tag_font="Barlow Condensed", tag_size=100, tag_ls="8", tag_y=352, mono_size=250).replace('font-family="Archivo Black"', 'font-family="Barlow Condensed"').replace('x="70" y="317"', 'x="118" y="317"').replace('x="280" y="317"', 'x="248" y="317"'))))
L.append(("1F More orange — ring two-thirds orange", svg(W, 454, ring(230, 227, r=190, w=36, gap=7).replace('d="', 'd="') if False else
    arc(230, 227, 190, 130, 355, 36, "url(#gOr)", 'filter="url(#sh)"') + arc(230, 227, 190, 5, 120, 36, "url(#gGr)", 'filter="url(#sh)"')
    + monogram(230, 227, size=180) + wordmark(480, 250) + tagline(486, 345))))
L.append(("1G Thin ring — slimmer ring, larger NF", svg(W, 454, classic(ring_w=26, ring_r=196, mono_size=205))))
L.append(("1H Diagonal split — grey top-left, orange bottom-right", svg(W, 454,
    arc(230, 227, 190, 45 + 6, 225 - 6, 36, "url(#gOr)", 'filter="url(#sh)"') + arc(230, 227, 190, 225 + 6, 405 - 6, 36, "url(#gGr)", 'filter="url(#sh)"')
    + monogram(230, 227, size=180) + wordmark(480, 250) + tagline(486, 345))))
L.append(("1I Italic — slanted wordmark for a dynamic feel", svg(W, 454, classic().replace('<text x="480" y="250"', '<text x="480" y="250" transform="skewX(-8)"').replace('<text x="486" y="345"', '<text x="486" y="345" transform="skewX(-8)"'))))
L.append(("1J Underlined — grey bar under the wordmark, tagline right-aligned", svg(W, 454, ring(230, 227) + monogram(230, 227, size=180) + wordmark(480, 250)
    + '<rect x="486" y="272" width="880" height="10" fill="url(#gGr)" filter="url(#sh2)"/>' + tagline(1366, 352, anchor="end"))))
L.append(("1K Dark version — for charcoal backgrounds (white Novo, orange Fab)", svg(W, 454,
    f'<rect width="{W}" height="454" fill="{CHAR}"/>' + ring(230, 227, gr_fill="#D5D7DA") + monogram(230, 227, size=180, b="#fff")
    + wordmark(480, 250, a="#fff", b="url(#gOr)") + tagline(486, 345, fill="#D5D7DA"))))

cards = ""
for i, (title, s) in enumerate(L, 1):
    open(os.path.join(OUT, f"novofab-1{'ABCDEFGHIJK'[i-1]}.svg"), "w", encoding="utf-8").write(s)
    cards += f'<div class="card"><div class="t">{title}</div><div class="l">{s}</div></div>'
html = f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#eceef0;font-family:Arial,sans-serif}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:18px}}
.card{{background:#fff;border:1px solid #d7d9dc;border-radius:10px;padding:14px 18px}}
.t{{font:700 17px Arial;color:#2D2E30;margin-bottom:8px}}
.l svg{{width:100%;height:auto;max-height:220px}}
</style><div class="grid">{cards}</div>"""
open(os.path.join(OUT, "sheet2.html"), "w", encoding="utf-8").write(html)
print("ok", len(L))
