import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/engagement-send-collision-check/scripts/find_collisions.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


class FindCollisionsTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_merges_files_unwraps_result_and_prints_reach(self):
        r = run(FX / "calendar_week1.json", FX / "calendar_week2.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("**Sends in window:** 4 across 2 days", r.stdout)
        lines = [l for l in r.stdout.splitlines() if l.startswith("- ") and " -> " in l]
        self.assertEqual(len(lines), 3)
        # largest combined reach first; "50,000" string parsed; potential_reach used when reach is null
        self.assertIn("reach 50,000 / 200", lines[0])
        self.assertIn("reach 200 / 45,000", lines[1])
        self.assertIn("reach 200 / 30,000", lines[2])

    def test_error_response(self):
        r = run(FX / "calendar_week2.json", FX / "denied.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("denied.json: Loomi Connect returned an error", r.stderr)


if __name__ == "__main__":
    unittest.main()
