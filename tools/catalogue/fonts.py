"""The catalogue's fonts as files: Roboto and Roboto Slab in every weight the catalogue uses (tools/fonts/roboto), so that
text taken out of a line can be set again exactly as it was."""
import os
import re

import fitz

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", "roboto")
_CACHE = {}

STYLES = ["Thin", "ThinItalic", "Light", "LightItalic", "Regular", "Italic", "Medium", "MediumItalic", "Bold", "BoldItalic",
          "Black", "BlackItalic"]
SLAB = ["Light", "Regular", "Medium", "Bold", "ExtraBold"]


def ttf(pdf_font):
    """the font file for a PDF font name ('ABCDEF+Roboto-LightItalic', 'RobotoSlab-Regular', 'MyriadPro-Regular' …)"""
    name = re.sub(r"^[A-Z]{6}\+", "", pdf_font or "")
    if name.startswith("RobotoSlab-"):
        st = name.split("-", 1)[1]
        st = {"ExtraLight": "Light", "Thin": "Light", "Black": "ExtraBold", "SemiBold": "Medium"}.get(st, st)
        if st not in SLAB:
            st = "Regular"
        return os.path.join(DIR, f"RobotoSlab-{st}.ttf")
    if name.startswith("Roboto-"):
        st = name.split("-", 1)[1]
        if st not in STYLES:
            st = "Italic" if "Italic" in st else "Regular"
        return os.path.join(DIR, f"Roboto-{st}.ttf")
    italic = "Italic" in name or "Oblique" in name
    if "Bold" in name or "Black" in name:
        return os.path.join(DIR, "Roboto-BoldItalic.ttf" if italic else "Roboto-Bold.ttf")
    if "Light" in name:
        return os.path.join(DIR, "Roboto-LightItalic.ttf" if italic else "Roboto-Light.ttf")
    return os.path.join(DIR, "Roboto-Italic.ttf" if italic else "Roboto-Regular.ttf")


def font(path):
    if path not in _CACHE:
        _CACHE[path] = fitz.Font(fontfile=path)
    return _CACHE[path]


def alias(path):
    """a short resource name per font file, the same on every page"""
    return "nt" + os.path.splitext(os.path.basename(path))[0].replace("-", "")


SYMBOL = {"a": "α", "b": "β", "g": "γ", "d": "δ", "m": "μ", "p": "π", "W": "Ω", "f": "φ", "°": "°", "±": "±", "´": "′"}


def char_for(c, pdf_font):
    """the Unicode character a glyph stands for when set again in Roboto (Symbol's 'a' is an alpha)"""
    if "Symbol" in (pdf_font or ""):
        return SYMBOL.get(c, c)
    return c
