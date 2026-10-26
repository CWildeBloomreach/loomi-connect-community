import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-experiment-readout" / "scripts"
          / "summarise_report.py")
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class SummariseReportTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_metric_wordings(self):
        cases = {"cr": "Conversion rate", "CR - Conversion Rate": "Conversion rate",
                 "Conversion Rate": "Conversion rate", "conversion": "Conversion rate",
                 "RPV - Revenue Per Visit": "Revenue per visit", "Revenue per visit": "Revenue per visit",
                 "Average Order Value": "Average order value", "add-to-cart rate": "Add-to-cart rate",
                 "Add to Cart Rate": "Add-to-cart rate"}
        for wording, label in cases.items():
            p = run(FIX / "sr_report.json", "--control", "Bucket A", "--metric", wording)
            self.assertEqual(p.returncode, 0, f"{wording}: {p.stderr}")
            self.assertIn(f"success metric: {label}", p.stdout, wording)

    def test_unknown_metric_still_fails(self):
        p = run(FIX / "sr_report.json", "--control", "Bucket A", "--metric", "bounce")
        self.assertEqual(p.returncode, 1)
        self.assertIn("Unknown metric", p.stderr)

    def test_error_returned_as_data_stops(self):
        p = run(FIX / "denied.json", "--control", "Bucket A", "--metric", "cr")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", p.stderr)
        self.assertIn("don't treat it as 'nothing found'", p.stderr)


if __name__ == "__main__":
    unittest.main()
