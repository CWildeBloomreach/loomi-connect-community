import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "product-opportunity-finder" / "scripts" / "product_opportunities.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args, files=None):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in (files or {}).items():
            Path(tmp, name).write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class ProductOpportunitiesTest(unittest.TestCase):
    def test_help(self):
        p = run("--help")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("declining_winner", p.stdout)

    def test_former_best_seller_at_zero_visits_is_declining_winner_not_dead_weight(self):
        p = run(FIX / "po_products_former_winner.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        winners = [c["pid"] for c in out["groups"]["declining_winner"]["products"]]
        self.assertIn("P900", winners)
        dead = [r["pid"] for r in out["groups"]["dead_weight"]["zero_visit_rows"]]
        self.assertNotIn("P900", dead)
        self.assertIn("P901", dead)  # a small product with 0 visits is still dead weight
        c = next(c for c in out["groups"]["declining_winner"]["products"] if c["pid"] == "P900")
        self.assertEqual(c["visits"], 0)
        self.assertGreater(c["revenue_at_stake"], 0)

    def test_no_add_to_carts_does_not_crash(self):
        p = run(FIX / "po_products_no_atc.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["baselines"]["median_orders_per_atc"], 0)

    def test_missing_and_odd_numbers(self):
        rows = [{"prod_id": "X1", "product_title": "a", "brand": "B", "visits": "1,200", "prev_visits": "N/A",
                 "atc": "", "conversions": None, "revenue": "£1,000.50", "prev_revenue": "—", "aov": "-"}]
        p = run("p.json", files={"p.json": {"result": {"success": True, "data": {"rows": rows}}}})
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["baselines"]["total_revenue"], 1000.5)
        self.assertEqual(out["rows_with_missing_figures"], 1)
        self.assertIn("counted as 0", out["missing_figures_note"])

    def test_error_returned_as_data_stops(self):
        p = run(FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("ACCESS_DENIED", out["error"])
        self.assertIn("don't treat it as 'nothing found'", out["error"])


if __name__ == "__main__":
    unittest.main()
