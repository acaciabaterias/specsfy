---
name: specsfy-base-interview
description: "Use quando o usuário quer ser entrevistado para aprofundar uma captura em `specs/ideias/`, uma ideia, um item em `specs/backlog/` ou uma spec existente antes de criar ou revisar a especificação. Use também quando uma transição automática pedir descoberta ou decisão material. Aplica o MCR-10 por perguntas adaptativas e produz um brief; para captura imediata sem perguntas use specsfy-base-idea, para refinamento leve use specsfy-base-backlog, e não use para escrever spec.md, tarefas, testes ou implementação."
---

# Entrevistar para a especificação

Conduza uma descoberta curta que transforme uma ideia vaga em decisões
testáveis. Mantenha o trabalho na conversa; `specsfy-base-specify` escreve a
spec inicial e `specsfy-base-update-spec` revisa uma spec já aprovada.

## Orquestrar a conversa

Ao concluir esta etapa ou detectar trabalho de outra etapa, anuncie
`Pendência detectada: <descrição> — ação: resolvendo nesta etapa` e resolva-a
quando pertencer ao próprio escopo. Quando houver troca de responsabilidade,
anuncie `Transição automática: $specsfy-base-interview → $<destino> — motivo:
<motivo> — resultado esperado: <resultado>` e carregue imediatamente a skill de
destino, sem pedir confirmação nem repetir o comando. Continue na mesma
conversa. Depois de uma correção necessária a esta etapa, anuncie `Retomada
automática: $<destino> → $specsfy-base-interview — pendência resolvida:
<resultado>` e retome-a imediatamente. Reavalie o estado após cada handoff para
evitar ciclos. Não peça confirmação para o handoff; ações sensíveis continuam
exigindo autorização específica.

## Preparar

1. Leia o pedido e, quando existir, a captura indicada em
   `specs/ideias/<data-hora>-<slug>.md`, o item em
   `specs/backlog/<NNNN>-<slug>.md` ou a spec em
   `specs/specs/<NNNN>-<slug>/spec.md`. Se houver mais de um candidato e o
   usuário não indicar qual aprofundar, pergunte.
2. Resuma em uma frase o problema, o usuário e o resultado percebido.
3. Separe o que já está decidido do que pode mudar escopo, experiência, segurança, dados, testes ou arquitetura.
4. Leia `references/discovery-map.md` somente para selecionar perguntas relevantes; não percorra a lista mecanicamente.
5. Leia `../specsfy-base-specify/references/mcr-10.md` e faça a análise categorial silenciosamente antes da primeira pergunta.

## Conversar

- Faça uma pergunta por vez: a lacuna P1 de maior `impacto × incerteza`.
- Comece pela decisão de maior impacto e incerteza.
- Ofereça 2–3 opções mutuamente exclusivas quando isso reduzir o esforço de resposta; recomende uma com justificativa curta.
- Aceite respostas livres e adapte a próxima pergunta.
- Não repita algo já respondido no pedido, no repositório ou em `spec.md`.
- Use padrões razoáveis para detalhes reversíveis e registre-os como suposições no resumo.
- Não transforme preferência técnica em requisito de produto sem explicar o efeito observável.
- Pare quando as decisões restantes forem reversíveis, de baixo risco ou puderem ser assumidas com segurança.
- Preserve os termos originais e diferencie declaração, inferência, hipótese,
  decisão, conflito e aberto.
- Confirme a intenção operacional com uma síntese; não alegue conhecer um estado
  mental que a pessoa não confirmou.
- Não recite as dez categorias nem faça uma pergunta para cada uma. Marque lentes
  irrelevantes como não aplicáveis com justificativa interna.

Garanta cobertura suficiente de:

- problema, atores e resultado desejado;
- escopo e fora de escopo;
- jornada principal, falhas e limites;
- regras de negócio e dados;
- segurança, privacidade, desempenho e acessibilidade quando relevantes;
- restrições técnicas existentes;
- sinais objetivos de aceite e sucesso.

## Encerrar

Apresente no chat um `Brief pronto para especificar` contendo:

1. Problema e objetivo.
2. Atores.
3. Escopo e fora de escopo.
4. Jornadas e regras essenciais.
5. Critérios de aceite em linguagem Given/When/Then.
6. Restrições técnicas e de qualidade.
7. Suposições.
8. Decisões ainda abertas, ou `Nenhuma decisão bloqueante`.
9. Vocabulário ambíguo/equivalente e inferências materiais confirmadas.

Não crie arquivos nesta etapa, a menos que o usuário peça explicitamente para
atualizar o item de backlog. Quando o brief estiver pronto, retorne
automaticamente para `$specsfy-base-update-spec` se a entrevista foi chamada
por uma mudança tardia em spec já aprovada. Para criar ou consolidar a definição
inicial, chame `$specsfy-base-specify`. Em ambos os casos, continue na mesma
conversa. Se a intenção de criar a spec ainda não estiver declarada, pergunte
apenas sobre a promoção; não peça confirmação para o handoff depois da resposta.

## Limites

- Não prolongue a conversa para buscar perfeição.
- Não invente stakeholders, integrações ou restrições.
- Não escreva código, testes ou tarefas.
- Se a ideia ainda estiver superficial e o objetivo for apenas registrá-la,
  anuncie e retorne automaticamente para `$specsfy-base-backlog`.
- Se o usuário já forneceu informação suficiente e pediu uma spec, faça o
  handoff automático imediatamente para `$specsfy-base-specify`.

## Especialistas sob demanda

Leia [references/specialists.md](references/specialists.md) quando a conversa
revelar tecnologia ou disciplina que exija contexto adicional. Anuncie a
pendência e carregue automaticamente um especialista já instalado. Se estiver
ausente, recomende o comando exato e peça autorização específica antes da
instalação.
