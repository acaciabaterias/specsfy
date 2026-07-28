# Backlog de requisitos e promoção de ideias

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | captura, organização, refinamento, priorização e promoção de ideias |
| Autoridade | uso público de `specsfy-base-backlog` e `specsfy-base-interview` |

## Papel

Explicar como transformar capturas e necessidades ainda abertas em um backlog
organizado, priorizado e verificável antes da promoção.

## Como usar

Consulte ao registrar uma ideia, escolher entre backlog e entrevista ou
promover um item para spec. Execute as skills pelos nomes indicados no fluxo.

## Atualize quando

- a estrutura de backlog ou specs mudar;
- uma skill assumir outra etapa do fluxo;
- estados ou critérios de promoção mudarem.

## Não use para

- substituir os requisitos formais e gates da spec promovida;
- substituir a spec promovida;
- autorizar implementação diretamente do backlog.

## Fonte da verdade e precedência

Os arquivos do projeto preservam o estado; as skills em `skills/`
governam o comportamento executável. Depois da promoção, a spec prevalece sobre
o backlog para comportamento, gates, tarefas e evidência. Para preservar sem
perguntas, use a [caixa de entrada de ideias](ideas.md).

## Estrutura

```text
specs/
├── ideias/
│   └── 2026-07-28-143205-ideia.md
├── backlog/
│   └── 0001-ideia.md
└── specs/
    └── 0001-feature/
        ├── spec.md
        └── research/
```

O item de backlog começa leve, mas pode amadurecer até produto,
desenvolvimento e testes compreenderem o comportamento esperado. Ele não contém
tarefas ou gates e nunca autoriza implementação diretamente.

## Organização do backlog

```text
Produto
└── Épico
    └── Funcionalidade
        ├── História ou requisito
        ├── Regra
        ├── Item técnico
        └── Melhoria
```

O épico representa um objetivo amplo. A funcionalidade delimita uma capacidade.
Histórias e requisitos representam entregas menores e verificáveis. Regras,
itens técnicos e melhorias também pertencem ao backlog quando tornam o
comportamento ou sua operação possível.

Nem toda ideia precisa nascer com a hierarquia completa. Use `A esclarecer` no
lugar de inventar uma relação.

## Anatomia de um item

Logo abaixo do título, mantenha as metainformações em uma tabela, não em lista:

| Metainformação | Valor |
| --- | --- |
| ID | `BACKLOG-0001` |
| Status | `Captured` |
| Produto | A esclarecer |
| Épico | A esclarecer |
| Funcionalidade | A esclarecer |
| Tipo | A esclarecer |
| Prioridade | Não priorizado |
| Criado em | data ISO |
| Spec promovida | Nenhuma |

Um item bem refinado pode conter:

- título, tipo e prioridade;
- produto, épico e funcionalidade;
- contexto do problema;
- objetivo ou história do usuário;
- comportamento esperado;
- regras de negócio;
- critérios de aceitação;
- segurança, privacidade, desempenho, volume e auditoria;
- dependências;
- situações de erro e exceções;
- dentro e fora de escopo.

A profundidade é adaptativa. Uma alteração simples exige menos detalhes;
autenticação, pagamentos, permissões, privacidade e processamento assíncrono
exigem análise cuidadosa. O melhor item não é o mais longo: é o que reduz
ambiguidade e permite verificar a entrega.

### Captura mínima e conversa

Antes de escrever, `$specsfy-base-backlog` reaproveita o pedido e confirma:

- problema percebido;
- pessoa afetada ou beneficiada;
- resultado ou valor esperado;
- contexto suficiente para distinguir a ideia.

Se algo estiver ausente, vago, contraditório ou ambíguo, a skill pergunta uma
lacuna relevante por vez e reavalia após cada resposta. Ela não usa questionário
fixo, não repete o que já foi explicado e não persiste placeholders nesses
campos. Se a pessoa não souber responder, explicita a lacuna sem inventar.

Esse é o mínimo de captura, não uma entrevista profunda. Hierarquia, prioridade,
regras detalhadas, aceite e solução técnica podem ser refinados depois.

### Duplicatas e referências

Antes de criar, a skill pesquisa termos do pedido em `specs/backlog/*.md`,
`specs/specs/*/spec.md` e `docs/**/*.md`. Ela separa possível duplicata de
backlog relacionado, spec relacionada ou documentação útil.

Uma possível duplicata exige confirmar se o item existente será atualizado ou
se há uma diferença real. Fontes úteis ficam em `Referências relacionadas` com
caminho e relação, sem substituir a intenção declarada pelo usuário.

## Padrões recorrentes

| Capacidade | Questões que o backlog deve tornar objetivas |
| --- | --- |
| Autenticação | estado da conta, tentativas, sessão, mensagens seguras, credenciais e autorização |
| Notificações | propriedade, contagem, evento de leitura, ações individual/em lote e isolamento |
| Permissões | perfil, operação, organização, alvo, invariantes, validação no servidor e auditoria |
| PIX/pagamentos | fluxo, estados, idempotência, webhook, falhas externas e dados sensíveis |
| Exportação | filtros, autorização, volume, fila, expiração, fuso horário e dados sensíveis |

Use a representação que reduz ambiguidade. Fluxos numerados ajudam em
integrações; matrizes ajudam em permissões; cenários ajudam a demonstrar
resultados e erros.

Um requisito funcional descreve o que o sistema faz. Um requisito não
funcional define condições mensuráveis de qualidade e operação. Troque “o
sistema deve ser rápido” por um limite de latência, volume e ambiente
verificáveis.

## Priorização

Mantenha o backlog realmente ordenado. Compare:

1. valor para usuário e negócio;
2. risco de segurança, privacidade e operação;
3. dependências e entregas desbloqueadas;
4. urgência;
5. esforço;
6. incerteza.

Prioridade é relativa; classificar tudo como alta não cria uma ordem.
Autenticação e autorização podem preceder melhorias visuais, assim como uma
infraestrutura de notificações pode preceder os eventos que dependem dela.

Exemplo de visão ordenada:

| Ordem | Prioridade | Tipo | Item | Objetivo |
| --- | --- | --- | --- | --- |
| 1 | Alta | Épico | Gestão de usuários | Administrar acesso |
| 2 | Alta | História | Realizar login | Acessar áreas privadas |
| 3 | Alta | Regra | Controlar permissões | Restringir operações por perfil |
| 4 | Média | Técnico | Notificações em fila | Evitar lentidão nas requisições |
| 5 | Baixa | Melhoria | Preferências de notificação | Escolher canais |

Cada linha aponta para um item próprio. Por exemplo, “realizar login” deve
esclarecer conta ativa, comparação de e-mail, proteção da senha, tentativas
inválidas, sessão, permissões, resultados de sucesso e falha e o que ficou fora
do escopo. “Criar uma tela de login” não cobre esse comportamento.

## Fluxo

```text
input → ideia capturada → backlog → interview → spec
```

1. Use `$specsfy-base-backlog` quando a ideia ainda for geral. A skill pesquisa
   material relacionado, conversa até a captura mínima ficar clara e produz
   `specs/backlog/<NNNN>-<slug>.md`. A mesma skill pode organizar, priorizar e
   refinar o item progressivamente.
2. Use `$specsfy-base-interview` para aprofundar uma ideia, um backlog ou uma
   spec. A entrevista faz uma pergunta relevante por vez e produz um brief.
3. Use `$specsfy-base-specify` somente quando houver intenção explícita de
   promover o material. A fonte normativa nasce em
   `specs/specs/<NNNN>-<slug>/spec.md`.
4. Depois da promoção, mantenha o backlog como proveniência, marque-o
   `Promoted` e registre o caminho da spec.

Ao concluir, a skill anuncia e executa automaticamente o avanço ou retorno; a
conversa continua sem repetir comandos nem autorizar implementação.

Backlog e spec possuem sequências independentes. `BACKLOG-0004` pode originar
`SPEC-0002`; identidade não implica prioridade.

## Estados do backlog

| Estado | Significado |
| --- | --- |
| `Captured` | ideia preservada com contexto mínimo |
| `Refining` | conversa ou pesquisa leve em andamento |
| `Ready for interview` | contexto suficiente para aprofundamento estruturado |
| `Promoted` | spec derivada criada e referenciada |

## Quando está refinado

Antes do handoff, a equipe deve conseguir responder:

- Qual problema será resolvido e quem será beneficiado?
- Qual evento inicia o comportamento e qual resultado será produzido?
- Quem pode executar a operação?
- Quais regras, erros e exceções precisam ser respeitados?
- Como verificar objetivamente o resultado?
- Há implicações de segurança, privacidade, desempenho ou volume?
- O que ficou fora da entrega?
- Quais dependências ou decisões continuam pendentes?

O agente identifica lacunas e pergunta uma por vez. Decisões que alteram
segurança, escopo, arquitetura ou experiência não são inventadas
silenciosamente. Esse diagnóstico prepara entrevista e spec; ainda não autoriza
desenvolvimento.

## Limites

- Não implementar diretamente de um backlog.
- Não exigir arquitetura, Gherkin ou plano técnico durante a captura inicial.
- Não apagar a formulação original ao resumir.
- Não promover automaticamente uma ideia.
- Não tratar o backlog como fonte normativa depois da promoção.

## Implementação executável

O contrato executável pertence às skills
[`specsfy-base-backlog`](../../skills/specsfy-base-backlog/),
[`specsfy-base-interview`](../../skills/specsfy-base-interview/)
e
[`specsfy-base-specify`](../../skills/specsfy-base-specify/).

## Justificativa de tamanho

O guia reúne estrutura, refinamento, priorização e promoção porque essas
decisões precisam ser comparadas no mesmo percurso público.
