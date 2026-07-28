# Acessibilidade — Specsfy

Toda cor de marca é aprovada por número, não por olho. Esta página traz os
contrastes WCAG 2.1 reais (fórmula de luminância relativa, não estimativa) e
as decisões de design que vieram de calculá-los — inclusive uma correção
aplicada depois da paleta inicial ter sido definida.

## Método

Contraste calculado como `(L1 + 0.05) / (L2 + 0.05)`, onde `L` é a
luminância relativa de cada cor (fórmula WCAG 2.1, sRGB linearizado). Metas:

- **4.5:1** — mínimo AA para texto normal.
- **3:1** — mínimo AA para texto grande (≥18.66px bold ou ≥24px regular) e
  para objetos gráficos/componentes de UI (ícones, bordas de campo).

## Pares calculados

| Par | Contraste | Passa AA texto normal? | Onde é usado |
|---|---|---|---|
| Midnight Mirage `#001F3F` texto / Praxeti White `#F6F7ED` fundo | **15.3:1** | Sim | Texto de corpo, modo claro |
| Praxeti White `#F6F7ED` texto / Midnight Mirage `#001F3F` fundo | **15.3:1** | Sim | Texto de corpo, modo escuro |
| Nuit Blanche `#1E488F` / Praxeti White `#F6F7ED` | **8.2:1** | Sim | Links, modo claro |
| Nuit Blanche clareado `#5F7DAB` / Midnight Mirage `#001F3F` | **3.95:1** | Não (passa só texto grande/UI) | Links, modo escuro — **use apenas em texto ≥ 18px ou sublinhado + ícone, nunca em texto pequeno isolado** |
| Midnight Mirage / First Colors of Spring `#DBE64C` (chip) | **12.2:1** | Sim | Texto de chip "Draft" |
| Midnight Mirage / Mantis `#74C365` (chip) | **7.7:1** | Sim | Texto de chip "Verified", modo claro |
| Picture Book Green `#00804C` / Praxeti White `#F6F7ED` | **4.6:1** | Sim (por pouco) | Texto/ícone "verified", modo claro |
| Mantis `#74C365` / Midnight Mirage `#001F3F` | **7.7:1** | Sim | Texto/ícone "verified", modo escuro |
| Picture Book Green `#00804C` / Midnight Mirage `#001F3F` | **3.3:1** | **Não** | — por isso o token `verified` troca para Mantis no modo escuro; ver `colors/palette.md` |
| Vermelho `#B91C1C` / Praxeti White `#F6F7ED` | **6.0:1** | Sim | Texto/label do estado RED, modo claro |
| Vermelho `#F87171` / Midnight Mirage `#001F3F` | **6.0:1** | Sim | Texto/label do estado RED, modo escuro |

## Correção aplicada: o vermelho não era o `#DC2626` "óbvio"

A escolha inicial e mais comum para vermelho de status (`#DC2626`, usada por
Tailwind/Radix e a maioria dos design systems) dá **4.47:1** sobre Praxeti
White — abaixo do mínimo de 4.5:1 para texto normal, por uma margem pequena
mas real. Como o estado `RED` do TDD/BDD frequentemente aparece como texto
curto (`RED`, badges de status), a marca usa **`#B91C1C`** em vez disso:
mesma família de vermelho, reconhecível, e **6.0:1** — folga real, não só o
mínimo técnico.

## Daltonismo — o ícone `tdd-cycle.svg`

`icons/tdd-cycle.svg` é o único lugar da marca que depende de vermelho e
verde para transmitir dois estados opostos (RED vs. GREEN) — exatamente o
par que usuários com deuteranopia/protanopia (as formas mais comuns de
daltonismo, ~8% dos homens) têm mais dificuldade em distinguir.

**Regra:** este ícone nunca deve ser a única forma de indicar o estado RED
ou GREEN em uma interface real. Sempre acompanhe com texto (`RED`/`GREEN`),
posição (esquerda = RED, direita = GREEN — o ícone já reforça isso com
setas) ou um segundo canal (ex. ✕ vs ✓). Em documentação e apresentações
(o uso principal do ícone hoje) isso é menos crítico porque o texto ao redor
já desambigua, mas qualquer uso futuro em UI real deve seguir a regra acima.

**Lacuna relacionada — `evidence.svg`/`task.svg` em fundo escuro:** o
checkmark interno desses dois ícones é Picture Book Green `#00804C` fixo no
arquivo (sem variante `-dark`, ao contrário do logo). Sobre Midnight Mirage
esse verde cai para **3.3:1**, abaixo do mínimo de acessibilidade — o mesmo
problema que fez o token `verified` trocar para Mantis no modo escuro (ver
`colors/palette.md`). Até existir uma variante dedicada, quem usar esses
ícones sobre fundo escuro deve recolorir o checkmark para Mantis `#74C365`
manualmente antes de publicar. Ver `icons/icons.md`.

## Movimento

`brand/style-guide.html` usa `scroll-behavior: smooth` para navegação por
âncora. Isso respeita `prefers-reduced-motion: reduce` (rolagem instantânea
e transições/animações reduzidas a ~0 para quem configurou o sistema para
motion reduzido). Qualquer novo material da marca com scroll suave, hover
animado ou transição de página deve seguir a mesma regra — nunca assuma que
motion é neutro.

## Foco de teclado

Todo link e elemento interativo em material oficial da marca precisa de um
estado de foco visível (`:focus-visible`) com contraste mínimo 3:1 contra o
fundo adjacente — não confie apenas em `:hover`. Ver a implementação em
`style-guide.html` (outline em Nuit Blanche/Nuit Blanche clareado).

## Texto alternativo

Todo SVG de `logo/` e `icons/` já inclui `role="img"` e `aria-label`
descritivo. Ao reutilizar esses arquivos embutidos (`<img src="...svg">` ou
inline), preserve o `aria-label` ou forneça um `alt`/label equivalente — não
o remova ao copiar o markup.
