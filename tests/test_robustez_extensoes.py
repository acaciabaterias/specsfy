from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = {
    "verify_repo": ROOT / ".agents/skills/specsfy-validate/scripts/verify_repo.py",
    "verify_evidence": ROOT / ".agents/skills/specsfy-implement/scripts/verify_evidence.py",
    "verify_acceptance": ROOT / ".agents/skills/specsfy-tdd-bdd/scripts/verify_acceptance.py",
    "review_findings": ROOT / ".agents/skills/specsfy-validate/scripts/review_findings.py",
    "load_research": ROOT / ".agents/skills/specsfy-specify/scripts/load_research.py",
    "analyze_change": ROOT / ".agents/skills/specsfy-specify/scripts/analyze_change.py",
}


def run_script(name: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPTS[name]), *args],
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS[name])
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    return path


class RobustnessImprovementTests(unittest.TestCase):
    """SPECSFY: US-001 US-002 US-003 US-004 US-005 US-006 US-007 US-008 FR-001 FR-002 FR-003 FR-004 FR-005 FR-006 FR-007 FR-008 FR-009 FR-010 NFR-001 NFR-002 NFR-003 NFR-004 NFR-005 NFR-006 AC-001 AC-002 AC-003 AC-004 AC-005 AC-006 AC-007 AC-008"""

    def test_attestation_binds_commit_task_and_file_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            delivered = write(root / "src/demo.py", "VALUE = 1\n")
            operated = write(root / ".github/workflows/demo.yml", "name: demo\n")
            spec = write(
                root / "specs/demo/spec.md",
                """
                # Demo
                **Evidence Contract**: 1
                - **FR-001**: Entrega.
                - [x] T001 [CODE] Criar src/demo.py — Refs: FR-001 — Depends: none
                  <!-- specsfy:evidence {"task":"T001","refs":["FR-001"],"files":["src/demo.py"],"commands":[{"run":"python3 -B -m unittest","exit":0}]} -->
                - [x] T002 [OPS] Criar .github/workflows/demo.yml — Refs: FR-001 — Depends: T001
                  <!-- specsfy:evidence {"task":"T002","refs":["FR-001"],"files":[".github/workflows/demo.yml"],"commands":[{"run":"python3 -B -m unittest","exit":0}]} -->
                """,
            )
            digest = hashlib.sha256(delivered.read_bytes()).hexdigest()
            ops_digest = hashlib.sha256(operated.read_bytes()).hexdigest()
            attestation = root / "attestation.json"
            attestation.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "result": "passed",
                        "boundary": "local",
                        "commit_sha": None,
                        "policy_digest": "a" * 64,
                        "checks": [
                            {
                                "name": "unittest",
                                "status": "passed",
                                "code": 0,
                                "detail": "OK",
                            }
                        ],
                        "evidence_bindings": [
                            {
                                "spec": "specs/demo/spec.md",
                                "task": "T001",
                                "refs": ["FR-001"],
                                "commands": [
                                    {"run": "python3 -B -m unittest", "exit": 0}
                                ],
                                "files": {"src/demo.py": digest},
                                "observed_checks": ["unittest"],
                            },
                            {
                                "spec": "specs/demo/spec.md",
                                "task": "T002",
                                "refs": ["FR-001"],
                                "commands": [
                                    {"run": "python3 -B -m unittest", "exit": 0}
                                ],
                                "files": {".github/workflows/demo.yml": ops_digest},
                                "observed_checks": ["unittest"],
                            }
                        ],
                    },
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            valid = run_script(
                "verify_evidence",
                str(spec),
                str(root),
                "--attestation",
                str(attestation),
                "--json",
                cwd=root,
            )
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
            valid_payload = json.loads(valid.stdout)
            self.assertEqual("attested", valid_payload["mode"])
            self.assertEqual(["T001", "T002"], [item["task"] for item in valid_payload["tasks"]])

            delivered.write_text("VALUE = 2\n", encoding="utf-8")
            changed = run_script(
                "verify_evidence",
                str(spec),
                str(root),
                "--attestation",
                str(attestation),
                "--json",
                cwd=root,
            )
            self.assertEqual(1, changed.returncode)
            self.assertIn("hash divergente", changed.stdout)

        self_test = run_script(
            "verify_repo",
            str(ROOT),
            "--self-test",
            "--json",
        )
        self.assertEqual(0, self_test.returncode, self_test.stdout + self_test.stderr)
        self.assertEqual([], json.loads(self_test.stdout)["evidence_bindings"])

    def test_policy_digest_covers_commands_limits_and_sources(self) -> None:
        module = load_module("verify_repo")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy = write(root / "policy.py", "VALUE = 1\n")
            checks = [{"name": "same", "command": ["python", "policy.py"]}]
            first = module.policy_digest(root, checks, 300.0, 65536, [policy])
            repeat = module.policy_digest(root, checks, 300.0, 65536, [policy])
            command_changed = module.policy_digest(
                root,
                [{"name": "same", "command": ["python", "-B", "policy.py"]}],
                300.0,
                65536,
                [policy],
            )
            limit_changed = module.policy_digest(root, checks, 301.0, 65536, [policy])
            policy.write_text("VALUE = 2\n", encoding="utf-8")
            source_changed = module.policy_digest(root, checks, 300.0, 65536, [policy])
            self.assertEqual(first, repeat)
            self.assertEqual(64, len(first))
            self.assertEqual(4, len({first, command_changed, limit_changed, source_changed}))
            python_link = root / "python-link"
            python_link.symlink_to(Path(sys.executable).resolve())
            runtime_a = module.policy_digest(
                root,
                [{"name": "same", "command": [sys.executable, "-B"]}],
                300.0,
                65536,
                [policy],
            )
            runtime_b = module.policy_digest(
                root,
                [{"name": "same", "command": [str(python_link), "-B"]}],
                300.0,
                65536,
                [policy],
            )
            self.assertEqual(runtime_a, runtime_b)

    def test_acceptance_audits_runner_attestation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = write(
                root / "specs/demo/spec.md",
                """
                # Demo
                **Slug**: demo
                #### AC-001 — Jornada
                ### 12. Plano de testes e rastreabilidade
                | Requisito | Cenário BDD | Nível | Arquivo/comando esperado | Evidência |
                | --- | --- | --- | --- | --- |
                | FR-001 | AC-001 | integração | runner | Passed: execução |
                ### 13. Validações
                """,
            )
            missing = write(
                root / "missing.json",
                json.dumps(
                    {
                        "schema_version": 2,
                        "result": "passed",
                        "checks": [],
                    }
                ),
            )
            rejected = run_script(
                "verify_acceptance",
                str(spec),
                str(root),
                "--attestation",
                str(missing),
                "--json",
            )
            self.assertEqual(1, rejected.returncode)
            self.assertIn("acceptance:demo", rejected.stdout)

            accepted = write(
                root / "accepted.json",
                json.dumps(
                    {
                        "schema_version": 2,
                        "result": "passed",
                        "checks": [
                            {
                                "name": "acceptance:demo",
                                "status": "passed",
                                "code": 0,
                                "detail": json.dumps(
                                    {
                                        "result": "passed",
                                        "criteria": ["AC-001"],
                                        "missing": [],
                                    },
                                    sort_keys=True,
                                ),
                            }
                        ],
                    }
                ),
            )
            valid = run_script(
                "verify_acceptance",
                str(spec),
                str(root),
                "--attestation",
                str(accepted),
                "--json",
            )
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
            self.assertTrue(json.loads(valid.stdout)["attested"])

    def test_ci_dependencies_are_immutably_pinned(self) -> None:
        workflow = (ROOT / ".github/workflows/specsfy.yml").read_text(encoding="utf-8")
        action_lines = re.findall(
            r"^\s*(?:-\s+)?uses:\s+([^\s]+)(?:\s+#\s*(.+))?$",
            workflow,
            re.MULTILINE,
        )
        self.assertGreaterEqual(len(action_lines), 4)
        for reference, comment in action_lines:
            self.assertRegex(reference, r"@[0-9a-f]{40}$")
            self.assertRegex(comment or "", r"^v?\d")
        self.assertRegex(workflow, r"python-version:\s*['\"]3\.12\.\d+['\"]")
        self.assertRegex(workflow, r"behave==\d+\.\d+\.\d+")
        self.assertRegex(workflow, r"PyYAML==\d+\.\d+\.\d+")

    def test_runner_times_out_and_truncates_output(self) -> None:
        module = load_module("verify_repo")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            slow = module.run(
                [sys.executable, "-c", "import time; time.sleep(1)"],
                root,
                name="slow",
                timeout_seconds=0.05,
                max_output_bytes=64,
            )
            self.assertEqual("timed_out", slow["status"])
            self.assertEqual(124, slow["code"])
            self.assertTrue(slow["timed_out"])

            verbose = module.run(
                [sys.executable, "-c", "print('X' * 100 + 'SECRET_AFTER_LIMIT')"],
                root,
                name="verbose",
                timeout_seconds=1,
                max_output_bytes=32,
            )
            self.assertEqual("passed", verbose["status"])
            self.assertTrue(verbose["truncated"])
            self.assertNotIn("SECRET_AFTER_LIMIT", verbose["detail"])
            self.assertLessEqual(len(verbose["detail"].encode("utf-8")), 96)

    def test_findings_validate_identity_refs_and_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / "evidence.txt", "proof\n")
            (root / "linked-evidence.txt").symlink_to(root / "evidence.txt")
            spec = write(
                root / "spec.md",
                """
                # Demo
                - **FR-001**: Regra.
                - **FIND-PROD-001** [P2] [Resolved] primeiro — Refs: FR-001 — Evidence: evidence.txt:1 — Effect: efeito — Suggestion: corrigir
                - **FIND-PROD-001** [P2] [Resolved] duplicado — Refs: FR-001 — Evidence: evidence.txt:1 — Effect: efeito — Suggestion: corrigir
                - **FIND-ARCH-002** [P2] [Resolved] ref ruim — Refs: FR-999 — Evidence: evidence.txt:1 — Effect: efeito — Suggestion: corrigir
                - **FIND-SEC-003** [P2] [Resolved] prova ruim — Refs: FR-001 — Evidence: missing.txt:1 — Effect: efeito — Suggestion: corrigir
                - **FIND-SEC-004** [P2] [Resolved] link ruim — Refs: FR-001 — Evidence: linked-evidence.txt:1 — Effect: efeito — Suggestion: corrigir
                """,
            )
            result = run_script(
                "review_findings", str(spec), "--root", str(root), "--json"
            )
            self.assertEqual(1, result.returncode)
            payload = json.loads(result.stdout)
            joined = "\n".join(payload["errors"])
            self.assertIn("duplicado", joined)
            self.assertIn("FR-999", joined)
            self.assertIn("missing.txt", joined)
            self.assertIn("linked-evidence.txt", joined)

    def test_research_validates_ids_budgets_and_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = write(
                root / "specs/demo/research/source.md",
                "# Visão Única\n\nconteúdo\n",
            )
            spec = write(
                root / "specs/demo/spec.md",
                f"""
                # Demo
                #### Researchs executados
                - **R-001** [high] primeira — Verdict: verified — Confidence: high — Evidence: research/{evidence.name}#visão-única — Budget: 1/2.
                - **R-001** [high] duplicada — Verdict: verified — Confidence: high — Evidence: research/{evidence.name}#ausente — Budget: 3/2.
                #### Artefatos de pesquisa armazenados
                - `specs/demo/research/{evidence.name}`: fonte.
                """,
            )
            result = run_script("load_research", str(spec), "--json")
            self.assertEqual(1, result.returncode)
            joined = "\n".join(json.loads(result.stdout)["errors"])
            self.assertIn("R-001: ID duplicado", joined)
            self.assertIn("orçamento excedido", joined)
            self.assertIn("âncora inexistente", joined)

            spec = write(
                root / "specs/demo/spec.md",
                f"""
                # Demo
                #### Researchs executados
                - **R-001** [high] primeira — Verdict: verified — Confidence: high — Evidence: research/{evidence.name}#visão-única — Budget: 2/3.
                - **R-002** [high] segunda — Verdict: verified — Confidence: high — Evidence: research/{evidence.name}#visão-única — Budget: 2/3.
                #### Artefatos de pesquisa armazenados
                - `specs/demo/research/{evidence.name}`: fonte.
                """,
            )
            aggregate = run_script("load_research", str(spec), "--json")
            self.assertEqual(1, aggregate.returncode)
            self.assertIn("orçamento total excedido", aggregate.stdout)

    def test_change_impact_uses_semantic_section_titles(self) -> None:
        module = load_module("analyze_change")
        old = "### 8. Plano técnico\nalpha\n"
        new = "### 1. Plano técnico\nbeta\n"
        payload = module.analyze(old, new, "impact", "HEAD")
        self.assertEqual(["plan"], payload["changed_areas"])
        self.assertEqual("Ato II", payload["reopen_from"])
        self.assertEqual(["Plan Gate", "Delivery Gate"], payload["invalidated_gates"])
        unknown = module.analyze(
            "### 99. Área futura\nalpha\n",
            "### 100. Área futura\nbeta\n",
            "impact",
            "HEAD",
        )
        self.assertEqual(["unknown"], unknown["changed_areas"])
        self.assertEqual("Ato I", unknown["reopen_from"])


if __name__ == "__main__":
    unittest.main()
