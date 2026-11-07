<?php
/**
 * Configuration of the AI machine finder (ask.php).
 * Copy this file to ai-config.php next to ask.php on the web server and fill in the API key.
 * ai-config.php is never published by the site build and must not be committed to Git.
 *
 * Get a key at https://console.anthropic.com/ (Settings → API keys). Usage is pay-as-you-go;
 * one question costs a fraction of a cent with the default model.
 */
return [
    'api_key'     => 'sk-ant-...',          // Anthropic API key
    'model'       => 'claude-haiku-4-5',    // fast and inexpensive; use 'claude-sonnet-4-5' for more careful answers
    'max_tokens'  => 900,
    'rate_limit'  => 40,                    // questions per visitor (IP) ...
    'rate_window' => 600,                   // ... per 10 minutes
];
