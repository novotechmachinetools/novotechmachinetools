#!/usr/bin/env python3
"""One-off: value-line model codes back to the manufacturer's original codes (NT-… → BS-/TBK-/TGK-/GZ).

Rewrites the generator sources, image alt texts, llms.txt, the catalogue template and the AI prompt,
longest phrase first so composite phrases ("NT-H 13 / 13 C") are mapped as a whole.
Run once, then: python3 tools/value_line_data.py && python3 tools/bandsaw_pages.py && python3 build.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODELS = {  # NT code → original code
    "NT-H 10 F": "BS-315GF",
    "NT-H 13 C": "BS-460G-JC",
    "NT-H 13": "BS-460G",
    "NT-H 16": "BS-2114TH",
    "NT-H 12 SC": "BS-5030",
    "NT-H 18": "BS-650GA",
    "NT-A 12 SC": "BS-5040",
    "NT-A 12 T": "BS300x370H",
    "NT-A 12": "BS300x370",
    "NT-A 13": "BS-460GB",
    "NT-A 14": "BS-500G",
    "NT-A 16": "BS-500GT",
    "NT-A 18": "BS-650G",
    "NT-A 24": "BS-850G",
    "NT-DC 11 AV": "TBK-4228B (improved)",
    "NT-DC 11 A": "TBK-4228B",
    "NT-DC 11 T": "TBK-4228A",
    "NT-DC 11": "TBK-4228",
    "NT-DC 14": "TGK-4235",
    "NT-DC 16": "TGK-4240",
    "NT-DC 20": "GZ4250/70",
    "NT-DC 24": "GZ4260/120",
}
COMPOSITE = {  # shorthand phrases first
    "NT-DC 11 / 11 T / 11 A / 11 AV": "TBK-4228 / 4228A / 4228B / 4228B (improved)",
    "NT-DC 11, 11 T, 14, 16, 20 and 24": "TBK-4228, TBK-4228A, TGK-4235, TGK-4240, GZ4250/70 and GZ4260/120",
    "NT-DC 11 A and NT-DC 11 AV": "TBK-4228B and TBK-4228B (improved)",
    "NT-DC 11 A / AV": "TBK-4228B / 4228B (improved)",
    "NT-DC 14 / 16 and NT-DC 20": "TGK-4235 / 4240 and GZ4250/70",
    "NT-DC 14 and NT-DC 16": "TGK-4235 and TGK-4240",
    "NT-DC 14 and 16": "TGK-4235 and 4240",
    "NT-DC 14 / 16": "TGK-4235 / 4240",
    "NT-DC 20 and NT-DC 24": "GZ4250/70 and GZ4260/120",
    "NT-DC 20 and 24": "GZ4250/70 and GZ4260/120",
    "NT-DC 20 / 24": "GZ4250/70 / GZ4260/120",
    "NT-H 13 / 13 C and NT-H 18": "BS-460G / 460G-JC and BS-650GA",
    "NT-H 13 / 13 C": "BS-460G / 460G-JC",
    "NT-A 12 / 12 T": "BS300x370 / 300x370H",
    "NT-A 14 / 16 / 18 / 24 CNC": "BS-500G / 500GT / 650G / 850G CNC",
    "NT-A 14 to NT-A 24 CNC": "BS-500G to BS-850G CNC",
    "NT-A 14 to NT-A 24": "BS-500G to BS-850G",
    "NT-A 14 and NT-A 16": "BS-500G and BS-500GT",
    "NT-A 14, 16 and 18": "BS-500G, 500GT and 650G",
    "NT-A 14/16": "BS-500G/500GT",
}
IDS = {
    "novotech-nt-h10f": "novotech-bs-315gf",
    "novotech-nt-h13": "novotech-bs-460g",
    "novotech-nt-h16": "novotech-bs-2114th",
    "novotech-nt-h12sc": "novotech-bs-5030",
    "novotech-nt-h18": "novotech-bs-650ga",
    "novotech-nt-a12sc": "novotech-bs-5040",
    "novotech-nt-a12": "novotech-bs300x370",
    "novotech-nt-a13": "novotech-bs-460gb",
    "novotech-nt-a-cnc": "novotech-bs-cnc",
    "novotech-nt-dc11": "novotech-tbk-4228",
    "novotech-nt-dc14": "novotech-tgk-4235",
    "novotech-nt-dc20": "novotech-gz4250",
}
GENERIC = [  # series wording that no longer applies
    ("NovoTech Semi-Automatic Band Saws — NT-H Hydraulic Bandsaws | Canada", "NovoTech Semi-Automatic Band Saws — Hydraulic Bandsaws | Canada"),
    ("NovoTech NT-H semi-automatic metal cutting band saws", "NovoTech semi-automatic metal cutting band saws"),
    ("NovoTech Automatic Band Saws — NT-A CNC Bandsaws | Canada", "NovoTech Automatic Band Saws — CNC Bandsaws | Canada"),
    ("NovoTech NT-A automatic metal cutting band saws", "NovoTech automatic metal cutting band saws"),
    ("NovoTech Double Column Band Saws — NT-DC Bandsaws | Canada", "NovoTech Double Column Band Saws — Twin-Column Bandsaws | Canada"),
    ("NovoTech NT-DC double column metal cutting band saws", "NovoTech double column metal cutting band saws"),
    ('short="NT-A CNC saws"', 'short="BS-500G–850G CNC saws"'),
    ("NovoTech value line band saw families (NT-series).", "NovoTech value line band saw families (manufacturer's original model codes)."),
    ("NovoTech value line (NT-series models)", "NovoTech value line (BS-, TBK-, TGK- and GZ-series models)"),
    ("The NT-DC 11 series offers", "The TBK-4228 series offers"),
    ("the NT-DC 11 series", "the TBK-4228 series"),
    ("NT-DC 11 series", "TBK-4228 series"),
]
FILES = [
    "tools/value_line_data.py", "tools/bandsaw_pages.py", "tools/image_map.json", "src/root/llms.txt",
    "src/root/ask.php", "tools/value_line_pdf/catalogue.html.j2", "content/pages/band-saw.json", "docs/seo-keywords.md",
]


def main():
    # longest first so "NT-DC 11 AV" wins over "NT-DC 11 A" and "NT-DC 11"
    simple = sorted(MODELS.items(), key=lambda kv: -len(kv[0]))
    for rel in FILES:
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        before = s
        for a, b in GENERIC:
            s = s.replace(a, b)
        for a, b in sorted(COMPOSITE.items(), key=lambda kv: -len(kv[0])):
            s = s.replace(a, b)
        for a, b in simple:
            s = re.sub(re.escape(a) + r"(?![A-Z0-9])(?! (?:F|C|SC|T|A|AV)\b)", b, s)   # not inside a longer code
        for a, b in sorted(IDS.items(), key=lambda kv: -len(kv[0])):
            s = s.replace(a, b)
        if s != before:
            open(p, "w", encoding="utf-8").write(s)
            print("rewrote", rel)
    left = []
    for rel in FILES:
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        left += [(rel, m.group(0)) for m in re.finditer(r"NT-[A-Z]+( \d+)?( [A-Z]+)?|novotech-nt-[a-z0-9-]+", s)]
    print("left:", left)


if __name__ == "__main__":
    main()
