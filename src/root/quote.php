<?php
/**
 * NovoTech quote-request handler.
 * Receives the form on each product page, checks it (honeypot, time to submit, Google reCAPTCHA, attachments) and emails it
 * to the sales inbox with the customer's drawings and photos attached.
 * Works with the JavaScript submit (returns JSON) and with a plain HTML POST (returns a small page).
 *
 * reCAPTCHA: put the secret key in form-config.php next to this file (copy form-config.sample.php). form-config.php is
 * never committed to Git. Without a secret the check is skipped, so the form keeps working until the keys are set.
 */
declare(strict_types=1);

$TO        = 'info@NovoTechMachineTools.com';
$FROM      = 'website@novotechmachinetools.com';   // must be a mailbox on this domain for HostPapa's mail server
$SUBJECT   = 'Quote request from NovoTechMachineTools.com';
$MIN_SECS  = 4;                                     // forms submitted faster than this are bots
$MAX_FILES = 5;
$MAX_BYTES = 10 * 1024 * 1024;                      // all attachments together
$OK_EXT    = ['pdf', 'dwg', 'dxf', 'step', 'stp', 'igs', 'iges', 'sldprt', 'x_t', 'jpg', 'jpeg', 'png', 'heic', 'webp', 'zip',
              'xls', 'xlsx', 'doc', 'docx', 'txt', 'csv'];

$cfgFile = __DIR__ . '/form-config.php';
$cfg = is_file($cfgFile) ? (array)(require $cfgFile) : [];
$SECRET = (string)($cfg['recaptcha_secret'] ?? '');

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
        echo "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><meta name=\"robots\" content=\"noindex\"><title>$title — NovoTech Machine Tools</title>"
           . "<body style=\"font-family:Arial,sans-serif;max-width:40em;margin:3em auto;padding:0 1em;line-height:1.5\"><h1>$title</h1><p>" . htmlspecialchars($msg, ENT_QUOTES, 'UTF-8') . "</p>"
           . "<p><a href=\"javascript:history.back()\">Go back</a> · <a href=\"/\">NovoTech home</a></p></body></html>";
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'This address only accepts form submissions.', 405);
}

// A request larger than PHP's post_max_size arrives with $_POST and $_FILES empty.
if (empty($_POST) && (int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 0) {
    respond(false, 'The attached files are too large. Please keep attachments under 10 MB in total, or email larger files to info@NovoTechMachineTools.com.', 413);
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

// Google reCAPTCHA v2
if ($SECRET !== '') {
    $token = $f('g-recaptcha-response', 4000);
    if ($token === '') {
        respond(false, 'Please tick “I’m not a robot” and send the form again.', 422);
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
    if (!is_array($res) || empty($res['success'])) {
        respond(false, 'The “I’m not a robot” check did not go through. Please tick it again and send the form.', 422);
    }
}

$name    = $f('name', 120);
$company = $f('company', 160);
$email   = $f('email', 160);
$phone   = $f('phone', 60);
$machine = $f('machine', 200);
$message = $f('message', 4000);
$page    = $f('page', 200);

if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Please add your name and a valid email address.', 422);
}
foreach ([$name, $company, $email, $phone, $machine, $page] as $v) {
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
            respond(false, 'One of the files is too large. Please keep attachments under 10 MB in total, or email larger files to info@NovoTechMachineTools.com.', 413);
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
            respond(false, 'The files add up to more than 10 MB. Please send fewer or smaller files, or email them to info@NovoTechMachineTools.com.', 413);
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

$lines = [
    "Quote request from " . ($page !== '' ? $page : 'NovoTechMachineTools.com'),
    "",
    "Name:     $name",
    "Company:  $company",
    "Email:    $email",
    "Phone:    $phone",
    "Machine:  $machine",
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
$lines[] = "Sent " . date('Y-m-d H:i:s T') . " from IP " . ($_SERVER['REMOTE_ADDR'] ?? '?');
$lines[] = "Page: " . ($_SERVER['HTTP_REFERER'] ?? '?');
$text = implode("\n", $lines);

$headers = [
    "From: NovoTech website <$FROM>",
    "Reply-To: " . ($name !== '' ? "$name <$email>" : $email),
    "MIME-Version: 1.0",
    "X-Mailer: NovoTech-quote-form",
];
if ($files) {
    $boundary = 'NT-' . bin2hex(random_bytes(12));
    $headers[] = "Content-Type: multipart/mixed; boundary=\"$boundary\"";
    $body = "This is a multi-part message in MIME format.\r\n\r\n"
          . "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n"
          . str_replace("\n", "\r\n", $text) . "\r\n";
    foreach ($files as $a) {
        $body .= "--$boundary\r\n"
               . "Content-Type: {$a['mime']}; name=\"{$a['name']}\"\r\n"
               . "Content-Transfer-Encoding: base64\r\n"
               . "Content-Disposition: attachment; filename=\"{$a['name']}\"\r\n\r\n"
               . chunk_split(base64_encode($a['data']), 76, "\r\n");
    }
    $body .= "--$boundary--\r\n";
} else {
    $headers[] = "Content-Type: text/plain; charset=UTF-8";
    $body = $text;
}
$subject = $SUBJECT . ($machine !== '' ? " — $machine" : '') . ($files ? ' (' . count($files) . ' file' . (count($files) > 1 ? 's' : '') . ' attached)' : '');
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$sent = @mail($TO, $subject, $body, implode("\r\n", $headers), "-f$FROM");

if ($sent) {
    respond(true, 'Thanks — your request is on its way. We will reply within one business day.');
}
respond(false, 'The message could not be sent from the website. Please email info@NovoTechMachineTools.com or call +1 647 526 5510.', 500);
