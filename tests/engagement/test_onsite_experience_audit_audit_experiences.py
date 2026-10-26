import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/onsite-experience-audit/scripts/audit_experiences.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


class AuditExperiencesTest(unittest.TestCase):
    def test_help(self):
        r = run("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Usage", r.stdout)

    def test_works(self):
        r = run("--now", "1790000000", FX / "onsite_banners.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("## Inventory", r.stdout)

    def test_error_response(self):
        r = run(FX / "onsite_banners.json", f"survey:{FX / 'denied.json'}")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", r.stderr)


if __name__ == "__main__":
    unittest.main()
