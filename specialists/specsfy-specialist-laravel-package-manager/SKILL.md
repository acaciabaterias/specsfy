---
name: specsfy-specialist-laravel-package-manager
description: Gerenciar pacotes Composer Laravel recebidos por URL do GitHub, com documentação, instalação autorizada e registro em `docs/packages/`.
---

# Gestor de pacotes Laravel

## Quando usar

- Use quando a tarefa receber uma URL de repositório GitHub de um pacote para
  uma aplicação Laravel.
- Use também quando um pacote Composer já instalado precisar de uma ficha de
  uso ou quando `composer.json`, `composer.lock` e `docs/packages/` estiverem
  fora de sincronia.
- Não use para pacotes npm, para PHP sem Laravel ou para publicar uma
  biblioteca no Packagist.

## Fluxo

1. Confirme a raiz do projeto e normalize a URL HTTPS do GitHub para
   `github.com/<organização>/<repositório>`. Aceite somente segmentos com
   letras minúsculas, números, ponto, sublinhado ou hífen; recuse URLs que não
   apontem para um repositório GitHub identificável.
2. Leia as instruções locais, `composer.json`, `composer.lock`,
   `.specsfy/PACKAGES.md`, `docs/packages/README.md` e as fichas existentes
   antes de propor qualquer pacote ou comando. Considere os pacotes já instalados antes de procurar uma alternativa nova.
3. Consulte no repositório informado o `composer.json`, o README, a
   documentação de configuração, a versão publicada e os exemplos de uso.
   Registre separadamente o que a fonte declara, o que o projeto local mostra
   e o que ainda não foi confirmado.
4. Identifique o nome Composer, a versão do PHP, as versões do Laravel, os
   requisitos adicionais, o comando de instalação, os arquivos de
   configuração, os comandos de publicação e a forma de teste. Se o
   repositório não expuser um pacote Composer compatível, pare antes de
   alterar o projeto e explique a lacuna. Se o pacote não estiver publicado no
   Packagist, confira `repositories` no manifest e peça autorização específica
   antes de acrescentar uma origem VCS.
5. Procure o pacote em `composer.json`, `composer.lock`, `vendor/composer/` e
   no código. Se ele já estiver instalado, reutilize-o e não execute outro
   `composer require`.
6. Quando o pacote ainda não existir e a solicitação atual autorizar a
   instalação, execute na raiz do projeto `composer require <vendor/nome>`.
   Use `--dev` somente quando o próprio projeto tratar o pacote como
   dependência de desenvolvimento. Não execute comandos de pós-instalação
   copiados do README sem conferir sua finalidade e autorização.
7. Crie ou atualize `docs/packages/<vendor>-<nome>.md` com nome Composer,
   versão do lockfile, URL GitHub, finalidade, instalação, configuração, uso
   observado no projeto, testes e fontes consultadas. Preserve notas humanas
   fora da seção gerenciada.
8. Crie ou atualize `docs/packages/README.md` como índice de todos os pacotes
   Composer declarados pelo projeto, com versão, finalidade curta e link para
   cada ficha. Aponte para `.specsfy/PACKAGES.md` quando a pessoa precisar da
   relação completa, incluindo dependências transitivas.

## Padrões

- `composer.lock` informa a versão instalada; nunca derive uma versão apenas
  da tag mais recente do GitHub ou de uma restrição do manifest.
- O nome da ficha usa o nome Composer normalizado, com `/` convertido em `-`.
  A mesma ficha deve continuar sendo atualizada quando a versão mudar.
- O índice lista dependências de produção e desenvolvimento separadamente e
  não transforma uma dependência transitiva em escolha do projeto.
- Cada ficha informa o ponto de entrada real usado pela aplicação, como
  provider, facade, middleware, command, migration, config ou classe, quando
  esse ponto existir no código local.
- Comandos de instalação, publicação e teste aparecem acompanhados da razão
  para executá-los e do arquivo que deve mudar.
- Nunca copie segredos, valores de `.env`, código inteiro do pacote ou
  documentação extensa de terceiros para `docs/packages/`.

## Antipadrões

- Instalar antes de ler o `composer.json` e o lockfile: pode introduzir uma
  versão incompatível ou repetir uma dependência já presente.
- Tratar qualquer repositório PHP como pacote Laravel: isso mistura biblioteca
  genérica, aplicação e extensão sem identificar o contrato Composer.
- Executar `php artisan vendor:publish`, migrations ou scripts do pacote sem
  confirmar o efeito e a autorização: esses comandos podem alterar arquivos,
  banco ou configuração.
- Criar uma ficha genérica baseada somente no README: a documentação deixa de
  explicar como o pacote aparece no projeto consumidor.

## Validação

- Confirme que a URL, o nome Composer, a versão e os requisitos aparecem em
  fontes primárias ou nos arquivos locais correspondentes.
- Execute `composer validate --strict` e confira `composer show <vendor/nome>`
  quando o pacote estiver instalado.
- Rode os testes, formatter e análise estática já disponíveis no projeto; não
  introduza um runner novo só para validar o pacote.
- Confira que `docs/packages/README.md` lista cada dependência direta do
  `composer.json`, que cada link aponta para uma ficha existente e que a ficha
  informa quando a finalidade ainda não foi confirmada.
- Verifique links, comandos, nomes de configuração e exemplos contra a versão
  instalada. Não declare compatibilidade, segurança ou funcionamento sem uma
  fonte ou teste correspondente.

## Skills relacionadas

- `$specsfy-specialist-laravel` orienta o uso do pacote dentro de HTTP,
  Eloquent, filas, autorização e testes Laravel.
- `$specsfy-specialist-technical-research` ajuda a comparar documentação,
  versões e fontes primárias quando o repositório não esclarecer uma dúvida.

Leia [references/standards.md](references/standards.md) para o contrato das
fichas, a hierarquia de fontes e os comandos Composer aplicáveis.
