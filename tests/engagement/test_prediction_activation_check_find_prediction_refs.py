import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/prediction-activation-check/scripts/find_prediction_refs.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args, cwd=None):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=cwd or tmp, capture_output=True, text=True)


class FindPredictionRefsTest(unittest.TestCase):
    def test_help(self):
        r = run("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Usage", r.stdout)

    def test_works(self):
        r = run(FX / "predictions.json", FX / "prediction_defs")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("segmentation: High churn risk [active]", r.stdout)

    def test_error_in_definitions(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(FX / "prediction_defs", Path(tmp) / "defs")
            shutil.copy(FX / "denied.json", Path(tmp) / "defs" / "scenario_x1.json")
            r = run(FX / "predictions.json", "defs", cwd=tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", r.stderr)
        self.assertNotIn("no references found", r.stdout)

    def test_error_in_predictions(self):
        r = run(FX / "denied.json", FX / "prediction_defs")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error", r.stderr)


if __name__ == "__main__":
    unittest.main()
