"""EUROSTAMP's air-bending charts (catalogue page 6) read cell by cell, for the imperial page: sheet thickness S across,
V opening / shortest flange B / inside radius Ri down, the force in t/m in the cells, and which cells are the
recommended V (dark blue)."""
import fitz

CAT = "/home/claude/eurostamp/pdf/cat.pdf"


def num(t):
    return float(t.replace(",", "."))


def read_table(page, x0, x1, y0=470, y1=760):
    words = [w for w in page.get_text("words") if x0 <= (w[0] + w[2]) / 2 <= x1 and y0 <= (w[1] + w[3]) / 2 <= y1]
    head = [w for w in words if 476 <= (w[1] + w[3]) / 2 <= 484]
    cols = []
    for w in sorted(head, key=lambda w: w[0]):
        t = w[4].replace("mm", "")
        if t and t[0].isdigit():
            cols.append((num(t), (w[0] + w[2]) / 2))
    body = [w for w in words if 488 <= (w[1] + w[3]) / 2 <= 752]
    rows = {}
    for w in body:
        cy = round((w[1] + w[3]) / 2 / 2) * 2
        rows.setdefault(cy, []).append(w)
    # rows of V / B / Ri: the first three words of the left columns
    left = x0 + 36
    table = []
    ys = sorted(rows)
    # merge rows whose words are split over two y values (cells set a point lower)
    merged = []
    for y in ys:
        if merged and y - merged[-1][0] <= 2:
            merged[-1][1].extend(rows[y])
        else:
            merged.append([y, list(rows[y])])
    for y, ws in merged:
        ws.sort(key=lambda w: w[0])
        lab = [w for w in ws if w[2] < left]
        cells = [w for w in ws if w[0] >= left - 2]
        if len(lab) < 3:
            continue
        V, B, Ri = (num(lab[0][4]), num(lab[1][4]), num(lab[2][4]))
        vals = {}
        for w in cells:
            cx = (w[0] + w[2]) / 2
            S = min(cols, key=lambda c: abs(c[1] - cx))
            vals[S[0]] = int(num(w[4]))
        table.append({"V": V, "B": B, "Ri": Ri, "F": vals, "y": y})
    return [c[0] for c in cols], table


def recommended(page, table, cols_x):
    """the dark-blue cells: (V, S) pairs"""
    out = set()
    for d in page.get_drawings():
        f = d.get("fill")
        if not f or not (f[2] > 0.35 and f[0] < 0.2):
            continue
        r = d["rect"]
        if not (5 < r.width < 14 and 8 < r.height < 16):
            continue
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        row = min(table, key=lambda t: abs(t["y"] - cy))
        if abs(row["y"] - cy) > 6:
            continue
        S = min(cols_x, key=lambda c: abs(c[1] - cx))
        out.add((row["V"], S[0]))
    return out


def charts():
    doc = fitz.open(CAT)
    page = doc[5]
    res = {}
    for name, (x0, x1) in (("mild", (30, 290)), ("stainless", (288, 560))):
        cols, table = read_table(page, x0, x1)
        words = [w for w in page.get_text("words") if x0 <= (w[0] + w[2]) / 2 <= x1 and 476 <= (w[1] + w[3]) / 2 <= 484]
        cols_x = []
        for w in sorted(words, key=lambda w: w[0]):
            t = w[4].replace("mm", "")
            if t and t[0].isdigit():
                cols_x.append((num(t), (w[0] + w[2]) / 2))
        res[name] = {"S": cols, "rows": table, "rec": sorted(recommended(page, table, cols_x))}
    return res


if __name__ == "__main__":
    import json
    c = charts()
    for k, v in c.items():
        print(k, v["S"])
        for r in v["rows"]:
            print("  ", r["V"], r["B"], r["Ri"], r["F"])
        print("  rec:", v["rec"])
