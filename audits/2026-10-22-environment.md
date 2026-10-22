# Reorganization baseline: 2026-10-22

Starting commit: `6f8a86a`. The existing uncommitted uv environment work in
README.md, README-course.md, env-spec.json, scripts/run-reference-benchmarks.sh,
.python-version, pyproject.toml, scripts/activate-study.sh and uv.lock was
authorized in the implementation plan and is preserved in this series.

The previous audit reported 50 generated HTML pages with no broken internal
links. This is a historical baseline, not the result of the English rebuild.
Existing EXPERIMENT_AUDIT.json and EXPERIMENT_AUDIT.md remain historical.

Observed GPU: NVIDIA GeForce RTX 4090, driver 570.124.06. Its unusual reported
49140 MiB is not a course requirement. Labs target a conventional 24 GB card.
Observed Python environment: Python 3.10, PyTorch 2.6.0+cu124, uv 0.11.29.
The plan's OS/CPU/cgroup baseline will be rechecked in final validation.

The Chinese Markdown and bundled vendor licenses are frozen in place. The
English course will use a separate tree and a separate archive configuration.
No AWS commands will be executed. Node count, network topology, remote software,
SSH access, scheduler and open ports remain unresolved hardware-profile fields.
