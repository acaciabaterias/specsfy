# Glossário do projeto

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | vocabulário transversal do Specsfy |
| Autoridade | significado operacional dos termos canônicos |

## Papel

Manter a linguagem transversal usada por pessoas, agentes, specs, skills e
validadores com significado operacional consistente.

## Como usar

Consulte antes de criar nomes para estados, gates, tarefas ou artefatos do
método. Preserve IDs e termos canônicos nas specs e testes.

## Atualize quando

- um termo transversal ganhar definição nova;
- duas palavras forem confirmadas como equivalentes;
- um termo legado precisar ser distinguido do termo vigente.

## Não use para

- definir vocabulário exclusivo de uma feature;
- acumular toda palavra encontrada no código;
- mudar silenciosamente o significado de IDs existentes.

## Fonte da verdade e precedência

Este glossário governa vocabulário transversal. Uma spec pode definir termos
locais sem contradizê-lo. Em conflito material, a decisão deve ser recomposta na
fonte normativa antes de alterar usos.

## Termos canônicos

| Termo | Definição operacional | Não confundir com |
| --- | --- | --- |
| Fatia vertical | Entrega demonstrável com problema, aceite, testes, tarefas e evidência próprios | camada técnica |
| Ideia capturada | Input preservado e pré-processado sem perguntas em `specs/ideias/<data-hora>-<slug>.md` | backlog, requisito ou autorização |
| Backlog | Item priorizável em `specs/backlog/<NNNN>-<slug>.md` que amadurece uma necessidade antes da promoção | captura bruta, spec ou tarefa |
| Interview | Conversa adaptativa que aprofunda ideia, backlog ou spec e prepara o handoff | captura superficial ou especificação |
| Spec | `specs/specs/<NNNN>-<slug>/spec.md`, fonte normativa única de uma fatia; somente o diretório é numerado | documento de contexto |
| Atualização de spec | incorporação explícita de pedido surgido depois do Definition Gate, com análise de impacto e reabertura seletiva dos atos | nova spec ou edição silenciosa de código |
| Research | Evidência externa consultada e indexada pela spec | requisito |
| Gate | Resultado verificável que autoriza o handoff entre atos | checkbox editorial |
| RED | Falha válida causada pelo comportamento ausente ou incorreto | erro de ambiente ou sintaxe |
| Cenário BDD | `AC-NNN` distinto, mantido em Gherkin na `spec.md` e associado por `**Cobre**` a histórias e requisitos | arquivo `.feature` executável |
| Caso TDD | Definição de teste executável com marcador `SPECSFY:` próprio e RED/GREEN observável | arquivo de teste ou marcador compartilhado por vários testes |
| Contexto transversal | Decisão vigente aplicável a várias fatias | comportamento de uma feature |
| ADR | Registro histórico de uma decisão arquitetural e suas consequências | arquitetura vigente |

## Regras de vocabulário

- Use `spec` para a fonte normativa e `contexto` para decisões transversais.
- Use `tarefa` somente para itens da seção 14 de uma spec.
- Use `Passed` apenas para um gate comprovado.
- Preserve `FR`, `NFR`, `AC`, `US`, `DEC` e `T` como IDs rastreáveis.
