"""the tool codes printed as block titles (Roboto Black / Bold Italic) through the catalogue"""
import re


def codes(doc):
    out = set()
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    t = s["text"].strip()
                    if "Italic" in s["font"] and ("Black" in s["font"] or "Bold" in s["font"]) and s["size"] >= 10:
                        out.update(re.findall(r"\d{4}", t))
    return frozenset(out)
