import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-rule-audit" / "scripts" / "audit_rules.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class AuditRulesTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def audit(self):
        p = run("--rules", FIX / "ar_ranking_rules.json", "--rules", FIX / "ar_media_rules.json",
                "--queries", FIX / "ar_queries.json", "--today", "2026-10-01")
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def test_media_rule_sharing_an_id_with_a_ranking_rule_is_kept(self):
        out = self.audit()
        self.assertIn("Rules checked: 4 (4 enabled)", out)
        self.assertIn("search media: 1", out)

    def test_rule_expired_by_end_date_is_not_a_duplicate(self):
        out = self.audit()
        self.assertIn("Expired but still switched on", out)
        self.assertNotIn("enabled ranking rules for \"jeans\"", out)

    def test_string_zero_visits_flag_no_searches(self):
        out = self.audit()
        self.assertIn("No searches for \"wellies\"", out)
        self.assertNotIn("No searches for \"jeans\"", out)

    def test_error_returned_as_data_stops(self):
        for args in (("--rules", FIX / "denied.json"),
                     ("--rules", FIX / "ar_ranking_rules.json", "--queries", FIX / "denied.json")):
            p = run(*args)
            self.assertEqual(p.returncode, 1, args)
            self.assertEqual(p.stdout, "")
            self.assertNotIn("Rules checked: 0", p.stdout)
            self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", p.stderr)


if __name__ == "__main__":
    unittest.main()
