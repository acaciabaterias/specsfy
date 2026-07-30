from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/install-cli.sh"


class InstallCliScriptTests(unittest.TestCase):
    def test_installs_local_checkout_from_any_working_directory(self) -> None:
        codex_skill = ROOT / ".agents" / "skills" / "specsfy-monorepo-documentator"
        claude_skill = ROOT / ".claude" / "skills" / "specsfy-monorepo-documentator"
        skill_before = (codex_skill / "SKILL.md").read_text(encoding="utf-8")
        claude_target_before = claude_skill.readlink()
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            fake_path, log = self._fake_npm(temporary)

            result = subprocess.run(
                [str(SCRIPT)],
                cwd=temporary,
                text=True,
                capture_output=True,
                check=False,
                env={
                    **os.environ,
                    "PATH": f"{fake_path}:{os.environ['PATH']}",
                    "SPECSFY_TEST_LOG": str(log),
                    "SPECSFY_TEST_BIN": str(temporary / "bin"),
                },
            )

            self.assertEqual(0, result.returncode, result.stderr)
            invocation = log.read_text(encoding="utf-8")
            self.assertIn("install --global --force", invocation)
            self.assertIn(str((ROOT / "cli").resolve()), invocation)
            self.assertIn("specsfy 0.4.0", result.stdout)
            self.assertFalse((ROOT / "specs").exists())
            self.assertEqual(
                skill_before,
                (codex_skill / "SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertEqual(claude_target_before, claude_skill.readlink())

    def test_can_install_published_cli_from_npm(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            fake_path, log = self._fake_npm(temporary)

            result = subprocess.run(
                [str(SCRIPT), "--npm"],
                text=True,
                capture_output=True,
                check=False,
                env={
                    **os.environ,
                    "PATH": f"{fake_path}:{os.environ['PATH']}",
                    "SPECSFY_TEST_LOG": str(log),
                    "SPECSFY_TEST_BIN": str(temporary / "bin"),
                },
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn(
                "@promovaweb/specsfy@latest",
                log.read_text(encoding="utf-8"),
            )

    def _fake_npm(self, temporary: Path) -> tuple[Path, Path]:
        fake_path = temporary / "fake-path"
        fake_path.mkdir()
        log = temporary / "npm.log"
        npm = fake_path / "npm"
        npm.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "if [[ \"$1 $2\" == \"prefix --global\" ]]; then\n"
            "  dirname \"$SPECSFY_TEST_BIN\"\n"
            "  exit 0\n"
            "fi\n"
            "printf '%s\\n' \"$*\" >> \"$SPECSFY_TEST_LOG\"\n"
            "mkdir -p \"$SPECSFY_TEST_BIN\"\n"
            "printf '#!/usr/bin/env bash\\nprintf \"specsfy 0.4.0\\\\n\"\\n' "
            "> \"$SPECSFY_TEST_BIN/specsfy\"\n"
            "chmod +x \"$SPECSFY_TEST_BIN/specsfy\"\n",
            encoding="utf-8",
        )
        npm.chmod(0o755)
        return fake_path, log


if __name__ == "__main__":
    unittest.main()
