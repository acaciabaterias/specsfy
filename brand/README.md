# Marca Specsfy

<p align="center">
  <picture>
    <source srcset="logo/icon.svg" type="image/svg+xml">
    <img src="logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>

Este diretório é a fonte normativa da identidade visual e verbal do Specsfy.
O sistema transforma intenção em software verificável por meio de especificação,
evidência e gates explícitos.

O [guia de marca em PDF](Specsfy-Manual-de-Marca.pdf) é o artefato de
distribuição. Este README e os arquivos especializados abaixo são suas fontes
editáveis.

## Essência

**Posicionamento:** Specsfy é o framework de especificação executável que
conecta intenção, decisão, implementação e evidência em um fluxo auditável.

**Promessa:** do pedido à prova, sem perder contexto.

**Tagline principal:** `Specify. Prove. Ship.`

### Personalidade

- **Precisa:** afirma somente o que pode sustentar.
- **Estruturada:** torna etapas, relações e limites visíveis.
- **Pragmática:** privilegia decisões e próximos passos úteis.
- **Auditável:** liga afirmações a fontes e evidências.
- **Sóbia:** usa contraste, espaço e hierarquia em vez de ornamento.

## Conceito visual

O logo é um símbolo quadrado, preto e branco, formado por **três camadas** e um
**símbolo de código**:

- as três camadas representam os três Atos da metodologia;
- os intervalos representam Gates e passagens verificáveis;
- a placa superior preenchida representa o resultado acumulado;
- o símbolo `</>` representa especificação executável e software.

O desenho é modular, direto e monocromático. Ele substitui integralmente a
identidade anterior; não existem variantes de tema nem wordmark oficial.

## Logo oficial

Os únicos arquivos canônicos são:

| Arquivo | Uso |
| --- | --- |
| [`logo/icon.svg`](logo/icon.svg) | Preferencial em documentação, web, produto e impressão |
| [`logo/icon.png`](logo/icon.png) | Fallback raster e integrações sem suporte a SVG |

Todas as regras de construção, área de proteção, tamanho mínimo, fundos,
acessibilidade e usos incorretos estão em
[`logo/LOGO.md`](logo/LOGO.md).

Resumo operacional:

- preserve a proporção quadrada e todas as três camadas;
- mantenha o preto `#000000` e o branco `#FFFFFF`;
- reserve área livre mínima de `1x`, sendo `x = 36` unidades do SVG
  (aproximadamente 7% da largura renderizada);
- use no mínimo 32 px em interfaces e 8 mm em impressão;
- em fundo escuro, colorido ou fotográfico, aplique uma placa branca com a área
  de proteção;
- não inverta, recolora, rotacione, corte, distorça, sombreie ou reorganize as
  camadas;
- quando o nome “Specsfy” acompanhar o símbolo, trate-o como texto editorial,
  fora da área de proteção; isso não cria um lockup.

### Padrão para README

Use 128 px e fallback explícito:

```html
<p align="center">
  <picture>
    <source srcset=".../brand/logo/icon.svg" type="image/svg+xml">
    <img src=".../brand/logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>
```

Ajuste apenas o prefixo `...` à profundidade do README.

## Cores

Preto e branco constituem a assinatura. A interface editorial usa neutros; as
cores funcionais comunicam significado e nunca alteram o logo.

| Papel | Claro | Escuro |
| --- | --- | --- |
| Assinatura | Black `#000000` | White `#FFFFFF` |
| Texto/superfície principal | Graphite `#171717` | Fog `#F5F5F5` |
| Texto secundário | Gray 500 `#737373` | Gray 400 `#A3A3A3` |
| Link | `#1D4ED8` | `#93C5FD` |
| Verificado | `#047857` | `#6EE7B7` |
| Rascunho/atenção | `#92400E` | `#FCD34D` |
| Erro/bloqueio | `#B91C1C` | `#FCA5A5` |

Contrastes de texto verificados:

| Combinação | Razão |
| --- | ---: |
| Black / White | 21.00:1 |
| Graphite / White | 17.93:1 |
| Gray 500 / White | 4.74:1 |
| Gray 400 / Graphite | 7.11:1 |
| Link claro / White | 6.70:1 |
| Link escuro / Graphite | 9.94:1 |

Consulte [`colors/palette.md`](colors/palette.md) para funções e acessibilidade,
e reutilize [`colors/tokens.css`](colors/tokens.css) ou
[`colors/tokens.json`](colors/tokens.json).

## Tipografia

IBM Plex é a família oficial:

- **IBM Plex Sans:** interface, títulos e texto corrido;
- **IBM Plex Mono:** código, comandos, caminhos, IDs e evidências.

Priorize legibilidade, hierarquia curta e alinhamento funcional. Não simule a
marca compondo “Specsfy” com uma fonte decorativa. Regras completas:
[`typography/typography.md`](typography/typography.md).

## Voz

A voz é direta, verificável e respeitosa:

- diga primeiro o resultado ou a decisão;
- prefira verbos concretos e frases curtas;
- diferencie fato, inferência, recomendação e estado;
- declare limites e próximos passos sem teatralidade;
- preserve termos técnicos quando eles carregam precisão.

Exemplos:

| Evite | Prefira |
| --- | --- |
| “Tudo pronto!” | “Os 42 testes passaram; a publicação ainda não foi executada.” |
| “Talvez seja melhor revisar.” | “Revise o schema antes de alterar o endpoint.” |
| “O sistema é super robusto.” | “O fluxo bloqueia a entrega quando falta evidência.” |

Consulte [`voice/voice.md`](voice/voice.md) e
[`description.md`](description.md).

## Ícones

Ícones de interface são monocromáticos, geométricos, desenhados em grade 32 ×
32 e têm função semântica. Eles não são versões do logo e não podem reproduzir
suas três camadas ou seu símbolo de código.

O catálogo e as regras ficam em [`icons/icons.md`](icons/icons.md). O estado
deve ser comunicado por forma, rótulo e, opcionalmente, cor funcional.

## Acessibilidade

- texto normal precisa alcançar WCAG AA (4.5:1);
- texto grande precisa alcançar pelo menos 3:1;
- foco visível, estado e ação não dependem apenas de cor;
- o logo informativo usa `alt="Logo do Specsfy"`;
- o logo decorativo usa `alt=""`;
- nenhuma textura ou fotografia pode atravessar o símbolo;
- SVG é preferencial; PNG deve permanecer nítido no tamanho final.

Veja a matriz completa em [`accessibility.md`](accessibility.md).

## Brand Gate

Antes de publicar:

- [ ] a mensagem cumpre promessa, posicionamento e voz;
- [ ] o logo vem de `logo/icon.svg` ou `logo/icon.png`;
- [ ] proporção, cores, área de proteção e tamanho mínimo foram preservados;
- [ ] fundo complexo recebeu placa branca;
- [ ] IBM Plex Sans e Mono foram aplicadas por função;
- [ ] cores funcionais não foram usadas como decoração;
- [ ] contraste, foco, rótulos e texto alternativo foram verificados;
- [ ] links, comandos, números e evidências foram conferidos;
- [ ] não existem assets, variantes ou regras paralelas.

O checklist operacional está em [`checklist.md`](checklist.md).

## Mapa da fonte

| Tema | Fonte |
| --- | --- |
| Manual do logo | [`logo/LOGO.md`](logo/LOGO.md) |
| Logo vetorial | [`logo/icon.svg`](logo/icon.svg) |
| Fallback raster | [`logo/icon.png`](logo/icon.png) |
| Paleta | [`colors/palette.md`](colors/palette.md) |
| Tokens | [`colors/tokens.css`](colors/tokens.css), [`colors/tokens.json`](colors/tokens.json) |
| Tipografia | [`typography/typography.md`](typography/typography.md) |
| Voz | [`voice/voice.md`](voice/voice.md) |
| Descrição institucional | [`description.md`](description.md) |
| Ícones conceituais | [`icons/icons.md`](icons/icons.md) |
| Acessibilidade | [`accessibility.md`](accessibility.md) |
| Referência rápida | [`guidelines.md`](guidelines.md) |
| Brand Gate | [`checklist.md`](checklist.md) |
| Fonte do PDF | [`guide/brand-guide.md`](guide/brand-guide.md) |
| Guia visual HTML | [`style-guide.html`](style-guide.html) |

## Manutenção

Mudanças na identidade devem atualizar na mesma entrega:

1. a fonte temática correspondente;
2. este README;
3. `guide/brand-guide.md` e, quando aplicável, `style-guide.html`;
4. o PDF com `make brand-guide`;
5. os contratos automatizados e os READMEs afetados.

Não edite artefatos dentro de `guide/build/` manualmente.
