import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/collection-suggester/scripts/preview_summary.py"
FIX = ROOT / "tests/fixtures/platform/collection"


def run(tmp, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp, capture_output=True, text=True)


class PreviewSummaryTest(unittest.TestCase):
    def test_help(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(tmp, "--help").returncode, 0)

    def test_out_writes_json_lines_and_still_prints(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = run(tmp, FIX / "grid_cargo.json", "--out", "profiles.jsonl")
            self.assertEqual(p.returncode, 0, p.stderr)
            saved = (Path(tmp) / "profiles.jsonl").read_text().splitlines()
            self.assertEqual(saved, p.stdout.splitlines())
            prof = json.loads(saved[0])
            self.assertEqual(prof["source"]["query"], "cargo pants")
            self.assertEqual(prof["numFound"], 200)
            self.assertIn({"value": "category=/men/pants", "share": 0.9}, prof["dominant"])

    def test_error_response_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = run(tmp, FIX / "grid_denied.json", "--out", "profiles.jsonl")
            self.assertEqual(p.returncode, 1)
            self.assertIn("Loomi Connect returned an error", json.loads(p.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
