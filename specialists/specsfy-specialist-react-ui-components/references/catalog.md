# Catálogo de componentes

Os 231 arquivos em `assets/components/` são exemplos TSX copiáveis. Escolha pela
intenção da interface e abra somente os candidatos relevantes.

| Família | Conteúdo |
| --- | --- |
| `actions-feedback/` | botões, menus, dialogs, alerts e banners |
| `data-display/` | tabelas, listas de descrição, avatares e badges |
| `forms/` | inputs, textareas, selects, comboboxes, radios e switches |
| `hero/` | primeiras dobras públicas e variações com navegação |
| `layout-navigation/` | shells, sidebars, navbars, autenticação, paginação e footers |
| `marketing-company/` | team, careers, offices, contact e support-contact |
| `marketing-content/` | blog, FAQ, press, about e conteúdo editorial |
| `marketing-conversion/` | CTA, newsletter, pricing e planos |
| `marketing-features/` | features, screenshots, workflows e support discovery |
| `marketing-proof/` | testimonials, logo clouds e stats |
| `typography/` | headings, texto, links e divisores |

## Descoberta

Listar a família sem carregar todo o catálogo:

```bash
rg --files assets/components/marketing-conversion
```

Filtrar nomes por intenção:

```bash
rg --files assets/components | rg 'pricing|comparison|toggle'
```

Ler dois ou três candidatos, comparar estrutura e dependências e escolher a
variante cuja intenção coincide com a composição definida pela skill de UI.
Nomes usados no mapa de composição, como `ui-hero`, correspondem à família
homônima desta tabela, como `assets/components/hero/`.
