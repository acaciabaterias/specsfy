# Checklist de Qualidade de Interface

Use antes de finalizar uma tela ou componente.

## Estrutura

- A tela tem um objetivo principal claro.
- A hierarquia visual guia o usuario na ordem certa.
- O primeiro viewport comunica produto/oferta/acao sem depender de texto escondido.
- Secoes repetidas variam ritmo visual sem parecer aleatorias.
- Containers, max-width e spacing vertical estao consistentes.

## Responsividade

- Mobile nao tem overflow horizontal.
- Grids viram uma coluna quando necessario.
- Texto longo cabe dentro de botoes, cards e colunas.
- Imagens usam `aspect-*`, `object-cover` ou dimensoes estaveis.
- Navbars, footers e formularios continuam utilizaveis em telas pequenas.

## Acessibilidade

- Inputs tem `label` associado.
- Icon-only buttons/links tem `sr-only` ou `aria-label`.
- SVG decorativo usa `aria-hidden="true"`.
- Imagens informativas tem `alt` util; imagens decorativas usam `alt=""`.
- Landmarks semanticos fazem sentido: `header`, `main`, `section`, `article`, `footer`, `nav`, `form`.
- Foco e estados interativos sao visiveis.

## Dados e Estado

- Lists usam keys estaveis.
- Dados mockados sao faceis de substituir.
- Links `href="#"` foram trocados quando rotas reais existem.
- Formularios tem estados de erro/sucesso quando a acao importa.
- Acoes destrutivas pedem confirmacao quando aplicavel.

## Visual

- Dark mode foi preservado se a referencia tinha dark mode.
- Cores nao viram uma paleta monotona sem contraste.
- CTAs principais usam uma cor consistente.
- Cards nao ficam aninhados sem necessidade.
- Texto nao sobrepoe imagens de forma ilegivel.
- Imagens externas sao adequadas ao dominio ou foram substituidas por assets reais.

## Integracao

- Imports batem com dependencias do projeto.
- Componentes locais existentes foram preferidos quando houver design system.
- `Link`, `Button`, `Input`, `Avatar` ou wrappers locais foram usados se o app ja os possui.
- Nenhuma biblioteca nova foi introduzida sem necessidade.

## Validacao

- Se existe app executavel, rode lint/typecheck/test ou dev server conforme o projeto.
- Para UI significativa, verifique screenshot desktop e mobile quando possivel.
- Se nao foi possivel validar, registre isso na resposta final.
