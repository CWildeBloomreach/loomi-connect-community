import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/segment-opportunity-finder/scripts/rank_opportunities.py"
FX = ROOT / "tests/fixtures/engagement"


class RankOpportunitiesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, str(SCRIPT), str(FX / "opportunities.json"), "--format", "json"],
                               cwd=tmp, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        cls.rows = {r["name"]: r for r in json.loads(r.stdout)}

    def value(self, name):
        return round(self.rows[name]["value"], 6)

    def test_help(self):
        self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True).returncode, 0)

    def test_value_basis_per_pattern(self):
        # size 1000 x default rate x value basis; store AOV $100
        self.assertEqual(self.value("Browsed shoes, never bought"), round(1000 * 0.02 * 80, 6))
        self.assertEqual(self.value("One-time buyers"), round(1000 * 0.05 * 100, 6))
        self.assertEqual(self.value("VIP slowdown"), round(1000 * 0.10 * 150, 6))
        self.assertEqual(self.value("Discount-led"), round(1000 * 0.10 * 20, 6))
        self.assertEqual(self.value("Cart abandoners"), round(1000 * 0.05 * 120, 6))
        self.assertEqual(self.value("New, no second order"), round(1000 * 0.08 * 100, 6))
        self.assertEqual(self.value("No consent"), round(1000 * 0.10 * 50, 6))

    def test_missing_basis_is_noted(self):
        self.assertEqual(self.value("Discount-led, no depth"), 0)
        self.assertIn("no value: discount_depth missing", self.rows["Discount-led, no depth"]["notes"])
        self.assertEqual(self.value("Affinity x trend"), round(1000 * 0.03 * 100, 6))
        self.assertIn("store AOV (category AOV not given)", self.rows["Affinity x trend"]["notes"])


if __name__ == "__main__":
    unittest.main()
