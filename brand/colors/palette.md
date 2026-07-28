# Paleta de cores — Specsfy

A paleta é composta por seis cores nomeadas (extraídas do moodboard de
referência da marca) mais uma cor funcional que não pertence à identidade
visual, mas ao próprio vocabulário do método.

A lógica semântica original do Specsfy continua valendo: **verde só aparece
quando algo foi verificado** (gate aprovado, teste `GREEN`, evidência
registrada) — nunca como decoração. O que muda aqui são os tons exatos.

## Cores primitivas (paleta nomeada)

| Nome | Hex | Papel na marca |
|---|---|---|
| **Midnight Mirage** | `#001F3F` | Cor primária. Logo, títulos, texto principal, fundo do modo escuro. |
| **Nuit Blanche** | `#1E488F` | Cor secundária. Links, elementos interativos, acentos de destaque. |
| **Picture Book Green** | `#00804C` | Verde de verificação — gate `Passed`, teste `GREEN`, evidência, em fundos claros. |
| **Mantis** | `#74C365` | Verde de verificação em fundos escuros; tint de fundo para badges "Verified" em fundos claros. |
| **First Colors of Spring** | `#DBE64C` | Sinalização de `Draft`/`Implementing` (substitui o âmbar do sistema anterior). Uso em chips/badges, nunca em texto corrido. |
| **Praxeti White** | `#F6F7ED` | Papel. Fundo padrão em modo claro, texto principal em modo escuro. |

## Cor funcional (fora da paleta nomeada)

| Token | Hex | Uso |
|---|---|---|
| `red-600` | `#B91C1C` (modo claro) / `#F87171` (modo escuro) | Exclusivamente para representar o estado `RED` do TDD/BDD — teste falhando por design, antes do código. Não faz parte do moodboard; é vermelho universal de status, mantido por convenção de acessibilidade (vermelho = falha é reconhecido independente de marca). `#B91C1C` (não o `#DC2626` mais comum) porque é o tom mais próximo que ainda passa 4.5:1 sobre Praxeti White — ver `accessibility.md`. |
| `paper-elevated` | `#FFFFFF` (modo claro) / `#06274F` (modo escuro) | Fundo de superfícies elevadas (cards, popovers) sobre `paper`. Não é uma sétima cor de acento — é um degrau de neutro acima/abaixo de Praxeti White e Midnight Mirage, usado só para dar profundidade a superfícies empilhadas, nunca como cor de texto, ícone, badge ou destaque. `style-guide.html` já usa este token (`--bg-elevated`); ele estava implementado sem estar documentado aqui — corrigido nesta revisão. |

## Regra de ouro (inalterada)

> Verde só aparece quando algo foi provado. First Colors of Spring só aparece
> em chips de estado "em andamento". Vermelho só aparece no estado `RED`.
> Nenhuma dessas três é decoração.

## Tokens semânticos

Os tokens semânticos mudam de valor entre modo claro e escuro; os tokens
primitivos (tabela acima) **nunca mudam** — são as cores nomeadas fixas.

| Token semântico | Modo claro | Modo escuro | Papel |
|---|---|---|---|
| `paper` | Praxeti White `#F6F7ED` | Midnight Mirage `#001F3F` | Fundo de página |
| `ink` | Midnight Mirage `#001F3F` | Praxeti White `#F6F7ED` | Texto principal, logo |
| `ink-secondary` | Midnight Mirage 62% opacidade | Praxeti White 65% opacidade | Texto secundário, legendas |
| `border` | Midnight Mirage 14% opacidade | Praxeti White 16% opacidade | Bordas, grades |
| `link` | Nuit Blanche `#1E488F` | Nuit Blanche clareado ~`#5F7DAB` | Links, interativos |
| `verified` | Picture Book Green `#00804C` | Mantis `#74C365` | Gate Passed, GREEN, evidência |
| `verified-tint` | Mantis `#74C365` (fundo de badge) | Picture Book Green 22% opacidade | Fundo de badges "Verified" |
| `draft` | First Colors of Spring `#DBE64C` (chip) | First Colors of Spring `#DBE64C` (chip) | Badge de Draft/Implementing — chip mantém o mesmo tom nos dois modos, com texto `Midnight Mirage` sempre por cima |
| `red` | `#B91C1C` | `#F87171` | Estado RED (ver cor funcional) |
| `paper-elevated` | `#FFFFFF` | Midnight Mirage 14% mais claro `#06274F` | Fundo de cards/superfícies elevadas sobre `paper` — nunca cor de texto ou de destaque |

Por que `verified` troca de Picture Book Green para Mantis no modo escuro:
Picture Book Green sobre o fundo Midnight Mirage do modo escuro cai abaixo de
contraste legível (verde escuro sobre azul-marinho quase preto). Mantis, mais
claro, resolve isso sem inventar uma cor fora da paleta nomeada.

## Pares de contraste aprovados (WCAG AA, texto normal)

- `ink` (Midnight Mirage) sobre `paper` (Praxeti White) — texto de corpo padrão, modo claro. **15.3:1**
- `ink` (Praxeti White) sobre `paper` (Midnight Mirage) — texto de corpo padrão, modo escuro. **15.3:1**
- Midnight Mirage sobre First Colors of Spring ou Mantis — texto de badges/chips (nunca o inverso: essas duas cores claras não servem como cor de texto). **12.2:1 / 7.7:1**
- Nuit Blanche sobre Praxeti White — links e texto curto interativo. **8.2:1**
- `red-600` (`#B91C1C`) sobre Praxeti White — texto/label do estado RED. **6.0:1**

Nunca escreva parágrafos longos em Nuit Blanche, Picture Book Green, Mantis
ou First Colors of Spring — são cores de acento e chip, não de leitura
longa. Razões completas e todos os pares calculados (incluindo os que
falham e por quê) estão em [`../accessibility.md`](../accessibility.md).

## Não fazer

- Não usar First Colors of Spring como cor de texto — é clara demais; use
  apenas como fundo de chip com texto Midnight Mirage por cima.
- Não usar Mantis nem Picture Book Green fora do sentido "verificado".
- Não introduzir um sétimo tom de acento além dos seis nomeados + vermelho
  funcional.
- Não usar gradientes entre as cores da paleta.
