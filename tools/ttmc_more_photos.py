#!/usr/bin/env python3
"""Sample photos for the NovoTech value-line machines built by TTMC (tools/ttmc_more_data.py) — crops from the supplier's
Vol. 23 catalogue page rasters until the high-resolution photos arrive.  PDF page N holds catalogue pages 2N-5 (left,
/home/claude/ttmc/img/pN-000.png) and 2N-4 (right, -001.png), 1240 × 1683 px.  The photo areas were found automatically
(/home/claude/ttmc/blobs.json: per page, L1… / R1… = boxes in page pixels) and picked by eye on half-size spread previews;
`fill` rectangles (printed captions, logos, text that overlaps a photo) are given in those spread-preview coordinates
(left page x 0 – 620, right page x 630 – 1250, both at half scale) and painted white before the crop.

    python3 tools/ttmc_more_photos.py [key …]      → tools/src-images/ttmc-more/<key>.jpg
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "ttmc-more")
IMG = "/home/claude/ttmc/img/"
BLOBS = json.load(open("/home/claude/ttmc/blobs.json"))

# key: (pdf page, blob id or a box (x0, y0, x1, y1) in spread-preview coordinates, [fill boxes in spread-preview coordinates], alt)
PLAN = {
 "tm-cs": (18, "R1", [], "CS-315 cold saw on stand with two-speed motor and double vise"),
 "tm-pds315h": (19, "L1", [], "PDS-315H semi-automatic hydraulic cold saw with coolant and hydraulic clamping"),
 "tm-pds400": (19, "R1", [(688, 140, 874, 234), (1056, 508, 1117, 528)], "PDS-400 heavy-duty cold saw for 16″ blades on cabinet stand"),
 "tm-qcs400": (20, "L1", [], "QCS-400 aluminum cut-off saw with pneumatic clamping and guard"),
 "tm-tv": (20, "R3", [(890, 128, 1088, 184), (978, 506, 1042, 532), (962, 544, 1032, 602)], "TV-300 abrasive cut-off saw on stand"),
 "tm-tv-sq": (20, "R1", [(804, 368, 882, 392)], "SQ-40-1 portable abrasive cut-off saw on wheels"),
 "tm-s75": (21, "L1", [(368, 310, 452, 332)], "S-75 heavy-duty belt grinder on pedestal, 3″ × 79″ belt"),
 "tm-s50": (21, "L2", [], "S-50 combination belt grinder and disc sander"),
 "tm-s50b": (21, "R1", [], "S-50B compact 3″ belt grinder"),
 "tm-s75f": (21, "R3", [], "S-75F mobile floor belt grinder for weld seams"),
 "tm-s75h": (22, "L1", [(476, 482, 522, 499)], "S-75HB heavy-duty belt grinder with built-in dust collector"),
 "tm-s100": (22, "R1", [(688, 396, 732, 416)], "S-100 belt grinder with 4″ belt on pedestal"),
 "tm-s220": (22, "R5", [(1090, 764, 1134, 780)], "S-220 wide-belt radius grinder and surface sander with 8″ belt"), "tm-prs": (23, "L3", [(56, 382, 118, 408)], "PRS-76C tube and profile end grinder with two-speed motor, forward and reverse"),
 "tm-prs150": (23, "R5", [(978, 506, 1000, 532)], "PRS-150 tube end grinder with 6″ belt for tube up to 5-3/4″"),
 "tm-sdd75": (24, "L1", [(286, 545, 330, 566), (412, 270, 432, 588)], "SDD75 multi-purpose belt grinder — flat, contact wheel and tube notching on one arm"),
 "tm-bgm50": (24, "R9", [(1054, 684, 1080, 708)], "BGM-50HV 2″ belt grinder for knives and tools, horizontal and vertical"),
 "tm-bgm50b": (25, "L1", [], "BGM-50 variable-speed 1-1/2″ belt grinder"),
 "tm-s50v": (25, "L7", [(384, 648, 402, 672)], "S-75V vertical column belt grinder"),
 "tm-cmd": (25, "R2", [(1013, 188, 1026, 214)], "CMD-80 edge chamfering machine for 15 – 45° weld preps"),
 "tm-cmd4": (25, "R1", [(824, 190, 852, 214)], "CMD-4 bench chamfering machine"),
 "tm-ds12": (25, "R12", [], "DS12A 12″ disc sander with two tables"),
 "tm-ds20": (26, "L5", [(368, 753, 398, 778)], "DS-20 20″ disc sander for metal on pedestal"),
 "tm-ds20v": (26, "R6", [(993, 771, 1047, 792)], "DS-20V variable-speed 20″ disc sander on cabinet base"),
 "tm-tsm300": (26, "L1", [], "TSM300 12″ disc sander on cabinet stand"),
 "tm-btm250": (27, "L1", [(468, 138, 526, 162)], "BTM250 6″ belt and 10″ disc sander on cabinet stand"),
 "tm-bkm250": (27, "L5", [], "BKM-250 belt sander and edge beveller"),
 "tm-bg": (27, "R1", [], "BG-8 8″ bench grinder"),
 "tm-bg60": (27, "R2", [], "BG-60 wire-wheel deburring and polishing machine"), "tm-sp2": (28, "L1", [], "SP-2 variable-speed grinding and polishing machine with belt and disc"),
 "tm-sp6": (28, "R1", [(958, 512, 990, 530)], "SP-6 belt grinder and 20″ disc sander combination with dust ports"),
 "tm-sp3": (29, "L1", [(270, 558, 302, 576)], "SP-3 belt grinder, grinding wheel and polishing wheel on one motor"),
 "tm-dc650": (29, "R5", [], "DC650 metal dust collector with three-stage filtration"),
 "tm-dvs14": (29, "R2", [], "DVS14 metal dust collector with cyclone separation"),
 "tm-bfm2560": (30, "L1", [(374, 436, 458, 452)], "BFM-2560 wide-belt finishing and deburring machine, 24″ working width"),
 "tm-wd1800": (30, "L2", [], "WD-1800 stainless-steel wet dust collector for metal grinding dust"),
 "tm-md380": (30, "R1", [(754, 108, 852, 128)], "MD-380 end-surface grinding machine"),
 "tm-vise": (31, "R13", [(1106, 574, 1150, 590)], "TSL-200 drill press vise"),
 "tm-vise-tq": (31, "L11", [], "TQA6″ tilting precision vise"),
 "tm-ac100h": (31, "L4", [], "AC-100H welding angle clamp for box and round tubing"),
 "tm-wtz": (32, "L1", [], "WTZ-16JF floor drill press with variable speed and digital display"),
 "tm-wtz16q": (32, "L2", [], "WTZ-16Q bench drill press with variable speed"),
 "tm-wtz16t": (32, "R2", [(1116, 520, 1176, 536)], "WTZ-16T drilling and tapping press with automatic reverse"), "tm-t25": (33, "L1", [(246, 78, 262, 222)], "T-25 gear-head drill press with 8 speeds, floor model"),
 "tm-t25c": (33, "R1", [], "T-25C gear-head drill press with 24 V control and spindle guard switch"),
 "tm-t25b": (33, "L5", [], "T-25B bench gear-head drill press"),
 "tm-t28": (34, "L1", [], "T-28 gear-head drill press with mechanical power feed"),
 "tm-t40": (34, "R2", [], "T-40 gear-head drill press, 1-9/16″ in steel, MT4"),
 "tm-t32": (34, "R1", [(880, 120, 886, 180)], "T-35 gear-head drill press with electric power feed"),
 "tm-t50": (35, "L1", [(296, 470, 330, 488)], "T-50 heavy-duty gear-head drill press, 2″ in steel, 12 speeds and power feed"),
 "tm-t50e": (35, "L2", [(506, 470, 556, 488)], "T-50E heavy-duty drill press with 400 mm throat and swivelling table"),
 "tm-tx530": (35, "R2", [(976, 450, 1030, 470)], "TX530A inverter-drive drill press with power feed and coolant"),
 "tm-t5025": (36, "R2", [], "T5025H gear-head drill press with tilting table"),
 "tm-t5025-1a": (36, "L1", [], "T5025-1A gear-head drill press with round table"),
 "tm-t4025": (36, "R3", [], "T4025 bench gear-head drill press"),
 "tm-tb": (37, "L2", [], "TB36 belt-drive industrial column drill"),
 "tm-tbv": (37, "R1", [], "TB36V inverter-drive column drill with coolant"), "tm-b5013": (38, "L4", [(300, 572, 348, 592)], "B5013 slotting machine with swivel head for keyways and splines"),
 "tm-b5012": (38, "L2", [], "B5012 keyseater for keyways in single and small-batch work"),
 "tm-tx20": (38, "R1", [(1020, 394, 1066, 410)], "TX-20 mini mill-drill on cabinet stand"),
 "tm-dm20": (38, "R5", [(846, 640, 912, 728), (680, 774, 726, 792)], "DM-20 radial drill-mill with cross table and box table"),
 "tm-zx5325": (39, "L4", [], "ZX5325C gear-head drilling and milling machine"),
 "tm-zx7550": (39, "L5", [(560, 186, 600, 200), (340, 540, 404, 558)], "ZX7550CW drilling and milling machine with vertical and horizontal spindles"),
 "tm-zx6350": (39, "R2", [(678, 542, 728, 560)], "ZX6350C drilling and milling machine with vertical and horizontal spindles"),
 "tm-4h": (39, "R3", [(964, 548, 1004, 562)], "4H turret milling machine with power feed and DRO"),
 "tm-x6332": (40, "L2", [], "X6332WA vertical and horizontal turret milling machine"),
 "tm-x6325": (40, "L3", [], "X6325W turret milling machine with horizontal spindle"),
 "tm-xq6226": (40, "R2", [], "XQ6226A universal milling machine with swivel head"),
 "tm-xq6226w": (40, "R1", [], "XQ6226W universal milling machine"),
 "tm-lm1450": (41, "L1", [], "LM-1450A universal milling machine, ISO50, with DRO"),
 "tm-lm1450b": (41, "L3", [], "LM-1450B universal milling machine with servo feed"),
 "tm-lm1450d": (41, "R4", [], "LM-1450D universal milling machine for production work"),
 "tm-x6336": (42, "L3", [], "X6336 turret milling machine with horizontal spindle"),
 "tm-x6436": (42, "R1", [], "X6436 universal milling machine with servo feeds"),
 "tm-x5750": (42, "R3", [(958, 520, 1004, 540)], "X5750 universal milling machine with ball screws and three servo motors"), "tm-ctk6416": (43, "L1", [], "CTK6416 slant-bed CNC lathe with gang tooling"),
 "tm-cnc100": (43, "R1", [], "CNC100 slot machining centre for grooving quartz and glass"),
 "tm-vmc8046": (44, "L1", [], "VMC8046 vertical machining centre, BT40, 16-tool changer"),
 "tm-vmc10562": (44, (772, 100, 1146, 444), [], "VMC10562 vertical machining centre, BT40, 24-tool changer"),
 "tm-th800": (45, "L2", [(160, 95, 266, 224)], "TH-800 CNC horizontal boring and milling machine with B-axis rotary table"),
 "tm-txk68": (45, "R2", [(676, 95, 884, 276)], "TXK68 CNC boring and milling machine"),
 "tm-txk160": (46, "L2", [(140, 146, 254, 268)], "TXK160 CNC boring and milling machine, fixed column"),
 "tm-txk160d": (46, "R2", [(764, 81, 882, 348)], "TXK160D CNC boring and milling machine with optional B axis"), "tm-3in1": (47, "R3", [(1034, 470, 1040, 546), (930, 604, 1028, 622)], "3-IN-1/1067×1.5 shear, brake and slip roll machine"),
 "tm-3in1-305": (47, "L4", [], "3-IN-1/305 bench shear, brake and roll"),
 "tm-3in1-1016": (47, "R1", [(1000, 196, 1032, 274), (884, 300, 956, 318)], "3-IN-1/1016 shear, brake and roll with segmented fingers"),
 "tm-minibrake": (47, "L1", [], "8″ mini shear brake for the bench"),
 "tm-e3in1": (48, "L2", [(500, 136, 560, 230)], "E3-IN-1/2040 motorized shear, brake and roll machine"),
 "tm-mcs1250e": (48, "R1", [(946, 412, 1024, 432)], "MCS-1250E motorized circle shear with pneumatic blank clamping"),
 "tm-hcs": (49, "L6", [], "HCS10/10 manual circle shear and flanging machine on stand"),
 "tm-ecs": (49, "L8", [(340, 576, 434, 596)], "ECS10/10 two-speed electric circle shear and flanging machine"),
 "tm-mcs1000": (49, "L1", [], "MCS1.0x1000 manual circle shear"),
 "tm-mms6": (49, "R6", [(722, 410, 776, 432), (862, 486, 866, 620)], "MMS-6 throatless rack-and-pinion bench shear"),
 "tm-mms3": (49, "R3", [], "MMS-3 bench shear for sheet, strip and wire"),
 "tm-hs": (50, "R3", [(1054, 322, 1124, 342)], "HS-12 lever shear for plate, flat and round bar"),
 "tm-ms": (50, "L1", [], "MS-24 hand bar cutter for round, square and flat bar"),
 "tm-hs300": (50, "L4", [], "HS-300 12″ hand guillotine shear"),
 "tm-hs800": (50, "R12", [(740, 754, 790, 774)], "HS-800 hand guillotine shear on stand"),
 "tm-pbs9": (51, "L3", [], "PBS-9 bar and section shear with punching station"),
 "tm-pbs7": (51, "L2", [], "PBS-7 bar and section shear"),
 "tm-gs1000": (51, "R2", [], "GS-1000 manual lever guillotine shear on stand"),
 "tm-khs": (51, "R5", [(668, 648, 762, 664)], "KHS-1250 manual guillotine shear with counter-balance and back gauge"),
 "tm-tsc": (51, "R4", [], "TSC1010/1.6 manual guillotine shear"), "tm-q01": (52, "L1", [], "Q01-1.5×1320 foot shear with front and back gauges"),
 "tm-q01a": (52, "L3", [(46, 496, 136, 512)], "Q01-1.5×1320A welded-steel foot shear"),
 "tm-q01b": (52, "R2", [], "Q01-1.6×1320B light-duty foot shear with spring hold-down"),
 "tm-q01b-gauge": (52, "R6", [], "Back gauge with scale on the foot shear"),
 "tm-bqf01": (53, "L2", [], "BQF01-1.0×1050 foot-operated bench shear"),
 "tm-ebq01": (53, "L5", [], "EBQ01-1.25×650 motorized bench shear with foot switch"),
 "tm-bq01": (53, "R1", [], "BQ01-1.25×650 hand-lever bench shear"),
 "tm-q01h": (53, "R5", [(892, 424, 1074, 478), (862, 668, 948, 686)], "Q01-1.5×1500 two-handle lever shear on stand"),
 "tm-hn3": (54, "L2", [], "HN-3 hand corner notcher, 90°"),
 "tm-hn4": (54, "L5", [], "HN-4 hand corner notcher on optional stand"),
 "tm-fn": (54, "L4", [], "FN1.5×80 foot-operated corner notcher on stand"),
 "tm-pnm": (54, "R1", [], "PNM-130 pneumatic 90° corner notcher on stand"),
 "tm-hnm6a": (55, "L1", [(368, 68, 414, 196), (118, 438, 178, 458)], "HNM-6A hydraulic adjustable-angle notcher, 30 – 135°"),
 "tm-hnm6": (55, "R1", [(896, 420, 940, 438)], "HNM-6 hydraulic 90° corner notcher"), "tm-pc24": (61, "L1", [(296, 400, 332, 430)], "PC 2′×4′ compact CNC plasma table with stepper drives"),
 "tm-pc510": (61, "R1", [(1082, 356, 1174, 382)], "PC 5′×10′ CNC plasma table with servo drives, torch height control and downdraft table"),
 "tm-pc-console": (61, "R5", [], "CNC console of the plasma table"),
 "tm-pcp3000e": (62, "L1", [(114, 324, 216, 350)], "PCP 300×3000E CNC plasma pipe cutting machine with chucks at both ends"),
 "tm-pcp6000": (62, "R1", [], "PCP 300×6000 CNC plasma pipe cutting machine with ball-transfer cradles"),
 "tm-eb1250": (63, "L1", [], "EB1250 magnetic sheet metal brake, 4 ft × 16 ga, with foot switch"),
 "tm-eb2500": (63, "R1", [], "EB2500 magnetic sheet metal brake, 8 ft × 16 ga"),
 "tm-eb-bars": (63, "R3", [], "Standard clamping bars of the magnetic brake — full length, short set, narrow and slotted"),
 "tm-bsm1016": (64, "L1", [], "BSM1016 folding brake with slitter on folding stand"),
 "tm-bsm2540": (64, "L3", [(388, 552, 448, 570)], "BSM2540 folding brake with slitter, 100″"),
 "tm-alb": (64, "R1", [(726, 348, 792, 372), (674, 400, 854, 416)], "ALB-3200 portable aluminum roofing brake with roller slitter"),
 "tm-alb-work": (64, "R4", [], "Bending flashing on the portable roofing brake"),
 "tm-3in1a": (65, "L1", [(334, 284, 476, 362)], "3-IN-1/760A shear, brake and roll with separate bending section"),
 "tm-wb14": (65, "R2", [], "WB-14 bench hand brake"),
 "tm-w1000": (65, "R5", [(994, 336, 1066, 360)], "W1.2×1000 bench hand brake"),
 "tm-zwj": (65, "R11", [(662, 728, 916, 808)], "ZWJ offset (jog) brake"), "tm-hb2250": (66, "L1", [], "HB-2250 hand brake on stand, 50″"),
 "tm-hb2248": (66, "L5", [(120, 620, 202, 636), (200, 650, 254, 666)], "HB-2248 all-steel hand brake on folding stand"),
 "tm-w1500": (66, "R7", [(890, 664, 960, 682), (1030, 648, 1052, 684)], "W1.2×1500 floor hand brake with one-piece blade"),
 "tm-w1220": (66, "R2", [], "W1.2×1220 bench hand brake"),
 "tm-pb1220": (67, "L3", [], "W1.5×1220 pan and box brake with removable fingers"),
 "tm-pb1220z": (67, "L7", [], "W1.5×1220Z heavy-duty pan and box brake"),
 "tm-bp1650": (67, "R1", [], "BP-1650 pan and box brake, 16 ga × 50″"),
 "tm-bp1648h": (67, (668, 330, 1214, 594), [(1136, 570, 1214, 590)], "BP-1648H pan and box brake on stand"),
 "tm-w2040": (68, "L1", [(210, 322, 280, 340)], "W2.0×2040 floor hand brake with counterweights, 80″ × 14 ga"),
 "tm-w2540a": (68, "R3", [], "W2.5×2540A floor pan and box brake with segment blade, 100″ × 12 ga"),
 "tm-w1220pb": (68, "R1", [(1016, 296, 1090, 318)], "W2.5×1220 floor pan and box brake"),
 "tm-wu": (69, "L1", [(40, 105, 272, 200), (36, 214, 272, 304)], "WU2.0×2500 pan and box brake with two counterweights"),
 "tm-w1830p": (69, "L6", [(284, 650, 364, 668)], "W1830×1.5P pan and box brake, 72″ × 16 ga"),
 "tm-w2540h": (69, "R4", [(998, 552, 1080, 570)], "W1.5×2540H heavy pan and box brake for pans to 5-1/8″ deep"),
 "tm-w1500h": (69, "R1", [(752, 306, 834, 324)], "W1.2×1500H pan and box brake with 125 mm fingers"),
 "tm-w1050": (70, "L5", [], "W1.5×1050 floor brake with sliding segments"),
 "tm-pbb1020": (70, "R1", [(842, 310, 922, 344)], "PBB1020/1A folding machine on stand"),
 "tm-wf": (70, "R4", [], "WF1.0×3000 folding machine, 10 ft"), "tm-pbb": (71, "L3", [(460, 626, 540, 662)], "PBB2020/1.2 folding machine with foot-operated clamping beam"),
 "tm-pbb1020": (71, "L1", [], "PBB1020/2.5 folding machine with foot clamping"),
 "tm-pbb3sh": (71, "R3", [], "PBB1020/3SH folding machine with quick-release clamp segments"),
 "tm-tsbs": (72, "L1", [(310, 278, 388, 290)], "TSBS 2020/2 manual folding machine with segmented blade"),
 "tm-tsb2060": (72, "R2", [], "TSB 2060/2 cast-iron folding machine with counterweight"),
 "tm-tfs": (72, "R1", [], "TFS 2020B folding machine with foot clamping"),
 "tm-mfs": (73, "L1", [(134, 296, 200, 312)], "MFS 2020 folding machine with foot clamping and segments"),
 "tm-efms": (73, "R1", [(800, 246, 872, 264), (668, 286, 990, 300)], "EFMS 2020 electric folding machine with foot pedal"),
 "tm-efm": (73, "R2", [(838, 544, 902, 560), (676, 556, 890, 584)], "EFM 3020 electric folding machine, 10 ft"),
 "tm-hw": (74, "L1", [], "HW1830×3.5 hydraulic folding machine with movable control panel"),
 "tm-hw2440": (74, "R1", [], "HW2440×3.5 hydraulic folding machine"),
 "tm-hw-angle": (74, "L3", [], "Bending angle setting on the hydraulic folding machine"),
 "tm-hw-box": (74, "L2", [], "Segments for bending boxes on the hydraulic folding machine"),
 "tm-hwe": (75, "L1", [(252, 312, 340, 326)], "HW2040×4.5E hydraulic folding machine with touch screen, servo back gauge and light curtain"), "tm-hbv": (76, "L1", [(150, 436, 210, 452)], "HBV48 hydraulic bending brake with four-way V-block and foot valve"),
 "tm-m55": (76, "R5", [(1104, 524, 1222, 556)], "M55 compact single-cylinder ironworker with punch, shear and notcher"),
 "tm-stand-ra785": (77, "L7", [], "RA785 roller table with measuring feed system"),
 "tm-stand-rb365": (77, "L6", [(164, 608, 242, 634)], "RB365 roller conveyor"),
 "tm-stand-rv": (77, "L3", [], "RV1100 V-roller stand"),
 "tm-slip-kw01": (78, "R5", [(908, 596, 1004, 612)], "KW01-0.8×1250 slip roll on stand"),
 "tm-slip-w01": (78, "L3", [], "W01-1.5×915 manual slip roll"),
 "tm-slip-1300": (78, "R1", [], "W01-1.5×1300 manual slip roll"),
 "tm-slip-sj": (78, "L1", [], "SJ300 bench slip roll with optional vise"),
 "tm-esr1020": (79, "L1", [], "ESR-1020×2 motorized slip roll with foot pedal"),
 "tm-w01-2": (79, "L2", [(98, 638, 162, 660)], "W01-2×1000 manual slip roll on stand, 14 ga"),
 "tm-esr1300e": (79, "R1", [(808, 290, 990, 304)], "ESR-1300×1.5E motorized slip roll, European design"),
 "tm-esr": (80, "L1", [(116, 304, 222, 322)], "ESR-1300×4.5 electric slip roll with wire grooves and cone rolling"),
 "tm-her": (80, "R1", [(662, 158, 706, 194), (1100, 196, 1172, 210)], "HER-1550×6.5 hydraulic slip roll with digital pinch-roll counter"), "tm-rbm10": (81, "L1", [(50, 200, 132, 214)], "RBM10 manual ring roller on stand"),
 "tm-erbm10": (81, "L4", [], "ERBM10HV motorized ring roller, horizontal and vertical, with foot pedal"),
 "tm-rbm30": (81, "R1", [(668, 320, 740, 342)], "RBM30 motorized ring roller with foot pedal"),
 "tm-rbm30hv": (81, "R6", [], "RBM30HV ring roller, horizontal and vertical"),
 "tm-rbm-rolls": (81, "R5", [], "Combination roll set of the ring roller"),
 "tm-rbm40": (82, "L2", [], "RBM40HV profile bender, horizontal and vertical, with foot pedal"),
 "tm-hrbm40": (82, "L1", [(462, 92, 542, 112)], "HRBM40HV profile bender with hydraulic top roll"),
 "tm-rbm50": (82, "L4", [], "RBM50HV profile bender with Ø2″ shafts"),
 "tm-hrbm50": (82, "L3", [(446, 470, 528, 486)], "HRBM50HV profile bender with hydraulic top roll"),
 "tm-crb76": (83, "L1", [], "CRB-76 decorative ring roller for tube and flat bar"),
 "tm-crb-rolls": (83, "L2", [], "Formers of the decorative ring roller"),
 "tm-rbm20": (83, "L6", [], "RBM20 ring roller with LED top-roll readout and foot pedal"),
 "tm-hrbm65": (83, "R2", [], "HRBM65 hydraulic profile bender with Ø2-1/2″ shafts and mobile control panel"),
 "tm-pf16g": (84, "L1", [(196, 344, 242, 364)], "PF16G lock former for Pittsburgh locks, double seams, drive cleats and Z shapes"),
 "tm-pf20g": (84, "L8", [(214, 660, 262, 680)], "PF20G lock former for Pittsburgh locks"),
 "tm-ax20g": (84, "R1", [(830, 358, 874, 374)], "AX20G auxiliary roll former with quick-change roll sets"),
 "tm-lock-forms": (84, "L2", [], "Pittsburgh lock formed on the lock former"),
 "tm-chb": (85, "L1", [(56, 236, 260, 252), (340, 96, 590, 250)], "CHB-24 hand brake for flanges on duct"),
 "tm-cb": (85, "L2", [(500, 436, 542, 456)], "CB-24 cleat bender for drive-cleat edges on duct"),
 "tm-rm08": (85, "R7", [(968, 630, 1018, 648)], "RM08 bench bead roller with six roll sets"),
 "tm-rm18": (85, "R6", [], "RM18 bead roller with 18″ throat on optional stand"),
 "tm-rmb": (85, "R3", [], "RM-B rotary machine with hardened rolls"), "tm-rm27": (86, "L2", [(414, 174, 460, 190)], "RM-27 heavy-duty bead roller with offset dies"),
 "tm-rm8h": (86, "L6", [(382, 438, 430, 456)], "RM-8H 8″ throat bead roller with 3/8″ bead and offset die sets"),
 "tm-sl10": (86, "L9", [], "SL-10 electric Pittsburgh seam closer"),
 "tm-rtb8as": (86, "R2", [], "RTB-8AS hand roller for round duct on welded stand"),
 "tm-rtb8": (86, "R1", [], "RTB-8 hand roller for forming round duct and pipe"),
 "tm-lb2": (86, "R4", [(702, 656, 736, 676)], "LB-2 channel letter bender for sign makers"),
 "tm-etb12": (87, "L3", [(34, 360, 82, 374)], "ETB-12 motorized beading machine with foot pedal"),
 "tm-tb12": (87, "L2", [], "TB-12 hand beading machine"),
 "tm-etb25": (87, "L8", [], "ETB-25 beading machine, 12 ga, with brake motor and foot pedal"),
 "tm-rm18e": (87, "R1", [(970, 290, 1030, 302)], "RM18E power beading machine for round duct"),
 "tm-lq15": (87, "R4", [(928, 578, 976, 596)], "LQ15 power slitting and bending machine for duct"),
 "tm-rm36": (88, "L4", [(104, 640, 146, 656), (204, 628, 300, 654)], "RM36 power-drive bead roller with 36″ throat and variable-speed foot pedal"),
 "tm-rm24m": (88, "L1", [(268, 176, 312, 194)], "RM24M hand-crank bead roller with 24″ throat"),
 "tm-rm42h": (88, "R1", [(918, 408, 970, 426)], "RM-42H high-throat variable-speed bead roller, 42″"),
 "tm-tb500": (89, "L1", [(34, 216, 78, 232), (48, 260, 100, 278)], "TB-500 ratchet tube bender on pedestal"),
 "tm-tb180": (89, "L6", [(148, 596, 240, 624)], "TB-180 vise-mount tube bender, 180° in one pull"),
 "tm-htb25t": (89, "R1", [(692, 324, 750, 338)], "HTB-25T 25-ton hydraulic tubing bender with air-hydraulic pump"),
 "tm-htb25t-stand": (89, "R5", [], "HTB-25T on the optional floor stand"),
 "tm-yp38": (90, "L1", [], "YP-38 bench bender for flat bar, 0 – 200°"),
 "tm-ubm30": (90, "L2", [], "UBM-30 bench bender for flat bar and rod"),
 "tm-rb1": (90, "L8", [], "RB-1 hand tube bender on stand, 270°"),
 "tm-tb3": (90, "L10", [(450, 656, 558, 670)], "TB-3 hand pipe bender for 2″ schedule 40 pipe"),
 "tm-tb3b": (90, "R2", [], "TB-3B air-hydraulic pipe bender on caster stand with die rack"),
 "tm-tb3c": (90, "R3", [], "TB-3C electric-hydraulic pipe bender on caster stand"), "tm-hb12": (91, "L2", [], "HB-12 hydraulic pipe bender with hand pump"),
 "tm-ehb10": (91, "L5", [], "EHB-10 electric-hydraulic pipe bender"),
 "tm-hb10": (91, "L6", [], "HB-10 hydraulic pipe bender on stand"),
 "tm-hb8": (91, "L1", [], "HB-8 hydraulic pipe bender with five die sets"),
 "tm-my22": (91, "R2", [], "MY-22 hand tube bender kit in a carry case"),
 "tm-w1": (91, "R5", [], "W-1 ornamental iron tool set — scroll former, bender, twister, shear and punch"),
 "tm-sbg30": (92, "L1", [], "SBG-30 bench bender for angles, rings, hoops and scrolls"),
 "tm-ub100a": (92, "L5", [(352, 548, 438, 568)], "UB-100A universal bender for flat bar, round and square"),
 "tm-ub70": (92, "L6", [], "UB-70 universal bender with bending tools"),
 "tm-pbs3": (92, "R1", [], "PBS-3 shear, brake and punch hanger board for on-site work"),
 "tm-jtr30": (92, "R7", [], "JTR-30 ring roller for flat bar and tube"),
 "tm-w10": (93, "L1", [], "W-10 rod forming tool for 180° bends"),
 "tm-mini-ub": (93, "L6", [], "Mini universal bender for wire, flat bar and tube"),
 "tm-pr5": (93, "R5", [(1150, 626, 1166, 646)], "PR-5 ring roller with three driven rolls"),
 "tm-pr5-stand": (93, "R4", [(758, 572, 840, 588)], "PR-5 ring roller on its heavy stand"),
 "tm-pr3": (93, "R1", [(700, 180, 736, 198)], "PR-3 bench ring roller"),
 "tm-tr40": (94, "L1", [], "TR-40 tube roller for square and rectangular tube"),
 "tm-etr50": (94, "L8", [(308, 630, 422, 686), (494, 668, 598, 684)], "ETR-50 electric tube roller with foot pedal"),
 "tm-tr50": (94, "L9", [(166, 630, 262, 676), (240, 486, 316, 512)], "TR-50 tube roller on adjustable stand"),
 "tm-tr60": (94, "R1", [(884, 424, 922, 442)], "TR-60 tube and pipe roller with quick-change lower roll"),
 "tm-htb1000": (95, "L2", [(108, 560, 172, 578)], "HTB-1000 electric-hydraulic pipe bender on caster stand"),
 "tm-tbm60": (95, "R1", [(966, 408, 1024, 426)], "TBM-60 electric rotary-draw tube bender with foot pedal"),
 "tm-tbm60-pos": (95, "R3", [(954, 628, 1090, 642)], "TBM-60 with the optional two-axis positioner"), "tm-htes": (96, "L1", [(390, 268, 462, 322)], "HTES-3000 hydraulic tube expander and swager on portable cart"),
 "tm-htb2000": (96, "R2", [(954, 288, 1000, 302)], "HTB-2000 hydraulic exhaust tube bender with tooling package"),
 "tm-jtb50": (97, "L3", [], "JTB-50 hydraulic PLC tube bender"),
 "tm-jtb40": (97, "L1", [], "JTB-40 hydraulic tube bender with foot pedal"),
 "tm-jtb80": (97, "R1", [(700, 342, 746, 360)], "JTB-80 hydraulic PLC tube bender for 3-1/8″ tube"),
 "tm-dollies": (98, "L6", [(204, 152, 568, 182), (428, 282, 570, 360)], "SFD-9 dolly stand with post dollies"),
 "tm-fr120": (98, "R2", [(670, 238, 750, 252)], "FR-120 hub-mounted fender roller"),
 "tm-ns1": (98, "R5", [(676, 418, 742, 438)], "NS-1 nibbler shears"),
 "tm-wg": (98, "L17", [(382, 654, 580, 700)], "Butt-weld panel clamps for auto body welding"),
 "tm-ss18fd": (99, "L6", [], "SS-18FD foot-operated shrinker-stretcher with two heads"),
 "tm-ss16f": (99, "L7", [], "SS-16F foot-operated shrinker-stretcher, 16 ga, 8″ throat"),
 "tm-fsm16": (99, "L8", [], "FSM-16 foot-operated shrinker-stretcher on wheeled base"),
 "tm-ss16": (99, "L3", [], "SS-16 bench shrinker-stretcher, 16 ga, 8″ throat"),
 "tm-sm16b": (99, "R1", [(876, 176, 924, 252)], "SM-16B industrial shrinker-stretcher"),
 "tm-ss-jaws": (99, "R4", [], "Shrinker and stretcher jaws"),
 "tm-pph12": (100, "L7", [], "PPH-12 pneumatic planishing hammer with foot pedal and anvils"),
 "tm-pph610": (100, "R3", [], "PPH-610 pneumatic planishing hammer, 24″ throat, 16 ga"),
 "tm-ph20d": (100, "R6", [], "PH-20D electric power hammer, 20″ throat, variable speed"),
 "tm-ph30d": (100, "R5", [], "PH-30D electric power hammer, 30″ throat"),
 "tm-anvils": (100, "L8", [], "Planishing hammer anvils from 3/4″ to 4″ radius"),
 "tm-bep": (100, "L1", [], "BEP-15 bullseye pick for dent repair"), "tm-f1210": (101, "L4", [], "F1.2×710 English wheel with 28″ throat and six lower wheels"),
 "tm-f1256": (101, "L5", [], "F1.2×560 English wheel on stand"),
 "tm-f1570": (101, "R1", [], "F1.5×700 English wheel, 16 ga steel, 27-1/2″ throat"),
 "tm-f12100": (101, "R3", [], "F1.2×1000 English wheel with 40″ throat and foot pressure control"),
 "tm-ufp2": (101, "R4", [(808, 548, 904, 568)], "UFP-2 planishing hammer and English wheel in one"),
 "tm-f15110": (102, "L1", [(270, 360, 332, 378)], "F1.5×1100 English wheel with 45″ throat"),
 "tm-pic50": (102, "L5", [(270, 650, 306, 666)], "PIC50 roller former that embosses a diamond pattern into sheet"),
 "tm-pic50-sample": (102, "L6", [], "Diamond pattern embossed by the PIC50"),
 "tm-f2063": (102, "R1", [], "F2.0×630 heavy English wheel, 14 ga"),
 "tm-f2076": (102, "R4", [(980, 640, 1034, 656)], "F2.0×760 heavy English wheel with 30″ throat"),
 "tm-pnm15": (103, "L3", [(180, 308, 250, 324)], "PNM 1-1/2 hole-saw pipe notcher for the hand drill"),
 "tm-utn40": (103, "L4", [], "UTN40 end-mill tube notcher, 1/2 – 2″"),
 "tm-utn40v": (103, "L9", [], "UTN40V variable-speed end-mill tube notcher"),
 "tm-ptn30": (103, "R1", [(1116, 180, 1196, 198), (1064, 362, 1110, 386)], "PTN-30 motorized tube and pipe notcher with hole saw and degree wheel"),
 "tm-ptn-work": (103, "L6", [], "Tube saddle notched on the pipe notcher"),
 "tm-pn12": (104, "L4", [], "PN-1/2S hole-saw pipe notcher for the drill press"),
 "tm-ptn12u": (104, "L12", [], "PTN-12U electric pipe notcher"),
 "tm-ra": (104, "L11", [(62, 584, 146, 600)], "RA hand tube notcher"),
 "tm-hp20": (104, "R10", [], "HP-20 hand lever punch for round and square holes"),
 "tm-fb4": (104, "R2", [], "FB-4 form bender"),
 "tm-ap5": (105, "L3", [], "AP-5 arbor press, 5 tons"),
 "tm-ap8": (105, "L1", [], "AP-8 arbor press, 8 tons"),
 "tm-rap": (105, "L8", [], "RAP-3 ratchet arbor press"),
 "tm-tp12a": (105, "R1", [(848, 400, 892, 418)], "TP-12A manual turret punch press on open stand"),
 "tm-tp12b": (105, "R2", [(1150, 438, 1200, 456)], "TP-12B manual turret punch press on cabinet stand"), "tm-bp3t": (106, "L1", [], "BP-3T bench press for punch, flare, bead and louver tooling"),
 "tm-ebp10t": (106, "L3", [(240, 640, 306, 660)], "EBP-10T hydraulic bench press with 25″ throat"),
 "tm-bp3f": (106, "R11", [(920, 662, 990, 676)], "BP3-F combination bench press with four stations on optional stand"),
 "tm-louver": (106, "R4", [], "Louver punches for the bench press"),
 "tm-hb10t": (107, "L1", [], "HB-10T mobile hydraulic horizontal bender"),
 "tm-hb40t": (107, "R1", [(1058, 278, 1220, 372)], "HB-40T hydraulic horizontal bender with PLC touch screen"),
 "tm-hb-vee": (107, "L3", [], "Vee bending die of the horizontal bender"),
 "tm-xm8": (108, "L2", [], "XM-8 hydraulic orbital riveter"),
 "tm-ebp25t": (108, "R1", [], "EBP-25T workshop press with motorized pump"),
 "tm-bp16t": (108, "R2", [], "BP-16T workshop press with hand pump"),
 "tm-hp12n": (109, "L2", [(184, 148, 238, 162)], "HP-12N 12-ton shop press brake for 12″ × 3/16″"),
 "tm-hp24n": (109, "L6", [], "HP-24N 20-ton shop press brake, 24″"),
 "tm-hframe": (109, "L14", [], "H-frame shop press, 20 – 30 tons"),
 "tm-hpp100": (109, "R3", [], "HPP-100 motorized workshop press with moving cylinder"),
 "tm-hp30s": (109, "R8", [], "HP-30S workshop press, European design"),
 "tm-hp30sa": (109, "R9", [], "HP-30S-A workshop press with hand pump"),
 "tm-hp30": (110, "L7", [(196, 476, 302, 500)], "HP-30 motorized H-frame hydraulic press"),
 "tm-hp100": (110, "L6", [], "HP-100 H-frame hydraulic press with separate hydraulic station"),
 "tm-hp80m": (110, "R1", [], "HP-80M hydraulic press with mobile cylinder and safety fence"),
 "tm-hpb1500": (110, "R5", [], "HPB-1500 press with brake function — V-block and support table"),
 "tm-hpb580": (110, "R4", [], "HPB-580 press with brake function"), "tm-hpb580d": (111, "L1", [(286, 322, 362, 340)], "HPB-580D two-cylinder press with brake function and safety fence"),
 "tm-hpb1500d": (111, "L4", [(404, 382, 560, 396)], "HPB-1500D two-cylinder hydraulic press brake"),
 "tm-hp150m1": (111, "R1", [(704, 332, 790, 348)], "HP-150M1 hydraulic press with sliding table"),
 "tm-hp200m1": (111, "R3", [(690, 404, 916, 486)], "HP-200M1 hydraulic press with sliding table"),
 "tm-hp20m1": (111, "R2", [], "HP-20M1 hydraulic press with sliding table"),
 "tm-hp63c": (112, "L1", [], "HP-63C C-frame hydraulic press with guard"),
 "tm-hp30c": (112, "L2", [], "HP-30C C-frame hydraulic press"),
 "tm-hp315fk": (112, "R1", [], "HP-315FK four-column hydraulic press with PLC control"),
 "tm-hp50f": (112, "R2", [(1120, 314, 1180, 332)], "HP-50F four-column hydraulic press with separate pump unit"),
 "tm-c41-40": (113, "R3", [], "C41-40KG self-contained pneumatic forging hammer"),
 "tm-c41-16": (113, "R2", [], "C41-16KG pneumatic forging hammer"),
}

DETAIL = {"tm-eb-bars", "tm-alb-work", "tm-hw-angle", "tm-hw-box", "tm-rbm-rolls", "tm-crb-rolls", "tm-lock-forms", "tm-ss-jaws", "tm-anvils",
          "tm-pic50-sample", "tm-ptn-work", "tm-louver", "tm-hb-vee", "tm-pc-console", "tm-q01b-gauge", "tm-dollies", "tm-wg", "tm-ns1", "tm-fr120"}


def to_page(box, page_side):
    """spread-preview box -> (side, page box) — side 'L' (left page) or 'R'"""
    x0, y0, x1, y1 = box
    if page_side == "R" or x0 >= 630:
        return "R", (int((x0 - 630) * 2), int(y0 * 2), int((x1 - 630) * 2), int(y1 * 2))
    return "L", (int(x0 * 2), int(y0 * 2), int(x1 * 2), int(y1 * 2))


def trim(im, thr=238, pad=10):
    g = im.convert("L").point(lambda v: 0 if v >= thr else 255)
    bb = g.getbbox()
    if not bb:
        return im
    l, t, r, b = bb
    return im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))


# captions, model labels, leader lines and stray marks around the photo, removed after the crop (clean_marks)
CLEAN = {
    "tm-q01b", "tm-rbm-rolls", "tm-rbm10", "tm-rm18", "tm-rmb", "tm-slip-kw01", "tm-tb12", "tm-tbm60", "tm-tbm60-pos", "tm-tr50",
    "tm-4h", "tm-ap8", "tm-bgm50b", "tm-bp1648h", "tm-bp3t", "tm-bqf01", "tm-crb-rolls", "tm-crb76", "tm-dm20", "tm-dvs14",
    "tm-e3in1", "tm-eb2500", "tm-ebq01", "tm-esr", "tm-esr1300e", "tm-etb12", "tm-etb25", "tm-etr50", "tm-f1210", "tm-f1256",
    "tm-fsm16", "tm-hb10", "tm-hb10t", "tm-hb2248", "tm-hb2250", "tm-hb40t", "tm-hbv", "tm-her", "tm-hnm6a", "tm-hp100",
    "tm-hp12n", "tm-hp150m1", "tm-hp200m1", "tm-hp24n", "tm-hp30", "tm-hp30c", "tm-hp315fk", "tm-hp50f", "tm-hpp100",
    "tm-hrbm40", "tm-hrbm50", "tm-htb1000", "tm-htb2000", "tm-htes", "tm-hw-angle", "tm-hw-box", "tm-lb2", "tm-lm1450",
    "tm-lm1450b", "tm-lq15", "tm-ms", "tm-mms6", "tm-txk160d", "tm-ufp2", "tm-vise", "tm-w01-2", "tm-w1500", "tm-w1830p", "tm-wf",
    "tm-x5750", "tm-x6436", "tm-xm8", "tm-xq6226", "tm-zx6350", "tm-zx7550",
}
# the supplier's logo on the machine, painted over with the colour around it — (top, bottom, left, right) in the cropped photo
LOGO = {
    "tm-pds315h": [(376, 416, 370, 445)], "tm-qcs400": [(150, 176, 140, 194)], "tm-t40": [(72, 99, 98, 157)],
    "tm-t50e": [(117, 138, 119, 156)], "tm-jtb50": [(109, 143, 55, 115)], "tm-jtb80": [(203, 242, 72, 157)],
    "tm-m55": [(12, 38, 211, 261)], "tm-hwe": [(245, 262, 348, 380)], "tm-t4025": [(169, 197, 159, 199)],
    "tm-bg60": [(202, 257, 319, 366)], "tm-ds20v": [(376, 407, 153, 204)], "tm-hrbm65": [(481, 507, 144, 185)],
    "tm-jtb40": [(164, 189, 66, 112)], "tm-sp6": [(567, 614, 359, 440)], "tm-t50": [(133, 152, 114, 143)],
    "tm-vmc10562": [(119, 143, 28, 68)], "tm-vmc8046": [(44, 56, 347, 363)], "tm-wtz16t": [(73, 85, 126, 143)],
    "tm-wd1800": [(136, 160, 126, 168)],
}
SCREEN = {"tm-pc-console": [(55, 84, 66, 158)]}   # the supplier's name on a control screen
# what clean_marks cannot separate from the machine (labels and leader lines that touch it, insets), painted white after it —
# (top, bottom, left, right, mode) in the cleaned photo; mode "w" paints the box white, "d" only the dark grey and black pixels
WHITE = {
    "tm-bqf01": [(330, 469, 0, 48, "w")], "tm-crb76": [(0, 125, 300, 443, "w")], "tm-ebq01": [(370, 417, 330, 540, "w")],
    "tm-etr50": [(350, 425, 0, 118, "w")], "tm-fsm16": [(40, 230, 225, 279, "w")],
    "tm-her": [(0, 426, 852, 1088, "w")],
    "tm-hp12n": [(345, 393, 150, 255, "w"), (190, 245, 60, 110, "w")], "tm-hpp100": [(60, 235, 380, 450, "w")],
    "tm-lb2": [(295, 360, 225, 304, "w")], "tm-q01b": [(368, 410, 275, 475, "d")], "tm-rbm-rolls": [(182, 211, 0, 236, "w")],
    "tm-rm18": [(185, 215, 190, 247, "w"), (200, 262, 140, 195, "d")], "tm-rmb": [(338, 368, 60, 340, "w")],
    "tm-t40": [(50, 130, 0, 40, "w"), (730, 785, 0, 40, "d")], "tm-t50": [(682, 712, 0, 90, "d")],
    "tm-tb12": [(205, 235, 255, 395, "w")], "tm-tr50": [(300, 420, 185, 395, "d")], "tm-hp30": [(168, 190, 166, 258, "d")],
}


def clean_marks(im, keep=0.02, text_h=0.07):
    """paint out every separate blob next to the machine that is small (under `keep` of the machine's ink) or as low as a line
    of text (under `text_h` of the photo height): captions, model labels, leader lines and specks on the white background"""
    a = np.asarray(im).copy()
    ink = a.min(axis=2) < 225
    lab, n = ndimage.label(ndimage.binary_dilation(ink, iterations=3))
    if n < 2:
        return im
    sizes = ndimage.sum(ink, lab, range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    kill = np.zeros(ink.shape, bool)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if i != main and (sizes[i - 1] < keep * sizes[main - 1] or sl[0].stop - sl[0].start < text_h * a.shape[0]):
            kill |= lab == i
    a[ndimage.binary_dilation(kill, iterations=2)] = 255
    return Image.fromarray(a)


def paint_logo(im, boxes):
    a = np.asarray(im).copy()
    for t, b, l, r in boxes:
        ring = np.concatenate([a[max(0, t - 4):t, l:r].reshape(-1, 3), a[b:b + 4, l:r].reshape(-1, 3),
                               a[t:b, max(0, l - 4):l].reshape(-1, 3), a[t:b, r:r + 4].reshape(-1, 3)])
        a[t:b, l:r] = np.median(ring, axis=0).astype(np.uint8)
    return Image.fromarray(a)


def paint_white(im, boxes):
    a = np.asarray(im).copy()
    for t, b, l, r, mode in boxes:
        roi = a[t:b, l:r]
        if mode == "w":
            roi[:] = 255
        else:
            c = roi.astype(int)
            dark = (c.max(axis=2) < 140) & (c.max(axis=2) - c.min(axis=2) < 45)
            roi[ndimage.binary_dilation(dark, iterations=1)] = 255
    return Image.fromarray(a)


def paint_screen(im, boxes):
    a = np.asarray(im).copy()
    for t, b, l, r in boxes:
        roi = a[t:b, l:r].astype(int)
        bg = np.median(roi[roi.min(axis=2) > 200], axis=0) if (roi.min(axis=2) > 200).any() else np.array([235, 235, 235])
        text = ((roi[..., 0] - roi[..., 1]) > 12) | (roi.max(axis=2) < 205)
        roi[ndimage.binary_dilation(text, iterations=2)] = bg
        a[t:b, l:r] = roi.astype(np.uint8)
    return Image.fromarray(a)


def process(key):
    page, blob, fills, alt = PLAN[key]
    if isinstance(blob, tuple):
        side, box = to_page(blob, None)
    else:
        side, box = blob[0], BLOBS[f"p{page}"][blob]
    im = Image.open(f"{IMG}p{page}-{'000' if side == 'L' else '001'}.png").convert("RGB")
    d = ImageDraw.Draw(im)
    for f in fills:
        fs, fb = to_page(f, None)
        if fs == side:
            d.rectangle(fb, fill=(255, 255, 255))
    x0, y0, x1, y1 = box
    im = trim(im.crop((max(0, x0 - 4), max(0, y0 - 4), min(im.width, x1 + 4), min(im.height, y1 + 4))))
    if key in LOGO:
        im = paint_logo(im, LOGO[key])
    if key in SCREEN:
        im = paint_screen(im, SCREEN[key])
    if key in CLEAN:
        im = trim(clean_marks(im))
    if key in WHITE:
        im = trim(paint_white(im, WHITE[key]))
    os.makedirs(DST, exist_ok=True)
    out = os.path.join(DST, key + ".jpg")
    im.save(out, quality=92)
    return im.size


def main():
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PLAN)
    for k in keys:
        print(f"{k:22s} {process(k)}")


if __name__ == "__main__":
    main()
