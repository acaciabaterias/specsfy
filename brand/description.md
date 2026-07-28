# Descrição de marca — Specsfy

## Posicionamento

Specsfy é uma metodologia — não uma ferramenta, não um framework de código —
para escrever software a partir de uma especificação única, executável e
rastreável, aplicando três atos rígidos (Definir, Projetar e provar, Entregar
e validar) com gates que só passam mediante evidência real.

O território que o Specsfy ocupa não é "documentação de software" nem
"metodologia ágil genérica". É o espaço específico entre **intenção** e
**código provado**: a distância que normalmente se perde em specs que
divergem do plano, planos que divergem das tarefas, e tarefas marcadas como
prontas sem teste que comprove isso.

## Tagline

**Principal:**
> Especifique. Prove. Entregue.

Três verbos, um por Ato — a tagline literalmente espelha a estrutura do
método. É a única tagline que deve aparecer ao lado do logo em materiais
oficiais.

**Alternativas** (para contextos onde a tagline principal já apareceu perto,
ou para variar em títulos de seção):
- "Uma especificação. Rastreável até o código."
- "Nenhum 'pronto' sem evidência."

## Elevator pitches

**Curto (uma frase, para bios/perfis):**
> Specsfy é uma metodologia para escrever software a partir de uma
> especificação única, testada antes do código e concluída só com evidência.

**Médio (para README, apresentações):**
> Specsfy organiza cada fatia de trabalho em três atos: definir com clareza o
> que precisa existir, projetar e provar os testes antes da implementação, e
> entregar com evidência verificável. Uma única fonte normativa por fatia
> (`spec.md`) elimina a divergência entre spec, plano e tarefas — e nenhum
> gate avança sem RED registrado antes do código ou prova depois dele.

**Longo (para artigos, onboarding):**
> A maioria dos processos de especificação falha silenciosamente: a spec diz
> uma coisa, o plano assume outra, as tarefas são marcadas como concluídas
> sem verificação, e o "pronto" vira uma palavra vazia. Specsfy parte de seis
> compromissos — fonte única, descoberta antes da solução, BDD como aceite,
> TDD antes da implementação, trabalho rastreável por IDs compartilhados, e
> conclusão só por evidência — e os aplica em três atos rígidos com entrada,
> saída, gate e handoff próprios. O resultado não é mais documentação: é
> menos distância entre o que o usuário quis, o comportamento aceito, os
> testes que provam esse comportamento, e o código que efetivamente existe.

## Voz e tom

| Traço | Como soa | Como não soa |
|---|---|---|
| **Preciso** | "O Gate não passa sem RED registrado nos dois níveis." | "O Gate normalmente exige que os testes estejam ok." |
| **Direto** | "Não crie `plan.md` paralelo." | "Recomendamos fortemente evitar arquivos adicionais quando possível." |
| **Sem hype** | "Reduz a distância entre intenção e código." | "Revolucione sua forma de desenvolver software!" |
| **Rigoroso, não burocrático** | "Cada gate é um compromisso, não uma categoria editorial." | "Preencha o checklist de 40 itens antes de prosseguir." |

Regras práticas:

- Frases curtas e verbos no imperativo quando se trata de instrução
  ("escreva", "prove", "registre") — nunca "você deveria considerar".
- Nunca prometa o que o método não garante. O Specsfy não promete "menos
  bugs" ou "mais velocidade" — promete rastreabilidade e evidência. Deixe o
  leitor tirar a conclusão de que isso reduz bugs, não afirme por ele.
- Números e siglas do método (`US-01`, `RQ-04`, `Gate: Passed`, `RED`,
  `GREEN`) sempre em `monoespaçada` (ver `typography/typography.md`) — nunca
  parafraseados ("o requisito quatro").
- Não use metáforas de guerra ("batalha contra bugs"), esporte
  ("touchdown") ou motivação corporativa genérica ("sinergia",
  "empoderar"). O campo semântico correto é **engenharia e prova**: gate,
  evidência, rastro, estado, transição.

## O que o Specsfy não é (para guiar a linguagem)

- Não é um gerador de documentação — não fale em "gerar specs
  automaticamente" como benefício central.
- Não é uma metodologia ágil concorrente do Scrum/Kanban — não a compare
  diretamente com esses frameworks; ela opera em outro nível (o que entra
  numa fatia de trabalho, não como o time se organiza no tempo).
- Não é exclusiva para desenvolvimento assistido por IA, embora funcione
  particularmente bem nesse contexto — o método serve tanto para trabalho
  humano quanto para agentes.
