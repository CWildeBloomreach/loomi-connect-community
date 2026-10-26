import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-redirect-audit" / "scripts" / "redirect_checks.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


def navigational(stdout):
    section = stdout.split("## Navigational queries without a redirect", 1)[1]
    return {line.split("|")[1].strip() for line in section.splitlines()
            if line.startswith("| ") and not line.startswith("| Query")}


class RedirectChecksTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_navigational_candidates(self):
        p = run("--redirects", FIX / "rc_redirect_detail.json", "--queries", FIX / "rc_queries.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        found = navigational(p.stdout)
        # Real navigational searches (session counts arrive as strings).
        for q in ("track order", "size guide", "returns", "klarna", "contact us"):
            self.assertIn(q, found)
        # Product searches that merely contain a navigational word.
        for q in ("plus size dress", "track pants", "mobile phone case", "free people", "size 10 shoes"):
            self.assertNotIn(q, found)

    def test_error_returned_as_data_stops(self):
        p = run("--redirects", FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", p.stderr)
        p = run("--redirects", FIX / "rc_redirect_detail.json", "--queries", FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("don't treat it as 'nothing found'", p.stderr)


if __name__ == "__main__":
    unittest.main()
