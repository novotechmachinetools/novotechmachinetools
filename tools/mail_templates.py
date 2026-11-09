#!/usr/bin/env python3
"""The e-mails of the quote form: writes src/root/quote-mail.php, which quote.php reads.  Edit the designs here and run this
file again; quote-mail.php is never edited by hand.

  * the notification to the sales inbox: HTML with a plain-text twin, the customer's files attached (the owner, Nov 9 2026:
    the web-form inquiries should arrive as HTML, not plain text)
  * the automatic reply to the customer, from info@ (the owner, Nov 9 2026: "we have received your request, our sales
    specialist will contact you as soon as possible", with his e-mail signature and the logo on top).  Of the three drafts he
    chose the layout of B (dark band) with the words of A, plus the line of C inviting drawings and photos by reply.
    quote.php sends it when $AUTOREPLY is true.

The templates hold {{PLACEHOLDERS}}; quote.php fills them with escaped values in one pass (strtr), so a value can never bring in
another placeholder.  The customer's own message is never repeated in the automatic reply, so nobody can use the form to send
a third party a text of their choosing.  The logo and the signature GIF are served from the site (src/img/email/).

    python3 tools/mail_templates.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "root", "quote-mail.php")
IMG = "https://novotechmachinetools.com/img/email/"
LOGO, GIF = IMG + "novotech-logo-600.png", IMG + "novotech-signature.gif"
SITE = "https://novotechmachinetools.com"
VIDEO = "https://www.youtube.com/watch?v=ZGo_n6-2_Qc&amp;t=3s"
PHONE, TEL = "+1 647 526 5510", "tel:+16475265510"
HOURS = "Monday to Friday, 9:00 – 17:00 Eastern"

ORANGE, ORANGE_TXT, INK, MUTED, BG, LINE = "#F28A1F", "#B85C00", "#2D2E30", "#5A5D62", "#F2F3F5", "#E2E0DC"
FONT = "Arial,Helvetica,sans-serif"


def T(k):
    """a placeholder quote.php fills"""
    return "{{" + k + "}}"


def signature(top=24):
    a = f"color:{ORANGE_TXT};text-decoration:none;"
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:{top}px;">
<tr><td style="padding:0 0 12px 0;"><img src="{GIF}" width="250" height="84" alt="NovoTech Machine Tools Inc." style="display:block;border:0;outline:none;"></td></tr>
<tr><td style="font-family:{FONT};font-size:14px;line-height:22px;color:{INK};">
<a href="{SITE}" style="{a}">www.NovoTechMachineTools.com</a><br>
<a href="mailto:info@NovoTechMachineTools.com" style="{a}">info@NovoTechMachineTools.com</a><br>
1365 Mid-Way Blvd 26, Mississauga<br>Ontario L5T 2J5, Canada<br>
Tel: <a href="{TEL}" style="color:{INK};text-decoration:none;">{PHONE}</a><br>
<a href="{VIDEO}" style="{a}">Our corporate video</a></td></tr></table>'''


def shell(inner, pre, bg="#FFFFFF"):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>NovoTech Machine Tools</title></head>
<body style="margin:0;padding:0;background:{bg};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{pre}</div>
{inner}
</body></html>'''


def button(href, label, solid=True):
    """a button that wraps under the one before it on a narrow screen (tables aligned left)"""
    if solid:
        td = f'<td style="border-radius:4px;background:{ORANGE};">'
        a = f"display:inline-block;padding:12px 22px;font-family:{FONT};font-size:15px;font-weight:bold;color:#1F1F1F;text-decoration:none;border-radius:4px;"
    else:
        td = f'<td style="border-radius:4px;border:2px solid {ORANGE};">'
        a = f"display:inline-block;padding:10px 20px;font-family:{FONT};font-size:15px;font-weight:bold;color:{INK};text-decoration:none;"
    return (f'<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 12px 12px 0;"><tr>'
            f'{td}<a href="{href}" style="{a}">{label}</a></td></tr></table>')


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


# ---------------------------------------------------------------------------------------------- the automatic reply
def auto_reply():
    inner = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#E9EAEC;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;">
<tr><td style="padding:22px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="{LOGO}" width="190" alt="NovoTech Machine Tools Inc." style="display:block;width:190px;height:auto;border:0;"></td>
<td align="right" style="font-family:{FONT};font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:{ORANGE_TXT};padding-left:10px;">Request received</td>
</tr></table></td></tr>
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
{button(SITE + "/products", "Browse our machines")}{button(VIDEO, "Watch our video", False)}{CLEAR}
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

Best regards,
The sales team
NovoTech Machine Tools Inc.

www.NovoTechMachineTools.com
info@NovoTechMachineTools.com
1365 Mid-Way Blvd 26, Mississauga
Ontario L5T 2J5, Canada
Tel: {PHONE}
Our corporate video: {VIDEO.replace("&amp;", "&")}
"""


# ---------------------------------------------------------------------------------------------- the notification to the sales inbox
def notification():
    inner = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{BG};">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:640px;background:#FFFFFF;border:1px solid {LINE};">
<tr><td style="padding:18px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="{LOGO}" width="170" alt="NovoTech Machine Tools" style="display:block;width:170px;height:auto;border:0;"></td>
<td align="right" style="font-family:{FONT};font-size:12px;line-height:17px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:{ORANGE_TXT};padding-left:10px;">New request<br>from the website</td>
</tr></table></td></tr>
<tr><td style="height:4px;line-height:4px;font-size:0;background:{ORANGE};">&nbsp;</td></tr>
<tr><td style="padding:24px 24px 6px 24px;">
<h1 style="margin:0 0 4px 0;font-family:{FONT};font-size:22px;line-height:28px;color:{INK};">{T("TITLE")}</h1>
{T("MACHINE")}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;border-top:1px solid {LINE};">{T("ROWS")}</table>
{T("MESSAGE")}
{T("FILES")}
<div style="height:20px;line-height:20px;font-size:0;">&nbsp;</div>
{T("BUTTONS")}{CLEAR}
</td></tr>
<tr><td style="padding:14px 24px 20px 24px;border-top:1px solid {LINE};font-family:{FONT};font-size:12px;line-height:18px;color:{MUTED};word-break:break-word;">{T("FOOTER")}</td></tr>
</table></td></tr></table>'''
    return shell(inner, T("PRE"), BG)


TEMPLATES = {
    "reply": auto_reply(), "text": TEXT,
    "summary_row": SUMMARY_ROW,
    "about": f' about <b style="color:#FFFFFF;">{T("T")}</b>',
    "notify": notification(),
    "notify_machine": f'<div style="font-family:{FONT};font-size:16px;line-height:22px;font-weight:bold;color:{ORANGE_TXT};">{T("T")}</div>',
    "notify_row": (f'<tr><td style="padding:9px 14px 9px 0;border-bottom:1px solid {LINE};font-family:{FONT};font-size:13px;color:{MUTED};'
                   f'white-space:nowrap;vertical-align:top;width:80px;">{T("K")}</td><td style="padding:9px 0;border-bottom:1px solid {LINE};'
                   f'font-family:{FONT};font-size:15px;line-height:21px;color:{INK};font-weight:bold;word-break:break-word;">{T("V")}</td></tr>'),
    "notify_message": (f'<div style="{LABEL}padding:22px 0 8px 0;">Message</div>'
                       f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{BG};border-left:4px solid {ORANGE};">'
                       f'<tr><td style="padding:14px 18px;font-family:{FONT};font-size:15px;line-height:23px;color:{INK};word-break:break-word;">{T("TEXT")}</td></tr></table>'),
    "notify_files": (f'<div style="{LABEL}padding:20px 0 6px 0;">Attached files ({T("N")})</div>'
                     f'<table role="presentation" cellpadding="0" cellspacing="0" border="0">{T("LIST")}</table>'),
    "notify_file": (f'<tr><td style="padding:3px 8px 3px 0;font-family:{FONT};font-size:12px;line-height:20px;color:{ORANGE};vertical-align:top;">&#9632;</td>'
                    f'<td style="padding:3px 0;font-family:{FONT};font-size:14px;line-height:20px;color:{INK};word-break:break-all;">{T("NAME")} '
                    f'<span style="color:{MUTED};">· {T("SIZE")}</span></td></tr>'),
    "muted": f'<span style="color:{MUTED};font-weight:normal;">{T("T")}</span>',
    "link": f'<a href="{T("HREF")}" style="color:{ORANGE_TXT};text-decoration:none;">{T("LABEL")}</a>',
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
           "function nt_mail_templates(): array",
           "{",
           "    $t = [];"]
    for k, v in TEMPLATES.items():
        assert "NTMAIL" not in v, k
        out += [f"    $t['{k}'] = <<<'NTMAIL'", v, "NTMAIL;"]
    out += ["    return $t;", "}", "", "return nt_mail_templates();", ""]
    return "\n".join(out)


if __name__ == "__main__":
    used = sorted({m for v in TEMPLATES.values() for m in re.findall(r"\{\{(\w+)\}\}", v)})
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(php())
    print(f"{os.path.relpath(OUT, ROOT)}: {len(TEMPLATES)} templates; placeholders {', '.join(used)}")
