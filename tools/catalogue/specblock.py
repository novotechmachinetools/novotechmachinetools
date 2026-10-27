"""'Max US t/ft = …' under every 'Max T/m = …' of the tool data blocks (Mat / H / Max T/m / α / R …).

The new line takes the place under Max T/m and the lines below it move down one line pitch.  Where that would run into
something the alternatives are tried in turn:
  down     at full size, then a little smaller (the new line is wider than 'Max T/m = 100')
  push     the length / weight box right under the block moves down one pitch with it (vector lines and text), the
           frame line that ran into the box top is lengthened
  merge    'tempered' (on its own line under 'Mat = 42CrMo4') joins the Mat line; H … Max T/m move up a pitch
  up       the lines from the top of the block to Max T/m move up a pitch
  inline   last resort: '(33.6 US t/ft)' at the end of the Max T/m line, if that is free — else reported
"""
import re
from collections import Counter

import fitz
import numpy as np

from textedit import Editor, page_lines
from fonts import ttf, font, char_for

US_T_FT = 0.3048 * 1.10231                 # metric tons per metre → US tons per foot
MAX_RE = re.compile(r"^Max\s*T/m\s*=\s*(\d+(?:[.,]\d+)?)")
LEN_RE = re.compile(r"^\d{2,4}\s*mm(\s+\d+(?:[.,]\d+)?\s*kg)?$", re.I)
KG_RE = re.compile(r"^\d+(?:[.,]\d+)?\s*kg$", re.I)
S = 3                                      # mask resolution, px per pt


def us_tft(v):
    return f"{v * US_T_FT:.1f}"


def ink_mask(page):
    pix = page.get_pixmap(matrix=fitz.Matrix(S, S), colorspace=fitz.csGRAY, alpha=False)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width) < 235


def glyph_rect(L, dy=0.0):
    """the area a line's glyphs cover (baseline-ish to cap height), moved dy down"""
    r = fitz.Rect(L.bbox)
    return fitz.Rect(r.x0, L.O.y - 0.80 * L.size + dy, r.x1, L.O.y + 0.22 * L.size + dy)


def _px(r, pad=0.0):
    return (max(0, int((r.y0 - pad) * S)), int(np.ceil((r.y1 + pad) * S)), max(0, int((r.x0 - pad) * S)), int(np.ceil((r.x1 + pad) * S)))


def free(mask, r, page, margin=1.0):
    R = fitz.Rect(r.x0 - margin, r.y0 - margin, r.x1 + margin, r.y1 + margin)
    if R.x0 < 8 or R.y0 < 8 or R.x1 > page.rect.width - 8 or R.y1 > page.rect.height - 8:
        return False
    y0, y1, x0, x1 = _px(R)
    return not mask[y0:y1, x0:x1].any()


def clear(mask, r, pad=0.6):
    y0, y1, x0, x1 = _px(r, pad)
    mask[y0:y1, x0:x1] = False


def mark(mask, r, pad=0.6):
    y0, y1, x0, x1 = _px(r, pad)
    mask[y0:y1, x0:x1] = True


def block_of(M, lines):
    """the data block a Max T/m line belongs to: the lines aligned with it (left, or right where the block is set flush
    right) at a line pitch; returns (lines, 'left' | 'right')"""
    cand = [L for L in lines if L.upright and abs(L.size - M.size) <= 0.3 * M.size]      # not the 8 pt box rows

    def chain(key):
        col = sorted([L for L in cand if abs(key(L) - key(M)) < 2.0], key=lambda L: L.O.y)
        i = col.index(M)
        blk, j = [M], i
        while j > 0 and col[j].O.y - col[j - 1].O.y < 1.9 * M.size:
            j -= 1
            blk.insert(0, col[j])
        j = i
        while j < len(col) - 1 and col[j + 1].O.y - col[j].O.y < 1.9 * M.size:
            j += 1
            blk.append(col[j])
        return blk
    left = chain(lambda L: L.O.x)
    right = chain(lambda L: L.bbox.x1)
    return (right, "right") if len(right) > len(left) else (left, "left")


def new_line_items(M, value):
    """'Max US t/ft = 33.6' in the fonts of the Max T/m line: label font, '=' font, number font"""
    lab = next(c for c in M.chars if c.c.strip())
    eq = next((c for c in M.chars if c.c == "="), lab)
    dig = next((c for c in reversed(M.chars) if c.c.isdigit()), lab)
    return [("Max US t/ft ", lab.font), ("= ", eq.font), (value, dig.font)]


# ------------------------------------------------------------------------------------------------- the box below
def _within(G, r):
    """r (possibly a zero-height / zero-width line rect) lies inside G"""
    return G.x0 <= r.x0 and r.x1 <= G.x1 and G.y0 <= r.y0 and r.y1 <= G.y1


def _seg_lines(d):
    """a drawing's straight segments as (p, q), 're' items as their four sides"""
    out = []
    for it in d["items"]:
        if it[0] == "l":
            out.append((it[1], it[2]))
        elif it[0] == "re":
            R = it[1]
            out += [(R.tl, R.tr), (R.bl, R.br), (R.tl, R.bl), (R.tr, R.br)]
    return out


def box_below(page, blk, lines, drawings):
    """the ruled length / weight box right under a block (within 30 pt, overlapping its columns): its outer rect"""
    bottom = max(L.bbox.y1 for L in blk)
    x0 = min(L.bbox.x0 for L in blk)
    x1 = max(L.bbox.x1 for L in blk)
    cells = [L for L in lines if L.upright and L.size <= 10 and (LEN_RE.match(L.t) or KG_RE.match(L.t))
             and bottom - 2 < L.bbox.y0 < bottom + 30 and L.bbox.x0 < x1 + 10 and L.bbox.x1 > x0 - 10]
    if not cells:
        return None
    tight = fitz.Rect(cells[0].bbox)
    for c in cells:
        tight |= c.bbox
    rows = sorted([L for L in lines if L.upright and L.size <= 10 and abs(L.bbox.x0 - tight.x0) < 60
                   and tight.y0 - 1 < L.bbox.y0 < tight.y0 + 140], key=lambda L: L.bbox.y0)
    for L in rows:
        if L.bbox.y0 - tight.y1 < 16 and L.bbox.x0 < tight.x1 + 30 and L.bbox.x1 > tight.x0 - 30:
            tight |= L.bbox
    big = fitz.Rect(tight.x0 - 10, tight.y0 - 8, tight.x1 + 10, tight.y1 + 10)
    xs, ys = [], []
    for d in drawings:
        if not d.get("color") or "s" not in (d.get("type") or ""):
            continue
        for p, q in _seg_lines(d):
            if big.contains(p) and big.contains(q):
                if abs(p.y - q.y) < 0.3 and abs(p.x - q.x) > 4:
                    ys.append(p.y)
                    xs += [p.x, q.x]
                elif abs(p.x - q.x) < 0.3 and abs(p.y - q.y) > 4:
                    xs.append(p.x)
                    ys += [p.y, q.y]
    if len(xs) < 2 or len(ys) < 2:
        return None
    R = fitz.Rect(min(xs), min(ys), max(xs), max(ys))
    if not _within(fitz.Rect(R.x0 - 0.5, R.y0 - 0.5, R.x1 + 0.5, R.y1 + 0.5), fitz.Rect(tight.x0 + 1, tight.y0 + 1, tight.x1 - 1, tight.y1 - 1)):
        return None
    return R


def _redraw(page, d, dy, items=None):
    sh = page.new_shape()
    for it in (items or d["items"]):
        k = it[0]
        if k == "l":
            sh.draw_line(it[1] + (0, dy), it[2] + (0, dy))
        elif k == "re":
            sh.draw_rect(it[1] + (0, dy, 0, dy))
        elif k == "qu":
            q = it[1]
            sh.draw_quad(fitz.Quad(q.ul + (0, dy), q.ur + (0, dy), q.ll + (0, dy), q.lr + (0, dy)))
        elif k == "c":
            sh.draw_bezier(it[1] + (0, dy), it[2] + (0, dy), it[3] + (0, dy), it[4] + (0, dy))
    lc = d.get("lineCap")
    lc = max(lc) if isinstance(lc, (list, tuple)) else (lc or 0)
    sh.finish(color=d.get("color"), fill=d.get("fill"), width=d.get("width") or 0.5, closePath=bool(d.get("closePath")),
              even_odd=bool(d.get("even_odd")), dashes=d.get("dashes") or None, lineCap=lc, lineJoin=int(d.get("lineJoin") or 0),
              fill_opacity=d.get("fill_opacity") if d.get("fill_opacity") is not None else 1,
              stroke_opacity=d.get("stroke_opacity") if d.get("stroke_opacity") is not None else 1)
    sh.commit()


def move_box(page, R, dy, lines, drawings):
    """move a ruled box (its lines, fills and text) dy down, with the frame line that joins it: the short connector into
    the box moves along, the vertical line that ends on it (or on the box top) is lengthened"""
    G = fitz.Rect(R.x0 - 0.8, R.y0 - 0.8, R.x1 + 0.8, R.y1 + 0.8)
    inside = [d for d in drawings if _within(G, d["rect"])]
    texts = [L for L in lines if G.contains(fitz.Point((L.bbox.x0 + L.bbox.x1) / 2, (L.bbox.y0 + L.bbox.y1) / 2))]
    conn, ext = [], []
    for d in drawings:
        if d in inside or not d.get("color") or len(d["items"]) != 1 or d["items"][0][0] != "l":
            continue
        p, q = d["items"][0][1], d["items"][0][2]
        if abs(p.y - q.y) < 0.3 and R.y0 - 0.5 <= p.y <= R.y1 + 0.5 and (min(abs(p.x - R.x1), abs(q.x - R.x1)) < 1.2
                                                                       or min(abs(p.x - R.x0), abs(q.x - R.x0)) < 1.2):
            conn.append(d)
    for d in drawings:
        if d in inside or d in conn or not d.get("color"):
            continue
        for p, q in _seg_lines(d):
            if abs(p.x - q.x) < 0.3:
                lo = max(p.y, q.y)
                if abs(lo - R.y0) < 1.2 and R.x0 - 1 <= p.x <= R.x1 + 1:
                    ext.append((p.x, lo, d))
                for c in conn:
                    a, b = c["items"][0][1], c["items"][0][2]
                    if abs(lo - a.y) < 1.2 and min(abs(p.x - a.x), abs(p.x - b.x)) < 1.2:
                        ext.append((p.x, lo, d))
    # MuPDF's 'covered' test counts the stroke's corners, so the redaction reaches 3 pt round the box; whatever else it
    # takes is set back where it was.  One rectangle per pass: with several, a path is not always taken out
    for r in [fitz.Rect(R.x0 - 3, R.y0 - 3, R.x1 + 3, R.y1 + 3)] + [
            fitz.Rect(d["rect"].x0 - 0.3, d["rect"].y0 - 0.5, d["rect"].x1 + 0.3, d["rect"].y1 + 0.5) for d in conn]:
        page.add_redact_annot(r, fill=False)
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=fitz.PDF_REDACT_TEXT_NONE)
    left = Counter(_sig(d) for d in page.get_drawings())
    removed = []
    for d in drawings:
        s = _sig(d)
        if left[s] > 0:
            left[s] -= 1
        else:
            removed.append(d)
    ours = {id(d) for d in inside + conn}
    rem = {id(d) for d in removed}
    stuck = [d for d in inside + conn if id(d) not in rem]
    gone = [c for L in texts for c in L.chars if c.c.strip()]
    for c in gone:
        w = c.adv() or c.size * 0.5
        ctr = fitz.Point(c.o.x + w / 2, c.o.y - 0.32 * c.size)
        r = max(0.25, min(w, c.size) * 0.16)
        page.add_redact_annot(fitz.Rect(ctr.x - r, ctr.y - r, ctr.x + r, ctr.y + r), fill=False)
    if gone:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                              text=fitz.PDF_REDACT_TEXT_REMOVE)
    stuck_ids = {id(d) for d in stuck}
    for d in drawings:                                 # in the page's own order, so fills stay under their lines
        if id(d) in rem:
            _redraw(page, d, dy if id(d) in ours else 0.0)
        elif id(d) in stuck_ids:
            _redraw(page, d, dy)
    for x, y, d in ext:
        sh = page.new_shape()
        sh.draw_line(fitz.Point(x, y), fitz.Point(x, y + dy))
        sh.finish(color=d["color"], width=d.get("width") or 0.5)
        sh.commit()
    by = {}
    for c in gone:
        by.setdefault(c.color, []).append(c)
    for col, cs in by.items():
        tw = fitz.TextWriter(page.rect)
        for c in cs:
            tw.append(fitz.Point(c.o.x, c.o.y + dy), char_for(c.c, c.font), font=font(ttf(c.font)), fontsize=c.size)
        tw.write_text(page, color=fitz.sRGB_to_pdf(col))
    return stuck


def _sig(d):
    r = d["rect"]
    return (d.get("type"), round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1), len(d["items"]))


# ------------------------------------------------------------------------------------------------- the page
BIG = (1.0, 0.9)
SMALL = (0.82, 0.74, 0.66)
DEBUG = []
ALPHA_FIRST = {187}        # crowded pages: 'α = …' joins the Mat line before anything else moves (the boxes stay put)


def _is_alpha(L):
    c = next((c for c in L.chars if c.c.strip()), None)
    return c is not None and (c.c == "α" or (c.c == "a" and "Symbol" in (c.font or ""))) and "=" in L.t


def add_us_lines(page, ppage=None, report=None):
    lines = page_lines(page, ppage)
    maxs = [L for L in lines if L.upright and MAX_RE.match(L.t)]
    if not maxs:
        return 0
    mask = ink_mask(page)
    drawings = page.get_drawings()
    pushes = []
    plans = []
    for M in maxs:
        v = float(MAX_RE.match(M.t).group(1).replace(",", "."))
        value = us_tft(v)
        blk, align = block_of(M, lines)
        i = blk.index(M)
        below = blk[i + 1:]
        if below:
            pitch = below[0].O.y - M.O.y
        else:
            ps = [b.O.y - a.O.y for a, b in zip(blk, blk[1:])]
            pitch = min(ps) if ps else 1.2 * M.size
        pitch = max(min(pitch, 1.6 * M.size), 1.1 * M.size)
        m2 = mask.copy()
        for L in blk:
            clear(m2, glyph_rect(L))
        items = new_line_items(M, value)

        def width(sc):
            return sum(font(ttf(f)).text_length(t, M.size * sc) for t, f in items)

        def x_at(sc):
            """where the new line starts along M's baseline"""
            return 0.0 if align == "left" else (M.bbox.x1 - M.O.x) - width(sc)

        def new_rect(sc, dy_down):
            x0 = M.O.x + x_at(sc)
            return fitz.Rect(x0, M.O.y + dy_down - 0.80 * M.size * sc, x0 + width(sc), M.O.y + dy_down + 0.22 * M.size * sc)

        def offs(sc):
            """(baseline of the new line under M, shift of the lines below): a smaller new line takes less room"""
            return pitch - 0.71 * M.size * (1 - sc), pitch - 0.92 * M.size * (1 - sc)

        R_box = box_below(page, blk, lines, drawings)
        T = next((L for L in blk[:i] if L.t.lower() == "tempered"), None)
        Mat = blk[blk.index(T) - 1] if T and blk.index(T) > 0 else None
        if not (Mat is not None and Mat.t.startswith("Mat")):
            T = None

        def try_down(scales):
            for sc in scales:
                d1, sh = offs(sc)
                if all(free(m2, glyph_rect(L, sh), page, margin=1.8) for L in below) and free(m2, new_rect(sc, d1), page):
                    return ("down", sc, d1, sh)

        def try_push(scales):
            if R_box is None or any(R_box.intersects(p[0]) for p in pushes):
                return None
            m3 = m2.copy()
            clear(m3, R_box, pad=1.0)
            for sc in scales:
                d1, sh = offs(sc)
                strip = fitz.Rect(R_box.x0 - 0.5, R_box.y1 + 0.5, R_box.x1 + 0.5, R_box.y1 + sh + 1.5)
                if not free(m3, strip, page, margin=0.5):
                    continue
                if all(free(m3, glyph_rect(L, sh), page) for L in below) and free(m3, new_rect(sc, d1), page):
                    return ("push", sc, d1, sh, R_box)

        def try_merge(scales):
            if T is None:
                return None
            sp = font(ttf(Mat.chars[-1].font)).text_length(" ", Mat.size)
            tw = font(ttf(T.main_font)).text_length("tempered", T.size)
            x_end = Mat.bbox.x1 + sp
            tr = fitz.Rect(x_end, Mat.O.y - 0.74 * Mat.size, x_end + tw + 1.5, Mat.O.y + 0.22 * Mat.size)
            if not free(m2, tr, page, margin=1.2):
                return None
            for sc in scales:
                if free(m2, new_rect(sc, 0.0), page):
                    return ("merge", sc, T, Mat, x_end)

        def try_alpha(scales):
            """'α = 30°' (the block's last line) moves to the end of the Mat line; the new line takes its place"""
            if align != "left" or not below or not _is_alpha(below[-1]) or not blk[0].t.startswith("Mat"):
                return None
            A, Mt = below[-1], blk[0]
            # some α lines come with a stray copy of their first glyph as a line of its own
            if any(not (len(L.t) == 1 and abs(L.O.x - A.O.x) < 1 and abs(L.O.y - A.O.y) < 1) for L in below[:-1]):
                return None
            txt = "".join(char_for(c.c, c.font) for c in A.chars).strip()
            ref = next((c for c in A.chars if c.c == "="), A.chars[-1])
            fpath = ttf(ref.font)
            sp = font(ttf(Mt.chars[-1].font)).text_length(" ", Mt.size)
            x_end = Mt.bbox.x1 + 1.1 * sp
            d_alpha = A.O.y - M.O.y
            thin = txt.replace(" ", "\u2009")
            for t2, a_sc in ((txt, 1.0), (txt, 0.86), (thin, 0.86), (thin, 0.78), (thin, 0.72)):
                aw = font(fpath).text_length(t2, A.size * a_sc)
                ar = fitz.Rect(x_end, Mt.O.y - 0.74 * A.size * a_sc, x_end + aw + 0.4, Mt.O.y + 0.2 * Mt.size)
                if not free(m2, ar, page, margin=0.8):
                    continue
                for sc in scales:
                    if free(m2, new_rect(sc, d_alpha), page):
                        return ("alpha", sc, d_alpha, A, Mt, x_end, t2, fpath, A.size * a_sc, ref.color)
            if DEBUG:
                print("   alpha: no room", fitz.Rect(x_end, Mt.O.y - Mt.size, x_end + aw, Mt.O.y))

        def try_compress():
            """every line of the block set again a little smaller at a tighter pitch, so that the new line fits in the
            height the block had: for blocks with nowhere to grow (a box beside them, the page foot under them)"""
            n = len(blk)
            if n < 3:
                return None
            y0, y1 = blk[0].O.y, blk[-1].O.y
            p2 = (y1 - y0) / n
            sc = min(1.0, p2 / pitch)
            if sc < 0.7:
                return None
            ys = [y0 + (k if k <= i else k + 1) * p2 for k in range(n)]
            y_new = y0 + (i + 1) * p2
            for L, y in zip(blk, ys):
                w = _line_width(L, sc)
                x = L.O.x if align == "left" else L.bbox.x1 - w
                if not free(m2, fitz.Rect(x, y - 0.8 * L.size * sc, x + w, y + 0.22 * L.size * sc), page, margin=0.6):
                    return None
            w = sum(font(ttf(f)).text_length(t, M.size * sc) for t, f in items)
            x = M.O.x if align == "left" else M.bbox.x1 - w
            if not free(m2, fitz.Rect(x, y_new - 0.8 * M.size * sc, x + w, y_new + 0.22 * M.size * sc), page, margin=0.6):
                return None
            return ("compress", sc, ys, y_new)

        def try_up(scales):
            above = blk[:i + 1]
            for sc in scales:
                if all(free(m2, glyph_rect(L, -pitch), page) for L in above) and free(m2, new_rect(sc, 0.0), page):
                    return ("up", sc)

        if page.number + 1 in ALPHA_FIRST:
            plan = (try_down(BIG) or try_alpha(BIG) or try_alpha(SMALL) or try_push(BIG) or try_merge(BIG)
                    or try_up(BIG) or try_down(SMALL) or try_push(SMALL) or try_merge(SMALL) or try_up(SMALL))
        else:
            plan = (try_down(BIG) or try_push(BIG) or try_merge(BIG) or try_up(BIG)
                    or try_down(SMALL) or try_push(SMALL) or try_merge(SMALL) or try_up(SMALL)
                    or try_alpha(BIG) or try_alpha(SMALL))
        if DEBUG:
            print("  plan", page.number + 1, M.t, align, [L.t for L in blk], "box" if R_box else "-", plan and plan[:2])
        if plan is None:
            plan = try_compress()
        if plan is None:
            dig = next((c for c in reversed(M.chars) if c.c.strip()), M.chars[-1])
            txt = f" ({value} US t/ft)"
            x = M.coords(dig.o)[0] + dig.adv()
            for sc in (0.82, 0.7):
                w = font(ttf(dig.font)).text_length(txt, M.size * sc)
                r = fitz.Rect(M.O.x + x, M.O.y - 0.75 * M.size * sc, M.O.x + x + w, M.O.y + 0.2 * M.size * sc)
                if free(m2, r, page, margin=0.8):
                    plan = ("inline", sc, x, txt, dig)
                    break
        if plan is None:
            if report is not None:
                report.append((page.number + 1, "us-t/ft", M.t))
            continue
        plans.append((M, blk, i, below, pitch, items, plan, x_at(plan[1])))
        # what the plan occupies, so that the next block on the page sees it
        kind = plan[0]
        if kind in ("down", "push"):
            d1, sh = plan[2], plan[3]
            mark(mask, new_rect(plan[1], d1))
            for L in below:
                mark(mask, glyph_rect(L, sh))
            if kind == "push":
                R = plan[4]
                pushes.append((R, sh))
                mark(mask, fitz.Rect(R.x0, R.y0 + sh, R.x1, R.y1 + sh))
        elif kind == "compress":
            _, sc, ys, y_new = plan
            for L, y in zip(blk, ys):
                mark(mask, fitz.Rect(L.bbox.x0, y - 0.8 * L.size * sc, L.bbox.x1, y + 0.22 * L.size * sc))
            mark(mask, fitz.Rect(M.bbox.x0, y_new - 0.8 * M.size * sc, M.bbox.x0 + width(sc), y_new + 0.22 * M.size * sc))
        elif kind == "alpha":
            _, sc, d_alpha, A, Mt, x_end, txt, fpath, asz, acol = plan
            mark(mask, new_rect(sc, d_alpha))
            mark(mask, fitz.Rect(x_end, Mt.O.y - 0.78 * asz, x_end + font(fpath).text_length(txt, asz), Mt.O.y + 0.24 * asz))
        elif kind in ("merge", "up"):
            mark(mask, new_rect(plan[1], 0.0))
            if kind == "up":
                for L in blk[:i + 1]:
                    mark(mask, glyph_rect(L, -pitch))
        if report is not None and (kind != "down" or plan[1] < 0.9):
            report.append((page.number + 1, "us-" + kind, f"{M.t} @{plan[1]:.2f}" if kind != "inline" else M.t))
    # the boxes move first (each move applies its own redactions), then the text edits
    for R, dy in pushes:
        move_box(page, R, dy, lines, page.get_drawings())     # the drawings as they are now: earlier moves changed them
    ed = Editor(page, lines)
    n = 0
    for M, blk, i, below, pitch, items, plan, x0 in plans:
        kind = plan[0]
        if kind in ("down", "push"):
            sc, d1, sh = plan[1], plan[2], plan[3]
            for L in below:
                ed.put_chars(L, L.chars, dy=-sh)
            write_items(ed, M, items, x0, -d1, sc)
        elif kind == "merge":
            _, sc, T, Mat, x_end = plan
            ed.put_chars(T, T.chars, dx=x_end - T.O.x, dy=T.O.y - Mat.O.y)
            k0 = blk.index(T)
            p_up = T.O.y - Mat.O.y
            for L in blk[k0 + 1:i + 1]:
                ed.put_chars(L, L.chars, dy=p_up)
            write_items(ed, M, items, x0, 0.0, sc)
        elif kind == "up":
            for L in blk[:i + 1]:
                ed.put_chars(L, L.chars, dy=pitch)
            write_items(ed, M, items, x0, 0.0, plan[1])
        elif kind == "compress":
            _, sc, ys, y_new = plan
            align = "left" if abs(blk[0].O.x - M.O.x) < 2 else "right"
            for L, y in zip(blk, ys):
                reset_line(ed, L, y, sc, align)
            w = sum(font(ttf(f)).text_length(t, M.size * sc) for t, f in items)
            x_new = 0.0 if align == "left" else (M.bbox.x1 - M.O.x) - w
            write_items(ed, M, items, x_new, -(y_new - M.O.y), sc)
        elif kind == "alpha":
            _, sc, d_alpha, A, Mt, x_end, txt, fpath, asz, acol = plan
            for L in below:                                  # the α line and any stray copy of its first glyph
                ed.drop(L.chars)
            ed.put_text(Mt, x_end - Mt.O.x, txt, fpath, asz, color=acol)
            write_items(ed, M, items, x0, -d_alpha, sc)
        else:
            _, sc, x, txt, dig = plan
            ed.put_text(M, x, txt, dig.font, M.size * sc, color=dig.color)
        n += 1
    ed.apply()
    return n


def _segments(L):
    """a line as (text, font, size, colour) pieces: consecutive glyphs in one font"""
    out = []
    for c in L.chars:
        ch = char_for(c.c, c.font)
        if out and out[-1][1] == c.font and abs(out[-1][2] - c.size) < 0.01 and out[-1][3] == c.color:
            out[-1][0] += ch
        else:
            out.append([ch, c.font, c.size, c.color])
    while out and not out[-1][0].strip():
        out.pop()
    return out


def _line_width(L, sc):
    segs = _segments(L)
    if segs:
        segs[0][0] = segs[0][0].lstrip()
    return sum(font(ttf(f)).text_length(t, sz * sc) for t, f, sz, _ in segs)


def reset_line(ed, L, y, sc, align):
    """L set again on baseline y at sc of its size (left lines keep their start, right ones their end)"""
    segs = _segments(L)
    if not segs:
        return
    segs[0][0] = segs[0][0].lstrip()
    ed.drop(L.chars)
    w = sum(font(ttf(f)).text_length(t, sz * sc) for t, f, sz, _ in segs)
    x = 0.0 if align == "left" else (L.bbox.x1 - L.O.x) - w
    dy = -(y - L.O.y)
    for t, f, sz, col in segs:
        x = ed.put_text(L, x, t, f, sz * sc, color=col, dy=dy)


def write_items(ed, M, items, x, dy, sc=1.0):
    """the new line's text pieces in their fonts on M's frame, x along and dy up (negative = below)"""
    cx = x
    for t, f in items:
        if t:
            cx = ed.put_text(M, cx, t, f, M.size * sc, color=M.color, dy=dy)
