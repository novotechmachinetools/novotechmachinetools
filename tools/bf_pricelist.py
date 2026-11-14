#!/usr/bin/env python3
"""Black Friday 2026 price list PDF — the file bf-quote.php e-mails to a buyer.

    python3 tools/bf_pricelist.py PRICES.json OUT.pdf

The machines, their text, photos and videos come from content/pages/black-friday-machinery-sale.json (the page shows them
without prices) and the links from the built page (dist/black-friday-machinery-sale.html, so the PDF links exactly where
the page does). The prices come only from PRICES.json, a private file kept out of this repository:
    {"<machine id>": {"price": <sale price>, "regular": <regular price>, "lease": "<monthly payment>", "lease_note"?: "…",
                      "pdf_optional"?: ["<option>: <price>"]}, …}
Rendered with Chromium (Playwright): Letter, NovoTech colours and fonts, the site's own photos.
"""
import html, json, os, re, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://novotechmachinetools.com/"
PAGE_SLUG = "black-friday-machinery-sale"
ORANGE, CHARCOAL, STEEL, INK, PAPER, LINE = "#F28A1F", "#2D2E30", "#5A5D62", "#1F2022", "#F4F5F6", "#D9DBDE"

prices = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
page = json.load(open(os.path.join(ROOT, "content", "pages", PAGE_SLUG + ".json"), encoding="utf-8"))
manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
image_map = json.load(open(os.path.join(ROOT, "tools", "image_map.json"), encoding="utf-8"))
built = open(os.path.join(ROOT, "dist", PAGE_SLUG + ".html"), encoding="utf-8").read()
TMP = tempfile.mkdtemp(prefix="bfpdf-")
e = html.escape


def links_of(mid):
    """the product page, brochure and buying-guide links of a machine card on the built page (absolute)"""
    m = re.search(r'<article[^>]*id="stock-' + re.escape(mid) + r'"(.*?)</article>', built, re.S)
    if not m:
        raise SystemExit(f"machine {mid} is not on the built page — run build.py first")
    out = {}
    for href, label in re.findall(r'<li><a href="([^"]+)"[^>]*>([^<]+)</a></li>', m.group(1)):
        out[label.strip()] = href if href.startswith("http") else SITE + href
    return out


def jpeg(key, width, name=None):
    """the largest manifest variant of an image, flattened on white and saved as JPEG at the given width (a small PDF)"""
    ent = manifest[key]
    v = max(ent["variants"], key=lambda x: x["w"])
    im = Image.open(os.path.join(ROOT, "src", v["file"]))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    p = os.path.join(TMP, (name or key) + f"-{width}.jpg")
    im.save(p, "JPEG", quality=76, optimize=True, progressive=False)
    return "file://" + p


def png(key, width):
    """a cut-out kept transparent (the cover machines sit on the orange band), with its drop shadow drawn in and the colours
    reduced, so the cover stays light (a CSS filter would make Chromium embed a large lossless bitmap)"""
    from PIL import ImageFilter
    ent = manifest[key]
    v = max(ent["variants"], key=lambda x: x["w"])
    im = Image.open(os.path.join(ROOT, "src", v["file"])).convert("RGBA")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    pad, off, blur = 34, 16, 13
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = im.getchannel("A").point(lambda x: x * 0.5)
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    shadow.putalpha(a)
    canvas.alpha_composite(shadow, (pad, pad + off))
    canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(im, (pad, pad))
    q = canvas.quantize(colors=255, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    p = os.path.join(TMP, key + f"-{width}.png")
    q.save(p, "PNG", optimize=True)
    return "file://" + p


def money(n):
    return f"C${n:,.0f}"


def yt(vid):
    return f"https://www.youtube.com/watch?v={vid}"


FONT = "file://" + os.path.join(ROOT, "src", "fonts")
cats = {c["id"]: c["title"] for c in page["stock_cats"]}
items = []
for it in page["stock"]:
    pr = prices.get(it["id"])
    if not pr:
        raise SystemExit(f"no price for {it['id']}")
    keys = [x[0] for x in it["images"]]
    caps = [(x[1] if len(x) > 1 else image_map.get(x[0], {}).get("alt", "")) for x in it["images"]]
    items.append(dict(it, pr=pr, links=links_of(it["id"]), main=jpeg(keys[0], 720), main_cap=caps[0],
                      thumbs=[(jpeg(k, 260), c) for k, c in list(zip(keys, caps))[1:4]]))

# ------------------------------------------------------------------ html
CSS = f"""
@font-face {{ font-family: B; font-weight: 400; src: url({FONT}/barlow-latin-400-normal.woff2); }}
@font-face {{ font-family: B; font-weight: 500; src: url({FONT}/barlow-latin-500-normal.woff2); }}
@font-face {{ font-family: B; font-weight: 600; src: url({FONT}/barlow-latin-600-normal.woff2); }}
@font-face {{ font-family: B; font-weight: 700; src: url({FONT}/barlow-latin-700-normal.woff2); }}
@font-face {{ font-family: BC; font-weight: 500; src: url({FONT}/barlow-condensed-latin-500-normal.woff2); }}
@font-face {{ font-family: BC; font-weight: 600; src: url({FONT}/barlow-condensed-latin-600-normal.woff2); }}
@font-face {{ font-family: BC; font-weight: 700; src: url({FONT}/barlow-condensed-latin-700-normal.woff2); }}
@font-face {{ font-family: D; font-weight: 400; src: url({FONT}/nt-diameter-400.woff2); unicode-range: U+00D8, U+00F8; size-adjust: 96.2%; }}
@font-face {{ font-family: D; font-weight: 600; src: url({FONT}/nt-diameter-600.woff2); unicode-range: U+00D8, U+00F8; size-adjust: 96.2%; }}
@font-face {{ font-family: D; font-weight: 700; src: url({FONT}/nt-diameter-700.woff2); unicode-range: U+00D8, U+00F8; size-adjust: 96.2%; }}
@page {{
  size: Letter; margin: 0.78in 0.5in 0.7in;
  @top-left {{ content: "NOVOTECH MACHINE TOOLS"; font: 700 9pt BC, sans-serif; letter-spacing: .12em; color: {CHARCOAL}; vertical-align: bottom; padding-bottom: 8pt; }}
  @top-right {{ content: "BLACK FRIDAY 2026 · IN-STOCK PRICE LIST"; font: 700 9pt BC, sans-serif; letter-spacing: .12em; color: {ORANGE}; vertical-align: bottom; padding-bottom: 8pt; }}
  @bottom-left {{ content: "Prices valid until Dec 4, 2026, 11:59 pm ET · CAD, plus applicable taxes · +1 647 526 5510 · info@novotechmachinetools.com"; font: 400 7.5pt B, sans-serif; color: {STEEL}; vertical-align: top; padding-top: 8pt; }}
  @bottom-right {{ content: "Page " counter(page) " of " counter(pages); font: 600 8pt B, sans-serif; color: {CHARCOAL}; vertical-align: top; padding-top: 8pt; }}
}}
@page :first {{ margin: 0; @top-left {{ content: none; }} @top-right {{ content: none; }} @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font: 400 9.4pt/1.38 D, B, sans-serif; color: {INK}; }}
a {{ color: inherit; }}
h1, h2, h3 {{ font-family: D, BC, sans-serif; margin: 0; line-height: 1.02; color: {CHARCOAL}; }}
/* ---------------- cover */
.cover {{ position: relative; width: 8.5in; height: 11in; overflow: hidden; background: {CHARCOAL}; color: #fff; break-after: page; }}
.cv-top {{ height: 1.55in; background: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 0.55in; border-bottom: 6pt solid {ORANGE}; }}
.cv-top img {{ height: 0.86in; }}
.cv-contact {{ text-align: right; font: 500 9.5pt/1.45 B, sans-serif; color: {CHARCOAL}; }}
.cv-contact b {{ font: 700 13pt BC, sans-serif; letter-spacing: .02em; }}
.cv-band {{ position: absolute; left: -10%; right: -10%; top: 5.15in; height: 2.15in; background: {ORANGE}; transform: rotate(-9deg); }}
.cv-band2 {{ position: absolute; left: -10%; right: -10%; top: 4.86in; height: 0.1in; background: {ORANGE}; opacity: .55; transform: rotate(-9deg); }}
.cv-title {{ position: absolute; left: 0.55in; top: 1.95in; z-index: 2; }}
.cv-dates {{ display: inline-block; font: 700 12pt BC, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: {INK}; background: {ORANGE}; padding: 4pt 9pt 3pt; border-radius: 2pt; }}
.cv-big {{ margin-top: 10pt; font: 700 72pt/.86 BC, sans-serif; text-transform: uppercase; color: #fff; }}
.cv-big span {{ display: block; color: {ORANGE}; }}
.cv-sub {{ margin-top: 12pt; font: 600 20pt BC, sans-serif; letter-spacing: .14em; text-transform: uppercase; }}
.cv-sub small {{ display: block; margin-top: 3pt; font: 500 11pt B, sans-serif; letter-spacing: 0; text-transform: none; color: #D9DBDE; }}
.cv-m1 {{ position: absolute; z-index: 2; right: 0.25in; top: 2.65in; width: 4.6in; }}
.cv-m2 {{ position: absolute; z-index: 3; right: 0.2in; top: 4.85in; width: 2.2in; }}
.cv-offers {{ position: absolute; z-index: 4; left: 0.55in; right: 0.55in; top: 7.45in; display: grid; grid-template-columns: 1fr 1fr; gap: 9pt; }}
.cv-offer {{ background: #fff; color: {INK}; border-top: 4pt solid {ORANGE}; border-radius: 3pt; padding: 9pt 11pt 9pt; }}
.cv-offer b {{ display: block; font: 700 14pt/1.1 BC, sans-serif; color: {CHARCOAL}; margin-bottom: 2pt; }}
.cv-offer span {{ font-size: 8.8pt; color: {STEEL}; }}
.cv-offer.tax {{ background: #FFF3E6; }}
.cv-foot {{ position: absolute; z-index: 4; left: 0.55in; right: 0.55in; bottom: 0.32in; font: 400 8.2pt/1.4 B, sans-serif; color: #C9CBCF; }}
.cv-foot b {{ color: #fff; }}
/* ---------------- machine */
.cat-h {{ break-after: avoid; margin: 0 0 6pt; }}
.item {{ break-inside: avoid; padding: 7pt 0 9pt; border-top: 1pt dashed {LINE}; }}
.cat-h + .item {{ border-top: 0; padding-top: 2pt; }}
.it-meta {{ display: flex; flex-wrap: wrap; align-items: center; gap: 4pt 8pt; margin: 4pt 0 7pt; }}
.st {{ display: inline-flex; align-items: center; gap: 5pt; font: 700 8pt BC, sans-serif; letter-spacing: .08em; text-transform: uppercase; color: #17663A; background: #E5F4EA; padding: 2.5pt 7pt 2pt; border-radius: 2pt; }}
.st::before {{ content: ""; width: 5pt; height: 5pt; border-radius: 50%; background: #1F9D55; }}
.st.back {{ color: #8A4A0E; background: #FFF3E6; }}
.st.back::before {{ background: {ORANGE}; }}
.brand {{ font: 600 7.8pt B, sans-serif; letter-spacing: .08em; text-transform: uppercase; color: {STEEL}; }}
.item h2 {{ font: 700 18pt/1.04 BC, sans-serif; }}
.it-sub {{ display: inline-block; font: 600 9.5pt BC, sans-serif; letter-spacing: .02em; color: #fff; background: {CHARCOAL}; border-left: 4pt solid {ORANGE}; padding: 2.5pt 9pt 2pt 8pt; }}
.it-grid {{ display: grid; grid-template-columns: 2.7in 1fr; gap: 13pt; align-items: start; }}
.media .main {{ border: .8pt solid {LINE}; background: #fff; height: 1.95in; display: flex; align-items: center; justify-content: center; padding: 6pt; }}
.media .main img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
.media .cap {{ margin: 2pt 0 0; font-size: 7pt; line-height: 1.25; color: {STEEL}; }}
.thumbs {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4pt; margin-top: 4pt; }}
.thumbs figure {{ margin: 0; }}
.thumbs .t {{ height: 0.52in; border: .6pt solid {LINE}; background: #fff; display: flex; align-items: center; justify-content: center; padding: 2pt; }}
.thumbs img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
.thumbs figcaption {{ display: none; }}
.price {{ display: grid; grid-template-columns: auto 1fr; border: 1.5pt solid {ORANGE}; border-radius: 4pt; overflow: hidden; margin-bottom: 7pt; }}
.price .p1 {{ padding: 4pt 10pt 4pt; background: #FFF3E6; }}
.price .lbl {{ display: block; font: 700 7pt BC, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #8A4A0E; }}
.price .bfp {{ display: block; font: 700 22pt/1 BC, sans-serif; color: {INK}; }}
.price .p2 {{ padding: 4pt 10pt; display: flex; flex-direction: column; justify-content: center; gap: 2pt; }}
.price .reg {{ font-size: 9.8pt; color: {STEEL}; }}
.price .reg s {{ color: #D0021B; font-weight: 700; }}   /* the regular price struck through in red (the owner, Nov 14 2026) */
.price .save {{ font: 700 10pt BC, sans-serif; color: #17663A; letter-spacing: .02em; }}
.price .lease {{ grid-column: 1 / -1; background: {CHARCOAL}; color: #fff; padding: 2.6pt 10pt; font: 600 8.6pt B, sans-serif; }}
.price .lease b {{ color: {ORANGE}; font-size: 10.4pt; }}
.price .lease small {{ color: #C9CBCF; font-weight: 400; font-size: 7.6pt; }}
.capy {{ margin: 0 0 5pt; font: 700 12pt/1.12 BC, sans-serif; }}
.capy span {{ display: block; font: 700 7pt BC, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #8A4A0E; }}
dl.caps {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 12pt; margin: 0 0 5pt; border-top: 2pt solid {ORANGE}; }}
dl.caps div {{ display: flex; justify-content: space-between; gap: 6pt; padding: 2.2pt 0; border-bottom: .6pt solid #E8EAEC; font-size: 8pt; }}
dl.caps dt {{ color: {STEEL}; }}
dl.caps dd {{ margin: 0; font-weight: 700; text-align: right; }}
.about {{ margin: 0 0 5pt; font-size: 8.4pt; line-height: 1.32; color: #3B3D40; }}
ul.key {{ list-style: none; margin: 0 0 5pt; padding: 0; }}
ul.key li {{ background: #FFF3E6; border-left: 3pt solid {ORANGE}; padding: 1.8pt 7pt; margin-bottom: 2pt; font-weight: 600; font-size: 8.2pt; }}
ul.feat {{ list-style: none; margin: 0 0 4pt; padding: 0; columns: 2; column-gap: 13pt; font-size: 8pt; line-height: 1.27; }}
ul.feat li {{ position: relative; padding: 0 0 2pt 9pt; break-inside: avoid; }}
ul.feat li::before {{ content: ""; position: absolute; left: 0; top: 4pt; width: 5.5pt; height: 2pt; background: {ORANGE}; }}
ul.feat.one {{ columns: 1; }}
.opt {{ margin: 2pt 0 4pt; font-size: 8pt; }}
.opt b {{ color: {CHARCOAL}; }}
.badges {{ display: flex; flex-wrap: wrap; gap: 3pt; margin: 3pt 0 5pt; }}
.badges span {{ font: 600 7.2pt B, sans-serif; color: {CHARCOAL}; background: {PAPER}; border: .6pt solid {LINE}; border-radius: 10pt; padding: 1.5pt 7pt; }}
.links {{ display: flex; flex-wrap: wrap; align-items: center; gap: 3pt 9pt; font-size: 7.9pt; }}
.links a {{ font-weight: 600; color: {INK}; text-decoration: underline; text-decoration-color: {ORANGE}; text-underline-offset: 1.5pt; }}
.links .vids {{ display: inline-flex; align-items: center; gap: 3pt; }}
.links .vids a {{ display: inline-flex; align-items: center; justify-content: center; min-width: 13pt; height: 13pt; padding: 0 3pt; text-decoration: none; background: {CHARCOAL}; color: #fff; border-radius: 2pt; font: 700 8pt BC, sans-serif; }}
.links .vids a:first-of-type {{ background: {ORANGE}; color: {INK}; }}
.links .lbl {{ font: 700 7.4pt BC, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: {STEEL}; }}
/* ---------------- terms */
.terms {{ break-before: page; }}
.terms h3 {{ font: 700 12.5pt BC, sans-serif; margin: 10pt 0 3pt; color: {CHARCOAL}; }}
.terms p, .terms li {{ font-size: 8.8pt; color: #3B3D40; margin: 0 0 4pt; }}
.terms ul {{ margin: 0 0 4pt; padding-left: 13pt; }}
.contact-box {{ margin-top: 14pt; display: grid; grid-template-columns: 1.15in 1fr; gap: 12pt; align-items: center; border: 1.4pt solid {ORANGE}; border-radius: 4pt; padding: 10pt 14pt; }}
.contact-box img {{ width: 1.15in; }}
.contact-box p {{ margin: 0; font-size: 9.2pt; }}
.contact-box b {{ font: 700 13pt BC, sans-serif; }}
"""


def li(xs):
    return "".join(f"<li>{e(x)}</li>" for x in xs)


def item_html(x):
    pr = x["pr"]
    save = pr["regular"] - pr["price"]
    note = pr.get("lease_note")
    lease_txt = (f'or <b>{e(pr["lease"])}</b> / month {e(note)}' if note else
                 f'or <b>{e(pr["lease"])}</b> / month for 36 months')
    lease = f'<div class="lease">{lease_txt} <small>· 36-month lease, 0% down, on approved credit</small></div>'
    status = (f'<span class="st back">Back order · about {x.get("lead", 90)} days · 10% down secures it</span>'
              if x.get("status") == "back" else '<span class="st">In stock in Mississauga, ON</span>')
    brand = x.get("brand") or ""
    caps = ""
    if x.get("caps"):
        caps = '<dl class="caps">' + "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in x["caps"]) + "</dl>"
    capy = f'<p class="capy"><span>Capacity</span>{e(x["capacity"])}</p>' if x.get("capacity") else ""
    feats = x.get("features") or []
    feat = f'<ul class="feat{" one" if len(feats) <= 3 else ""}">{li(feats)}</ul>' if feats else ""
    opt = ""
    if pr.get("pdf_optional"):
        opt = '<p class="opt"><b>Optional:</b> ' + e("; ".join(pr["pdf_optional"])) + "</p>"
    badges = "".join(f"<span>{e(b)}</span>" for b in x.get("badges") or [])
    vids = x.get("videos") or []
    vlinks = ""
    if vids:
        vlinks = ('<span class="vids"><span class="lbl">Videos</span>' +
                  "".join(f'<a href="{yt(v)}">{i + 1}</a>' for i, v in enumerate(vids)) + "</span>")
    L = x["links"]
    more = [f'<a href="{SITE}{PAGE_SLUG}#stock-{x["id"]}">All photos and videos</a>']
    for lab in ("Brochure (PDF)", "Product page", "Buying guide"):
        if lab in L:
            more.append(f'<a href="{L[lab]}">{lab}</a>')
    thumbs = "".join(f'<figure><div class="t"><img src="{s}" alt=""></div><figcaption>{e(c)}</figcaption></figure>' for s, c in x["thumbs"])
    return f"""
<section class="item" id="m-{x['id']}">
  <h2>{e(x['title'])}</h2>
  <div class="it-meta">{f'<span class="it-sub">{e(x["sub"])}</span>' if x.get('sub') else ''}{status}{f'<span class="brand">{e(brand)}</span>' if brand else ''}</div>
  <div class="it-grid">
    <div class="media">
      <div class="main"><img src="{x['main']}" alt=""></div>
      <p class="cap">{e(x['main_cap'])}</p>
      {f'<div class="thumbs">{thumbs}</div>' if thumbs else ''}
    </div>
    <div class="info">
      <div class="price">
        <div class="p1"><span class="lbl">Black Friday price</span><span class="bfp">{money(pr['price'])}</span></div>
        <div class="p2"><span class="reg">Regular price <s>{money(pr['regular'])}</s></span><span class="save">You save {money(save)}</span></div>
        {lease}
      </div>
      {capy}{caps}
      {f'<p class="about">{e(x["about"])}</p>' if x.get('about') else ''}
      {f'<ul class="key">{li(x["key"])}</ul>' if x.get('key') else ''}
      {feat}{opt}
      {f'<div class="badges">{badges}</div>' if badges else ''}
      <div class="links">{vlinks}{''.join(more)}</div>
    </div>
  </div>
</section>"""


logo = jpeg("novotech-logo", 700, "logo")
body = []
body.append(f"""
<div class="cover">
  <div class="cv-top"><img src="{logo}" alt="NovoTech Machine Tools">
    <div class="cv-contact"><b>+1 647 526 5510</b><br>info@novotechmachinetools.com<br>novotechmachinetools.com<br>1365 Mid-Way Blvd, Unit 26, Mississauga, ON</div></div>
  <div class="cv-band2"></div><div class="cv-band"></div>
  <div class="cv-title"><span class="cv-dates">Now until Dec 4, 2026</span>
    <div class="cv-big">Black<span>Friday</span></div>
    <div class="cv-sub">In-stock price list<small>{len(items)} machines at Black Friday prices<br>from our Mississauga, ON warehouse</small></div></div>
  <img class="cv-m1" src="{png('dn-xl-1', 760)}" alt="">
  <img class="cv-m2" src="{png('bk-hero-auto-350ga', 420)}" alt="">
  <div class="cv-offers">
    <div class="cv-offer"><b>Black Friday prices on stock</b><span>Every machine in this list, while quantities last</span></div>
    <div class="cv-offer"><b>5% off factory orders</b><span>Confirm by Dec 4 — only 10% down, 90% on delivery</span></div>
    <div class="cv-offer"><b>0% down financing</b><span>36-month lease payment shown for every machine, on approved credit</span></div>
    <div class="cv-offer tax"><b>100% first-year write-off*</b><span>Eligible manufacturing equipment — Ontario manufacturers can add a 15% tax credit*</span></div>
  </div>
  <div class="cv-foot"><b>Prices valid until Friday, December 4, 2026, 11:59 pm ET.</b> Prices in Canadian dollars, plus applicable taxes. To reserve a machine, reply to our email or call +1 647 526 5510 (Mon–Fri 9:00–17:00 ET). *See the terms on the last page.</div>
</div>""")
for cid, ctitle in cats.items():
    xs = [x for x in items if x["cat"] == cid]
    if not xs:
        continue
    body.append(f'<h1 class="sec-title cat-h">{e(ctitle)}</h1>')
    body += [item_html(x) for x in xs]
body.append(f"""
<section class="terms">
  <h1 class="sec-title">Black Friday terms</h1>
  <h3>Prices and dates</h3>
  <ul><li>Black Friday prices are valid now until Friday, December 4, 2026, 11:59 pm Eastern time, while quantities last. In-stock machines are first come, first served.</li>
  <li>All prices are in Canadian dollars (CAD), plus applicable taxes, for pickup at our Mississauga, ON warehouse. Freight across Canada and the US is arranged at competitive rates. Installation and training are available on request at an additional charge, except where a machine says it includes them.</li>
  <li>Back-order machines (marked in this list) are sold at their Black Friday price with 10% down to secure the order.</li></ul>
  <h3>Factory orders: 5% off</h3>
  <p>Any machine ordered from the factory and confirmed by December 4, 2026 is 5% off, with only 10% down to confirm the order and the remaining 90% on delivery.</p>
  <h3>Financing</h3>
  <p>The monthly payments shown are for a 36-month lease with 0% down, on approved credit (OAC), with a $10 buyout at the end of the lease, plus applicable taxes. Rates quoted on November 13, 2026 by our financing partner and subject to change.</p>
  <h3>100% first-year write-off*</h3>
  <p>Federal immediate expensing: machinery used in Canada mainly to manufacture or process goods for sale or lease can be deducted in full in the tax year it becomes available for use, so a machine from stock can be delivered and running before your year-end. Ontario Made Manufacturing Investment Tax Credit: eligible Ontario corporations can also claim a 15% tax credit on qualifying manufacturing machinery and equipment.</p>
  <p><i>*General information, not tax advice. Eligibility depends on your business, how the machine is used and when it becomes available for use. Ask your accountant.</i></p>
  <h3>Warranty</h3>
  <p>Warranty and money-back guarantee as shown for each machine. Specifications and photos are for reference and subject to change without notice; errors and omissions excepted.</p>
  <div class="contact-box"><img src="{logo}" alt="">
    <p><b>Reserve your machine: +1 647 526 5510</b><br>info@novotechmachinetools.com · novotechmachinetools.com<br>Showroom and warehouse: 1365 Mid-Way Blvd, Unit 26, Mississauga, ON L5T 2J5 · Mon–Fri 9:00–17:00 ET<br>
    <a href="{SITE}{PAGE_SLUG}">See every machine with photos and videos online</a></p></div>
</section>""")

doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>NovoTech Black Friday 2026 — In-stock price list</title><style>{CSS}</style></head><body>{"".join(body)}</body></html>'
hp = os.path.join(TMP, "pricelist.html")
open(hp, "w", encoding="utf-8").write(doc)

import asyncio
from playwright.async_api import async_playwright


async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto("file://" + hp, wait_until="load")
        await pg.evaluate("document.fonts.ready")
        await pg.pdf(path=OUT, prefer_css_page_size=True, print_background=True, tagged=True, outline=True)
        await b.close()

asyncio.run(render())
from pypdf import PdfReader, PdfWriter   # title and author in the file properties
r = PdfReader(OUT)
w = PdfWriter(clone_from=r)
w.add_metadata({"/Title": "NovoTech Black Friday 2026 — In-stock price list", "/Author": "NovoTech Machine Tools Inc.",
                "/Subject": "Black Friday prices, valid until Dec 4, 2026"})
with open(OUT, "wb") as f:
    w.write(f)
print(OUT, f"{os.path.getsize(OUT) / 1e6:.1f} MB,", len(r.pages), "pages; html", hp)
