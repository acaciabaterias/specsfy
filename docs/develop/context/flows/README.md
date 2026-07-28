# Fluxos transversais

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | índice |
| Escopo | mapas que atravessam módulos |
| Autoridade | critérios e navegação de fluxos transversais |

## Papel

Indexar mapas que atravessam módulos e explicar como documentá-los sem criar uma
segunda fonte de requisitos.

## Como usar

Consulte quando uma jornada depender de três ou mais componentes ou quando a
ordem de eventos for difícil de compreender apenas por texto linear.

## Atualize quando

- um fluxo transversal for criado, movido ou removido;
- seus componentes ou links para specs mudarem;
- o contrato de documentação de fluxos mudar.

## Não use para

- copiar Gherkin, regras e exceções de uma feature;
- documentar chamadas internas triviais;
- manter fluxo sem spec ou fonte executável relacionada.

## Fonte da verdade e precedência

`specs/specs/<NNNN>-<slug>/spec.md` governa comportamento, erros e aceite. Código e testes
demonstram a execução. Um documento de fluxo apenas mostra sequência,
responsabilidades e links para essas fontes.

## Fluxos transversais

- [Release do CLI](cli-release.md): prepara pacote, changelog e executável em
  `cli/`, cria a tag no commit validado do monorepo e publica as mesmas notas no
  GitHub Release.

O fluxo canônico do método permanece na
[visão arquitetural](../architecture/README.md) porque é uma invariante do
projeto, não uma feature independente.

Antes dos três atos, o fluxo de entrada é:

```text
ideia → backlog → interview → spec
```

Backlog e entrevista preparam a decisão; somente a spec governa comportamento,
gates, tarefas e evidência.

Durante os três atos, as etapas são bidirecionais:

```text
backlog ↔ interview → specify ↔ validate → tasks ↔ tdd-bdd → implement → documentator ↔ progress
                         ↑       ↑            ↑
                         └──── update-spec ───┘
```

Cada skill resolve pendências pertencentes ao próprio escopo. Quando o estado
exigir outra responsabilidade, ela anuncia origem, destino, motivo e resultado
esperado e carrega automaticamente a skill responsável na mesma conversa, sem
pedir confirmação. O mesmo protocolo governa avanço, retorno e retomada.
Depois de cada tarefa de código, `implement` entrega o estado observado a
`documentator`, que reconstrói `<projeto>/docs/` antes de a tarefa ou o gate
final ser concluído. A pessoa também pode acionar `documentator` diretamente,
sem spec ou implementação recente.

Pedido surgido depois da definição retorna a `update-spec`. A skill chama
`interview` quando faltar decisão, `validate` quando mudar comportamento e
`tasks` quando mudar somente o plano. Teste ou RED ausente chama `tdd-bdd` com
o plano pendente; se o plano já estava aprovado, `tasks` reabre o Ato II antes
de chamar `tdd-bdd`. Depois da correção, a etapa que detectou a pendência é
retomada automaticamente. Handoffs não autorizam instalação, deploy, publicação
ou ação destrutiva, que continuam exigindo autorização específica.

Crie um arquivo somente quando o mapa tiver gatilho de leitura e atualização
próprio. Ao criá-lo, adicione a rota neste índice e no
[roteador de contexto](../README.md).

## Contrato de um fluxo

Cada fluxo deve declarar:

- gatilho e estado inicial;
- componentes e responsabilidade de cada etapa;
- ordem, resultado e falha transversal;
- spec ou specs que governam o comportamento;
- testes ou fontes executáveis que demonstram a sequência;
- condição que exige atualização do mapa.
