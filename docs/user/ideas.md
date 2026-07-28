# Caixa de entrada de ideias

`specs/ideias/` recebe pensamentos antes de qualquer entrevista ou decisão de
produto. A captura é deliberadamente rápida: o agente não faz perguntas e não
transforma o texto em compromisso de entrega.

## Capturar

```text
Use $specsfy-base-idea para guardar esta ideia:
quero permitir que a pessoa continue um formulário em outro dispositivo.
```

O resultado usa o formato:

```text
specs/ideias/AAAA-MM-DD-HHMMSS-<slug>.md
```

Data e hora evitam uma fila numerada artificial e preservam a ordem real de
chegada. Se duas capturas tiverem o mesmo nome no mesmo segundo, o Specsfy
adiciona um sufixo sem sobrescrever a anterior.

## O que o arquivo organiza

- metadados e integridade do texto original;
- texto original completo;
- resumo processado;
- problema ou oportunidade;
- pessoas e valor percebidos;
- sinais de escopo, regras ou solução;
- riscos, dependências e direções possíveis;
- pontos a revisar no futuro;
- rastreabilidade para backlog ou spec derivados.

Declarações, inferências e lacunas permanecem identificadas. Campo sem base no
texto é marcado como não identificado; o agente não inventa respostas.

O texto será versionado no Git. Não inclua senhas, tokens, chaves privadas ou
dados pessoais sensíveis. Se o agente detectar um segredo evidente, ele não
grava a captura e pede apenas que o conteúdo sensível seja removido.

## Ideia, backlog e spec

```text
captura sem perguntas → backlog refinável → spec normativa
```

- `specs/ideias/` preserva o input;
- `specs/backlog/` organiza algo escolhido para refinamento;
- `specs/specs/<NNNN>-<slug>/spec.md` governa comportamento e entrega.

Uma captura pode permanecer indefinidamente na caixa de entrada. Quando quiser
avançar, use `$specsfy-base-backlog` ou `$specsfy-base-interview` com o caminho
do arquivo.

## Templates instalados

O CLI mantém os templates documentais em `.specsfy/templates/`:

```text
Idea.md
Backlog.md
Spec.md
Tasks.md
Project.md
Stack.md
Rules.md
Database.md
```

Alterações locais são protegidas pelo instalador e só são substituídas com
`--force`.
