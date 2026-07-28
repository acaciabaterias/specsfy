# Criar a especificação com `specsfy-base-specify`

Esta skill cria a fonte única da entrega. Ela reúne descoberta, requisitos,
comportamentos, plano, testes, tarefas e evidências no mesmo `spec.md`.

## Quando usar

Use para promover um backlog entrevistado ou criar uma spec nova ainda em
estado Draft. Para mudar uma spec que já foi definida, use update-spec.

## Como pedir

Com um backlog:

```text
Use $specsfy-base-specify para promover
specs/backlog/0003-idioma-da-interface.md.
```

Com um brief na conversa:

```text
Use $specsfy-base-specify para criar uma especificação para recuperação de senha
com base nas decisões desta conversa.
```

## Exemplo passo a passo

1. A skill confirma a raiz do projeto e o próximo número disponível.
2. Ela lê contexto, instruções e evidências necessárias.
3. Cria o pacote:

```text
specs/specs/0004-recuperar-senha/
├── spec.md
└── research/        # somente quando houver pesquisa externa
```

4. Preenche o Ato I com requisitos e cenários.
5. Mantém decisões ainda abertas claramente marcadas.
6. Executa validadores sem inventar uma aprovação.

Research apoia decisões, mas nunca substitui o texto normativo de `spec.md`.

## O que esperar

- formato `Specsfy/2.0`;
- IDs rastreáveis para histórias, requisitos e critérios;
- cenários que cobrem sucesso, variação e falha;
- uma única fonte normativa;
- status Draft ou Defined conforme a evidência real.

## Erros comuns

- criar `plan.md`, `tasks.md` ou `research.md`;
- copiar uma fonte externa como requisito sem decisão;
- aprovar gates com campos incompletos;
- misturar várias entregas grandes na mesma spec.

## Próximo passo

Use [`specsfy-base-validate`](specsfy-base-validate.md) para provar que a
definição está pronta. Se uma decisão importante faltar, a transição volta para
[`specsfy-base-interview`](specsfy-base-interview.md).
