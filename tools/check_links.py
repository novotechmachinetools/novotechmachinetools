#!/usr/bin/env python3
"""Broken-link check over dist/: every internal href/src and every #anchor must resolve.

Pages of the old site that have not been rebuilt yet (press brakes, lasers …) are listed in OLD_SITE
and allowed until their rebuild; anything else that is missing fails the build.

    python3 tools/check_links.py        (exit 1 on broken links)
"""
import glob
import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
OLD_SITE = {
    "products", "about-us", "contact-us", "brochures", "metal-fabricating-articles", "privacy-policy",
    "press-brake", "laser-cutting-machine", "shear-cutting", "iron-worker-punch", "plate-roller-bender",
    "pipe-profile-roll-bender", "folder-sheet-metal-brake", "horizontal-press-brake",
    "hydraulic-press", "plate-beveler",
    "lock-former", "sheet-metal-plate-deburring-edge-rounding-finishing-grinding",
    "pipe-polishing-deburring-grinding-brushing", "corner-notcher", "aluminum-and-pvc-upcut-saws",
    "press-brake-tooling-punch-and-die", "the-benefits-of-using-a-rebar-bender-and-cutter-in-construction",
}


def main():
    exists = set()
    for root, _, files in os.walk(DIST):
        for f in files:
            exists.add(os.path.relpath(os.path.join(root, f), DIST))
    pages = sorted(glob.glob(os.path.join(DIST, "*.html")))
    ids = {p: set(re.findall(r'id="([^"]+)"', open(p, encoding="utf-8").read())) for p in pages}
    broken = []
    for p in pages:
        s = open(p, encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src|data-src|poster)="([^"]+)"', s):
            u = m.group(1)
            if u.startswith(("http:", "https:", "mailto:", "tel:", "data:", "//", "javascript:")):
                continue
            path, _, frag = u.partition("#")
            path = unquote(path.split("?")[0]).lstrip("/")
            if path in ("", "./"):
                if frag and frag not in ids[p]:
                    broken.append((os.path.basename(p), u, "anchor not on page"))
                continue
            target = next((c for c in (path, path + ".html", path + "/index.html") if c in exists), None)
            if target is None:
                if path not in OLD_SITE:
                    broken.append((os.path.basename(p), u, "target missing"))
            elif frag and target.endswith(".html") and frag not in ids.get(os.path.join(DIST, target), set()):
                broken.append((os.path.basename(p), u, "anchor missing on target"))
    for b in sorted(set(broken)):
        print("BROKEN", *b)
    print(f"{len(pages)} pages checked, {len(set(broken))} broken links")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
