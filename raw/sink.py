import http.server, os, time

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)

PAGE = b"""<script>
addEventListener('message', async e => {
  const m = e.data;
  if (m.get) {
    const r = await fetch('/f/' + m.get);
    e.source.postMessage({file: m.get, ok: r.ok, body: r.ok ? await r.text() : null}, '*');
  } else if (m.name) {
    await fetch('/' + m.name, {method: 'POST', body: m.body});
    e.source.postMessage({saved: m.name}, '*');
  }
});
</script>sink"""


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.startswith("/lib/"):
            with open(os.path.join(OUT, "collector.js"), "rb") as f:
                body = b"window.__fbCollector = function () {\n" + f.read() + b"\n};"
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/f/"):
            rel = self.path[3:].lstrip("/")
            p = os.path.normpath(os.path.join(ROOT, rel))
            if not p.startswith(ROOT) or not os.path.exists(p):
                self.send_response(404)
                self.end_headers()
                return
            self.send_response(200)
            self.end_headers()
            with open(p, "rb") as f:
                self.wfile.write(f.read())
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(PAGE)

    def do_POST(self):
        rel = self.path.strip("/").lstrip("/")
        p = os.path.normpath(os.path.join(ROOT, rel)) if rel else os.path.join(OUT, f"batch_{int(time.time())}.json")
        if not p.startswith(ROOT):
            p = os.path.join(OUT, os.path.basename(rel))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        with open(p, "wb") as f:
            f.write(data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")


http.server.HTTPServer(("127.0.0.1", 8765), H).serve_forever()
