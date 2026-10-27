"""Page-specific work for the catalogue edition: handlers that run before the line-by-line cleanup (running text set
again in English, tables in both units), POST steps after the inch values, and the NovoTech pages (cover, edition page,
back cover) and the American-style section."""
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WORK = os.path.join(ROOT, "tools", "cache", "edition")

HANDLERS = {}            # page number → fn(page, ppage, ctx)
POST = {}                # page number → fn(page, ctx)


def front_pages():
    """NovoTech cover, edition page and back cover (HTML → PDF), as a fitz document of 3 pages"""
    sys.path.insert(0, os.path.join(ROOT, "tools", "brochure"))
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import eurostamp_edition as EE
    sample = os.path.join(ROOT, "tools", "brochure", "out", "img", "es-edition-sample.png")
    out = os.path.join(WORK, "front.pdf")
    EE.front_back_pdf(sample, "700+", out)
    return fitz.open(out)


def american_pages():
    p = os.path.join(WORK, "american.pdf")
    return fitz.open(p) if os.path.exists(p) else None
