---
name: specsfy-specialist-data-modeling
description: Modelar dados, entidades, relações, ciclos de vida, qualidade e contratos persistentes antes de implementar mudanças.
---

# Modelar os dados do produto

Use esta skill para entender e evoluir dados persistentes, sem escolher banco ou
biblioteca por suposição. Leia a stack, o sistema atual, migrations, schemas,
models, contratos e testes antes de propor alteração.

## Trabalho

1. Identifique as entidades, seus papéis e as relações observadas no código.
2. Registre campos, tipos, obrigatoriedade, origem, ciclo de vida e quem pode
   consultar ou alterar cada informação.
3. Descreva unicidade, consistência, retenção, exclusão, histórico e migração
   quando forem pertinentes.
4. Atualize a seção de dados da spec e encaminhe respostas confirmadas para
   `$specsfy-aux-database` e `.specsfy/DATABASE.md`.
5. Derive cenários para criação, leitura, atualização, exclusão, autorização e
   dados inválidos. A implementação usa o especialista do banco detectado.

Não invente campos, relações ou tecnologia. A pessoa confirma o que o produto
precisa guardar quando o sistema atual não responder.
