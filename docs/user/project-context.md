# Contexto persistente do projeto

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | arquivos de contexto mantidos em cada projeto consumidor |
| Autoridade | localização, finalidade e regras de preservação desses arquivos |

## Papel

Explicar como manter uma descrição durável do projeto, seu stack, suas regras e
sua persistência para que pessoas e agentes compartilhem o mesmo contexto sem
criar uma segunda spec.

## Como usar

Execute `$specsfy-setup` depois de instalar o framework e sempre que quiser
verificar sua consistência. A skill detecta Laravel, Next.js e Astro por seus
manifests, sugere um modelo apropriado e garante esta estrutura:

```text
<projeto>/
├── PROJECT.md
└── .specsfy/
    ├── STACK.md
    ├── RULES.md
    └── DATABASE.md
```

Ela também reserva blocos delimitados para as diretrizes do Specsfy em
`AGENTS.md` e `CLAUDE.md`. Conteúdo fora desses blocos pertence ao usuário e é
preservado. A referência publicável das diretrizes vive em
[`specsfy-setup`](../../skills/specsfy-setup/).

| Arquivo | Conteúdo | Skill mantenedora |
| --- | --- | --- |
| `PROJECT.md` | história, finalidade, pessoas, capacidades e limites | `$specsfy-setup` cria o modelo; a equipe mantém a narrativa |
| `.specsfy/STACK.md` | tecnologias estruturais e evidências | `$specsfy-aux-stack` |
| `.specsfy/RULES.md` | regras explícitas confirmadas | `$specsfy-aux-rules` |
| `.specsfy/DATABASE.md` | fontes, tabelas, campos, relações e migrations | `$specsfy-aux-database` |

Os quatro modelos ficam em `.specsfy/templates/Project.md`, `Stack.md`,
`Rules.md` e `Database.md`, junto dos demais templates do framework.

Execute `$specsfy-aux-stack` após alterar frameworks, runtimes, ferramentas
estruturais ou persistência. Execute `$specsfy-aux-database` sempre que criar ou
alterar banco, schema, tabela, coleção, model persistente, campo, relação,
índice ou migration. Use `$specsfy-aux-rules` para formular e acrescentar uma
regra confirmada sem duplicar ou apagar regras anteriores.

## Monitoramento durante mudanças

O monitor é uma verificação executada pelas skills durante o fluxo, não um
daemon em segundo plano. Ele examina caminhos staged, unstaged e untracked:

```bash
python3 -B .agents/skills/specsfy-setup/scripts/monitor_context.py \
  --project . --check
```

| Sinal observado | Obrigação |
| --- | --- |
| manifest, lockfile ou configuração estrutural | atualizar `.specsfy/STACK.md` com `$specsfy-aux-stack` |
| banco, schema, model persistente, tabela, campo ou migration | atualizar `.specsfy/DATABASE.md` com `$specsfy-aux-database` |
| código da aplicação | revisar `PROJECT.md` |
| código da aplicação ou persistência | reconstruir `docs/` com `$specsfy-documentator` |
| instrução ou convenção | revisar `.specsfy/RULES.md` com `$specsfy-aux-rules` |

`PENDING` impede a conclusão da tarefa e do Delivery Gate. Quando uma mudança
de aplicação não altera história, finalidade, capacidades ou limites, registre
essa avaliação na evidência da tarefa e execute novamente com
`--acknowledge-project-no-change`. Para uma revisão de regras sem regra nova,
use `--acknowledge-rules-no-change` somente depois de registrar a justificativa.
Veja a topologia e o `--check` no guia de
[documentação técnica do sistema](system-documentation.md).

## Atualize quando

- a localização ou finalidade de um dos quatro arquivos mudar;
- uma skill mantenedora ganhar ou perder responsabilidade;
- a política de preservação dos blocos gerenciados mudar;
- um novo stack receber modelo próprio no setup.
- os sinais monitorados ou a política de bloqueio documental mudarem.

## Não use para

- substituir `specs/specs/<NNNN>-<slug>/spec.md`;
- registrar tarefas, gates ou aceite de uma fatia;
- copiar segredos, dados de produção ou valores de `.env`;
- tratar inferência de uma ferramenta como regra confirmada pelo usuário.

## Fonte da verdade e precedência

Schemas, migrations, manifests, lockfiles e configurações comprovam o estado
implementado. Os quatro arquivos sintetizam esse estado e o conhecimento humano
durável. A spec continua governando comportamento e mudança; `AGENTS.md` e
`CLAUDE.md` governam instruções dos agentes. Em divergência, preserve o conteúdo
observado, sinalize o conflito e corrija a fonte proprietária antes da síntese.

## Preservação e atualização

- O setup cria um arquivo de contexto somente quando ele ainda não existe.
- As auxiliares atualizam apenas blocos detectados delimitados e preservam
  seções humanas.
- Uma nova varredura nunca autoriza remover silenciosamente uma decisão humana.
- `DATABASE.md` usa tabelas Markdown para facilitar mapeamento e comparação.
- Valores sensíveis não são lidos nem registrados; cite somente nomes seguros
  de variáveis e caminhos das fontes.
