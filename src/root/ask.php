<?php
/**
 * NovoTech AI machine finder — Claude's chat answer on the live site.
 *
 * The finder panel (js/ai.js) answers every question at once from the site's machine index (ai/catalogue.json, written
 * by the site build): every machine that does the job, the smallest first, then similar machines. On the live server it
 * also sends the question here with the conversation so far and the engine's lists; Claude gets the whole catalogue
 * (every family and model with its main capacities, prompt-cached) plus the full details of the machines in those lists,
 * answers like a chat — streamed as it writes — and keeps or corrects the lists (the owner, Nov 7 2026: like Claude's own
 * chat, but recommending only NovoTech's machines, never other makers or outside sites).
 *
 * Setup on the web server: copy ai-config.sample.php to ai-config.php and put the API key in it. Without a key the
 * endpoint answers {"error":"not_configured"} and the panel keeps its built-in answer.
 * Check before going live:  php ask.php < request.json  prints the request it would send to Claude.
 */
declare(strict_types=1);

header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

$config = __DIR__ . '/ai-config.php';
$cfg = is_file($config) ? (include $config) : [];
$API_KEY   = $cfg['api_key']   ?? '';
$MODEL     = $cfg['model']     ?? 'claude-sonnet-5-5';
$MAX_TOK   = (int)($cfg['max_tokens'] ?? 2500);
$RATE_N    = (int)($cfg['rate_limit'] ?? 40);        // questions per IP per window
$RATE_SECS = (int)($cfg['rate_window'] ?? 600);      // window length in seconds
$DAY_N     = (int)($cfg['daily_limit'] ?? 400);      // questions per day for the whole site (a cost ceiling)
$API_URL   = $cfg['api_url'] ?? 'https://api.anthropic.com/v1/messages';

function fail(string $code, string $msg, int $http = 200): void {
    http_response_code($http);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => $code, 'message' => $msg]);
    exit;
}

$CLI = PHP_SAPI === 'cli';
if (!$CLI && ($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    fail('method', 'POST only', 405);
}
if (!$CLI && ($API_KEY === '' || strpos($API_KEY, '...') !== false)) {
    fail('not_configured', 'The AI assistant is not configured on this server yet.');
}

// ---- limits: per IP, and per day for the whole site (file based; fine for a product site)
if (!$CLI) {
    $ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    $now = time();
    $bucket = sys_get_temp_dir() . '/novotech-ask-' . md5($ip) . '.json';
    $hits = is_file($bucket) ? (json_decode((string)file_get_contents($bucket), true) ?: []) : [];
    $hits = array_values(array_filter($hits, static fn($t) => $t > $now - $RATE_SECS));
    if (count($hits) >= $RATE_N) {
        fail('rate_limit', 'Too many questions in a short time — please try again in a few minutes.', 429);
    }
    $hits[] = $now;
    @file_put_contents($bucket, json_encode($hits));
    $dayFile = sys_get_temp_dir() . '/novotech-ask-day-' . date('Ymd') . '.txt';
    $day = (int)@file_get_contents($dayFile);
    if ($day >= $DAY_N) {
        fail('daily_limit', 'The assistant has answered many questions today — please call or email us.');
    }
    @file_put_contents($dayFile, (string)($day + 1));
}

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
    $content = trim(mb_substr((string)$m['content'], 0, 2500));
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
$stream = !$CLI && !empty($in['stream']);
$engine = isset($in['engine']) ? mb_substr(strip_tags((string)$in['engine']), 0, 2000) : '';

// ---- catalogue
$catPath = __DIR__ . '/ai/catalogue.json';
if (!is_file($catPath)) {
    fail('no_catalogue', 'Catalogue file missing on the server.', 500);
}
$cat = json_decode((string)file_get_contents($catPath), true);
$byId = [];
foreach ($cat['families'] ?? [] as $f) { $byId[$f['id']] = $f; }

/** the engine's lists from the panel, checked against the catalogue */
function refs($list, array $byId, int $max): array {
    $out = [];
    foreach (array_slice(is_array($list) ? $list : [], 0, $max) as $r) {
        if (!is_array($r) || !isset($r['id']) || !is_string($r['id']) || !isset($byId[$r['id']])) { continue; }
        $model = isset($r['model']) && is_string($r['model']) ? mb_substr($r['model'], 0, 80) : '';
        $also = [];
        foreach (array_slice(is_array($r['also'] ?? null) ? $r['also'] : [], 0, 12) as $a) { if (is_string($a) && $a !== '') { $also[] = mb_substr($a, 0, 80); } }
        $out[] = ['id' => $r['id'], 'model' => $model, 'also' => $also];
    }
    return $out;
}
$fits = refs($in['fits'] ?? [], $byId, 90);
$maybe = refs($in['maybe'] ?? [], $byId, 30);
$closest = refs($in['closest'] ?? [], $byId, 5);

/** a value without its metric twin in brackets, the first part only: "66 US tons (60 t)" -> "66 US tons" */
function brief(string $v): string {
    $v = preg_replace('/\s*\([^)]*\)/u', '', $v);
    $v = explode(' · ', (string)$v)[0];
    return trim(preg_replace('/\s+/u', ' ', $v));
}
$CAPS = '/capacit|max|force|tonnage|length|thickness|width|diameter|Ø|bar\b|pipe|tube|laser power|bed|working|table|punch|load|section|angle|flat|cut/iu';
/** each model with its two main capacities, for the index */
function modelLine(array $f, string $CAPS): string {
    $per = [];
    foreach ($f['specs'] ?? [] as $t) {
        $rows = array_values(array_filter($t['rows'], static fn($r) => preg_match($CAPS, (string)$r[0]) === 1));
        if (!$rows) { $rows = $t['rows']; }
        $rows = array_slice($rows, 0, 2);
        foreach ($t['models'] as $i => $name) {
            if (isset($per[$name])) { continue; }
            $vals = [];
            foreach ($rows as $r) {
                $v = $r[$i + 1] ?? '';
                if ($v !== '' && $v !== '—') { $vals[] = brief((string)$v); }
            }
            $per[$name] = $vals;
        }
    }
    $out = [];
    foreach ($f['models'] as $m) {
        $name = $m['name'];
        $vals = $per[$name] ?? [];
        if (!$vals) {
            foreach ($m as $k => $v) {
                if ($k === 'name' || $k === 'img' || is_array($v) && isset($v['src'])) { continue; }
                $vals[] = str_replace('_', ' ', (string)$k) . ' ' . brief(is_array($v) ? implode('/', $v) : (string)$v);
                if (count($vals) >= 2) { break; }
            }
        }
        $out[] = $vals ? $name . ' (' . implode(', ', $vals) . ')' : $name;
    }
    return implode('; ', $out);
}

// the whole catalogue, one line per machine family with every model: Claude can point to any machine on the site
$index = [];
foreach ($cat['families'] ?? [] as $f) {
    $line = ($f['line'] ?? '') === 'Premium line' ? 'NovoTech premium line' : (($f['line'] ?? '') === 'Value line' ? 'NovoTech value line' : ($f['brand'] ?? ''));
    $models = modelLine($f, $CAPS);
    $index[] = $f['id'] . ' | ' . $f['name'] . ' | ' . $line . ' | page /' . $f['page'] . ' | ' . ($f['headline'] ?: '') . ($models ? ' | models: ' . $models : '');
}

// full details of the machines in the engine's lists (the first families in full, the rest in short)
$seen = [];
$order = [];
foreach (array_merge($fits, $closest, $maybe) as $r) {
    if (!isset($seen[$r['id']])) { $seen[$r['id']] = 1; $order[] = $r['id']; }
}
$details = [];
foreach ($order as $i => $id) {
    $f = $byId[$id];
    $full = $i < 14;
    $line = ($f['line'] ?? '') === 'Premium line' ? 'NovoTech premium line' : (($f['line'] ?? '') === 'Value line' ? 'NovoTech value line' : ($f['brand'] ?? ''));
    $d = '### ' . $f['name'] . "\nid: " . $f['id'] . ' | ' . $line . ' | category: ' . $f['category'] . ' | page: /' . $f['href'] . "\n";
    if ($f['headline']) { $d .= 'Capacity: ' . $f['headline'] . "\n"; }
    $d .= 'Summary: ' . $f['summary'] . "\n";
    if ($full) {
        if ($f['features']) { $d .= 'Features: ' . implode('; ', $f['features']) . "\n"; }
        if (!empty($f['optional'])) { $d .= 'Options: ' . implode('; ', array_slice($f['optional'], 0, 14)) . "\n"; }
        foreach ($f['specs'] ?? [] as $t) {
            $d .= 'Table ' . $t['title'] . ' — models: ' . implode(' | ', $t['models']) . "\n";
            foreach ($t['rows'] as $r) { $d .= '  ' . array_shift($r) . ': ' . implode(' | ', $r) . "\n"; }
        }
        foreach ($f['models'] as $m) {
            $parts = [];
            foreach ($m as $k => $v) {
                if ($k === 'name' || $k === 'img') { continue; }
                $parts[] = str_replace('_', ' ', (string)$k) . ': ' . (is_array($v) ? implode('/', $v) : $v);
            }
            if ($parts) { $d .= '  ' . $m['name'] . ' — ' . implode('; ', $parts) . "\n"; }
        }
    }
    $details[] = $d;
}
$fmt = static fn(array $list) => implode("\n", array_map(static fn($r, $i) => ($i + 1) . '. ' . $r['id'] . ($r['model'] !== '' ? ' / ' . $r['model'] : ' (whole series)') . (!empty($r['also']) ? ' — the ' . implode(', ', $r['also']) . ' of the same series also ' . (count($r['also']) === 1 ? 'does' : 'do') . ' it' : ''), $list, array_keys($list)));

$c = $cat['contact'] ?? [];
$a = $c['address'] ?? [];
$addr = trim(($a['street'] ?? '') . ', ' . ($a['city'] ?? '') . ', ' . ($a['region'] ?? '') . ' ' . ($a['postal'] ?? ''));

$rules = <<<TXT
You are the AI machine finder on the website of NovoTech Machine Tools Inc., a metal fabrication machinery supplier in Mississauga, Ontario, Canada (showroom and warehouse: $addr; phone {$c['phone']}; email {$c['email']}; hours {$c['hours']} Eastern). Talk with visitors like a knowledgeable, friendly applications engineer in a chat: answer their questions about metalworking and fabrication — processes, materials, tonnage and capacity, choosing and comparing machines, tooling, set-up, maintenance, safety, power supply, delivery and financing — from your own knowledge and from NovoTech's catalogue below.

Rules:
- Recommend, name and compare ONLY machines in NovoTech's catalogue below. Never mention, recommend or compare other brands, manufacturers, dealers or their products, and never cite, quote or link to other websites or outside sources. If a visitor asks about another brand or a machine NovoTech does not sell, say politely that you can only advise on NovoTech's machines and point to the closest NovoTech machine. Links, if any, only to NovoTech's own pages, written as [text](/page).
- Stay on topic — metalworking, fabrication and NovoTech. For unrelated requests (homework, code, general chat), say in one sentence that you are NovoTech's machine finder and ask what they want to make.
- Never invent models, capacities, prices, stock or delivery times. Use the catalogue's numbers; when a size is not listed, say so and offer to confirm it with the visitor's drawing.
- When the visitor describes a job, the answer lists EVERY series in the catalogue that does it — one card per series, showing the model of the series that fits the job most closely, with the other sizes of that series that also do it named on the card — from the closest fit to the largest; then, separately, the machines that may also do it but you are not sure of (no data for that size, another type of machine, a borderline size), each with the reason. A word the visitor uses about the kind of machine (automatic or autofeed, semi-automatic, manual, miter, CNC or NC, electric, hydraulic, mechanical, premium or value line, single-phase) is a condition, not a preference: a machine without it is not an answer, and the engine says how many it left out for that reason; when no machine of that exact kind does the job, the engine lists the ones that do and says they lack it. The site's own engine has already checked the spec tables and applied these rules — its lists are below: keep them unless you find a real mistake, and add any series it missed. The cards under your answer show every series in the lists, so in your text name the smallest machine that does the job, explain why, and mention the notable alternatives — do not write out the whole list and do not list the sizes of one series one by one.
- Checking capacities: the visitor's size must be within the model's capacity. Section benders (angle rolls) list for each profile the largest section and the minimum rolling diameter after the arrow, and a smaller section with its tighter minimum diameter; "2-inch pipe" in North America means NPS 2 (2-3/8″ OD). Press brakes: air bending needs about 575 × t² / V US tons per foot (V ≈ 8 × t); stainless needs about 1.5 times as much. Rebar benders and cutters: the "max single bar" rating is for mild steel; Grade 400W rebar needs a bigger machine — say so when it matters.
- Two lines: the NovoTech premium line (built in Turkey and Europe, heavier construction) and the NovoTech value line (lower price). A machine whose line is "NovoTech premium line" is sold only under NovoTech's name — never name another maker for it, and never use words from the ids as brand names.
- Every machine ships with a CSA-approved electrical panel; three-phase machines are supplied for 600 V (208, 240 or 480 V on request). Every new machine has a 1-year warranty; in-stock models have a 7-day money-back guarantee; financing with 0% down is available through NovoTech's financing partners; NovoTech delivers, installs and trains across Canada, with spare parts and support from Mississauga. Mention these only when relevant.
- NovoTech does not publish prices: for a price or quote, invite the visitor to use "Get a quote" on the machine's card or page, or to call or email.
- Answer in the language the visitor writes in. Write like a helpful chat: short paragraphs, a list when it helps, model names in **bold**, inches first with millimetres in brackets when useful. No headings, no marketing fluff.
- End EVERY answer with one last line exactly in this form: RESULTS: {"use_engine": true}   when the engine's lists are right (most of the time). When you correct or replace them — the engine found nothing, misunderstood the question, or missed or wrongly listed a machine — give the complete lists instead, in order, ids and model names exactly as in the catalogue (model "" for a whole series): RESULTS: {"fits": [{"id": "...", "model": "..."}], "maybe": [{"id": "...", "model": "...", "note": "why it may also do it"}]}

NovoTech's catalogue — every machine family on the site (id | name | line | page | capacity | models with their main capacities):
TXT;

$dynamic = "The site's engine, for the visitor's last message:\n" . ($engine !== '' ? 'Its answer: ' . $engine . "\n" : '')
    . ($fits ? "Machines that do the job, smallest first:\n" . $fmt($fits) . "\n" : "Machines that do the job: none found.\n")
    . ($closest ? "Closest machines (below the size asked):\n" . $fmt($closest) . "\n" : '')
    . ($maybe ? "Similar machines that may also do it:\n" . $fmt($maybe) . "\n" : '')
    . ($details ? "\nFull details of those machines:\n\n" . implode("\n", $details) : '');

$system = [
    ['type' => 'text', 'text' => $rules . "\n" . implode("\n", $index), 'cache_control' => ['type' => 'ephemeral']],   // the same for every question: cached
    ['type' => 'text', 'text' => $dynamic],
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

/** the answer the visitor sees: nothing from RESULTS on, and NovoTech's own name for its premium line */
function visible(string $t): string {
    $i = strpos($t, 'RESULTS:');
    if ($i !== false) { $t = substr($t, 0, $i); }
    return (string)preg_replace('/\b[ŞS]ahinler\b/iu', 'NovoTech premium line', rtrim($t));
}
/** the lists Claude gave, checked against the catalogue */
function results(string $t, array $byId): array {
    if (!preg_match('/RESULTS:\s*(\{.*\})\s*$/s', $t, $m)) { return ['use_engine' => true]; }
    $j = json_decode($m[1], true);
    if (!is_array($j) || !empty($j['use_engine'])) { return ['use_engine' => true]; }
    $clean = static function ($list) use ($byId) {
        $out = [];
        foreach (array_slice(is_array($list) ? $list : [], 0, 150) as $r) {
            if (!is_array($r) || !isset($r['id']) || !isset($byId[$r['id']])) { continue; }
            $model = isset($r['model']) ? (string)$r['model'] : '';
            if ($model !== '' && !in_array($model, array_column($byId[$r['id']]['models'], 'name'), true)) { $model = ''; }
            $e = ['id' => $r['id'], 'model' => $model];
            if (!empty($r['note'])) { $e['note'] = mb_substr((string)$r['note'], 0, 200); }
            $out[] = $e;
        }
        return $out;
    };
    $fitsOut = $clean($j['fits'] ?? []);
    $maybeOut = $clean($j['maybe'] ?? []);
    return ($fitsOut || $maybeOut) ? ['fits' => $fitsOut, 'maybe' => $maybeOut] : ['use_engine' => true];
}

$headers = ['Content-Type: application/json', 'x-api-key: ' . $API_KEY, 'anthropic-version: 2023-06-01'];

if (!$stream) {
    $ch = curl_init($API_URL);
    curl_setopt_array($ch, [
        CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 90,
        CURLOPT_HTTPHEADER => $headers, CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE),
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
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['answer' => visible($text), 'results' => results($text, $byId), 'model' => $MODEL], JSON_UNESCAPED_UNICODE);
    exit;
}

// ---- streamed answer: Server-Sent Events, {"t": "..."} as Claude writes, then {"done": true, ...}
header('Content-Type: text/event-stream; charset=utf-8');
header('X-Accel-Buffering: no');
@ini_set('zlib.output_compression', '0');
@ini_set('output_buffering', '0');
while (ob_get_level() > 0) { @ob_end_flush(); }
ob_implicit_flush(true);
$emit = static function (array $o): void { echo 'data: ' . json_encode($o, JSON_UNESCAPED_UNICODE) . "\n\n"; @flush(); };
echo ': ' . str_repeat(' ', 2048) . "\n\n";   // some servers buffer the first 2 KB
@flush();

$payload['stream'] = true;
$acc = '';      // everything Claude wrote
$buf = '';      // the SSE bytes not yet parsed
$sent = 0;      // characters of the visible text already sent
$upErr = '';
$ch = curl_init($API_URL);
curl_setopt_array($ch, [
    CURLOPT_POST => true, CURLOPT_TIMEOUT => 120, CURLOPT_HTTPHEADER => $headers,
    CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE),
    CURLOPT_WRITEFUNCTION => static function ($ch, string $chunk) use (&$acc, &$buf, &$sent, &$upErr, $emit): int {
        $buf .= $chunk;
        while (($pos = strpos($buf, "\n\n")) !== false) {
            $event = substr($buf, 0, $pos);
            $buf = substr($buf, $pos + 2);
            foreach (explode("\n", $event) as $line) {
                if (strpos($line, 'data:') !== 0) { continue; }
                $d = json_decode(trim(substr($line, 5)), true);
                if (!is_array($d)) { continue; }
                if (($d['type'] ?? '') === 'content_block_delta' && (($d['delta']['type'] ?? '') === 'text_delta')) {
                    $acc .= (string)$d['delta']['text'];
                    // send what is safe: hold back the last characters (a name or "RESULTS:" may be half written)
                    $vis = visible($acc);
                    $safe = strpos($acc, 'RESULTS:') !== false ? mb_strlen($vis) : max(0, mb_strlen($vis) - 12);
                    if ($safe > $sent) { $emit(['t' => mb_substr($vis, $sent, $safe - $sent)]); $sent = $safe; }
                } elseif (($d['type'] ?? '') === 'error') {
                    $upErr = (string)($d['error']['message'] ?? 'error');
                }
            }
        }
        if ($buf !== '' && $buf[0] === '{' && strpos($buf, '"error"') !== false) { $upErr = substr($buf, 0, 300); }
        return strlen($chunk);
    },
]);
curl_exec($ch);
$http = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$err = curl_error($ch);
curl_close($ch);
if ($http >= 400 || $err !== '' || ($upErr !== '' && $acc === '')) {
    error_log('ask.php upstream error ' . $http . ' ' . $err . ' ' . $upErr);
    $emit(['error' => 'upstream', 'message' => 'The assistant is temporarily unavailable. Please call ' . ($c['phone'] ?? '') . ' or email ' . ($c['email'] ?? '') . '.']);
    exit;
}
$vis = visible($acc);
if (mb_strlen($vis) > $sent) { $emit(['t' => mb_substr($vis, $sent)]); }
$emit(['done' => true, 'answer' => $vis, 'results' => results($acc, $byId), 'model' => $MODEL]);
