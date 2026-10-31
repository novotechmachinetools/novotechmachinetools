#!/usr/bin/env python3
"""NovoTech value-line sheet-metal machines — CNC / NC / electric press brakes, hydraulic swing beam and guillotine shears,
CNC V-grooving machines, panel benders and the hydraulic ironworker.  Metric data from the supplier's 2025/26 brochures,
website tables and the quotations NovoTech received (see /home/claude/value-sheet-src); shown as imperial (metric) like the rest of the
site.  Model numbers are the supplier's: tonnage × bending length (press brakes), thickness × length (shears), length × width
(V-grooving), bend width (panel benders), tonnage (ironworker).

Pages fed from here: novotech-cnc-press-brakes (WAD CNC, heavy-duty WAD, WC67K/E NC, WADG electric), hydraulic-
shearing-machine (QC12K swing beam, Q11K guillotine), v-grooving-machine (horizontal, vertical); the panel benders are
appended to panel-bender.html (tools/dener_pages.py) and the ironworker to ironworker-machines.html (tools/sahinler_pages.py).
"""
from dener_data import inch, feet, length, tons, hp, speed, weight, dims, gal, mmin, table, spec, vids, CAPS  # noqa: F401

BRAND = "novotech"
P_PB = "novotech-cnc-press-brakes"       # hydraulic CNC, NC and electric on one page (Oct 2026: the two pages were merged)
P_HPB = P_EPB = P_PB
P_SHEAR = "hydraulic-shearing-machine"
P_VG = "v-grooving-machine"
P_PANEL = "panel-bender"
P_IRON = "ironworker-machines"

VOLT = "CSA-approved electrical panel, 600 V 3-phase standard (208 / 240 / 480 V on request)"
CAPS.update({25: "1″", 30: "1-3/16″", 40: "1-9/16″", 2: "5/64″", 3: "1/8″", 1.5: "1/16″", 1: "0.04″", 2.5: "3/32″", 35: "1-3/8″", 50: "2″", 28: "1-1/8″", 15: "19/32″", 5: "3/16″", 11: "7/16″", 45: "1-3/4″", 55: "2-1/8″", 60: "2-3/8″", 65: "2-9/16″", 70: "2-3/4″", 75: "3″"})


def cap(mm):
    return f"{CAPS[mm]} ({mm:g} mm)"


def kw_hp(v):
    """'11' → 14.8 HP (11 kW); '2X15' → 2 × 20.1 HP (2 × 15 kW); 'Estun: 4.4; …' → first value"""
    s = str(v)
    if ";" in s:
        s = s.split(";")[0].split(":")[-1].strip()
    if "x" in s.lower():
        n, k = s.lower().replace("×", "x").split("x")
        return f"{n.strip()} × {hp(float(k))}"
    return hp(float(s))


# ------------------------------------------------------------------------------------------------ CNC hydraulic press brakes
# (model, kN, length, oil L, approach, bend, return, X stroke, X speed, R stroke, R speed, between columns, throat, stroke, open height, servo kW (Estun), pump ml/r, weight t, L, W, H)
WAD = [("WAD-50T/1300", 500, 1300, 130, 160, 13, 160, 500, 350, 200, 200, 1120, 250, 150, 460, 4.4, 13, 3.5, 1750, 1500, 2330),
       ("WAD-50T/1600", 500, 1600, 130, 160, 18, 200, 500, 400, 200, 200, 1300, 250, 150, 460, 4.4, 13, 3.5, 2150, 1500, 2330),
       ("WAD-70T/2000", 700, 2000, 130, 220, 13, 160, 500, 350, 200, 200, 1600, 300, 150, 460, 5.5, 13, 4.2, 2400, 1600, 2400),
       ("WAD-70T/2500", 700, 2500, 130, 220, 15, 200, 500, 400, 200, 200, 2050, 300, 150, 460, 5.5, 13, 4.4, 3100, 1600, 2400),
       ("WAD-80T/2500", 800, 2500, 170, 220, 12, 145, 500, 350, 200, 200, 2050, 300, 150, 460, 8.7, 16, 5.6, 3100, 1600, 2460),
       ("WAD-110T/3200", 1100, 3200, 170, 220, 12, 160, 500, 350, 200, 200, 2700, 400, 200, 480, 10.8, 19, 7.5, 3750, 2202, 2700),
       ("WAD-110T/4100", 1100, 4100, 170, 220, 12, 160, 500, 350, 200, 200, 3600, 400, 200, 480, 10.8, 19, 8.7, 4700, 1800, 2700),
       ("WAD-135T/3200", 1350, 3200, 170, 220, 10, 130, 500, 350, 200, 200, 2700, 400, 200, 480, 10.8, 19, 8.3, 3800, 1800, 2700),
       ("WAD-135T/4100", 1350, 4100, 170, 220, 10, 130, 500, 350, 200, 200, 3600, 400, 200, 480, 10.8, 19, 10.5, 4700, 1800, 2700),
       ("WAD-170T/3200", 1700, 3200, 300, 160, 10, 100, 500, 350, 200, 200, 2700, 450, 200, 480, 13.2, 25, 10.8, 3800, 2000, 2800),
       ("WAD-170T/4100", 1700, 4100, 300, 160, 10, 100, 500, 350, 200, 200, 3600, 450, 200, 480, 13.2, 25, 12.5, 4700, 2000, 2800),
       ("WAD-170T/5000", 1700, 5000, 300, 160, 10, 100, 500, 350, 200, 200, 4000, 450, 200, 480, 13.2, 25, 13.4, 6300, 2000, 3160),
       ("WAD-170T/6000", 1700, 6000, 300, 160, 10, 100, 500, 350, 200, 200, 4800, 450, 200, 480, 13.2, 25, 19.5, 6300, 2000, 3160),
       ("WAD-220T/3200", 2200, 3200, 300, 160, 9, 105, 500, 350, 200, 200, 2600, 450, 200, 480, 16.7, 32, 12.5, 3800, 2200, 2850),
       ("WAD-220T/4100", 2200, 4100, 300, 160, 9, 105, 500, 350, 200, 200, 3600, 450, 200, 480, 16.7, 32, 14.6, 4700, 2200, 2850),
       ("WAD-220T/5000", 2200, 5000, 300, 160, 9, 105, 500, 350, 200, 200, 4000, 450, 200, 480, 16.7, 32, 17.5, 5600, 2200, 2980),
       ("WAD-220T/6000", 2200, 6000, 300, 160, 9, 105, 500, 350, 200, 200, 4800, 450, 200, 480, 16.7, 32, 20.5, 6700, 2200, 3220),
       ("WAD-250T/3200", 2500, 3200, 460, 130, 8.5, 100, 500, 350, 200, 200, 2600, 450, 250, 540, 16.7, 32, 16.5, 3800, 2200, 3120),
       ("WAD-250T/4000", 2500, 4000, 460, 130, 8.5, 100, 500, 350, 200, 200, 3100, 450, 250, 540, 16.7, 32, 16.6, 4600, 2200, 3150),
       ("WAD-250T/5000", 2500, 5000, 460, 130, 8.5, 100, 500, 350, 200, 200, 3800, 450, 250, 540, 16.7, 32, 20.5, 5600, 2150, 3150),
       ("WAD-250T/6000", 2500, 6000, 460, 130, 8.5, 100, 500, 350, 200, 200, 4800, 450, 250, 540, 16.7, 32, 25.5, 6300, 2150, 3150),
       ("WAD-300T/3200", 3000, 3200, 650, 120, 8.5, 110, 500, 350, 200, 200, 2600, 500, 250, 570, 21.4, 40, 18.8, 3500, 2250, 3200),
       ("WAD-300T/4000", 3000, 4000, 650, 120, 8.5, 110, 500, 350, 200, 200, 3100, 500, 250, 570, 21.4, 40, 19.9, 4300, 2500, 3400),
       ("WAD-300T/5000", 3000, 5000, 650, 120, 8.5, 110, 500, 350, 200, 200, 3800, 500, 250, 570, 21.4, 40, 26.3, 5300, 2500, 3400),
       ("WAD-300T/6000", 3000, 6000, 650, 120, 8.5, 110, 500, 350, 200, 200, 4800, 500, 250, 570, 21.4, 40, 29.7, 6300, 2500, 3400)]
WAD_S, WAD_M, WAD_L = WAD[:9], WAD[9:17], WAD[17:]

# heavy duty: (model, kN, length, oil, approach, bend, return, X stroke, X speed, R stroke, R speed, columns, throat, stroke, open, servo kW, pump, weight, L, W, H)
WAD_H = [("WAD-400T/4000", 4000, 4000, 800, 80, 8, 80, 980, 200, 200, 40, 3100, 500, 300, 610, "26.9", "50", 24.8, 4300, 2700, 3500),
         ("WAD-400T/5000", 4000, 5000, 800, 80, 8, 80, 980, 200, 200, 40, 3800, 500, 300, 610, "26.9", "50", 30, 5300, 2700, 3500),
         ("WAD-400T/6000", 4000, 6000, 800, 80, 8, 80, 980, 200, 200, 40, 4800, 500, 300, 610, "26.9", "50", 35.5, 6300, 2700, 3500),
         ("WAD-500T/4000", 5000, 4000, 760, 80, 9.5, 110, 980, 220, 200, 40, 3100, 500, 300, 610, "33", "64", 33.5, 4300, 2700, 3500),
         ("WAD-500T/5000", 5000, 5000, 760, 80, 9.5, 110, 980, 200, 200, 40, 3800, 500, 300, 610, "33", "64", 36.2, 5300, 2700, 3500),
         ("WAD-500T/6000", 5000, 6000, 760, 80, 9.5, 110, 980, 200, 200, 40, 4800, 500, 300, 610, "33", "64", 41.8, 6300, 2700, 3600),
         ("WAD-600T/4000", 6000, 4000, 1050, 80, 8.5, 85, 980, 200, 200, 40, 3100, 600, 320, 650, "45", "80", 43.1, 4300, 3300, 3900),
         ("WAD-600T/5000", 6000, 5000, 1050, 80, 8.5, 85, 980, 220, 200, 40, 3800, 600, 320, 650, "45", "80", 48.3, 5300, 3300, 3900),
         ("WAD-600T/6000", 6000, 6000, 1050, 80, 8.5, 85, 980, 200, 200, 40, 4800, 600, 320, 650, "45", "80", 56.2, 6300, 3300, 3900),
         ("WAD-800T/4000", 8000, 4000, 1800, 80, 8, 90, 980, 220, 200, 40, 2800, 600, 320, 800, "2X26.9", "2 × 50", 57, 4250, 3500, 4100),
         ("WAD-800T/5000", 8000, 5000, 1800, 80, 8, 90, 980, 220, 200, 40, 3700, 600, 320, 800, "2X26.9", "2 × 50", 66, 5300, 3600, 4420),
         ("WAD-800T/6000", 8000, 6000, 1800, 80, 8, 90, 980, 220, 200, 40, 4600, 600, 320, 800, "2X26.9", "2 × 50", 74, 6300, 3600, 4300),
         ("WAD-800T/8000", 8000, 8000, 1800, 80, 8, 90, 980, 200, 200, 40, 6300, 600, 320, 800, "2X26.9", "2 × 50", 87.5, 8300, 3600, 4500),
         ("WAD-1000T/5000", 10000, 5000, 1700, 80, 8.5, 100, 980, 200, 200, 40, 3600, 600, 400, 920, "2X33", "2 × 64", 78, 5260, 4410, 4260),
         ("WAD-1000T/6000", 10000, 6000, 1700, 80, 8.5, 100, 980, 200, 200, 40, 4600, 600, 400, 920, "2X33", "2 × 64", 88, 6260, 4410, 4460),
         ("WAD-1000T/7000", 10000, 7000, 1900, 80, 8.5, 100, 980, 200, 200, 40, 5600, 600, 400, 920, "2X33", "2 × 64", 96, 7310, 4410, 4680),
         ("WAD-1000T/8000", 10000, 8000, 1900, 80, 8.5, 100, 980, 200, 200, 40, 6300, 600, 400, 920, "2X33", "2 × 64", 106, 8300, 4410, 4980),
         ("WAD-1200T/5000", 12000, 5000, 2300, 80, 8.5, 80, 980, 200, 200, 40, 3500, 600, 400, 920, "2X45", "2 × 80", 97, 5280, 4620, 4260),
         ("WAD-1200T/6000", 12000, 6000, 2300, 80, 8.5, 80, 980, 200, 200, 40, 4500, 600, 400, 920, "2X45", "2 × 80", 106, 6280, 4620, 4560),
         ("WAD-1200T/7000", 12000, 7000, 2300, 80, 8.5, 80, 980, 200, 200, 40, 5300, 600, 400, 920, "2X45", "2 × 80", 113, 7280, 4620, 4860),
         ("WAD-1200T/8000", 12000, 8000, 2300, 80, 8.5, 80, 980, 200, 200, 40, 6300, 600, 400, 920, "2X45", "2 × 80", 123, 8280, 4620, 5060)]
WAD_H1, WAD_H2 = WAD_H[:9], WAD_H[9:]


def pb_rows(data):
    return [("Bending force", [tons(r[1] / 10) for r in data]),
            ("Bending length", [length(r[2]) for r in data]),
            ("Distance between columns", [inch(r[11]) for r in data]),
            ("Throat depth", [inch(r[12]) for r in data]),
            ("Stroke", [inch(r[13]) for r in data]),
            ("Daylight", "open height", [inch(r[14]) for r in data]),
            ("Approach speed", [speed(r[4]) for r in data]),
            ("Bending speed", [speed(r[5]) for r in data]),
            ("Return speed", [speed(r[6]) for r in data]),
            ("Back gauge X stroke · speed", [f"{inch(r[7])} · {speed(r[8])}" for r in data]),
            ("Back gauge R stroke · speed", [f"{inch(r[9])} · {speed(r[10])}" for r in data]),
            ("Servo main motor", [kw_hp(r[15]) for r in data]),
            ("Hydraulic oil tank", [gal(r[3]) for r in data]),
            ("Dimensions L × W × H", [dims(r[18], r[19], r[20]) for r in data]),
            ("Weight", [weight(round(r[17] * 1000)) if r[17] else "—" for r in data])]


PB_GK = ["bending_force", "bending_length", "stroke", "daylight", "weight"]
PB_G_FROM = ["Bending force", "Bending length", "Stroke", "Daylight", "Weight"]
NOTE_PB = ("Bending force in US tons (metric tons in brackets); the model number is the supplier's — metric tonnage × metric bending length. "
           "Capacities vary with the V-die opening, material and sheet length: check the bending chart or ask us for the tonnage your part needs. "
           "Dimensions are overall L (along the bed) × W × H with the standard front supports; weights are reference values.")

T_WAD_S = table("CNC hydraulic press brakes · 4 – 13.5 ft", "9 models · 55 – 149 US tons", [r[0] for r in WAD_S], pb_rows(WAD_S))
T_WAD_C = table("Compact CNC press brakes · 4.3 and 5.2 ft", "2 models · 55 US tons", [r[0] for r in WAD[:2]], pb_rows(WAD[:2]))
T_WAD_M = table("CNC hydraulic press brakes · 170 – 220 t", "8 models · 187 – 243 US tons · 10 – 20 ft", [r[0] for r in WAD_M], pb_rows(WAD_M))
T_WAD_L = table("CNC hydraulic press brakes · 250 – 300 t", "8 models · 276 – 331 US tons · 10 – 20 ft", [r[0] for r in WAD_L], pb_rows(WAD_L))
T_WAD = table("CNC hydraulic press brakes · 50 – 300 t", "25 models · 55 – 331 US tons · 4 – 20 ft", [r[0] for r in WAD], pb_rows(WAD))
T_WAD_H1 = table("Heavy-duty CNC press brakes · 400 – 600 t", "9 models · 441 – 661 US tons · 13 – 20 ft", [r[0] for r in WAD_H1], pb_rows(WAD_H1))
T_WAD_H2 = table("Heavy-duty CNC press brakes · 800 – 1,200 t", "12 models · 882 – 1,323 US tons · 13 – 26 ft · twin pumps", [r[0] for r in WAD_H2], pb_rows(WAD_H2))

# NC torsion bar: (model, kN, length, oil, approach, bend, return, X stroke, X speed, columns, throat, stroke, open, kW, pump, weight t, L, W, H)
NC = [("WC67K-30t/1600", 300, 1600, 80, 120, 17, 160, 600, 150, 1300, 200, 80, 335, 5.5, 11, 2.1, 1800, 1200, 1700),
      ("WC67K/E-30t/2000", 300, 2000, 100, 140, 17, 160, 600, 150, 1600, 200, 80, 335, 5.5, 11, 2.3, 2200, 1200, 1700),
      ("WC67K/E-40t/2500", 400, 2500, 170, 110, 15, 90, 600, 150, 2030, 250, 100, 355, 5.5, 13, 3.2, 2700, 1200, 1900),
      ("WC67K-63t/2500", 630, 2500, 170, 100, 10, 70, 600, 150, 2050, 250, 120, 370, 5.5, 13, 4.1, 2500, 1350, 2282),
      ("WC67K/E-80t/2500", 800, 2500, 170, 110, 10, 80, 600, 150, 2050, 250, 120, 380, 5.5, 16, 4.6, 2500, 1400, 2150),
      ("WC67K/E-100t/2500", 1000, 2500, 260, 90, 7.5, 70, 600, 150, 2050, 320, 160, 430, 7.5, 16, 5.6, 2500, 1500, 2200),
      ("WC67K-100t/3200", 1000, 3200, 260, 100, 7.5, 70, 600, 150, 2510, 320, 160, 430, 7.5, 16, 6.7, 3200, 1500, 2300),
      ("WC67K-100t/4000", 1000, 4000, 260, 120, 7.5, 70, 600, 150, 3100, 420, 160, 430, 7.5, 16, 8.4, 4000, 1500, 2400),
      ("WC67K/E-125t/2500", 1250, 2500, 260, 90, 7, 65, 600, 150, 2050, 320, 160, 430, 7.5, 16, 6.3, 2570, 1620, 2450),
      ("WC67K-125t/3200", 1250, 3200, 260, 95, 7, 65, 600, 150, 2510, 320, 160, 430, 7.5, 16, 7.1, 3200, 1600, 2350),
      ("WC67K-125t/4000", 1250, 4000, 260, 110, 7, 65, 600, 150, 3100, 420, 160, 430, 7.5, 16, 9, 4000, 1750, 2590),
      ("WC67K/E-125t/5000", 1250, 5000, 260, 120, 7, 65, 600, 150, 3800, 320, 160, 430, 7.5, 16, 11.5, 5000, 1600, 2450),
      ("WC67K/E-125t/6000", 1250, 6000, 260, 130, 7, 65, 600, 150, 4800, 320, 160, 430, 7.5, 16, 14.6, 6000, 1600, 2450),
      ("WC67K/E-160t/2500", 1600, 2500, 260, 110, 7, 75, 600, 150, 2050, 350, 200, 480, 11, 20, 8.6, 2500, 1650, 2700),
      ("WC67K-160t/3200", 1600, 3200, 260, 110, 7, 75, 600, 150, 2510, 350, 200, 480, 11, 20, 9.8, 3200, 1650, 2800),
      ("WC67K-160t/4000", 1600, 4000, 260, 110, 7, 75, 600, 150, 3100, 350, 200, 480, 11, 20, 11.5, 4000, 1650, 2800),
      ("WC67K/E-160t/5000", 1600, 5000, 260, 120, 7, 75, 600, 150, 3800, 350, 200, 480, 11, 20, 13.5, 5000, 1750, 3100),
      ("WC67K/E-160t/6000", 1600, 6000, 260, 120, 7, 75, 600, 150, 4800, 350, 200, 480, 11, 20, 16.5, 6000, 1750, 3300),
      ("WC67K-200T/3200", 2000, 3200, 435, 100, 8.5, 65, 600, 150, 2510, 350, 200, 480, 15, 32, 11.4, 3200, 1650, 2800),
      ("WC67K-200T/4000", 2000, 4000, 435, 100, 8.5, 65, 600, 150, 3100, 350, 200, 480, 15, 32, 13.7, 4000, 1650, 2800),
      ("WC67K/E-200T/5000", 2000, 5000, 435, 100, 8.5, 65, 600, 150, 3800, 350, 200, 480, 15, 32, 16.4, 5000, 1950, 3100),
      ("WC67K/E-200T/6000", 2000, 6000, 435, 100, 8.5, 65, 600, 150, 4800, 350, 200, 480, 15, 32, 22.5, 6000, 1950, 3100),
      ("WC67K-250T/3200", 2500, 3200, 435, 100, 8, 75, 600, 150, 2600, 400, 250, 580, 18.5, 40, 15.5, 3300, 2100, 3150),
      ("WC67K-250T/4000", 2500, 4000, 435, 100, 8, 75, 600, 150, 3100, 400, 250, 580, 18.5, 40, 17.6, 4000, 2100, 3150),
      ("WC67K/E-250T/5000", 2500, 5000, 435, 100, 8, 75, 600, 150, 3800, 400, 250, 580, 18.5, 40, 21, 5000, 2100, 3200),
      ("WC67K/E-250T/6000", 2500, 6000, 540, 100, 8, 75, 600, 150, 4800, 400, 250, 580, 18.5, 40, 23.5, 6000, 2100, 3200),
      ("WC67K-300T/3200", 3000, 3200, 540, 90, 8, 75, 600, 150, 2600, 400, 250, 580, 18.5, 40, 17.1, 3200, 2200, 3200),
      ("WC67K-300T/4000", 3000, 4000, 540, 100, 8, 75, 600, 150, 3100, 400, 250, 580, 18.5, 40, 18.8, 4000, 2200, 3200),
      ("WC67K/E-300T/5000", 3000, 5000, 540, 110, 8, 75, 600, 150, 3800, 400, 250, 580, 18.5, 40, 24, 5000, 2200, 3200),
      ("WC67K/E-300T/6000", 3000, 6000, 540, 130, 8, 75, 600, 150, 4800, 400, 250, 580, 18.5, 40, 28, 6000, 2200, 3200),
      ("WC67K/E-400T/3200", 4000, 3200, 540, 90, 7, 75, 600, 150, 2500, 400, 250, 580, 22, 50, 20.3, 3300, 2400, 3200),
      ("WC67K/E-400T/4000", 4000, 4000, 540, 90, 7, 75, 600, 150, 3100, 400, 250, 580, 22, 50, 23.8, 4000, 2400, 3200),
      ("WC67K/E-400T/5000", 4000, 5000, 550, 90, 7, 75, 850, 150, 3800, 400, 250, 580, 22, 50, 27.9, 5000, 2400, 3200),
      ("WC67K/E-400T/6000", 4000, 6000, 550, 90, 7, 75, 850, 150, 4800, 400, 250, 580, 22, 50, 33, 6000, 2400, 3200)]
NC_S, NC_M, NC_L = NC[:13], NC[13:22], NC[22:]


def nc_rows(data):
    return [("Bending force", [tons(r[1] / 10) for r in data]),
            ("Bending length", [length(r[2]) for r in data]),
            ("Distance between columns", [inch(r[9]) for r in data]),
            ("Throat depth", [inch(r[10]) for r in data]),
            ("Stroke", [inch(r[11]) for r in data]),
            ("Daylight", "open height", [inch(r[12]) for r in data]),
            ("Approach speed", [speed(r[4]) for r in data]),
            ("Bending speed", [speed(r[5]) for r in data]),
            ("Return speed", [speed(r[6]) for r in data]),
            ("Back gauge X stroke · speed", [f"{inch(r[7])} · {speed(r[8])}" for r in data]),
            ("Main motor", [hp(r[13]) for r in data]),
            ("Hydraulic oil tank", [gal(r[3]) for r in data]),
            ("Dimensions L × W × H", [dims(r[16], r[17], r[18]) for r in data]),
            ("Weight", [weight(round(r[15] * 1000)) for r in data])]


T_NC_S = table("NC press brakes · 30 – 125 t", "13 models · 33 – 138 US tons · 5 – 20 ft", [r[0] for r in NC_S], nc_rows(NC_S))
T_NC_C = table("Compact NC press brake · 5.2 ft", "1 model · 33 US tons", [NC[0][0]], nc_rows(NC[:1]))
T_NC_M = table("NC press brakes · 160 – 200 t", "9 models · 176 – 220 US tons · 8 – 20 ft", [r[0] for r in NC_M], nc_rows(NC_M))
T_NC_L = table("NC press brakes · 250 – 400 t", "12 models · 276 – 441 US tons · 10 – 20 ft", [r[0] for r in NC_L], nc_rows(NC_L))
T_NC = table("NC press brakes · 30 – 400 t", "34 models · 33 – 441 US tons · 5 – 20 ft", [r[0] for r in NC], nc_rows(NC))

# electric WADG: (model, kN, length, approach, bend, return, X stroke, X speed, R stroke, R speed, columns, throat, stroke, open, kW, weight t, L, W, H)
WADG = [("WADG-10T/500", 100, 500, 180, "0.15-30", 180, 200, 400, 80, 200, 510, 200, 150, 420, "5.5", 0.8, 640, 980, 1250),
        ("WADG-20T/800", 200, 800, 250, "0.15-30", 250, 400, 500, 150, 200, 680, 250, 150, 420, "15", 3.1, 1200, 1560, 2450),
        ("WADG-30T/1250", 300, 1250, 250, "0.15-30", 250, 400, 500, 150, 200, 900, 250, 150, 420, "20", 4.12, 1460, 1660, 2470),
        ("WADG-40T/1300", 400, 1300, 250, "0.15-30", 250, 400, 500, 150, 200, 920, 255, 150, 420, "2X15", 4.5, 1700, 2050, 2280),
        ("WADG-40T/1600", 400, 1600, 250, "0.15-30", 250, 400, 500, 150, 200, 920, 255, 150, 420, "2X15", 4.85, 1700, 2050, 2280),
        ("WADG-50T/1600", 500, 1600, 250, "0.15-30", 250, 400, 500, 150, 200, 1250, 255, 150, 420, "2X15", 4.9, 2200, 2050, 2280),
        ("WADG-60T/2000", 600, 2000, 250, "0.15-30", 250, 500, 500, 150, 200, 1600, 300, 200, 470, "2X20", 6, 2700, 2150, 2380),
        ("WADG-80T/2500", 800, 2500, 200, "0.15-30", 200, 500, 500, 150, 200, 2000, 460, 200, 470, "2X25", 8.9, 3000, 2250, 2380),
        ("WADG-100T/3200", 1000, 3200, 200, "0.15-30", 200, 500, 500, 150, 200, 2700, 460, 200, 470, "2X25", 10.7, 4000, 2450, 2580),
        ("WADG-160T/3200", 1600, 3200, 200, "0.15-30", 200, 500, 500, 150, 200, 2700, 460, 250, 520, "3X25", 11.8, 4000, 2450, 2780)]
WADG_MINI = [("WADG-3T/200", 30, 200, 200, "1-30", 200, 300, None, 120, 420, "2", 0.32, 700, 700, 1980),
             ("WADG-6T/400", 60, 400, 200, "1-30", 200, 370, 160, 120, 420, "3", 0.56, 750, 750, 1980),
             ("WADG-12T/600", 120, 600, 200, "1-30", 200, 450, 200, 120, 420, "5.5", 0.76, 850, 850, 2080)]
T_WADG = table("Electric servo press brakes · WADG", "10 models · 11 – 176 US tons · 1.6 – 10.5 ft", [r[0] for r in WADG], [
    ("Bending force", [tons(r[1] / 10) for r in WADG]),
    ("Bending length", [length(r[2]) for r in WADG]),
    ("Distance between columns", [inch(r[10]) for r in WADG]),
    ("Throat depth", [inch(r[11]) for r in WADG]),
    ("Stroke", [inch(r[12]) for r in WADG]),
    ("Daylight", "open height", [inch(r[13]) for r in WADG]),
    ("Approach / return speed", [speed(r[3]) for r in WADG]),
    ("Bending speed", "programmable", ["0.006 – 1.18 in/s (0.15 – 30 mm/s)"] * len(WADG)),
    ("Back gauge X stroke · speed", [f"{inch(r[6])} · {speed(r[7])}" for r in WADG]),
    ("Back gauge R stroke · speed", [f"{inch(r[8])} · {speed(r[9])}" for r in WADG]),
    ("Servo motors", [kw_hp(r[14]) for r in WADG]),
    ("Dimensions L × W × H", [dims(r[16], r[17], r[18]) for r in WADG]),
    ("Weight", [weight(round(r[15] * 1000)) for r in WADG])])
T_WADG_MINI = table("Compact electric servo press brakes", "3 models · 3.3 – 13 US tons · 8 – 24″", [r[0] for r in WADG_MINI], [
    ("Bending force", [tons(r[1] / 10) for r in WADG_MINI]),
    ("Bending length", [inch(r[2]) for r in WADG_MINI]),
    ("Distance between columns", [inch(r[6]) for r in WADG_MINI]),
    ("Throat depth", [inch(r[7]) if r[7] else "—" for r in WADG_MINI]),
    ("Stroke", [inch(r[8]) for r in WADG_MINI]),
    ("Daylight", "open height", [inch(r[9]) for r in WADG_MINI]),
    ("Approach / return speed", [speed(r[3]) for r in WADG_MINI]),
    ("Bending speed", "programmable", ["0.04 – 1.18 in/s (1 – 30 mm/s)"] * 3),
    ("Servo motor", [kw_hp(r[10]) for r in WADG_MINI]),
    ("Dimensions L × W × H", [dims(r[12], r[13], r[14]) for r in WADG_MINI]),
    ("Weight", [weight(round(r[11] * 1000)) for r in WADG_MINI])])
NOTE_EPB = ("Bending force in US tons (metric tons in brackets); the model number is the supplier's — metric tonnage × metric bending length. "
            "Servo-electric drive through belts and dual lead ball screws: no hydraulic oil, 0.15 – 30 mm/s programmable bending speed, power drawn only while the ram moves.")

# ------------------------------------------------------------------------------------------------ shears
# swing beam: (model, mm, length, oil, strokes/min, back gauge, angle, kW, pump, weight t, L, W, H)
QC = [("QC12K-4×2500", 4, 2500, 140, 33, "20–650", 1.5, 7.5, 25, 3.5, 3035, 1570, 1720), ("QC12K-4×3200", 4, 3200, 190, 26, "20–650", 1.5, 7.5, 25, 5.5, 3750, 1640, 1850),
      ("QC12K-4×4000", 4, 4000, 190, 23, "20–800", 1.5, 7.5, 25, 7.5, 4550, 1900, 1900), ("QC12K-4×5000", 4, 5000, 320, 16, "20–800", 1.5, 7.5, 25, 8.5, 5700, 1900, 2000),
      ("QC12K-4×6000", 4, 6000, 440, 12, "20–800", 1.5, 15, 32, 17, 6500, 2460, 2250),
      ("QC12K-6×2500", 6, 2500, 190, 17, "20–650", 2, 7.5, 25, 5.5, 3050, 1650, 1900), ("QC12K-6×3200", 6, 3200, 190, 17, "20–650", 1.5, 7.5, 25, 6.5, 3750, 1650, 1900),
      ("QC12K-6×4000", 6, 4000, 190, 15, "20–800", 1.5, 7.5, 25, 8.2, 4550, 2000, 2000), ("QC12K-6×5000", 6, 5000, 320, 11, "20–800", 1.5, 15, 32, 12.6, 5700, 2450, 2300),
      ("QC12K-6×6000", 6, 6000, 440, 8, "20–800", 1.5, 15, 32, 19.5, 6550, 2470, 2500),
      ("QC12K-8×2500", 8, 2500, 190, 13, "20–650", 2, 11, 32, 5.8, 3060, 1650, 1900), ("QC12K-8×3200", 8, 3200, 190, 13, "20–650", 1.5, 11, 32, 6.8, 3760, 1650, 1900),
      ("QC12K-8×4000", 8, 4000, 190, 12, "20–800", 1.5, 15, 32, 8.8, 4560, 1960, 1920), ("QC12K-8×5000", 8, 5000, 320, 10, "20–800", 1.5, 18.5, 40, 12.8, 5600, 2360, 2180),
      ("QC12K-8×6000", 8, 6000, 440, 9, "20–800", 1.5, 18.5, 40, 21.5, 6600, 2450, 2500),
      ("QC12K-10×2500", 10, 2500, 190, 13, "20–800", 2, 15, 32, 7, 3050, 2000, 1920), ("QC12K-10×3200", 10, 3200, 190, 13, "20–800", 1.5, 15, 32, 8.5, 3800, 2000, 1920),
      ("QC12K-10×4000", 10, 4000, 400, 9, "20–800", 1.5, 22, 50, 11.8, 4700, 2100, 2200), ("QC12K-10×6000", 10, 6000, 440, 6, "20–800", 1.5, 22, 50, 27.5, 6600, 2100, 2300),
      ("QC12K-12×2500", 12, 2500, 400, 12, "20–800", 2, 22, 50, 9.8, 3170, 2150, 2180), ("QC12K-12×3200", 12, 3200, 400, 10, "20–800", 2, 22, 50, 11.5, 3800, 2150, 2180),
      ("QC12K-12×4000", 12, 4000, 400, 8, "20–800", 1.75, 22, 50, 13.8, 4700, 2280, 2200), ("QC12K-12×5000", 12, 5000, 440, 6, "20–800", 2, 30, 63, 19, 5800, 2450, 2400),
      ("QC12K-12×6000", 12, 6000, 440, 5, "20–800", 2, 30, 63, 31, 6600, 2600, 2700),
      ("QC12K-16×2500", 16, 2500, 400, 13, "20–800", 2.5, 22, 50, 11, 3250, 2300, 2200), ("QC12K-16×3200", 16, 3200, 400, 10, "20–800", 2, 22, 50, 12.6, 3870, 2300, 2180),
      ("QC12K-16×4000", 16, 4000, 600, 9, "20–800", 1.75, 22, 50, 17, 4700, 2575, 2200), ("QC12K-16×5000", 16, 5000, 600, 7, "20–800", 2.5, 30, 63, 24, 5900, 2600, 2700),
      ("QC12K-16×6000", 16, 6000, 600, 5, "20–800", 2.5, 30, 63, 36.8, 6600, 2700, 2900),
      ("QC12K-20×2500", 20, 2500, 500, 8, "20–800", 2.5, 30, 80, 14.3, 3300, 2580, 2300), ("QC12K-20×3200", 20, 3200, 500, 7, "20–800", 2.5, 30, 80, 16, 4150, 2600, 2500),
      ("QC12K-20×4000", 20, 4000, 550, 5, "20–800", 2.5, 30, 80, 23, 4850, 2600, 2800)]
QC_S, QC_M, QC_L = QC[:10], QC[10:24], QC[24:]


def bg(r):
    a, b = r.split("–")
    return f"{int(a) / 25.4:.1f} – {int(b) / 25.4:.1f}″ ({r} mm)"


def qc_rows(data):
    return [("Cutting capacity, mild steel", "≤ 450 N/mm² · 65,000 psi", [cap(r[1]) for r in data]),
            ("Cutting length", [length(r[2]) for r in data]),
            ("Strokes per minute", [str(r[4]) for r in data]),
            ("Cutting angle", [f"{r[6]:g}°" for r in data]),
            ("Back gauge range", [bg(r[5]) for r in data]),
            ("Main motor", [hp(r[7]) for r in data]),
            ("Hydraulic oil tank", [gal(r[3]) for r in data]),
            ("Dimensions L × W × H", [dims(r[10], r[11], r[12]) for r in data]),
            ("Weight", [weight(round(r[9] * 1000)) for r in data])]


T_QC_S = table("Swing beam shears · 5/32″ and 1/4″", "10 models · 8 – 20 ft", [r[0] for r in QC_S], qc_rows(QC_S))
T_QC_M = table("Swing beam shears · 5/16″ to 15/32″", "14 models · 8 – 20 ft", [r[0] for r in QC_M], qc_rows(QC_M))
T_QC_L = table("Swing beam shears · 5/8″ and 3/4″", "8 models · 8 – 20 ft", [r[0] for r in QC_L], qc_rows(QC_L))

# guillotine: (model, mm, length, oil, strokes/min, back gauge, rake angle, kW, pump, weight t, L, W, H)
Q11 = [("Q11K-6×2500", 6, 2500, 300, "16 – 25", "20–800", "0.5° – 1.5°", "7.5", 20, 5.7, 3200, 1950, 2050), ("Q11K-6×3200", 6, 3200, 300, "14 – 20", "20–800", "0.5° – 1.5°", "7.5", 20, 6.6, 3900, 1950, 2075),
       ("Q11K-6×4000", 6, 4000, 340, "12 – 17", "20–800", "0.5° – 1.5°", "7.5", 20, 7.9, 4640, 2000, 2100), ("Q11K-6×5000", 6, 5000, 340, "8 – 14", "20–800", "0.5° – 1.5°", "11", 32, 14, 5780, 2100, 2380),
       ("Q11K-6×6000", 6, 6000, 340, "7 – 12", "20–800", "0.5° – 1.5°", "11", 32, 18.5, 6750, 2200, 2500),
       ("Q11K-8×2500", 8, 2500, 300, "13 – 20", "20–800", "0.5° – 1.5°", "11", 32, 6.2, 3150, 1970, 2055), ("Q11K-8×3200", 8, 3200, 300, "11 – 18", "20–800", "0.5° – 1.5°", "11", 32, 7.4, 3850, 2050, 2100),
       ("Q11K-8×4000", 8, 4000, 340, "9 – 16", "20–800", "0.5° – 1.5°", "15", 32, 10.4, 4650, 2100, 2400), ("Q11K-8×5000", 8, 5000, 350, "8 – 15", "20–800", "0.5° – 1.5°", "15", 32, 15.5, 5700, 1950, 2600),
       ("Q11K-8×6000", 8, 6000, 580, "7 – 14", "20–800", "0.5° – 1.5°", "15", 40, 20, 6750, 2250, 2615),
       ("Q11K-10×3200", 10, 3200, 300, "9 – 16", "20–800", "0.5° – 2.5°", "15", 32, 8.4, 3850, 1720, 2242), ("Q11K-10×4000", 10, 4000, 405, "10 – 16", "20–800", "0.5° – 2°", "22", 63, 12.1, 4680, 1895, 2335),
       ("Q11K-13×2500", 13, 2500, 405, "10 – 20", "20–800", "0.5° – 2°", "22", 63, 7.6, 3250, 1950, 2110), ("Q11K-13×3200", 13, 3200, 405, "9 – 18", "20–800", "0.5° – 2°", "22", 63, 10.3, 3900, 2070, 2315),
       ("Q11K-13×4000", 13, 4000, 405, "8 – 16", "20–800", "0.5° – 2°", "22", 63, 13.5, 4800, 2150, 2460), ("Q11K-13×5000", 13, 5000, 505, "7 – 14", "20–1000", "0.5° – 2°", "22", 63, 22, 5800, 2270, 2800),
       ("Q11K-13×6000", 13, 6000, 1020, "6 – 12", "20–1000", "0.5° – 2°", "37", 80, 27, 6950, 2450, 3050),
       ("Q11K-16×2500", 16, 2500, 475, "9 – 18", "20–800", "0.5° – 2.5°", "22", 63, 9.3, 3280, 2020, 2270), ("Q11K-16×3200", 16, 3200, 475, "8 – 17", "20–800", "0.5° – 2.5°", "22", 63, 12.2, 3950, 2150, 2450),
       ("Q11K-16×4000", 16, 4000, 595, "7 – 15", "20–800", "0.5° – 2.5°", "22", 63, 15, 4800, 2130, 2550), ("Q11K-16×5000", 16, 5000, 595, "5 – 11", "20–800", "0.5° – 2.5°", "30", 63, 22.5, 5810, 2330, 2780),
       ("Q11K-16×6000", 16, 6000, 1020, "6 – 11", "20–1000", "0.5° – 2.5°", "37", 80, 32.5, 7000, 2500, 3000), ("Q11K-16×8000", 16, 8000, 2060, "4 – 8", "20–1000", "0.5° – 2.5°", "45", 100, 62, 9050, 3180, 3500),
       ("Q11K-20×2500", 20, 2500, 510, "7 – 16", "20–800", "0.5° – 3°", "30", 63, 12.5, 3200, 2220, 2520), ("Q11K-20×3200", 20, 3200, 510, "6 – 15", "20–800", "0.5° – 3°", "30", 63, 14.1, 3950, 2150, 2600),
       ("Q11K-20×4000", 20, 4000, 640, "6 – 14", "20–800", "0.5° – 3°", "37", 80, 20.7, 4750, 2400, 2900), ("Q11K-20×6000", 20, 6000, 1500, "5 – 11", "20–1000", "0.5° – 3°", "2X30", "2 × 63", 44, 7000, 2850, 3350),
       ("Q11K-25×2500", 25, 2500, 750, "5 – 14", "20–800", "0.5° – 3.5°", "37", 80, 15, 3270, 2000, 2650), ("Q11K-25×3200", 25, 3200, 820, "5 – 10", "20–800", "0.5° – 3.5°", "37", 80, 18.5, 3970, 2200, 2670),
       ("Q11K-25×4000", 25, 4000, 1200, "5 – 8", "20–800", "0.5° – 3.5°", "45", 100, 26, 4900, 2800, 3190),
       ("Q11K-30×2500", 30, 2500, 780, "5 – 12", "20–1000", "0.5° – 3°", "45", 100, 21.5, 3450, 2500, 2900), ("Q11K-30×3200", 30, 3200, 1000, "4 – 10", "20–1000", "0.5° – 3°", "45", 100, 27, 4150, 2700, 2850),
       ("Q11K-30×4000", 30, 4000, 1400, "3 – 7", "20–1000", "0.5° – 3.5°", "55", 125, 35, 5200, 2600, 3350),
       ("Q11K-40×2500", 40, 2500, 1370, "4 – 8", "20–1000", "0.5° – 4°", "55", 125, 36.5, 4000, 2950, 3150)]
Q11_S, Q11_M, Q11_L = Q11[:10], Q11[10:23], Q11[23:]


def q11_rows(data):
    return [("Cutting capacity, mild steel", "≤ 450 N/mm² · 65,000 psi", [cap(r[1]) for r in data]),
            ("Cutting length", [length(r[2]) for r in data]),
            ("Cuts per minute", "at max / min angle", [r[4] for r in data]),
            ("Rake angle", "variable", [r[6] for r in data]),
            ("Back gauge range", [bg(r[5]) for r in data]),
            ("Main motor", [kw_hp(r[7]) for r in data]),
            ("Hydraulic oil tank", [gal(r[3]) for r in data]),
            ("Dimensions L × W × H", [dims(r[10], r[11], r[12]) for r in data]),
            ("Weight", [weight(round(r[9] * 1000)) for r in data])]


T_Q11_S = table("Guillotine shears · 1/4″ and 5/16″", "10 models · 8 – 20 ft", [r[0] for r in Q11_S], q11_rows(Q11_S))
T_Q11_M = table("Guillotine shears · 3/8″ to 5/8″", "13 models · 8 – 26 ft", [r[0] for r in Q11_M], q11_rows(Q11_M))
T_Q11_L = table("Guillotine shears · 3/4″ to 1-9/16″", "11 models · 8 – 20 ft", [r[0] for r in Q11_L], q11_rows(Q11_L))
SH_GK = ["capacity", "length", "strokes", "motor", "weight"]
SH_G_FROM_QC = ["Cutting capacity, mild steel", "Cutting length", "Strokes per minute", "Main motor", "Weight"]
SH_G_FROM_Q11 = ["Cutting capacity, mild steel", "Cutting length", "Cuts per minute", "Main motor", "Weight"]
NOTE_SH = ("Capacities are the supplier's ratings over the full blade length for mild steel of up to 65,000 psi (450 N/mm²); stainless steel runs about "
           "60 % of the mild-steel thickness, aluminum about 150 %. The model number is the metric thickness × cutting length. Dimensions are overall "
           "L (along the blade) × W × H; weights are reference values.")

# ------------------------------------------------------------------------------------------------ V-grooving
VG_H = [("3200 × 1250", 3200, 1250, 5300, 2250, 1650), ("4000 × 1250", 4000, 1250, 5800, 2250, 1650), ("4000 × 1500", 4000, 1500, 5800, 2500, 1650),
        ("5000 × 1250", 5000, 1250, 6800, 2250, 1650), ("5000 × 1500", 5000, 1500, 6800, 2500, 1650), ("6000 × 1250", 6000, 1250, 7800, 2250, 1650), ("6000 × 1500", 6000, 1500, 7800, 2500, 1650)]
VG_V = [("3200 × 1250", 3200, 1250, 5000, 2550, 2100), ("3200 × 1500", 3200, 1500, 5000, 2800, 2100), ("4000 × 1250", 4000, 1250, 5800, 2550, 2100), ("4000 × 1500", 4000, 1500, 5850, 2800, 2100)]


def vg_rows(data, thick, kw, bar):
    n = len(data)
    return [("Max. grooving length", [length(r[1]) for r in data]),
            ("Max. grooving width", "sheet width", [inch(r[2]) for r in data]),
            ("Sheet thickness", "min – max", [f"0.016″ – {thick} (0.4 – {thick_mm(thick)} mm)"] * n),
            ("Min. edge distance", [inch(8)] * n),
            ("Grooving speed", [f"up to {mmin(90)}"] * n),
            ("Return speed", [f"up to {mmin(120)}"] * n),
            ("Positioning accuracy", "X and Y", ["± 0.0004″ (± 0.01 mm) · 0.001 mm resolution"] * n),
            ("Main servo motor", [hp(kw)] * n),
            ("Hydraulic clamping pressure", [bar] * n),
            ("Dimensions L × W × H", [dims(r[3], r[4], r[5]) for r in data])]


def thick_mm(t):
    return {"5/32″": 4, "1/4″": 6}[t]


T_VG_H = table("Horizontal CNC V-grooving machines", "7 models · 10.5 – 20 ft × 49 – 59″ · to 5/32″ stainless", [r[0] for r in VG_H], vg_rows(VG_H, "5/32″", 5.5, "1,015 – 1,305 psi (7 – 9 MPa)"))
T_VG_V = table("Vertical CNC V-grooving machines", "4 models · 10.5 – 13 ft × 49 – 59″ · to 1/4″", [r[0] for r in VG_V], vg_rows(VG_V, "1/4″", 4.4, "870 – 1,160 psi (6 – 8 MPa)"))
VG_GK = ["length", "width", "thickness", "speed", "motor"]
VG_G_FROM = ["Max. grooving length", "Max. grooving width", "Sheet thickness", "Grooving speed", "Main servo motor"]
NOTE_VG = ("The model number is the metric grooving length × width. Maximum thickness is for stainless steel; mild steel and aluminum to about "
           "the same thickness. The horizontal machine lays the sheet flat on the table (longest sheets, four-tool head); the vertical machine stands it "
           "against the clamping beam (smaller footprint, thicker plate).")

# ------------------------------------------------------------------------------------------------ panel benders
# (model, ss mm, mild mm, alu mm, bend width, bend height, kW, min 4-side box, min 2-side, max blank, diagonal, weight t, axes, L, W, H)
PBM = [("PB-M1600", 1.5, 2, 3, 1600, 200, 38, "280 × 180", 180, "1,600 × 1,200", 2340, 12, 15, 4780, 2150, 2900),
       ("PB-M2100", 1.5, 2, 3, 2190, 200, 76, "280 × 180", 180, "2,190 × 1,200", 2854, 21, 15, 5650, 2750, 3200),
       ("PB-M2600", 1.5, 2, 3, 2610, 200, 108, "280 × 180", 180, "2,610 × 1,200", 3240, 24, 15, 6100, 3250, 3300),
       ("PB-M3200", 1.5, 2, 3, 3200, 200, 154, "280 × 180", 180, "3,200 × 1,200", 3794, 28, 17, 6900, 4100, 3500),
       ("PB-M4200", 1.5, 2, 2.5, 4200, 200, 182, "280 × 220", 220, "4,200 × 1,200", 4752, 36, 19, 8000, 5100, 3600),
       ("PB-M2100-300", 1, 1.5, 2, 2100, 300, 76, "280 × 180", 180, "2,100 × 1,200", 3036, 21, 15, 5800, 2600, 3500),
       ("PB-M2600-300", 1, 1.5, 2, 2600, 300, 108, "280 × 180", 180, "2,600 × 1,200", 3426, 25, 15, 6300, 3150, 3550),
       ("PB-MH2100", 1, 1.5, 2, 2100, 200, 53, "280 × 180", 180, "2,100 × 1,400", 2854, 17.5, 15, 5650, 2650, 3200),
       ("PB-MH2600", 1, 1.5, 2, 2600, 200, 66, "280 × 180", 180, "2,600 × 1,400", 3240, 21, 15, 5650, 3150, 3200)]
PBA = [("PB-A1630", 1.5, 2, 3, 1630, 200, 44, "370 × 180", 180, "1,600 × 1,200", 2340, 12, 26, 4780, 2750, 2900),
       ("PB-A2190", 1.5, 2, 3, 2190, 200, 89, "370 × 180", 180, "2,190 × 1,200", 2854, 21, 26, 5650, 3650, 3200),
       ("PB-A2610", 1.5, 2, 3, 2610, 200, 118, "370 × 180", 180, "2,610 × 1,250", 3240, 24, 26, 6100, 4100, 3350),
       ("PB-A3200", 1.5, 2, 2.5, 3200, 200, 165, "390 × 180", 180, "3,200 × 1,250", 3794, 28, 28, 6900, 4200, 3500)]


def ga(mm):
    return {3: "1/8″ (3.0 mm)", 2.5: "3/32″ (2.5 mm)", 2: "14 ga (2.0 mm)", 1.5: "16 ga (1.5 mm)", 1: "20 ga (1.0 mm)"}[mm]


def box(s):
    a, b = [int(x) for x in s.replace(" ", "").split("×")]
    return f"{a / 25.4:.1f} × {b / 25.4:.1f}″ ({s} mm)"


def blank(s):
    a, b = [int(x.replace(",", "")) for x in s.replace(" ", "").split("×")]
    return f"{a / 25.4:.0f} × {b / 25.4:.0f}″ ({s} mm)"


def pb_rows_panel(data):
    return [("Max. bending width", [inch(r[4]) for r in data]),
            ("Max. blank size L × W", [blank(r[9]) for r in data]),
            ("Max. bending height", [inch(r[5]) for r in data]),
            ("Max. thickness, mild steel", [ga(r[2]) for r in data]),
            ("Max. thickness, stainless steel", [ga(r[1]) for r in data]),
            ("Max. thickness, aluminum", [ga(r[3]) for r in data]),
            ("Min. thickness", ["0.014″ (0.35 mm)"] * len(data)),
            ("Min. four-side box, inside", [box(r[7]) for r in data]),
            ("Min. two-side box, inside", [inch(r[8]) for r in data]),
            ("Blank diagonal, max.", [inch(r[10]) for r in data]),
            ("Bending speed", ["0.2 s per bend"] * len(data)),
            ("Servo axes", [str(r[12]) for r in data]),
            ("Installed power", [hp(r[6]) for r in data]),
            ("Noise", ["about 50 dB"] * len(data)),
            ("Dimensions L × W × H", [dims(r[13], r[14], r[15]) for r in data]),
            ("Weight", [f"about {weight(round(r[11] * 1000))}" for r in data])]


T_PBM = table("PB-M press-arm panel benders", "9 models · 63 – 165″ bend width · 14 ga mild steel", [r[0] for r in PBM], pb_rows_panel(PBM))
T_PBA = table("PB-A automatic tool-change panel benders", "4 models · 64 – 126″ bend width · 14 ga mild steel", [r[0] for r in PBA], pb_rows_panel(PBA))
PN_GK = ["bending_width", "thickness", "bending_height", "speed", "weight"]
PN_G_FROM = ["Max. bending width", "Max. thickness, mild steel", "Max. bending height", "Bending speed", "Weight"]
NOTE_PN = ("Capacities are the supplier's ratings; the model number is the metric bending width (-300: 300 mm bending height; MH: 1,400 mm deep blank). "
           "Minimum box sizes and blank sizes are approximate and depend on the tooling fitted.")

# ------------------------------------------------------------------------------------------------ ironworker
# (model, t, shear plate mm, angle°, max shear t×w, stroke, spm, throat, punch thickness, punch Ø, kW, L, W, H, round, square, angle 90, angle 45, tee 90, tee 45, joist, channel)
IW = [("Q35Y-50", 50, 12, 7, "300 × 12", 35, "10 – 18", 115, 12, 25, "4", 950, 550, 1800, None, None, None, None, None, None, None, None),
      ("Q35Y-60", 60, 16, 7, "250 × 16 · 400 × 8", 80, "9 – 25", 300, 16, 25, "5.5", 1640, 730, 1770, 45, 40, "120×120×12", "50×50×5", "120×120×12", "60×60×8", "126×74×5", "126×53×5"),
      ("Q35Y-90", 90, 20, 8, "330 × 20 · 480 × 10", 80, "12 – 28", 355, 20, 30, "7.5", 1860, 800, 1900, 50, 50, "140×140×12", "70×70×7", "140×140×12", "70×70×10", "160×86×6", "160×60×5"),
      ("Q35Y-120", 120, 25, 8, "330 × 25 · 600 × 16", 80, "12 – 28", 400, 25, 35, "11", 2355, 960, 2090, 60, 50, "160×160×14", "80×80×7", "160×160×14", "80×80×10", "200×102×9", "200×75×9"),
      ("Q35Y-160", 160, 30, 8, "335 × 30 · 600 × 20", 80, "12 – 28", 600, 28, 38, "11", 2680, 1040, 2300, 65, 55, "180×180×16", "80×80×10", "180×180×16", "80×80×10", "280×124×10", "280×86×11"),
      ("Q35Y-200", 200, 40, 8, "400 × 35 · 700 × 25", 80, "10", 600, 35, 40, "15", 2970, 1240, 2350, 70, 60, "200×200×18", "100×100×10", "200×200×18", "80×80×10", "300×126×11", "300×89×12"),
      ("Q35Y-250", 250, 50, 8, "400 × 40 · 750 × 30", 80, "10", 600, 40, 40, "18.5", 3000, 1440, 2450, 75, 65, "200×200×18", "120×120×16", "200×200×18", "80×80×10", "320×130×10", "300×92×12")]


def sec(s):
    """'120×120×12' → 4.7 × 4.7 × 15/32″ (120×120×12 mm): legs in decimal inches, thickness as the nearest fraction"""
    if not s:
        return "—"
    *legs, t = [int(x) for x in s.split("×")]
    return " × ".join(f"{v / 25.4:.1f}" for v in legs) + f" × {CAPS.get(t, f'{t / 25.4:.2f}″')} ({s} mm)"


def shear_size(s):
    out = []
    for part in s.split("·"):
        w, t = [int(x) for x in part.strip().split("×")]
        out.append(f"{w / 25.4:.1f} × {CAPS.get(t, f'{t / 25.4:.2f}″')}")
    return " · ".join(out) + f" ({s} mm)"


T_IW = table("Q35Y hydraulic ironworkers", "7 models · 55 – 276 US tons", [r[0] for r in IW], [
    ("Punching force", [tons(r[1]) for r in IW]),
    ("Punching, max. thickness", [cap(r[8]) for r in IW]),
    ("Punching, max. Ø", [f"Ø{r[9] / 25.4:.2f}″ ({r[9]} mm)" for r in IW]),
    ("Flat bar shear, max. thickness", [cap(r[2]) for r in IW]),
    ("Flat bar shear, width × thickness", [shear_size(r[4]) for r in IW]),
    ("Bar shear — round · square", [f"Ø{r[14] / 25.4:.2f}″ · □{r[15] / 25.4:.2f}″ ({r[14]} · {r[15]} mm)" if r[14] else "—" for r in IW]),
    ("Angle shear 90°", [sec(r[16]) for r in IW]),
    ("Angle shear 45°", [sec(r[17]) for r in IW]),
    ("Tee shear 90° · 45°", [f"{sec(r[18])} · {sec(r[19])}" if r[18] else "—" for r in IW]),
    ("I-beam · channel shear", [f"{sec(r[20])} · {sec(r[21])}" if r[20] else "—" for r in IW]),
    ("Shear angle", [f"{r[3]}°" for r in IW]),
    ("Ram stroke", [inch(r[5]) for r in IW]),
    ("Strokes per minute", [r[6] for r in IW]),
    ("Throat depth", [inch(r[7]) for r in IW]),
    ("Main motor", [hp(float(r[10])) for r in IW]),
    ("Dimensions L × W × H", [dims(r[11], r[12], r[13]) for r in IW])])
IW_GK = ["force", "punching", "angle", "flat", "motor"]
IW_G_FROM = ["Punching force", "Punching, max. thickness", "Angle shear 90°", "Flat bar shear, max. thickness", "Main motor"]
NOTE_IW = ("Capacities are the supplier's ratings for steel of up to 65,000 psi (450 N/mm²); the Q35Y-50 is the compact single-station bench model, "
           "the Q35Y-60 and up have the five stations and the section-shear capacities shown. The model number is the metric tonnage.")

# ------------------------------------------------------------------------------------------------ families
PB_STD = ["Delem DA-53Tx 15″ touch-screen CNC control; 4 axes — Y1, Y2 (independent ram cylinders), X and R back gauge",
          "Electro-hydraulic servo synchronisation: Hawe (Germany) valves, linear scales on both sides, ± 0.01 mm ram repeatability",
          "Mild hybrid drive as standard: a servo motor and servo pump in place of the conventional motor and pump — the pump turns only while the ram "
          "moves and stops while the machine waits, loads or unloads: 40 – 60 % less energy, cooler oil, about 60 dB, longer life for the pump, seals and valves",
          "Servo back gauge on ball screws and linear guides, ± 0.01 mm; two stop fingers with four positioning steps",
          "Motorised CNC crowning (V axis) on 110 t and up; Schneider electrics; Estun servo drives",
          "Manual top-tool clamps, a segmented 2-V die and a sectioned punch set (42CrMo, HRC 47); front support arms on linear rail",
          "Side guards, enclosed rear guard, anti-panic foot pedal with emergency stop", VOLT]
PB_OPT = ["Delem DA-58Tx (18.5″ 2D graphic), DA-66S (24″ 2D with 3D view) or DA-69S (24″ 3D) control; ESA S840 or S875 W; Cybelec CybTouch 12; SCS920 21.5″",
          "6-axis back gauge X1, X2, R1, R2, Z1, Z2 on ball screws; back gauge strokes to 39″ (1,000 mm)",
          "DSP laser finger protection (EN 12622 CAT 4 / SIL 3) or light curtains", "CNC sheet follower supports", "Quick-release top clamps, double-sided quick clamps or Rolleri pneumatic clamps; Wila hydraulic clamping",
          "Automatic angle measurement", "Hydraulic oil cooler; automatic lubrication", "Tandem machines on one control; robot bending cells", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
NC_STD = ["Estun E21PS NC control — programs the back gauge (X) and ram depth (Y), 40 programs × 25 steps, one-way / two-way positioning, stroke counter; inches or millimetres",
          "Torsion-bar synchronised ram with mechanical depth stops — simple, rigid and easy to service",
          "Motorised X back gauge on ball screw and linear guide, 23.6″ (600 mm) stroke; manual crowning",
          "Welded, stress-relieved monoblock frame machined in one setting; Rexroth-type hydraulic block; Schneider electrics",
          "Manual top-tool clamps, segmented 2-V die and sectioned punch set; front support arms", "Side and rear guards; foot pedal with emergency stop", VOLT]
NC_OPT = ["Estun E315PS 15.6″ touch NC control (6+1 axes, tool and material database), Delem DA-41T 7″ touch or ESA S630 10″ touch control", "Y-axis CNC upgrade (closed-loop ram) to the WAD series", "DSP laser finger protection or light curtain",
          "Sheet follower support; longer back gauge", "Hydraulic oil cooler", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
EPB_STD = ["Servo motors driving the ram through timing belts (Maco, Italy) and dual lead ball screws — no hydraulic oil, no pump, no valves",
           "± 0.01 mm ram repeatability from Givi / Fagor magnetic scales on both sides; 95 % transmission efficiency, about 70 % less energy",
           "Programmable bending speed 0.15 – 30 mm/s; 180 – 250 mm/s approach and return",
           "Delem DA-53Tx 15″ touch CNC control; X and R back gauge axes on HIWIN linear guides and TBI ball screws, Inovance servo drives",
           "Manual top-tool clamps and 2-V die with segmented punch; Schneider electrics; NACHI bearings; automatic lubrication",
           "Light curtain, side and rear guards, foot pedal with emergency stop", VOLT]
EPB_OPT = ["Delem DA-58Tx 2D graphic, DA-66S or DA-69S control; ESA S840 or S875 W; Cybelec CybTouch 12", "Wila hydraulic clamping; DSP laser finger protection", "Angle measurement; CNC crowning on 60 t and up",
           "Robot bending cell with Estun robot", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
QC_STD = ["Estun E21S NC control: motorised back gauge, cutting-angle and blade-gap setting, stroke counter, 40 programs × 25 steps, inches or millimetres",
          "Swing beam on two cylinders with accumulator return; Rexroth hydraulic valve block with pressure gauge and overload protection",
          "Motorised back gauge on ball screws, 0.8 – 25.6″ (20 – 650 mm), 31.5″ (800 mm) on 13 ft and up, with support fingers and retract",
          "Hydraulic hold-downs every 100 mm; four-edge rectangular blades; manual single-point blade-gap adjustment",
          "Shadow-line light, ball-transfer front tables, squaring arm, front guard with light barrier, rear safety barrier", "Siemens or Wannan main motor; Schneider electrics; NOK seals", VOLT]
QC_OPT = ["Estun E200PS or Delem DAC-360T control with programmable blade gap", "Pneumatic sheet support (return of the cut piece)", "Longer front support arms; roller tables",
          "Hydraulic oil cooler; automatic lubrication", "Spare blade set", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
Q11_STD = ["Estun E21S NC control: motorised back gauge, variable rake angle and blade gap set from the control, stroke counter, inches or millimetres",
           "Guillotine beam on linear rollers with a variable rake angle — thin sheet cut fast and flat at 0.5°, thick plate at the high angle with less distortion",
           "Motorised ball-screw back gauge to 31.5″ (800 mm), 39.4″ (1,000 mm) on the large machines, with sheet support",
           "Hydraulic hold-downs; four-edge blades; Rexroth valve block with overload protection; accumulator return",
           "Shadow-line light, ball-transfer front tables, squaring arm, front guard with light barrier, rear safety barrier", "Siemens or Wannan main motor; Schneider electrics", VOLT]
Q11_OPT = ["Delem DAC-360T or Estun E200PS control", "Pneumatic sheet support; conveyor for cut strips", "Longer front support arms; roller tables", "Hydraulic oil cooler", "Spare blade set",
           "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
VG_STD = ["4-axis CNC with a 15″ touchscreen and Taiwan servo motors — program groove depth, pitch and position, the machine runs the sheet",
          "Four-tool grooving head on ball screws, 0.001 mm resolution, ± 0.01 mm positioning; alloy cutters, double-nozzle chip blowing",
          "Hydraulic blank holder (Yuken, Japan) that clamps without marking; rack-and-pinion and ball-screw drives",
          "60 mm low-alloy steel beam and Q345 base, stress-relieved, ± 0.03 mm bed flatness", "Automatic lubrication; air-cooled servo cabinet", VOLT]
VG_OPT = ["Table lengths to 20 ft (6 m), widths 49″ or 59″", "Extra cutter sets; special profile cutters", "Dust extraction", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
PN_STD_M = ["15 servo axes with 0.01° resolution: upper and lower bending blades, blank-holder, press arm and the sheet manipulator",
            "0.2 s per bend; mild steel to 14 ga, stainless to 16 ga, aluminum to 1/8″; bending height 7.9″ (200 mm)",
            "Three-point Y positioning with suction-cup manipulator; the patented press arm feeds and supports the blank",
            "Cast QT500 / HT300 frame, stress-relieved and vibration-aged; automatic lubrication", "CNC with a 10,000-part process library and ESA control option; offline programming, remote monitoring",
            "Standard and hemming tools; perimeter guarding and light curtains", VOLT]
PN_STD_A = ["Automatic tool change — 0.5 s per change, 24 – 28 servo axes: the tool set reconfigures itself for every side of the part",
            "0.2 s per bend; mild steel to 14 ga, stainless to 16 ga, aluminum to 1/8″; ± 0.1 mm thickness detection", "Suction-cup manipulator with rotation; press-arm feeding",
            "Cast QT500 / HT300 frame, stress-relieved and vibration-aged; automatic lubrication", "CNC with process library, ESA control option, offline programming, cloud monitoring; robot interface",
            "Perimeter guarding and light curtains", VOLT]
PN_OPT = ["Robot or gantry loading and unloading, sheet stacks and pallets", "300 mm bending height (-300 models); 1,400 mm deep blanks (MH models)", "Extra bending and hemming tools", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
IW_STD = ["Five stations: punching, flat-bar shear, angle shear at 90° and 45°, round / square bar shear and rectangular notching — each with hold-down and guard",
          "Single cylinder with adjustable stroke and two foot pedals; strokes per minute as the table", "Punch and die, flat-bar blades, angle blades, bar blades and notching blades included",
          "Hydraulic valve block with overload protection; Schneider electrics; LED lighting at the stations", "Travel-limit switches and interlocked guards", VOLT]
IW_OPT = ["Tee, I-beam and channel blades; V-notching; pipe notching; bending tools", "Large-hole and section punching tools; punch sets", "Back gauge for the shear station; length stops", "Custom voltage: 208 V, 240 V or 480 V 3-phase"]
LINE = "NovoTech value line — built in China to North American standards and sold under NovoTech's name"

# the controls the value line is built with — a short note under every press brake (the buying guide on press-brake.html compares them)
CTL_WAD = {"title": "Delem DA-53Tx as standard; DA-58Tx, DA-66S, DA-69S, ESA S840 / S875 W, Cybelec CybTouch 12 or SCS920 to order",
           "text": "The value-line CNC brakes ship with the 15″ Delem DA-53Tx — touch-screen numeric programming with a 2D tool and product view, "
                   "crowning and servo control, up to 4 axes — the control most Canadian job shops know. Order the machine with the 18.5″ "
                   "DA-58Tx (2D graphic programming with automatic bend sequence and collision check), the 24″ DA-66S (2D with a 3D machine view) "
                   "or DA-69S (full 3D), the ESA S840 (15.6″, 6 axes) or S875 W (21.5″ 3D), the Cybelec CybTouch 12 (12″ 2D) or the SCS920 "
                   "(21.5″, 6+1 axes) when the work calls for graphic programming, more axes or a control your operators already run.",
           "images": ["ctl-delem-da53tx", "ctl-delem-da58tx", "ctl-delem-da66s", "ctl-delem-da69s", "ctl-esa-s840-card", "ctl-esa-s875w-card", "ctl-cybelec-ct12", "ctl-scs920"]}
CTL_NC = {"title": "Estun E21PS as standard; Estun E315PS, Delem DA-41T or ESA S630 to order",
          "text": "The torsion-bar brakes carry the Estun E21PS: a two-axis NC that positions the back gauge (X) and the ram depth (Y) from 40 stored "
                  "programs of 25 steps, with one-way or two-way positioning, retract, a stroke counter and inch / mm display — simple to learn in "
                  "an hour. For angle programming and a tool and material database, the 15.6″ touch Estun E315PS (6+1 axes), the 7″ touch Delem "
                  "DA-41T (100 programs, angle programming) or the 10″ ESA S630 (2D, 4 axes) can be fitted instead.",
          "images": ["ctl-estun-e21ps", "ctl-estun-e315ps", "ctl-delem-da41t", "ctl-esa-s630"]}
CTL_EPB = {"title": "Delem DA-53Tx as standard; DA-58Tx, DA-66S, DA-69S, ESA S840 / S875 W or Cybelec CybTouch 12 to order",
           "text": "The electric brakes use the same 15″ Delem DA-53Tx as the hydraulic CNC line, driving the servo ram and the X-R back gauge; "
                   "the 2D graphic DA-58Tx, the 24″ DA-66S and DA-69S, the ESA S840 and S875 W and the Cybelec CybTouch 12 are the options.",
           "images": ["ctl-delem-da53tx", "ctl-delem-da58tx", "ctl-delem-da66s", "ctl-delem-da69s", "ctl-esa-s875w-card", "ctl-cybelec-ct12"]}

HPB_FAMILIES = [
    dict(id="vl-wad", control=CTL_WAD, group="pb-cnc", page=P_HPB, brand=BRAND,
         name="CNC hydraulic press brakes, 55 – 331 US tons × 4 – 20 ft",
         short="CNC press brakes 50 – 300 t",
         models_label="WAD-50T/1300 – WAD-300T/6000 · 25 models",
         summary="The value-line CNC press brake: electro-hydraulic servo synchronisation with Hawe valves and linear scales, a servo-driven pump that "
                 "only runs while the ram moves, a Delem DA-53Tx control and a servo back gauge on ball screws — the same architecture as the European "
                 "machines, built to a price that lets a small shop own a real CNC brake. Twenty-five models on one design, from 55 US tons × 4 ft to "
                 "331 US tons × 20 ft: the 110 and 135 t × 10 ft machines are the ones most Canadian shops ask for; from 170 t up the machines have "
                 "17.7 – 19.7″ throats, 7.9 – 9.8″ strokes and 18.9 – 22.4″ daylight for deep boxes, with 25 – 40 cc pumps and 13 – 21 kW servo main "
                 "motors, and the 220 and 250 t × 13 ft bend 3/8″ plate the full length. Delem DA-53Tx standard with 4+1 axes and CNC crowning; "
                 "DA-58Tx, DA-66S / 69S controls, 6-axis back gauges, DSP laser protection, sheet followers and Wila clamping are options.",
         features=["Mild steel to 1/4″ over 10 ft on the 110 t, 5/16″ on the 135 t, 3/8″ over 13 ft on the 220 t and 1/2″ over 13 ft on the 300 t (V = 8 × thickness)"] + PB_STD,
         optional=PB_OPT,
         images=["vl-wad-1", "vl-wad-2", "vl-wade-1", "vl-wad-robot", "vl-pb-da53", "vl-pb-da58", "vl-pb-backgauge", "vl-pb-clamps", "vl-pb-quickclamp",
                 "vl-pb-hydclamp", "vl-pb-clamp-open", "vl-pb-cylinders", "vl-pb-fingers", "vl-pb-servo-bg", "vl-pb-crowning", "vl-pb-dsp", "vl-pb-follower-detail"],
         videos=vids(("gYyQIv5HRME", "WAD-110T/3200 CNC press brake — 10 ft × 121 US tons, Delem DA-53TX, mild-hybrid servo drive")),
         # the die-alignment video (KyNWOyaBKDM) was filmed on a Dener brake: off the WAD section (owner, Oct 30 2026); the channel's
         # WADE / DSP-laser videos show the supplier's badges, so they stay off the page too
         specs=spec([T_WAD], PB_GK, PB_G_FROM, NOTE_PB)),
    dict(id="vl-wad-heavy", control=CTL_WAD, group="pb-cnc", page=P_HPB, brand=BRAND,
         name="Heavy-duty CNC press brakes, 441 – 1,323 US tons × 13 – 26 ft, and tandems",
         short="Heavy-duty & tandem press brakes",
         models_label="WAD-400T/4000 – WAD-1200T/8000 · 21 models · tandem to 60 ft",
         summary="For plate work, poles, towers and long profiles: 400 to 1,200 t machines with 13, 16, 20, 23 and 26 ft beds, 23.6″ throats, strokes "
                 "to 15.7″ and 36″ daylight, twin pumps and twin servo motors from 800 t up, and a 38.6″ (980 mm) back gauge stroke as standard. CNC "
                 "sheet followers, extra-long front supports and tandem configurations — two machines on one control bending to 60 ft — are built to "
                 "order; the 3,000 t × 30 ft machine in the photos shows how far the range goes.",
         features=["Twin cylinders and twin pumps from 800 t; 38.6″ (980 mm) X back gauge stroke; 11 – 15 ft bed widths"] + PB_STD,
         optional=PB_OPT + ["Extra-long front supports and CNC sheet followers for plate", "Tandem and tridem machines to 60 ft on one control"],
         images=["vl-wad-heavy", "vl-wad-follower", "vl-wad-tandem", "vl-wad-tandem-2"],
         videos=[],
         specs=spec([T_WAD_H1, T_WAD_H2], PB_GK, PB_G_FROM, NOTE_PB)),
    dict(id="vl-nc", control=CTL_NC, group="pb-nc", page=P_HPB, brand=BRAND,
         name="NC hydraulic press brakes, 33 – 441 US tons × 5 – 20 ft — torsion bar",
         short="NC press brakes 30 – 400 t",
         models_label="WC67K-30t/1600 – WC67K/E-400T/6000 · 34 models",
         summary="The simplest press brake we sell: a torsion bar keeps the two ram cylinders in step mechanically, mechanical stops set the depth "
                 "and an Estun E21PS control positions the back gauge and the ram for 40 stored programs. No servo valves, no linear scales — nothing "
                 "that needs a technician — which is why these machines run for decades in general fabrication shops bending brackets, boxes, "
                 "channels, roofing and plate. Thirty-four models on one design, from 33 tons × 5 ft to 441 tons × 20 ft: the 100 t × 10 ft and "
                 "125 t × 13 ft are the standard sizes, and from 160 t up the machines have 13.8 – 15.7″ throats, 7.9 – 9.8″ strokes, 18.9 – 22.8″ "
                 "daylight, 20 – 50 cc pumps and 11 – 22 kW motors for 3/8″ and 1/2″ plate in simple shapes.",
         features=["Mild steel to 1/4″ over 10 ft on the 100 t, 5/16″ over 10 ft on the 125 t, 3/8″ over 10 ft on the 200 t, 1/2″ over 13 ft on the 300 t "
                   "and 1/2″ over 20 ft on the 400 t (V = 8 × thickness)"] + NC_STD,
         optional=NC_OPT,
         images=["vl-nc-1", "vl-nc-backgauge", "vl-nc-torsion", "vl-nc-bg-motor", "vl-nc-photo-1", "vl-nc-photo-2", "vl-nc-photo-3"],
         videos=vids(("0imM4bArpBc", "5 ft × 50 ton hydraulic press brake with Estun NC control")),
         specs=spec([T_NC], PB_GK, PB_G_FROM, NOTE_PB)),
]

COMPACT_FAMILIES = [
    dict(id="vl-wad-compact", control=CTL_WAD, group="pb-compact-cnc", page=P_HPB, brand=BRAND,
         name="Compact CNC hydraulic press brakes, 55 US tons × 4.3 and 5.2 ft",
         short="Compact CNC press brakes 50 t",
         models_label="WAD-50T/1300 · WAD-50T/1600 · 2 models",
         summary="The two smallest WAD machines are the value line's compact CNC press brakes: 50 metric tons (55 US tons) over 1,300 or "
                 "1,600 mm (4.3 and 5.2 ft), 44 or 51″ between the frames, a 9.8″ throat, 5.9″ stroke and 18.1″ daylight, on a 69 – 85 × 59″ "
                 "footprint at 7,700 lb. The same electro-hydraulic servo architecture as the big machines — Hawe valves, linear scales on "
                 "both sides, a servo-driven pump that only runs while the ram moves, Y1-Y2-X-R axes and the 15″ Delem DA-53Tx — with a "
                 "sectioned punch set and a 2-V die in the crate. Mild steel to 1/8″ (3 mm) over the full length and 5/32″ (4 mm) over 4.3 ft; stainless to 3/32″. For "
                 "enclosures, HVAC fittings, brackets and small-part production where a 10 ft machine would stand idle — and the lowest-priced "
                 "real CNC press brake NovoTech sells.",
         headline="55 US tons × 4.3 / 5.2 ft · 4 axes · Delem DA-53Tx · 7,700 lb · servo pump",
         features=["Mild steel to 1/8″ (3 mm) over the full length and 5/32″ (4 mm) over 4.3 ft (V = 8 × thickness); 44 / 51″ (1,120 / 1,300 mm) between the frames",
                   "9.8″ (250 mm) throat, 5.9″ (150 mm) stroke, 18.1″ (460 mm) daylight; 19.7″ (500 mm) X back gauge travel",
                   "4.4 kW (6 HP) servo main motor on a 13 cc pump — the quietest and most frugal CNC brake in the range"] + PB_STD,
         optional=PB_OPT,
         images=["vl-cp-wad1600", "vl-cp-wad1300", "vl-cp-clamps", "vl-cp-backgauge", "vl-cp-fingers", "vl-cp-laser", "vl-cp-servo", "vl-cp-finger-drive",
                 "vl-cp-pump-motor", "vl-cp-hawe", "vl-cp-valve", "vl-cp-hydraulics", "vl-cp-rear", "vl-cp-front-supports", "vl-cp-rear-gauge", "vl-cp-cabinet",
                 "vl-cp-clamps-2", "vl-cp-fingers-2"],
         videos=[],
         specs=spec([T_WAD_C], PB_GK, PB_G_FROM, NOTE_PB)),
    dict(id="vl-nc-compact", control=CTL_NC, group="pb-compact-nc", page=P_HPB, brand=BRAND,
         name="Compact NC hydraulic press brake, 33 US tons × 5.2 ft — torsion bar",
         short="Compact NC press brake 30 t",
         models_label="WC67K-30T/1600 · 1 model",
         summary="The smallest torsion-bar press brake: 30 metric tons (33 US tons) over 1,600 mm (5.2 ft), 51″ between the frames, a 7.9″ "
                 "throat and 13.2″ daylight, 4,630 lb on a 71 × 47″ footprint. A torsion bar keeps the two cylinders in step, mechanical "
                 "stops set the depth and the Estun E21PS control positions the back gauge and the ram for 40 stored programs — nothing "
                 "that needs a technician. Mild steel to 14 ga (2 mm) over the full length and 1/8″ (3 mm) over 4 ft. The press brake for a maintenance shop, a "
                 "sign maker or a small fabricator bending brackets, boxes and channels in one material, at the lowest price of any "
                 "powered press brake we sell.",
         headline="33 US tons × 5.2 ft · torsion bar · Estun E21PS · 4,630 lb",
         features=["Mild steel to 14 ga (2 mm) over 5.2 ft and 1/8″ (3 mm) over 4 ft (V = 8 × thickness); 51″ (1,300 mm) between the frames, 7.9″ (200 mm) throat, 13.2″ (335 mm) daylight",
                   "23.6″ (600 mm) motorised X back gauge on ball screw and linear guide; 5.5 kW (7.5 HP) motor"] + NC_STD,
         optional=NC_OPT,
         # frames of the WC67K video (captured in the browser, the supplier's logo painted out) for the operator controls, pedal and
         # back gauge; the generic back-gauge-motor photo gave way to the real drive
         images=["vl-cp-nc-adh", "vl-cp-e21", "vl-cp-nc-buttons", "vl-cp-nc-pedal", "vl-cp-nc-bg-fingers", "vl-cp-nc-bg-drive",
                 "vl-cp-nc-cabinet", "vl-cp-nc-screw", "vl-cp-nc-valve", "vl-nc-torsion"],
         videos=vids(("0imM4bArpBc", "5 ft × 50 ton hydraulic press brake with Estun NC control")),
         specs=spec([T_NC_C], PB_GK, PB_G_FROM, NOTE_PB)),
]

EPB_FAMILIES = [
    dict(id="vl-wadg", control=CTL_EPB, group="pb-electric", page=P_EPB, brand=BRAND,
         name="Electric servo press brakes, 11 – 176 US tons × 1.6 – 10.5 ft",
         short="Electric press brakes 10 – 160 t",
         models_label="WADG-10T/500 – WADG-160T/3200 · 10 models",
         summary="A press brake without hydraulics: servo motors drive the ram through timing belts and dual lead ball screws, so there is no oil, no pump "
                 "running between bends, no valves to drift and no warm-up — the ram repeats to ± 0.01 mm from the first part, bends at any speed "
                 "from 0.15 to 30 mm/s and the machine draws power only while it moves (about 70 % less than a hydraulic brake). Ten models from 11 "
                 "tons × 20″ for small parts to 176 tons × 10.5 ft, all with a Delem DA-53Tx control and X-R servo back gauge; the 40 and 50 t machines "
                 "are also sold in robot bending cells.",
         features=["Mild steel to 1/4″ over 10 ft on the 100 t; 5/16″ over 10 ft on the 160 t (V = 8 × thickness)"] + EPB_STD,
         optional=EPB_OPT,
         images=["vl-wadg-1", "vl-wadg-robot", "vl-wadg-motors", "vl-wadg-ram", "vl-wadg-drawing", "vl-wadg-support", "vl-wadg-tooling", "vl-wadg-parts"],
         videos=[],
         specs=spec([T_WADG], PB_GK, PB_G_FROM, NOTE_EPB)),
    dict(id="vl-wadg-mini", group="pb-electric", page=P_EPB, brand=BRAND,
         name="Compact electric servo press brakes, 3 – 13 US tons × 8 – 24″",
         short="Compact electric press brakes",
         models_label="WADG-3T/200 · WADG-6T/400 · WADG-12T/600",
         summary="Bench-size electric brakes for electronics enclosures, brackets, small appliance and instrument parts: 3, 6 and 12 t over 8, 16 and 24″, "
                 "a 2 – 5.5 kW servo motor, 4.7″ stroke and 16.5″ daylight in a 28 – 33″ footprint on 220 V. Two CNC axes (X and R back gauge) "
                 "with a touchscreen control, a manual top-tool clamp and a 2-V die — the same ± 0.01 mm repeatability "
                 "as the big machines, with 50 % less energy and 40 % less noise than a small hydraulic brake.",
         features=["Single-phase or 3-phase supply; 20 % smaller footprint than a hydraulic brake of the same tonnage"] + EPB_STD[:3] + ["Touchscreen CNC with X and R back gauge axes on cylindrical guides", "Manual top-tool clamp and 2-V die; foot pedal with emergency stop"],
         optional=["Single-V mechanical die clamping", "Light curtain", "Custom voltage"],
         # the compact model itself (ADH product photo, background removed with Pixelcut, supplier logo and model label painted out —
         # tools/src-images/value-sheet/vl-wadg-mini-1.png), then the standard tooling and typical parts
         images=["vl-wadg-mini-1", "vl-wadg-tooling", "vl-wadg-parts"],
         videos=[],
         specs=spec([T_WADG_MINI], PB_GK, PB_G_FROM, NOTE_EPB)),
]

SHEAR_FAMILIES = [
    dict(id="vl-qc12k", group="sh-swing", page=P_SHEAR, brand=BRAND,
         name="Hydraulic swing beam shears, 5/32″ – 3/4″ × 8 – 20 ft",
         short="Swing beam shears",
         models_label="QC12K-4×2500 – QC12K-20×4000 · 32 models",
         summary="The hydraulic shear most shops buy: a swing beam on two cylinders cuts the full length in one stroke, the Estun E21S control "
                 "positions the motorised back gauge and sets the cutting angle, and hydraulic hold-downs keep the sheet flat. Thirty-two models from "
                 "5/32″ × 8 ft to 3/4″ × 13 ft; the 1/4″ × 8 ft and 1/4″ × 10 ft machines (QC12K-6×2500 and 6×3200) are the sizes we quote most, "
                 "with 17 strokes a minute, a 7.5 kW motor and 25.6″ of back gauge. Ball-transfer front tables, shadow-line light, squaring arm and "
                 "a light-barrier front guard are standard.",
         features=["5/32″ to 3/4″ (4 – 20 mm) mild steel; stainless about 60 % of that thickness"] + QC_STD,
         optional=QC_OPT,
         images=["vl-qc12k-1", "vl-qc12k-2", "vl-qc12k-rear", "vl-sh-backgauge", "vl-sh-holddowns", "vl-sh-holddowns-2", "vl-sh-e21s", "vl-sh-roller", "vl-sh-photo-1", "vl-sh-photo-2", "vl-sh-photo-3"],
         videos=[],      # the channel's swing beam shear video was filmed at the supplier's factory with its logo in view
         specs=spec([T_QC_S, T_QC_M, T_QC_L], SH_GK, SH_G_FROM_QC, NOTE_SH)),
    dict(id="vl-q11k", group="sh-guillotine", page=P_SHEAR, brand=BRAND,
         name="Hydraulic guillotine shears, 1/4″ – 1-9/16″ × 8 – 26 ft, variable rake angle",
         short="Guillotine shears",
         models_label="Q11K-6×2500 – Q11K-40×2500 · 34 models",
         summary="The production shear: a guillotine beam on linear rollers with a rake angle the control sets between 0.5° and 4°, so thin sheet is cut "
                 "fast and flat and 1″ plate is cut at the high angle with less twist and less force. The blade gap is adjusted from the Estun E21S "
                 "control as well, with the back gauge and the stroke length. Thirty-four models from 1/4″ × 8 ft to 1-9/16″ × 8 ft and 5/8″ × 26 ft, "
                 "with 7.5 to 55 kW motors and twin pumps on the 20 mm × 20 ft machine.",
         features=["1/4″ to 1-9/16″ (6 – 40 mm) mild steel over 8 – 26 ft; up to 25 cuts a minute"] + Q11_STD,
         optional=Q11_OPT,
         images=["vl-q11k-1", "vl-q11k-rear", "vl-q11k-rear-2", "vl-q11k-controls", "vl-q11k-valve", "vl-q11k-measure", "vl-q11k-feed", "vl-q11k-rexroth", "vl-q11k-holddown",
                 "vl-g-photo-1", "vl-g-photo-2", "vl-g-photo-3", "vl-g-photo-4", "vl-g-photo-5"],
         videos=[],
         specs=spec([T_Q11_S, T_Q11_M, T_Q11_L], SH_GK, SH_G_FROM_Q11, NOTE_SH)),
]

VG_FAMILIES = [
    dict(id="vl-vg-h", group="vg-h", page=P_VG, brand=BRAND,
         name="Horizontal CNC V-grooving machines, 10.5 – 20 ft × 49 – 59″, to 5/32″ stainless",
         short="Horizontal V-grooving",
         models_label="3200 × 1250 – 6000 × 1500 · 7 models",
         summary="V-grooving cuts a V-shaped channel along the bend line so the sheet folds to a sharp, zero-radius corner with no springback and no "
                 "cracking of the finish — the way stainless elevator doors, column cladding, appliance panels and architectural trim are made. "
                 "On the horizontal machine the sheet lies flat on a 49 or 59″ table, pneumatic clamps hold it and a four-tool head on ball screws "
                 "planes the groove at up to 295 ft/min, ± 0.01 mm. Seven table sizes from 10.5 to 20 ft; sheet from 0.016″ to 5/32″.",
         features=["Sheet 0.016″ – 5/32″ (0.4 – 4 mm); 10.5 – 20 ft table lengths; 5.5 kW servo"] + VG_STD,
         optional=VG_OPT,
         images=["vl-vg-h-1", "vl-vg-head", "vl-vg-trial", "vl-vg-clamps", "vl-vg-table", "vl-vg-control", "vl-vg-ruler", "vl-vg-parts", "vl-vg-corner"],
         videos=[],
         specs=spec([T_VG_H], VG_GK, VG_G_FROM, NOTE_VG)),
    dict(id="vl-vg-v", group="vg-v", page=P_VG, brand=BRAND,
         name="Vertical CNC V-grooving machines, 10.5 – 13 ft × 49 – 59″, to 1/4″",
         short="Vertical V-grooving",
         models_label="3200 × 1250 – 4000 × 1500 · 4 models",
         summary="The vertical machine stands the sheet against a fixed beam and feeds it from the rear, so the bed cannot sag and the groove depth "
                 "holds ± 0.03 mm over the length; it takes half the floor space of the horizontal machine and grooves plate to 1/4″. The same "
                 "Taiwan servo CNC, four-cutter head and hydraulic blank holder. Four sizes: 10.5 and 13 ft × 49 or 59″.",
         features=["Sheet 0.016″ – 1/4″ (0.4 – 6 mm); rear feeding with replaceable worktable; 4.4 kW servo"] + VG_STD,
         optional=VG_OPT,
         images=["vl-vg-v-1", "vl-vg-v-scene", "vl-vg-cutters", "vl-vg-beam", "vl-vg-control-2", "vl-vg-parts-2"],
         videos=[],
         specs=spec([T_VG_V], VG_GK, VG_G_FROM, NOTE_VG)),
]

PANEL_FAMILIES = [
    dict(id="vl-pbm", group="panel-value", page=P_PANEL, brand=BRAND,
         name="PB-M press-arm panel benders, 63 – 165″ bend width — NovoTech value line",
         short="PB-M panel benders",
         models_label="PB-M1600 – PB-M4200 · 9 models · 15 servo axes",
         summary="The value-line panel bender: a fully servo-electric bending cell with 15 axes, a patented press arm that feeds and supports the blank "
                 "and a suction-cup manipulator that turns it, forming every side of a panel — up, down, hems, box corners — at 0.2 s per bend. "
                 "Mild steel to 14 ga, stainless to 16 ga, aluminum to 1/8″, bending heights of 7.9″ (11.8″ on the -300 models), blanks to "
                 "165 × 47″. Nine models from 63″ to 165″ bend width, with robot loading as an option.",
         features=["Nine sizes, 63 – 165″ (1,600 – 4,200 mm) bend width; MH models take 55″-deep blanks"] + PN_STD_M,
         optional=PN_OPT,
         images=["vl-pbm-1", "vl-pbm-bending", "vl-pbm-bend", "vl-pbm-holder", "vl-pb-blades", "vl-pb-frame", "vl-pbm-profiles"],
         videos=[],
         specs=spec([T_PBM], PN_GK, PN_G_FROM, NOTE_PN)),
    dict(id="vl-pba", group="panel-value", page=P_PANEL, brand=BRAND,
         name="PB-A automatic tool-change panel benders, 64 – 126″ bend width — NovoTech value line",
         short="PB-A panel benders",
         models_label="PB-A1630 – PB-A3200 · 4 models · 26 – 28 servo axes",
         summary="The PB-A adds an automatic tool changer: the blank-holder tool set reconfigures itself in 0.5 s for every side and every notch of the "
                 "part, so parts with different flange lengths on each side, cut-outs and narrow boxes run without an operator touching a tool. "
                 "26 – 28 servo axes, ± 0.1 mm thickness detection, 0.2 s per bend; the same capacities as the PB-M. Four sizes from 64″ to 126″.",
         features=["Four sizes, 64 – 126″ (1,630 – 3,200 mm) bend width; minimum four-side box 14.6 × 7.1″"] + PN_STD_A,
         optional=PN_OPT,
         images=["vl-pba-1", "vl-pb-robot-cell", "vl-pb-unit", "vl-pba-head", "vl-pb-tools", "vl-pb-operator", "vl-pb-tool-diagram"],
         videos=[],
         specs=spec([T_PBA], PN_GK, PN_G_FROM, NOTE_PN)),
]

IRON_FAMILIES = [
    dict(id="vl-q35y", group="iron-value", page=P_IRON, brand=BRAND,
         name="Q35Y hydraulic ironworkers, 55 – 276 US tons — NovoTech value line",
         short="Q35Y ironworkers",
         models_label="Q35Y-50 · 60 · 90 · 120 · 160 · 200 · 250",
         summary="The value-line steelworker: one hydraulic cylinder, five stations — punching, flat-bar shear, angle shear at 90° and 45°, round and "
                 "square bar shear and rectangular notching — and the tooling to use them in the crate. The 66 US ton Q35Y-60 punches Ø1″ through "
                 "5/8″ and shears 4-3/4 × 4-3/4 × 1/2″ angle; the 132-ton Q35Y-120 punches Ø1-3/8″ through 1″ and shears 6-1/4″ angle and 1″ "
                 "flat; the 200 and 250 t machines cut 7-7/8″ angle, 12″ channel and 1-9/16″ to 2″ plate. The Q35Y-50 is the compact single-station bench model.",
         features=["Punching to Ø1-9/16″ × 1-9/16″, angle to 7-7/8 × 7-7/8 × 11/16″, flat bar to 15-3/4 × 1-9/16″"] + IW_STD,
         optional=IW_OPT,
         images=["vl-q35y-1", "vl-iw-punch", "vl-iw-notch", "vl-iw-angle", "vl-iw-flat", "vl-iw-notch-die", "vl-iw-tooling", "vl-iw-valve", "vl-iw-motor", "vl-iw-gauge"],
         videos=[],
         specs=spec([T_IW], IW_GK, IW_G_FROM, NOTE_IW)),
]

ALL = HPB_FAMILIES + COMPACT_FAMILIES + EPB_FAMILIES + SHEAR_FAMILIES + VG_FAMILIES + PANEL_FAMILIES + IRON_FAMILIES
