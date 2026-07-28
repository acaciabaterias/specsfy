# Fluxo de Conversa

Use este roteiro para ajudar o usuario a criar uma interface sem transformar a conversa em formulario longo.

## 1. Identificar a tela

Determine a categoria principal:

- landing/public page;
- dashboard/app autenticado;
- formulario ou fluxo de coleta;
- tabela/lista/dados;
- artigo/conteudo;
- componente isolado.

Se o usuario ja colou um snippet, pule perguntas de descoberta e classifique o componente.

## 2. Definir objetivo

Pergunta util:

> Qual e a acao principal que esta tela precisa gerar?

Exemplos:

- capturar lead;
- vender plano;
- explicar produto;
- mostrar metricas;
- permitir edicao;
- conduzir contato;
- navegar para conteudo.

## 3. Definir usuario e densidade

Pergunta util:

> Essa interface e para visitante publico, cliente logado, operador interno ou admin?

Use a resposta para decidir:

- publico/marketing -> mais narrativa, prova visual, CTA;
- app interno -> mais densidade, filtros, estados, navegacao clara;
- admin -> tabelas, badges, acoes por linha, confirmacoes;
- onboarding/formulario -> etapas, validacao, progresso, feedback.

## 4. Escolher composicao

Abra [composition-map.md](composition-map.md) e defina a hierarquia com
`$specsfy-specialist-ui-design`.

Escolha uma sequencia inicial e comunique de forma simples:

```text
Vou montar como: hero -> beneficios -> prova social -> FAQ -> footer.
```

Ou:

```text
Vou montar como: app shell -> filtros -> tabela -> detalhes -> dialogs de acao.
```

## 5. Escolher referencias

Abra [catalog.md](catalog.md), liste apenas a família necessária e leia somente
os assets escolhidos.

Evite carregar todas as referencias de uma skill grande.

## 6. Implementar por incrementos

Ordem sugerida:

1. estrutura de layout;
2. secoes/componentes principais;
3. dados e estados;
4. acoes e feedback;
5. responsividade e dark mode;
6. acessibilidade;
7. validacao.

## 7. Pedir confirmacao apenas quando necessario

Nao pergunte sobre detalhes cosmeticos se o projeto ja indica padrao.

Pergunte quando houver risco de retrabalho alto:

- escolher entre dashboard e landing;
- escolher framework/rota de destino;
- decidir se instala dependencia;
- substituir design system existente;
- introduzir biblioteca nova.
