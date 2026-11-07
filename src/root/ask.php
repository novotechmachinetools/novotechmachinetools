<?php
/**
 * NovoTech AI machine finder — the conversational answer on the live site.
 *
 * The finder panel (js/ai.js) answers every question at once from the site's machine index (ai/catalogue.json, written
 * by the site build) and shows the best match and the similar machines. On the live server it also sends the question
 * here, with the conversation so far and the ids of the machines its own engine found most relevant; this script gives
 * Claude a one-line index of every machine on the site plus the full details (spec tables, features, options) of those
 * candidates, and returns Claude's answer and the machines it recommends, which the page shows as cards.
 *
 * Setup on the web server: copy ai-config.sample.php to ai-config.php and put the API key in it. Without a key the
 * endpoint answers {"error":"not_configured"} and the panel keeps its built-in answer.
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

$config = __DIR__ . '/ai-config.php';
$cfg = is_file($config) ? (include $config) : [];
$API_KEY   = $cfg['api_key']   ?? '';
$MODEL     = $cfg['model']     ?? 'claude-sonnet-5-5';
$MAX_TOK   = (int)($cfg['max_tokens'] ?? 900);
$RATE_N    = (int)($cfg['rate_limit'] ?? 40);        // questions per IP per window
$RATE_SECS = (int)($cfg['rate_window'] ?? 600);      // window length in seconds

function fail(string $code, string $msg, int $http = 200): void {
    http_response_code($http);
    echo json_encode(['error' => $code, 'message' => $msg]);
    exit;
}

$CLI = PHP_SAPI === 'cli';    // php ask.php < request.json prints the prompt it would send (a check before going live)
if (!$CLI && ($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    fail('method', 'POST only', 405);
}
if (!$CLI && ($API_KEY === '' || strpos($API_KEY, '...') !== false)) {
    fail('not_configured', 'The AI assistant is not configured on this server yet.');
}

// ---- simple per-IP rate limit (file based; fine for a product site)
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$bucket = sys_get_temp_dir() . '/novotech-ask-' . md5($ip) . '.json';
$now = time();
$hits = [];
if (is_file($bucket)) {
    $hits = json_decode((string)file_get_contents($bucket), true) ?: [];
    $hits = array_values(array_filter($hits, static fn($t) => $t > $now - $RATE_SECS));
}
if (count($hits) >= $RATE_N) {
    fail('rate_limit', 'Too many questions in a short time — please try again in a few minutes.', 429);
}
$hits[] = $now;
@file_put_contents($bucket, json_encode($hits));

// ---- input
$raw = $CLI ? stream_get_contents(STDIN) : file_get_contents('php://input');
$in = json_decode((string)$raw, true);
if (!is_array($in) || !isset($in['messages']) || !is_array($in['messages'])) {
    fail('bad_request', 'Expected {"messages":[...]}', 400);
}
$messages = [];
foreach (array_slice($in['messages'], -12) as $m) {
    if (!is_array($m) || !isset($m['role'], $m['content'])) { continue; }
    $role = $m['role'] === 'assistant' ? 'assistant' : 'user';
    $content = trim(mb_substr((string)$m['content'], 0, 2000));
    if ($content === '') { continue; }
    $messages[] = ['role' => $role, 'content' => $content];
}
if (!$messages || end($messages)['role'] !== 'user') {
    fail('bad_request', 'The last message must be from the user.', 400);
}
$clean = [];   // the API needs alternating roles, starting with the user
foreach ($messages as $m) {
    if ($clean && end($clean)['role'] === $m['role']) {
        $clean[count($clean) - 1]['content'] .= "\n" . $m['content'];
    } else {
        $clean[] = $m;
    }
}
if ($clean[0]['role'] !== 'user') { array_shift($clean); }
$messages = $clean;
$candidates = [];
foreach (array_slice((array)($in['candidates'] ?? []), 0, 24) as $c) {
    if (is_string($c) && preg_match('/^[A-Za-z0-9_.-]{1,80}$/', $c)) { $candidates[] = $c; }
}
$engine = isset($in['engine']) ? mb_substr(strip_tags((string)$in['engine']), 0, 1500) : '';

// ---- catalogue
$catPath = __DIR__ . '/ai/catalogue.json';
if (!is_file($catPath)) {
    fail('no_catalogue', 'Catalogue file missing on the server.', 500);
}
$cat = json_decode((string)file_get_contents($catPath), true);
$byId = [];
foreach ($cat['families'] ?? [] as $f) { $byId[$f['id']] = $f; }

// one line per machine family: the whole range, so Claude can point to any machine
$index = [];
foreach ($cat['families'] ?? [] as $f) {
    $models = implode(', ', array_slice(array_column($f['models'], 'name'), 0, 12));
    $index[] = $f['id'] . ' | ' . $f['name'] . ' | ' . ($f['line'] ?: $f['brand']) . ' | ' . $f['page_nav'] . ' | ' . ($f['headline'] ?: '') . ($models ? ' | models: ' . $models : '');
}
// full details of the machines the panel's engine found most relevant
$details = [];
foreach ($candidates as $i => $id) {
    if (!isset($byId[$id])) { continue; }
    $f = $byId[$id];
    $full = $i < 12;
    $d = "### " . $f['name'] . "\nid: " . $f['id'] . " | line: " . ($f['line'] ?: $f['brand']) . " | category: " . $f['category'] . " | page: /" . $f['page'] . "\n";
    if ($f['headline']) { $d .= "Capacity: " . $f['headline'] . "\n"; }
    $d .= "Summary: " . $f['summary'] . "\n";
    if ($full) {
        if ($f['features']) { $d .= "Features: " . implode('; ', $f['features']) . "\n"; }
        if (!empty($f['optional'])) { $d .= "Options: " . implode('; ', array_slice($f['optional'], 0, 12)) . "\n"; }
        foreach ($f['specs'] ?? [] as $t) {
            $d .= "Table " . $t['title'] . " — models: " . implode(' | ', $t['models']) . "\n";
            foreach ($t['rows'] as $r) { $d .= "  " . array_shift($r) . ": " . implode(' | ', $r) . "\n"; }
        }
        foreach ($f['models'] as $m) {
            $parts = [];
            foreach ($m as $k => $v) {
                if ($k === 'name') { continue; }
                $parts[] = str_replace('_', ' ', $k) . ': ' . (is_array($v) ? implode('/', $v) : $v);
            }
            if ($parts) { $d .= "  " . $m['name'] . " — " . implode('; ', $parts) . "\n"; }
        }
    } else {
        $d .= "Models: " . implode(', ', array_column($f['models'], 'name')) . "\n";
    }
    $details[] = $d;
}
$c = $cat['contact'] ?? [];
$a = $c['address'] ?? [];
$addr = trim(($a['street'] ?? '') . ', ' . ($a['city'] ?? '') . ', ' . ($a['region'] ?? '') . ' ' . ($a['postal'] ?? ''));

$rules = <<<TXT
You are the AI machine finder of NovoTech Machine Tools Inc., a metalworking machinery supplier in Mississauga, Ontario, Canada (showroom and warehouse: $addr; phone {$c['phone']}; email {$c['email']}; hours {$c['hours']} Eastern). Visitors describe what they need to cut, bend, roll, punch, weld or finish, or ask about a machine; you recommend the most suitable machines from NovoTech's catalogue and explain briefly why.

Rules:
- Recommend ONLY machines in the catalogue below. Never invent models, capacities, prices or delivery times. If nothing fits, say so, suggest the closest machine and invite the visitor to call or email NovoTech.
- Check the numbers: the visitor's size must be within the model's capacity. Section benders (angle rolls) list for each profile the largest section and the minimum rolling diameter after the arrow, and a smaller section with its tighter minimum diameter; "2-inch pipe" in North America means NPS 2 (2-3/8″ OD). Press brakes: air bending needs about 575 × t² / V US tons per foot (V ≈ 8 × t); stainless needs about 1.5 times as much. Prefer the smallest machine that does the job with a sensible margin, and say when a bigger one is the safer choice.
- Two lines: the NovoTech premium line (built in Turkey and Europe, heavier construction) and the NovoTech value line (lower price). When both fit, mention one of each unless the visitor asked for premium or budget. A machine whose line is "NovoTech" premium line is sold only as NovoTech's premium line — never name another maker for it, and never use words from the ids as brand names.
- Every machine ships with a CSA-approved electrical panel; three-phase machines are supplied for 600 V (208, 240 or 480 V on request). Every new machine has a 1-year warranty; in-stock models have a 7-day money-back guarantee; financing with 0% down is available through NovoTech's financing partners; NovoTech delivers, installs and trains across Canada, with spare parts and support from Mississauga. Mention these only when relevant.
- NovoTech does not publish prices: for a price or quote, invite the visitor to use "Request a quote" on the machine's page or to call or email.
- Answer in the language the visitor writes in. Be short and concrete: 2–5 sentences, then the recommended models with a one-line reason each. Inches first, millimetres in brackets when useful. No marketing fluff, no headings.
- End EVERY answer with one line exactly in this form, ids from the catalogue, 0–5 entries, the best first: RESULTS: [{"id":"<family id>","model":"<model name or empty>"}]

Every machine family on the site (id | name | line | category | capacity | models):
TXT;
$system = [
    ['type' => 'text', 'text' => $rules . "\n" . implode("\n", $index), 'cache_control' => ['type' => 'ephemeral']],
    ['type' => 'text', 'text' => "Full details of the machines most relevant to this conversation:\n\n" . implode("\n", $details)
        . ($engine !== '' ? "\n\nThe site's built-in finder suggested (check it, you may disagree): " . $engine : '')],
];

$payload = [
    'model' => $MODEL,
    'max_tokens' => $MAX_TOK,
    'system' => $system,
    'messages' => $messages,
];

if ($CLI) {
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

$ch = curl_init('https://api.anthropic.com/v1/messages');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 60,
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'x-api-key: ' . $API_KEY,
        'anthropic-version: 2023-06-01',
    ],
    CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE),
]);
$res = curl_exec($ch);
$http = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$err = curl_error($ch);
curl_close($ch);

if ($res === false || $http >= 400) {
    error_log('ask.php upstream error ' . $http . ' ' . $err . ' ' . substr((string)$res, 0, 300));
    fail('upstream', 'The assistant is temporarily unavailable. Please call ' . ($c['phone'] ?? '') . ' or email ' . ($c['email'] ?? '') . '.', 502);
}
$data = json_decode((string)$res, true);
$text = '';
foreach ($data['content'] ?? [] as $block) {
    if (($block['type'] ?? '') === 'text') { $text .= $block['text']; }
}
$results = [];
if (preg_match('/RESULTS:\s*(\[.*\])\s*$/s', $text, $m)) {
    $results = json_decode($m[1], true) ?: [];
    $text = trim(preg_replace('/RESULTS:\s*\[.*\]\s*$/s', '', $text));
}
$text = preg_replace('/\b[ŞS]ahinler\b/iu', 'NovoTech premium line', $text);   // sold under NovoTech's own name
$valid = [];
foreach ($results as $r) {
    if (is_array($r) && isset($r['id']) && isset($byId[$r['id']])) {
        $valid[] = ['id' => $r['id'], 'model' => isset($r['model']) ? mb_substr((string)$r['model'], 0, 60) : ''];
    }
}
echo json_encode(['answer' => $text, 'results' => array_slice($valid, 0, 6), 'model' => $MODEL], JSON_UNESCAPED_UNICODE);
