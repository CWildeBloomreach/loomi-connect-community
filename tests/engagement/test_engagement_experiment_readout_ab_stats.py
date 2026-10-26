import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/engagement-experiment-readout/scripts/ab_stats.py"
FIXTURES = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


def run_cfg(cfg):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "counts.json"
        p.write_text(json.dumps(cfg))
        return subprocess.run([sys.executable, str(SCRIPT), "counts.json"],
                              cwd=tmp, capture_output=True, text=True)


class AbStatsTest(unittest.TestCase):
    def test_help(self):
        r = run("--help")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("--example", r.stdout)

    def test_example_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            ex = subprocess.run([sys.executable, str(SCRIPT), "--example"], cwd=tmp,
                                capture_output=True, text=True, check=True).stdout
            (Path(tmp) / "c.json").write_text(ex)
            r = subprocess.run([sys.executable, str(SCRIPT), "c.json"], cwd=tmp, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("already left out", r.stdout)

    def test_messy_input(self):
        r = run(FIXTURES / "ab_stats_messy.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout
        # string counts and "$1,234.00" revenue parse
        self.assertIn("| Variant A | 5,000 | 60 | 1.20% | 1,234.00 |", out)
        # n=0 variant is reported, not a crash
        self.assertIn("**Variant B** is left out of the tests", out)
        self.assertIn("Variant B: **not tested**", out)
        # control with 0 conversions: direction comes from the absolute difference
        self.assertIn("Variant A: **significantly better**", out)
        # periods without the control are skipped with a note
        self.assertIn("week 1: skipped (no control counts)", out)
        # mixed customers: honest about not removing them
        self.assertIn("does not remove them", out)

    def test_significantly_worse_with_zero_variant_conversions(self):
        r = run_cfg({"metric": "conversion", "variants": [
            {"name": "C", "n": 5000, "conversions": 80}, {"name": "A", "n": 5000, "conversions": 0}]})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("A: **significantly worse**", r.stdout)

    def test_control_without_customers_stops(self):
        r = run_cfg({"variants": [{"name": "C", "n": "0", "conversions": 0}, {"name": "A", "n": 10, "conversions": 1}]})
        self.assertEqual(r.returncode, 1)
        self.assertIn("can't be tested", r.stdout)

    def test_revenue_strings(self):
        r = run_cfg({"metric": "revenue", "currency": "$", "variants": [
            {"name": "C", "n": "1,000", "conversions": "50", "revenue": "$2,500.00"},
            {"name": "A", "n": "1000", "conversions": "55", "revenue": "£2,750"}]})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("revenue per customer $2.50 → $2.75", r.stdout)


if __name__ == "__main__":
    unittest.main()
