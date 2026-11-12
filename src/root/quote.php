<?php
/**
 * NovoTech quote-request handler.
 * Receives the form on each product page, checks it (honeypot, time to submit, Google reCAPTCHA, attachments) and emails it
 * to the sales inbox with the customer's drawings and photos attached, as HTML with a plain-text twin. With $AUTOREPLY set,
 * the customer gets an automatic reply too. The e-mail designs are in quote-mail.php, written by tools/mail_templates.py.
 * Works with the JavaScript submit (returns JSON) and with a plain HTML POST (returns a small page).
 *
 * reCAPTCHA v3: put the secret key in form-config.php next to this file (copy form-config.sample.php); the site key goes into
 * content/site.json. form-config.php is never committed to Git. Without a secret the check is skipped, so the form keeps
 * working until the keys are set.
 */
declare(strict_types=1);

$TO        = 'info@NovoTechMachineTools.com';
$FROM      = 'website@novotechmachinetools.com';   // must be a mailbox on this domain for HostPapa's mail server
$SUBJECT   = 'Quote request from NovoTechMachineTools.com';
$MIN_SECS  = 4;                                     // forms submitted faster than this are bots
$MAX_FILES = 10;                                    // the owner, Nov 9 2026 (was 5 files and 10 MB)
$MAX_BYTES = 13 * 1024 * 1024;                      // all attachments together; the e-mail stays under 20 MB
$OK_EXT    = ['pdf', 'dwg', 'dxf', 'step', 'stp', 'igs', 'iges', 'sldprt', 'x_t', 'jpg', 'jpeg', 'png', 'heic', 'webp', 'zip',
              'xls', 'xlsx', 'doc', 'docx', 'txt', 'csv'];

$cfgFile = __DIR__ . '/form-config.php';
$cfg = is_file($cfgFile) ? (array)(require $cfgFile) : [];
$SECRET = (string)($cfg['recaptcha_secret'] ?? '');
$MIN_SCORE = (float)($cfg['recaptcha_min_score'] ?? 0.5);     // reCAPTCHA v3: 0.0 = bot … 1.0 = person

// The e-mail designs (tools/mail_templates.py); without the file the notification goes out as plain text, as before
define('NT_QUOTE', true);
require __DIR__ . '/mail-lib.php';                  // nt_e, nt_fill, nt_addr, nt_alternative, nt_images, nt_machine
$mailFile = __DIR__ . '/quote-mail.php';
$MAIL = is_file($mailFile) ? (array)(require $mailFile) : [];
// The automatic reply to the customer (design in tools/mail_templates.py): true sends it (approved by the owner, Nov 9 2026).
// It comes from the sales inbox and the customer's reply goes back there
$AUTOREPLY  = true;
$REPLY_FROM = 'info@novotechmachinetools.com';

header('X-Content-Type-Options: nosniff');
$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false;

function respond(bool $ok, string $msg, int $code = 200): void {
    global $wantsJson;
    http_response_code($code);
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'error' => $ok ? null : $msg]);
    } else {
        header('Content-Type: text/html; charset=utf-8');
        $title = $ok ? 'Thank you' : 'Something went wrong';
        $tick  = $ok ? '<svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true" style="vertical-align:-4px;margin-right:10px"><circle cx="12" cy="12" r="12" fill="#43A047"/><path d="M6.8 12.4l3.4 3.4 7-7.4" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>' : '';
        $color = $ok ? ' style="color:#43A047"' : '';
        echo "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><meta name=\"robots\" content=\"noindex\"><title>$title — NovoTech Machine Tools</title>"
           . "<body style=\"font-family:Arial,sans-serif;max-width:40em;margin:3em auto;padding:0 1em;line-height:1.5\"><h1$color>$tick$title</h1><p$color>" . htmlspecialchars($msg, ENT_QUOTES, 'UTF-8') . "</p>"
           . "<p><a href=\"javascript:history.back()\">Go back</a> · <a href=\"/\">NovoTech home</a></p></body></html>";
    }
    exit;
}

// what the automatic reply may repeat from the form: short, and without a web or e-mail address in it
function nt_safe(string $s, int $max): string {
    return (mb_strlen($s) <= $max && !preg_match('~https?:|www\.|://|@|\.(com|net|org|info|biz|ru|cn|xyz|top)\b~i', $s)) ? $s : '';
}

// the page the form was sent from: the address the page put in the form, else the browser's Referer; only this site's pages,
// without query or fragment
function nt_page_url(string $field, string $ref): string {
    foreach ([$field, $ref] as $u) {
        $p = parse_url($u);
        if (is_array($p) && ($p['scheme'] ?? '') === 'https' && preg_match('/^(www\.)?novotechmachinetools\.com$/i', $p['host'] ?? '')
            && preg_match('#^(/[A-Za-z0-9._~-]*)*$#', $p['path'] ?? '/')) {
            return 'https://novotechmachinetools.com' . (($p['path'] ?? '') !== '' ? $p['path'] : '/');
        }
    }
    return '';
}

// the automatic reply's button back to the page the request came from, named after it: "Browse band saws" (the owner,
// Nov 9 2026). Pages that are not about machines get "Browse our machines" and the products page.
function nt_browse(string $short, string $url): array {
    $other = ['home page', 'contact us', 'about us', 'products', 'brochures', 'articles', 'rebar bender and cutter benefits'];
    $short = nt_safe($short, 60);
    if ($url === '' || $short === '' || in_array(mb_strtolower($short), $other, true) || count(preg_split('/\s+/', $short)) > 7) {
        return ['https://novotechmachinetools.com/products', 'Browse our machines'];
    }
    // "Band saws" -> "band saws"; brand names and abbreviations keep their capitals (NovoTech, Bekamak, European, CNC, H-frame)
    $first = (string)preg_replace('/[\s-].*$/s', '', $short);
    $keep = ['NovoTech', 'Bekamak', 'Bystronic', 'Trumpf', 'Wila', 'Amada', 'Dener', 'Durma', 'Plastmak', 'Isitan', 'Eurostamp',
             'European', 'American', 'Canadian'];
    if (preg_match('/^[A-Z][a-z]/', $short) && !in_array($first, $keep, true)) {
        $short = mb_strtolower(mb_substr($short, 0, 1)) . mb_substr($short, 1);
    }
    return [$url, "Browse $short"];
}

// the notification to the sales inbox, in HTML, in the look of the automatic reply (the owner, Nov 9 2026): [HTML, pictures]
function nt_notification(array $M, array $d): array {
    $row  = static function (string $k, string $v) use ($M): string { return nt_fill($M['summary_row'], ['K' => nt_e($k), 'V' => $v]); };
    $link = static function (string $href, string $label, string $tpl = 'link') use ($M): string {
        return nt_fill($M[$tpl], ['HREF' => nt_e($href), 'LABEL' => nt_e($label)]);
    };
    $box  = static function (string $title, string $body) use ($M): string { return nt_fill($M['box'], ['TITLE' => nt_e($title), 'BODY' => $body]); };
    $tel = (string)preg_replace('/[^0-9+]/', '', $d['phone']);
    $mailto = 'mailto:' . str_replace('%40', '@', rawurlencode($d['email']));
    $m = $d['machine'];
    $about = $m === '' ? $M['notify_no_machine']
           : (stripos($m, 'not sure') === 0 ? $M['notify_not_sure'] : nt_fill($M['notify_about'], ['T' => nt_machine($m)]));
    $rows = $row('Email', $link($mailto, $d['email']))
          . ($d['phone'] !== '' ? $row('Phone', strlen($tel) >= 7 ? $link("tel:$tel", $d['phone']) : nt_e($d['phone'])) : '')
          . $row('Page', $d['url'] !== '' ? $link($d['url'], $d['page']) : nt_e($d['page']))
          . $row('Received', nt_e($d['when']));
    $files = '';
    if ($d['files']) {
        $list = '';
        foreach ($d['files'] as $a) {
            $list .= nt_fill($M['notify_file'], ['NAME' => nt_e($a['name']), 'SIZE' => number_format(max(1, $a['size'] / 1024), 0) . ' KB']);
        }
        $files = $box('Attached files (' . count($d['files']) . ')', nt_fill($M['files_table'], ['LIST' => $list]));
    }
    $text = $d['message'] !== '' ? nl2br(nt_e($d['message']), false) : nt_fill($M['muted'], ['T' => 'No message']);
    // no "Reply to" button: a button in an e-mail can only open a new, empty message, while the mail program's own Reply
    // answers the customer (Reply-To) with this request below it (the owner, Nov 9 2026)
    $buttons = strlen($tel) >= 7 ? nt_fill($M['button'], ['HREF' => nt_e("tel:$tel"), 'LABEL' => 'Call ' . nt_e($d['phone'])]) : '';
    $footer = 'Sent from IP ' . nt_e($d['ip'])
            . ($d['url'] !== '' ? '<br>Form on ' . $link($d['url'], $d['url'], 'link_dark') : ($d['ref'] !== '' ? '<br>Form on ' . nt_e($d['ref']) : ''));
    $pre = array_filter([$d['name'], $d['company'], $m], static function ($x) { return $x !== ''; });
    list($src, $images) = nt_images($M['notify']);
    return [nt_fill($M['notify'], $src + [
        'LABEL'   => 'New quote request',
        'PRE'     => nt_e(implode(' · ', $pre)),
        'NAME'    => nt_e($d['name']),
        'COMPANY' => $d['company'] !== '' ? nt_fill($M['notify_company'], ['T' => nt_e($d['company'])]) : '',
        'ABOUT'   => $about,
        'DETAILS' => $box('Details', nt_fill($M['rows_table'], ['ROWS' => $rows])),
        'MESSAGE' => $box('Message', nt_fill($M['text_block'], ['TEXT' => $text])),
        'FILES'   => $files,
        'BUTTONS' => $buttons,
        'FOOTER'  => $footer,
    ]), $images];
}

// the automatic reply: [plain text, HTML, pictures]; the customer's own message is never repeated in it
function nt_autoreply(array $M, string $name, string $machine, string $page, string $when, array $browse): array {
    $name = nt_safe($name, 60);
    $machine = nt_safe($machine, 140);
    $page = nt_safe($page, 80);
    $about = $machine !== '' && stripos($machine, 'not sure') !== 0;
    $srow = static function (string $k, string $v) use ($M): string { return nt_fill($M['summary_row'], ['K' => nt_e($k), 'V' => nt_machine($v)]); };
    list($src, $images) = nt_images($M['reply']);
    $html = nt_fill($M['reply'], $src + [
        'COMMA_NAME'   => $name !== '' ? ', ' . nt_e($name) : '',
        'ABOUT'        => $about ? nt_fill($M['about'], ['T' => nt_machine($machine)]) : '',
        'ROWS'         => ($machine !== '' ? $srow('Machine', $machine) : '') . ($page !== '' ? $srow('Page', $page) : '') . $srow('Received', $when),
        'BROWSE_URL'   => nt_e($browse[0]),
        'BROWSE_LABEL' => nt_e($browse[1]),
    ]);
    $text = nt_fill($M['text'], [
        'COMMA_NAME'   => $name !== '' ? ", $name" : '',
        'ABOUT'        => $about ? " about $machine" : '',
        'ROWS'         => ($machine !== '' ? "Machine:  $machine\n" : '') . ($page !== '' ? "Page:     $page\n" : '') . "Received: $when\n",
        'BROWSE_URL'   => $browse[0],
        'BROWSE_LABEL' => $browse[1],
    ]);
    return [$text, $html, $images];
}

// at most 10 automatic replies to one address a day (the owner, Nov 9 2026; was 3), 10 to one IP an hour and 100 a day in all,
// so the form cannot be used to flood someone's inbox; the log in the temp folder keeps hashes, not addresses
function nt_autoreply_allowed(string $email, string $ip): bool {
    $fh = @fopen(rtrim(sys_get_temp_dir(), '/\\') . '/nt-autoreply-' . substr(md5(__DIR__), 0, 10) . '.json', 'c+');
    if ($fh === false) { return true; }
    if (!flock($fh, LOCK_EX)) { fclose($fh); return true; }
    $now = time();
    $log = json_decode((string)stream_get_contents($fh), true);
    $keep = [];
    foreach (is_array($log) ? $log : [] as $r) {
        if (is_array($r) && count($r) === 3 && (int)$r[0] > $now - 86400) { $keep[] = $r; }
    }
    $e = substr(hash('sha256', 'e|' . strtolower($email)), 0, 20);
    $i = substr(hash('sha256', 'i|' . $ip), 0, 20);
    $byEmail = 0;
    $byIp = 0;
    foreach ($keep as $r) {
        if ($r[1] === $e) { $byEmail++; }
        if ($r[2] === $i && (int)$r[0] > $now - 3600) { $byIp++; }
    }
    $ok = $byEmail < 10 && $byIp < 10 && count($keep) < 100;
    if ($ok) { $keep[] = [$now, $e, $i]; }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, (string)json_encode($keep));
    fflush($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
    return $ok;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'This address only accepts form submissions.', 405);
}

// A request larger than PHP's post_max_size arrives with $_POST and $_FILES empty.
if (empty($_POST) && (int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 0) {
    respond(false, 'The attached files are too large. Please keep attachments under ' . intdiv($MAX_BYTES, 1048576) . ' MB in total, or email larger files to info@NovoTechMachineTools.com.', 413);
}

$f = static function (string $k, int $max = 500): string {
    $v = isset($_POST[$k]) ? (string)$_POST[$k] : '';
    $v = trim(str_replace(["\r", "\0"], '', $v));
    return mb_substr($v, 0, $max);
};

// Spam checks: honeypot field, time-to-submit, and header injection.
if ($f('website') !== '') {
    respond(true, 'Thanks — your request has been received.');   // pretend success to bots
}
$ts = (int)$f('ts', 20);
if ($ts > 0 && (time() - $ts) < $MIN_SECS) {
    respond(true, 'Thanks — your request has been received.');
}

// Google reCAPTCHA v3: the token the page fetched when the form was sent, checked with Google; a score from 0.0 (bot) to
// 1.0 (person) comes back, and requests below the threshold are refused
if ($SECRET !== '') {
    $token = $f('g-recaptcha-response', 4000);
    $blocked = 'Our spam filter could not confirm that this request was sent by a person. Please try again, or email '
             . 'info@NovoTechMachineTools.com or call +1 647 526 5510.';
    if ($token === '') {
        respond(false, $blocked, 422);
    }
    $post = http_build_query(['secret' => $SECRET, 'response' => $token, 'remoteip' => $_SERVER['REMOTE_ADDR'] ?? '']);
    $raw = false;
    if (function_exists('curl_init')) {
        $ch = curl_init('https://www.google.com/recaptcha/api/siteverify');
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $post, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10]);
        $raw = curl_exec($ch);
        curl_close($ch);
    } else {
        $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
                                                 'content' => $post, 'timeout' => 10]]);
        $raw = @file_get_contents('https://www.google.com/recaptcha/api/siteverify', false, $ctx);
    }
    $res = is_string($raw) ? json_decode($raw, true) : null;
    $score = is_array($res) && isset($res['score']) ? (float)$res['score'] : 0.0;
    if (!is_array($res) || empty($res['success']) || ($res['action'] ?? 'quote') !== 'quote' || $score < $MIN_SCORE) {
        respond(false, $blocked, 422);
    }
}

$name    = $f('name', 120);
$company = $f('company', 160);
$email   = $f('email', 160);
$phone   = $f('phone', 60);
$machine = $f('machine', 200);
$message = $f('message', 4000);
$page    = $f('page', 200);
$pageShort = $f('page_short', 80);    // the page in a word or two: "Rebar benders", "Ironworkers", "Contact us"
$rfq     = $f('rfq', 60);            // the machine in a word or two, for the subject: "press brake", "plate roller", "bandsaw"

if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please add your name and a valid email address.', 422);
}
foreach ([$name, $company, $email, $phone, $machine, $page, $pageShort, $rfq] as $v) {
    if (preg_match('/[\r\n]/', $v)) { respond(false, 'Invalid input.', 422); }
}

// Attachments: drawings, photos and documents
$files = [];
if (isset($_FILES['files']) && is_array($_FILES['files']['name'] ?? null)) {
    $n = count($_FILES['files']['name']);
    $total = 0;
    for ($i = 0; $i < $n; $i++) {
        $err = (int)$_FILES['files']['error'][$i];
        if ($err === UPLOAD_ERR_NO_FILE) { continue; }
        if ($err === UPLOAD_ERR_INI_SIZE || $err === UPLOAD_ERR_FORM_SIZE) {
            respond(false, 'One of the files is too large. Please keep attachments under ' . intdiv($MAX_BYTES, 1048576) . ' MB in total, or email larger files to info@NovoTechMachineTools.com.', 413);
        }
        if ($err !== UPLOAD_ERR_OK) { respond(false, 'A file could not be uploaded. Please try again.', 400); }
        $tmp = (string)$_FILES['files']['tmp_name'][$i];
        if (!is_uploaded_file($tmp)) { respond(false, 'Invalid upload.', 400); }
        $orig = (string)$_FILES['files']['name'][$i];
        $ext = strtolower(pathinfo($orig, PATHINFO_EXTENSION));
        if (!in_array($ext, $OK_EXT, true)) {
            respond(false, 'We accept PDF, DWG, DXF, STEP, IGES, JPG, PNG, ZIP, Excel and Word files — “' . mb_substr($orig, 0, 80) . '” is not one of them.', 415);
        }
        $size = (int)filesize($tmp);
        $total += $size;
        if (count($files) >= $MAX_FILES) { respond(false, "Please attach up to $MAX_FILES files.", 413); }
        if ($total > $MAX_BYTES) {
            respond(false, 'The files add up to more than ' . intdiv($MAX_BYTES, 1048576) . ' MB. Please send fewer or smaller files, or email them to info@NovoTechMachineTools.com.', 413);
        }
        $base = preg_replace('/[^A-Za-z0-9._ ()-]+/', '_', pathinfo($orig, PATHINFO_FILENAME));
        $base = trim(mb_substr((string)$base, 0, 80), ' ._') ?: 'attachment';
        $mime = 'application/octet-stream';
        if (function_exists('finfo_open')) {
            $fi = finfo_open(FILEINFO_MIME_TYPE);
            $det = $fi ? (string)finfo_file($fi, $tmp) : '';
            if ($fi) { finfo_close($fi); }
            if ($det !== '' && preg_match('#^[a-z]+/[a-z0-9.+-]+$#i', $det)) { $mime = $det; }
        }
        if (preg_match('#^(text/x-php|application/x-(httpd-)?php|application/x-(ms)?dos-?exec|application/x-executable)#i', $mime)) {
            respond(false, 'This file type is not accepted.', 415);
        }
        $files[] = ['name' => "$base.$ext", 'mime' => $mime, 'data' => (string)file_get_contents($tmp), 'size' => $size];
    }
}

$now  = new DateTime('now', new DateTimeZone('America/Toronto'));
$when = $now->format('F j, Y, g:i A T');                       // November 9, 2026, 4:51 PM EST
$ip   = (string)($_SERVER['REMOTE_ADDR'] ?? '?');
$ref  = (string)($_SERVER['HTTP_REFERER'] ?? '');
$pageUrl   = nt_page_url($f('page_url', 300), $ref);
$pageLabel = $pageShort !== '' ? $pageShort : ($page !== '' ? $page : 'NovoTechMachineTools.com');

$lines = [
    "Quote request from " . ($page !== '' ? $page : 'NovoTechMachineTools.com'),
    "",
    "Name:     $name",
    "Company:  $company",
    "Email:    $email",
    "Phone:    $phone",
    "Machine:  " . ($machine !== '' ? $machine : '(not chosen)'),
    "Page:     " . ($pageShort !== '' ? $pageShort : $page),
    "",
    "Message:",
    $message,
    "",
];
if ($files) {
    $lines[] = "Attached files:";
    foreach ($files as $a) { $lines[] = sprintf("  %s (%s KB)", $a['name'], number_format(max(1, $a['size'] / 1024), 0)); }
    $lines[] = "";
}
$lines[] = "----";
$lines[] = "Sent $when from IP $ip";
$lines[] = "Page: " . ($ref !== '' ? $ref : '?');
$text = implode("\n", $lines);

// the same in HTML (the owner, Nov 9 2026); the plain text above goes along for mail programs that do not show HTML
list($html, $htmlImages) = isset($MAIL['notify']) ? nt_notification($MAIL, [
    'name' => $name, 'company' => $company, 'email' => $email, 'phone' => $phone, 'machine' => $machine, 'message' => $message,
    'page' => $pageLabel, 'url' => $pageUrl, 'ref' => $ref, 'files' => $files, 'when' => $when, 'ip' => $ip,
]) : ['', []];

$headers = [
    "From: NovoTech website <$FROM>",
    "Reply-To: " . nt_addr($name, $email),
    "MIME-Version: 1.0",
    "X-Mailer: NovoTech-quote-form",
];
$alt = 'NTA-' . bin2hex(random_bytes(12));
$part = $html !== ''
    ? ["Content-Type: multipart/alternative; boundary=\"$alt\"", nt_alternative($text, $html, $alt, $htmlImages)]
    : ["Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit", str_replace("\n", "\r\n", $text) . "\r\n"];
if ($files) {
    $boundary = 'NT-' . bin2hex(random_bytes(12));
    $headers[] = "Content-Type: multipart/mixed; boundary=\"$boundary\"";
    $body = "This is a multi-part message in MIME format.\r\n\r\n--$boundary\r\n{$part[0]}\r\n\r\n{$part[1]}";
    foreach ($files as $a) {
        $body .= "--$boundary\r\n"
               . "Content-Type: {$a['mime']}; name=\"{$a['name']}\"\r\n"
               . "Content-Transfer-Encoding: base64\r\n"
               . "Content-Disposition: attachment; filename=\"{$a['name']}\"\r\n\r\n"
               . chunk_split(base64_encode($a['data']), 76, "\r\n");
    }
    $body .= "--$boundary--\r\n";
} elseif ($html !== '') {
    $headers[] = $part[0];
    $body = "This is a multi-part message in MIME format.\r\n\r\n" . $part[1];
} else {
    $headers[] = "Content-Type: text/plain; charset=UTF-8";
    $body = $text;
}
// a short subject: "RFQ for press brake", "RFQ for plate roller", "RFQ for bandsaw" — the machine in a word or two, no model, specs
// or page (the owner, Nov 11 2026: "a 10-km subject is confusing"); the page and the machine chosen are in the e-mail itself.
// $rfq is the page's machine (content/rfq.json), or on a general page the machine family picked in the form; a dealer enquiry says so
$dealer = stripos($machine, 'sales agent') !== false || stripos($machine, 'dealer') !== false;
$rfqName = preg_replace('/[^\p{L}\p{N} \-\/&.]+/u', '', $rfq);
$subject = $dealer ? 'Dealer inquiry' : ($rfqName !== '' ? "RFQ for $rfqName" : 'RFQ');
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$sent = @mail($TO, $subject, $body, implode("\r\n", $headers), "-f$FROM");

// the automatic reply to the customer, once the request has reached the sales inbox: from info@, and replies go back there
if ($sent && $AUTOREPLY && isset($MAIL['reply'], $MAIL['text']) && nt_autoreply_allowed($email, $ip)) {
    list($arText, $arHtml, $arImages) = nt_autoreply($MAIL, $name, $machine, $pageShort, $when, nt_browse($pageShort, $pageUrl));
    $b = 'NTR-' . bin2hex(random_bytes(12));
    $arHeaders = [
        "From: NovoTech Machine Tools <$REPLY_FROM>",
        "Reply-To: NovoTech Machine Tools <$REPLY_FROM>",
        "MIME-Version: 1.0",
        "Auto-Submitted: auto-generated",            // RFC 3834: out-of-office replies are not sent back to it
        "X-Auto-Response-Suppress: All",
        "X-Mailer: NovoTech-quote-form",
        "Content-Type: multipart/alternative; boundary=\"$b\"",
    ];
    @mail($email, 'We received your request | NovoTech Machine Tools',
          "This is a multi-part message in MIME format.\r\n\r\n" . nt_alternative($arText, $arHtml, $b, $arImages), implode("\r\n", $arHeaders), "-f$REPLY_FROM");
}

if ($sent) {
    respond(true, 'Thanks — your request is on its way. We will reply within one business day.');
}
respond(false, 'The message could not be sent from the website. Please email info@NovoTechMachineTools.com or call +1 647 526 5510.', 500);
