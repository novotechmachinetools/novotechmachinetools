<?php
/**
 * The e-mail helpers shared by quote.php (the quote form) and ask.php (the AI chat's contact requests): escaping, filling
 * the designs of quote-mail.php, addresses, multipart bodies and the pictures that travel inside the e-mails.
 * Read by those two only; never served (.htaccess).
 */
if (!defined('NT_QUOTE')) { http_response_code(404); exit; }

function nt_e(string $s): string {
    return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

// a machine name for HTML: escaped, and a number keeps its unit on the same line ("20 ft", "300 t")
function nt_machine(string $s): string {
    return (string)preg_replace('/(\d) (?=(ft|in|mm|m|t|ga|US)\b)/u', '$1&nbsp;', nt_e($s));
}

// fills the {{KEY}} placeholders of a design in one pass, so a value can never bring in another placeholder
function nt_fill(string $tpl, array $v): string {
    $map = [];
    foreach ($v as $k => $x) { $map['{{' . $k . '}}'] = (string)$x; }
    return strtr($tpl, $map);
}

// "Name" <address> for a header: quoted, or encoded when the name is not plain ASCII
function nt_addr(string $name, string $email): string {
    if ($name === '') { return $email; }
    $n = preg_match('/^[\x20-\x7E]*$/', $name) ? '"' . addcslashes($name, '"\\') . '"' : '=?UTF-8?B?' . base64_encode($name) . '?=';
    return "$n <$email>";
}

// a plain-text and an HTML part as one multipart/alternative body; the Content-Type header names the boundary $b. The HTML
// part carries its pictures with it (multipart/related, from nt_images)
function nt_alternative(string $text, string $html, string $b, array $images = []): string {
    $part = "Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html), 76, "\r\n");
    if ($images) {
        $r = 'NTI-' . bin2hex(random_bytes(12));
        $rel = "Content-Type: multipart/related; type=\"text/html\"; boundary=\"$r\"\r\n\r\n--$r\r\n" . $part;
        foreach ($images as $im) {
            $rel .= "--$r\r\nContent-Type: {$im['mime']}; name=\"{$im['name']}\"\r\nContent-Transfer-Encoding: base64\r\n"
                  . "Content-ID: <{$im['cid']}>\r\nContent-Disposition: inline; filename=\"{$im['name']}\"\r\n\r\n"
                  . chunk_split(base64_encode($im['data']), 76, "\r\n");
        }
        $part = $rel . "--$r--\r\n";
    }
    return "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n"
         . quoted_printable_encode(str_replace("\n", "\r\n", $text)) . "\r\n"
         . "--$b\r\n" . $part
         . "--$b--\r\n";
}

// the pictures a template names ({{LOGO}}, {{SIG}}, {{ICON_…}}) go inside the e-mail, because Outlook does not download
// pictures from the internet by itself (the owner, Nov 9 2026): [placeholder => "cid:…", the parts for nt_alternative].
// A picture missing on the server is linked from the site instead.
function nt_images(string $tpl): array {
    $src = [];
    $parts = [];
    $all = function_exists('nt_mail_images') ? nt_mail_images() : [];
    foreach ($all as $k => $im) {
        if (strpos($tpl, '{{' . $k . '}}') === false) { continue; }
        $file = __DIR__ . '/' . $im[0];
        $data = is_file($file) ? (string)file_get_contents($file) : '';
        if ($data === '') { $src[$k] = 'https://novotechmachinetools.com/' . $im[0]; continue; }
        $cid = strtolower(str_replace('_', '-', $k)) . '@novotechmachinetools.com';
        $src[$k] = "cid:$cid";
        $parts[] = ['cid' => $cid, 'mime' => $im[1], 'name' => basename($im[0]), 'data' => $data];
    }
    return [$src, $parts];
}
