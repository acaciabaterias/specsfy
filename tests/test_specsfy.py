from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
SPEC = ROOT / "specs" / "specsfy" / "spec.md"
MCR_REFERENCE = (
    SKILLS / "specsfy-specify" / "references" / "mcr-10.md"
)
AGENT_GUIDE = ROOT / "AGENTS.md"
README = ROOT / "README.md"
EXPECTED_SKILLS = {
    "specsfy-discuss",
    "specsfy-specify",
    "specsfy-validate",
    "specsfy-tdd-bdd",
    "specsfy-tasks",
    "specsfy-implement",
    "specsfy-progress",
}


def run_script(relative: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / relative), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def write_temp_spec(directory: str, text: str) -> Path:
    path = Path(directory) / "specs" / "specsfy" / "spec.md"
    path.parent.mkdir(parents=True)
    reference = path.parent / "research" / "spec-kit"
    reference.mkdir(parents=True)
    (reference / "LICENSE").write_text("fixture\n", encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    return path


def reset_task_progress(text: str, task_id: str) -> str:
    pattern = re.compile(
        rf"(?ms)^- \[[ xX]\] {re.escape(task_id)}\b.*?"
        r"(?=^- \[[ xX]\] T\d{3,}\b|^#### |^### 15\.)"
    )
    match = pattern.search(text)
    if not match:
        raise AssertionError(f"Bloco da tarefa {task_id} não encontrado")
    block = re.sub(r"^- \[[ xX]\]", "- [ ]", match.group(0), count=1)
    block = re.sub(
        r"^(\s+-\s+)\[[ xX]\](\s+\*\*(?:PREP|EXECUTE|VERIFY|EVIDENCE|IMPROVE)\*\*:)",
        r"\1[ ]\2",
        block,
        flags=re.MULTILINE,
    )
    return text[: match.start()] + block + text[match.end() :]


def set_workflow_state(
    text: str,
    *,
    status: str,
    definition: str,
    plan: str,
    delivery: str,
) -> str:
    values = {
        "Status": status,
        "Definition Gate": definition,
        "Plan Gate": plan,
        "Delivery Gate": delivery,
    }
    for key, value in values.items():
        text = re.sub(
            rf"^\*\*{re.escape(key)}\*\*: .+$",
            f"**{key}**: {value}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    headings = {
        "Gate do Ato I — Definição": definition,
        "Gate do Ato II — Plano": plan,
        "Gate do Ato III — Entrega": delivery,
    }
    for heading, value in headings.items():
        text = re.sub(
            rf"(#### {re.escape(heading)}.*?-\s+\*\*Resultado\*\*:)[^\n]*",
            rf"\1 {value}",
            text,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
    return text


def progress_spec_text(
    slug: str,
    *,
    status: str,
    delivery_gate: str,
    open_second_task: bool = False,
) -> str:
    second_parent = " " if open_second_task else "x"
    second_steps = (
        ("x", " ", " ", " ", " ")
        if open_second_task
        else ("x", "x", "x", "x", "x")
    )
    checklist = "\n".join(
        f"  - [{mark}] **{name}**: evidência {name.lower()}."
        for mark, name in zip(
            second_steps,
            ("PREP", "EXECUTE", "VERIFY", "EVIDENCE", "IMPROVE"),
            strict=True,
        )
    )
    return f"""# Especificação integrada: {slug}

**Formato**: Specsfy/2.0
**Slug**: {slug}
**Status**: {status}
**Definition Gate**: Passed
**Plan Gate**: Passed
**Delivery Gate**: {delivery_gate}
**Atualizada em**: 2026-07-24

## Ato II — Projetar e provar

### 14. Tarefas

- [x] T001 [TEST] Preparar {slug} — Refs: FR-001, AC-001 — Depends: none
  - [x] **PREP**: evidência prep.
  - [x] **EXECUTE**: evidência execute.
  - [x] **VERIFY**: evidência verify.
  - [x] **EVIDENCE**: evidência evidence.
  - [x] **IMPROVE**: evidência improve.

- [{second_parent}] T002 [CODE] Construir {slug} — Refs: FR-001, AC-001 — Depends: T001
{checklist}

### 15. Ordem de execução
"""


class SkillContractTests(unittest.TestCase):
    """SPECSFY: US-001 US-002 US-007 US-008 FR-001 FR-002 FR-003 FR-004 FR-005 FR-006 FR-007 FR-008 FR-009 FR-010 FR-011 FR-012 FR-013 FR-014 NFR-002 NFR-003 NFR-004 AC-001 AC-002 AC-007 AC-008"""

    def test_exactly_seven_skills_have_valid_core_files(self) -> None:
        skill_dirs = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(EXPECTED_SKILLS, skill_dirs)
        for name in sorted(EXPECTED_SKILLS):
            skill = SKILLS / name
            body = (skill / "SKILL.md").read_text(encoding="utf-8")
            metadata = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", body)
            self.assertIn("description:", body)
            self.assertNotIn("[TODO:", body)
            self.assertLess(len(body.splitlines()), 500)
            self.assertIn(f"${name}", metadata)

    def test_skills_contain_all_reusable_mechanisms_without_caches(self) -> None:
        self.assertTrue(
            (SKILLS / "specsfy-specify" / "assets" / "spec-template.md").is_file()
        )
        self.assertTrue(
            (SKILLS / "specsfy-validate" / "scripts" / "validate_spec.py").is_file()
        )
        self.assertTrue(
            (SKILLS / "specsfy-tasks" / "scripts" / "validate_tasks.py").is_file()
        )
        self.assertTrue(
            (SKILLS / "specsfy-progress" / "scripts" / "progress.py").is_file()
        )
        self.assertEqual([], list(SKILLS.rglob("__pycache__")))
        self.assertEqual([], list(SKILLS.rglob("*.pyc")))

    def test_only_generated_specs_live_under_specs(self) -> None:
        self.assertFalse((ROOT / "spec.md").exists())
        self.assertFalse((ROOT / "tasks.md").exists())
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertFalse((ROOT / "spec-kit").exists())
        self.assertTrue(SPEC.is_file())
        generated = sorted((ROOT / "specs").glob("*/spec.md"))
        self.assertIn(SPEC, generated)
        self.assertIn(ROOT / "specs" / "extensoes-speckit" / "spec.md", generated)
        self.assertTrue(all(path.parent.parent == ROOT / "specs" for path in generated))

    def test_research_is_colocated_and_indexed_without_competing_source(self) -> None:
        package = SPEC.parent
        research = package / "research"
        text = SPEC.read_text(encoding="utf-8")
        self.assertTrue(research.is_dir())
        self.assertTrue((research / "spec-kit" / "LICENSE").is_file())
        self.assertIn("#### Artefatos de pesquisa armazenados", text)
        self.assertIn("specs/specsfy/research/spec-kit/", text)
        self.assertFalse((package / "research.md").exists())

    def test_spec_uses_rigid_integrated_structure(self) -> None:
        text = SPEC.read_text(encoding="utf-8")
        self.assertIn("**Formato**: Specsfy/2.0", text)
        self.assertIn("**Slug**: specsfy", text)
        self.assertEqual(
            [
                "Ato I — Definir",
                "Ato II — Projetar e provar",
                "Ato III — Entregar e validar",
            ],
            re.findall(r"^## (Ato [IVX]+ — .+)$", text, re.MULTILINE),
        )
        for section in (
            "Research e esclarecimentos",
            "Artefatos de pesquisa armazenados",
            "Migrations",
            "Models",
            "Controllers e casos de uso",
            "Views e experiência",
            "Queries e repositórios",
            "Modelo de dados",
            "APIs expostas",
            "Documentação das APIs consultadas",
            "Estratégia TDD",
            "Cenários BDD de aceite",
            "Validações",
            "Tarefas",
        ):
            self.assertIn(section, text)

    def test_template_matches_the_rigid_validator_contract(self) -> None:
        template = (
            SKILLS / "specsfy-specify" / "assets" / "spec-template.md"
        ).read_text(encoding="utf-8")
        template = template.replace("[slug-kebab-case]", "template-feature")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "specs" / "template-feature" / "spec.md"
            path.parent.mkdir(parents=True)
            path.write_text(template, encoding="utf-8")
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py",
                str(path),
                "--allow-draft",
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_every_acceptance_criterion_contains_real_gherkin(self) -> None:
        text = SPEC.read_text(encoding="utf-8")
        ac_count = len(re.findall(r"^#### AC-\d{3,}\b", text, re.MULTILINE))
        blocks = re.findall(r"```gherkin\s*(.*?)```", text, re.DOTALL)
        self.assertGreater(ac_count, 0)
        self.assertEqual(ac_count, len(blocks))
        for block in blocks:
            for keyword in ("Feature:", "Scenario:", "Given ", "When ", "Then "):
                self.assertIn(keyword, block)
            self.assertRegex(block, r"@AC-\d{3,}")
            self.assertRegex(block, r"@FR-\d{3,}|@NFR-\d{3,}")


class ToolingTests(unittest.TestCase):
    """SPECSFY: US-003 US-004 US-005 US-006 US-007 US-008 FR-005 FR-006 FR-007 FR-008 FR-009 FR-010 FR-011 FR-012 FR-013 FR-014 AC-003 AC-004 AC-005 AC-006 AC-007 AC-008 NFR-001 NFR-003"""

    def test_valid_spec_passes(self) -> None:
        result = run_script(
            ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(SPEC)
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("RESULTADO: READY", result.stdout)

    def test_spec_without_gherkin_then_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "    Then o agente pergunta", "    Outcome o agente pergunta", 1
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("não possui `Then` em Gherkin", result.stdout)

    def test_draft_spec_is_not_ready_unless_explicitly_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = set_workflow_state(
                SPEC.read_text(encoding="utf-8"),
                status="Draft",
                definition="Pending",
                plan="Pending",
                delivery="Pending",
            )
            path = write_temp_spec(directory, text)
            strict = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
            intermediate = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py",
                str(path),
                "--allow-draft",
            )
        self.assertEqual(1, strict.returncode)
        self.assertIn("Status Draft", strict.stdout)
        self.assertEqual(0, intermediate.returncode, intermediate.stdout + intermediate.stderr)

    def test_draft_cannot_claim_passed_spec_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = set_workflow_state(
                SPEC.read_text(encoding="utf-8"),
                status="Draft",
                definition="Passed",
                plan="Pending",
                delivery="Pending",
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py",
                str(path),
                "--allow-draft",
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("Status Draft não pode", result.stdout)

    def test_heading_level_is_rigid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "### 9. Modelo de dados", "## 9. Modelo de dados", 1
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("deve usar nível H3", result.stdout)

    def test_unindexed_research_artifact_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_temp_spec(directory, SPEC.read_text(encoding="utf-8"))
            extra = path.parent / "research" / "unindexed-api"
            extra.mkdir()
            (extra / "openapi.json").write_text("{}\n", encoding="utf-8")
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("não está indexado", result.stdout)

    def test_declared_external_research_must_exist_locally(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_temp_spec(directory, SPEC.read_text(encoding="utf-8"))
            shutil.rmtree(path.parent / "research")
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("evidência em research", result.stdout)

    def test_research_root_cannot_be_a_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_temp_spec(directory, SPEC.read_text(encoding="utf-8"))
            research = path.parent / "research"
            shutil.rmtree(research)
            outside = Path(directory) / "outside-research" / "spec-kit"
            outside.mkdir(parents=True)
            (outside / "LICENSE").write_text("fixture\n", encoding="utf-8")
            research.symlink_to(outside.parent, target_is_directory=True)
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("research não pode ser symlink", result.stdout)

    def test_complete_spec_requires_closed_tasks_and_dod(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                SPEC.read_text(encoding="utf-8"),
                "T010",
            )
            text = re.sub(
                r"^\*\*Status\*\*: .+$",
                "**Status**: Complete",
                text,
                count=1,
                flags=re.MULTILINE,
            )
            text = text.replace(
                "- [x] `Delivery Gate` está `Passed`.",
                "- [ ] `Delivery Gate` está `Passed`.",
                1,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("tarefas abertas", result.stdout)
        self.assertIn("Definition of Done", result.stdout)

    def test_gate_metadata_must_match_validation_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = re.sub(
                r"(#### Gate do Ato III — Entrega\s*\n\s*-\s+\*\*Resultado\*\*:)\s*.+",
                r"\1 Failed",
                SPEC.read_text(encoding="utf-8"),
                count=1,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("diverge do metadata Delivery Gate", result.stdout)

    def test_valid_embedded_tasks_pass(self) -> None:
        result = run_script(
            ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(SPEC)
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_task_requires_canonical_progress_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                SPEC.read_text(encoding="utf-8"),
                "T009",
            ).replace(
                "  - [ ] **PREP**: RED BDD e TDD dos mesmos IDs confirmados.\n",
                "",
                1,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("checklist canônico", result.stdout)

    def test_completed_parent_rejects_open_checklist_item(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "  - [x] **PREP**: Escopo BDD e IDs confirmados.",
                "  - [ ] **PREP**: Escopo BDD e IDs confirmados.",
                1,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("concluída com itens de checklist abertos", result.stdout)

    def test_open_parent_rejects_fully_completed_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                SPEC.read_text(encoding="utf-8"),
                "T009",
            )
            start = text.index("- [ ] T009")
            end = text.index("#### Fase final — Regressão do checklist", start)
            block = text[start:end].replace("  - [ ]", "  - [x]")
            text = text[:start] + block + text[end:]
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("aberta, mas todos os itens", result.stdout)

    def test_progress_on_blocked_task_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                reset_task_progress(SPEC.read_text(encoding="utf-8"), "T009"),
                "T010",
            ).replace(
                "  - [ ] **PREP**: Behave, unittest, validadores, quick validation, rastreabilidade e auditorias identificados.",
                "  - [x] **PREP**: Behave, unittest, validadores, quick validation, rastreabilidade e auditorias identificados.",
                1,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("progresso em checklist enquanto dependências", result.stdout)

    def test_pending_tasks_require_explicit_draft_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "**Plan Gate**: Passed", "**Plan Gate**: Pending", 1
            )
            path = write_temp_spec(directory, text)
            strict = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
            intermediate = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py",
                str(path),
                "--allow-draft",
            )
        self.assertEqual(1, strict.returncode)
        self.assertIn("Plan Gate precisa estar Passed", strict.stdout)
        self.assertEqual(0, intermediate.returncode, intermediate.stdout + intermediate.stderr)

    def test_code_task_requires_bdd_and_tdd_predecessors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "Materializar aceite integrado em tests/features/specsfy.feature",
                "Materializar aceite integrado em tests/features/specsfy.txt",
                1,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("sem predecessor BDD", result.stdout)

    def test_plan_gate_requires_completed_bdd_and_tdd_predecessors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                SPEC.read_text(encoding="utf-8"),
                "T001",
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn(
            "Plan Gate exige predecessor BDD T001 concluído",
            result.stdout,
        )

    def test_task_cycle_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "— Depends: none", "— Depends: T002", 1
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py", str(path)
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("Ciclo de dependências", result.stdout)

    def test_next_task_reads_embedded_backlog(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                reset_task_progress(SPEC.read_text(encoding="utf-8"), "T009"),
                "T010",
            )
            text = re.sub(
                r"^\*\*Status\*\*: .+$",
                "**Status**: Implementing",
                text,
                count=1,
                flags=re.MULTILINE,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py",
                str(path),
                "--all",
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("T009", result.stdout)

    def test_next_task_surfaces_next_checklist_item(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                reset_task_progress(SPEC.read_text(encoding="utf-8"), "T009"),
                "T010",
            )
            text = re.sub(
                r"^\*\*Status\*\*: .+$",
                "**Status**: Implementing",
                text,
                count=1,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"^\*\*Delivery Gate\*\*: .+$",
                "**Delivery Gate**: In Progress",
                text,
                count=1,
                flags=re.MULTILINE,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py", str(path)
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PRÓXIMO ITEM: T009 PREP", result.stdout)
        self.assertIn("Progresso: 0/5", result.stdout)

    def test_next_task_rejects_completed_parent_with_open_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "  - [x] **PREP**: Escopo BDD e IDs confirmados.",
                "  - [ ] **PREP**: Escopo BDD e IDs confirmados.",
                1,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py", str(path)
            )
        self.assertEqual(2, result.returncode)
        self.assertIn("checklist", result.stderr)

    def test_next_task_rejects_pending_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = SPEC.read_text(encoding="utf-8").replace(
                "**Plan Gate**: Passed", "**Plan Gate**: Pending", 1
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py", str(path)
            )
        self.assertEqual(2, result.returncode)
        self.assertIn("Plan Gate", result.stderr)

    def test_next_task_rejects_false_completion_without_test_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = re.sub(
                r"^-\s+\[ \]\s+(T\d{3,})",
                r"- [x] \1",
                SPEC.read_text(encoding="utf-8"),
                flags=re.MULTILINE,
            )
            text = text.replace(
                "**Delivery Gate**: Passed", "**Delivery Gate**: In Progress", 1
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py", str(path)
            )
        self.assertEqual(2, result.returncode)
        self.assertIn("Delivery Gate", result.stderr)

    def test_next_task_rejects_complete_status_with_open_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = reset_task_progress(
                SPEC.read_text(encoding="utf-8"),
                "T010",
            )
            text = re.sub(
                r"^\*\*Status\*\*: .+$",
                "**Status**: Complete",
                text,
                count=1,
                flags=re.MULTILINE,
            )
            path = write_temp_spec(directory, text)
            result = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py", str(path)
            )
        self.assertEqual(2, result.returncode)
        self.assertIn("tarefas abertas", result.stderr)

    def test_traceability_passes_and_detects_gap(self) -> None:
        script = ".agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py"
        passing = run_script(script, str(SPEC), str(ROOT), "--kinds", "FR,AC,NFR")
        self.assertEqual(0, passing.returncode, passing.stdout + passing.stderr)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tests").mkdir()
            (root / "tests" / "test_empty.py").write_text(
                "def test_empty():\n    assert True\n", encoding="utf-8"
            )
            failing = run_script(script, str(SPEC), str(root), "--kinds", "FR,AC,NFR")
        self.assertEqual(1, failing.returncode)
        self.assertIn("SEM TESTE", failing.stdout)

    def test_traceability_ignores_fixture_markers(self) -> None:
        script = ".agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_tests = root / "tests" / "fixtures"
            fixture_tests.mkdir(parents=True)
            (fixture_tests / "false_evidence.feature").write_text(
                "@FR-001 @AC-001\nFeature: falsa\n", encoding="utf-8"
            )
            result = run_script(script, str(SPEC), str(root))
        self.assertEqual(1, result.returncode)
        self.assertIn("SEM TESTE", result.stdout)

    def test_traceability_ignores_research_markers(self) -> None:
        script = ".agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            researched_tests = root / "research" / "api-sdk" / "tests"
            researched_tests.mkdir(parents=True)
            (researched_tests / "false_evidence.feature").write_text(
                "@FR-001 @AC-001\nFeature: evidência externa\n",
                encoding="utf-8",
            )
            result = run_script(script, str(SPEC), str(root), "--json")
        self.assertEqual(1, result.returncode)
        self.assertNotIn("false_evidence.feature", result.stdout)


class ProgressTests(unittest.TestCase):
    """SPECSFY: US-008 FR-013 FR-014 AC-008 NFR-001 NFR-003"""

    SCRIPT = ".agents/skills/specsfy-progress/scripts/progress.py"

    def test_progress_reports_current_repository_in_human_and_json_formats(self) -> None:
        before = SPEC.read_text(encoding="utf-8")
        human = run_script(self.SCRIPT, ".")
        machine = run_script(self.SCRIPT, ".", "--json")
        after = SPEC.read_text(encoding="utf-8")

        self.assertEqual(0, human.returncode, human.stdout + human.stderr)
        self.assertIn("Progresso geral", human.stdout)
        self.assertIn("specsfy", human.stdout)
        self.assertEqual(0, machine.returncode, machine.stdout + machine.stderr)
        payload = json.loads(machine.stdout)
        top_level_specs = sorted((ROOT / "specs").glob("*/spec.md"))
        self.assertEqual(len(top_level_specs), payload["summary"]["total_specs"])
        self.assertEqual(
            sum(item["tasks"]["total"] for item in payload["specs"]),
            payload["summary"]["tasks"]["total"],
        )
        self.assertEqual(
            sum(item["checklists"]["total"] for item in payload["specs"]),
            payload["summary"]["checklists"]["total"],
        )
        self.assertIn("specsfy", [item["slug"] for item in payload["specs"]])
        self.assertEqual(before, after)

    def test_progress_aggregates_specs_and_ignores_nested_research(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha = root / "specs" / "alpha" / "spec.md"
            beta = root / "specs" / "beta" / "spec.md"
            nested = root / "specs" / "alpha" / "research" / "vendor" / "spec.md"
            alpha.parent.mkdir(parents=True)
            beta.parent.mkdir(parents=True)
            nested.parent.mkdir(parents=True)
            alpha.write_text(
                progress_spec_text(
                    "alpha",
                    status="Complete",
                    delivery_gate="Passed",
                ),
                encoding="utf-8",
            )
            beta.write_text(
                progress_spec_text(
                    "beta",
                    status="Implementing",
                    delivery_gate="In Progress",
                    open_second_task=True,
                ),
                encoding="utf-8",
            )
            nested.write_text(
                progress_spec_text(
                    "vendor",
                    status="Complete",
                    delivery_gate="Passed",
                ),
                encoding="utf-8",
            )
            result = run_script(self.SCRIPT, str(root), "--json")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(2, payload["summary"]["total_specs"])
        self.assertEqual(1, payload["summary"]["complete_specs"])
        self.assertEqual({"complete": 3, "total": 4, "percent": 75.0}, payload["summary"]["tasks"])
        self.assertEqual(
            {"complete": 16, "total": 20, "percent": 80.0},
            payload["summary"]["checklists"],
        )
        beta_report = next(item for item in payload["specs"] if item["slug"] == "beta")
        self.assertEqual("T002", beta_report["next"]["task"])
        self.assertEqual("EXECUTE", beta_report["next"]["item"])

    def test_progress_without_specs_returns_actionable_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_script(self.SCRIPT, directory)

        self.assertEqual(2, result.returncode)
        self.assertIn("Nenhuma especificação encontrada", result.stderr)
        self.assertIn("specs/<slug>/spec.md", result.stderr)

    def test_progress_routes_defined_spec_without_tasks_to_planning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "specs" / "idea" / "spec.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                """# Especificação integrada: Idea

**Formato**: Specsfy/2.0
**Slug**: idea
**Status**: Defined
**Definition Gate**: Passed
**Plan Gate**: Pending
**Delivery Gate**: Pending

### 14. Tarefas

Nenhuma tarefa criada.

### 15. Ordem de execução

Pending.
""",
                encoding="utf-8",
            )
            result = run_script(
                ".agents/skills/specsfy-progress/scripts/progress.py",
                str(root),
                "--json",
            )
            human = run_script(
                ".agents/skills/specsfy-progress/scripts/progress.py",
                str(root),
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        spec = json.loads(result.stdout)["specs"][0]
        self.assertEqual([], spec["blockers"])
        self.assertEqual("specsfy-tasks", spec["next_skill"])
        self.assertIn("$specsfy-tasks", human.stdout)

    def test_progress_filters_by_slug_and_rejects_unknown_slug(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for slug in ("alpha", "beta"):
                path = root / "specs" / slug / "spec.md"
                path.parent.mkdir(parents=True)
                path.write_text(
                    progress_spec_text(
                        slug,
                        status="Complete",
                        delivery_gate="Passed",
                    ),
                    encoding="utf-8",
                )
            selected = run_script(self.SCRIPT, str(root), "--slug", "beta", "--json")
            missing = run_script(self.SCRIPT, str(root), "--slug", "gamma")

        self.assertEqual(0, selected.returncode, selected.stdout + selected.stderr)
        payload = json.loads(selected.stdout)
        self.assertEqual(1, payload["summary"]["total_specs"])
        self.assertEqual(["beta"], [item["slug"] for item in payload["specs"]])
        self.assertEqual(2, missing.returncode)
        self.assertIn("gamma", missing.stderr)


class MCR10ContractTests(unittest.TestCase):
    """SPECSFY: US-009 FR-015 FR-016 AC-009 NFR-002 NFR-004"""

    def test_mcr_reference_is_canonical_complete_and_publishable(self) -> None:
        self.assertTrue(MCR_REFERENCE.is_file())
        self.assertFalse((ROOT / "MCR-10-metodo-categorial-de-requisitos.md").exists())
        text = MCR_REFERENCE.read_text(encoding="utf-8")
        self.assertIn("**Versão:** 1.0", text)
        self.assertIn("**Status:** referência estável", text)
        self.assertEqual(
            10,
            len(re.findall(r"^### 5\.\d+ .+$", text, re.MULTILINE)),
        )
        for section in (
            "Finalidade e intenção",
            "Adaptação moderna para software",
            "Equivalência terminológica",
            "Protocolo de conversa",
            "Critérios de conclusão",
            "Regras para uso por inteligência artificial",
            "Prompt operacional",
            "Referências e fidelidade conceitual",
        ):
            self.assertIn(section, text)
        self.assertIn("https://en.wikisource.org/wiki/The_Works_of_Aristotle/Categories", text)
        self.assertIn("https://plato.stanford.edu/archives/spr2021/entries/aristotle-categories/", text)
        self.assertNotRegex(text, r"\b(?:TODO|TBD|FIXME)\b")

    def test_discuss_and_specify_apply_the_same_mcr_reference(self) -> None:
        specify = (SKILLS / "specsfy-specify" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        discuss = (SKILLS / "specsfy-discuss" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("references/mcr-10.md", specify)
        self.assertIn("../specsfy-specify/references/mcr-10.md", discuss)
        self.assertIn("uma pergunta por vez", discuss)
        self.assertIn("intenção", discuss)
        self.assertIn("declaração", specify)
        self.assertIn("inferência", specify)

    def test_agents_guide_governs_skill_development(self) -> None:
        self.assertTrue(AGENT_GUIDE.is_file())
        text = AGENT_GUIDE.read_text(encoding="utf-8")
        for content in (
            "Guia de desenvolvimento das skills",
            "Três atos por fatia vertical",
            "MCR-10",
            "skill-creator",
            "BDD",
            "TDD",
            "quick_validate.py",
            "specs/<slug>/spec.md",
            ".agents/skills/<nome>/",
        ):
            self.assertIn(content, text)


class ThreeActContractTests(unittest.TestCase):
    """SPECSFY: US-010 FR-017 FR-018 AC-010 NFR-002 NFR-003"""

    ACTS = [
        "Ato I — Definir",
        "Ato II — Projetar e provar",
        "Ato III — Entregar e validar",
    ]

    def test_spec_uses_exactly_three_acts_and_three_matching_gates(self) -> None:
        text = SPEC.read_text(encoding="utf-8")
        self.assertIn("**Formato**: Specsfy/2.0", text)
        self.assertEqual(
            self.ACTS,
            re.findall(r"^## (Ato [IVX]+ — .+)$", text, re.MULTILINE),
        )
        self.assertNotIn("## Parte ", text)
        for gate in ("Definition", "Plan", "Delivery"):
            self.assertIn(f"**{gate} Gate**: Passed", text)
        for legacy in ("Spec", "Tasks", "Tests"):
            self.assertNotIn(f"**{legacy} Gate**:", text)

    def test_template_and_skills_publish_the_same_handoffs(self) -> None:
        template = (
            SKILLS / "specsfy-specify" / "assets" / "spec-template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("**Formato**: Specsfy/2.0", template)
        self.assertEqual(
            self.ACTS,
            re.findall(r"^## (Ato [IVX]+ — .+)$", template, re.MULTILINE),
        )
        guide = AGENT_GUIDE.read_text(encoding="utf-8")
        self.assertIn("Draft → Defined → Planned → Implementing → Complete", guide)
        handoffs = {
            "specsfy-validate": "Status: Defined",
            "specsfy-tasks": "Status: Planned",
            "specsfy-implement": "Status: Implementing",
        }
        for skill, expected in handoffs.items():
            body = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(expected, body)

    def test_validator_rejects_gate_that_is_ahead_of_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text = set_workflow_state(
                SPEC.read_text(encoding="utf-8"),
                status="Defined",
                definition="Passed",
                plan="Pending",
                delivery="Pending",
            )
            valid = write_temp_spec(directory, text)
            valid_result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py",
                str(valid),
            )
            invalid_text = text.replace(
                "**Plan Gate**: Pending", "**Plan Gate**: Passed", 1
            )
            valid.write_text(invalid_text, encoding="utf-8")
            invalid_result = run_script(
                ".agents/skills/specsfy-validate/scripts/validate_spec.py",
                str(valid),
            )
        self.assertEqual(0, valid_result.returncode, valid_result.stdout + valid_result.stderr)
        self.assertEqual(1, invalid_result.returncode)
        self.assertIn("Status Defined", invalid_result.stdout)

    def test_progress_exposes_three_act_gate_names(self) -> None:
        result = run_script(
            ".agents/skills/specsfy-progress/scripts/progress.py",
            ".",
            "--json",
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        gates = next(
            item["gates"] for item in payload["specs"] if item["slug"] == "specsfy"
        )
        self.assertEqual({"definition", "plan", "delivery"}, set(gates))
        self.assertEqual({"Passed"}, set(gates.values()))


class ReadmeContractTests(unittest.TestCase):
    """SPECSFY: US-011 FR-019 FR-020 FR-021 NFR-005 AC-011"""

    def test_readme_publishes_the_complete_method_and_naming_status(self) -> None:
        self.assertTrue(README.is_file())
        text = README.read_text(encoding="utf-8")
        for heading in (
            "# Specsfy",
            "## Proposta",
            "## Fonte da verdade",
            "## Os três atos rígidos",
            "### Ato I — Definir",
            "### Ato II — Projetar e provar",
            "### Ato III — Entregar e validar",
            "## Máquina de estados e gates",
            "## BDD e TDD",
            "## MCR-10",
            "## Tarefas e evidências",
            "## Catálogo atual de skills",
            "## Nomenclatura recomendada",
            "## Fluxo completo",
            "## Estrutura do repositório",
            "## Como usar",
            "## Validação",
            "## Limites e antipadrões",
            "## Evolução recomendada",
        ):
            self.assertIn(heading, text)
        for contract in (
            "specs/<slug>/spec.md",
            "Draft → Defined → Planned → Implementing → Complete",
            "Definition Gate",
            "Plan Gate",
            "Delivery Gate",
            "Given/When/Then",
            "RED → GREEN → REFACTOR",
            "PREP → EXECUTE → VERIFY → EVIDENCE → IMPROVE",
            "Proposta ainda não implementada",
            "specsfy-a<ato>-s<etapa>-<responsabilidade>",
        ):
            self.assertIn(contract, text)
        for skill in EXPECTED_SKILLS:
            self.assertIn(skill, text)
        for proposed in (
            "specsfy-a1-s1-discover",
            "specsfy-a1-s2-specify",
            "specsfy-a1-s3-validate-definition",
            "specsfy-a2-s1-plan",
            "specsfy-a2-s2-prove-plan",
            "specsfy-a3-s1-implement",
            "specsfy-a3-s2-validate-delivery",
            "specsfy-x-s1-progress",
        ):
            self.assertIn(proposed, text)
        self.assertNotRegex(text, r"\b(?:TODO|TBD|FIXME)\b")

    def test_readme_commands_and_local_links_are_usable(self) -> None:
        self.assertTrue(README.is_file())
        text = README.read_text(encoding="utf-8")
        for command in (
            "validate_spec.py specs/<slug>/spec.md",
            "validate_tasks.py specs/<slug>/spec.md",
            "check_traceability.py specs/<slug>/spec.md .",
            "progress.py .",
        ):
            self.assertIn(command, text)
        local_links = re.findall(
            r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)",
            text,
        )
        self.assertTrue(local_links)
        missing = [
            target
            for target in local_links
            if not (ROOT / target.split("#", 1)[0]).exists()
        ]
        self.assertEqual([], missing)

    def test_readme_ends_with_project_credits(self) -> None:
        text = README.read_text(encoding="utf-8")
        credits = text[text.rfind("## Créditos") :]
        for value in (
            "Promovaweb",
            "Luiz Eduardo Oliveira Fonseca",
            "comunidade",
            "https://promovaweb.com",
            "contato@promovaweb.com",
        ):
            self.assertIn(value, credits)
        self.assertTrue(
            text.rstrip().endswith(
                "[contato@promovaweb.com](mailto:contato@promovaweb.com)."
            )
        )


if __name__ == "__main__":
    unittest.main()
