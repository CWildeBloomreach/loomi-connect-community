import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/peak-readiness-check/scripts/render_checklist.py"
FIX = ROOT / "tests/fixtures/platform/peak_readiness"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True)


def verdict(items):
    p = run(FIX / items, "--event", "Big Sale", "--window", "2026-11-27 to 2026-12-01", "--today", "2026-10-26")
    assert p.returncode == 0, p.stderr
    line = next(x for x in p.stdout.splitlines() if x.startswith("**Verdict:**"))
    return line.split("**Verdict:** ", 1)[1].split(":", 1)[0], p.stdout


class RenderChecklistTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_nothing_checked_is_never_go(self):
        self.assertEqual(verdict("items_unchecked.json")[0], "INCOMPLETE")

    def test_green_with_unchecked_is_not_go(self):
        self.assertEqual(verdict("items_green_and_unchecked.json")[0], "INCOMPLETE")

    def test_all_green_is_go(self):
        self.assertEqual(verdict("items_green.json")[0], "GO")

    def test_lowercase_area_and_status_still_block(self):
        v, out = verdict("items_lowercase.json")
        self.assertEqual(v, "NO-GO")
        self.assertIn("| 1 | Search |", out)


if __name__ == "__main__":
    unittest.main()
