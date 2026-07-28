# Padrões e referências Redis

## Seleção de estrutura

- Strings: cache simples, contadores e tokens compactos.
- Hashes: atributos pequenos com atualizações parciais.
- Sets e sorted sets: unicidade, ranking e janelas.
- Streams: log com grupos de consumidores e confirmação explícita.
- Pub/Sub: evento transitório, nunca fila durável.

## Resiliência

- Defina timeouts baixos, pool limitado e circuit breaking no cliente.
- Evite retry cego de operações não idempotentes.
- Planeje cold start após flush/failover e carga no source of truth.
- Escolha RDB, AOF ou nenhum conforme durabilidade e RTO.

## Fontes oficiais

- Documentação: https://redis.io/docs/latest/
- Estruturas de dados: https://redis.io/docs/latest/develop/data-types/
- Expiração: https://redis.io/docs/latest/commands/expire/
- Eviction: https://redis.io/docs/latest/develop/reference/eviction/
- Persistência: https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- Segurança: https://redis.io/docs/latest/operate/oss_and_stack/management/security/
- Clustering: https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
