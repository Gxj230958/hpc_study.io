"""Check generated local HTML links, assets and duplicate HTML ids."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
prefix = "/hpc_study.io/"
failures = []

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.duplicates = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])

pages = {}
for file in root.rglob("*.html"):
    parsed = Links()
    parsed.feed(file.read_text())
    pages[file] = parsed
for file, parsed in pages.items():
    if file.name == "404.html":
        continue
    for link in parsed.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        path = unquote(url.path)
        if path.startswith(prefix):
            target = root / path[len(prefix):]
        elif path.startswith("/"):
            target = root / path.lstrip("/")
        elif not path:
            target = file
        else:
            target = file.parent / path
        if target.is_dir():
            target /= "index.html"
        target = target.resolve()
        if not target.exists():
            failures.append(f"{file.relative_to(root)}: missing {link}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            failures.append(f"{file.relative_to(root)}: missing anchor {link}")
    for duplicate in parsed.duplicates:
        failures.append(f"{file.relative_to(root)}: duplicate id {duplicate}")
print(f"Checked {len(pages)} HTML pages; {len(failures)} failures")
for item in failures:
    print(item)
raise SystemExit(bool(failures))
