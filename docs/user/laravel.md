# Usar Specsfy com Laravel

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | aplicação da metodologia em projetos Laravel |
| Autoridade | catálogo e skill `specsfy-specialist-laravel` |

## Papel

Adicionar critérios Laravel ao fluxo Specsfy sem substituir a spec da fatia,
as convenções do projeto ou a versão comprovada pelos manifests.

## Como usar

### Pré-condições e detecção

O catálogo detecta Laravel por `artisan`, `composer.json` ou pela dependência
`laravel/framework`. Confirme a versão e as extensões em `composer.json` e
`composer.lock` antes de usar uma API do framework.

## Instalação

Na raiz do projeto:

```bash
specsfy install --project . --detected
```

Confira a recomendação antes, se preferir:

```bash
specsfy skills detect --project .
```

Para instalar explicitamente:

```bash
specsfy skills add specsfy-specialist-laravel --project .
```

## Passo a passo de uso

1. Capture ou promova a ideia pelo [primeiro projeto](getting-started.md).
2. Peça ao agente para usar `$specsfy-specialist-laravel` na fatia ativa.
3. Confirme a versão, extensões, convenções locais e o caminho da requisição.
4. Na definição e no plano, trate autorização, validação, transação,
   idempotência, filas, falhas e migrations quando aplicáveis.
5. Derive testes para caminho feliz, autorização, validação, efeitos e falhas.
6. Implemente controllers finos e mantenha regras no boundary adotado pelo
   projeto; inspecione consultas e N+1 quando cardinalidade importar.
7. Execute os checks existentes. Em Laravel com Pest, o CLI oferece:

```bash
specsfy test --project .
```

O CLI detecta `artisan` e `pestphp/pest`, chama `php artisan test` e preserva o
exit code. Ele não recebe uma string arbitrária de shell.

## O que o especialista acrescenta

- contratos HTTP, Form Requests, policies, resources e bindings;
- Eloquent, eager loading, casts e transações conscientes;
- jobs idempotentes, tentativas, backoff e tratamento de falha;
- migrations compatíveis com volume, locks, rollback e deploy misto;
- verificação de queues, scheduler, cache, configuração e ambiente.

## Resultado esperado

A spec continua sendo a fonte normativa, enquanto testes e implementação
consideram os riscos Laravel observados no projeto e na versão instalada.

## Limites

- não aplique a skill a PHP sem Laravel;
- não presuma APIs pela versão mais recente da documentação;
- não execute migration, deploy ou comando operacional sem autorização;
- não confie apenas na validação ou autorização da interface.

## Atualize quando

- a detecção do catálogo ou o nome da skill mudar;
- o fluxo, os padrões ou a validação do especialista mudar;
- o runner Laravel exposto pelo CLI mudar.

## Não use para

- documentar PHP sem Laravel;
- fixar uma versão de Laravel não comprovada pelo projeto;
- substituir a documentação operacional da aplicação.

## Fonte da verdade e precedência

A skill e seus padrões pertencem a
[`specsfy-specialist-laravel`](../../specialists/specsfy-specialist-laravel/).
O estado do projeto é comprovado por código, `composer.json`, `composer.lock`,
testes e configuração locais.
