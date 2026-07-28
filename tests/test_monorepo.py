from __future__ import annotations

import subprocess
import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".bash",
    ".feature",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".yaml",
    ".yml",
}
LEGACY_PATTERNS = (
    re.compile(r"github\.com/specsfy/"),
    re.compile(r"raw\.githubusercontent\.com/specsfy/"),
    re.compile(r"api\.github\.com/repos/specsfy/"),
    re.compile(
        r"(?<!\.)\bspecsfy/"
        r"(?:dev|brand|skills|docs|example|specsfy|specialists|cli)\b"
    ),
    re.compile(r"oito repositórios|oito raízes Git|repositórios independentes"),
    re.compile(
        r"specsfy-hub-documentator|hub-documentation\.md|"
        r"collect_hub_evidence\.py"
    ),
    re.compile(r"raiz proprietária|raízes proprietárias"),
)
GENERATED_DIRECTORIES = {".venv", "node_modules", "vendor", "__pycache__"}


class MonorepoContractTest(unittest.TestCase):
    def test_public_origin_is_the_promovaweb_monorepo(self) -> None:
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

        self.assertIn("github.com/promovaweb/specsfy", remote)

    def test_product_modules_share_one_git_root(self) -> None:
        for module in (
            "brand",
            "cli",
            "docs",
            "example",
            "skills",
            "specialists",
            "specsfy",
        ):
            with self.subTest(module=module):
                root = subprocess.run(
                    ["git", "-C", module, "rev-parse", "--show-toplevel"],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                self.assertEqual(str(ROOT), root)

    def test_text_sources_do_not_reference_the_legacy_multi_repo(self) -> None:
        violations: list[str] = []
        for path in ROOT.rglob("*"):
            if (
                not path.is_file()
                or ".git" in path.parts
                or GENERATED_DIRECTORIES.intersection(path.parts)
                or path.suffix not in TEXT_SUFFIXES
                or path.name == "test_monorepo.py"
            ):
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in LEGACY_PATTERNS:
                if pattern.search(content):
                    violations.append(
                        f"{path.relative_to(ROOT)}: {pattern.pattern}"
                    )

        self.assertEqual([], violations)

    def test_cli_uses_monorepo_distribution_endpoints(self) -> None:
        installer = (
            ROOT / "cli/src/specsfy_cli/installer.py"
        ).read_text(encoding="utf-8")
        catalog = (
            ROOT / "cli/src/specsfy_cli/catalog.py"
        ).read_text(encoding="utf-8")
        updater = (
            ROOT / "cli/src/specsfy_cli/updater.py"
        ).read_text(encoding="utf-8")
        package = (ROOT / "cli/pyproject.toml").read_text(encoding="utf-8")

        self.assertIn("https://github.com/promovaweb/specsfy.git", installer)
        self.assertIn('BASE_DIRECTORY = "skills"', installer)
        self.assertIn('SPECIALISTS_DIRECTORY = "specialists"', installer)
        self.assertIn(
            "raw.githubusercontent.com/promovaweb/specsfy/main/specialists/catalog.json",
            catalog,
        )
        self.assertIn(
            "api.github.com/repos/promovaweb/specsfy/tags",
            updater,
        )
        for endpoint in (
            'Homepage = "https://github.com/promovaweb/specsfy"',
            'Repository = "https://github.com/promovaweb/specsfy.git"',
            'Documentation = "https://github.com/promovaweb/specsfy/tree/main/docs"',
            'Issues = "https://github.com/promovaweb/specsfy/issues"',
        ):
            self.assertIn(endpoint, package)


if __name__ == "__main__":
    unittest.main()
