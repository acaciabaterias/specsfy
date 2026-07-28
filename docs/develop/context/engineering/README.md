# Contexto de engenharia

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../../../brand/logo/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../../../../brand/logo/logo-light.svg">
    <img src="../../../../brand/logo/logo-light.svg" alt="Logo oficial do Specsfy" width="180">
  </picture>
</p>

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | índice |
| Escopo | práticas e ferramentas de engenharia |
| Autoridade | roteamento para escolhas e políticas de implementação |

## Papel

Direcionar pessoas e agentes para o contexto exato de stack, dependências,
convenções ou testes sem exigir a leitura de todo o diretório.

## Como usar

Escolha uma folha pela mudança observável. Leia mais de uma somente quando a
decisão atravessar seus escopos.

## Atualize quando

- uma folha de engenharia for criada, consolidada ou removida;
- o gatilho de leitura ou atualização de uma folha mudar;
- um assunto adquirir responsabilidade independente.

## Não use para

- repetir regras das folhas;
- listar todos os arquivos ou pacotes;
- registrar comportamento de feature.

## Fonte da verdade e precedência

Este índice governa apenas o roteamento. As folhas governam decisões
transversais; manifests, lockfiles, testes e configurações mostram o estado
executável.

## Roteamento de engenharia

| Assunto | Leia quando | Atualize quando |
| --- | --- | --- |
| Tecnologias estruturais | [stack.md](stack.md) | uma escolha ou responsabilidade de stack mudar |
| Dependências | [packages.md](packages.md) | política ou pacote estrutural mudar |
| Padrões de implementação | [conventions.md](conventions.md) | convenção transversal mudar |
| Estratégia de verificação | [testing.md](testing.md) | runner, nível de teste ou gate mudar |
