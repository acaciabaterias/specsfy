# Manual de Marca — Specsfy

Este manual governa a identidade verbal e visual do Specsfy. A marca expressa
um framework de especificação executável: intenção, decisão, implementação e
evidência conectadas por um processo auditável.

## 1. Fundamentos

### Posicionamento

Specsfy é o framework de especificação executável que conecta intenção,
decisão, implementação e evidência em um fluxo auditável.

### Promessa e tagline

> Do pedido à prova, sem perder contexto.

Tagline principal: `Especifique. Comprove. Entregue.`

### Personalidade

| Atributo | Como aparece |
| --- | --- |
| Precisa | Faz afirmações sustentadas por fonte ou evidência |
| Estruturada | Expõe etapas, relações, limites e estados |
| Pragmática | Conduz a uma decisão ou próximo passo útil |
| Auditável | Mantém rastreabilidade entre intenção e prova |
| Sóbria | Usa contraste, espaço e hierarquia sem ornamento gratuito |

## 2. Conceito visual

O logo é um símbolo quadrado monocromático formado por **três camadas** e um
**símbolo de código** `</>`.

- as três camadas representam os três Atos da metodologia;
- os intervalos entre elas representam Gates e passagens verificáveis;
- a placa superior preenchida representa o resultado acumulado;
- o símbolo de código representa especificação executável e software.

O resultado é modular, técnico e memorável. A forma deve permanecer inteira:
suprimir ou reorganizar uma camada altera o significado.

## 3. Logo oficial

![Logo do Specsfy](../logo/icon.svg){width=128px}

### Arquivos canônicos

| Arquivo | Aplicação |
| --- | --- |
| `logo/icon.svg` | Fonte preferencial para documentação, web, produto e impressão |
| `logo/icon.png` | Fallback raster para sistemas sem suporte a SVG |

Não existem wordmark, versão invertida ou variante por tema. O nome “Specsfy”
pode acompanhar o símbolo como texto editorial, sempre fora da área de
proteção, mas essa composição não constitui uma assinatura oficial.

### Construção

O desenho usa canvas e `viewBox` de 512 × 512. Os grupos editáveis são:
`layer-bottom`, `layer-middle`, `layer-top`, `layer-code-left`,
`layer-code-slash` e `layer-code-right`.

- contorno das camadas: 36 unidades;
- contorno do código: 32 unidades;
- extremidades e junções arredondadas;
- placa superior preenchida em preto;
- símbolo de código branco.

### Cores

O logo usa exclusivamente:

| Elemento | Cor |
| --- | --- |
| Camadas e placa superior | Black `#000000` |
| Símbolo de código | White `#FFFFFF` |
| Exterior do símbolo | Transparente |

Não recolora o logo com cores funcionais ou de campanha.

### Área de proteção

Reserve `1x` em todos os lados, sendo `x = 36` unidades do SVG. Em qualquer
tamanho renderizado isso equivale a aproximadamente 7% da largura do símbolo.
Texto, bordas, outros logos e conteúdo visual não entram nessa área.

### Tamanho mínimo

- digital: 32 × 32 px;
- impressão: 8 × 8 mm;
- cabeçalho de README: 128 × 128 px.

Acima desses mínimos, preserve a proporção quadrada e prefira o SVG.

### Fundos

- fundo branco ou muito claro: aplique o asset diretamente;
- fundo escuro, colorido, texturizado ou fotográfico: use uma placa branca que
  inclua toda a área de proteção;
- nunca use filtro de inversão;
- nunca permita que o fundo atravesse as áreas internas ou prejudique os
  contornos.

### Usos incorretos

<div class="dont">

- não inverter preto e branco;
- não recolorir, aplicar gradiente, sombra, brilho ou textura;
- não girar, inclinar, comprimir ou esticar;
- não cortar a forma nem remover camadas;
- não mudar a ordem ou o espaçamento das camadas;
- não redesenhar o símbolo de código;
- não encerrá-lo em formas que reduzam a área de proteção;
- não criar lockup ou variante paralela.

</div>

O contrato detalhado vive em `logo/LOGO.md`.

## 4. Sistema de cores

Preto e branco formam a assinatura. Neutros organizam a leitura. Azul, verde,
âmbar e vermelho são reservados a funções e estados.

<div class="swatch-grid">
  <div class="swatch"><div class="swatch-color" style="background:#000000"></div><div class="swatch-meta"><div class="swatch-token">Black</div><div class="swatch-hex">#000000</div><div class="swatch-usage">Logo e texto de maior ênfase</div></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#FFFFFF"></div><div class="swatch-meta"><div class="swatch-token">White</div><div class="swatch-hex">#FFFFFF</div><div class="swatch-usage">Logo e superfície principal</div></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#171717"></div><div class="swatch-meta"><div class="swatch-token">Graphite</div><div class="swatch-hex">#171717</div><div class="swatch-usage">Texto e superfície escura</div></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#F5F5F5"></div><div class="swatch-meta"><div class="swatch-token">Fog</div><div class="swatch-hex">#F5F5F5</div><div class="swatch-usage">Superfície secundária</div></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#1D4ED8"></div><div class="swatch-meta"><div class="swatch-token">Link</div><div class="swatch-hex">#1D4ED8</div><div class="swatch-usage">Links e foco no tema claro</div></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#047857"></div><div class="swatch-meta"><div class="swatch-token">Verified</div><div class="swatch-hex">#047857</div><div class="swatch-usage">Estado comprovado</div></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#92400E"></div><div class="swatch-meta"><div class="swatch-token">Draft</div><div class="swatch-hex">#92400E</div><div class="swatch-usage">Atenção ou rascunho</div></div></div>
  <div class="swatch"><div class="swatch-color" style="background:#B91C1C"></div><div class="swatch-meta"><div class="swatch-token">Blocked</div><div class="swatch-hex">#B91C1C</div><div class="swatch-usage">Erro ou bloqueio</div></div></div>
</div>

### Contraste verificado

| Combinação | Razão |
| --- | ---: |
| Black / White | 21.00:1 |
| Graphite / White | 17.93:1 |
| Gray 500 / White | 4.74:1 |
| Gray 400 / Graphite | 7.11:1 |
| Link claro / White | 6.70:1 |
| Link escuro / Graphite | 9.94:1 |
| Verified claro / White | 5.48:1 |
| Draft claro / White | 7.09:1 |
| Blocked claro / White | 6.47:1 |

Cor nunca é o único indicador de estado. Combine forma, rótulo e mensagem.

## 5. Tipografia

IBM Plex traduz a precisão técnica sem perder legibilidade.

<div class="type-sample">
  <div class="type-row"><div class="type-label">Display</div><div><div class="t-display">Intenção que chega à prova.</div><span class="type-spec">IBM Plex Sans · 600</span></div></div>
  <div class="type-row"><div class="type-label">Título</div><div><div class="t-h2-sample">Decisões rastreáveis</div><span class="type-spec">IBM Plex Sans · 600</span></div></div>
  <div class="type-row"><div class="type-label">Corpo</div><div><div class="t-body-sample">Cada mudança preserva contexto e registra evidência.</div><span class="type-spec">IBM Plex Sans · 400</span></div></div>
  <div class="type-row"><div class="type-label">Código</div><div><span class="t-mono-sample">specsfy install --target ./projeto</span><span class="type-spec">IBM Plex Mono · 400/500</span></div></div>
</div>

- IBM Plex Sans: títulos, corpo, navegação e interface;
- IBM Plex Mono: código, comandos, caminhos, IDs, métricas e evidência;
- pesos preferenciais: 400 e 600;
- não use fonte decorativa para simular um wordmark.

## 6. Voz e tom

### Princípios

1. Comece pelo resultado, decisão ou propósito.
2. Use verbos concretos e frases que possam ser verificadas.
3. Separe fato, inferência, recomendação e estado.
4. Quantifique evidências quando possível.
5. Declare limites e o próximo passo.

### Exemplos

| Evite | Prefira |
| --- | --- |
| “Tudo pronto!” | “Os 42 testes passaram; a publicação ainda não foi executada.” |
| “Talvez seja melhor revisar.” | “Revise o schema antes de alterar o endpoint.” |
| “O sistema é robusto.” | “O Gate bloqueia a entrega quando falta evidência.” |

Em erro, seja específico e acionável. Em conteúdo institucional, mantenha a
mesma precisão, sem transformar sobriedade em frieza.

## 7. Ícones

Ícones conceituais são recursos de interface, não variantes do logo.

- grade de 32 × 32;
- traço base de 2.4 unidades;
- cantos e terminais arredondados;
- desenho monocromático;
- estado comunicado também por rótulo;
- proibido copiar as três camadas ou o símbolo de código do logo.

O catálogo inclui discovery, specification, plan, task, evidence, gate,
verified e blocked. A fonte normativa é `icons/icons.md`.

## 8. Acessibilidade

- texto normal: contraste mínimo de 4.5:1;
- texto grande e componentes essenciais: mínimo de 3:1;
- foco visível em controles;
- zoom e modo escuro sem perda de conteúdo;
- logo informativo: `alt="Logo do Specsfy"`;
- logo decorativo: `alt=""`;
- SVG preferencial e PNG nítido no tamanho final;
- nenhum significado transmitido apenas por cor.

## 9. Aplicações

### README

```html
<p align="center">
  <picture>
    <source srcset=".../brand/logo/icon.svg" type="image/svg+xml">
    <img src=".../brand/logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>
```

### Interfaces

Use superfícies amplas, bordas discretas e hierarquia baseada em contraste e
espaço. Reserve cor a links, foco e estados. Evidências e comandos usam Mono.

### Materiais com fundo complexo

Crie uma placa branca sem efeito, respeitando `1x` em todos os lados. Não
adapte o asset à fotografia.

## 10. Brand Gate

<ul class="checklist">
<li>Posicionamento, promessa e voz permanecem coerentes.</li>
<li>O logo veio de icon.svg ou icon.png.</li>
<li>Três camadas, símbolo de código, proporção e cores estão íntegros.</li>
<li>Área de proteção, tamanho mínimo e tratamento de fundo foram respeitados.</li>
<li>IBM Plex Sans e Mono cumprem suas funções.</li>
<li>Cores funcionais têm significado e contraste suficiente.</li>
<li>Foco, rótulos e texto alternativo foram verificados.</li>
<li>Não existe asset, regra ou fonte paralela.</li>
</ul>

## 11. Governança

As fontes especializadas vivem em `brand/`. Alterações devem sincronizar
README, manual do logo, paleta, tokens, guia visual, fonte deste PDF e testes.
O PDF é reconstruído na raiz com:

```bash
make brand-guide
```

Não edite o PDF ou arquivos de `guide/build/` manualmente.
