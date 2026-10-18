"""Convert the old band-saw buying guide (WebSite X5 export → extracted markdown) into an HTML article fragment
for the new hub page, keeping the original anchors (ids) so existing Google links keep working.

    python3 -I tools/guide_convert.py
Writes content/articles/band-saw-guide.html and registers the guide images in tools/image_map.json (section "guide").
"""
import re, os, json, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/claude/novotech-src/extracted/band-saw.md"
IMG_SRC = "/home/claude/novotech-src/images-guide"
lines = open(SRC, encoding="utf-8").read().split("\n")
imap = json.load(open(os.path.join(ROOT, "tools", "image_map.json"), encoding="utf-8"))

# old → new internal links
LINK_MAP = [
    (r"bekamak-pivot-band-saw\.html#Manual-Double-Miter-Band-Saw-ARG-PLUS-FE", "manual-band-saws.html"),
    (r"bekamak-pivot-band-saw\.html#Semi-Automatic-mitering-Band-Saw-BMSY-DG-G-series", "semi-automatic-band-saws.html"),
    (r"bekamak-pivot-band-saw\.html#Fully-Automatic[^)\"]*", "automatic-band-saws.html"),
    (r"bekamak-pivot-band-saw\.html#dual-column[^)\"]*", "double-column-band-saws.html"),
    (r"bekamak-pivot-band-saw\.html#Dual-column[^)\"]*", "double-column-band-saws.html"),
    (r"bekamak-pivot-band-saw\.html(#[^)\"]*)?", "band-saw.html#band-saw-range"),
    (r"band-saw\.html#reques-a-quote", "#reques-a-quote"),
]
def fix_link(href):
    for pat, rep in LINK_MAP:
        if re.fullmatch(pat, href):
            return rep
    return href

def inline(text):
    text = html.escape(text, quote=False)
    def repl(m):
        label, href = m.group(1), m.group(2)
        if "youtube.com" in href or "youtu.be" in href:
            return label                      # keep the article readable: videos are embedded on the pages
        href = fix_link(html.unescape(href))
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)
    return text

out = []
i = 0
in_table = False
section_open = False
first_heading_done = False
def img_key(path):
    base = os.path.basename(path)
    key = "guide-" + re.sub(r"[^a-z0-9]+", "-", os.path.splitext(base)[0].lower()).strip("-")
    key = re.sub(r"-[a-z0-9]{8}$", "", key)  # X5 duplicate suffixes like _a462s2tu
    return key, base
skip_until_first_anchor = True
while i < len(lines):
    ln = lines[i].rstrip()
    if skip_until_first_anchor:
        if ln.startswith("<!-- anchor: What-is-a-band-saw-machine"):
            skip_until_first_anchor = False
        else:
            i += 1; continue
    if ln.startswith("<!-- anchor:"):
        aid = re.search(r"anchor:\s*([^ ]+)\s*-->", ln).group(1)
        if aid == "reques-a-quote":
            break
        # heading is the next non-empty line
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        heading = lines[j].strip() if j < len(lines) else aid
        if section_open:
            out.append("</section>")
        out.append(f'<section class="guide-section" id="{html.escape(aid, quote=True)}">')
        out.append(f"<h3>{inline(heading)}</h3>")
        section_open = True
        i = j + 1; continue
    if ln.startswith("[TABLE]"):
        rows = []
        i += 1
        while i < len(lines) and not lines[i].startswith("[/TABLE]"):
            if "|" in lines[i]:
                rows.append([c.strip() for c in lines[i].split("|")])
            i += 1
        if rows:
            head, body = rows[0], rows[1:]
            out.append('<div class="table-scroll" tabindex="0"><table class="spec-table spec-table-simple guide-table"><thead><tr>' + "".join(f"<th scope=\"col\">{inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
            for r in body:
                out.append("<tr>" + f"<th scope=\"row\">{inline(r[0])}</th>" + "".join(f"<td>{inline(c)}</td>" for c in r[1:]) + "</tr>")
            out.append("</tbody></table></div>")
        i += 1; continue
    m = re.match(r"\[IMAGE (\S+) alt=\"([^\"]*)\" (\d+)x(\d+)(?: link=(\S+))?\]", ln)
    if m:
        path, alt, w, h, link = m.groups()
        key, base = img_key(path)
        src = os.path.join(IMG_SRC, base)
        if not os.path.exists(src):
            alt_base = re.sub(r"_[a-z0-9]{8}(?=\.webp$)", "", base)
            src = os.path.join(IMG_SRC, alt_base)
        if os.path.exists(src):
            if key not in imap:
                imap[key] = {"src": src, "alt": alt.strip() or "Band saw", "section": "guide", "trim": False, "quality": 80}
            out.append(f'<figure class="guide-figure" data-img="{key}"></figure>')
        i += 1; continue
    if ln.startswith("[BUTTON"):
        i += 1; continue
    if ln.startswith("- "):
        items = []
        while i < len(lines) and lines[i].startswith("- "):
            items.append(inline(lines[i][2:].strip())); i += 1
        out.append("<ul>" + "".join(f"<li>{t}</li>" for t in items) + "</ul>")
        continue
    if ln.strip():
        txt = ln.strip()
        # short lines without a full stop = sub-headings
        if len(txt) < 70 and not txt.endswith((".", ":", "?")) and not txt.startswith("[") and not re.search(r"\]\(", txt):
            out.append(f"<h4>{inline(txt)}</h4>")
        elif len(txt) < 70 and txt.endswith(":") and not re.search(r"\]\(", txt):
            out.append(f"<h4>{inline(txt.rstrip(':'))}</h4>")
        else:
            out.append(f"<p>{inline(txt)}</p>")
    i += 1
if section_open:
    out.append("</section>")
open(os.path.join(ROOT, "content", "articles", "band-saw-guide.html"), "w", encoding="utf-8").write("\n".join(out))
json.dump(imap, open(os.path.join(ROOT, "tools", "image_map.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("sections:", sum(1 for o in out if o.startswith("<section")), "| figures:", sum(1 for o in out if o.startswith("<figure")), "| paragraphs:", sum(1 for o in out if o.startswith("<p>")))
