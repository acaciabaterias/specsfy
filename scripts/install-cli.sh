#!/usr/bin/env bash

set -euo pipefail

readonly SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly WORKSPACE_DIRECTORY="$(cd -- "${SCRIPT_DIRECTORY}/.." && pwd -P)"
readonly LOCAL_CLI_DIRECTORY="${WORKSPACE_DIRECTORY}/cli"
readonly GITHUB_CLI_SOURCE="git+https://github.com/promovaweb/specsfy.git#subdirectory=cli"

usage() {
    cat <<'EOF'
Uso: ./scripts/install-cli.sh [--github]

Instala ou atualiza o executável specsfy para o usuário atual com uv tool.

Sem argumentos:
  instala o checkout local disponível em cli/.

--github:
  instala a versão publicada em cli/ na branch main de promovaweb/specsfy.

Este script instala somente o CLI. Ele não instala skills e não cria arquivos
de projeto no monorepo oficial do Specsfy.

Download público do executável: get.specsfy.dev
EOF
}

cli_source="${LOCAL_CLI_DIRECTORY}"
case "${1:-}" in
    "")
        ;;
    --github)
        cli_source="${GITHUB_CLI_SOURCE}"
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *)
        printf 'erro: argumento desconhecido: %s\n\n' "$1" >&2
        usage >&2
        exit 2
        ;;
esac

if (( $# > 1 )); then
    printf 'erro: informe no máximo um argumento\n\n' >&2
    usage >&2
    exit 2
fi

if ! command -v uv >/dev/null 2>&1; then
    printf '%s\n' \
        'erro: uv não foi encontrado no PATH.' \
        'Instale-o por https://docs.astral.sh/uv/getting-started/installation/ e tente novamente.' \
        >&2
    exit 1
fi

if [[ "${cli_source}" == "${LOCAL_CLI_DIRECTORY}" ]]; then
    if [[ ! -f "${LOCAL_CLI_DIRECTORY}/pyproject.toml" ]]; then
        printf 'erro: checkout do CLI não encontrado em %s\n' \
            "${LOCAL_CLI_DIRECTORY}" >&2
        printf '%s\n' \
            'Clone https://github.com/promovaweb/specsfy.git ou use --github.' \
            >&2
        exit 1
    fi
fi

printf 'Instalando Specsfy CLI de %s\n' "${cli_source}"
uv tool install --force --reinstall "${cli_source}"

bin_directory="$(uv tool dir --bin)"
specsfy_executable="${bin_directory}/specsfy"
if [[ ! -x "${specsfy_executable}" ]]; then
    printf 'erro: uv concluiu, mas o executável não foi encontrado em %s\n' \
        "${specsfy_executable}" >&2
    exit 1
fi

installed_version="$("${specsfy_executable}" --version)"
printf 'Instalação concluída: %s\n' "${installed_version}"
printf 'Executável: %s\n' "${specsfy_executable}"

case ":${PATH}:" in
    *":${bin_directory}:"*)
        ;;
    *)
        printf 'Aviso: adicione %s ao PATH para executar `specsfy` diretamente.\n' \
            "${bin_directory}" >&2
        ;;
esac
