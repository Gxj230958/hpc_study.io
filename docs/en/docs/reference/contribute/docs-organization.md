# Documentation Organization

**Prerequisites:** [Contributing](before-contributing.md). **Objective:** Place content without breaking published links.

English lessons live in docs/en/docs. The explicit root configuration defines the course navigation. The unchanged docs/zh/docs tree is published with mkdocs.archive.yml into archive/zh, with its own Chinese search index.

course/url-map.json records every original Markdown source, source hash, destination and heading anchors. scripts/course.py defines migration rules. Moved legacy pages redirect directly to their final English targets; the archive remains available for original context.

Downloads are assembled from versioned examples, scripts and uv files by the build hook. Next, use [the writing conventions](docs-style.md).
