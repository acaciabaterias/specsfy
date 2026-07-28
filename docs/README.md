# Documentação do Specsfy

<p align="center">
  <picture>
    <source srcset="../brand/icons/icon.svg" type="image/svg+xml">
    <img src="../brand/icons/icon.png" alt="Ícone do framework Specsfy" width="128">
  </picture>
</p>

O módulo `docs/` publica a documentação final do Specsfy para o usuário.

A porta de entrada e a visão geral do projeto estão em
[`specsfy/`](../specsfy/). A metodologia base
está em [`skills/`](../skills/); especialistas
opcionais estão em
[`specialists/`](../specialists/).

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | índice |
| Escopo | documentação final para o usuário e contexto transversal de manutenção |
| Autoridade | portal da documentação; cada documento de destino define seu próprio escopo |

## Papel

Organizar a documentação publicada do método e permitir que pessoas encontrem
conceitos, guias, decisões e fontes autorizadas sem depender do workspace de
desenvolvimento.

O diretório [`context/`](context/README.md) mantém decisões transversais usadas
por pessoas mantenedoras e agentes. O diretório
[`decisions/`](decisions/README.md) preserva o histórico arquitetural.

## Como usar

Para conhecer o projeto, comece pela
[visão geral](../specsfy/). Para aplicar ou manter o
método:

1. use este portal para localizar a documentação;
2. consulte o [roteador de contexto](context/README.md) quando a dúvida envolver
   arquitetura, engenharia, dados ou vocabulário;
3. consulte o [índice de decisões](decisions/README.md) para entender a
   motivação histórica de uma escolha;
4. abra o [catálogo de skills](../skills/) para executar
   a metodologia;
5. siga o [Guia de instalação](installation.md) para instalar o CLI e o
   framework;
6. conduza a primeira fatia pelo [uso básico](basic-usage.md);
7. use [Atualizar uma especificação](update-spec.md) quando lembrar de algo
   depois da definição;
8. avance para [seleção técnica e automação](advanced-usage.md) quando
   necessário;
9. use o [CLI e a TUI](cli.md) para operar e acompanhar projetos;
10. mantenha o [contexto persistente do projeto](project-context.md);
11. reconstrua a [documentação técnica do sistema](system-documentation.md);
12. mantenha a [documentação oficial do monorepo](monorepo-documentation.md) ao evoluir o
   próprio Specsfy;
13. registre ideias ainda abertas no [backlog](backlog.md);
14. instale [skills especialistas](specialists.md) somente quando necessárias;
15. consulte os guias de [Laravel](laravel.md), [Astro](astro.md) ou
    [Next.js](nextjs.md) quando a stack exigir;
16. use o [mapa dos módulos](repositories.md) e os
    [créditos](credits.md) para navegar e atribuir corretamente.

## Conversa contínua entre etapas

Você não precisa copiar o comando da próxima skill. Quando uma etapa termina ou
encontra uma pendência de outra responsabilidade, o agente:

1. informa `Pendência detectada` quando houver algo a resolver;
2. anuncia a `Transição automática`, com origem, destino, motivo e resultado
   esperado;
3. carrega imediatamente a skill responsável sem pedir confirmação;
4. continua na mesma conversa, preservando o contexto;
5. depois de corrigir uma pendência anterior, anuncia a `Retomada automática` e
   volta à etapa que a detectou.

O protocolo vale tanto para avançar quanto para retornar a uma etapa anterior.
O handoff não exige confirmação. Instalação de especialista, deploy, publicação
e ações destrutivas continuam exigindo autorização própria.

## Atualize quando

- surgir uma nova categoria de documentação final;
- um guia for criado, movido ou substituído;
- a hierarquia, a autoridade ou as regras de manutenção mudarem;
- uma decisão transversal alterar o modo como o usuário aplica o método.

## Não use para

- manter a implementação das skills ou scripts;
- guardar specs, tarefas ou evidências de uma entrega;
- publicar ativos de marca;
- definir instruções do monorepo;
- duplicar o roteamento técnico de `context/README.md`.

## Fonte da verdade e precedência

O módulo `docs/` governa a documentação final. As demais autoridades são:

- comportamento de uma fatia: `specs/specs/<NNNN>-<slug>/spec.md` no projeto que aplica o
  método;
- metodologia executável: [`skills/`](../skills/);
- visão geral pública:
  [`specsfy/`](../specsfy/);
- identidade: [`brand/`](../brand/);
- orquestração e testes integrados:
  [`promovaweb/specsfy`](https://github.com/promovaweb/specsfy);
- contexto vigente: documento específico em [`context/`](context/README.md);
- motivação histórica: ADR em [`decisions/`](decisions/README.md).

Quando fontes divergirem, não escolha silenciosamente. Preserve o estado
observado e corrija primeiro a fonte proprietária.

## Como a documentação está organizada

| Camada | Responsabilidade |
| --- | --- |
| `README.md` | portal da documentação final |
| `backlog.md` | captura de ideias e promoção para entrevista/spec |
| `installation.md` | instalação do CLI e do framework no projeto consumidor |
| `basic-usage.md` | primeira fatia, dos requisitos à entrega comprovada |
| `update-spec.md` | incorporação de pedidos surgidos depois da definição |
| `advanced-usage.md` | especialistas, automação, atualização e reabertura |
| `cli.md` | comandos, atualização e interface terminal |
| `laravel.md` | aplicação do método em projetos Laravel |
| `astro.md` | aplicação do método em projetos Astro |
| `nextjs.md` | aplicação do método em projetos Next.js |
| `project-context.md` | projeto, stack, regras e mapa de dados persistentes |
| `system-documentation.md` | reconstrução técnica do projeto consumidor |
| `monorepo-documentation.md` | documentação técnica e guias oficiais do próprio Specsfy |
| `specialists.md` | catálogo técnico opcional |
| `repositories.md` | responsabilidades e públicos dos módulos |
| `credits.md` | autoria, comunidade e identidade |
| `context/README.md` | roteamento seletivo do contexto transversal |
| `context/project.md` | finalidade e limites normativos |
| `context/glossary.md` | vocabulário canônico |
| `context/architecture/` | raízes, módulos e dependências |
| `context/engineering/` | stack, pacotes, convenções e testes |
| `context/data/` | persistência, migrations e privacidade |
| `context/flows/` | fluxos que atravessam módulos |
| `decisions/` | motivação e consequências históricas |

Os índices explicam onde encontrar conteúdo. Os documentos normativos definem
seu escopo. Skills, scripts, testes e configurações comprovam o estado
executável em seus repositórios proprietários.

## Como navegar

1. Comece pela [visão geral do Specsfy](../specsfy/).
2. Use este portal para escolher a classe de documentação.
3. Consulte o [roteador operacional](context/README.md) para selecionar somente
   os contextos exigidos pela sua dúvida.
4. Siga links adicionais apenas quando o documento selecionado declarar uma
   dependência real.
5. Volte ao [módulo de skills](../skills/) para
   executar ou inspecionar a metodologia.

## Autoridade das fontes

| Informação | Fonte autorizada |
| --- | --- |
| visão geral do projeto | `specsfy/` |
| documentação final | `docs/` |
| metodologia executável | `skills/` |
| identidade | `brand/` |
| aplicação interna e documentação operacional | `example/` |
| orquestração e testes integrados | `promovaweb/specsfy` |
| decisão transversal vigente | documento específico em `context/` |
| motivação histórica | ADR em `decisions/` |
| comportamento de uma fatia | `specs/specs/<NNNN>-<slug>/spec.md` no projeto correspondente |
| estado implementado | código, testes, manifests e configurações |

## Onde registrar cada informação

| Informação nova ou alterada | Registre em |
| --- | --- |
| tutorial, guia ou referência final | `docs/` |
| regra ou decisão transversal vigente | contexto selecionado por [context/README.md](context/README.md) |
| motivação e alternativas arquiteturais | ADR indexado em [decisions/README.md](decisions/README.md) |
| comportamento, aceite, plano ou tarefa | `specs/specs/<NNNN>-<slug>/spec.md` do projeto |
| skill, script, referência operacional ou asset | `skills/` |
| cor, tipografia, logo ou voz | `brand/` |
| visão geral resumida | `specsfy/` |
| aplicação interna e documentação operacional | `example/` |
| regra de integração do monorepo | `AGENTS.md` |

Registre cada fato em uma única fonte autorizada. Nos demais lugares, use links.

## Quando criar um documento

Crie um arquivo somente quando:

- existe conteúdo real, atual e independente;
- o assunto possui público e gatilhos próprios de leitura;
- natureza, escopo e autoridade podem ser declarados com precisão;
- um índice existente pode tornar o arquivo alcançável;
- o conteúdo não duplica uma spec, skill, fonte executável ou outro contexto.

## Como manter a documentação

- leia a fonte normativa e o contexto aplicável antes de editar;
- mantenha uma formulação autorizada e substitua repetições por links;
- atualize índices ao criar, mover, dividir ou remover documentos;
- preserve motivação histórica em ADRs e contexto vigente no presente;
- valide links, âncoras, alcançabilidade e contratos;
- use o histórico do Git para autoria e tempo;
- remova explicações obsoletas em vez de acumular versões contraditórias;
- revise `docs/` junto ao diff integrado do monorepo.

## Mapa da documentação

| Necessidade | Destino |
| --- | --- |
| conhecer o projeto | [Visão geral](../specsfy/) |
| aplicar a metodologia | [Skills](../skills/) |
| registrar e amadurecer uma ideia | [Backlog](backlog.md) |
| instalar o CLI e o framework | [Guia de instalação](installation.md) |
| entregar a primeira fatia | [Uso básico](basic-usage.md) |
| adicionar, remover, corrigir ou mudar um pedido já definido | [Atualizar uma especificação](update-spec.md) |
| combinar especialistas e automação | [Uso avançado](advanced-usage.md) |
| operar e acompanhar | [CLI e TUI](cli.md) |
| aplicar em Laravel | [Laravel](laravel.md) |
| aplicar em Astro | [Astro](astro.md) |
| aplicar em Next.js | [Next.js](nextjs.md) |
| manter história, stack, regras e banco | [Contexto persistente](project-context.md) |
| documentar arquitetura, código, banco, testes e pacotes | [Documentação técnica do sistema](system-documentation.md) |
| reconciliar os módulos e documentar o Specsfy | [Documentação oficial do monorepo](monorepo-documentation.md) |
| especializar por tecnologia | [Skills especialistas](specialists.md) |
| escolher o repositório correto | [Mapa dos repositórios](repositories.md) |
| consultar autoria e identidade | [Créditos](credits.md) |
| selecionar contexto técnico | [Contexto do projeto](context/README.md) |
| consultar decisões históricas | [Decisões](decisions/README.md) |
| usar a identidade oficial | [Marca](../brand/) |
| contribuir com a integração | [Monorepo](https://github.com/promovaweb/specsfy) |
