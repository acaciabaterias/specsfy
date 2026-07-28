# Specsfy

<p align="center">
  <picture>
    <source srcset="brand/icons/icon.svg" type="image/svg+xml">
    <img src="brand/icons/icon.png" alt="Ícone do framework Specsfy" width="160">
  </picture>
</p>

> Especifique. Prove. Entregue.

Esta é a apresentação pública do Specsfy, uma metodologia prática para
desenvolver software a partir de uma
especificação única, executável e rastreável. Todo o projeto é mantido neste
monorepo: [`promovaweb/specsfy`](https://github.com/promovaweb/specsfy).

## Estrutura

| Caminho | Responsabilidade |
| --- | --- |
| [`skills/`](skills/) | metodologia executável e skills base |
| [`specialists/`](specialists/) | skills técnicas opcionais |
| [`cli/`](cli/) | CLI, TUI, instalação e atualização |
| [`docs/`](docs/) | documentação oficial e contexto transversal |
| [`brand/`](brand/) | identidade visual e verbal |
| [`example/`](example/) | aplicação interna de validação |
| [`specsfy/`](specsfy/) | tutorial público detalhado |
| [`tests/`](tests/) | contratos integrados do monorepo |

Todos os caminhos compartilham a mesma raiz, histórico, branch, issues, tags e
releases Git.

## Instalação

Requer Python 3.11+, [`uv`](https://docs.astral.sh/uv/) e o comando
[`skills`](https://github.com/vercel-labs/skills) ou `npx`.
Enquanto o repositório for privado, autentique uma vez com `gh auth login`;
o CLI reutiliza essa sessão. Em automações, defina `GH_TOKEN` ou
`GITHUB_TOKEN` com acesso de leitura ao repositório.

```bash
uv tool install 'git+https://github.com/promovaweb/specsfy.git#subdirectory=cli'
specsfy --version
cd caminho/do/projeto
specsfy install --project .
```

O CLI instala a metodologia de `skills/` e, sob demanda, especialistas de
`specialists/`. Veja o [guia de instalação](docs/user/installation.md), o
[primeiro uso](docs/user/getting-started.md) e o
[guia do CLI](docs/user/cli.md).
O portal completo está em [`docs/README.md`](docs/README.md).

Para desenvolver a partir do checkout:

```bash
git clone https://github.com/promovaweb/specsfy.git
cd specsfy
./scripts/install-cli.sh
```

Para reconstruir o manual de marca após alterar suas fontes:

```bash
make brand-guide
```

Esta raiz não é um projeto consumidor e não recebe `specs/` ou skills
instaladas.

## Validação

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
```

Os módulos possuem verificações focais descritas em seus `AGENTS.md`. Consulte
[`AGENTS.md`](AGENTS.md) antes de contribuir.

As skills locais
[`specsfy-monorepo-documentator`](.agents/skills/specsfy-monorepo-documentator/) e
[`specsfy-release-cli`](.agents/skills/specsfy-release-cli/) mantêm,
respectivamente, a documentação oficial e as releases estáveis do CLI.
