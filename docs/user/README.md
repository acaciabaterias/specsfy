# Guia completo do usuário

<p align="center">
  <picture>
    <source srcset="../../brand/logo/icon.svg" type="image/svg+xml">
    <img src="../../brand/logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>

O Specsfy ajuda você a transformar uma ideia em software testado sem espalhar
requisitos, planos e tarefas por vários arquivos. Você conversa normalmente
com o agente; as skills organizam o trabalho e mantêm uma única especificação
como referência.

Este guia ensina primeiro a lógica da metodologia, depois prepara o ambiente,
acompanha a primeira entrega e, por fim, apresenta operação e recursos
avançados. Você não precisa conhecer a implementação do framework.

## Leia online ou como ebook

Este mesmo percurso está disponível na edição portátil **v1.1.0**:

- [PDF](../../ebook/Specsfy-Guia-do-Usuario-v1.1.0.pdf), para leitura,
  compartilhamento e impressão;
- [EPUB](../../ebook/Specsfy-Guia-do-Usuario-v1.1.0.epub), para leitores
  digitais com fonte e tamanho ajustáveis.

Os dois formatos são reconstruídos a partir destas páginas. A versão vigente e
os hashes verificáveis ficam na [pasta do ebook](../../ebook/README.md).

## Percurso pedagógico

Siga as etapas abaixo na primeira leitura. Depois, use esta página como mapa
para voltar diretamente ao assunto de que precisar.

### 1. Entenda a metodologia

Comece pela [Metodologia](method.md). Ali você aprende a ideia central: cada
entrega mantém problema, requisitos, exemplos de comportamento, plano técnico,
tarefas, testes e evidências em uma única `spec.md`.

O trabalho acontece em três atos:

1. **Ato I — Definir:** entender e validar o que deve ser entregue.
2. **Ato II — Projetar e provar:** preparar tarefas e obter o RED, a falha
   esperada antes da implementação.
3. **Ato III — Entregar e validar:** implementar, obter testes verdes e
   registrar evidências.

### 2. Instale o Specsfy

Com o método entendido, siga a [Instalação](installation.md) para instalar o
CLI e preparar um projeto consumidor. A instalação cria a estrutura necessária
para trabalhar com specs, contexto e skills sem transformar este monorepo em
um projeto consumidor.

### 3. Faça a primeira entrega

Use [Primeiro projeto](getting-started.md) como tutorial guiado. Ele leva de um
pedido inicial até uma entrega validada sem exigir que você decore cada skill.

Se ainda não quiser iniciar a especificação:

- preserve um texto sem perguntas na [Caixa de entrada de ideias](ideas.md);
- refine e priorize uma proposta no [Backlog](backlog.md).

### 4. Aprofunde o fluxo base

O índice de [Skills base](skills/README.md) apresenta o fluxo completo. Leia
cada etapa nesta ordem:

1. [Capturar uma ideia](skills/specsfy-base-idea.md);
2. [Refinar no backlog](skills/specsfy-base-backlog.md);
3. [Conduzir a entrevista](skills/specsfy-base-interview.md);
4. [Criar a especificação](skills/specsfy-base-specify.md);
5. [Validar a definição](skills/specsfy-base-validate.md);
6. [Preparar as tarefas](skills/specsfy-base-tasks.md);
7. [Preparar TDD e BDD](skills/specsfy-base-tdd-bdd.md);
8. [Implementar](skills/specsfy-base-implement.md);
9. [Atualizar a especificação](skills/specsfy-base-update-spec.md);
10. [Consultar o progresso](skills/specsfy-base-progress.md).

Essas páginas explicam quando usar cada skill, como pedir em linguagem natural,
o resultado esperado, os erros comuns e o próximo passo.

### 5. Opere o projeto no dia a dia

Depois da primeira entrega, aprofunde somente o que fizer parte da sua rotina:

- [CLI e TUI](cli.md): comandos, interface visual e acompanhamento;
- [Contexto do projeto](project-context.md): stack, regras, banco e convenções;
- [Documentação do sistema](system-documentation.md): documentação técnica
  derivada da aplicação;
- [Mudanças posteriores](update-spec.md): como incorporar um novo pedido à
  mesma especificação.

### 6. Avance quando precisar

Os próximos guias são opcionais e fazem mais sentido depois que o fluxo base já
estiver familiar:

- [Especialistas](specialists.md), para conhecimento técnico adicional;
- [Uso avançado](advanced-usage.md), para automação e integrações;
- aplicação em projetos [Laravel](laravel.md), [Astro](astro.md) ou
  [Next.js](nextjs.md);
- [Mapa técnico](../develop/modules.md), para conhecer os módulos do monorepo;
- [Créditos](credits.md), para autoria e identidade do projeto.

Se você pretende contribuir ou modificar o próprio framework, continue no
[guia técnico](../develop/README.md). Ele é um percurso separado do uso em
projetos consumidores.

## Conversa contínua entre etapas

Quando uma etapa depende de outra skill, o agente anuncia a transição, resolve
a pendência e retoma o trabalho na mesma conversa. Você não precisa repetir o
pedido nem conduzir cada passagem manualmente.

## A ideia central em um exemplo

Imagine uma página de boas-vindas. Você pode preservar a ideia, refiná-la no
backlog e promovê-la até chegar a:

```text
specs/specs/0001-pagina-boas-vindas/spec.md
```

Em seguida, o agente valida a definição, organiza tarefas, prepara testes,
implementa e registra evidências nesse mesmo arquivo. Se depois surgir um
botão novo, a mudança retorna à mesma `spec.md` e reabre apenas os atos
afetados. Não são criados `plan.md`, `tasks.md` ou documentos normativos
paralelos.

Para começar esse percurso com orientação passo a passo, siga agora
[a Metodologia](method.md).
