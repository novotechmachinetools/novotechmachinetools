#!/bin/bash
# Go-live swap (Nov 8 2026): the old WebSite X5 site is moved aside (kept, not deleted) and the new site takes the
# document root. The new site is staged from the test copy in public_html/new, then the two folders swap names, so the
# site is down only for the instant between the two renames. The deployment of branch "hostpapa" then brings it current.
set -u
LOG="$HOME/golive.log"; exec >>"$LOG" 2>&1; echo "=== $(date)"
OLD="$HOME/public_html_old_website_x5_2026-11-08"; NEXT="$HOME/public_html_next"
[ -e "$OLD" ] && { echo "already swapped"; exit 0; }
[ -f "$HOME/public_html/new/quote.php" ] || { echo "no staged new site"; exit 1; }
rm -rf "$NEXT"; mkdir -p "$NEXT"
rsync -a "$HOME/public_html/new/" "$NEXT/" && rm -f "$NEXT/_oldsite-files.txt" "$NEXT/_oldsite-all.txt"
for d in .well-known cgi-bin; do [ -e "$HOME/public_html/$d" ] && cp -a "$HOME/public_html/$d" "$NEXT/"; done
[ -f "$NEXT/form-config.php" ] || { echo "form-config.php missing in staged site"; exit 1; }
mv "$HOME/public_html" "$OLD" && mv "$NEXT" "$HOME/public_html" && echo "swapped: $(ls "$HOME/public_html" | wc -l) entries in public_html"
chmod 755 "$HOME/public_html"; ls -ld "$HOME/public_html" "$OLD"
