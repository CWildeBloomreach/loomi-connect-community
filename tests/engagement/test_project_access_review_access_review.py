import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/project-access-review/scripts/access_review.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


def flags_by_email(out):
    rows = {}
    for line in out.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 5 and "@" in cells[0]:
            rows[cells[0]] = cells[-1]
    return rows


class AccessReviewTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_generic_and_test_accounts(self):
        r = run("--company-domain", "acme.example", f"Prod={FX / 'users_prod.json'}")
        self.assertEqual(r.returncode, 0, r.stderr)
        f = flags_by_email(r.stdout)
        self.assertNotIn("generic", f["dev.patel@acme.example"])
        self.assertNotIn("test", f["dev.patel@acme.example"])
        self.assertNotIn("generic", f["tech.nguyen@acme.example"])
        self.assertIn("generic", f["marketing@acme.example"])
        self.assertIn("generic", f["test1@acme.example"])
        self.assertIn("generic", f["api+sync@acme.example"])
        self.assertIn("test/alias", f["jane.test@acme.example"])

    def test_many_projects_with_two_projects(self):
        r = run("--company-domain", "acme.example", f"Prod={FX / 'users_prod.json'}",
                f"Sandbox={FX / 'users_sandbox.json'}")
        self.assertEqual(r.returncode, 0, r.stderr)
        f = flags_by_email(r.stdout)
        self.assertIn("2 projects", f["dev.patel@acme.example"])
        self.assertNotIn("projects", f["marketing@acme.example"])
        self.assertIn("In 2+ projects: 2", r.stdout)

    def test_error_response(self):
        r = run("--company-domain", "acme.example", f"Prod={FX / 'denied.json'}")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", r.stderr)


if __name__ == "__main__":
    unittest.main()
