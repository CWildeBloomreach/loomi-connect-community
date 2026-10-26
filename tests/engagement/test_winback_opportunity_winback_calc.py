import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/winback-opportunity/scripts/winback_calc.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


def money(x):
    sys.dont_write_bytecode = True  # never write into the skill's folder
    spec = importlib.util.spec_from_file_location("winback_calc", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.money(x, "$")


class WinbackCalcTest(unittest.TestCase):
    def test_help(self):
        r = run("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("--example", r.stdout)

    def test_example_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            ex = subprocess.run([sys.executable, str(SCRIPT), "--example"], cwd=tmp,
                                capture_output=True, text=True, check=True).stdout
            json.loads(ex)

    def test_money_rounding_carries_to_next_unit(self):
        self.assertEqual(money(999600), "$1.0M")
        self.assertEqual(money(950000), "$950k")
        self.assertEqual(money(9999.6), "$10k")
        self.assertEqual(money(1_250_000), "$1.2M")
        self.assertEqual(money(420), "$420")

    def test_en_dash_bands_match_default_rates(self):
        r = run(FX / "winback_grid.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("no win-back rate given", r.stdout)
        self.assertIn("| 31–90 | ~18,000 |", r.stdout)
        self.assertIn("| 12.0% |", r.stdout)
        self.assertIn("| 7.0% |", r.stdout)


if __name__ == "__main__":
    unittest.main()
