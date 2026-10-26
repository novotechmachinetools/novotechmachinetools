#!/usr/bin/env python3
"""Local preview server for dist/ that serves clean URLs, gzip and cache headers the way the production .htaccess does:
/band-saw → band-saw.html, / → index.html (or rebar-bender-and-cutter.html while there is no home page).
    python3 tools/serve.py [port]
"""
import gzip
import io
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

    # gzip text responses like the production host does, so Lighthouse on the preview sees the real transfer sizes
    GZ = (".html", ".css", ".js", ".svg", ".json", ".xml", ".txt", ".webmanifest")

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isfile(path) and path.endswith(self.GZ) and "gzip" in self.headers.get("Accept-Encoding", ""):
            raw = open(path, "rb").read()
            data = gzip.compress(raw, 6)
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(path))
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "public, max-age=31536000" if not path.endswith(".html") else "public, max-age=3600")
            self.end_headers()
            return io.BytesIO(data)
        return super().send_head()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
