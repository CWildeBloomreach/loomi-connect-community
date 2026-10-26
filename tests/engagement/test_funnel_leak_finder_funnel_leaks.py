import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/funnel-leak-finder/scripts/funnel_leaks.py"
FIXTURES = ROOT / "tests/fixtures/engagement"


def run_json(cfg_or_path):
    with tempfile.TemporaryDirectory() as tmp:
        if isinstance(cfg_or_path, dict):
            (Path(tmp) / "funnel.json").write_text(json.dumps(cfg_or_path))
            path = "funnel.json"
        else:
            path = str(cfg_or_path)
        r = subprocess.run([sys.executable, str(SCRIPT), path, "--format", "json"],
                           cwd=tmp, capture_output=True, text=True)
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout)


class FunnelLeaksTest(unittest.TestCase):
    def test_help(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)

    def test_abandoned_carts_use_cart_step_not_last_step(self):
        out = run_json(FIXTURES / "funnel_checkout.json")
        a = out["abandoned_carts"]
        self.assertEqual(a["cart_step"], "Added to cart")
        self.assertEqual(a["customers"], 4000 - 1500)  # not checkout - purchase (500)
        self.assertEqual(a["value_in_carts"], 2500 * 90)
        self.assertEqual(out["counts"][0], 20000)  # "20,000" parsed
        self.assertEqual(out["aov"], 80.0)  # "$80.00" parsed

    def test_explicit_cart_step(self):
        out = run_json({"steps": ["View", "Basket add", "Checkout", "Buy"], "counts": [1000, 600, 300, 200],
                        "aov": 50, "cart_step": 2})
        self.assertEqual(out["abandoned_carts"]["customers"], 100)

    def test_unreliable_purchase_still_reports_view_to_cart(self):
        out = run_json(FIXTURES / "funnel_unreliable_purchase.json")
        view_to_cart, cart_to_buy = out["rows"]
        self.assertIsNotNone(view_to_cart["value_walking_away"])
        self.assertIsNone(cart_to_buy["value_walking_away"])
        self.assertEqual(out["biggest_leak"]["to"], "Added to cart")
        self.assertIsNone(out["abandoned_carts"])  # cart -> purchase can't be measured
        self.assertTrue(out["caveats"])

    def test_missing_count_is_flagged(self):
        out = run_json({"steps": ["View", "Cart", "Buy"], "counts": [1000, "N/A", 50], "aov": 40})
        self.assertEqual(out["counts"][1], 0)
        self.assertTrue(any("missing" in c for c in out["caveats"]))


if __name__ == "__main__":
    unittest.main()
