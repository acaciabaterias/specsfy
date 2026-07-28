---
name: specsfy-specialist-{{slug}}
description: "{{Verbo(s) no infinitivo + domínio coberto}}. Use para {{gatilhos positivos e concretos}}; use também para {{gatilho secundário, se houver}}; não use para {{limite negativo ou skill vizinha que cobre o caso adjacente}}."
---

# {{Título humano do domínio}}

## Quando usar

- Acionar quando {{sinal observável no pedido, no código ou no ambiente}}.
- Acionar também quando {{segundo sinal, se distinto do primeiro}}.
- Não acionar quando {{caso adjacente coberto por outra skill}}; usar
  `$specsfy-specialist-{{skill-vizinha}}` nesse caso.
- Combinar com `$specsfy-specialist-{{skill-complementar}}` quando
  {{condição que exige as duas}}.

## Fluxo

1. Descobrir {{versão, ambiente, workload ou configuração real do projeto}}
   antes de recomendar; nunca assumir a partir de memória genérica.
2. {{Passo de modelagem/decisão inicial específico do domínio}}.
3. {{Passo central que produz o artefato técnico — schema, componente,
   pipeline, teste, diagnóstico}}.
4. {{Passo de verificação intermediária com evidência observável}}.
5. {{Passo de integração com o restante do sistema/projeto consumidor}}.
6. {{Passo final de registro/comunicação do risco residual ou trade-off}}.

Ajuste o número de passos ao domínio; mantenha cada passo verificável e
específico o bastante para orientar uma decisão real, nunca um lembrete
genérico como "planeje com cuidado".

## Padrões

- {{Regra afirmativa concreta e testável}}.
- {{Regra afirmativa concreta e testável}}.
- {{Proibição explícita com o motivo técnico, quando não for óbvio}}.
- {{Regra sobre quando NÃO aplicar uma prática comum do domínio}}.
- {{Regra sobre limite, threshold ou condição de decisão}}.

Cada item deve ser verificável olhando o código, a configuração ou o
resultado — nunca uma aspiração ("cuidar da performance") sem critério de
checagem.

## Antipadrões

- {{Erro comum observável e por que ele falha em produção/escala/manutenção}}.
- {{Erro comum observável e por que ele falha em produção/escala/manutenção}}.
- {{Confusão frequente com outra prática ou skill, e como diferenciá-la}}.

## Validação

- {{Comando, teste ou inspeção concreta que comprova o passo 3 do Fluxo}}.
- {{Caso de borda ou cenário adversarial que precisa de evidência antes de
  declarar pronto}}.
- {{Métrica, log ou saída que comprova ausência de regressão}}.
- Não declarar {{propriedade do domínio — seguro, íntegro, performático,
  acessível}} sem a evidência acima; linguagem absoluta sem prova é proibida.

## Skills relacionadas

- `$specsfy-specialist-{{skill-relacionada-1}}` para {{fronteira clara de
  responsabilidade}}.
- `$specsfy-specialist-{{skill-relacionada-2}}` quando {{condição}}.

Leia [references/standards.md](references/standards.md) para
{{lista do que a referência aprofunda: decisões específicas, tabelas,
thresholds, comandos e fontes oficiais}}. Se o domínio exigir catálogo,
checklist ou fluxo de decisão extensos, adicione arquivos adicionais em
`references/` e linke cada um pelo nome no ponto do Fluxo em que ele se aplica.
