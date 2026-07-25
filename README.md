# Specsfy Dev

Este é o workspace orquestrador de desenvolvimento do Specsfy. Ele reúne cinco
repositórios independentes, cada um com sua própria raiz Git, no mesmo layout
local para permitir especificação, testes de contrato, integração e evolução
coordenada.

Este README não é a apresentação pública do método. A porta de entrada para o
usuário final está em [`specsfy/`](specsfy/) e em
[`https://github.com/specsfy/specsfy`](https://github.com/specsfy/specsfy).

## Repositórios

| Caminho local | Repositório | Responsabilidade |
| --- | --- | --- |
| `./` | [`specsfy/dev`](https://github.com/specsfy/dev) | orquestração, specs de desenvolvimento e testes integrados |
| `brand/` | [`specsfy/brand`](https://github.com/specsfy/brand) | identidade visual, verbal e ativos de marca |
| `skills/` | [`specsfy/skills`](https://github.com/specsfy/skills) | metodologia executável, skills, scripts e referências |
| `docs/` | [`specsfy/docs`](https://github.com/specsfy/docs) | documentação final para o usuário |
| `specsfy/` | [`specsfy/specsfy`](https://github.com/specsfy/specsfy) | porta de entrada e visão geral do projeto |

Cada linha da tabela é uma raiz Git com remoto, branch, histórico e commits
próprios. Os quatro filhos são ignorados pelo repositório `dev`; não são
submódulos e não existem gitlinks entre eles.

## Como o workspace funciona

```text
dev/
├── AGENTS.md
├── README.md
├── specs/
├── tests/
├── .agents/skills ──► skills/
├── .claude/skills ──► skills/
├── brand/             # Git: specsfy/brand
├── skills/            # Git: specsfy/skills
├── docs/              # Git: specsfy/docs
└── specsfy/           # Git: specsfy/specsfy
```

- `specs/<slug>/spec.md` mantém a fonte normativa de cada mudança integrada.
- `tests/` contém BDD e contratos que podem atravessar os repositórios.
- `.agents/skills` e `.claude/skills` expõem localmente o catálogo versionado
  por `skills/`.
- O pai enxerga os filhos pelo filesystem, mas não versiona seu conteúdo.

## Preparar o workspace

Clone o orquestrador e os quatro filhos nos caminhos canônicos:

```bash
git clone https://github.com/specsfy/dev.git specsfy
git -C specsfy clone https://github.com/specsfy/brand.git brand
git -C specsfy clone https://github.com/specsfy/skills.git skills
git -C specsfy clone https://github.com/specsfy/docs.git docs
git -C specsfy clone https://github.com/specsfy/specsfy.git specsfy
```

Crie as projeções locais das skills quando elas ainda não existirem:

```bash
mkdir -p .agents .claude
ln -s "$PWD/skills" .agents/skills
ln -s "$PWD/skills" .claude/skills
```

## Trabalhar com Git

Execute Git na raiz proprietária da mudança:

```bash
git status --short --branch
git -C skills status --short --branch
git -C docs status --short --branch
git -C brand status --short --branch
git -C specsfy status --short --branch
```

O status do pai não mostra mudanças dos filhos, pois esses diretórios estão no
`.gitignore`. Uma entrega transversal pode exigir vários commits coordenados,
mas cada commit deve permanecer no repositório que possui os arquivos.

Não adicione os filhos ao índice do pai, não crie `.gitmodules` e não mova
conteúdo entre owners apenas para produzir um único commit.

## Onde alterar

- visão geral pública: `specsfy/README.md`;
- documentação final: [`docs/README.md`](docs/README.md);
- metodologia, skills e automação: `skills/`;
- marca: `brand/`;
- specs, testes integrados e orquestração: raiz `dev`;
- decisões transversais: comece pelo
  [roteador de contexto](docs/context/README.md).

As regras completas para agentes e contribuições estão em
[`AGENTS.md`](AGENTS.md). O desenvolvimento da metodologia possui instruções
adicionais em [`skills/AGENTS.md`](skills/AGENTS.md).

## Validação integrada

Na raiz do workspace:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
python3 -B .agents/skills/specsfy-validate/scripts/verify_repo.py . \
  --boundary local
```

Antes de concluir, execute também os validadores específicos de cada repositório
alterado e confira seu `git diff` separadamente.
