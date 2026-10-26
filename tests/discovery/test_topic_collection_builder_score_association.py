import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "topic-collection-builder" / "scripts" / "score_association.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


WORDINGS = (FIX / "sa_grid_pickleball.json", FIX / "sa_grid_pickleball_std.json")


class ScoreAssociationTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_options_after_a_family_group(self):
        p = run("--terms", "pickleball", "--exclude", "tennis", *WORDINGS,
                "--family", "Court shoes", FIX / "sa_family_shoes.json", "--top", "5", "--markdown")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("## Family: Court shoes", p.stdout)
        self.assertIn("Indoor court shoe", p.stdout)

    def test_options_after_a_rule_group(self):
        p = run("--terms", "pickleball", *WORDINGS, "--rule", "sport=pickleball", FIX / "sa_grid_pickleball.json",
                "--top", "5")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual([r["rule"] for r in out["rules"]], ["sport=pickleball"])
        self.assertEqual(out["rules"][0]["returned"], 2)

    def test_documented_command_still_works(self):
        p = run("--terms", "pickleball,pickle ball", "--exclude", "tennis,padel,badminton", *WORDINGS,
                "--family", "Court shoes", FIX / "sa_family_shoes.json", "--markdown")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("core: 1", p.stdout)

    def test_error_returned_as_data_stops(self):
        p = run("--terms", "pickleball", FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("ACCESS_DENIED", out["error"])


if __name__ == "__main__":
    unittest.main()
