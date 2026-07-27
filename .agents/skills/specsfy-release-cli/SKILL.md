---
name: specsfy-release-cli
description: Publicar uma versão estável do Specsfy CLI a partir do workspace orquestrador, mantendo versão do pacote, executável, CHANGELOG.md, commit, tag Git e GitHub Release coerentes. Use somente no dev hub quando a pessoa pedir para lançar, publicar ou retomar uma versão do repositório specsfy/cli. Não use para releases de outros repositórios, versões de pré-lançamento ou atualização do CLI em projetos consumidores.
---

# Publicar o Specsfy CLI

Executar a partir de `/home/luizeof/specsfy`. Exigir uma versão `X.Y.Z` e notas
de release confirmadas pela pessoa. Não inferir autorização para publicar apenas
de uma mudança de código ou de versão.

## 1. Classificar o estado

1. Validar os owners:

```bash
git remote get-url origin
git -C cli remote get-url origin
git -C cli branch --show-current
gh auth status
```

Exigir os remotos `specsfy/dev` e `specsfy/cli`, branch `main` no CLI e acesso
ao repositório `specsfy/cli`.

2. Atualizar referências sem alterar arquivos e comparar a branch:

```bash
git -C cli fetch origin main --tags
git -C cli status --porcelain
git -C cli rev-parse HEAD
git -C cli rev-parse origin/main
git -C cli rev-parse --verify refs/tags/vX.Y.Z
gh release view vX.Y.Z --repo specsfy/cli --json tagName,targetCommitish,body
```

Para uma publicação nova, exigir worktree limpa, `HEAD` igual a `origin/main` e
ausência da tag e do release. Não limpar, descartar ou incorporar mudanças
preexistentes.

Se já existir estado parcial, não recriar commit, tag ou versão:

- release existente: extrair a seção do changelog, comparar seu corpo e
  confirmar que tag, commit e versão convergem;
- tag remota sem release: confirmar que aponta para o commit de release e
  retomar somente a criação do GitHub Release;
- tag apenas local: confirmar o commit e retomar o push atômico;
- commit de release local sem tag: validar artefatos e retomar pela tag;
- arquivos preparados sem commit: validar o diff permitido e retomar pelos
  testes.

Interromper diante de divergência, versão já publicada com outro conteúdo,
branch dessincronizada ou mudança que não pertença ao release.

## 2. Preparar versão e changelog

Escrever as notas em um arquivo temporário Markdown. Manter conteúdo orientado
ao usuário e não incluir o título da versão. Executar:

```bash
python3 -B .agents/skills/specsfy-release-cli/scripts/release_changelog.py prepare \
  --cli cli \
  --version X.Y.Z \
  --date YYYY-MM-DD \
  --notes-file /caminho/notas.md
```

O script exige versão estável crescente, atualiza `cli/pyproject.toml` e
`cli/src/specsfy_cli/__init__.py` e promove as notas sob
`## [X.Y.Z] - YYYY-MM-DD` em `cli/CHANGELOG.md`.

Atualizar o lock e produzir o único arquivo de notas que seguirá até o GitHub:

```bash
cd cli
uv lock
uv sync --locked
./scripts/build-executable.sh
uv run python -B -m unittest discover -s tests -p 'test_*.py'
uv run specsfy --help
./bin/specsfy --version
cd ..
python3 -B .agents/skills/specsfy-release-cli/scripts/release_changelog.py extract \
  --changelog cli/CHANGELOG.md \
  --version X.Y.Z \
  --output /caminho/release-notes.md
```

Exigir que `uv run specsfy --version`, `./bin/specsfy --version`,
`pyproject.toml`, `__version__`, `uv.lock` e `bin/specsfy.build.json` mostrem
`X.Y.Z`.

## 3. Revisar e versionar

Revisar o diff e permitir somente os artefatos esperados:

- `CHANGELOG.md`;
- `pyproject.toml`;
- `src/specsfy_cli/__init__.py`;
- `uv.lock`;
- `bin/specsfy`;
- `bin/specsfy.build.json`.

Apresentar versão, notas e diff à pessoa antes da publicação remota. Após a
confirmação explícita, criar um commit e uma tag anotada no mesmo commit:

```bash
git -C cli add CHANGELOG.md pyproject.toml src/specsfy_cli/__init__.py \
  uv.lock bin/specsfy bin/specsfy.build.json
git -C cli commit -m "chore(release): vX.Y.Z"
git -C cli tag -a vX.Y.Z -m "Specsfy CLI vX.Y.Z"
git -C cli rev-parse HEAD
git -C cli rev-list -n 1 vX.Y.Z
```

Os dois hashes devem ser idênticos.

## 4. Publicar e comprovar

Enviar branch e tag na mesma operação e criar o release a partir das notas
extraídas do changelog:

```bash
git -C cli push --atomic origin main vX.Y.Z
gh release create vX.Y.Z \
  --repo specsfy/cli \
  --verify-tag \
  --title "Specsfy CLI vX.Y.Z" \
  --notes-file /caminho/release-notes.md
gh release view vX.Y.Z \
  --repo specsfy/cli \
  --json url,tagName,targetCommitish,body
gh release view vX.Y.Z \
  --repo specsfy/cli \
  --json body > /caminho/release-publicado.json
python3 -B .agents/skills/specsfy-release-cli/scripts/release_changelog.py verify \
  --changelog cli/CHANGELOG.md \
  --version X.Y.Z \
  --release-json /caminho/release-publicado.json
git -C cli ls-remote origin "refs/tags/vX.Y.Z^{}"
gh run list --repo specsfy/cli --branch vX.Y.Z --workflow validate
```

Exigir sucesso de `release_changelog.py verify`. Confirmar também que a tag
remota aponta para o commit publicado e que a suíte de CI da tag concluiu. Se o
push ou `gh release create` falhar, preservar o estado e retomar pela
classificação inicial; nunca criar uma segunda tag para compensar uma
publicação parcial.

Concluir informando versão, commit, tag, URL do GitHub Release, testes e
correspondência exata das notas.
