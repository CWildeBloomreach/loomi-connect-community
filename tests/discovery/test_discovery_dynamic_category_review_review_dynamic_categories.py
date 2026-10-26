import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-dynamic-category-review" / "scripts"
          / "review_dynamic_categories.py")
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args, copy=()):
    """Run the script by its full path from a fresh working folder, as an assistant would.

    Files named in `copy` are copied into the working folder under the same name, because the
    script reads category IDs from grid file names."""
    with tempfile.TemporaryDirectory() as tmp:
        for name in copy:
            shutil.copy(FIX / name, Path(tmp, name))
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class ReviewDynamicCategoriesTest(unittest.TestCase):
    def test_help(self):
        p = run("--help")
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_non_numeric_static_grid_id_is_matched(self):
        files = ("def_brg_dyn_k3sneak.json", "grid_brg_dyn_k3sneak.json", "grid_womens-sneakers.json")
        p = run("--definitions", files[0], "--grids", files[1], files[2], "--today", "2026-10-01", copy=files)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Duplicates a static category", p.stdout)
        self.assertIn("(42 products)", p.stdout)
        self.assertNotIn("Fetch womens-sneakers", p.stdout)
        self.assertNotIn("grid_womens-sneakers", p.stdout)

    def test_error_returned_as_data_stops(self):
        p = run("--definitions", FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", p.stderr)
        self.assertIn("don't treat it as 'nothing found'", p.stderr)


if __name__ == "__main__":
    unittest.main()
