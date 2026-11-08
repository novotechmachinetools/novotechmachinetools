#!/bin/bash
# one-off: publish the old site's file inventory (names only) for the migration check; removed by the next deploy
cp "$HOME/oldsite-files.txt" "$HOME/public_html/new/_oldsite-files.txt"
find "$HOME/public_html" -path "$HOME/public_html/new" -prune -o -type f -printf '%P\n' > "$HOME/public_html/new/_oldsite-all.txt"
