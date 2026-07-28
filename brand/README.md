# brand/ — Manual de marca Specsfy

<p align="center">
  <picture>
    <source srcset="icons/icon.svg" type="image/svg+xml">
    <img src="icons/icon.png" alt="Ícone do framework Specsfy" width="128">
  </picture>
</p>

Este arquivo é o manual completo da marca Specsfy: posicionamento, voz e tom,
cor, tipografia, logo, ícones e acessibilidade, todos por extenso em um único
lugar. Ele existe para ser lido do início ao fim por um agente ou uma pessoa
que precisa produzir qualquer material com o nome, o símbolo ou a voz do
Specsfy sem precisar abrir sete arquivos diferentes.

O guia completo também é publicado como
[`Specsfy-Manual-de-Marca.pdf`](Specsfy-Manual-de-Marca.pdf) neste módulo. O
gerador, o comando `make brand-guide` e a folha `.pdf/style.css` pertencem à
raiz do [`monorepo`](https://github.com/promovaweb/specsfy); `brand/` mantém a
fonte editorial, o template visual e o PDF publicado.

Cada seção também tem uma **fonte normativa** própria — o arquivo específico
onde aquele valor exato (hex, geometria de SVG, CSS, JSON) é definido e
versionado. Este manual resume e explica; a fonte normativa é o valor
verdadeiro caso um número aqui e um número lá algum dia divirjam. A tabela
completa de fontes normativas está na seção [12. Mapa de arquivos](#12-mapa-de-arquivos).
Ver [Regra de manutenção](#13-regra-de-manutenção) para como editar sem
quebrar essa relação.

## Sumário

1. [Posicionamento](#1-posicionamento)
2. [Tagline e elevator pitches](#2-tagline-e-elevator-pitches)
3. [Personalidade da marca](#3-personalidade-da-marca)
4. [Voz e tom](#4-voz-e-tom)
5. [Cor](#5-cor)
6. [Tipografia](#6-tipografia)
7. [Logo](#7-logo)
8. [Ícones](#8-ícones)
9. [Acessibilidade](#9-acessibilidade)
10. [Do's e Don'ts gerais (cross-asset)](#10-dos-e-donts-gerais-cross-asset)
11. [Brand Gate — checklist de publicação](#11-brand-gate--checklist-de-publicação)
12. [Mapa de arquivos](#12-mapa-de-arquivos)
13. [Regra de manutenção](#13-regra-de-manutenção)

---

## 1. Posicionamento

Specsfy é uma metodologia — não uma ferramenta, não um framework de código —
para escrever software a partir de uma especificação única, executável e
rastreável, aplicando três atos rígidos (Definir, Projetar e provar, Entregar
e validar) com gates que só passam mediante evidência real.

O território que o Specsfy ocupa não é "documentação de software" nem
"metodologia ágil genérica". É o espaço específico entre **intenção** e
**código provado**: a distância que normalmente se perde em specs que
divergem do plano, planos que divergem das tarefas, e tarefas marcadas como
prontas sem teste que comprove isso.

**O que o Specsfy não é** (para guiar a linguagem em qualquer material):

- Não é um gerador de documentação — não fale em "gerar specs
  automaticamente" como benefício central.
- Não é uma metodologia ágil concorrente do Scrum/Kanban — não a compare
  diretamente com esses frameworks; ela opera em outro nível (o que entra
  numa fatia de trabalho, não como o time se organiza no tempo).
- Não é exclusiva para desenvolvimento assistido por IA, embora funcione
  particularmente bem nesse contexto — o método serve tanto para trabalho
  humano quanto para agentes.

## 2. Tagline e elevator pitches

**Tagline principal** (a única que deve aparecer ao lado do logo em materiais
oficiais):

> Especifique. Prove. Entregue.

Três verbos, um por Ato — a tagline literalmente espelha a estrutura do
método.

**Alternativas** (para contextos onde a tagline principal já apareceu perto,
ou para variar em títulos de seção):

- "Uma especificação. Rastreável até o código."
- "Nenhum 'pronto' sem evidência."

**Curto** (uma frase, para bios/perfis):

> Specsfy é uma metodologia para escrever software a partir de uma
> especificação única, testada antes do código e concluída só com evidência.

**Médio** (para README, apresentações):

> Specsfy organiza cada fatia de trabalho em três atos: definir com clareza o
> que precisa existir, projetar e provar os testes antes da implementação, e
> entregar com evidência verificável. Uma única fonte normativa por fatia
> (`spec.md`) elimina a divergência entre spec, plano e tarefas — e nenhum
> gate avança sem RED registrado antes do código ou prova depois dele.

**Longo** (para artigos, onboarding):

> A maioria dos processos de especificação falha silenciosamente: a spec diz
> uma coisa, o plano assume outra, as tarefas são marcadas como concluídas
> sem verificação, e o "pronto" vira uma palavra vazia. Specsfy parte de seis
> compromissos — fonte única, descoberta antes da solução, BDD como aceite,
> TDD antes da implementação, trabalho rastreável por IDs compartilhados, e
> conclusão só por evidência — e os aplica em três atos rígidos com entrada,
> saída, gate e handoff próprios. O resultado não é mais documentação: é
> menos distância entre o que o usuário quis, o comportamento aceito, os
> testes que provam esse comportamento, e o código que efetivamente existe.

## 3. Personalidade da marca

**Flat / estrutural.** O Specsfy se parece com um desenho técnico, não com
um produto de consumo: formas sólidas preenchidas (sem traço/contorno),
grid explícito, cor usada com função (não decoração), tipografia que assume
um par sans + mono como parte da identidade, não como escolha de "modo
código".

Três adjetivos que resumem a personalidade:

1. **Rigoroso** — nada é decorativo só por estética; toda forma carrega
   significado (o checkmark é sempre verificação, o verde é sempre "provado").
2. **Rastreável** — a mesma lógica de IDs e handoffs do método aparece na
   marca: cores emprestadas dos estados (`RED`, `Draft`), tipografia mono
   para IDs, ícones que remetem a conceitos específicos do método.
3. **Sóbrio** — sem gradientes, sombras, ilustração decorativa ou linguagem
   promocional. A marca não precisa convencer com efeito visual; precisa
   comunicar precisão.

## 4. Voz e tom

| Traço | Como soa | Como não soa |
|---|---|---|
| **Preciso** | "O Gate não passa sem RED registrado nos dois níveis." | "O Gate normalmente exige que os testes estejam ok." |
| **Direto** | "Não crie `plan.md` paralelo." | "Recomendamos fortemente evitar arquivos adicionais quando possível." |
| **Sem hype** | "Reduz a distância entre intenção e código." | "Revolucione sua forma de desenvolver software!" |
| **Rigoroso, não burocrático** | "Cada gate é um compromisso, não uma categoria editorial." | "Preencha o checklist de 40 itens antes de prosseguir." |

**Regras práticas:**

- Frases curtas e verbos no imperativo quando se trata de instrução
  ("escreva", "prove", "registre") — nunca "você deveria considerar".
- Nunca prometa o que o método não garante. O Specsfy não promete "menos
  bugs" ou "mais velocidade" — promete rastreabilidade e evidência. Deixe o
  leitor tirar a conclusão de que isso reduz bugs, não afirme por ele.
- Números e siglas do método (`US-01`, `RQ-04`, `Gate: Passed`, `RED`,
  `GREEN`) sempre em `monoespaçada` (ver [Tipografia](#6-tipografia)) — nunca
  parafraseados ("o requisito quatro").
- Não use metáforas de guerra ("batalha contra bugs"), esporte
  ("touchdown") ou motivação corporativa genérica ("sinergia",
  "empoderar"). O campo semântico correto é **engenharia e prova**: gate,
  evidência, rastro, estado, transição.

### Por que um glossário existe

O método inteiro depende de IDs e nomes de estado que não podem ter
sinônimo — `US-01` não pode virar "a primeira história" em um documento e
continuar `US-01` em outro, ou a rastreabilidade que é a proposta central do
Specsfy quebra silenciosamente. A voz da marca aplica a mesma disciplina à
prosa: um termo, uma grafia, sempre.

### Glossário de termos canônicos

| Termo | Grafia fixa | Nunca escreva | Nota |
|---|---|---|---|
| Gate | `Gate` (maiúsculo, en) | "portão", "checkpoint", "milestone" | Sempre com o nome completo: `Definition Gate`, `Plan Gate`, `Delivery Gate`. |
| Ato | Ato I / Ato II / Ato III | "fase", "etapa", "sprint", "estágio" | Numeração romana, sempre. |
| spec.md | `spec.md` (mono) | "a especificação" isolado quando se refere ao arquivo | "a especificação" é aceitável quando fala do conceito, não do arquivo. |
| RED / GREEN | `RED` / `GREEN` (mono, maiúsculo) | "vermelho"/"verde" quando se refere ao estado do teste | "vermelho"/"verde" só valem falando de cor, nunca do estado TDD. |
| Estado canônico | `Draft → Defined → Planned → Implementing → Complete` | reordenar, renomear ou abreviar os estados | É uma sequência fixa, não uma lista de exemplos. |
| Ciclo de tarefa | `READY → RED → GREEN → VERIFIED → DONE` | pular etapas na descrição ("de READY direto pra DONE") | Mesmo em prosa corrida, cite a cadeia completa na primeira menção. |
| Handoff | `handoff` | "entrega" (confunde com Ato III — Entregar) | Handoff = transição verificável entre atos; entrega = o ato inteiro. |
| Evidência | `evidência` | "prova" como substantivo solto | "provar"/"prova" como verbo/ação é ok ("provar o teste"); "evidência" é o registro. |
| IDs (`US-01`, `RQ-04`, `CN-02`) | mono, formato `PREFIXO-NN` | escrever por extenso ("história de usuário um") | Sempre cite o ID mesmo quando parafrasear o conteúdo. |

### Exemplos por canal

**Commit message:**

```
fix: corrige contraste do vermelho semântico (RED) para AA

DC2626 dava 4.47:1 sobre Praxeti White, abaixo do mínimo de texto.
Troca para B91C1C (6.0:1). Ver brand/accessibility.md.
```

Direto, técnico, sem "melhorias" vagas — diz o número, diz a causa.

**Mensagem de validação/erro** (ex.: `validate_spec.py`):

```
Definition Gate: Failed
US-03 não tem cenário BDD associado — adicione um Scenario em spec.md
antes de marcar este Gate como Passed.
```

Diz o que falhou, onde, e a ação exata para resolver. Nunca "algo deu
errado" ou "verifique sua configuração".

**Título de seção de documentação:**

> Certo: "Ato II — Projetar e provar"
> Errado: "Fase de Planejamento 🚀"

Sem emoji como marcador de seção, sem hype no título de algo que já é
estrutural.

**Resposta de um agente conversando com o usuário** (ex.: `specsfy-base-interview`):

> "US-04 depende de um comportamento que ainda não está confirmado: o que
> acontece se o usuário cancelar no meio da importação? Isso muda o
> cenário BDD que vou escrever a seguir."

Uma pergunta por vez, nomeando o ID afetado, explicando a consequência —
não "me conte mais sobre seus requisitos" genérico.

**Post/anúncio** (uso raro, mas se existir):

> "Specsfy: uma especificação, rastreável até o código. Sem plan.md
> paralelo, sem 'pronto' sem evidência."

Ainda factual — vende pelo mecanismo, não pelo adjetivo.

### Nunca dizer

- **"Simplesmente"** antes de qualquer instrução — minimiza esforço real do
  leitor e geralmente esconde um passo faltando.
- **Emoji como marcador de seção ou de status** (✅/🚀/🔥 no lugar de
  `Gate: Passed`) — o método já tem um vocabulário de estado; emoji o
  duplica informalmente.
- **"Nosso/nossa IA"** referindo-se genericamente ao agente — nomeie a
  skill (`specsfy-base-interview`, `specsfy-base-validate`) quando o contexto permite;
  é mais preciso e mais rastreável, coerente com o resto da marca.
- **Desculpas performáticas em mensagem de erro** ("Ops! Algo deu errado 😅")
  — diga o que falhou e como corrigir, sem tom.
- **Voz passiva para esconder responsabilidade** ("o Gate não foi
  aprovado" sem dizer por quê) — sempre nomeie a causa verificável.

### Idioma

Português é o idioma primário de prosa (specs, guidelines, conversas). Os
identificadores literais do sistema — nomes de estado, arquivos, siglas,
nomes de Gate — permanecem em inglês e mono porque são *tokens*, não texto:
traduzi-los quebraria a busca por texto e a rastreabilidade entre
documentos. A regra de bolso: se aparece em um `grep` do repositório para
rastrear algo, não traduza; se é explicação ao redor, português.

## 5. Cor

A paleta é composta por seis cores nomeadas (extraídas do moodboard de
referência da marca) mais duas cores funcionais que não pertencem à
identidade visual em si, mas resolvem um papel específico: uma emprestada do
vocabulário do método (`RED`), outra de elevação de superfície neutra.

**Regra de ouro:**

> Verde só aparece quando algo foi provado. First Colors of Spring só aparece
> em chips de estado "em andamento". Vermelho só aparece no estado `RED`.
> Nenhuma dessas três é decoração.

### Paleta nomeada (primitivos)

| Nome | Hex | Papel na marca |
|---|---|---|
| **Midnight Mirage** | `#001F3F` | Cor primária. Logo, títulos, texto principal, fundo do modo escuro. |
| **Nuit Blanche** | `#1E488F` | Cor secundária. Links, elementos interativos, acentos de destaque. |
| **Picture Book Green** | `#00804C` | Verde de verificação — gate `Passed`, teste `GREEN`, evidência, em fundos claros. |
| **Mantis** | `#74C365` | Verde de verificação em fundos escuros; tint de fundo para badges "Verified" em fundos claros. |
| **First Colors of Spring** | `#DBE64C` | Sinalização de `Draft`/`Implementing` (substitui o âmbar do sistema anterior). Uso em chips/badges, nunca em texto corrido. |
| **Praxeti White** | `#F6F7ED` | Papel. Fundo padrão em modo claro, texto principal em modo escuro. |

Os tokens primitivos **nunca mudam** — são as cores nomeadas fixas,
independentes de modo claro/escuro.

### Cores funcionais (fora da paleta nomeada)

| Token | Hex | Uso |
|---|---|---|
| `red-600` | `#B91C1C` (modo claro) / `#F87171` (modo escuro) | Exclusivamente para representar o estado `RED` do TDD/BDD — teste falhando por design, antes do código. Não faz parte do moodboard; é vermelho universal de status, mantido por convenção de acessibilidade. `#B91C1C` (não o `#DC2626` mais comum) porque é o tom mais próximo que ainda passa 4.5:1 sobre Praxeti White — ver [Acessibilidade](#9-acessibilidade). |
| `paper-elevated` | `#FFFFFF` (modo claro) / `#06274F` (modo escuro) | Fundo de superfícies elevadas (cards, popovers) sobre `paper`. Não é uma sétima cor de acento — é um degrau de neutro para dar profundidade a superfícies empilhadas, nunca cor de texto, ícone, badge ou destaque. Já era usado em `style-guide.html` (`--bg-elevated`) sem estar documentado; formalizado nesta revisão. |

### Tokens semânticos

Os tokens semânticos trocam de valor entre modo claro e escuro.

| Token semântico | Modo claro | Modo escuro | Papel |
|---|---|---|---|
| `paper` | Praxeti White `#F6F7ED` | Midnight Mirage `#001F3F` | Fundo de página |
| `paper-elevated` | `#FFFFFF` | `#06274F` | Fundo de cards/superfícies elevadas sobre `paper` |
| `ink` | Midnight Mirage `#001F3F` | Praxeti White `#F6F7ED` | Texto principal, logo |
| `ink-secondary` | Midnight Mirage 62% opacidade | Praxeti White 65% opacidade | Texto secundário, legendas |
| `border` | Midnight Mirage 14% opacidade | Praxeti White 16% opacidade | Bordas, grades |
| `link` | Nuit Blanche `#1E488F` | Nuit Blanche clareado ~`#5F7DAB` | Links, interativos |
| `verified` | Picture Book Green `#00804C` | Mantis `#74C365` | Gate Passed, GREEN, evidência |
| `verified-tint` | Mantis `#74C365` (fundo de badge) | Picture Book Green 22% opacidade | Fundo de badges "Verified" |
| `draft` | First Colors of Spring `#DBE64C` (chip) | First Colors of Spring `#DBE64C` (chip) | Badge de Draft/Implementing — chip mantém o mesmo tom nos dois modos, texto `Midnight Mirage` sempre por cima |
| `red` | `#B91C1C` | `#F87171` | Estado RED |

Por que `verified` troca de Picture Book Green para Mantis no modo escuro:
Picture Book Green sobre o fundo Midnight Mirage do modo escuro cai abaixo de
contraste legível (verde escuro sobre azul-marinho quase preto — **3.3:1**).
Mantis, mais claro, resolve isso sem inventar uma cor fora da paleta nomeada.

### Pares de contraste aprovados (WCAG AA, texto normal)

- `ink` (Midnight Mirage) sobre `paper` (Praxeti White) — texto de corpo padrão, modo claro. **15.3:1**
- `ink` (Praxeti White) sobre `paper` (Midnight Mirage) — texto de corpo padrão, modo escuro. **15.3:1**
- Midnight Mirage sobre First Colors of Spring ou Mantis — texto de badges/chips (nunca o inverso: essas duas cores claras não servem como cor de texto). **12.2:1 / 7.7:1**
- Nuit Blanche sobre Praxeti White — links e texto curto interativo. **8.2:1**
- `red-600` (`#B91C1C`) sobre Praxeti White — texto/label do estado RED. **6.0:1**

Nunca escreva parágrafos longos em Nuit Blanche, Picture Book Green, Mantis
ou First Colors of Spring — são cores de acento e chip, não de leitura
longa. Tabela completa de pares calculados (incluindo os que falham e por
quê) na seção [Acessibilidade](#9-acessibilidade).

### Não fazer (cor)

- Não usar First Colors of Spring como cor de texto — é clara demais; use
  apenas como fundo de chip com texto Midnight Mirage por cima.
- Não usar Mantis nem Picture Book Green fora do sentido "verificado".
- Não introduzir um oitavo tom de acento além dos seis nomeados + vermelho
  funcional + `paper-elevated`.
- Não usar gradientes entre as cores da paleta.
- Não usar `paper-elevated` como cor de texto, ícone, badge ou destaque —
  é exclusivamente fundo de superfície.

### Tokens CSS

Fonte normativa: [`colors/tokens.css`](colors/tokens.css). Copie/`@import`
direto de lá; o bloco abaixo é para leitura.

```css
:root {
  /* Primitivos — paleta nomeada (fixos, não variam por tema) */
  --specsfy-midnight-mirage: #001F3F;
  --specsfy-nuit-blanche: #1E488F;
  --specsfy-picture-book-green: #00804C;
  --specsfy-mantis: #74C365;
  --specsfy-first-colors-of-spring: #DBE64C;
  --specsfy-praxeti-white: #F6F7ED;

  /* Funcional — fora da paleta nomeada, exclusivo do estado RED. */
  --specsfy-red: #B91C1C;

  /* Semânticos — modo claro (padrão) */
  --specsfy-paper: var(--specsfy-praxeti-white);
  --specsfy-paper-elevated: #FFFFFF;
  --specsfy-ink: var(--specsfy-midnight-mirage);
  --specsfy-ink-secondary: rgba(0, 31, 63, 0.62);
  --specsfy-border: rgba(0, 31, 63, 0.14);
  --specsfy-link: var(--specsfy-nuit-blanche);
  --specsfy-verified: var(--specsfy-picture-book-green);
  --specsfy-verified-tint: var(--specsfy-mantis);
  --specsfy-draft: var(--specsfy-first-colors-of-spring);
}

@media (prefers-color-scheme: dark) {
  :root {
    --specsfy-paper: var(--specsfy-midnight-mirage);
    --specsfy-paper-elevated: #06274F;
    --specsfy-ink: var(--specsfy-praxeti-white);
    --specsfy-ink-secondary: rgba(246, 247, 237, 0.65);
    --specsfy-border: rgba(246, 247, 237, 0.16);
    --specsfy-link: #5F7DAB;
    --specsfy-verified: var(--specsfy-mantis);
    --specsfy-verified-tint: rgba(0, 128, 76, 0.22);
    --specsfy-red: #F87171;
  }
}
```

`tokens.css` também define `:root[data-theme="dark"]` e
`:root[data-theme="light"]` equivalentes, para sites com toggle manual de
tema em vez de (ou além de) `prefers-color-scheme`.

### Tokens JSON

Fonte normativa: [`colors/tokens.json`](colors/tokens.json). Para design
tools (Figma, Style Dictionary) ou stacks que não usam CSS.

```json
{
  "name": "specsfy",
  "primitive": {
    "midnightMirage": { "value": "#001F3F" },
    "nuitBlanche": { "value": "#1E488F" },
    "pictureBookGreen": { "value": "#00804C" },
    "mantis": { "value": "#74C365" },
    "firstColorsOfSpring": { "value": "#DBE64C" },
    "praxetiWhite": { "value": "#F6F7ED" }
  },
  "functional": {
    "red": { "light": { "value": "#B91C1C" }, "dark": { "value": "#F87171" } },
    "paperElevated": { "light": { "value": "#FFFFFF" }, "dark": { "value": "#06274F" } }
  },
  "semantic": {
    "paper": { "light": "#F6F7ED", "dark": "#001F3F" },
    "paperElevated": { "light": "#FFFFFF", "dark": "#06274F" },
    "ink": { "light": "#001F3F", "dark": "#F6F7ED" },
    "inkSecondary": { "light": "rgba(0,31,63,0.62)", "dark": "rgba(246,247,237,0.65)" },
    "border": { "light": "rgba(0,31,63,0.14)", "dark": "rgba(246,247,237,0.16)" },
    "link": { "light": "#1E488F", "dark": "#5F7DAB" },
    "verified": { "light": "#00804C", "dark": "#74C365" },
    "verifiedTint": { "light": "#74C365", "dark": "rgba(0,128,76,0.22)" },
    "draft": { "light": "#DBE64C", "dark": "#DBE64C" },
    "red": { "light": "#B91C1C", "dark": "#F87171" }
  }
}
```

O JSON completo (com os campos `usage`/`note` por token) está em
[`colors/tokens.json`](colors/tokens.json) — o bloco acima omite esses
campos só para caber como referência de leitura.

## 6. Tipografia

O Specsfy usa a família **IBM Plex** — não por acaso: foi desenhada para
contextos de engenharia, é aberta (SIL Open Font License 1.1, uso livre
comercial e de código) e já entrega uma dupla sans/mono desenhada para
conviver na mesma página. Isso resolve exatamente o par que o método
precisa: prosa legível para specs + monoespaçada para IDs, comandos e código.

| Papel | Família | Peso padrão |
|---|---|---|
| Títulos e UI | **IBM Plex Sans** | 600 (SemiBold) para títulos, 400/500 para corpo |
| Corpo de texto | **IBM Plex Sans** | 400 |
| Código, IDs, comandos, estados | **IBM Plex Mono** | 400, 500 para ênfase |

Não use uma terceira família. Se precisar de um tom mais "editorial" para
citações longas de spec, use itálico de IBM Plex Sans — não introduza serifa.

### Por que monoespaçada é parte da marca, não um detalhe técnico

O método já usa monoespaço implicitamente sempre que cita `US-01`, `RQ-04`,
`Gate: Passed`, `spec.md`, nomes de skill como `specsfy-base-validate`. Tratar isso
como tipografia de marca (não como "formatação de markdown") reforça a ideia
central: **rastreabilidade é literal, não estilística**. Sempre que um ID,
estado, caminho de arquivo ou comando aparecer em uma peça de marca, use
IBM Plex Mono.

### Stack CSS (com fallback do sistema)

```css
:root {
  --specsfy-font-sans: "IBM Plex Sans", "Inter", -apple-system,
    "Segoe UI", Roboto, sans-serif;
  --specsfy-font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas,
    "Liberation Mono", Menlo, monospace;
}
```

### Escala hierárquica

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

### Regras de uso (tipografia)

- Títulos sempre em `ink-950` ou `ink-900` — nunca em cor de acento (verde,
  âmbar, vermelho) fora de badges de estado.
- Não use mais de 3 pesos na mesma peça (ex.: 400 corpo + 500 ênfase + 600
  título).
- Tracking (letter-spacing) neutro no corpo; pode abrir levemente (+2%) em
  títulos grandes (Display/H1) para leitura em telas.
- Em código/mono, nunca aplique itálico — quebra a leitura de IDs.

### Licenciamento

IBM Plex Sans e IBM Plex Mono são distribuídas sob **SIL Open Font License
1.1**: uso livre em produtos comerciais, sem exigência de atribuição visível.
Fontes disponíveis em Google Fonts e no repositório oficial da IBM
(`github.com/IBM/plex`).

## 7. Logo

### Conceito

O símbolo combina três ideias do método em uma única forma:

1. **Documento com canto dobrado** — o `spec.md`, fonte única de verdade.
2. **Checkmark verde** — nada avança sem evidência; verde é reservado para o
   que foi verificado.
3. **Três marcas na base** — os três Atos rígidos (Definir, Projetar e
   provar, Entregar e validar).

O estilo é **flat**: formas sólidas preenchidas, sem traço/contorno. O
documento é uma silhueta preenchida (canto dobrado recortado como vazado,
não desenhado por cima); o checkmark vive dentro de um badge circular
preenchido. Sem gradiente, sombra ou efeito 3D em nenhuma parte. As três
ideias juntas são o que torna o símbolo específico do Specsfy — nunca use
apenas uma delas isoladamente.

### Arquivos

| Arquivo | Uso |
|---|---|
| [`logo/mark.svg`](logo/mark.svg) | Símbolo isolado, colorido, fundo transparente. Avatar, ícone de app, redes sociais. |
| [`logo/favicon.svg`](logo/favicon.svg) | Símbolo com fundo sólido Midnight Mirage, documento preenchido Praxeti White. Otimizado para tamanhos pequenos (16–32px). |
| [`logo/logo-light.svg`](logo/logo-light.svg) | Símbolo + wordmark "Specsfy" em Midnight Mirage. Para fundos claros (Praxeti White). |
| [`logo/logo-dark.svg`](logo/logo-dark.svg) | Símbolo + wordmark em Praxeti White. Para fundos escuros (Midnight Mirage, preto, fotos escuras). |

### Área de proteção (clear space)

Mantenha ao redor do logo um espaço livre mínimo igual à altura do símbolo
dividida por 2 (metade da altura do ícone de documento, ~13px na escala
base). Nenhum outro elemento — texto, borda, outro logo — pode invadir essa
área.

### Tamanho mínimo

- Lockup completo (símbolo + wordmark): **96px** de largura.
- Símbolo isolado: **20px** de altura. Abaixo disso, use `favicon.svg`
  (fundo sólido lê melhor em tamanhos minúsculos que a silhueta isolada).

### Fundos permitidos

- `logo-light.svg` sobre Praxeti White ou fotografia clara.
- `logo-dark.svg` sobre Midnight Mirage ou fotografia escura.
- Nunca sobre fundos com padrão/textura que reduza o contraste das formas.

### Regra do checkmark

O checkmark vive dentro de um badge circular preenchido, sempre um verde de
verificação da paleta nomeada — nunca uma cor fora dela, nunca decorativo:

- Sobre fundo claro (Praxeti White): badge **Picture Book Green** `#00804C`
  com o check em Praxeti White por cima.
- Sobre fundo escuro (Midnight Mirage): badge **Mantis** `#74C365` com o
  check em Midnight Mirage por cima — Picture Book Green perde contraste
  sobre Midnight Mirage, por isso a troca do badge.

### Não fazer (logo)

- Não usar qualquer verde fora de Picture Book Green/Mantis para o badge do checkmark.
- Não distorcer, inclinar ou espelhar o símbolo.
- Não adicionar sombra, brilho, contorno/traço ou efeito 3D às formas preenchidas.
- Não recriar o wordmark digitando "Specsfy" em outra fonte — use sempre os
  arquivos SVG fornecidos ou o arquivo de fonte real (IBM Plex Sans
  SemiBold) convertido em contorno.
- Não separar o símbolo do wordmark em um mesmo contexto de marca a menos
  que o espaço só comporte o símbolo (favicon, avatar).
- Não usar o símbolo sem o checkmark — sem ele, a forma perde o significado
  ("documento provado"), não só o visual.

### Nota técnica sobre o wordmark em SVG

`logo-light.svg` e `logo-dark.svg` usam `<text>` com a stack de fontes da
seção [Tipografia](#6-tipografia). Isso garante edição fácil, mas depende de
IBM Plex Sans estar disponível no ambiente de renderização. Para impressão,
apresentações ou qualquer uso onde a fonte não está garantida, converta o
texto em contornos (`Path > Object to Path` no Inkscape/Illustrator) antes de
exportar, e salve como um `logo-light-outlined.svg` ao lado do original.

## 8. Ícones

### Ícone do framework

O ícone do framework identifica de forma compacta o Specsfy e o conjunto de
seus repositórios. Sua geometria combina três placas empilhadas com o símbolo
de código na placa superior.

| Arquivo | Uso |
|---|---|
| [`icons/icon.svg`](icons/icon.svg) | Fonte vetorial preferencial para README, documentação, interfaces e materiais escaláveis. |
| [`icons/icon.png`](icons/icon.png) | Fallback raster RGBA de 512×512 para consumidores que não aceitam SVG. |

Use sempre `icon.svg` primeiro e `icon.png` como fallback do mesmo conteúdo,
com texto alternativo `Ícone do framework Specsfy`. Este ativo representa o
framework; não substitui os lockups institucionais de `logo/` nem integra a
família de oito ícones conceituais. Os demais módulos devem referenciar os
arquivos canônicos de `brand/`, sem manter cópias divergentes.

### Ícones conceituais

Conjunto conceitual de 8 ícones que representam os elementos centrais do
método. Feitos para documentação, apresentações e futuras interfaces — não
para substituir o símbolo da marca (`logo/mark.svg`), que é único e não deve
ser remixado.

### Especificação técnica

- Grid: `viewBox 0 0 32 32`.
- Estilo: **flat** — formas sólidas preenchidas (`fill`), sem `stroke`. Sem
  gradiente, sombra ou efeito 3D.
- Cantos levemente arredondados nas barras/hastes (`rx` pequeno); demais
  contornos retos e geométricos.
- Detalhes internos (linhas de texto, moldura de checkbox, corte do canto
  dobrado) são recortes vazados no preenchimento (`fill-rule="evenodd"`),
  não formas desenhadas por cima — cada ícone continua uma única cor sólida
  (mais o fundo aparecendo através do vazado).
- Cor: a maioria usa `fill="currentColor"` — herdam a cor do texto ao redor
  via CSS (`color: var(--specsfy-ink)` etc). **Duas exceções documentadas**,
  porque a cor faz parte do significado, não é decoração:
  - `tdd-cycle.svg` — metade vermelha (`#B91C1C`), metade verde (Picture Book
    Green `#00804C`). Representa literalmente o ciclo RED → GREEN; recolorir
    destrói o significado.
  - `evidence.svg` e `task.svg` (checkmarks internos) — o restante do ícone é
    um anel/moldura vazada (não um disco sólido), para o checkmark sempre
    aparecer contra o fundo da página, não contra uma forma preenchida. O
    checkmark é sempre Picture Book Green `#00804C` em fundo claro, igual à
    regra do logo. Em superfícies escuras, troque para Mantis `#74C365`
    (mesma regra do logo).

**Lacuna conhecida:** ao contrário do logo (que tem arquivos
`logo-light.svg`/`logo-dark.svg` separados), `evidence.svg` e `task.svg` só
existem como um único arquivo com `#00804C` fixo — não há variante `-dark`
pronta. Picture Book Green sobre Midnight Mirage cai para **3.3:1**, abaixo
do mínimo de acessibilidade. Hoje isso é aceitável porque o uso predominante
é documentação sobre fundo claro; qualquer uso real sobre fundo escuro deve
recolorir o checkmark manualmente para Mantis `#74C365` antes de publicar —
não usar o arquivo como está. O mesmo vale, com o mesmo motivo, para
`tdd-cycle.svg` (ver [Acessibilidade](#9-acessibilidade)).

### Inventário

| Arquivo | Representa | Onde usar |
|---|---|---|
| [`icons/spec.svg`](icons/spec.svg) | O `spec.md`, fonte única de verdade | Cabeçalho de seções sobre especificação, links para specs |
| [`icons/gherkin.svg`](icons/gherkin.svg) | BDD / cenários Gherkin (Given-When-Then) | Documentação de aceite, exemplos de `.feature` |
| [`icons/tdd-cycle.svg`](icons/tdd-cycle.svg) | O ciclo RED → GREEN do TDD (único ícone com metade vermelha, metade verde fixas) | Explicações do Ato II, badges de status de teste |
| [`icons/gate.svg`](icons/gate.svg) | Um gate (Definition/Plan/Delivery) | Indicar checkpoints, "Gate: Passed" |
| [`icons/evidence.svg`](icons/evidence.svg) | Evidência registrada e verificada | Seções de evidência, changelogs de verificação |
| [`icons/task.svg`](icons/task.svg) | Tarefas e o ciclo READY→RED→GREEN→VERIFIED→DONE | Backlogs, listas de tarefas |
| [`icons/acts.svg`](icons/acts.svg) | Os três Atos rígidos em progressão | Diagramas de processo, onboarding |
| [`icons/traceability.svg`](icons/traceability.svg) | IDs ligando história→requisito→cenário→teste→tarefa | Matriz de rastreabilidade, explicações de IDs |

### Não fazer (ícones)

- Não usar dois ícones diferentes para o mesmo conceito no mesmo documento.
- Não colorir `spec.svg`, `gherkin.svg`, `gate.svg`, `task.svg`, `acts.svg`
  ou `traceability.svg` com verde/vermelho/First Colors of Spring — eles são
  neutros (`currentColor`, tipicamente Midnight Mirage ou Praxeti White).
- Não redesenhar os checkmarks internos em cor diferente de Picture Book
  Green (claro) / Mantis (escuro).
- Não misturar este conjunto com ícones de bibliotecas externas (Feather,
  Lucide, Font Awesome) na mesma peça — o estilo flat e o grid não batem
  com conjuntos de traço/outline.
- Não adicionar `stroke`/contorno às formas preenchidas.

## 9. Acessibilidade

Toda cor de marca é aprovada por número, não por olho. Esta seção traz os
contrastes WCAG 2.1 reais (fórmula de luminância relativa, não estimativa) e
as decisões de design que vieram de calculá-los — inclusive uma correção
aplicada depois da paleta inicial ter sido definida.

### Método

Contraste calculado como `(L1 + 0.05) / (L2 + 0.05)`, onde `L` é a
luminância relativa de cada cor (fórmula WCAG 2.1, sRGB linearizado). Metas:

- **4.5:1** — mínimo AA para texto normal.
- **3:1** — mínimo AA para texto grande (≥18.66px bold ou ≥24px regular) e
  para objetos gráficos/componentes de UI (ícones, bordas de campo).

### Pares calculados

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
| Picture Book Green `#00804C` / Midnight Mirage `#001F3F` | **3.3:1** | **Não** | — por isso o token `verified` troca para Mantis no modo escuro |
| Vermelho `#B91C1C` / Praxeti White `#F6F7ED` | **6.0:1** | Sim | Texto/label do estado RED, modo claro |
| Vermelho `#F87171` / Midnight Mirage `#001F3F` | **6.0:1** | Sim | Texto/label do estado RED, modo escuro |

### Correção aplicada: o vermelho não era o `#DC2626` "óbvio"

A escolha inicial e mais comum para vermelho de status (`#DC2626`, usada por
Tailwind/Radix e a maioria dos design systems) dá **4.47:1** sobre Praxeti
White — abaixo do mínimo de 4.5:1 para texto normal, por uma margem pequena
mas real. Como o estado `RED` do TDD/BDD frequentemente aparece como texto
curto (`RED`, badges de status), a marca usa **`#B91C1C`** em vez disso:
mesma família de vermelho, reconhecível, e **6.0:1** — folga real, não só o
mínimo técnico.

### Daltonismo — o ícone `tdd-cycle.svg`

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
problema que fez o token `verified` trocar para Mantis no modo escuro. Até
existir uma variante dedicada, quem usar esses ícones sobre fundo escuro
deve recolorir o checkmark para Mantis `#74C365` manualmente antes de
publicar.

### Movimento

`brand/style-guide.html` usa `scroll-behavior: smooth` para navegação por
âncora. Isso respeita `prefers-reduced-motion: reduce` (rolagem instantânea
e transições/animações reduzidas a ~0 para quem configurou o sistema para
motion reduzido). Qualquer novo material da marca com scroll suave, hover
animado ou transição de página deve seguir a mesma regra — nunca assuma que
motion é neutro.

### Foco de teclado

Todo link e elemento interativo em material oficial da marca precisa de um
estado de foco visível (`:focus-visible`) com contraste mínimo 3:1 contra o
fundo adjacente — não confie apenas em `:hover`. Ver a implementação em
`style-guide.html` (outline em Nuit Blanche/Nuit Blanche clareado).

### Texto alternativo

Todo SVG de `logo/` e `icons/` já inclui `role="img"` e `aria-label`
descritivo. Ao reutilizar esses arquivos embutidos (`<img src="...svg">` ou
inline), preserve o `aria-label` ou forneça um `alt`/label equivalente — não
o remova ao copiar o markup.

## 10. Do's e Don'ts gerais (cross-asset)

**Fazer:**

- Manter a paleta nomeada de 6 cores (+ vermelho funcional + `paper-elevated`)
  em qualquer peça — apresentação, README, site.
- Usar o par IBM Plex Sans/Mono em qualquer material que represente a marca
  oficialmente.
- Reservar Picture Book Green/Mantis exclusivamente para estados
  verificados/provados.
- Tratar os ícones conceituais (`icons/`) como vocabulário visual do método,
  não como enfeite — cada um mapeia para um conceito específico.

**Não fazer:**

- Não introduzir uma oitava cor de acento ou gradiente em nenhuma peça.
- Não usar o símbolo do logo sem o checkmark, ou recolorir o checkmark fora
  de Picture Book Green (claro) / Mantis (escuro).
- Não usar verde/vermelho/First Colors of Spring fora do sentido semântico
  definido na seção [Cor](#5-cor).
- Não escrever a tagline ou nome do método com hype ("revolucionário",
  "definitivo") — a voz do Specsfy vende precisão, não entusiasmo.
- Não criar uma segunda linha de ícones ou uma variação de logo sem atualizar
  este manual e as fontes normativas correspondentes — a marca segue a
  mesma regra do método: **fonte única, sem divergência entre arquivos.**

## 11. Brand Gate — checklist de publicação

O Specsfy não deixa uma tarefa passar de `READY` para `DONE` sem evidência.
A marca segue a mesma regra: nenhum material — slide, post, README, tela —
sai como "pronto" só porque parece certo. Ele passa pelo **Brand Gate**
abaixo primeiro.

Use isto antes de publicar qualquer coisa com o nome, o símbolo ou a voz do
Specsfy. Se um item falhar, o material não está pronto — corrija ou
justifique a exceção por escrito ao lado do item.

**Cor**

- [ ] Usa apenas as 6 cores nomeadas + vermelho funcional + `paper-elevated`
      — nenhuma cor de acento a mais.
- [ ] Picture Book Green/Mantis aparece **apenas** onde algo foi
      verificado/provado — não como decoração ou preenchimento neutro.
- [ ] First Colors of Spring aparece só como chip com texto Midnight
      Mirage por cima — nunca como cor de texto ou fundo de área grande.
- [ ] Se há texto sobre cor, o par passa 4.5:1 (ou 3:1 para texto
      grande/UI) — conferido na seção [Acessibilidade](#9-acessibilidade), não estimado a olho.
- [ ] Nenhum gradiente.

**Tipografia**

- [ ] IBM Plex Sans para título/corpo, IBM Plex Mono para IDs/estados/código
      — nenhuma terceira família.
- [ ] IDs e estados do método (`US-01`, `Gate: Passed`, `RED`) estão em
      mono mesmo fora de bloco de código.

**Logo**

- [ ] O símbolo sempre inclui as três partes juntas: documento, checkmark,
      três marcas. Nunca usado incompleto.
- [ ] Checkmark é Picture Book Green (fundo claro) ou Mantis (fundo
      escuro) — nunca outra cor.
- [ ] `logo-light.svg`/`logo-dark.svg` escolhido conforme o fundo real da
      peça, não por padrão.
- [ ] Respeita clear space e tamanho mínimo.
- [ ] Símbolo não foi distorcido, inclinado, espelhado, nem ganhou sombra
      ou brilho.

**Ícones**

- [ ] Cada ícone usado corresponde ao conceito certo — não há dois ícones
      para a mesma ideia no mesmo material.
- [ ] Ícones neutros usam `currentColor`; as duas exceções de cor fixa
      (`tdd-cycle.svg`, checkmarks de `evidence.svg`/`task.svg`) não foram
      recoloridas incorretamente (e foram recoloridas para Mantis se o
      fundo é escuro — ver lacuna conhecida na seção [Ícones](#8-ícones)).
- [ ] Se `tdd-cycle.svg` aparece sozinho (sem texto RED/GREEN ao redor),
      foi avaliado o risco de daltonismo.

**Voz**

- [ ] Termos do glossário grafados de forma canônica — sem sinônimo solto
      para Gate, Ato, RED/GREEN, handoff, evidência.
- [ ] Tagline usada é exatamente "Especifique. Prove. Entregue." (ou uma
      das alternativas listadas na seção [Tagline](#2-tagline-e-elevator-pitches))
      — não uma paráfrase nova.
- [ ] Nenhuma promessa que o método não garante (velocidade, "menos bugs")
      — só rastreabilidade e evidência, ditas sem hype.
- [ ] Sem emoji como marcador de seção/status, sem metáfora de guerra ou
      esporte, sem "simplesmente".

**Acessibilidade**

- [ ] Elementos interativos têm estado de foco visível (`:focus-visible`),
      não só `:hover`.
- [ ] Animações/transições respeitam `prefers-reduced-motion`.
- [ ] SVGs mantêm `role="img"` + `aria-label` (ou `alt` equivalente) ao
      serem reutilizados.

**Fonte única**

- [ ] Se este material mudou uma regra (nova cor, nova exceção, novo
      termo), a fonte normativa correspondente foi atualizada — não só o
      material final. Ver a tabela na seção [Mapa de arquivos](#12-mapa-de-arquivos).
- [ ] Este `README.md` ainda reflete todos os arquivos que existem —
      nenhum arquivo novo ficou fora do manual.

Se tudo acima está marcado, o material passou no Brand Gate. Se algo não
se aplica (ex.: peça sem texto, sem interatividade), marque como N/A com uma
frase dizendo por quê — omissão silenciosa não conta como "passou".

## 12. Mapa de arquivos

Assim como o método trata `spec.md` como fonte única por fatia, cada aspecto
da marca tem **um** arquivo normativo: o lugar onde o valor exato (hex,
geometria de SVG, CSS, JSON) é definido. Este manual explica e resume cada
um deles por extenso nas seções acima; a tabela abaixo é o índice reverso —
de aspecto da marca para arquivo exato — útil quando o que se precisa é o
valor binário/exato, não a explicação.

| Aspecto | Fonte normativa |
|---|---|
| Cartão de referência rápida (resumo de uma tela) | [`guidelines.md`](guidelines.md) |
| Style guide visual renderizado (abrir no navegador, não editar) | [`style-guide.html`](style-guide.html) |
| Manual completo em PDF | [`Specsfy-Manual-de-Marca.pdf`](Specsfy-Manual-de-Marca.pdf), gerado no monorepo [`promovaweb/specsfy`](https://github.com/promovaweb/specsfy) a partir de [`guide/brand-guide.md`](guide/brand-guide.md) |
| Cor — hex, tokens semânticos, pares aprovados | [`colors/palette.md`](colors/palette.md) |
| Cor — custom properties CSS | [`colors/tokens.css`](colors/tokens.css) |
| Cor — tokens em JSON (Figma, Style Dictionary) | [`colors/tokens.json`](colors/tokens.json) |
| Tipografia | [`typography/typography.md`](typography/typography.md) |
| Logo — regras de uso | [`logo/logo.md`](logo/logo.md) |
| Logo — arquivos SVG | [`logo/mark.svg`](logo/mark.svg), [`logo/favicon.svg`](logo/favicon.svg), [`logo/logo-light.svg`](logo/logo-light.svg), [`logo/logo-dark.svg`](logo/logo-dark.svg) |
| Ícone do framework — regras de uso e formatos | [`icons/icons.md`](icons/icons.md), [`icons/icon.svg`](icons/icon.svg), [`icons/icon.png`](icons/icon.png) |
| Ícones — especificação e inventário | [`icons/icons.md`](icons/icons.md) |
| Ícones — arquivos SVG | [`icons/spec.svg`](icons/spec.svg), [`icons/gherkin.svg`](icons/gherkin.svg), [`icons/tdd-cycle.svg`](icons/tdd-cycle.svg), [`icons/gate.svg`](icons/gate.svg), [`icons/evidence.svg`](icons/evidence.svg), [`icons/task.svg`](icons/task.svg), [`icons/acts.svg`](icons/acts.svg), [`icons/traceability.svg`](icons/traceability.svg) |
| Posicionamento, tagline, elevator pitches | [`description.md`](description.md) |
| Voz aprofundada — glossário, exemplos por canal | [`voice/voice.md`](voice/voice.md) |
| Acessibilidade — contrastes reais, daltonismo, motion | [`accessibility.md`](accessibility.md) |
| Checklist de publicação (Brand Gate) | [`checklist.md`](checklist.md) |

## 13. Regra de manutenção

Este `README.md` é o manual completo — a leitura de uma vez só, pensada para
um agente ou uma pessoa nova na marca. Cada arquivo listado no
[Mapa de arquivos](#12-mapa-de-arquivos) continua sendo a **fonte normativa**
do seu aspecto: é ali que um valor exato (um hex, uma coordenada de SVG, uma
linha de CSS/JSON) é definido primeiro.

Ao alterar qualquer regra da marca:

1. Edite a fonte normativa correspondente primeiro (ex.: um novo hex vai em
   `colors/palette.md` **e** em `colors/tokens.css`/`colors/tokens.json`
   juntos).
2. Replique a mudança na seção correspondente deste `README.md` — ele deixa
   de ser confiável no minuto em que diverge do arquivo normativo.
3. Se a mudança afeta o cartão de referência rápida (`guidelines.md`),
   atualize-o também.
4. Rode o material (ou a própria mudança de marca) contra o
   [Brand Gate](#11-brand-gate--checklist-de-publicação) antes de considerar
   a alteração pronta.

Nenhum arquivo novo em `brand/` deve ficar fora deste manual e do
[Mapa de arquivos](#12-mapa-de-arquivos) — a mesma regra de fonte única que
o método aplica ao código, a marca aplica a si mesma.
