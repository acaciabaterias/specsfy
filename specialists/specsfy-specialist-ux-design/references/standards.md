# Padrões de pesquisa e design de experiência

## Escolher o método pela decisão

| Pergunta | Método inicial | Evidência produzida |
| --- | --- | --- |
| como a tarefa acontece hoje? | entrevista contextual + observação | comportamento, contexto e workaround |
| pessoas encontram e nomeiam conteúdo? | card sorting/tree testing | agrupamento, rótulo e caminho |
| o fluxo pode ser concluído? | teste moderado ou não moderado | sucesso, erro, hesitação e compreensão |
| qual variante performa melhor em escala? | experimento controlado | diferença causal dentro das métricas |
| quais problemas já se repetem? | análise de suporte e analytics | frequência, etapa e segmento |
| a proposta comunica valor? | prototype test orientado a tarefa | interpretação e intenção de ação |

Não escolha entrevista para confirmar comportamento que pode ser observado nem
experimento para uma solução cuja falha básica ainda não foi diagnosticada.

## Plano mínimo de pesquisa

1. decisão que o estudo informará;
2. hipótese e evidência que poderia refutá-la;
3. público, critérios de recrutamento e exclusões;
4. método, tarefas, roteiro e piloto;
5. consentimento, gravação, acesso, retenção e anonimização;
6. sinais observados e regra de severidade;
7. limitações e critério de parada.

Perguntas devem pedir episódios reais e decisões, não aprovação da solução.
Durante teste de tarefa, use prompts neutros e não ensine o caminho que está
sendo avaliado.

## Qualidade da evidência

- **Observação:** comportamento, fala ou artefato registrado.
- **Interpretação:** explicação plausível para a observação.
- **Achado:** padrão sustentado por evidências relacionadas.
- **Recomendação:** mudança proposta para tratar o achado.
- **Questão aberta:** incerteza que ainda requer decisão ou pesquisa.

Mantenha esses níveis separados na síntese. Uma recomendação sem rastreio para
achado é opinião; um achado sem rastreio para evidência é memória.

Classifique severidade combinando impacto sobre a tarefa, frequência observada,
recuperabilidade e risco do domínio. Não converta contagem pequena de pesquisa
qualitativa em percentual populacional.

## Jornada e serviço

Mapeie:

- gatilho, objetivo e critério de conclusão da pessoa;
- canais, dispositivos e mudança de contexto;
- passos, decisões, espera e dependências;
- dados ou documentos necessários;
- falhas, recuperação, suporte e handoffs;
- responsável interno e evidência operacional por etapa.

Otimize o serviço completo, não apenas a tela. Um formulário curto que transfere
trabalho manual para suporte pode piorar a jornada total.

## Formulários e conteúdo

- Pergunte somente o necessário para a decisão atual e explique informação
  sensível ou inesperada.
- Use uma pergunta por página quando isso melhora foco e recuperação; agrupe
  campos quando a comparação ou o preenchimento conjunto for essencial.
- Preserve entrada após erro, associe mensagem ao campo e forneça resumo quando
  múltiplos erros precisam ser percorridos.
- Escreva ação pelo resultado (`Salvar endereço`), não pelo mecanismo
  (`Continuar`), quando o efeito precisa ser claro.
- Diferencie dado opcional, exemplo de formato e restrição real.

## Onboarding

- Defina o primeiro valor observável e conduza até ele.
- Solicite permissão e configuração no momento de uso.
- Permita pular conteúdo instrucional que não bloqueia a tarefa.
- Preserve progresso e ofereça retomada explícita.
- Meça conclusão de tarefa e ativação, não quantidade de slides vistos.

## Evidência de validação

- participantes correspondem aos critérios e desvios estão registrados;
- tarefas não contêm o nome do controle ou o caminho esperado;
- sucesso independente, sucesso assistido, falha e abandono são distintos;
- notas e gravações consentidas sustentam cada achado;
- limitações de amostra, ambiente e fidelidade do protótipo estão explícitas;
- reavaliação usa tarefas críticas comparáveis depois da mudança.

## Fontes primárias e consolidadas

- ISO 9241-210: https://www.iso.org/standard/77520.html
- W3C COGA guidance: https://www.w3.org/TR/coga-usable/
- GOV.UK Service Manual: https://www.gov.uk/service-manual
- GOV.UK Design System patterns: https://design-system.service.gov.uk/patterns/
- USWDS Design Principles: https://designsystem.digital.gov/design-principles/
- Nielsen Norman Group usability heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
