# Padrões e referências Astro

## Escolhas de renderização

| Necessidade | Escolha |
| --- | --- |
| Conteúdo igual para todos, conhecido no build | Static (default) — HTML pré-gerado, cacheável em CDN |
| Dado por sessão/usuário ou que precisa de frescor real-time | On-demand rendering (`server` output ou `export const prerender = false`) |
| Interação localizada num pedaço da página | Island — componente de framework hidratado, resto continua HTML |
| Contrato HTTP explícito para outro cliente | Endpoint (`.ts`/`.js` em `pages/`) com validação e cache próprios |

Prefira sempre a opção mais alta da tabela que resolve o requisito — cada
degrau abaixo custa cache e simplicidade.

## Diretivas de hidratação (ilhas)

| Diretiva | Quando usar | Custo |
| --- | --- | --- |
| `client:load` | Interação crítica, visível e necessária imediatamente (ex.: campo de busca do header) | JS baixado e executado o mais cedo possível |
| `client:idle` | Interação de prioridade média, pode esperar o browser ficar ocioso | Adia execução, não adia download |
| `client:visible` | Interação abaixo da dobra, só importa quando o elemento entra em viewport | Melhor para conteúdo longo/scroll |
| `client:media` | Interação só relevante em certo breakpoint/mídia | Evita hidratar componente não usado nesse viewport |
| `client:only` | Componente que não pode nem deve renderizar no servidor (depende de API só de browser) | Perde SSR do componente; usar com parcimônia |

Cada prop passada a uma ilha é serializada como JSON no HTML — envie apenas
os campos que o componente realmente usa, nunca o objeto de domínio inteiro.

## Content collections

- Defina um schema Zod por coleção; um campo ausente ou de tipo errado deve
  falhar o build (`astro check`/`astro build`), não aparecer como `undefined`
  em produção.
- Relacione coleções por referência (`reference()`), não por string solta
  copiada manualmente — evita slug/ID divergente entre entradas relacionadas.
- Trate slugs derivados de título como dado que precisa de checagem de
  unicidade explícita antes do build, especialmente com conteúdo vindo de
  CMS externo.

## Actions e endpoints

- Actions (`astro:actions`) validam entrada com schema antes de executar
  qualquer efeito colateral, do mesmo modo que um endpoint HTTP; tratam-se
  como superfície pública, mesmo quando chamadas só pela própria UI.
- Endpoints (`pages/**/*.ts`) devem declarar os métodos HTTP suportados
  explicitamente e retornar `Content-Type` e status corretos; não reaproveitar
  um endpoint de leitura para receber mutation sem validação equivalente.

## Imagens e assets

- Usar `astro:assets` (`<Image />`/`<Picture />`) para otimização automática
  de formato, tamanho e lazy loading, em vez de `<img>` cru com asset não
  processado.
- Declarar `width`/`height` (ou usar o componente que os infere) para evitar
  layout shift (CLS) durante o carregamento.

## SSR, adapters e runtime

- Adapters edge (Cloudflare, Vercel Edge, Deno) não expõem a API completa do
  Node (`fs`, alguns módulos nativos); confirmar compatibilidade antes de
  importar uma dependência server-only em rota `server`-rendered.
- Cache de resposta em rota on-demand precisa de headers explícitos
  (`Cache-Control`) — o adapter não infere isso sozinho como faz com
  estático.

## SEO e metadados

- Gerar `canonical` a partir da URL final real da página (incluindo
  trailing slash e domínio configurado), não de um valor fixo copiado entre
  páginas.
- Sitemap e RSS devem refletir apenas conteúdo publicado (respeitar
  `draft`/`published` do schema de conteúdo).

## Fontes oficiais

- Documentação: https://docs.astro.build/
- Islands: https://docs.astro.build/en/concepts/islands/
- Client directives: https://docs.astro.build/en/reference/directives-reference/#client-directives
- Routing: https://docs.astro.build/en/guides/routing/
- Content collections: https://docs.astro.build/en/guides/content-collections/
- On-demand rendering: https://docs.astro.build/en/guides/on-demand-rendering/
- Actions: https://docs.astro.build/en/guides/actions/
- Images: https://docs.astro.build/en/guides/images/
- Deploy: https://docs.astro.build/en/guides/deploy/
