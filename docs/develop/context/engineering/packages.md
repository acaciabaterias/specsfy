# Política de pacotes

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | dependências de desenvolvimento e execução |
| Autoridade | política de adoção, atualização e remoção de pacotes |

## Papel

Definir como dependências são avaliadas, introduzidas, atualizadas e removidas
sem transformar este documento em inventário de versões.

## Como usar

Leia antes de adicionar import de terceiro ou ferramenta necessária ao
desenvolvimento, teste ou publicação.

## Atualize quando

- a política de dependências mudar;
- um pacote se tornar estrutural;
- uma exceção de segurança ou compatibilidade for aceita.

## Não use para

- copiar a lista de dependências transitivas;
- registrar versão já presente em manifest;
- autorizar pacote sem teste e justificativa.

## Fonte da verdade e precedência

Manifests e lockfiles são as fontes executáveis de pacotes e versões. Este
documento registra somente finalidade, política e restrições. Na ausência de
manifest, comandos explícitos revelam dependências efêmeras.

Os manifests de `example/` pertencem à aplicação interna de validação em
`example/`. Eles são a fonte das dependências PHP e JavaScript daquele
aplicativo, não um catálogo de pacotes obrigatórios para usar o Specsfy.

## Pacotes estruturais

| Pacote ou ferramenta | Papel | Forma atual |
| --- | --- | --- |
| Behave | executar aceite Gherkin | fornecido de forma efêmera por `uv` |
| PyYAML | validar metadata de skills | fornecido de forma efêmera por `uv` |
| Textual | renderizar a TUI do CLI | manifest e lockfile de `cli/` |
| Hatchling | construir a distribuição Python | build-system de `cli/` |

## Política de dependências

- Justificar finalidade e alternativa baseada na biblioteca padrão.
- Cobrir o contrato introduzido com teste.
- Definir fonte de versão e estratégia de atualização.
- Avaliar licença, segurança, manutenção e compatibilidade.
- Remover dependência que não possua mais consumidor.
- Não documentar pacote transitivo como escolha arquitetural.
- Alterar pacote de `example/` somente com teste da capacidade exercitada e
  atualização de sua documentação operacional na mesma entrega.
- Alterar pacote do CLI somente no repositório `cli/`, com lockfile,
  teste da TUI e build da distribuição.
