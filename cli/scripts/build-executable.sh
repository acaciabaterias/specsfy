#!/usr/bin/env bash

set -euo pipefail

readonly SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly REPOSITORY_DIRECTORY="$(cd -- "${SCRIPT_DIRECTORY}/.." && pwd -P)"
readonly OUTPUT_DIRECTORY="${REPOSITORY_DIRECTORY}/bin"
readonly OUTPUT_EXECUTABLE="${OUTPUT_DIRECTORY}/specsfy"
readonly OUTPUT_MANIFEST="${OUTPUT_DIRECTORY}/specsfy.build.json"

if ! command -v uv >/dev/null 2>&1; then
    printf 'erro: uv não foi encontrado no PATH\n' >&2
    exit 1
fi

temporary_directory="$(mktemp -d)"
cleanup() {
    rm -rf -- "${temporary_directory}"
}
trap cleanup EXIT

application_directory="${temporary_directory}/application"
mkdir -p -- "${application_directory}" "${OUTPUT_DIRECTORY}"

uv pip install \
    --quiet \
    --target "${application_directory}" \
    "${REPOSITORY_DIRECTORY}"

find "${application_directory}" \
    \( -type d -name __pycache__ -o -type f \( -name '*.pyc' -o -name '*.pyo' \) \) \
    -exec rm -rf -- {} +

printf '%s\n' \
    'from specsfy_cli.app import main' \
    '' \
    'raise SystemExit(main())' \
    > "${application_directory}/__main__.py"

python3 -B -m zipapp \
    "${application_directory}" \
    --python "/usr/bin/env python3" \
    --output "${OUTPUT_EXECUTABLE}" \
    --compress
chmod 755 "${OUTPUT_EXECUTABLE}"

source_sha256="$(
    python3 -B "${SCRIPT_DIRECTORY}/source_fingerprint.py" \
        "${REPOSITORY_DIRECTORY}"
)"
binary_sha256="$(
    python3 -B -c \
        'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' \
        "${OUTPUT_EXECUTABLE}"
)"
cli_version="$(
    PYTHONPATH="${REPOSITORY_DIRECTORY}/src" \
        python3 -B -c 'from specsfy_cli import __version__; print(__version__)'
)"
printf '{\n  "schema_version": 2,\n  "format": "python-zipapp",\n  "version": "%s",\n  "source_sha256": "%s",\n  "binary_sha256": "%s"\n}\n' \
    "${cli_version}" \
    "${source_sha256}" \
    "${binary_sha256}" \
    > "${OUTPUT_MANIFEST}"

printf 'Executável reconstruído: %s\n' "${OUTPUT_EXECUTABLE}"
printf 'Fingerprint: %s\n' "${source_sha256}"
