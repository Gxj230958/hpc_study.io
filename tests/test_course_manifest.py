"""Exercise failure cases in the course manifest contract using isolated fixtures."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ManifestContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.data = json.loads((ROOT / "course/labs.json").read_text())
        sources = {"scripts/check-labs.py", "course/labs.json"}
        sources.update("docs/en/docs/" + lab["page"] for lab in self.data["labs"])
        sources.update(source for lab in self.data["labs"] for source in lab["sources"])
        for source in sources:
            target = self.root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / source, target)

    def tearDown(self):
        self.temp.cleanup()

    def check(self, expected):
        (self.root / "course/labs.json").write_text(json.dumps(self.data))
        result = subprocess.run([sys.executable, str(self.root / "scripts/check-labs.py")],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode == 0, expected, result.stdout + result.stderr)

    def test_complete_inventory(self):
        self.check(True)

    def test_missing_level(self):
        self.data["labs"][0]["difficulty"] = "core"
        self.check(False)

    def test_missing_metadata(self):
        del self.data["labs"][0]["hardware"]
        self.check(False)

    def test_missing_source(self):
        self.data["labs"][0]["sources"] = ["examples/does-not-exist.py"]
        self.check(False)

    def test_open_answer(self):
        page = self.root / "docs/en/docs" / self.data["labs"][0]["page"]
        page.write_text(page.read_text().replace('??? success "Answer"', '???+ success "Answer"', 1))
        self.check(False)

    def test_answer_attached_to_wrong_experiment(self):
        page = self.root / "docs/en/docs" / self.data["labs"][0]["page"]
        page.write_text(page.read_text().replace('??? success "Answer"', '??? note "Discussion"', 1))
        self.check(False)


if __name__ == "__main__":
    unittest.main()
