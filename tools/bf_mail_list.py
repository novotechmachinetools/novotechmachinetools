#!/usr/bin/env python3
"""The Black Friday price list inside the e-mail bf-quote.php sends a buyer (the owner, Nov 14 2026: "the same list as the PDF,
with the photos and the prices in front of them, in the body of the e-mail, so you can scroll through it").

    python3 tools/bf_mail_list.py PRICES.json PRIVATE_OUT.json

Writes two things:
  * the photos of the e-mail, public (they carry no price): src/img/email/bf/<photo>-m.jpg (the main photo, 400 × 300) and
    <photo>-t.jpg (the small ones, 128 × 96), JPEG on white because Outlook shows neither WebP nor transparency;
  * PRIVATE_OUT.json, the list with its prices, for ~/novotech-private/black-friday/bf-mail-list.json on the server (never in
    this repository, never in dist/): {"cats": [{"id", "title", "items": [{"id", "html"}]}]}. The HTML of a machine names its
    photos with short names (cid:i12@nt, looked up in "images"), and bf-quote.php puts those photos inside the e-mail (Outlook does not
    download pictures from the internet by itself), and {{PICK}} where it flags the machines the buyer asked about.

The design follows the price list PDF (tools/bf_pricelist.py): orange price box, the regular price struck through in red,
the 36-month lease payment, capacity, description, features, options, badges and links. Its classes are styled by the <style>
of the bf_offer e-mail (tools/mail_templates.py BF_LIST_CSS); sizes and colours that matter also sit on the tags, so the list
still reads where a mail app drops the <style>. Kept small: Gmail cuts e-mails whose HTML passes 102 KB.
"""
import html
import json
import os
import re
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://novotechmachinetools.com/"
PAGE_SLUG = "black-friday-machinery-sale"
IMG_DIR = os.path.join(ROOT, "src", "img", "email", "bf")
e = html.escape

prices = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
page = json.load(open(os.path.join(ROOT, "content", "pages", PAGE_SLUG + ".json"), encoding="utf-8"))
manifest = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json"), encoding="utf-8"))
image_map = json.load(open(os.path.join(ROOT, "tools", "image_map.json"), encoding="utf-8"))
built = open(os.path.join(ROOT, "dist", PAGE_SLUG + ".html"), encoding="utf-8").read()
os.makedirs(IMG_DIR, exist_ok=True)


def links_of(mid):
    """the product page, brochure and buying-guide links of a machine card on the built page (absolute)"""
    m = re.search(r'<article[^>]*id="stock-' + re.escape(mid) + r'"(.*?)</article>', built, re.S)
    if not m:
        raise SystemExit(f"machine {mid} is not on the built page — run build.py first")
    out = {}
    for href, label in re.findall(r'<li><a href="([^"]+)"[^>]*>([^<]+)</a></li>', m.group(1)):
        out[label.strip()] = href if href.startswith("http") else SITE + href
    return out


IMAGES = {}   # short cid name -> the photo's file under the site root, for bf-quote.php


def photo(key, size, suffix):
    """the photo on a white canvas of the given size (contained, a small margin), JPEG; returns its short cid name"""
    name = f"{key}-{suffix}"
    rel = f"img/email/bf/{name}.jpg"
    path = os.path.join(IMG_DIR, name + ".jpg")
    v = max(manifest[key]["variants"], key=lambda x: x["w"])
    src = os.path.join(ROOT, "src", v["file"])
    if not os.path.exists(path) or os.path.getmtime(path) < os.path.getmtime(src):
        im = Image.open(src)
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg.convert("RGB")
        W, H = size
        pad = round(W * 0.03)
        im.thumbnail((W - 2 * pad, H - 2 * pad), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), (255, 255, 255))
        canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
        canvas.save(path, "JPEG", quality=72 if suffix == "m" else 68, optimize=True, progressive=False)
    for k, v in IMAGES.items():
        if v == rel:
            return k
    k = f"i{len(IMAGES) + 1}"
    IMAGES[k] = rel
    return k


def cid(name):
    return f"cid:{name}@nt"


def money(n):
    return f"C${n:,.0f}"


def yt(vid):
    return f"https://youtu.be/{vid}"


FONT = "font-family:Arial,Helvetica,sans-serif;"


def item_html(it, pr):
    keys = [x[0] for x in it["images"]]
    caps = [(x[1] if len(x) > 1 else image_map.get(x[0], {}).get("alt", "")) for x in it["images"]]
    L = links_of(it["id"])
    page_url = f"{SITE}{PAGE_SLUG}#stock-{it['id']}"
    main = photo(keys[0], (400, 300), "m")
    thumbs = [photo(k, (128, 96), "t") for k in keys[1:4]]
    status = (f'<span class="bst bstb" style="color:#8A4A0E;">Back order &middot; about {it.get("lead", 90)} days &middot; 10% down secures it</span>'
              if it.get("status") == "back" else '<span class="bst">&#9679; In stock in Mississauga, ON</span>')
    brand = f' &nbsp;<span class="bbr">{e(it["brand"])}</span>' if it.get("brand") else ""
    sub = f'<span class="bs">{e(it["sub"])}</span> ' if it.get("sub") else ""

    th = "".join(f'<td class="th"><img src="{cid(t)}" width="62" height="47" alt="" class="thi"></td>' for t in thumbs)
    media = (f'<a href="{page_url}"><img src="{cid(main)}" width="200" height="150" alt="{e(it["title"])}" class="mi"></a>'
             + (f'<table cellpadding="0" cellspacing="0" border="0"><tr>{th}</tr></table>' if th else ""))

    save = pr["regular"] - pr["price"]
    note = pr.get("lease_note")
    lease = (f'or <b>{e(pr["lease"])}</b> / month {e(note)}' if note else
             f'or <b>{e(pr["lease"])}</b> / month for 36 months')
    box = (f'<table width="100%" cellpadding="0" cellspacing="0" border="0" class="pb" style="border:2px solid #F28A1F;">'
           f'<tr><td class="p1" bgcolor="#FFF3E6"><div class="pl">Black Friday price</div><b class="pp">{money(pr["price"])}</b></td>'
           f'<td class="p2">Regular price <s class="rg" style="color:#D0021B;">{money(pr["regular"])}</s><br><b class="sv">You save {money(save)}</b></td></tr>'
           f'<tr><td colspan="2" class="ls" bgcolor="#2D2E30" style="color:#FFFFFF;">{lease} <span>&middot; 0% down, on approved credit</span></td></tr></table>')

    parts = [box]
    if it.get("capacity"):
        parts.append(f'<div class="cy"><span>Capacity</span>{e(it["capacity"])}</div>')
    if it.get("caps"):
        rows = "".join(f'<tr><td class="kv">{e(a)}</td><td class="kv kvv">{e(b)}</td></tr>' for a, b in it["caps"])
        parts.append(f'<table width="100%" cellpadding="0" cellspacing="0" border="0" class="kt">{rows}</table>')
    if it.get("about"):
        parts.append(f'<p class="ab">{e(it["about"])}</p>')
    for k in it.get("key") or []:
        parts.append(f'<div class="ky">{e(k)}</div>')
    if it.get("features"):
        parts.append('<div class="ft">' + "<br>".join(f'<b>■</b> {e(f)}' for f in it["features"]) + "</div>")
    if pr.get("pdf_optional"):
        parts.append(f'<div class="op"><b>Optional:</b> {e("; ".join(pr["pdf_optional"]))}</div>')
    if it.get("badges"):
        parts.append('<div class="bd">' + " &middot; ".join(e(b) for b in it["badges"]) + "</div>")
    links = []
    vids = it.get("videos") or []
    if vids:
        links.append("Videos " + " ".join(f'<a href="{yt(v)}" class="vd">{i + 1}</a>' for i, v in enumerate(vids)))
    links.append(f'<a href="{page_url}">All photos and videos</a>')
    for lab in ("Brochure (PDF)", "Product page", "Buying guide"):
        if lab in L:
            links.append(f'<a href="{L[lab]}">{lab}</a>')
    parts.append('<div class="lk">' + " &middot; ".join(links) + "</div>")

    return (f'<tr><td class="bm">{{{{PICK}}}}'
            f'<div class="bt">{e(it["title"])}</div><div class="bmeta">{sub}{status}{brand}</div>'
            f'<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td class="c1" width="200" valign="top">{media}</td>'
            f'<td class="c2" valign="top">{"".join(parts)}</td></tr></table></td></tr>')


cats = []
for cid_, title in [(c["id"], c["title"]) for c in page["stock_cats"]]:
    xs = [it for it in page["stock"] if it["cat"] == cid_]
    if not xs:
        continue
    items = []
    for it in xs:
        pr = prices.get(it["id"])
        if not pr:
            raise SystemExit(f"no price for {it['id']}")
        items.append({"id": it["id"], "html": item_html(it, pr)})
    cats.append({"id": cid_, "title": title, "items": items})

data = {"made": "tools/bf_mail_list.py", "cats": cats, "images": IMAGES}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
size = sum(len(i["html"].encode()) for c in cats for i in c["items"])
imgs = sorted(f for f in os.listdir(IMG_DIR) if f.endswith(".jpg"))
total = sum(os.path.getsize(os.path.join(IMG_DIR, f)) for f in imgs)
print(f"{OUT}: {sum(len(c['items']) for c in cats)} machines, list HTML {size / 1024:.0f} KB; "
      f"{len(imgs)} photos in src/img/email/bf ({total / 1024:.0f} KB)")
