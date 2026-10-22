"""Validate the assessed curriculum, metadata, source links and closed answers."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("--final", action="store_true")
args = p.parse_args()
data = json.loads((ROOT / "course/labs.json").read_text())
modules = {"machine", "cpu", "mpi", "cuda", "measurement", "science", "distributed", "datacenter"}
assert set(data["assessed_modules"]) == modules
assert len(data["labs"]) == 24
ids = set()
levels = {"warm-up": 10, "core": 20, "stretch": 30}
required = {"id", "module", "difficulty", "duration_minutes", "hardware", "local_executable",
            "answer", "page", "anchor", "sources", "commands", "expected_returncodes",
            "validation_status", "task", "expected_behavior", "troubleshooting", "cleanup"}
for module in modules:
    members = [x for x in data["labs"] if x["module"] == module]
    assert len(members) == 3 and {x["difficulty"] for x in members} == set(levels), module
for lab in data["labs"]:
    assert required <= lab.keys(), lab["id"]
    assert lab["id"] not in ids, lab["id"]
    ids.add(lab["id"])
    assert lab["duration_minutes"] == levels[lab["difficulty"]]
    assert type(lab["local_executable"]) is bool and lab["answer"] is True
    for key in ("hardware", "task", "expected_behavior", "troubleshooting", "cleanup", "validation_status"):
        assert isinstance(lab[key], str) and lab[key].strip(), (lab["id"], key)
    assert lab["sources"] and all((ROOT / s).is_file() for s in lab["sources"]), lab["id"]
    assert len(lab["commands"]) == len(lab["expected_returncodes"])
    assert isinstance(lab.get("repetitions", 1), int) and 1 <= lab.get("repetitions", 1) <= 10
    if lab["local_executable"]:
        assert lab["commands"], lab["id"]
    text = (ROOT / "docs/en/docs" / lab["page"]).read_text()
    match = re.search(r"^## [^\n]*\{#" + re.escape(lab["anchor"]) + r"\}\n(.*?)(?=^## |\Z)",
                      text, flags=re.M | re.S)
    assert match, (lab["id"], "missing attached section")
    section = match[1]
    assert len(re.findall(r'^\?\?\? success "Answer"\s*$', section, re.M)) == 1, lab["id"]
    assert not re.search(r"^\?\?\?\+", section, re.M), lab["id"]
    for source in lab["sources"]:
        assert f"/downloads/source/{source}" in section, (lab["id"], source)
    for command in lab["commands"] + lab.get("fallback_commands", []):
        assert command in section, (lab["id"], "undocumented command", command)
    if args.final:
        assert lab["validation_status"] != "pending", lab["id"]
        evidence = lab["validation_evidence"]
        report = json.loads((ROOT / evidence["report"]).read_text())
        result = next(x for x in report["labs"] if x["id"] == lab["id"])
        assert result["status"] == lab["validation_status"], lab["id"]
print(f"Checked {len(modules)} modules, 24 experiments, source links and closed answers")
