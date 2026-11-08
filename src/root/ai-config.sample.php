<?php
/**
 * Configuration of the AI machine finder's chat answers (ask.php).
 * Copy this file to ai-config.php next to ask.php on the web server and fill in the API key.
 * ai-config.php is never published by the site build and must not be committed to Git.
 *
 * Without a key the finder still works everywhere: the panel answers from its built-in engine (every machine that does
 * the job, the smallest first, then similar machines, sizes checked against every model). With a key, Claude also
 * answers like a chat, from the whole catalogue, streamed as it writes — recommending only NovoTech's machines.
 *
 * Get a key at https://console.anthropic.com/ (Settings → API keys). Usage is pay-as-you-go; set a monthly spending
 * limit there as well.
 */
return [
    'api_key'     => 'sk-ant-...',           // Anthropic API key
    'model'       => 'claude-sonnet-5-5',    // careful answers; 'claude-haiku-5-5' is faster and costs less
    'max_tokens'  => 2500,                   // room for the answer and the full list of machines
    'rate_limit'  => 40,                     // questions per visitor (IP) ...
    'rate_window' => 600,                    // ... per 10 minutes
    'daily_limit' => 400,                    // questions per day for the whole site — a ceiling on the cost
];
