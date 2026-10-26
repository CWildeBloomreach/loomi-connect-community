import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "plugins" / "loomi-discovery" / "skills"
SCRIPT = SKILLS / "discovery-zero-results-triage" / "scripts" / "grid_summary.py"
COPIES = [SKILLS / "discovery-synonym-review" / "scripts" / "grid_summary.py"]
POSITIONS = [SKILLS / s / "scripts" / "grid_positions.py"
             for s in ("product-opportunity-finder", "brand-performance-review", "new-arrivals-tracker")]
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(script, *args):
    """Run a script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class GridSummaryTest(unittest.TestCase):
    def test_copies_are_identical(self):
        for other in COPIES:
            self.assertEqual(SCRIPT.read_bytes(), other.read_bytes(), other)
        for other in POSITIONS[1:]:
            self.assertEqual(POSITIONS[0].read_bytes(), other.read_bytes(), other)

    def test_help(self):
        for script in [SCRIPT, POSITIONS[0]]:
            p = run(script, "--help")
            self.assertEqual(p.returncode, 0, script)

    def test_call_tool_wrapper_and_debug_experiments(self):
        p = run(SCRIPT, FIX / "gs_grid_call_tool.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["numFound"], 3)
        self.assertEqual(out["titles"], ["Linen shirt"])
        self.assertEqual(out["ab_test_buckets"], ["exp_12:bucket_b"])
        self.assertEqual(out["ranking_rule_ids"], ["901"])

    def test_grid_positions_reads_the_same_file(self):
        p = run(POSITIONS[0], FIX / "gs_grid_call_tool.json", "--pids", "G1")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["positions"]["G1"]["position"], 1)
        self.assertEqual(out["ab_test_buckets"], ["exp_12:bucket_b"])

    def test_error_returned_as_data_stops(self):
        for script in (SCRIPT, POSITIONS[0]):
            p = run(script, FIX / "denied.json")
            self.assertEqual(p.returncode, 1, script)
            out = json.loads(p.stdout)
            self.assertFalse(out["ok"])
            self.assertIn("ACCESS_DENIED", out["error"])


if __name__ == "__main__":
    unittest.main()
