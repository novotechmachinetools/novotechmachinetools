#!/usr/bin/env python3
"""Brochure PDFs small enough to attach to an e-mail (the owner, Nov 9 2026) — without breaking them (Nov 12 2026).

The strictest common limit on the way to a customer is a 20 MB message (iCloud Mail, the classic Outlook client); an
attachment grows by about 37 % in the message (base64 and line breaks), so a PDF of at most 13.9 MB (LIMIT) fits every major
mailbox — Gmail, Outlook.com and Yahoo take 25 MB, Microsoft 365 35 MB by default.  Only PDFs over the limit are touched;
smaller ones keep their full quality.

The first version (PyMuPDF: rewrite_images, font subsetting, garbage collection, object streams) left the photos of the
Chromium-made brochures pointing at image patterns that no longer existed — "Unknown pattern" in poppler, and in Acrobat,
Chrome and phone viewers the pages came out without their photos (the owner, Nov 12 2026: the Plastmak brochure "has no
photos, it is all wrong").  So the photos are now changed in place and nothing else:

  * every JPEG photo drawn finer than the target resolution is scaled down to it and saved again as a JPEG in the SAME PDF
    object, so every page, pattern and form that uses it still finds it; its colour space and soft mask stay;
  * the resolution steps down (300 → 250 → 220 → 200 → 180 dpi, JPEG quality 85) only as far as the limit needs;
  * text, vector drawings, fonts and lossless images are not touched, no object is renumbered or dropped by hand;
  * the result is checked before it replaces anything: no image errors (pdfimages -list), qpdf --check clean, and every page
    rendered and compared with the original in ½-inch tiles (a photo that went missing shows at once).
The original goes to /home/claude/pdf-originals/ before it is replaced.

    python3 tools/pdf_email_fit.py                  every src/files/**/*.pdf over the limit
    python3 tools/pdf_email_fit.py a.pdf b.pdf      only these (a generator calls fit() on the PDF it has just written)
    python3 tools/pdf_email_fit.py --dry-run        report what would change, write nothing
    python3 tools/pdf_email_fit.py --check a.pdf    only report broken images
"""
import glob
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

import pikepdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = 13_900_000          # bytes
KEEP = "/home/claude/pdf-originals"
STEPS = [300, 250, 220, 200, 180]     # dpi, best first
QUALITY = 85


def image_errors(path):
    """the number of image / pattern errors poppler reports — 0 for a sound file"""
    r = subprocess.run(["pdfimages", "-list", path], capture_output=True, text=True)
    return len(re.findall(r"(?i)syntax error|unknown pattern", r.stderr))


def _max_ppi(path):
    """object number → the highest resolution at which that image is drawn anywhere in the file"""
    ppi = {}
    for line in subprocess.run(["pdfimages", "-list", path], capture_output=True, text=True).stdout.splitlines()[2:]:
        c = line.split()
        if len(c) >= 16 and c[2] == "image":
            ppi[int(c[10])] = max(ppi.get(int(c[10]), 0), float(c[12]), float(c[13]))
    return ppi


def _shrink(src, dst, target):
    ppi = _max_ppi(src)
    changed = 0
    with pikepdf.open(src) as pdf:
        for obj in pdf.objects:
            if not isinstance(obj, pikepdf.Stream) or obj.get("/Subtype") != "/Image":
                continue
            if obj.get("/Filter") != "/DCTDecode" or obj.get("/BitsPerComponent", 8) != 8 or "/Decode" in obj:
                continue
            p = ppi.get(obj.objgen[0])
            if not p or p <= target * 1.08:
                continue
            raw = obj.read_raw_bytes()
            im = Image.open(io.BytesIO(raw))
            if im.mode not in ("RGB", "L"):
                continue                   # CMYK / inverted JPEGs stay as they are
            f = target / p
            w, h = max(1, round(im.width * f)), max(1, round(im.height * f))
            buf = io.BytesIO()
            im.resize((w, h), Image.LANCZOS).save(buf, "JPEG", quality=QUALITY, optimize=True)
            if buf.tell() >= len(raw):
                continue
            obj.write(buf.getvalue(), filter=pikepdf.Name.DCTDecode)
            obj.Width, obj.Height = w, h
            if "/DecodeParms" in obj:
                del obj["/DecodeParms"]
            changed += 1
        pdf.save(dst, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.preserve)
    return changed


def pages_match(a, b, tmp):
    """every page of b rendered and compared with a at 40 dpi in 20 × 20 px (½-inch) tiles: a photo that went missing turns
    its tiles white (≈30 – 40 / 255 off), a photo that was only scaled down changes them a little (< 10) — the worst tile decides"""
    import numpy as np
    for d in ("a", "b"):
        os.makedirs(os.path.join(tmp, d), exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "40", "-png", a if d == "a" else b, os.path.join(tmp, d, "p")], check=True, capture_output=True)
    fa, fb = sorted(os.listdir(os.path.join(tmp, "a"))), sorted(os.listdir(os.path.join(tmp, "b")))
    if fa != fb:
        return False, "page count differs"
    worst, where = 0.0, ""
    for f in fa:
        x = np.asarray(Image.open(os.path.join(tmp, "a", f)).convert("L"), dtype=np.float32)
        y = np.asarray(Image.open(os.path.join(tmp, "b", f)).convert("L"), dtype=np.float32)
        if x.shape != y.shape:
            return False, f"{f}: page size differs"
        d = np.abs(x - y)
        H, W = (d.shape[0] // 20) * 20, (d.shape[1] // 20) * 20
        t = float(d[:H, :W].reshape(H // 20, 20, W // 20, 20).mean(axis=(1, 3)).max())
        if t > worst:
            worst, where = t, f
    return worst < 20.0, f"worst ½-inch tile {worst:.1f} / 255 off ({where})"


def fit(path, dry_run=False, log=print):
    """shrink `path` in place if it is over LIMIT; returns (old size, new size, dpi) or None when nothing changed"""
    size = os.path.getsize(path)
    if size <= LIMIT:
        return None
    if image_errors(path):
        raise SystemExit(f"{path}: its images are already broken — rebuild it from its source first")
    tmp = tempfile.mkdtemp(prefix="pdffit-")
    out = os.path.join(tmp, "fit.pdf")
    try:
        for dpi in STEPS:
            n = _shrink(path, out, dpi)
            new = os.path.getsize(out)
            if new <= LIMIT:
                break
        else:
            raise SystemExit(f"{path}: still over {LIMIT / 1e6:.1f} MB at {STEPS[-1]} dpi")
        errs = image_errors(out)
        chk = subprocess.run(["qpdf", "--check", out], capture_output=True, text=True).returncode
        ok, msg = pages_match(path, out, tmp)
        if errs or chk not in (0, 3) or not ok:       # qpdf: 3 = warnings only
            raise SystemExit(f"{path}: the smaller file failed its check (image errors {errs}, qpdf {chk}, {msg}) — left as it was")
        log(f"{os.path.basename(path)}: {size / 1e6:.1f} MB -> {new / 1e6:.1f} MB ({n} photos at {dpi} dpi, JPEG quality "
            f"{QUALITY}; {msg})")
        if not dry_run:
            os.makedirs(KEEP, exist_ok=True)
            keep = os.path.join(KEEP, os.path.basename(path))
            if not os.path.exists(keep):
                shutil.copy2(path, keep)
            shutil.move(out, path)
        return size, new, dpi
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = args or sorted(glob.glob(os.path.join(ROOT, "src", "files", "**", "*.pdf"), recursive=True))
    if "--check" in sys.argv:
        bad = [(f, image_errors(f)) for f in files]
        for f, n in bad:
            if n:
                print(f"BROKEN ({n} image errors): {os.path.relpath(f, ROOT)}")
        print(f"{sum(1 for _, n in bad if n)} of {len(files)} PDFs have broken images")
        return
    dry = "--dry-run" in sys.argv
    changed = 0
    for f in files:
        if fit(f, dry_run=dry):
            changed += 1
    print(f"{changed} PDF(s) over {LIMIT / 1e6:.1f} MB {'would be ' if dry else ''}made smaller; the rest left as they are")


if __name__ == "__main__":
    main()
