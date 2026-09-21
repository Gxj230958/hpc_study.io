"""Run small reproducible course checks and retain each command's raw output."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--gpu", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
os.chdir(root)
out = root / "build/validation"
out.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, OMP_NUM_THREADS="4", OPENBLAS_NUM_THREADS="4", MKL_NUM_THREADS="4")
env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
records = []
started_utc = datetime.now(timezone.utc).isoformat()
sources = sorted(p for p in (root / "examples").rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts)
sources += [Path(__file__).resolve(), root / "env-spec.json", root / "requirements-study.txt"]
source_hashes = {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}

def run(name, command, extra=None, expected_returncode=0):
    child_env = dict(env, **(extra or {}))
    result = subprocess.run(command, env=child_env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=180)
    (out / f"{name}.txt").write_text(result.stdout)
    passed = result.returncode == expected_returncode
    records.append({"name":name, "command":command, "env":extra or {},
                    "returncode":result.returncode, "expected_returncode":expected_returncode, "passed":passed})
    print(name, "PASS" if passed else "FAIL", flush=True)
    if not passed:
        print(result.stdout)

run("compile-cpu", ["make", "-B", "-C", "examples", "cpu"])
for threads in (1, 2, 4, 8):
    for n in (1, 17, 100003):
        run(f"sum-{threads}-{n}", ["./build/sum", str(n)], {"OMP_NUM_THREADS":str(threads)})
run("sum-invalid", ["./build/sum", "-1"], expected_returncode=2)
run("memory", ["./build/memory"])
for ranks in (1, 2, 3, 4):
    for n in (0, 2, 100003):
        run(f"mpi-{ranks}-{n}", ["mpiexec", "-n", str(ranks), sys.executable, "examples/mpi/sum.py", "--n", str(n)],
            {"OMP_NUM_THREADS":"1", "OPENBLAS_NUM_THREADS":"1"})
run("pingpong", ["mpiexec", "-n", "2", sys.executable, "examples/mpi/pingpong.py"])
run("solve", [sys.executable, "examples/science/solve.py"])
run("quantize", [sys.executable, "examples/ml/quantize.py"])
run("train-cpu", [sys.executable, "examples/ml/train.py", "--device", "cpu"])
if args.gpu:
    run("gpu-info", ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"])
    run("witness", [sys.executable, "examples/ml/witness.py"])
    run("compile-cuda", ["make", "-B", "-C", "examples", "cuda"])
    run("cuda", ["./build/cuda_labs"])
    for tool in ("memcheck", "synccheck", "racecheck"):
        run(f"cuda-{tool}", ["compute-sanitizer", "--error-exitcode", "1", "--tool", tool, "./build/cuda_labs"])
    run("train-cuda", [sys.executable, "examples/ml/train.py", "--device", "cuda"])
    run("precision", [sys.executable, "examples/ml/precision.py"])
assert source_hashes == {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}, "Source changed during validation"
summary = {"started_utc":started_utc, "timestamp_utc":datetime.now(timezone.utc).isoformat(),
           "source_sha256_at_start":source_hashes, "records":records,
           "all_passed":all(x["passed"] for x in records)}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
raise SystemExit(0 if summary["all_passed"] else 1)
