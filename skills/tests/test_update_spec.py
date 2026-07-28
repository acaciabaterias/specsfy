from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "specsfy-base-update-spec"
SCRIPT = SKILL / "scripts" / "analyze_change.py"


def load_script():
    spec = importlib.util.spec_from_file_location("analyze_update_spec", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("não foi possível carregar analyze_change.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UpdateSpecTests(unittest.TestCase):
    def test_skill_has_canonical_structure_and_metadata(self) -> None:
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("name: specsfy-base-update-spec", content)
        self.assertIn('display_name: "Atualizar especificação"', metadata)
        self.assertIn("$specsfy-base-update-spec", metadata)

    def test_analyzer_reopens_only_the_acts_invalidated_by_the_change(self) -> None:
        analyzer = load_script()
        original = (
            "### 3. Escopo e atores\n\nOriginal\n\n"
            "### 10. Plano técnico\n\nPlano original\n\n"
            "### 11. Estratégia TDD\n\nTeste original\n"
        )
        definition_change = original.replace("Original", "Com novo comportamento")
        plan_change = original.replace("Plano original", "Plano revisado")
        evidence_change = original.replace("Teste original", "Teste reexecutado")

        definition = analyzer.analyze(original, definition_change, "impact", "HEAD")
        plan = analyzer.analyze(original, plan_change, "impact", "HEAD")
        evidence = analyzer.analyze(original, evidence_change, "impact", "HEAD")

        self.assertEqual("Ato I", definition["reopen_from"])
        self.assertEqual(
            ["Definition Gate", "Plan Gate", "Delivery Gate"],
            definition["invalidated_gates"],
        )
        self.assertEqual("Ato II", plan["reopen_from"])
        self.assertEqual(
            ["Plan Gate", "Delivery Gate"],
            plan["invalidated_gates"],
        )
        self.assertEqual("Nenhum", evidence["reopen_from"])
        self.assertEqual([], evidence["invalidated_gates"])


if __name__ == "__main__":
    unittest.main()
