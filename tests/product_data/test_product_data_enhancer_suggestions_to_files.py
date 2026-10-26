import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-product-data/skills/product-data-enhancer/scripts/suggestions_to_files.py"
FIX = ROOT / "tests/fixtures/product_data"


class SuggestionsToFilesTest(unittest.TestCase):
    def test_help(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)

    def test_csv_cells_cannot_run_as_formulas_and_paths_stay_inside(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, str(SCRIPT), str(FIX / "suggestions.jsonl"), "--out-dir", "out"],
                               cwd=tmp, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            out = Path(tmp) / "out"
            with open(out / "suggestions.csv", newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            for r in rows:
                for v in r.values():
                    self.assertFalse(v[:1] in ("=", "+", "-", "@", "\t", "\r"), repr(v))
            first = rows[0]
            self.assertEqual(first["current"], "'=HYPERLINK(\"https://example.invalid\",\"x\")")
            self.assertEqual(first["suggested"], "'+cmd|' /C calc'!A0")
            self.assertTrue(first["evidence"].startswith("'@SUM"))
            self.assertEqual(rows[1]["current"], "'-2+3")
            self.assertEqual(rows[1]["suggested"], "Plain text stays as it is")
            self.assertTrue(rows[1]["evidence"].startswith("'\t"))
            # The JSON Lines review file keeps the raw text.
            self.assertIn('"current": "=HYPERLINK', (out / "suggestions.jsonl").read_text())
            # A product ID with path parts can't write outside jsonld/.
            written = sorted(p.name for p in (out / "jsonld").iterdir())
            self.assertEqual(written, [".._.._escape.json", "EX-1001.json"])
            self.assertEqual(sorted(x.name for x in Path(tmp).iterdir()), ["out"])
            self.assertEqual(sorted(x.name for x in out.iterdir()),
                             ["jsonld", "review.md", "suggestions.csv", "suggestions.jsonl"])


if __name__ == "__main__":
    unittest.main()
