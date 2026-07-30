# Informações permanentes do projeto

O Specsfy separa a descrição durável do sistema das especificações de cada
mudança. O arquivo `PROJECT.md` explica a finalidade da aplicação, enquanto
quatro documentos em `.specsfy/` registram a stack, as instruções confirmadas,
a persistência observada no código e os pacotes instalados.

Execute `$specsfy-setup` depois de instalar o framework ou quando precisar
verificar os quatro contextos iniciais. A skill detecta Laravel, Next.js e
Astro pelos manifests e sugere o modelo correspondente.
`$specsfy-documentator` acrescenta e atualiza `PACKAGES.md`. Juntas, as skills
mantêm esta estrutura:

```text
<projeto>/
├── PROJECT.md
└── .specsfy/
    ├── STACK.md
    ├── RULES.md
    ├── DATABASE.md
    └── PACKAGES.md
```

O setup também reserva blocos delimitados para as diretrizes do Specsfy em
`AGENTS.md` e `CLAUDE.md`. Conteúdo fora desses blocos pertence ao usuário e é
preservado. A referência publicável das diretrizes vive em
[`specsfy-setup`](../../skills/specsfy-setup/).

| Arquivo | Conteúdo | Skill mantenedora |
| --- | --- | --- |
| `PROJECT.md` | finalidade e capacidades | `$specsfy-setup` cria o modelo |
| `.specsfy/STACK.md` | stack e evidências | `$specsfy-aux-stack` |
| `.specsfy/RULES.md` | regras explícitas confirmadas | `$specsfy-aux-rules` |
| `.specsfy/DATABASE.md` | persistência e relações | `$specsfy-aux-database` |
| `.specsfy/PACKAGES.md` | pacotes npm e Composer com finalidade | `$specsfy-documentator` |

Os quatro modelos ficam em `.specsfy/templates/Project.md`, `Stack.md`,
`Rules.md` e `Database.md`, junto dos demais templates do framework. Para
personalizar um deles, mantenha o mesmo nome em
`.specsfy/templates/custom/`; essa cópia tem precedência e não é alterada pelo
CLI.

Execute `$specsfy-aux-stack` após alterar frameworks, runtimes, ferramentas
estruturais ou persistência. Execute `$specsfy-aux-database` sempre que criar ou
alterar banco, schema, tabela, coleção, model persistente, campo, relação,
índice ou migration. Use `$specsfy-aux-rules` para formular e acrescentar uma
regra confirmada sem duplicar ou apagar regras anteriores.

## Monitoramento durante mudanças

O monitor é executado pelas skills no início e no fim de uma mudança. Ele lê os
arquivos staged, unstaged e untracked do Git para descobrir qual documento
precisa ser revisto, mas não permanece como daemon em segundo plano:

```bash
python3 -B .agents/skills/specsfy-setup/scripts/monitor_context.py \
  --project . --check
```

| Sinal observado | Obrigação |
| --- | --- |
| manifest, lockfile ou configuração | `$specsfy-aux-stack` revisa `STACK.md` |
| manifest ou lockfile npm/Composer | `$specsfy-documentator` reconstrói `PACKAGES.md` e `docs/` |
| schema, model ou migration | `$specsfy-aux-database` revisa `DATABASE.md` |
| código da aplicação | revisar `PROJECT.md` |
| aplicação ou persistência | `$specsfy-documentator` reconstrói `docs/` e `PACKAGES.md` |
| instrução ou convenção | `$specsfy-aux-rules` revisa `RULES.md` |

`PENDING` impede a conclusão da tarefa e do Delivery Gate. Quando uma mudança
de aplicação não altera história, finalidade, capacidades ou limites, registre
essa avaliação na evidência da tarefa e execute novamente com
`--acknowledge-project-no-change`. Para uma revisão de regras sem regra nova,
use `--acknowledge-rules-no-change` somente depois de registrar a justificativa.
Veja a topologia e o `--check` no guia de
[documentação técnica do sistema](system-documentation.md).

## Preservação e atualização

- O setup cria um arquivo de informações somente quando ele ainda não existe.
- As auxiliares atualizam apenas blocos detectados delimitados e preservam
  seções humanas.
- Uma nova varredura nunca autoriza remover silenciosamente uma definição
  humana.
- `DATABASE.md` usa tabelas Markdown para facilitar mapeamento e comparação.
- `PACKAGES.md` deriva de manifests, lockfiles e metadados locais, preservando
  texto humano fora do bloco gerado.
- Valores sensíveis não são lidos nem registrados. Cite somente nomes seguros
  de variáveis e caminhos das fontes.

O estado implementado é comprovado pelas fontes do próprio projeto. Os
manifests e lockfiles mostram a stack, enquanto schemas e migrations mostram a
persistência. Os cinco documentos resumem essas evidências e as definições
humanas que precisam permanecer entre mudanças. Eles não substituem a
`spec.md`, não registram gates e nunca devem copiar segredos, valores de `.env`
ou registros de produção.
