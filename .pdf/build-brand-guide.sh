#!/usr/bin/env bash
# Gera o manual de marca publicado em brand/ a partir das fontes coordenadas
# pelo monorepo promovaweb/specsfy.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUB_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BRAND_ROOT="$HUB_ROOT/brand"
MD_SOURCE="$BRAND_ROOT/guide/brand-guide.md"
TEMPLATE="$BRAND_ROOT/guide/template.html"
STYLE_GUIDE="$BRAND_ROOT/style-guide.html"
PDF_STYLE="$HUB_ROOT/.pdf/style.css"
BUILD_DIR="$HUB_ROOT/.pdf/build"
OUT_HTML="$BUILD_DIR/brand-guide.html"
OUT_PDF="$BRAND_ROOT/Specsfy-Manual-de-Marca.pdf"

for bin in pandoc weasyprint; do
  if ! command -v "$bin" >/dev/null 2>&1; then
    echo "Erro: '$bin' não encontrado no PATH." >&2
    echo "Instale com: brew install pandoc weasyprint" >&2
    echo "         ou: apt-get install pandoc weasyprint" >&2
    exit 1
  fi
done

for source in "$MD_SOURCE" "$TEMPLATE" "$STYLE_GUIDE" "$PDF_STYLE"; do
  if [ ! -f "$source" ]; then
    echo "Erro: fonte obrigatória ausente: $source" >&2
    exit 1
  fi
done

mkdir -p "$BUILD_DIR"

# Reutiliza as fontes IBM Plex já embutidas no style guide, sem duplicar os
# binários base64 na folha de estilo do PDF.
FONT_FACES_FILE="$BUILD_DIR/fontfaces.css"
awk '
  /@font-face/ { p = 1 }
  /:root[ \t]*\{/ { exit }
  p { print }
' "$STYLE_GUIDE" > "$FONT_FACES_FILE"

if [ ! -s "$FONT_FACES_FILE" ]; then
  echo "Erro: não encontrei blocos @font-face em $STYLE_GUIDE." >&2
  exit 1
fi

FILLED_TEMPLATE="$BUILD_DIR/template.filled.html"
awk -v ff="$FONT_FACES_FILE" '
  $0 == "$fontfaces$" {
    while ((getline line < ff) > 0) print line
    close(ff)
    next
  }
  { print }
' "$TEMPLATE" > "$FILLED_TEMPLATE"

MESES=(janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro)
DAY="$(date +%-d)"
MONTH_NUM="$((10#$(date +%m)))"
YEAR="$(date +%Y)"
PT_DATE="$DAY de ${MESES[$((MONTH_NUM - 1))]} de $YEAR"

pandoc "$MD_SOURCE" \
  --from=markdown \
  --to=html5 \
  --standalone \
  --template="$FILLED_TEMPLATE" \
  --toc \
  --toc-depth=2 \
  --metadata title="Manual de Marca — Specsfy" \
  --metadata date="$PT_DATE" \
  --output "$OUT_HTML"

weasyprint \
  "$OUT_HTML" \
  "$OUT_PDF" \
  --base-url "$BRAND_ROOT/guide" \
  --stylesheet "$PDF_STYLE"

echo "OK: $OUT_PDF ($(du -h "$OUT_PDF" | cut -f1))"
