"""Share course presentation fixes without changing frozen Chinese sources."""
from pathlib import Path
from mkdocs.structure.files import File


def on_files(files, config, **kwargs):
    root = Path(__file__).resolve().parents[1]
    files.append(File("course.css", str(root / "site-content"), config["site_dir"],
                      config["use_directory_urls"], dest_uri="static/css/course.css"))
    return files
