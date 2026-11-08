"""Cover pictures for the Brochures page: the first page of every PDF the page lists that has no cover yet (the owner,
Nov 7 2026: several brochures showed no picture).

    python3 tools/make_pdf_covers.py            # only the PDFs without a cover
    python3 tools/make_pdf_covers.py --all      # redo every cover

Renders page 1 at 640 px wide into tools/src-images/brochures/pdf-<name>.jpg (the build looks a brochure's cover up as
the image 'pdf-' + its file name), registers it in tools/image_map.json and makes the web sizes with make_images.py.
Reads the PDF list from dist/brochures.html, so build the site first.
"""
import json, os, re, subprocess, sys
import fitz  # PyMuPDF

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "tools", "image_map.json")
MANIFEST = os.path.join(ROOT, "tools", "image_manifest.json")
OUT = os.path.join(ROOT, "tools", "src-images", "brochures")


def key_of(href):
    return "pdf-" + re.sub(r"[^a-z0-9]+", "-", os.path.basename(href)[:-4].lower()).strip("-")


def title_of(href):
    base = os.path.basename(href)[:-4]
    if "/wikus/" in href:
        return f"WIKUS {base.replace('-', ' ').upper()} data sheet"
    return re.sub(r"^NovoTech-", "", base).replace("-", " ") + " PDF"


def main():
    redo = "--all" in sys.argv
    page = open(os.path.join(ROOT, "dist", "brochures.html"), encoding="utf-8").read()
    hrefs = sorted(set(re.findall(r'href="(files/[^"]+\.pdf)"', page)))
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    raw = open(MAP, encoding="utf-8").read()
    image_map = json.loads(raw)
    made = []
    os.makedirs(OUT, exist_ok=True)
    for href in hrefs:
        key = key_of(href)
        if key in manifest and not redo:
            continue
        pdf = os.path.join(ROOT, "src", href)
        if not os.path.exists(pdf):
            print("missing PDF:", href)
            continue
        doc = fitz.open(pdf)
        p0 = doc[0]
        zoom = 640 / p0.rect.width
        pix = p0.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        dst = os.path.join(OUT, key + ".jpg")
        pix.save(dst, jpg_quality=88)
        image_map[key] = {"src": os.path.relpath(dst, ROOT), "alt": "Cover of the " + title_of(href), "section": "site",
                          "trim": False, "quality": 80, "cutout": False}
        made.append(key)
        print(f"{key}: {pix.width}x{pix.height}")
    if not made:
        print("every brochure has a cover")
        return
    open(MAP, "w", encoding="utf-8").write(json.dumps(image_map, indent=1, ensure_ascii=False))
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "make_images.py"), "--only", ",".join(made)], check=True)


if __name__ == "__main__":
    main()
