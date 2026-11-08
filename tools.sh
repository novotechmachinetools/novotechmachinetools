#!/bin/bash
# one-off inventory of the old site (read-only)
cd "$HOME/public_html" || exit 1
find . -path ./new -prune -o -type f \( -iname '*.html' -o -iname '*.htm' -o -iname '*.pdf' -o -iname '*.php' -o -iname '*.xml' -o -iname '*.txt' \) -printf '%s %P\n' > "$HOME/oldsite-files.txt" 2>&1
find . -path ./new -prune -o -type f -printf '%P\n' | awk -F/ '{print $1}' | sort | uniq -c > "$HOME/oldsite-dirs.txt"
cp .htaccess "$HOME/oldsite-htaccess.txt"
date > "$HOME/oldsite-inventory.done"
