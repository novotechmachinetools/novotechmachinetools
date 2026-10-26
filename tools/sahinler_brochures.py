#!/usr/bin/env python3
"""NovoTech-format brochures for the premium line (the Turkish-built machines sold without the supplier's brand): five
brochure specs in tools/brochure/specs/premium-*.json, built by tools/brochure/build_brochure.py, and the pdf entries the
page generators attach to the families (PDFS below, imported by tools/sahinler_lib.py).

    python3 tools/sahinler_brochures.py            # writes the specs
    for s in tools/brochure/specs/premium-*.json; do python3 tools/brochure/build_brochure.py $s; done
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVER = "NovoTech premium line · made in Turkey · sold & serviced in Canada by NovoTech"
KICKER = "NovoTech premium line · made in Turkey"
MADE_IN = "Made in Turkey to NovoTech's specification — CE-certified, European components"
ABOUT_LINE = ("The machines in this catalogue are NovoTech's premium line: built in Turkey to NovoTech's specification by a CE-certified "
              "metal-forming plant with more than 40 years of machine building and exports to over 100 countries, with European hydraulic "
              "and electrical components, inspected before shipping, and sold under NovoTech's name with a CSA-approved panel, a 1-year "
              "warranty and spare parts and technical support from NovoTech in Mississauga, Ontario.")

# brochure name → (pdf file, button label, families by set, spec)
BROCHURES = {
    "premium-angle-rolls": dict(
        file="files/NovoTech-Angle-Rolls-Section-Benders-2026.pdf", label="Download the angle rolls brochure",
        title="Angle rolls and section benders",
        subtitle="PK motorized benders · HPK 40 – 120 hydraulic section and pipe benders · HPK DP heavy-duty beam benders to HEB 600 · TC-42 NC coiler",
        range_label="Angle rolls and section benders", about_for="angle rolls and section benders",
        about_title="Angle, pipe, tube and beam bent into rings, arcs and spirals",
        about_text=[ABOUT_LINE,
                    "An angle roll pushes a bar, angle, pipe, tube or beam between three rolls to bend it into an arc, a ring or a spiral. The PK 30 and PK 35 are "
                    "the motorized benders for small flat bar, angle and tube; the hydraulic HPK 40 to HPK 120 add digital readouts, hydraulic guide rolls and "
                    "optional NC control for section and pipe to 6″ Schedule 40; the HPK DP heavy-duty benders roll channel, I-beam and H-beam up to HEB 600; "
                    "and the TC-42 NC coiling machine winds tube into variable-pitch coils. Every machine rolls horizontally or vertically and ships with a "
                    "standard roll set; pipe, tube, angle and special profile rolls are available for all of them."],
        family_sets=["sahinler"], families=["sahinler-pk", "sahinler-hpk-40", "sahinler-hpk-50-60", "sahinler-hpk-65-80", "sahinler-hpk-100-120", "sahinler-hpk-dp", "sahinler-tc-42"],
        groups=[{"title": "Motorized section benders", "families": ["sahinler-pk"]},
                {"title": "Hydraulic section and pipe benders", "families": ["sahinler-hpk-40", "sahinler-hpk-50-60", "sahinler-hpk-65-80", "sahinler-hpk-100-120"]},
                {"title": "Heavy-duty beam benders and coilers", "families": ["sahinler-hpk-dp", "sahinler-tc-42"]}],
        cover_photos=["sh-hpk80", "sh-hpk160dp", "sh-pk35"]),
    "premium-ironworkers": dict(
        file="files/NovoTech-Ironworkers-Punching-Machines-2026.pdf", label="Download the ironworkers & punching brochure",
        title="Hydraulic ironworkers and punching machines",
        subtitle="HKM single- and double-piston ironworkers 44 – 193 US tons · HPM hydraulic punches to 193 US tons · HPM DP, HPM CNC and NC punching lines",
        range_label="Ironworkers and punching machines", about_for="ironworkers and punching machines",
        about_title="Five stations on one machine — punch, shear, notch, cut angle and bar",
        about_text=[ABOUT_LINE,
                    "The HKM ironworkers put the five jobs of the structural shop on one machine: punching, round and square bar shear, angle shear, flat-bar and "
                    "sheet shear and rectangular notching, each with its own station and LED light — single-piston machines from the 44 US ton HKM 40 to the "
                    "193 US ton HKM 175, and double-piston machines with two cylinders and two pedals so two operators work at once. The HPM hydraulic punching "
                    "machines make round, oblong and shaped holes in plate, angle and sections in one stroke — bench-height 33 and 44 ton punches, 72 to 193 ton "
                    "machines with a 24.6″ throat, double-head HPM DP, the HPM CNC with a Siemens-controlled table and the NC lines that copy hole patterns along "
                    "angles, flat bar and beams. Punches and dies interchange across the range."],
        family_sets=["sahinler"], families=["sahinler-hkm-single", "sahinler-hkm-double", "sahinler-hpm", "sahinler-hpm-dp", "sahinler-hpm-cnc", "sahinler-hpm-nc-line"],
        groups=[{"title": "Hydraulic ironworkers", "families": ["sahinler-hkm-single", "sahinler-hkm-double"]},
                {"title": "Hydraulic punching machines", "families": ["sahinler-hpm", "sahinler-hpm-dp", "sahinler-hpm-cnc", "sahinler-hpm-nc-line"]}],
        cover_photos=["sh-hkm115", "sh-hpm65", "sh-hkm60"]),
    "premium-shop-presses": dict(
        file="files/NovoTech-Hydraulic-Shop-Presses-2026.pdf", label="Download the shop presses brochure",
        title="Hydraulic shop presses",
        subtitle="DPM H-frame shop presses 33 – 220 US tons · DPM-K and DK mobile-cylinder presses · AT T-slot die presses · AP garage press brakes · DK-S straightening presses to 441 US tons",
        range_label="Hydraulic shop presses", about_for="hydraulic shop presses",
        about_title="The press every repair shop and fabricator reaches for several times a day",
        about_text=[ABOUT_LINE,
                    "A hydraulic shop press presses bearings, bushings and pins, straightens shafts and bar, bends flat bar and short plate and pushes a die for the "
                    "odd forming job. The DPM series runs from 33 to 220 US tons with two-speed joystick control, a pressure gauge and relief valve; the DPM-K and "
                    "DK carry a cylinder that slides across the frame so the ram meets the work instead of the work being shifted under the ram; the AT presses "
                    "have T-slot tables for your own forming, blanking and coining dies; the AP garage-type press brake bends 1/4″ and 3/8″ plate over 40″ and "
                    "60″ with its prism die; and the DK-S 3-axis straightening presses from 220 to 441 US tons straighten plates, beams and bar under a moving ram."],
        family_sets=["sahinler"], families=["sahinler-dpm", "sahinler-dpm-k", "sahinler-at", "sahinler-ap", "sahinler-dk-s"],
        groups=[{"title": "H-frame shop presses", "families": ["sahinler-dpm", "sahinler-dpm-k"]},
                {"title": "Die presses, press brakes and straightening presses", "families": ["sahinler-at", "sahinler-ap", "sahinler-dk-s"]}],
        cover_photos=["sh-dpm", "sh-dks400", "sh-dpmk"]),
    "premium-plate-rolls": dict(
        file="files/NovoTech-Plate-Rolls-Premium-Line-2026.pdf", label="Download the premium-line plate rolls brochure",
        title="Plate rolling machines",
        subtitle="4R HSS heavy-duty, 4R HS-L linear and 4R HS orbital 4-roll plate rolls · 4RH cassette rolls · 4R HC conical rolls · 3R UHS and 3R HS 3-roll plate rolls",
        range_label="Plate rolling machines", about_for="plate rolling machines",
        about_title="Four-roll and three-roll plate rolls for shells, tanks, stacks and cones",
        about_text=[ABOUT_LINE,
                    "A four-roll plate roll pinches the plate between the top and bottom rolls and bends it with the two side rolls, so the sheet is pre-bent at "
                    "both ends and rolled into a shell in one pass without a flat end — the 4R HSS heavy-duty machines with an NC console and hydraulic drop-end "
                    "roll plate to 10 ft and more, the 4R HS-L and 4R HS are the linear and orbital versions for the general fabricator, the 4RH cassette rolls "
                    "serve the sheet-metal shop and the 4R HC rolls cones on cone-machined rolls. The three-roll 3R UHS translating heavy-duty and 3R HS hydraulic "
                    "plate rolls take thicker plate at a lower price. Overhead cranes, hydraulic side supports, cone-bending devices and digital readouts are options "
                    "across the range."],
        family_sets=["plate-rolls"], families=["sahinler-4r-hss", "sahinler-4r-hsl", "sahinler-4r-hs", "sahinler-4rh", "sahinler-4r-hc", "sahinler-3r-uhs", "sahinler-3r-hs"],
        groups=[{"title": "Four-roll plate rolls", "families": ["sahinler-4r-hss", "sahinler-4r-hsl", "sahinler-4r-hs", "sahinler-4rh", "sahinler-4r-hc"]},
                {"title": "Three-roll plate rolls", "families": ["sahinler-3r-uhs", "sahinler-3r-hs"]}],
        cover_photos=["sh-4rhss-30-380-nc", "sh-3rhs-20-210", "sh-4rh-10-90-nc"]),
    "premium-sheet-metal": dict(
        file="files/NovoTech-Notchers-Circle-Cutters-Pipe-Polishers-Benders-2026.pdf", label="Download the notchers, circle cutters, polishers & benders brochure",
        title="Corner notchers, circle cutters, pipe polishers and pipe benders",
        subtitle="HNM fixed and variable-angle hydraulic corner notchers · SDK 6 / SDK 8 circular cutting and flanging machines · EFM 6 elliptical cutter · BT 114-S pipe polisher · SPB 60 / 76 NC pipe draw benders",
        range_label="Sheet-metal and pipe shop machines", about_for="corner notchers, circle cutters, pipe polishers and pipe benders",
        about_title="The machines around the shear and the press brake",
        about_text=[ABOUT_LINE,
                    "The HNM hydraulic corner notchers cut the 90° and variable-angle notches that let a sheet fold into a box; the SDK 6 and SDK 8 cut and flange "
                    "circular blanks and tank heads to Ø15 ft in 5/16″ plate and the EFM 6 does the same for elliptical heads; the BT 114-S polishes and sands "
                    "round and square tube to a satin finish with a mobile pendant; and the SPB 60 and SPB 76 NC draw benders bend handrail and furniture tube "
                    "around a die with a programmed sequence of bends. All with a CSA-approved panel, installed and supported from Mississauga."],
        family_sets=["sahinler", "circle-cutting", "tube-benders"],
        families=["sahinler-hnm-fixed", "sahinler-hnm-variable", "sahinler-sdk", "sahinler-efm", "sahinler-bt-114-s", "sahinler-spb"],
        groups=[{"title": "Hydraulic corner notchers", "families": ["sahinler-hnm-fixed", "sahinler-hnm-variable"]},
                {"title": "Circular and elliptical cutting and flanging", "families": ["sahinler-sdk", "sahinler-efm"]},
                {"title": "Pipe polishing and pipe bending", "families": ["sahinler-bt-114-s", "sahinler-spb"]}],
        cover_photos=["sh-hnm6v", "sh-sdk8", "sh-bt114s-photo"]),
}


def pdf_entry(name):
    b = BROCHURES[name]
    f = os.path.join(ROOT, "src", b["file"])
    size = f"PDF · {os.path.getsize(f) / 1e6:.0f} MB · imperial units" if os.path.exists(f) else "PDF · imperial units"
    return {"file": b["file"], "label": b["label"], "size": size}


# family id → brochure name
FAMILY_PDF = {fid: name for name, b in BROCHURES.items() for fid in b["families"]}


def write_specs():
    d = os.path.join(ROOT, "tools", "brochure", "specs")
    for name, b in BROCHURES.items():
        spec = {k: v for k, v in b.items() if k not in ("file", "label")}
        spec.update(cover_line=COVER, about_kicker=KICKER, country="Turkey", made_in=MADE_IN, single_phase=False, year="2026", out="src/" + b["file"])
        json.dump(spec, open(os.path.join(d, name + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(BROCHURES)} premium-line brochure specs written")


if __name__ == "__main__":
    write_specs()
