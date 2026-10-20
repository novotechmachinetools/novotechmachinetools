"""Build the 1200x630 social-share (Open Graph) image for every page.

    python3 -I tools/make_social.py

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


def load_cutout(name):
    """The hero as a full-resolution cut-out (never the white-background source photo as a white box —
    the house rule for every product photo on a non-white surface)."""
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


def build(page):
    slug = page["slug"]
    title = page.get("social_title") or page["h1"]
    tagline = page.get("social_tagline") or "Sold, installed and supported in Canada by NovoTech Machine Tools, Mississauga, ON"
    img = Image.new("RGB", (W, H), CHARCOAL)
    d = ImageDraw.Draw(img)
    # orange slanted band on the right
    d.polygon([(640, 0), (W, 0), (W, H), (520, H)], fill=ORANGE)
    # product cut-out centred on the band
    try:
        cut = load_cutout(page["hero_image"])
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
    # title
    tf = ImageFont.truetype(F_TITLE, 66)
    lines = wrap(d, title, tf, 470)
    y = 190
    for ln in lines[:3]:
        d.text((56, y), ln, font=tf, fill=WHITE)
        y += 72
    # orange rule + tagline
    d.rectangle((56, y + 10, 56 + 90, y + 16), fill=ORANGE)
    tf2 = ImageFont.truetype(F_TEXT, 24)
    y += 36
    for ln in wrap(d, tagline, tf2, 470)[:3]:
        d.text((56, y), ln, font=tf2, fill=MIST)
        y += 32
    # domain
    tf3 = ImageFont.truetype(F_TEXT, 26)
    d.text((56, H - 70), "NovoTechMachineTools.com  ·  +1 647 526 5510", font=tf3, fill=WHITE)
    out = os.path.join(out_dir, slug + ".jpg")
    q = 86
    while True:
        img.save(out, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(out) < 290_000 or q <= 60:
            break
        q -= 6
    print(f"{slug}.jpg  {os.path.getsize(out)//1024} KB  q={q}")


for fn in sorted(glob.glob(os.path.join(ROOT, "content", "pages", "*.json"))):
    if os.path.basename(fn).startswith("_"):
        continue
    build(json.load(open(fn, encoding="utf-8")))
