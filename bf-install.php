<?php
/* One-time installer, Black Friday 2026 (Nov 14): saves the two private Black Friday files — bf-config.php and the price-list
   PDF — into ~/novotech-private/black-friday, outside public_html, where bf-quote.php reads them.
   It accepts only a POST carrying the secret whose SHA-256 is TOKEN_SHA256, and only files whose content matches the SHA-256
   pinned below byte for byte, so it can write nothing else. It deletes itself after a successful run, and the next deploy
   (rsync --delete) would remove it anyway. Any other request gets a plain 404. */
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
const TOKEN_SHA256 = 'cffbf0cb6232939186481fea69e72b4e0a4ecb8d9e93de7e4a9b1e48b690c196';
const FILES = [
    'bf-config.php' => '4f9980978b0bc7c67932340745110f676142f23e92d92579e2f9a28a590ad6d4',
    'NovoTech-Black-Friday-2026-Price-List.pdf' => '24237ed9223416e1bc85a02c259f226360a565c0ba3c848311b6de11d2e82b9a',
];
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST' || !hash_equals(TOKEN_SHA256, hash('sha256', (string)($_POST['token'] ?? '')))) {
    http_response_code(404);
    exit("Not found\n");
}
$home = (string)preg_replace('#/public_html(?:/.*)?$#', '', __DIR__);
$base = ($home !== __DIR__ ? $home : dirname(__DIR__)) . '/novotech-private';
$dir = $base . '/black-friday';
if (!is_dir($dir) && !mkdir($dir, 0700, true)) { http_response_code(500); exit("cannot create the private folder\n"); }
@chmod($base, 0700);
@chmod($dir, 0700);
$f = $_FILES['files'] ?? ['name' => []];
if (!is_array($f['name'] ?? null)) { $f = ['name' => []]; }
$saved = 0;
$out = ["folder ~/novotech-private/black-friday"];
foreach ($f['name'] as $i => $name) {
    $name = basename((string)$name);
    $want = FILES[$name] ?? null;
    if ($want === null) { $out[] = "rejected $name (not one of the two files)"; continue; }
    if (($f['error'][$i] ?? 1) !== UPLOAD_ERR_OK) { $out[] = "rejected $name (upload error " . (int)($f['error'][$i] ?? -1) . ")"; continue; }
    $got = hash_file('sha256', (string)$f['tmp_name'][$i]);
    if (!hash_equals($want, (string)$got)) { $out[] = "rejected $name (content does not match)"; continue; }
    $dest = "$dir/$name";
    if (!move_uploaded_file((string)$f['tmp_name'][$i], $dest)) { $out[] = "failed $name"; continue; }
    @chmod($dest, 0600);
    $saved++;
    $out[] = "saved $name " . filesize($dest) . " bytes sha256 " . substr((string)hash_file('sha256', $dest), 0, 16);
}
// The server's PHP takes uploads of up to 2 MB per file, so the price-list PDF may also arrive in parts ("parts[]", in order):
// they are joined and kept only if the whole file matches its pinned SHA-256.
$p = $_FILES['parts'] ?? null;
if (is_array($p) && is_array($p['name'] ?? null) && count($p['name']) > 0) {
    $pdf = 'NovoTech-Black-Friday-2026-Price-List.pdf';
    $tmp = "$dir/.$pdf.part";
    $fh = fopen($tmp, 'wb');
    $ok = $fh !== false;
    foreach ($p['tmp_name'] as $i => $t) {
        if (!$ok) { break; }
        if (($p['error'][$i] ?? 1) !== UPLOAD_ERR_OK) { $out[] = "rejected part $i (upload error " . (int)($p['error'][$i] ?? -1) . ")"; $ok = false; break; }
        $ok = fwrite($fh, (string)file_get_contents((string)$t)) !== false;
    }
    if ($fh !== false) { fclose($fh); }
    if ($ok && hash_equals(FILES[$pdf], (string)hash_file('sha256', $tmp)) && rename($tmp, "$dir/$pdf")) {
        @chmod("$dir/$pdf", 0600);
        $out[] = "saved $pdf " . filesize("$dir/$pdf") . " bytes sha256 " . substr((string)hash_file('sha256', "$dir/$pdf"), 0, 16) . " (from " . count($p['name']) . " parts)";
    } else {
        @unlink($tmp);
        $out[] = "rejected $pdf parts (content does not match)";
    }
}
$complete = true;
foreach (FILES as $name => $want) {
    if (!is_file("$dir/$name") || !hash_equals($want, (string)hash_file('sha256', "$dir/$name"))) { $complete = false; }
}
if ($complete) { $out[] = @unlink(__FILE__) ? "installer removed itself" : "installer could not remove itself"; }
echo implode("\n", $out), "\n";
