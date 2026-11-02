#!/usr/bin/env python3
"""NovoTech editions of Dener's fiber laser documents — every page, picture and detail of the original, in NovoTech's catalogue
format, with the units in imperial (metric in brackets).  The owner, Nov 1 2026: "change nothing, delete nothing, only the units
become imperial — every PDF converted to the NovoTech format is converted completely".

    python3 tools/brochure/dener_laser_editions.py [gfl] [smart] [spec] [tube] [--html]

  gfl    Dener's GFL catalogue (GFL_EN, Oct 2026)           → src/files/NovoTech-Dener-GFL-Fiber-Laser-2026.pdf
  smart  Dener's Smart catalogue (SMART_EN, Oct 2026)       → src/files/NovoTech-Dener-Smart-Fiber-Laser-2026.pdf
  tube   Dener's tube catalogue (TUBE_EN) with the extra details of the Turkish one (dener_borulazer — capacities by chuck,
         the model list, the BOCI head, photos; their weights, powers and accelerations differ from TUBE_EN's, which are kept)
                                                            → src/files/NovoTech-Dener-Tube-Lasers-2026.pdf
  spec   the PRO Laser 3015 6 & 12 kW offer (GFL 3015 L / 4020 L / 6020 L)
                                                            → src/files/NovoTech-Dener-GFL-Fiber-Laser-Technical-Specification-2026.pdf
         where the offer contradicts the catalogue, the catalogue's figure is used, checked on en.dener.com (the owner, Nov 1 2026):
         X-Y acceleration 1.5 G, Z acceleration 1 G, Z travel 350 mm, repeatability 0.03 mm, lens change in 2 minutes,
         a 1,300,000 m² campus.

Left out, and why: Dener's own addresses, phone numbers and QR codes (NovoTech's contact details are on every page; a "scan to
watch" code leads to NovoTech's GFL videos instead); the Smart catalogue's open-type series (no fully open lasers anywhere — the
owner, Oct 2026); the offer's commercial lines (installation by Dener Canada / Dener USA engineers, transportation included) and
its press brake special-offer page, which are not technical content.

Images: tools/src-images/dener-brochure/ (rasters and page regions taken from those PDFs, the product range from the approved
hydraulic press brake brochure) and the site's renders.  Layout: the format of NovoTech's Dener hydraulic press brake brochure —
charcoal header band with an orange tab, Oswald titles over an orange rule, Barlow text, the included-with-every-machine box, the
grey footer band with the address and the page number.
"""
import argparse
import hashlib
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_brochure as BB           # noqa: E402  img(): the site's photos as JPEGs for Chromium

SRC = os.path.join(ROOT, "tools", "src-images", "dener-brochure")
OUTIMG = os.path.join(HERE, "out", "img")
FONTS_O = "file://" + os.path.join(HERE, "fonts")
FONTS_B = "file://" + os.path.join(ROOT, "src", "fonts")
ORANGE, OR2, CHAR, GREY = "#f2a23b", "#e08a1e", "#2d2e30", "#55575b"
VIDEO_URL = "https://novotechmachinetools.com/fiber-laser-cutting-machine#dn-gfl"


# ------------------------------------------------------------------------------------------------------------------ images
def im(src, w=1600, bg=(255, 255, 255)):
    """file:// URL of a JPEG of a source image (path relative to tools/src-images/dener-brochure, an absolute path, or a site
    image key), at most w px wide and flattened over bg — Chromium keeps JPEG data as-is, so the PDF stays small"""
    render = os.path.join(ROOT, "tools", "src-images", "dener", src + ".png")
    if not os.path.isabs(src) and not os.path.exists(os.path.join(SRC, src)):
        if not os.path.exists(render):
            return BB.img(src, w)["src"]
        src = render                       # the full-size Dener render behind a site photo
    path = src if os.path.isabs(src) else os.path.join(SRC, src)
    key = hashlib.md5(f"{path}|{w}|{bg}".encode()).hexdigest()[:10]
    out = os.path.join(OUTIMG, f"dl-{os.path.splitext(os.path.basename(path))[0]}-{key}.jpg")
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(path):
        from PIL import Image
        os.makedirs(OUTIMG, exist_ok=True)
        x = Image.open(path)
        if x.width > w:
            x = x.resize((w, round(x.height * w / x.width)), Image.LANCZOS)
        if x.mode in ("RGBA", "LA", "P"):
            x = x.convert("RGBA")
            b = Image.new("RGB", x.size, bg); b.paste(x, mask=x.split()[-1]); x = b
        x.convert("RGB").save(out, quality=88, optimize=True)
    return "file://" + out


def qr(url):
    import segno
    out = os.path.join(OUTIMG, "qr-" + hashlib.md5(url.encode()).hexdigest()[:10] + ".svg")
    if not os.path.exists(out):
        os.makedirs(OUTIMG, exist_ok=True)
        segno.make(url, error="m").save(out, scale=4, border=1, dark=CHAR)
    return "file://" + out


# ------------------------------------------------------------------------------------------------------------- html pieces
def e(t):
    return html.escape(t, quote=False)


CHECK = ('<svg class="ck" viewBox="0 0 10 8"><path d="M1 4.3 3.7 6.9 9 1.2" fill="none" stroke="%s" stroke-width="1.9" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>' % ORANGE)


def title(eyebrow, h, cls=""):
    return f'<div class="ttl {cls}"><div class="eyebrow">{eyebrow}</div><h1>{h}</h1><div class="rule"></div></div>'


def P(*paras, cls=""):
    return "".join(f'<p class="{cls}">{p}</p>' for p in paras)


def checks(items, cols=1, cls=""):
    lis = "".join(f"<li>{CHECK}<span>{i}</span></li>" for i in items)
    return f'<ul class="checks c{cols} {cls}">{lis}</ul>'


def h3(t):
    return f"<h3>{t}</h3>"


def h2(t, extra=""):
    return f'<h2>{t}{(" <small>" + extra + "</small>") if extra else ""}</h2>'


def fig(src, cap="", h=None, w=None, cls="", fit="contain", bg=(255, 255, 255), px=1600):
    st = []
    if h:
        st.append(f"height:{h}pt")
    if w:
        st.append(f"width:{w}pt")
    style = f' style="{";".join(st)}"' if st else ""
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return (f'<figure class="fig {cls}"><div class="im"{style}><img src="{im(src, px, bg)}" style="object-fit:{fit}"></div>{c}</figure>')


def grid(cells, cols=2, gap=16, cls=""):
    return f'<div class="grid {cls}" style="grid-template-columns:repeat({cols},1fr);gap:{gap}pt">' + "".join(
        f"<div>{c}</div>" for c in cells) + "</div>"


def row(*cells, cols=None, gap=18, cls="", align="start"):
    cols = cols or " ".join(["1fr"] * len(cells))
    return f'<div class="grid {cls}" style="grid-template-columns:{cols};gap:{gap}pt;align-items:{align}">' + "".join(
        f"<div>{c}</div>" for c in cells) + "</div>"


def card(img, ttl, body, sub="", h=96, cls=""):
    i = f'<div class="cim" style="height:{h}pt"><img src="{im(img, 900)}"></div>' if img else ""
    s = f'<div class="csub">{sub}</div>' if sub else ""
    return f'<div class="card {cls}">{i}<div class="ctl">{ttl}</div>{s}<div class="cbd">{body}</div></div>'


def icon_row(icon, ttl, body):
    return (f'<div class="irow"><img class="ico" src="{im(icon, 500)}"><div><div class="ittl">{ttl}</div>'
            f'<p>{body}</p></div></div>')


def labelled(img, labels, h=None, px=2200):
    """an image with NovoTech label tags at % positions: [(text, left%, top%)]"""
    tags = "".join(f'<span class="tag" style="left:{x}%;top:{y}%">{t}</span>' for t, x, y in labels)
    st = f' style="height:{h}pt"' if h else ""
    return f'<div class="lab"{st}><img src="{im(img, px)}">{tags}</div>'


def pct(crop, labels):
    """label centres as % of a cropped page region: [(text, bbox in page pt)] → [(text, left%, top%)]"""
    x0, y0, x1, y1 = crop
    return [(t, round(((b[0] + b[2]) / 2 - x0) / (x1 - x0) * 100, 1), round(((b[1] + b[3]) / 2 - y0) / (y1 - y0) * 100, 1)) for t, b in labels]


def stats(items, cls=""):
    return f'<div class="stats {cls}">' + "".join(f'<div><b>{n}</b><span>{l}</span></div>' for n, l in items) + "</div>"


def kv(rows, head=None):
    """a two-column specification table: [(label, value)] — value may be a list for one cell per column of head"""
    th = ""
    if head:
        th = "<thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead>"
    trs = ""
    for r in rows:
        lab, vals = r[0], r[1:]
        trs += f"<tr><th>{lab}</th>" + "".join(f"<td>{v}</td>" for v in vals) + "</tr>"
    return f'<table class="kv">{th}<tbody>{trs}</tbody></table>'


def mtable(head, rows, corner="Model", cls=""):
    """the NovoTech specification table: orange corner cell, charcoal model header, banded rows; rows [(label, unit, cells)]"""
    units = any(u for _, u, _ in rows)
    th = f'<th class="corner">{corner}</th>' + ('<th class="unit"></th>' if units else "") + "".join(f"<th>{h}</th>" for h in head)
    body = ""
    for lab, unit, cells in rows:
        body += f'<tr><th>{lab}</th>' + (f'<td class="unit">{unit}</td>' if units else "") + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    return f'<table class="mt {cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


INCLUDED = [("Made in Turkey with European components", False), ("CSA-approved electrical panel", False), ("1-year warranty", False),
            ("<b>7-day money-back guarantee</b> (in-stock machines only)", False),
            ("Spare parts &amp; technical support readily available in Canada", False),
            ("<b>Order Today with Just 10% Down — 0% Down Financing Available</b>", False), ("<b>Installation and training available</b>", False)]


def included(cls="", two=False):
    items = [t for t, _ in INCLUDED]
    if two:
        return (f'<div class="incl incl2 {cls}"><div class="ih">Included with every<br>NovoTech machine</div>'
                f'{checks(items[:4])}{checks(items[4:])}</div>')
    return (f'<div class="incl {cls}"><div class="ih">Included with every<br>NovoTech machine</div>'
            f'{checks(items[:3])}{checks(items[3:5])}{checks(items[5:])}</div>')


def qrbox(text, url=VIDEO_URL):
    return f'<div class="qr"><img src="{qr(url)}"><span>{text}</span></div>'


DISCLAIMER = ("Specifications subject to change without notice. Imperial values are converted from the manufacturer's metric data and "
              "rounded: plate thicknesses in common fractions (1/2, 1/4, 1/8, 1/16). Model numbers are manufacturer designations. "
              "Photos may show optional equipment.")


# ------------------------------------------------------------------------------------------------------------------- pages
class Book:
    def __init__(self, slug, header, sub, out):
        self.slug, self.header, self.sub, self.out = slug, header, sub, out
        self.pages = []

    def page(self, tab, body, toc=None, header=None, sub=None, cls="", key=None):
        self.pages.append({"kind": "std", "tab": tab, "body": body, "toc": toc, "header": header or self.header,
                           "sub": sub or self.sub, "cls": cls, "key": key})

    def num(self, key):
        return next(i for i, p in enumerate(self.pages, 1) if p.get("key") == key)

    def cover(self, tag, eyebrow, l1, l2, tagline, hero, stats_, hero_h=330, minis=()):
        self.pages.append({"kind": "cover", "tag": tag, "eyebrow": eyebrow, "l1": l1, "l2": l2, "tagline": tagline, "hero": hero,
                           "stats": stats_, "hero_h": hero_h, "minis": minis})

    def back(self, line2, photos):
        self.pages.append({"kind": "back", "line2": line2, "photos": photos})

    def contents(self):
        out = []
        for i, p in enumerate(self.pages, 1):
            if p.get("toc"):
                out.append((p["toc"], i))
        return out


LOGO = None


def logo():
    global LOGO
    if LOGO is None:
        LOGO = BB.img("novotech-logo", 800, png=True)["src"]
    return LOGO


def footer(n):
    return (f'<div class="ftr"><img src="{logo()}"><div class="fn">NovoTech Machine Tools Inc.</div>'
            f'<div class="fa">1365 Mid-Way Blvd, 26, Mississauga, ON L5T 2J5, Canada<br>'
            f'NovoTechMachineTools.com&nbsp; | &nbsp;info@NovoTechMachineTools.com&nbsp; | &nbsp;+1 647 526 5510</div>'
            f'<div class="pg">{n:02d}</div></div>')


def render_page(p, n, book):
    if p["kind"] == "cover":
        st = "".join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in p["stats"])
        minis = ""
        if p["minis"]:
            minis = '<div class="cminis">' + "".join(f'<div><img src="{im(m, 1000)}"></div>' for m in p["minis"]) + "</div>"
        return (f'<section class="page cover"><img class="clogo" src="{logo()}"><div class="ctag">{p["tag"]}</div>'
                f'<div class="ceye">{p["eyebrow"]}</div><div class="cl1">{p["l1"]}</div><div class="cl2">{p["l2"]}</div>'
                f'<div class="crule"></div><div class="ctagline">{p["tagline"]}</div>'
                f'<div class="chero" style="height:{p["hero_h"]}pt"><img src="{im(p["hero"], 2200)}"></div>{minis}'
                f'<div class="cstats">{st}</div>{footer(n)}</section>')
    if p["kind"] == "back":
        ph = "".join(f'<div><img src="{im(x, 900)}"></div>' for x in p["photos"])
        items = [t for t, _ in INCLUDED]
        return (f'<section class="page backc"><img class="blogo" src="{logo()}">'
                f'<div class="bl1">LET’S FIND THE RIGHT</div><div class="bl2">{p["line2"]}</div>'
                f'<p class="bp">Call or visit us for quotes, demonstrations, installation and service. In-stock machines ship fast from our '
                f'Mississauga, ON location.</p>'
                f'<div class="bcols"><div><i>Phone</i><b>+1 647 526 5510</b></div>'
                f'<div><i>Web &amp; email</i><b class="w">NovoTechMachineTools.com</b><span>info@NovoTechMachineTools.com</span></div>'
                f'<div><i>Address</i><span>1365 Mid-Way Blvd, 26<br>Mississauga, ON L5T 2J5<br>Canada</span></div></div>'
                f'<div class="bincl"><div class="bih">Included with every NovoTech machine</div>{checks(items[:4])}{checks(items[4:])}</div>'
                f'<div class="bph">{ph}</div><div class="bdis">{DISCLAIMER}</div><div class="bband"></div></section>')
    return (f'<section class="page {p["cls"]}"><div class="hdr"><div class="ht">{p["header"]}</div><div class="hs">{p["sub"]}</div>'
            f'<div class="tab">{p["tab"]}</div></div><div class="body">{p["body"]}</div>{footer(n)}</section>')


CSS = """
@font-face{font-family:Oswald;font-weight:400;src:url(%(O)s/oswald-latin-400-normal.woff2)}
@font-face{font-family:Oswald;font-weight:500;src:url(%(O)s/oswald-latin-500-normal.woff2)}
@font-face{font-family:Oswald;font-weight:600;src:url(%(O)s/oswald-latin-600-normal.woff2)}
@font-face{font-family:Oswald;font-weight:700;src:url(%(O)s/oswald-latin-700-normal.woff2)}
@font-face{font-family:Barlow;font-weight:400;src:url(%(B)s/barlow-latin-400-normal.woff2)}
@font-face{font-family:Barlow;font-weight:500;src:url(%(B)s/barlow-latin-500-normal.woff2)}
@font-face{font-family:Barlow;font-weight:600;src:url(%(B)s/barlow-latin-600-normal.woff2)}
@font-face{font-family:Barlow;font-weight:700;src:url(%(B)s/barlow-latin-700-normal.woff2)}
@font-face{font-family:BarlowX;font-weight:400;src:url(%(B)s/barlow-latin-ext-400-normal.woff2)}
@font-face{font-family:BarlowX;font-weight:700;src:url(%(B)s/barlow-latin-ext-700-normal.woff2)}
@font-face{font-family:OswaldX;font-weight:700;src:url(%(O)s/oswald-latin-ext-700-normal.woff2)}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:Barlow,BarlowX,sans-serif;color:%(G)s;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:612pt;height:792pt;position:relative;overflow:hidden;page-break-after:always;break-after:page;background:#fff}
.hdr{position:absolute;left:0;top:0;width:612pt;height:56.2pt;background:%(C)s}
.ht{position:absolute;left:39.6pt;top:11.2pt;font:600 12.5pt/1.2 Oswald;color:#fff;text-transform:uppercase;letter-spacing:.01em}
.hs{position:absolute;left:39.6pt;top:32.2pt;font:400 7.8pt/1 Barlow;color:#b8babd;text-transform:uppercase;letter-spacing:.09em}
.tab{position:absolute;right:0;top:16.5pt;height:25.5pt;background:%(O1)s;padding:0 40pt 0 28pt;font:600 8.6pt/25.5pt Oswald;color:%(C)s;
 letter-spacing:.15em;text-transform:uppercase;clip-path:polygon(13pt 0,100%% 0,100%% 100%%,0 100%%)}
.body{position:absolute;left:39.6pt;right:39.6pt;top:68pt;bottom:70pt;display:flex;flex-direction:column}
.body.top{top:64pt}
.ttl{margin-bottom:12pt}
.eyebrow{font:400 8.5pt/1.25 Oswald;color:%(O2)s;letter-spacing:.31em;text-transform:uppercase}
h1{font:700 23pt/1.06 Oswald,OswaldX;color:%(C)s;text-transform:uppercase;margin-top:1pt}
.rule{width:72pt;height:3.7pt;background:%(O1)s;margin-top:7pt}
p{font:400 10pt/1.43 Barlow,BarlowX;color:%(G)s;margin:0 0 8pt}
p.sm,.sm p{font-size:9pt;line-height:1.4}
p.xs,.xs p{font-size:8.4pt;line-height:1.38}
b,strong{font-weight:700;color:%(C)s}
h2{font:700 11.5pt/1.2 Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.04em;border-bottom:1.5pt solid %(O1)s;padding-bottom:3.5pt;margin:6pt 0 8pt}
h2 small{font:400 8.6pt Oswald;color:%(O2)s;letter-spacing:.18em;margin-left:6pt}
h3{font:600 10.5pt/1.2 Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.03em;margin:2pt 0 5pt}
.checks{list-style:none;margin:0 0 6pt}
.checks li{display:flex;gap:6pt;align-items:flex-start;font:400 9.2pt/1.35 Barlow,BarlowX;color:%(C)s;margin:0 0 3.2pt}
.checks .ck{width:9pt;height:7.2pt;flex:0 0 9pt;margin-top:3pt}
.checks.c2{columns:2;column-gap:18pt}
.checks.c2 li{break-inside:avoid}
.checks.sm li{font-size:8.4pt}
.grid{display:grid}
.fig{margin:0}
.fig .im{width:100%%;display:flex;align-items:center;justify-content:center;overflow:hidden}
.fig img{width:100%%;height:100%%;display:block}
.fig figcaption{font:400 7.8pt/1.3 Barlow;color:#7a7c80;margin-top:4pt;text-align:center}
.card{display:flex;flex-direction:column}
.cim{display:flex;align-items:center;justify-content:center;margin-bottom:6pt}
.cim img{max-width:100%%;max-height:100%%;object-fit:contain}
.ctl{font:500 11pt/1.2 Oswald;color:%(C)s;border-top:1.8pt solid %(O1)s;padding-top:5pt}
.csub{font:400 7.8pt Barlow;color:#7a7c80;margin-top:1pt}
.cbd{margin-top:5pt}
.cbd p{font-size:8.8pt;line-height:1.4;margin-bottom:5pt}
.irow{display:flex;gap:14pt;align-items:center;background:#f4f4f5;border-left:3.7pt solid %(O1)s;padding:9pt 12pt;margin-bottom:9pt}
.irow .ico{width:58pt;height:58pt;object-fit:contain;flex:0 0 58pt;border-radius:50%%}
.ittl{font:600 10.5pt/1.2 Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.03em;margin-bottom:3pt}
.irow p{font-size:9pt;margin:0}
.lab{position:relative;width:100%%}
.lab img{width:100%%;height:100%%;object-fit:contain;display:block}
.tag{position:absolute;background:#fff;border-left:3pt solid %(O1)s;box-shadow:0 .6pt 2.2pt rgba(0,0,0,.35);padding:2.6pt 6pt 2.4pt 5pt;
 font:500 8pt/1 Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.06em;white-space:nowrap;transform:translate(-50%%,-50%%)}
.stats{display:flex;background:%(C)s;padding:12pt 14pt 11pt;gap:0}
.stats>div{flex:1;padding-right:10pt}
.stats b{display:block;font:700 19pt/1.1 Oswald;color:%(O1)s}
.stats span{display:block;font:400 7.8pt/1.3 Barlow;color:#c9cbce;text-transform:uppercase;letter-spacing:.1em;margin-top:4pt}
.incl{display:grid;grid-template-columns:118pt 1fr 1fr 1fr;gap:10pt;background:#eeeff0;border-left:3.7pt solid %(O1)s;padding:9pt 12pt 6pt;margin-top:auto}
.incl2{grid-template-columns:92pt 1fr 1fr;margin-top:0}
.incl .ih{font:600 8.4pt/1.25 Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.04em;align-self:center}
.incl .checks li{font-size:8.1pt;margin-bottom:2.5pt}
.incl .checks .ck{margin-top:2pt}
.kv{border-collapse:collapse;width:100%%;font:400 9.2pt/1.3 Barlow,BarlowX;color:%(C)s}
.kv th,.kv td{padding:6.5pt 8pt;border-bottom:.8pt solid #d9dadc;text-align:left;vertical-align:middle}
.kv tbody th{font:700 9.2pt Barlow;color:%(C)s;width:150pt}
.kv thead th{background:%(C)s;color:#fff;font:500 9pt Oswald;letter-spacing:.04em;text-transform:uppercase;border:0}
.kv thead th:first-child{background:%(O1)s;color:%(C)s}
.kv tbody tr:nth-child(odd){background:#f4f4f5}
.mt{border-collapse:collapse;width:100%%;font:400 8pt/1.25 Barlow,BarlowX;color:%(C)s}
.mt th,.mt td{padding:4.6pt 5pt;text-align:center;vertical-align:middle}
.mt thead th{background:%(C)s;color:#fff;font:500 8pt Oswald;letter-spacing:.03em}
.mt thead th.corner{background:%(O1)s;color:%(C)s;text-align:left}
.mt thead th.unit{background:%(C)s}
.mt tbody th{text-align:left;font:500 8pt Barlow;color:%(C)s}
.mt td.unit{color:#8c8e91;font-size:7.4pt}
.mt tbody tr:nth-child(even){background:#f4f4f5}
.mt tbody tr{border-bottom:.6pt solid #e2e3e5}
.note{font:italic 400 7.8pt/1.35 Barlow;color:#6d6f73;margin:5pt 0 0}
.qr{display:flex;align-items:center;gap:7pt}
.qr img{width:50pt;height:50pt}
.qr span{font:400 7.6pt/1.3 Barlow;color:#6d6f73;max-width:110pt}
.chips{display:grid;grid-template-columns:repeat(3,1fr);gap:5pt 10pt;margin-top:10pt}
.chips div{font:500 8.4pt/1.2 Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.04em;border-left:3pt solid %(O1)s;background:#f4f4f5;padding:5pt 7pt}
.box{border:.8pt solid %(C)s;border-left:3.7pt solid %(O1)s;padding:8pt 10pt}
.box .bt{font:500 8.6pt Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.04em}
.box p{font-size:8.2pt;margin:2pt 0 0;color:%(C)s}
.toc{columns:2;column-gap:36pt;margin-top:4pt}
.toc div{display:flex;align-items:baseline;font:400 9.2pt/1.25 Barlow;color:%(C)s;margin-bottom:8pt;break-inside:avoid}
.toc i{flex:1;border-bottom:1pt dotted #8c8e91;margin:0 6pt;transform:translateY(-2pt)}
.toc b{font:600 9.2pt Oswald;color:%(O2)s}
.ttlx{display:flex;align-items:baseline;gap:8pt;border-bottom:1.5pt solid %(O1)s;padding-bottom:4pt;margin:14pt 0 10pt}
.ttlx span{font:700 15pt Oswald;color:%(C)s;text-transform:uppercase}
.ttlx small{font:400 9pt Oswald;color:%(O2)s;letter-spacing:.18em;text-transform:uppercase}
.dark{background:%(C)s;color:#fff}
.photo-panel{position:relative;overflow:hidden}
.photo-panel>img{width:100%%;height:100%%;object-fit:cover;object-position:50%% 70%%;display:block}
.overlay{position:absolute;left:18pt;right:18pt;bottom:18pt;background:rgba(32,33,35,.86);border-left:3.7pt solid %(O1)s;padding:12pt 14pt}
.overlay .st{display:grid;grid-template-columns:repeat(4,1fr);gap:8pt}
.overlay .st div{border-left:.8pt solid rgba(255,255,255,.25);padding-left:8pt}
.overlay .st div:first-child{border-left:0;padding-left:0}
.overlay .st b{display:block;font:600 11pt/1.15 Oswald;color:%(O1)s;text-transform:uppercase}
.overlay .st span{display:block;font:400 8pt/1.2 Barlow;color:#e6e7e8}
.overlay p{color:#fff;margin:10pt 0 0;font-size:11pt}
.overlay p b{color:#fff}
.diag{position:relative;width:250pt;height:132pt;margin:4pt auto 0}
.diag .c{position:absolute;left:50%%;top:50%%;width:66pt;height:66pt;margin:-33pt 0 0 -33pt;border-radius:50%%;background:%(O1)s;
 display:flex;align-items:center;justify-content:center;text-align:center;font:500 7.6pt/1.15 Oswald;color:%(C)s;text-transform:uppercase;
 box-shadow:0 0 0 5pt #fff,0 0 0 6.2pt %(O1)s}
.diag .l{position:absolute;font:600 8.4pt/1 Oswald;color:%(C)s;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
.diag svg{position:absolute;left:0;top:0;width:100%%;height:100%%}
.mtag{display:inline-block;background:%(O1)s;font:600 7.6pt/1 Oswald;color:%(C)s;letter-spacing:.14em;text-transform:uppercase;
 padding:4pt 10pt;clip-path:polygon(5pt 0,100%% 0,calc(100%% - 5pt) 100%%,0 100%%);margin-right:8pt}
.mline{display:flex;align-items:center;font:600 10pt Oswald;color:%(C)s;margin:6pt 0 2pt}
.mline small{font:400 8.2pt Barlow;color:#6d6f73;margin-left:8pt}
.badges{display:flex;gap:14pt;align-items:center;justify-content:center}
.badges img{height:62pt;object-fit:contain}
.mt.big{font-size:9pt}
.mt.big th,.mt.big td{padding:6pt 6pt}
.mt.big thead th{font-size:9pt}
.mt small,.kv small{font-size:.82em;color:#6d6f73}
.kv.spec3 thead th{text-align:center}
.kv thead small{color:#c9cbce}
.kv.spec3 th,.kv.spec3 td{padding:5.6pt 8pt}
.kv.spec3 thead th:first-child{text-align:left}
.kv.spec3 td{text-align:center}
.mt-auto{margin-top:auto}
.capt{border-collapse:collapse;width:100%%;margin-top:4pt;font:400 7.4pt/1.22 Barlow,BarlowX;color:%(C)s}
.capt th,.capt td{padding:2.4pt 4pt;border-bottom:.6pt solid #e2e3e5;text-align:left;vertical-align:top}
.capt th{font:600 7.6pt Barlow;width:52pt;color:%(C)s}
.capt tr:nth-child(odd){background:#f4f4f5}
.mt.tight{font-size:7.1pt;line-height:1.2}
.mt.tight th,.mt.tight td{padding:3.2pt 3pt}
.mt.tight thead th{font-size:7.6pt}
.mt.tight tbody th{font-size:7.2pt;width:84pt}
ol.num{margin:0 0 6pt 16pt;font:400 9.6pt/1.42 Barlow;color:%(C)s}
ol.num li{margin-bottom:5pt;padding-left:3pt}
.faq{border-left:3.7pt solid %(O1)s;background:#f4f4f5;padding:8pt 12pt;margin-bottom:8pt}
.faq h3{margin:0 0 3pt}
.faq p{margin:0;font-size:9.6pt}
.toc2{columns:2;column-gap:28pt}
.toc2 div{margin-bottom:4.2pt;font-size:8.8pt}
.toc2 em{font-style:normal;font:600 8.8pt Oswald;color:%(O2)s;display:inline-block;min-width:30pt}
.toc2 .t1 span{padding-left:10pt}
.toc2 .t2 span{padding-left:20pt;color:%(G)s}
/* footer */
.ftr{position:absolute;left:0;bottom:0;width:612pt;height:58.5pt;background:#eeeff0;border-top:3pt solid %(O1)s}
.ftr img{position:absolute;left:40pt;top:9.5pt;height:31.5pt}
.ftr .fn{position:absolute;left:148.2pt;top:9.8pt;font:700 8.1pt/1 Barlow;color:%(C)s}
.ftr .fa{position:absolute;left:148.2pt;top:21pt;font:400 7.4pt/1.33 Barlow;color:%(G)s}
.ftr .pg{position:absolute;right:39.6pt;top:12.3pt;font:600 16pt/1 Oswald;color:%(O1)s}
/* cover */
.cover .clogo{position:absolute;left:40pt;top:30pt;height:56pt}
.cover .ctag{position:absolute;right:39.8pt;top:45pt;height:26.2pt;background:%(C)s;color:#fff;font:600 9pt/26.2pt Oswald;letter-spacing:.15em;
 text-transform:uppercase;padding:0 16pt 0 24pt;clip-path:polygon(10pt 0,100%% 0,100%% 100%%,0 100%%)}
.cover .ceye{position:absolute;left:39.6pt;top:112pt;font:400 10pt Oswald;color:%(O2)s;letter-spacing:.3em;text-transform:uppercase}
.cover .cl1,.cover .cl2{position:absolute;left:38pt;font:700 46pt/1 Oswald;text-transform:uppercase}
.cover .cl1{top:128pt;color:%(C)s}
.cover .cl2{top:174pt;color:%(O2)s}
.cover .crule{position:absolute;left:39.8pt;top:233.2pt;width:93.7pt;height:6pt;background:%(O1)s}
.cover .ctagline{position:absolute;left:39.6pt;top:250pt;font:400 14pt Oswald;color:%(G)s;letter-spacing:.02em;text-transform:uppercase}
.cover .chero{position:absolute;left:30pt;right:30pt;top:282pt;display:flex;align-items:center;justify-content:center}
.cover .chero img{max-width:100%%;max-height:100%%;object-fit:contain}
.cover .cminis{position:absolute;left:40pt;right:40pt;top:612pt;height:62pt;display:flex;gap:12pt}
.cover .cminis div{flex:1;display:flex;align-items:center;justify-content:center}
.cover .cminis img{max-width:100%%;max-height:100%%;object-fit:contain}
.cover .cstats{position:absolute;left:0;right:0;top:682.5pt;height:51pt;background:%(C)s;display:flex;padding:0 39.6pt 0 42.4pt}
.cover .cstats div{flex:1;padding-top:6pt}
.cover .cstats b{display:block;font:600 17pt/1.15 Oswald;color:%(O1)s}
.cover .cstats span{display:block;font:400 7.6pt/1 Barlow;color:#c9cbce;letter-spacing:.11em;text-transform:uppercase;margin-top:3pt}
/* back cover */
.backc{background:%(C)s}
.backc .blogo{position:absolute;left:44pt;top:44pt;height:72pt}
.backc .bl1,.backc .bl2{position:absolute;left:43.2pt;font:700 34pt/1 Oswald;text-transform:uppercase}
.backc .bl1{top:126pt;color:#fff}
.backc .bl2{top:161pt;color:%(O1)s}
.backc .bp{position:absolute;left:43.2pt;top:216pt;width:420pt;font:400 12pt/1.37 Barlow;color:#c9cbce}
.backc .bcols{position:absolute;left:43.5pt;right:43.5pt;top:267pt;display:grid;grid-template-columns:repeat(3,1fr);gap:10.5pt}
.backc .bcols div{border-top:3pt solid %(O1)s;padding-top:7pt}
.backc .bcols i{display:block;font:400 9pt Oswald;font-style:normal;color:#9a9ca0;letter-spacing:.12em;text-transform:uppercase;margin-bottom:4pt}
.backc .bcols b{display:block;font:400 17pt/1.2 Oswald;color:#fff}
.backc .bcols b.w{font-size:14pt}
.backc .bcols span{display:block;font:400 10pt/1.35 Barlow;color:#fff}
.backc .bincl{position:absolute;left:43.5pt;right:43.5pt;top:345pt;height:110pt;background:#3a3c40;border-left:4.5pt solid %(O1)s;
 padding:9pt 16pt;display:grid;grid-template-columns:1fr 1fr;column-gap:16pt;align-content:start}
.backc .bih{grid-column:1/3;font:400 11pt Oswald;color:#fff;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6pt}
.backc .bincl .checks li{color:#e6e7e8;font-size:9.6pt;margin-bottom:3.2pt}
.backc .bincl b{color:#e6e7e8}
.backc .bph{position:absolute;left:44pt;right:44pt;top:474pt;height:262pt;display:grid;grid-template-columns:repeat(2,1fr);grid-template-rows:126pt 126pt;gap:10pt}
.backc .bph div{background:#fff;border-bottom:3pt solid %(O1)s;display:flex;align-items:center;justify-content:center;padding:6pt;height:126pt;overflow:hidden}
.backc .bph img{max-width:100%%;max-height:100%%;object-fit:contain}
.backc .bdis{position:absolute;left:43.2pt;right:43.2pt;top:747pt;font:400 7pt/1.3 Barlow;color:#8e9094}
.backc .bband{position:absolute;left:0;right:0;bottom:0;height:14pt;background:%(O1)s}
""" % {"O": FONTS_O, "B": FONTS_B, "O1": ORANGE, "O2": OR2, "C": CHAR, "G": GREY}


def to_html(book):
    pages = "".join(render_page(p, i, book) for i, p in enumerate(book.pages, 1))
    return f"<!doctype html><html lang=en><head><meta charset=utf-8><style>{CSS}</style></head><body>{pages}</body></html>"


def overflow_report(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('section.page')].map((s, i) => {
        const b = s.querySelector('.body'); if (!b) return null;
        const over = [...b.children].some(c => c.getBoundingClientRect().bottom > b.getBoundingClientRect().bottom + 1);
        return over ? i + 1 : null }).filter(x => x)""")


def build(book, html_only=False):
    from playwright.sync_api import sync_playwright
    hp = os.path.join(HERE, "out", book.slug + ".html")
    os.makedirs(os.path.dirname(hp), exist_ok=True)
    open(hp, "w", encoding="utf-8").write(to_html(book))
    if html_only:
        print("wrote", hp)
        return hp
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + hp, wait_until="networkidle")
        pg.wait_for_timeout(500)
        over = overflow_report(pg)
        if over:
            print("WARNING overflowing pages:", over)
        pg.pdf(path=book.out, width="8.5in", height="11in", print_background=True, prefer_css_page_size=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    import fitz
    d = fitz.open(book.out)
    d.set_metadata({"title": book.title, "author": "NovoTech Machine Tools Inc.", "subject": book.subject,
                    "creator": "NovoTech Machine Tools Inc.", "producer": "NovoTech Machine Tools Inc."})
    tmp = book.out + ".tmp"
    d.save(tmp, garbage=3, deflate=True)
    d.close()
    os.replace(tmp, book.out)
    print(f"wrote {book.out} ({os.path.getsize(book.out) / 1048576:.1f} MB, {len(book.pages)} pages)")
    return book.out


# ------------------------------------------------------------------------------------------------- shared Dener pages
ABOUT = [
    "Dener Makina was established in 1974 in the Kayseri Old Industrial Zone. Since 2000, the company has focused on the production of "
    "CNC Sheet Metal Processing Machines, manufacturing a wide range of products including Guillotine Shears, Hydraulic Press Brakes, "
    "Ball Screw Press Brakes, Servo-Electric Press Brakes, Plasma Cutting Machines, and Fiber Laser Cutting Machines.",
    "In 2016, the company made a major investment by expanding its facilities to include 1,670,000 sq ft (155,000 m²) of factory "
    "buildings and 290,000 sq ft (27,000 m²) of social facilities on a 14,000,000 sq ft (1,300,000 m²) site within the İncesu Organized "
    "Industrial Zone (O.S.B). In this new phase, Dener Makina began the production of CNC Metal Processing Machines such as Taksan "
    "Integrated Systems, Double Column Machining Centers, 5-Axis Simultaneous Machining Centers, Vertical Machining Centers, Lathes, "
    "and Grinding Machines.",
    "With its extensive production range, over half a century of experience, skilled workforce, and multinational R&amp;D center, Dener "
    "Makina holds a leading position globally by providing high-value industrial investment products in the fields of CNC Sheet Metal "
    "Processing and CNC Metal Processing Machines."]


def about_page(book):
    """page 2: About Dener, the included box, sold & serviced, and the contents (filled in once every page is known)"""
    book.page("About", "@@ABOUT@@", toc=None, header="About Dener", sub="Dener Makina · Kayseri, Türkiye")


def fill_about(book):
    toc = "".join(f"<div><span>{t}</span><i></i><b>{n:02d}</b></div>" for t, n in book.contents())
    body = (title("Manufacturer · established 1974", "About Dener") + P(*ABOUT, cls="sm")
            + row(included("in-about", two=True), '<div class="box"><div class="bt">Sold &amp; serviced in Canada</div>'
                  '<p>by NovoTech Machine Tools — Mississauga, ON</p></div>', cols="2.3fr 1fr", gap=14)
            + '<div class="ttlx"><span>Contents</span><small>This brochure</small></div>' + f'<div class="toc">{toc}</div>')
    for p in book.pages:
        if p.get("body") == "@@ABOUT@@":
            p["body"] = body


CAMPUS_LABELS = ["Sheet Processing Machines Production Plant", "Machine Tools Production Plant", "Production Plant",
                 "Sheet Welding Factory", "Sheet Cladding Factory", "Technology Center", "Administrative Building",
                 "Social Facilities", "Main Entrance", "Visitor Parking Area", "Helicopter Pad"]


def campus_page(book):
    body = (title("Dener Makina · İncesu Organized Industrial Zone, Kayseri", "Dener production campus")
            + fig("gfl/campus.jpg", "Dener production campus, Kayseri — 1,670,000 sq ft (155,000 m²) of factory buildings on a "
                  "14,000,000 sq ft (1,300,000 m²) site", h=232, fit="cover", px=2400)
            + '<div class="chips">' + "".join(f"<div>{t}</div>" for t in CAMPUS_LABELS) + "</div>"
            + stats([("52+", "Years of experience"), ("100+", "Export countries"), ("14,000,000 sq ft", "Production campus (1,300,000 m²)")],
                    cls="mt-auto"))
    book.page("Production campus", body, toc="Production Campus")


SOFTWARE = ("CypNest is a nesting software for CypCut/HypCut laser cutting systems. It offers advanced features like drawing "
            "modification, quick nesting, and toolpath optimization. It supports DWG, DXF files, and Excel-based batch import. The "
            "powerful algorithm enables efficient manual or automatic nesting, with smart toolpath strategies to minimize travel. CypNest "
            "also generates production and pricing reports, perfectly integrating with HypCut/CypCut software.")
SPEED_UP = ["Drawing Modification and intelligent part recognition", "Supports DWG and DXF formats. Excel table-based part creation and import support.",
            "Nesting Strategy: Powerful algorithm for high efficiency and fast production rate",
            "No part quantity limitation, supports manual and automatic nesting, and free-form sheet placement",
            "Toolpath Optimization: Smart cutting path strategy to minimize travel length",
            "Smooth operation with toolpath adjustment options and multiple contact settings",
            "Generates production and pricing analysis reports. Technical and cutting parameters perfectly match HypCut/CypCut laser cutting software."]


def software_page(book, cyp="gfl/cypnest.png"):
    body = (title("Smart software", "CypNest nesting solution") + P(SOFTWARE)
            + fig(cyp, "CypNest nesting software", h=300, px=1600)
            + h2("Speed up production") + checks(SPEED_UP))
    book.page("Smart software", body, toc="Software — CypNest")


HEAD_1 = ("Focusing on 2D, 3D and angle cutting, the cost-effective BLT Series Smart Cutter is available for power levels below 30 kW "
          "and offers excellent performance with stable cutting, easy installation and setup. Brand new optical solutions are available "
          "with closed-loop autofocus.")
HEAD_2 = ("Slag-free cutting, nozzle cooling and water cooling sensor can be supported. Makes cutting more stable and efficient. Smart "
          "Drilling and Auto Re-cutting functions meet the most demanding air standard and N2 high-performance cutting, significantly "
          "increasing efficiency and productivity.")


def head_page(book):
    left = (h3("Stable and efficient cutting process")
            + '<div class="ittl" style="margin-top:8pt">LED indicators</div>'
            + P("<b>LEDs on the laser head; communication.</b> The sensors provide information that the power is working correctly.", cls="sm")
            + '<div class="box" style="margin-top:6pt"><p style="font-size:9pt">Equipped with advanced technology, it offers a cutting '
              'solution that combines high performance with affordable costs.</p></div>')
    body = (title("BLT series smart cutter · closed-loop autofocus", "Laser cutting head") + P(HEAD_1, HEAD_2, cls="sm")
            + row(left, fig("gfl/head-leds.jpg", "BLT cutting head — LED indicators: power, run, link and sensor", h=300, px=1400),
                  cols="1fr 1.1fr", gap=20, align="center")
            + row(fig("gfl/optics-drawers.png", "Ready-to-use optical drawers", h=170, px=1000),
                  '<h3 style="font-size:13pt;color:%s">Easy installation and low repair costs</h3>' % CHAR
                  + P("Lens change in 2 minutes with ready-to-use optical drawers."), cols="1fr 1fr", gap=20, align="center"))
    book.page("Laser cutting head", body, toc="Laser Cutting Head")


EASE = [("gfl/icon-handwheel.jpg", "Handwheel", "The machine has a handwheel for precise axis movement adjustments. It is especially useful "
         "when precise positioning is required to make small cuts from the remaining parts of metal sheets that have been previously used for cutting."),
        ("gfl/icon-resume.jpg", "Resume cutting after an alarm", "When the machine is stopped or paused for any reason, cutting can be started again from the desired point.")]
SECURITY = [("gfl/icon-head-protect.jpg", "Protecting the cutting head", "If the cutting head is very close to hitting a piece or pallet, the "
             "machine stops immediately to prevent damage. After the machine stops, the operator can check and resolve the issue, then press "
             "the start button to resume cutting from where it left off."),
            ("gfl/icon-glasses.jpg", "Protective glasses", "In order to prevent damage to the eyes caused by the fiber laser light, there are "
             "viewing glasses on the front doors of the machine suitable for the fiber laser wavelength."),
            ("gfl/icon-estop.jpg", "Emergency stops", "An easy access to emergency stop button provides a safe working environment to the "
             "operator. A buzzer found on top of the machine shows in real time the working state of the machine."),
            ("gfl/icon-barriers.jpg", "Safety barriers", "Light safety barriers stop the pallet change process if breached, preventing injury. "
             "After a reset, the pallet change can be resumed in the desired direction.")]


def ease_page(book):
    body = (title("Operator comfort and safety", "Ease of use &amp; security")
            + h2("Ease of use") + "".join(icon_row(*x) for x in EASE)
            + h2("Security") + "".join(icon_row(*x) for x in SECURITY))
    book.page("Ease of use &amp; security", body, toc="Ease of Use &amp; Security")


SERVICE = [("gfl/service-parts.jpg", "Fast service and spare part delivery", [
    "Dener Makina responds to service requests as quickly as possible to ensure production continuity. All service and parts needs "
    "received from our customers are systematically evaluated and processed by our experienced customer representatives. From the moment "
    "a malfunction is reported, the response process is meticulously managed. Our field teams are quickly deployed, minimizing production "
    "interruptions.",
    "Our spare parts inventory management is fully aligned with our machinery. By constantly maintaining critical parts in stock, we offer "
    "our customers fast and reliable parts supply. This prevents time loss during service interventions and ensures the uninterrupted "
    "operation of your machines."]),
    ("gfl/service-rnd.jpg", "R&amp;D service backup", [
        "Dener Makina's R&amp;D center actively works to develop service solutions tailored to customer needs. Based on feedback from field "
        "experience, existing machines are updated with software and hardware, and new functions are integrated. This allows the machines "
        "to easily adapt to changing production needs.",
        "Technical requirements, particularly those encountered in production for specific processes and sectors, are analyzed by our "
        "engineering departments and solution-focused projects are developed.",
        "This allows user-specific machines to be optimized for high efficiency. This R&amp;D-supported approach is key to Dener's success."]),
    ("gfl/service-remote.jpg", "Remote and digital support", [
        "Thanks to our remote access system integrated into our digital infrastructure, our machines can be accessed from anywhere in the "
        "world. This system allows software updates, error analysis, and setting checks to be performed instantly. In cases where urgent "
        "technical support is required, rapid solutions are provided before physical intervention, resulting in time and cost savings.",
        "Our remote access support service is designed to be compatible with all our machine models. Being available to our customers "
        "whenever they need it is the cornerstone of our service approach. This digital support system increases efficiency, minimizes "
        "downtime, and ensures uninterrupted production."])]


def service_page(book):
    body = title("Dener Makina · service, parts and R&amp;D", "Service &amp; support")
    for img, t, paras in SERVICE:
        body += row(h3(t) + P(*paras, cls="xs"), fig(img, h=118, fit="cover", px=900), cols="1fr 190pt", gap=16, align="start")
    book.page("Service", body, toc="Service &amp; Support")


def world_page(book):
    body = (title("Global manufacturing &amp; sales network", "Dener worldwide")
            + fig("gfl/world.jpg", h=300, px=2200)
            + stats([("52+", "Years of experience"), ("100+", "Exports to countries"), ("14,000,000 sq ft", "Production campus (1,300,000 m²)")])
            + P("Dener Makina A.Ş. reserves the right to modify catalog information and machine specifications without obligation to notify.",
                cls="note"))
    book.page("Dener worldwide", body, toc="Dener Worldwide")


RANGE = [("Press brakes", [("range/hydraulic.png", "Hydraulic press brake"), ("range/tandem.jpg", "Tandem press brake"),
                           ("range/servo.png", "Servo-electric press brake"), ("range/ballscrew.png", "Ball-screw press brake")]),
         ("Panel bender", [("range/panel.png", "Panel bender")]),
         ("Shears", [("range/shear-cnc.png", "CNC hydraulic shear"), ("range/shear-nc.png", "NC hydraulic shear")]),
         ("Laser cutting machines", [("range/gfl.png", "GFL fiber laser cutting machine"), ("range/smart.png", "Smart fiber laser cutting machine"),
                                     ("range/tube.png", "Tube profile laser cutting machine")]),
         ("Machine tools", [("range/lathe.png", "CNC lathe"), ("range/vmc.png", "CNC vertical milling machine"),
                            ("range/double-column.png", "Double-column milling machine"), ("range/5-axis.png", "5-axis machining center"),
                            ("range/grinder.png", "NC grinding machine")])]


def range_page(book):
    def items(lst, h):
        return "".join(f'<div class="rg"><div class="ri" style="height:{h}pt"><img src="{im(i, 900)}"></div><span>{t}</span></div>' for i, t in lst)
    pb, panel, shears, lasers, tools = RANGE
    body = (title("“The future is here” · available through NovoTech", "Dener product range")
            + '<style>.rg span{font:500 8.6pt/1.2 Oswald;color:%s;display:block;margin-top:4pt}.ri{display:flex;align-items:center;'
              'justify-content:center}.ri img{max-width:100%%;max-height:100%%;object-fit:contain}</style>' % CHAR
            + h2(pb[0]) + f'<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:12pt">{items(pb[1], 84)}</div>'
            + row(h2(panel[0]) + items(panel[1], 84), h2(shears[0]) + f'<div class="grid" style="grid-template-columns:1fr 1fr;gap:12pt">'
                  f'{items(shears[1], 84)}</div>', cols="1fr 2fr", gap=18)
            + h2(lasers[0]) + f'<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:12pt">{items(lasers[1], 84)}</div>'
            + h2(tools[0]) + f'<div class="grid" style="grid-template-columns:repeat(5,1fr);gap:10pt">{items(tools[1], 68)}</div>')
    book.page("Dener product range", body, toc="Dener Product Range")


def diagram(center, labels):
    """the catalogue's 'rigid and optimized body structure' wheel: a centre disc and five labels round it"""
    pos = {"tl": ("left:2pt;top:8pt", ""), "tr": ("right:2pt;top:8pt", ""), "l": ("left:0;top:60pt", ""),
           "r": ("right:0;top:60pt", ""), "b": ("left:50%;bottom:0;transform:translateX(-50%)", "")}
    spans = "".join(f'<div class="l" style="{pos[k][0]}">{t}</div>' for k, t in labels)
    svg = ('<svg viewBox="0 0 250 132" preserveAspectRatio="none"><g stroke="%s" stroke-width="1.1" fill="none">'
           '<path d="M92 20 L106 38"/><path d="M158 20 L144 38"/><path d="M78 64 L88 64"/><path d="M172 64 L162 64"/>'
           '<path d="M125 104 L125 116"/></g></svg>' % ORANGE)
    return f'<div class="diag">{svg}<div class="c">{center}</div>{spans}</div>'


def spec_rows_gfl_catalogue():
    return [("Machine model", "GFL"), ("Table size", "3015 · 4020 · 6020<br><small>10 × 5 ft · 13 × 6.6 ft · 20 × 6.6 ft</small>"),
            ("Power", "3,000 W · 6,000 W · 12,000 W · 20,000 W · 30,000 W · 40,000 W"), ("Precision", "±0.0012″ (±0.03 mm)"),
            ("Max. speed", "394 ft/min (120 m/min)"), ("Max. acceleration", "1.5 G"), ("Voltage and frequency", "380 V 50 Hz / 60 Hz")]


# ---------------------------------------------------------------------------------------------------------- GFL catalogue
def book_gfl():
    b = Book("gfl", "GFL fiber laser", "Dener GFL fiber laser cutting machine",
             os.path.join(ROOT, "src", "files", "NovoTech-Dener-GFL-Fiber-Laser-2026.pdf"))
    b.title, b.subject = "Dener GFL Fiber Laser — NovoTech Machine Tools", "Dener GFL fiber laser cutting machine catalogue, imperial edition"
    b.cover("Dener · GFL fiber laser", "“The future is here” · sold &amp; serviced in Canada by NovoTech", "GFL", "Fiber laser",
            "Faster cutting · higher precision · maximum efficiency", "dn-gfl-1",
            [("Since 1974", "Manufacturing experience"), ("3 – 40 kW", "Laser source power"), ("10 – 20 ft", "Table length"),
             ("Canada", "Parts &amp; technical support")], hero_h=380)
    about_page(b)
    campus_page(b)
    # catalogue p3 — design advantages
    body = (title("GFL series", "GFL series — design advantages")
            + fig("gfl/open-front.png", "GFL with the front door open: cutting area and swivelling control unit", h=258, px=1400)
            + P("Through optic technology, DENER Fiber Laser Machine is able to achieve high-speed performance while cutting 2D sheet metal. "
                "Equipped with various cutting modes and well-known fiber laser sources, Dener fiber laser can easily cut challenging parts. "
                "A well-thought-out design allows easy transport and installation with a machine equipped with a user-friendly interface. "
                "Speed achieved on X, Y, and Z axes is significantly satisfying and allows fast return on investment combined with cutting precision.",
                "Dener body frame was designed and manufactured regarding user needs. With a stress-relief robust body structure and a bridge "
                "designed with space geometry, the machine is ready to encounter high acceleration.",
                "Six aspiration pneumatic compartments are also available on this model to facilitate the suction of polluted fume resulting "
                "from cutting. Small parts that fall during the cutting process can be found in one of the six scrap boxes mounted on suitable "
                "wheels that are easy to remove. The machine is adapted to work with an aspiration system that can collect all the fume "
                "resulting from the cutting process.",
                "From choosing high quality steel, followed by a welding art, the frame passes through stress relief process. The remaining "
                "machining of the parts is made on very precise 5 axis portal milling boring machine. The obtained final frame is rigid, "
                "ergonomic and highly resistant to high speed displacements of the bridge."))
    b.page("Design advantages", body, toc="Design Advantages")
    # catalogue p4 — the machine
    labels = pct((628, 410, 1176, 762), [("Control unit", (673.4, 467.0, 753.9, 483.9)), ("LED", (804.7, 436.9, 828.9, 453.7)),
                                          ("Compact body", (861.1, 476.2, 958.7, 493.1)), ("Protective glass", (940.3, 418.0, 1047.3, 434.8)),
                                          ("Pallet", (1064.2, 499.1, 1102.3, 515.9)), ("Light curtain", (1066.7, 720.2, 1153.9, 737.1)),
                                          ("Scrap box", (851.9, 737.6, 918.2, 754.4))])
    body = (title("GFL fiber laser cutting machine", "GFL fiber laser cutting machine")
            + row(h2("Differentiating features") + checks(["Advanced hardware, best in class", "Advanced remote access and ease of control",
                                                         "High security and easy maintenance", "Ease of use with Windows-based operating system"]),
                  diagram("Rigid and<br>optimized<br>body structure", [("tl", "High speed"), ("tr", "High cutting quality"),
                                                                     ("l", "Low cost"), ("r", "High technology"), ("b", "Quality components")]),
                  cols="1fr 1fr", gap=20, align="center")
            + '<div style="margin-top:14pt">' + labelled("gfl/machine-labelled.jpg", labels, h=330) + "</div>")
    b.page("GFL fiber laser", body, toc="GFL Fiber Laser Cutting Machine")
    # catalogue p5 — laser power
    body = ('<div class="photo-panel" style="height:600pt;margin-top:-4pt"><img src="%s">'
            '<div style="position:absolute;left:18pt;top:16pt;right:18pt"><div style="font:700 30pt/1.05 Oswald;color:#fff;text-transform:uppercase">'
            'Laser power</div><div style="font:500 17pt/1.2 Oswald;color:#fff">Moves your production forward</div>'
            '<div style="width:60pt;height:3.7pt;background:%s;margin-top:8pt"></div></div>'
            '<div class="overlay"><div class="st"><div><b>High laser</b><span>Precision</span></div><div><b>High-speed</b><span>Cutting</span></div>'
            '<div><b>Lower energy</b><span>Consumption</span></div><div><b>Lower</b><span>Operating cost</span></div></div>'
            '<p><b>GFL Series</b> delivers speed, precision and efficiency for modern production.</p></div></div>'
            % (im("gfl/laser-power.jpg", 1400), ORANGE))
    b.page("Laser power", body, toc="Laser Power")
    software_page(b)
    head_page(b)
    # catalogue p8 — equipment
    cards = [card("gfl/resonator-2.png", "Laser resonator", P("It offers high electro-optical conversion efficiency, excellent beam quality, "
                  "and high energy density. With a wide modulation frequency range, strong reliability, long service life, and maintenance-free "
                  "operation, it delivers stable and efficient laser performance.", cls="sm")
                  + f'<img src="{im("gfl/resonator-1.png", 600)}" style="height:46pt;object-fit:contain">', h=128),
             card("gfl/chiller.png", "Chiller", P("The chiller continuously communicates with the CNC control unit to maintain the optimal "
                  "operating temperature for the laser source and cutting head. This improves process stability, protects critical components, "
                  "and supports consistent cutting quality during long production cycles.", cls="sm"), h=128),
             card("gfl/light-curtain.png", "Light curtain", P("The light curtain is designed to ensure operator safety during pallet change "
                  "operations. It detects any intrusion into the protected area and immediately triggers the necessary safety response, helping "
                  "prevent accidents and ensuring safe machine operation.", cls="sm"), h=128),
             card("gfl/rack-pinion.png", "Rack and pinion system", P("The rack and pinion system enhances positioning accuracy while providing "
                  "ease of assembly, reduced wear, and long service life. Thanks to this component, movement across various axes is achieved "
                  "with a positioning tolerance of ±0.002″ (±0.05 mm), ensuring stable and precise axis motion performance.", cls="sm")
                  + f'<img src="{im("gfl/rack-graphs.png", 900)}" style="width:100%;height:44pt;object-fit:contain">', h=128)]
    b.page("Equipment", title("Laser resonator · chiller · light curtain · rack and pinion", "Equipment") + grid(cards, 2, 20), toc="Equipment")
    cards = [card("gfl/z-axis.png", "Performant Z axis", P("The Dener fiber laser Z axis is designed and configured to reach a speed of 1G. "
                  "The Z axis can handle high acceleration while maintaining cutting accuracy. Ahead of its competitors, the Z axis on the GFL "
                  "model has a stroke length of 13.8″ (350 mm).", cls="sm"), h=150),
             card("gfl/welded-frame.png", "Compact welded frame", P("From choosing high-quality steel, followed by the art of welding, the "
                  "frame passes through a stress-relief process. The remaining machining of the parts is carried out on a highly precise "
                  "5-axis portal milling and boring machine. The obtained final frame is rigid, ergonomic, and highly resistant to "
                  "high-speed displacements of the bridge.", cls="sm"), h=150),
             card("gfl/cutting-tables.png", "Cutting tables", P("The shuttle table system consists of two moving tables. While the cutting "
                  "process continues on the table inside the machine, the other table can be used to load sheets or collect processed parts.", cls="sm"), h=150),
             card("gfl/scrap-boxes.png", "Scrap boxes", P("With an ergonomic design, scrap boxes are easy to pull and small parts and scrap "
                  "can be easily reached. Optionally, a CNC-controlled conveyor can be included.", cls="sm"), h=150)]
    b.page("Equipment", title("Z axis · welded frame · cutting tables · scrap boxes", "Equipment") + grid(cards, 2, 20))
    ease_page(b)
    # catalogue p11 — the GFL
    body = (title("GFL fiber laser", "GFL fiber laser")
            + fig("dn-gfl-1", "GFL fiber laser — closed cabin with the control unit", h=228, px=2200)
            + fig("dn-gfl-2", "GFL fiber laser — shuttle table side", h=212, px=2200)
            + '<div class="badges" style="margin-top:10pt">' + "".join(f'<img src="{im(x, 700)}">' for x in
                                                                     ("gfl/badge-support.jpg", "gfl/badge-speed.jpg", "gfl/badge-cost.jpg")) + "</div>")
    b.page("GFL fiber laser", body)
    body = (title("GFL series", "Technical specifications")
            + kv(spec_rows_gfl_catalogue(), head=["Technical specifications", "GFL series"])
            + P("*Cutting thicknesses may vary due to factors such as material quality, operator settings, and cutting speed.", cls="note")
            + P("Custom voltage available: 208 V, 240 V, 480 V or 600 V 3-phase. CSA-approved electrical panel.", cls="note")
            + '<div style="margin-top:14pt">' + fig("dn-gfl-3", h=236, px=2000) + "</div>" + included())
    b.page("Technical specifications", body, toc="Technical Specifications")
    service_page(b)
    world_page(b)
    range_page(b)
    b.back("Fiber laser for your shop.", ["dn-gfl-1", "dn-gfl-2", "dn-gfl-3", "dn-gfl-control"])
    fill_about(b)
    return b


# -------------------------------------------------------------------------------------------------------- Smart catalogue
def book_smart():
    from dener_data import nom_ft, mmin
    b = Book("smart", "Smart fiber laser", "Dener Smart fiber laser cutting machine",
             os.path.join(ROOT, "src", "files", "NovoTech-Dener-Smart-Fiber-Laser-2026.pdf"))
    b.title, b.subject = "Dener Smart Fiber Laser — NovoTech Machine Tools", "Dener Smart fiber laser cutting machine catalogue, imperial edition"
    b.cover("Dener · Smart fiber laser", "“The future is here” · sold &amp; serviced in Canada by NovoTech", "Smart", "Fiber laser",
            "Faster cutting · higher precision · maximum efficiency", "dn-smart-1",
            [("Since 1974", "Manufacturing experience"), ("3 – 40 kW", "Laser source power"), ("10 – 82 ft", "Table length"),
             ("Canada", "Parts &amp; technical support")], hero_h=380)
    about_page(b)
    campus_page(b)
    body = (title("Smart series", "Smart series — design advantages")
            + fig("smart/open-front.png", "Smart with the front open: cutting area, CNC control unit and remote handset", h=300, px=1400)
            + P("Through optic technology, DENER Fiber Laser Machine is able to achieve high speed performance while cutting 2D sheet metal. "
                "Equipped with various cutting modes and well-known fiber laser source, Dener fiber laser can easily cut challenging parts. "
                "A well thought design that allows easy transport and installation with a machine equipped with a user friendly equipment. "
                "Speed achieved on X, Y and Z axis are significantly satisfying and allow a fast return on investment combined with cutting precision.",
                "Our machine body with a stress relief robust body structure and a bridge designed with space geometry, the machine is ready to "
                "encounter high acceleration.",
                "Six aspiration pneumatic compartments are also available on this model to facilitate the suction of polluted fume resulting "
                "from cutting. Small parts that fall during the cutting process can be found in one of the six scrap boxes mounted on suitable "
                "wheels that are easy to remove. The machine is adapted to work with an aspiration system that can collect all the fume "
                "resulting from the cutting process."))
    b.page("Design advantages", body, toc="Design Advantages")
    labels = pct((600, 334, 1190, 762), [("Scrap box", (773.6, 729.8, 854.6, 750.2)), ("Compact body", (715.7, 393.1, 830.6, 413.5)),
                                         ("Pallet", (630.5, 454.4, 675.9, 474.7)), ("Protective glass", (958.2, 349.6, 1088.6, 370.0)),
                                         ("Control unit", (1081.8, 368.6, 1177.3, 389.0))])
    body = (title("Smart fiber laser cutting machine", "Smart fiber laser cutting machine")
            + row(h2("Design advantages") + checks(["Precise positioning", "Optimized energy efficiency", "Ergonomic and compact design",
                                                  "Advanced safety standards", "Low maintenance cost"]),
                  diagram("Rigid and<br>optimized<br>body structure", [("tl", "High speed"), ("tr", "High cutting quality"),
                                                                     ("l", "Low cost"), ("r", "High technology"), ("b", "Quality components")]),
                  cols="1fr 1fr", gap=20, align="center")
            + '<div style="margin-top:14pt">' + labelled("smart/machine-labelled.jpg", labels, h=360) + "</div>")
    b.page("Smart fiber laser", body, toc="Smart Fiber Laser Cutting Machine")
    body = ('<div class="photo-panel" style="height:600pt;margin-top:-4pt"><img src="%s">'
            '<div style="position:absolute;left:18pt;top:16pt;right:18pt"><div style="font:700 30pt/1.05 Oswald;color:#fff;text-transform:uppercase">'
            'Precision meets<br>performance</div><div style="font:500 15pt/1.2 Oswald;color:#fff;margin-top:4pt">Advanced laser cutting for modern production</div>'
            '<div style="width:60pt;height:3.7pt;background:%s;margin-top:8pt"></div></div>'
            '<div class="overlay"><div class="st"><div><b>Superior</b><span>Cut accuracy</span></div><div><b>Faster</b><span>Throughput</span></div>'
            '<div><b>Energy</b><span>Efficient operation</span></div><div><b>Lower</b><span>Operating cost</span></div></div>'
            '<p><b>SMART Series</b> delivers speed, precision and efficiency for modern production.</p></div></div>'
            % (im("smart/precision.jpg", 1400), ORANGE))
    b.page("Precision meets performance", body, toc="Precision Meets Performance")
    software_page(b)
    head_page(b)
    cards = [card("smart/raycus.png", "Resonator", P("Raycus is a global brand that stands out in the laser processing industry with its "
                  "reliability, long lifespan, and high performance. With stable power output, precise cutting quality, and an excellent "
                  "price-to-performance ratio, it is one of the most preferred laser resonators worldwide.", cls="sm"), sub="Raycus RFL series", h=128),
             card("smart/chiller.png", "Chiller", P("Specially developed for fiber laser cutting machines, S&amp;A chillers provide stable "
                  "temperature control for resonators and optical systems, enhancing cutting quality and machine lifespan. Thanks to its "
                  "dual-circuit cooling design, it independently balances the resonator and optical path. Its compact design allows for easy "
                  "integration, while quiet operation and energy-efficient performance help lower operating costs. With low maintenance "
                  "requirements, it is an ideal solution for long-term, uninterrupted operation.", cls="sm"), sub="S&amp;A CWFL series", h=128),
             card("smart/fscut.png", "FSCUT control unit", P("The FSCUT control unit, specially developed for fiber laser cutting machines, "
                  "elevates cutting speed and quality to the next level thanks to its high performance and advanced software support. It "
                  "intelligently optimizes cutting parameters, delivering stable and fast performance even in complex geometries. With its "
                  "user-friendly interface, it offers easy programming capability, operates with fewer errors, and contributes to achieving "
                  "higher overall efficiency.", cls="sm"), h=128),
             card("smart/servo.png", "Servo motor and motor driver", P("For high-precision motion control in fiber laser cutting machines, "
                  "Inovance motor and drive systems deliver superior performance and reliability. With high response speeds and stable torque "
                  "output, they ensure maximum accuracy in axis movements. Advanced control algorithms minimize vibration, improving cutting "
                  "quality and extending machine lifespan. Their compact design allows for easy installation and wiring. With energy-efficient "
                  "operation and high dynamic performance, Inovance systems bring power.", cls="sm"), sub="Inovance", h=128)]
    b.page("Equipment", title("Resonator · chiller · FSCUT control · servo drives", "Equipment") + grid(cards, 2, 20), toc="Equipment")
    cards = [card("smart/reducer.png", "Reducer", P("Techmech gearboxes are specially preferred in fiber laser cutting machines for "
                  "high-precision motion transmission. With their high torque capacity and low backlash design, they ensure maximum accuracy "
                  "in axis movements. Their compact structure provides space efficiency in machine design, while the durable materials and "
                  "high efficiency rate offer long-lasting and trouble-free operation.", cls="sm"), sub="Techmech", h=128),
             card("smart/rack.png", "Rack and pinion", P("TWEBOLUN pinion and rack systems are specially designed for high-precision axis "
                  "movements in fiber laser cutting machines. With low backlash and stable power transmission, they accurately follow cutting "
                  "paths, ensuring high precision even in complex geometries. Durable materials and long-lasting design provide uninterrupted "
                  "performance in production. Easy installation and low maintenance requirements enhance operational efficiency.", cls="sm"),
                  sub="TWEBOLUN", h=128),
             card("smart/smc.png", "Gas regulator", P("SMC regulators provide high precision and stability in pressure control for fiber "
                  "laser cutting machines. They contribute to the safe, efficient, and long-lasting operation of air systems, optimizing the "
                  "overall performance of the machine. Produced by Japan-based SMC Corporation, these regulators offer a reliable solution "
                  "worldwide for industrial automation and pneumatic control systems.", cls="sm"), sub="SMC", h=128),
             card("smart/scrap-boxes.png", "Scrap boxes", P("With an ergonomic design, scrap boxes are easy to pull and small parts and scrap "
                  "can be easily reached. Optionally, a CNC-controlled conveyor can be included.", cls="sm"), h=128)]
    b.page("Equipment", title("Reducer · rack and pinion · gas regulator · scrap boxes", "Equipment") + grid(cards, 2, 20))
    ease_page(b)

    def badges(*names):
        return '<div class="badges" style="margin-top:10pt">' + "".join(f'<img src="{im("gfl/badge-" + n + ".jpg", 700)}">' for n in names) + "</div>"

    def sizes(codes):
        return " · ".join(codes) + "<br><small>" + " · ".join(f"{nom_ft(int(c[:-2]) * 100)} × {nom_ft(int(c[-2:]) * 100)}" for c in codes) + " ft</small>"

    power = "3,000 W · 6,000 W · 12,000 W · 20,000 W · 30,000 W · 40,000 W"
    note = (P("*Cutting thicknesses may vary due to factors such as material quality, operator settings, and cutting speed.", cls="note")
            + P("Custom voltage available: 208 V, 240 V, 480 V or 600 V 3-phase. CSA-approved electrical panel.", cls="note"))
    body = (title("Smart fiber laser · closed type series", "Smart fiber laser")
            + fig("dn-smart-1", "Smart Laser 6020 — closed cabin", h=226, px=2200)
            + fig("dn-smart-2", "Smart closed type — shuttle table", h=214, px=2200) + badges("support", "speed"))
    b.page("Closed type series", body, toc="Closed Type Series")
    body = ('<div class="eyebrow" style="margin-bottom:2pt">Closed type / double table</div>'
            '<h1>Engineered for speed</h1><h1 style="color:%s">Built for value</h1><div class="rule" style="margin-bottom:14pt"></div>' % OR2
            + kv([("Machine model", "Smart"), ("Table size", sizes(["3015", "4020", "6020", "6025", "8025", "12526"])), ("Power", power),
                  ("Precision", "±0.0012″ (±0.03 mm)"), ("Max. speed", mmin(140)), ("Max. acceleration", "1 G"),
                  ("Voltage and frequency", "380 V 50 Hz / 60 Hz")], head=["Technical specifications", "Closed type / double table"])
            + note + included())
    b.page("Technical specifications", body)
    body = (title("Smart fiber laser · semi closed type series", "Smart fiber laser")
            + fig("smart/semi-top.jpg", "Smart semi closed type — single table, the cabin travels with the gantry", h=200, px=2000)
            + row(fig("smart/semi-close.jpg", h=150, px=1400), fig("smart/semi-rear.png", h=150, px=1400), gap=14)
            + badges("support", "cost"))
    b.page("Semi closed type series", body, toc="Semi Closed Type Series")
    body = ('<div class="eyebrow" style="margin-bottom:2pt">Semi closed type / single table</div>'
            '<h1>Designed for flexibility</h1><h1 style="color:%s">Built for productivity</h1><div class="rule" style="margin-bottom:14pt"></div>' % OR2
            + kv([("Machine model", "Smart"), ("Table size", sizes(["6025", "8025", "12525", "14035", "16045", "25031", "25040"])),
                  ("Power", power), ("Precision", "±0.0004″ (±0.01 mm)"), ("Max. speed", mmin(75)), ("Max. acceleration", "0.6 G"),
                  ("Voltage and frequency", "380 V 50 Hz / 60 Hz")], head=["Technical specifications", "Semi closed type / single table"])
            + note + included())
    b.page("Technical specifications", body)
    service_page(b)
    world_page(b)
    range_page(b)
    b.back("Fiber laser for your shop.", ["dn-smart-1", "dn-smart-2", "smart/semi-top.jpg", "smart/open-front.png"])
    fill_about(b)
    return b


# ------------------------------------------------------------------------------------- GFL full technical specification
def frac_cell(mm):
    from dener_data import frac_in
    return f"{frac_in(mm)}<br><small>({mm} mm)</small>"


def book_spec():
    from dener_data import weight, mmin
    b = Book("spec", "GFL fiber laser — technical specification", "Dener PRO 3015 · GFL 3015 L / 4020 L / 6020 L · 6 &amp; 12 kW",
             os.path.join(ROOT, "src", "files", "NovoTech-Dener-GFL-Fiber-Laser-Technical-Specification-2026.pdf"))
    b.title = "Dener GFL Fiber Laser — Full Technical Specification — NovoTech Machine Tools"
    b.subject = "Dener PRO 3015 6 & 12 kW / GFL 3015 L, 4020 L, 6020 L fiber laser cutting machine — full technical specification, imperial edition"
    b.cover("Dener · GFL full technical specification", "PRO-3015 · 6 &amp; 12 kW · compact fiber laser technology", "GFL fiber laser",
            "Technical specification", "Your partner in laser cutting machines", "dn-gfl-1",
            [("Since 1974", "Manufacturing experience"), ("6 &amp; 12 kW", "Raycus · FSCUT"), ("1.5 G", "X-Y acceleration"),
             ("Canada", "Parts &amp; technical support")], hero_h=380)
    b.page("Contents", "@@TOC@@", header="Technical specification", sub="Contents")
    # 1 — Dener Machinery
    flags = ('<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:14pt;margin-top:8pt">'
             + "".join(f'<div><img src="{im(f, 400)}" style="height:34pt;border:.6pt solid #ddd"><h3 style="margin-top:5pt">{c}</h3>'
                       f'{checks(o, cls="sm")}</div>' for f, c, o in [
                           ("pro/flag-tr.png", "Türkiye", ["Dener Makina headquarter — Kayseri", "Representative — Bursa", "Representative — İstanbul",
                                                         "Representative — İzmir", "Representative — Anatolian region"]),
                           ("pro/flag-in.png", "India", ["Dener Makina office &amp; showroom — Pune"]),
                           ("pro/flag-us.png", "USA", ["Dener Makina office &amp; showroom — Chicago"])]) + "</div>")
    body = (title("1 · Dener Machinery", "About Dener")
            + fig("pro/campus-labelled.jpg", "Dener campus, Kayseri: machine tool assembly, sheet metal machine fabrication, assembly and welding "
                  "halls, tooling workshop, machine covers fabrication, headquarters and showroom", h=232, fit="cover", px=2000)
            + P("Dener Makina, established in 1974 in Kayseri / Turkey, is globally recognized as one of the best sheet metal machine "
                "manufacturers. With 800 expert employees and a production capacity of 3,400 machines, Dener constantly improves its production technology.",
                "The company is located on a 14,000,000 sq ft (1,300,000 m²) site with 1,670,000 sq ft (155,000 m²) of closed area and exports to "
                "more than 100 countries, mainly to European Union countries, the USA and Asia. All Dener machines meet EU standards and a strict "
                "quality control is made at every stage of production.", cls="sm")
            + row(h3("Dener group product range — sheet metal division") + checks(["Fiber laser cutting machines", "100% electrical press brakes (widest range)",
                                                                                "Hydraulic press brakes", "Tandem press brakes", "Plasma cutting machines",
                                                                                "Hydraulic shearing machines"], cls="sm"),
                  h3("Machining division") + checks(["Vertical milling machines", "Lathes", "Surface grinding machines"], cls="sm"), cols="1.3fr 1fr")
            + flags)
    b.page("About", body, key="dener")
    # 2 — machine information
    labels = pct((60, 272, 525, 496), [("Aspiration system (option)", (122.1, 307.9, 184.0, 325.4)), ("LED", (320.0, 292.5, 332.8, 301.0)),
                                       ("Compact body", (360.8, 300.9, 409.7, 309.4)), ("Protective glass", (407.4, 325.7, 462.0, 334.2)),
                                       ("Pallet", (456.2, 347.7, 477.8, 356.2)), ("Control unit", (241.5, 279.5, 282.2, 288.0)),
                                       ("Chiller", (100.2, 483.3, 122.1, 491.8)), ("Scrap box", (392.3, 468.6, 426.6, 477.1)),
                                       ("Light curtain", (469.2, 451.8, 512.6, 460.3))])
    body = (title("2 · Machine information · 2.1 machine concept", "Machine specification")
            + P("Through optic technology, the DENER fiber laser machine is able to achieve high-speed performance while cutting 2D sheet metal. "
                "Equipped with various cutting modes and well-known fiber laser sources, the Dener fiber laser can easily cut challenging parts. "
                "A well-thought design allows easy transport and installation, with a machine equipped with user-friendly equipment. Speeds "
                "achieved on the X, Y and Z axes are significantly satisfying and allow a fast return on investment combined with cutting precision.", cls="sm")
            + labelled("pro/machine-labelled.jpg", labels, h=258)
            + P("The Dener body frame was designed and manufactured around the user's needs. With a stress-relieved, robust body structure and a "
                "bridge designed with space geometry, the machine is ready for high acceleration.",
                "Six pneumatic aspiration compartments are also available on this model to facilitate the suction of the polluted fume resulting "
                "from cutting. Small parts that fall during the cutting process can be found in one of the six scrap boxes mounted on wheels that are "
                "easy to remove. The machine is adapted to work with an aspiration system that can collect all the fume resulting from the cutting "
                "process. The cutting tables were designed to reduce the exchange time, therefore increasing productivity.", cls="sm"))
    b.page("Machine information", body, key="info")
    # 3 — fiber laser advantages
    body = (title("3 · Fiber laser advantages", "Fiber laser technology advantages")
            + P("Compared to CO2 laser technology, fiber laser technology requires less maintenance and its operation consumes less energy. "
                "While a CO2 laser requires 3 – 4 hours of maintenance per week, a fiber laser requires far less maintenance.",
                "Fiber lasers cut reflective materials such as copper, brass, aluminum and stainless steel, operations that are not possible on a CO2 laser.",
                "Cutting thickness limits on fiber lasers are disappearing over time. A 20 kW laser source is able to cut 2-3/8″ (60 mm) mild steel, "
                "and higher power sources are also available.",
                "Fiber laser technology is the best alternative to the CO2 laser, as the shorter wavelength and higher power at the focal point make "
                "cutting easier. The fiber laser combines a fast return on investment, lower production cost, high profitability and lower "
                "maintenance. Contrary to CO2, a fiber laser does not require a warm-up stage before it can cut.", cls="sm")
            + row(h2("Keywords") + checks(["Fast", "Reliable", "High quality cutting", "Affordable", "High technology", "Rigid body frame",
                                          "Quality components", "Low operating cost", "Low maintenance cost"]),
                  fig("pro/advantages-icons.png", h=200, px=1100), cols="1fr 1.2fr", gap=20, align="center")
            + fig("pro/parts.jpg", "Parts cut on a Dener fiber laser", h=118, px=1800))
    b.page("Fiber laser advantages", body, key="adv")
    # 4 — design and manufacturing
    body = (title("4 · Design and manufacturing advantages", "Dener manufacturing")
            + P("All DENER machines are manufactured with respect to European safety norms. A meticulous control is made at every step of the "
                "production line, enhancing the quality of the final product. The ERP system we use gives real-time visibility on the production "
                "process. DENER only uses quality components from well-known suppliers.", cls="sm")
            + h2("Compact welded frame")
            + P("From choosing high-quality steel, followed by the art of welding, the frame passes through a stress-relief process. The remaining "
                "machining of the parts is made on a very precise 5-axis portal milling and boring machine. The final frame is rigid, ergonomic and "
                "highly resistant to high-speed displacements of the bridge.", cls="sm")
            + fig("pro/frame.png", h=190, px=2000)
            + h2("Bridge")
            + P("The DENER fiber laser bridge is designed with space geometry and ensures stability and precision during the cutting process. "
                "The bridge can easily operate at high speed.", cls="sm")
            + fig("pro/bridge.png", h=150, px=1400))
    b.page("Design &amp; manufacturing", body, key="design")
    # 5.5 / 5.6 — rack and pinion, Z axis
    body = (title("5 · Machine components and options", "Rack and pinion · Z axis")
            + P("<i>Dener reserves the right to replace components with newer, better-performing systems.</i>", cls="sm")
            + h2("Rack and pinion system", "Framo Morat")
            + row(P("The advanced combination of planetary gearbox, pinion, rack and lubrication systems results in a high-end linear motion "
                    "system. Positioning accuracy is enhanced, assembly is easy, wear is low and service life is long.",
                    "Thanks to these genuine components, displacement on the various axes is accomplished with a positioning tolerance of "
                    "±0.002″ (±0.05 mm) — positioning of the axis, not cutting precision.", cls="sm"),
                  fig("pro/rack-pinion.png", h=120, px=800), cols="1.4fr 1fr", align="center")
            + fig("pro/rack-graphs.png", h=62, px=1200)
            + h2("Performant Z axis")
            + P("The Dener fiber laser Z axis is designed and configured to reach 1 G. The Z axis can handle high acceleration while keeping its "
                "cutting accuracy. Ahead of its competitors, the Z axis on the GFL model has a stroke of 13.8″ (350 mm).", cls="sm")
            + labelled("pro/z-axis.png", [("13.8″ (350 mm) stroke", 78, 30)], h=200, px=1400))
    b.page("Components", body, key="rack")
    # GFL L technical information + Boji head
    body = (title("GFL 3015 L · GFL 4020 L · GFL 6020 L", "Technical information")
            + kv([("X axis", mmin(120)), ("Y axis", mmin(120)), ("Positioning tolerance", "±0.002″ (±0.05 mm)"),
                  ("Repeatability", "±0.0012″ (±0.03 mm)")], head=["Axis", "GFL 3015 L · 4020 L · 6020 L"])
            + P("Note: the information given is for the axes, not for cutting.", cls="note")
            + h2("5.3 · Automatic laser cutting head", "Boji BLT 421 · standard")
            + P("The BLT 4 series delivers great performance with stable cutting and simple installation and setup, and is available for power "
                "levels below 30 kW. Thanks to the capacitive sensor, the offset can be set directly from the sheet position.", cls="sm")
            + row(fig("pro/boji-1.png", h=220, px=700),
                  checks(["Brand new optical solutions come with closed-loop auto focusing", "Slag-free cutting, nozzle cooling and water "
                          "cooling sensor supported — makes cutting more stable and efficient", "<b>Ready-to-use optics drawer: lens changed in 2 minutes</b>",
                          "<b>Groups of internal sensors for real-time closed-loop monitoring</b>"]) + qrbox("Scan to watch GFL videos on NovoTechMachineTools.com"),
                  fig("pro/boji-2.png", h=220, px=700), cols="1fr 1.5fr 1fr", gap=14, align="center"))
    b.page("Cutting head", body, key="boji")
    # Precitec
    body = (title("5.3.2 · Cutting head · option", "Precitec ProCutter 2.0")
            + P("With the ProCutter 2.0, cutting processes that were previously hidden away can now be used in an industrially stable manner. "
                "It is no longer necessary to choose between high quality and high speed: both are possible — increased machine utilization and a "
                "shorter payback period. The amount of rework is reduced to a minimum.")
            + fig("pro/precitec-1.png", h=210, px=1300) + fig("pro/precitec-2.png", h=230, px=1300)
            + row(checks(["Maximum productivity thanks to superior technology", "Around-the-clock consistent cut quality at high laser power",
                          "Intelligent sensors at their best"]), qrbox("Scan to watch GFL videos on NovoTechMachineTools.com"), cols="1.6fr 1fr", align="center"))
    b.page("Precitec (option)", body, key="precitec")
    # Raycus
    body = (title("5.2.1 · Power source · standard", "Raycus fiber laser power source")
            + P("The single-module CW fiber laser is completely researched, developed and produced by Raycus independently. Raycus has an "
                "efficient and professional R&amp;D and production team. The single-module CW fiber laser series not only meets the diversified "
                "demands of customers to the greatest extent, but also provides a personal customization service. The laser output connector is "
                "QBH, with multiple control modes. Its good compatibility has been widely recognized by the market, and the product sells well at "
                "home and abroad.",
                "It has the advantages of high electro-optical conversion efficiency, good beam quality, high energy density, wide modulation "
                "frequency, strong reliability, long life and maintenance-free operation. It can be widely used in welding, precision cutting, "
                "cladding, surface treatment, 3D printing and other fields. Its optical fiber output makes it easier to integrate with robots into "
                "flexible manufacturing equipment to meet the needs of metal processing.", cls="sm")
            + row(fig("pro/raycus-1.png", h=130, px=900), fig("pro/raycus-2.png", h=230, px=1300), cols="1fr 1.5fr", align="center")
            + '<div class="stats" style="margin-top:12pt"><div><b>From 2 kW to 20 kW</b><span>Raycus fiber laser power sources</span></div></div>')
    b.page("Raycus (standard)", body, key="raycus")
    # IPG
    body = (title("5.2.2 · Power source · optional", "IPG fiber laser power source")
            + P("YLS-CUT lasers have been developed specifically for demanding cutting applications. Supplied in the smallest form factor "
                "available on the market, these lasers can be easily integrated within cutting machines. The lasers are packaged in a hermetically "
                "sealed cabinet containing an internal dryer, enabling the laser to be used in the harshest of production environments.",
                "The YLS-CUT incorporates the latest IPG technical improvements in the design of diode modules, fiber blocks, digital power "
                "supplies and digital control electronics, resulting in unparalleled reliability and increased control flexibility, stability and "
                "precision. The new control system allows integrated control of both the laser and the process subsystem. The industry-leading "
                "wall-plug efficiency of over 40% results in electrical cost savings adding up to many tens of thousands of dollars over the "
                "lifetime of a laser. Hot redundancy ensures 100% uptime with no change in power, record reliability and maintenance-free operation.",
                "The CUT series lasers are available up to 20 kW output power with a wide variety of fiber delivery options, starting at a 50 µm "
                "core diameter. The YLS-U is the latest super-compact hermetic cabinet packaging in the 1 – 10 kW power range, incorporating all "
                "the features and technology advancements of the YLS-CUT series. YLS-U series lasers are also available with the High Peak Power "
                "(HPP) option, enabling faster and cleaner piercing, increased quality of fine-feature cutting and denser part nesting.", cls="sm")
            + fig("pro/ipg.png", h=210, px=1300)
            + '<div class="stats" style="margin-top:10pt"><div><b>From 2 kW to 20 kW</b><span>IPG YLS fiber laser power sources (optional)</span></div></div>')
    b.page("IPG (option)", body, key="ipg")
    # chiller
    body = (title("5.4 · Chiller · standard", "S&amp;A chiller")
            + P("With more than 20 years of experience, S&amp;A chillers were designed specially for fiber laser technology. The chiller cools the "
                "resonator and the cutting head optics. Inlets and outlets are made of stainless steel to ensure the durability of the product. "
                "The water pump and all other equipment were also developed for long-life operation. Chillers are matched to the cutting power and "
                "come in different sizes.", cls="sm")
            + row(fig("pro/chiller-1.png", h=230, px=800), fig("pro/chiller-2.png", h=230, px=800),
                  checks(["Dual cooling circuit", "Active cooling", "Temperature stability: ±1.8 °F (±1 °C)",
                          "Temperature control range: 41 – 95 °F (5 – 35 °C)", "Refrigerant: R-410a", "Intelligent digital control panel",
                          "Integrated alarm functions", "Back-mounted fill port and easy-to-read water level check", "RS-485 Modbus communication function",
                          "High reliability, energy efficiency and durability", "Available in 380 V"], cls="sm"), cols="1fr 1fr 1.6fr", gap=14, align="center")
            + grid([card("pro/chiller-inlet.png", "Dual water inlet and water outlet", P("Stainless steel inlet and outlet to prevent corrosion and leakage.", cls="sm"), h=70),
                    card("pro/chiller-panel.png", "Dual temperature control", P("The intelligent control panel offers two independent temperature "
                         "control systems: one controls the temperature of the fiber laser, the other the optics.", cls="sm"), h=70),
                    card("pro/chiller-casters.png", "Caster wheels for easy mobility", P("Four caster wheels offer easy mobility and unmatched flexibility.", cls="sm"), h=70),
                    card("pro/chiller-ventilation.png", "Ventilation", P("Air inlets and outlets of the chiller: keep the clearances shown "
                         "round the unit.", cls="sm"), h=70)], 4, 12))
    b.page("Chiller (standard)", body, key="chiller")
    # aspiration, scrap boxes
    body = (title("5.13 · 5.16 · standard", "Aspiration cells · scrap boxes")
            + h2("Aspiration cells", "standard")
            + P("DENER fiber laser aspiration was designed to be highly efficient in treating the polluted fume. The aspiration units are "
                "activated depending on the cutting position.")
            + fig("pro/aspiration.jpg", h=230, px=1800)
            + h2("Scrap boxes", "standard")
            + P("With an ergonomic design, the scrap boxes are easy to pull, and small parts and scrap can be easily reached.")
            + row(fig("pro/scrap-boxes.jpg", h=170, px=1300), qrbox("Scan to watch GFL videos on NovoTechMachineTools.com"), cols="2fr 1fr", align="center"))
    b.page("Aspiration · scrap boxes", body, key="aspiration")
    # cutting tables, light curtain
    body = (title("5.14 · 5.15 · standard", "Cutting tables · safety")
            + h2("Cutting tables", "standard")
            + P("DENER GFL fiber lasers are equipped with a dual exchangeable table. It allows a fast change of table in one motion.")
            + fig("pro/cutting-tables.jpg", h=240, px=1800)
            + h2("Safety · light curtain", "standard")
            + row(P("Machines systematically stop working when the operator is inside the working region.") + qrbox("Scan to watch GFL videos on NovoTechMachineTools.com"),
                  fig("pro/light-curtain.png", h=200, px=1000), cols="1fr 1fr", align="center"))
    b.page("Tables · safety", body, key="tables")
    # emergency stop, doors
    body = (title("5.15 · 5.18 · standard", "Emergency stops · doors")
            + h2("Emergency stop button and buzzer", "standard")
            + P("An easily accessible emergency stop button provides a safe working environment for the operator. A buzzer on top of the "
                "machine shows the working state of the machine in real time.")
            + fig("pro/estop.jpg", h=300, px=1800)
            + h2("Front sliding door and rear pneumatic door", "standard")
            + row(P("A front sliding door with special laser glass allows the machine user to operate safely, gives easy access to the "
                    "cutting head and makes maintenance of the machine easier."), qrbox("Scan to watch GFL videos on NovoTechMachineTools.com"),
                  cols="1.6fr 1fr", align="center"))
    b.page("Emergency stops · doors", body, key="doors")
    # nozzle cleaning, calibration, lubrication, linear guides
    body = (title("5.11 · 5.17 · 5.7", "Nozzle cleaning · calibration · lubrication · linear guides")
            + h2("Nozzle cleaning")
            + P("With the automatic nozzle cleaning provided, we ensure a better cutting quality and a longer life of the nozzle.")
            + h2("Calibration")
            + P("The DENER fiber laser calibrates directly on the sheet metal, so the cutting process can start faster.")
            + h2("Automatic lubrication system", "standard")
            + P("The Dener fiber laser is equipped with a centralized lubrication system that lubricates the axes according to the travel "
                "distance. It ensures that the mechanical parts work smoothly.")
            + fig("pro/lubrication.jpg", h=150, px=1400)
            + h2("Linear guides", "standard · THK")
            + P("THK linear guides resist heavy loads and ensure stability and precision in the motion of the different axes.")
            + fig("pro/linear-guide.jpg", h=130, px=1400))
    b.page("Nozzle · lubrication · guides", body, key="nozzle")
    # electrical
    body = (title("5.8 · 5.10", "Electrical components")
            + P("DENER only uses the best-quality electrical components on the market. Circuit breakers are made by SIEMENS and servo drives "
                "by YASKAWA. Through the selection of trusted components, DENER ensures the quality of the fiber laser machine.")
            + row(fig("pro/electrical-1.png", h=290, px=900), fig("pro/electrical-2.png", h=290, px=900), fig("pro/electrical-3.png", h=290, px=900), gap=12)
            + h2("Air conditioner on the electrical enclosure", "optional")
            + P("The electrical enclosure can be equipped with an air conditioner on customer demand. This option is advised in very hot "
                "working environments."))
    b.page("Electrical", body, key="elec")
    # Hoerbiger
    body = (title("Gas control · standard", "Hoerbiger gas control")
            + P("The cutting gas control system from HOERBIGER merges the features that are crucial for future-oriented laser cutting:")
            + fig("pro/hoerbiger.png", h=250, px=1400)
            + row(h3("Cutting gas control") + checks(["High gas pressure", "Fast, precise gas pressure control", "High flow rate and low valve weight",
                                                   "Low power consumption"]) + P("These factors push the limits of speed, precision and "
                                                                                 "stability in the cutting process.", cls="sm"),
                  h3("Gas pressure control valve with pilot valves") + checks(["Maximum dynamics", "Gas-tight pilot valves",
                                                                             "Back-pressure resistant gas selector valves (no check valves)",
                                                                             "Rapid gas pressure changes", "Extremely stable gas control performance",
                                                                             "Entire cutting gas function in one unit", "Compact design and low weight"]),
                  gap=22))
    b.page("Hoerbiger (standard)", body, key="gas")
    # servo, pneumatics, starting kit
    body = (title("5.9 · servo motors · pneumatic system · starting kit", "Servo motors · pneumatics")
            + h2("Servo motors")
            + row(kv([("YASKAWA", "Standard"), ("FANUC", "Optional")], head=["Brand", "Supply"]),
                  fig("pro/servo-yaskawa.png", "Yaskawa", h=110, px=700), fig("pro/servo-fanuc.png", "Fanuc", h=110, px=700),
                  cols="1.2fr 1fr 1fr", align="center")
            + P("To improve the quality of our machines, DENER may use different brands.", cls="note")
            + h2("Pneumatic system")
            + row(P("Through the use of FESTO pneumatic components, the management and distribution of air in the system is well done. "
                    "An optional chemical dryer can also be mounted."), fig("pro/pneumatic.png", h=190, px=1200), cols="1fr 1.3fr", align="center")
            + h2("Starting kit")
            + P("The fiber laser machine is delivered with a starting kit of nozzles, ceramics and protective windows.")
            + fig("pro/starting-kit.jpg", h=110, px=1400))
    b.page("Servo · pneumatics", body, key="servo")
    # FSCUT
    body = (title("5.1.1 · Control unit · standard", "Control unit FSCUT")
            + P("FSCUT is a cost-effective laser control system for 1.5 – 60 kW cutting. Based on EtherCAT and integrating motion control, laser "
                "control and gas control, it is widely used for sheet metal.")
            + row(fig("pro/fscut-panel.png", h=280, px=900), fig("pro/fscut-models.jpg", "FSCUT models, remote, interface and nesting", h=280, px=1100),
                  cols="1fr 1fr", gap=20, align="center")
            + h2("FSCUT features")
            + fig("pro/fscut-features-1.jpg", h=200, px=1800))
    b.page("FSCUT (standard)", body, key="fscut")
    body = (title("5.1.1 · Control unit · standard", "FSCUT features")
            + fig("pro/fscut-features-2.jpg", h=278, px=1800)
            + h2("FSCUT 4000E and 8000C")
            + fig("pro/fscut-compare.jpg", "System, feature and technique functions of the FSCUT 4000E and 8000C", h=262, px=1400))
    b.page("FSCUT features", body)
    # CypNest
    body = (title("6.1 · Software", "CypNest")
            + P("CypNest is a nesting software designed for the CypCut / HypCut sheet laser cutting system. It integrates advanced functions of "
                "drawing modification, quick nesting, toolpath generation, analysis reports and more to meet your production needs.")
            + P("<b>Drawing modification and import</b> — intelligent parts recognition, drawing error identification and optimization. Supports "
                "DWG and DXF file formats. Supports batch creation and import of parts via an Excel table.",
                "<b>Nesting strategy</b> — a powerful algorithm engine of high efficiency and production rate; no limit on sheet and part "
                "quantity in nesting; supports manual and automatic nesting; supports free-form sheet nesting.",
                "<b>Toolpath optimization</b> — a smart toolpath strategy to minimize travel length; smooth operation for toolpath adjusting; "
                "multiple common-line options to meet your production needs.",
                "<b>Production assist</b> — generates analysis reports of production and pricing. Technique and cutting parameters perfectly "
                "match the HypCut / CypCut laser cutting software.", cls="sm")
            + fig("pro/cypnest-nest.jpg", "A sheet nested in CypNest", h=300, px=1800))
    b.page("CypNest", body, key="cypnest")
    # Fanuc
    fanuc = ["High-speed Z-axis gap control", "Laser assist gas selection", "Laser assist gas pressure control", "Laser power, frequency and duty control commands",
             "Laser parameter overrides", "High-speed piercing", "Piercing time control", "Laser power control in real time",
             "Edge machining for high-quality contours", "Start-up function to stabilize cutting", "Laser restart", "Cutting parameter library",
             "High-speed positioning (ping-pong or frog jump)", "Fly-cut operation", "Integrated laser diagnostics", "3D laser machining",
             "Tool center point programming", "Bevel cutting compensation", "W-axis gap control", "HMI customization"]
    dif = ["Cutting technology tables", "2D graphical view of the nesting and parts", "Alarm messages", "Live cutting area monitor", "Power control data",
           "Edge control data", "Sheet measurement", "Work offset", "Auto beam centering", "Full keyboard with emergency stop", "Feed rate joystick",
           "Industrial mouse", "Camera and monitoring"]
    body = (title("5.1.2 · Control unit · option", "Control unit FANUC")
            + row(checks(fanuc, 2, cls="sm"), fig("pro/fanuc.jpg", h=300, px=900), cols="2fr 1fr", gap=14, align="start")
            + h2("DENER interface and Fanuc")
            + row(checks(dif, cls="sm"), fig("pro/fanuc-icons.png", h=230, px=1000), cols="1fr 1fr", gap=14, align="start"))
    b.page("Fanuc (option)", body, key="fanuc")
    # Metalix
    body = (title("6.2 · Software", "Metalix CAD/CAM")
            + P("The cncKad software provides an integrated system covering the complete cycle of CNC operations, and includes the following modules:")
            + P("<b>AutoNest</b> — automatic true-shape nesting for optimal material utilization, an automatic DXF-to-NC solution and detailed data reports.",
                "<b>Post-processing</b> — advanced post-processors generate efficient NC code, including macros, optimized tool path, minimal "
                "turret rotation and support for machine operations such as oiling, vacuum and ram rate.",
                "<b>Simulation</b> — graphic simulation of the NC program enables easy editing while viewing the processed sheet. The program is "
                "automatically checked for errors such as missing parameters, clamp errors, over-travel errors and more. The NC-to-DFT option "
                "imports legacy NC programs and simulates them as well.",
                "<b>DNC</b> — the DNC module supports uploading and downloading NC files to the machine, as well as batch loading and extracting "
                "NC files from the machine controller.",
                "<b>Import and export</b> (optional) — 3D integration with SolidWorks®, Solid Edge®, Autodesk® Inventor® and ProE® through a "
                "real-time associative link, and reading files directly from AutoCAD®.",
                "cncKad also offers parametric programming, advanced processing technologies and support for a wide range of machines.", cls="sm")
            + fig("pro/metalix.png", "Figure 6 — cncKad", h=170, px=1600))
    b.page("Metalix", body, key="metalix")
    # cutting parameters
    kw = [3, 4, 6, 8, 12, 15, 20]
    cut = {"Mild steel": [18, 20, 25, 30, 35, 40, 50], "Stainless steel": [8, 10, 15, 25, 30, 35, 50], "Aluminum": [6, 8, 15, 25, 30, 35, 40],
           "Copper": [4, 6, 8, 10, 12, 12, 12], "Brass": [4, 6, 10, 12, 15, 18, 20]}

    def cut_table(cols):
        return mtable([f"{kw[i] * 1000:,} W" for i in cols], [(m, "", [frac_cell(v[i]) for i in cols]) for m, v in cut.items()],
                      corner="Material", cls="big")
    body = (title("5.12 · Cutting parameters", "Cutting parameters (capacity)")
            + P("Maximum cutting thickness by laser source power. Plate thicknesses are given in the nearest 1/16″, with Dener's millimetre value.", cls="sm")
            + cut_table(range(4)) + '<div style="height:16pt"></div>' + cut_table(range(4, 7))
            + P("Cutting thicknesses may vary due to factors such as material quality, operator settings and cutting speed.", cls="note")
            + included())
    b.page("Cutting parameters", body, key="cutting")
    # other technical specification
    sizes = [(1530, 3050, 16, 8500), (2040, 4050, 22, 10200), (2040, 6050, 30, 12600)]
    cols = "".join(f"<th>{w:,} × {l:,} mm<br><small>{w / 25.4:.1f} × {l / 25.4:.1f}″</small></th>" for w, l, _, _ in sizes)

    def span(lab, val):
        return f'<tr><th>{lab}</th><td colspan="3">{val}</td></tr>'
    trs = (span("X, Y transfer system", "Rack &amp; pinion") + span("Z transfer system", "Ball screw")
           + span("Z axis stroke", "13.8″ (350 mm)") + span("Max. speed X, Y axis", mmin(120)) + span("Max. speed Z axis", mmin(50))
           + span("X, Y acceleration", "1.5 G") + span("Z acceleration", "1 G") + span("Axis positioning precision", "±0.002″ (±0.05 mm)")
           + span("Axis repeatability precision", "±0.0012″ (±0.03 mm)")
           + "<tr><th>Shuttle change time</th>" + "".join(f"<td>{t} s</td>" for _, _, t, _ in sizes) + "</tr>"
           + span("Cutting assistance gas", "Oxygen, nitrogen, air")
           + "<tr><th>Approx. weight</th>" + "".join(f"<td>{weight(k)}</td>" for *_, k in sizes) + "</tr>")
    body = (title("Technical data", "Other technical specification")
            + f'<table class="kv spec3"><thead><tr><th>Net cutting size</th>{cols}</tr></thead><tbody>{trs}</tbody></table>'
            + P("GFL 3015 L · GFL 4020 L · GFL 6020 L.", cls="note")
            + '<div style="margin-top:10pt">' + fig("dn-gfl-2", h=118, px=1800) + "</div>" + included())
    b.page("Technical specification", body, key="spec")
    # electric consumption
    cons = ["35.8", "39.7", "46.4", "51.45", "64", "80", "96"]
    core = [50, 50, 50, 100, 100, 100, 100]

    def ec(cols):
        return mtable([f"{kw[i] * 1000:,} W" for i in cols], [("Consumption", "kW", [cons[i] for i in cols]),
                                                            ("Core diameter", "µm", [core[i] for i in cols])], corner="Source power", cls="big")
    body = (title("Technical data", "Electric consumption") + ec(range(4)) + '<div style="height:16pt"></div>' + ec(range(4, 7))
            + P("Total electrical consumption of the machine by laser source power; fiber core diameter of the laser source.", cls="note")
            + '<div style="margin-top:16pt">' + fig("pro/raycus-2.png", h=220, px=1300) + "</div>" + included())
    b.page("Electric consumption", body, key="power")
    # configuration
    box = ('<span style="display:inline-block;min-width:54pt;text-align:center;border:1.2pt solid %s;padding:6pt 8pt;margin-right:10pt;'
           'font:600 11pt Oswald;color:%s;%s">%s</span>')
    body = (title("Standard configuration", "Configuration")
            + kv([("Choose size", "".join(box % (CHAR, CHAR, "background:#fdebd3" if i == 0 else "", f"{n} · {c}") for i, (n, c) in
                                              enumerate([(1, "3015"), (2, "4020"), (3, "6020")]))),
                  ("Resonator power", box % (CHAR, CHAR, "", "6 kW") + "Raycus / FSCUT"),
                  ("Choose configuration", box % (CHAR, CHAR, "background:#fdebd3", "1 ✓") + box % (CHAR, CHAR, "", "2"))])
            + h2("Standard")
            + checks(["Boji cutting head", "Machine body", "Raycus resonator", "Control unit: FSCUT series", "Software: CypCut", "Exchangeable tables",
                      "Camera for visualization of the working area", "Air cutting system", "Cutting features", "Operating kit"], 2)
            + P("*Filter is not included. UPS is not included.", cls="note")
            + '<div style="margin-top:12pt">' + fig("dn-gfl-1", h=200, px=1800) + "</div>" + included())
    b.page("Configuration", body, key="config")
    # warranty
    body = (title("Warranty", "Standard warranty conditions")
            + '<ol class="num">' + "".join(f"<li>{x}</li>" for x in [
                "The warranty time is 12 months for mechanical parts and moving systems. Our warranty is limited to replacing parts found to "
                "be defective; consumable items are not included.",
                "We reserve the right to invoice service or visits found to be necessary due to incorrect use of the machine or lack of maintenance.",
                "12 months for the laser source, except the parts listed in the following section.",
                "Cooling unit, ventilation filter, compressor and air dryer if included in the offer; the pneumatic system is 12 months.",
                "Consumables of the cutting head are not covered by the warranty."]) + "</ol>"
            + h2("Excluded from warranty")
            + P("Dener excludes the machine parts described in the following articles from the warranty scope:", cls="sm")
            + checks(["All optical parts are consumables and are not covered by the warranty.",
                      "Consumables such as nozzles, cooling water, oils and filters are not covered by the warranty.",
                      "Malfunctions that may occur as a result of the use of bad-quality gas, cooling water or electricity provided by the customer are not covered by the warranty.",
                      "Malfunctions that may occur in the mirrors, the laser or the cooling unit itself due to the cooling water used in the cooling unit are not covered by the warranty.",
                      "Failures that may occur as a result of incorrect setting of cutting parameters, incorrect light line adjustment and back "
                      "reflection are not covered by the warranty. Such errors occur when untrained or incompletely trained personnel use the "
                      "machine; such uses are not covered under warranty.",
                      "Using the machine for purposes other than cutting is out of warranty.",
                      "Malfunctions that occur as a result of incomplete maintenance or careless use are not covered by the warranty. Periodic "
                      "maintenance and related procedures must be carried out by the customer.",
                      "All work done by any company other than DENER, or not authorized by DENER, and the results of this work are not covered by the warranty."], cls="sm")
            + included())
    b.page("Warranty", body, key="warranty")
    # FAQ
    faq = [("What is the life of a nozzle?", "Nozzle life is mainly related to the usage of the machine. For example, wrong nozzle centering and wrong "
            "cutting parameters will damage the component faster."),
           ("Consumables?", "We recommend using original consumables. Any damage to the machine related to the use of bad-quality consumables "
            "will not be covered by the warranty."),
           ("Do I need a nozzle for every thickness?", "No, nozzles are usable for a certain range of thickness (check the nozzle document)."),
           ("What is the smallest hole that I can cut in a plate?", "The smallest hole diameter in a plate is half the thickness of the plate."),
           ("How loud is the laser machine?", "70 – 75 decibels."),
           ("Is the machine delivered with a starting kit?", "Yes, the machine is delivered with a set of protective lenses, nozzles and ceramics."),
           ("How is the maintenance on a fiber laser?", "The machine is provided with a periodic maintenance label. A fiber laser needs less "
            "maintenance than a CO2 laser.")]
    body = (title("Questions &amp; answers", "FAQ") + "".join(f'<div class="faq"><h3>{q}</h3><p>{a}</p></div>' for q, a in faq) + included())
    b.page("FAQ", body, key="faq")
    # transport, installation requirement
    body = (title("7 · Transport dimensions · installation", "Transport")
            + row(kv([("GFL 3015", "1 × A"), ("GFL 4020", "1 × B"), ("GFL 6020", "2 × B")], head=["Choose size", "Trucks"]),
                  fig("pro/trucks.jpg", "A — closed trailer · B — flatbed trailer", h=120, px=1100), cols="1fr 1.2fr", gap=20, align="center")
            + h2("Installation requirement")
            + fig("pro/installation.jpg", "Supplied by the customer: the connection cables from the customer's electrical panel to all machine "
                  "components, the electrical cabinet, the complete gas system installation, the compressor system, a suitable PC, a USB modem "
                  "and a set of sheet metal for test cutting", h=360, px=2000))
    b.page("Transport · installation", body, key="transport")
    b.back("Fiber laser for your shop.", ["dn-gfl-1", "dn-gfl-2", "dn-gfl-3", "dn-gfl-control"])
    # contents: the offer's numbered sections and the technical data pages
    toc = [("1", "DENER Machinery", "dener", 0), ("2", "Machine information", "info", 0), ("2.1", "Machine concept", "info", 1),
           ("3", "Fiber laser advantages", "adv", 0), ("4", "Design and manufacturing advantages", "design", 0),
           ("5", "Machine components and options", "rack", 0), ("5.1", "Control unit", "fscut", 1), ("5.1.1", "FSCUT", "fscut", 2),
           ("5.1.2", "FANUC (option)", "fanuc", 2), ("5.2", "Power sources (resonator)", "raycus", 1), ("5.2.1", "Raycus", "raycus", 2),
           ("5.2.2", "IPG (option)", "ipg", 2), ("5.3", "Cutting head", "boji", 1), ("5.3.1", "Boji", "boji", 2),
           ("5.3.2", "Precitec (option)", "precitec", 2), ("5.4", "Chiller", "chiller", 1), ("5.5", "Rack and pinion system", "rack", 1),
           ("5.6", "High-speed Z, X and Y axes", "boji", 1), ("5.7", "Linear guides", "nozzle", 1), ("5.8", "Electric panel components", "elec", 1),
           ("5.9", "Pneumatic system", "servo", 1), ("5.10", "Air conditioner (option)", "elec", 1), ("5.11", "Nozzle cleaning and calibration", "nozzle", 1),
           ("5.12", "Burr-free cutting parameters", "cutting", 1), ("5.13", "Aspiration system", "aspiration", 1), ("5.14", "Shuttle table", "tables", 1),
           ("5.15", "Safety system", "tables", 1), ("5.16", "Scrap boxes", "aspiration", 1), ("5.17", "Automatic central lubrication", "nozzle", 1),
           ("5.18", "Front door and pallet door", "doors", 1), ("6", "Software", "cypnest", 0), ("6.1", "CypNest", "cypnest", 1),
           ("6.2", "Metalix", "metalix", 1), ("7", "Transport dimensions", "transport", 0),
           ("", "Gas control · servo motors · starting kit", "gas", 0), ("", "Other technical specification", "spec", 0),
           ("", "Electric consumption", "power", 0), ("", "Configuration", "config", 0), ("", "Warranty conditions", "warranty", 0),
           ("", "FAQ", "faq", 0), ("", "Installation requirement", "transport", 0)]
    rows_ = "".join(f'<div class="t{lv}"><span><em>{n}</em>{t}</span><i></i><b>{b.num(k):02d}</b></div>' for n, t, k, lv in toc)
    body = (title("Full technical specification · Dener PRO 3015 · 6 &amp; 12 kW", "Contents")
            + f'<div class="toc toc2">{rows_}</div>'
            + row(included(two=True), '<div class="box"><div class="bt">Sold &amp; serviced in Canada</div>'
                  '<p>by NovoTech Machine Tools — Mississauga, ON</p></div>', cols="2.3fr 1fr", gap=14, cls="mt-auto"))
    for pg in b.pages:
        if pg.get("body") == "@@TOC@@":
            pg["body"] = body
    return b


# ---------------------------------------------------------------------------------------------------------- tube catalogue
TUBE_EQUIP_1 = [
    ("tube/resonator.png", "Resonator", "MAX series", "The MAX fiber laser resonator delivers fast, precise and reliable cutting performance with its high "
     "beam quality, energy-efficient operation, and stable power output. Its compact design and low maintenance requirements help support "
     "production continuity."),
    ("tube/chiller.png", "Chiller", "S&amp;A CWFL series", "Specially developed for fiber laser cutting machines, S&amp;A chillers provide stable "
     "temperature control for resonators and optical systems, enhancing cutting quality and machine lifespan. Thanks to its dual-circuit "
     "cooling design, it independently balances the resonator and optical path. Its compact design allows for easy integration, while quiet "
     "operation and energy-efficient performance help lower operating costs. With low maintenance requirements, it is an ideal solution for "
     "long-term, uninterrupted operation."),
    ("tube/fscut.png", "FSCUT control unit", "", "The FSCUT system is a control unit designed for tube and profile cutting operations. Based on "
     "EtherCAT technology, it features a visual control interface, laser control functions, and gas management capabilities. Widely used in "
     "the industry, it includes a specially developed interface optimized for tube and profile cutting applications, providing reliable and "
     "efficient operation."),
    ("tube/servo.png", "Servo motor and motor driver", "Inovance", "For high-precision motion control in fiber laser cutting machines, Inovance "
     "motor and drive systems deliver superior performance and reliability. With high response speeds and stable torque output, they ensure "
     "maximum accuracy in axis movements. Advanced control algorithms minimize vibration, improving cutting quality and extending machine "
     "lifespan. Their compact design allows for easy installation and wiring. With energy-efficient operation and high dynamic performance, "
     "Inovance systems bring power.")]
TUBE_EQUIP_2 = [
    ("tube/reducer.png", "Reducer", "Techmech", "Techmech gearboxes are specially preferred in fiber laser cutting machines for high-precision "
     "motion transmission. With their high torque capacity and low backlash design, they ensure maximum accuracy in axis movements. Their "
     "compact structure provides space efficiency in machine design, while the durable materials and high efficiency rate offer long-lasting "
     "and trouble-free operation."),
    ("tube/pinion.png", "Rack and pinion", "TWEBOLUN", "TWEBOLUN pinion and rack systems are specially designed for high-precision axis movements "
     "in fiber laser cutting machines. With low backlash and stable power transmission, they accurately follow cutting paths, ensuring high "
     "precision even in complex geometries. Durable materials and long-lasting design provide uninterrupted performance in production. Easy "
     "installation and low maintenance requirements enhance operational efficiency."),
    ("tube/smc.png", "Gas regulator", "SMC", "SMC regulators provide high precision and stability in pressure control for fiber laser cutting "
     "machines. They contribute to the safe, efficient, and long-lasting operation of air systems, optimizing the overall performance of the "
     "machine. Produced by Japan-based SMC Corporation, these regulators offer a reliable solution worldwide for industrial automation and "
     "pneumatic control systems."),
    # from Dener's Turkish tube laser catalogue (dener_borulazer), translated
    ("tube/boci.png", "Tube laser cutting head", "BOCI", "The BOCI tube laser cutting head is designed to deliver high performance and reliability "
     "in tube and profile cutting. It cuts round, square, rectangular and special-shaped profiles precisely and fast, and its compact, rigid "
     "structure guarantees stability even at high speeds. The autofocus system adapts quickly to different material thicknesses and cutting "
     "requirements. An advanced dust-protection design, optimized gas channels and highly durable optical components give a long service "
     "life and continuous performance — high precision, superior cut quality and higher production efficiency.")]
TUBEST = ("TubeST is a professional 3D nesting solution for tube and profile laser cutting. Its intelligent automation simplifies drawing, nesting "
          "and toolpath creation, helping manufacturers reduce material waste, shorten programming time and achieve reliable results across "
          "complex parts.")
TUBEST_LIST = ["Imports IGS and SAT files and exports compatible files for TubeST, CypTube and TubePro.",
               "Detects tiny or redundant geometry and processes it automatically.",
               "Creates rectangular, L-shaped, H-shaped, I-shaped and custom profiles.",
               "Optimized auto nesting uses remnants first and minimizes tube-tail waste.",
               "Advanced toolpaths include lead-ins, compensation, cooling points, micro joints and weld kerf.",
               "Automatic toolpath checks help prevent cutting-head interference and support safer production."]
# cutting capacity by chuck (the Turkish catalogue's charts): chuck → [(profile, size)] in mm; d = the diagonal limit
TUBE_CAPS = [(120, "8 – 120", None), (180, "10 – 180", None), (250, "15 – 250", None), (350, "30 – 350", None)]


def book_tube():
    from dener_data import weight, mmin, EFTL_M, FTL_M, dims

    def mm_in(a, b):
        return f"{a / 25.4:.1f} – {b / 25.4:.1f}″"

    def dia(a, b):
        return f"Ø{mm_in(a, b)} <small>(Ø{a} – Ø{b} mm)</small>"

    def prof(a, b):
        return f"{a / 25.4:.1f} × {a / 25.4:.1f} – {b / 25.4:.1f} × {b / 25.4:.1f}″ profile <small>({a}×{a} – {b}×{b} mm)</small>"

    FT = {6000: "20 ft", 7000: "23 ft", 9000: "30 ft", 12000: "40 ft"}

    def lw(mm, kg, chuck):
        return f"{FT[mm]}, {weight(kg).split(' (')[0]} <small>({mm:,} mm, {kg:,} kg)</small> · {chuck} chuck"

    def spd(v, chuck):
        return f"{mmin(v)} · {chuck} chuck"

    def badges(*names):
        return '<div class="badges" style="margin-top:10pt">' + "".join(f'<img src="{im("gfl/badge-" + n + ".jpg", 700)}">' for n in names) + "</div>"

    b = Book("tube", "Tube fiber laser", "Dener FTL and E-FTL tube profile fiber laser cutting machines",
             os.path.join(ROOT, "src", "files", "NovoTech-Dener-Tube-Lasers-2026.pdf"))
    b.title, b.subject = "Dener Tube Fiber Laser — NovoTech Machine Tools", "Dener FTL and E-FTL tube fiber laser catalogue, imperial edition"
    b.cover("Dener · Tube fiber laser", "“The future is here” · sold &amp; serviced in Canada by NovoTech", "Tube", "Fiber laser",
            "Faster cutting · higher precision · maximum efficiency", "tube/cover.png",
            [("Since 1974", "Manufacturing experience"), ("Ø0.3 – 25.2″", "Round tube and profile"), ("20 – 40 ft", "Tube length"),
             ("Canada", "Parts &amp; technical support")], hero_h=200, minis=("tube/ftl-2.png", "tube/eftl-side.png"))
    about_page(b)
    campus_page(b)
    # catalogue p3 — design advantages
    body = (title("Tube series", "Tube series — design advantages")
            + fig("tube/cabin.png", "The cutting cabin: control unit on its arm, laser-safe viewing window and unloading chute", h=300, px=1400)
            + P("DENER FTL and E-FTL are specially designed for metal tube processing applications. With the semi-automatic loading system, it "
                "reduces the operator’s workload and increases production efficiency. Thanks to the optional angled cutting feature, precise "
                "cuts can be performed at various angles. The machine is capable of fast and precise cutting on metal tubes of different "
                "diameters, shapes, and lengths. Its user-friendly interface and safe operating system streamline workflows and optimize "
                "production processes.",
                "Equipped with advanced fiber laser technology, DENER FTL and E-FTL deliver high-quality cutting results with smooth edges and "
                "minimal material deformation. Their robust construction ensures reliable performance even under demanding production "
                "conditions, while optimized cutting parameters help reduce material waste and operating costs. Offering flexibility, "
                "precision, and productivity in a single solution, these machines are ideal for a wide range of industries, including "
                "automotive, construction, furniture, and general metal fabrication."))
    b.page("Design advantages", body, toc="Design Advantages")
    # catalogue p4 — the machine
    labels = pct((563, 352, 1190, 742), [("Chuck", (643.3, 396.4, 687.9, 417.3)), ("Servo support", (742.3, 384.3, 842.3, 405.2)),
                                         ("Loading system", (675.1, 457.7, 787.2, 478.5)), ("Protective glass", (832.6, 457.7, 945.8, 478.5)),
                                         ("Unloading system", (971.5, 482.1, 1099.2, 503.0)), ("Control unit", (803.8, 698.8, 888.8, 719.7))])
    body = (title("Tube fiber laser cutting machine", "Tube fiber laser cutting machine")
            + row(h2("Design advantages") + checks(["Precise cutting and clamping", "Energy saving", "User-friendly operation",
                                                  "Cost-effective", "Flawless performance"]),
                  diagram("Rigid and<br>optimized<br>body structure", [("tl", "High speed"), ("tr", "High cutting quality"),
                                                                     ("l", "Low cost"), ("r", "High technology"), ("b", "Quality components")]),
                  cols="1fr 1fr", gap=20, align="center")
            + '<div style="margin-top:14pt">' + labelled("tube/machine-labelled.jpg", labels, h=330) + "</div>")
    b.page("Tube fiber laser", body, toc="Tube Fiber Laser Cutting Machine")
    # catalogue p5 — engineered for every profile
    body = ('<div class="photo-panel" style="height:654pt;margin-top:-4pt"><img src="%s" style="object-position:50%% 55%%">'
            '<div style="position:absolute;left:0;top:0;right:0;height:62%%;background:linear-gradient(180deg,rgba(24,25,27,.86) 0%%,'
            'rgba(24,25,27,.62) 45%%,rgba(24,25,27,0) 100%%)"></div>'
            '<div style="position:absolute;left:18pt;top:16pt;right:18pt"><div style="font:700 30pt/1.05 Oswald;color:#fff;text-transform:uppercase">'
            'Engineered for<br>every profile</div><div style="font:500 17pt/1.2 Oswald;color:#fff;margin-top:4pt">Tube &amp; profile laser cutting</div>'
            '<div style="width:60pt;height:3.7pt;background:%s;margin-top:8pt"></div>'
            '<p style="color:#fff;font-size:10.5pt;max-width:330pt;margin-top:10pt;text-shadow:0 1pt 3pt rgba(0,0,0,.7)">The Tube Laser Series '
            'delivers fast, precise, and flexible cutting for tubes and profiles. Designed for modern production, it simplifies complex operations, '
            'improves material efficiency, and ensures consistent results across every part.</p></div>'
            '<div class="overlay"><div class="st"><div><b>Complex</b><span>Profile cutting</span></div><div><b>High-speed</b><span>Production</span></div>'
            '<div><b>Precise &amp; clean</b><span>Results</span></div><div><b>Reduced</b><span>Material waste</span></div></div>'
            '<p><b>Tube Series</b> delivers speed, precision and efficiency for modern production.</p></div></div>'
            % (im("tube/cutting.png", 1400), ORANGE))
    b.page("Engineered for every profile", body, toc="Engineered for Every Profile")
    # catalogue p6 — software
    body = (title("Software", "TubeST nesting solution") + P(TUBEST)
            + fig("tube/tubest.png", "TubeST — tube and profile parts nested along a 39.4 ft (12,000 mm) bar", h=290, px=1600)
            + h2("Optimize tube &amp; profile cutting") + checks(TUBEST_LIST))
    b.page("Software", body, toc="Software — TubeST")
    head_page(b)
    cards = [card(i, t, P(x, cls="sm"), sub=s, h=118) for i, t, s, x in TUBE_EQUIP_1]
    b.page("Equipment", title("Resonator · chiller · FSCUT control · servo drives", "Equipment") + grid(cards, 2, 20), toc="Equipment")
    cards = [card(i, t, P(x, cls="sm"), sub=s, h=118) for i, t, s, x in TUBE_EQUIP_2]
    b.page("Equipment", title("Reducer · rack and pinion · gas regulator · cutting head", "Equipment") + grid(cards, 2, 20))
    ease_page(b)
    note = (P("*Cutting thicknesses may vary due to factors such as material quality, operator settings, and cutting speed.", cls="note")
            + P("Custom voltage available: 208 V, 240 V, 480 V or 600 V 3-phase. CSA-approved electrical panel.", cls="note"))
    power = "3,000 W · 6,000 W · 12,000 W · 20,000 W"
    # catalogue p11-12 — FTL, 250 and 350 chucks
    body = (title("Tube profile fiber laser · FTL series", "FTL series")
            + fig("tube/ftl-1.png", "FTL with the loading system", h=150, px=2000) + fig("tube/ftl-2.png", "FTL — loading, cutting cabin and unloading", h=220, px=2000)
            + badges("speed", "support"))
    b.page("FTL series", body, toc="FTL Series")
    body = ('<div class="eyebrow" style="margin-bottom:2pt">Technical specifications · FTL series</div>'
            '<h1>Tube profile</h1><h1 style="color:%s">Fiber laser</h1><div class="rule" style="margin-bottom:14pt"></div>' % OR2
            + kv([("Machine model", "FTL"), ("Resonator power options", power),
                  ("Tube diameters", f"{dia(15, 250)}<br>{prof(15, 250)}<br>{dia(30, 350)}<br>{prof(30, 350)}"),
                  ("Repeatability", "±0.002″ (±0.05 mm)"), ("Max. speed", f"{spd(80, 250)}<br>{spd(54, 350)}"), ("Max. acceleration", "0.6 G"),
                  ("Voltage and frequency", "380 V 50 Hz / 60 Hz"),
                  ("Max. profile length and weight capacity", f"{lw(6000, 600, 250)}<br>{lw(9000, 1000, 350)}<br>{lw(12000, 1200, 250)}")],
                 head=["Technical specifications", "FTL series"])
            + note + included())
    b.page("Technical specifications", body)
    # catalogue p13-14 — FTL, 350, 500 and 640 chucks
    body = (title("Tube profile fiber laser · FTL series", "FTL series")
            + fig("tube/ftl-3.png", h=110, px=2000) + fig("tube/ftl-4.png", "FTL — the cutting cabin between the loading and unloading beds", h=150, px=2400)
            + fig("tube/ftl-5.png", "FTL for long, heavy tube — bars to 40 ft (12 m)", h=170, px=2000) + badges("cost", "support"))
    b.page("FTL series", body)
    body = ('<div class="eyebrow" style="margin-bottom:2pt">Technical specifications · FTL series</div>'
            '<h1>Tube profile</h1><h1 style="color:%s">Fiber laser</h1><div class="rule" style="margin-bottom:14pt"></div>' % OR2
            + kv([("Machine model", "FTL"), ("Resonator power options", power),
                  ("Tube diameters", f"{dia(30, 350)}<br>{prof(30, 350)}<br>{dia(30, 500)}<br>{prof(30, 500)}<br>{dia(120, 640)}<br>{prof(120, 640)}"),
                  ("Repeatability", "±0.004″ (±0.1 mm)"), ("Max. speed", f"{spd(54, 350)}<br>{spd(25, 500)}<br>{spd(25, 640)}"),
                  ("Max. acceleration", "0.6 G"), ("Voltage and frequency", "380 V 50 Hz / 60 Hz"),
                  ("Max. profile length and weight capacity", f"{lw(12000, 1400, 350)}<br>{lw(12000, 2100, 500)}<br>{lw(12000, 2600, 640)}")],
                 head=["Technical specifications", "FTL series"])
            + note + included())
    b.page("Technical specifications", body)
    # catalogue p15-16 — E-FTL
    body = (title("Tube profile fiber laser · E-FTL series", "E-FTL series")
            + fig("tube/eftl-side.png", "E-FTL — the cutting cabin and the bed", h=170, px=2000)
            + fig("tube/eftl-rear.png", "E-FTL — the loading side with the tube supports", h=180, px=2000) + badges("cost", "support", "speed"))
    b.page("E-FTL series", body, toc="E-FTL Series")
    body = ('<div class="eyebrow" style="margin-bottom:2pt">Technical specifications · E-FTL series</div>'
            '<h1>Tube profile</h1><h1 style="color:%s">Fiber laser</h1><div class="rule" style="margin-bottom:12pt"></div>' % OR2
            + kv([("Machine model", "E-FTL"), ("Resonator power options", power),
                  ("Tube diameters", "<br>".join(f"{dia(a, c)} · {prof(a, c)}" for a, c in ((8, 120), (10, 180), (15, 250), (30, 350)))),
                  ("Repeatability", "±0.002″ (±0.05 mm)"), ("Max. speed", f"{spd(120, '120 / 180')}<br>{spd(80, 250)}<br>{spd(54, 350)}"),
                  ("Max. acceleration", "1 G"), ("Voltage and frequency", "380 V 50 Hz / 60 Hz"),
                  ("Max. profile length and weight capacity", "<br>".join(lw(m, k, c) for m, k, c in
                   ((7000, 120, 120), (7000, 240, 180), (7000, 300, 250), (7000, 600, 350), (9000, 440, 250), (9000, 1200, 350),
                    (12000, 1200, 250), (12000, 1800, 350))))],
                 head=["Technical specifications", "E-FTL series"])
            + note + included())
    b.page("Technical specifications", body)

    # ---- the extra details of Dener's Turkish tube laser catalogue (the owner, Nov 1 2026): capacities by chuck, the model list, photos
    def cap_rows(n):
        """[(profile, size in mm, diagonal limit in mm or None)] as Dener charts them"""
        if n == 540:
            return [("Round", "Ø30 – 540", None), ("Square", "30 – 500", 710), ("Rectangular", "30 – 500 × 30 – 500", 710),
                    ("U profile", "30 – 500 × 30 – 540", 710), ("H profile", "30 – 500 × 30 – 540", 710), ("L profile", "30 – 500 × 30 – 540", None)]
        if n == 640:
            return [("Round", "Ø120 – 640", None), ("Square", "120 – 640", 640), ("Rectangular", "120 – 640 × 120 – 640", 640),
                    ("U profile", "120 – 570 × 120 – 640", 640), ("H profile", "120 – 570 × 120 – 640", 640), ("L profile", "120 – 570 × 120 – 570", 640)]
        r = next(x for c, x, _ in TUBE_CAPS if c == n)
        return [("Round", "Ø" + r, None), ("Square", r, None), ("Rectangular", f"{r} × {r}", None)] + [
            (p_, f"{r} × {r}", None) for p_ in ("U profile", "H profile", "L profile")]

    def to_in(t):
        import re
        return re.sub(r"(\d+)", lambda m: f"{int(m.group(1)) / 25.4:.1f}", t) + "″"

    def cap_card(n):
        rows = "".join(f"<tr><th>{p_}</th><td>{to_in(v)}{f' · diagonal ≤{d / 25.4:.1f}″' if d else ''}<br>"
                       f"<small>{v} mm{f' · ≤{d} mm' if d else ''}</small></td></tr>" for p_, v, d in cap_rows(n))
        return (f'<div class="card"><div class="cim" style="height:58pt"><img src="{im(f"tube/chuck-{n}.png", 600)}"></div>'
                f'<div class="ctl">Ø{n / 25.4:.1f}″ chuck <small style="font:400 8pt Barlow;color:#7a7c80">({n} mm)</small></div>'
                f'<table class="capt"><tbody>{rows}</tbody></table></div>')
    body = (title("Tube profile laser cutting machine", "Cutting capacity by chuck")
            + P("The sections each chuck clamps — round, square and rectangular tube and the open U, H and L profiles. The model number "
                "gives the chuck: 6025 = Ø250 mm chuck.", cls="xs")
            + grid([cap_card(n) for n in (120, 180, 250, 350, 540, 640)], 3, 12)
            + P("Sizes as charted by Dener, in inches with the millimetres below. Ask NovoTech to check a large or unusual section against the "
                "chuck before ordering.", cls="note"))
    b.page("Cutting capacity", body, toc="Cutting Capacity by Chuck")

    def model_page(series, ms, common, extra):
        def tl(mm):
            from dener_data import _ft_m
            return _ft_m(mm).replace(" (", "<br><small>(") + "</small>"
        rows = [("Chuck", "", [f"Ø{m[1] / 25.4:.1f}″<br><small>Ø{m[1]} mm</small>" for m in ms]),
                ("Max. tube length", "", [tl(m[2]) for m in ms])] + extra(ms) + [
            ("Axis travel X · Y · Z", "", [f"{m[3] / 25.4:.1f} · {m[4] / 25.4:,.0f} · {m[5] / 25.4:.1f}″<br><small>{m[3]:,} · {m[4]:,} · {m[5]:,} mm</small>" for m in ms]),
            ("Tube feed speed", "", [mmin(m[6]).replace(" (", "<br><small>(") + "</small>" for m in ms]),
            ("Chuck rotation", "", [f"{m[7]} rpm" for m in ms]),
            ("Loading + unloading length", "", [_lu_cell(*m[9]) for m in ms]),
            ("Machine size L × W × H", "", [dims(*m[8]).replace(" (", "<br><small>(") + "</small>" for m in ms])]
        return (title(f"Tube profile laser cutting machine · {series}", f"{series} models")
                + kv(common, head=[f"{series} series", "Every model"])
                + '<div style="margin-top:10pt">' + mtable([m[0].split(" ")[-1] for m in ms], rows, corner=series, cls="tight") + "</div>"
                + P("The model number is the bed length and the chuck: 6025 = 6 m (20 ft) bed, Ø250 mm chuck. Laser source power, acceleration, "
                    "repeatability and tube weight: see the technical specifications of the series.", cls="note"))

    def _lu_cell(a, b_):
        from dener_data import _NOM_FT
        return f"{_NOM_FT[a]} + {_NOM_FT[b_]} ft<br><small>{a} + {b_} m</small>"

    def _unl_cell(m_):
        from dener_data import _NOM_FT
        return f"{_NOM_FT[m_]} ft<br><small>{m_} m</small>"

    common_e = [("Chucks", "2 moving chucks · minimum remnant 1.4″ (35 mm)"), ("Tube support", "Servo-following support system"),
                ("Automatic lubrication", "Standard"), ("Resonator", "Maxphotonics"), ("Control", "FSCUT3000 · TubePro interface"),
                ("Nesting software", "TubeST, small-tube version"), ("Motor and drive", "Inovance"), ("Unloading length", "6.6 ft (2 m)")]
    extra_e = lambda ms: [("Bevel cutting", "", ["Option"] * len(ms)),
                          ("Loading system", "", ["Semi-automatic or fully automatic · option"] * 2 + ["Fully automatic · option"] * 4),
                          ("Cutting head", "BOCI", ["≤3 kW BLT310T<br>6 kW BLT421TS"] * 2 + ["≤3 kW BLT310T<br>6 kW BLT421TS<br>12 kW BLT442T"] * 4)]
    b.page("Model list", model_page("E-FTL", EFTL_M, common_e, extra_e), toc="E-FTL Models")
    common_f = [("Chucks", "3 moving chucks · minimum remnant 0″ — the last part is cut with no tail"), ("Tube support", "Servo-following support system"),
                ("Automatic lubrication", "Standard"), ("Resonator", "Maxphotonics"), ("Cutting head", "BOCI: ≤3 kW BLT310T · 6 kW BLT421TS · 12 kW BLT442T · 20 kW BLT560H"),
                ("Control", "FSCUT5000A · TubePro interface"), ("Nesting software", "TubeST, professional version"), ("Motor and drive", "Inovance"),
                ("Loading system", "Semi-automatic loading system · option")]
    extra_f = lambda ms: [("Bevel cutting", "", ["Option"] * 6 + ["Standard"] * 3),
                          ("Unloading length", "", [_unl_cell(m[9][1]) for m in ms])]
    b.page("Model list", model_page("FTL", FTL_M, common_f, extra_f), toc="FTL Models")
    body = (title("Dener tube profile laser cutting machine", "Perfect cut")
            + fig("tube/hall.jpg", "A Dener FTL tube laser in a production hall", h=300, fit="cover", px=2000)
            + row(fig("tube/head-cut.png", "The BOCI head cutting a tube held in the chuck", h=262, fit="cover", px=1200),
                  fig("tube/cutting.png", "Sparks fly clear of the chuck jaws", h=262, fit="cover", px=1200), gap=14))
    b.page("In production", body, toc="In Production")
    service_page(b)
    world_page(b)
    range_page(b)
    b.back("Tube laser for your shop.", ["tube/cover.png", "tube/ftl-5.png", "tube/cabin.png", "tube/hall.jpg"])
    fill_about(b)
    return b


BOOKS = {"gfl": book_gfl, "smart": book_smart, "spec": book_spec, "tube": book_tube}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("books", nargs="*", default=list(BOOKS))
    ap.add_argument("--html", action="store_true")
    a = ap.parse_args()
    for k in a.books:
        build(BOOKS[k](), a.html)


if __name__ == "__main__":
    main()
