#!/usr/bin/env python3
"""Wecotech photos: the renders and sample-part photos extracted from the Wecotech tube-end-forming catalogue
(/home/claude/wecotech/cat.pdf → `pdfimages -j -p -f 8 -l 63 cat.pdf img/w`, files img/w-<page>-<n>.jpg) → copied to
tools/src-images/wecotech/<key>.jpg.  The machine renders are on white and are cut out by BiRefNet; the sample parts (grey
studio background), tool diagrams and option crops stay rectangular (cutout=False).  No logo removal — Wecotech is shown
under its own name.

    python3 tools/wecotech_photos.py        export (copy)
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/wecotech/img/"
OUT = os.path.join(ROOT, "tools", "src-images", "wecotech")


def R(page, n, alt, cutout=True):
    return dict(src=f"w-{page:03d}-{n:03d}.jpg", alt=alt, cutout=cutout)


PHOTOS = {
    # Easy line
    "wt-tubex": R(9, 10, "Wecotech Tubex compact tube end expander — vertical hydraulic unit with foot switch"),
    "wt-tubex-horizontal": R(9, 11, "Tubex — optional horizontal version", False),
    "wt-tubex-table": R(9, 12, "Tubex — optional Ø480 mm steel supporting table", False),
    "wt-tubex-part": R(9, 1, "Expanded and calibrated tube end made on the Tubex", False),
    "wt-tubin": R(11, 21, "Wecotech Tubin compact tube end reducer (impander)"),
    "wt-tubin-horizontal": R(11, 22, "Tubin — optional horizontal version", False),
    "wt-tubin-part": R(11, 16, "Reduced tube end made on the Tubin", False),
    "wt-tubepunch": R(13, 29, "Wecotech Tubepunch tube end punching unit"),
    "wt-tubepunch-unit": R(13, 28, "Tubepunch — punching unit with punch and die interface", False),
    "wt-tubepunch-part": R(13, 24, "Slotted tube end made on the Tubepunch", False),
    "wt-tubepress": R(15, 37, "Wecotech Tubepress tube straightening press"),
    "wt-tubepress-process": R(15, 40, "Tubepress — the bent tube is pressed round again before forming", False),
    "wt-tubepress-part": R(15, 35, "Tube end calibrated round after bending", False),
    # Universal line
    "wt-tubex-u": R(17, 42, "Wecotech Tubex-U universal production expander with touchscreen on pivot arm"),
    "wt-tubex-u-horizontal": R(17, 48, "Tubex-U — optional horizontal version", False),
    "wt-tubex-u-part": R(17, 43, "Expanded tube end made on the Tubex-U", False),
    "wt-tubin-u": R(19, 61, "Wecotech Tubin-U universal production reducer"),
    "wt-tubin-u-horizontal": R(19, 60, "Tubin-U — optional horizontal version", False),
    "wt-tubin-u-part": R(19, 56, "Reduced tube end made on the Tubin-U", False),
    "wt-tubax-u": R(27, 93, "Wecotech Tubax-U axial forming machine with tube clamping"),
    "wt-tubax-u-300": R(27, 94, "Tubax-U variant 300 with the larger clamping unit", False),
    "wt-tubax-u-diagram": R(27, 91, "Tubax-U — clamping and moulding jaws hold the tube while the axial tool forms the end", False),
    "wt-tubax-u-part": R(27, 85, "Axially formed tube end with collar made on the Tubax-U", False),
    "wt-tubax-rotary": R(29, 104, "Wecotech Tubax-Rotary Electra servo-electric rotary forming machine"),
    "wt-tubax-rotary-400": R(29, 105, "Tubax-Rotary Electra variant 400 for tube to Ø400 mm", False),
    "wt-tubax-rotary-diagram": R(29, 102, "Tubax-Rotary — the rotating forming head moves axially against the clamped tube", False),
    "wt-tubax-rotary-part": R(29, 96, "Rolled collar with sealing face made on the Tubax-Rotary", False),
    "wt-tubax-multi": R(31, 108, "Wecotech Tubax-Multi Electra multi-station forming centre with servo tool changer"),
    "wt-tubax-multi-part": R(31, 112, "Press-fit copper elbow formed on the Tubax-Multi", False),
    "wt-tubax-multi-part2": R(31, 109, "Tube with formed ends from the Tubax-Multi", False),
    "wt-tubiroll": R(33, 116, "Wecotech Tubiroll-2R automatic beading and flanging machine with light curtain"),
    "wt-tubiroll-diagram": R(33, 123, "Tubiroll-2R — two rolls bead or flange the tube end", False),
    "wt-tubiroll-part": R(33, 117, "Beaded duct end made on the Tubiroll-2R", False),
    # Traditional line
    "wt-tubimatic-c160": R(41, 170, "Wecotech Tubimatic C 160 UNO end former for commercially available C-tools"),
    "wt-tubimatic-c80tre": R(39, 150, "Tubimatic C 80 TRE with three C-tool stations", False),
    "wt-tubimatic-c80uno": R(37, 148, "Tubimatic C 80 UNO compact end former", False),
    "wt-tubimatic-c-diagram": R(37, 143, "Tubimatic C — expansion, impanding and C-IO combination tool sets", False),
    "wt-tubimatic-c-part": R(37, 136, "Flared and expanded tube end made with a C-tool", False),
    "wt-tubimatic-io80": R(43, 183, "Wecotech Tubimatic IO 80 inner / outer tool end former"),
    "wt-tubimatic-io80-electra": R(45, 191, "Tubimatic IO 80 Electra — servo-electric version", False),
    "wt-tubimatic-ious80": R(47, 209, "Tubimatic IO-US 80 Electra with swivelling forming unit", False),
    "wt-tubimatic-io-diagram": R(43, 180, "Tubimatic IO — inner and outer tools form the tube end in one stroke", False),
    "wt-tubimatic-io-part": R(43, 177, "Double-flared tube end made with IO-tools", False),
    "wt-tubimatic-io160": R(49, 224, "Wecotech Tubimatic IO 160 inner / outer tool end former for tube to Ø160 mm"),
    "wt-tubimatic-io160-electra": R(51, 229, "Tubimatic IO 160 Electra — servo-electric version", False),
    "wt-tubimatic-ious160": R(53, 250, "Tubimatic IO-US 160 Electra with swivelling forming unit", False),
    "wt-tubimatic-io160-diagram": R(49, 221, "Tubimatic IO 160 — inner / outer forming of a bent tube end", False),
    "wt-tubimatic-io160-part": R(49, 215, "Bent tube with calibrated end from the Tubimatic IO 160", False),
    # Weco line
    "wt-tubex-io-s": R(55, 262, "Wecotech Tubex IO-S combined inner / outer tube end former"),
    "wt-tubex-io-s-guard": R(55, 265, "Tubex IO-S — optional safety guard with light curtain", False),
    "wt-tubex-io-s-diagram": R(55, 266, "Tubex IO-S — inner mandrel and radial outer jaws around the tube", False),
    "wt-tubex-io-s-part": R(55, 257, "Beaded and flanged tube end made on the Tubex IO-S", False),
    "wt-wecomatic-200": R(57, 280, "Wecotech Wecomatic IO-S 200 CNC radial forming machine with light-curtain guard"),
    "wt-wecomatic-200-side": R(57, 283, "Wecomatic IO-S — version operated from the side", False),
    "wt-wecomatic-200-part": R(57, 274, "Multi-step formed exhaust tube end made on the Wecomatic", False),
    "wt-wecomatic-speed": R(59, 291, "Wecotech Wecomatic IO-S Speed CNC radial forming machine"),
    "wt-wecomatic-highspeed": R(61, 309, "Wecomatic IO-S High Speed with three hydraulic pumps", False),
    "wt-wecomatic-400": R(59, 298, "Wecomatic IO-S variant 400 for tube to Ø400 mm", False),
    "wt-wecomatic-diagram": R(59, 292, "Wecomatic IO-S — inner tool, outer top jaws and expansion mandrel", False),
    "wt-wecomatic-part": R(59, 286, "Beaded tube end made on the Wecomatic IO-S", False),
    "wt-flanging-cell": R(63, 320, "Wecotech flanging cell with rotating head for bellows and T-pieces"),
    "wt-flanging-cell-bellows": R(63, 319, "Bellows flanged directly onto the flange in the flanging cell", False),
    "wt-flanging-cell-step": R(63, 315, "Flanging cell — the part is held by eight hydraulic clamps while the head rolls the flange", False),
    # cutting and deburring
    "wt-tubecut": R(21, 69, "Wecotech Tubecut IO-S 160 Electra tube shearing cutter"),
    "wt-tubecut-notable": R(21, 70, "Tubecut IO-S 160 — version without the supporting table", False),
    "wt-tubecut-diagram": R(21, 67, "Tubecut IO-S — the tube is clamped and sheared between inner and outer tools", False),
    "wt-tubecut-part": R(21, 64, "Burr-free sheared copper elbows from the Tubecut", False),
    "wt-tubeshear": R(23, 77, "Wecotech Tubeshear with the height-adjustable working table"),
    "wt-tubeshear-process": R(23, 75, "Tubeshear — scoring knife and chopping knife", False),
    "wt-tubeshear-part": R(23, 73, "Bent tube cut on the Tubeshear", False),
    "wt-rotobrush": R(25, 79, "Wecotech Rotobrush tube end deburring machine"),
    "wt-rotobrush-head": R(25, 83, "Rotobrush — wire brush head with rotating frame", False),
    "wt-rotobrush-part": R(25, 81, "Deburred tube end from the Rotobrush", False),
}


def export(keys=None):
    os.makedirs(OUT, exist_ok=True)
    for k in keys or PHOTOS:
        p = PHOTOS[k]
        shutil.copy(SRC + p["src"], os.path.join(OUT, k + ".jpg"))
    print(f"wecotech photos: {len(keys or PHOTOS)} copied to {OUT}")


if __name__ == "__main__":
    export(sys.argv[1:] or None)
