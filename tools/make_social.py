"""Build the 1200x630 social-share (Open Graph) image for every page.

    python3 -I tools/make_social.py                 every page (and delete the images of pages that no longer exist)
    python3 -I tools/make_social.py --stale         only the pages without an image, or whose photo, heading or tagline
                                                    changed since it was drawn (build.py runs this itself)
    python3 -I tools/make_social.py <slug> …        the given pages

Reads content/pages/*.json (hero_image + social_title/h1) and tools/image_map.json for the source
photo, writes src/img/social/<slug>.jpg (JPEG, < 300 KB so WhatsApp/Facebook/LinkedIn accept it).
Layout: charcoal left panel with the NovoTech logo, page title and a one-line tagline; orange slanted
band on the right carrying the product cut-out — the same "Forge" look as the brochures.
"""
import json, os, glob
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout2 import auto_cutout, is_white_background  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 630
ORANGE, CHARCOAL, WHITE, MIST = (242, 138, 31), (45, 46, 48), (255, 255, 255), (200, 203, 207)
imap = json.load(open(os.path.join(ROOT, "tools", "image_map.json")))
F_TITLE = os.path.join(ROOT, "tools", "fonts", "barlow-condensed-latin-700-normal.ttf")
F_TEXT = os.path.join(ROOT, "tools", "fonts", "barlow-latin-500-normal.ttf")
out_dir = os.path.join(ROOT, "src", "img", "social")
os.makedirs(out_dir, exist_ok=True)


MANIFEST = json.load(open(os.path.join(ROOT, "tools", "image_manifest.json")))


def load_cutout(name):
    """The hero as a cut-out (never the white-background source photo as a white box — the house rule for every product
    photo on a non-white surface): the largest web variant when make_images already cut it out (BiRefNet), otherwise a
    full-resolution cut-out of the source photo."""
    m = MANIFEST.get(name) or {}
    if m.get("alpha") and m.get("variants"):
        v = max(m["variants"], key=lambda x: x["w"])
        im = Image.open(os.path.join(ROOT, "src", v["file"])).convert("RGBA")
        bbox = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        return im.crop(bbox) if bbox else im
    spec = imap[name]
    im = Image.open(os.path.join(ROOT, spec["src"]))
    if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] < 8:
        pass                                            # already a cut-out
    else:
        im = im.convert("RGB")
        white, level = is_white_background(im)
        if spec.get("cutout") if spec.get("cutout") is not None else white:
            im = auto_cutout(im, level)                 # full-resolution cut-out, same pipeline as make_images
    im = im.convert("RGBA")
    bbox = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    return im


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def build(page, default_hero=None):
    """default_hero: the photo for pages without a hero of their own (contact, brochures, articles, products, privacy)"""
    slug = page["slug"]
    title = page.get("social_title") or page["h1"]
    tagline = page.get("social_tagline") or "Sold, installed and supported in Canada\nMississauga, ON, Canada"
    img = Image.new("RGB", (W, H), CHARCOAL)
    d = ImageDraw.Draw(img)
    # orange slanted band on the right
    d.polygon([(640, 0), (W, 0), (W, H), (520, H)], fill=ORANGE)
    # product cut-out centred on the band
    try:
        cut = load_cutout(page.get("social_image") or page.get("hero_image") or default_hero)
        box_w, box_h = 560, 520
        cut.thumbnail((box_w, box_h), Image.LANCZOS)
        x = 580 + (W - 580 - cut.width) // 2 + 20
        y = (H - cut.height) // 2
        shadow = Image.new("RGBA", cut.size, (0, 0, 0, 0))
        img.paste(cut, (x, y), cut)
    except Exception as e:
        print("no hero for", slug, e)
    # logo (white wordmark would be ideal; use the colour logo on a white plate)
    logo = Image.open(os.path.join(ROOT, "src", "img", "site", "novotech-logo-800.webp")).convert("RGBA")
    lw = 300
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    plate = Image.new("RGB", (lw + 28, logo.height + 20), WHITE)
    plate.paste(logo, (14, 10), logo)
    img.paste(plate, (56, 48))
    # title: the whole heading when it fits in three lines, otherwise the part before its dash ("Rebar benders — …"),
    # never a heading cut off in the middle of a phrase
    head = title
    for dash in (" — ", " – ", " - ", ": "):
        if dash in title:
            head = title.split(dash)[0]
            break
    for text, size, max_lines in ((title, 66, 3), (title, 58, 3), (head, 66, 3), (head, 58, 3), (head, 50, 4)):
        tf = ImageFont.truetype(F_TITLE, size)
        lines = wrap(d, text, tf, 470)
        if len(lines) <= max_lines:
            break
    y = 190 if len(lines) <= 3 else 170
    for ln in lines[:max_lines]:
        d.text((56, y), ln, font=tf, fill=WHITE)
        y += round(size * 1.09)
    # orange rule + tagline
    d.rectangle((56, y + 10, 56 + 90, y + 16), fill=ORANGE)
    tf2 = ImageFont.truetype(F_TEXT, 24)
    y += 36
    for ln in [w for part in tagline.split("\n") for w in wrap(d, part, tf2, 440)][:3]:
        if y > H - 140:                                 # keep clear of the domain and phone lines
            break
        d.text((56, y), ln, font=tf2, fill=MIST)
        y += 32
    # domain and phone, two lines so they stay clear of the orange band
    tf3 = ImageFont.truetype(F_TEXT, 26)
    d.text((56, H - 98), "NovoTechMachineTools.com", font=tf3, fill=WHITE)
    d.text((56, H - 64), "+1 647 526 5510", font=tf3, fill=WHITE)
    out = os.path.join(out_dir, slug + ".jpg")
    q = 86
    while True:
        img.save(out, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(out) < 290_000 or q <= 60:
            break
        q -= 6
    print(f"{slug}.jpg  {os.path.getsize(out)//1024} KB  q={q}")


SOURCES = os.path.join(ROOT, "tools", "social_sources.json")     # what each card was drawn from, to redraw it when that changes
STYLE = 2                                                        # bump to redraw every card after a layout change


def card_key(page, default_hero):
    hero = page.get("social_image") or page.get("hero_image") or default_hero
    m = MANIFEST.get(hero) or {}
    v = max(m["variants"], key=lambda x: x["w"])["bytes"] if m.get("variants") else None
    return [STYLE, hero, v, page.get("social_title") or page["h1"], page.get("social_tagline")]


def main(args):
    pages = {}
    for fn in sorted(glob.glob(os.path.join(ROOT, "content", "pages", "*.json"))):
        if not os.path.basename(fn).startswith("_"):
            p = json.load(open(fn, encoding="utf-8"))
            pages[p["slug"]] = p
    default_hero = pages.get("index", {}).get("hero_image")
    done = json.load(open(SOURCES)) if os.path.exists(SOURCES) else {}
    if "--stale" in args or "--missing" in args:          # pages without a card, or whose photo, heading or tagline changed
        todo = [s for s in pages if not os.path.exists(os.path.join(out_dir, s + ".jpg"))
                or done.get(s) != card_key(pages[s], default_hero)]
    elif args:
        todo = [a for a in args if not a.startswith("--")]
    else:
        todo = list(pages)
    for fn in os.listdir(out_dir):                          # cards of pages that no longer exist
        if fn.endswith(".jpg") and fn[:-4] not in pages:
            os.remove(os.path.join(out_dir, fn))
            print("removed", fn)
    for s in todo:
        build(pages[s], default_hero)
        done[s] = card_key(pages[s], default_hero)
    done = {s: k for s, k in sorted(done.items()) if s in pages}
    with open(SOURCES, "w", encoding="utf-8") as f:
        f.write("{\n" + ",\n".join(f"{json.dumps(s)}: {json.dumps(k, ensure_ascii=False)}" for s, k in done.items()) + "\n}\n")


if __name__ == "__main__":
    main(sys.argv[1:])
