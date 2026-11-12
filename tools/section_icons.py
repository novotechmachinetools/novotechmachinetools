#!/usr/bin/env python3
"""Section shapes for the capacity tables of the profile benders (the owner, Nov 11 2026: "the original tables of the Şahinler
and TTMC profile benders show every section as a shape — use the shapes in the site's tables and in the brochures instead of
descriptions").

Each icon is drawn the way both catalogues draw a section-bending capacity: the bent bar as an arc (bending centre below it)
with the cross-section at both ends, as you see it looking along the bar.  At each end the horizontal direction is the
radius (away from the bending centre = outward, to the left at the left end, to the right at the right end) and the vertical
direction is across the ring.  Our own vector drawings, in the NovoTech orange and grey; the row's text stays beside the
shape for screen readers and search engines.

    icon_id(family_id, label)  -> an id below, or None (not a profile bender, or not a section row)
    svg(icon_id)               -> inline <svg> markup
    python3 tools/section_icons.py OUT.html   (a sheet of every shape, for checking)
"""
import math
import re
import sys

ORANGE, INK, GREY = "#F28A1F", "#1F2022", "#A4A8AE"


def _rect(u0, u1, v0, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def _circle(r, n=40):
    return [(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _hollow(outer, inset):
    (u0, v0), (u1, v1) = outer[0], outer[2]
    return [outer, _rect(u0 + inset, u1 - inset, v0 + inset, v1 - inset)[::-1]]


# u: along the radius (+ = outward, away from the bending centre); v: across the ring.  Shapes are centred when drawn.
T = 2.1          # wall of the open sections
SHAPES = {
    # bars
    "flat-edge":   [_rect(-7, 7, -2, 2)],                       # flat bar on edge: its width along the radius (hard way)
    "flat-flat":   [_rect(-2, 2, -8, 8)],                       # flat bar flat: its width across the ring (easy way)
    "square-bar":  [_rect(-5.5, 5.5, -5.5, 5.5)],
    "round-bar":   [_circle(6)],
    # tubes
    "round-tube":  [_circle(6.6), _circle(4.9)[::-1]],
    "pipe":        [_circle(6.6), _circle(3.7)[::-1]],
    "rect-edge":   _hollow(_rect(-7.5, 7.5, -4.2, 4.2), 1.7),   # long side along the radius
    "rect-flat":   _hollow(_rect(-4.2, 4.2, -7.5, 7.5), 1.7),   # long side across the ring
    "square-tube": _hollow(_rect(-6, 6, -6, 6), 1.7),
    # angles (equal legs): one leg across the ring, the other along the radius, outward or inward
    "angle-out":   [[(-6.5, -6.5), (6.5, -6.5), (6.5, -6.5 + T), (-6.5 + T, -6.5 + T), (-6.5 + T, 6.5), (-6.5, 6.5)]],
    "angle-in":    [[(6.5, -6.5), (-6.5, -6.5), (-6.5, -6.5 + T), (6.5 - T, -6.5 + T), (6.5 - T, 6.5), (6.5, 6.5)]],
    # tees: flange across the ring and the stem along the radius, outward or inward; or the flange flat along the radius
    "tee-out":     [[(-6.5, -7), (-6.5 + T, -7), (-6.5 + T, -T / 2), (6.5, -T / 2), (6.5, T / 2), (-6.5 + T, T / 2), (-6.5 + T, 7), (-6.5, 7)]],
    "tee-in":      [[(6.5, -7), (6.5 - T, -7), (6.5 - T, -T / 2), (-6.5, -T / 2), (-6.5, T / 2), (6.5 - T, T / 2), (6.5 - T, 7), (6.5, 7)]],
    "tee-flat":    [[(-7, -6.5), (7, -6.5), (7, -6.5 + T), (T / 2, -6.5 + T), (T / 2, 6.5), (-T / 2, 6.5), (-T / 2, -6.5 + T), (-7, -6.5 + T)]],
    # channels (web about 2.3 x the flange): web across the ring with the flanges outward or inward; or the web flat along the radius
    "ch-out":      [[(-3.4, -8), (3.6, -8), (3.6, -8 + T), (-3.4 + T, -8 + T), (-3.4 + T, 8 - T), (3.6, 8 - T), (3.6, 8), (-3.4, 8)]],
    "ch-in":       [[(3.4, -8), (-3.6, -8), (-3.6, -8 + T), (3.4 - T, -8 + T), (3.4 - T, 8 - T), (-3.6, 8 - T), (-3.6, 8), (3.4, 8)]],
    "ch-flat":     [[(-8, -3.4), (8, -3.4), (8, 3.6), (8 - T, 3.6), (8 - T, -3.4 + T), (-8 + T, -3.4 + T), (-8 + T, 3.6), (-8, 3.6)]],
    # I-beams (IPN, flange about half the height) and H-beams (HEA / HEB, flange as wide as the beam is high):
    # web across the ring with the flanges along the radius (easy way), or the web along the radius (hard way)
    "i-easy":      [[(-3.6, -8), (3.6, -8), (3.6, -6.3), (0.9, -6.3), (0.9, 6.3), (3.6, 6.3), (3.6, 8), (-3.6, 8), (-3.6, 6.3), (-0.9, 6.3), (-0.9, -6.3), (-3.6, -6.3)]],
    "h-easy":      [[(-7, -7), (7, -7), (7, -5.1), (1, -5.1), (1, 5.1), (7, 5.1), (7, 7), (-7, 7), (-7, 5.1), (-1, 5.1), (-1, -5.1), (-7, -5.1)]],
    "i-hard":      [[(-8, -3.6), (-6.3, -3.6), (-6.3, -0.9), (6.3, -0.9), (6.3, -3.6), (8, -3.6), (8, 3.6), (6.3, 3.6), (6.3, 0.9), (-6.3, 0.9), (-6.3, 3.6), (-8, 3.6)]],
    "h-hard":      [[(-7, -7), (-5.1, -7), (-5.1, -1), (5.1, -1), (5.1, -7), (7, -7), (7, 7), (5.1, 7), (5.1, 1), (-5.1, 1), (-5.1, 7), (-7, 7)]],
}

NAMES = {   # what each shape shows (the title of the drawing)
    "flat-edge": "flat bar on edge", "flat-flat": "flat bar flat", "square-bar": "square bar", "round-bar": "round bar",
    "round-tube": "round tube", "pipe": "pipe", "rect-edge": "rectangular tube on edge", "rect-flat": "rectangular tube flat",
    "square-tube": "square tube", "angle-out": "angle, leg out", "angle-in": "angle, leg in", "tee-out": "tee, stem out",
    "tee-in": "tee, stem in", "tee-flat": "tee, flange flat", "ch-out": "channel, flanges out", "ch-in": "channel, flanges in",
    "ch-flat": "channel, web flat", "i-easy": "I-beam, easy way", "h-easy": "H-beam, easy way", "i-hard": "I-beam, hard way",
    "h-hard": "H-beam, hard way",
}

# the profile benders whose capacity tables get the shapes: Şahinler (premium line) PK / HPK, TTMC (value line) RBM / HRBM
FAMILIES = re.compile(r"^(sahinler-pk|sahinler-hpk|tt-rbm)")

RULES = [   # (pattern on the row label, icon); the first match wins
    (r"^flat bar.*(on edge|hard way)", "flat-edge"),
    (r"^flat bar.*(flat|easy way)", "flat-flat"),
    (r"^square bar", "square-bar"),
    (r"^round bar", "round-bar"),
    (r"^pipe", "pipe"),
    (r"^round tube", "round-tube"),
    (r"^rectangular tube.*on edge", "rect-edge"),
    (r"^rectangular tube.*flat", "rect-flat"),
    (r"^rectangular tube", None),          # by maker below
    (r"^square tube", "square-tube"),
    (r"^angle.*leg out", "angle-out"),
    (r"^angle.*leg in", "angle-in"),
    (r"^(tee|t-bar).*stem out", "tee-out"),
    (r"^(tee|t-bar).*stem in", "tee-in"),
    (r"^(tee|t-bar).*flange", "tee-flat"),
    (r"^channel.*flanges out", "ch-out"),
    (r"^channel.*flanges in", "ch-in"),
    (r"^channel.*(hard way|web flat)", "ch-flat"),
    (r"^i-beam.*easy way", "i-easy"),
    (r"^i-beam.*hard way", "i-hard"),
    (r"^h-beam.*easy way", "h-easy"),
    (r"^h-beam.*hard way", "h-hard"),
]


def icon_id(family_id, label):
    if not family_id or not FAMILIES.match(family_id) or not label:
        return None
    low = label.lower()
    for pat, ico in RULES:
        if re.search(pat, low):
            if ico is None:          # the catalogues draw the rectangular tube on edge (Şahinler) or flat (TTMC)
                return "rect-edge" if family_id.startswith("sahinler") else "rect-flat"
            return ico
    return None


def _path(contours, cx, cy, side, k=1.15):
    us = [u for c in contours for u, _ in c]
    vs = [v for c in contours for _, v in c]
    du, dv = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
    d = ""
    for c in contours:
        pts = [(cx + side * k * (u - du), cy - k * (v - dv)) for u, v in c]
        d += "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"
    return d


def svg(icon, cls="sec-ico"):
    """the bent bar (grey arc, bending centre below) with the section at both ends (orange)"""
    if icon not in SHAPES:
        return ""
    cy = 21.5
    left = _path(SHAPES[icon], 10.5, cy, -1)      # at the left end, outward is to the left
    right = _path(SHAPES[icon], 61.5, cy, 1)
    return (f'<svg class="{cls}" viewBox="0 6 72 26" width="72" height="26" aria-hidden="true" focusable="false">'
            f'<title>{NAMES[icon]}</title>'
            f'<path d="M20 21.5 A18.5 18.5 0 0 1 52 21.5" fill="none" stroke="{GREY}" stroke-width="2.8" stroke-linecap="round"/>'
            f'<path d="{left}{right}" fill="{ORANGE}" fill-rule="evenodd" stroke="{INK}" stroke-width=".7" stroke-linejoin="round"/>'
            f'</svg>')


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "section-icons.html"
    rows = "".join(f'<tr><td>{svg(k)}</td><td>{svg(k, "big")}</td><td>{k}</td><td>{NAMES[k]}</td></tr>' for k in SHAPES)
    open(out, "w").write('<!doctype html><meta charset="utf-8"><style>body{font:14px sans-serif;margin:16px}'
                         'td{padding:4px 10px;border-bottom:1px solid #ddd}.big{width:216px;height:78px}</style>'
                         f"<table>{rows}</table>")
    print(out)
