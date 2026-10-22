"""Serve the built project at the same URL prefix as GitHub Pages."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

p = argparse.ArgumentParser()
p.add_argument("--port", type=int, default=8008)
args = p.parse_args()
root = Path(__file__).resolve().parents[1] / "site"


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        prefix = "/hpc_study.io/"
        if path.startswith(prefix):
            path = "/" + path[len(prefix):]
        else:
            path = "/__not_published__"
        return super().translate_path(path)

    def do_GET(self):
        path = urlsplit(self.path).path
        prefix = "/hpc_study.io"
        if path in ("/", prefix):
            self.send_response(302)
            self.send_header("Location", prefix + "/")
            self.end_headers()
            return
        if not path.startswith(prefix + "/"):
            self.send_error(404)
            return
        super().do_GET()


print(f"http://127.0.0.1:{args.port}/hpc_study.io/", flush=True)
ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(root))).serve_forever()
