# Ícones — Specsfy

## Ícone do framework

`icon.svg` e `icon.png` são as duas representações canônicas do ícone do
framework Specsfy. O símbolo mostra três placas empilhadas, com a placa superior
marcada por um par de chevrons e uma barra de código.

| Arquivo | Uso |
|---|---|
| [`icon.svg`](icon.svg) | Fonte vetorial preferencial para README, documentação, interfaces e materiais escaláveis. |
| [`icon.png`](icon.png) | Fallback raster RGBA de 512×512 para consumidores que não aceitam SVG. |

Use o SVG como primeira opção e o PNG como fallback do mesmo conteúdo, sempre
com texto alternativo `Ícone do framework Specsfy`. Esses arquivos identificam
o framework e seus repositórios; não substituem os lockups institucionais de
`../logo/` e não entram na contagem dos ícones conceituais abaixo. Não altere
cores, geometria ou proporção em uma cópia local: referencie a versão publicada
por `brand/`.

## Ícones conceituais

Conjunto conceitual de 8 ícones que representam os elementos centrais do
método. Feitos para documentação, apresentações e futuras interfaces — não
para substituir o símbolo da marca (`../logo/mark.svg`), que é único e não
deve ser remixado.

## Especificação técnica

- Grid: `viewBox 0 0 32 32`.
- Estilo: **flat** — formas sólidas preenchidas (`fill`), sem `stroke`. Sem
  gradiente, sombra ou efeito 3D.
- Cantos levemente arredondados nas barras/hastes (`rx` pequeno); demais
  contornos retos e geométricos.
- Detalhes internos (linhas de texto, moldura de checkbox, corte do canto
  dobrado) são recortes vazados no preenchimento — via `fill-rule="evenodd"`
  — não formas desenhadas por cima. Isso mantém cada ícone como uma única
  cor sólida (mais o fundo aparecendo através do vazado), verdadeiramente
  flat/monocromático.
- Cor: a maioria usa `fill="currentColor"` — herdam a cor do texto ao redor
  via CSS (`color: var(--specsfy-ink)` etc). **Duas exceções documentadas**,
  porque a cor faz parte do significado, não é decoração:
  - `tdd-cycle.svg` — metade vermelha (`#B91C1C`), metade verde (Picture Book
    Green `#00804C`). Representa literalmente o ciclo RED → GREEN; recolorir
    destrói o significado. (Vermelho é `#B91C1C`, não o `#DC2626` mais comum
    — é o tom que passa 4.5:1 sobre Praxeti White, ver `../accessibility.md`.)
  - `evidence.svg` e `task.svg` (checkmarks internos) — o restante do ícone é
    um anel/moldura vazada (não um disco sólido), para que o checkmark sempre
    apareça contra o fundo da página, não contra uma forma preenchida. O
    checkmark é sempre Picture Book Green `#00804C` em fundo claro, igual à
    regra do logo. Em superfícies escuras, troque para Mantis `#74C365`
    (mesma regra do logo).

**Lacuna conhecida:** ao contrário do logo (que tem arquivos `logo-light.svg`/
`logo-dark.svg` separados), `evidence.svg` e `task.svg` só existem como um
único arquivo com `#00804C` fixo — não há uma variante `-dark` pronta. Picture
Book Green sobre Midnight Mirage cai para **3.3:1**, abaixo do mínimo de
acessibilidade (ver `../accessibility.md`). Hoje isso é aceitável porque o uso
predominante é documentação sobre fundo claro; qualquer uso real sobre fundo
escuro deve recolorir o checkmark manualmente para Mantis `#74C365` antes de
publicar — não usar o arquivo como está. O mesmo vale para `tdd-cycle.svg`,
que já documenta essa exceção separadamente (ver `../accessibility.md`).

## Inventário

| Arquivo | Representa | Onde usar |
|---|---|---|
| `spec.svg` | O `spec.md`, fonte única de verdade | Cabeçalho de seções sobre especificação, links para specs |
| `gherkin.svg` | BDD / cenários Gherkin (Given-When-Then) | Documentação de aceite, exemplos de `.feature` |
| `tdd-cycle.svg` | O ciclo RED → GREEN do TDD | Explicações do Ato II, badges de status de teste |
| `gate.svg` | Um gate (Definition/Plan/Delivery) | Indicar checkpoints, "Gate: Passed" |
| `evidence.svg` | Evidência registrada/verificada | Seções de evidência, changelogs de verificação |
| `task.svg` | Tarefas e o ciclo READY→RED→GREEN→VERIFIED→DONE | Backlogs, listas de tarefas |
| `acts.svg` | Os três Atos rígidos em progressão | Diagramas de processo, onboarding |
| `traceability.svg` | IDs ligando história→requisito→cenário→teste→tarefa | Matriz de rastreabilidade, explicações de IDs |

## Não fazer

- Não usar dois ícones diferentes para o mesmo conceito no mesmo documento.
- Não colorir `spec.svg`, `gherkin.svg`, `gate.svg`, `task.svg`, `acts.svg`
  ou `traceability.svg` com verde/vermelho/First Colors of Spring — eles são
  neutros (`currentColor`, tipicamente Midnight Mirage ou Praxeti White).
- Não redesenhar os checkmarks internos em cor diferente de Picture Book
  Green (claro) / Mantis (escuro).
- Não misturar este conjunto com ícones de bibliotecas externas (Feather,
  Lucide, Font Awesome) na mesma peça — o estilo flat e o grid não batem
  com conjuntos de traço/outline.
- Não adicionar `stroke`/contorno às formas preenchidas — o conjunto é
  monocromático por preenchimento, não por linha.
