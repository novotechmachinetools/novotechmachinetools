#!/usr/bin/env python3
"""Unit conversion and table helpers for the NovoTech value-line machines built by TTMC (tools/ttmc_more_*.py).

The supplier's Vol. 23 catalogue is metric; the website shows imperial first with the catalogue's metric value in brackets:
  L  225          -> 8.9″ (225 mm)                decimal inches (machine sizes, travels, strokes)
  F  60           -> 2-3/8″ (60 mm)               fractional inches (capacities)
  D  60           -> Ø2-3/8″ (60 mm)              round capacity
  R  (75, 45)     -> 3 × 1-3/4″ (75 × 45 mm)      rectangular capacity
  T  1.5          -> 16 ga (1.5 mm)                sheet / plate thickness: gauge to 2.5 mm, fractions above
  KW 1.1          -> 1.5 HP (1.1 kW)               motor; (kW, kW…) for several motors
  KG 143 / (143, 171) -> 315 lb (143 kg)           net weight (the catalogue's N.W./G.W.: net weight is shown)
  PK (86, 58, 77) -> 34 × 23 × 30″ (86 × 58 × 77 cm)   packing size; [("body", (…)), ("stand", (…))] for several crates
  RPM, MMIN (m/min -> ft/min), TON (metric t -> US tons), LIT (L -> US gal), MPA / BAR (-> psi), DEG, TXT
"""
from fractions import Fraction

GAUGE = {0.4: "28 ga", 0.5: "26 ga", 0.6: "24 ga", 0.7: "22 ga", 0.75: "22 ga", 0.8: "22 ga", 0.9: "20 ga", 1.0: "20 ga", 1.2: "18 ga",
         1.25: "18 ga", 1.5: "16 ga", 1.6: "16 ga", 2.0: "14 ga", 2.5: "12 ga"}
FRAC_T = {3.0: "1/8″", 3.2: "1/8″", 4.0: "5/32″", 4.5: "3/16″", 5.0: "3/16″", 6.0: "1/4″", 6.35: "1/4″", 6.5: "1/4″", 8.0: "5/16″", 10.0: "3/8″",
          12.0: "1/2″", 12.7: "1/2″", 13.0: "1/2″", 15.0: "5/8″", 16.0: "5/8″", 20.0: "3/4″", 22.0: "7/8″", 25.0: "1″", 30.0: "1-1/4″"}
HP = {0.04: "1/20", 0.09: "1/8", 0.12: "1/6", 0.15: "1/5", 0.18: "1/4", 0.25: "1/3", 0.37: "1/2", 0.4: "1/2", 0.45: "0.6", 0.55: "3/4", 0.75: "1",
      1.1: "1.5", 1.5: "2", 1.8: "2.5", 2.2: "3", 3.0: "4", 4.0: "5.5", 5.5: "7.5", 7.5: "10", 11.0: "15", 15.0: "20", 18.5: "25", 22.0: "30", 30.0: "40", 37.0: "50"}


def num(v, nd=0):
    s = f"{v:,.{nd}f}"
    return s.rstrip("0").rstrip(".") if nd and "." in s else s


def frac(mm, den=None):
    """inches as a fraction: nearest 1/16″ below 2″, 1/8″ from 2″, 1/4″ from 12″"""
    v = mm / 25.4
    den = den or (16 if v < 2 else 8 if v < 12 else 4)
    whole = int(v)
    fr = Fraction(round((v - whole) * den), den)
    if fr == 1:
        whole, fr = whole + 1, Fraction(0)
    if fr == 0:
        return f"{whole}″"
    return (f"{whole}-" if whole else "") + f"{fr.numerator}/{fr.denominator}″"


def dec(mm, nd=1):
    v = mm / 25.4
    return f"{num(v, nd)}″"


def mm_s(mm):
    return f"{mm:,.10g}"


def L(mm, nd=1):
    return f"{dec(mm, nd)} ({mm_s(mm)} mm)"


def F(mm):
    return f"{frac(mm)} ({mm_s(mm)} mm)"


def D(mm):
    return f"Ø{frac(mm)} ({mm_s(mm)} mm)"


def R(ab):
    a, b = ab
    return f"{frac(a).rstrip('″')} × {frac(b)} ({mm_s(a)} × {mm_s(b)} mm)"


def T(mm):
    if mm in GAUGE:
        return f"{GAUGE[mm]} ({mm_s(mm)} mm)"
    if mm in FRAC_T:
        return f"{FRAC_T[mm]} ({mm_s(mm)} mm)"
    return F(mm)


def hp(kw):
    return HP.get(round(kw, 2)) or num(kw / 0.7457, 1)


def KW(kw):
    if isinstance(kw, (tuple, list)):
        return " + ".join(f"{hp(k)} HP" for k in kw) + " (" + " + ".join(f"{k:g}" for k in kw) + " kW)"
    return f"{hp(kw)} HP ({kw:g} kW)"


def KG(kg):
    if isinstance(kg, (tuple, list)):
        kg = kg[0]
    return f"{round(kg * 2.20462):,} lb ({kg:,.10g} kg)"


def _pk(t):
    return " × ".join(f"{x / 2.54:.0f}" for x in t) + "″ (" + " × ".join(f"{x:g}" for x in t) + " cm)"


def PK(v):
    if isinstance(v, list):
        return " + ".join(f"{_pk(t)} {lab}" for lab, t in v)
    return _pk(v)


def MMIN(m):
    if isinstance(m, (tuple, list)):
        return " / ".join(num(x * 3.2808, 0) for x in m) + " ft/min (" + " / ".join(f"{x:g}" for x in m) + " m/min)"
    return f"{num(m * 3.2808, 0)} ft/min ({m:g} m/min)"


def IPM(m):
    """machine-tool feed / rapid traverse: m/min -> inches per minute"""
    if isinstance(m, (tuple, list)):
        return " / ".join(num(x * 39.37, 0) for x in m) + " ipm (" + " / ".join(f"{x:g}" for x in m) + " m/min)"
    return f"{num(m * 39.37, 0)} ipm ({m:g} m/min)"


def TON(t):
    return f"{num(t * 1.10231, 1)} US tons ({t:g} t)"


def LIT(l):
    return f"{num(l * 0.264172, 1)} US gal ({l:g} L)"


def MPA(p):
    return f"{num(p * 145.038, 0)} psi ({p:g} MPa)"


def BAR(p):
    return f"{num(p * 14.5038, 0)} psi ({p:g} bar)"


def RPM(v):
    if isinstance(v, (tuple, list)):
        return " / ".join(f"{x:,}" if isinstance(x, int) else str(x) for x in v) + " rpm"
    return f"{v:,} rpm" if isinstance(v, int) else f"{v} rpm"


def MS(v):
    """belt / wheel surface speed m/s -> surface feet per minute"""
    if isinstance(v, (tuple, list)):
        return " / ".join(num(x * 196.85, 0) for x in v) + " ft/min (" + " / ".join(f"{x:g}" for x in v) + " m/s)"
    return f"{num(v * 196.85, 0)} ft/min ({v:g} m/s)"


def BELT(v):
    """(length, width) mm -> 'width × length″' as abrasive belts are sold in North America: 3 × 79″ (75 × 2,000 mm)"""
    ln, w = v
    lin, win = ln / 25.4, w / 25.4
    ls = f"{lin:.0f}" if lin >= 24 else frac(ln).rstrip("″")
    step = 4 if win < 3.9 else 2                      # nominal belt width: nearest 1/4″, from 4″ nearest 1/2″
    ws = str(Fraction(round(win * step), step))
    ws = ws if "/" not in ws else (f"{int(Fraction(ws))}-{Fraction(ws) - int(Fraction(ws))}" if Fraction(ws) > 1 else ws)
    return f"{ws} × {ls}″ ({mm_s(w)} × {mm_s(ln)} mm)"


def WHEEL(v):
    """(diameter, width) mm -> Ø7-7/8 × 3″ (200 × 75 mm)"""
    d, w = v
    return f"Ø{frac(d).rstrip('″')} × {frac(w)} ({mm_s(d)} × {mm_s(w)} mm)"


def DEG(v):
    return f"{v}°" if not isinstance(v, str) else v


def TXT(v):
    return v


KINDS = dict(L=L, F=F, D=D, R=R, T=T, KW=KW, KG=KG, PK=PK, MMIN=MMIN, IPM=IPM, MS=MS, BELT=BELT, WHEEL=WHEEL, TON=TON, LIT=LIT, MPA=MPA, BAR=BAR, RPM=RPM, DEG=DEG, TXT=TXT,
             L0=lambda v: L(v, 0), L2=lambda v: L(v, 2))


def cell(kind, v):
    if v is None or v == "—":
        return "—"
    if isinstance(v, str) and kind not in ("TXT", "DEG", "RPM"):
        return v                      # finished text in a numeric row ("—", "manual", "1,200 ft/min" …)
    return KINDS[kind](v)


def table(title, sub, models, rows):
    """rows: (label, kind, [value per model]) or (label, sub, kind, [values]) — a single value (not a list) is repeated for every model.
    A label starting with '*' is a key row (shown in the at-a-glance summary)."""
    out = []
    for r in rows:
        if len(r) == 4:
            label, s, kind, vals = r
        else:
            label, kind, vals = r
            s = ""
        key = label.startswith("*")
        label = label.lstrip("*")
        if not isinstance(vals, list):
            vals = [vals] * len(models)
        if len(vals) != len(models):
            raise SystemExit(f"{title}: row '{label}' has {len(vals)} cells for {len(models)} models")
        out.append({"label": label, "sub": s, "cells": [cell(kind, v) for v in vals], "key": key})
    return {"title": title, "sub": sub, "models": list(models), "rows": out}


def spec(tables, glance_keys, glance_labels, note, caps=None):
    """glance_labels: per glance key the row label it is read from (None -> '—'); a label may be a tuple of alternatives."""
    models = []
    for t in tables:
        rr = {r["label"]: r["cells"] for r in t["rows"]}
        for i, m in enumerate(t["models"]):
            g = []
            for lab in glance_labels:
                labs = lab if isinstance(lab, tuple) else (lab,)
                v = next((rr[x][i] for x in labs if x and x in rr), "—")
                g.append(v)
            models.append({"name": m, "glance": g})
    return {"kind": "table", "tables": tables, "models": models, "glance_keys": glance_keys, "caps": caps or {}, "note": note}
