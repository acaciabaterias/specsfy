---
name: specsfy-base-backlog
description: "Use quando o usuário apresenta uma ideia vaga, oportunidade, problema ainda superficial, pedido para anotar algo para depois ou quer conversar levemente antes de decidir se vale especificar. Use também quando uma transição automática retornar à captura de uma ideia. Detecta lacunas e ambiguidades, faz perguntas adaptativas até obter uma captura mínima e cria ou atualiza um item em `specs/backlog/`; não use para entrevista profunda, criação de `spec.md`, requisitos formais, tarefas, testes ou implementação."
---

# Registrar uma ideia no backlog

Converse de forma leve para preservar uma ideia sem exigir imediatamente o
rigor de uma especificação. Conforme ela amadurece, organize informação
suficiente para produto, desenvolvimento e testes compreenderem o
comportamento e verificarem a entrega, sem transformar o backlog em spec.

## Orquestrar a conversa

Ao concluir esta etapa ou detectar trabalho de outra etapa, anuncie
`Pendência detectada: <descrição> — ação: resolvendo nesta etapa` e resolva-a
quando pertencer ao próprio escopo. Quando houver troca de responsabilidade,
anuncie `Transição automática: $specsfy-base-backlog → $<destino> — motivo:
<motivo> — resultado esperado: <resultado>` e carregue imediatamente a skill de
destino, sem pedir confirmação nem repetir o comando. Continue na mesma
conversa. Depois de uma correção necessária a esta etapa, anuncie `Retomada
automática: $<destino> → $specsfy-base-backlog — pendência resolvida:
<resultado>` e retome-a imediatamente. Reavalie o estado após cada handoff para
evitar ciclos. Não peça confirmação para o handoff; ações sensíveis continuam
exigindo autorização específica.

## Buscar duplicatas e referências

1. Extraia termos derivados do pedido do usuário, incluindo nomes do domínio e
   equivalentes evidentes já usados na conversa.
2. Antes de criar o item, pesquise esses termos em:
   - `specs/backlog/*.md`;
   - `specs/specs/*/spec.md`;
   - `docs/**/*.md`.
3. Leia somente os resultados plausíveis e classifique cada relação:
   - **possível duplicata**: problema, pessoa, resultado e contexto
     substancialmente iguais;
   - **backlog relacionado**: ideia complementar, dependência ou precedente;
   - **spec relacionada**: comportamento já definido ou entregue que limita ou
     informa a ideia;
   - **documentação relacionada**: vocabulário, regra ou contexto do projeto.
4. Apresente correspondências materiais com seus caminhos. Diante de uma
   possível duplicata, confirme com o usuário se deve atualizar o item
   existente ou registrar uma diferença real; não crie outro item antes dessa
   decisão.
5. Registre as fontes úteis em `Referências relacionadas`, com caminho relativo
   à raiz do projeto e tipo de relação. Não copie uma decisão da fonte para a
   ideia sem distinguir o que o usuário declarou.

Se não houver resultado relevante, registre isso sem preencher a seção com
fontes genéricas. Repita a busca quando uma resposta mudar materialmente os
termos, o problema, a pessoa, o resultado ou o contexto.

## Garantir a captura mínima

1. Preserve a formulação original e separe o que o usuário declarou do que foi
   inferido ou continua em aberto.
2. Confirme se a conversa já esclareceu estes itens essenciais:
   - problema percebido;
   - pessoa afetada ou beneficiada;
   - resultado ou valor esperado;
   - contexto suficiente para distinguir a ideia de pedidos semelhantes.
3. Se algum item estiver ausente, vago, contraditório ou ambíguo, selecione a
   lacuna de maior impacto. Faça uma pergunta por vez e não repita o que já foi
   respondido no pedido ou no item existente.
4. Reavalie as lacunas depois de cada resposta e faça a próxima pergunta
   somente quando ainda for necessária. Não transforme os quatro itens em um
   questionário fixo.
5. Não crie nem atualize o arquivo enquanto algum item essencial continuar
   ausente ou ambíguo. Se o usuário não souber responder, explique qual lacuna
   impede a captura mínima e não invente conteúdo.

A captura mínima não exige regras detalhadas, critérios de aceitação, solução
técnica, hierarquia ou prioridade. Esses dados podem permanecer para
refinamento posterior.

## Decidir e executar a operação

1. Se o usuário apenas quiser explorar sem registrar, converse e confirme antes
   de escrever.
2. Se existir um item correspondente, atualize-o sem mudar seu ID e preserve a
   formulação anterior da ideia.
3. Se for uma ideia nova e a captura mínima estiver clara, execute:

```bash
python3 -B <diretório-da-skill>/scripts/iniciar_backlog.py \
  --title "<título curto>" \
  --idea "<formulação original>" \
  --problem "<problema percebido>" \
  --person "<pessoa afetada ou beneficiada>" \
  --result "<resultado ou valor esperado>" \
  --context "<contexto que distingue a ideia>" \
  [--slug <slug>] [--root <raiz>]
```

4. Use o caminho absoluto impresso pelo script. Não crie uma spec nesta etapa.

## Conversar no nível de ideia

- Mantenha cada pergunta curta, concreta e respondível.
- Preserve a fala original em `Ideia original`; não apresente inferência como
  declaração do usuário.
- Registre dúvidas, riscos ou dependências como sinais para aprofundar, sem
  fingir que decisões ausentes já foram tomadas.
- Evite arquitetura, modelo de dados, contratos, Gherkin, estimativas e plano
  técnico.
- Pare assim que outra pessoa conseguir entender por que a ideia merece ser
  retomada.

## Organizar e refinar

Leia `references/backlog-quality.md` ao estruturar, refinar, priorizar ou
avaliar prontidão de um backlog.

- Classifique, quando conhecido, em Produto → Épico → Funcionalidade → item.
- Use tipos como épico, história, regra, técnico e melhoria sem confundir tipo
  com prioridade.
- Mantenha uma ordem real do backlog. Considere valor, risco, dependências,
  urgência, esforço, desbloqueios e incerteza; não marque tudo como alta.
- Aprofunde campos conforme risco e complexidade. Autenticação, pagamentos,
  permissões, privacidade e operações assíncronas exigem mais cuidado que uma
  alteração simples.
- Prefira comportamento observável a solução de interface. “Criar tela de
  login” não substitui autenticação, sessão, autorização, falhas e segurança.
- Torne qualidades mensuráveis quando materiais; não registre apenas “rápido”,
  “seguro” ou “escalável”.
- Use listas, fluxos, cenários ou matrizes quando representarem melhor a regra.
  Uma matriz de permissão é preferível a parágrafos ambíguos.
- Diferencie requisito funcional do atributo de qualidade e operação.

## Manter o item

Use exatamente `specs/backlog/<NNNN>-<slug>.md`. Mantenha:

- `Status: Captured` enquanto a ideia estiver apenas registrada;
- `Status: Refining` durante aprofundamento;
- `Status: Ready for interview` quando houver contexto suficiente para
  entrevista;
- `Status: Promoted` depois que uma spec derivada existir.

Mantenha as metainformações na tabela logo abaixo do título; não as converta em
uma lista. Preencha as quatro seções essenciais com conteúdo esclarecido e
somente as demais seções aplicáveis do template. Não invente prioridade, prazo,
stakeholder, solução ou evidência. Um item `Captured` pode continuar curto; um
item refinado deve registrar comportamento, regras, aceite, erros, dependências,
fora de escopo e qualidades relevantes.

Use o checklist `Pronto para desenvolvimento` como diagnóstico, não como
autorização de implementação. Lacuna que altere segurança, escopo, arquitetura
ou experiência exige pergunta; não a complete silenciosamente. Mesmo com o
checklist concluído, a implementação só começa depois da promoção para spec e
dos gates aplicáveis.

## Encerrar

Resuma o que foi registrado, apresente o caminho e indique um único próximo
passo:

- manter no backlog;
- chamar automaticamente `$specsfy-base-interview` para aprofundar e continuar
  a entrevista na mesma conversa;
- descartar ou fundir com outro item, somente com confirmação do usuário.

Não salte diretamente para `$specsfy-base-specify`. A promoção exige entrevista
suficiente e intenção explícita de criar a spec; o handoff entre skills é
automático.

## Limites

- Não criar `spec.md`, tarefas, research, testes ou código.
- Não transformar hipótese técnica em requisito.
- Não exigir respostas próprias de uma especificação completa.
- Não mover nem apagar item existente sem confirmação.
