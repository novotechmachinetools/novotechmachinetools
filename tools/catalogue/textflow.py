"""Running text set again in English: on the pages where EUROSTAMP's Italian and English are whole paragraphs (the
introduction, the section openers, the ESH and EUROGRIP pages), both languages are taken out of the regions listed here
and the English — rewritten in plain North American English, with inch values beside the millimetres — is set in their
place, in the catalogue's own fonts and colours.

  clear   regions whose text is removed (a line goes when its centre is inside), with the grey bars that separated the
          Italian from the English
  box     where the new text is set: given, or 'auto' — from the top-left of the removed text to the region's bottom-right
  html    the text, with the classes of CSS below (b: body, h: heading, t: title, l: list item …)

handler(page, ppage, ctx) clears the regions before the line-by-line clean-up; post(page, ctx) sets the text after the
inch values are in (the boxes are reserved, so no inch value is placed where the text will go).
"""
import os

import fitz

from textedit import Editor, page_lines

HERE = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(os.path.dirname(HERE), "fonts", "roboto")
ARCHIVE = fitz.Archive(FONTDIR)

BLUE, INK, GREY, WARM = "#005688", "#231f20", "#58595b", "#8b807b"
CSS = """
@font-face {font-family: RT; src: url(Roboto-Thin.ttf);}
@font-face {font-family: RL; src: url(Roboto-Light.ttf);}
@font-face {font-family: RR; src: url(Roboto-Regular.ttf);}
@font-face {font-family: RM; src: url(Roboto-Medium.ttf);}
@font-face {font-family: RB; src: url(Roboto-Bold.ttf);}
@font-face {font-family: SL; src: url(RobotoSlab-Light.ttf);}
@font-face {font-family: SR; src: url(RobotoSlab-Regular.ttf);}
@font-face {font-family: SB; src: url(RobotoSlab-Bold.ttf);}
@font-face {font-family: SX; src: url(RobotoSlab-ExtraBold.ttf);}
* {margin: 0; padding: 0;}
p {font-family: RL; font-size: 9.5px; color: %(INK)s; line-height: 1.26; margin: 0 0 5.2px 0; text-align: left;}
.h {font-family: RR; font-size: 10px; color: %(BLUE)s; line-height: 1.2; margin: 0 0 3.2px 0;}
.h2 {font-family: RR; font-size: 10px; color: %(BLUE)s; line-height: 1.2; margin: 9px 0 3.2px 0;}
.t {font-family: RM; font-size: 10px; color: %(BLUE)s; line-height: 1.12; margin: 0;}
.l {margin-left: 9px; text-indent: -9px;}
.bl {color: %(BLUE)s;}
.w {color: #ffffff;}
.g {color: %(GREY)s;}
.m {font-family: RM;}
.bo {font-family: RB;}
.r {text-align: right;}
.c {text-align: center;}
.j {text-align: justify;}
""" % dict(INK=INK, BLUE=BLUE, GREY=GREY)


def R(*a):
    return fitz.Rect(*a)


def mm(v, places=None):
    """'105 mm (4.13″)' style helper for the copy below: decimal inches, leading zero dropped"""
    x = v / 25.4
    p = places if places is not None else (2 if x >= 1 else 3)
    s = f"{x:.{p}f}"
    return (s[1:] if s.startswith("0.") else s) + "″"


# ------------------------------------------------------------------------------------------------------------- copy
def eurogrip_model(title_clear, col_clear, title, paras, title_box=None, col_box=None):
    """a EUROGRIP model page: the title over the drawing (set to the page's right margin), the description column on
    the right"""
    return [dict(clear=[title_clear], box=title_box or "auto-wide", html=f'<p class="t">{title}</p>'),
            dict(clear=[col_clear], box=col_box or "auto", html=paras)]


def desc(*ps):
    return '<p class="h">DESCRIPTION</p>' + "".join(f"<p>{p}</p>" for p in ps)


def spec(*ps):
    return '<p class="h2">TECHNICAL SPECIFICATIONS</p>' + "".join(f"<p>{p}</p>" for p in ps)


Z1 = (f"height 100 mm ({mm(100)}), body 27 mm ({mm(27)}), bending axis at 7 mm ({mm(7)})")
Z2 = (f"height 120 mm ({mm(120)}), body 40 mm ({mm(40)}), bending axis at 20 mm ({mm(20)})")
CHECK = "Check every dimension of your intermediates against the drawing on this page."
TOP_FEATURES = ('<p class="h">TECHNICAL FEATURES</p>'
                "<p>Each tool can be mounted facing front or reversed (turned 180°), whichever the bend needs.</p>"
                "<p>Tools load vertically in either direction and engage automatically when the clamps are open. There is "
                "no limit on the length, shape or number of tools loaded.</p>"
                "<p>One lever per module locks every tool in it: the tools are lifted against the reference surfaces and "
                "clamped there, so they are perfectly aligned. In the locked position the lever does not stick out.</p>"
                "<p>Unlocking: opening the lever releases all the tools in the module, and the safety system keeps them "
                "from falling out.</p>"
                "<p>Removal: lift each tool up to the stop, tilt it slightly and slide it out downward. It takes no more "
                "effort than the weight of the tool.</p>")

SECTION_TAIL = "With the matching upper and lower adapters, they also fit press brakes with other clamping systems."

PAGES = {
    # ---------------------------------------------------------------------------------------------- introduction
    3: [dict(clear=[R(55, 598, 540, 714)], box=R(61.8, 606, 290, 714),
             html=f'<p class="m" style="font-size:12px; color:{WARM}; line-height:1.2; margin-bottom:8px">'
                  "EUROSTAMP Tooling means quality, expertise and precision.</p>"
                  f'<p style="font-size:10px; color:{WARM}">Since 1970 we have been making press brake tooling of '
                  "outstanding accuracy for customers who demand the highest performance and reliability.</p>")],
    4: [dict(clear=[R(260, 70, 400, 460)], box=R(200, 76.9, 388.4, 140),
             html='<p class="r w" style="font-family:SB; font-size:30px; line-height:1.0">WHO<br>WE ARE</p>'),
        dict(clear=[R(30, 70, 258, 690)], art=[R(30, 350, 258, 360)], box=R(33.4, 75.5, 254.1, 690),
             html='<p class="w" style="font-size:10px; margin-bottom:8px">EUROSTAMP has been making press brake tooling '
                  "since 1970. We are proud to build punches, dies and bending equipment that are accurate, reliable and "
                  "made to the highest quality standards. Our modern machine shop and our large stock let us meet every "
                  "requirement, including special requests.</p>"
                  '<p class="w" style="font-size:10px; margin-bottom:8px">Our tools are made from C45 medium-carbon '
                  "steel, plain or tempered, and from Italian chrome-molybdenum steel. Every working surface is induction "
                  f"hardened to 55 – 60 HRC, up to 3 mm ({mm(3)}) deep.</p>"
                  '<p class="w" style="font-size:10px">We also offer a wide range of press brake accessories: upper and '
                  "lower adapters, and manual and pneumatic clamping systems. Our in-house engineering department designs "
                  "custom bending solutions quickly and accurately.</p>")],
    5: [dict(clear=[R(30, 36, 540, 100)], box=R(34.1, 41.2, 530, 100),
             html=f'<p style="font-family:SB; font-size:30px; color:{WARM}; line-height:1.0">OUR PHILOSOPHY</p>'),
        dict(clear=[R(30, 108, 280, 395)], box=R(34.0, 116.1, 271.7, 395),
             html=f'<p style="font-size:10px; color:{WARM}; margin-bottom:8px">EUROSTAMP Tooling is an Italian company with '
                  "an international outlook. From the start we chose to focus entirely on designing and making press brake "
                  "tooling, and we have invested in state-of-the-art technology for every step of our production.</p>"
                  f'<p style="font-size:10px; color:{WARM}">Our production team brings a craftsman’s care to detail, '
                  "precision and quality control. We work with the best Italian suppliers of raw materials and keep "
                  "investing in new equipment and in a large, well-organized warehouse, so finished tools are ready to "
                  "ship.</p>"),
        dict(clear=[R(284, 108, 540, 395)], box=R(289.1, 116.1, 526.8, 395),
             html=f'<p style="font-size:10px; color:{WARM}">We invest in training our production and engineering staff and '
                  "in research and development, because we believe the best way to serve our customers is to exceed their "
                  "expectations with innovative solutions and first-class support before and after the sale. Our sales "
                  "team works every day alongside production and engineering to bring this approach to customers around "
                  "the world.</p>"),
        dict(clear=[R(30, 615, 285, 797)], box=R(30, 622.3, 275.4, 700),
             html=f'<p class="r" style="font-family:SB; font-size:30px; color:{WARM}; line-height:1.0">OUR<br>EXPERTISE</p>'),
        dict(clear=[R(288, 608, 540, 797)], art=[R(288, 705, 540, 714)], box=R(292.6, 614.0, 526.9, 720),
             html=f'<p style="font-size:10px; color:{WARM}">Our specialists control every stage of production, from choosing '
                  "the alloys and raw steels to milling, hardening and grinding each part. We use 100% Italian steel for "
                  "the highest accuracy and mechanical properties.</p>")],
    # ---------------------------------------------------------------------------------------------- section openers
    14: [dict(clear=[R(75, 390, 375, 762)], box=R(60, 395.2, 368.7, 762),
              html='<p class="r w bo" style="font-size:10px; margin-bottom:9px">The upper and lower tools in this section fit '
                   "these press brakes:</p>"
                   '<p class="r w" style="font-size:10px; margin-bottom:9px">ACL, Accurpress, AM Machinery, Amada, Atlantic, '
                   "Adira, Baykal, BL, Boschert, Boutillon, Bystronic-Beyeler Euro-B, Coastone, Colgar, Dener, Deratech, "
                   "Durmazlar, Ermaksan, Farina, Gade, Gasparini, Gizelis, Haco, Hindustan, Iturrospe, Jfy, JMT, LFK, "
                   "Metfab, MVD, Oriance, Prima Power, Promecam, Rico, RPC, Salvagnini, Schiavi, SMD, Sorg, Somo, Vicla, "
                   "Vimercati, Warcom, Yangli, Yawei and Ysd — and every other press brake with European-style "
                   "(Amada-Promecam) clamping.</p>"
                   f'<p class="r w" style="font-size:10px">{SECTION_TAIL}</p>')],
    90: [dict(clear=[R(90, 395, 345, 665)], box=R(80, 400.0, 338.1, 665),
              html='<p class="r w bo" style="font-size:10px; margin-bottom:9px">The upper and lower tools in this section fit '
                   "these press brakes:</p>"
                   '<p class="r w" style="font-size:10px; margin-bottom:9px">Trumpf, LVD, Darley, Safan and other press '
                   "brakes with New Standard (NSCL) clamping.</p>"
                   f'<p class="r w" style="font-size:10px">{SECTION_TAIL}</p>')],
    146: [dict(clear=[R(80, 395, 322, 665)], box=R(70, 401.4, 316.2, 665),
               html='<p class="r w bo" style="font-size:10px; margin-bottom:9px">The upper and lower tools in this section '
                    "fit these press brakes:</p>"
                    '<p class="r w" style="font-size:10px; margin-bottom:9px">Trumpf, LVD, Darley, RPC, Safan and other '
                    "press brakes with New Standard (NSCL) clamping.</p>"
                    f'<p class="r w" style="font-size:10px">{SECTION_TAIL}</p>')],
    170: [dict(clear=[R(90, 382, 362, 670)], box=R(80, 387.5, 357.5, 670),
               html='<p class="r w bo" style="font-size:10px; margin-bottom:9px">The upper and lower tools in this section '
                    "fit Bystronic / Beyeler press brakes with these clamping types:</p>"
                    '<p class="r w" style="font-size:10px">Bystronic / Beyeler type RFA</p>'
                    '<p class="r w" style="font-size:10px">Bystronic / Beyeler type RF</p>'
                    '<p class="r w" style="font-size:10px; margin-bottom:9px">Bystronic / Beyeler type R</p>'
                    f'<p class="r w" style="font-size:10px">{SECTION_TAIL}</p>')],
    190: [dict(clear=[R(30, 290, 345, 390)], box=R(37.1, 296.0, 560, 340),
               html='<p class="w" style="font-family:SX; font-size:44px; line-height:1.0">ACCESSORIES</p>')],
    # ---------------------------------------------------------------------------------------------- ESH series
    79: [dict(clear=[R(60, 28, 290, 64)], box=R(30, 32.2, 271.8, 64),
              html='<p class="r w" style="font-family:SR; font-size:13px; line-height:1.12">ESH SERIES TOOLS</p>'
                   '<p class="r w" style="font-family:SL; font-size:13px; line-height:1.12">(EUROSTAMP Same Height)</p>'),
         dict(clear=[R(30, 143, 515, 220)], box=R(34.2, 147.0, 505, 220),
              html=f'<p class="g" style="font-family:RR; font-size:9px; line-height:1.33">EUROSTAMP HAS ADDED A COMPLETE NEW '
                   "SERIES OF UPPER AND LOWER TOOLS FOR EUROPEAN-STYLE (AMADA-PROMECAM) CLAMPING.</p>"),
         dict(clear=[R(30, 252, 535, 376)], box=R(34.2, 256.3, 528, 376),
              html='<p class="h" style="margin-bottom:8px">COMMON FEATURES</p>'),
         dict(clear=[], box=R(34.3, 277.2, 257.1, 376),
              html=f'<p class="g">Every tool in the series is made from premium CrMo steel. Its high tensile strength, '
                   "950 – 1,050 N/mm² (138 – 152 ksi), lets the same tool section carry higher tonnage.</p>"),
         dict(clear=[], box=R(305.0, 277.2, 528, 376),
              html='<p class="g">Punches and dies are hardened differently, each for the best performance in the way it '
                   "works.</p>")],
    80: [dict(clear=[R(52, 45, 545, 340)], art=[R(52, 196, 545, 210)], box=R(58.0, 50.5, 545, 70),
              html='<p class="h">UPPER TOOL INNOVATIONS</p>'),
         dict(clear=[], box=R(57.8, 84.6, 287.4, 340),
              html=f'<p class="g l">• Punch tips are induction hardened to 55 – 58 HRC, to an average depth of more than '
                   f"3 mm ({mm(3)}): a very hard tip radius and working surface that last longer.</p>"
                   '<p class="g l">• Angles of 86°, 60°, 30° and 26°.</p>'
                   '<p class="g l">• Punch profiles redesigned for maximum flexibility, so more part profiles can be '
                   "formed.</p>"),
         dict(clear=[], box=R(311.1, 84.6, 540.6, 340),
              html=f'<p class="g l">• A working height of 120 mm ({mm(120)}) suits the daylight and stroke of most press '
                   "brakes on the market.</p>"
                   '<p class="g l">• Every punch in the range has the same working height, so any punches can be set up '
                   "in stages (bending stations) to form complex parts with 90° bends.</p>"),
         dict(clear=[R(52, 556, 545, 785)], box=R(59.0, 560.6, 545, 590),
              html='<p class="h">LOWER TOOL INNOVATIONS — INSERT DIES</p>'),
         dict(clear=[], box=R(57.8, 599.3, 290.2, 790),
              html='<p class="g">The die inserts are gas nitrided: the whole surface, not only the shoulders, gets a thin '
                   "nitride layer up to 65 HRC. The harder surface protects the V shoulders against wear from the sheet, "
                   "reduces wear on the sides of the V and keeps zinc and other particles from sticking to them, which "
                   "prevents galling.</p>"),
         dict(clear=[], box=R(311.1, 599.3, 540.6, 790),
              html='<p class="g">The dies are then phosphate coated, which gives them their black color and protects them '
                   "against corrosion.</p>"
                   f'<p class="g">Die inserts come in 86° and 30°, with V openings from 6 to 25 mm ({mm(6)} – {mm(25)}).</p>')],
    81: [dict(clear=[R(30, 58, 545, 210)], box=R(34.0, 62.8, 269.5, 210),
              html='<p class="g">The die insert profiles have been redesigned for today’s work:</p>'
                   '<p class="g l">• Large shoulder radii, to reduce marking of the sheet.</p>'
                   '<p class="g l">• Narrow-V die inserts have a slimmer body for more complex parts, such as short offset '
                   "bends (often needed on thin sheet).</p>"),
         dict(clear=[], box=R(304.6, 62.8, 540.1, 210),
              html='<p class="g l">• Chamfered outside corners reduce the risk of hitting burrs or distortions close to the '
                   "bend line.</p>"),
         dict(clear=[R(300, 214, 545, 398)], box=R(304.8, 219.2, 540.1, 398),
              html='<p class="h">OPTIONAL TREATMENT (EXTRA CHARGE)</p>'
                   '<p class="g">On request, punches can also be phosphate coated: a crystalline phosphate layer that '
                   "protects the surface against corrosion and helps lubrication. The cost depends on the total weight.</p>"),
         dict(clear=[R(160, 413, 412, 443)], box=R(150, 417.3, 425, 443),
              html='<p class="h c">NEW STANDARD SECTIONING</p>'),
         dict(clear=[R(280, 571, 540, 632)], box=R(283.7, 575.6, 540, 633),
              html=f'<p class="bo g" style="font-size:8.8px; margin-bottom:4px">UPPER TOOLS (TOTAL LENGTH 800 MM / {mm(800, 2)}):</p>'
                   '<p class="g" style="margin-bottom:1px">100 mm LH horn – 10 – 15 – 15 – 20 – 40 – 50 – 150 – 300 mm – '
                   "100 mm RH horn</p>"
                   '<p class="g" style="font-size:8.5px">(3.94″ LH horn – .394 – .591 – .591 – .787 – 1.57 – 1.97 – 5.91 – '
                   "11.81″ – 3.94″ RH horn)</p>"),
         dict(clear=[R(280, 718, 540, 778)], box=R(283.8, 722.2, 540, 780),
              html=f'<p class="bo g" style="font-size:8.8px; margin-bottom:4px">LOWER TOOLS (TOTAL LENGTH 800 MM / {mm(800, 2)}):</p>'
                   '<p class="g" style="margin-bottom:1px">100 – 10 – 15 – 15 – 20 – 40 – 50 – 150 – 400 mm</p>'
                   '<p class="g" style="font-size:8.5px">(3.94 – .394 – .591 – .591 – .787 – 1.57 – 1.97 – 5.91 – '
                   "15.75″)</p>")],
    # ---------------------------------------------------------------------------------------------- EUROGRIP
    213: [dict(clear=[R(30, 66, 352, 113)], box=R(34.0, 70.3, 348, 113),
               html='<p class="t">COMPLETE CLAMPING SYSTEM FOR EUROPEAN-STYLE (AMADA-PROMECAM) UPPER TOOLS</p>'),
          dict(clear=[R(30, 140, 295, 628)], box="auto",
               html='<p class="h">CHANGING TOOLS WITH A STANDARD CLAMPING SYSTEM</p>'
                    "<p>On a standard system the upper tools are held by safety clamps screwed to the intermediates, which "
                    "are fixed to the upper beam.</p>"
                    "<p>The tang of the intermediate clamp engages the safety groove machined in the punch, so the tool "
                    "cannot fall out when the clamp is opened. It also means every tool has to be inserted and removed from "
                    "the side of the machine and slid along to its working position: it cannot be put in or taken out "
                    "vertically.</p>"
                    "<p>Once the new punches are in place:</p>"
                    '<p class="l">• tighten all the clamp screws slightly,</p>'
                    '<p class="l">• lower the upper beam so it pushes the tools up against their reference surface (the '
                    "underside of the intermediate) and aligns them,</p>"
                    '<p class="l">• tighten all the clamp screws firmly.</p>'
                    "<p>The time this takes is time the machine is not bending, and it can make a real difference to "
                    "productivity.</p>")],
    214: [dict(clear=[R(30, 110, 265, 375)], box="auto",
               html='<p class="bl">The mechanical design of the EUROGRIP clamp makes it possible to:</p>'
                    '<p class="l">• insert and remove punches vertically, instead of sliding them in from the side, with '
                    "the same high level of safety;</p>"
                    '<p class="l">• lift the punch as the clamp closes, so it is aligned when it is locked.</p>'),
          dict(clear=[R(30, 480, 265, 752)], box="auto",
               html='<p class="bl">The table shows the average time for each step of removing and replacing the upper '
                    "tools on a 3 m (10 ft) press brake with 15 intermediates, to compare the EUROGRIP systems with the "
                    "standard one.</p>"
                    "<p>Estimated time for each step of an upper tool change (3 m / 10 ft press brake with 15 "
                    "intermediates).</p>"),
          dict(clear=[R(296, 422, 450, 466)], box=R(299.9, 425.6, 450, 466),
               html='<p style="font-family:RR; font-size:9px; line-height:1.1">AVERAGE TIME WITH THE STANDARD SYSTEM</p>'),
          dict(clear=[R(430, 457, 530, 478)], box=R(380, 460.0, 524.6, 478),
               html=f'<p class="r bo" style="font-size:8px; color:{BLUE}">about 9.5 minutes</p>'),
          dict(clear=[R(296, 490, 450, 534)], box=R(299.9, 493.4, 450, 534),
               html='<p style="font-family:RR; font-size:9px; line-height:1.1">AVERAGE TIME WITH THE EUROGRIP MANUAL '
                    "SYSTEM</p>"),
          dict(clear=[R(430, 527, 530, 548)], box=R(380, 529.8, 524.6, 548),
               html=f'<p class="r bo" style="font-size:8px; color:{BLUE}">about 3.0 minutes (–70%)</p>'),
          dict(clear=[R(296, 560, 450, 604)], box=R(299.9, 563.5, 450, 604),
               html='<p style="font-family:RR; font-size:9px; line-height:1.1">AVERAGE TIME WITH THE EUROGRIP PNEUMATIC '
                    "SYSTEM</p>"),
          dict(clear=[R(430, 596, 530, 618)], box=R(380, 599.3, 524.6, 618),
               html=f'<p class="r bo" style="font-size:8px; color:{BLUE}">about 1.5 minutes (–85%)</p>'),
          dict(clear=[R(296, 636, 530, 790)], art=[R(330, 715, 345, 790)], box=R(299.9, 640.8, 510, 680),
               html='<p style="font-family:RR; font-size:8.8px; line-height:1.15">ONE TOOL CHANGE TAKES THIS SHARE OF AN '
                    "HOUR OF PRODUCTION TIME:</p>"),
          dict(clear=[], box=R(339.9, 686.1, 520, 720),
               html='<p class="bo" style="font-size:8px; line-height:1.2; margin:0">16% with the standard system</p>'
                    '<p class="bo" style="font-size:8px; line-height:1.2; margin:0">5% with EUROGRIP manual</p>'
                    '<p class="bo" style="font-size:8px; line-height:1.2; margin:0">2.5% with EUROGRIP pneumatic</p>')],
    216: [dict(clear=[R(30, 340, 270, 452)], box="auto",
               html="<p>With the clamp open, the punch is pushed straight up until its safety groove meets the clamp’s "
                    "safety fingers, which hook it and hold it up.</p>"),
          dict(clear=[R(295, 340, 530, 452)], box="auto",
               html="<p>As the clamp closes, the safety fingers lift the punch to the reference surface (the underside of "
                    "the intermediate) and hold it there until the clamp is fully closed and the punch is locked.</p>"),
          dict(clear=[R(30, 697, 270, 780)], box="auto",
               html="<p>When the clamp is opened, the punch is released and drops until it is caught by the safety "
                    "fingers.</p>"),
          dict(clear=[R(295, 697, 530, 780)], box="auto",
               html="<p>To remove it, lift the punch by hand and push its tip toward the back of the machine to free it "
                    "from the safety fingers, then slide it out downward.</p>")],
    217: [dict(clear=[R(30, 62, 460, 90)], box=R(34.8, 65.9, 460, 92),
               html='<p class="t">THE EUROGRIP RANGE FOR UPPER TOOL CLAMPING</p>'),
          dict(clear=[R(30, 116, 248, 478)], box="auto",
               html="<p>The EUROGRIP clamp is the basis of a complete range of solutions developed by EUROSTAMP to suit "
                    "standard press brake equipment and each customer’s needs.</p>"
                    '<p style="margin-left:38px">The range includes manual and pneumatic systems.</p>'
                    '<p style="margin-left:38px">Each system comes in two versions, EASY and TOP.</p>'
                    '<p style="margin-left:38px">Each version comes in two models, to suit the size of the original '
                    "intermediates.</p>"),
          dict(clear=[R(58, 505, 210, 552)], box=R(61.1, 508.4, 210, 552),
               html='<p style="font-family:RR; font-size:8.8px; line-height:1.15">TYPICAL DIMENSIONS OF A Z1 '
                    "INTERMEDIATE</p>"),
          dict(clear=[R(58, 557, 210, 605)], box=R(61.1, 560.8, 210, 605),
               html='<p style="font-family:RR; font-size:8.8px; line-height:1.15">TYPICAL DIMENSIONS OF A Z2 '
                    "INTERMEDIATE</p>")],
    218: [dict(clear=[R(30, 78, 300, 104)], box=R(34.1, 81.7, 300, 106),
               html='<p class="t">MANUAL CLAMPING SYSTEMS – INTRODUCTION</p>'),
          dict(clear=[R(30, 145, 280, 300)], art=[R(30, 288, 530, 302)], box="auto",
               html="<p>Each clamp has its own sturdy, easy-to-use handle. It folds away at the top of the clamp, so it "
                    "never interferes with the part being bent.</p>"),
          dict(clear=[R(284, 145, 530, 285)], box="auto",
               html="<p>The same principle is used in an upper adapter that takes Trumpf / Wila-style punches on machines "
                    "with European-style (Amada-Promecam) clamping.</p>")],
    219: eurogrip_model(R(150, 69, 420, 126), R(328, 199, 530, 468),
                        "EUROGRIP MANUAL SYSTEM M-EASY: FRONT CLAMP TO RETROFIT A Z1 INTERMEDIATE",
                        desc("A front clamp that replaces the existing one on your intermediate.")
                        + spec(f"For Z1 intermediates only ({Z1}). {CHECK}")),
    220: eurogrip_model(R(140, 69, 505, 126), R(305, 194, 530, 462),
                        "EUROGRIP MANUAL SYSTEM M-EASY: CLAMP AND FRONT PLATE TO RETROFIT A Z2 INTERMEDIATE",
                        desc("An assembly of the 4389 clamp and a new front plate, mounted on the main body of your existing "
                             "intermediate.")
                        + spec(f"For Z2 intermediates only (minimum {Z2}). {CHECK}")),
    221: eurogrip_model(R(182, 70, 485, 127), R(331, 193, 530, 752),
                        "EUROGRIP MANUAL SYSTEM M-TOP: FRONT CLAMP MOUNTED ON A DEDICATED Z1 INTERMEDIATE",
                        desc("A complete intermediate: a special, larger manual clamp mounted on a high-quality Z1 "
                             "intermediate body designed for it.",
                             "The best choice when you are replacing worn or damaged intermediates, or when your "
                             "intermediates are not suited to the M-EASY.",
                             "The 4390 comes ready for the optional manual rear clamp 4404 (through holes already "
                             "drilled).")
                        + spec(f"For machines built for Z1 intermediates ({Z1}). {CHECK}")),
    222: eurogrip_model(R(150, 63, 470, 120), R(331, 190, 530, 765),
                        "EUROGRIP MANUAL SYSTEM M-TOP: FRONT CLAMP MOUNTED ON A DEDICATED Z2 INTERMEDIATE",
                        desc("A complete intermediate: a special, larger manual clamp mounted on a high-quality Z2 "
                             "intermediate body designed for it.",
                             "The best choice when you are replacing worn or damaged intermediates, or when your "
                             "intermediates are not suited to the M-EASY.",
                             "The 4400 comes ready for the optional manual rear clamp 4404 (through holes already "
                             "drilled).")
                        + spec(f"For machines built for Z2 intermediates ({Z2}). {CHECK}", "Weight: 5.5 kg (12.1 lb)")),
    223: eurogrip_model(R(150, 63, 462, 120), R(343, 190, 530, 776),
                        "EUROGRIP MANUAL SYSTEM M-TOP Z1 DUO: FRONT AND REAR CLAMPS MOUNTED ON A DEDICATED Z1 INTERMEDIATE",
                        TOP_FEATURES),
    224: eurogrip_model(R(150, 63, 462, 120), R(343, 190, 530, 776),
                        "EUROGRIP MANUAL SYSTEM M-TOP Z2 DUO: FRONT AND REAR CLAMPS MOUNTED ON A DEDICATED Z2 INTERMEDIATE",
                        TOP_FEATURES),
    225: eurogrip_model(R(146, 63, 510, 120), R(331, 190, 530, 670),
                        "EUROGRIP MANUAL SYSTEM M-WDP: UPPER ADAPTER FROM AMADA STYLE (Z1) TO WILA / TRUMPF STYLE",
                        desc("An upper adapter from the standard Amada-Promecam (European) style to the standard Trumpf / "
                             "Wila style.",
                             "Its front clamp, worked by a fold-away handle, loads, removes, aligns and locks Trumpf / "
                             "Wila-style punches on press brakes with a European-style (Amada-Promecam) upper beam.")
                        + spec(f"For machines built for Z1 intermediates ({Z1}). {CHECK}", "Weight: 6.7 kg (14.8 lb)")),
    226: [dict(clear=[R(30, 62, 340, 89)], box=R(34.1, 65.4, 340, 92),
               html='<p class="t">MANUAL CLAMPING SYSTEMS – OPTIONAL ADD-ONS</p>'),
          dict(clear=[R(355, 108, 545, 412)], art=[R(355, 428, 530, 442)], box="auto",
               html='<p class="h">OPTIONAL REAR CLAMP, M-EASY MODELS ONLY</p>'
                    "<p>For mounting punches reversed on intermediates fitted with M-EASY clamps (4389 and 4409).</p>"
                    "<p>The rear clamp is operated from the front of the machine with two Allen screws.</p>"
                    f"<p>To fit it, two Ø9 mm ({mm(9)}) through holes must be drilled in the intermediate body.</p>"),
          dict(clear=[R(355, 463, 545, 776)], box="auto",
               html='<p class="h">OPTIONAL REAR CLAMP, M-TOP, P-EASY AND P-TOP MODELS</p>'
                    "<p>For mounting punches reversed on intermediates fitted with M-TOP, P-EASY or P-TOP systems.</p>"
                    "<p>The rear clamp is operated from the front of the machine with two Allen screws.</p>"
                    "<p>All M-TOP, P-EASY and P-TOP models come with the through holes already drilled, so no machining is "
                    "needed to fit the clamp.</p>")],
    227: [dict(clear=[R(30, 62, 305, 89)], box=R(34.8, 65.4, 305, 92),
               html='<p class="t">PNEUMATIC CLAMPING SYSTEMS – INTRODUCTION</p>'),
          dict(clear=[R(30, 110, 280, 185)], box="auto",
               html="<p>Every clamp on the upper beam is operated by compressed air, controlled by a pneumatic control unit "
                    "and carried through hoses that connect the intermediates in series.</p>"),
          dict(clear=[R(284, 110, 530, 185)], box="auto",
               html="<p>The pneumatic range also includes a system for clamping the lower tools.</p>"),
          dict(clear=[R(30, 637, 280, 750)], box="auto",
               html="<p>The EUROGRIP upper pneumatic systems replace some of the standard parts supplied with the press "
                    "brake. Depending on the model, only the intermediates are replaced (P-EASY), or the top beam clamps "
                    "as well (P-TOP).</p>"),
          dict(clear=[R(284, 637, 530, 750)], box="auto",
               html="<p>Every pneumatic system needs a pneumatic control unit and a connection kit (hoses, fittings, cables "
                    "and switch).</p>")],
    228: eurogrip_model(R(160, 69, 485, 126), R(331, 180, 530, 795),
                        "EUROGRIP PNEUMATIC SYSTEM P-EASY: PNEUMATIC CLAMP MOUNTED ON A DEDICATED Z1 INTERMEDIATE",
                        desc("A complete intermediate: a special pneumatic clamp mounted on a high-quality Z1 intermediate "
                             "body machined for the clamp’s moving fingers (see 2 and 3 on page 219).",
                             "Each new intermediate replaces an existing one and uses the top beam clamp already on the "
                             "machine. It is connected to the others in series with a plastic hose, so it can still be "
                             "shifted left or right and removed.",
                             "The 4392 comes ready for the optional manual rear clamp 4404 (through holes already "
                             "drilled).")
                        + spec(f"For machines built for Z1 intermediates ({Z1}). {CHECK}", "Weight: 5.2 kg (11.5 lb)")),
    229: eurogrip_model(R(148, 68, 472, 126), R(331, 186, 530, 790),
                        "EUROGRIP PNEUMATIC SYSTEM P-EASY: PNEUMATIC CLAMP MOUNTED ON A DEDICATED Z2 INTERMEDIATE",
                        desc("A complete intermediate: a special pneumatic clamp mounted on a high-quality Z2 intermediate "
                             "body machined for the clamp’s moving fingers (see 2 and 3 on page 219).",
                             "Each new intermediate replaces an existing one and uses the top beam clamp already on the "
                             "machine. It is connected to the others in series with a dedicated steel tube, so it can still "
                             "be shifted left or right and removed.",
                             "The 4405 comes ready for the optional manual rear clamp 4404 (through holes already "
                             "drilled).")
                        + spec(f"For machines built for Z2 intermediates ({Z2}). {CHECK}", "Weight: 5.9 kg (13.0 lb)")),
    230: eurogrip_model(R(173, 65, 530, 132), R(331, 195, 530, 545),
                        "EUROGRIP PNEUMATIC SYSTEM P-TOP: PNEUMATIC TOP BEAM CLAMP – REQUIRED FOR EVERY P-TOP MODEL",
                        desc("It replaces the standard clamps on the machine’s upper beam (see 1 on page 219).",
                             "The top beam clamps are connected in series with steel tubing. Each one feeds air to its "
                             "intermediate through an internal valve, so the intermediate can be shifted left or right, or "
                             "removed, without any bypass.",
                             "The recommended solution when intermediates are shifted or removed many times a day.")),
    231: eurogrip_model(R(151, 65, 530, 142), R(331, 195, 530, 788),
                        "EUROGRIP PNEUMATIC SYSTEM P-TOP: PNEUMATIC CLAMP MOUNTED ON A DEDICATED Z1 INTERMEDIATE – "
                        "REQUIRES THE 4399 TOP BEAM CLAMP",
                        desc("A complete intermediate: a special pneumatic clamp mounted on a high-quality Z1 intermediate "
                             "body machined for the clamp’s moving fingers (see 2 and 3 on page 219).",
                             "Each new intermediate replaces an existing one and works with the 4399 top beam clamp, which "
                             "supplies the air.",
                             "The intermediate 4391 comes ready for the optional manual rear clamp 4404 (through holes "
                             "already drilled).")
                        + spec(f"For machines built for Z1 intermediates ({Z1}). {CHECK}", "Weight: 6.2 kg (13.7 lb)",
                               "Code 4398 is the intermediate and top beam clamp together (4391 + 4399).")),
    232: eurogrip_model(R(130, 68, 530, 147), R(330, 195, 530, 795),
                        "EUROGRIP PNEUMATIC SYSTEM P-TOP: PNEUMATIC CLAMP MOUNTED ON A DEDICATED Z2 INTERMEDIATE – "
                        "REQUIRES THE 4399 TOP BEAM CLAMP",
                        desc("A complete intermediate: a special pneumatic clamp mounted on a high-quality Z2 intermediate "
                             "body machined for the clamp’s moving fingers (see 2 and 3 on page 219).",
                             "Each new intermediate replaces an existing one and works with the 4399 top beam clamp, which "
                             "supplies the air.",
                             "The intermediate 4410 comes ready for the optional manual rear clamp 4404 (through holes "
                             "already drilled).")
                        + spec(f"For machines built for Z2 intermediates ({Z2}). {CHECK}", "Weight: 6.2 kg (13.7 lb)",
                               "Code 4412 is the intermediate and top beam clamp together (4410 + 4399).")),
    233: eurogrip_model(R(171, 68, 530, 125), R(331, 396, 530, 790),
                        "EUROGRIP LOWER PNEUMATIC SYSTEM P-DHOLD: PNEUMATIC DIE HOLDER FOR AMADA-STYLE DIES",
                        desc("A modular European-style (Amada-Promecam) lower die holder with a row of pneumatic clamps on "
                             "its front. Each module connects to the next with a fold-away connector.",
                             "Recommended when the lower tools are changed often: the whole lower tool set is clamped or "
                             "released at once.")
                        + spec("Fits any machine with a flat lower table to the European (Amada-Promecam) standard. "
                               f"Modules 835, 415 and 625 mm long ({mm(835, 2)}, {mm(415, 2)} and {mm(625, 2)}).")),
    234: [dict(clear=[R(30, 94, 535, 163)], box=R(34.0, 98.8, 526.6, 163),
               html="<p>Every EUROGRIP pneumatic system needs a pneumatic control unit, which holds the electrical and "
                    "pneumatic components that drive the system, and a connection kit for the model ordered, with the "
                    "hoses, cables and fittings needed to install it.</p>"),
          dict(clear=[R(268, 224, 535, 356)], art=[R(268, 205, 530, 219)], box=R(271.8, 227.8, 526.6, 356),
               html='<p class="h">DESCRIPTION</p>'
                    f"<p>Connects to the shop’s compressed-air supply (minimum inlet pressure 6 bar / 87 psi).</p>"
                    "<p>One outlet supplies one clamping system, upper or lower.</p>"
                    "<p>Holds all the electrical connections and the safety system.</p>"),
          dict(clear=[R(30, 459, 295, 590)], art=[R(30, 600, 300, 615)], box=R(34.2, 463.2, 295, 590),
               html='<p class="h">DESCRIPTION</p>'
                    "<p>Connects to the shop’s compressed-air supply (minimum inlet pressure 6 bar / 87 psi). Two outlets "
                    "supply both clamping systems, upper and lower.</p>"
                    "<p>Holds all the electrical connections and the safety system.</p>"),
          dict(clear=[R(30, 740, 290, 792)], art=[R(30, 722, 268, 737)], box=R(34.2, 744.0, 290, 795),
               html='<p class="h">DESCRIPTION</p>'
                    "<p>The hardware needed to install and connect the P-EASY system.</p>"),
          dict(clear=[R(291, 740, 535, 792)], art=[R(290, 721, 528, 736)], box=R(294.6, 744.0, 530, 795),
               html='<p class="h">DESCRIPTION</p>'
                    "<p>The hardware needed to install and connect the P-TOP system.</p>")],
}


# ------------------------------------------------------------------------------------------------------------- run
def _is_bar(d, rect):
    f = d.get("fill")
    r = d["rect"]
    if not f or not rect.contains(r):
        return False
    grey = abs(f[0] - f[1]) < 0.06 and abs(f[1] - f[2]) < 0.06
    return r.height <= 8.5 and r.width >= 30 and (grey or min(f[:3]) > 0.9)


def handler(page, ppage, ctx):
    pno = page.number + 1
    ops = PAGES.get(pno)
    if not ops:
        return
    lines = page_lines(page, ppage)
    ed = Editor(page, lines)
    flows = ctx.setdefault("flows", [])
    art = []
    for op in ops:
        rects = op.get("clear", [])
        hit = []
        for L in lines:
            c = fitz.Point((L.bbox.x0 + L.bbox.x1) / 2, (L.bbox.y0 + L.bbox.y1) / 2)
            if any(r.contains(c) for r in rects) and not L.removed:
                hit.append(L)
                ed.drop_line(L)
        box = op.get("box", "auto")
        if isinstance(box, str):
            if hit:
                x0 = min(L.bbox.x0 for L in hit)
                y0 = min(L.bbox.y0 for L in hit)
            else:
                x0, y0 = rects[0].x0, rects[0].y0
            box = fitz.Rect(x0, y0, 527.0 if box == "auto-wide" else rects[0].x1, rects[0].y1)
        flows.append((fitz.Rect(box), op["html"]))
        used = measure(box, op["html"])
        ctx.setdefault("reserve", []).append(fitz.Rect(box.x0, box.y0, box.x1, box.y0 + used + 1.5))
        for r in rects + op.get("art", []):
            for d in page.get_drawings():
                if _is_bar(d, r):
                    art.append(d["rect"])
        for r in op.get("art", []):
            art.append(r)
    ed.apply()
    if art:
        for r in art:
            page.add_redact_annot(fitz.Rect(r.x0 - 0.6, r.y0 - 0.6, r.x1 + 0.6, r.y1 + 0.6), fill=False)
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=fitz.PDF_REDACT_TEXT_NONE)


def measure(box, html):
    """the height the text takes in `box` (set on a scratch page)"""
    doc = fitz.open()
    p = doc.new_page(width=max(box.x1 + 10, 600), height=max(box.y1 + 10, 850))
    spare, scale = p.insert_htmlbox(box, html, css=CSS, archive=ARCHIVE, scale_low=0.8)
    return box.height - max(0.0, spare) if spare >= 0 else box.height


def post(page, ctx, report=None):
    for box, html in ctx.get("flows", []):
        spare, scale = page.insert_htmlbox(box, html, css=CSS, archive=ARCHIVE, scale_low=0.8)
        if (spare < 0 or scale < 0.999) and report is not None:
            report.append((page.number + 1, "flow-fit", f"{box} scale {scale:.2f}"))
