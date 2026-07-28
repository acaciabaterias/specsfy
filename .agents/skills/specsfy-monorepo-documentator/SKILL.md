---
name: specsfy-monorepo-documentator
description: Manter a documentação oficial do próprio projeto Specsfy no monorepo promovaweb/specsfy. Use somente na raiz oficial quando o pedido for documentar o Specsfy, reconciliar mudanças transversais, revisar docs/context/ ou atualizar guias em docs/. Não use em projetos consumidores; para reconstruir a documentação de uma aplicação, use specsfy-documentator.
---

# Documentar o monorepo Specsfy

1. Executar na raiz:

```bash
python3 -B .agents/skills/specsfy-monorepo-documentator/scripts/collect_monorepo_evidence.py \
  --workspace .
```

2. Interromper se o coletor informar que o diretório não representa o monorepo
   oficial.
3. Ler integralmente o `AGENTS.md` da raiz e as instruções dos módulos afetados.
4. Ler `docs/context/README.md` e apenas os contextos roteados pela mudança.
5. Ler [o padrão documental](references/documentation-standard.md) antes de
   editar topologia, classificação ou percurso de leitura.
6. Comparar cada afirmação com código, teste, manifest, configuração, schema,
   documentação operacional ou contexto normativo do módulo responsável.
7. Atualizar ambos os percursos quando a mudança alcançar arquitetura e uso:
   - documentação técnica transversal em `docs/context/`;
   - guias para usuários em `docs/`.
   Manter `docs/installation.md` como guia canônico de instalação.
8. Usar links relativos entre módulos. URLs públicas usam
   `https://github.com/promovaweb/specsfy`.
9. Executar testes focais dos módulos, regressão integrada e revisar o único
   status e diff do monorepo.

## Política de evidência

- Registrar como fato apenas o que uma fonte atual comprovar.
- Distinguir decisão vigente, estado implementado, inferência e lacuna.
- Preservar o estado observado quando fontes divergirem.
- Não copiar inventários extensos derivados de manifests, rotas, schemas ou
  testes.
- Não copiar segredos, dados de produção ou conteúdo interno sem finalidade.
- Não criar `plan.md`, `tasks.md`, `research.md`, `data-model.md` ou `specs/` na
  raiz.

## Fronteira com o documentador do consumidor

Esta skill documenta a metodologia, a arquitetura do monorepo e seus guias
oficiais. Para `<projeto>/docs/` de uma aplicação consumidora, carregue
`$specsfy-documentator`.

## Exclusividade local

- Manter a fonte somente em
  `.agents/skills/specsfy-monorepo-documentator/`.
- Expor a mesma fonte ao Claude pelo symlink
  `.claude/skills/specsfy-monorepo-documentator`.
- Não criar skill homônima em `skills/` nem incluí-la no instalador.
- Em pedido somente de auditoria, coletar e ler sem publicar arquivos.
