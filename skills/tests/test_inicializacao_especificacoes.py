from __future__ import annotations

import ast
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "specsfy-03-specify/scripts/iniciar_spec.py"
MODEL = ROOT / "templates/Spec.md"


def run_initializer(
    cwd: Path,
    title: str,
    *,
    root: Path | None = None,
    slug: str | None = None,
) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, "-B", str(SCRIPT), "--title", title]
    if root is not None:
        args.extend(["--root", str(root)])
    if slug is not None:
        args.extend(["--slug", slug])
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class InitializationTests(unittest.TestCase):
    """SPECSFY: US-001 US-002 FR-001 FR-002 FR-003 FR-004 FR-005 FR-006 FR-007 NFR-001 NFR-002 NFR-003 AC-001 AC-002 AC-003 AC-004 AC-005"""

    def test_uses_cwd_and_explicit_root(self) -> None:
        """SPECSFY: FR-001 FR-002 AC-001 AC-002"""
        with tempfile.TemporaryDirectory() as current_directory:
            current = Path(current_directory)
            created = run_initializer(current, "Current Project")
            self.assertEqual(0, created.returncode, created.stderr)
            expected = (
                current / "specs" / "specs" / "0001-current-project" / "spec.md"
            )
            self.assertEqual(str(expected.resolve()), created.stdout.strip())
            self.assertTrue(expected.is_file())
            self.assertFalse((expected.parent / "0001-spec.md").exists())

        with tempfile.TemporaryDirectory() as git_directory:
            git_root = Path(git_directory)
            subprocess.run(
                ["git", "init", "-q"],
                cwd=git_root,
                check=True,
                capture_output=True,
            )
            nested = git_root / "nested" / "agent-workdir"
            nested.mkdir(parents=True)
            created = run_initializer(nested, "Nested Project")
            self.assertEqual(0, created.returncode, created.stderr)
            self.assertTrue(
                (
                    nested
                    / "specs"
                    / "specs"
                    / "0001-nested-project"
                    / "spec.md"
                ).is_file()
            )
            self.assertFalse((git_root / "specs").exists())

        with (
            tempfile.TemporaryDirectory() as outside_directory,
            tempfile.TemporaryDirectory() as target_directory,
        ):
            outside = Path(outside_directory)
            target = Path(target_directory)
            created = run_initializer(outside, "Explicit Root", root=target)
            self.assertEqual(0, created.returncode, created.stderr)
            self.assertTrue(
                (
                    target
                    / "specs"
                    / "specs"
                    / "0001-explicit-root"
                    / "spec.md"
                ).is_file()
            )
            self.assertFalse((outside / "specs").exists())

    def test_fills_model_and_rejects_invalid_input(self) -> None:
        """SPECSFY: FR-003 FR-004 AC-001 AC-005"""
        self.assertTrue(MODEL.is_file(), f"modelo ausente: {MODEL}")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            created = run_initializer(
                root,
                "Título com Acento",
                slug="slug-explicito",
            )
            self.assertEqual(0, created.returncode, created.stderr)
            spec = (
                root / "specs" / "specs" / "0001-slug-explicito" / "spec.md"
            )
            content = spec.read_text(encoding="utf-8")
            self.assertIn("# Especificação integrada: Título com Acento", content)
            self.assertIn("| Campo | Valor |", content)
            self.assertIn("| --- | --- |", content)
            self.assertIn("| ID | SPEC-0001 |", content)
            self.assertIn("| Slug | 0001-slug-explicito |", content)
            self.assertIn("| Atualizada em |", content)
            self.assertNotIn("**ID**:", content)
            self.assertEqual(3, content.count("## Ato "))
            self.assertEqual(
                18,
                sum(
                    line.startswith("### ")
                    and line[4:6].rstrip(".").isdigit()
                    for line in content.splitlines()
                ),
            )
            self.assertNotIn("{{", content)

            invalid = run_initializer(root, "!!!")
            self.assertNotEqual(0, invalid.returncode)
            self.assertIn("erro:", invalid.stderr.lower())
            self.assertEqual([spec], list(root.rglob("spec.md")))

            invalid_slug = run_initializer(root, "Another", slug="Not Valid")
            self.assertNotEqual(0, invalid_slug.returncode)
            self.assertIn("kebab-case", invalid_slug.stderr)

    def test_allocates_next_incremental_id(self) -> None:
        """SPECSFY: FR-005 FR-006 AC-003"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            specs = root / "specs" / "specs"
            for name in ("0001-first", "0003-third", "legacy"):
                (specs / name).mkdir(parents=True)
            created = run_initializer(root, "Fourth")
            self.assertEqual(0, created.returncode, created.stderr)
            spec = specs / "0004-fourth" / "spec.md"
            self.assertTrue(spec.is_file())
            self.assertIn("| ID | SPEC-0004 |", spec.read_text(encoding="utf-8"))
            self.assertTrue((specs / "legacy").is_dir())

    def test_concurrent_initializations_are_unique(self) -> None:
        """SPECSFY: FR-007 AC-004"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            processes = [
                subprocess.Popen(
                    [sys.executable, "-B", str(SCRIPT), "--title", title],
                    cwd=root,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                for title in ("Alpha", "Beta")
            ]
            results = [
                process.communicate() + (process.returncode,) for process in processes
            ]
            self.assertTrue(
                all(code == 0 for _, _, code in results),
                results,
            )
            directories = sorted(
                path.name
                for path in (root / "specs" / "specs").iterdir()
                if path.is_dir()
            )
            self.assertEqual(["0001", "0002"], [name[:4] for name in directories])

    def test_ids_sort_lexicographically(self) -> None:
        """SPECSFY: NFR-003 AC-003 AC-004"""
        names = [f"{number:04d}-spec" for number in (1, 2, 10, 999, 9999)]
        self.assertEqual(names, sorted(reversed(names)))

    def test_standard_library_and_actionable_errors(self) -> None:
        """SPECSFY: NFR-001 NFR-002 AC-005"""
        self.assertTrue(SCRIPT.is_file(), f"script ausente: {SCRIPT}")
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        imported = {
            alias.name.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported.update(
            node.module.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.assertLessEqual(imported, sys.stdlib_module_names)

        with tempfile.NamedTemporaryFile() as file_root:
            failed = run_initializer(Path.cwd(), "Invalid Root", root=Path(file_root.name))
        self.assertNotEqual(0, failed.returncode)
        self.assertIn("erro:", failed.stderr.lower())
        self.assertIn(file_root.name, failed.stderr)

    def test_prefers_template_installed_in_consumer_project(self) -> None:
        """SPECSFY: FR-003 AC-001"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed_template = root / ".specsfy" / "templates" / "Spec.md"
            installed_template.parent.mkdir(parents=True)
            installed_template.write_text(
                "# {{SPEC_NAME}}\n"
                "| Campo | Valor |\n"
                "| --- | --- |\n"
                "| ID | {{SPEC_ID}} |\n"
                "| Slug | {{SPEC_NUMBER}}-{{SPEC_SLUG}} |\n"
                "| Atualizada em | {{CURRENT_DATE}} |\n"
                "template instalado\n",
                encoding="utf-8",
            )

            created = run_initializer(root, "Template local")

            self.assertEqual(0, created.returncode, created.stderr)
            content = Path(created.stdout.strip()).read_text(encoding="utf-8")
            self.assertIn("template instalado", content)
            self.assertIn("| ID | SPEC-0001 |", content)

    def test_prefers_custom_template_over_installed_default(self) -> None:
        """SPECSFY: FR-003 AC-001"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            templates = root / ".specsfy" / "templates"
            custom = templates / "custom"
            custom.mkdir(parents=True)
            default_content = MODEL.read_text(encoding="utf-8").replace(
                "# Especificação integrada:",
                "# Template padrão:",
            )
            custom_content = MODEL.read_text(encoding="utf-8").replace(
                "# Especificação integrada:",
                "# Template customizado:",
            )
            (templates / "Spec.md").write_text(
                default_content,
                encoding="utf-8",
            )
            (custom / "Spec.md").write_text(
                custom_content,
                encoding="utf-8",
            )

            created = run_initializer(root, "Precedência customizada")

            self.assertEqual(0, created.returncode, created.stderr)
            content = Path(created.stdout.strip()).read_text(encoding="utf-8")
            self.assertIn("# Template customizado:", content)
            self.assertNotIn("# Template padrão:", content)


if __name__ == "__main__":
    unittest.main()
