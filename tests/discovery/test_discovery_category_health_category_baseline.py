import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-category-health" / "scripts" / "category_baseline.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args, files=None):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in (files or {}).items():
            Path(tmp, name).write_text(json.dumps(content), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class CategoryBaselineTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_odd_numbers_parse(self):
        rows = [{"cat_id": "c1", "category": "Tops", "browse_sessions": "1,200", "visits": "1,300",
                 "conversion_rate": "2.5%", "bounce_rate": "N/A", "rpv": "£1.10", "prev_browse_sessions": "—"}]
        p = run("t.json", files={"t.json": {"result": {"success": True, "data": {"rows": rows}}}})
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["peer_medians"]["static"]["conversion_rate"], 2.5)
        self.assertEqual(out["peer_medians"]["static"]["rpv"], 1.1)
        self.assertIsNone(out["peer_medians"]["static"]["bounce_rate"])

    def test_error_returned_as_data_stops(self):
        for args in ((FIX / "denied.json",), ("t.json", "--categories", FIX / "denied.json")):
            p = run(*args, files={"t.json": {"data": {"rows": []}}})
            self.assertEqual(p.returncode, 1, args)
            out = json.loads(p.stdout)
            self.assertFalse(out["ok"])
            self.assertIn("ACCESS_DENIED", out["error"])


if __name__ == "__main__":
    unittest.main()
