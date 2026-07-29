# Tipografia — Specsfy

## Escolha

O Specsfy usa a família **IBM Plex** — não por acaso: foi desenhada para
contextos de engenharia, é aberta (SIL Open Font License 1.1, uso livre
comercial e de código) e já entrega uma dupla sans/mono desenhada para
conviver na mesma página. Isso resolve exatamente o par que o método precisa:
prosa legível para specs + monoespaçada para IDs, comandos e código.

| Papel | Família | Peso padrão |
|---|---|---|
| Títulos e UI | **IBM Plex Sans** | 600 (SemiBold) para títulos, 400/500 para corpo |
| Corpo de texto | **IBM Plex Sans** | 400 |
| Código, IDs, comandos, estados | **IBM Plex Mono** | 400, 500 para ênfase |

Não use uma terceira família. Se precisar de um tom mais "editorial" para
citações longas de spec, use itálico de IBM Plex Sans — não introduza serifa.

## Por que monoespaçada é parte da marca, não um detalhe técnico

O método já usa monoespaço implicitamente sempre que cita `US-01`, `RQ-04`,
`Gate: Passed`, `spec.md`, nomes de skill como `specsfy-04-validate`. Tratar isso
como tipografia de marca (não como "formatação de markdown") reforça a ideia
central: **rastreabilidade é literal, não estilística**. Sempre que um ID,
estado, caminho de arquivo ou comando aparecer em uma peça de marca, use
IBM Plex Mono.

## Stack CSS (com fallback do sistema)

```css
:root {
  --specsfy-font-sans: "IBM Plex Sans", "Inter", -apple-system,
    "Segoe UI", Roboto, sans-serif;
  --specsfy-font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas,
    "Liberation Mono", Menlo, monospace;
}
```

## Escala hierárquica

| Nível | Tamanho / line-height | Peso | Família | Uso |
|---|---|---|---|---|
| Display | 40px / 48px | 600 | Sans | Capas, título de apresentação |
| H1 | 32px / 40px | 600 | Sans | Título de página/documento |
| H2 | 24px / 32px | 600 | Sans | Seções (ex.: "Ato I — Definir") |
| H3 | 18px / 28px | 600 | Sans | Subseções |
| Corpo | 16px / 26px | 400 | Sans | Texto corrido |
| Legenda | 13px / 18px | 400 | Sans | Notas, metadados |
| Código inline | 0.9em | 400 | Mono | `spec.md`, `US-01`, `Gate: Passed` |
| Bloco de código | 14px / 22px | 400 | Mono | Comandos, trechos de Gherkin/teste |

## Regras de uso

- Títulos sempre em `ink-950` ou `ink-900` — nunca em cor de acento (verde,
  âmbar, vermelho) fora de badges de estado.
- Não use mais de 3 pesos na mesma peça (ex.: 400 corpo + 500 ênfase + 600
  título).
- Tracking (letter-spacing) neutro no corpo; pode abrir levemente (+2%) em
  títulos grandes (Display/H1) para leitura em telas.
- Em código/mono, nunca aplique itálico — quebra a leitura de IDs.

## Licenciamento

IBM Plex Sans e IBM Plex Mono são distribuídas sob **SIL Open Font License
1.1**: uso livre em produtos comerciais, sem exigência de atribuição visível.
Fontes disponíveis em Google Fonts e no repositório oficial da IBM
(`github.com/IBM/plex`).
