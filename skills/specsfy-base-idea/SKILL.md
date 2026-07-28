---
name: specsfy-base-idea
description: "Use quando o usuário enviar uma ideia, pensamento, necessidade, oportunidade ou texto livre para guardar, capturar, anotar ou retomar depois. Preserve o input integral, faça pré-processamento silencioso e crie imediatamente um arquivo timestampado em `specs/ideias/`. Não faça perguntas, não peça confirmação e não crie backlog, spec, tarefas, testes ou código."
---

# Capturar uma ideia sem interromper

Registre imediatamente o texto recebido em `specs/ideias/`. Trate a captura como
uma caixa de entrada durável anterior ao backlog: ela preserva intenção e
organiza sinais úteis, mas não decide requisitos nem autoriza implementação.

## Não interromper a captura

- Não faça perguntas, mesmo quando a ideia estiver vaga, contraditória ou
  incompleta.
- Não peça confirmação antes de escrever.
- Não bloqueie a captura por duplicata, falta de contexto ou incerteza.
- Registre lacunas em `Pontos a revisar no futuro`; não tente resolvê-las com o
  usuário nesta etapa.
- Depois de salvar, informe somente o caminho, um resumo breve do que foi
  processado e o próximo passo opcional. Não inicie o próximo passo
  automaticamente.

## Preservar e pré-processar

1. Faça uma verificação silenciosa de credenciais, tokens, chaves privadas e
   dados pessoais sensíveis evidentes. Se encontrar algum, não grave o arquivo
   nem faça perguntas; informe que a política de privacidade exige remover o
   dado sensível e reenviar a ideia.
2. Use como texto original todo o input que expressa a ideia. Preserve sua
   formulação integral, sem “corrigi-la” ou substituir palavras.
3. Derive silenciosamente um título curto, concreto e fiel. Gere o slug a
   partir dele.
4. Separe a análise nas categorias:
   - **Declaração:** conteúdo explicitamente presente no texto original;
   - **Inferência:** interpretação plausível, sempre identificada como tal;
   - **A revisar:** lacuna, conflito ou decisão que poderá ser revista depois.
5. Extraia somente quando houver evidência:
   - resumo em uma frase;
   - problema ou oportunidade;
   - pessoas afetadas ou beneficiadas;
   - resultado ou valor esperado;
   - sinais de escopo, regra, restrição, canal ou solução mencionada;
   - riscos, dependências e relações evidentes;
   - possíveis direções de backlog ou spec, sem promovê-las.
6. Use `Não identificado no texto original.` quando não houver base. Não
   invente stakeholder, prioridade, prazo, regra, solução ou critério de aceite.

## Criar o arquivo

Execute uma única vez:

```bash
python3 -B <diretório-da-skill>/scripts/capturar_ideia.py \
  --input "<texto original integral>" \
  --title "<título derivado>" \
  --summary "<resumo>" \
  --problem "<problema ou oportunidade>" \
  --people "<pessoas afetadas>" \
  --value "<resultado ou valor>" \
  --signals "<sinais extraídos>" \
  --risks "<riscos ou dependências>" \
  --directions "<direções futuras possíveis>" \
  --review "<pontos a revisar futuramente>" \
  [--root <raiz>]
```

O script usa `.specsfy/templates/Idea.md`, cria
`specs/ideias/AAAA-MM-DD-HHMMSS-<slug>.md` e nunca sobrescreve uma captura
existente. Se o template estiver ausente, relate a instalação incompleta; não
crie um template paralelo dentro da skill.

## Orquestrar a conversa

Esta skill é uma exceção deliberada ao handoff automático do framework:
capturar é o resultado final do pedido e precisa ocorrer sem perguntas nem
transições. Após escrever, apenas sugira um destes próximos passos:

- manter a ideia na caixa de entrada;
- usar `$specsfy-base-backlog` para refiná-la;
- usar `$specsfy-base-interview` quando o usuário quiser aprofundá-la.

Somente carregue outra skill se o mesmo pedido também ordenar explicitamente
esse trabalho. Nesse caso, anuncie
`Transição automática: $specsfy-base-idea → $<destino> — motivo: <motivo> —
resultado esperado: <resultado>` depois de a captura estar segura.

## Limites

- Não pesquisar duplicatas antes de salvar.
- Não alterar nem apagar capturas anteriores.
- Não transformar inferência em declaração do usuário.
- Não criar `specs/backlog/`, `specs/specs/`, tarefas, research, testes ou
  código.
- Não usar a ideia como fonte normativa de comportamento.
