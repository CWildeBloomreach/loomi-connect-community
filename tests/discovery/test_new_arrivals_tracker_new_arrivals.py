import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "loomi-discovery" / "skills" / "new-arrivals-tracker" / "scripts"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(script, *args, files=None):
    """Run a script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in (files or {}).items():
            Path(tmp, name).write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class NewArrivalsTest(unittest.TestCase):
    def test_help(self):
        for script in ("new_arrivals.py", "new_by_category.py", "new_in_grid.py", "grid_positions.py"):
            p = run(script, "--help")
            self.assertEqual(p.returncode, 0, f"{script}: {p.stderr}")

    def test_widened_release_window_is_not_unreliable(self):
        # Products released 40-55 days ago had previous-period views, as expected; only products
        # released at most --days minus --lag days ago are checked.
        p = run("new_arrivals.py", FIX / "na_products.json", "--new", FIX / "na_new_widened.txt", "--days", "30")
        self.assertEqual(p.returncode, 0, p.stderr)
        chk = json.loads(p.stdout)["release_data_check"]
        self.assertEqual(chk["new_with_release_age"], 4)
        self.assertEqual(chk["with_previous_period_views"], 0)
        self.assertEqual(chk["checked_release_age_up_to_days"], 28)
        self.assertTrue(chk["verdict"].startswith("OK"), chk["verdict"])
        self.assertTrue(chk["age_adjusted"])

    def test_old_products_only_is_not_checked(self):
        p = run("new_arrivals.py", FIX / "na_products.json", "--new", "old.txt", "--days", "30",
                files={"old.txt": "W0,40\nW1,45\n"})
        self.assertEqual(p.returncode, 0, p.stderr)
        chk = json.loads(p.stdout)["release_data_check"]
        self.assertTrue(chk["verdict"].startswith("Not checked"), chk["verdict"])
        self.assertEqual(chk["new_with_release_age"], 0)

    def test_fallback_reports_fallback_not_a_check(self):
        p = run("new_arrivals.py", FIX / "na_products.json", "--fallback-no-prev")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        chk = out["release_data_check"]
        self.assertTrue(chk["verdict"].startswith("Fallback used"), chk["verdict"])
        self.assertEqual(chk["new_with_release_age"], 0)
        self.assertIsNone(chk["share"])
        self.assertEqual(out["new_products"], 4)

    def test_fallback_markdown(self):
        p = run("new_arrivals.py", FIX / "na_products.json", "--fallback-no-prev", "--markdown")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Fallback used", p.stdout)
        self.assertNotIn("OK: new products had no earlier views", p.stdout)

    def test_error_returned_as_data_stops(self):
        p = run("new_arrivals.py", FIX / "denied.json", "--fallback-no-prev")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("ACCESS_DENIED", out["error"])
        p = run("new_arrivals.py", FIX / "denied.json", "--fallback-no-prev", "--markdown")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error", p.stderr)

    def test_other_scripts_stop_on_error(self):
        for args in (("new_by_category.py", "--all", FIX / "denied.json", "--new", FIX / "denied.json"),
                     ("new_in_grid.py", FIX / "denied.json", "--new", "n.txt"),
                     ("grid_positions.py", FIX / "denied.json")):
            p = run(*args, files={"n.txt": "N1\n"})
            self.assertEqual(p.returncode, 1, args[0])
            self.assertFalse(json.loads(p.stdout)["ok"], args[0])


if __name__ == "__main__":
    unittest.main()
