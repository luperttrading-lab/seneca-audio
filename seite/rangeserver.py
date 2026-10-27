import http.server, os, re, sys
class H(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path); rng = self.headers.get("Range")
        if not rng or not os.path.isfile(path): return super().send_head()
        size = os.path.getsize(path); a, b = re.match(r"bytes=(\d*)-(\d*)", rng).groups()
        a = int(a) if a else 0; b = int(b) if b else size - 1
        f = open(path, "rb"); f.seek(a)
        self.send_response(206); self.send_header("Content-Type", self.guess_type(path)); self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {a}-{b}/{size}"); self.send_header("Content-Length", str(b - a + 1)); self.end_headers()
        self.rest = b - a + 1; return f
    def copyfile(self, src, dst):
        n = getattr(self, "rest", None)
        if n is None: return super().copyfile(src, dst)
        dst.write(src.read(n))
    def log_message(self, *a): pass
os.chdir(sys.argv[1]); http.server.ThreadingHTTPServer(("127.0.0.1", 8766), H).serve_forever()
