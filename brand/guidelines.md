# Brand Guidelines — Specsfy (cartão de referência rápida)

O manual completo da marca — com todo o conteúdo abaixo por extenso, glossário,
exemplos por canal e o checklist de publicação embutido — é
[`README.md`](README.md). Este arquivo é a versão condensada: um cartão de
uma tela para quem já conhece a marca e só precisa checar um valor rápido.
Cada seção também tem uma fonte normativa própria (tabela abaixo) — este
arquivo é resumo e mapa, não a duplicata dos valores exatos.

| Aspecto | Fonte normativa |
|---|---|
| Cores | [`colors/palette.md`](colors/palette.md) · tokens em [`colors/tokens.css`](colors/tokens.css) / [`colors/tokens.json`](colors/tokens.json) |
| Tipografia | [`typography/typography.md`](typography/typography.md) |
| Logo | [`logo/logo.md`](logo/logo.md) |
| Ícone do framework | [`icons/icon.svg`](icons/icon.svg) · fallback [`icons/icon.png`](icons/icon.png) |
| Ícones | [`icons/icons.md`](icons/icons.md) |
| Posicionamento, tagline, elevator pitches | [`description.md`](description.md) |
| Voz aprofundada — glossário, exemplos por canal | [`voice/voice.md`](voice/voice.md) |
| Acessibilidade — contrastes reais, daltonismo, motion | [`accessibility.md`](accessibility.md) |
| Checklist de publicação | [`checklist.md`](checklist.md) |

## Personalidade da marca

**Flat / estrutural.** O Specsfy se parece com um desenho técnico, não com
um produto de consumo: formas sólidas preenchidas, grid explícito, cor usada
com função (não decoração), tipografia que assume um par sans + mono como
parte da identidade, não como escolha de "modo código".

Três adjetivos que resumem a personalidade:

1. **Rigoroso** — nada é decorativo só por estética; toda forma carrega
   significado (o checkmark é sempre verificação, o verde é sempre "provado").
2. **Rastreável** — a mesma lógica de IDs e handoffs do método aparece na
   marca: cores emprestadas dos estados (`RED`, `Draft`), tipografia mono
   para IDs, ícones que remetem a conceitos específicos do método.
3. **Sóbrio** — sem gradientes, sombras, ilustração decorativa ou linguagem
   promocional. A marca não precisa convencer com efeito visual; precisa
   comunicar precisão.

## Resumo rápido — cor

- Paleta nomeada de 6 cores: **Midnight Mirage** `#001F3F` (primária),
  **Nuit Blanche** `#1E488F` (links/interativos), **Picture Book Green**
  `#00804C` e **Mantis** `#74C365` (verificação, claro/escuro), **First
  Colors of Spring** `#DBE64C` (chip de Draft) e **Praxeti White** `#F6F7ED`
  (papel).
- Verde (Picture Book Green/Mantis) **só** para o que foi provado (gate,
  teste GREEN, evidência). Nunca decorativo.
- Vermelho (`#B91C1C` em fundo claro, `#F87171` em fundo escuro — fora da
  paleta nomeada) é emprestado do vocabulário do método (estado `RED`) — uso
  exclusivamente semântico. First Colors of Spring substitui o âmbar para
  `Draft`/`Implementing`, sempre como chip, nunca como cor de texto.
- Sem gradientes. Ver [`colors/palette.md`](colors/palette.md) para tokens
  completos e pares de contraste aprovados.

## Resumo rápido — tipografia

- **IBM Plex Sans** (texto e títulos) + **IBM Plex Mono** (código, IDs,
  estados) — nenhuma terceira família.
- IDs e estados do método (`US-01`, `Gate: Passed`, `spec.md`) sempre em
  mono, mesmo fora de blocos de código — é parte da marca, não formatação.

## Resumo rápido — logo

- Estilo flat: formas sólidas preenchidas, sem traço/contorno.
- Símbolo = documento preenchido (spec.md) + badge circular com checkmark
  (evidência) + três marcas (os três Atos). As três ideias juntas são o que
  torna o símbolo específico do Specsfy — nunca use apenas uma delas
  isoladamente.
- `logo-light.svg` em fundos claros, `logo-dark.svg` em fundos escuros,
  `favicon.svg` para tamanhos pequenos, `mark.svg` para o símbolo isolado.
- Clear space e tamanho mínimo: ver [`logo/logo.md`](logo/logo.md).

## Resumo rápido — ícone do framework

- Use [`icons/icon.svg`](icons/icon.svg) como formato vetorial preferencial e
  [`icons/icon.png`](icons/icon.png) como fallback raster RGBA de 512×512.
- Exiba o ícone do framework nas portas README e em interfaces que representem
  o ecossistema, sempre com texto alternativo `Ícone do framework Specsfy`.
- Não confunda esse ativo com o logo institucional de `logo/` nem com os oito
  ícones conceituais descritos em [`icons/icons.md`](icons/icons.md).

## Resumo rápido — voz

- Tagline oficial: **"Especifique. Prove. Entregue."**
- Tom: preciso, direto, sem hype, rigoroso sem ser burocrático.
- Vocabulário correto: gate, evidência, rastro, estado, transição. Vocabulário
  errado: sinergia, revolucionar, empoderar, batalha, touchdown.
- Termos com grafia fixa (Gate, Ato, RED/GREEN, handoff, evidência, IDs) —
  glossário completo e exemplos por canal em [`voice/voice.md`](voice/voice.md).
- Detalhes de posicionamento e pitches em [`description.md`](description.md).

## Resumo rápido — acessibilidade

- Todo par texto/fundo é aprovado por contraste calculado (WCAG), não a
  olho — inclusive uma correção real: o vermelho semântico usa `#B91C1C`,
  não o `#DC2626` mais comum, porque este último falha AA sobre Praxeti
  White.
- `tdd-cycle.svg` depende de vermelho/verde — nunca use sozinho como único
  sinal de estado em UI real; acompanhe de texto ou posição.
- Foco de teclado visível e `prefers-reduced-motion` são obrigatórios em
  qualquer material interativo.
- Detalhes e todos os pares calculados em [`accessibility.md`](accessibility.md).

## Do's e Don'ts gerais (cross-asset)

**Fazer:**
- Manter a paleta nomeada de 6 cores (+ vermelho funcional) em qualquer
  peça — apresentação, README, site. Ver `colors/palette.md`.
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
  definido em `colors/palette.md`.
- Não escrever a tagline ou nome do método com hype ("revolucionário",
  "definitivo") — a voz do Specsfy vende precisão, não entusiasmo.
- Não criar uma segunda linha de ícones ou uma variação de logo sem atualizar
  este documento e as fontes normativas correspondentes — a marca segue a
  mesma regra do método: **fonte única, sem divergência entre arquivos.**

## Antes de publicar

Rode o material contra [`checklist.md`](checklist.md) — o "Brand Gate".
Assim como o método não marca uma tarefa como `DONE` sem evidência, nenhum
material de marca é "final" só porque parece certo.
