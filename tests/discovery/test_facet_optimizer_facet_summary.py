import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "facet-optimizer" / "scripts" / "facet_summary.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class FacetSummaryTest(unittest.TestCase):
    def test_help(self):
        p = run("--help")
        self.assertEqual(p.returncode, 0)
        self.assertIn("merge_candidates", p.stdout)

    def test_same_named_categories_are_not_merge_candidates(self):
        p = run(FIX / "fs_grid.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        facets = {f["name"]: f for f in json.loads(p.stdout.splitlines()[0])["facets"]}
        self.assertNotIn("merge_candidates", facets["category"]["flags"])
        self.assertNotIn("merge", facets["category"])
        self.assertIn("merge_candidates", facets["color"]["flags"])
        self.assertEqual(facets["color"]["merge"], [["Grey", "grey"]])

    def test_error_returned_as_data_stops(self):
        p = run(FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("ACCESS_DENIED", out["error"])


if __name__ == "__main__":
    unittest.main()
