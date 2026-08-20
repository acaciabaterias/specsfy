---
name: specsfy-mvp-milestone-interviewer
description: Use para explorar o MVP por conversa, preservar cada resposta em uma série de Inboxes e importar `MVP.md` como a milestone 1.0. Leia `BRAND.md` da raiz quando existir. Não use para tratar as capturas como backlog, criar specs, tarefas ou código.
---

# Explorar o MVP em uma série de Inboxes

## Modo de interação

Modo de interação: `perguntas`.
Antes de formular qualquer pergunta, leia e aplique o
`Contrato de perguntas numeradas` de `.specsfy/Spec.md`.

Esta skill conversa para revelar o MVP sem converter cada fala em requisito ou
plano. Cada fala da pessoa vira uma Inbox imutável. O backlog trata a série
depois, com todos os registros como proveniência.

## Carregar o contexto disponível

1. Resolva a raiz do projeto consumidor antes de ler qualquer arquivo. Se ela
   for um submódulo Git, descubra o superprojeto com
   `git -C <raiz> rev-parse --show-superproject-working-tree`. A saída não
   vazia acrescenta somente essa raiz pai à busca. Não percorra outros pais.
2. Leia `MVP.md` se existir como arquivo regular na raiz do consumidor. Quando
   ele estiver ausente e a raiz for um submódulo, leia `MVP.md` no
   superprojeto. O arquivo local tem prioridade. Preserve a fonte consultada e
   use-a como contexto declarado, sem substituir o que a pessoa disser.
3. Se `MVP.md` foi importado, execute uma vez:

   ```bash
   node \
     .agents/skills/specsfy-mvp-milestone-interviewer/scripts/importar_mvp.mjs \
     --root <raiz>
   ```

   O comando cria `specs/milestones/M01.md` com o título `Milestone 1.0`, a
   origem e o hash SHA-256 de `MVP.md`. Se `M01.md` existir, não o sobrescreva:
   registre a divergência na primeira Inbox e siga a conversa.
4. Leia `BRAND.md` seguindo a mesma ordem: raiz do consumidor e, somente como
   fallback de submódulo, superprojeto. Use-o para manter linguagem, público,
   proposta e limites de marca coerentes durante as perguntas. Não copie seu
   conteúdo para as Inboxes.
5. Registre na primeira captura o caminho de `MVP.md` e `BRAND.md` consultados
   ou informe que cada arquivo estava ausente. Não crie, mova nem altere esses
   arquivos.
6. Leia `PROJECT.md`, Inboxes, backlog e specs existentes apenas se ajudarem a
   evitar repetição ou contradição. Eles continuam separados da formulação
   recebida nesta sessão.
7. Quando `MVP.md` ou a conversa indicar informações que o produto precisa
   guardar, consultar, compartilhar ou apagar, preserve primeiro a Inbox e
   carregue `$specsfy-data-discovery` para conduzir essa parte da conversa e
   registrar somente respostas confirmadas em `.specsfy/DATABASE.md`.

Antes da importação, faça a mesma triagem de dados sensíveis usada pela Inbox.
Se a fonte tiver credencial, token, chave privada ou dado pessoal sensível,
não gere a milestone nem reproduza o valor em mensagens.

## Preservar a sessão

1. Derive uma identificação estável no formato `DESC-AAAAMMDD-<slug>` a partir
   do primeiro tema recebido.
2. Antes da primeira rodada, capture a formulação inicial da pessoa usando
   `$specsfy-01-inbox`, com a identificação em `--session` e o turno `1` em
   `--turn`.
3. Depois de cada resposta da pessoa, capture o texto integral em outra Inbox
   com a mesma sessão e o próximo turno. Nunca edite, reúna ou substitua uma
   captura anterior.
4. Informe `--sources` em toda chamada: liste o caminho de `MVP.md` e
   `BRAND.md` consultados, inclusive quando vierem do superprojeto, ou indique
   que estavam ausentes.
5. Aplique a triagem de dados sensíveis do `$specsfy-01-inbox` antes de cada
   escrita. Se ela impedir a captura, interrompa a conversa até receber texto
   seguro para registrar.

Use o script da Inbox com os campos da captura e acrescente a sessão:

```bash
node .agents/skills/specsfy-01-inbox/scripts/capturar_inbox.mjs \
  --input "<texto integral da pessoa>" \
  --title "<tema da descoberta>" \
  --session "DESC-AAAAMMDD-<slug>" \
  --turn "<número sequencial>" \
  --sources "<situação de MVP.md e BRAND.md>" \
  [campos de análise da Inbox] [--root <raiz>]
```

## Conduzir uma conversa adaptativa

1. Comece por finalidade, pessoa atendida e problema observável.
2. Releia todas as Inboxes da sessão depois de cada captura. Mostre uma síntese
   curta que separe formulação recebida e hipótese da conversa.
3. Monte a rodada conforme o contrato central: pelo menos três perguntas
   numeradas, opções específicas, `Escrever outra resposta` e `Avançar`.
4. Explore apenas o necessário para entender jornada, dados indispensáveis,
   papéis, regras, integrações, limites, demonstração e validação. Não aplique
   formulário fixo nem repita uma resposta já preservada.
5. Quando a pessoa encerrar ou adiar uma área, capture a formulação dela e
   indique a Inbox correspondente na síntese. Não preencha lacunas por conta
   própria.

## Encerrar e tratar depois

Ao encerrar, informe a identificação da sessão, a lista ordenada de Inboxes e
uma síntese não normativa de finalidade, pessoa, jornada e pontos em aberto.
Se a pessoa pedir refinamento, anuncie `Transição automática:
$specsfy-mvp-milestone-interviewer para $specsfy-02-backlog; motivo: tratar a
série de capturas da descoberta; resultado esperado: backlog com proveniência
da sessão` e carregue a skill de backlog na mesma conversa.

O backlog escolhe o que será agrupado, aprofundado ou promovido. Só depois do
refinamento a pessoa pode solicitar specs ou ajustar as relações da milestone.

## Limites

- Não invente respostas, objetivo, condição de saída, fora de escopo ou
  vínculos da milestone importada.
- Não sobrescreva a milestone 1.0 existente.
- Não crie ou atualize backlog, specs, tarefas, testes ou código.
- Não trate Inbox como fonte normativa.
- Não use o entrevistador de roadmap para ampliar o MVP sem confirmação.
