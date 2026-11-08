<?php
/**
 * Configuration of the quote form (quote.php).
 * Copy this file to form-config.php next to quote.php on the web server and fill in the reCAPTCHA secret key.
 * form-config.php is never published by the site build and must not be committed to Git.
 *
 * Keys: https://www.google.com/recaptcha/admin/create — type "Score based (v3)", domains novotechmachinetools.com and
 * novotechmachinetools.github.io. The site key (public) goes into content/site.json as "recaptcha_site_key"; the secret key
 * goes here.
 */
return [
    'recaptcha_secret'    => '',    // reCAPTCHA v3 secret key; empty = no check (the form still works)
    'recaptcha_min_score' => 0.5,   // requests scored below this are refused (0.0 = bot … 1.0 = person)
];
