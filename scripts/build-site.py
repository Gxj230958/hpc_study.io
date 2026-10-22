"""Build English first, then the independent frozen Chinese archive."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for config in ("mkdocs.study.yml", "mkdocs.archive.yml"):
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "-f", config],
                   cwd=root, check=True)
subprocess.run([sys.executable, "scripts/check-site.py", "site"], cwd=root, check=True)
