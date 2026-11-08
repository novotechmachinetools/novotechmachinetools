#!/usr/bin/env python3
"""Tell Bing (and the other IndexNow engines) which pages changed — run after a production deploy.

    python3 tools/indexnow.py                 # every URL in dist/sitemap.xml
    python3 tools/indexnow.py press-brake band-saw   # only these pages
    python3 tools/indexnow.py --dry-run       # print the request, send nothing

The key is INDEXNOW_KEY in build.py; the build copies the key file to the site root, which is how
the engines verify the submission. IndexNow is for the live host only (novotechmachinetools.com) —
the staging site on GitHub Pages is noindex and is never submitted.
"""
import json, re, sys, os, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = re.search(r'INDEXNOW_KEY = "([0-9a-f]+)"', open(os.path.join(ROOT, "build.py")).read()).group(1)
HOST = "novotechmachinetools.com"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
dry = "--dry-run" in sys.argv
if args:
    urls = [f"https://{HOST}/{a.strip('/')}" for a in args]
else:
    sm = open(os.path.join(ROOT, "dist", "sitemap.xml")).read()
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
body = {"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}
print(f"{len(body['urlList'])} URLs → api.indexnow.org" + (" (dry run)" if dry else ""))
if dry:
    print(json.dumps(body, indent=1)[:1500]); sys.exit()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=json.dumps(body).encode(), headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("HTTP", r.status, "— accepted" if r.status in (200, 202) else "")
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:300])
    print("422 = key file not found at the site root yet; 403 = key does not match; 429 = too many submissions")
