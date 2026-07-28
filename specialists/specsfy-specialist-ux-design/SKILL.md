---
name: specsfy-specialist-ux-design
description: Investigar, estruturar e validar experiências com pesquisa, arquitetura da informação, jornadas, fluxos, formulários, onboarding e recuperação de erros. Use para problemas de usabilidade, fluxo, descoberta, conteúdo ou validação com usuários; não reduza UX a acabamento visual.
---

# Design de experiência

## Quando usar

- Acionar para investigar comportamento, estruturar jornadas, arquitetura da
  informação, formulários, onboarding, conteúdo e recuperação de erros.
- Acionar quando há dúvida sobre o problema, a sequência, a linguagem ou a
  capacidade de uma pessoa concluir uma tarefa.
- Não acionar para acabamento visual isolado; usar
  `$specsfy-specialist-ui-design` quando intenção e fluxo já estão validados.
- Combinar com `$specsfy-specialist-prototyping` quando uma hipótese precisar
  de artefato descartável antes de implementação.

## Fluxo

1. Formular a decisão de produto e a hipótese de comportamento antes de
   escolher método; definir público, contexto, frequência e risco.
2. Inventariar evidência existente e marcar separadamente fato observado,
   inferência, hipótese e preferência interna.
3. Selecionar método proporcional à pergunta e ao risco usando
   [references/standards.md](references/standards.md); definir recrutamento,
   consentimento, roteiro e critério de parada.
4. Mapear jornada atual com entradas, decisões, esperas, erros, canais,
   dependências e handoffs; não apagar exceções críticas.
5. Prototipar na fidelidade mínima que torne a hipótese testável sem simular
   comportamento que altere o resultado.
6. Conduzir sessões com tarefas e prompts neutros, registrando sucesso, erro,
   tempo, hesitação, compreensão e citações relevantes.
7. Sintetizar achados por evidência, severidade, alcance e impacto; separar
   claramente achado, interpretação, recomendação e questão aberta.

## Padrões

- Usar linguagem do domínio e revelar complexidade progressivamente.
- Manter status do sistema, próximo passo e possibilidade de recuperação visíveis.
- Pedir informação no momento em que é necessária e explicar o motivo.
- Evitar confirmação para ações triviais; oferecer undo quando mais seguro.
- Preservar dados após erro e apontar correção no contexto.
- Projetar onboarding como caminho para valor, não tour obrigatório.
- Não usar dark patterns, urgência artificial ou consentimento ambíguo.

## Antipadrões

- Perguntar “você gostou?” ou apresentar a solução antes da tarefa; mede
  cortesia e racionalização, não capacidade de uso.
- Transformar uma única sessão ou fala em regra universal; sem recorrência,
  contexto e triangulação, a evidência não sustenta abrangência.
- Recrutar apenas colegas ou especialistas quando o produto serve iniciantes;
  o vocabulário e os atalhos observados deixam de representar o público.
- Entregar uma lista de soluções sem rastrear cada item ao achado; preferência
  da equipe passa a parecer conclusão de pesquisa.
- Medir apenas tempo sem distinguir abandono, sucesso assistido e erro crítico;
  o número mascara a qualidade real da conclusão.

## Validação

- Demonstrar que cada pergunta de pesquisa tem método, participante e evidência
  compatíveis com a decisão que pretende informar.
- Rastrear achados até notas ou gravações consentidas e recomendações até
  achados; anonimizar dados conforme política do projeto.
- Incluir públicos, dispositivos, contextos e tecnologias assistivas
  relevantes ao risco, registrando lacunas de recrutamento.
- Revalidar mudanças estruturais com as mesmas tarefas críticas e comparar
  sucesso independente, erro e compreensão.
- Não declarar uma experiência “intuitiva” ou validada sem evidência observada
  e limites explícitos da amostra.

## Skills relacionadas

- `$specsfy-specialist-ui-design` materializa hierarquia visual e estados
  depois que tarefa e fluxo estão definidos.
- `$specsfy-specialist-prototyping` cria o artefato mínimo para testar uma
  hipótese de interação.
- `$specsfy-specialist-web-accessibility` avalia conformidade e uso com
  tecnologias assistivas além do recorte de pesquisa.
- `$specsfy-specialist-domain-modeling` alinha vocabulário e invariantes quando
  a experiência atravessa regras complexas do domínio.

Leia [references/standards.md](references/standards.md) para escolher método,
estruturar pesquisa, avaliar formulários, conteúdo, onboarding e serviços.
