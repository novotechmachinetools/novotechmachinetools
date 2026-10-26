#!/usr/bin/env python3
"""Plastmak (Bursa, Turkey) aluminum and PVC window and door machinery — photos from four sources outside the repo:

  /home/claude/plastmak/web/   plastmak.com product photos (2,560 px studio shots on white, 1,080 – 1,920 px details), decoded
                               from the page captures in the Downloads folder (plastmak[bc]-NN.json)
  /home/claude/plastmak/img/   images of NovoTech's Plastmak catalogue (NovoTech_Plastmak_Window_Machinery_2026.pdf), p<page>-<n>
  /home/claude/plastmak/work/  k24-<page>-<n>.png: images of the 2024 Plastmak catalogue (16.11.2024 KATALOG KÜÇÜK.pdf) for
                               the 211, 211S and 521S, whose website photos are cropped

The catalogue's cut-outs carry soft masks that lost parts of the white machine bodies (the colour under the lost parts is
gone too), so machines are cut here from the original photos on white with BiRefNet (`W`, alpha cached in
tools/cache/birefnet/); only machines with no other photo keep the catalogue's mask (`C`), after checking.  A `W` photo of
a saw whose roller conveyors run out of the frame is cropped to the machine plus `arms` × its width each side, and the
conveyors fade out at the crop.  Specks a mask leaves around the machine (components under 0.4 % of it) are dropped.
`LINE` lines up the cut-outs of a production group.  Written to tools/src-images/plastmak/<key>.webp|jpg — cut-outs as
RGBA WebP (q 95, lossless alpha; make_images keeps the alpha), photos as JPEG, all at most 1,800 px.

    python3 tools/plastmak_photos.py [key ...] [--missing]      then   python3 tools/make_images.py --only $(cat tools/plastmak_keys.txt)
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "plastmak")
BR, W_, K = "/home/claude/plastmak/img/", "/home/claude/plastmak/web/", "/home/claude/plastmak/work/"
MAX_SIDE = 1800                 # the site uses 1200 px at most; keeps the repo lean


def C(src, alt, **kw):
    """a cut-out from NovoTech's catalogue, its own mask kept"""
    return dict(src=src, alt=alt, kind="C", **kw)


def W(src, alt, arms=None, size="1024", up=False, crop=None, **kw):
    """a machine photographed on white, cut out here with BiRefNet"""
    return dict(src=src, alt=alt, kind="W", arms=arms, size=size, up=up, crop=crop, **kw)


def P(src, alt, crop=None, **kw):
    """a photo, kept rectangular"""
    return dict(src=src, alt=alt, kind="P", crop=crop, **kw)


def LINE(keys, alt, cols=3):
    """a production group: the cut-outs of its machines (keys exported first) lined up on transparent ground"""
    return dict(keys=keys, alt=alt, kind="LINE", cols=cols)


PHOTOS = {
    # ---- saws ---------------------------------------------------------------------------------------------------------
    "pm-401": W(W_ + "2026_01_401-1-copy.jpg", "Plastmak SÇ 401 aluminum and PVC upcut saw, Ø17-11/16″ (450 mm) blade", arms=0.55),
    "pm-401-table": P(W_ + "2026_01_401-copy.jpg", "SÇ 401 turntable with pneumatic vertical and horizontal clamps"),
    "pm-401-scale": P(W_ + "2024_02_4-14.jpg", "SÇ 401 turntable, 0° – 180° with quick stops"),
    "pm-401-guard": P(W_ + "2024_02_2-21.jpg", "SÇ 401 protective cover over the cutting area"),
    "pm-402": W(W_ + "2026_01_402-1-copy.jpg", "Plastmak SÇ 402 automatic upcut saw, Ø21-5/8″ (550 mm) blade", arms=0.55),
    "pm-403": W(W_ + "2026_01_KML06073-copy.jpg", "Plastmak SÇ 403 automatic upcut saw, Ø23-5/8″ / Ø25-9/16″ (600 / 650 mm) blade", arms=0.55),
    "pm-402-table": P(W_ + "2026_01_402-copy.jpg", "SÇ 402 table: pneumatic clamps, angle scale and roller conveyor"),
    "pm-402-blade": P(W_ + "2026_01_402-copy-1.jpg", "SÇ 402 blade rising through the table"),
    "pm-403-panel": P(W_ + "2026_01_KML09333-copy.jpg", "SÇ 403 control panel and cutting table"),
    "pm-403-clamps": P(W_ + "2026_01_KML09347-copy.jpg", "SÇ 403 horizontal clamp and roller conveyor"),
    "pm-403-blade": P(W_ + "2026_01_KML09355-copy.jpg", "SÇ 403 blade at 45°, profile clamped from above and the side"),
    "pm-403-guard": P(BR + "p15-0.jpg", "SÇ 403 front-rear moving guard"),
    "pm-450": W(W_ + "2026_01_450-copy-1.jpg", "Plastmak SÇ 450 shutter box and lamella saw, Ø21-5/8″ (550 mm) blade", arms=0.6),
    "pm-450-clamps": P(W_ + "2026_01_KML08705-copy.jpg", "SÇ 450 clamping pistons matched to the shutter box"),
    "pm-450-blade": P(W_ + "2024_02_5-11.jpg", "SÇ 450 cutting a roller-shutter box"),
    "pm-450-roller": P(W_ + "2024_02_6-7.jpg", "SÇ 450 pressure roller holding a pack of lamellas"),
    "pm-450-table": P(W_ + "2024_02_2-23.jpg", "SÇ 450 cutting table and controls"),
    "pm-400s": W(W_ + "2026_01_400s-copy.jpg", "Plastmak SÇ 400S double-head saw, 2 × Ø19-11/16″ (500 mm) blades", size="1280"),
    "pm-4000s": W(W_ + "2026_01_sc4000s-copy.jpg", "Plastmak SÇ 4000S servo double-head saw, 2 × Ø23-5/8″ (600 mm) blades", size="1280"),
    "pm-400s-head": P(W_ + "2026_01_DSC08863-Enhanced-NR-copy-2.jpg", "SÇ 400S saw head with guard and profile support"),
    "pm-400s-console": P(W_ + "2026_01_DSC08866-Enhanced-NR-copy-2.jpg", "SÇ 400S control console: touch panel, USB and Ethernet"),
    "pm-400s-vise": P(W_ + "2026_01_DSC08871-Enhanced-NR-copy-2.jpg", "SÇ 400S vise at the saw head"),
    "pm-400s-support": P(W_ + "2026_01_SC-400S.00_00_27_00.Still001-copy-2.jpg", "SÇ 400S automatic support arm for long profiles"),
    "pm-400s-guard": P(BR + "p16-2.jpg", "SÇ 400S short-piece cutting rail guard"),
    "pm-4000s-heads": P(W_ + "2024_02_2-31.jpg", "SÇ 4000S heads tilted to 45° inward"),
    "pm-4000s-tilt": P(W_ + "2026_01_DSC08937-copy-2.jpg", "SÇ 4000S head tilting between 90° and 45°"),
    "pm-4000s-console": P(W_ + "2026_01_KML05972-copy.jpg", "SÇ 4000S head and 10″ touch panel"),
    "pm-4000s-conveyor": P(W_ + "2026_01_KML08376-copy.jpg", "SÇ 4000S moving conveyor between the heads"),
    "pm-4000s-clamps": P(BR + "p18-3.jpg", "SÇ 4000S top clamps for precise cuts"),
    "pm-4000s-slide": P(BR + "p18-4.jpg", "SÇ 4000S linear slide of the moving head"),
    "pm-301": W(W_ + "2026_01_301-1-copy.jpg", "Plastmak SÇ 301 glazing bead saw", arms=0.7),
    "pm-301s": W(W_ + "2026_01_DSC04504-Enhanced-NR-copy-2.jpg", "Plastmak SÇ 301S mouldless glazing bead saw", arms=0.7),
    "pm-301-mould": P(W_ + "2026_01_KML08857-copy.jpg", "SÇ 301 adjustable universal mould"),
    "pm-301-saws": P(W_ + "2024_02_1-10.jpg", "SÇ 301 twin saws cutting the bead at 45°"),
    "pm-301s-wheel": P(W_ + "2024_02_2-12.jpg", "SÇ 301S wheel holding 12 bead profiles"),
    "pm-301s-clamps": P(W_ + "2024_02_3-10.jpg", "SÇ 301S pneumatic bead clamps"),
    "pm-301s-twin": P(W_ + "2026_01_DSC04510-Enhanced-NR-copy-2.jpg", "SÇ 301S cutting two beads at once"),
    "pm-301s-top": P(W_ + "2026_01_DSC04507-Enhanced-NR-copy-2.jpg", "SÇ 301S cutting head from above"),
    "pm-431": W(W_ + "2026_01_431-6-copy.jpg", "Plastmak SÇ 431 overhead miter saw, Ø15-3/4″ (400 mm) blade", arms=0.6),
    "pm-441": C(BR + "p37-0.png", "Plastmak SÇ 441 bench miter saw, Ø11-13/16″ (300 mm) blade"),
    "pm-451": C(BR + "p37-1.png", "Plastmak SÇ 451 bench miter saw, Ø15-3/4″ (400 mm) blade"),
    "pm-431-table": P(W_ + "2024_02_1-22.jpg", "SÇ 431 table, saw guard and pneumatic clamp"),
    "pm-431-head": P(W_ + "2026_01_431-copy.jpg", "SÇ 431 saw head and roller conveyor"),
    # ---- welding & corner cleaning --------------------------------------------------------------------------------------
    "pm-100gp": W(W_ + "2026_01_kaynak-makinasi-copy.jpg", "Plastmak SÇ 100 Gold Plus 4-corner PVC welding machine", size="1280"),
    "pm-100gp-full": W(W_ + "2026_01_DSC08774-Enhanced-NR-copy.jpg", "Plastmak SÇ 100 Gold Plus Full 4-corner welding and cleaning line", size="1280"),
    "pm-gp-head": P(W_ + "2026_01_KML06542-copy-2.jpg", "Gold Plus welding head on its linear rail"),
    "pm-gp-heads": P(W_ + "2026_01_KML06550-copy-2.jpg", "Gold Plus heads and automatic carriers"),
    "pm-gp-top": P(W_ + "2026_01_KML06555-copy-2.jpg", "Gold Plus: the four heads seen from above"),
    "pm-gp-press": P(W_ + "2024_02_3-30.jpg", "Gold Plus welding head with its top presses"),
    "pm-gp-heater": P(W_ + "2024_02_8-3.jpg", "Gold Plus heating plate and clamps"),
    "pm-gp-console": P(W_ + "2024_02_2-34.jpg", "Gold Plus touch screen and barcode scanner"),
    "pm-gp-robot": P(W_ + "2026_03_2.png", "Gold Plus Full robotic carrier arm taking a welded frame to the cleaner"),
    "pm-gp-cleaner": P(W_ + "2024_02_5-6.jpg", "Gold Plus Full CNC corner cleaning station"),
    "pm-gp-corner": P(W_ + "2026_03_3.png", "Welded corners of a laminated and a white PVC frame"),
    "pm-100": W(W_ + "2024_03_sc100-copy-2.jpg", "Plastmak SÇ 100 double-head PVC welding machine", size="1280"),
    "pm-101": W(W_ + "2026_01_101-copy.jpg", "Plastmak SÇ 101 single-head PVC welding machine"),
    "pm-100-head": P(W_ + "2024_03_KML08426-Enhanced-NR-copy-2.jpg", "SÇ 100 welding head"),
    "pm-100-side": P(W_ + "2024_03_DSC08826-copy-2.jpg", "SÇ 100 head and control panel"),
    "pm-100-heater": P(W_ + "2024_03_KML08448-Enhanced-NR-copy.jpg", "SÇ 100 heating plate between the profile clamps"),
    "pm-100-panel": P(BR + "p06-0.jpg", "SÇ 100 operation panel"),
    "pm-100-guide": P(BR + "p06-3.jpg", "SÇ 100 linear guide of the moving head"),
    "pm-101-head": P(W_ + "2026_01_101-copy-1.jpg", "SÇ 101 head with individual top clamps"),
    "pm-101-plates": P(W_ + "2026_01_101-.jpg", "SÇ 101 moulds and heating plate"),
    "pm-6000": W(W_ + "2026_01_sc6000-copy.jpg", "Plastmak SÇ 6000 semi-automatic CNC corner cleaner"),
    "pm-6000s": W(W_ + "2026_01_6000s-copy-2.jpg", "Plastmak SÇ 6000S CNC corner cleaning machine"),
    "pm-6000-panel": P(W_ + "2026_01_sc6000-detay-copy.jpg", "SÇ 6000 touch panel and profile carry tables"),
    "pm-6000-saw": P(W_ + "2024_02_1-7.jpg", "SÇ 6000 Ø9-13/16″ (250 mm) saw behind its guard"),
    "pm-6000-head": P(W_ + "2024_02_6-3.jpg", "SÇ 6000 high-frequency spindle with the cleaning saw"),
    "pm-6000-inside": P(W_ + "2026_01_DSC09003-copy.jpg", "Inside the SÇ 6000: tools and profile stops"),
    "pm-6000s-tools": P(W_ + "2024_02_1-3.jpg", "SÇ 6000S tool group"),
    "pm-6000s-head": P(W_ + "2024_02_4-2.jpg", "SÇ 6000S spindle and saw on the servo axes"),
    "pm-6000s-inside": P(W_ + "2024_02_6-2.jpg", "Inside the SÇ 6000S"),
    "pm-6000s-scraper": P(W_ + "2026_01_6000-0-copy.jpg", "SÇ 6000S scraping tools"),
    "pm-6000s-pendant": P(W_ + "2024_02_2-3.jpg", "SÇ 6000S handwheel for setting the axes"),
    "pm-601": C(BR + "p10-1.png", "Plastmak SÇ 601 corner cleaning machine with 3 knives"),
    "pm-601-inside": P(W_ + "2024_02_2-30.jpg", "SÇ 601 knife stack and profile stops"),
    "pm-601-cutter": P(W_ + "2024_02_3-27.jpg", "SÇ 601 knife cleaning the corner of a laminated profile"),
    "pm-601-scraper": P(W_ + "2024_02_4-19.jpg", "SÇ 601 bearing-guided scraper on the profile surface"),
    # ---- machining centre, CNC, end milling, copy routers ---------------------------------------------------------------
    "pm-4550": W(W_ + "2026_01_DSC08160-Enhanced-NR-copy-2.jpg", "Plastmak SÇ 4550 9-axis aluminum and PVC profile machining and cutting centre", size="1536"),
    "pm-4550-spindles": P(W_ + "2026_01_DSC08072-copy-3.jpg", "SÇ 4550: the ten air-cooled spindles"),
    "pm-4550-heads": P(W_ + "2026_01_DSC08078-copy-2.jpg", "SÇ 4550 spindle heads around the profile"),
    "pm-4550-saw": P(W_ + "2026_01_DSC08079-copy.jpg", "SÇ 4550 Ø21-5/8″ (550 mm) servo cutting unit"),
    "pm-4550-printer": P(W_ + "2026_01_DSC08090-copy-2.jpg", "SÇ 4550 barcode printer and UPS"),
    "pm-4550-outfeed": P(W_ + "2026_01_DSC08098-copy-3.jpg", "SÇ 4550 outlet conveyor with belt system"),
    "pm-4550-station": P(W_ + "2026_01_4550-copy.jpg", "SÇ 4550 waiting station for processed profiles"),
    "pm-5000": W(W_ + "2024_03_5000-copy-scaled.jpg", "Plastmak SÇ 5000 3-axis CNC drilling and milling machine for PVC"),
    "pm-5000s": W(W_ + "2026_01_5000s-copy.jpg", "Plastmak SÇ 5000S 3-axis CNC drilling and milling machine for aluminum and PVC"),
    "pm-5000-screen": P(W_ + "2026_01_5000-copy-2-1.jpg", "SÇ 5000 touch screen"),
    "pm-5000-spindles": P(W_ + "2026_01_5000-.jpg", "SÇ 5000 spindles and profile clamps"),
    "pm-5000-inside": P(W_ + "2026_01_DSC04074-Enhanced-NR-copy.jpg", "Inside the SÇ 5000"),
    "pm-5000-heads": P(W_ + "2026_01_5000-0-copy.jpg", "SÇ 5000 spindle motors on the servo axes"),
    "pm-5000s-screen": P(W_ + "2026_01_DSC04237-copy-2.jpg", "SÇ 5000S 19″ Windows screen with DXF drawing"),
    "pm-5000s-console": P(W_ + "2026_01_DSC04292-Enhanced-NR-copy-2.jpg", "SÇ 5000S working area and screen"),
    "pm-5000s-spindles": P(W_ + "2026_01_DSC04297-Enhanced-NR-copy.jpg", "SÇ 5000S three independent spindles"),
    "pm-5000s-inside": P(W_ + "2026_01_DSC04269-Enhanced-NR-copy.jpg", "Inside the SÇ 5000S"),
    "pm-5000s-clamp": P(W_ + "2026_01_DSC04302-copy.jpg", "SÇ 5000S profile clamp and cutter"),
    "pm-5000s-table": P(W_ + "2026_01_DSC04311-copy.jpg", "SÇ 5000S profile clamps on the wide table"),
    "pm-211": W(K + "k24-13-002.png", "Plastmak SÇ 211 end milling machine with 2-knife cutter set", up=True),
    "pm-211s": W(K + "k24-14-000.png", "Plastmak SÇ 211S end milling machine with serial blade change", up=True),
    "pm-211-front": P(W_ + "2026_01_KML08873-copy.jpg", "SÇ 211 cutter area and controls"),
    "pm-211-vises": P(W_ + "2026_01_211-copy-2.jpg", "SÇ 211 two vertical and one horizontal vise"),
    "pm-211-cutters": P(W_ + "2024_02_3-17.jpg", "SÇ 211 cutter stack and profile stop"),
    "pm-211-stack": P(W_ + "2024_02_4-12-e1717743449576.jpg", "SÇ 211 cutter stack for the mullion end"),
    "pm-211s-change": P(BR + "p27-0.jpg", "SÇ 211S blade group changed with a single button"),
    "pm-501": C(BR + "p28-1.png", "Plastmak SÇ 501 copy router with triple drilling unit"),
    "pm-502s": W(W_ + "2024_02_1-26.jpg", "Plastmak SÇ 502S high-frequency copy router"),
    "pm-512": C(BR + "p30-2.png", "Plastmak SÇ 512 high-frequency 3-hole copy router"),
    "pm-521s": W(K + "k24-31-000.png", "Plastmak SÇ 521S triple water drainage slot router", up=True),
    "pm-542": W(W_ + "2026_01_542-copy.jpg", "Plastmak SÇ 542 high-frequency aluminum copy router"),
    "pm-501-drill": P(W_ + "2024_02_2-25.jpg", "SÇ 501 triple drilling unit"),
    "pm-501-head": P(W_ + "2026_01_501-copy-2-1.jpg", "SÇ 501 copy head and profile clamps"),
    "pm-502-panel": P(W_ + "2024_02_2-26.jpg", "SÇ 502S controls: copy routing, cooling, drainage slot and triple drilling"),
    "pm-502-template": P(W_ + "2026_01_502-copy.jpg", "SÇ 502S universal template"),
    "pm-502-top": P(W_ + "2024_02_3-23.jpg", "SÇ 502S router head and clamps"),
    "pm-512-head": P(W_ + "2024_02_2-11.jpg", "SÇ 512 router head, triple drilling and cooling"),
    "pm-521s-heads": P(W_ + "2026_01_DSC04188-Enhanced-NR-copy-2.jpg", "SÇ 521S three drainage-slot routers"),
    "pm-521s-table": P(W_ + "2026_01_DSC04195-Enhanced-NR-copy-2.jpg", "SÇ 521S routers over the moving table"),
    "pm-542-spindle": P(W_ + "2026_01_542-.jpg", "SÇ 542 18,000 rpm spindle"),
    "pm-542-template": P(W_ + "2026_01_542-copy-1.jpg", "SÇ 542 template system for aluminum hardware cut-outs"),
    "pm-542-head": P(W_ + "2024_02_2-29.jpg", "SÇ 542 router head over the profile clamps"),
    "pm-542-clamp": P(W_ + "2024_02_3-26.jpg", "SÇ 542 pneumatic profile clamp"),
    "pm-542-top": P(W_ + "2024_02_4-18.jpg", "SÇ 542 copy head and template from above"),
    # ---- assembly, portable machines, conveyors ------------------------------------------------------------------------
    "pm-902": W(W_ + "2026_01_DSC08946-Enhanced-NR-copy-2.jpg", "Plastmak SÇ 902 hydraulic corner crimping machine for aluminum"),
    "pm-902-table": P(W_ + "2024_02_3-13.jpg", "SÇ 902 crimping table and support arms"),
    "pm-902-heads": P(W_ + "2026_01_DSC08961-Enhanced-NR-copy-2.jpg", "SÇ 902 knife holders, 4 right and 4 left"),
    "pm-902-knives": P(W_ + "2024_02_5-8.jpg", "SÇ 902 crimping knives"),
    "pm-902-scale": P(W_ + "2024_02_8-1.jpg", "SÇ 902 millimetre scale for knife height and advance"),
    "pm-902-wedge": P(W_ + "2024_02_6-5.jpg", "SÇ 902 pneumatic centring miter wedge"),
    "pm-902-cylinder": P(W_ + "2024_02_4-9.jpg", "SÇ 902 hydraulic knife cylinder"),
    "pm-screw-single": C(BR + "p34-0.png", "Plastmak single screwing machine with roller tables"),
    "pm-screw-double": C(BR + "p36-1.png", "Plastmak double-head screwing machine with support tables"),
    "pm-screw-motor": P(BR + "p36-0.png", "Pneumatic screwing motor", crop=(0, 0, 1500, 640)),
    "pm-sash": C(BR + "p35-0.png", "Plastmak sash assembly machine with laser alignment and automatic screwing"),
    "pm-221": W(W_ + "2024_02_S.C-221.jpg", "Plastmak SÇ 221 portable notching and milling machine"),
    "pm-551": W(W_ + "2024_02_S.C-551.jpg", "Plastmak SÇ 551 portable copy milling machine"),
    "pm-table": C(BR + "p38-3.png", "Two-shelf steel stand for the portable machines"),
    "pm-1000": W(W_ + "2026_01_1000-20-copy.jpg", "Plastmak SÇ 1000 digital measuring conveyor, 9′ 10″ (3 m)"),
    "pm-1000-panel": P(W_ + "2026_01_KML09470-copy.jpg", "SÇ 1000 touch screen and measuring stop"),
    "pm-1001": C(BR + "p38-0.png", "Plastmak SÇ 1001 aluminum roller conveyor"),
    "pm-1002": C(BR + "p38-1.png", "Plastmak SÇ 1002 plastic roller conveyor"),
    "pm-1003": C(BR + "p38-2.png", "Plastmak SÇ 1003 sheet-metal conveyor"),
    "pm-compressor": C(BR + "p43-0.png", "SÇ 801 air compressor, 130 gal (500 l)"),
    # ---- production groups (after the machines above) ------------------------------------------------------------------
    "pm-line-pvc1": LINE(["pm-401", "pm-501", "pm-101", "pm-301", "pm-211", "pm-601"],
                         "PVC single-head group: SÇ 401 saw, SÇ 501 copy router, SÇ 101 welder, SÇ 301 bead saw, SÇ 211 end mill, SÇ 601 corner cleaner"),
    "pm-line-pvc2": LINE(["pm-400s", "pm-501", "pm-100", "pm-301", "pm-211", "pm-601"],
                         "PVC double-head group: SÇ 400S saw, SÇ 501 copy router, SÇ 100 welder, SÇ 301 bead saw, SÇ 211 end mill, SÇ 601 corner cleaner"),
    "pm-line-alu": LINE(["pm-4000s", "pm-5000s", "pm-211s", "pm-902"],
                        "Aluminum double-head group: SÇ 4000S saw, SÇ 5000S CNC, SÇ 211S end mill, SÇ 902 corner crimper", cols=2),
    "pm-line-shop": LINE(["pm-compressor", "pm-400s", "pm-5000", "pm-100", "pm-6000", "pm-211s", "pm-301s"],
                         "PVC window workshop: SÇ 801 compressor, SÇ 400S saw, SÇ 5000 CNC, SÇ 100 welder, SÇ 6000 corner cleaner, "
                         "SÇ 211S end mill, SÇ 301S bead saw", cols=4),
}


# ------------------------------------------------------------------------------------------------ masks
def clean_alpha(alpha, keep=0.004):
    """drop the specks a mask leaves around the machine: alpha components under `keep` × the largest one"""
    a = np.array(alpha)
    lab, n = ndimage.label(a > 24)
    if n <= 1:
        return alpha
    sizes = ndimage.sum(np.ones_like(a), lab, range(1, n + 1))
    drop = [i + 1 for i, s in enumerate(sizes) if s < keep * sizes.max()]
    if drop:
        a[np.isin(lab, drop)] = 0
    return Image.fromarray(a)


def focus_box(im, arms, thr=236, pad=0.03):
    """content box of a machine on white; with `arms`, the body (columns carrying most of the machine) plus arms × its width
    each side.  Returns the box and which sides cut through content."""
    g = np.asarray(im.convert("L"))
    m = g < thr
    cols, rows = m.sum(0), m.sum(1)
    xs, ys = np.where(cols > 2)[0], np.where(rows > 2)[0]
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cut_l = cut_r = False
    if arms is not None:
        body = np.where(cols > 0.35 * cols.max())[0]
        bx0, bx1 = body.min(), body.max()
        bw = bx1 - bx0
        nx0, nx1 = max(x0, bx0 - int(arms * bw)), min(x1, bx1 + int(arms * bw))
        cut_l, cut_r = nx0 > x0 + 10, nx1 < x1 - 10
        x0, x1 = nx0, nx1
        ys = np.where(m[:, x0:x1 + 1].sum(1) > 2)[0]
        y0, y1 = ys.min(), ys.max()
    px, py = int(pad * (x1 - x0)), int(pad * (y1 - y0))
    box = (max(0, x0 - (0 if cut_l else px)), max(0, y0 - py), min(im.width, x1 + 1 + (0 if cut_r else px)), min(im.height, y1 + 1 + py))
    return box, cut_l, cut_r


def fade_sides(alpha, left, right, frac=0.07):
    """conveyors that run out of the photo fade out over the outer `frac` of the width instead of ending in a straight cut"""
    a = np.asarray(alpha).astype(np.float32)
    h, w = a.shape
    n = max(8, int(frac * w))
    ramp = np.linspace(0.0, 1.0, n, dtype=np.float32)
    if left:
        a[:, :n] *= ramp[None, :]
    if right:
        a[:, w - n:] *= ramp[::-1][None, :]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def matte_rgba(im):
    """RGBA → (RGB matted on white, cleaned alpha)"""
    im = im.convert("RGBA")
    alpha = clean_alpha(im.split()[-1])
    im.putalpha(alpha)
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB"), alpha


def fit(im, alpha=None):
    s = MAX_SIDE / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        if alpha is not None:
            alpha = alpha.resize(im.size, Image.LANCZOS)
    return im, alpha


def save_cutout(key, rgb, alpha):
    bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    rgb, alpha = rgb.crop(bb), alpha.crop(bb)
    rgb, alpha = fit(rgb, alpha)
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return save_rgba(key, out)


def save_rgba(key, out):
    """cut-outs as WebP: near-lossless colour (q 95), lossless alpha — a tenth of a PNG's size for the same picture"""
    path = os.path.join(DST, key + ".webp")
    for e in (".png", ".jpg"):
        if os.path.exists(os.path.join(DST, key + e)):
            os.remove(os.path.join(DST, key + e))
    out.save(path, quality=95, alpha_quality=100, method=6)
    return path, out.size


# ------------------------------------------------------------------------------------------------ kinds
def birefnet_cutout(key, spec):
    from birefnet_cut import cut_rgba
    im = Image.open(spec["src"])
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert("RGB")
    if spec.get("crop"):
        im = im.crop(spec["crop"])
    box, cut_l, cut_r = focus_box(im, spec.get("arms"))
    im = im.crop(box)
    if spec.get("up"):
        from esrgan import upscale
        im = upscale(im)
    cut = cut_rgba(im, spec.get("size", "1024"), cache_key=f"plastmak-{key}")
    alpha = clean_alpha(cut.getchannel("A"))
    if cut_l or cut_r:
        alpha = fade_sides(alpha, cut_l, cut_r)
    return save_cutout(key, im, alpha)


def lineup(keys, cols):
    """machines of a production group in a grid of equal cells, each scaled to fit its cell, standing on a common line"""
    parts = [Image.open(os.path.join(DST, k + ".webp")).convert("RGBA") for k in keys]
    cell, gap = 820, 70
    rows = (len(parts) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell + (cols - 1) * gap, rows * cell + (rows - 1) * gap), (255, 255, 255, 0))
    for k, im in enumerate(parts):
        s = min(cell / im.width, cell / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        r, c = divmod(k, cols)
        n_in_row = min(cols, len(parts) - r * cols)
        x0 = (sheet.width - (n_in_row * cell + (n_in_row - 1) * gap)) // 2       # centre a short last row
        sheet.alpha_composite(im, (x0 + c * (cell + gap) + (cell - im.width) // 2, r * (cell + gap) + (cell - im.height)))
    return sheet


def process(key, spec):
    os.makedirs(DST, exist_ok=True)
    kind = spec["kind"]
    if kind == "LINE":
        out = lineup(spec["keys"], spec["cols"])
        out = out.crop(out.getchannel("A").getbbox())
        rgb, alpha = fit(out.convert("RGB"), out.getchannel("A"))
        out = rgb.convert("RGBA"); out.putalpha(alpha)
        return save_rgba(key, out)
    if kind == "W":
        return birefnet_cutout(key, spec)
    im = Image.open(spec["src"])
    if kind == "C":
        rgb, alpha = matte_rgba(im)
        return save_cutout(key, rgb, alpha)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert("RGB")
    if spec.get("crop"):
        im = im.crop(spec["crop"])
    im, _ = fit(im)
    path = os.path.join(DST, key + ".jpg")
    for e in (".png", ".webp"):
        if os.path.exists(os.path.join(DST, key + e)):
            os.remove(os.path.join(DST, key + e))
    im.save(path, quality=90)
    return path, im.size


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    missing = "--missing" in sys.argv          # only keys without an export yet
    keys = args or list(PHOTOS)
    order = {"P": 0, "C": 1, "W": 2, "LINE": 3}                # fast ones first, line-ups after their machines
    for key in sorted(keys, key=lambda k: order[PHOTOS[k]["kind"]]):
        if missing and any(os.path.exists(os.path.join(DST, key + e)) for e in (".webp", ".jpg")):
            continue
        path, size = process(key, PHOTOS[key])
        print(f"{key:24s} {size} -> {os.path.relpath(path, ROOT)}", flush=True)
    print("exit 0", flush=True)


if __name__ == "__main__":
    main()
