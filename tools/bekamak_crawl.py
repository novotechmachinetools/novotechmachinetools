#!/usr/bin/env python3
"""Crawl bekamak.com (English product pages) into the Bekamak source folder.

For every product slug on bekamak.com it saves
  /home/claude/bekamak/site/img/<file>.jpg            the four slider photos at full size — the files behind the
                                                       "popup-gallery-item" links (1000 px), never the *_main.jpg thumbnails
  /home/claude/bekamak/site/img/details/<file>.jpg    every Standard / Optional Feature photo (800–1200 px)
  /home/claude/bekamak/site/products.json             {slug: {title, description, gallery: [files],
                                                               standard: [{title, file}], optional: [{title, file}],
                                                               specs: {capacity: {"+30": {round, rect, square}, …}, rows: {label: text}}}}
  /home/claude/bekamak/site/details.json              {slug: [{title, file}]}  (standard + optional, for bekamak_details.py)

    python3 tools/bekamak_crawl.py              crawl everything (skips files already downloaded)
    python3 tools/bekamak_crawl.py bms-230-dg   one product
"""
import html
import json
import os
import re
import sys
import urllib.request

BASE = "https://www.bekamak.com/"
OUT = "/home/claude/bekamak/site"
HEADERS = {"User-Agent": "Mozilla/5.0 (NovoTech site build)"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "ignore")


def download(rel, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return False
    data = get(BASE + rel.lstrip("/"), binary=True)
    with open(dest, "wb") as fh:
        fh.write(data)
    return True


def clean(t):
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def strip_tags(t):
    return clean(re.sub(r"<[^>]+>", " ", t))


def parse_specs(page):
    """The Technical Details tab: a capacity-by-angle table (round / rectangular / square, mm) followed by
    label/value rows (motor, blade speed, blade, working height, weight, L/W/H)."""
    i, j = page.find('id="teknik-detaylar"'), page.find('id="opsiyon-ozellikler"')
    if i < 0:
        return {}
    cap, rows = {}, {}
    for r in re.findall(r"<tr>(.*?)</tr>", page[i:j], re.S):
        cells = [strip_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
        if len(cells) == 5 and re.match(r"^[+-]?\d+°?$", cells[1]):
            ang = cells[1].replace("°", "")
            ang = "0" if ang in ("0", "+0", "-0") else ang
            def num(t):
                m = re.search(r"([\d.,]+)", t)
                return float(m.group(1).replace(",", ".")) if m else None
            rect = re.findall(r"([\d.,]+)\s*[xX×]\s*([\d.,]+)", cells[3])
            cap[ang] = {"round": num(cells[2]),
                        "rect": [float(rect[0][0].replace(",", ".")), float(rect[0][1].replace(",", "."))] if rect else None,
                        "square": num(cells[4])}
        elif len(cells) == 2 and cells[0]:
            rows[cells[0]] = cells[1]
    return {"capacity": cap, "rows": rows}


def product_slugs():
    page = get(BASE)
    slugs = sorted(set(re.findall(r'href="[^"]*?urun/([^"/]+)/?"', page)))
    return [s for s in slugs if s]


def parse_product(slug):
    page = get(f"{BASE}urun/{slug}/en")
    title = clean(re.search(r"<title>(.*?)</title>", page, re.S).group(1)) if re.search(r"<title>", page) else slug
    title = title.split("|")[0].strip()
    m = re.search(r'class="urun_detay_ust_aciklama">(.*?)</div>', page, re.S)
    description = clean(m.group(1)) if m else ""
    gallery = []
    for href in re.findall(r'<a href="(images/urunler/[^"]+\.jpe?g)" class="popup-gallery-item slide"', page):
        if "_main" in href:
            continue
        if href not in gallery:
            gallery.append(href)
    sections = {}
    for key, div_id in (("optional", "opsiyon-ozellikler"), ("standard", "standart-ozellikler")):
        m = re.search(r'id="%s">(.*?)<div class="tab-content-box' % div_id, page, re.S)
        items = []
        if m:
            block = m.group(1)
            # photos + captions sit in HTML comments; the visible list repeats the captions as text
            # two generations of pages: images/products_standard|products_option/<name>.jpg (unique names) and
            # images/urun_standart|urun_opsiyon/<id>.jpg (numeric ids that repeat between the two folders)
            for href, t in re.findall(r'<a href="(images/(?:products_[a-z]+|urun_[a-z]+)/[^"]+)"[^>]*title="([^"]*)"', block):
                t = clean(t)
                folder = href.split("/")[1]
                fname = os.path.basename(href)
                if folder.startswith("urun_"):
                    fname = ("std-" if "standart" in folder else "opt-") + fname
                if t and not any(i["file"] == fname for i in items):
                    items.append({"title": t, "file": fname, "rel": href})
            seen = {i["title"].lower() for i in items}
            for t in re.findall(r'<li[^>]*>([^<]+)</li>', block):
                t = clean(t)
                if t and t.lower() not in seen:
                    items.append({"title": t, "file": None, "rel": None})
                    seen.add(t.lower())
        sections[key] = items
    return {"title": title, "description": description, "gallery": gallery, **sections, "specs": parse_specs(page)}


def main():
    os.makedirs(os.path.join(OUT, "img", "details"), exist_ok=True)
    ppath = os.path.join(OUT, "products.json")
    products = json.load(open(ppath)) if os.path.exists(ppath) else {}
    slugs = sys.argv[1:] or product_slugs()
    for slug in slugs:
        try:
            p = parse_product(slug)
        except Exception as e:  # noqa: BLE001
            print(f"!! {slug}: {e}")
            continue
        n = 0
        for rel in p["gallery"]:
            n += download(rel, os.path.join(OUT, "img", os.path.basename(rel)))
        for key in ("standard", "optional"):
            for it in p[key]:
                if it["rel"]:
                    n += download(it["rel"], os.path.join(OUT, "img", "details", it["file"]))
                it.pop("rel", None)
        p["gallery"] = [os.path.basename(r) for r in p["gallery"]]
        products[slug] = p
        print(f"{slug:28s} {len(p['gallery'])} photos  {len(p['standard']):2d} standard  {len(p['optional']):2d} optional  ({n} new files)")
    json.dump(products, open(ppath, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    details = {s: [i for i in p["standard"] + p["optional"] if i["file"]] for s, p in products.items()}
    json.dump(details, open(os.path.join(OUT, "details.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(products), "products →", ppath)


if __name__ == "__main__":
    main()
