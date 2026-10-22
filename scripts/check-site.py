"""Check generated local HTML links, assets and duplicate HTML ids."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import json
import re
from urllib.parse import urljoin

root = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
prefix = "/hpc_study.io/"
failures = []

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.duplicates = []
        self.redirect = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            match = re.search(r"url\s*=\s*(.+)", attrs.get("content", ""), re.I)
            if match:
                self.redirect = match[1].strip("\"' ")
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if attrs.get("srcset"):
            self.links.extend(x.strip().split()[0] for x in attrs["srcset"].split(","))

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

for file in pages:
    visited = set()
    target = file
    while target in pages and pages[target].redirect:
        if target in visited:
            failures.append(f"Redirect loop starting at {file.relative_to(root)}")
            break
        visited.add(target)
        relative = pages[target].redirect
        target = (target.parent / unquote(urlsplit(relative).path)).resolve()
        if target.is_dir():
            target /= "index.html"

mapping = Path("course/url-map.json")
if mapping.exists() and (root / "archive/zh").exists():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from course import url, redirects
    for record in json.loads(mapping.read_text()):
        destination = (root / url(record["english"]) / "index.html").resolve()
        archived = (root / url(record["archive"]) / "index.html").resolve()
        for target in (destination, archived):
            if target not in pages:
                failures.append(f"Mapping target missing: {target}")
                continue
            for heading in record["anchors"]:
                if heading["id"] not in pages[target].ids:
                    failures.append(f"Compatibility anchor missing: {target.relative_to(root)}#{heading['id']}")
    for old, new in redirects().items():
        source = (root / url(old) / "index.html").resolve()
        target = (root / url(new) / "index.html").resolve()
        if source not in pages or not pages[source].redirect:
            failures.append(f"Missing redirect: {old}")
        else:
            actual = (source.parent / pages[source].redirect).resolve()
            if actual.is_dir():
                actual /= "index.html"
            if actual != target:
                failures.append(f"Incorrect redirect {old}: {actual}")
print(f"Checked {len(pages)} HTML pages; {len(failures)} failures")
for item in failures:
    print(item)
raise SystemExit(bool(failures))
