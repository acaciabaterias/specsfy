# Definir o MVP por milestones

Use `$specsfy-mvp-milestone-interviewer` (`specsfy-mvp-milestone-interviewer`)
para explorar o menor produto utilizável sem perder o caminho da conversa. A
skill lê `MVP.md` e `BRAND.md` da raiz do projeto. Quando o projeto é um
submódulo Git e esses arquivos não estão nele, ela os procura na raiz do Hub
que contém o submódulo. Cada resposta fica preservada em uma Inbox da mesma
sessão. Quando você escolher uma opção pelo número, a captura registra o texto
da opção escolhida, e não somente `1`, `2` ou `3`.

## Quando usar

Use antes de criar um conjunto de specs para um produto novo ou quando o MVP
ainda não tem uma jornada confirmada. Se `MVP.md` existir, a skill o importa
como `specs/milestones/M01.md`, separa seus temas em Inboxes e cria um backlog
candidato para cada Inbox. Nenhum desses arquivos existentes é substituído.

Um arquivo no projeto tem prioridade. O Hub só entra na busca quando o projeto
é um submódulo Git e o arquivo local está ausente. Assim, um `MVP.md` ou
`BRAND.md` específico do projeto não é trocado pelo contexto compartilhado.

Cada rodada traz uma pergunta numerada. Abaixo dela, você recebe três ou mais
sugestões, `Escrever outra resposta`, `Gere outras opções` e `Avançar`
desde a primeira rodada.

Quando a jornada indicar que o sistema precisa guardar informações, a skill
pergunta, uma por vez, sobre cada informação ausente ou ambígua durante a
entrevista do backlog correspondente. São no máximo oito perguntas por área;
para continuar, você precisa pedir mais e indicar quantas deseja responder. As
respostas confirmadas ficam em `.specsfy/DATABASE.md`.

## Como descrever a tarefa

Peça: “use o entrevistador de MVP para organizar os marcos do meu sistema de
leads”.

## Exemplo passo a passo

```text
MVP.md → M01 + Inboxes + backlogs candidatos → entrevista de cada backlog
→ milestones sincronizadas
```

## O que esperar

O importador cria `M01`, Inboxes e vários backlogs candidatos, um para cada
tema do MVP. A própria skill carrega `$specsfy-02-backlog` para entrevistar cada
item, chama `$specsfy-data-discovery` quando houver dados ambíguos e retorna à
fila até entrevistar todos. Depois sincroniza os milestones e só chama
`$specsfy-03-specify` para itens cuja promoção você autorizar. A skill não cria
código durante a conversa.

## Erros comuns

- pedir tarefas técnicas antes de entrevistar todos os backlogs gerados;
- misturar uma hipótese da conversa com o texto que foi registrado;
- esperar que um backlog candidato seja promovido sem entrevista.

## Próximo passo

Leia [Milestones](../milestones.md) para conhecer arquivos e sincronização.
