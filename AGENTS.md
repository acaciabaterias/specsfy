# Guia do monorepo Specsfy

Este `AGENTS.md` governa o monorepo oficial do Specsfy em
`/home/luizeof/specsfy`, publicado em
[`promovaweb/specsfy`](https://github.com/promovaweb/specsfy).

## Fronteiras Git e ownership

Todo o projeto compartilha uma única raiz Git. Os diretórios abaixo são módulos
com responsabilidades próprias, não repositórios, submódulos ou worktrees
independentes.

| Caminho | Responsabilidade |
| --- | --- |
| `./` | integração, automação e testes transversais |
| `brand/` | identidade visual e verbal |
| `skills/` | metodologia executável e skills base |
| `docs/` | documentação oficial para usuários e contexto transversal |
| `example/` | aplicação interna de validação |
| `specsfy/` | visão geral pública detalhada |
| `specialists/` | skills técnicas opcionais |
| `cli/` | instalação, TUI e progresso visual |

- Execute Git somente na raiz do monorepo.
- Mantenha regras de exclusão somente no `.gitignore` da raiz; módulos não
  possuem `.gitignore` próprio.
- Preserve mudanças preexistentes em qualquer módulo.
- Links internos usam caminhos relativos. Links públicos apontam para
  `https://github.com/promovaweb/specsfy` e, quando necessário, para o caminho
  do módulo em `tree/main/<diretório>`.
- Mudanças transversais formam uma única entrega coerente.

## Fonte da verdade

- Esta raiz desenvolve e integra a metodologia, mas não é um projeto consumidor:
  não crie `specs/` nela.
- `.agents/skills/` e `.claude/skills/` contêm somente as skills locais de
  documentação do projeto e release do CLI.
- Para documentar o próprio Specsfy, leia integralmente
  `.agents/skills/specsfy-monorepo-documentator/SKILL.md` e execute seu coletor.
- Para lançar ou retomar uma versão do CLI, leia integralmente
  `.agents/skills/specsfy-release-cli/SKILL.md`. A tag e o GitHub Release
  pertencem ao monorepo; os artefatos versionados do pacote ficam em `cli/`.
- Projetos consumidores mantêm sua fonte normativa em
  `specs/specs/<NNNN>-<slug>/spec.md`; ideias ainda não promovidas ficam em
  `specs/backlog/`.
- A metodologia vive em `skills/`; siga também `skills/AGENTS.md`.
- Especialistas vivem em `specialists/`; não os instale na raiz do monorepo.
- O CLI vive em `cli/` e recusa esta raiz como projeto consumidor.
- Detalhes operacionais da aplicação interna permanecem em `example/README.md`.

Não crie `plan.md`, `tasks.md`, `research.md`, `data-model.md` ou outra fonte
normativa paralela.

## Disciplina documental

- Toda criação ou alteração atualiza, na mesma entrega, a documentação aplicável.
- Documentação deriva das fontes executáveis e não duplica inventários de
  manifests, rotas, schemas ou testes.
- Decisões transversais vivem em `docs/context/`; guias públicos vivem em
  `docs/`.
- Use `docs/context/README.md` como roteador e leia apenas os contextos exigidos.

### ClickUp

Esta regra é local ao monorepo e não deve ser publicada nas skills instaladas
em projetos consumidores.

- Use o MCP ClickUp como caminho principal.
- Use `codex_apps.clickup` apenas como fallback.
- Não repita pelo fallback uma mutação já confirmada.

## Fluxo de uma mudança

1. Identifique os módulos e contextos afetados.
2. Inspecione instruções, status e diff da raiz.
3. Atualize o contrato integrado em BDD/TDD e observe RED.
4. Edite cada arquivo no módulo responsável.
5. Execute testes focais nos módulos e regressão na raiz.
6. Registre evidência nos testes e na documentação.
7. Revise o único diff integrado antes de concluir.

Mudança de comportamento reabre os Atos I–III. Mudança de plano reabre os Atos
II–III.

## Validação

Na raiz:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
```

Execute também os validadores declarados no `AGENTS.md` de cada módulo alterado.
Para uma skill:

```bash
cd skills
uv run --quiet --with pyyaml python \
  /home/luizeof/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  <nome>
```

## Critério de entrega

- uma única raiz Git e um único remoto `promovaweb/specsfy`;
- um único `.gitignore` central, com regras prefixadas pelo módulo;
- ownership de diretório correto;
- nenhuma referência ao antigo conjunto de repositórios;
- endpoints do CLI e links públicos apontam para o monorepo;
- BDD, TDD, regressão e rastreabilidade verdes;
- nenhum cache, placeholder ou fonte normativa paralela.
