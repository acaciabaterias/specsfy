# Usar Specsfy com Laravel

`$specsfy-specialist-laravel` acrescenta verificações próprias do Laravel ao
fluxo do Specsfy. A spec continua governando a mudança, e o especialista segue
as convenções e a versão comprovadas pelo projeto.

## Confirmar a detecção

O catálogo detecta Laravel por `artisan`, `composer.json` ou pela dependência
`laravel/framework`. Confirme a versão e as extensões em `composer.json` e
`composer.lock`. Uma API só deve orientar a implementação quando existir na
versão usada pela aplicação.

## Instalação

Na raiz do projeto, `--detected` instala o framework e o especialista quando o
catálogo reconhece Laravel:

```bash
specsfy install --project . --detected
```

Para revisar a recomendação sem instalar arquivos, use `skills detect`. A saída
deve incluir `specsfy-specialist-laravel` quando `artisan` ou a dependência do
framework for encontrada:

```bash
specsfy skills detect --project .
```

Quando o nome já estiver confirmado, `skills install` instala somente o
especialista Laravel e registra os arquivos gerenciados:

```bash
specsfy skills install specsfy-specialist-laravel --project .
```

## Aplicar na spec

1. Capture ou promova a ideia pelo [primeiro projeto](getting-started.md).
2. Peça ao agente para usar `$specsfy-specialist-laravel` na fatia ativa.
3. Confirme a versão, extensões, convenções locais e o caminho da requisição.
4. Na definição e no plano, registre autorização e validação. Quando a mudança
   alcançar persistência ou execução assíncrona, inclua transações,
   idempotência, filas, falhas e migrations.
5. Derive testes para caminho feliz, autorização, validação, efeitos e falhas.
6. Implemente controllers finos e mantenha as regras na camada já adotada pelo
   projeto. Inspecione as consultas e o N+1 quando a quantidade de relações
   puder aumentar o tempo da resposta.
7. Execute os checks existentes. Em Laravel com Pest, o CLI oferece:

```bash
specsfy test --project .
```

O CLI detecta `artisan` e `pestphp/pest`, chama `php artisan test` e preserva o
exit code. Ele não recebe uma string arbitrária de shell.

## O que o especialista acrescenta

- contratos HTTP, Form Requests, policies, resources e bindings.
- Eloquent, eager loading, casts e transações conscientes.
- jobs idempotentes, tentativas, backoff e tratamento de falha.
- migrations compatíveis com volume, locks, rollback e deploy misto.
- verificação de queues, scheduler, cache, configuração e ambiente.

## Resultado esperado

A spec continua sendo a fonte normativa, enquanto os testes e a implementação
consideram as falhas possíveis do Laravel observado no projeto e na versão
instalada.

## Limites

- não aplique a skill a PHP sem Laravel.
- não presuma APIs pela versão mais recente da documentação.
- não execute migration, deploy ou comando operacional sem autorização.
- não confie apenas na validação ou autorização da interface.

Não use esse especialista para PHP sem Laravel nem para fixar uma versão que o
projeto não comprova. O código, `composer.json`, `composer.lock`, os testes e a
configuração local permanecem como evidência do estado da aplicação.
