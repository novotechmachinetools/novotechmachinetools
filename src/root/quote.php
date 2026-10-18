<?php
/**
 * NovoTech quote-request handler.
 * Receives the form on each product page, validates it and emails it to the sales inbox.
 * Works with the JavaScript submit (returns JSON) and with a plain HTML POST (returns a small page).
 */
declare(strict_types=1);

$TO       = 'info@NovoTechMachineTools.com';
$FROM     = 'website@novotechmachinetools.com';   // must be a mailbox on this domain for HostPapa's mail server
$SUBJECT  = 'Quote request from NovoTechMachineTools.com';
$MIN_SECS = 4;                                      // forms submitted faster than this are bots

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
           . "<p><a href=\"javascript:history.back()\">Go back</a> · <a href=\"index.html\">NovoTech home</a></p></body></html>";
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'This address only accepts form submissions.', 405);
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
    "----",
    "Sent " . date('Y-m-d H:i:s T') . " from IP " . ($_SERVER['REMOTE_ADDR'] ?? '?'),
    "Page: " . ($_SERVER['HTTP_REFERER'] ?? '?'),
];
$body = implode("\n", $lines);

$headers = [
    "From: NovoTech website <$FROM>",
    "Reply-To: " . ($name !== '' ? "$name <$email>" : $email),
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "X-Mailer: NovoTech-quote-form",
];
$subject = $SUBJECT . ($machine !== '' ? " — $machine" : '');
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$sent = @mail($TO, $subject, $body, implode("\r\n", $headers), "-f$FROM");

if ($sent) {
    respond(true, 'Thanks — your request is on its way. We will reply within one business day.');
}
respond(false, 'The message could not be sent from the website. Please email info@NovoTechMachineTools.com or call +1 647 526 5510.', 500);
