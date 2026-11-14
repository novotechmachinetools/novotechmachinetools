<?php
/* One-time installer (Nov 14 2026): puts the private Black Friday files (settings, price list PDF, the price list of the
   e-mail) into ~/novotech-private/black-friday, then deletes itself. It accepts only these three files, identified by their
   SHA-256, and only with the token whose SHA-256 is below. Nothing else is read or written. */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
$TOKEN = 'd53cc36e52716e0bf861db58b12e98801054632f2402a7bfbcdbb1089c7ec258';
$FILES = [
    'f1' => ['bf-config.php', 'b83ad902bce480c5158b3cf89c9eb9f5b3cd6c2350af82c9d56345a1b7844b29'],
    'f2' => ['NovoTech-Black-Friday-2026-Price-List.pdf', 'f58bfd102e6b8d0b1f324f82393283d8e0eb883d727e39728964aec8bbc36cfd'],
    'f3' => ['bf-mail-list.json', '700fb16653efee3026e5f0148889bcad69b8ef0ba0bb73aecc7de2aa9adcd489'],
];
function out(int $code, array $a): void { http_response_code($code); echo json_encode($a); exit; }
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { out(404, ['ok' => false]); }
if (!hash_equals($TOKEN, hash('sha256', (string)($_POST['token'] ?? '')))) { out(404, ['ok' => false]); }
$home = (string)preg_replace('#/public_html(?:/.*)?$#', '', __DIR__);
if ($home === __DIR__) { $home = dirname(__DIR__); }
$dir = $home . '/novotech-private/black-friday';
if (!is_dir($dir) && !@mkdir($dir, 0700, true)) { out(500, ['ok' => false, 'error' => 'no private folder']); }
foreach ($FILES as $field => [$name, $sha]) {
    $f = $_FILES[$field] ?? null;
    if (!is_array($f) || ($f['error'] ?? 1) !== UPLOAD_ERR_OK || !is_uploaded_file((string)$f['tmp_name'])) {
        out(400, ['ok' => false, 'error' => "missing $name", 'code' => is_array($f) ? ($f['error'] ?? null) : null]);
    }
    if (!hash_equals($sha, (string)hash_file('sha256', (string)$f['tmp_name']))) { out(400, ['ok' => false, 'error' => "checksum $name"]); }
}
$done = [];
foreach ($FILES as $field => [$name, $sha]) {
    $dst = "$dir/$name";
    if (is_file($dst)) { @copy($dst, "$dst.bak"); @chmod("$dst.bak", 0600); }
    $tmp = "$dst.new";
    if (!move_uploaded_file((string)$_FILES[$field]['tmp_name'], $tmp)) { out(500, ['ok' => false, 'error' => "write $name"]); }
    @chmod($tmp, 0600);
    if (!rename($tmp, $dst)) { out(500, ['ok' => false, 'error' => "rename $name"]); }
    $done[$name] = ['bytes' => filesize($dst), 'sha256' => substr((string)hash_file('sha256', $dst), 0, 16)];
}
$gone = @unlink(__FILE__);
out(200, ['ok' => true, 'files' => $done, 'self_deleted' => $gone]);
