---
name: specsfy-specialist-interface-experience
description: Analisar o sistema atual e orientar a descoberta, o plano e a entrega de interfaces completas, bonitas e compatíveis com a stack existente.
---

# Experiência de interface

## Quando usar

- Acionar ao criar ou alterar tela, dashboard, lista, formulário, jornada ou
  CRUD usado por pessoas.
- Acionar antes de UX, UI e implementação para entender o sistema existente e
  organizar a conversa sobre a interface.
- Não usar para endpoint, job ou mudança interna sem superfície para pessoas.

## Fluxo

1. Carregar `$specsfy-setup` e ler `.specsfy/STACK.md`,
   `.specsfy/PACKAGES.md`, manifests, instruções locais e documentação atual.
   Executar `node .agents/skills/specsfy-setup/scripts/inspect_interface.mjs
   --project <raiz>` para localizar rotas, componentes e tecnologias antes da
   leitura detalhada.
2. Examinar as telas, fluxos, rotas, componentes, conteúdo, permissões, estados
   e testes ligados à área afetada. Registrar o que a pessoa já consegue fazer,
   o que deve permanecer e o que a entrega muda.
3. Identificar framework, roteamento, primitives, estilos, formulários e runner
   de testes usados pelo projeto. Seguir essas fontes e não trocar tecnologia
   ou biblioteca sem confirmação da pessoa.
4. Aplicar o contrato central de perguntas: perguntar uma lacuna por rodada
   sobre telas, fluxo de informação, formulário, formato de ação e composição.
   Oferecer opções textuais compatíveis com o sistema atual, `Escrever outra
   resposta`, `Gere outras opções` e `Avançar`.
5. Registrar na seção 10 da spec a stack observada, cada tela, o fluxo, os
   formulários, a composição, os estados e a acessibilidade. Um CRUD não pode
   ficar restrito a API, banco ou serviço.
6. Criar na seção 14 a `Fase de interface`, com uma tarefa por tela e testes
   para navegação, formulário, validações, feedback e teclado.
7. Chamar `$specsfy-specialist-ux-design` para jornada,
   `$specsfy-specialist-ui-design` para composição e o especialista da stack
   detectada para implementação. `$specsfy-specialist-react` só se aplica a
   projetos React.

## Resultado esperado

Uma interface simples, funcional e completa para a tarefa, coerente com o
sistema existente. O plano mostra as telas e formulários a criar ou alterar,
seus componentes e seus testes. A implementação preserva tudo fora do alcance
registrado.

## Validação

- Confirmar que a pessoa recebeu pergunta sobre as telas em toda entrega que
  cria ou altera uma interface.
- Conferir que a seção 10 registra a stack e o sistema atual antes da proposta.
- Executar `validate_spec.mjs`, `validate_tasks.mjs` e
  `validate_interface_tasks.mjs` conforme a etapa.
- Verificar mobile e desktop, loading, vazio, erro, sucesso, permissão,
  teclado e foco antes de concluir a interface.
