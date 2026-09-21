"""Archive actual validation output with hashes of the tested source files."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
stamp = datetime.now(timezone.utc)
destination = root / "docs/zh/docs/learning/results" / stamp.strftime("%Y-%m-%d")
destination.mkdir(parents=True, exist_ok=True)
summary = json.loads((root / "build/validation/summary.json").read_text())
if not summary["all_passed"]:
    raise SystemExit("Refusing to publish a passing record for a failing suite")
for name, expected in summary["source_sha256_at_start"].items():
    actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"Source changed since validation: {name}")
shutil.copytree(root / "build/validation", destination / "checks", dirs_exist_ok=True)
reference = root / "build/reference"
for name in ("hpl/output.txt", "hpcg-revision.txt", "hpl-archive-sha256.txt"):
    target = destination / "reference" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(reference / name, target)
latest_hpcg = sorted(reference.glob("hpcg-20*"))[-1]
for file in latest_hpcg.glob("*.txt"):
    shutil.copy2(file, destination / "reference" / file.name)
browser = root / "build/browser/summary.json"
if browser.exists():
    shutil.copy2(browser, destination / "browser-summary.json")
nsys = root / ".tools/nsys/nsight-systems/2023.4.4/target-linux-x64/nsys"
result = subprocess.run([str(nsys), "stats", "--force-export=true", "--report", "cuda_gpu_kern_sum,cuda_gpu_mem_time_sum", "build/cuda-trace.nsys-rep"],
                        cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
(destination / "nsys-stats.txt").write_text(result.stdout)
sources = sorted(file for file in (root / "examples").rglob("*")
                 if file.is_file() and "__pycache__" not in file.parts)
sources += [root / name for name in (
    "scripts/validate.py", "scripts/install-cuda.py", "scripts/run-reference-benchmarks.sh",
    "scripts/archive-validation.py", "env-spec.json", "requirements-study.txt")]
metadata = {
    "recorded_utc":stamp.isoformat(),
    "scope":"single-node teaching correctness checks; HPL/HPCG short runs are not official submissions",
    "packages":{name:importlib.metadata.version(name) for name in ("torch", "numpy", "scipy", "mpi4py-mpich")},
    "cuda_toolkit":"12.4.1",
    "profiler_note":"Nsight Systems capture is separate from the unprofiled correctness/timing run.",
    "cgroup_cpu_max":Path("/sys/fs/cgroup/cpu.max").read_text().strip(),
    "cgroup_memory_max":Path("/sys/fs/cgroup/memory.max").read_text().strip(),
    "source_sha256":{str(file.relative_to(root)):hashlib.sha256(file.read_bytes()).hexdigest() for file in sources},
    "not_tested":["multi-GPU NCCL", "multi-node network", "AMD HIP", "OpenCL device path", "NVIDIA OpenACC offload"],
}
(destination / "environment.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
print(destination)
