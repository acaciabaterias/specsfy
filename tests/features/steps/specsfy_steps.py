from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
SPEC = ROOT / "specs" / "specsfy" / "spec.md"
MCR_REFERENCE = (
    ROOT / ".agents" / "skills" / "specsfy-specify" / "references" / "mcr-10.md"
)
AGENT_GUIDE = ROOT / "AGENTS.md"
README = ROOT / "README.md"


def run_script(relative: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / relative), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


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


@given("o repositório Specsfy")
def given_repository(context) -> None:
    context.root = ROOT


@when('executo a verificação de aceite "{check}"')
def when_check(context, check: str) -> None:
    text = SPEC.read_text(encoding="utf-8")
    if check == "skill-catalog":
        skills = {
            path.name
            for path in (ROOT / ".agents" / "skills").glob("specsfy-*")
            if path.is_dir()
        }
        context.acceptance = (
            len(skills) == 7
            and "specsfy-discuss" in skills
            and "specsfy-progress" in skills
        )
        context.detail = sorted(skills)
    elif check == "rigid-source":
        feature_package = ROOT / "specs" / "specsfy"
        research = feature_package / "research"
        context.acceptance = (
            "**Formato**: Specsfy/2.0" in text
            and "**Slug**: specsfy" in text
            and not (ROOT / "spec.md").exists()
            and not (ROOT / "tasks.md").exists()
            and not (ROOT / "spec-kit").exists()
            and research.is_dir()
            and (research / "spec-kit" / "LICENSE").is_file()
            and "specs/specsfy/research/spec-kit/" in text
            and all(
                heading in text
                for heading in (
                    "## Ato I — Definir",
                    "## Ato II — Projetar e provar",
                    "## Ato III — Entregar e validar",
                )
            )
        )
        context.detail = "formato/partes/fonte normativa/pesquisa colocalizada"
    elif check == "strict-validation":
        result = run_script(
            ".agents/skills/specsfy-validate/scripts/validate_spec.py",
            "specs/specsfy/spec.md",
        )
        context.acceptance = result.returncode == 0
        context.detail = result.stdout + result.stderr
    elif check == "bdd-tdd-contract":
        gherkin_blocks = re.findall(r"```gherkin\s*(.*?)```", text, re.DOTALL)
        result = run_script(
            ".agents/skills/specsfy-tdd-bdd/scripts/check_traceability.py",
            "specs/specsfy/spec.md",
            ".",
            "--kinds",
            "FR,AC,NFR",
        )
        context.acceptance = (
            len(gherkin_blocks) >= 6
            and all(
                all(keyword in block for keyword in ("Feature:", "Scenario:", "Given ", "When ", "Then "))
                for block in gherkin_blocks
            )
            and result.returncode == 0
        )
        context.detail = result.stdout + result.stderr
    elif check == "embedded-tasks":
        result = run_script(
            ".agents/skills/specsfy-tasks/scripts/validate_tasks.py",
            "specs/specsfy/spec.md",
        )
        context.acceptance = result.returncode == 0
        context.detail = result.stdout + result.stderr
    elif check == "execution":
        completed = re.sub(
            r"^-\s+\[ \]\s+(T\d{3,})",
            r"- [x] \1",
            text,
            flags=re.MULTILINE,
        )
        completed = re.sub(
            r"^(\s+-\s+)\[ \](\s+\*\*(?:PREP|EXECUTE|VERIFY|EVIDENCE|IMPROVE)\*\*:)",
            r"\1[x]\2",
            completed,
            flags=re.MULTILINE,
        )
        completed = completed.replace("**Status**: Implementing", "**Status**: Complete", 1)
        completed = completed.replace(
            "**Delivery Gate**: In Progress", "**Delivery Gate**: Passed", 1
        )
        with tempfile.TemporaryDirectory() as directory:
            completed_spec = Path(directory) / "spec.md"
            completed_spec.write_text(completed, encoding="utf-8")
            result = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py",
                str(completed_spec),
                "--all",
            )
        context.acceptance = result.returncode == 0 and "Estado: complete" in result.stdout
        context.detail = result.stdout + result.stderr
    elif check == "task-checklists":
        progress = reset_task_progress(reset_task_progress(text, "T009"), "T010")
        progress = re.sub(
            r"^\*\*Status\*\*: .+$",
            "**Status**: Implementing",
            progress,
            count=1,
            flags=re.MULTILINE,
        )
        progress = re.sub(
            r"^\*\*Delivery Gate\*\*: .+$",
            "**Delivery Gate**: In Progress",
            progress,
            count=1,
            flags=re.MULTILINE,
        )
        inconsistent = progress.replace("- [ ] T009", "- [x] T009", 1)
        with tempfile.TemporaryDirectory() as directory:
            temporary_spec = Path(directory) / "invalid-spec.md"
            temporary_spec.write_text(inconsistent, encoding="utf-8")
            progress_spec = Path(directory) / "progress-spec.md"
            progress_spec.write_text(progress, encoding="utf-8")
            validation = run_script(
                ".agents/skills/specsfy-tasks/scripts/validate_tasks.py",
                str(temporary_spec),
            )
            selection = run_script(
                ".agents/skills/specsfy-implement/scripts/next_task.py",
                str(progress_spec),
            )
        context.acceptance = (
            validation.returncode == 1
            and "checklist" in validation.stdout
            and selection.returncode == 0
            and "PRÓXIMO ITEM: T009 PREP" in selection.stdout
        )
        context.detail = (
            "validation:\n"
            + validation.stdout
            + validation.stderr
            + "\nselection:\n"
            + selection.stdout
            + selection.stderr
        )
    elif check == "overall-progress":
        before = SPEC.read_text(encoding="utf-8")
        human = run_script(
            ".agents/skills/specsfy-progress/scripts/progress.py",
            ".",
        )
        machine = run_script(
            ".agents/skills/specsfy-progress/scripts/progress.py",
            ".",
            "--json",
        )
        try:
            payload = json.loads(machine.stdout)
        except json.JSONDecodeError:
            payload = {}
        after = SPEC.read_text(encoding="utf-8")
        context.acceptance = (
            human.returncode == 0
            and machine.returncode == 0
            and "Progresso geral" in human.stdout
            and "specsfy" in human.stdout
            and payload.get("summary", {}).get("total_specs", 0) >= 1
            and bool(payload.get("specs"))
            and before == after
        )
        context.detail = (
            "human:\n"
            + human.stdout
            + human.stderr
            + "\njson:\n"
            + machine.stdout
            + machine.stderr
        )
    elif check == "mcr-10":
        specify = (
            ROOT / ".agents" / "skills" / "specsfy-specify" / "SKILL.md"
        ).read_text(encoding="utf-8")
        discuss = (
            ROOT / ".agents" / "skills" / "specsfy-discuss" / "SKILL.md"
        ).read_text(encoding="utf-8")
        reference = (
            MCR_REFERENCE.read_text(encoding="utf-8")
            if MCR_REFERENCE.is_file()
            else ""
        )
        guide = AGENT_GUIDE.read_text(encoding="utf-8") if AGENT_GUIDE.is_file() else ""
        categories = re.findall(r"^### 5\.\d+ .+$", reference, re.MULTILINE)
        context.acceptance = (
            MCR_REFERENCE.is_file()
            and AGENT_GUIDE.is_file()
            and not (ROOT / "MCR-10-metodo-categorial-de-requisitos.md").exists()
            and len(categories) == 10
            and "references/mcr-10.md" in specify
            and "../specsfy-specify/references/mcr-10.md" in discuss
            and "uma pergunta por vez" in discuss
            and "Finalidade e intenção" in reference
            and "Adaptação moderna para software" in reference
            and "declaração" in reference
            and "inferência" in reference
            and "AGENTS.md" in guide
            and "MCR-10" in guide
        )
        context.detail = {
            "reference_exists": MCR_REFERENCE.is_file(),
            "guide_exists": AGENT_GUIDE.is_file(),
            "root_copy_exists": (
                ROOT / "MCR-10-metodo-categorial-de-requisitos.md"
            ).exists(),
            "category_count": len(categories),
        }
    elif check == "three-act-flow":
        validation = run_script(
            ".agents/skills/specsfy-validate/scripts/validate_spec.py",
            "specs/specsfy/spec.md",
        )
        progress = run_script(
            ".agents/skills/specsfy-progress/scripts/progress.py",
            ".",
            "--json",
        )
        try:
            payload = json.loads(progress.stdout)
        except json.JSONDecodeError:
            payload = {}
        acts = re.findall(r"^## (Ato [IVX]+ — .+)$", text, re.MULTILINE)
        gates = next(
            (
                item.get("gates", {})
                for item in payload.get("specs", [])
                if item.get("slug") == "specsfy"
            ),
            {},
        )
        context.acceptance = (
            "**Formato**: Specsfy/2.0" in text
            and acts
            == [
                "Ato I — Definir",
                "Ato II — Projetar e provar",
                "Ato III — Entregar e validar",
            ]
            and "## Parte " not in text
            and all(
                f"**{name} Gate**: Passed" in text
                for name in ("Definition", "Plan", "Delivery")
            )
            and not any(
                f"**{name} Gate**:" in text
                for name in ("Spec", "Tasks", "Tests")
            )
            and validation.returncode == 0
            and progress.returncode == 0
            and set(gates) == {"definition", "plan", "delivery"}
        )
        context.detail = (
            f"acts={acts}; gates={gates}\n"
            + validation.stdout
            + validation.stderr
            + progress.stdout
            + progress.stderr
        )
    elif check == "readme-guide":
        readme = README.read_text(encoding="utf-8") if README.is_file() else ""
        current_skills = (
            "specsfy-discuss",
            "specsfy-specify",
            "specsfy-validate",
            "specsfy-tdd-bdd",
            "specsfy-tasks",
            "specsfy-implement",
            "specsfy-progress",
        )
        proposed_skills = (
            "specsfy-a1-s1-discover",
            "specsfy-a1-s2-specify",
            "specsfy-a1-s3-validate-definition",
            "specsfy-a2-s1-plan",
            "specsfy-a2-s2-prove-plan",
            "specsfy-a3-s1-implement",
            "specsfy-a3-s2-validate-delivery",
            "specsfy-x-s1-progress",
        )
        context.acceptance = (
            README.is_file()
            and "## Os três atos rígidos" in readme
            and "Draft → Defined → Planned → Implementing → Complete" in readme
            and all(gate in readme for gate in ("Definition Gate", "Plan Gate", "Delivery Gate"))
            and all(skill in readme for skill in current_skills)
            and all(skill in readme for skill in proposed_skills)
            and "Proposta ainda não implementada" in readme
            and "specs/<slug>/spec.md" in readme
            and "MCR-10" in readme
            and "Gherkin" in readme
            and "RED → GREEN → REFACTOR" in readme
            and "## Créditos" in readme
            and "Promovaweb" in readme
            and "Luiz Eduardo Oliveira Fonseca" in readme
            and "comunidade" in readme
            and "promovaweb.com" in readme
            and "contato@promovaweb.com" in readme
            and readme.rstrip().endswith(
                "[contato@promovaweb.com](mailto:contato@promovaweb.com)."
            )
        )
        context.detail = {
            "readme_exists": README.is_file(),
            "readme_size": len(readme),
            "missing_current": [skill for skill in current_skills if skill not in readme],
            "missing_proposed": [skill for skill in proposed_skills if skill not in readme],
        }
    else:
        raise AssertionError(f"Verificação desconhecida: {check}")


@then("a verificação de aceite passa")
def then_passes(context) -> None:
    assert context.acceptance, context.detail
