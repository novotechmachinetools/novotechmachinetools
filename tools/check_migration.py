"""Old-site URLs → new site: where does each address that Google sends visitors to end up after the move to HostPapa?

    python3 tools/check_migration.py /path/to/Pages.csv [more.csv ...]

Reads Search Console "Pages" exports (first column: the URL; Clicks and Impressions when present) and replays what
src/root/.htaccess will do on the server: the mod_alias Redirect / RedirectMatch rules in file order, then the
".html → address without .html" rule, then the files in dist/. Prints every address that would end on a missing page
(404), on the home page through a redirect (Google treats those as soft 404s), or through more than one hop.
The Search Console exports are private data: keep them outside the repository (e.g. /home/claude/seo-data/).
Build the site first (python3 build.py) so dist/ holds the production pages.
"""
import csv, os, re, shlex, sys
from urllib.parse import urlsplit, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
rules = []
for line in open(os.path.join(ROOT, "src", "root", ".htaccess"), encoding="utf-8"):
    try:
        p = shlex.split(line)
    except ValueError:
        p = line.split()
    if not p or p[0].startswith("#"):
        continue
    if p[0] == "RedirectMatch" and len(p) >= 3 and p[1] == "410":
        rules.append(("gone", re.compile(p[2].replace("\\s", " ")), None))
    elif p[0] == "RedirectMatch" and len(p) >= 4:
        rules.append(("match", re.compile(p[2].replace("\\s", " ")), p[3]))
    elif p[0] == "Redirect" and len(p) >= 4:
        rules.append(("prefix", p[2], p[3]))


def exists(path):
    """the file Apache would serve for a URL path, or None"""
    path = unquote(path.split("#")[0])
    rel = path.lstrip("/")
    full = os.path.join(DIST, rel)
    if rel == "" or os.path.isdir(full):
        idx = os.path.join(full, "index.html")
        return idx if os.path.exists(idx) else None
    if os.path.isfile(full):
        return full
    if "." not in os.path.basename(rel) and os.path.isfile(full + ".html"):
        return full + ".html"
    return None


def step(path):
    """one request: (status, location or file)"""
    for kind, pat, dest in rules:
        if kind == "gone":
            if pat.search(path):
                return 410, None
        elif kind == "match":
            m = pat.search(path)
            if m:
                return 301, m.expand(re.sub(r"\$(\d)", r"\\\1", dest))
        elif path == pat or path.startswith(pat.rstrip("/") + "/"):
            return 301, dest + path[len(pat):]
    if path.endswith(".html"):
        return 301, path[:-5]
    f = exists(path)
    return (200, f) if f else (404, None)


def follow(path, limit=6):
    hops = []
    for _ in range(limit):
        st, where = step(path)
        if st != 301:
            return st, path, hops
        hops.append(where)
        path = urlsplit(where).path or "/"
    return 310, path, hops


def main():
    rows = []
    for fn in sys.argv[1:]:
        with open(fn, encoding="utf-8-sig") as f:
            for r in csv.reader(f):
                if not r or not r[0].startswith("http"):
                    continue
                num = lambda x: float(x.replace(",", "").replace("%", "") or 0)
                rows.append((r[0], num(r[1]) if len(r) > 1 else 0, num(r[2]) if len(r) > 2 else 0))
    seen, bad, home, chains, ok, gone = set(), [], [], [], 0, 0
    for url, clicks, impr in sorted(rows, key=lambda x: -x[1]):
        u = urlsplit(url)
        if u.path in seen:
            continue
        seen.add(u.path)
        st, final, hops = follow(u.path or "/")
        if st == 410:
            gone += 1
        elif st != 200:
            bad.append((url, clicks, impr, st, final))
        elif hops and final in ("/", "/index"):
            home.append((url, clicks, impr))
        else:
            ok += 1
        # one hop is the .html → clean address rule; a second one means a redirect that lands on a .html address
        if len(hops) > 1 and not (len(hops) == 2 and not hops[0].endswith(".html") and hops[1] == hops[0]):
            chains.append((url, hops))
    print(f"{len(seen)} old addresses: {ok} reach a page, {len(home)} redirect to the home page, {gone} are marked gone (410, old pictures), {len(bad)} end on an error")
    for url, c, i, st, final in bad:
        print(f"  {st}  {int(c):5d} clicks {int(i):7d} impr  {url}  ->  {final}")
    for url, c, i in home:
        print(f"  HOME {int(c):5d} clicks {int(i):7d} impr  {url}")
    long = [(u, h) for u, h in chains if len(h) > 2]
    for url, hops in long:
        print("  CHAIN", url, " -> ".join(hops))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
