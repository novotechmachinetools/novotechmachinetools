"""Page-specific work for the catalogue edition: handlers that run before the line-by-line cleanup (running text set
again in English, tables in both units), POST steps after the inch values, and the NovoTech pages (cover, edition page,
back cover) and the American-style section."""
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WORK = os.path.join(ROOT, "tools", "cache", "edition")

HANDLERS = {}            # page number → [fn(page, ppage, ctx), …] before the clean-up
POST = {}                # page number → [fn(page, ctx, report), …] after the inch values

sys.path.insert(0, HERE)
import page6             # noqa: E402
import pagefix           # noqa: E402
import textflow          # noqa: E402


def on(pno, handler=None, post=None):
    if handler:
        HANDLERS.setdefault(pno, []).append(handler)
    if post:
        POST.setdefault(pno, []).append(post)


on(6, page6.metric_handler)
for _p in range(8, 13):
    on(_p, pagefix.index_head)
on(17, pagefix.p17)
on(82, post=pagefix.p82)
on(204, pagefix.p204)
on(215, pagefix.p215)
for _p in textflow.PAGES:
    on(_p, textflow.handler, textflow.post)


def imperial6():
    """the air-bending page in inches, which goes in front of EUROSTAMP's page 6 (built afresh)"""
    p = os.path.join(WORK, "imperial6.pdf")
    page6.build(p)
    return fitz.open(p)


def front_pages(sample=None):
    """NovoTech cover, edition page and back cover (HTML → PDF), as a fitz document of 3 pages.  `sample`: a PNG of a
    finished catalogue page for the edition page (punch 1055 on page 36)"""
    sys.path.insert(0, os.path.join(ROOT, "tools", "brochure"))
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import eurostamp_edition as EE
    sample = sample or os.path.join(ROOT, "tools", "brochure", "out", "img", "es-edition-sample.png")
    out = os.path.join(WORK, "front.pdf")
    EE.front_back_pdf(sample, "700+", out)
    return fitz.open(out)


def american_pages():
    """the American-style section (pages 272 – 277), built afresh"""
    import american
    p, report = american.build(os.path.join(WORK, "american.pdf"))
    for r in report:
        if r[2]:
            print("american: no room for the mm of", r)
    return fitz.open(p)
