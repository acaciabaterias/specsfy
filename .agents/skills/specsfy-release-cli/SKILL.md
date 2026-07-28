---
name: specsfy-release-cli
description: Publicar uma versão estável do Specsfy CLI a partir do monorepo promovaweb/specsfy, mantendo pacote, executável, CHANGELOG.md, commit, tag e GitHub Release coerentes. Use quando a pessoa pedir para lançar ou retomar uma versão do CLI. Não use para pré-releases nem apenas para atualizar o CLI de um consumidor.
---

# Publicar o Specsfy CLI

Executar na raiz `/home/luizeof/specsfy`. Exigir versão `X.Y.Z`, notas
confirmadas e autorização explícita antes de push.

## 1. Classificar o estado

```bash
git remote get-url origin
git branch --show-current
gh auth status
git fetch origin main --tags
git status --porcelain
git rev-parse HEAD
git rev-parse origin/main
git rev-parse --verify refs/tags/vX.Y.Z
gh release view vX.Y.Z --repo promovaweb/specsfy \
  --json tagName,targetCommitish,body
```

Exigir remoto `https://github.com/promovaweb/specsfy`, branch `main`, acesso ao
mesmo repositório, worktree limpa, `HEAD` igual a `origin/main` e ausência da
tag e do release para publicação nova.

Em estado parcial, não recriar commit, tag ou versão. Compare tag, commit,
artefatos e seção do changelog e retome apenas a etapa ausente.

## 2. Preparar versão

```bash
python3 -B .agents/skills/specsfy-release-cli/scripts/release_changelog.py prepare \
  --cli cli --version X.Y.Z --date YYYY-MM-DD \
  --notes-file /caminho/notas.md
cd cli
uv lock
uv sync --locked
./scripts/build-executable.sh
uv run python -B -m unittest discover -s tests -p 'test_*.py'
uv run specsfy --help
./bin/specsfy --version
cd ..
python3 -B .agents/skills/specsfy-release-cli/scripts/release_changelog.py extract \
  --changelog cli/CHANGELOG.md --version X.Y.Z \
  --output /caminho/release-notes.md
```

Exigir `X.Y.Z` em `pyproject.toml`, `__version__`, `uv.lock`, CLI instalado,
binário e `bin/specsfy.build.json`. O changelog promove as notas sob
`## [X.Y.Z] - YYYY-MM-DD`.

## 3. Revisar e versionar

Permitir somente:

- `cli/CHANGELOG.md`;
- `cli/pyproject.toml`;
- `cli/src/specsfy_cli/__init__.py`;
- `cli/uv.lock`;
- `cli/bin/specsfy`;
- `cli/bin/specsfy.build.json`.

Apresentar notas e diff. Após confirmação:

```bash
git add cli/CHANGELOG.md cli/pyproject.toml \
  cli/src/specsfy_cli/__init__.py cli/uv.lock \
  cli/bin/specsfy cli/bin/specsfy.build.json
git commit -m "chore(release): vX.Y.Z"
git tag -a vX.Y.Z -m "Specsfy CLI vX.Y.Z"
git rev-parse HEAD
git rev-list -n 1 vX.Y.Z
```

Os hashes devem ser idênticos. A tag pertence ao monorepo.

## 4. Publicar e comprovar

```bash
git push --atomic origin main vX.Y.Z
gh release create vX.Y.Z \
  --repo promovaweb/specsfy --verify-tag \
  --title "Specsfy CLI vX.Y.Z" \
  --notes-file /caminho/release-notes.md
gh release view vX.Y.Z --repo promovaweb/specsfy \
  --json url,tagName,targetCommitish,body
gh release view vX.Y.Z --repo promovaweb/specsfy \
  --json body > /caminho/release-publicado.json
python3 -B .agents/skills/specsfy-release-cli/scripts/release_changelog.py verify \
  --changelog cli/CHANGELOG.md --version X.Y.Z \
  --release-json /caminho/release-publicado.json
git ls-remote origin "refs/tags/vX.Y.Z^{}"
gh run list --repo promovaweb/specsfy --branch vX.Y.Z --workflow Specsfy
```

Confirmar tag remota, CI e equivalência exata das notas. Em falha, preservar o
estado e reclassificar; nunca criar uma tag compensatória.
