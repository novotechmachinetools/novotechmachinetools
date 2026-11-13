#!/usr/bin/env python3
"""Plastmak (Bursa, Turkey) aluminum and PVC window and door machinery — the saws page (the old site's URL, menu "Aluminum & PVC
saws") and the new "Aluminum & PVC processing machines" hub with four pages; image registration (section 'plastmak').

    Aluminum & PVC saws               aluminum-and-pvc-upcut-saws               SC 401 · 402 · 403 · 450 · 400S · 4000S · 301 · 301S · 431 · 441 · 451
    Aluminum & PVC processing machines pvc-aluminum-window-machines (hub)
        ├ pvc-window-welding-machines             SC 100 Gold Plus · Gold Plus Full · SC 100 · SC 101 · SC 6000 · 6000S · SC 601
        ├ profile-machining-centres-copy-routers  SC 4550 · 5000 · 5000S · 501 · 502S · 512 · 521S · 542 · 211 · 211S
        ├ window-assembly-machines                SC 902 · screwing and sash assembly · SC 221 · 551 · SC 1000 – 1003
        └ window-production-lines                 PVC single-head · PVC double-head · aluminum double-head · PVC workshop

    python3 tools/plastmak_photos.py                 # catalogue, plastmak.com and 2024-catalogue images → tools/src-images/plastmak
    python3 tools/plastmak_pages.py                  # families, pages, image_map entries (tools/plastmak_keys.txt)
    python3 tools/make_images.py --only $(cat tools/plastmak_keys.txt)

The brochure on the pages, src/files/NovoTech-Plastmak-Window-Machinery-2026.pdf, is built from these families since Nov 12 2026
(the owner: the first catalogue was disorganised, its photos broken and its contents wrong — "build a new one from scratch"):

    python3 tools/brochure/build_brochure.py tools/brochure/specs/plastmak.json
"""
import json
import os
import shutil

from isitan_lib import VOLT_FAQ_GENERIC, write_category, write_families, write_hub
import plastmak_data as D
import plastmak_photos as PH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = "plastmak"
SECTION = "Aluminum & PVC processing machines"
PDF_SRC = "/mnt/user-data/attachments/c238f6cc-e8bd-5b1f-a645-cb18914b0540/9e251d13-NovoTech_Plastmak_Window_Machinery_2026.pdf"
PDF_FILE = "files/NovoTech-Plastmak-Window-Machinery-2026.pdf"
PDF_LABEL = "Download the Plastmak window machinery brochure"


def pdf():
    f = os.path.join(ROOT, "src", PDF_FILE)
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": PDF_FILE, "label": PDF_LABEL, "size": size}


def families(page=None):
    return [dict(f, pdf=pdf()) for f in D.FAMILIES if page is None or f["page"] == page]


ALL = families(D.P_SAWS) + families(D.P_WELD) + families(D.P_CNC) + families(D.P_ASSY) + families(D.P_LINES)

BRAND_LINE = ("Plastmak machines are built in Bursa, Turkey, by Plastmak — PVC and aluminum window and door machinery from a family "
              "business founded in 1968, exported to more than 60 countries. Sold, installed and supported in Canada by NovoTech.")
ORIGIN = {"title": "Made in Turkey by Plastmak", "text": "Plastmak builds PVC and aluminum window and door machinery in Bursa — roots in "
          "Anadolu Makina, founded in 1968, Plastmak since 2007, about 80 % of production exported to more than 60 countries."}
SHARED = {"hero_brand_line": BRAND_LINE, "origin_feature": ORIGIN, "intro_video": None, "catalogue_pdf": pdf(), "catalogue_pdfs": None}
RELATED_TITLE = "More aluminum, PVC and metal machinery from NovoTech"
P = D.PLASTMAK

# ------------------------------------------------------------------------------------------------ saws
PAGE_SAWS = dict(
    title="Automatic Upcut Saws for Aluminum Extrusion & PVC | NovoTech",
    meta="Rising-blade saws for aluminum extrusions and vinyl window profiles, Ø17-11/16″ to Ø25-9/16″ blades, with double-head, glazing bead and miter saws.",
    h1="Aluminum & PVC upcut saws — automatic upcut, double-head, glazing bead and miter saws for extrusions and window profiles",
    intro="An upcut saw (rising-blade saw) raises its blade from under the table through a profile that is already clamped, so the "
          "cut is guarded, square and nearly burr-free — the standard saw for aluminum extrusions and PVC (vinyl) window profiles. "
          "NovoTech supplies the saws of Plastmak, built in Bursa, Turkey: the SC 401, whose Ø17-11/16″ blade turns from 0° to "
          "180°; the fully automatic SC 402 and SC 403 with Ø21-5/8″ to Ø25-9/16″ blades and hydro-pneumatic feed, for profiles "
          "up to 9-3/16 × 12-3/8″; the SC 450 for roller-shutter boxes and lamella packs; the SC 400S and SC 4000S double-head "
          "saws, which cut both ends of a frame profile at once, up to 171-5/8″ long; the SC 301 and SC 301S glazing bead saws; "
          "and the SC 431, SC 441 and SC 451 miter saws. Supplied with a CSA-approved panel, installed and supported from "
          "Mississauga, ON, Canada.",
    points=["Upcut saws Ø17-11/16″ – Ø25-9/16″ (450 – 650 mm), automatic from the SC 402, profiles to 9-3/16 × 12-3/8″",
            "Double-head saws: 2 × Ø19-11/16″ or 2 × Ø23-5/8″, lengths 19-1/8″ – 171-5/8″, ±.020″ on the SC 4000S",
            "Glazing bead, shutter box and miter saws — the whole cutting side of a window shop"],
    hero="pm-402", minis=["pm-401", "pm-4000s"],
    groups=[("pm-upcut", "Upcut saws",
             "Rising-blade saws for aluminum and PVC profiles, from the 0° – 180° SC 401 to the fully automatic SC 402 and SC 403, "
             "and the SC 450 for roller-shutter work.", P),
            ("pm-double", "Double-head miter saws", "Both ends of a profile in one stroke, square or mitred, to the length set on the control.", P),
            ("pm-bead", "Glazing bead saws", "45° bead cutting, with a universal mould or with no moulds at all.", P),
            ("pm-miter", "Overhead and bench miter saws", "Top-down miter saws for the shop and the site.", P)],
    faq=[{"q": "What is an upcut saw?",
          "a": "A saw whose blade sits under the table and rises through the profile, which is clamped from above and from the side "
               "before the cut. The blade stays covered until it cuts, the profile cannot move, and the cut comes out square and "
               "nearly burr-free — which is why aluminum and PVC window shops use upcut saws rather than chop saws. The SC 401, "
               "SC 402 and SC 403 are upcut saws; the SC 431, 441 and 451 cut from above."},
         {"q": "Which blade size do I need?",
          "a": "The blade decides the largest profile. At 90° the Ø17-11/16″ (450 mm) SC 401 cuts profiles up to 5-5/16″ high and "
               "8-9/16″ wide, the Ø21-5/8″ (550 mm) SC 402 7-1/16 × 10-7/16″, and the SC 403 8-3/16 × 11-5/16″ with its "
               "Ø23-5/8″ (600 mm) blade or 9-3/16 × 12-3/8″ with the Ø25-9/16″ (650 mm) one. Most window and door profiles fit "
               "the SC 401 or 402; curtain-wall and large door profiles need the SC 403. Send us your largest profile and we will "
               "check it against the cutting chart."},
         {"q": "Upcut saw or double-head saw?",
          "a": "An upcut saw cuts one end at a time — flexible and inexpensive, enough for a few dozen windows a shift. A double-head "
               "saw cuts both ends at once, to a length typed in or read from a barcode, with both heads tilting to 45°: the SC "
               "400S and SC 4000S roughly double a shop's output and take measuring errors out of the job. Many shops run a "
               "double-head saw for frames and an upcut saw for mullions and odd cuts."},
         {"q": "Do they cut aluminum as well as PVC?",
          "a": "Yes. The SC 402, 403, 400S and 4000S cut both, with hydro-pneumatic or hydro-check feeds that keep aluminum cuts "
               "clean and spray or oil cooling for the blade; the SC 401 slows its feed in aluminum and takes an optional cooling "
               "device and hydro-check. Fit a blade made for the material you cut."},
         {"q": "What do the model names mean?",
          "a": "SC — often written SC — is Plastmak's model prefix. Across the range, 1xx are welders, 2xx end mills and notchers, "
               "3xx bead saws, 4xx saws, 5xx routers and CNCs, 6xx corner cleaners, 9xx crimpers and 1000s conveyors; an S marks "
               "the servo or upgraded version, as on the SC 400S and SC 4000S."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about aluminum and PVC saws",
    related_pages=[{"href": f"{D.P_HUB}.html", "label": "Aluminum & PVC processing machines"},
                   {"href": f"{D.P_LINES}.html", "label": "Window production lines"},
                   {"href": "circular-cold-saws.html", "label": "Circular cold saws"}, {"href": "band-saw.html", "label": "Band saws"}],
    related_title="More aluminum, PVC and metal cutting machinery from NovoTech",
)

# ------------------------------------------------------------------------------------------------ welding & corner cleaning
PAGE_WELD = dict(
    title="PVC Window Welders & Corner Cleaners, 1–4 Corners | NovoTech",
    meta="Vinyl window welding machines from a single-head 25° – 180° welder to 4-corner welders and a welding and cleaning line, with knife and CNC corner cleaners.",
    h1="PVC window welding and corner cleaning machines — single-head, double-head and 4-corner welders, CNC corner cleaners",
    intro="A PVC (vinyl) window frame is joined by welding: the mitred profile ends are pressed against a heated plate until they "
          "melt, then pushed together and held while the seam cools; the bead of melted plastic left on the corner is cleaned "
          "off afterwards. NovoTech supplies the welders and corner cleaners of Plastmak, built in Bursa, Turkey: the SC 101 "
          "single-head welder for any angle from 25° to 180°; the SC 100 double-head welder for profiles 13-3/8″ to 126″ long; "
          "the SC 100 Gold Plus, which welds all four corners of a frame up to 145-11/16 × 106-5/16″ at once, and the Gold Plus "
          "Full line that adds a robot and a CNC cleaner; the SC 601 corner cleaner with three knives; and the SC 6000 and SC "
          "6000S CNC corner cleaners. All three welders can make a 0.2 mm (.008″) seam. Supplied with a CSA-approved panel, "
          "installed and supported from Mississauga, ON, Canada.",
    points=["SC 101 single-head, 25° – 180° · SC 100 double-head, profiles 13-3/8″ – 126″ long and to 6-5/16″ high",
            "SC 100 Gold Plus: four corners at once, frames to 145-11/16 × 106-5/16″ · Gold Plus Full welding and cleaning line",
            "SC 601 three-knife corner cleaner · SC 6000 and 6000S CNC cleaners, up to 500 frames a shift"],
    hero="pm-100gp", minis=["pm-100", "pm-6000s"],
    groups=[("pm-weld", "PVC window welding machines",
             "Single, double and 4-corner welders with PLC or servo control and welding recipes for every profile.", P),
            ("pm-clean", "Corner cleaning machines", "They take the weld bead off the corners, faces and seal grooves after welding.", P)],
    faq=[{"q": "How does a PVC welder work?",
          "a": "The two mitred profiles are clamped and pressed against a Teflon-covered heating plate until their ends melt; the "
               "plate is withdrawn and the ends are pressed together and held while the joint cools — welding, cooling and "
               "temperature set for each profile type. A 0.2 mm seam limits the weld bead to 0.2 mm (.008″), so laminated and "
               "coloured profiles need little or no cleaning."},
         {"q": "Which welder for my output?",
          "a": "The single-head SC 101 welds one corner at a time — four cycles a frame, any angle, the right start for small "
               "shops and arched windows. The double-head SC 100 welds two corners at once, and the SC 100 Gold Plus all four, so "
               "a frame is welded in one cycle and comes out square. The Gold Plus Full carries the frame on to a CNC cleaner by "
               "robot, with no operator in between."},
         {"q": "Why clean the corners?",
          "a": "Welding leaves a bead of melted PVC on the faces and in the gasket grooves of every corner; left on, it stops "
               "gaskets and hardware from seating and looks poor. The SC 601 cleans the corner and faces with knives in one PLC "
               "cycle; the CNC cleaners also clean seal grooves, radii and laminated profiles — the SC 6000S with 10 tools and "
               "automatic profile recognition."},
         {"q": "What frame sizes fit the 4-corner welder?",
          "a": "Frames from 16-1/8 × 19-1/2″ (410 × 495 mm) up to 145-11/16 × 106-5/16″ (3,700 × 2,700 mm), with profiles 1-9/16″ to "
               "7-7/8″ high and up to 5-7/8″ wide. With the gasket press option the range is 20-1/2 × 20-1/2″ to "
               "143-11/16 × 104-5/16″."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about PVC window welding machines",
    related_pages=[{"href": f"{D.P_SAWS}.html", "label": "Aluminum & PVC saws"}],
)

# ------------------------------------------------------------------------------------------------ CNC, copy routers, end milling
PAGE_CNC = dict(
    title="Aluminum Profile CNC Centres & Copy Routers | NovoTech",
    meta="A 9-axis profile machining centre to 21′ 4″, 3-axis CNC drilling and milling machines, copy and drainage routers and end mills for window profiles.",
    h1="Profile machining centres, copy routers and end milling machines for aluminum and PVC windows",
    intro="Before a window frame is assembled, its profiles are machined for the hardware — lock and handle places, hinge and "
          "espagnolette slots, drainage slots — and its mullions are end-milled to fit the frame. NovoTech supplies these machines "
          "from Plastmak, built in Bursa, Turkey, from template-guided to fully automatic: copy routers that follow a template "
          "(the SC 501, 502S and 512 with triple drilling units, the SC 521S for drainage slots and the SC 542 for aluminum); the "
          "SC 211 and SC 211S end milling machines; the SC 5000 and SC 5000S 3-axis CNC drilling and milling machines with three "
          "spindles; and the SC 4550, a 9-axis machining and cutting centre that takes profiles up to 21′ 4″ (6,500 mm) from a "
          "magazine and delivers them machined, cut and labelled. Supplied with a CSA-approved panel, installed and supported "
          "from Mississauga, ON, Canada.",
    points=["SC 4550: 9 axes, 10 spindles, profiles 78-3/4″ – 255-7/8″, cut at 30° – 150°",
            "SC 5000 · 5000S: 3-axis CNC, 3 spindles at 18,000 rpm, travel 15-3/8 × 7-7/8 × 7-7/8″",
            "Copy routers SC 501 · 502S · 512 · 521S · 542 · end mills SC 211 · 211S, cutters to Ø6-5/16″"],
    hero="pm-4550", minis=["pm-5000s", "pm-502s"],
    groups=[("pm-cnc", "CNC profile machining centres", "Programmed machining of every hardware place in one clamping — up to a 9-axis line with saw and magazine.", P),
            ("pm-copy", "Copy routers", "Template-guided routing and triple drilling for lock, handle, hinge and drainage cut-outs in series.", P),
            ("pm-endmill", "End milling machines", "Mullion (transom) ends milled to the contour of the frame profile.", P)],
    faq=[{"q": "Copy router or CNC?",
          "a": "A copy router repeats a cut-out from a template: quick to set up, inexpensive, ideal for a few profile systems. A "
               "CNC is programmed instead — new hardware or a new profile system is a new program, not a new template — and the "
               "SC 5000 and 5000S make every cut-out of a profile in one clamping, the SC 5000S from DXF drawings. The SC 4550 "
               "adds a magazine, cutting and labelling for unattended work."},
         {"q": "What does an end milling machine do?",
          "a": "It cuts the end of a mullion (transom) to the shape of the frame profile it meets, so the T-joint closes tight and "
               "can be screwed. A stack of cutters matching the profile does it in one pass; the SC 211S changes the whole stack "
               "with one button when the profile series changes and mills at angles from −45° to +45°."},
         {"q": "Which machines work on aluminum?",
          "a": "The SC 502S, 512, 542, 5000S, 4550 and 211S work on aluminum as well as PVC, with 18,000 rpm spindles and cooling "
               "where aluminum needs it; the SC 501, 521S and 5000 are for PVC, and the SC 211 mills both."},
         {"q": "What does the SC 4550 do?",
          "a": "It takes up to seven profiles from its magazine, measures each, clamps it on a 3-axis holding station, grooves, "
               "drills, marks and mills it with ten spindles and cuts it with a servo saw at any angle from 30° to 150° — "
               "profiles 78-3/4″ to 255-7/8″ long. Finished parts leave on a conveyor with a printed barcode label, and the "
               "offcuts go to a cart."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about profile machining centres and copy routers",
    related_pages=[{"href": f"{D.P_SAWS}.html", "label": "Aluminum & PVC saws"}],
)

# ------------------------------------------------------------------------------------------------ assembly
PAGE_ASSY = dict(
    title="Corner Crimping & Window Assembly Machines | NovoTech",
    meta="A hydraulic corner crimper for aluminum frames, pneumatic screwing and sash assembly machines, portable notching and copy milling machines and conveyors.",
    h1="Window assembly machines — corner crimper, screwing and sash assembly, portable machines and conveyors",
    intro="Once the profiles are cut and machined, the frames are put together: aluminum corners are crimped over cleats, "
          "reinforcements and hardware are screwed in, and the sashes are fitted with their hardware. NovoTech supplies the "
          "machines for that from Plastmak, built in Bursa, Turkey: the SC 902 hydraulic corner crimper with 4 + 4 knives; single "
          "and double-head pneumatic screwing machines and a sash assembly machine that fits a double-opening sash's hardware in "
          "3.5 minutes; the SC 221 and SC 551 portable notching and copy milling machines; and the SC 1000 digital measuring "
          "conveyor with the SC 1001 – 1003 conveyors that carry profiles to and from every machine. Supplied with a "
          "CSA-approved panel, installed and supported from Mississauga, ON, Canada.",
    points=["SC 902 hydraulic corner crimper: 4 + 4 knives, aluminum profiles to 5-1/8″ high",
            "Single and double-head screwing machines · sash assembly machine, double sash in 3.5 min",
            "SC 221 · SC 551 portable machines · SC 1000 measuring conveyor 9′ 10″, ±.020″"],
    hero="pm-902", minis=["pm-sash", "pm-1000"],
    groups=[("pm-crimp", "Corner crimping machine", "Aluminum frame corners locked over their cleats by hydraulic knives.", P),
            ("pm-screw", "Screwing and sash assembly machines", "Pneumatic screwing stations and automatic sash hardware fitting.", P),
            ("pm-portable", "Portable machines and conveyors", "Bench machines for small shops and site work, and the conveyors that link every machine.", P)],
    faq=[{"q": "How is an aluminum frame joined?",
          "a": "Aluminum profiles are not welded: a cleat (corner bracket) is pushed into the mitred ends, and the crimper drives "
               "knives into the profile walls over the cleat so they lock onto it. The SC 902 does it hydraulically with four "
               "knives a side, set to the profile with millimetre scales, while a pneumatic miter wedge holds the corner square."},
         {"q": "What does the sash assembly machine do?",
          "a": "It fits the hardware of single and double-opening sashes without moulds or templates: it measures the sash, drills "
               "with a three-arm unit, mills the espagnolette groove and screws the hardware in, aligned by laser — 3.5 minutes on "
               "average for a double-opening window."},
         {"q": "Why a digital measuring conveyor?",
          "a": "It sets the saw's length stop for you: type the length on the SC 1000's touch screen and the stop moves there to "
               "±.020″ (±0.5 mm), then retracts at one push so the cut piece comes out. No tape and no reading errors, and it fits "
               "any of the saws."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about window assembly machines",
    related_pages=[{"href": f"{D.P_SAWS}.html", "label": "Aluminum & PVC saws"}],
)

# ------------------------------------------------------------------------------------------------ production groups
PAGE_LINES = dict(
    title="Window Production Lines, 40 – 220 Windows a Shift | NovoTech",
    meta="Matched PVC and aluminum window production groups — single-head, double-head and aluminum sets and a full PVC workshop — with power, air and weight.",
    h1="Window production lines — PVC and aluminum production groups for 40 to 220 windows a shift",
    intro="A window shop is a flow of machines, and its output is set by the slowest of them. Plastmak plans production groups in "
          "which every step keeps pace with the others, and NovoTech supplies four of them: a PVC single-head group (six machines, "
          "40 – 60 windows in an 8-hour shift), a PVC double-head group (six machines, 80 – 120 windows), an aluminum double-head "
          "group (four machines, 80 – 120 windows) and a complete PVC workshop laid out as a loop (seven machines, 200 – 220 "
          "windows). Each table lists the machines with their capacity, power, air and weight, and the totals for the group. "
          "Machines can be swapped or added to suit your profiles and output; we plan the layout, install the line and train your "
          "team from Mississauga, ON, Canada.",
    points=["PVC single-head group: 6 machines, 40 – 60 windows a shift",
            "PVC double-head and aluminum double-head groups: 80 – 120 windows a shift",
            "Complete PVC workshop with compressor: 7 machines, 200 – 220 windows a shift"],
    hero="pm-line-shop", minis=["pm-line-pvc2", "pm-line-alu"],
    groups=[("pm-lines", "Production groups", "Matched sets of Plastmak machines, from a starting shop to a complete production loop.", P)],
    faq=[{"q": "How many windows will a group make?",
          "a": "Plastmak's figures for an 8-hour shift are 40 – 60 windows for the PVC single-head group, 80 – 120 for the PVC and "
               "aluminum double-head groups and 200 – 220 for the complete workshop. The real number depends on window sizes and "
               "types, the profile system and how many people run the line — tell us your mix and we will estimate it."},
         {"q": "Can I start small and grow?",
          "a": "Yes. The groups share machines: the copy router, end mill, bead saw and corner cleaner of the single-head group stay "
               "when a double-head saw and welder are added, and a CNC corner cleaner, a 3-axis CNC or a 4-corner welder can "
               "follow later."},
         {"q": "What do I need on site?",
          "a": "Three-phase power for the installed load in each table, compressed air at 87 – 116 psi (6 – 8 bar) for the "
               "consumption listed — the workshop group includes a 130 gal (500 l) compressor — and floor space for the machines in "
               "a loop, with room for 21-ft profiles. We provide a layout before delivery."},
         VOLT_FAQ_GENERIC],
    faq_title="Questions we get asked about window production lines",
    related_pages=[{"href": f"{D.P_SAWS}.html", "label": "Aluminum & PVC saws"}],
)

# ------------------------------------------------------------------------------------------------ hub
HUB_PAGE = dict(
    title="Aluminum & PVC Window Fabrication Machinery | NovoTech",
    meta="Welders, corner cleaners, CNC machining centres, copy routers, end mills, corner crimpers and complete lines for vinyl and aluminum windows and doors.",
    h1="Aluminum & PVC window and door machinery — welding, cleaning, machining, assembly and complete lines",
    intro="Window and door shops turn PVC (vinyl) and aluminum profiles into frames in a set order: cut, machine the hardware "
          "places, weld or crimp the corners, clean the welds, mill the mullion ends, cut the glazing beads and assemble. NovoTech "
          "supplies the machines for every step from Plastmak, built in Bursa, Turkey: single-, double- and 4-corner PVC welders "
          "and CNC corner cleaners; a 9-axis profile machining centre, 3-axis CNC drilling and milling machines, copy routers and "
          "end milling machines; a hydraulic corner crimper, screwing and sash assembly machines, portable machines and "
          "conveyors; and complete production groups for 40 to 220 windows a shift. The saws have their own page — upcut, "
          "double-head, bead and miter saws. Every machine is supplied with a CSA-approved panel, installed and supported from "
          "Mississauga, ON, Canada. Below, each page in brief.",
    points=[f"<a href=\"{D.P_WELD}\">PVC welding & corner cleaning</a> — 1, 2 and 4-corner welders, knife and CNC corner cleaners",
            f"<a href=\"{D.P_CNC}\">CNC centres & copy routers</a> — 9-axis centre, 3-axis CNC, copy routers, end mills · "
            f"<a href=\"{D.P_ASSY}\">assembly machines & conveyors</a>",
            f"<a href=\"{D.P_LINES}\">Production groups</a> for 40 – 220 windows a shift · <a href=\"{D.P_SAWS}\">aluminum & PVC saws</a>"],
    hero="pm-100gp", minis=["pm-4550", "pm-5000s"],
    faq=[{"q": "What machines does a PVC window shop need?",
          "a": "At the least a saw, a copy router for the hardware and drainage holes, a welder, a corner cleaner, an end milling "
               "machine for the mullions and a glazing bead saw — the six machines of the PVC single-head group, about 40 – 60 "
               "windows a shift. Double-head saws and welders double that; a 4-corner welder, CNC corner cleaner and 3-axis CNC "
               "take a shop past 200 windows a shift."},
         {"q": "What is different for aluminum windows?",
          "a": "Aluminum frames are not welded but joined with corner cleats and crimped — on the SC 902 — and the profiles are "
               "cut on saws with cooling and hydro-check feeds, machined on copy routers or CNCs with cooled 18,000 rpm spindles "
               "and end-milled on the heavier SC 211S. The aluminum double-head group puts those machines together."},
         {"q": "PVC, uPVC or vinyl?",
          "a": "The same material: rigid PVC, called uPVC in Europe and vinyl in North America. Every machine on these pages that "
               "is marked PVC works on vinyl window and door profiles."},
         {"q": "Can you plan a complete shop?",
          "a": "Yes. Tell us the windows and doors you make, the profile systems and the output you need; we propose the machines, "
               "a layout and the air and power supply — as in Plastmak's workshop plan — then install and commission the line "
               "and train your operators."},
         {"q": "Do you install the machines and train operators?",
          "a": "Yes. Our technicians install and commission every machine anywhere in Canada, set it up for your profiles and train "
               "the operators; spare parts and tooling are supplied from Mississauga, ON, Canada, and we support every machine by video "
               "call."},
         VOLT_FAQ_GENERIC],
    range_lead="Capacity, profiles, power, air and weight for every model on the four pages. Each row links to the full specification table of its machine.",
    range_cols=["Capacity", "Profiles", "Power", "Air", "Weight"],
    range_caption="Aluminum and PVC window and door machinery supplied by NovoTech — Plastmak, made in Turkey",
    range_note="Power is the machine's total installed power; air is the consumption at 87 – 116 psi (6 – 8 bar). Production groups show the sums of their machines. Weights are approximate.",
)
SUBPAGES = [  # slug, title, image, blurb, nav label
    (D.P_WELD, "PVC welding & corner cleaning", "pm-100gp", "SC 101 single-head, SC 100 double-head and SC 100 Gold Plus 4-corner welders, the Gold Plus Full line, SC 601 and SC 6000 / 6000S corner cleaners.", "PVC welding & corner cleaning"),
    (D.P_CNC, "CNC centres, copy routers & end mills", "pm-4550", "SC 4550 9-axis machining centre, SC 5000 / 5000S 3-axis CNC, five copy routers and the SC 211 / 211S end milling machines.", "CNC centres & copy routers"),
    (D.P_ASSY, "Assembly machines & conveyors", "pm-902", "SC 902 hydraulic corner crimper, screwing and sash assembly machines, SC 221 / 551 portable machines and SC 1000 – 1003 conveyors.", "Assembly & conveyors"),
    (D.P_LINES, "Window production lines", "pm-line-pvc2", "Four matched production groups for PVC and aluminum windows, 40 to 220 windows a shift, with power, air and weight.", "Production lines"),
]
PAGES = {D.P_WELD: PAGE_WELD, D.P_CNC: PAGE_CNC, D.P_ASSY: PAGE_ASSY, D.P_LINES: PAGE_LINES}


def register_images():
    imap_path = os.path.join(ROOT, "tools", "image_map.json")
    imap = json.load(open(imap_path, encoding="utf-8"))
    d = os.path.join(ROOT, "tools", "src-images", "plastmak")
    keys = []
    for key, p in PH.PHOTOS.items():
        f = [x for x in os.listdir(d) if x.startswith(key + ".")] if os.path.isdir(d) else []
        if not f:
            print("!! missing export for", key)
            continue
        ext = os.path.splitext(f[0])[1]
        imap[key] = {"src": f"tools/src-images/plastmak/{key}{ext}", "alt": p["alt"], "section": "plastmak", "trim": False, "quality": 82,
                     "cutout": ext in (".png", ".webp")}
        keys.append(key)
    imap["plastmak-logo"] = {"src": "tools/src-images/plastmak-logo.png", "alt": "Plastmak", "section": "site", "trim": True, "quality": 90, "cutout": False}
    keys.append("plastmak-logo")
    json.dump(imap, open(imap_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "tools", "plastmak_keys.txt"), "w").write(",".join(keys))
    return keys


def video_ids():
    return list(dict.fromkeys(v["id"] for f in D.FAMILIES for v in f["videos"]))


def copy_pdf():
    """only when the site has no brochure at all: the owner's first catalogue.  The site's copy is the generated brochure
    (tools/brochure/specs/plastmak.json, Nov 12 2026), so it is never overwritten from the original"""
    dst = os.path.join(ROOT, "src", PDF_FILE)
    if not os.path.exists(dst):
        shutil.copyfile(PDF_SRC, dst)


def build():
    copy_pdf()
    SHARED["catalogue_pdf"] = pdf()
    allf = families(D.P_SAWS) + families(D.P_WELD) + families(D.P_CNC) + families(D.P_ASSY) + families(D.P_LINES)
    write_families(SET, allf)
    write_category(D.P_SAWS, PAGE_SAWS, allf, SET, "Aluminum & PVC saws", extra={**SHARED, "nav_label": "Aluminum & PVC saws"})
    hub = {"slug": D.P_HUB, "label": "All aluminum & PVC processing machines", "image": "pm-100gp",
           "blurb": "Every Plastmak welding, cleaning, machining and assembly machine and production group NovoTech supplies."}
    sib = [(s, nav, title) for s, title, _, _, nav in SUBPAGES]
    for slug, p in PAGES.items():
        extra = dict(SHARED, nav_label=dict((s, nav) for s, _, _, _, nav in SUBPAGES)[slug])
        write_category(slug, {**p, "related_title": RELATED_TITLE}, allf, SET, SECTION, hub=hub, siblings=sib, extra=extra)
    write_hub(D.P_HUB, {**HUB_PAGE, "artifact_title": "Aluminum & PVC Window Machinery", "faq_title": "Questions we get asked about window and door machinery",
                        "nav_label": "All aluminum & PVC processing machines", "related_blurb": hub["blurb"]},
              allf, SET, SECTION, SUBPAGES,
              extra={**SHARED, "range_pick": ["capacity", "profile", "power", "air", "weight"],
                     "related_pages": [{"href": f"{s}.html", "label": t} for s, t, _, _, _ in SUBPAGES] +
                                      [{"href": f"{D.P_SAWS}.html", "label": "Aluminum & PVC saws"}, {"href": "circular-cold-saws.html", "label": "Circular cold saws"}]})
    keys = register_images()
    pages = [PAGE_SAWS, HUB_PAGE] + list(PAGES.values())
    used = {k for f in D.FAMILIES for k in f["images"]} | {p["hero"] for p in pages} | {m for p in pages for m in p["minis"]} | {s[2] for s in SUBPAGES}
    unused = sorted(set(keys) - used - {"plastmak-logo"})
    if unused:
        print("photos not used on a page:", unused)
    missing = sorted(used - set(keys))
    if missing:
        print("!! image keys without a photo:", missing)
    open(os.path.join(ROOT, "tools", "plastmak_vids.txt"), "w").write(" ".join(video_ids()))
    for name, p in [("saws", PAGE_SAWS), ("hub", HUB_PAGE)] + [(s, PAGES[s]) for s in PAGES]:
        print(f"{name:42s} title {len(p['title'])} · meta {len(p['meta'])}")
    print(f"plastmak: {len(D.FAMILIES)} families · {sum(len(f['specs']['models']) for f in D.FAMILIES)} models · images: {len(keys)} · videos: {len(video_ids())}")


if __name__ == "__main__":
    build()
