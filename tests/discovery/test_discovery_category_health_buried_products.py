import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-category-health" / "scripts"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(script, *args):
    """Run a script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class BuriedProductsTest(unittest.TestCase):
    def test_help(self):
        p = run("buried_products.py", "--help")
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_null_rates_in_top_window_do_not_crash(self):
        p = run("buried_products.py", "--grid", FIX / "bp_grid.json", FIX / "bp_products_null_rates.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertIsNone(out["top_window"]["median_rpv"])
        self.assertIsNone(out["top_window"]["median_conversion_rate"])
        self.assertEqual(out["buried"], [])
        self.assertIn("weren't judged", out["note"])

    def test_brand_names_trimmed_on_both_sides(self):
        p = run("buried_products.py", "--grid", FIX / "bp_grid.json", FIX / "bp_products_null_rates.json")
        out = json.loads(p.stdout)
        top = dict(out["top_window"]["brands"])
        self.assertIn("Pacifica", top)
        self.assertNotIn("Pacifica ", top)
        missing = [b for b, _ in out["brands_missing_from_top"]]
        self.assertEqual(missing, ["Tailspin"])  # "Pacifica" is in the top window

    def test_error_returned_as_data_stops(self):
        for args in (("buried_products.py", "--grid", FIX / "denied.json"),
                     ("buried_products.py", "--grid", FIX / "bp_grid.json", FIX / "denied.json")):
            p = run(*args)
            self.assertEqual(p.returncode, 1, args)
            out = json.loads(p.stdout)
            self.assertFalse(out["ok"])
            self.assertIn("ACCESS_DENIED", out["error"])


if __name__ == "__main__":
    unittest.main()
