# Paleta de cores — Specsfy

O novo logo estabelece uma identidade primária **monocromática**. Preto e
branco constroem a marca; cores adicionais existem somente para função de
interface e nunca recolorem o logo.

## Cores de identidade

| Token | Hex | Uso |
| --- | --- | --- |
| **Black** | `#000000` | três camadas do logo, títulos e texto principal em superfícies claras |
| **White** | `#FFFFFF` | símbolo de código do logo, fundo seguro e texto principal em superfícies escuras |

Esses dois valores são imutáveis no ativo canônico. O logo não acompanha o
tema da interface: em fundo escuro, use uma placa branca.

## Neutros de interface

| Token | Claro | Escuro | Uso |
| --- | --- | --- | --- |
| `paper` | White `#FFFFFF` | Graphite `#171717` | fundo de página |
| `paper-elevated` | Fog `#F5F5F5` | `#262626` | cards e superfícies elevadas |
| `ink` | Black `#000000` | White `#FFFFFF` | texto principal |
| `ink-secondary` | Gray `#737373` | Gray `#A3A3A3` | texto secundário |
| `border` | `#D4D4D4` | `#404040` | divisores, grades e bordas |

Graphite, Fog e os cinzas são neutros operacionais. Não substituem o preto e o
branco do logo.

## Cores funcionais

| Estado | Claro | Escuro | Regra |
| --- | --- | --- | --- |
| `link` | `#1D4ED8` | `#93C5FD` | links e foco; sempre com sublinhado ou outro sinal além da cor |
| `verified` | `#047857` | `#6EE7B7` | `Passed`, `GREEN`, `VERIFIED` e evidência confirmada |
| `draft` | `#92400E` | `#FCD34D` | `Draft`, `Planned` e trabalho em andamento |
| `red` | `#B91C1C` | `#FCA5A5` | estado `RED`, falha e bloqueio |

Cores funcionais comunicam estado. Não são cores da assinatura institucional e
não entram em `brand/logo/icon.svg`.

## Contrastes aprovados

| Par | Contraste |
| --- | --- |
| Black `#000000` / White `#FFFFFF` | **21.00:1** |
| Graphite `#171717` / White `#FFFFFF` | **17.93:1** |
| Gray `#737373` / White `#FFFFFF` | **4.74:1** |
| Gray `#A3A3A3` / Graphite `#171717` | **7.11:1** |
| Link `#1D4ED8` / White | **6.70:1** |
| Link `#93C5FD` / Graphite | **9.94:1** |
| Verified `#047857` / White | **5.48:1** |
| Verified `#6EE7B7` / Graphite | **11.76:1** |
| Draft `#92400E` / White | **7.09:1** |
| Draft `#FCD34D` / Graphite | **12.43:1** |
| RED `#B91C1C` / White | **6.47:1** |
| RED `#FCA5A5` / Graphite | **9.45:1** |

## Regra de uso

- Use preto e branco para reconhecimento de marca e hierarquia principal.
- Use no máximo uma cor funcional dominante por bloco.
- Combine estado com texto, ícone ou posição; cor sozinha não é evidência.
- Não use cor funcional como decoração.
- Não aplique gradiente, textura ou transparência ao logo.
- Não crie nomes promocionais para os neutros: os tokens descrevem função.

As implementações normativas ficam em
[`tokens.css`](tokens.css) e [`tokens.json`](tokens.json). Atualize os três
arquivos juntos.
