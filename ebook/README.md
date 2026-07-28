# Ebook do guia do usuário

<p align="center">
  <picture>
    <source srcset="../brand/logo/icon.svg" type="image/svg+xml">
    <img src="../brand/logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>

Esta pasta publica o conteúdo completo de `docs/user/` em PDF e EPUB. Os
arquivos Markdown continuam sendo a única fonte editorial; não edite os
artefatos gerados.

## Edição vigente

A versão está em [`VERSION`](VERSION) e segue SemVer:

- `PATCH`: correção de texto, link, exemplo ou apresentação;
- `MINOR`: nova página, novo percurso ou ampliação material;
- `MAJOR`: reorganização incompatível da jornada ou do contrato editorial.

Os artefatos vigentes usam o padrão:

```text
Specsfy-Guia-do-Usuario-v<versão>.pdf
Specsfy-Guia-do-Usuario-v<versão>.epub
```

[`build.json`](build.json) registra a edição, a ordem, o digest das fontes e os
hashes dos dois arquivos. As tabelas `## Classificação` permanecem nas fontes
Markdown: o build extrai `Natureza`, `Escopo` e `Autoridade` para
`document_metadata` no manifesto, mas não as exibe no PDF nem no EPUB.

Nos artefatos portáteis, todo link clicável navega dentro do próprio ebook.
Referências externas continuam visíveis como texto, sem abrir o navegador ou
retirar a pessoa da leitura. O build também verifica se cada capítulo e âncora
interna referenciada realmente existe.

## Gerar

Na raiz do monorepo:

```bash
make ebook
```

O build exige que a [ordem pedagógica canônica](../docs/user/reading-order.txt)
inclua cada página Markdown de `docs/user/` exatamente uma vez. Imagens e
demais arquivos desse percurso entram automaticamente no digest.

## Regra de atualização

Toda alteração em `docs/user/`, inclusive imagens, exige:

1. ajustar `VERSION` conforme o impacto editorial;
2. atualizar
   [`docs/user/reading-order.txt`](../docs/user/reading-order.txt) se uma
   página foi criada, movida ou removida;
3. executar `make ebook`;
4. executar `make verify-ebook`.

A regressão da raiz também executa a verificação. Ela falha se o digest das
fontes ou os hashes do PDF e EPUB não coincidirem com `build.json`.
