"""Inch values on a cleaned catalogue page (English only, US t/ft lines in): every dimension number on the drawings, the
scale grids, the tool data lines, the piece counts of the segmentation sets and the length / weight boxes.

  dimension 835 on a slanted isometric bar    → 32.87″ under it, along the same baseline and with the same slant
  '1 X 200' piece labels                      → '7.87″' under the length
  'H = 66.65'                                 → 'H = 66.65 (2.624″)'
  length / weight box (835 mm | 9.9 kg …)     → a twin box beside it in inches and pounds, with the same SECTIONED /
                                                 HORN tags; where no twin fits, both units inside each cell
  dimensions drawn as outlines (no text)      → read with Tesseract (ocrnums.py) and annotated the same way

Placement (placer.py): the value goes where it is free and reads as its number's — nearer to it than to any other
number — after it on the same line, or stacked above / below, at a smaller size when space is short, over light shading or
across a thin line (with a white patch) as a last resort.
"""
import io
import re

import fitz
import pdfplumber
from shapely.geometry import Polygon

import placer as PL
import textmodel as TM
from fonts import ttf, font

NUM_RE = re.compile(r"^(R\s?|Ø\s?|ø\s?)?(\d{1,4}(?:\.\d{1,3})?)$")
SPEC_RE = re.compile(r"^(H|R|V|B|L|S|v)\s*=\s*(\d+(?:\.\d+)?)$")
LEN_RE = re.compile(r"^(\d{2,4})\s*mm$", re.I)
LENGTH_CODES = {"1000", "1050", "1100", "1250", "1275", "1300", "2050", "2550", "3050", "3200", "4000", "4050"}  # codes that are also lengths
COUNT_RE = re.compile(r"^(\d{1,2})\s*[x×]\s*(\d{2,4})(?:\s*mm)?$", re.I)     # '2x150': two pieces of 150 mm
KG_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*kg$", re.I)
BOTH_RE = re.compile(r"^(\d{2,4})\s*mm\s+(\d+(?:\.\d+)?)\s*kg$", re.I)
TAG_RE = re.compile(r"^(SECTIONED|HORN|SHORT SECTIONED)$")
MMV_RE = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)\s?mm$")
BLACK = 0x231F20


def number_rows(dims):
    """runs of plain numbers set one after the other on a common baseline, close together: [[(run, value, prefix)]]"""
    n = len(dims)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    tight = []
    for i in range(n):
        a = dims[i][0]
        for j in range(i + 1, n):
            b = dims[j][0]
            if a.u[0] * b.u[0] + a.u[1] * b.u[1] < 0.995 or abs(a.size / b.size - 1) > 0.15:
                continue
            # b's baseline offset from a's, across the line
            dx, dy = b.origin.x - a.origin.x, b.origin.y - a.origin.y
            across = abs(dx * -a.u[1] + dy * a.u[0])
            if across > 0.3 * a.size:
                continue
            along = dx * a.u[0] + dy * a.u[1]
            gap = along - a.adv if along > 0 else -along - b.adv
            if gap < 2.0 * a.size:
                parent[find(i)] = find(j)
                if gap < 0.6 * a.size:
                    tight.append(i)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    tight_roots = {find(i) for i in tight}
    out = []
    for root, idx in groups.items():
        if len(idx) >= 3 or (len(idx) == 2 and root in tight_roots):
            g = [dims[i] for i in idx]
            r0 = g[0][0]
            g.sort(key=lambda d: r0.along(d[0].origin))
            out.append(g)
    return out


def is_blue(c):
    r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
    return b >= 100 and b - r >= 60 and b >= g and r + g + b < 450


def is_grey(c):
    r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
    return abs(r - g) < 16 and abs(g - b) < 16 and 70 <= r <= 175


def inch(mm, places=None):
    return PL.inch(mm, places)


def one_page_plumber(page):
    tmp = fitz.open()
    tmp.insert_pdf(page.parent, from_page=page.number, to_page=page.number)
    return pdfplumber.open(io.BytesIO(tmp.tobytes())).pages[0]


# ------------------------------------------------------------------------------------------------------------- boxes
def cells(runs):
    """the length / weight boxes' cells: [{'mm', 'kg', 'L' (run), 'K' (run or None), 'T' (tag run or None)}]"""
    lens, kgs, tags = [], [], []
    for r in runs:
        if not r.upright or r.size > 10:
            continue
        t = re.sub(r"\s+", " ", r.t)
        if BOTH_RE.match(t) or LEN_RE.match(t) or COUNT_RE.match(t):
            lens.append(r)
        elif KG_RE.match(t):
            kgs.append(r)
        elif TAG_RE.match(t) and r.size <= 6.5:
            tags.append(r)
    rows = []
    for L in lens:
        t = re.sub(r"\s+", " ", L.t)
        Ts = [x for x in tags if -1.0 <= x.bbox.y0 - L.bbox.y1 < 5.5 and abs(x.bbox.x0 - L.bbox.x0) < 9]
        T = Ts[0] if Ts else None
        m = BOTH_RE.match(t)
        if m:
            rows.append({"mm": int(m.group(1)), "kg": float(m.group(2)), "L": L, "K": None, "T": T})
            continue
        # the weight in the same row: level with the length, or centred on length + tag
        cy = L.origin.y
        lo, hi = L.bbox.y0 - 2.5, (T.bbox.y1 if T else L.bbox.y1) + 3.0
        cand = [K for K in kgs if -2 < K.bbox.x0 - L.bbox.x1 < 48 and lo < (K.bbox.y0 + K.bbox.y1) / 2 < hi]
        K = min(cand, key=lambda K: abs(K.origin.y - cy)) if cand else None
        mc = COUNT_RE.match(t)
        rows.append({"mm": int(mc.group(2) if mc else LEN_RE.match(t).group(1)), "n": int(mc.group(1)) if mc else None,
                     "kg": float(KG_RE.match(re.sub(r"\s+", " ", K.t)).group(1)) if K else None,
                     "L": L, "K": K, "T": T})
    rows.sort(key=lambda r: (round(r["L"].bbox.x0), r["L"].bbox.y0))
    boxes = []
    for r in rows:
        for b in boxes:
            last = b["rows"][-1]
            if abs(last["L"].bbox.x0 - r["L"].bbox.x0) < 4 and 0 < r["L"].bbox.y0 - last["L"].bbox.y0 < 26:
                b["rows"].append(r)
                break
        else:
            boxes.append({"rows": [r]})
    return boxes


def box_lines(drawings, rect):
    hs, vs, col, wid = [], [], None, 0.5
    big = fitz.Rect(rect.x0 - 12, rect.y0 - 9, rect.x1 + 12, rect.y1 + 12)
    for d in drawings:
        if not d.get("color") or "s" not in (d.get("type") or ""):
            continue
        for it in d["items"]:
            if it[0] == "l":
                p, q = it[1], it[2]
                if not (big.contains(p) and big.contains(q)):
                    continue
                if abs(p.y - q.y) < 0.3 and abs(p.x - q.x) > 8:
                    hs.append((p.y, min(p.x, q.x), max(p.x, q.x)))
                elif abs(p.x - q.x) < 0.3 and abs(p.y - q.y) > 4:
                    vs.append((p.x, min(p.y, q.y), max(p.y, q.y)))
                else:
                    continue
                col, wid = d["color"], d.get("width") or 0.5
            elif it[0] == "re":
                R = it[1]
                if not big.contains(R) or R.width < 8:
                    continue
                hs += [(R.y0, R.x0, R.x1), (R.y1, R.x0, R.x1)]
                vs += [(R.x0, R.y0, R.y1), (R.x1, R.y0, R.y1)]
                col, wid = d["color"], d.get("width") or 0.5
    return col, wid, hs, vs


def box_geometry(drawings, b):
    rows = b["rows"]
    tight = fitz.Rect(min(r["L"].bbox.x0 for r in rows), min(r["L"].bbox.y0 for r in rows),
                      max((r["K"] or r["L"]).bbox.x1 for r in rows), max((r["T"] or r["L"]).bbox.y1 for r in rows))
    col, wid, hs, vs = box_lines(drawings, tight)
    lefts = [v[0] for v in vs if v[0] <= tight.x0 + 2]
    rights = [v[0] for v in vs if v[0] >= tight.x1 - 2]
    X0 = max(lefts) if lefts else tight.x0 - 4
    X0 = min([v for v in lefts if v > tight.x0 - 12] or [X0])
    X1 = min([v for v in rights if v < tight.x1 + 14] or [tight.x1 + 4])
    Y0 = min([h[0] for h in hs if h[0] < tight.y0 + 1 and h[0] > tight.y0 - 9] + [tight.y0 - 2])
    Y1 = max([h[0] for h in hs if h[0] > tight.y1 - 1 and h[0] < tight.y1 + 9] + [tight.y1 + 3])
    full = sorted(set(round(h[0], 2) for h in hs if h[2] - h[1] > 0.6 * (X1 - X0) and Y0 - 0.5 <= h[0] <= Y1 + 0.5))
    mids = sorted(v[0] for v in vs if X0 + 3 < v[0] < X1 - 3)
    gaps = []
    outer = sorted((v[1], v[2]) for v in vs if abs(v[0] - X0) < 1.5)
    for (a1, b1), (a2, b2) in zip(outer, outer[1:]):
        if a2 - b1 > 1.5:
            gaps.append((b1, a2))
    return {"X0": X0, "X1": X1, "Y0": Y0, "Y1": Y1, "full": full, "mid": mids[0] if mids else None, "gaps": gaps,
            "col": col or (0.584, 0.661, 0.795), "wid": wid}


def lb_text(kg):
    return PL.lb_text(kg)


def rect_poly(R):
    return Polygon([(R.x0, R.y0), (R.x1, R.y0), (R.x1, R.y1), (R.x0, R.y1)])


def twin_plan(cv, geo, b, dry_taken):
    rows = b["rows"]
    X0, X1, Y0, Y1 = geo["X0"], geo["X1"], geo["Y0"], geo["Y1"]
    fs0 = rows[0]["L"].size
    LF = font(ttf("Roboto-Light"))
    ins = [(f"{r['n']} × " if r.get("n") else "") + inch(r["mm"], 2) for r in rows]
    lbs = [lb_text(r["kg"]) if r["kg"] is not None else "" for r in rows]
    H = Y1 - Y0
    for f in (fs0, fs0 * 0.9, fs0 * 0.82, fs0 * 0.75):
        pad = 0.44 * f
        wi = max(LF.text_length(t, f) for t in ins) + 2 * pad
        tagw = max([LF.text_length(r["T"].t, r["T"].size) + 2 * pad for r in rows if r["T"]] or [0])
        wi = max(wi, tagw)
        wl = (max(LF.text_length(t, f) for t in lbs if t) + 2 * pad) if any(lbs) else 0
        W = wi + wl
        # beside it on the right reads best (row for row), then under it, then on the left, then over it
        Wb = max(W, X1 - X0)
        spots = [("right", fitz.Rect(X1, Y0, X1 + W, Y1))]
        for g in (3, 6):
            spots += [("below", fitz.Rect(X0, Y1 + g, X0 + Wb, Y1 + g + H)), ("below", fitz.Rect(X1 - Wb, Y1 + g, X1, Y1 + g + H))]
        spots.append(("left", fitz.Rect(X0 - W, Y0, X0, Y1)))
        for g in (3, 6):
            spots += [("above", fitz.Rect(X0, Y0 - g - H, X0 + Wb, Y0 - g)), ("above", fitz.Rect(X1 - Wb, Y0 - g - H, X1, Y0 - g))]
        for spot, R in spots:
            test = fitz.Rect(R.x0 + (1.8 if spot == "right" else 0), R.y0 + (1.2 if spot in ("right", "left") else 0),
                             R.x1 - (1.8 if spot == "left" else 0), R.y1 - (1.2 if spot in ("right", "left") else 0))
            poly = rect_poly(test)
            if cv.free(poly, "clean", margin=7) and not any(poly.intersects(t) for t in dry_taken):
                dry_taken.append(rect_poly(R).buffer(1.0))
                return {"spot": spot, "R": R, "f": f, "pad": pad, "wi": wi if spot in ("right", "left") else R.width * wi / W,
                        "wl": wl, "ins": ins, "lbs": lbs, "dy": R.y0 - Y0}
    return None


def twin_draw(cv, geo, b, plan):
    page = cv.page
    R, dy, f, pad = plan["R"], plan["dy"], plan["f"], plan["pad"]
    col, wid = geo["col"], geo["wid"]
    sh = page.new_shape()
    sh.draw_rect(R)
    sh.finish(color=col, fill=(1, 1, 1), width=wid)
    for y in geo["full"]:
        if R.y0 + 0.5 < y + dy < R.y1 - 0.5:
            sh.draw_line(fitz.Point(R.x0, y + dy), fitz.Point(R.x1, y + dy))
    if plan["wl"]:
        sh.draw_line(fitz.Point(R.x0 + plan["wi"], R.y0), fitz.Point(R.x0 + plan["wi"], R.y1))
    sh.finish(color=col, width=wid)
    for g0, g1 in geo["gaps"]:
        sh.draw_rect(fitz.Rect(R.x0 - 0.4, g0 + dy + 0.35, R.x1 + 0.4, g1 + dy - 0.35))
        sh.finish(color=None, fill=(1, 1, 1), width=0)
    sh.commit()
    LF = font(ttf("Roboto-Light"))
    for r, ti, tl in zip(b["rows"], plan["ins"], plan["lbs"]):
        PL.put_text(page, fitz.Point(R.x0 + pad, r["L"].origin.y + dy), (1, 0), (0, -1), ti, f, "light", PL.rgb(BLACK))
        if r["T"] is not None:
            T = r["T"]
            PL.put_text(page, fitz.Point(R.x0 + pad, T.origin.y + dy), (1, 0), (0, -1), T.t, T.size, "light", PL.rgb(T.color))
        if tl:
            yk = (r["K"].origin.y if r["K"] else r["L"].origin.y) + dy
            PL.put_text(page, fitz.Point(R.x1 - pad - LF.text_length(tl, f), yk), (1, 0), (0, -1), tl, f, "light", PL.rgb(BLACK))
    cv.take_rect(R, pad=1.0)


def free_below(cv, geo, limit=40.0):
    """clean paper under a box, in pt"""
    X0, X1, Y1 = geo["X0"], geo["X1"], geo["Y1"]
    g = 0.0
    while g < limit:
        R = fitz.Rect(X0 - 0.4, Y1 + PL.PAD + 0.7, X1 + 0.4, Y1 + PL.PAD + 0.7 + g + 0.5)
        if not cv.free(rect_poly(R), "clean", margin=7):
            break
        g += 0.5
    return g


def tag_lines(txt, size0, fs, room, LF):
    """a tag ('SECTIONED', 'SHORT SECTIONED') for the left cell: (size, [lines]) — on one line at up to its own size,
    smaller if need be, else on two"""
    ft = min(size0, max(4.0, 0.74 * fs))
    for f in (ft, ft * 0.93, 3.9):
        if LF.text_length(txt, f) <= room:
            return f, [txt]
    words = txt.split()
    if len(words) > 1:
        for f in (ft, 3.9):
            lines = [" ".join(words[:-1]), words[-1]]
            if all(LF.text_length(t, f) <= room for t in lines):
                return f, lines
    return 3.6, [txt]


def dual_rows(rows, bounds, fs, room, LF):
    """the height each row needs with both units in its cells, and its tag lines"""
    out = []
    for r, (top, bot) in zip(rows, bounds):
        need = 2.06 * fs + 1.6
        tl = None
        if r["T"] is not None:
            ft, lines = tag_lines(r["T"].t, r["T"].size, fs, room, LF)
            tl = (ft, lines)
            need += 0.24 * fs + len(lines) * 1.04 * ft
        out.append((need, tl))
    return out


def dual_plan(cv, geo, b):
    """both units inside each cell — '835 mm' over '32.87″', '9.9 kg' over '21.8 lb', the tag under them — at the
    largest size the box holds, the box growing downwards into clean paper where the rows need it"""
    rows = b["rows"]
    X0, X1, ys = geo["X0"], geo["X1"], geo["full"]
    mid = geo["mid"] if geo["mid"] is not None else (X0 + X1) / 2
    LF = font(ttf("Roboto-Light"))
    bounds = []
    for r in rows:
        cy = r["L"].origin.y - 0.35 * r["L"].size
        top = max([y for y in ys if y <= cy + 0.5] or [r["L"].bbox.y0 - 2])
        bot = min([y for y in ys if y > cy + 0.5] or [(r["T"] or r["L"]).bbox.y1 + 3])
        bounds.append((top, bot))
    heights = [bot - top for top, bot in bounds]
    tiled = bool(ys) and all(abs(bounds[k][1] - bounds[k + 1][0]) < 0.6 for k in range(len(bounds) - 1)) \
        and abs(bounds[0][0] - ys[0]) < 0.6 and abs(bounds[-1][1] - ys[-1]) < 0.6
    room = mid - X0 - 3.0
    spare = free_below(cv, geo) if tiled else 0.0
    fs0 = rows[0]["L"].size
    best = None
    fs = min(6.2, 0.8 * fs0)
    while fs >= 4.6 - 1e-6:
        lay = dual_rows(rows, bounds, fs, room, LF)
        grow = sum(max(0.0, need - h) for (need, _), h in zip(lay, heights))
        if grow <= 0.05 or (tiled and grow <= spare - 1.0):
            best = (fs, lay, grow)
            break
        fs -= 0.2
    if best is None:
        fs = 4.6
        best = (fs, dual_rows(rows, bounds, fs, room, LF), 0.0)
    fs, lay, grow = best
    if grow > 0.05:
        new_h = [max(h, need) for (need, _), h in zip(lay, heights)]
        y, nb = geo["Y0"], []
        for h in new_h:
            nb.append((y, y + h))
            y += h
        bounds = nb
    return {"fs": fs, "lay": lay, "bounds": bounds, "grow": grow, "mid": mid}


def dual_texts(geo, b, plan):
    """[(origin, text, size)] for the cells"""
    rows = b["rows"]
    X0, X1 = geo["X0"], geo["X1"]
    fs = plan["fs"]
    LF = font(ttf("Roboto-Light"))
    padl = min(4.0, max(1.6, rows[0]["L"].bbox.x0 - X0))
    padr = 2.2
    out = []
    for r, (top, bot), (need, tl) in zip(rows, plan["bounds"], plan["lay"]):
        h = bot - top
        block = 2.06 * fs + ((0.24 * fs + len(tl[1]) * 1.04 * tl[0]) if tl else 0.0)
        y0 = top + (h - block) / 2
        b1 = y0 + 0.76 * fs
        b2 = b1 + 1.08 * fs
        cnt = f"{r['n']} × " if r.get("n") else ""
        out.append((fitz.Point(X0 + padl, b1), f"{cnt}{r['mm']} mm", fs))
        out.append((fitz.Point(X0 + padl, b2), cnt + inch(r["mm"], 2), fs))
        if tl:
            ft, lines = tl
            yb = b2 + 0.22 * fs + 0.78 * ft
            for t in lines:
                out.append((fitz.Point(X0 + padl, yb), t, ft))
                yb += 1.04 * ft
        if r["kg"] is not None:
            kg_txt = (f"{r['kg']:.1f}" if r["kg"] < 100 else f"{r['kg']:.0f}") + " kg"
            for y, t in ((b1, kg_txt), (b2, lb_text(r["kg"]))):
                out.append((fitz.Point(X1 - padr - LF.text_length(t, fs), y), t, fs))
    return out


def rebuild_box(page, geo, bounds, mid):
    """the box's rules taken out and drawn again round the new rows (white ground, same colour and width)"""
    import specblock as SB
    X0, X1, Y0, Y1 = geo["X0"], geo["X1"], geo["Y0"], geo["Y1"]
    before = page.get_drawings()
    G = fitz.Rect(X0 - 0.8, Y0 - 0.8, X1 + 0.8, Y1 + 0.8)
    page.add_redact_annot(fitz.Rect(X0 - 3, Y0 - 3, X1 + 3, Y1 + 3), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                          text=fitz.PDF_REDACT_TEXT_NONE)
    left = {}
    for d in page.get_drawings():
        s = SB._sig(d)
        left[s] = left.get(s, 0) + 1
    for d in before:
        s = SB._sig(d)
        if left.get(s, 0) > 0:
            left[s] -= 1
        elif not SB._within(G, d["rect"]):
            SB._redraw(page, d, 0.0)                     # not the box's: back where it was
    top, bot = bounds[0][0], bounds[-1][1]
    col, wid = geo["col"], geo["wid"]
    sh = page.new_shape()
    sh.draw_rect(fitz.Rect(X0, top, X1, bot))
    sh.finish(color=col, fill=(1, 1, 1), width=wid)
    for (a, b_) in bounds[:-1]:
        sh.draw_line(fitz.Point(X0, b_), fitz.Point(X1, b_))
    sh.draw_line(fitz.Point(mid, top), fitz.Point(mid, bot))
    sh.finish(color=col, width=wid)
    sh.commit()
    return fitz.Rect(X0, top, X1, bot)


# ------------------------------------------------------------------------------------------------------------- page
def piece_labels(runs):
    """'N / X / L' stacked in the small tool pictures of the segmentation pages → {id(L run): (N, L)}"""
    xs = [r for r in runs if r.t in ("X", "x") and r.upright]
    out = {}
    for x in xs:
        cx = (x.bbox.x0 + x.bbox.x1) / 2
        above = [r for r in runs if r is not x and re.fullmatch(r"\d{1,2}", r.t) and abs((r.bbox.x0 + r.bbox.x1) / 2 - cx) < 4
                 and 0 <= x.bbox.y0 - r.bbox.y1 < 5]
        below = [r for r in runs if r is not x and re.fullmatch(r"\d{2,4}", r.t) and abs((r.bbox.x0 + r.bbox.x1) / 2 - cx) < 8
                 and 0 <= r.bbox.y0 - x.bbox.y1 < 5]
        if above and below:
            out[id(below[0])] = (int(above[0].t), int(below[0].t), above[0], x)
    return out


def annotate_page(page, codes=frozenset(), skip_rects=(), ocr=False, report=None, box_mode="auto", reserve=()):
    """add the inch values; returns counts.  `reserve`: areas where text will be set later (no inch value goes there)"""
    rep = report if report is not None else []
    pno = page.number + 1
    pp = one_page_plumber(page)
    runs = TM.runs(page, pp)
    cv = PL.Canvas(page, runs)
    for r in reserve:
        cv.take_rect(fitz.Rect(r), pad=1.0)
    polys = {id(r): r.outline() for r in runs}
    n = {"dim": 0, "spec": 0, "box": 0, "piece": 0, "ocr": 0}

    def others(r):
        return [polys[id(o)] for o in runs if o is not r]

    def skipped(r):
        return any(fitz.Rect(s).contains(r.origin) for s in skip_rects)

    # 1 · tool data lines: 'H = 66.65' → '(2.624″)' after it
    for r in runs:
        t = re.sub(r"\s+", " ", r.t)
        m = SPEC_RE.match(t)
        if not m or not r.upright or skipped(r) or is_blue(r.color):
            continue
        v = float(m.group(2))
        if not v:
            continue
        txt = f"({v / 25.4:.3f}″)" if v >= 25.4 else f"({inch(v)})"
        dig = next((k for k, c in enumerate(r.chars) if c[0].isdigit()), 0)
        r.num_x = r.along(r.chars[dig][1])
        res = PL.place(cv, r, txt, others(r), order=["after", "after>"], weight="light",
                       stages=[("clean", 0.82), ("clean", 0.7), ("light", 0.7), ("clean", 0.6), ("knock", 0.7),
                               ("knock", 0.6)], color=BLACK)
        if not res:                                     # last resort: under the value
            res = PL.place(cv, r, txt, others(r), order=["below-v"], weight="light",
                           stages=[("clean", 0.7), ("clean", 0.6), ("light", 0.6)], color=BLACK)
        if res:
            n["spec"] += 1
        else:
            rep.append((pno, "spec", r.t))
    # 2 · the length / weight boxes
    bxs = [b for b in cells(runs) if not any(skipped(r["L"]) for r in b["rows"])]
    drawings = page.get_drawings()
    geos = [box_geometry(drawings, b) for b in bxs]
    plans = None
    if bxs and box_mode in ("auto", "twin"):
        taken = []
        plans = [twin_plan(cv, g, b, taken) for g, b in zip(geos, bxs)]
        if box_mode == "auto" and not all(plans):
            plans = None
    box_runs = set()
    for b in bxs:
        for r in b["rows"]:
            for x in (r["L"], r["K"], r["T"]):
                if x is not None:
                    box_runs.add(id(x))
    if plans:
        for g, b, pl in zip(geos, bxs, plans):
            twin_draw(cv, g, b, pl)
            n["box"] += 1
    elif bxs:
        dplans = [dual_plan(cv, g, b) for g, b in zip(geos, bxs)]
        for b in bxs:
            for r in b["rows"]:
                for x in (r["L"], r["K"], r["T"]):
                    if x is not None:
                        page.add_redact_annot(fitz.Rect(x.bbox.x0 + 0.15, x.bbox.y0 + 0.6, x.bbox.x1 - 0.15, x.bbox.y1 - 0.6),
                                              fill=False)
        page.apply_redactions(images=0, graphics=0, text=0)
        for g, b, dp in zip(geos, bxs, dplans):
            if dp["grow"] > 0.05:
                R = rebuild_box(page, g, dp["bounds"], dp["mid"])
                cv.take_rect(R, pad=0.8)
                rep.append((pno, "box-grown", f"{b['rows'][0]['mm']} mm +{dp['grow']:.1f}pt @{dp['fs']:.1f}"))
            for o, t, fs in dual_texts(g, b, dp):
                PL.put_text(page, o, (1, 0), (0, -1), t, fs, "light", PL.rgb(BLACK))
            if dp["fs"] < 5.2:
                rep.append((pno, "box-small", f"{b['rows'][0]['mm']} mm @{dp['fs']:.1f}"))
        n["box"] += len(bxs)
    # 3 · piece labels of the segmentation pictures: the length gets its inch value under it
    pieces = piece_labels(runs)
    for r in runs:
        if id(r) not in pieces or skipped(r):
            continue
        cnt, mm, a, x = pieces[id(r)]
        res = PL.place(cv, r, (f"({inch(mm, 2)})", inch(mm, 2)), others(r), order=["below", "below-far", "after", "before"],
                       weight="reg", stages=[("clean", 0.88), ("clean", 0.75), ("light", 0.75), ("clean", 0.62),
                                             ("light", 0.62), ("knock", 0.62), ("clean", 0.52), ("light", 0.52),
                                             ("knock", 0.52), ("clean", 0.44)])
        if res:
            n["piece"] += 1
        else:
            rep.append((pno, "piece", r.t))
    piece_ids = set(pieces) | {id(v[2]) for v in pieces.values()} | {id(v[3]) for v in pieces.values()}
    # 4 · dimensions and grid marks
    dims = []
    for r in runs:
        if id(r) in box_runs or id(r) in piece_ids or skipped(r):
            continue
        m = NUM_RE.match(r.t)
        if not m or r.size >= 17 or r.weight == "bold" or r.color == 0xFFFFFF:
            continue
        if r.origin.y > page.rect.height - 50 and r.size >= 15:
            continue                                     # the page number
        v = float(m.group(2))
        if v == 0:
            continue
        if v >= 1000 and not is_blue(r.color):
            continue                                     # black 4-digit numbers are tool codes; blue ones are lengths
        if v >= 1000 and not m.group(1) and r.t in codes and r.t not in LENGTH_CODES:
            continue                                     # a blue tool code in a call-out ('4389' on the EUROGRIP drawings)
        dims.append((r, v, m.group(1)))
    # rows of numbers set close together (the piece lengths of the segmentation diagrams) are laid out as a row: every
    # value under its own number at one size
    done_ids = set()
    row_left = []
    for row in number_rows([d for d in dims if not d[2]]):
        texts = [inch(v) for r, v, pre in row]
        res = PL.place_row(cv, [d[0] for d in row], texts)
        for (r, v, pre), x in zip(row, res):
            if x:
                done_ids.add(id(r))
                n["dim"] += 1
            else:
                row_left.append(id(r))
    dims = [d for d in dims if id(d[0]) not in done_ids]
    for r, v, pre in [d for d in dims if id(d[0]) in row_left]:
        # a row member whose place under (or over) the row was taken: still under or over its own number
        res = PL.place(cv, r, (f"({inch(v)})", inch(v)), others(r), order=["below", "above", "below-far"])
        if res:
            done_ids.add(id(r))
            n["dim"] += 1
    dims = [d for d in dims if id(d[0]) not in done_ids]

    # crowded numbers first: they have the fewest spots
    def crowd(d):
        r = d[0]
        c = r.outline().centroid
        return -sum(1 for o in dims if o[0] is not r and polys[id(o[0])].centroid.distance(c) < 3.2 * r.size)
    for r, v, pre in sorted(dims, key=lambda d: (crowd(d), -len(d[0].t))):
        stacked = (pre.strip() + " " if pre else "") + inch(v)
        inline = f"({inch(v)})"
        res = PL.place(cv, r, (inline, stacked), others(r))
        if not res:                                       # a number on a tool body, its dimension line just under it:
            res = PL.place(cv, r, (inline, stacked), others(r), order=["below-far"])     # a little lower down
        if not res:                                       # last: on a small white patch over the grid or the tool body
            res = PL.place(cv, r, (inline, stacked), others(r), order=["below", "above", "after", "before", "below-far"],
                           stages=[("force", 0.62), ("force", 0.52), ("force", 0.44)])
        if res:
            n["dim"] += 1
        else:
            rep.append((pno, "dim", r.t))
    # 4b · millimetre values in tables and notes: '0.5 mm' → '0.5 mm (.020″)'
    for r in runs:
        if id(r) in box_runs or skipped(r) or "″" in r.t or is_blue(r.color) and r.size > 12:
            continue
        m = MMV_RE.search(re.sub(r"\s+", " ", r.t))
        if not m or (r.chars and not r.upright):
            continue
        v = float(m.group(1))
        if not v:
            continue
        res = PL.place(cv, r, f"({inch(v)})", others(r), order=["after", "after>"],
                       weight="light" if r.weight == "light" else "reg",
                       stages=[("clean", 0.85), ("clean", 0.72), ("light", 0.72), ("clean", 0.6)])
        if res:
            n["dim"] += 1
        else:
            rep.append((pno, "mm", r.t))
    # 5 · dimensions drawn as outlines (vector glyphs): read with Tesseract, annotated the same way
    if ocr:
        import glyphnums
        fakes = []
        for f in glyphnums.found(page):
            fake = FakeRun(f)
            if any(polys[id(o)].intersects(fake.outline()) for o in runs) or skipped(fake):
                continue                                     # real text already there, or a page handler's area
            fakes.append(fake)
        allp = list(polys.values()) + [fk.outline() for fk in fakes]
        for fake in fakes:
            v = fake.value
            stacked = (fake.prefix.strip() + " " if fake.prefix else "") + inch(v)
            own = fake.outline()
            res = PL.place(cv, fake, (f"({inch(v)})", stacked), [p for p in allp if p is not own and not p.equals(own)])
            if res:
                n["ocr"] += 1
            else:
                rep.append((pno, "ocr", fake.t))
    return n


class FakeRun:
    """a number read from the drawing (glyphnums.found), shaped like textmodel.Run for the placer"""

    def __init__(self, f):
        self.t = f["text"]
        self.value = f["value"]
        self.prefix = f.get("prefix", "")
        self.size = f["size"]
        self.u, self.v = tuple(f["u"]), tuple(f["v"])
        self.weight, self.italic = "reg", False
        self.color = f.get("color", 0x2E6EB5)
        self.origin = fitz.Point(f["origin"])
        self.adv = f["adv"]
        self.bbox = f["rect"]
        self.chars = []

    def along(self, p):
        return (p[0] - self.origin.x) * self.u[0] + (p[1] - self.origin.y) * self.u[1]

    def point(self, x, y, size=None):
        s = self.size if size is None else size
        return fitz.Point(self.origin.x + x * self.u[0] + y * s * self.v[0], self.origin.y + x * self.u[1] + y * s * self.v[1])

    @property
    def upright(self):
        return abs(self.u[0] - 1) < 0.01

    @property
    def vertical(self):
        return abs(self.u[1] + 1) < 0.01

    def outline(self, lo=None, hi=None):
        lo = -0.03 if lo is None else lo
        hi = 0.74 if hi is None else hi
        pts = [self.point(0, lo), self.point(self.adv, lo), self.point(self.adv, hi), self.point(0, hi)]
        return Polygon([(p.x, p.y) for p in pts])
