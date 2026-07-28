#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


START = "<!-- specsfy:framework:start -->"
END = "<!-- specsfy:framework:end -->"
SPEC_PATH_TOKEN = "{{SPECSFY_SPEC_PATH}}"


def json_object(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def detected_stack(project: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    composer = json_object(project / "composer.json")
    composer_packages = {
        **composer.get("require", {}),
        **composer.get("require-dev", {}),
    }
    if "laravel/framework" in composer_packages:
        rows.append(("Framework", "Laravel", "`composer.json`"))
    if composer:
        rows.append(("Linguagem", "PHP", "`composer.json`"))

    package = json_object(project / "package.json")
    packages = {
        **package.get("dependencies", {}),
        **package.get("devDependencies", {}),
    }
    if "next" in packages:
        rows.append(("Framework", "Next.js", "`package.json`"))
    if "astro" in packages:
        rows.append(("Framework", "Astro", "`package.json`"))
    if "react" in packages:
        rows.append(("Biblioteca", "React", "`package.json`"))
    if package:
        rows.append(("Runtime", "Node.js", "`package.json`"))
    return list(dict.fromkeys(rows))


def stack_label(rows: list[tuple[str, str, str]]) -> str:
    frameworks = [technology for kind, technology, _ in rows if kind == "Framework"]
    return ", ".join(frameworks) if frameworks else "stack ainda não identificado"


def model_guidance(rows: list[tuple[str, str, str]]) -> str:
    frameworks = {technology for kind, technology, _ in rows if kind == "Framework"}
    guidance: list[str] = []
    if "Laravel" in frameworks:
        guidance.append(
            "Para Laravel, descreva módulos de domínio, fronteiras HTTP/console e "
            "use `database/migrations` como primeira evidência do mapa de dados."
        )
    if "Next.js" in frameworks:
        guidance.append(
            "Para Next.js, explicite App Router, Server Components, Client "
            "Components e fronteiras entre servidor e navegador."
        )
    if "Astro" in frameworks:
        guidance.append(
            "Para Astro, explicite páginas, conteúdo, integrações e as ilhas "
            "interativas hidratadas no cliente."
        )
    if not guidance:
        guidance.append(
            "Confirme os manifests e as fronteiras principais antes de completar "
            "o modelo genérico."
        )
    return "\n\n".join(guidance)


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def merge_block(path: Path, block: str) -> bool:
    content = path.read_text(encoding="utf-8") if path.is_file() else ""
    if START in content and END in content:
        before, remainder = content.split(START, 1)
        _, after = remainder.split(END, 1)
        updated = f"{before}{block}{after}".rstrip() + "\n"
    else:
        updated = content.rstrip()
        if updated:
            updated += "\n\n"
        updated += block.rstrip() + "\n"
    if updated == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(updated, encoding="utf-8")
    return True


def framework_blocks() -> tuple[str, str]:
    reference = (
        Path(__file__).resolve().parents[1]
        / "references"
        / "framework-instructions.md"
    )
    reference_content = reference.read_text(encoding="utf-8")
    agents = (
        START
        + reference_content.split(START, 1)[1].split(END, 1)[0]
        + END
    ).replace(
        SPEC_PATH_TOKEN,
        ".specsfy/Spec.md",
    )
    claude = f"{START}\n@.specsfy/Spec.md\n{END}"
    return agents, claude


def project_template(label: str, guidance: str) -> str:
    return f"""# Projeto

## História e motivação

Descreva a origem do projeto, o problema que motivou sua criação e sua evolução.

## Finalidade

Explique para que o sistema serve e qual resultado entrega.

## Pessoas e contexto de uso

Registre quem usa o sistema e em quais situações.

## Capacidades principais

Liste as capacidades estáveis sem transformar esta descrição em inventário de
rotas, schemas ou tarefas.

## Limites

Explique o que o sistema deliberadamente não faz.

## Contexto técnico

Modelo inicial sugerido a partir de: **{label}**. Detalhes verificáveis ficam em
`.specsfy/STACK.md` e `.specsfy/DATABASE.md`.

{guidance}
"""


def stack_template(rows: list[tuple[str, str, str]]) -> str:
    rendered = rows or [
        ("Framework", "A confirmar", "Nenhum manifest reconhecido"),
    ]
    table = "\n".join(f"| {kind} | {technology} | {source} |" for kind, technology, source in rendered)
    return f"""# Stack do sistema

Documente tecnologias estruturais e a evidência executável que confirma cada
uma. Preserve decisões humanas nas seções livres deste arquivo.

## Inventário detectado

<!-- specsfy:stack:start -->
| Camada | Tecnologia | Evidência |
| --- | --- | --- |
{table}
<!-- specsfy:stack:end -->

## Decisões e observações do projeto

Acrescente aqui escolhas, restrições e contexto que não podem ser inferidos dos
manifests.
"""


def rules_template(label: str, guidance: str) -> str:
    return f"""# Regras do sistema

Estas regras complementam as instruções dos agentes sem substituir specs ou
critérios de aceite. Modelo inicial sugerido para **{label}**.

{guidance}

## Arquitetura

## Código e qualidade

## Testes

## Segurança e privacidade

## Operação

## Regras específicas do projeto
"""


def database_template(label: str, guidance: str) -> str:
    return f"""# Banco de dados

Mapa de persistência do sistema. Modelo inicial sugerido para **{label}**.

{guidance}

## Fontes de dados

<!-- specsfy:database:start -->
| Fonte | Tecnologia | Configuração segura | Evidência |
| --- | --- | --- | --- |
| Principal | A confirmar | Nome de variável, nunca o valor | A confirmar |

## Estruturas

| Estrutura | Tipo | Campos | Relações | Fonte |
| --- | --- | --- | --- | --- |
| A confirmar | A confirmar | A confirmar | A confirmar | A confirmar |
<!-- specsfy:database:end -->

## Decisões, ownership e retenção

Registre finalidade, ownership, classificação, retenção, constraints e decisões
que não estejam explícitas nos schemas.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path.cwd())
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)
    rows = detected_stack(project)
    label = stack_label(rows)
    guidance = model_guidance(rows)
    targets = {
        project / "PROJECT.md": project_template(label, guidance),
        project / ".specsfy" / "STACK.md": stack_template(rows),
        project / ".specsfy" / "RULES.md": rules_template(label, guidance),
        project / ".specsfy" / "DATABASE.md": database_template(label, guidance),
    }
    changed = [path for path, content in targets.items() if write_if_missing(path, content)]
    agents_block, claude_block = framework_blocks()
    if merge_block(project / "AGENTS.md", agents_block):
        changed.append(project / "AGENTS.md")
    if merge_block(project / "CLAUDE.md", claude_block):
        changed.append(project / "CLAUDE.md")
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
