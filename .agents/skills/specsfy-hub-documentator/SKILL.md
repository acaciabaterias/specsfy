---
name: specsfy-hub-documentator
description: Manter a documentação oficial do próprio projeto Specsfy no workspace orquestrador composto pelos oito repositórios da organização. Use somente no hub de desenvolvimento quando o pedido for documentar o Specsfy, reconciliar mudanças transversais, produzir ou revisar documentação técnica em docs/context/, ou criar e atualizar guias para usuários em specsfy/docs, inclusive a instalação do CLI e do framework. Não use em projetos consumidores; para reconstruir o diretório docs/ de uma aplicação, use specsfy-documentator.
---

# Documentar o hub Specsfy

1. Executar a partir da raiz do workspace orquestrador:

```bash
python3 -B .agents/skills/specsfy-hub-documentator/scripts/collect_hub_evidence.py \
  --workspace .
```

2. Interromper se o coletor informar que o diretório não representa o hub
   Specsfy. Não adaptar esta skill para uma raiz parcial ou projeto consumidor.
3. Ler integralmente o `AGENTS.md` do workspace e o `AGENTS.md` de cada owner
   afetado. Quando o owner não possuir instrução própria, aplicar o
   `AGENTS.md` do workspace. Tratar as oito raízes Git como repositórios
   independentes.
4. Ler `docs/context/README.md` e somente os contextos roteados pela mudança.
5. Ler [o padrão documental](references/documentation-standard.md) antes de
   editar topologia, classificação ou percurso de leitura.
6. Comparar cada afirmação com a fonte proprietária: código, teste, manifest,
   configuração, schema, documentação operacional ou contexto normativo.
7. Atualizar cada percurso afetado; atualizar ambos quando a mudança alcançar
   arquitetura e jornada pública:
   - documentação técnica transversal em `docs/context/`;
   - guias para usuários em arquivos temáticos na raiz de `docs/`.
   Criar `docs/installation.md` quando ausente e mantê-lo como guia temático da
   instalação do CLI e do framework no projeto consumidor. Derivar seus
   pré-requisitos e comandos de `cli/` e o conjunto instalado de `cli/` e
   `skills/`; manter `docs/README.md` e `docs/cli.md` apontando para esse guia.
8. Somente `docs/`, raiz Git `specsfy/docs`, recebe a documentação oficial
   publicada. Alterar outro repositório apenas quando seu próprio contrato
   executável ou sua documentação de owner também mudou.
9. Usar links relativos dentro de `docs/` e URLs
   `https://github.com/specsfy/<repositorio>` para atravessar raízes Git.
10. Executar testes focais declarados pelo owner. Quando `docs/` não publicar
    suíte própria, executar os contratos integrados que inspecionam seus
    arquivos a partir do hub. Rodar a regressão integrada e revisar `git status`
    e `git diff` separadamente nas oito raízes antes de concluir.

## Política de evidência

- Registrar como fato apenas o que uma fonte proprietária comprovar.
- Distinguir decisão vigente, estado implementado, inferência e lacuna.
- Preservar o estado observado quando fontes divergirem e indicar o conflito.
- Não copiar inventários extensos que já derivam de manifests, rotas, schemas ou
  testes; explicar responsabilidade e apontar para a fonte.
- Não copiar segredos, valores de ambiente, dados de produção ou conteúdo
  interno sem finalidade documental.
- Não criar `plan.md`, `tasks.md`, `research.md`, `data-model.md` ou `specs/`
  na raiz do hub.

## Fronteira com o documentador do consumidor

Esta skill documenta a metodologia, a arquitetura do hub e seus guias oficiais
em `specsfy/docs`. Quando o destino for `<projeto>/docs/` de uma aplicação
consumidora, carregar `$specsfy-documentator`; não reutilizar o padrão editorial
do hub como gerador de inventário da aplicação.

## Exclusividade local

- Manter a fonte desta skill somente em
  `specsfy/dev/.agents/skills/specsfy-hub-documentator/`.
- Expor a mesma fonte ao Claude pelo symlink
  `.claude/skills/specsfy-hub-documentator`; não manter uma segunda cópia.
- Não criar skill homônima em `specsfy/skills`, não adicioná-la ao catálogo do
  framework e não incluí-la no instalador ou na TUI do CLI.
- Em pedido somente de auditoria, executar coleta e leitura sem editar; publicar
  arquivos apenas quando a pessoa pedir criação, atualização ou reconciliação.
