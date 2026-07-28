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

**O que o Specsfy não é** — para guiar a linguagem em qualquer material:

- Não é um gerador de documentação — não fale em "gerar specs
  automaticamente" como benefício central.
- Não é uma metodologia ágil concorrente do Scrum/Kanban — não a compare
  diretamente com esses frameworks; ela opera em outro nível (o que entra
  numa fatia de trabalho, não como o time se organiza no tempo).
- Não é exclusiva para desenvolvimento assistido por IA, embora funcione
  particularmente bem nesse contexto — o método serve tanto para trabalho
  humano quanto para agentes.

### Personalidade da marca

**Flat / estrutural.** O Specsfy se parece com um desenho técnico, não com
um produto de consumo: formas sólidas preenchidas (sem traço/contorno),
grid explícito, cor usada com função (não decoração), tipografia que assume
um par sans + mono como parte da identidade, não como escolha de "modo
código".

Três adjetivos resumem a personalidade:

1. **Rigoroso** — nada é arredondado só por estética; toda forma carrega
   significado (o checkmark é sempre verificação, o verde é sempre "provado").
2. **Rastreável** — a mesma lógica de IDs e handoffs do método aparece na
   marca: cores emprestadas dos estados (`RED`, `Draft`), tipografia mono
   para IDs, ícones que remetem a conceitos específicos do método.
3. **Sóbrio** — sem gradientes, sombras, ilustração decorativa ou linguagem
   promocional. A marca não precisa convencer com efeito visual; precisa
   comunicar precisão.

## 2. Tagline e elevator pitches

**Tagline principal** — a única que deve aparecer ao lado do logo em
materiais oficiais:

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

## 3. Voz e tom

<div class="voice-table">

| Traço | Como soa | Como não soa |
|---|---|---|
| **Preciso** | "O Gate não passa sem RED registrado nos dois níveis." | "O Gate normalmente exige que os testes estejam ok." |
| **Direto** | "Não crie `plan.md` paralelo." | "Recomendamos fortemente evitar arquivos adicionais quando possível." |
| **Sem hype** | "Reduz a distância entre intenção e código." | "Revolucione sua forma de desenvolver software!" |
| **Rigoroso, não burocrático** | "Cada gate é um compromisso, não uma categoria editorial." | "Preencha o checklist de 40 itens antes de prosseguir." |

</div>

**Regras práticas:**

- Frases curtas e verbos no imperativo quando se trata de instrução
  ("escreva", "prove", "registre") — nunca "você deveria considerar".
- Nunca prometa o que o método não garante. O Specsfy não promete "menos
  bugs" ou "mais velocidade" — promete rastreabilidade e evidência. Deixe o
  leitor tirar a conclusão de que isso reduz bugs, não afirme por ele.
- Números e siglas do método (`US-01`, `RQ-04`, `Gate: Passed`, `RED`,
  `GREEN`) sempre em monoespaçada — nunca parafraseados ("o requisito
  quatro").
- Não use metáforas de guerra ("batalha contra bugs"), esporte
  ("touchdown") ou motivação corporativa genérica ("sinergia",
  "empoderar"). O campo semântico correto é **engenharia e prova**: gate,
  evidência, rastro, estado, transição.

### Glossário de termos canônicos

O método inteiro depende de IDs e nomes de estado que não podem ter
sinônimo — `US-01` não pode virar "a primeira história" em um documento e
continuar `US-01` em outro, ou a rastreabilidade que é a proposta central do
Specsfy quebra silenciosamente. A voz da marca aplica a mesma disciplina à
prosa: um termo, uma grafia, sempre.

| Termo | Grafia fixa | Nunca escreva | Nota |
|---|---|---|---|
| Gate | `Gate` (maiúsculo, en) | "portão", "checkpoint", "milestone" | Sempre com o nome completo: `Definition Gate`, `Plan Gate`, `Delivery Gate`. |
| Ato | Ato I / Ato II / Ato III | "fase", "etapa", "sprint", "estágio" | Numeração romana, sempre. |
| spec.md | `spec.md` (mono) | "a especificação" isolado quando se refere ao arquivo | Aceitável falando do conceito, não do arquivo. |
| RED / GREEN | `RED` / `GREEN` (mono, maiúsculo) | "vermelho"/"verde" quando se refere ao estado do teste | "vermelho"/"verde" só valem falando de cor. |
| Estado canônico | `Draft → Defined → Planned → Implementing → Complete` | reordenar, renomear ou abreviar os estados | Sequência fixa, não lista de exemplos. |
| Ciclo de tarefa | `READY → RED → GREEN → VERIFIED → DONE` | pular etapas na descrição | Cite a cadeia completa na primeira menção. |
| Handoff | `handoff` | "entrega" (confunde com Ato III) | Handoff = transição verificável entre atos; entrega = o ato inteiro. |
| Evidência | `evidência` | "prova" como substantivo solto | "provar"/"prova" como verbo é ok; "evidência" é o registro. |
| IDs (`US-01`, `RQ-04`, `CN-02`) | mono, formato `PREFIXO-NN` | escrever por extenso | Sempre cite o ID mesmo parafraseando o conteúdo. |

### Exemplos por canal

**Commit message:**

```
fix: corrige contraste do vermelho semântico (RED) para AA

DC2626 dava 4.47:1 sobre Praxeti White, abaixo do mínimo de texto.
Troca para B91C1C (6.0:1). Ver brand/accessibility.md.
```

**Mensagem de validação/erro** (ex.: `validate_spec.py`):

```
Definition Gate: Failed
US-03 não tem cenário BDD associado — adicione um Scenario em spec.md
antes de marcar este Gate como Passed.
```

**Título de seção de documentação:** "Ato II — Projetar e provar" — nunca
"Fase de Planejamento" com emoji de foguete no título. Sem emoji como
marcador de seção, sem hype no título de algo que já é estrutural.

**Resposta de um agente conversando com o usuário** (ex.: `specsfy-base-interview`):

> "US-04 depende de um comportamento que ainda não está confirmado: o que
> acontece se o usuário cancelar no meio da importação? Isso muda o
> cenário BDD que vou escrever a seguir."

**Post/anúncio** (uso raro, mas se existir):

> "Specsfy: uma especificação, rastreável até o código. Sem plan.md
> paralelo, sem 'pronto' sem evidência."

### Nunca dizer

<div class="dont">

- **"Simplesmente"** antes de qualquer instrução — minimiza esforço real do
  leitor e geralmente esconde um passo faltando.
- **Emoji como marcador de seção ou de status** — o método já tem um
  vocabulário de estado; emoji o duplica informalmente.
- **"Nosso/nossa IA"** genérico — nomeie a skill (`specsfy-base-interview`,
  `specsfy-base-validate`) quando o contexto permite.
- **Desculpas performáticas em mensagem de erro** ("Ops! Algo deu errado",
  seguido de emoji) — diga o que falhou e como corrigir, sem tom.
- **Voz passiva para esconder responsabilidade** — sempre nomeie a causa
  verificável.

</div>

### Idioma

Português é o idioma primário de prosa. Os identificadores literais do
sistema — nomes de estado, arquivos, siglas, nomes de Gate — permanecem em
inglês e mono porque são *tokens*, não texto: traduzi-los quebraria a busca
por texto e a rastreabilidade entre documentos. Regra de bolso: se aparece
em um `grep` do repositório para rastrear algo, não traduza; se é explicação
ao redor, português.

## 4. Cor

**Regra de ouro:**

> Verde só aparece quando algo foi provado. First Colors of Spring só aparece
> em chips de estado "em andamento". Vermelho só aparece no estado `RED`.
> Nenhuma dessas três é decoração.

### Paleta nomeada

<div class="swatch-grid">
<div class="swatch"><div class="swatch-color" style="background:#001F3F"></div><div class="swatch-meta"><div class="swatch-token">Midnight Mirage</div><div class="swatch-hex">#001F3F</div><div class="swatch-usage">Primária: logo, títulos, texto, fundo escuro</div></div></div>
<div class="swatch"><div class="swatch-color" style="background:#1E488F"></div><div class="swatch-meta"><div class="swatch-token">Nuit Blanche</div><div class="swatch-hex">#1E488F</div><div class="swatch-usage">Secundária: links, interativos</div></div></div>
<div class="swatch"><div class="swatch-color" style="background:#00804C"></div><div class="swatch-meta"><div class="swatch-token">Picture Book Green</div><div class="swatch-hex">#00804C</div><div class="swatch-usage">Verificação — fundos claros</div></div></div>
<div class="swatch"><div class="swatch-color" style="background:#74C365"></div><div class="swatch-meta"><div class="swatch-token">Mantis</div><div class="swatch-hex">#74C365</div><div class="swatch-usage">Verificação — fundos escuros</div></div></div>
<div class="swatch"><div class="swatch-color" style="background:#DBE64C"></div><div class="swatch-meta"><div class="swatch-token">First Colors of Spring</div><div class="swatch-hex">#DBE64C</div><div class="swatch-usage">Chip Draft/Implementing</div></div></div>
<div class="swatch"><div class="swatch-color" style="background:#F6F7ED;border-bottom:1px solid var(--border)"></div><div class="swatch-meta"><div class="swatch-token">Praxeti White</div><div class="swatch-hex">#F6F7ED</div><div class="swatch-usage">Papel — fundo claro padrão</div></div></div>
</div>

Os tokens primitivos acima **nunca mudam** — são as cores nomeadas fixas,
independentes de modo claro/escuro.

### Cores funcionais (fora da paleta nomeada)

<div class="swatch-grid">
<div class="swatch"><div class="swatch-color" style="background:#B91C1C"></div><div class="swatch-meta"><div class="swatch-token">Vermelho (RED)</div><div class="swatch-hex">#B91C1C claro · #F87171 escuro</div><div class="swatch-usage">Exclusivo do estado RED do TDD/BDD</div></div></div>
<div class="swatch"><div class="swatch-color" style="background:#FFFFFF;border-bottom:1px solid var(--border)"></div><div class="swatch-meta"><div class="swatch-token">Paper elevated</div><div class="swatch-hex">#FFFFFF claro · #06274F escuro</div><div class="swatch-usage">Fundo de superfícies elevadas — nunca texto</div></div></div>
</div>

`red-600` não faz parte do moodboard: é vermelho universal de status,
mantido por convenção de acessibilidade. `#B91C1C` (não o `#DC2626` mais
comum) porque é o tom mais próximo que ainda passa 4.5:1 sobre Praxeti
White — ver [Acessibilidade](#8-acessibilidade). `paper-elevated` não é
uma sétima cor de acento: é um degrau de neutro para dar profundidade a
cards/superfícies empilhadas, nunca cor de texto, ícone, badge ou destaque.

### Tokens semânticos

| Token semântico | Modo claro | Modo escuro | Papel |
|---|---|---|---|
| `paper` | Praxeti White `#F6F7ED` | Midnight Mirage `#001F3F` | Fundo de página |
| `paper-elevated` | `#FFFFFF` | `#06274F` | Fundo de cards/superfícies elevadas |
| `ink` | Midnight Mirage `#001F3F` | Praxeti White `#F6F7ED` | Texto principal, logo |
| `ink-secondary` | Midnight Mirage 62% | Praxeti White 65% | Texto secundário, legendas |
| `border` | Midnight Mirage 14% | Praxeti White 16% | Bordas, grades |
| `link` | Nuit Blanche `#1E488F` | Nuit Blanche clareado ~`#5F7DAB` | Links, interativos |
| `verified` | Picture Book Green `#00804C` | Mantis `#74C365` | Gate Passed, GREEN, evidência |
| `verified-tint` | Mantis `#74C365` | Picture Book Green 22% | Fundo de badges "Verified" |
| `draft` | First Colors of Spring `#DBE64C` | First Colors of Spring `#DBE64C` | Badge Draft/Implementing |
| `red` | `#B91C1C` | `#F87171` | Estado RED |

`verified` troca de Picture Book Green para Mantis no modo escuro porque
Picture Book Green sobre Midnight Mirage cai para **3.3:1** — abaixo do
mínimo de acessibilidade. Mantis, mais claro, resolve isso sem inventar uma
cor fora da paleta nomeada.

Exemplo de chips no uso real:
<span class="chip draft">Draft</span>&nbsp;
<span class="chip verified">Verified</span>&nbsp;
<span class="chip red">RED</span>

### Pares de contraste aprovados (WCAG AA, texto normal)

- `ink` (Midnight Mirage) sobre `paper` (Praxeti White) — texto de corpo, modo claro. **15.3:1**
- `ink` (Praxeti White) sobre `paper` (Midnight Mirage) — texto de corpo, modo escuro. **15.3:1**
- Midnight Mirage sobre First Colors of Spring ou Mantis — texto de badges/chips. **12.2:1 / 7.7:1**
- Nuit Blanche sobre Praxeti White — links e texto curto interativo. **8.2:1**
- `red-600` (`#B91C1C`) sobre Praxeti White — texto/label do estado RED. **6.0:1**

Nunca escreva parágrafos longos em Nuit Blanche, Picture Book Green, Mantis
ou First Colors of Spring — são cores de acento e chip, não de leitura
longa.

### Não fazer (cor)

<div class="dont">

- Não usar First Colors of Spring como cor de texto.
- Não usar Mantis nem Picture Book Green fora do sentido "verificado".
- Não introduzir um oitavo tom de acento além dos seis nomeados + vermelho
  funcional + `paper-elevated`.
- Não usar gradientes entre as cores da paleta.
- Não usar `paper-elevated` como cor de texto, ícone, badge ou destaque.

</div>

## 5. Tipografia

O Specsfy usa a família **IBM Plex** — desenhada para contextos de
engenharia, aberta (SIL Open Font License 1.1, uso livre comercial e de
código) e já entrega uma dupla sans/mono desenhada para conviver na mesma
página: prosa legível para specs + monoespaçada para IDs, comandos e código.

| Papel | Família | Peso padrão |
|---|---|---|
| Títulos e UI | **IBM Plex Sans** | 600 (SemiBold) título, 400/500 corpo |
| Corpo de texto | **IBM Plex Sans** | 400 |
| Código, IDs, comandos, estados | **IBM Plex Mono** | 400, 500 para ênfase |

Não use uma terceira família. Se precisar de tom mais "editorial" para
citações longas, use itálico de IBM Plex Sans — não introduza serifa.

**Por que monoespaçada é parte da marca, não um detalhe técnico:** o método
já usa monoespaço implicitamente sempre que cita `US-01`, `RQ-04`,
`Gate: Passed`, `spec.md`. Tratar isso como tipografia de marca reforça a
ideia central: **rastreabilidade é literal, não estilística.**

### Escala hierárquica

<div class="type-sample">
<div class="type-row"><span class="type-label">Display</span><div><div class="t-display">Especifique. Prove. Entregue.</div><span class="type-spec">IBM Plex Sans · 600 · 40px / 48px</span></div></div>
<div class="type-row"><span class="type-label">H2</span><div><div class="t-h2-sample">Ato I — Definir</div><span class="type-spec">IBM Plex Sans · 600 · 24px / 32px</span></div></div>
<div class="type-row"><span class="type-label">Corpo</span><div><p class="t-body-sample">Specsfy organiza cada fatia de trabalho em três atos: definir, projetar e provar, entregar e validar.</p><span class="type-spec">IBM Plex Sans · 400 · 16px / 26px</span></div></div>
<div class="type-row"><span class="type-label">Mono</span><div><span class="t-mono-sample">US-01 · Gate: Passed · spec.md</span><span class="type-spec">IBM Plex Mono · 400–500 · 0.9em</span></div></div>
</div>

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

### Regras de uso

- Títulos sempre em `ink` — nunca em cor de acento fora de badges de estado.
- Não use mais de 3 pesos na mesma peça.
- Tracking neutro no corpo; pode abrir levemente (+2%) em títulos grandes.
- Em código/mono, nunca aplique itálico — quebra a leitura de IDs.

### Licenciamento

IBM Plex Sans e IBM Plex Mono são distribuídas sob **SIL Open Font License
1.1**: uso livre em produtos comerciais, sem exigência de atribuição
visível. Disponíveis em Google Fonts e em `github.com/IBM/plex`.

## 6. Logo

### Conceito

O símbolo combina três ideias do método em uma única forma:

1. **Documento com canto dobrado** — o `spec.md`, fonte única de verdade.
2. **Checkmark verde** — nada avança sem evidência; verde é reservado para o
   que foi verificado.
3. **Três marcas na base** — os três Atos rígidos.

O estilo é **flat**: formas sólidas preenchidas, sem traço/contorno. O
documento é uma silhueta preenchida (canto dobrado recortado como vazado);
o checkmark vive dentro de um badge circular preenchido. As três ideias
juntas são o que torna o símbolo específico do Specsfy — nunca use apenas
uma delas isoladamente.

<div class="logo-cards">
<div class="logo-card light"><svg width="180" height="40" viewBox="0 0 180 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Specsfy">
  <g transform="translate(0,4)">
    <path fill="#001F3F" fill-rule="evenodd" d="M7,3 L19,3 L25,9 L25,27 L7,27 Z M19,3 L25,9 L19,9 Z"/>
    <circle fill="#00804C" cx="16.5" cy="19" r="7"/>
    <path fill="#F6F7ED" transform="translate(11.3,14) scale(0.72)" d="M4.5,8.1 L2.4,6 L1.7,6.7 L4.5,9.5 L10.5,3.5 L9.8,2.8 Z"/>
    <rect fill="#001F3F" x="10.5" y="28.5" width="2.4" height="3" rx="1.2"/>
    <rect fill="#001F3F" x="15.3" y="28.5" width="2.4" height="3" rx="1.2"/>
    <rect fill="#001F3F" x="20.1" y="28.5" width="2.4" height="3" rx="1.2"/>
  </g>
  <text x="40" y="28" font-family="IBM Plex Sans" font-weight="600" font-size="26" fill="#001F3F" letter-spacing="0.2">Specsfy</text>
</svg></div>
<div class="logo-card dark"><svg width="180" height="40" viewBox="0 0 180 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Specsfy">
  <g transform="translate(0,4)">
    <path fill="#F6F7ED" fill-rule="evenodd" d="M7,3 L19,3 L25,9 L25,27 L7,27 Z M19,3 L25,9 L19,9 Z"/>
    <circle fill="#74C365" cx="16.5" cy="19" r="7"/>
    <path fill="#001F3F" transform="translate(11.3,14) scale(0.72)" d="M4.5,8.1 L2.4,6 L1.7,6.7 L4.5,9.5 L10.5,3.5 L9.8,2.8 Z"/>
    <rect fill="#F6F7ED" x="10.5" y="28.5" width="2.4" height="3" rx="1.2"/>
    <rect fill="#F6F7ED" x="15.3" y="28.5" width="2.4" height="3" rx="1.2"/>
    <rect fill="#F6F7ED" x="20.1" y="28.5" width="2.4" height="3" rx="1.2"/>
  </g>
  <text x="40" y="28" font-family="IBM Plex Sans" font-weight="600" font-size="26" fill="#F6F7ED" letter-spacing="0.2">Specsfy</text>
</svg></div>
</div>

### Arquivos

| Arquivo | Uso |
|---|---|
| `logo/mark.svg` | Símbolo isolado, colorido, fundo transparente. Avatar, ícone de app, redes sociais. |
| `logo/favicon.svg` | Símbolo com fundo sólido Midnight Mirage, documento preenchido Praxeti White. Tamanhos pequenos (16–32px). |
| `logo/logo-light.svg` | Símbolo + wordmark em Midnight Mirage. Fundos claros. |
| `logo/logo-dark.svg` | Símbolo + wordmark em Praxeti White. Fundos escuros. |

### Regras de uso

- **Clear space:** espaço livre mínimo ao redor igual à metade da altura do
  símbolo (~13px na escala base). Nenhum outro elemento pode invadir essa
  área.
- **Tamanho mínimo:** lockup completo, 96px de largura; símbolo isolado,
  20px de altura (abaixo disso, use `favicon.svg`).
- **Fundos:** `logo-light.svg` sobre Praxeti White/fotografia clara;
  `logo-dark.svg` sobre Midnight Mirage/fotografia escura; nunca sobre
  fundos com textura que reduza o contraste das formas.
- **Checkmark:** badge circular sempre num verde de verificação da paleta —
  Picture Book Green `#00804C` em fundo claro, Mantis `#74C365` em fundo
  escuro (Picture Book Green perde contraste sobre Midnight Mirage).

### Não fazer (logo)

<div class="dont">

- Não usar qualquer verde fora de Picture Book Green/Mantis no badge do checkmark.
- Não distorcer, inclinar ou espelhar o símbolo.
- Não adicionar sombra, brilho, contorno/traço ou efeito 3D às formas preenchidas.
- Não recriar o wordmark digitando "Specsfy" em outra fonte.
- Não separar o símbolo do wordmark a menos que o espaço só comporte o
  símbolo (favicon, avatar).
- Não usar o símbolo sem o checkmark — sem ele, a forma perde o
  significado ("documento provado"), não só o visual.

</div>

## 7. Ícones

### Ícone do framework

O ícone do framework identifica o Specsfy e seus repositórios: três placas
empilhadas, com a placa superior marcada pelo símbolo de código. Use
`icons/icon.svg` como fonte vetorial preferencial e `icons/icon.png` como
fallback raster RGBA de 512×512. Mantenha o texto alternativo
`Ícone do framework Specsfy`.

<div style="text-align:center; margin:24px 0;">
<svg width="128" height="128" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ícone do framework Specsfy">
  <path d="M34 334L256 478L478 334" fill="none" stroke="#000" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M34 254L256 398L478 254" fill="none" stroke="#000" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M245.73 18.11C251.96 14.10 260.04 14.10 266.27 18.11L489.19 161.63C493.45 164.37 496 169.08 496 174.15C496 179.21 493.45 183.92 489.19 186.66L266.27 334.01C260.04 338.03 251.96 338.03 245.73 334.01L22.81 186.66C18.55 183.92 16 179.21 16 174.15C16 169.08 18.55 164.37 22.81 161.63Z" fill="#000"/>
  <path d="M190.5 143.5L160 176L190.5 208.5" fill="none" stroke="#FFF" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M269 124L243 228" fill="none" stroke="#FFF" stroke-width="32" stroke-linecap="round"/>
  <path d="M321.5 143.5L352 176L321.5 208.5" fill="none" stroke="#FFF" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
</div>

Ele não substitui o logo institucional de `logo/` e não faz parte do conjunto
conceitual abaixo. Os módulos usam os arquivos canônicos de `brand/`, sem
duplicar os binários.

### Ícones conceituais

Conjunto conceitual de 8 ícones para documentação, apresentações e futuras
interfaces — não substituem o símbolo da marca, que é único e não deve ser
remixado.

**Especificação técnica:** grid `viewBox 0 0 32 32`; estilo **flat** —
formas sólidas preenchidas (`fill`), sem `stroke`, sem gradiente/sombra/3D.
Detalhes internos (linhas de texto, moldura de checkbox, corte do canto
dobrado) são recortes vazados no preenchimento (`fill-rule="evenodd"`), não
formas desenhadas por cima. A maioria usa `currentColor` — duas exceções de
cor fixa porque a cor é parte do significado: `tdd-cycle.svg` (metade
vermelha, metade verde) e os checkmarks internos de `evidence.svg`/
`task.svg` (Picture Book Green, troque para Mantis em fundo escuro — nesses
dois o restante do ícone é um anel/moldura vazada, não um disco sólido,
para o checkmark sempre aparecer contra o fundo da página).

<div class="icon-grid">
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <path fill="currentColor" fill-rule="evenodd" d="M8,4 L18,4 L24,10 L24,28 L8,28 Z M18,4 L24,10 L18,10 Z M11,14 H21 V16 H11 Z M11,18 H21 V20 H11 Z M11,22 H17 V24 H11 Z"/>
</svg><div class="icon-name">spec.svg</div><div class="icon-desc">O spec.md, fonte única de verdade</div></div>
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <polygon fill="currentColor" points="5,5 9,8 5,11"/>
  <rect fill="currentColor" x="12" y="7" width="15" height="2" rx="1"/>
  <polygon fill="currentColor" points="5,13 9,16 5,19"/>
  <rect fill="currentColor" x="12" y="15" width="15" height="2" rx="1"/>
  <polygon fill="currentColor" points="5,21 9,24 5,27"/>
  <rect fill="currentColor" x="12" y="23" width="15" height="2" rx="1"/>
</svg><div class="icon-name">gherkin.svg</div><div class="icon-desc">BDD / cenários Given-When-Then</div></div>
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <path fill="#B91C1C" d="M6,16 A10,10 0 0 1 26,16 Z"/>
  <path fill="#00804C" d="M26,16 A10,10 0 0 1 6,16 Z"/>
  <polygon fill="#B91C1C" points="26,16 22.5,13.3 22.5,18.7"/>
  <polygon fill="#00804C" points="6,16 9.5,13.3 9.5,18.7"/>
</svg><div class="icon-name">tdd-cycle.svg</div><div class="icon-desc">Ciclo RED → GREEN do TDD</div></div>
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <rect fill="currentColor" x="6" y="6" width="2.2" height="21" rx="1.1"/>
  <rect fill="currentColor" x="23.8" y="6" width="2.2" height="21" rx="1.1"/>
  <rect fill="currentColor" x="6" y="6" width="20" height="1.8" rx="0.9"/>
  <path fill="currentColor" transform="translate(11.2,12.5) scale(1.1)" d="M4.5,8.1 L2.4,6 L1.7,6.7 L4.5,9.5 L10.5,3.5 L9.8,2.8 Z"/>
</svg><div class="icon-name">gate.svg</div><div class="icon-desc">Um gate (Definition/Plan/Delivery)</div></div>
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <path fill="currentColor" fill-rule="evenodd" d="M13,5 A8,8 0 1 1 12.999,5 Z M13,7.4 A5.6,5.6 0 1 0 13.001,7.4 Z"/>
  <rect fill="currentColor" x="17.3" y="18.3" width="2.6" height="11" rx="1.3" transform="rotate(45 18.6 23.8)"/>
  <path fill="#00804C" transform="translate(8.4,8.4) scale(0.78)" d="M4.5,8.1 L2.4,6 L1.7,6.7 L4.5,9.5 L10.5,3.5 L9.8,2.8 Z"/>
</svg><div class="icon-name">evidence.svg</div><div class="icon-desc">Evidência registrada e verificada</div></div>
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <path fill="currentColor" fill-rule="evenodd" d="M6,7.4 L11.6,7.4 A1.4,1.4 0 0 1 13,8.8 L13,10.6 A1.4,1.4 0 0 1 11.6,12 L6,12 A1.4,1.4 0 0 1 4.6,10.6 L4.6,8.8 A1.4,1.4 0 0 1 6,7.4 Z M6.55,8.7 L11.05,8.7 A0.7,0.7 0 0 1 11.75,9.4 L11.75,10 A0.7,0.7 0 0 1 11.05,10.7 L6.55,10.7 A0.7,0.7 0 0 1 5.85,10 L5.85,9.4 A0.7,0.7 0 0 1 6.55,8.7 Z"/>
  <path fill="#00804C" transform="translate(6.9,8.05) scale(0.24)" d="M4.5,8.1 L2.4,6 L1.7,6.7 L4.5,9.5 L10.5,3.5 L9.8,2.8 Z"/>
  <rect fill="currentColor" x="16" y="8" width="11" height="2" rx="1"/>
  <path fill="currentColor" opacity="0.4" fill-rule="evenodd" d="M6,15.4 L11.6,15.4 A1.4,1.4 0 0 1 13,16.8 L13,18.6 A1.4,1.4 0 0 1 11.6,20 L6,20 A1.4,1.4 0 0 1 4.6,18.6 L4.6,16.8 A1.4,1.4 0 0 1 6,15.4 Z M6.55,16.7 L11.05,16.7 A0.7,0.7 0 0 1 11.75,17.4 L11.75,18 A0.7,0.7 0 0 1 11.05,18.7 L6.55,18.7 A0.7,0.7 0 0 1 5.85,18 L5.85,17.4 A0.7,0.7 0 0 1 6.55,16.7 Z"/>
  <rect fill="currentColor" opacity="0.4" x="16" y="16" width="11" height="2" rx="1"/>
  <path fill="currentColor" opacity="0.4" fill-rule="evenodd" d="M6,23.4 L11.6,23.4 A1.4,1.4 0 0 1 13,24.8 L13,26.6 A1.4,1.4 0 0 1 11.6,28 L6,28 A1.4,1.4 0 0 1 4.6,26.6 L4.6,24.8 A1.4,1.4 0 0 1 6,23.4 Z M6.55,24.7 L11.05,24.7 A0.7,0.7 0 0 1 11.75,25.4 L11.75,26 A0.7,0.7 0 0 1 11.05,26.7 L6.55,26.7 A0.7,0.7 0 0 1 5.85,26 L5.85,25.4 A0.7,0.7 0 0 1 6.55,24.7 Z"/>
  <rect fill="currentColor" opacity="0.4" x="16" y="24" width="11" height="2" rx="1"/>
</svg><div class="icon-name">task.svg</div><div class="icon-desc">Tarefas: READY→RED→GREEN→VERIFIED→DONE</div></div>
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <rect fill="currentColor" x="7" y="19" width="5" height="8" rx="1"/>
  <rect fill="currentColor" x="14" y="13" width="5" height="14" rx="1"/>
  <rect fill="currentColor" x="21" y="7" width="5" height="20" rx="1"/>
</svg><div class="icon-name">acts.svg</div><div class="icon-desc">Os três Atos em progressão</div></div>
<div class="icon-card"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <g fill="currentColor">
    <rect x="-5.75" y="-1" width="11.51" height="2.2" rx="1.1" transform="translate(7.85,17) rotate(-60.3)"/>
    <rect x="-5.78" y="-1" width="11.56" height="2.2" rx="1.1" transform="translate(13.6,17) rotate(59.9)"/>
    <rect x="-5.75" y="-1" width="11.51" height="2.2" rx="1.1" transform="translate(19.35,17) rotate(-60.3)"/>
    <rect x="-5.78" y="-1" width="11.56" height="2.2" rx="1.1" transform="translate(25.1,17) rotate(59.9)"/>
    <circle cx="5" cy="22" r="2.6"/>
    <circle cx="10.7" cy="12" r="2.6"/>
    <circle cx="16.5" cy="22" r="2.6"/>
    <circle cx="22.2" cy="12" r="2.6"/>
    <circle cx="28" cy="22" r="2.6"/>
  </g>
</svg><div class="icon-name">traceability.svg</div><div class="icon-desc">IDs ligando história→requisito→cenário→teste→tarefa</div></div>
</div>

**Lacuna conhecida:** `evidence.svg` e `task.svg` só existem como arquivo
único com Picture Book Green fixo — não há variante `-dark`. Sobre Midnight
Mirage esse verde cai para 3.3:1, abaixo do mínimo de acessibilidade; quem
usar esses ícones sobre fundo escuro deve recolorir o checkmark para Mantis
manualmente antes de publicar. Ver [Acessibilidade](#8-acessibilidade).

### Não fazer (ícones)

<div class="dont">

- Não usar dois ícones diferentes para o mesmo conceito no mesmo documento.
- Não colorir os ícones neutros com verde/vermelho/First Colors of Spring.
- Não redesenhar os checkmarks internos em cor diferente da regra do logo.
- Não misturar este conjunto com ícones de bibliotecas externas na mesma
  peça — o estilo flat e o grid não batem com conjuntos de traço/outline.

</div>

<a id="8-acessibilidade"></a>

## 8. Acessibilidade

Toda cor de marca é aprovada por número, não por olho. Contraste calculado
como `(L1 + 0.05) / (L2 + 0.05)`, luminância relativa em sRGB linearizado
(fórmula WCAG 2.1). Metas: **4.5:1** mínimo AA para texto normal; **3:1**
para texto grande (≥18.66px bold ou ≥24px regular) e componentes de UI.

| Par | Contraste | Passa AA texto normal? | Onde é usado |
|---|---|---|---|
| Midnight Mirage / Praxeti White | **15.3:1** | Sim | Texto de corpo, modo claro |
| Praxeti White / Midnight Mirage | **15.3:1** | Sim | Texto de corpo, modo escuro |
| Nuit Blanche / Praxeti White | **8.2:1** | Sim | Links, modo claro |
| Nuit Blanche clareado `#5F7DAB` / Midnight Mirage | **3.95:1** | Não (só texto grande/UI) | Links, modo escuro — nunca em texto pequeno isolado |
| Midnight Mirage / First Colors of Spring | **12.2:1** | Sim | Texto de chip "Draft" |
| Midnight Mirage / Mantis | **7.7:1** | Sim | Texto de chip "Verified", modo claro |
| Picture Book Green / Praxeti White | **4.6:1** | Sim (por pouco) | Texto/ícone "verified", modo claro |
| Mantis / Midnight Mirage | **7.7:1** | Sim | Texto/ícone "verified", modo escuro |
| Picture Book Green / Midnight Mirage | **3.3:1** | **Não** | Por isso `verified` troca para Mantis no modo escuro |
| Vermelho `#B91C1C` / Praxeti White | **6.0:1** | Sim | Texto/label RED, modo claro |
| Vermelho `#F87171` / Midnight Mirage | **6.0:1** | Sim | Texto/label RED, modo escuro |

### A correção do vermelho

A escolha inicial e mais comum para vermelho de status (`#DC2626`, usada por
Tailwind/Radix e a maioria dos design systems) dá **4.47:1** sobre Praxeti
White — abaixo do mínimo de 4.5:1, por uma margem pequena mas real. A marca
usa **`#B91C1C`** em vez disso: mesma família de vermelho, reconhecível, e
**6.0:1** — folga real, não só o mínimo técnico.

### Daltonismo

`tdd-cycle.svg` é o único lugar da marca que depende de vermelho e verde
para transmitir dois estados opostos — exatamente o par que usuários com
deuteranopia/protanopia (~8% dos homens) têm mais dificuldade em
distinguir. **Regra:** nunca a única forma de indicar RED/GREEN em UI real —
acompanhe sempre de texto, posição ou um segundo canal (✕ vs ✓).

### Movimento e foco de teclado

Materiais interativos da marca devem respeitar `prefers-reduced-motion`
(scroll instantâneo, transições reduzidas a ~0) e ter estado de foco visível
(`:focus-visible`, contraste mínimo 3:1) — nunca depender só de `:hover`.

### Texto alternativo

Todo SVG de logo/ícones inclui `role="img"` e `aria-label` descritivo. Ao
reutilizar esses arquivos, preserve o `aria-label` ou forneça um `alt`
equivalente.

## 9. Brand Gate — checklist de publicação

O Specsfy não deixa uma tarefa passar de `READY` para `DONE` sem evidência.
A marca segue a mesma regra: nenhum material sai como "pronto" só porque
parece certo. Ele passa pelo Brand Gate abaixo primeiro.

**Cor**

<ul class="checklist">
<li>Usa apenas as 6 cores nomeadas + vermelho funcional + paper-elevated.</li>
<li>Picture Book Green/Mantis aparece só onde algo foi verificado/provado.</li>
<li>First Colors of Spring só como chip com texto Midnight Mirage por cima.</li>
<li>Texto sobre cor passa 4.5:1 (ou 3:1 texto grande/UI) — conferido, não estimado.</li>
<li>Nenhum gradiente ou sombra.</li>
</ul>

**Tipografia**

<ul class="checklist">
<li>IBM Plex Sans para título/corpo, IBM Plex Mono para IDs/estados/código.</li>
<li>IDs e estados do método em mono mesmo fora de bloco de código.</li>
</ul>

**Logo**

<ul class="checklist">
<li>Símbolo sempre com as três partes juntas — nunca usado incompleto.</li>
<li>Checkmark é Picture Book Green (claro) ou Mantis (escuro) — nunca outra cor.</li>
<li>logo-light/logo-dark escolhido conforme o fundo real da peça.</li>
<li>Respeita clear space e tamanho mínimo.</li>
<li>Símbolo não foi distorcido, inclinado, espelhado, nem ganhou sombra ou brilho.</li>
</ul>

**Ícones**

<ul class="checklist">
<li>Cada ícone corresponde ao conceito certo — sem dois ícones para a mesma ideia.</li>
<li>Ícones neutros usam currentColor; exceções de cor fixa não foram recoloridas incorretamente.</li>
<li>tdd-cycle.svg sozinho (sem texto RED/GREEN) foi avaliado quanto a daltonismo.</li>
</ul>

**Voz**

<ul class="checklist">
<li>Termos do glossário grafados de forma canônica — sem sinônimo solto.</li>
<li>Tagline usada é exatamente "Especifique. Prove. Entregue." ou uma alternativa listada.</li>
<li>Nenhuma promessa que o método não garante.</li>
<li>Sem emoji como marcador de seção/status, sem metáfora de guerra ou esporte, sem "simplesmente".</li>
</ul>

**Acessibilidade**

<ul class="checklist">
<li>Elementos interativos têm foco visível (:focus-visible), não só :hover.</li>
<li>Animações/transições respeitam prefers-reduced-motion.</li>
<li>SVGs mantêm role="img" + aria-label ao serem reutilizados.</li>
</ul>

Se tudo acima está marcado, o material passou no Brand Gate. Se algo não se
aplica, marque como N/A com uma frase dizendo por quê — omissão silenciosa
não conta como "passou".

## 10. Sobre este documento

Este PDF é gerado a partir de `brand/guide/brand-guide.md` e publicado como
`brand/Specsfy-Manual-de-Marca.pdf`. O monorepo `promovaweb/specsfy` mantém
`.pdf/build-brand-guide.sh`, `.pdf/style.css` e o `Makefile` que executam o
pipeline Markdown → HTML via Pandoc → PDF via WeasyPrint. Nenhum gerador vive
em `docs/` ou neste repositório de marca.

Na raiz do monorepo, reconstrua o PDF quando o Markdown, o CSS do PDF, o template ou
a fonte visual mudar:

```
make brand-guide
```

O `Makefile` do monorepo mantém essas fontes como dependências do PDF e evita uma
segunda cópia em `brand/guide/`. A folha `.pdf/style.css` aplica os tokens
Midnight Mirage, Praxeti White, Mantis e as famílias IBM Plex ao documento.

Os valores exatos (hex, tokens CSS/JSON, geometria de SVG) continuam
normativos em seus arquivos de origem dentro do repositório — `colors/`,
`logo/`, `icons/icon.svg`, `icons/icon.png`, os ícones conceituais,
`typography/` — e no manual completo `brand/README.md`.
Se uma regra mudar, atualize a fonte normativa e este arquivo juntos antes
de gerar um novo PDF.
