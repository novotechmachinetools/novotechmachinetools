<?php
// Temporary check (Nov 14 2026): the PHP upload limits the live site runs with. Removed by the next deploy.
header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
echo 'upload_max_filesize=', ini_get('upload_max_filesize'), ' post_max_size=', ini_get('post_max_size'), ' max_file_uploads=', ini_get('max_file_uploads'), "\n";
