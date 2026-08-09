# Arquitetura das skills

Skills são unidades executáveis de orientação. Cada uma possui gatilho,
responsabilidade, limites, fluxo, validação e relações com outras skills.

## Catálogos

| Diretório | Conteúdo |
| --- | --- |
| `skills/` | método base, setup, auxiliares e documentador do consumidor |
| `specialists/` | conhecimento técnico opcional |
| `.agents/skills/` | operações exclusivas do monorepo |

Skills locais do monorepo não são instaladas em consumidores.

## Estrutura

Uma skill típica usa:

```text
<nome>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
└── assets/
```

Somente `SKILL.md` é obrigatório em todos os casos. Os demais diretórios
existem quando a responsabilidade exige.

## Frontmatter e descoberta

`SKILL.md` declara:

```yaml
---
name: specsfy-08-exemplo
description: "Use quando...; não use para..."
---
```

`name` deve coincidir com o diretório. `description` é o contrato de
descoberta: contém gatilhos observáveis e limites negativos. Se duas skills
disputam a mesma solicitação, corrija as descrições e os limites antes de
adicionar mais instruções.

`agents/openai.yaml` fornece o prompt padrão e menciona `$<nome-da-skill>`.

## Corpo e referências

O corpo usa instruções imperativas e mantém o fluxo essencial perto da ação.
Conteúdo extenso, padrões externos e matrizes de decisão ficam em
`references/`, com indicação explícita de quando devem ser lidos.

Scripts automatizam transformações determinísticas. Eles retornam códigos úteis,
não instalam globalmente e não realizam ações destrutivas por padrão.

Templates de documentos gerenciados vivem em `skills/templates/` e são
publicados juntos em `.specsfy/templates/`. Nos projetos consumidores, um
arquivo homônimo em `.specsfy/templates/custom/` tem precedência. Esse
diretório pertence ao usuário e não entra no lock nem nas atualizações do CLI.
Assets internos permanecem materiais de saída específicos de uma skill, nunca
uma segunda fonte normativa.

## Handoff

As skills base participam da orquestração:

```text
Pendência detectada → Transição automática → execução da skill de destino
→ Retomada automática
```

O handoff é usado quando a responsabilidade muda. A skill de origem não executa
silenciosamente o trabalho da vizinha. A skill de destino relê a spec e valida
suas próprias pré-condições.

`specsfy-01-inbox` é a exceção de entrada: ela registra a entrada antes de
qualquer handoff, não pergunta e apenas sugere a próxima etapa. Esse limite
impede que uma anotação simples se transforme em refinamento implícito.

`specsfy-02-backlog` é a responsável exclusiva pelas perguntas de decisão
material. `specify`, `update-spec` e `validate` fazem handoff para seu ciclo e
retomam depois. O ciclo reanalisa cada resposta, não possui limite de perguntas
e oferece `avançar` depois da décima pergunta, preservando qualquer lacuna
restante como definição pendente.

## Relação das skills base

```text
inbox → backlog → specify → validate
       → tasks → tdd-bdd → implement → progress
                         ↑
                    update-spec
```

`update-spec` pode reabrir definição, plano ou entrega. `progress` é somente
leitura. `documentator` atua depois de mudanças implementadas no consumidor e
projeta `docs/` junto de `.specsfy/PACKAGES.md`.

## Instalação

`cli/src/installer.ts` define o conjunto instalado. O instalador:

- clona somente o diretório necessário do monorepo.
- delega materialização ao instalador `skills`.
- mantém `skills-lock.json` e fingerprints Specsfy.
- preserva conteúdo local alterado sem `--force`.
- mescla blocos gerenciados em `AGENTS.md` e `CLAUDE.md`.
- recusa a raiz oficial como consumidor.

Os arquivos `Inbox.md`, `Backlog.md`, `Spec.md`, `Tasks.md`, `Project.md`,
`Stack.md`, `Rules.md` e `Database.md` são gerenciados individualmente, com
fingerprints próprios e proteção contra sobrescrita local. A resolução usada
pelas skills segue `custom/<Nome>.md`, template gerenciado e, somente no
monorepo, `skills/templates/<Nome>.md`.

## Alterar uma skill

1. escreva ou atualize o contrato BDD/TDD.
2. observe RED.
3. altere `SKILL.md`, scripts, referências ou assets do owner.
4. sincronize fixtures instaladas quando o teste exigir.
5. execute a suíte do módulo.
6. rode `quick_validate.py`.
7. atualize a página de usuário e este contexto quando a interface mudar.

## Inventário de pacotes do consumidor

`specsfy-documentator/scripts/build_documentation.mjs` percorre os manifests npm
e Composer fora de árvores geradas. O script combina dependências diretas com
entradas transitivas de `package-lock.json` e `composer.lock`, usa descrições
locais quando disponíveis e escreve o bloco reconstruível de
`.specsfy/PACKAGES.md`. O modo `--check` trata esse arquivo como parte do mesmo
contrato de atualização de `docs/`.

`specsfy-setup/scripts/monitor_context.mjs` encaminha mudanças em manifests ou
lockfiles para o documentador. O inventário é derivado e não substitui os
manifests nem autoriza instalar, atualizar ou remover dependências.

## Validação

O validador verifica frontmatter, nome, metadata e estrutura. Testes focais
devem verificar o comportamento específico. Validação estrutural não prova a
metodologia.
