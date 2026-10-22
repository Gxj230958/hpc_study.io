"""Execute reviewed manifest commands; never launch remote/cloud configurations."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("--gpu", action="store_true")
p.add_argument("--reference", action="store_true")
p.add_argument("--output", default="build/labs")
args = p.parse_args()
out = ROOT / args.output
out.mkdir(parents=True, exist_ok=True)
data = json.loads((ROOT / "course/labs.json").read_text())
env = dict(os.environ, OMP_NUM_THREADS="4", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
           NVIDIA_TF32_OVERRIDE="0", TORCH_ALLOW_TF32_CUBLAS_OVERRIDE="0")
env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
started = datetime.now(timezone.utc).isoformat()
sources = sorted({ROOT / s for lab in data["labs"] for s in lab["sources"]})
sources += [Path(__file__).resolve()]
hashes = {str(s.relative_to(ROOT)): hashlib.sha256(s.read_bytes()).hexdigest() for s in sources}
results = []


def run(lab_id, index, command, expected=0):
    log = out / f"{lab_id}-{index}.txt"
    begin = time.monotonic()
    timed_out = False
    with log.open("w") as stream:
        child = subprocess.Popen(["bash", "-c", command], cwd=ROOT, env=env,
                                 stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            code = child.wait(timeout=600 if lab_id == "reference-benchmarks" else 180)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(child.pid, signal.SIGKILL)
            code = child.wait()
    output = log.read_text()
    passed = code == expected and not timed_out
    if "examples/" in command and ".py" in command:
        passed = passed and ("LOST UPDATE" if expected == 1 else "PASS") in output
    return {"command": command, "expected_returncode": expected, "returncode": code,
            "timeout": timed_out, "passed": passed, "elapsed_seconds": time.monotonic()-begin,
            "log": str(log.relative_to(ROOT)), "output": output}


for lab in data["labs"]:
    result = {"id": lab["id"], "records": [], "primary_executed": False}
    if lab["module"] == "datacenter":
        commands = lab["commands"] if lab.get("analysis_only") else []
        result["status"] = "analysis-not-hardware-execution"
        result["records"] = [run(lab["id"], i, c) for i, c in enumerate(commands)]
    else:
        can_run = lab["local_executable"] and (args.gpu or not lab.get("requires_gpu"))
        if lab["id"] == "reference-benchmarks" and not args.reference:
            can_run = False
        if can_run:
            result["primary_executed"] = True
            result["records"] = [run(lab["id"], f"{repeat}-{i}", c, expected)
                                 for repeat in range(lab.get("repetitions", 1))
                                 for i, (c, expected) in enumerate(zip(lab["commands"], lab["expected_returncodes"]))]
            result["status"] = "passed-local-primary"
        else:
            result["status"] = "not-executed"
        if lab.get("fallback_commands"):
            result["fallback_records"] = [run(lab["id"] + "-fallback", i, c)
                                           for i, c in enumerate(lab["fallback_commands"])]
            if not can_run:
                result["status"] = "not-executed-primary; fallback-passed"
    all_records = result["records"] + result.get("fallback_records", [])
    if not all(r["passed"] for r in all_records):
        result["status"] = "failed"
    results.append(result)
    print(lab["id"], result["status"], flush=True)
assert hashes == {str(s.relative_to(ROOT)): hashlib.sha256(s.read_bytes()).hexdigest() for s in sources}, "Sources changed during validation"
report = {"started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
          "source_sha256": hashes, "labs": results, "all_executed_checks_passed": all(r["status"] != "failed" for r in results),
          "limitations": ["No multi-GPU or remote two-node execution", "Datacenter results are sourced analysis and calculations", "No AWS commands executed"]}
(out / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
raise SystemExit(not report["all_executed_checks_passed"])
