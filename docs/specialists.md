# Skills especialistas

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | catálogo técnico opcional e instalação sob demanda |
| Autoridade | uso público de `specialists/` |

## Papel

Separar o método `specsfy-base-*` do contexto técnico
`specsfy-specialist-*`, permitindo instalar somente o conhecimento necessário
em cada projeto consumidor.

## Como usar

Detecte tecnologias e revise a sugestão:

```bash
specsfy skills detect
```

Instale nomes explícitos:

```bash
specsfy skills add \
  specsfy-specialist-laravel \
  specsfy-specialist-postgres \
  specsfy-specialist-redis
```

As skills base podem propor um especialista. Se ele já estiver instalado,
anunciam a transição automática e o carregam na mesma conversa. Se estiver
ausente, a instalação recebe autorização específica; o handoff não instala nada
automaticamente.

## Atualize quando

- uma skill entrar, sair ou mudar de responsabilidade;
- o prefixo, detecção ou modo de instalação mudar;
- padrões oficiais relevantes mudarem.

## Não use para

- redefinir o fluxo dos três atos;
- criar uma spec ou substituir a fonte normativa do projeto;
- instalar todo o catálogo por padrão;
- copiar versões de dependências mantidas em manifests.

## Fonte da verdade e precedência

Diretórios, `SKILL.md`, referências, metadata e `catalog.json` vivem em
[`specialists/`](https://github.com/promovaweb/specsfy/tree/main/specialists). Esta página
orienta usuários sem duplicar o conteúdo operacional de cada skill.

## Catálogo por domínio

| Domínio | Especialistas |
| --- | --- |
| backend e dados | Laravel, Supabase, Postgres, Redis e APIs web |
| frontend | React, Astro, Next.js, TypeScript e Tailwind CSS |
| interface | shadcn/ui, UI, UX e acessibilidade web |
| plataforma | Docker, Docker Swarm, Ansible e engenharia de entrega |
| qualidade | segurança, observabilidade e performance |
| design técnico | arquitetura e modelagem de domínio |
| engenharia | code review, debugging, prototipação, pesquisa e conflitos Git |

Cada especialista inclui workflow, padrões, validação e referências oficiais.
Use especialistas relacionados em conjunto apenas quando seus boundaries forem
realmente tocados.

## Relação com as bases

- `specsfy-base-interview` identifica necessidade.
- `specsfy-base-specify` registra requisitos e NFRs.
- `specsfy-base-validate` seleciona lentes de revisão.
- `specsfy-base-tasks` usa checklists técnicos para decompor trabalho.
- `specsfy-base-tdd-bdd` preserva RED/GREEN.
- `specsfy-base-implement` executa no contexto da stack.
- `specsfy-base-update-spec` revisa requisitos e NFRs afetados por pedido tardio.
- `specsfy-base-progress` identifica contexto e executa a transição automática.

Especialista complementa conhecimento; nunca avança gate por presença.
