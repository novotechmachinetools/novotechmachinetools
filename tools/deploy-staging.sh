#!/usr/bin/env bash
# Build the staging site (noindex, github.io base URL) and force-push it to the gh-pages branch.
#   bash tools/deploy-staging.sh
# Afterwards the working tree is rebuilt as the production site in dist/.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 build.py --staging >/dev/null
python3 tools/check_links.py            # refuse to deploy with broken internal links
touch dist/.nojekyll
rm -f dist/quote.php                      # GitHub Pages cannot run PHP; the form only works on HostPapa
git checkout -q -b tmp-dist
git add -f dist >/dev/null
git commit -q -m "staging build"
git subtree split --prefix dist -b gh-pages-new -q >/dev/null
git checkout -q main
git branch -q -D tmp-dist
git branch -q -D gh-pages 2>/dev/null || true
git branch -m gh-pages-new gh-pages
git push -q -f origin gh-pages
python3 build.py >/dev/null               # leave dist/ as the production build
echo "gh-pages updated: $(git rev-parse --short gh-pages)"
