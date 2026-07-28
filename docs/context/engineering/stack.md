# Stack de engenharia

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | tecnologias estruturais |
| Autoridade | função, restrições e critérios das escolhas tecnológicas |

## Papel

Explicar tecnologias estruturais, suas responsabilidades e os critérios para
mudá-las sem duplicar versões mantidas por fontes executáveis.

## Como usar

Leia ao introduzir linguagem, runner, formato ou ferramenta transversal. Use
[packages.md](packages.md) para dependências e
[testing.md](testing.md) para comandos.

## Atualize quando

- uma tecnologia estrutural for adotada ou removida;
- a responsabilidade de uma ferramenta mudar;
- uma nova fonte executável de versão for criada.

## Não use para

- copiar uma árvore completa de dependências;
- fixar versão fora de manifest ou lockfile;
- transformar preferência pessoal em regra do projeto.

## Fonte da verdade e precedência

Este arquivo explica escolhas. Manifests, lockfiles, workflows e comandos são
fontes executáveis de versão e configuração. Atualmente o repositório não mantém
manifest próprio de dependências Python.

## Stack vigente

| Tecnologia | Responsabilidade | Fonte executável |
| --- | --- | --- |
| Markdown | skills, specs e contexto legível | arquivos versionados |
| Python 3 | validadores e testes de contrato | scripts e ambiente de execução |
| biblioteca padrão | automação determinística principal | imports dos scripts |
| Behave | aceite Gherkin | comandos e arquivos em `tests/features/` |
| `unittest` | TDD e regressão | arquivos `tests/test_*.py` |
| `uv` | ambiente efêmero para runners auxiliares | comandos documentados |
| GitHub Actions | verificação em CI | `.github/workflows/` |

## Aplicação de validação

`example/`, no repositório `example/`, é uma aplicação interna Laravel com
cliente Inertia React. Ela exercita a metodologia em uma superfície real, mas
não transforma PHP, JavaScript ou seu runtime em dependências do Specsfy.

| Área do exemplo | Responsabilidade | Fonte executável |
| --- | --- | --- |
| Laravel e PHP | domínio, HTTP, autenticação e persistência | `example/composer.json` e lockfile |
| Inertia, React e TypeScript | páginas e interação web | `example/package.json` e lockfile |
| SQLite | estado local da aplicação | migrations e configuração de `example/` |
| Pest, linters e build | regressão da superfície de validação | scripts dos manifests do exemplo |

## CLI e catálogos

| Área | Responsabilidade | Fonte executável |
| --- | --- | --- |
| Python, argparse, subprocess e urllib | comandos, instalação, projeção, runners e detecção de versões | `cli/` |
| Textual | interface terminal, streaming e resultados de testes | `cli/pyproject.toml` e lockfile |
| uv | instalação e atualização isoladas do CLI | manifest, lockfile e comandos publicados |
| Markdown/YAML | instruções e metadata das skills | `skills/` e `specialists/` |
| JSON | catálogo detectável e lock de instalação | `specialists/catalog.json` e lock do consumidor |

O CLI é ferramenta de distribuição; suas dependências não passam a ser
dependências dos projetos consumidores nem do workspace `promovaweb/specsfy`.

## Critérios de escolha

- Preferir biblioteca padrão para scripts determinísticos.
- Exigir benefício observável antes de adicionar dependência.
- Manter equivalência entre execução local e CI.
- Registrar versão em fonte executável, não neste contexto.
- Evitar rede, instalação global e ação destrutiva por padrão.
- Manter a stack de `example/` isolada da implementação da metodologia; sua
  adoção demonstra integração, não cria requisito para projetos usuários.
