#!/usr/bin/env python3
"""Gecam (Parma, Italy) deburring, finishing, corner grinding and corner welding machines, and the Eurofintec pipe finishing
machines Gecam builds — photos from four sources outside the repo:

  /home/claude/gecam/img/      gecam.com product images (Oct 25): machines on white (cut out by BiRefNet in make_images, `B`),
                               detail photos and samples (kept rectangular, `P`)
  /home/claude/gecam/catimg/   images of the 2026 Gecam catalogue (Catalogo_Gecam_EN_26.pdf, pdfimages -p): machines as RGBA
                               cut-outs (rgba-<page>-<n>.png, image + soft mask, `C`), details, and the worked samples of page 22
  /home/claude/gecam/boximg/   images of the metal-box brochure (metal_box_deburring_and_grinding_machine.pdf): CWS touch screen

Small images are upscaled 2x with Real-ESRGAN (`up`); cut-outs are matted on white with their alpha resized to match and
written as PNG, photos as JPEG.  Written to tools/src-images/gecam/<key>.png|jpg.

    python3 tools/gecam_photos.py [key ...]      then   python3 tools/make_images.py --only $(cat tools/gecam_keys.txt)
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "tools", "src-images", "gecam")
W, CAT, BOX = "/home/claude/gecam/img/", "/home/claude/gecam/catimg/", "/home/claude/gecam/boximg/"
OWN = "/home/claude/gecam/owner/"     # photos the owner sent (Nov 7 2026), turned upright from their EXIF orientation
WEL = "/home/claude/gecam/welcor/"    # images of GECAM's corner welder offers to NovoTech and the WELCOR 4-axis brochure (Nov 7 2026);
                                      # welcor-4-copper-group.png: the two halves of the offer's photo joined, the phone watermark removed
MAX_SIDE = 2600


def C(src, alt, up=False, **kw):
    """an RGBA cut-out"""
    return dict(src=src, alt=alt, up=up, cutout=True, **kw)


def B(src, alt, up=False, crop=None, **kw):
    """a machine on a white background, cut out by BiRefNet in make_images"""
    return dict(src=src, alt=alt, up=up, crop=crop, cutout=True, rect=True, **kw)


def P(src, alt, crop=None, up=False, **kw):
    """a photo, kept rectangular"""
    return dict(src=src, alt=alt, crop=crop, up=up, cutout=False, **kw)


PHOTOS = {
    # ---- G15 · G30 compact deburring machines -------------------------------------------------------------------------
    "gc-g15": C(CAT + "rgba-006-008.png", "Gecam G15 compact deburring machine, 5-7/8″ working width", up=True),
    "gc-g30": C(CAT + "rgba-007-015.png", "Gecam G30 deburring machine, 11-13/16″ working width", up=True),
    "gc-g15-infeed": P(CAT + "g-006-010.png", "G15 conveyor belt at the infeed", up=True),
    "gc-g15-brushes": P(CAT + "g-006-011.png", "G15 rotating and oscillating top brushes (T group)", up=True),
    "gc-g30-belts": P(CAT + "g-007-012.png", "Two abrasive belt units (R groups) inside a G30", up=True),
    "gc-g30-rb": P(W + "RB.jpg", "Abrasive belt and cylindrical brush (R + B groups) in a G30", up=True),
    "gc-g30-panel": P(CAT + "g-007-014.png", "G30 control panel", up=True),
    "gc-g30-rollers": P(CAT + "g-007-013.png", "Rubberized pressure rollers at the G30 infeed", up=True),
    "gc-g30-conveyor": P(W + "rulliera-G.jpg", "Additional infeed and outfeed rollers (optional)"),
    "gc-g30-sample": P(W + "DSC03725.jpg", "Laser-cut plate after deburring and edge rounding"),
    "gc-sample-r": C(CAT + "rgba-022-103.png", "Sample: deburred with the abrasive belt (R group)", up=True),
    # ---- G65 · G135 wide-belt deburring machines ----------------------------------------------------------------------
    "gc-g65": C(CAT + "rgba-008-020.png", "Gecam G65 wide-belt deburring machine, 25-9/16″ working width", up=True),
    "gc-g135": C(CAT + "rgba-009-025.png", "Gecam G135 wide-belt deburring machine, 53-1/8″ working width", up=True),
    "gc-g65-glass": B(W + "GE65.jpg", "G65 wide-belt deburring machine with glazed side doors"),
    "gc-g65-rxb4": P(W + "G65_RXB4.jpg", "Inside a G65 RXB4: abrasive belt, top brushes and four-brush carousel"),
    "gc-g65-rx": P(W + "RX_CONFIG.jpg", "Abrasive belt unit and double row of top brushes (R + X groups)"),
    "gc-g135-rxr": P(W + "RXR-1.jpg", "G135 with belt, top-brush and belt units (RXR)"),
    "gc-x-brushes": P(CAT + "g-008-017.png", "Top brushes of the X group, turning and oscillating across the part", up=True),
    "gc-touch": P(W + "PLC_low.jpg", "Touch screen: speed, thickness and working pressure of every group"),
    "gc-grit-set": P(W + "grit-set.jpg", "Electronic grit set: the belt thickness stored for each grit"),
    "gc-g135-ext-brush": B(W + "spazzola-esterna.jpg", "G135 with the external cylindrical brush below the outfeed (b group, configurable)"),
    "gc-g135-long-table": B(W + "G135-piano-lungo.jpg", "Wide-belt deburring machine with extended infeed table (optional)"),
    "gc-belt-cleaning": P(W + "spazzola-pulizia-tappeto.jpg", "Conveyor belt cleaning brush (optional)"),
    "gc-g135-dust": P(W + "G135GDC6000.jpg", "G135 connected to a Gecam GDC cartridge dust collector (optional)"),
    "gc-sample-rx": C(CAT + "rgba-022-093.png", "Sample: deburred and edge-rounded with belt and top brushes (RX)", up=True),
    "gc-sample-rxx": C(CAT + "rgba-022-107.png", "Sample: deburred and rounded with RXX", up=True),
    "gc-sample-rb": C(CAT + "rgba-022-101.png", "Sample: deburred and finished with belt and cylindrical brush (RB)", up=True),
    "gc-sample-oxide": C(CAT + "rgba-022-095.png", "Sample: oxide removed from laser-cut edges with the X group", up=True),
    # ---- GM65 · GM110 single-belt finishing machines ------------------------------------------------------------------
    "gc-gm65": C(CAT + "rgba-012-039.png", "Gecam GM65 single-belt deburring and satin finishing machine, 25-9/16″", up=True),
    "gc-gm110": C(CAT + "rgba-013-045.png", "Gecam GM110 single-belt deburring and satin finishing machine, 43-5/16″", up=True),
    "gc-gm-belt": P(CAT + "rgba-012-041.png", "Abrasive belt unit of a GM machine", up=True),
    "gc-sample-brass": P(CAT + "g-012-037.png", "Satin-finished brass part", up=True),
    "gc-sample-plate": P(CAT + "g-012-038.png", "Deburred and satin-finished steel plate", up=True),
    "gc-sample-copper": P(CAT + "g-013-047.png", "Copper bar after deburring", up=True),
    "gc-sample-hairline": C(CAT + "rgba-022-109.png", "Sample: hairline (satin) finish", up=True),
    "gc-sample-satin": C(CAT + "rgba-022-113.png", "Sample: satin finish with the abrasive belt (R)", up=True),
    # ---- G30 WET · G65/135 WET ----------------------------------------------------------------------------------------
    "gc-g30-wet": B(W + "GE30_wet.jpg", "Gecam G30 WET wet deburring machine, 11-13/16″"),
    "gc-g65-wet": C(CAT + "rgba-019-077.png", "Gecam G65/135 WET wet deburring machine, 51-3/16″", up=True),
    "gc-g30-wet-side": B(W + "G3WRR_laterale.jpg", "G30 WET with two belt units (RR), side view"),
    "gc-wet-rr": P(W + "RR.jpg", "Two abrasive belt units (RR) of a wet machine"),
    "gc-wet-rt": P(W + "G3-wet-RT-config.jpg", "Belt unit and top brushes (RT) in a G30 WET"),
    "gc-sample-rbb": C(CAT + "rgba-022-099.png", "Sample: satin finish with belt and two cylindrical brushes (RBB)", up=True),
    # ---- G135RB8 -------------------------------------------------------------------------------------------------------
    "gc-g135rb8": B(W + "G135-RB8.jpg", "Gecam G135RB8 edge rounding machine with eight-brush carousel, 53-1/8″"),
    "gc-rb8-carousel": P(W + "G135RB8_INT.jpg", "Carousel of eight cylindrical abrasive brushes turning in both directions"),
    "gc-rb8-belt": P(W + "G135-RB8_R.jpg", "Abrasive belt unit (R group) of the G135RB8", up=True),
    "gc-rb8-touch": P(W + "TOUCH-1.jpg", "Touch-screen control of the G135RB8"),
    "gc-rb8-before-after": P(W + "campioni-prima-dopo.jpg", "Laser-cut parts before and after edge rounding"),
    "gc-rb8-plate": P(CAT + "g-010-029.png", "Plate with edges rounded, inside the holes too", up=True),
    "gc-sample-r2": C(CAT + "rgba-022-097.png", "Sample: 5/64″ (2 mm) edge radius from the eight-brush carousel", up=True),
    "gc-sample-rb8": C(CAT + "rgba-022-111.png", "Sample: deburred and rounded with RB8", up=True),
    # ---- GT06 · GT13 ----------------------------------------------------------------------------------------------------
    "gc-gt06": B(W + "GT06.jpg", "Gecam GT06 double-sided edge rounding machine, 23-5/8″"),
    "gc-gt13": B(W + "GT13-1.jpg", "Gecam GT13 double-sided edge rounding machine, 51-3/16″"),
    "gc-gt13-rcs": B(W + "GT13RCS-sc.jpg", "GT13 in RCS configuration", up=True),
    "gc-gt06-inside": P(W + "GT06-UP.jpg", "Cross belts with strip brushes working above and below the part"),
    "gc-gt-strips": P(W + "DSC02723.jpg", "Strip brushes on a cross belt", up=True),
    "gc-gt-gauge": P(W + "calibro-spazzole.jpg", "Strip brushes, easily replaced as they wear"),
    "gc-gt-touch": P(W + "touch.jpg", "Touch screen with stored work programs"),
    "gc-sample-holes": C(CAT + "rgba-022-105.png", "Sample: deburred and rounded inside the holes", up=True),
    # ---- G65DCC ---------------------------------------------------------------------------------------------------------
    "gc-g65dcc": C(CAT + "rgba-016-060.png", "Gecam G65DCC deslagging and edge rounding machine, 23-5/8″", up=True),
    "gc-dcc-inside": P(W + "DSC_0141-1.jpg", "D belt on its large rubber roller and the C strip-brush belts"),
    "gc-dcc-touch": P(W + "touch-screen.jpg", "G65DCC touch screen"),
    "gc-dcc-before": P(W + "DSC_0467.jpg", "Plasma-cut part with slag, before deslagging"),
    "gc-dcc-after": P(W + "DSC_0488.jpg", "Plasma-cut part after deslagging and edge rounding"),
    "gc-dcc-edge": P(W + "DSC_0579.jpg", "Plate edge with slag (left) and after the G65DCC (right)"),
    "gc-dcc-thick": P(W + "DSC_0013.jpg", "Thick plasma-cut part — the work the G65DCC deslags"),
    # ---- CUB brush deburring machines -----------------------------------------------------------------------------------
    "gc-cub": B(W + "CUB30-BB.jpg", "Gecam CUB brush deburring machine with two brush heads"),
    "gc-cub-cat": C(CAT + "rgba-014-048.png", "CUB brush deburring machine with two brush units", up=True),
    "gc-cub-30": B(W + "CUB30.jpg", "Gecam CUB 30 brush deburring machine with conveyor", up=True),
    "gc-cub-compact": C(CAT + "rgba-014-052.png", "Compact CUB brush deburring machine", up=True),
    "gc-cub-brushes": P(W + "CUB-BRUSHES.jpg", "Two cylindrical brush heads with independent pressure adjustment"),
    "gc-cub-heads": P(W + "DSC_0141.jpg", "CUB brush heads, positioned by handwheel"),
    "gc-sample-scotch": C(CAT + "rgba-022-115.png", "Sample: Scotch-Brite finish with a cylindrical brush (B group)", up=True),
    # ---- EASY T ----------------------------------------------------------------------------------------------------------
    "gc-easy-t": B(W + "Easty-T.jpg", "Gecam EASY T brushing workstation with vacuum table"),
    "gc-easy-t-tools": P(W + "doppio-utensile.jpg", "Two tools on the 180° tilting arm"),
    "gc-easy-t-work": P(W + "DSC_0311.jpg", "Brushing a part held down by the vacuum table"),
    "gc-easy-t-operator": P(CAT + "g-015-056.png", "Operator guiding the brush head along a part", up=True),
    "gc-easy-t-brush": P(CAT + "g-015-057.png", "Top brush rounding the edges of a part", up=True),
    # ---- GCB --------------------------------------------------------------------------------------------------------------
    "gc-gcb": B(W + "GCB25RR_completa.jpg", "Gecam GCB 25 RR double crossed-belt deburring bench"),
    "gc-gcb-cat": C(CAT + "rgba-011-032.png", "GCB bench with crossed belts and table", up=True),
    "gc-gcb-work": P(W + "DSC_0790.jpg", "Operator deburring a part on the GCB"),
    "gc-gcb-brush": P(W + "spazzola.jpg", "Single independent brush (T group) for edge rounding"),
    "gc-gcb-vacuum": P(W + "DSC_0192.jpg", "Suction-cup manipulator for shaped parts (optional)"),
    # ---- 135 automatic corner grinder -------------------------------------------------------------------------------------
    "gc-135": B(OWN + "135-hd.jpg", "GECAM 135 automatic corner grinder"),          # the owner's larger copies (Nov 7 2026)
    "gc-135-2h": B(W + "135_2T.jpg", "GECAM 135 two-head version"),
    "gc-135-head": P(W + "testa-135.jpg", "GECAM 135 grinding head on its carriage"),
    "gc-135-pad": P(OWN + "135-pad-hd.jpg", "Pad and contact roller pressing the belt on the weld"),
    "gc-135-guides": P(OWN + "135-guides-hd.jpg", "Two grinding heads over the part support with plastic slides"),
    "gc-135-touch": P(W + "DSC_0095.jpg", "Touch-screen control (optional)"),
    "gc-135-sample": P(W + "campione-135.jpg", "Box edge after weld grinding on the GECAM 135"),
    # ---- 131 · 136 corner grinders ----------------------------------------------------------------------------------------
    "gc-136": B(W + "136.jpg", "GECAM 136 corner grinder"),
    "gc-131": B(OWN + "131-hd.jpg", "GECAM 131 corner grinder", up=True),
    "gc-136-box": B(W + "136-con-scatola.jpg", "GECAM 136 grinding the welded corner of a box"),
    "gc-136-head": P(W + "testa.jpg", "GECAM 136 belt head with oscillating fork"),
    "gc-131-table": P(W + "131-piano-guide.jpg", "GECAM 131 work table with squaring guides"),
    "gc-131-head": P(OWN + "131-head-hd.jpg", "GECAM 131 belt fork at a box corner"),
    # the owner's photos (Nov 7 2026)
    "gc-131-showroom": P(OWN + "131-showroom.jpg", "GECAM 131 with its control panel, work table and dust extraction"),
    "gc-131-showroom-2": P(OWN + "131-showroom-2.jpg", "GECAM 131 work table and belt housing"),
    "gc-131-belt": P(OWN + "131-belt.jpg", "GECAM 131 abrasive belt between the guide plates"),
    "gc-131-dust": P(OWN + "131-dust-collector.jpg", "GECAM 131 with its dust extraction fan", up=True),
    "gc-131-panel": P(OWN + "131-panel.jpg", "GECAM 131 control panel"),
    "gc-131-extractor": P(OWN + "131-extractor.jpg", "Dust extraction fan on the GECAM 131"),
    "gc-131-grinding": P(OWN + "131-grinding.jpg", "GECAM 131 grinding the corner weld of a steel box", crop=(0, 0, 2534, 1293)),
    "gc-136-studio": B(OWN + "136-studio.jpg", "GECAM 136 with a box on the work table"),
    "gc-136-side": P(OWN + "136-side.jpg", "GECAM 136 inclined belt head, dust hood and drive motor"),
    "gc-136-top": P(OWN + "136-top.jpg", "GECAM 136 work table, part stop and dust hood"),
    "gc-136-table": P(OWN + "136-table.jpg", "GECAM 136 work table with guides and hand wheel", up=True),
    "gc-136-guide": P(OWN + "136-guide.jpg", "Abrasive belt and part guide of the GECAM 136"),
    "gc-136-belt": P(OWN + "136-belt.jpg", "GECAM 136 belt under the work table edge", up=True),
    "gc-136-grinding": P(OWN + "136-grinding.jpg", "GECAM 136 grinding the weld of a steel box"),
    "gc-136-corner": P(OWN + "136-corner.jpg", "Box corner radiused on the GECAM 136"),
    "gc-136-before-after": P(OWN + "136-before-after.jpg", "Welded box corner before and after grinding"),
    "gc-box-corner": P(BOX + "x-002-025.png", "Box corner after weld grinding", up=True),
    # ---- special corner grinders --------------------------------------------------------------------------------------------
    "gc-upper-corner": B(W + "GS059LV.jpg", "Gecam automatic upper-corner grinder with two heads"),
    "gc-six-head": B(W + "DSC_0656.jpg", "Gecam six-head PLC corner grinder"),
    "gc-tube-corner": B(W + "GS040DE.jpg", "Gecam four-head corner grinder for 90° tube frames", up=True),
    "gc-upper-corner-panel": P(W + "control-GS059LV.jpg", "Touch-screen control of the upper-corner grinder"),
    "gc-six-head-heads": P(W + "stretto-teste.jpg", "Lower heads of the six-head grinder at a box corner"),
    "gc-six-head-pads": P(W + "pattini.jpg", "Rubber pads pressing the belts on two corners at once"),
    "gc-tube-corner-table": P(W + "piano-appoggio.jpg", "Frame support of the tube corner grinder"),
    "gc-tube-corner-heads": P(W + "teste-laterali.jpg", "Side heads of the tube corner grinder"),
    "gc-corner-before": P(W + "campione-prima.jpg", "Welded box corner before grinding"),
    "gc-corner-after": P(W + "campione-dopo.jpg", "The same corner after grinding"),
    # ---- CWS corner welding machines ------------------------------------------------------------------------------------------
    "gc-cws": B(W + "CWS-300.jpg", "GECAM CWS 300 one-axis corner welding machine"),
    "gc-cws-welding": P(W + "lavorazione.jpg", "TIG torch welding a corner along the copper guide"),
    "gc-cws-copper": P(W + "gruppo-rame.jpg", "Copper groups that hold the corner and draw off the heat"),
    "gc-cws-stop": P(W + "riscontro.jpg", "External copper squaring guide the corner rests against"),
    "gc-cws-touch": P(BOX + "x-002-031.png", "Touch panel of the CWS", up=True),
    "gc-cws-bent": P(W + "piega.jpg", "Bent corner before welding"),
    "gc-cws-welded": P(W + "saldato.jpg", "Welded corner"),
    "gc-cws-boxes": P(BOX + "x-002-030.png", "Corner-welded boxes", up=True),
    "gc-cws-bend": P(WEL + "bend-rule.png", "How the corner is bent for welding: the edges .0004″ (0.01 mm) apart and centred, or "
                     "overlapping by half the sheet thickness at most"),
    "gc-lorch-t250": B(WEL + "lorch-t250.png", "Lorch T-series TIG power source — GECAM offers the T 250 with its corner welders",
                       up=True),          # the photo of the offers shows a T 220
    # 2-axis: GECAM's CWS 300 2 axes XY offer
    "gc-cws-xy": B(WEL + "cws-300-xy.png", "GECAM CWS 300 XY two-axis corner welding machine", up=True),
    "gc-cws-xy-corner": P(WEL + "cws-xy-corner.png", "Box corner clamped against the copper groups, TIG torch at the seam"),
    "gc-cws-xy-head": P(WEL + "cws-xy-head.png", "Torch and copper corner group of the CWS 300 XY"),
    "gc-cws-xy-touch": P(WEL + "cws-xy-touch.png", "Touch panel of the CWS 300 XY: X and Y positions, part counter, recipe number"),
    "gc-cws-xy-copper": P(WEL + "cws-xy-copper.png", "Inner copper group pressing the corner from inside, torch below", up=True),
    # WELCOR 400: the 3-axis offer (render, drawings) and the 4-axis offer (photos)
    "gc-welcor": B(WEL + "welcor-400-render.png", "GECAM WELCOR 400 corner welder", up=True),
    "gc-welcor-front": P(WEL + "welcor-400-front.png", "WELCOR 400 front view with the largest box, 39-3/8 × 39-3/8″ (1,000 × 1,000 mm), "
                         "corner up — machine 43-5/16″ (1,100 mm) wide", up=True),
    "gc-welcor-side": P(WEL + "welcor-400-side.png", "WELCOR 400 side view: torch axes, welding torch and pneumatic block — machine "
                        "87″ (2,210 mm) high, 61-3/4″ (1,569 mm) deep", up=True),
    "gc-welcor-4": P(WEL + "welcor-4-frame.png", "GECAM WELCOR 400 4-axis welding the corner of a square frame"),
    "gc-welcor-4-laser": P(WEL + "welcor-4-laser.png", "Laser sensor beside the TIG torch on the rotary actuator"),
    "gc-welcor-4-clamps": P(WEL + "welcor-4-clamps.png", "Pneumatic clamps and copper pads holding the corner"),
    "gc-welcor-4-panel": P(WEL + "welcor-4-panel.png", "Control panel with color touch screen and signal tower"),
    "gc-welcor-4-copper": P(WEL + "welcor-4-copper-group.png", "Copper group: aluminum support and copper unit, 3/8″ to 7-7/8″ "
                            "(10 – 200 mm) thick"),
    "gc-welcor-4-path": P(WEL + "welcor-4-path.png", "Largest torch path, 15-3/4 × 1-7/8 × 4-7/16″ (400 × 48 × 112 mm), on a box up "
                          "to 39-3/8 × 39-3/8″ (1,000 × 1,000 mm)"),
    # ---- Eurofintec 141 · 144 orbital pipe sanders ---------------------------------------------------------------------------
    "ef-141": B(W + "141.jpg", "Eurofintec 141 orbital pipe sander, Ø3/8″ – 3-1/8″"),
    "ef-144": B(W + "144alimentatore.jpg", "Eurofintec 144 orbital pipe sander, Ø9/16″ – 5-7/8″, with feeder (optional)", up=True),
    "ef-141-bend": P(W + "141-tubo-gomito.jpg", "141 sanding a bent tube"),
    "ef-141-small": P(W + "141-tubo-piccolo.jpg", "141 sanding small-diameter tube"),
    "ef-144-feeder": P(W + "alimentatore.jpg", "Automatic feeder kit on the 144 (optional)"),
    "ef-144-panel": P(W + "144-quadro-elett.jpg", "144 control box"),
    # ---- Eurofintec 128 S · 128 SL · 128 DL centreless ------------------------------------------------------------------------
    "ef-128sl": B(W + "128SL.jpg", "Eurofintec 128 SL centreless pipe sander"),
    "ef-128dl": B(W + "128DL.jpg", "Eurofintec 128 DL two-head centreless sander", up=True),
    "ef-128-work": P(W + "DSC_0847.jpg", "128 SL sanding a tube"),
    "ef-128-wheel": P(W + "DSC_0162.jpg", "Contact wheel and belt of the 128"),
    "ef-128dl-heads": P(W + "DSC_0964.jpg", "The two heads of the 128 DL"),
    "ef-128dl-guide": P(W + "DSC_0969.jpg", "Prismatic work support of the 128 DL"),
    "ef-128-wet": P(W + "acqua.jpg", "Wet version: coolant on the belt (optional)"),
    # ---- Eurofintec 228 -----------------------------------------------------------------------------------------------------
    "ef-228": B(W + "228.jpg", "Eurofintec 228 pipe sander, Ø3/8″ – 15-3/4″"),
    "ef-228-rollers": B(W + "228rollers.jpg", "228 with pipe roller stands (optional)", up=True),
    "ef-228-work": P(W + "DSC_0063.jpg", "Contrast roller and belt on a pipe"),
    "ef-228-large": P(W + "DSC05005.jpg", "Sanding large-diameter pipe"),
    # ---- Eurofintec 728 · 143 -----------------------------------------------------------------------------------------------
    "ef-728": B(W + "728.jpg", "Eurofintec 728 tube brushing machine", up=True),
    "ef-143": B(W + "143.jpg", "Eurofintec 143 tube-end deburring machine"),
    "ef-143-front": B(W + "CARTER-FRONTALE.jpg", "143 with its front guard, seen from the operator side"),
    "ef-728-brush": P(W + "spazzola-728.jpg", "728 brush and contrast roller"),
    "ef-728-adjust": P(W + "reg.-spazzola-728-1.jpg", "Handwheel adjustment of the brush as it wears"),
    "ef-728-pneumatic": P(W + "pneumatica-728.jpg", "Pneumatic compensation of the contrast roller"),
    "ef-728-contrast": P(W + "gruppo-contrasto-728.jpg", "Grooved rubber contrast roller with tilt adjustment"),
    "ef-143-brush": P(W + "SPAZZOLA-1.jpg", "Wire brush of the 143"),
    "ef-143-45": P(W + "Accessorio-45.jpg", "Support for tube ends cut at 45°", up=True),
}


def matte_rgba(im):
    """RGBA → (RGB matted on white, alpha)"""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB"), im.split()[-1]


def fit(im, alpha=None):
    s = MAX_SIDE / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        if alpha is not None:
            alpha = alpha.resize(im.size, Image.LANCZOS)
    return im, alpha


def process(key, spec):
    im = Image.open(spec["src"])
    os.makedirs(DST, exist_ok=True)
    if spec.get("cutout") and not spec.get("rect"):
        rgb, alpha = matte_rgba(im)
        bb = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
        rgb, alpha = rgb.crop(bb), alpha.crop(bb)
        if spec.get("up"):
            from esrgan import upscale
            big = upscale(rgb)
            alpha = alpha.resize(big.size, Image.LANCZOS)
            rgb = big
        rgb, alpha = fit(rgb, alpha)
        out = rgb.convert("RGBA"); out.putalpha(alpha)
        path = os.path.join(DST, key + ".png")
        if os.path.exists(os.path.join(DST, key + ".jpg")):
            os.remove(os.path.join(DST, key + ".jpg"))
        out.save(path, optimize=True)
        return path, out.size
    im = im.convert("RGB")
    if spec.get("crop"):
        im = im.crop(spec["crop"])
    if spec.get("up"):
        from esrgan import upscale
        im = upscale(im)
    im, _ = fit(im)
    path = os.path.join(DST, key + ".jpg")
    if os.path.exists(os.path.join(DST, key + ".png")):
        os.remove(os.path.join(DST, key + ".png"))
    im.save(path, quality=92)
    return path, im.size


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    missing = "--missing" in sys.argv          # only keys without an export yet
    keys = args or list(PHOTOS)
    for key in keys:
        if missing and any(os.path.exists(os.path.join(DST, key + e)) for e in (".png", ".jpg")):
            continue
        path, size = process(key, PHOTOS[key])
        print(f"{key:24s} {size} -> {os.path.relpath(path, ROOT)}", flush=True)


if __name__ == "__main__":
    main()
