#!/usr/bin/env python3
"""Brochure PDFs small enough to attach to an e-mail (the owner, Nov 9 2026).

The strictest common limit on the way to a customer is a 20 MB message (iCloud Mail, the classic Outlook client); an
attachment grows by about 37 % in the message (base64 and line breaks), so a PDF of at most 13.9 MB (LIMIT) fits every major
mailbox — Gmail, Outlook.com and Yahoo take 25 MB, Microsoft 365 35 MB by default.  Only PDFs over the limit are touched;
smaller ones keep their full quality.

For a PDF over the limit, the best result that fits is kept:
  1. lossless first — unused glyphs dropped from the embedded fonts, unused objects removed, streams and objects compressed;
  2. then the photos: those finer than the target resolution are downsampled and saved as JPEG, starting at 400 dpi,
     quality 90, and stepping down only as far as needed.  Text, vector drawings and lossless images are never touched.
The original goes to /home/claude/pdf-originals/ before it is replaced.

    python3 tools/pdf_email_fit.py                  every src/files/**/*.pdf over the limit
    python3 tools/pdf_email_fit.py a.pdf b.pdf      only these (a generator calls fit() on the PDF it has just written)
    python3 tools/pdf_email_fit.py --dry-run        report what would change, write nothing
"""
import glob
import os
import shutil
import sys
import tempfile

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = 13_900_000          # bytes
KEEP = "/home/claude/pdf-originals"
# (dpi, JPEG quality), best first
STEPS = [(400, 90), (350, 90), (300, 90), (300, 85), (250, 85), (250, 80), (230, 85), (220, 85), (200, 85), (200, 80), (180, 82),
         (180, 80), (160, 80), (150, 80), (130, 78), (110, 75)]


def _attempt(src, out, step):
    doc = pymupdf.open(src)
    if step:
        dpi, q = step
        doc.rewrite_images(dpi_threshold=dpi + 10, dpi_target=dpi, quality=q, lossy=True, lossless=False, bitonal=False)
    try:
        doc.subset_fonts()
    except Exception:            # a font MuPDF cannot subset stays as it is
        pass
    doc.save(out, garbage=4, deflate=True, use_objstms=1)
    pages = doc.page_count
    doc.close()
    return os.path.getsize(out), pages


def fit(path, dry_run=False, log=print):
    """recompress `path` in place if it is over LIMIT; returns (old size, new size, step) or None when nothing changed"""
    size = os.path.getsize(path)
    if size <= LIMIT:
        return None
    with pymupdf.open(path) as d:
        pages = d.page_count
    tmp = tempfile.mkdtemp(prefix="pdffit-")
    out = os.path.join(tmp, "fit.pdf")
    for step in [None] + STEPS:
        new, n = _attempt(path, out, step)
        if n != pages:
            raise SystemExit(f"{path}: page count changed ({pages} -> {n})")
        if new <= LIMIT:
            label = "lossless" if step is None else f"photos at {step[0]} dpi, JPEG quality {step[1]}"
            log(f"{os.path.basename(path)}: {size / 1e6:.1f} MB -> {new / 1e6:.1f} MB ({label})")
            if not dry_run:
                os.makedirs(KEEP, exist_ok=True)
                keep = os.path.join(KEEP, os.path.basename(path))
                if not os.path.exists(keep):
                    shutil.copy2(path, keep)
                shutil.move(out, path)
            shutil.rmtree(tmp, ignore_errors=True)
            return size, new, step
    shutil.rmtree(tmp, ignore_errors=True)
    raise SystemExit(f"{path}: still over {LIMIT / 1e6:.1f} MB at the lowest step")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    files = args or sorted(glob.glob(os.path.join(ROOT, "src", "files", "**", "*.pdf"), recursive=True))
    changed = 0
    for f in files:
        if fit(f, dry_run=dry):
            changed += 1
    print(f"{changed} PDF(s) over {LIMIT / 1e6:.1f} MB {'would be ' if dry else ''}recompressed; the rest left as they are")


if __name__ == "__main__":
    main()
