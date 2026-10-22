"""Assets, compatibility anchors and downloadable runnable sources."""
import html
import os
from pathlib import Path
import sys
import zipfile
from mkdocs.structure.files import File

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course import ROOT, ZH, headings, inventory, redirects, url


def on_config(config, **kwargs):
    for plugin in config.plugins.values():
        if plugin.__class__.__module__.startswith("mkdocs_redirects"):
            plugin.config["redirect_maps"] = redirects()
    return config


def on_files(files, config, **kwargs):
    for source in sorted(ZH.rglob("*")):
        if source.is_file() and source.suffix != ".md":
            files.append(File(source.relative_to(ZH).as_posix(), str(ZH),
                              config["site_dir"], config["use_directory_urls"]))
    return files


def on_page_markdown(markdown, page, **kwargs):
    records = [r for r in inventory() if r["english"] == page.file.src_uri]
    if records:
        existing = {h["id"] for h in headings(markdown)}
        links = []
        for record in records:
            archive = "/hpc_study.io/" + url(record["archive"])
            links.append(f'[{record["original"]}]({archive})')
        markdown += "\n\n## Sources and Attribution\n\nAdapted from HPC Wiki Team and contributors under CC BY-NC-SA 4.0. Frozen originals: " + ", ".join(links) + ".\n"
        if page.file.src_uri == "gpu/cuda.md":
            markdown += "\nCUDA teaching material originally by interestingLSY, Peking University supercomputing team.\n"
        for record in records:
            for h in record["anchors"]:
                if h["id"] not in existing:
                    markdown += f'\n<span id="{html.escape(h["id"], quote=True)}"></span>\n'
                    existing.add(h["id"])
    return markdown


def on_post_build(config, **kwargs):
    import shutil
    dest = Path(config["site_dir"]) / "downloads"
    dest.mkdir(exist_ok=True)
    sources = [p for p in (ROOT / "examples").rglob("*")
               if p.is_file() and "__pycache__" not in p.parts]
    sources += [ROOT / name for name in ("pyproject.toml", "uv.lock", ".python-version",
                "env-spec.json", "LICENSE", "README-course.md", "requirements-study.txt")]
    sources += [p for p in (ROOT / "scripts").glob("*") if p.is_file()
                and p.suffix in (".sh", ".py")]
    sources += list((ROOT / "course").glob("*.json"))
    with zipfile.ZipFile(dest / "hpc-study-examples.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(sources):
            relative = source.relative_to(ROOT)
            archive.write(source, relative)
            target = dest / "source" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for name in ("url-map", "labs"):
        shutil.copyfile(ROOT / f"course/{name}.json", dest / f"{name}.json")
    report = ROOT / "audits/2026-10-22-validation.json"
    if report.exists():
        shutil.copyfile(report, dest / "validation.json")
