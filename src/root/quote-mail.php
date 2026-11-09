<?php
/**
 * The e-mails of the quote form, read by quote.php: the HTML notification to the sales inbox and the automatic reply to
 * the customer. Written by tools/mail_templates.py: edit the designs there and run it again.
 */
if (!defined('NT_QUOTE')) { http_response_code(404); exit; }

function nt_mail_templates(): array
{
    $t = [];
    $t['reply'] = <<<'NTMAIL'
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>NovoTech Machine Tools</title></head>
<body style="margin:0;padding:0;background:#E9EAEC;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">We have received your request. A NovoTech sales specialist will contact you as soon as possible.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#E9EAEC;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;">
<tr><td style="padding:22px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="https://novotechmachinetools.com/img/email/novotech-logo-600.png" width="190" alt="NovoTech Machine Tools Inc." style="display:block;width:190px;height:auto;border:0;"></td>
<td align="right" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#B85C00;padding-left:10px;">Request received</td>
</tr></table></td></tr>
<tr><td style="background:#2D2E30;padding:30px 24px 28px 24px;">
<h1 style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:28px;line-height:34px;font-weight:bold;color:#FFFFFF;">Thank you{{COMMA_NAME}}!</h1>
<div style="width:64px;height:4px;line-height:4px;font-size:0;background:#F28A1F;margin-top:14px;">&nbsp;</div>
<p style="margin:0;padding-top:14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#E1E2E4;">We have received your request{{ABOUT}}. One of our sales specialists will contact you as soon as possible.</p>
</td></tr>
<tr><td style="padding:28px 24px 6px 24px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F2F3F5;border-left:4px solid #F28A1F;">
<tr><td style="padding:14px 18px;">
<div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#5A5D62;padding-bottom:6px;">Your request</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0">{{ROWS}}</table>
</td></tr></table>
<div style="height:22px;line-height:22px;font-size:0;">&nbsp;</div>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#2D2E30;">If you would like to add drawings, photos of your parts or anything else, simply reply to this email.</p>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#2D2E30;">Need an answer sooner? Call us at <a href="tel:+16475265510" style="color:#B85C00;font-weight:bold;text-decoration:none;">+1 647 526 5510</a>, Monday to Friday, 9:00&nbsp;–&nbsp;17:00 Eastern.</p>
<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 12px 12px 0;"><tr><td style="border-radius:4px;background:#F28A1F;"><a href="{{BROWSE_URL}}" style="display:inline-block;padding:12px 22px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1F1F1F;text-decoration:none;border-radius:4px;">{{BROWSE_LABEL}}</a></td></tr></table><table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 12px 12px 0;"><tr><td style="border-radius:4px;border:2px solid #F28A1F;"><a href="https://www.youtube.com/watch?v=ZGo_n6-2_Qc&amp;t=3s" style="display:inline-block;padding:10px 20px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#2D2E30;text-decoration:none;">Watch our video</a></td></tr></table><div style="clear:both;height:0;line-height:0;font-size:0;">&nbsp;</div>
</td></tr>
<tr><td style="padding:16px 24px 30px 24px;">
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#2D2E30;margin-bottom:0;">Best regards,<br><b>The sales team</b><br>NovoTech Machine Tools Inc.</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px;">
<tr><td style="padding:0 0 12px 0;"><img src="https://novotechmachinetools.com/img/email/novotech-signature.gif" width="250" height="84" alt="NovoTech Machine Tools Inc." style="display:block;border:0;outline:none;"></td></tr>
<tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:22px;color:#2D2E30;">
<a href="https://novotechmachinetools.com" style="color:#B85C00;text-decoration:none;">www.NovoTechMachineTools.com</a><br>
<a href="mailto:info@NovoTechMachineTools.com" style="color:#B85C00;text-decoration:none;">info@NovoTechMachineTools.com</a><br>
1365 Mid-Way Blvd 26, Mississauga<br>Ontario L5T 2J5, Canada<br>
Tel: <a href="tel:+16475265510" style="color:#2D2E30;text-decoration:none;">+1 647 526 5510</a><br>
<a href="https://www.youtube.com/watch?v=ZGo_n6-2_Qc&amp;t=3s" style="color:#B85C00;text-decoration:none;">Our corporate video</a></td></tr></table>
</td></tr>
<tr><td style="background:#2D2E30;padding:16px 24px;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#B4B6BA;">You received this email because you sent a request on NovoTechMachineTools.com.</td></tr>
</table></td></tr></table>
</body></html>
NTMAIL;
    $t['text'] = <<<'NTMAIL'
Thank you{{COMMA_NAME}}!

We have received your request{{ABOUT}}. One of our sales specialists will contact you as soon as possible.

Your request
{{ROWS}}
If you would like to add drawings, photos of your parts or anything else, simply reply to this email.

Need an answer sooner? Call us at +1 647 526 5510, Monday to Friday, 9:00 – 17:00 Eastern.

{{BROWSE_LABEL}}: {{BROWSE_URL}}

Best regards,
The sales team
NovoTech Machine Tools Inc.

www.NovoTechMachineTools.com
info@NovoTechMachineTools.com
1365 Mid-Way Blvd 26, Mississauga
Ontario L5T 2J5, Canada
Tel: +1 647 526 5510
Our corporate video: https://www.youtube.com/watch?v=ZGo_n6-2_Qc&t=3s

NTMAIL;
    $t['summary_row'] = <<<'NTMAIL'
<tr><td style="padding:6px 12px 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#5A5D62;white-space:nowrap;vertical-align:top;">{{K}}</td><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;font-weight:bold;">{{V}}</td></tr>
NTMAIL;
    $t['about'] = <<<'NTMAIL'
 about <b style="color:#FFFFFF;">{{T}}</b>
NTMAIL;
    $t['notify'] = <<<'NTMAIL'
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>NovoTech Machine Tools</title></head>
<body style="margin:0;padding:0;background:#E9EAEC;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{{PRE}}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#E9EAEC;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;">
<tr><td style="padding:22px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="https://novotechmachinetools.com/img/email/novotech-logo-600.png" width="190" alt="NovoTech Machine Tools Inc." style="display:block;width:190px;height:auto;border:0;"></td>
<td align="right" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#B85C00;padding-left:10px;">New quote request</td>
</tr></table></td></tr>
<tr><td style="background:#2D2E30;padding:30px 24px 28px 24px;">
<h1 style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:28px;line-height:34px;font-weight:bold;color:#FFFFFF;word-break:break-word;">{{NAME}}</h1>
{{COMPANY}}
<div style="width:64px;height:4px;line-height:4px;font-size:0;background:#F28A1F;margin-top:14px;">&nbsp;</div>
<p style="margin:0;padding-top:14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#E1E2E4;">{{ABOUT}}</p>
</td></tr>
<tr><td style="padding:28px 24px 6px 24px;">
{{DETAILS}}
{{MESSAGE}}
{{FILES}}
<div style="height:6px;line-height:6px;font-size:0;">&nbsp;</div>
{{BUTTONS}}<div style="clear:both;height:0;line-height:0;font-size:0;">&nbsp;</div>
</td></tr>
<tr><td style="padding:0 24px 18px 24px;font-size:0;line-height:0;">&nbsp;</td></tr>
<tr><td style="background:#2D2E30;padding:16px 24px;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#B4B6BA;word-break:break-word;">{{FOOTER}}</td></tr>
</table></td></tr></table>
</body></html>
NTMAIL;
    $t['notify_company'] = <<<'NTMAIL'
<div style="padding-top:4px;font-family:Arial,Helvetica,sans-serif;font-size:17px;line-height:24px;color:#C9CBCF;word-break:break-word;">{{T}}</div>
NTMAIL;
    $t['notify_about'] = <<<'NTMAIL'
About <b style="color:#FFFFFF;">{{T}}</b>
NTMAIL;
    $t['notify_not_sure'] = <<<'NTMAIL'
Not sure which machine fits — please advise
NTMAIL;
    $t['notify_no_machine'] = <<<'NTMAIL'
<span style="color:#B4B6BA;">No machine chosen</span>
NTMAIL;
    $t['box'] = <<<'NTMAIL'
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F2F3F5;border-left:4px solid #F28A1F;"><tr><td style="padding:14px 18px;"><div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#5A5D62;padding-bottom:8px;">{{TITLE}}</div>{{BODY}}</td></tr></table><div style="height:16px;line-height:16px;font-size:0;">&nbsp;</div>
NTMAIL;
    $t['rows_table'] = <<<'NTMAIL'
<table role="presentation" cellpadding="0" cellspacing="0" border="0">{{ROWS}}</table>
NTMAIL;
    $t['text_block'] = <<<'NTMAIL'
<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:23px;color:#2D2E30;word-break:break-word;">{{TEXT}}</div>
NTMAIL;
    $t['files_table'] = <<<'NTMAIL'
<table role="presentation" cellpadding="0" cellspacing="0" border="0">{{LIST}}</table>
NTMAIL;
    $t['notify_file'] = <<<'NTMAIL'
<tr><td style="padding:3px 8px 3px 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:20px;color:#F28A1F;vertical-align:top;">&#9632;</td><td style="padding:3px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;word-break:break-all;">{{NAME}} <span style="color:#5A5D62;">· {{SIZE}}</span></td></tr>
NTMAIL;
    $t['muted'] = <<<'NTMAIL'
<span style="color:#5A5D62;font-weight:normal;">{{T}}</span>
NTMAIL;
    $t['link'] = <<<'NTMAIL'
<a href="{{HREF}}" style="color:#B85C00;text-decoration:none;">{{LABEL}}</a>
NTMAIL;
    $t['link_dark'] = <<<'NTMAIL'
<a href="{{HREF}}" style="color:#F28A1F;text-decoration:none;">{{LABEL}}</a>
NTMAIL;
    $t['button'] = <<<'NTMAIL'
<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 12px 12px 0;"><tr><td style="border-radius:4px;background:#F28A1F;"><a href="{{HREF}}" style="display:inline-block;padding:12px 22px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1F1F1F;text-decoration:none;border-radius:4px;">{{LABEL}}</a></td></tr></table>
NTMAIL;
    $t['button_ghost'] = <<<'NTMAIL'
<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 12px 12px 0;"><tr><td style="border-radius:4px;border:2px solid #F28A1F;"><a href="{{HREF}}" style="display:inline-block;padding:10px 20px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#2D2E30;text-decoration:none;">{{LABEL}}</a></td></tr></table>
NTMAIL;
    return $t;
}

return nt_mail_templates();
