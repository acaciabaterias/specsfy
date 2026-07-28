# Uso avançado do Specsfy

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | seleção técnica, automação, atualização e retomada de mudanças |
| Autoridade | interfaces de `cli/`, `skills/` e `specialists/` |

## Papel

Combinar o método base com especialistas, saída estruturada, monitoramento e
reabertura disciplinada dos gates em projetos já operacionais.

## Como usar

### Pré-condições

- jornada de [uso básico](basic-usage.md) compreendida;
- CLI e framework instalados;
- projeto consumidor selecionado explicitamente.

## Detecte e instale contexto técnico

Veja as recomendações sem alterar o projeto:

```bash
specsfy skills detect --project .
```

Instale o framework e todos os especialistas detectados:

```bash
specsfy install --project . --detected
```

Ou componha uma seleção explícita:

```bash
specsfy install --project . \
  --specialist specsfy-specialist-laravel \
  --specialist specsfy-specialist-postgres
```

Em projeto já preparado, adicione somente especialistas:

```bash
specsfy skills add specsfy-specialist-laravel --project .
```

Detecção é recomendação baseada em manifests, dependências e marcadores do
projeto. Revise a seleção antes de instalar. Especialistas orientam decisões
técnicas; não criam specs nem avançam gates.

## Automatize a leitura de progresso

```bash
specsfy progress --project . --json
specsfy progress --project . --watch --interval 0.5 --json
```

O JSON contém `summary` e `specs`. Com `--watch`, um snapshot novo aparece
somente quando o conteúdo das specs muda. Use essa saída em painéis e
automação de leitura; ela não deve ser usada para editar gates.

## Ajuste a atualização visual

```bash
specsfy config show --project .
specsfy config set --project . --watch-interval 0.5
```

A configuração vive em `<projeto>/.specsfy/config.json` e preserva chaves
desconhecidas. Consulte todos os recursos no [guia do CLI](cli.md).

## Atualize sem perder customizações

```bash
uv tool upgrade specsfy-cli
specsfy skills update --project .
```

O CLI usa fingerprints para distinguir conteúdo gerenciado intacto de
customização local. Divergência bloqueia atualização ou remoção. Use `--force`
somente após revisar a diferença e decidir descartar o conteúdo protegido.

## Reabra a entrada correta

Quando lembrar de algo depois da definição, use a entrada explícita:

```text
Use $specsfy-base-update-spec em
specs/specs/<NNNN>-<slug>/spec.md:
quero adicionar, remover, corrigir ou mudar este pedido.
```

Quando um requisito observável muda, a skill reabre a definição; Definition,
Plan e Delivery Gate precisam de evidência nova. Quando apenas o plano técnico
muda, ela reabre o Ato II e o Ato III. Uma entrada alterada invalida provas
posteriores construídas sobre a versão anterior, mas preserva tarefas e
evidências que continuam compatíveis.

As skills fazem transições e retomadas na mesma conversa. Esse handoff não
amplia autorização para instalar, publicar, fazer deploy ou executar ação
destrutiva.

Consulte [Atualizar uma especificação](update-spec.md) para a classificação
completa e exemplos em linguagem comum.

## Resultado esperado

O projeto mantém framework e especialistas deliberadamente selecionados,
automação somente de leitura e gates coerentes com a versão atual da entrada.

## Limites

- `--force` pode descartar customizações protegidas;
- `--detected` depende do catálogo e do estado observado no projeto;
- a TUI e o progresso projetam estado, não substituem a spec;
- especialista não substitui descoberta de versão, convenções ou riscos locais.

## Atualize quando

- argumentos públicos de seleção, progresso ou configuração mudarem;
- proteções de atualização ou remoção mudarem;
- a política de reabertura dos atos mudar.

## Não use para

- substituir o tutorial de primeira instalação;
- escolher especialista sem observar o projeto;
- automatizar escrita em gates ou specs.

## Fonte da verdade e precedência

Comandos e proteções pertencem a
[`cli/`](https://github.com/promovaweb/specsfy/tree/main/cli), o método base a
[`skills/`](https://github.com/promovaweb/specsfy/tree/main/skills) e o catálogo opcional a
[`specialists/`](https://github.com/promovaweb/specsfy/tree/main/specialists).
