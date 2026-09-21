"""Keep the independent site's homepage outside the upstream tutorial changes."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def on_page_markdown(markdown, page, **kwargs):
    if page.file.src_uri == "index.md":
        return (ROOT / "site-content/home.md").read_text()
    return markdown

def on_post_build(config, **kwargs):
    dest = Path(config["site_dir"]) / "downloads"
    dest.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest / "hpc-study-examples.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((ROOT / "examples").rglob("*")):
            if file.is_file() and "__pycache__" not in file.parts:
                archive.write(file, file.relative_to(ROOT))
        for name in ("requirements-study.txt", "env-spec.json", "LICENSE", "README-course.md"):
            archive.write(ROOT / name, name)
        for name in ("install-cuda.py", "validate.py", "run-reference-benchmarks.sh"):
            archive.write(ROOT / "scripts" / name, "scripts/" + name)
