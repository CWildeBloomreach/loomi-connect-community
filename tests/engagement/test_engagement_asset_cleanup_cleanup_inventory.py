import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/engagement-asset-cleanup/scripts/cleanup_inventory.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


class CleanupInventoryTest(unittest.TestCase):
    def test_help(self):
        r = run("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Usage", r.stdout)

    def test_works(self):
        r = run("--now", "1790000000", f"scenario:{FX / 'scenarios_list.json'}")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Scenarios", r.stdout)

    def test_error_response(self):
        r = run(f"scenario:{FX / 'scenarios_list.json'}", f"segmentation:{FX / 'denied.json'}")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", r.stderr)
        self.assertIn("don't treat it as 'nothing found'", r.stderr)


if __name__ == "__main__":
    unittest.main()
