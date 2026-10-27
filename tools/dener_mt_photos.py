#!/usr/bin/env python3
"""Dener machine-tool photos → tools/src-images/dener/<key>.jpg (section 'dener', like tools/dener_photos.py).

Source: frames of NovoTech's own YouTube videos filmed at Dener in Kayseri, Turkey (TMC 1200, TTH-10, TTC-8, TGH-B 450 and
the machine-tool assembly hall) — the full-resolution frames YouTube keeps for every video (oardefault / oar1 – 3 for the
vertical Shorts, maxres frames for the grinder video), fetched from i.ytimg.com into /home/claude/dener-mt/yt/.  Dener's own
product photos are on dener.com, which this workspace cannot reach.

The TDC double-column machining centres have no photo yet: tdc_diagram() draws their working envelope instead.

Also writes 16:9 thumbnails for the Shorts (the vertical frame on a blurred copy of itself) into /home/claude/gms-site/yt/,
where tools/yt_thumbs.py picks them up instead of YouTube's own (a three-frame strip for Shorts).

    python3 tools/dener_mt_photos.py
"""
import os
import subprocess

from PIL import Image, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YT = "/home/claude/dener-mt/yt/"
OUT = os.path.join(ROOT, "tools", "src-images", "dener")
THUMBS = "/home/claude/gms-site/yt"
SHORTS = {"gUYhBOqIP3M": "oardefault", "XhIVx8rzqnY": "oardefault", "dim9DA1TmoQ": "oardefault", "_bkvwzuOYW0": "oardefault"}


def F(frame, box, alt, blur=()):
    return dict(src=YT + frame + ".jpg", box=box, alt=alt, blur=list(blur))


PHOTOS = {
    # TTC compact lathes (TTC-8 at Dener's showroom)
    "dn-ttc-1": F("dim9DA1TmoQ_oardefault", (0, 400, 1080, 1480), "Dener TTC-8 CNC lathe — 8″ chuck, 45° slant bed, chip conveyor at the side"),
    "dn-ttc-2": F("dim9DA1TmoQ_oar3", (0, 380, 1080, 1730), "Dener TTC-8 CNC lathe — the control and the front door"),
    "dn-ttc-3": F("dim9DA1TmoQ_oar2", (0, 220, 1080, 1300), "Dener TTC-8 — the 12-station turret and the hydraulic chuck inside the machine"),
    # TTH lathes (TTH-10)
    "dn-tth-1": F("XhIVx8rzqnY_oardefault", (0, 230, 1080, 1580), "Dener TTH-10 CNC lathe — 10″ chuck, 45° slant bed, front view"),
    "dn-tth-2": F("XhIVx8rzqnY_oar1", (0, 330, 1080, 1410), "Dener TTH-10 — the CNC control on the front of the machine"),
    "dn-tth-3": F("XhIVx8rzqnY_oar2", (0, 200, 1080, 1550), "Dener TTH-10 — 12-station servo turret with VDI and boring-bar holders"),
    "dn-tth-4": F("XhIVx8rzqnY_oar3", (0, 300, 1080, 1500), "Dener TTH-10 — chip conveyor, coolant tank and hydraulic unit at the back"),
    "dn-mt-lathe-casting": F("_bkvwzuOYW0_oar3", (0, 330, 1080, 1530), "One-piece 45° slant-bed casting of a Dener CNC lathe on the assembly line in Kayseri"),
    # TMC vertical machining centres (TMC 1200)
    "dn-tmc-1": F("gUYhBOqIP3M_oardefault", (0, 120, 1080, 1470), "Dener TMC 1200 vertical machining centre — BBT40 spindle, 24-tool changer",
                  blur=[(0, 520, 280, 920)]),
    "dn-tmc-2": F("gUYhBOqIP3M_oar1", (0, 420, 1080, 1500), "Dener TMC 1200 — the enclosure from the side, with the electrical cabinet"),
    "dn-tmc-3": F("gUYhBOqIP3M_oar3", (0, 560, 1080, 1640), "Dener TMC 1200 — the work area: 51 × 24″ T-slot table under the spindle"),
    "dn-mt-vmc-line": F("_bkvwzuOYW0_oardefault", (0, 200, 1080, 1550), "Vertical machining centre castings on Dener's machine-tool assembly line in Kayseri, Turkey"),
    # TGH surface grinder
    "dn-tgh-1": F("ofby5Vxihsc_maxresdefault", (0, 0, 1280, 720), "Dener TGH-B 450 NC surface grinder — 17.7 × 35.4″ table, 10″ touchscreen control"),
}


def frame(key, p):
    """crop boxes are given for a 1080-px-wide frame and scaled to the frame's own width (one Short keeps a 720-px frame)"""
    im = Image.open(p["src"]).convert("RGB")
    k = im.width / 1080 if im.height > im.width else 1.0
    sc = lambda b: tuple(round(v * k) for v in b)       # noqa: E731
    for b in p["blur"]:                                   # a reflection in the machine's window: blurred, feathered edges
        b = sc(b)
        soft = im.filter(ImageFilter.GaussianBlur(26 * k))
        mask = Image.new("L", im.size, 0)
        mask.paste(255, (b[0] + 20, b[1] + 20, b[2] - 20, b[3] - 20))
        mask = mask.filter(ImageFilter.GaussianBlur(18 * k))
        im = Image.composite(soft, im, mask)
    im = im.crop(sc(p["box"]))
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Sharpness(im).enhance(1.25)
    path = os.path.join(OUT, key + ".jpg")
    im.save(path, quality=92)
    return path


def short_thumb(vid, which):
    """1280 × 720 for the video card: the vertical frame centred on a darkened, blurred copy of itself"""
    src = Image.open(YT + f"{vid}_{which}.jpg").convert("RGB")
    top = (round(1280 * src.height / src.width) - 720) // 2
    bg = src.resize((1280, round(1280 * src.height / src.width))).crop((0, top, 1280, top + 720))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(30))).enhance(0.55)
    fg = src.resize((round(720 * src.width / src.height), 720), Image.LANCZOS)
    bg.paste(fg, ((1280 - fg.width) // 2, 0))
    os.makedirs(THUMBS, exist_ok=True)
    path = os.path.join(THUMBS, vid + ".jpg")
    bg.save(path, quality=88)
    return path


TDC = [("TDC 2112", 2100, 1220, 600, 1400, (2000, 1200)), ("TDC 3116", 3100, 1600, 1020, 1700, (3000, 1500)),
       ("TDC 4120", 4100, 2020, 1020, 2100, (4000, 1800))]


def i1(mm):
    return f"{mm / 25.4:,.1f}″"


def tdc_diagram():
    """the TDC working envelope: a front view of the gantry with its travels, and the three sizes in a table (SVG → PNG
    with the site's Chromium)"""
    rows = "".join(
        f'<tr><td class="m">{m}</td><td>{i1(x)} × {i1(y)} × {i1(z)}<small>{x:,} × {y:,} × {z:,} mm</small></td>'
        f'<td>{i1(c)}<small>{c:,} mm</small></td><td>{i1(t[0])} × {i1(t[1])}<small>{t[0]:,} × {t[1]:,} mm</small></td></tr>'
        for m, x, y, z, c, t in TDC)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face {{font-family: R; src: url(file://{ROOT}/tools/fonts/roboto/Roboto-Regular.ttf);}}
    @font-face {{font-family: RM; src: url(file://{ROOT}/tools/fonts/roboto/Roboto-Medium.ttf);}}
    @font-face {{font-family: RB; src: url(file://{ROOT}/tools/fonts/roboto/Roboto-Bold.ttf);}}
    body {{margin: 0; width: 1600px; height: 1000px; background: #fff; font-family: R; color: #2d2e30;}}
    .t {{position: absolute; left: 60px; top: 46px; font: 34px RB; letter-spacing: .5px;}}
    .s {{position: absolute; left: 60px; top: 94px; font: 22px R; color: #6b6d70;}}
    svg {{position: absolute; left: 40px; top: 150px;}}
    table {{position: absolute; left: 60px; top: 742px; border-collapse: collapse; font-size: 22px; width: 1480px;}}
    th {{font: 18px RM; text-transform: uppercase; letter-spacing: .6px; color: #fff; background: #2d2e30; text-align: left; padding: 10px 16px;}}
    td {{padding: 10px 16px; border-bottom: 1px solid #d9dadb; vertical-align: top;}}
    td small {{display: block; font-size: 16px; color: #7b7d80; margin-top: 2px;}}
    td.m {{font: 22px RB; color: #e8892a; white-space: nowrap;}}
    .lab {{font: 21px RM; fill: #2d2e30;}}
    .dim {{font: 21px RB; fill: #e8892a;}}
    </style></head><body>
    <div class="t">TDC DOUBLE-COLUMN MACHINING CENTRES — WORKING ENVELOPE</div>
    <div class="s">Front view, not to scale · X along the table, Y across it (the saddle on the cross rail), Z up and down (the ram)</div>
    <svg width="1520" height="580" viewBox="0 0 1520 580">
      <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z" fill="#e8892a"/></marker></defs>
      <rect x="160" y="470" width="1200" height="60" fill="#5a5c60"/>
      <rect x="250" y="440" width="1020" height="30" fill="#9a9ca0"/>
      <g stroke="#7e8085" stroke-width="3">{''.join(f'<line x1="{x}" y1="442" x2="{x}" y2="468"/>' for x in range(300, 1240, 70))}</g>
      <rect x="200" y="60" width="110" height="410" fill="#2d2e30"/>
      <rect x="1210" y="60" width="110" height="410" fill="#2d2e30"/>
      <rect x="170" y="40" width="1180" height="80" fill="#3c3e42"/>
      <rect x="640" y="70" width="240" height="110" fill="#e8892a"/>
      <rect x="705" y="120" width="110" height="250" fill="#4a4c50"/>
      <rect x="735" y="370" width="50" height="38" fill="#9a9ca0"/>
      <polygon points="748,408 772,408 760,428" fill="#9a9ca0"/>
      <text class="lab" x="760" y="35" text-anchor="middle">cross rail</text>
      <text class="lab" x="255" y="30" text-anchor="middle">column</text>
      <text class="lab" x="1265" y="30" text-anchor="middle">column</text>
      <text class="lab" x="760" y="560" text-anchor="middle">bed and table (T-slots)</text>
      <line x1="320" y1="235" x2="1200" y2="235" stroke="#e8892a" stroke-width="3" marker-start="url(#a)" marker-end="url(#a)"/>
      <rect x="402" y="207" width="190" height="34" fill="#fff"/>
      <text class="dim" x="497" y="232" text-anchor="middle">between columns</text>
      <line x1="260" y1="408" x2="1260" y2="408" stroke="#e8892a" stroke-width="3" stroke-dasharray="12 8" marker-start="url(#a)" marker-end="url(#a)"/>
      <rect x="985" y="380" width="200" height="34" fill="#fff"/>
      <text class="dim" x="1085" y="405" text-anchor="middle">X travel (table)</text>
      <line x1="910" y1="140" x2="910" y2="400" stroke="#e8892a" stroke-width="3" marker-start="url(#a)" marker-end="url(#a)"/>
      <text class="dim" x="925" y="290">Z travel (ram)</text>
      <circle cx="760" cy="95" r="16" fill="none" stroke="#fff" stroke-width="3"/><circle cx="760" cy="95" r="4" fill="#fff"/>
      <text class="lab" x="625" y="150" text-anchor="end">Y travel (saddle) ⊙</text>
    </svg>
    <table><tr><th>Model</th><th>Travels X × Y × Z</th><th>Between columns</th><th>Table</th></tr>{rows}</table>
    </body></html>"""
    tmp = os.path.join("/tmp", "tdc_diagram.html")
    open(tmp, "w", encoding="utf-8").write(html)
    out = os.path.join(OUT, "dn-tdc-diagram.png")
    js = f"""const {{chromium}} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{viewport: {{width: 1600, height: 1000}}}});
await p.goto('file://{tmp}'); await p.waitForTimeout(300); await p.screenshot({{path: '{out}'}}); await b.close(); }})();"""
    subprocess.run(["node", "-e", js], check=True)
    return out


PHOTOS["dn-tdc-diagram"] = dict(src=None, box=None, blur=[], alt="TDC double-column machining centres — working envelope: X, Y and Z "
                                                                 "travels, distance between columns and table of the TDC 2112, 3116 and 4120 (diagram)")


def export():
    os.makedirs(OUT, exist_ok=True)
    for key, p in PHOTOS.items():
        path = tdc_diagram() if key == "dn-tdc-diagram" else frame(key, p)
        print(key, Image.open(path).size)
    for vid, which in SHORTS.items():
        print("thumb", short_thumb(vid, which))


if __name__ == "__main__":
    export()
