# Usar Specsfy com Astro

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | aplicação da metodologia em projetos Astro |
| Autoridade | catálogo e skill `specsfy-specialist-astro` |

## Papel

Adicionar decisões de renderização, conteúdo, ilhas e performance ao fluxo
Specsfy de um site Astro.

## Como usar

### Pré-condições e detecção

O catálogo detecta Astro pela dependência `astro` em `package.json` ou pelos
arquivos `astro.config.mjs` e `astro.config.ts`. Descubra no projeto a versão,
o output mode, o adapter, as integrações e as fontes de conteúdo.

## Instalação

```bash
specsfy skills detect --project .
specsfy skills add specsfy-specialist-astro --project .
```

Para instalar o framework e as recomendações detectadas em uma chamada:

```bash
specsfy install --project . --detected
```

## Passo a passo de uso

1. Conduza a ideia até a spec conforme o [uso básico](basic-usage.md).
2. Peça ao agente para usar `$specsfy-specialist-astro` na fatia ativa.
3. Classifique cada rota afetada como estática, sob demanda ou endpoint.
4. Mantenha HTML estático por padrão e escolha uma diretiva `client:*` somente
   para a interação que precisa de hidratação.
5. Modele conteúdo com schemas e relações explícitas; defina cache, headers,
   imagens e metadados quando aplicáveis.
6. Crie testes derivados do Gherkin para rotas, conteúdo inválido e
   comportamento hidratado.
7. Execute `astro check`, a suíte do projeto, o build de produção e o preview no
   runtime do adapter disponível no projeto.

## O que o especialista acrescenta

- escolha explícita entre static, on-demand, island e endpoint;
- proteção contra transporte de dados sensíveis para ilhas;
- validação de slugs, relações e conteúdo;
- semântica, canonical, sitemap e dados estruturados;
- inspeção de payload cliente, Core Web Vitals e compatibilidade do adapter.

## Resultado esperado

A fatia preserva a fonte normativa Specsfy e torna observáveis a estratégia de
renderização, a hidratação necessária, os contratos de conteúdo e a validação
no runtime alvo.

## Limites

- não escolha SSR sem necessidade de sessão, personalização ou frescor;
- não suponha APIs de Node em adapters edge;
- não valide apenas no servidor de desenvolvimento;
- confirme scripts e comandos disponíveis no `package.json`.

## Atualize quando

- a detecção do catálogo ou o nome da skill mudar;
- o fluxo, os padrões ou a validação do especialista mudar;
- o contrato público de instalação de especialistas mudar.

## Não use para

- prescrever um adapter ou modo de saída sem evidência;
- duplicar a documentação oficial do Astro;
- substituir scripts e convenções do projeto consumidor.

## Fonte da verdade e precedência

A skill pertence a
[`specsfy-specialist-astro`](../specialists/specsfy-specialist-astro/).
Versão, adapter, scripts e integrações pertencem aos manifests, lockfiles e
configuração do projeto consumidor.
