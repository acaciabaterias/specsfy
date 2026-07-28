# Como a metodologia funciona

O Specsfy ajuda você a transformar um pedido em uma entrega comprovada. Você explica
o que precisa; o agente organiza definição, plano, testes e implementação.

A metodologia existe para responder, durante todo o trabalho, a três perguntas:

1. **O que será entregue?**
2. **Como sabemos que o plano está pronto?**
3. **Qual evidência comprova que a entrega funciona?**

Você não precisa decorar comandos nem escolher cada skill. O agente identifica a
etapa atual, anuncia as transições e mantém o trabalho na mesma conversa.

## Uma única especificação

Cada entrega escolhida possui uma única fonte de referência:

```text
specs/specs/<NNNN>-<slug>/spec.md
```

`NNNN` é o número da entrega, como `0001`. O `slug` é um nome curto que ajuda a
reconhecer o assunto, como `recuperar-senha`.

Essa `spec.md` reúne:

- o problema e o resultado esperado;
- quem será afetado e quais regras precisam ser respeitadas;
- histórias, requisitos e limites;
- exemplos de comportamento escritos em BDD;
- decisões, riscos e plano técnico;
- tarefas, testes e evidências da execução;
- gates e estado atual da entrega.

Plano e tarefas ficam dentro da própria spec. O Specsfy não cria `plan.md` ou
`tasks.md`. Assim, um arquivo não fica contando uma versão antiga da entrega.

## Da ideia até o código

Nem todo texto precisa virar uma entrega imediatamente. O destino depende do
quanto você já decidiu:

- Uma **ideia** é uma captura rápida. Ela preserva seu texto em
  `specs/ideias/` sem perguntas e sem autorizar implementação.
- O **backlog** guarda algo que você quer organizar e refinar, mas ainda não
  escolheu como entrega. Ele vive em `specs/backlog/`.
- A **spec** representa uma entrega escolhida. A partir dela, definição, plano,
  testes, código e evidências passam a seguir o mesmo contrato.

O percurso mais completo fica assim:

```text
ideia → backlog → entrevista → spec → plano e RED → código → validação
```

Você também pode começar com “implemente recuperação de senha”. O agente
verifica o que falta e conduz as etapas necessárias antes de mexer no código.

## Os três atos

Os atos são grupos de trabalho. Cada um termina com um **gate**, que é um ponto
de controle baseado em evidência. Um **gate** aprovado não significa apenas
“parece bom”: significa que as condições daquela etapa foram verificadas.

### Antes dos atos: escolha o destino da ideia

**Objetivo:** preservar o pedido sem forçar uma entrega antes da hora.

**Sua participação:** você informa a ideia e decide quando vale refiná-la ou
promovê-la. Se pedir apenas para capturar, o agente não inicia uma entrevista.

**Prova técnica:** a captura recebe um arquivo próprio em `specs/ideias/`. Se
for escolhida para refinamento, passa ao backlog. Somente uma promoção
intencional cria a `spec.md` normativa.

Essa separação mantém a caixa de entrada leve e impede que toda observação se
transforme em código ou em uma especificação extensa.

### Ato I — Definir o que precisa mudar

**Objetivo:** entender o problema e transformar a intenção em comportamento
que possa ser conferido.

**Sua participação:** você responde apenas às dúvidas que realmente mudam a
entrega. O agente reaproveita tudo o que já foi dito, pergunta uma lacuna
importante por vez e não inventa requisitos quando faltar uma decisão.

**Prova técnica:** a spec registra finalidade, pessoas afetadas, requisitos,
limites e cenários BDD. A validação procura contradições, decisões em aberto e
dúvidas prioritárias.

O ato termina com:

```text
Definition Gate: Passed
```

Isso quer dizer que a definição está clara o suficiente para orientar um plano.
Ainda não quer dizer que a solução foi implementada.

### Ato II — Planejar e provar antes de implementar

**Objetivo:** decidir como a mudança será construída e demonstrar que os testes
conseguem detectar a ausência do novo comportamento.

**Sua participação:** você decide quando houver uma escolha material de produto,
risco ou estratégia. Detalhes técnicos comprováveis podem ser derivados do
código, da stack e das regras do projeto.

**Prova técnica:** o agente registra tarefas, contratos, dados, riscos e
reversibilidade na spec. Depois, transforma os cenários BDD em testes TDD
executáveis e observa o **RED**: uma falha causada pela funcionalidade que ainda
não existe.

O ato termina com:

```text
Plan Gate: Passed
```

O RED precisa falhar pelo motivo esperado. Erro de sintaxe, dependência ausente
ou ambiente quebrado não prova que o teste protege o comportamento.

### Ato III — Entregar e conferir o resultado

**Objetivo:** implementar cada tarefa e reunir evidências atuais de que a
entrega atende à definição.

**Sua participação:** você acompanha decisões novas ou mudanças de escopo. Não
precisa comandar cada ciclo de teste; o agente registra o que foi executado e
apresenta o resultado verificável.

**Prova técnica:** cada tarefa segue:

```text
RED → GREEN → REFACTOR
```

- **RED:** o teste falha pela razão esperada;
- **GREEN:** a menor implementação faz o teste passar;
- **REFACTOR:** o código é melhorado sem mudar o comportamento.

Depois, o agente executa o aceite, a regressão completa, verifica a
rastreabilidade entre requisito e teste, atualiza o contexto e reconstrói a
documentação aplicável.

O ato termina com:

```text
Delivery Gate: Passed
Status: Complete
```

`Complete` significa que a entrega possui código e evidência atual. Não é apenas
uma tarefa marcada como concluída.

## Como BDD e TDD trabalham juntos

BDD e TDD têm papéis diferentes e complementares.

O **BDD** descreve o comportamento em uma linguagem que produto,
desenvolvimento e testes conseguem discutir. Por exemplo:

```gherkin
Cenário: pessoa solicita recuperação de senha
  Dado que existe uma conta para o e-mail informado
  Quando a pessoa solicita a recuperação
  Então o sistema confirma o pedido sem revelar dados privados
```

Esse cenário deixa visível a regra e o resultado esperado, mas o texto Gherkin
não é executado como uma suíte separada pelo Specsfy.

O **TDD** transforma o comportamento em testes executáveis na ferramenta já
usada pelo projeto. Primeiro o teste falha pelo motivo correto; depois a
implementação faz o teste passar. Em resumo:

- BDD ajuda a definir **o comportamento que importa**;
- TDD comprova **que o código apresenta esse comportamento**.

Essa ligação evita dois extremos: uma descrição clara sem prova automática, ou
um teste técnico que não representa o que foi pedido.

## O agente conduz as transições

As skills dividem responsabilidades, mas você não precisa operar o fluxo como
uma lista de comandos. Quando uma etapa depende de outra, o agente:

1. informa de qual skill está saindo e para qual está indo;
2. explica a pendência que motivou a transição;
3. resolve a pendência no contexto correto;
4. retorna à etapa anterior quando necessário.

Por exemplo, se a implementação encontrar um teste ausente, o agente volta ao
planejamento e à preparação TDD, obtém um RED válido e só então retoma o código.
Ele não aprova um gate apenas para contornar a pendência.

## Mudanças durante o trabalho

Se o pedido mudar depois que a spec já existe, você pode explicar a alteração
em linguagem normal. A mudança entra na mesma `spec.md`; não é criada uma
segunda especificação.

O Specsfy reabre somente as provas que perderam validade:

- se mudou o comportamento, reabre definição, plano e entrega;
- se mudou somente a estratégia técnica, reabre plano e entrega;
- se apenas uma evidência ficou desatualizada, repete a validação necessária.

Use [`specsfy-base-update-spec`](skills/specsfy-base-update-spec.md) para esse
fluxo.

## Contexto que permanece entre entregas

Além da spec de cada entrega, o projeto mantém informações que valem para o
sistema inteiro:

- `PROJECT.md`: finalidade, capacidades e limites do projeto;
- `.specsfy/STACK.md`: tecnologias estruturais e suas evidências;
- `.specsfy/RULES.md`: regras confirmadas para o trabalho;
- `.specsfy/DATABASE.md`: mapa da persistência e das relações.

O agente consulta esse contexto antes de planejar e o revisa durante a
implementação. Assim, uma nova entrega não precisa redescobrir a arquitetura,
as convenções ou o banco desde o início.

## O que você encontra ao final

Uma entrega completa deixa um caminho auditável:

- a intenção e as decisões estão na spec;
- cada requisito aponta para critérios de aceite;
- os cenários BDD explicam o comportamento;
- os testes TDD demonstram o resultado no código;
- as tarefas registram execução e evidências;
- os gates mostram quais etapas foram realmente comprovadas;
- a documentação reflete o sistema implementado.

Para consultar esse estado sem alterar arquivos, use
[`specsfy-base-progress`](skills/specsfy-base-progress.md).

## Limites do método

O método não decide requisitos importantes sem você, não transforma toda ideia
em spec e não trata pesquisa como requisito aprovado. Também não aceita erro de
ambiente como RED nem substitui os testes e as ferramentas do seu projeto.

Agora siga a [instalação](installation.md) e faça o
[primeiro projeto](getting-started.md).
