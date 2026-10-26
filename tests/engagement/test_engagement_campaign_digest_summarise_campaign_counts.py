import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/engagement-campaign-digest/scripts/summarise_campaign_counts.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


class SummariseCampaignCountsTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_unsubscribed_and_string_counts(self):
        r = run(FX / "campaign_counts.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("| Weekly newsletter | 10,000 | 9,800 |", r.stdout)
        self.assertIn("| 0.82% |", r.stdout)  # 80 "unsubscribed" / 9,800 delivered
        self.assertIn("High unsubscribe: Weekly newsletter", r.stdout)
        self.assertIn("Missing value: Flash sale SMS: clicked", r.stdout)

    def test_error_response(self):
        r = run(FX / "denied.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", r.stderr)


if __name__ == "__main__":
    unittest.main()
