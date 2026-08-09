from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "specsfy-update-spec"
SCRIPT = SKILL / "scripts" / "analyze_change.mjs"

class UpdateSpecTests(unittest.TestCase):
    def test_skill_has_canonical_structure_and_metadata(self) -> None:
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("name: specsfy-update-spec", content)
        self.assertIn('display_name: "Atualizar especificação"', metadata)
        self.assertIn("$specsfy-update-spec", metadata)

    def test_analyzer_reopens_only_the_acts_invalidated_by_the_change(self) -> None:
        original = (
            "### 3. Escopo e atores\n\nOriginal\n\n"
            "### 10. Plano técnico\n\nPlano original\n\n"
            "### 11. Estratégia TDD\n\nTeste original\n"
        )
        definition_change = original.replace("Original", "Com novo comportamento")
        plan_change = original.replace("Plano original", "Plano revisado")
        evidence_change = original.replace("Teste original", "Teste reexecutado")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = root / "spec.md"
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@specsfy.local"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Specsfy Test"], cwd=root, check=True)
            spec.write_text(original, encoding="utf-8")
            subprocess.run(["git", "add", "spec.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "base"], cwd=root, check=True, capture_output=True)
            def analyze(content: str) -> dict:
                spec.write_text(content, encoding="utf-8")
                run = subprocess.run(["node", str(SCRIPT), str(spec), "--json"], cwd=root, text=True, capture_output=True, check=False)
                self.assertEqual(0, run.returncode, run.stderr)
                return json.loads(run.stdout)
            definition = analyze(definition_change)
            plan = analyze(plan_change)
            evidence = analyze(evidence_change)

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
