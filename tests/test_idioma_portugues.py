from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_SPECSFY_SKILLS = tuple(
    sorted((ROOT / "example/.agents/skills").glob("specsfy-*"))
)
PROSE_ROOTS = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "docs",
    ROOT / "skills",
    ROOT / "specialists",
    ROOT / "brand",
    ROOT / "specsfy",
    ROOT / ".agents",
    ROOT / "cli/README.md",
    ROOT / "cli/AGENTS.md",
    ROOT / "example/.specsfy",
    ROOT / "example/docs",
    *EXAMPLE_SPECSFY_SKILLS,
)
PYTHON_ROOTS = (
    ROOT / ".agents",
    ROOT / ".ebook",
    ROOT / "cli",
    ROOT / "scripts",
    ROOT / "skills",
    ROOT / "specialists",
    ROOT / "tests",
    *EXAMPLE_SPECSFY_SKILLS,
)
PROSE_SUFFIXES = {".feature", ".md", ".txt", ".tsx", ".yaml", ".yml"}
GENERATED_PARTS = {".venv", "__pycache__", "node_modules", "vendor"}

# Esses padrões cobrem estruturas frequentes de prosa em inglês sem confundir
# identificadores, comandos e termos técnicos preservados pelo ecossistema.
ENGLISH_PROSE_PATTERNS = (
    re.compile(
        r"\b(?:the|this|these|those)\s+"
        r"(?:user|project|system|application|feature|component|repository|"
        r"workspace|skill|file|source|template|page|team|product|data|"
        r"request|response)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:use|uses|using|run|read|write|create|creates|return|returns|"
        r"ensure|check|validate|build|install|select|click)\s+"
        r"(?:the|this|these|those|an)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:you|we)\s+"
        r"(?:can|must|should|will|are|use|need|have|recommend|support)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:get started|learn more|contact us|sign in|sign up|"
        r"create account|privacy policy|all rights reserved|accept all|"
        r"reject all|email address|first name|last name|full name|"
        r"send message|view all|read more|start today)\b",
        re.IGNORECASE,
    ),
)
ENGLISH_DOCSTRING_WORDS = {
    "and",
    "build",
    "check",
    "collect",
    "create",
    "ensure",
    "extract",
    "file",
    "for",
    "from",
    "official",
    "prepare",
    "project",
    "read",
    "repository",
    "return",
    "run",
    "skill",
    "source",
    "test",
    "that",
    "the",
    "this",
    "use",
    "validate",
    "when",
    "with",
    "without",
    "workspace",
    "write",
}
PORTUGUESE_DOCSTRING_WORDS = {
    "a",
    "arquivo",
    "com",
    "cria",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "executa",
    "lê",
    "o",
    "oficial",
    "ou",
    "para",
    "por",
    "projeto",
    "repositório",
    "retorna",
    "sem",
    "teste",
    "testes",
    "um",
    "uma",
    "usa",
    "usar",
    "valida",
}
LATIN_PLACEHOLDERS = (
    "lorem ipsum",
    "dolor sit amet",
    "consectetur adipiscing",
    "sed do eiusmod",
    "ut enim ad minim veniam",
    "erat pellentesque",
    "maecenas",
    "risus nulla",
    "suspendisse",
)
ENGLISH_DISPLAY_NAME_TERMS = re.compile(
    r"\b(?:aux|code review|debugging|documentator|domain modeling|"
    r"performance|react ui components|release|setup)\b",
    re.IGNORECASE,
)
ENGLISH_RUNTIME_COPY = re.compile(
    r"\b(?:baseline unavailable|dashboard de|use kebab-case)\b|"
    r"approximation, not tokenizer output",
    re.IGNORECASE,
)
ENGLISH_UI_COPY = re.compile(
    r"\b(?:article|business|comparison|every 24 hours|growth|language|"
    r"optional|scale|submit|video|yes)\b",
    re.IGNORECASE,
)
VISIBLE_TSX_PATTERNS = (
    re.compile(r">\s*([^<{][^<{]*?)\s*<"),
    re.compile(
        r"\b(?:answer|description|eyebrow|heading|label|name|question|title)"
        r"\s*:\s*[\"'`]([^\"'`{}]+)[\"'`]"
    ),
    re.compile(
        r"\b(?:alt|aria-label|placeholder|title)\s*=\s*"
        r"[\"'`]([^\"'`{}]+)[\"'`]"
    ),
)


def files_under(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return [
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file()
        and not GENERATED_PARTS.intersection(candidate.relative_to(ROOT).parts)
    ]


class PortugueseLanguageContractTest(unittest.TestCase):
    def test_owned_prose_does_not_contain_common_english_sentences(self) -> None:
        violations: list[str] = []
        for prose_root in PROSE_ROOTS:
            for path in files_under(prose_root):
                if path.suffix not in PROSE_SUFFIXES:
                    continue
                fenced = False
                for line_number, line in enumerate(
                    path.read_text(encoding="utf-8", errors="ignore").splitlines(),
                    start=1,
                ):
                    stripped = line.strip()
                    if stripped.startswith("```"):
                        fenced = not fenced
                        continue
                    if fenced or "https://" in stripped or "http://" in stripped:
                        continue
                    if any(
                        pattern.search(stripped)
                        for pattern in ENGLISH_PROSE_PATTERNS
                    ):
                        violations.append(
                            f"{path.relative_to(ROOT)}:{line_number}: {stripped}"
                        )

        self.assertEqual([], violations)

    def test_python_docstrings_are_in_portuguese(self) -> None:
        violations: list[str] = []
        for python_root in PYTHON_ROOTS:
            for path in files_under(python_root):
                if path.suffix != ".py" or path.name == "test_idioma_portugues.py":
                    continue
                try:
                    tree = ast.parse(path.read_text(encoding="utf-8"))
                except (SyntaxError, UnicodeDecodeError):
                    continue
                nodes = [tree]
                nodes.extend(
                    node
                    for node in ast.walk(tree)
                    if isinstance(
                        node,
                        (ast.AsyncFunctionDef, ast.ClassDef, ast.FunctionDef),
                    )
                )
                for node in nodes:
                    docstring = ast.get_docstring(node, clean=False)
                    if not docstring or docstring.startswith("SPECSFY:"):
                        continue
                    words = set(
                        re.findall(r"[A-Za-zÀ-ÿ]+", docstring.casefold())
                    )
                    english_score = len(words & ENGLISH_DOCSTRING_WORDS)
                    portuguese_score = len(words & PORTUGUESE_DOCSTRING_WORDS)
                    if english_score >= 2 and english_score > portuguese_score:
                        violations.append(
                            f"{path.relative_to(ROOT)}:"
                            f"{getattr(node, 'lineno', 1)}: "
                            f"{docstring.splitlines()[0]}"
                        )

        self.assertEqual([], violations)

    def test_python_runtime_copy_is_in_portuguese(self) -> None:
        violations: list[str] = []
        for python_root in PYTHON_ROOTS:
            for path in files_under(python_root):
                if path.suffix != ".py" or path.name == "test_idioma_portugues.py":
                    continue
                try:
                    tree = ast.parse(path.read_text(encoding="utf-8"))
                except (SyntaxError, UnicodeDecodeError):
                    continue
                for node in ast.walk(tree):
                    if (
                        isinstance(node, ast.Constant)
                        and isinstance(node.value, str)
                        and ENGLISH_RUNTIME_COPY.search(node.value)
                    ):
                        violations.append(
                            f"{path.relative_to(ROOT)}:"
                            f"{getattr(node, 'lineno', 1)}: {node.value}"
                        )

        self.assertEqual([], violations)

    def test_skill_display_names_are_in_portuguese(self) -> None:
        violations: list[str] = []
        metadata_roots = (
            ROOT / ".agents",
            ROOT / "skills",
            ROOT / "specialists",
        )
        for metadata_root in metadata_roots:
            for path in metadata_root.rglob("openai.yaml"):
                for line_number, line in enumerate(
                    path.read_text(encoding="utf-8").splitlines(),
                    start=1,
                ):
                    if (
                        "display_name:" in line
                        and ENGLISH_DISPLAY_NAME_TERMS.search(line)
                    ):
                        violations.append(
                            f"{path.relative_to(ROOT)}:{line_number}: "
                            f"{line.strip()}"
                        )

        self.assertEqual([], violations)

    def test_react_gallery_has_no_latin_placeholder_copy(self) -> None:
        gallery = (
            ROOT
            / "specialists/specsfy-specialist-react-ui-components/assets"
        )
        violations: list[str] = []
        for path in gallery.rglob("*.tsx"):
            content = path.read_text(encoding="utf-8").casefold()
            for placeholder in LATIN_PLACEHOLDERS:
                if placeholder in content:
                    violations.append(
                        f"{path.relative_to(ROOT)}: {placeholder}"
                    )

        self.assertEqual([], violations)

    def test_react_gallery_visible_copy_is_in_portuguese(self) -> None:
        gallery = (
            ROOT
            / "specialists/specsfy-specialist-react-ui-components/assets"
        )
        violations: list[str] = []
        for path in gallery.rglob("*.tsx"):
            content = path.read_text(encoding="utf-8")
            for pattern in VISIBLE_TSX_PATTERNS:
                for match in pattern.finditer(content):
                    value = " ".join(match.group(1).split())
                    if ENGLISH_UI_COPY.search(value):
                        line_number = content[: match.start()].count("\n") + 1
                        violations.append(
                            f"{path.relative_to(ROOT)}:{line_number}: {value}"
                        )

        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
