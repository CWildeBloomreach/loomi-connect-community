import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "autosuggest-audit" / "scripts" / "autosuggest_check.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args, files=None):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in (files or {}).items():
            Path(tmp, name).write_text(json.dumps(content), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class AutosuggestCheckTest(unittest.TestCase):
    def test_help(self):
        for flag in ("--help", "-h"):
            p = run(flag)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("missing_top_queries", p.stdout)

    def test_string_session_counts(self):
        rows = [{"query": "jeans", "browse_sessions": "1,200", "conversion_rate": "3%", "rpv": "$2.00"},
                {"query": "jersey top", "browse_sessions": "300", "conversion_rate": "N/A", "rpv": ""}]
        p = run(FIX / "as_suggestions.json", "q.json", files={"q.json": {"data": {"rows": rows}}})
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual([m["query"] for m in out["missing_top_queries"]], ["jersey top"])
        self.assertEqual(out["missing_top_queries"][0]["sessions"], 300)

    def test_error_returned_as_data_stops(self):
        p = run(FIX / "as_suggestions.json", FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("ACCESS_DENIED", out["error"])


if __name__ == "__main__":
    unittest.main()
