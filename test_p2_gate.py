import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).with_name("p2_gate.py")


class GateTest(unittest.TestCase):
    def check(self, state, roadmap, expected, identities=None, launch=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            planning = root / ".planning"
            planning.mkdir()
            files = {"STATE.md": state, "ROADMAP.md": roadmap}
            if identities is not None:
                files["p2-completed.json"] = identities
            for name, content in files.items():
                (planning / name).write_text(content, encoding="utf-8")
            command = [sys.executable, str(GATE), str(root)]
            if launch:
                command += ["--", sys.executable, "-c",
                            "from pathlib import Path; Path('ran').touch()"]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stderr)
            self.assertEqual((root / "ran").exists(), launch and expected == 0)
            for name, content in files.items():
                self.assertEqual((planning / name).read_text(encoding="utf-8"), content)

    def test_zero(self):
        self.check("Progress: 0/1", "- [ ] **Phase 1: A**", 0, launch=True)

    def test_equal_counts_different_identity(self):
        self.check("Progress: 1/2", "- [x] **Phase 1: A**\n- [ ] **Phase 2: B**",
                   2, '["2"]', launch=True)

    def test_equal_counts_matching_identity(self):
        self.check("Progress: 1/2", "- [x] **Phase 1: A**\n- [ ] **Phase 2: B**",
                   0, '["01"]')

    def test_missing_identity(self):
        self.check("Progress: 1/1", "- [x] **Phase 1: A**", 3, launch=True)

    def test_count_conflict(self):
        self.check("Progress: 1/1", "- [ ] **Phase 1: A**", 2, launch=True)

    def test_duplicate_phase(self):
        self.check("Progress: 0/2", "- [ ] **Phase 1: A**\n- [ ] **Phase 01: A**", 3)

    def test_bad_identity_file(self):
        self.check("Progress: 1/1", "- [x] **Phase 1: A**", 3, '["1", 1]')


if __name__ == "__main__":
    unittest.main()
