"""Small page-specific fixes that run before the line-by-line clean-up."""
import os

import fitz

from fonts import font

FD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", "roboto")
BOLD = os.path.join(FD, "Roboto-Bold.ttf")
LIGHT = os.path.join(FD, "Roboto-Light.ttf")
ITALIC = os.path.join(FD, "Roboto-Italic.ttf")
INK = (0.137, 0.122, 0.125)
FRAME = (0.584, 0.661, 0.795)


def _redact_text(page, rects):
    for r in rects:
        page.add_redact_annot(fitz.Rect(r), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)


def _centered(page, cx, y, text, size, path, color):
    fo = font(path)
    tw = fitz.TextWriter(page.rect)
    tw.append(fitz.Point(cx - fo.text_length(text, size) / 2, y), text, font=fo, fontsize=size)
    tw.write_text(page, color=color)


def p204(page, ppage, ctx):
    """the offset-holder table's header: one white line per cell, like CODE and Z (the Italian / English pairs went)"""
    _redact_text(page, [(150, 88, 250, 113), (262, 88, 366, 113), (376, 88, 532, 113)])
    for cx, t in ((197.9, "OFFSET Z"), (313.5, "ANGLE"), (454.4, "MAX SHEET THICKNESS")):
        _centered(page, cx, 104.6, t, 8.71, BOLD, (1, 1, 1))


def p17(page, ppage, ctx):
    """the moving-horn boxes are drawn as outlines ('2x150 | 3,5 kg'): set again as text with a decimal point, and an
    inch / lb twin under each box (the boxes' frames stay)"""
    boxes = [(fitz.Rect(353.7, 95.5, 405.8, 104.6), 3.5), (fitz.Rect(353.7, 133.2, 405.9, 142.3), 3.5),
             (fitz.Rect(353.7, 169.3, 405.1, 178.3), 4.0)]
    mid = 381.4
    for R, _ in boxes:
        page.add_redact_annot(fitz.Rect(R.x0 + 0.9, R.y0 + 0.9, R.x1 - 0.9, R.y1 - 0.9), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                          text=fitz.PDF_REDACT_TEXT_NONE)
    fs = 5.6
    for R, kg in boxes:
        T = fitz.Rect(R.x0, R.y1 + 1.6, R.x1, R.y1 + 1.6 + R.height)
        sh = page.new_shape()
        sh.draw_rect(T)
        sh.finish(color=FRAME, fill=(1, 1, 1), width=0.4)
        sh.draw_line(fitz.Point(mid, T.y0), fitz.Point(mid, T.y1))
        sh.finish(color=FRAME, width=0.4)
        sh.commit()
        lb = kg * 2.20462
        for box, a, b in ((R, "2 × 150 mm", f"{kg:.1f} kg"), (T, "2 × 5.91″", f"{lb:.1f} lb")):
            y = box.y0 + box.height / 2 + 0.36 * fs
            _centered(page, (box.x0 + mid) / 2, y, a, fs if box is T else 5.2, LIGHT, INK)
            _centered(page, (mid + box.x1) / 2, y, b, fs, LIGHT, INK)
    ctx["skip_rects"] += [fitz.Rect(R.x0 - 1, R.y0 - 1, R.x1 + 1, R.y1 + R.height + 3) for R, _ in boxes]


def _lines(page, x, cy, lines, size, path, color, lead=1.12, align="left"):
    """lines of text centred as a block on cy"""
    fo = font(path)
    n = len(lines)
    y = cy - (n - 1) * lead * size / 2 + 0.36 * size
    tw = fitz.TextWriter(page.rect)
    for t in lines:
        xx = x - fo.text_length(t, size) / 2 if align == "center" else x
        tw.append(fitz.Point(xx, y), t, font=fo, fontsize=size)
        y += lead * size
    tw.write_text(page, color=color)


P215_SYSTEMS = {"std": ["Standard clamping system", "(each clamp with two screws)"],
                "man": ["EUROGRIP manual clamping system", "(M-EASY or M-TOP)"],
                "pn": ["EUROGRIP pneumatic clamping", "system (P-EASY or P-TOP)"]}
SECT = "(3 × 835 mm + 1 sectioned)"
P215_ROWS = [  # (band top, band bottom, system, what is done)
    (88.3, 137.6, "std", ["Loosen 30 Allen bolts", "(5 seconds each)"]),
    (137.6, 186.8, "man", ["Unlock 15 handles", "(3 seconds each)"]),
    (186.8, 236.1, "pn", ["A push-button opens the clamps", "(2 seconds)"]),
    (235.2, 284.5, "std", ["Slide the tools out from the side", "of the machine " + SECT]),
    (284.5, 333.7, "man", ["Remove the tools vertically from", "the front " + SECT]),
    (333.7, 383.0, "pn", ["Remove the tools vertically from", "the front " + SECT]),
    (383.0, 432.2, "std", ["Insert the tools from the side and", "slide them into place", SECT]),
    (432.2, 481.5, "man", ["Insert the tools vertically from", "the front " + SECT]),
    (481.5, 530.7, "pn", ["Insert the tools vertically from", "the front " + SECT]),
    (641.6, 690.8, "man", ["Lock 15 handles", "(3 seconds each)"]),
    (690.8, 740.1, "pn", ["A push-button closes the clamps", "(2 seconds)"]),
]
P215_LOCK = [(530.7, 568.0, ["Lightly tighten 30 Allen bolts", "(4 seconds each)"]),
             (568.0, 604.9, ["Lower the upper beam to align", "the tools"]),
             (604.9, 641.6, ["Fully tighten 30 Allen bolts", "(3 seconds each)"])]
P215_PHASES = [(181.0, "UNLOCKING THE CLAMPS"), (316.0, "REMOVING THE PUNCHES"), (471.0, "INSERTING THE PUNCHES"),
               (642.0, "LOCKING THE CLAMPS")]


def p215(page, ppage, ctx):
    """the tool-change time table: the two text columns and the phase names set again in English only, one block per
    cell (the Italian and English were stacked in each cell)"""
    _redact_text(page, [(140, 90, 447, 738), (36, 168, 136, 192), (36, 302, 136, 326), (36, 457, 136, 481),
                        (36, 628, 136, 652)])
    ink = (0.137, 0.122, 0.125)
    for top, bot, sysk, what in P215_ROWS:
        cy = (top + bot) / 2
        _lines(page, 145.1, cy, P215_SYSTEMS[sysk], 7.8, ITALIC, ink)
        _lines(page, 288.7, cy, what, 7.8, ITALIC, ink)
    _lines(page, 145.1, (530.7 + 641.6) / 2, P215_SYSTEMS["std"], 7.8, ITALIC, ink)
    for top, bot, what in P215_LOCK:
        _lines(page, 288.7, (top + bot) / 2, what, 7.8, ITALIC, ink)
    for cy, t in P215_PHASES:
        _lines(page, 85.6, cy, [t], 7.4, ITALIC, ink, align="center")
    ctx["no_numbers"] = True


def index_head(page, ppage, ctx):
    """the product index's header row ('CODICE/CODE', 'PAGINA/PAGE', drawn as outlines): each cell painted over in the
    bar's own colour and labelled CODE or PAGE"""
    bars = [d for d in page.get_drawings() if d.get("fill") and abs(d["fill"][0] - 0.546) < 0.03 and abs(d["fill"][2] - 0.482) < 0.03
            and d["rect"].width > 400 and 10 < d["rect"].height < 20]
    if not bars:
        return
    bar = bars[0]["rect"]
    col = bars[0]["fill"]
    seps = sorted({round(d["rect"].x0, 1) for d in page.get_drawings() if d.get("fill") == (1.0, 1.0, 1.0)
                   and d["rect"].width < 2 and d["rect"].y0 <= bar.y0 + 1 and d["rect"].y1 >= bar.y1 - 1
                   and bar.x0 < d["rect"].x0 < bar.x1})
    edges = [bar.x0] + seps + [bar.x1]
    sh = page.new_shape()
    for a, b in zip(edges, edges[1:]):
        sh.draw_rect(fitz.Rect(a + 1.1, bar.y0 + 0.4, b - 1.1, bar.y1 - 0.4))
    sh.finish(color=None, fill=col, width=0)
    sh.commit()
    med = os.path.join(FD, "Roboto-Medium.ttf")
    for k, (a, b) in enumerate(zip(edges, edges[1:])):
        _centered(page, (a + b) / 2, bar.y0 + bar.height / 2 + 2.7, "CODE" if k % 2 == 0 else "PAGE", 7.6, med, (1, 1, 1))


def _rotated(page, x, cy, text, size, path, color):
    """text reading bottom to top, baseline at x, centred on cy"""
    fo = font(path)
    w = fo.text_length(text, size)
    pivot = fitz.Point(x, cy + w / 2)
    tw = fitz.TextWriter(page.rect)
    tw.append(pivot, text, font=fo, fontsize=size)
    tw.write_text(page, color=color, morph=(pivot, fitz.Matrix(90)))


P82_BLUE = (0.27, 0.48, 0.66)


def p82(page, ctx, report=None):
    """the ESH horns are pictures, their dimensions part of them: the inch values written beside them"""
    reg = os.path.join(FD, "Roboto-Regular.ttf")
    fs = 6.6
    for cx, y, t in ((245.7, 290.6, "1.38″"), (488.5, 404.1, ".984″"), (267.1, 608.2, ".787″")):
        _centered(page, cx, y, t, fs, reg, P82_BLUE)
    for x, y, t in ((268.4, 362.6, "R .197″"), (505.0, 494.0, "R .394″"), (281.0, 697.0, "R .315″")):
        fo = font(reg)
        tw = fitz.TextWriter(page.rect)
        tw.append(fitz.Point(x, y), t, font=fo, fontsize=fs)
        tw.write_text(page, color=P82_BLUE)
    for x, cy, t in ((294.0, 392.8, ".394″"), (526.5, 509.0, ".394″"), (300.5, 711.6, ".472″")):
        _rotated(page, x, cy, t, fs, reg, P82_BLUE)
