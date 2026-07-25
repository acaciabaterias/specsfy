from __future__ import annotations

import json
import os
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
    "load_research": ROOT / ".agents/skills/specsfy-specify/scripts/load_research.py",
    "analyze_change": ROOT / ".agents/skills/specsfy-specify/scripts/analyze_change.py",
    "review_findings": ROOT / ".agents/skills/specsfy-validate/scripts/review_findings.py",
    "verify_acceptance": ROOT / ".agents/skills/specsfy-tdd-bdd/scripts/verify_acceptance.py",
    "analyze_context": ROOT / ".agents/skills/specsfy-progress/scripts/analyze_context.py",
    "render_delivery": ROOT / ".agents/skills/specsfy-implement/scripts/render_delivery.py",
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


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    return path


class ExtensionAdaptationTests(unittest.TestCase):
    """SPECSFY: US-001 US-002 US-003 US-004 US-005 US-006 US-007 US-008 FR-001 FR-002 FR-003 FR-004 FR-005 FR-006 FR-007 FR-008 FR-009 FR-010 FR-011 FR-012 FR-013 FR-014 FR-015 FR-016 FR-017 NFR-001 NFR-002 NFR-003 NFR-004 NFR-005 NFR-006 AC-001 AC-002 AC-003 AC-004 AC-005 AC-006 AC-007 AC-008"""

    def test_gate_parity_attestation_and_canaries(self) -> None:
        payloads: list[dict[str, object]] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for boundary in ("local", "git", "ci"):
                result = run_script(
                    "verify_repo",
                    str(ROOT),
                    "--boundary",
                    boundary,
                    "--self-test",
                    "--json",
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual("passed", payload["result"])
                self.assertTrue(payload["canaries"])
                payloads.append(payload)
            normalized = [
                (item["result"], item["checks"], item["canaries"])
                for item in payloads
            ]
            self.assertEqual(normalized[0], normalized[1])
            self.assertEqual(normalized[1], normalized[2])

            attestation = root / "attestation.json"
            result = run_script(
                "verify_repo",
                str(ROOT),
                "--boundary",
                "ci",
                "--self-test",
                "--json",
                "--attestation",
                str(attestation),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue(attestation.is_file())
            saved = json.loads(attestation.read_text(encoding="utf-8"))
            self.assertEqual("ci", saved["boundary"])

    def test_evidence_and_full_trace_chain(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = write(
                root / "specs/demo/spec.md",
                """
                # Demo
                **Evidence Contract**: 1
                #### US-001 — Demo
                #### AC-001 — Demo
                - **FR-001**: Demo.
                - [x] T001 [TEST] Criar teste em tests/demo.feature — Refs: US-001, FR-001, AC-001 — Depends: none
                - [x] T002 [CODE] Criar código em src/demo.py — Refs: US-001, FR-001, AC-001 — Depends: T001
                  <!-- specsfy:evidence {"task":"T002","refs":["FR-001","AC-001"],"files":["src/demo.py"],"commands":[{"run":"python3 -B -m unittest","exit":0}]} -->
                """,
            )
            write(root / "src/demo.py", "VALUE = 1\n")
            write(
                root / "tests/demo.feature",
                "@US-001 @FR-001 @AC-001\nFeature: demo\nScenario: demo\n Given demo\n When demo\n Then demo\n",
            )
            evidence = run_script(
                "verify_evidence", str(spec), str(root), "--json", cwd=root
            )
            self.assertEqual(0, evidence.returncode, evidence.stdout + evidence.stderr)
            data = json.loads(evidence.stdout)
            self.assertEqual("passed", data["result"])

            chain = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / ".agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py"),
                    str(spec),
                    str(root),
                    "--kinds",
                    "FR,AC",
                    "--full-chain",
                    "--json",
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, chain.returncode, chain.stdout + chain.stderr)
            self.assertEqual([], json.loads(chain.stdout)["broken_chains"])

            (root / "src/demo.py").unlink()
            missing = run_script(
                "verify_evidence", str(spec), str(root), "--json", cwd=root
            )
            self.assertEqual(1, missing.returncode)
            self.assertIn("src/demo.py", missing.stdout)

    def test_research_loader_and_claim_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = write(
                root / "specs/demo/spec.md",
                """
                # Demo
                #### Artefatos de pesquisa armazenados
                - `specs/demo/research/api.md`: snapshot permitido.
                #### Researchs executados
                - **R-001** [critical] API suporta retry — Verdict: verified — Confidence: high — Evidence: research/api.md#retry — Budget: 2/10.
                """,
            )
            write(root / "specs/demo/research/api.md", "# API\n## retry\nconfirmado\n")
            result = run_script(
                "load_research", str(spec), "--emit-content", "--json", cwd=root
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("passed", payload["result"])
            self.assertEqual(1, len(payload["artifacts"]))
            self.assertIn("confirmado", payload["artifacts"][0]["content"])

            unverified = spec.read_text(encoding="utf-8").replace(
                "Verdict: verified", "Verdict: unverifiable"
            )
            spec.write_text(unverified, encoding="utf-8")
            blocked = run_script("load_research", str(spec), "--json", cwd=root)
            self.assertEqual(1, blocked.returncode)
            self.assertIn("critical", blocked.stdout)

            outside = write(root / "outside.md", "fora\n")
            artifact = root / "specs/demo/research/api.md"
            artifact.unlink()
            artifact.symlink_to(outside)
            unsafe = run_script("load_research", str(spec), "--json", cwd=root)
            self.assertEqual(1, unsafe.returncode)

    def test_change_impact_and_changelog(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            spec = write(
                root / "specs/demo/spec.md",
                """
                # Demo
                ### 7. Requisitos
                - **FR-001**: Primeiro comportamento.
                ### 8. Plano técnico
                Plano inicial.
                ### 13. Validações
                Evidência inicial.
                """,
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=root, check=True)
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "Primeiro comportamento", "Comportamento alterado"
                )
                + "\n- **FR-002**: Segundo comportamento.\n",
                encoding="utf-8",
            )
            impact = run_script(
                "analyze_change", str(spec), "--base", "HEAD", "--mode", "impact", "--json", cwd=root
            )
            self.assertEqual(0, impact.returncode, impact.stdout + impact.stderr)
            impact_data = json.loads(impact.stdout)
            self.assertEqual("Ato I", impact_data["reopen_from"])
            changelog = run_script(
                "analyze_change", str(spec), "--base", "HEAD", "--mode", "changelog", "--json", cwd=root
            )
            self.assertEqual(0, changelog.returncode, changelog.stdout + changelog.stderr)
            changes = json.loads(changelog.stdout)
            self.assertIn("FR-002", changes["added"])
            self.assertIn("FR-001", changes["changed"])

    def test_review_findings_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            write(Path(directory) / "src/a.py", "VALUE = 1\n")
            write(Path(directory) / "src/log.py", "VALUE = 1\n")
            spec = write(
                Path(directory) / "spec.md",
                """
                # Demo
                - **FR-001**: Regra funcional.
                - **NFR-001**: Regra não funcional. **Verificação**: inspeção.
                - **FIND-PROD-001** [P2] [Resolved] valor conflitante — Refs: FR-001 — Evidence: spec.md:1 — Effect: retrabalho — Suggestion: confirmar métrica
                - **FIND-ARCH-001** [P1] [Open] fronteira violada — Refs: FR-001 — Evidence: src/a.py:1 — Effect: acoplamento — Suggestion: decidir adaptador
                - **FIND-SEC-001** [P3] [Accepted] log excessivo — Refs: NFR-001 — Evidence: src/log.py:2 — Effect: exposição — Suggestion: mascarar
                """,
            )
            result = run_script("review_findings", str(spec), "--json")
            self.assertEqual(1, result.returncode)
            payload = json.loads(result.stdout)
            self.assertEqual(3, len(payload["findings"]))
            self.assertEqual(["FIND-ARCH-001"], payload["blocking"])

            spec.write_text(
                spec.read_text(encoding="utf-8").replace("[P1] [Open]", "[P1] [Resolved]"),
                encoding="utf-8",
            )
            resolved = run_script("review_findings", str(spec), "--json")
            self.assertEqual(0, resolved.returncode, resolved.stdout + resolved.stderr)

            spec.write_text(
                "# Demo\n"
                "Use `- **FIND-ARCH-001** [P1] [Open] descrição — Refs: FR-001` "
                "como exemplo de sintaxe.\n",
                encoding="utf-8",
            )
            example = run_script("review_findings", str(spec), "--json")
            self.assertEqual(0, example.returncode, example.stdout + example.stderr)
            self.assertEqual([], json.loads(example.stdout)["findings"])

    def test_acceptance_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = write(
                Path(directory) / "spec.md",
                """
                #### AC-001 — Um
                #### AC-002 — Dois
                ### 12. Plano de testes e rastreabilidade
                | Requisito | Cenário BDD | Nível | Arquivo/comando esperado | Evidência |
                | --- | --- | --- | --- | --- |
                | FR-001 | AC-001 | BDD | tests/one.feature | Passed: 1 cenário |
                | FR-002 | AC-002 | Manual | inspeção | Passed: aprovado por Ana |
                """,
            )
            result = run_script("verify_acceptance", str(spec), str(Path(directory)), "--json")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual([], json.loads(result.stdout)["missing"])

            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "| FR-002 | AC-002 | Manual | inspeção | Passed: aprovado por Ana |\n",
                    "",
                ),
                encoding="utf-8",
            )
            missing = run_script("verify_acceptance", str(spec), str(Path(directory)), "--json")
            self.assertEqual(1, missing.returncode)
            self.assertIn("AC-002", missing.stdout)

    def test_context_analysis_labels_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = write(
                root / "spec.md",
                """
                # Demo
                ## Primeira
                abcd abcd abcd abcd
                ## Segunda
                efgh efgh
                """,
            )
            estimated = run_script("analyze_context", str(spec), "--json")
            self.assertEqual(0, estimated.returncode, estimated.stdout + estimated.stderr)
            first = json.loads(estimated.stdout)
            self.assertEqual("estimated", first["source"])
            self.assertTrue(all(item["source"] == "estimated" for item in first["sections"]))

            usage = write(
                root / "usage.json",
                json.dumps({"input_tokens": 100, "output_tokens": 20}),
            )
            measured = run_script(
                "analyze_context", str(spec), "--usage-json", str(usage), "--json"
            )
            self.assertEqual(0, measured.returncode, measured.stdout + measured.stderr)
            self.assertEqual("measured", json.loads(measured.stdout)["source"])
            baseline = write(root / "baseline.md", "# Menor\nabcd\n")
            compared = run_script(
                "analyze_context", str(spec), "--compare", str(baseline), "--json"
            )
            self.assertEqual(0, compared.returncode, compared.stdout + compared.stderr)
            comparison = json.loads(compared.stdout)["comparison"]
            self.assertEqual("estimated", comparison["source"])
            self.assertGreater(comparison["current"], comparison["baseline"])

    def test_delivery_renderer_requires_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = write(
                Path(directory) / "spec.md",
                """
                # Demo
                **Status**: Implementing
                **Definition Gate**: Passed
                **Plan Gate**: Passed
                **Delivery Gate**: In Progress
                #### FR-001 — requisito
                - [x] T001 [CODE] Entregar src/demo.py — Refs: FR-001 — Depends: none
                  <!-- specsfy:evidence {"task":"T001","refs":["FR-001"],"files":["src/demo.py"],"commands":[{"run":"python3 -B -m unittest","exit":0}]} -->
                #### Riscos
                - risco → rollback.
                """,
            )
            blocked = run_script("render_delivery", str(spec), "--format", "json")
            self.assertEqual(1, blocked.returncode)
            preview = run_script(
                "render_delivery", str(spec), "--format", "json", "--preview"
            )
            self.assertEqual(0, preview.returncode, preview.stdout + preview.stderr)
            self.assertTrue(json.loads(preview.stdout)["preview"])

            spec.write_text(
                spec.read_text(encoding="utf-8")
                .replace("**Status**: Implementing", "**Status**: Complete")
                .replace("**Delivery Gate**: In Progress", "**Delivery Gate**: Passed"),
                encoding="utf-8",
            )
            final = run_script("render_delivery", str(spec), "--format", "markdown")
            self.assertEqual(0, final.returncode, final.stdout + final.stderr)
            self.assertIn("Delivery Gate", final.stdout)
            self.assertIn("FR-001", final.stdout)
            self.assertIn("python3 -B -m unittest", final.stdout)

    def test_read_only_tools_are_deterministic(self) -> None:
        spec = ROOT / "specs/extensoes-speckit/spec.md"
        before = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        calls = [
            ("verify_repo", (str(ROOT), "--boundary", "local", "--self-test", "--json")),
            ("load_research", (str(spec), "--json")),
            ("review_findings", (str(spec), "--json")),
            ("analyze_context", (str(spec), "--json")),
            ("render_delivery", (str(spec), "--preview", "--format", "json")),
            ("verify_evidence", (str(spec), str(ROOT), "--json")),
        ]
        for name, arguments in calls:
            first = run_script(name, *arguments)
            second = run_script(name, *arguments)
            self.assertEqual(first.returncode, second.returncode, name)
            self.assertEqual(first.stdout, second.stdout, name)
            self.assertEqual(first.stderr, second.stderr, name)
        after = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(before, after)

    def test_scripts_do_not_install_network_or_shell_markdown(self) -> None:
        for path in SCRIPTS.values():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("shell=True", text, path)
            self.assertNotRegex(text, r"\b(?:requests|urllib|httpx)\b")
            self.assertNotRegex(text, r"\b(?:pip install|uv add|uv pip)\b")

    def test_all_fourteen_suggestions_are_published_in_existing_skills(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in (
            "Quality Gates",
            "CI Guard",
            "Verify Tasks",
            "Spec Trace",
            "Spec Reference Loader",
            "Research Harness",
            "What-if",
            "Spec Changelog",
            "Spec Critique",
            "Architecture Guard",
            "Security Review",
            "QA Testing",
            "Token Consumption Analyzer",
            "PR Bridge",
        ):
            self.assertIn(name, readme)
        skill_dirs = [
            path
            for path in (ROOT / ".agents/skills").glob("specsfy-*")
            if path.is_dir()
        ]
        self.assertEqual(7, len(skill_dirs))


if __name__ == "__main__":
    unittest.main()
