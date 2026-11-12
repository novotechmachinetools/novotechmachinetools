#!/bin/bash
# Runs on the HostPapa server (cPanel Git Version Control -> .cpanel.yml), inside the clone of the built site.
# Copies the checked-out build into the document root with rsync. The branch picks the target:
#   hostpapa           -> ~/public_html        (the live site)
#   anything else      -> ~/public_html/new    (the test copy, built with --staging: noindex)
# Server-side files that never come from the repository are left alone: form-config.php and ai-config.php (keys),
# .well-known (AutoSSL), cgi-bin, error_log.
set -euo pipefail
cd "$(dirname "$0")"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
case "$BRANCH" in
  hostpapa) DEST="$HOME/public_html" ;;
  *)        DEST="$HOME/public_html/new" ;;
esac
mkdir -p "$DEST"
LOG="$HOME/deploy-hostpapa.log"
{
  echo "== $(date -u +%FT%TZ) branch=$BRANCH commit=$(git rev-parse --short HEAD 2>/dev/null || echo ?) -> $DEST"
  # the live document root is only overwritten once the old WebSite X5 site has been moved away (public_html_old-…)
  if [ "$DEST" = "$HOME/public_html" ] && { [ -e "$DEST/imsearch.php" ] || [ -d "$DEST/gallery" ] || [ -d "$DEST/pluginAppObj" ]; }; then
    echo "refusing: the old site is still in public_html — rename it first"; exit 1
  fi
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --omit-dir-times --no-perms --no-owner --no-group \
      --exclude='.git' --exclude='.cpanel.yml' --exclude='.deploy-hostpapa.sh' \
      --exclude='form-config.php' --exclude='ai-config.php' --exclude='.well-known' --exclude='cgi-bin' --exclude='error_log' \
      ./ "$DEST/"
  else
    echo "rsync missing: copying with cp (nothing is deleted)"
    cp -a . "$DEST/"
    rm -rf "$DEST/.git" "$DEST/.cpanel.yml" "$DEST/.deploy-hostpapa.sh"
  fi
  # the web server must be able to enter the document root: on Nov 12 2026 a deploy left public_html 0750 without the web
  # server's group and the whole site answered 403 ("pcfg_openfile: unable to check htaccess file") — rsync no longer touches
  # the owner or group (--no-owner --no-group) and the root is set to 0755 after every copy
  chmod 755 "$DEST"
  chmod 644 "$DEST/.htaccess" "$DEST/.user.ini" 2>/dev/null || true
  find "$DEST" -name '*.php' -exec chmod 644 {} + 2>/dev/null || true
  echo "done: $(find "$DEST" -type f | wc -l) files"
} >>"$LOG" 2>&1
