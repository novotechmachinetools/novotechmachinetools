<?php
/* One-time installer (Nov 14 2026, second run): replaces the Black Friday price-list PDF in ~/novotech-private/black-friday
   (outside public_html, where bf-quote.php reads it) with the new edition. Only a POST carrying the secret whose SHA-256 is
   TOKEN_SHA256 is accepted, and only a file whose content matches PDF_SHA256 byte for byte, so it can write nothing else.
   It deletes itself after a successful run; the next deploy (rsync --delete) would remove it anyway. Anything else: 404. */
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
const TOKEN_SHA256 = 'aadc63788200dcee652e2ba9d2d45208f36e1a568813b22d820d15978cb64fef';
const PDF_NAME = 'NovoTech-Black-Friday-2026-Price-List.pdf';
const PDF_SHA256 = '3ca380dde199db89d642b34061a4fb5d6b0b485ffe2a6d4bd6c731968d1a1d17';
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST' || !hash_equals(TOKEN_SHA256, hash('sha256', (string)($_POST['token'] ?? '')))) {
    http_response_code(404);
    exit("Not found\n");
}
$home = (string)preg_replace('#/public_html(?:/.*)?$#', '', __DIR__);
$dir = ($home !== __DIR__ ? $home : dirname(__DIR__)) . '/novotech-private/black-friday';
if (!is_dir($dir)) { http_response_code(500); exit("private folder missing\n"); }
$f = $_FILES['pdf'] ?? null;
if (!is_array($f) || ($f['error'] ?? 1) !== UPLOAD_ERR_OK) { http_response_code(400); exit('upload error ' . (int)($f['error'] ?? -1) . "\n"); }
if (!hash_equals(PDF_SHA256, (string)hash_file('sha256', (string)$f['tmp_name']))) { http_response_code(400); exit("rejected: content does not match\n"); }
$tmp = "$dir/." . PDF_NAME . '.new';
if (!move_uploaded_file((string)$f['tmp_name'], $tmp) || !rename($tmp, "$dir/" . PDF_NAME)) { http_response_code(500); exit("could not save\n"); }
@chmod("$dir/" . PDF_NAME, 0600);
echo 'saved ' . PDF_NAME . ' ' . filesize("$dir/" . PDF_NAME) . ' bytes sha256 ' . substr((string)hash_file('sha256', "$dir/" . PDF_NAME), 0, 16) . "\n";
echo @unlink(__FILE__) ? "installer removed itself\n" : "installer could not remove itself\n";
