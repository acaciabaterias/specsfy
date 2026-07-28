# Usar Specsfy com Next.js

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | aplicação da metodologia em projetos Next.js |
| Autoridade | catálogo e skill `specsfy-specialist-nextjs` |

## Papel

Adicionar fronteiras server/client, cache, mutations, rotas e deploy ao fluxo
Specsfy de uma aplicação Next.js.

## Como usar

### Pré-condições e detecção

O catálogo detecta Next.js pela dependência `next` em `package.json` ou por
`next.config.js`, `next.config.mjs` e `next.config.ts`. Confirme versão,
App/Pages Router, runtime, destino de deploy e flags antes de planejar.

## Instalação

```bash
specsfy skills detect --project .
specsfy skills add specsfy-specialist-nextjs --project .
```

Ou instale bases e recomendações detectadas:

```bash
specsfy install --project . --detected
```

## Passo a passo de uso

1. Conduza a ideia até a spec pelo [uso básico](basic-usage.md).
2. Peça ao agente para usar `$specsfy-specialist-nextjs` na fatia ativa.
3. Mapeie rota, layout, `loading`, `error`, `not-found` e boundaries de dados.
4. No App Router, mantenha componentes no servidor por padrão e mova ao cliente
   apenas o boundary que requer estado, eventos ou APIs do navegador.
5. Defina cache, revalidation, tags e comportamento dinâmico explicitamente.
6. Trate Server Actions e Route Handlers como superfícies públicas: valide
   autenticação, autorização e entrada em cada mutation.
7. Derive testes para estados, redirects, autorização, invalidação e isolamento
   de dados entre usuários.
8. Execute lint, typecheck, testes, build e runtime de produção conforme os
   scripts do `package.json`.

## O que o especialista acrescenta

- controle da fronteira entre Server e Client Components;
- prevenção de segredos e módulos server-only no bundle cliente;
- análise de waterfalls, streaming e recuperação de erro;
- cache como contrato compatível com a versão instalada;
- metadata, assets, bundle, imagens, fontes e Web Vitals.

## Resultado esperado

As decisões de renderização, cache e segurança ficam rastreadas pela spec e
provadas por testes e build na versão e no router realmente usados.

## Limites

- não presuma App Router ou semântica de cache sem confirmar a versão;
- não mova uma árvore inteira ao cliente por conveniência;
- não use middleware para lógica longa ou incompatível com o runtime;
- não assuma comportamento específico do host sem documentá-lo.

## Atualize quando

- a detecção do catálogo ou o nome da skill mudar;
- o fluxo, os padrões ou a validação do especialista mudar;
- o contrato público de instalação de especialistas mudar.

## Não use para

- escolher App Router, Pages Router ou runtime sem evidência;
- duplicar documentação versionada do Next.js;
- substituir scripts, configuração ou convenções da aplicação.

## Fonte da verdade e precedência

A skill pertence a
[`specialists/`](https://github.com/promovaweb/specsfy/tree/main/specialists/specsfy-specialist-nextjs).
Router, versão, runtime e scripts são comprovados por código, `package.json`,
lockfile e configuração do projeto consumidor.
