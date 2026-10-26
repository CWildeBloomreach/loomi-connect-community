import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "brand-performance-review" / "scripts" / "brand_scorecard.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args, files=None):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in (files or {}).items():
            Path(tmp, name).write_text(json.dumps(content), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class BrandScorecardTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_error_returned_as_data_stops(self):
        p = run("--brands", FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("ACCESS_DENIED", out["error"])
        p = run("--brands", FIX / "denied.json", "--markdown")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error", p.stderr)

    def test_pound_and_blank_figures(self):
        rows = [{"brand": "Contoso", "visits": "2,000", "prev_visits": "", "atc": 100, "conversions": 40,
                 "revenue": "£4,000.00", "prev_revenue": "N/A"},
                {"brand": "Tailspin", "visits": 1000, "prev_visits": 900, "atc": 50, "conversions": 20,
                 "revenue": "$1,000.00", "prev_revenue": "$900.00"}]
        p = run("--brands", "b.json", "--min-visits", "1", files={"b.json": {"data": {"rows": rows}}})
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["account"]["revenue"], 5000.0)
        self.assertEqual(out["account"]["visits"], 3000)


if __name__ == "__main__":
    unittest.main()
