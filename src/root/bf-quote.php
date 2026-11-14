<?php
/**
 * NovoTech — Black Friday 2026 instant quote: the form on /black-friday-machine-sale (templates/black-friday.html, js/bf.js).
 *
 * The owner (Nov 13 2026): the page shows the in-stock machines without prices; a buyer fills in his company details and the
 * website e-mails him the price list by itself — unless he is a machinery dealer or reseller, one of NovoTech's suppliers or
 * a competitor (by e-mail, domain, company name or phone). Every request also reaches info@ so the owner can follow up: "price
 * list sent to …", or "on hold" with the reasons and a link to review it and send the price list with one click.
 *
 * The price list (a PDF, and optionally the prices for a table in the e-mail), the supplier and competitor lists and the log
 * live in ~/novotech-private/black-friday/ on the server — outside the website, outside Git (see bf-config.sample.php). The
 * e-mail designs are in quote-mail.php (tools/mail_templates.py), shared with quote.php.
 */
declare(strict_types=1);

$FROM       = 'website@novotechmachinetools.com';   // the notification to info@ (as quote.php)
$REPLY_FROM = 'info@novotechmachinetools.com';      // the price list to the buyer: from the sales inbox, replies go there
$MIN_SECS   = 4;                                     // forms sent faster than this are bots
$PAGE       = 'https://novotechmachinetools.com/black-friday-machine-sale';
$PHONE      = '+1 647 526 5510';

define('NT_QUOTE', true);
require __DIR__ . '/mail-lib.php';                   // nt_e, nt_fill, nt_addr, nt_alternative, nt_images, nt_machine
$mailFile = __DIR__ . '/quote-mail.php';
$MAIL = is_file($mailFile) ? (array)(require $mailFile) : [];
$cfgFile = __DIR__ . '/form-config.php';             // the reCAPTCHA secret, shared with quote.php
$cfg = is_file($cfgFile) ? (array)(require $cfgFile) : [];
$CAPTCHA   = (string)($cfg['recaptcha_secret'] ?? '');
$MIN_SCORE = (float)($cfg['recaptcha_min_score'] ?? 0.5);

// ~/novotech-private/black-friday: from public_html (the live site) or public_html/new (the test copy) up to the home folder
function bf_private_dir(): string {
    $env = getenv('NT_PRIVATE_DIR');
    if (is_string($env) && $env !== '') { return rtrim($env, '/'); }
    $home = (string)preg_replace('#/public_html(?:/.*)?$#', '', __DIR__);
    return ($home !== __DIR__ ? $home : dirname(__DIR__)) . '/novotech-private/black-friday';
}
$PRIV = bf_private_dir();
$BF = is_file("$PRIV/bf-config.php") ? (array)(require "$PRIV/bf-config.php") : [];
$TO = (string)($BF['notify_to'] ?? 'info@NovoTechMachineTools.com');

header('X-Content-Type-Options: nosniff');
header('X-Robots-Tag: noindex, nofollow');
$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false;

// ------------------------------------------------------------------------------------------------ small helpers
function bf_page(string $title, string $body, int $code = 200): void {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       . '<meta name="robots" content="noindex"><title>' . nt_e($title) . ' — NovoTech Machine Tools</title>'
       . '<body style="font-family:Arial,sans-serif;max-width:44em;margin:2.5em auto;padding:0 1em;line-height:1.5;color:#2D2E30">'
       . '<h1 style="font-size:26px">' . nt_e($title) . '</h1>' . $body . '</body></html>';
    exit;
}

function respond(bool $ok, string $msg, int $code = 200): void {
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($ok ? ['ok' => true, 'message' => $msg] : ['ok' => false, 'error' => $msg]);
        exit;
    }
    bf_page($ok ? 'Thank you' : 'Something went wrong', '<p>' . nt_e($msg) . '</p><p><a href="javascript:history.back()">Go back</a> · <a href="/">NovoTech home</a></p>', $code);
}

// a name the e-mail to the buyer may repeat: letters, spaces, . ' - only (the form must not be a way to mail a stranger a text)
function bf_first_name(string $name): string {
    $first = trim((string)preg_split('/\s+/u', trim($name))[0]);
    return preg_match("/^[\\p{L}][\\p{L}.'\\-]{0,29}$/u", $first) ? $first : '';
}

// lower case, every run of other characters one space: "Westway Machinery Ltd." -> "westway machinery ltd"
function bf_norm(string $s): string {
    return trim((string)preg_replace('/[^a-z0-9]+/', ' ', strtolower($s)));
}

// the host of an e-mail address or a web address, without www.
function bf_domain(string $s): string {
    $s = strtolower(trim($s));
    if (strpos($s, '@') !== false) { return (string)substr($s, strrpos($s, '@') + 1); }
    if ($s === '') { return ''; }
    $h = (string)(parse_url(preg_match('#^[a-z]+://#', $s) ? $s : "http://$s", PHP_URL_HOST) ?? '');
    return (string)preg_replace('/^www\./', '', $h);
}

// the word from $words that the domain or the company name contains, or ''. A domain contains a word of 5 letters or more
// anywhere ("westwaymachinery" in westwaymachinery.com, "dener" in dener.com.tr); a shorter word ("lvd", "davi") must be a
// whole part of the domain, so davidsonwelding.com is not taken for Davi. A company name matches on whole words ("westway
// machinery" in "Westway Machinery Ltd.").
function bf_match(array $words, string $domain, string $company): string {
    $dom = str_replace(['.', '-', ' '], '', $domain);
    $parts = preg_split('/[.\- ]+/', $domain) ?: [];
    $name = ' ' . bf_norm($company) . ' ';
    foreach ($words as $w) {
        $w = strtolower(trim((string)$w));
        if ($w === '') { continue; }
        $base = (string)preg_replace('/\.(com\.tr|com\.cn|com\.tw|co\.uk|com|ca|net|org|co|it|de|ch|es|tr|cn|tw|us|eu)$/', '', $w);
        $compact = (string)preg_replace('/[^a-z0-9]/', '', $base);
        if ($domain !== '' && $compact !== '' && ((strlen($compact) >= 5 && strpos($dom, $compact) !== false) || in_array($compact, $parts, true))) {
            return $w;
        }
        $phrase = bf_norm($base);
        if (strlen($phrase) >= 3 && strpos($name, " $phrase ") !== false) { return $w; }
    }
    return '';
}

// the last ten digits of a phone number (North American numbers with or without the 1)
function bf_digits(string $s): string {
    $d = (string)preg_replace('/\D+/', '', $s);
    return strlen($d) > 10 ? substr($d, -10) : $d;
}

function bf_token(string $id): string {
    global $BF;
    $k = (string)($BF['secret'] ?? '');
    return $k === '' ? '' : hash_hmac('sha256', 'bf|' . $id, $k);
}

function bf_save(array $r): bool {
    global $PRIV;
    $dir = "$PRIV/requests";
    if (!is_dir($dir) && !@mkdir($dir, 0700, true)) { return false; }
    return @file_put_contents("$dir/{$r['id']}.json", (string)json_encode($r, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), LOCK_EX) !== false;
}

function bf_load(string $id): ?array {
    global $PRIV;
    if (!preg_match('/^\d{8}-\d{6}-[a-f0-9]{8}$/', $id)) { return null; }
    $f = "$PRIV/requests/$id.json";
    $r = is_file($f) ? json_decode((string)file_get_contents($f), true) : null;
    return is_array($r) ? $r : null;
}

// one line per request in requests.csv (opens in Excel): the follow-up list
function bf_log(array $r, string $event): void {
    global $PRIV;
    if (!is_dir($PRIV) && !@mkdir($PRIV, 0700, true)) { return; }
    $f = "$PRIV/requests.csv";
    $new = !is_file($f);
    $fh = @fopen($f, 'a');
    if ($fh === false) { return; }
    if (flock($fh, LOCK_EX)) {
        if ($new) {
            fputcsv($fh, ['received', 'event', 'id', 'name', 'company', 'email', 'phone', 'city', 'province/state', 'country', 'website',
                          'business', 'machines', 'news ok', 'reasons on hold', 'ip']);
        }
        fputcsv($fh, [$r['when'], $event, $r['id'], $r['name'], $r['company'], $r['email'], $r['phone'], $r['city'], $r['region'],
                      $r['country'], $r['web'], $r['business'], implode('; ', bf_machine_labels($r['machines'])), $r['news'] ? 'yes' : 'no',
                      implode('; ', $r['reasons']), $r['ip']]);
        flock($fh, LOCK_UN);
    }
    fclose($fh);
}

// at most 3 price lists by itself to one address a day, 10 to one IP an hour and 300 a day in all; the counts keep hashes only
function bf_rate_ok(string $email, string $ip): bool {
    global $PRIV;
    if (!is_dir($PRIV) && !@mkdir($PRIV, 0700, true)) { return true; }
    $fh = @fopen("$PRIV/rate.json", 'c+');
    if ($fh === false) { return true; }
    if (!flock($fh, LOCK_EX)) { fclose($fh); return true; }
    $now = time();
    $log = json_decode((string)stream_get_contents($fh), true);
    $keep = [];
    foreach (is_array($log) ? $log : [] as $x) {
        if (is_array($x) && count($x) === 3 && (int)$x[0] > $now - 86400) { $keep[] = $x; }
    }
    $e = substr(hash('sha256', 'e|' . strtolower($email)), 0, 20);
    $i = substr(hash('sha256', 'i|' . $ip), 0, 20);
    $byE = 0; $byI = 0;
    foreach ($keep as $x) {
        if ($x[1] === $e) { $byE++; }
        if ($x[2] === $i && (int)$x[0] > $now - 3600) { $byI++; }
    }
    $ok = $byE < 3 && $byI < 10 && count($keep) < 300;
    if ($ok) { $keep[] = [$now, $e, $i]; }
    ftruncate($fh, 0); rewind($fh); fwrite($fh, (string)json_encode($keep)); fflush($fh);
    flock($fh, LOCK_UN); fclose($fh);
    return $ok;
}

// the machines of the price list by id: ['xl-30135' => ['name' => …, 'type' => …, 'price' => …], …]
function bf_machines(): array {
    global $BF;
    $out = [];
    foreach ((array)($BF['machines'] ?? []) as $m) {
        if (is_array($m) && !empty($m['id'])) { $out[(string)$m['id']] = $m; }
    }
    return $out;
}

function bf_machine_labels(array $ids): array {
    $all = bf_machines();
    $out = [];
    foreach ($ids as $id) {
        if ($id === 'factory-order') { $out[] = 'Factory order (another size or model, 5% off)'; continue; }
        $m = $all[$id] ?? null;
        $out[] = $m ? trim(($m['name'] ?? $id) . (!empty($m['type']) ? ' — ' . $m['type'] : '')) : strtoupper(str_replace('-', ' ', $id));
    }
    return $out;
}

// ------------------------------------------------------------------------------------------------ the e-mails
// the price list to the buyer: HTML with a plain-text twin, the PDF attached. False when there is nothing to send.
function bf_send_offer(array $r): bool {
    global $BF, $MAIL, $PRIV, $PAGE, $REPLY_FROM;
    if (!isset($MAIL['bf_offer'], $MAIL['bf_offer_text'])) { return false; }
    $pdf = (string)($BF['pdf'] ?? '');
    $pdfPath = $pdf !== '' ? $PRIV . '/' . basename($pdf) : '';
    $hasPdf = $pdfPath !== '' && is_file($pdfPath) && filesize($pdfPath) > 0;
    $all = bf_machines();
    $priced = array_filter($all, static function ($m) { return !empty($m['price']); });
    if (!$hasPdf && !$priced) { return false; }

    $first = bf_first_name($r['name']);
    $picked = array_values(array_filter($r['machines'], static function ($id) use ($all) { return isset($all[$id]) || $id === 'factory-order'; }));
    $row = static function (string $k, string $v) use ($MAIL): string { return nt_fill($MAIL['summary_row'], ['K' => nt_e($k), 'V' => $v]); };
    $pickedHtml = $pickedText = '';
    if ($picked) {
        $rows = '';
        foreach (bf_machine_labels($picked) as $i => $label) { $rows .= $row($i === 0 ? 'You asked about' : '', nt_machine($label)); }
        $pickedHtml = nt_fill($MAIL['box'], ['TITLE' => 'Your request', 'BODY' => nt_fill($MAIL['rows_table'], ['ROWS' => $rows])]);
        $pickedText = "You asked about:\n- " . implode("\n- ", bf_machine_labels($picked)) . "\n\n";
    }
    $pricesHtml = $pricesText = '';
    if ($priced) {
        $rows = '';
        $lines = [];
        foreach ($priced as $id => $m) {
            $mine = in_array($id, $picked, true);
            $qty = (int)($m['qty'] ?? 0);
            $rows .= nt_fill($MAIL['bf_price_row'], [
                'MARK'    => $mine ? $MAIL['bf_mark'] : '',
                'MODEL'   => nt_machine((string)($m['name'] ?? $id)),
                'TYPE'    => nt_e((string)($m['type'] ?? '')),
                'REGULAR' => !empty($m['regular']) ? '<span style="color:#5A5D62;text-decoration:line-through;">' . nt_e((string)$m['regular']) . '</span><br>' : '',
                'PRICE'   => nt_e((string)$m['price']),
                'QTY'     => $qty > 1 ? '<br><span style="font-size:12px;color:#5A5D62;">' . $qty . ' in stock</span>' : '',
            ]);
            $lines[] = '- ' . ($m['name'] ?? $id) . (!empty($m['type']) ? ', ' . $m['type'] : '') . ': ' . $m['price']
                     . (!empty($m['regular']) ? ' (regular ' . $m['regular'] . ')' : '');
        }
        $pricesHtml = nt_fill($MAIL['bf_prices_box'], [
            'TITLE' => 'Black Friday prices · in stock in Mississauga, ON',
            'ROWS'  => $rows,
            'NOTE'  => ($picked ? '&#9632; = the machines you asked about. ' : '') . 'Prices in CAD, plus applicable taxes; freight, installation and training extra.'
                     . ($hasPdf ? ' Full specifications in the attached PDF.' : ''),
        ]);
        $pricesText = "Black Friday prices (in stock in Mississauga, ON; CAD, plus applicable taxes):\n" . implode("\n", $lines) . "\n\n";
    }
    $attached = $hasPdf ? 'Your Black Friday price list is attached, with the sale price and the full specifications of every machine in stock. ' : '';
    list($src, $images) = nt_images($MAIL['bf_offer']);
    $html = nt_fill($MAIL['bf_offer'], $src + [
        'COMMA_NAME' => $first !== '' ? ', ' . nt_e($first) : '',
        'ATTACHED'   => nt_e($attached),
        'PICKED'     => $pickedHtml,
        'PRICES'     => $pricesHtml,
        'PAGE_URL'   => nt_e($PAGE),
    ]);
    $text = nt_fill($MAIL['bf_offer_text'], [
        'COMMA_NAME'    => $first !== '' ? ", $first" : '',
        'ATTACHED_TEXT' => $attached,
        'PICKED_TEXT'   => $pickedText,
        'PRICES_TEXT'   => $pricesText,
        'PAGE_URL'      => $PAGE,
    ]);
    $alt = 'NTB-' . bin2hex(random_bytes(12));
    $headers = [
        "From: NovoTech Machine Tools <$REPLY_FROM>",
        "Reply-To: NovoTech Machine Tools <$REPLY_FROM>",
        "MIME-Version: 1.0",
        "Auto-Submitted: auto-replied",
        "X-Mailer: NovoTech-black-friday",
    ];
    if ($hasPdf) {
        $mix = 'NTM-' . bin2hex(random_bytes(12));
        $name = (string)preg_replace('/[^A-Za-z0-9._ ()-]+/', '_', (string)($BF['pdf_name'] ?? basename($pdfPath)));
        $headers[] = "Content-Type: multipart/mixed; boundary=\"$mix\"";
        $body = "This is a multi-part message in MIME format.\r\n\r\n--$mix\r\nContent-Type: multipart/alternative; boundary=\"$alt\"\r\n\r\n"
              . nt_alternative($text, $html, $alt, $images)
              . "--$mix\r\nContent-Type: application/pdf; name=\"$name\"\r\nContent-Transfer-Encoding: base64\r\n"
              . "Content-Disposition: attachment; filename=\"$name\"\r\n\r\n"
              . chunk_split(base64_encode((string)file_get_contents($pdfPath)), 76, "\r\n")
              . "--$mix--\r\n";
    } else {
        $headers[] = "Content-Type: multipart/alternative; boundary=\"$alt\"";
        $body = "This is a multi-part message in MIME format.\r\n\r\n" . nt_alternative($text, $html, $alt, $images);
    }
    $subject = '=?UTF-8?B?' . base64_encode('Your Black Friday price list | NovoTech Machine Tools') . '?=';
    return @mail($r['email'], $subject, $body, implode("\r\n", $headers), "-f$REPLY_FROM");
}

// the copy to info@: what the site did, with every detail of the buyer, the reasons when it waits, and the review link
function bf_notify(array $r, string $status): bool {
    global $MAIL, $TO, $FROM, $PHONE;
    $link = static function (string $href, string $label) use ($MAIL): string { return nt_fill($MAIL['link'], ['HREF' => nt_e($href), 'LABEL' => nt_e($label)]); };
    $row = static function (string $k, string $v) use ($MAIL): string { return nt_fill($MAIL['summary_row'], ['K' => nt_e($k), 'V' => $v]); };
    $box = static function (string $title, string $body) use ($MAIL): string { return nt_fill($MAIL['box'], ['TITLE' => nt_e($title), 'BODY' => $body]); };
    $tel = (string)preg_replace('/[^0-9+]/', '', $r['phone']);
    $web = $r['web'] !== '' ? (preg_match('#^https?://#i', $r['web']) ? $r['web'] : 'https://' . $r['web']) : '';
    $machines = bf_machine_labels($r['machines']);
    $rows = $row('Email', $link('mailto:' . str_replace('%40', '@', rawurlencode($r['email'])), $r['email']))
          . $row('Phone', strlen($tel) >= 7 ? $link("tel:$tel", $r['phone']) : nt_e($r['phone']))
          . $row('Business', nt_e($r['business']))
          . $row('Location', nt_e(implode(', ', array_filter([$r['city'], $r['region'], $r['country']]))))
          . ($web !== '' && filter_var($web, FILTER_VALIDATE_URL) ? $row('Website', $link($web, $r['web'])) : ($r['web'] !== '' ? $row('Website', nt_e($r['web'])) : ''))
          . $row('Machines', $machines ? implode('<br>', array_map('nt_machine', $machines)) : nt_fill($MAIL['muted'], ['T' => 'none ticked']))
          . $row('Own use', $r['own_use'] ? 'Confirmed: buying for use in own business' : '<span style="color:#B3261E;">Not confirmed</span>')
          . $row('Offers and news', $r['news'] ? 'Yes, may be emailed offers' : 'No')
          . $row('Received', nt_e($r['when']));
    $sent = $status === 'sent' || $status === 'approved';
    if ($sent) {
        $label = $status === 'approved' ? 'Price list sent (approved)' : 'Price list sent automatically';
        $about = 'Black Friday price list sent to <b style="color:#FFFFFF;">' . nt_e($r['email']) . '</b>';
    } elseif ($status === 'failed') {
        $label = 'Black Friday — not sent';
        $about = '<b style="color:#FFFFFF;">The price list could not be sent</b> (no price list on the server, or the mail server refused it). Please send it by hand.';
    } else {
        $label = 'Black Friday — on hold';
        $about = '<b style="color:#FFFFFF;">On hold — nothing was sent.</b> Check the reasons below before sending the price list.';
    }
    $reasons = $r['reasons'] ? $box('Why it is on hold', nt_fill($MAIL['text_block'], ['TEXT' => implode('<br>', array_map(static function ($x) { return '&#9632; ' . nt_e($x); }, $r['reasons']))])) : '';
    $msg = $r['message'] !== '' ? nl2br(nt_e($r['message']), false) : nt_fill($MAIL['muted'], ['T' => 'No message']);
    $tok = bf_token($r['id']);
    $review = (!$sent && $tok !== '' && !empty($r['saved']))
        ? 'https://novotechmachinetools.com/bf-quote.php?review=' . rawurlencode($r['id']) . '&t=' . $tok : '';
    $buttons = ($review !== '' ? nt_fill($MAIL['button'], ['HREF' => nt_e($review), 'LABEL' => 'Review and send the price list']) : '')
             . (strlen($tel) >= 7 ? nt_fill($review !== '' ? $MAIL['button_ghost'] : $MAIL['button'], ['HREF' => nt_e("tel:$tel"), 'LABEL' => 'Call ' . nt_e($r['phone'])]) : '');
    list($src, $images) = nt_images($MAIL['notify']);
    $html = nt_fill($MAIL['notify'], $src + [
        'LABEL'   => nt_e($label),
        'PRE'     => nt_e(($sent ? 'Price list sent: ' : 'On hold: ') . $r['name'] . ' · ' . $r['company']),
        'NAME'    => nt_e($r['name']),
        'COMPANY' => nt_fill($MAIL['notify_company'], ['T' => nt_e($r['company'])]),
        'ABOUT'   => $about,
        'DETAILS' => $reasons . $box('Details', nt_fill($MAIL['rows_table'], ['ROWS' => $rows])),
        'MESSAGE' => $box('Message', nt_fill($MAIL['text_block'], ['TEXT' => $msg])),
        'FILES'   => '',
        'BUTTONS' => $buttons,
        'FOOTER'  => 'Black Friday instant quote · request ' . nt_e($r['id']) . ' · IP ' . nt_e($r['ip'])
                   . ($review === '' && !$sent ? '<br>To send the price list, reply to the customer with the PDF attached.' : ''),
    ]);
    $text = "Black Friday instant quote — " . ($sent ? "price list sent to {$r['email']}" : ($status === 'failed' ? 'NOT SENT' : 'ON HOLD, nothing sent')) . "\n\n"
          . ($r['reasons'] ? "Why it is on hold:\n- " . implode("\n- ", $r['reasons']) . "\n\n" : '')
          . "Name:      {$r['name']}\nCompany:   {$r['company']}\nEmail:     {$r['email']}\nPhone:     {$r['phone']}\n"
          . "Business:  {$r['business']}\nLocation:  " . implode(', ', array_filter([$r['city'], $r['region'], $r['country']])) . "\n"
          . "Website:   {$r['web']}\nMachines:  " . implode('; ', $machines) . "\nOwn use:   " . ($r['own_use'] ? 'confirmed' : 'NOT confirmed') . "\n"
          . "News:      " . ($r['news'] ? 'yes' : 'no') . "\nReceived:  {$r['when']}\n\nMessage:\n{$r['message']}\n\n"
          . ($review !== '' ? "Review and send: $review\n" : '') . "Request {$r['id']}, IP {$r['ip']}\n";
    $alt = 'NTN-' . bin2hex(random_bytes(12));
    $headers = [
        "From: NovoTech website <$FROM>",
        "Reply-To: " . nt_addr($r['name'], $r['email']),
        "MIME-Version: 1.0",
        "X-Mailer: NovoTech-black-friday",
        "Content-Type: multipart/alternative; boundary=\"$alt\"",
    ];
    $who = $r['company'] !== '' ? $r['company'] : $r['name'];
    $subject = $sent ? "Black Friday price list sent: $who" : ($status === 'failed' ? "Black Friday price list NOT sent: $who" : "ON HOLD — Black Friday request: $who");
    $subject = '=?UTF-8?B?' . base64_encode((string)preg_replace('/[\r\n]+/', ' ', $subject)) . '?=';
    return @mail($TO, $subject, "This is a multi-part message in MIME format.\r\n\r\n" . nt_alternative($text, $html, $alt, $images),
                 implode("\r\n", $headers), "-f$FROM");
}

// ------------------------------------------------------------------------------------------------ review and send (the owner)
// GET shows the request and a button; only the POST sends — e-mail scanners open links, and must never send a price list
if (isset($_GET['review']) || (($_POST['action'] ?? '') === 'approve')) {
    $id = (string)($_GET['review'] ?? $_POST['id'] ?? '');
    $t  = (string)($_GET['t'] ?? $_POST['t'] ?? '');
    $tok = bf_token($id);
    $r = $tok !== '' && hash_equals($tok, $t) ? bf_load($id) : null;
    if (!$r) { bf_page('Link not valid', '<p>This review link is not valid or the request is no longer on the server.</p>', 404); }
    $details = '<table style="border-collapse:collapse;margin:12px 0 18px">';
    foreach (['Name' => $r['name'], 'Company' => $r['company'], 'Email' => $r['email'], 'Phone' => $r['phone'], 'Business' => $r['business'],
              'Location' => implode(', ', array_filter([$r['city'], $r['region'], $r['country']])), 'Website' => $r['web'],
              'Machines' => implode('; ', bf_machine_labels($r['machines'])), 'Received' => $r['when']] as $k => $v) {
        $details .= '<tr><td style="padding:4px 14px 4px 0;color:#5A5D62;vertical-align:top">' . nt_e($k) . '</td><td style="padding:4px 0;font-weight:bold">' . nt_e((string)$v) . '</td></tr>';
    }
    $details .= '</table>';
    $why = $r['reasons'] ? '<p style="background:#FFF3E6;border-left:4px solid #F28A1F;padding:10px 14px">On hold because:<br>&#9632; '
         . implode('<br>&#9632; ', array_map('nt_e', $r['reasons'])) . '</p>' : '';
    if (!empty($r['sent_at'])) {
        bf_page('Already sent', '<p>The price list was sent to ' . nt_e($r['email']) . ' on ' . nt_e((string)$r['sent_at']) . '.</p>' . $details);
    }
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        bf_page('Send the Black Friday price list?', $why . $details
            . '<form method="post" action="bf-quote.php"><input type="hidden" name="action" value="approve"><input type="hidden" name="id" value="' . nt_e($id) . '">'
            . '<input type="hidden" name="t" value="' . nt_e($t) . '"><button type="submit" style="font:bold 18px Arial;padding:12px 26px;background:#F28A1F;border:0;border-radius:3px;cursor:pointer">'
            . 'Send the price list to ' . nt_e($r['email']) . '</button></form><p style="color:#5A5D62">Not sending it? Just close this page.</p>');
    }
    if (bf_send_offer($r)) {
        $r['status'] = 'approved';
        $r['sent_at'] = (new DateTime('now', new DateTimeZone('America/Toronto')))->format('F j, Y, g:i A T');
        bf_save($r);
        bf_log($r, 'sent after review');
        bf_page('Price list sent', '<p style="color:#2E7D32;font-weight:bold">The Black Friday price list is on its way to ' . nt_e($r['email']) . '.</p>' . $details);
    }
    bf_page('Not sent', '<p>The price list could not be sent: check that the PDF is in ~/novotech-private/black-friday/ and try again, or email it by hand.</p>' . $details, 500);
}

// ------------------------------------------------------------------------------------------------ the form
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'This address only accepts form submissions.', 405);
}
$f = static function (string $k, int $max = 300): string {
    $v = isset($_POST[$k]) && is_string($_POST[$k]) ? $_POST[$k] : '';
    return mb_substr(trim(str_replace(["\r", "\0"], '', $v)), 0, $max);
};
$thanks = 'Thanks — your request has been received.';
if ($f('website') !== '') { respond(true, $thanks); }                    // honeypot: pretend success to bots
$ts = (int)$f('ts', 20);
if ($ts > 0 && (time() - $ts) < $MIN_SECS) { respond(true, $thanks); }

if ($CAPTCHA !== '') {   // Google reCAPTCHA v3, as quote.php; the page asks for the action "bf_quote"
    $token = $f('g-recaptcha-response', 4000);
    $blocked = "Our spam filter could not confirm that this request was sent by a person. Please try again, or call $PHONE.";
    if ($token === '') { respond(false, $blocked, 422); }
    $post = http_build_query(['secret' => $CAPTCHA, 'response' => $token, 'remoteip' => $_SERVER['REMOTE_ADDR'] ?? '']);
    $raw = false;
    if (function_exists('curl_init')) {
        $ch = curl_init('https://www.google.com/recaptcha/api/siteverify');
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $post, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10]);
        $raw = curl_exec($ch);
        curl_close($ch);
    } else {
        $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => "Content-Type: application/x-www-form-urlencoded\r\n", 'content' => $post, 'timeout' => 10]]);
        $raw = @file_get_contents('https://www.google.com/recaptcha/api/siteverify', false, $ctx);
    }
    $res = is_string($raw) ? json_decode($raw, true) : null;
    $score = is_array($res) && isset($res['score']) ? (float)$res['score'] : 0.0;
    if (!is_array($res) || empty($res['success']) || ($res['action'] ?? 'bf_quote') !== 'bf_quote' || $score < $MIN_SCORE) {
        respond(false, $blocked, 422);
    }
}

$r = [
    'name' => $f('name', 120), 'company' => $f('company', 160), 'email' => $f('email', 160), 'phone' => $f('phone', 60),
    'city' => $f('city', 80), 'region' => $f('region', 80), 'country' => $f('country', 60), 'web' => $f('company_web', 200),
    'business' => $f('business', 80), 'message' => $f('message', 3000),
    'own_use' => $f('own_use', 2) === '1', 'news' => $f('news', 2) === '1',
    'machines' => [],
];
foreach ((array)($_POST['machines'] ?? []) as $m) {
    if (is_string($m) && preg_match('/^[a-z0-9-]{1,60}$/', $m) && count($r['machines']) < 30) { $r['machines'][] = $m; }
}
$r['machines'] = array_values(array_unique($r['machines']));
foreach (['name', 'company', 'email', 'phone', 'city', 'region', 'country', 'web', 'business'] as $k) {
    if (preg_match('/[\r\n]/', $r[$k])) { respond(false, 'Invalid input.', 422); }
}
if ($r['name'] === '' || $r['company'] === '' || !filter_var($r['email'], FILTER_VALIDATE_EMAIL) || strlen(bf_digits($r['phone'])) < 7
    || $r['city'] === '' || $r['region'] === '' || $r['business'] === '') {
    respond(false, 'Please fill in the fields marked required, with a valid email address and phone number.', 422);
}
if (!$r['own_use']) {
    respond(false, 'Please confirm that you are buying for use in your own business.', 422);
}

$now = new DateTime('now', new DateTimeZone('America/Toronto'));
$r['when'] = $now->format('F j, Y, g:i A T');
$r['id'] = $now->format('Ymd-His') . '-' . bin2hex(random_bytes(4));
$r['ip'] = (string)($_SERVER['REMOTE_ADDR'] ?? '?');

// ------------------------------------------------------------------------------------------------ the checks
$reasons = [];
$domain = bf_domain($r['email']);
$webDomain = bf_domain($r['web']);
$lists = [
    'a NovoTech supplier'   => (array)($BF['suppliers'] ?? []),
    'a competitor'          => (array)($BF['competitors'] ?? []),
];
foreach ($lists as $who => $words) {
    if ($w = bf_match($words, $domain, $r['company'])) { $reasons[] = "Email domain or company name matches $who: \"$w\""; }
    elseif ($webDomain !== '' && ($w = bf_match($words, $webDomain, ''))) { $reasons[] = "Website matches $who: \"$w\""; }
}
foreach ((array)($BF['competitor_emails'] ?? []) as $e) {
    if (strcasecmp(trim((string)$e), $r['email']) === 0) { $reasons[] = 'Email address is on the competitor list'; break; }
}
$pd = bf_digits($r['phone']);
foreach ((array)($BF['competitor_phones'] ?? []) as $p) {
    $cd = bf_digits((string)$p);
    if (strlen($cd) >= 7 && strlen($pd) >= 7 && (substr($pd, -strlen($cd)) === $cd || substr($cd, -strlen($pd)) === $pd)) {
        $reasons[] = 'Phone number is on the competitor list (' . $p . ')'; break;
    }
}
if (stripos($r['business'], 'dealer') !== false || stripos($r['business'], 'reseller') !== false) {
    $reasons[] = 'Says the company is a machinery dealer, distributor or reseller';
}
if ($w = bf_match((array)($BF['dealer_words'] ?? []), $domain . ' ' . $webDomain, $r['company'])) {
    $reasons[] = "Company name or domain suggests a machinery seller: \"$w\"";
}
$free = ['gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.ca', 'hotmail.com', 'hotmail.ca', 'outlook.com', 'live.com', 'live.ca', 'msn.com',
         'icloud.com', 'me.com', 'aol.com', 'proton.me', 'protonmail.com', 'gmx.com', 'mail.com', 'yandex.com', 'rogers.com', 'bell.net',
         'sympatico.ca', 'shaw.ca', 'telus.net', 'videotron.ca', 'cogeco.ca', 'qq.com', '163.com'];
$r['free_email'] = in_array($domain, $free, true);
if ($r['free_email'] && !empty($BF['hold_free_email'])) { $reasons[] = "Free email address ($domain)"; }
if (!$BF) { $reasons[] = 'The Black Friday settings (bf-config.php) are not on the server yet'; }
elseif (array_key_exists('auto_send', $BF) && !$BF['auto_send']) { $reasons[] = 'Automatic sending is switched off: every request waits for review'; }
if (!$reasons && !bf_rate_ok($r['email'], $r['ip'])) { $reasons[] = 'Too many price lists to this address or from this connection today'; }
$r['reasons'] = $reasons;

// ------------------------------------------------------------------------------------------------ send, or hold for review
$r['status'] = $reasons ? 'held' : 'sent';
if (!$reasons) {
    if (bf_send_offer($r)) {
        $r['sent_at'] = $r['when'];
    } else {
        $r['status'] = 'failed';
        $r['reasons'][] = 'The price list could not be sent automatically';
    }
}
$r['saved'] = bf_save($r);
bf_log($r, $r['status']);
bf_notify($r, $r['status']);

$first = bf_first_name($r['name']);
$hi = $first !== '' ? "Thanks, $first!" : 'Thank you!';
if ($r['status'] === 'sent') {
    respond(true, "$hi Your Black Friday price list is on its way to {$r['email']}. It usually arrives within a few minutes — if you don't see it, check your spam folder or call $PHONE.");
}
respond(true, "$hi We received your request. A NovoTech specialist will email your Black Friday pricing shortly.");
