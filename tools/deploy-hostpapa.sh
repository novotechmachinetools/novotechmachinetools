#!/usr/bin/env bash
# Build the site and publish the build to a deployment branch that the HostPapa server pulls (cPanel Git Version Control):
#   bash tools/deploy-hostpapa.sh staging   -> branch hostpapa-staging: --staging build (noindex), served at /new/
#   bash tools/deploy-hostpapa.sh preview   -> branch hostpapa-staging: the production build itself, served at /new/ (a last look before go-live)
#   bash tools/deploy-hostpapa.sh prod      -> branch hostpapa: production build, served at the document root
# The branch keeps a linear history (one commit per deploy on top of the last), so the server's "git pull" fast-forwards.
# The commit is built from dist/ with a temporary index — no second copy of the 900 MB build on disk; unchanged images
# are the same blobs GitHub already has, so a push carries only what changed.
# Afterwards the server side is triggered with the cPanel API (device shell: bash ~/hp.sh update BRANCH; bash ~/hp.sh deploy).
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-staging}"
case "$MODE" in
  staging) BRANCH=hostpapa-staging; FLAGS=--staging ;;
  preview) BRANCH=hostpapa-staging; FLAGS= ;;
  prod)    BRANCH=hostpapa;         FLAGS= ;;
  *) echo "usage: $0 staging|preview|prod" >&2; exit 2 ;;
esac
python3 build.py $FLAGS >/dev/null
python3 tools/check_links.py
[ -f dist/.cpanel.yml ] && [ -f dist/.deploy-hostpapa.sh ] || { echo "deployment files missing in dist/" >&2; exit 1; }
[ -f dist/quote.php ] && [ -f dist/ask.php ] || { echo "php endpoints missing in dist/" >&2; exit 1; }
for secret in form-config.php ai-config.php; do [ -e "dist/$secret" ] && { echo "refusing: dist/$secret must never be published" >&2; exit 1; }; done
SRC="$(git rev-parse --short HEAD)"
git fetch -q origin "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH" 2>/dev/null || true
PARENT="$(git rev-parse -q --verify "refs/remotes/origin/$BRANCH" || true)"
TMPIDX="$(mktemp)"; trap 'rm -f "$TMPIDX"' EXIT
export GIT_INDEX_FILE="$TMPIDX"
git read-tree --empty
git add -f dist
TREE="$(git rev-parse "$(git write-tree):dist")"
unset GIT_INDEX_FILE
if [ -n "$PARENT" ] && [ "$(git rev-parse "$PARENT^{tree}")" = "$TREE" ]; then echo "nothing changed on $BRANCH ($(git rev-parse --short "$PARENT"))"; else
  COMMIT="$(GIT_AUTHOR_NAME="NovoTech build" GIT_AUTHOR_EMAIL="novotechmachinetools@gmail.com" GIT_COMMITTER_NAME="NovoTech build" GIT_COMMITTER_EMAIL="novotechmachinetools@gmail.com" \
    git commit-tree "$TREE" ${PARENT:+-p "$PARENT"} -m "$MODE build $(date -u '+%Y-%m-%d %H:%M') UTC from main $SRC")"
  git update-ref "refs/heads/$BRANCH" "$COMMIT"
  git push -q origin "refs/heads/$BRANCH:refs/heads/$BRANCH"
  echo "$BRANCH: $(git rev-parse --short "$COMMIT") pushed — $(find dist -type f | wc -l) files, from main $SRC"
fi
if [ -n "$FLAGS" ]; then python3 build.py >/dev/null; fi   # leave dist/ as the production build
