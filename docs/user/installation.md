# Instalação do Specsfy

## Classificação

| Campo | Valor |
| --- | --- |
| Natureza | normativo |
| Escopo | instalação do CLI e do framework em um projeto consumidor |
| Autoridade | interfaces públicas de `cli/` e `skills/` |

## 1. Instale o CLI

O CLI requer Python 3.11 ou superior. Baixe o executável diretamente de
`get.specsfy.dev` para a pasta de comandos do seu usuário:

```bash
mkdir -p "$HOME/.local/bin"
curl -fL get.specsfy.dev -o "$HOME/.local/bin/specsfy"
chmod +x "$HOME/.local/bin/specsfy"
```

Confira a instalação:

```bash
specsfy --version
```

Se o terminal ainda não encontrar o comando, inclua a pasta no `PATH` da sessão
e tente novamente:

```bash
export PATH="$HOME/.local/bin:$PATH"
specsfy --version
```

Para atualizar o CLI depois, repita o download. O novo arquivo substitui o
executável anterior:

```bash
curl -fL get.specsfy.dev -o "$HOME/.local/bin/specsfy"
chmod +x "$HOME/.local/bin/specsfy"
```

## 2. Prepare seu projeto

Entre no projeto em que você quer usar o Specsfy e execute:

```bash
cd caminho/do/projeto
specsfy install --project .
```

O comando prepara o projeto para trabalhar com a metodologia:

- instala o fluxo base em `.agents/skills/specsfy-base-*`;
- adiciona setup, documentação e contexto para o agente entender o projeto;
- publica o contrato central em `.specsfy/Spec.md`;
- adiciona templates, exemplos e registros técnicos dentro de `.specsfy/`;
- integra orientações gerenciadas a `AGENTS.md` e `CLAUDE.md` sem apagar seu
  conteúdo.

Essa etapa não cria uma especificação de produto. Ela apenas deixa o ambiente
pronto para você iniciar a primeira entrega.

## 3. Confirme que está pronto

Na raiz do projeto, execute:

```bash
specsfy skills list
specsfy progress --project .
```

O primeiro comando deve listar as skills instaladas. O segundo pode informar
zero specs; isso é esperado em um projeto novo e confirma que o CLI consegue
ler o ambiente.

Você também pode abrir a interface visual:

```bash
specsfy
```

## Se algo não funcionar

- **`specsfy: command not found`:** adicione `$HOME/.local/bin` ao `PATH` e
  abra um novo terminal.
- **Python incompatível:** confirme com `python3 --version`; o CLI requer
  Python 3.11 ou superior.
- **Falha ao instalar skills:** disponibilize o comando `skills` ou o `npx`,
  usado como alternativa pelo CLI.
- **Arquivo local protegido:** uma instalação repetida preserva
  customizações. Revise a diferença antes de usar `--force`, pois essa opção
  descarta o conteúdo protegido.

## Próximo passo

Siga o [primeiro projeto](getting-started.md) para transformar um pedido em uma
entrega validada. Depois, consulte o [guia do CLI e da TUI](cli.md) quando
precisar de comandos, progresso ou opções avançadas.
