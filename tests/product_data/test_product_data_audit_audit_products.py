import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-product-data/skills/product-data-audit/scripts/audit_products.py"
FIX = ROOT / "tests/fixtures/product_data"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True)


class AuditProductsTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_bool_and_missing_numbers(self):
        p = run(FIX / "products_grid.json", "--performance", FIX / "performance.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        s2 = {x["pid"]: [g["detail"] for g in x["gaps"] if g["code"] == "S2"] for x in out["products"]}
        self.assertEqual(s2["EX-1"], ["price is not a number (True)"])
        self.assertEqual(s2["EX-2"], ["no price"])
        self.assertEqual(s2["EX-3"], [])  # sale_price "NA" is missing, not a sale price of 0
        self.assertEqual(out["summary"]["performance_rows_missing_values"]["rows"], 1)
        rev = {x["pid"]: x["revenue"] for x in out["products"]}
        self.assertEqual(rev["EX-1"], 1000.0)
        self.assertEqual(rev["EX-2"], 0.0)

    def test_error_response_stops_json(self):
        p = run(FIX / "products_grid.json", "--performance", FIX / "performance_denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", out["error"])

    def test_error_response_stops_markdown(self):
        p = run(FIX / "products_grid.json", "--performance", FIX / "performance_denied.json", "--markdown")
        self.assertEqual(p.returncode, 1)
        self.assertIn("Loomi Connect returned an error", p.stderr)


if __name__ == "__main__":
    unittest.main()
