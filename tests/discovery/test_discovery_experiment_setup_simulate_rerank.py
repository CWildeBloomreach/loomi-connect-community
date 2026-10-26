import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-experiment-setup" / "scripts"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(script, *args):
    """Run a script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class SimulateRerankTest(unittest.TestCase):
    def test_help(self):
        for script in ("simulate_rerank.py", "estimate_duration.py"):
            self.assertEqual(run(script, "--help").returncode, 0, script)

    def test_error_returned_as_data_stops(self):
        p = run("simulate_rerank.py", FIX / "denied.json", "--boost-brand", "Contoso")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", p.stderr)


if __name__ == "__main__":
    unittest.main()
