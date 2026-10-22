"""Shared migration rules. Chinese source content is never rewritten."""
from pathlib import Path
import hashlib
import json
import markdown
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
ZH = ROOT / "docs/zh/docs"
EN = ROOT / "docs/en/docs"


def destination(path):
    if path == "hardware/gpu.md":
        return "gpu/arch.md"
    if path == "static/vendor/README.md":
        return "reference/licenses.md"
    for prefix, replacement in (("platform/", "clusters/"), ("hpc-intro/", "foundations/")):
        if path.startswith(prefix):
            return replacement + path[len(prefix):]
    if path in ("gpu/openacc.md", "gpu/opencl.md", "gpu/hip.md"):
        return "reference/programming-models/" + path.split("/")[-1]
    if path.split("/")[0] in ("competition", "power-management", "misc", "contribute"):
        return "reference/" + path
    return path


def headings(text):
    md = markdown.Markdown(extensions=["toc", "attr_list", "pymdownx.superfences"])
    md.convert(text)
    def flatten(nodes):
        return [item for node in nodes for item in
                [{"id": node["id"], "title": node["name"]}] + flatten(node["children"])]
    return flatten(md.toc_tokens)


@lru_cache(maxsize=1)
def inventory():
    return [{"original": p.relative_to(ZH).as_posix(),
             "english": destination(p.relative_to(ZH).as_posix()),
             "archive": "archive/zh/" + p.relative_to(ZH).as_posix(),
             "original_url": "/hpc_study.io/" + url(p.relative_to(ZH).as_posix()),
             "english_url": "/hpc_study.io/" + url(destination(p.relative_to(ZH).as_posix())),
             "archive_url": "/hpc_study.io/archive/zh/" + url(p.relative_to(ZH).as_posix()),
             "source_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
             "anchors": headings(p.read_text()),
             "anchor_policy": "compatibility anchor; consult archived original for context"}
            for p in sorted(ZH.rglob("*.md"))]


def redirects():
    result = {r["original"]: r["english"] for r in inventory()
              if r["original"] != r["english"] and not r["original"].startswith("static/")}
    result["performance-analysis/nsys.md"] = "gpu/nsys.md"
    return result


def url(path):
    name = path.rsplit("/", 1)[-1]
    return path[:-len(name)] if name in ("index.md", "README.md") else path[:-3] + "/"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "course/url-map.json"
    data = json.dumps(inventory(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        assert target.read_text() == data, "URL map or frozen source hashes have changed"
        for record in inventory():
            assert (EN / record["english"]).is_file(), record["english"]
        print(f"Checked {len(inventory())} original Markdown mappings and frozen hashes")
    else:
        target.parent.mkdir(exist_ok=True)
        target.write_text(data)
