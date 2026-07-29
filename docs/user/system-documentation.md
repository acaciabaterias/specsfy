# Documentação técnica do sistema

`$specsfy-documentator` reconstrói a visão técnica de uma aplicação em
`<projeto>/docs/`. Esses arquivos explicam o código do projeto consumidor e não
se confundem com a documentação oficial da metodologia Specsfy.

Execute `$specsfy-documentator` livremente para documentar um sistema legado ou
atualizar sua visão técnica. Depois de cada tarefa de código concluída por
`$specsfy-07-implement`, a transição para o documentador é obrigatória. A
implementação só continua quando `docs/` representar o código atual.

A skill lê o código completo e as fontes que descrevem a aplicação. Isso inclui
os manifests, as migrations, as rotas e os testes, além das informações
permanentes do projeto. Cada execução reconstrói blocos delimitados nos
seguintes arquivos e preserva o texto humano externo:

| Arquivo no consumidor | Conteúdo |
| --- | --- |
| `docs/README.md` | portal e ordem de leitura |
| `docs/architecture.md` | componentes, dependências e UML Mermaid |
| `docs/application.md` | módulos e implementações observadas |
| `docs/database.md` | entidades, campos, relações e `erDiagram` |
| `docs/flows.md` | rotas, `flowchart` e `sequenceDiagram` |
| `docs/testing.md` | runners, comandos, inventário e resumo |
| `docs/frontend.md` | views, páginas, componentes, React e Tailwind |
| `docs/packages.md` | runtime, framework, nativos, integrados e terceiros |
| `docs/integrations.md` | serviços externos e nomes de configuração |
| `docs/decisions.md` | escolhas explícitas e suas fontes |

Em Laravel, o inventário acompanha a requisição pelas rotas, controllers e
services, relaciona Eloquent e migrations e registra os testes Pest ou PHPUnit.
Em projetos Node, Next.js, React ou Astro, a documentação mostra páginas,
endpoints, componentes e scripts, além do runner observado no repositório.

Cada pacote recebe a versão e a referência do repositório no GitHub. Quando
essa origem não puder ser confirmada localmente, a documentação publica uma
busca identificada como tal, em vez de inventar uma URL.

Depois da reconstrução, a própria skill executa o modo `--check`. O comando
compara os blocos gerados com o estado atual e falha quando `docs/` está
desatualizado:

```bash
python3 -B .agents/skills/specsfy-documentator/scripts/build_documentation.py \
  --project . --check
```

O monitor do setup também retorna `PENDING` quando o código da aplicação ou a
persistência mudou sem uma nova reconstrução de `docs/`. Esse estado impede a
conclusão da tarefa e do Delivery Gate.

O código, os testes, os manifests, os schemas e as migrations comprovam o
estado implementado. A spec governa o comportamento da mudança, enquanto
`PROJECT.md` e `.specsfy/` preservam informações válidas para o sistema
inteiro. Os arquivos em `<projeto>/docs/` podem ser reconstruídos dessas fontes
e não devem copiar segredos, valores de ambiente, registros de produção ou
código integral.
