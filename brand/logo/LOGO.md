# Logo oficial do Specsfy

Este documento é a fonte normativa de uso do logo. A geometria exata vive em
[`icon.svg`](icon.svg); [`icon.png`](icon.png) é o fallback raster derivado do
mesmo desenho. Nenhuma cópia em outro diretório é canônica.

## Conceito

O logo representa o método como uma pilha de software verificável:

1. **Três camadas** representam os três Atos — Definir, Projetar e provar,
   Entregar e validar. Nenhuma camada existe isoladamente.
2. **Os intervalos entre as camadas** representam Gates e handoffs: cada avanço
   preserva o que foi definido e comprovado abaixo.
3. **A placa superior preenchida** concentra o resultado corrente do trabalho.
4. **O símbolo de código em negativo** (`</>`) comunica que a especificação
   chega a software executável sem perder rastreabilidade.

O desenho é modular, técnico e direto. A profundidade vem da repetição das
camadas, não de sombra, gradiente ou perspectiva fotográfica.

## Construção

- Prancheta: **512 × 512** unidades, `viewBox="0 0 512 512"`.
- Proporção: **1:1**; nunca recortar nem transformar em retângulo.
- Placa superior: forma preenchida, com vértices laterais e cantos arredondados.
- Placas intermediária e inferior: caminhos abertos com traço de **36 unidades**.
- Código: três caminhos com traço de **32 unidades**, pontas e junções
  arredondadas.
- Eixo: todas as formas são centralizadas em `x = 256`.
- Limites visuais aproximados: `x = 16–496` e `y = 14–496`.
- Camadas editáveis do SVG:
  `layer-bottom`, `layer-middle`, `layer-top`, `layer-code-left`,
  `layer-code-slash` e `layer-code-right`.

Os grupos são camadas nomeadas do Inkscape. Preserve nomes, ordem e IDs ao
editar; eles tornam a construção auditável e evitam uma silhueta achatada sem
estrutura.

## Arquivos canônicos

| Arquivo | Papel | Quando usar |
| --- | --- | --- |
| [`icon.svg`](icon.svg) | fonte vetorial mestre, 512 × 512, editável por camadas | README, web, interface, impressão e qualquer material escalável |
| [`icon.png`](icon.png) | fallback RGBA, 512 × 512, fundo transparente | plataformas que não aceitam SVG |

Use SVG por padrão. Use PNG somente por incompatibilidade técnica. Ao exportar
outro tamanho raster, derive-o do SVG e não redimensione repetidamente o PNG.

## Cores

O logo é estritamente monocromático:

| Elemento | Valor |
| --- | --- |
| três camadas | preto `#000000` |
| símbolo de código | branco `#FFFFFF` |
| área externa | transparente |

Preto e branco são parte da geometria: o branco não é um acento e sim o recorte
que torna `</>` legível. Não aplique cores semânticas, `currentColor`,
gradiente, opacidade, textura ou duotone ao arquivo canônico.

## Área de proteção

Defina `x` como a espessura estrutural de **36 unidades** do SVG. Mantenha no
mínimo `1x` de espaço livre em todos os lados, equivalente a aproximadamente
**7%** da largura renderizada.

Exemplos:

| Logo renderizado | Proteção mínima em cada lado |
| --- | --- |
| 32 px | 3 px |
| 64 px | 5 px |
| 128 px | 9 px |
| 256 px | 18 px |

Texto, borda, outro logo, recorte de imagem ou margem da peça não pode invadir
essa área. A transparência interna do arquivo não substitui a proteção externa.

## Tamanho mínimo

- Digital: **32 px** de largura e altura.
- Impresso: **8 mm** de largura e altura.
- README do monorepo: **128 px**.

Abaixo de 32 px, as três camadas e o símbolo de código perdem separação. Não
remova detalhes para criar uma versão reduzida; solicite um ativo específico e
atualize este contrato antes de publicá-lo.

## Fundos

O ativo canônico foi desenhado para fundo branco `#FFFFFF` ou neutro muito
claro. O preto das camadas deve manter contraste mínimo de 3:1 contra a
superfície.

- Em fundo claro: use o arquivo diretamente.
- Em fundo escuro, colorido, fotográfico ou texturizado: coloque o logo dentro
  de uma placa branca com proteção mínima de `1x`.
- Não use o arquivo diretamente sobre preto: as camadas desaparecem.
- Não use `filter: invert()`, blend mode ou recoloração improvisada para criar
  uma versão reversa.

Não existe variante escura oficial. Uma futura variante só passa a existir
quando possuir arquivo canônico próprio, regra de contraste e atualização deste
documento.

## Assinatura e nome

O logo oficial é somente o símbolo quadrado. Não há wordmark nem lockup
horizontal aprovado.

Quando o nome **Specsfy** acompanhar o logo:

- componha o nome como texto editorial independente em IBM Plex Sans SemiBold;
- mantenha pelo menos `1x` entre símbolo e nome;
- não una os dois elementos num novo arquivo chamado “logo”;
- não use outra grafia, caixa alta integral ou fonte para simular um wordmark.

A tagline “Especifique. Comprove. Entregue.” também fica fora da área de
proteção e não integra o logo.

## Acessibilidade

- Preserve `role="img"`, `<title>` e `<desc>` do SVG.
- Em `<img>`, use `alt="Logo do Specsfy"`.
- Se o nome visível ao lado já identifica a marca e a repetição for redundante,
  use `alt=""` somente quando o logo for estritamente decorativo.
- Não dependa apenas da forma para comunicar uma ação ou estado.
- Garanta 3:1 entre as camadas pretas e o fundo.
- O PNG deve manter canal alfa e dimensões de 512 × 512.

## Usos incorretos

- Não distorcer, inclinar, girar ou espelhar.
- Não recortar nenhuma das três camadas.
- Não separar ou reordenar as camadas.
- Não alterar a espessura de 36 unidades das placas nem a de 32 unidades do
  código.
- Não trocar `</>` por outro glifo.
- Não adicionar sombra, brilho, contorno, volume, gradiente ou animação.
- Não recolorir partes isoladas.
- Não aplicar diretamente em fundo escuro ou complexo.
- Não recriar o logo em outra ferramenta quando o SVG canônico puder ser usado.
- Não manter cópia divergente em outro módulo.

## Checklist

- [ ] O arquivo vem de `brand/logo/icon.svg` ou do fallback `icon.png`.
- [ ] As três camadas e o símbolo de código estão completos.
- [ ] A proporção permanece 1:1.
- [ ] As cores continuam `#000000` e `#FFFFFF`.
- [ ] A proteção mínima de `1x` (7%) foi respeitada.
- [ ] O tamanho é pelo menos 32 px digital ou 8 mm impresso.
- [ ] O fundo é claro ou existe uma placa branca de proteção.
- [ ] O texto alternativo ou rótulo acessível está presente.
- [ ] Nenhum efeito, recoloração ou wordmark improvisado foi adicionado.
