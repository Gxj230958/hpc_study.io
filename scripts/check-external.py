"""Audit external references separately; access failures are not invented link status."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
references = {}


class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.source = source

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        # Canonical URLs and edit links are not lesson references.
        if tag not in ("a", "img", "script"):
            return
        for key in ("href", "src"):
            link = attrs.get(key, "")
            url = urlsplit(link)
            if url.scheme not in ("https", "http"):
                continue
            if url.netloc == "gxj230958.github.io":
                continue
            references.setdefault(urldefrag(link)[0], set()).add(self.source)


pages = sorted((ROOT / "site").rglob("*.html"))
for source in pages:
    Links(str(source.relative_to(ROOT / "site"))).feed(source.read_text())


def check(item):
    url, sources = item
    result = {"url": url, "pages": sorted(sources)}
    try:
        request = Request(url, method="HEAD", headers={"User-Agent": "HPCStudy-LinkAudit/1.0"})
        try:
            response = urlopen(request, timeout=12)
        except HTTPError as error:
            if error.code != 405:
                raise
            response = urlopen(Request(url, headers={"User-Agent": "HPCStudy-LinkAudit/1.0"}), timeout=12)
        with response:
            result.update(status="reachable", http_status=response.status, final_url=response.url)
    except HTTPError as error:
        result.update(status="inaccessible-from-validation-host", http_status=error.code,
                      error=str(error))
    except (URLError, TimeoutError, OSError, ValueError) as error:
        result.update(status="not-verified", error=str(error))
    return result


with ThreadPoolExecutor(max_workers=8) as pool:
    records = list(pool.map(check, sorted(references.items())))
report = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "html_pages_scanned": len(pages), "records": records,
          "counts": {s: sum(r["status"] == s for r in records)
                     for s in ("reachable", "inaccessible-from-validation-host", "not-verified")},
          "limitations": "HEAD/GET reachability only; remote content and external heading anchors are not verified. A blocked request does not prove a broken page."}
target = ROOT / "audits/2026-10-22-external-links.json"
target.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report["counts"]))
