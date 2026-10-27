"""NovoTech's logo on every catalogue page, linked to the website: top right where the paper is free (left of the
style tab of the odd pages), else top left, else bottom centre; on a page with no free corner (full-bleed photos and
section openers) on a small white tile."""
import os

import fitz
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO = os.path.join(ROOT, "tools", "brochure", "out", "img", "novotech-logo-800.png")
URL = "https://novotechmachinetools.com"
H = 17.0                                       # logo height, pt
W = H * 800 / 279
S = 3
_xref = {}


def _ink(page):
    pix = page.get_pixmap(matrix=fitz.Matrix(S, S), colorspace=fitz.csGRAY, alpha=False)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width) < 240


def _free(ink, r, pad=3.0):
    X0, Y0 = int((r.x0 - pad) * S), int((r.y0 - pad) * S)
    X1, Y1 = int((r.x1 + pad) * S), int((r.y1 + pad) * S)
    if X0 < 0 or Y0 < 0 or X1 > ink.shape[1] or Y1 > ink.shape[0]:
        return False
    return not ink[Y0:Y1, X0:X1].any()


def spots(page):
    pw, ph = page.rect.width, page.rect.height
    y = 7.0
    return [fitz.Rect(pw - 40 - W, y, pw - 40, y + H),          # top right, clear of the style tab
            fitz.Rect(36, y, 36 + W, y + H),                    # top left
            fitz.Rect((pw - W) / 2, y, (pw + W) / 2, y + H),    # top centre
            fitz.Rect((pw - W) / 2, ph - 10 - H, (pw + W) / 2, ph - 10)]


def place_logo(page):
    ink = _ink(page)
    cand = spots(page)
    rect = next((r for r in cand if _free(ink, r)), None)
    tile = rect is None
    if tile:
        rect = cand[0]
        bg = fitz.Rect(rect.x0 - 4, rect.y0 - 3, rect.x1 + 4, rect.y1 + 3)
        sh = page.new_shape()
        sh.draw_rect(bg, radius=0.18)
        sh.finish(color=None, fill=(1, 1, 1), fill_opacity=0.94, width=0)
        sh.commit()
    doc = id(page.parent)
    if doc in _xref:
        page.insert_image(rect, xref=_xref[doc], keep_proportion=True)
    else:
        _xref[doc] = page.insert_image(rect, filename=LOGO, keep_proportion=True)
    page.insert_link({"kind": fitz.LINK_URI, "from": rect, "uri": URL})
    return rect, tile
