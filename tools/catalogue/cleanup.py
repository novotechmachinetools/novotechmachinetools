"""English only: the Italian taken out of EUROSTAMP's bilingual (IT / EN) catalogue pages.

  'PUNZONI - 88° / PUNCHES - 88°'  one line, two languages     → the English part stays, moved to where the line began
                                                                   (or kept at its end when the line is right-aligned)
  'TEMPRATO AD INDUZIONE'           Italian line, English line   → the English moves up into the Italian line's place
  'INDUCTION HARDENED'               under it                       (centred in the bar for two-line header bars)
  'SEZIONATO', 'PESO FINO A …'      Italian with no English      → set again in English (translations in it_en.py)
  'FRAZ. / SECT.', 'SCARP. / HORN'  the length-box tags          → 'SECTIONED', 'HORN'; 'SECT. SHORT' → 'SHORT SECTIONED'
  '9,9 kg', '66,4'                  decimal commas               → decimal points

Pages whose Italian is running text (the introduction, the ESH and EUROGRIP pages …) are set again from English copy
written for NovoTech (pages.py); this module handles the rest line by line and reports what it could not place.
"""
import re

import fitz

from lang import text_lang, word_lang
from textedit import Editor, page_lines, SEP_RE
import it_en

TAGS = [(re.compile(r"^FRAZ\.?\s*/\s*S(?:E?C)?T\.?$|^FRAZ\.?\s*/\s*SET\.?$"), "SECTIONED"),
        (re.compile(r"^SCARP\.?\s*/\s*HORN$"), "HORN"),
        (re.compile(r"^SECT\.\s*SHORT$"), "SHORT SECTIONED"),
        (re.compile(r"^SEZ\s?IONATO$|^SEZ ONATO$"), "SECTIONED")]
DEC_RE = re.compile(r"(?<=\d),(?=\d)")


def is_italic(font):
    return "Italic" in font or "Oblique" in font


def part_lang(txt):
    lg = text_lang(txt)
    if lg == "mixed":
        words = re.findall(r"[A-Za-zÀ-ÿ’']+", txt)
        its = sum(1 for w in words if word_lang(w) == "it")
        ens = sum(1 for w in words if word_lang(w) == "en")
        lg = "it" if its > ens else "en"
    return lg


# -------------------------------------------------------------------------------------------------------- geometry
def filled_rects(page):
    """non-white filled rectangles (header bars, table cells)"""
    out = []
    for d in page.get_drawings():
        f = d.get("fill")
        if not f or min(f[:3]) > 0.93:
            continue
        r = d["rect"]
        if r.width > 20 and r.height > 6:
            out.append((fitz.Rect(r), tuple(f[:3])))
    return out


def container(rects, bbox):
    best = None
    for r, f in rects:
        if r.contains(fitz.Rect(bbox.x0 + 0.5, bbox.y0 + 0.5, bbox.x1 - 0.5, bbox.y1 - 0.5)):
            if best is None or r.get_area() < best[0].get_area():
                best = (r, f)
    return best


def alignment(line, rects, lines):
    """'left', 'right' or 'center' for a one-line label"""
    c = container(rects, line.bbox)
    if c:
        r = c[0]
        lg, rg = line.bbox.x0 - r.x0, r.x1 - line.bbox.x1
        if abs(lg - rg) < 2.5:
            return "center"
        return "right" if rg < lg else "left"
    # aligned with other lines of the same block?
    same = [L for L in lines if L is not line and L.block == line.block and abs(L.size - line.size) < 2]
    if same:
        if any(abs(L.bbox.x0 - line.bbox.x0) < 1.5 for L in same):
            return "left"
        if any(abs(L.bbox.x1 - line.bbox.x1) < 1.5 for L in same):
            return "right"
        if any(abs((L.bbox.x0 + L.bbox.x1) / 2 - (line.bbox.x0 + line.bbox.x1) / 2) < 1.5 for L in same):
            return "center"
    return "left"


def width_of(chars):
    ink = [c for c in chars if c.c.strip()]
    if not ink:
        return 0.0
    ln = ink[0].line
    return ln.coords(ink[-1].o)[0] + ink[-1].adv() - ln.coords(ink[0].o)[0]


# -------------------------------------------------------------------------------------------------------- partners
def below_partner(it, lines, used):
    """the English line set right under the Italian one (same direction, size and alignment)"""
    best, bd = None, 1e9
    for L in lines:
        if L is it or L.removed or id(L) in used:
            continue
        if abs(L.u[0] - it.u[0]) > 0.02 or abs(L.u[1] - it.u[1]) > 0.02:
            continue
        if not (0.7 < L.size / it.size < 1.35):
            continue
        x, y = it.coords(L.O)
        if not (-2.6 * it.size < y < -0.75 * it.size):        # baseline 0.75 – 2.6 sizes under it
            continue
        al = (abs(x) < 3.5 or abs(it.end - (x + width_of(L.chars))) < 3.5 or
              abs((it.end) / 2 - (x + width_of(L.chars) / 2)) < 3.5)
        if not al:
            continue
        lg = part_lang(L.t)
        if lg == "it":
            continue
        if lg is None and not is_italic(L.main_font):
            continue
        if -y < bd:
            best, bd = L, -y
    return best


def column_groups(lines):
    """{id(line): [lines of its column group]}: lines one under the other (same direction and size, left, right or
    centre aligned, baselines at most 2.6 sizes apart), chained"""
    parent = {id(L): id(L) for L in lines}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for A in lines:
        for B in lines:
            if A is B or abs(A.u[0] - B.u[0]) > 0.02 or abs(A.u[1] - B.u[1]) > 0.02:
                continue
            if not (0.7 < B.size / A.size < 1.35):
                continue
            x, y = A.coords(B.O)
            if not (-2.6 * A.size < y < -0.5 * A.size):
                continue
            wb = width_of(B.chars)
            if abs(x) < 3.5 or abs(A.end - (x + wb)) < 3.5 or abs(A.end / 2 - (x + wb / 2)) < 3.5:
                parent[find(id(A))] = find(id(B))
    out = {}
    for L in lines:
        out.setdefault(find(id(L)), []).append(L)
    return {id(L): out[find(id(L))] for L in lines}


# -------------------------------------------------------------------------------------------------------- one page
def clean_page(page, ppage=None, skip=None, report=None):
    """English only on one page.  `skip`: ids of lines a page handler already dealt with.  Returns the Editor (applied)."""
    lines = page_lines(page, ppage)
    rects = filled_rects(page)
    ed = Editor(page, lines)
    used = set(skip or ())
    pno = page.number + 1
    rep = report if report is not None else []

    english = set()                                  # lines that read English after steps 1 – 2

    def done(L):
        used.add(id(L))

    # 1 · page-specific whole-line replacements and the length-box tags
    for L in lines:
        if id(L) in used:
            continue
        new = it_en.line_for(pno, L.t)
        if new is None:
            for rx, rep_t in TAGS:
                if rx.match(L.t):
                    new = rep_t
                    break
        if new is None:
            continue
        done(L)
        if new:
            english.add(id(L))
        if new == L.t:
            continue
        al = alignment(L, rects, lines)
        # keep what the new text shares with the old at its start (its fonts stay: 'Sheet metal thickness = Max 1' …)
        ink = [c for c in L.chars if c.c.strip() or c is not L.chars[-1]]
        k = 0
        old_t = L.text.lstrip()
        lead = len(L.text) - len(old_t)
        while k < min(len(old_t), len(new)) and old_t[k] == new[k]:
            k += 1
        if new and k >= 3 and al == "left":
            while k > 0 and not old_t[k - 1].strip():
                k -= 1                                       # restart at a word, not after a space
            cut = L.chars[lead + k] if lead + k < len(L.chars) else None
            rest = L.chars[lead + k:]
            ed.drop(rest)
            ref = cut if cut is not None and cut.c.strip() else (L.chars[lead + k - 1] if lead + k > 0 else L.chars[0])
            x = L.coords(cut.o)[0] if cut is not None else L.end
            if cut is not None and not cut.c.strip() and lead + k > 0:
                x = L.coords(L.chars[lead + k - 1].o)[0] + L.chars[lead + k - 1].adv()
            ed.put_text(L, x, new[k:], ref.font, ref.size, color=ref.color)
            continue
        ed.drop(L.chars)
        if new:
            size = None
            if any(rx.match(L.t) for rx, _ in TAGS) and L.upright:
                room = cell_room(page, L)                  # a tag stays inside its cell of the length box
                from fonts import ttf, font
                w = font(ttf(L.main_font)).text_length(new, L.size)
                if room and w > room:
                    size = max(3.6, L.size * room / w)
            set_text(ed, L, new, al, size=size)
    # 2 · 'IT / EN' on one line
    for L in lines:
        if id(L) in used or not SEP_RE.search(L.text) or L.t.endswith("/"):
            continue
        parts = L.parts()
        langs = [part_lang(t) for _, t in parts]
        if "it" not in langs:
            continue
        keep = [(cs, t) for (cs, t), lg in zip(parts, langs) if lg != "it" and cs]
        if not keep or len(parts) != 2:
            rep.append((pno, "split?", L.t))
            continue
        done(L)
        english.add(id(L))
        al = alignment(L, rects, lines)
        cs = keep[0][0]
        drop = [c for c in L.chars if c not in cs]
        ed.drop(drop)
        x0 = L.coords(cs[0].o)[0]
        w = width_of(cs)
        if al == "left":
            dx = -x0
        elif al == "right":
            dx = 0.0
        else:
            dx = (L.end - w) / 2 - x0
        if abs(dx) > 0.01:
            ed.put_chars(L, cs, dx=dx)
    # 3 · whole Italian lines: dropped when English sits in the same column right under (or over) them — the English
    #     stays where it is (centred in a two-line header bar); otherwise set again in English (it_en.py)
    groups = column_groups(lines)
    for L in lines:
        if id(L) in used:
            continue
        t = L.t
        trailing = t.endswith("/")
        if part_lang(t.rstrip("/ ") if trailing else t) != "it":
            continue
        g = groups.get(id(L), [])
        en = [P for P in g if P is not L and not P.removed and (id(P) in english or (
              id(P) not in used and part_lang(P.t.rstrip("/ ")) != "it" and (part_lang(P.t) == "en" or is_italic(P.main_font))))]
        tr = it_en.translate(t)
        if en and tr is None:
            done(L)
            ed.drop_line(L)
            c = container(rects, L.bbox)
            if c and all(c[0].contains(P.bbox) for P in en) and len(en) == 1 and id(en[0]) not in used:
                P = en[0]
                done(P)
                x, y = L.coords(P.O)
                _shift(ed, P, L, 0.0, -y / 2)
                P.removed = True
            continue
        if tr is not None:
            done(L)
            ed.drop(L.chars)
            if tr:
                set_text(ed, L, tr, alignment(L, rects, lines))
            continue
        rep.append((pno, "italian", t))
    # 4 · decimal commas → points (the rest of the line moves over by the difference in width)
    for L in lines:
        if L.removed:
            continue
        ms = [m.start() for m in DEC_RE.finditer(L.text)]
        ms = [k for k in ms if L.chars[k] not in ed.gone]
        if not ms and not any(c.c in "Øø" for c in L.chars if c not in ed.gone):
            continue
        tail = [c for c in L.chars if c not in ed.gone]
        ed.put_chars(L, tail)
    for a in ed.adds:
        fix_decimals(a[3])
        fix_diameter(a[3])
    ed.apply()
    return ed


def fix_decimals(items):
    """[(x, y, ch, fontpath, size)] in reading order: a comma between digits becomes a point, what follows moves over"""
    from fonts import font
    shift = 0.0
    for i, (x, y, ch, path, size) in enumerate(items):
        if shift:
            items[i] = (x + shift, y, ch, path, size)
        if ch == "," and 0 < i < len(items) - 1 and items[i - 1][2].isdigit() and items[i + 1][2].isdigit() \
                and abs(items[i + 1][1] - y) < 0.5 and abs(items[i - 1][1] - y) < 0.5:
            fo = font(path)
            items[i] = (x + shift, y, ".", path, size)
            shift += fo.text_length(".", size) - fo.text_length(",", size)


INTER = {"light": "/usr/share/fonts/opentype/inter/Inter-Light.otf", "reg": "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
         "med": "/usr/share/fonts/opentype/inter/Inter-Medium.otf", "bold": "/usr/share/fonts/opentype/inter/Inter-Bold.otf"}


def fix_diameter(items):
    """the diameter sign as a round Ø (Inter's, cap height matched to Roboto's); what follows moves over"""
    from fonts import font
    from textmodel import weight_of
    shift = 0.0
    for i, (x, y, ch, path, size) in enumerate(items):
        if shift:
            items[i] = (x + shift, y, ch, path, size)
        if ch in "Øø" and "Inter" not in path:
            w = weight_of(path.rsplit("/", 1)[-1])
            ip = INTER[w]
            s2 = size * 0.711 / 0.7275
            shift += font(ip).text_length("Ø", s2) - font(path).text_length(ch, size)
            items[i] = (x + shift - (font(ip).text_length("Ø", s2) - font(path).text_length(ch, size)), y, "Ø", ip, s2)


def set_text(ed, L, txt, al, size=None):
    """`txt` in the line's main font, size and colour, in place of the line"""
    f = L.main_font
    from fonts import ttf, font
    size = size or L.size
    w = font(ttf(f)).text_length(txt, size)
    if al == "right":
        x = L.end - w
    elif al == "center":
        x = (L.end - w) / 2
    else:
        x = 0.0
    ed.put_text(L, x, txt, f, size, color=L.color)


def cell_room(page, L):
    """width from the start of a (left-aligned) line to the nearest vertical rule on its right, less 1 pt"""
    cy = L.O.y - 0.35 * L.size
    best = None
    for d in page.get_drawings():
        if not d.get("color"):
            continue
        for it in d["items"]:
            segs = []
            if it[0] == "l":
                segs.append((it[1], it[2]))
            elif it[0] == "re":
                R = it[1]
                segs += [(R.tl, R.bl), (R.tr, R.br)]
            for p, q in segs:
                if abs(p.x - q.x) < 0.3 and min(p.y, q.y) - 0.5 <= cy <= max(p.y, q.y) + 0.5 and p.x > L.bbox.x0 + 4:
                    if best is None or p.x < best:
                        best = p.x
    return (best - L.O.x - 1.0) if best is not None else None


def move_into(ed, it, en, rects):
    """the English line `en` set in the Italian line `it`'s place: same start (or end, or centre), its baseline — or, in a
    two-line header bar, halfway between the two"""
    x, y = it.coords(en.O)
    wi, we = it.end, width_of(en.chars)
    if abs(x) < 3.5:
        dx = -x
    elif abs(wi - (x + we)) < 3.5:
        dx = wi - (x + we)
    else:
        dx = (wi - we) / 2 - x
    c = container(rects, it.bbox | en.bbox)
    dy = -y if not c else -y / 2
    _shift(ed, en, it, dx, dy)
    en.removed = True


def _shift(ed, en, it, dx, dy):
    """move `en`'s characters by dx along / dy up `it`'s frame"""
    ed.drop(en.chars)
    items = []
    for c in en.chars:
        if not c.c.strip():
            continue
        x, y = it.coords(c.o)
        items.append((x + dx, y + dy, c))
    from fonts import ttf, char_for
    by = {}
    for x, y, c in items:
        by.setdefault(c.color, []).append((x, y, char_for(c.c, c.font), ttf(c.font), c.size))
    for col, its in by.items():
        ed.adds.append((it.u, it.v, fitz.Point(it.O), its, col))
