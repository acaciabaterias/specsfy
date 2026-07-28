from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from specsfy_cli import __version__


ROOT = Path(__file__).resolve().parents[1]
BINARY = ROOT / "bin/specsfy"
MANIFEST = ROOT / "bin/specsfy.build.json"
FINGERPRINT_SCRIPT = ROOT / "scripts/source_fingerprint.py"


class BinaryArtifactTests(unittest.TestCase):
    def test_source_fingerprint_ignores_permissions_not_tracked_by_git(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.py"
            source.write_text("value = 1\n", encoding="utf-8")
            source.chmod(0o644)
            regular = subprocess.run(
                [sys.executable, "-B", str(FINGERPRINT_SCRIPT), str(root)],
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()

            source.chmod(0o664)
            group_writable = subprocess.run(
                [sys.executable, "-B", str(FINGERPRINT_SCRIPT), str(root)],
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            source.chmod(0o755)
            executable = subprocess.run(
                [sys.executable, "-B", str(FINGERPRINT_SCRIPT), str(root)],
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()

        self.assertEqual(regular, group_writable)
        self.assertNotEqual(regular, executable)

    def test_binary_matches_the_current_cli_source(self) -> None:
        self.assertTrue(BINARY.is_file(), f"execute scripts/build-executable.sh")
        self.assertTrue(BINARY.stat().st_mode & 0o111)
        self.assertTrue(MANIFEST.is_file())
        expected = subprocess.run(
            [sys.executable, "-B", str(FINGERPRINT_SCRIPT), str(ROOT)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(2, manifest["schema_version"])
        self.assertEqual(__version__, manifest["version"])
        self.assertEqual(expected, manifest["source_sha256"])
        self.assertEqual(
            hashlib.sha256(BINARY.read_bytes()).hexdigest(),
            manifest["binary_sha256"],
        )

        result = subprocess.run(
            [str(BINARY), "--version"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(__version__, result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
