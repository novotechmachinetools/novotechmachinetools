#!/usr/bin/env python3
"""Local preview server for dist/ that serves clean URLs the way the production .htaccess does:
/band-saw → band-saw.html, / → index.html (or rebar-bender-and-cutter.html while there is no home page).
    python3 tools/serve.py [port]
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dist")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def translate_path(self, path):
        p = path.split("?", 1)[0].split("#", 1)[0]
        if p in ("", "/"):
            for cand in ("index.html", "rebar-bender-and-cutter.html"):
                if os.path.exists(os.path.join(ROOT, cand)):
                    return os.path.join(ROOT, cand)
        full = super().translate_path(path)
        if not os.path.exists(full) and "." not in os.path.basename(p) and os.path.exists(full + ".html"):
            return full + ".html"
        return full

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
