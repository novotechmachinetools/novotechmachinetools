<?php
/**
 * The e-mails of the quote form, read by quote.php: the HTML notification to the sales inbox and the automatic reply to
 * the customer. Written by tools/mail_templates.py: edit the designs there and run it again.
 */
if (!defined('NT_QUOTE')) { http_response_code(404); exit; }

// the pictures the templates name: placeholder => [file under the site root, type]
function nt_mail_images(): array
{
    return [
        'LOGO' => ['img/email/novotech-logo.png', 'image/png'],
        'SIG' => ['img/email/novotech-signature.gif', 'image/gif'],
        'ICON_YOUTUBE' => ['img/email/icon-youtube.png', 'image/png'],
        'ICON_FACEBOOK' => ['img/email/icon-facebook.png', 'image/png'],
        'ICON_INSTAGRAM' => ['img/email/icon-instagram.png', 'image/png'],
        'ICON_TIKTOK' => ['img/email/icon-tiktok.png', 'image/png'],
        'ICON_WHATSAPP' => ['img/email/icon-whatsapp.png', 'image/png'],
        'ICON_LINKEDIN' => ['img/email/icon-linkedin.png', 'image/png'],
    ];
}

function nt_mail_templates(): array
{
    $t = [];
    $t['bf_offer'] = <<<'NTMAIL'
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>NovoTech Machine Tools</title></head>
<body style="margin:0;padding:0;background:#E9EAEC;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">Your NovoTech Black Friday price list: in-stock machines in Mississauga, ON, 5% off factory orders until Dec 4.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#E9EAEC;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;">
<tr><td style="padding:22px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="{{LOGO}}" width="190" height="65" alt="NovoTech Machine Tools Inc." style="display:block;width:190px;height:auto;border:0;"></td>
<td align="right" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#B85C00;padding-left:10px;">Black Friday 2026</td>
</tr></table></td></tr>
<tr><td style="background:#2D2E30;padding:30px 24px 28px 24px;">
<div style="display:inline-block;background:#F28A1F;padding:5px 10px 4px 10px;font-family:'Arial Narrow',Arial,Helvetica,sans-serif;font-size:15px;line-height:18px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#1F2022;">Black Friday price list</div>
<h1 style="margin:14px 0 0 0;font-family:Arial,Helvetica,sans-serif;font-size:28px;line-height:34px;font-weight:bold;color:#FFFFFF;">Here are your Black Friday prices{{COMMA_NAME}}</h1>
<div style="width:64px;height:4px;line-height:4px;font-size:0;background:#F28A1F;margin-top:14px;">&nbsp;</div>
<p style="margin:0;padding-top:14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#E1E2E4;">Thank you for your interest. {{ATTACHED}}The machines are in our Mississauga, ON warehouse, ready to ship, and they are first come, first served: reply to this email or call us to reserve yours.</p>
</td></tr>
<tr><td style="padding:28px 24px 6px 24px;">
{{PICKED}}
{{PRICES}}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F2F3F5;border-left:4px solid #F28A1F;">
<tr><td style="padding:14px 18px;">
<div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#5A5D62;padding-bottom:6px;">Black Friday terms</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding:6px 12px 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#5A5D62;white-space:nowrap;vertical-align:top;">In-stock machines</td><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;font-weight:bold;">Black Friday prices, first come, first served</td></tr><tr><td style="padding:6px 12px 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#5A5D62;white-space:nowrap;vertical-align:top;">Factory orders</td><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;font-weight:bold;">5% off when confirmed by Dec 4 &middot; only 10% down, balance on delivery</td></tr><tr><td style="padding:6px 12px 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#5A5D62;white-space:nowrap;vertical-align:top;">Financing</td><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;font-weight:bold;">0% down through our financing partners, on approved credit</td></tr><tr><td style="padding:6px 12px 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#5A5D62;white-space:nowrap;vertical-align:top;">Write-off</td><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;font-weight:bold;">100% in year one on eligible manufacturing equipment*</td></tr><tr><td style="padding:6px 12px 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#5A5D62;white-space:nowrap;vertical-align:top;">Offer ends</td><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;font-weight:bold;">Friday, December 4, 2026, 11:59 pm Eastern</td></tr></table>
</td></tr></table>
<div style="height:22px;line-height:22px;font-size:0;">&nbsp;</div>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#2D2E30;">Questions about a machine, options, voltage or delivery to your shop? Simply reply to this email.</p>
<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 14px 14px 0;"><tr><td align="center" bgcolor="#F28A1F" style="background:#F28A1F;border:2px solid #F28A1F;border-radius:3px;padding:14px 30px;"><a href="tel:+16475265510" style="display:inline-block;font-family:'Arial Narrow',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;font-weight:bold;color:#1F2022;text-decoration:none;"><span style="color:#1F2022;">Call +1 647 526 5510</span></a></td></tr></table><table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 14px 14px 0;"><tr><td align="center" bgcolor="#FFFFFF" style="background:#FFFFFF;border:2px solid #2D2E30;border-radius:3px;padding:14px 30px;"><a href="{{PAGE_URL}}" style="display:inline-block;font-family:'Arial Narrow',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;font-weight:bold;color:#2D2E30;text-decoration:none;"><span style="color:#2D2E30;">See the machines</span></a></td></tr></table><div style="clear:both;height:0;line-height:0;font-size:0;">&nbsp;</div>
</td></tr>
<tr><td style="padding:16px 24px 12px 24px;">
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#2D2E30;margin-bottom:0;">Best regards,<br><b>The sales team</b><br>NovoTech Machine Tools Inc.</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px;">
<tr><td style="padding:0 0 10px 0;"><img src="{{SIG}}" width="260" height="117" alt="NovoTech Machine Tools Inc." style="display:block;border:0;outline:none;"></td></tr>
<tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:22px;color:#2D2E30;">
<a href="https://novotechmachinetools.com" style="color:#B85C00;text-decoration:none;">www.NovoTechMachineTools.com</a><br>
<a href="mailto:info@NovoTechMachineTools.com" style="color:#B85C00;text-decoration:none;">info@NovoTechMachineTools.com</a><br>
1365 Mid-Way Blvd 26, Mississauga<br>Ontario L5T 2J5, Canada<br>
Tel: <a href="tel:+16475265510" style="color:#2D2E30;text-decoration:none;">+1 647 526 5510</a></td></tr>
<tr><td style="padding:12px 0 0 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding:0 8px 0 0;"><a href="https://www.youtube.com/@NovoTechMachineTools" style="text-decoration:none;"><img src="{{ICON_YOUTUBE}}" width="28" height="28" alt="YouTube" title="NovoTech on YouTube" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.facebook.com/novotechmachinetoolscanada" style="text-decoration:none;"><img src="{{ICON_FACEBOOK}}" width="28" height="28" alt="Facebook" title="NovoTech on Facebook" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.instagram.com/novotech_machinetools/" style="text-decoration:none;"><img src="{{ICON_INSTAGRAM}}" width="28" height="28" alt="Instagram" title="NovoTech on Instagram" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.tiktok.com/@novotechmachinetools" style="text-decoration:none;"><img src="{{ICON_TIKTOK}}" width="28" height="28" alt="TikTok" title="NovoTech on TikTok" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://wa.me/16475265510" style="text-decoration:none;"><img src="{{ICON_WHATSAPP}}" width="28" height="28" alt="WhatsApp" title="NovoTech on WhatsApp" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.linkedin.com/company/novotech-machine-tools-inc/" style="text-decoration:none;"><img src="{{ICON_LINKEDIN}}" width="28" height="28" alt="LinkedIn" title="NovoTech on LinkedIn" style="display:block;border:0;outline:none;"></a></td></tr></table></td></tr></table>
</td></tr>
<tr><td style="padding:6px 24px 22px 24px;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#5A5D62;">*Canadian businesses can deduct 100% of the cost of eligible manufacturing and processing equipment in the tax year it becomes available for use, and eligible Ontario corporations can add the 15% Ontario Made Manufacturing Investment Tax Credit. General information, not tax advice: ask your accountant whether your business qualifies.</td></tr>
<tr><td style="background:#2D2E30;padding:16px 24px;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#B4B6BA;">You received this email because you asked for the Black Friday price list on NovoTechMachineTools.com.</td></tr>
</table></td></tr></table>
</body></html>
NTMAIL;
    $t['bf_offer_text'] = <<<'NTMAIL'
Here are your Black Friday prices{{COMMA_NAME}}

Thank you for your interest. {{ATTACHED_TEXT}}The machines are in our Mississauga, ON warehouse, ready to ship, and they are first come, first served: reply to this email or call us to reserve yours.

{{PICKED_TEXT}}{{PRICES_TEXT}}Black Friday terms
In-stock machines: Black Friday prices, first come, first served
Factory orders: 5% off when confirmed by Dec 4, only 10% down, balance on delivery
Financing: 0% down through our financing partners, on approved credit
Write-off: 100% in year one on eligible manufacturing equipment*
Offer ends: Friday, December 4, 2026, 11:59 pm Eastern

Questions about a machine, options, voltage or delivery to your shop? Simply reply to this email, or call +1 647 526 5510.

See the machines: {{PAGE_URL}}

Best regards,
The sales team
NovoTech Machine Tools Inc.

www.NovoTechMachineTools.com
info@NovoTechMachineTools.com
1365 Mid-Way Blvd 26, Mississauga
Ontario L5T 2J5, Canada
Tel: +1 647 526 5510

*Canadian businesses can deduct 100% of the cost of eligible manufacturing and processing equipment in the tax year it becomes available for use, and eligible Ontario corporations can add the 15% Ontario Made Manufacturing Investment Tax Credit. General information, not tax advice: ask your accountant whether your business qualifies.

You received this email because you asked for the Black Friday price list on NovoTechMachineTools.com.

NTMAIL;
    $t['bf_price_row'] = <<<'NTMAIL'
<tr><td style="padding:9px 10px 9px 0;border-bottom:1px solid #E2E0DC;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2D2E30;vertical-align:top;">{{MARK}}<b>{{MODEL}}</b><br><span style="color:#5A5D62;">{{TYPE}}</span></td><td align="right" style="padding:9px 0;border-bottom:1px solid #E2E0DC;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:20px;color:#2D2E30;vertical-align:top;white-space:nowrap;">{{REGULAR}}<b style="color:#B85C00;">{{PRICE}}</b>{{QTY}}</td></tr>
NTMAIL;
    $t['bf_prices_box'] = <<<'NTMAIL'
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid #E2E0DC;border-top:4px solid #F28A1F;"><tr><td style="padding:14px 18px 6px 18px;"><div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#5A5D62;padding-bottom:4px;">{{TITLE}}</div><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{{ROWS}}</table><p style="margin:10px 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#5A5D62;">{{NOTE}}</p></td></tr></table><div style="height:16px;line-height:16px;font-size:0;">&nbsp;</div>
NTMAIL;
    $t['bf_mark'] = <<<'NTMAIL'
<span style="color:#F28A1F;">&#9632;&nbsp;</span>
NTMAIL;
    $t['reply'] = <<<'NTMAIL'
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>NovoTech Machine Tools</title></head>
<body style="margin:0;padding:0;background:#E9EAEC;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">We have received your request. A NovoTech sales specialist will contact you as soon as possible.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#E9EAEC;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;">
<tr><td style="padding:22px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="{{LOGO}}" width="190" height="65" alt="NovoTech Machine Tools Inc." style="display:block;width:190px;height:auto;border:0;"></td>
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
<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 14px 14px 0;"><tr><td align="center" bgcolor="#F28A1F" style="background:#F28A1F;border:2px solid #F28A1F;border-radius:3px;padding:14px 30px;"><a href="{{BROWSE_URL}}" style="display:inline-block;font-family:'Arial Narrow',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;font-weight:bold;color:#1F2022;text-decoration:none;"><span style="color:#1F2022;">{{BROWSE_LABEL}}</span></a></td></tr></table><table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 14px 14px 0;"><tr><td align="center" bgcolor="#FFFFFF" style="background:#FFFFFF;border:2px solid #2D2E30;border-radius:3px;padding:14px 30px;"><a href="https://www.youtube.com/watch?v=ZGo_n6-2_Qc&amp;t=3s" style="display:inline-block;font-family:'Arial Narrow',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;font-weight:bold;color:#2D2E30;text-decoration:none;"><span style="color:#2D2E30;">Watch our video</span></a></td></tr></table><div style="clear:both;height:0;line-height:0;font-size:0;">&nbsp;</div>
</td></tr>
<tr><td style="padding:16px 24px 30px 24px;">
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:25px;color:#2D2E30;margin-bottom:0;">Best regards,<br><b>The sales team</b><br>NovoTech Machine Tools Inc.</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px;">
<tr><td style="padding:0 0 10px 0;"><img src="{{SIG}}" width="260" height="117" alt="NovoTech Machine Tools Inc." style="display:block;border:0;outline:none;"></td></tr>
<tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:22px;color:#2D2E30;">
<a href="https://novotechmachinetools.com" style="color:#B85C00;text-decoration:none;">www.NovoTechMachineTools.com</a><br>
<a href="mailto:info@NovoTechMachineTools.com" style="color:#B85C00;text-decoration:none;">info@NovoTechMachineTools.com</a><br>
1365 Mid-Way Blvd 26, Mississauga<br>Ontario L5T 2J5, Canada<br>
Tel: <a href="tel:+16475265510" style="color:#2D2E30;text-decoration:none;">+1 647 526 5510</a></td></tr>
<tr><td style="padding:12px 0 0 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding:0 8px 0 0;"><a href="https://www.youtube.com/@NovoTechMachineTools" style="text-decoration:none;"><img src="{{ICON_YOUTUBE}}" width="28" height="28" alt="YouTube" title="NovoTech on YouTube" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.facebook.com/novotechmachinetoolscanada" style="text-decoration:none;"><img src="{{ICON_FACEBOOK}}" width="28" height="28" alt="Facebook" title="NovoTech on Facebook" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.instagram.com/novotech_machinetools/" style="text-decoration:none;"><img src="{{ICON_INSTAGRAM}}" width="28" height="28" alt="Instagram" title="NovoTech on Instagram" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.tiktok.com/@novotechmachinetools" style="text-decoration:none;"><img src="{{ICON_TIKTOK}}" width="28" height="28" alt="TikTok" title="NovoTech on TikTok" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://wa.me/16475265510" style="text-decoration:none;"><img src="{{ICON_WHATSAPP}}" width="28" height="28" alt="WhatsApp" title="NovoTech on WhatsApp" style="display:block;border:0;outline:none;"></a></td><td style="padding:0 8px 0 0;"><a href="https://www.linkedin.com/company/novotech-machine-tools-inc/" style="text-decoration:none;"><img src="{{ICON_LINKEDIN}}" width="28" height="28" alt="LinkedIn" title="NovoTech on LinkedIn" style="display:block;border:0;outline:none;"></a></td></tr></table></td></tr></table>
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

YouTube: https://www.youtube.com/@NovoTechMachineTools
Facebook: https://www.facebook.com/novotechmachinetoolscanada
Instagram: https://www.instagram.com/novotech_machinetools/
TikTok: https://www.tiktok.com/@novotechmachinetools
WhatsApp: https://wa.me/16475265510
LinkedIn: https://www.linkedin.com/company/novotech-machine-tools-inc/

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
<body style="margin:0;padding:0;background:#FFFFFF;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{{PRE}}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;border:1px solid #E2E0DC;">
<tr><td style="padding:22px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><img src="{{LOGO}}" width="190" height="65" alt="NovoTech Machine Tools Inc." style="display:block;width:190px;height:auto;border:0;"></td>
<td align="right" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#B85C00;padding-left:10px;">{{LABEL}}</td>
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
<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 14px 14px 0;"><tr><td align="center" bgcolor="#F28A1F" style="background:#F28A1F;border:2px solid #F28A1F;border-radius:3px;padding:14px 30px;"><a href="{{HREF}}" style="display:inline-block;font-family:'Arial Narrow',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;font-weight:bold;color:#1F2022;text-decoration:none;"><span style="color:#1F2022;">{{LABEL}}</span></a></td></tr></table>
NTMAIL;
    $t['button_ghost'] = <<<'NTMAIL'
<table role="presentation" align="left" cellpadding="0" cellspacing="0" border="0" style="margin:0 14px 14px 0;"><tr><td align="center" bgcolor="#FFFFFF" style="background:#FFFFFF;border:2px solid #2D2E30;border-radius:3px;padding:14px 30px;"><a href="{{HREF}}" style="display:inline-block;font-family:'Arial Narrow',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;font-weight:bold;color:#2D2E30;text-decoration:none;"><span style="color:#2D2E30;">{{LABEL}}</span></a></td></tr></table>
NTMAIL;
    return $t;
}

return nt_mail_templates();
