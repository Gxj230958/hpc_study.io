"""Publish dated English evidence after successful lab, site and browser checks."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = "audits/2026-10-22-validation.json"
labs = json.loads((ROOT / "build/labs/summary.json").read_text())
suite = json.loads((ROOT / "build/validation/summary.json").read_text())
browser = json.loads((ROOT / "build/browser-english/summary.json").read_text())
cpu = json.loads((ROOT / "build/labs-cpu/summary.json").read_text())
assert labs["all_executed_checks_passed"] and suite["all_passed"] and browser["passed"]
assert cpu["all_executed_checks_passed"]
for report, key in ((labs, "source_sha256"), (suite, "source_sha256_at_start")):
    for name, expected in report[key].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
assert hashlib.sha256((ROOT / "scripts/browser-check.py").read_bytes()).hexdigest() == browser["script_sha256"]
build_log = (ROOT / "build/english-site-build.log").read_text()
assert "Checked 179 HTML pages; 0 failures" in build_log
manifest = json.loads((ROOT / "course/labs.json").read_text())
for lab in manifest["labs"]:
    record = next(x for x in labs["labs"] if x["id"] == lab["id"])
    lab["validation_status"] = record["status"]
    lab["validation_evidence"] = {"report": TARGET, "lab_id": lab["id"],
                                  "executed_utc": labs["finished_utc"]}
(ROOT / "course/labs.json").write_text(json.dumps(manifest, indent=2) + "\n")


def command(args):
    result = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=30)
    return {"command": args, "returncode": result.returncode, "output": result.stdout}


tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
source_files = sorted(set(tracked + untracked))
hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
          for name in source_files if (ROOT / name).is_file() and not name.startswith("audits/")}
changed = subprocess.check_output(["git", "diff", "--name-only", "6f8a86a"], cwd=ROOT, text=True).splitlines()
for item in suite["records"]:
    item["output"] = (ROOT / "build/validation" / (item["name"] + ".txt")).read_text()
reference_dir = ROOT / "build/reference"
latest_hpcg = sorted(reference_dir.glob("hpcg-20*"))[-1]
reference_files = [reference_dir / "hpl/output.txt", reference_dir / "hpcg-revision.txt",
                   reference_dir / "hpl-archive-sha256.txt"] + list(latest_hpcg.glob("*.txt"))
report = {"recorded_utc": datetime.now(timezone.utc).isoformat(),
          "baseline_commit": "6f8a86a", "scope": "English course reorganization; local teaching correctness and browser validation",
          "lab_execution": {k: v for k, v in labs.items() if k != "labs"}, "labs": labs["labs"],
          "correctness_suite": suite, "browser": browser,
          "cpu_extra_validation": cpu,
          "strict_build": {"command": ["uv", "run", "--only-group", "docs", "python", "scripts/build-site.py"],
                           "environment": {"UV_PROJECT_ENVIRONMENT": "/tmp/hpc-study-docs"}, "html_pages": 179,
                           "internal_link_asset_anchor_redirect_failures": 0, "log": build_log},
          "external_links": json.loads((ROOT / "audits/2026-10-22-external-links.json").read_text()),
          "additional_checks": [command([sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
                                command(["/tmp/hpc-study-docs/bin/python", "-c", "import importlib.util; assert importlib.util.find_spec('torch') is None; print('PASS docs-only environment excludes torch')"]),
                                command(["env", "-u", "LD_LIBRARY_PATH", "/tmp/hpc-study-cpu/bin/python", "-c", "import torch; assert torch.version.cuda is None; print(torch.__version__, 'PASS CPU-only runtime')"])],
          "environment": {"os": platform.platform(), "python": sys.version,
                          "packages": {name: importlib.metadata.version(name) for name in
                                       ("torch", "numpy", "scipy", "mpi4py-mpich", "mkdocs", "mkdocs-material", "playwright")},
                          "cgroup_cpu_max": Path("/sys/fs/cgroup/cpu.max").read_text().strip(),
                          "cgroup_memory_max": Path("/sys/fs/cgroup/memory.max").read_text().strip(),
                          "tools": [command(c) for c in (["uv", "--version"], ["gcc", "--version"],
                              ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"],
                              [str(ROOT / ".tools/cuda/bin/nvcc"), "--version"],
                              [str(ROOT / ".tools/cuda/bin/compute-sanitizer"), "--version"])]},
          "reference_outputs": {str(f.relative_to(ROOT)): f.read_text() for f in reference_files},
          "source_sha256": hashes, "hash_scope": "Versioned course sources and new files; generated audits excluded to avoid self-reference",
          "changed_files": sorted(set(changed + untracked)),
          "todo": ["Execute the two-GPU NCCL configuration on allocated hardware",
                   "Fill remote hardware profile and execute two-node TCP DDP",
                   "Recheck inaccessible and timed-out external references from another network",
                   "Validate datacenter-specific profiling and porting assumptions after allocation"],
          "limitations": ["No A100/H100/H200 execution; specifications are sourced and rooflines calculated",
                          "No AWS commands executed and no cloud resources provisioned",
                          "HPL/HPCG are bounded teaching workloads, not official submissions",
                          "Original September audit artifacts remain historical",
                          "Compatibility anchors can point to source attribution rather than translated section context"],
          "resolved_during_validation": ["Repeat profiling initially refused a stale SQLite export; --force-export=true was added and rerun successfully",
                                         "CI exposed mobile language-menu overflow under wider font metrics; shared CSS aligns the popup and browser checks stress both menus",
                                         "CPU wheel initially loaded an unrelated Python 3.12 library via inherited LD_LIBRARY_PATH; CPU validation used env -u LD_LIBRARY_PATH",
                                         "Chromium download retried and missing Linux browser libraries were installed"]}
assert all(check["returncode"] == 0 for check in report["additional_checks"])
(ROOT / TARGET).write_text(json.dumps(report, indent=2) + "\n")
print(TARGET)
