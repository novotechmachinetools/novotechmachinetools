#!/usr/bin/env python3
"""The e-mails of the quote form: writes src/root/quote-mail.php, which quote.php reads.  Edit the designs here and run this
file again; quote-mail.php is never edited by hand.

  * the notification to the sales inbox: HTML with a plain-text twin, the customer's files attached (the owner, Nov 9 2026:
    the web-form inquiries should arrive as HTML, not plain text, in the look of the automatic reply)
  * the automatic reply to the customer, from info@ (the owner, Nov 9 2026: "we have received your request, our sales
    specialist will contact you as soon as possible", with his e-mail signature and the logo on top).  Of the three drafts he
    chose the layout of B (dark band) with the words of A, plus the line of C inviting drawings and photos by reply.
    Its first button leads back to the page the request came from, named after it ("Browse band saws").
    quote.php sends it when $AUTOREPLY is true.

The pictures (logo, the owner's animated signature GIF, the social icons) travel inside the e-mails: Outlook does not download
pictures from the internet by itself (the owner, Nov 9 2026: "the logo does not open").  The templates name them {{LOGO}},
{{SIG}} and {{ICON_…}}; quote.php puts in cid: references to the attached copies (src/img/email/, listed in IMAGES), or the
picture's address on the site if the file is missing.  The buttons are tables padded in the cell, which Outlook draws at full
size, in the look of the site's buttons.

The other {{PLACEHOLDERS}} are filled by quote.php with escaped values in one pass (strtr), so a value can never bring in
another placeholder.  The customer's own message is never repeated in the automatic reply, so nobody can use the form to send
a third party a text of their choosing.

    python3 tools/mail_templates.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "root", "quote-mail.php")
SITE = "https://novotechmachinetools.com"
VIDEO = "https://www.youtube.com/watch?v=ZGo_n6-2_Qc&amp;t=3s"
PHONE, TEL = "+1 647 526 5510", "tel:+16475265510"
HOURS = "Monday to Friday, 9:00 – 17:00 Eastern"

ORANGE, ORANGE_TXT, INK, MUTED, BG, LINE = "#F28A1F", "#B85C00", "#2D2E30", "#5A5D62", "#F2F3F5", "#E2E0DC"
BTN_INK = "#1F2022"                                        # the site's --ink, the text of its orange buttons
FONT = "Arial,Helvetica,sans-serif"
BTN_FONT = "'Arial Narrow',Arial,Helvetica,sans-serif"     # the site's buttons are set in a condensed face

# the signature's social row (the owner, Nov 9 2026, in this order), addresses from content/site.json; icons rendered from the
# site's own icon set (Font Awesome Free, CC BY 4.0) as 56 px PNGs shown at 28 px
SOCIAL = ["YouTube", "Facebook", "Instagram", "TikTok", "WhatsApp", "LinkedIn"]
_site = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
_urls = {s["name"]: s["url"] for s in _site.get("social", []) + _site.get("social_more", []) if s.get("url")}
SOCIAL_LINKS = [(n, _urls[n]) for n in SOCIAL]

# placeholder -> (file under the site root, type); quote.php attaches the ones a template names
IMAGES = {"LOGO": ("img/email/novotech-logo.png", "image/png"), "SIG": ("img/email/novotech-signature.gif", "image/gif")}
IMAGES.update({"ICON_" + n.upper(): (f"img/email/icon-{n.lower()}.png", "image/png") for n in SOCIAL})


def T(k):
    """a placeholder quote.php fills"""
    return "{{" + k + "}}"


def signature(top=24):
    a = f"color:{ORANGE_TXT};text-decoration:none;"
    icons = "".join(f'<td style="padding:0 8px 0 0;"><a href="{u}" style="text-decoration:none;"><img src="{T("ICON_" + n.upper())}" width="28" height="28" '
                    f'alt="{n}" title="NovoTech on {n}" style="display:block;border:0;outline:none;"></a></td>' for n, u in SOCIAL_LINKS)
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:{top}px;">
<tr><td style="padding:0 0 10px 0;"><img src="{T("SIG")}" width="260" height="117" alt="NovoTech Machine Tools Inc." style="display:block;border:0;outline:none;"></td></tr>
<tr><td style="font-family:{FONT};font-size:14px;line-height:22px;color:{INK};">
<a href="{SITE}" style="{a}">www.NovoTechMachineTools.com</a><br>
<a href="mailto:info@NovoTechMachineTools.com" style="{a}">info@NovoTechMachineTools.com</a><br>
1365 Mid-Way Blvd 26, Mississauga<br>Ontario L5T 2J5, Canada<br>
Tel: <a href="{TEL}" style="color:{INK};text-decoration:none;">{PHONE}</a></td></tr>
<tr><td style="padding:12px 0 0 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>{icons}</tr></table></td></tr></table>'''


def shell(inner, pre, bg="#FFFFFF"):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>NovoTech Machine Tools</title></head>
<body style="margin:0;padding:0;background:{bg};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{pre}</div>
{inner}
</body></html>'''


def button(href, label, solid=True):
    """the site's buttons: orange with dark text, or white with a charcoal frame; the padding sits in the cell so Outlook draws the
    full button, and tables aligned left let the second wrap under the first on a narrow screen"""
    bg, edge, fg = (ORANGE, ORANGE, BTN_INK) if solid else ("#FFFFFF", INK, INK)
    return (f'<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 14px 14px 0;"><tr>'
            f'<td align="center" bgcolor="{bg}" style="background:{bg};border:2px solid {edge};border-radius:3px;padding:14px 30px;">'
            f'<a href="{href}" style="display:inline-block;font-family:{BTN_FONT};font-size:20px;line-height:24px;font-weight:bold;color:{fg};text-decoration:none;">'
            f'<span style="color:{fg};">{label}</span></a></td></tr></table>')


CLEAR = '<div style="clear:both;height:0;line-height:0;font-size:0;">&nbsp;</div>'
LABEL = f"font-family:{FONT};font-size:12px;letter-spacing:1px;text-transform:uppercase;color:{MUTED};"
SUMMARY_ROW = (f'<tr><td style="padding:6px 12px 6px 0;font-family:{FONT};font-size:14px;color:{MUTED};white-space:nowrap;vertical-align:top;">{T("K")}</td>'
               f'<td style="padding:6px 0;font-family:{FONT};font-size:14px;line-height:20px;color:{INK};font-weight:bold;">{T("V")}</td></tr>')


def summary(title="Your request"):
    return f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{BG};border-left:4px solid {ORANGE};">
<tr><td style="padding:14px 18px;">
<div style="{LABEL}padding-bottom:6px;">{title}</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0">{T("ROWS")}</table>
</td></tr></table>'''


def P(t, extra=""):
    return f'<p style="margin:0 0 16px 0;font-family:{FONT};font-size:16px;line-height:25px;color:{INK};{extra}">{t}</p>'


REGARDS = "Best regards,<br><b>The sales team</b><br>NovoTech Machine Tools Inc."
CALL = f'<a href="{TEL}" style="color:{ORANGE_TXT};font-weight:bold;text-decoration:none;">{PHONE}</a>'
WHY = "You received this email because you sent a request on NovoTechMachineTools.com."
DRAWINGS = "If you would like to add drawings, photos of your parts or anything else, simply reply to this email."
SOONER = f"Need an answer sooner? Call us at {CALL}, {HOURS.replace(' – ', '&nbsp;–&nbsp;')}."   # the hours never split over two lines


def header(label):
    return f'''<tr><td style="padding:22px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="{T("LOGO")}" width="190" height="65" alt="NovoTech Machine Tools Inc." style="display:block;width:190px;height:auto;border:0;"></td>
<td align="right" style="font-family:{FONT};font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:{ORANGE_TXT};padding-left:10px;">{label}</td>
</tr></table></td></tr>'''


# ---------------------------------------------------------------------------------------------- the automatic reply
def auto_reply():
    inner = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#E9EAEC;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;">
{header("Request received")}
<tr><td style="background:{INK};padding:30px 24px 28px 24px;">
<h1 style="margin:0;font-family:{FONT};font-size:28px;line-height:34px;font-weight:bold;color:#FFFFFF;">Thank you{T("COMMA_NAME")}!</h1>
<div style="width:64px;height:4px;line-height:4px;font-size:0;background:{ORANGE};margin-top:14px;">&nbsp;</div>
<p style="margin:0;padding-top:14px;font-family:{FONT};font-size:16px;line-height:25px;color:#E1E2E4;">We have received your request{T("ABOUT")}. One of our sales specialists will contact you as soon as possible.</p>
</td></tr>
<tr><td style="padding:28px 24px 6px 24px;">
{summary()}
<div style="height:22px;line-height:22px;font-size:0;">&nbsp;</div>
{P(DRAWINGS)}
{P(SOONER)}
{button(T("BROWSE_URL"), T("BROWSE_LABEL"))}{button(VIDEO, "Watch our video", False)}{CLEAR}
</td></tr>
<tr><td style="padding:16px 24px 30px 24px;">
{P(REGARDS, "margin-bottom:0;")}
{signature(18)}
</td></tr>
<tr><td style="background:{INK};padding:16px 24px;font-family:{FONT};font-size:12px;line-height:18px;color:#B4B6BA;">{WHY}</td></tr>
</table></td></tr></table>'''
    return shell(inner, "We have received your request. A NovoTech sales specialist will contact you as soon as possible.", "#E9EAEC")


# its plain-text twin (for mail programs that do not show HTML, and for spam filters)
TEXT = f"""Thank you{T("COMMA_NAME")}!

We have received your request{T("ABOUT")}. One of our sales specialists will contact you as soon as possible.

Your request
{T("ROWS")}
{DRAWINGS}

Need an answer sooner? Call us at {PHONE}, {HOURS}.

{T("BROWSE_LABEL")}: {T("BROWSE_URL")}

Best regards,
The sales team
NovoTech Machine Tools Inc.

www.NovoTechMachineTools.com
info@NovoTechMachineTools.com
1365 Mid-Way Blvd 26, Mississauga
Ontario L5T 2J5, Canada
Tel: {PHONE}

""" + "\n".join(f"{n}: {u}" for n, u in SOCIAL_LINKS) + "\n"


# ---------------------------------------------------------------------------------------------- the notification to the sales inbox
def notification():
    """{{LABEL}} at the top right: "New quote request" from the form, "Contact from the AI chat" from ask.php.
    The look of the automatic reply (the owner, Nov 9 2026: "make the e-mail I receive look like this one"): the customer's
    name in the dark band, the machine under it, then boxes for the details, the message and the files.  White around the card,
    not grey: Outlook gives a reply the background of the e-mail replied to, and the owner's signature is on white (Nov 9 2026)"""
    inner = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;border:1px solid {LINE};">
{header(T("LABEL"))}
<tr><td style="background:{INK};padding:30px 24px 28px 24px;">
<h1 style="margin:0;font-family:{FONT};font-size:28px;line-height:34px;font-weight:bold;color:#FFFFFF;word-break:break-word;">{T("NAME")}</h1>
{T("COMPANY")}
<div style="width:64px;height:4px;line-height:4px;font-size:0;background:{ORANGE};margin-top:14px;">&nbsp;</div>
<p style="margin:0;padding-top:14px;font-family:{FONT};font-size:16px;line-height:25px;color:#E1E2E4;">{T("ABOUT")}</p>
</td></tr>
<tr><td style="padding:28px 24px 6px 24px;">
{T("DETAILS")}
{T("MESSAGE")}
{T("FILES")}
<div style="height:6px;line-height:6px;font-size:0;">&nbsp;</div>
{T("BUTTONS")}{CLEAR}
</td></tr>
<tr><td style="padding:0 24px 18px 24px;font-size:0;line-height:0;">&nbsp;</td></tr>
<tr><td style="background:{INK};padding:16px 24px;font-family:{FONT};font-size:12px;line-height:18px;color:#B4B6BA;word-break:break-word;">{T("FOOTER")}</td></tr>
</table></td></tr></table>'''
    return shell(inner, T("PRE"), "#FFFFFF")


TEMPLATES = {
    "reply": auto_reply(), "text": TEXT,
    "summary_row": SUMMARY_ROW,
    "about": f' about <b style="color:#FFFFFF;">{T("T")}</b>',
    "notify": notification(),
    "notify_company": f'<div style="padding-top:4px;font-family:{FONT};font-size:17px;line-height:24px;color:#C9CBCF;word-break:break-word;">{T("T")}</div>',
    "notify_about": f'About <b style="color:#FFFFFF;">{T("T")}</b>',
    "notify_not_sure": 'Not sure which machine fits — please advise',
    "notify_no_machine": '<span style="color:#B4B6BA;">No machine chosen</span>',
    # a grey box with an orange edge, like "Your request" in the automatic reply
    "box": (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{BG};border-left:4px solid {ORANGE};">'
            f'<tr><td style="padding:14px 18px;"><div style="{LABEL}padding-bottom:8px;">{T("TITLE")}</div>{T("BODY")}</td></tr></table>'
            '<div style="height:16px;line-height:16px;font-size:0;">&nbsp;</div>'),
    "rows_table": f'<table role="presentation" cellpadding="0" cellspacing="0" border="0">{T("ROWS")}</table>',
    "text_block": f'<div style="font-family:{FONT};font-size:15px;line-height:23px;color:{INK};word-break:break-word;">{T("TEXT")}</div>',
    "files_table": f'<table role="presentation" cellpadding="0" cellspacing="0" border="0">{T("LIST")}</table>',
    "notify_file": (f'<tr><td style="padding:3px 8px 3px 0;font-family:{FONT};font-size:12px;line-height:20px;color:{ORANGE};vertical-align:top;">&#9632;</td>'
                    f'<td style="padding:3px 0;font-family:{FONT};font-size:14px;line-height:20px;color:{INK};word-break:break-all;">{T("NAME")} '
                    f'<span style="color:{MUTED};">· {T("SIZE")}</span></td></tr>'),
    "muted": f'<span style="color:{MUTED};font-weight:normal;">{T("T")}</span>',
    "link": f'<a href="{T("HREF")}" style="color:{ORANGE_TXT};text-decoration:none;">{T("LABEL")}</a>',
    "link_dark": f'<a href="{T("HREF")}" style="color:{ORANGE};text-decoration:none;">{T("LABEL")}</a>',
    "button": button(T("HREF"), T("LABEL")),
    "button_ghost": button(T("HREF"), T("LABEL"), False),
}


def php():
    out = ["<?php",
           "/**",
           " * The e-mails of the quote form, read by quote.php: the HTML notification to the sales inbox and the automatic reply to",
           " * the customer. Written by tools/mail_templates.py: edit the designs there and run it again.",
           " */",
           "if (!defined('NT_QUOTE')) { http_response_code(404); exit; }",
           "",
           "// the pictures the templates name: placeholder => [file under the site root, type]",
           "function nt_mail_images(): array",
           "{",
           "    return ["]
    out += [f"        '{k}' => ['{f}', '{t}']," for k, (f, t) in IMAGES.items()]
    out += ["    ];", "}", "",
            "function nt_mail_templates(): array",
            "{",
            "    $t = [];"]
    for k, v in TEMPLATES.items():
        assert "NTMAIL" not in v, k
        out += [f"    $t['{k}'] = <<<'NTMAIL'", v, "NTMAIL;"]
    out += ["    return $t;", "}", "", "return nt_mail_templates();", ""]
    return "\n".join(out)


if __name__ == "__main__":
    for k, (f, _) in IMAGES.items():
        assert os.path.isfile(os.path.join(ROOT, "src", f)), f"missing picture {f}"
    used = sorted({m for v in TEMPLATES.values() for m in re.findall(r"\{\{(\w+)\}\}", v)})
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(php())
    print(f"{os.path.relpath(OUT, ROOT)}: {len(TEMPLATES)} templates, {len(IMAGES)} pictures; placeholders {', '.join(used)}")
