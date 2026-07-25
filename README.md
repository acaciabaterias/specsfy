# Specsfy Dev

Este é o workspace orquestrador de desenvolvimento do Specsfy. Ele reúne seis
repositórios independentes, cada um com sua própria raiz Git, no mesmo layout
local para permitir especificação, testes de contrato, integração e evolução
coordenada.

Este README não é a apresentação pública do método. A porta de entrada para o
usuário final está em
[`specsfy/specsfy`](https://github.com/specsfy/specsfy), e a documentação oficial
da metodologia está em [`specsfy/docs`](https://github.com/specsfy/docs).

## Repositórios

| Caminho local | Repositório | Responsabilidade |
| --- | --- | --- |
| `./` | [`specsfy/dev`](https://github.com/specsfy/dev) | orquestração e testes integrados autônomos |
| `brand/` | [`specsfy/brand`](https://github.com/specsfy/brand) | identidade visual, verbal e ativos de marca |
| `skills/` | [`specsfy/skills`](https://github.com/specsfy/skills) | metodologia executável, skills, scripts e referências |
| `docs/` | [`specsfy/docs`](https://github.com/specsfy/docs) | documentação final para o usuário |
| `example/` | [`specsfy/example`](https://github.com/specsfy/example) | aplicação interna de validação |
| `specsfy/` | [`specsfy/specsfy`](https://github.com/specsfy/specsfy) | porta de entrada e visão geral do projeto |

Cada linha da tabela é uma raiz Git com remoto, branch, histórico e commits
próprios. Os cinco filhos são ignorados pelo repositório `dev`; não são
submódulos e não existem gitlinks entre eles.

## Como o workspace funciona

```text
dev/
├── AGENTS.md
├── README.md
├── tests/
├── example/            # Git: specsfy/example
├── brand/             # Git: specsfy/brand
├── skills/            # Git: specsfy/skills
├── docs/              # Git: specsfy/docs
└── specsfy/           # Git: specsfy/specsfy
```

- `tests/` contém BDD e contratos que podem atravessar os repositórios.
- `example/` contém a aplicação Laravel usada para exercitar e validar o
  framework em um produto real; ela é versionada por `specsfy/example`.
- `skills/` é acessado diretamente como um repositório filho; o pai não instala
  ou projeta essas skills em `.agents/` ou `.claude/`.
- O pai enxerga os filhos pelo filesystem, mas não versiona seu conteúdo.

O repositório `dev` não é um projeto consumidor do Specsfy. Por isso, sua raiz
não contém `specs/`, `.agents/` ou `.claude/`. Specs são criadas somente nos
projetos que aplicam a metodologia.

## Aplicação de exemplo

[`specsfy/example`](https://github.com/specsfy/example) demonstra uma aplicação
Laravel com autenticação, segurança e equipes e serve como ambiente interno para
testar o fluxo completo do Specsfy.

Sua instalação, capacidades, arquitetura, dados, rotas e comandos estão em
[`README.md de specsfy/example`](https://github.com/specsfy/example/blob/main/README.md).
Essa documentação acompanha o aplicativo; ela não substitui a documentação
oficial da metodologia publicada por `specsfy/docs`.

## Preparar o workspace

Clone o orquestrador e os cinco filhos nos caminhos canônicos:

```bash
git clone https://github.com/specsfy/dev.git specsfy
git -C specsfy clone https://github.com/specsfy/brand.git brand
git -C specsfy clone https://github.com/specsfy/skills.git skills
git -C specsfy clone https://github.com/specsfy/docs.git docs
git -C specsfy clone https://github.com/specsfy/example.git example
git -C specsfy clone https://github.com/specsfy/specsfy.git specsfy
```

## Trabalhar com Git

Execute Git na raiz proprietária da mudança:

```bash
git status --short --branch
git -C skills status --short --branch
git -C docs status --short --branch
git -C example status --short --branch
git -C brand status --short --branch
git -C specsfy status --short --branch
```

O status do pai não mostra mudanças dos filhos, pois esses diretórios estão no
`.gitignore`. Uma entrega transversal pode exigir vários commits coordenados,
mas cada commit deve permanecer no repositório que possui os arquivos.

Não adicione os filhos ao índice do pai, não crie `.gitmodules` e não mova
conteúdo entre owners apenas para produzir um único commit.

## Onde alterar

- visão geral pública:
  [`specsfy/specsfy`](https://github.com/specsfy/specsfy);
- documentação oficial para usuários: `docs/README.md`, publicada em
  [`specsfy/docs`](https://github.com/specsfy/docs);
- aplicação interna de validação e sua documentação: `example/`;
- metodologia, skills e automação: `skills/`;
- marca: `brand/`;
- testes integrados e orquestração: raiz `dev`;
- specs de produto: repositório do projeto que aplica Specsfy, nunca a raiz
  `dev`;
- decisões transversais: comece pelo
  `docs/context/README.md`, publicado no repositório
  [`specsfy/docs`](https://github.com/specsfy/docs).

As regras completas para agentes e contribuições estão em
[`AGENTS.md`](AGENTS.md). O desenvolvimento da metodologia possui instruções
adicionais em
[`specsfy/skills`](https://github.com/specsfy/skills/blob/main/AGENTS.md).

## Validação integrada

Na raiz do workspace:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
```

Esses comandos não carregam nem executam as skills do projeto. Antes de
concluir, entre na raiz de cada repositório filho alterado, execute seus
validadores próprios e confira seu `git diff` separadamente.
