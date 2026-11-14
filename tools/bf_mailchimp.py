#!/usr/bin/env python3
"""The Black Friday 2026 campaign e-mail for Mailchimp — every machine of the sale WITHOUT prices (the owner, Nov 14 2026:
"put every machine of the price list in it, like the PDF, but without prices"). Prices only ever go out by e-mail from the
instant-quote form, so every machine leads there ("Get the Black Friday price"), to its own no-price PDF and to its card.

    python3 tools/bf_mailchimp.py OUT.html

Mailchimp sends no attachments, so the whole list as a PDF is a download button (files/black-friday/…In-Stock-Machines.pdf).
The pictures are the site's own (img/email/bf/, made by tools/bf_mail_list.py, and bf-hero.jpg, the banner): Mailchimp mail
links its pictures. Styles sit on the tags (Mailchimp inlines anything else anyway); one <style> stacks the columns on phones.
Mailchimp's merge tags give the preview text, the "view in browser" link, the unsubscribe link and the postal address that
every campaign must carry. Kept compact: Gmail cuts e-mails past 102 KB, and Mailchimp lengthens every link for its click
tracking, so each machine has four links (photo, price, PDF, video); its card on the page has the rest.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://novotechmachinetools.com/"
PAGE_SLUG = "black-friday-machinery-sale"
BF = SITE + PAGE_SLUG
ASK = BF + "#instant-quote"
CATALOGUE = SITE + "files/black-friday/NovoTech-Black-Friday-2026-In-Stock-Machines.pdf"
IMG = SITE + "img/email/bf/"
e = html.escape
FONT = "font-family:Arial,Helvetica,sans-serif;"
ORANGE, ORANGE_TXT, INK, CHAR, MUTED, LINE = "#F28A1F", "#B85C00", "#1F2022", "#2D2E30", "#5A5D62", "#D9DBDE"

page = json.load(open(os.path.join(ROOT, "content", "pages", PAGE_SLUG + ".json"), encoding="utf-8"))
built = open(os.path.join(ROOT, "dist", PAGE_SLUG + ".html"), encoding="utf-8").read()
OUT = sys.argv[1]


def links_of(mid):
    m = re.search(r'<article[^>]*id="stock-' + re.escape(mid) + r'"(.*?)</article>', built, re.S)
    if not m:
        raise SystemExit(f"machine {mid} is not on the built page — run build.py first")
    return {lab.strip(): (h if h.startswith("http") else SITE + h)
            for h, lab in re.findall(r'<li><a href="([^"]+)"[^>]*>([^<]+)</a></li>', m.group(1))}


def photo_url(key):
    path = os.path.join(ROOT, "src", "img", "email", "bf", f"{key}-m.jpg")
    if not os.path.exists(path):
        raise SystemExit(f"no e-mail photo {key}-m.jpg — run tools/bf_mail_list.py first")
    return f"{IMG}{key}-m.jpg"


def button(href, label, solid=True):
    bg, edge, fg = (ORANGE, ORANGE, INK) if solid else ("#FFFFFF", "#FFFFFF", INK)
    return (f'<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 12px 12px 0;"><tr>'
            f'<td align="center" bgcolor="{bg}" style="background:{bg};border:2px solid {edge};border-radius:3px;padding:13px 22px;">'
            f'<a href="{href}" style="{FONT}font-size:17px;line-height:20px;font-weight:bold;color:{fg};text-decoration:none;">{label}</a>'
            f'</td></tr></table>')


def item(it):
    L = links_of(it["id"])
    card = f"{BF}#stock-{it['id']}"
    status = (f'<b style="color:#8A4A0E;">Back order &middot; about {it.get("lead", 90)} days</b>' if it.get("status") == "back"
              else '<b style="color:#17663A;">&#9679; In stock in Mississauga, ON</b>')
    sub = f'<b style="background:{CHAR};color:#FFFFFF;padding:2px 7px;">{e(it["sub"])}</b> ' if it.get("sub") else ""
    body = []
    if it.get("capacity"):
        body.append(f'<div style="padding:0 0 4px;font-size:15px;line-height:20px;font-weight:bold;color:{INK};">'
                    f'<span style="display:block;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:#8A4A0E;">Capacity</span>'
                    f'{e(it["capacity"])}</div>')
    if it.get("caps"):
        body.append('<div style="padding:2px 0 6px;font-size:12px;line-height:18px;color:#3B3D40;">'
                    + "<br>".join(f'{e(a)}: <b>{e(b)}</b>' for a, b in it["caps"]) + "</div>")
    if it.get("about"):
        body.append(f'<div style="padding:2px 0 6px;font-size:13px;line-height:19px;color:#3B3D40;">{e(it["about"])}</div>')
    for k in it.get("key") or []:
        body.append(f'<div style="background:#FFF3E6;border-left:3px solid {ORANGE};padding:4px 8px;margin:2px 0 4px;'
                    f'font-size:13px;line-height:18px;font-weight:bold;">{e(k)}</div>')
    feats = (it.get("features") or [])[:7]   # the first seven, as the card on the page shows them
    if feats:
        body.append('<div style="padding:4px 0;font-size:13px;line-height:19px;">'
                    + "<br>".join(f'■ {e(f)}' for f in feats) + "</div>")
    if it.get("optional"):
        body.append(f'<div style="padding:2px 0 4px;font-size:13px;line-height:18px;"><b>Optional:</b> {e("; ".join(it["optional"]))}</div>')
    if it.get("badges"):
        body.append(f'<div style="padding:2px 0 8px;font-size:12px;line-height:18px;color:{MUTED};">'
                    + " &middot; ".join(e(b) for b in it["badges"]) + "</div>")
    links = [f'<a href="{SITE}{it["sheet"]}" style="color:{INK};font-weight:bold;">Machine PDF</a>']
    if it.get("videos"):
        links.append(f'<a href="https://youtu.be/{it["videos"][0]}" style="color:{INK};font-weight:bold;">Video</a>')
    body.append(
        f'<table cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="{ORANGE}" style="padding:9px 14px;">'
        f'<a href="{BF}?m={it["id"]}#instant-quote" style="{FONT}font-size:14px;font-weight:bold;color:{INK};text-decoration:none;">'
        f'Get the Black Friday price &rarr;</a></td></tr></table>'
        f'<div style="padding:8px 0 0;font-size:13px;line-height:20px;">' + " &middot; ".join(links) + "</div>")
    return (f'<tr><td style="{FONT}padding:16px 0 18px;border-bottom:1px dashed {LINE};font-size:14px;line-height:20px;color:{CHAR};">'
            f'<div style="font-size:20px;line-height:25px;font-weight:bold;color:{INK};">{e(it["title"])}</div>'
            f'<div style="padding:6px 0 0;font-size:11px;line-height:22px;letter-spacing:.3px;">{sub}{status}</div>'
            f'<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td class="c1" width="200" valign="top" style="padding:12px 16px 0 0;">'
            f'<a href="{card}"><img class="mi" src="{photo_url(it["images"][0][0])}" width="200" height="150" alt="{e(it["title"])}" '
            f'style="display:block;width:200px;height:150px;border:1px solid {LINE};"></a></td>'
            f'<td class="c2" valign="top" style="{FONT}padding:12px 0 0;font-size:14px;line-height:20px;color:{CHAR};">{"".join(body)}</td>'
            f'</tr></table></td></tr>')


def cat_row(title):
    return (f'<tr><td style="{FONT}padding:22px 0 6px;border-bottom:3px solid {ORANGE};font-size:13px;line-height:18px;font-weight:bold;'
            f'letter-spacing:1px;text-transform:uppercase;color:{ORANGE_TXT};">{e(title)}</td></tr>')


def offer(title, text):
    return (f'<td class="o2" width="50%" valign="top" style="{FONT}padding:6px;">'
            f'<div style="border-top:4px solid {ORANGE};background:#FFFFFF;padding:10px 12px;">'
            f'<div style="font-size:16px;line-height:20px;font-weight:bold;color:{INK};">{title}</div>'
            f'<div style="font-size:13px;line-height:18px;color:{MUTED};padding-top:2px;">{text}</div></div></td>')


rows = []
for c in page["stock_cats"]:
    xs = [it for it in page["stock"] if it["cat"] == c["id"]]
    if xs:
        rows.append(cat_row(c["title"]))
        rows += [item(it) for it in xs]
n = len(page["stock"])

doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>*|MC:SUBJECT|*</title>
<style>@media only screen and (max-width:600px){{.c1,.c2,.o2{{display:block!important;width:100%!important}}.c1{{padding:12px 0 0!important}}.mi{{width:100%!important;height:auto!important}}}}</style>
</head>
<body style="margin:0;padding:0;background:#E9EAEC;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">*|MC_PREVIEW_TEXT|*</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#E9EAEC;"><tr><td align="center" style="padding:20px 10px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;">
<tr><td style="padding:16px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><a href="{SITE}"><img src="{SITE}img/email/novotech-logo.png" width="170" alt="NovoTech Machine Tools Inc." style="display:block;width:170px;height:auto;border:0;"></a></td>
<td align="right" style="{FONT}font-size:12px;line-height:16px;color:{MUTED};"><a href="*|ARCHIVE|*" style="color:{MUTED};">View in your browser</a></td>
</tr></table></td></tr>
<tr><td><a href="{BF}"><img src="{IMG}bf-hero.jpg" width="600" alt="Black Friday: in-stock machines on sale in Mississauga, ON, now until Dec 4, 2026" style="display:block;width:100%;max-width:600px;height:auto;border:0;"></a></td></tr>
<tr><td style="background:{CHAR};padding:24px 24px 14px 24px;">
<h1 style="margin:0;{FONT}font-size:26px;line-height:32px;font-weight:bold;color:#FFFFFF;">{n} machines in stock, at Black Friday prices</h1>
<div style="width:64px;height:4px;line-height:4px;font-size:0;background:{ORANGE};margin-top:12px;">&nbsp;</div>
<p style="margin:0;padding:12px 0 16px;{FONT}font-size:16px;line-height:24px;color:#E1E2E4;">Rebar benders and cutters, band saws, plate rollers, angle rolls, CNC press brakes and more, in our Mississauga, ON warehouse and ready to ship. Ask for the price list and we email it to you in minutes. In-stock machines are first come, first served.</p>
{button(ASK, "Get the Black Friday prices")}{button(CATALOGUE, "Download the PDF catalogue", False)}
<div style="clear:both;height:0;line-height:0;font-size:0;">&nbsp;</div></td></tr>
<tr><td style="background:#F2F3F5;padding:12px 18px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>{offer("Black Friday prices on stock", "Every machine below, while quantities last")}{offer("5% off factory orders", "Confirm by Dec 4: only 10% down, balance on delivery")}</tr>
<tr>{offer("0% down financing", "36-month lease, on approved credit")}{offer("100% first-year write-off*", "Eligible manufacturing equipment")}</tr>
</table></td></tr>
<tr><td style="padding:4px 24px 10px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{"".join(rows)}
</table></td></tr>
<tr><td style="padding:10px 24px 24px 24px;{FONT}font-size:15px;line-height:23px;color:{CHAR};">
<p style="margin:0 0 14px 0;">Need a different size or model? Order any machine from the factory by December 4 and take 5% off, with only 10% down and the balance on delivery. Questions? Reply to this email or call <a href="tel:+16475265510" style="color:{ORANGE_TXT};font-weight:bold;text-decoration:none;">+1 647 526 5510</a>.</p>
{button(ASK, "Get the Black Friday prices")}<div style="clear:both;height:0;line-height:0;font-size:0;">&nbsp;</div>
<p style="margin:10px 0 0 0;font-size:13px;line-height:19px;color:{MUTED};">NovoTech Machine Tools Inc. &middot; 1365 Mid-Way Blvd, Unit 26, Mississauga, ON L5T 2J5 &middot; Mon&ndash;Fri 9:00&ndash;17:00 ET</p>
</td></tr>
<tr><td style="padding:0 24px 20px 24px;{FONT}font-size:12px;line-height:18px;color:{MUTED};">Offer ends Friday, December 4, 2026, 11:59 pm Eastern; in-stock machines while quantities last. Prices in Canadian dollars, plus applicable taxes. *Canadian businesses can deduct 100% of the cost of eligible manufacturing and processing equipment in the tax year it becomes available for use, and eligible Ontario corporations can add the 15% Ontario Made Manufacturing Investment Tax Credit. General information, not tax advice: ask your accountant whether your business qualifies.</td></tr>
<tr><td style="background:{CHAR};padding:18px 24px;{FONT}font-size:12px;line-height:18px;color:#B4B6BA;">
*|LIST:DESCRIPTION|*<br><br>
<a href="*|UNSUB|*" style="color:#FFFFFF;">Unsubscribe</a> &middot; <a href="*|UPDATE_PROFILE|*" style="color:#FFFFFF;">Update your preferences</a><br><br>
*|HTML:LIST_ADDRESS_HTML|*
*|IF:REWARDS|* *|HTML:REWARDS|* *|END:IF|*
</td></tr>
</table></td></tr></table>
</body></html>
'''
open(OUT, "w", encoding="utf-8").write(doc)
links = len(re.findall(r'href="', doc))
print(f"{OUT}: {n} machines, {len(doc.encode()) / 1024:.0f} KB HTML, {links} links "
      f"(about {(len(doc.encode()) + links * 110) / 1024:.0f} KB once Mailchimp tracks the links)")
