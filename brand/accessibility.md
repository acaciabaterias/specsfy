# Acessibilidade — Specsfy

A identidade combina contraste máximo no logo com cores funcionais verificadas
para interface. Nenhuma aprovação depende apenas de percepção visual.

## Método

Contraste calculado pela fórmula WCAG de luminância relativa:
`(L1 + 0.05) / (L2 + 0.05)`.

- **4.5:1** para texto normal.
- **3:1** para texto grande, componentes e objetos gráficos.

## Logo

As camadas pretas `#000000` sobre branco `#FFFFFF` atingem **21.00:1**. O
símbolo de código branco aparece dentro da placa preta com o mesmo contraste.

Regras:

- use o logo diretamente somente em fundo claro com pelo menos 3:1 contra o
  preto das camadas;
- em fundo escuro, fotográfico, colorido ou texturizado, use placa branca com a
  área de proteção definida em [`logo/LOGO.md`](logo/LOGO.md);
- não use inversão por CSS nem versão recolorida não publicada;
- preserve as três camadas: remover uma delas altera o significado e reduz a
  capacidade de reconhecimento;
- abaixo de 32 px, não publique o logo.

## Pares calculados da interface

| Par | Contraste | Resultado |
| --- | --- | --- |
| Black `#000000` / White `#FFFFFF` | **21.00:1** | AAA |
| Graphite `#171717` / White `#FFFFFF` | **17.93:1** | AAA |
| Gray `#737373` / White | **4.74:1** | AA texto normal |
| Gray `#A3A3A3` / Graphite | **7.11:1** | AAA |
| Link `#1D4ED8` / White | **6.70:1** | AA |
| Link `#93C5FD` / Graphite | **9.94:1** | AAA |
| Verified `#047857` / White | **5.48:1** | AA |
| Verified `#6EE7B7` / Graphite | **11.76:1** | AAA |
| Draft `#92400E` / White | **7.09:1** | AAA |
| Draft `#FCD34D` / Graphite | **12.43:1** | AAA |
| RED `#B91C1C` / White | **6.47:1** | AA |
| RED `#FCA5A5` / Graphite | **9.45:1** | AAA |

## Cor não é o único canal

- `RED`, `GREEN`, `Passed`, `Draft` e `Verified` aparecem como texto.
- Ícones de estado precisam de rótulo ou contexto adjacente.
- Links permanecem sublinhados ou distinguíveis por outro sinal.
- O ciclo TDD não depende apenas do par vermelho/verde.

## SVG e texto alternativo

O logo canônico contém `role="img"`, `<title>` e `<desc>`. Ao usar como arquivo:

```html
<img src="logo/icon.svg" alt="Logo do Specsfy">
```

Use `alt=""` somente quando o nome visível já torna a imagem redundante e ela
não funciona como link. Ícones conceituais seguem a mesma regra: rótulo útil ou
silêncio intencional, nunca `alt="imagem"`.

## Movimento e foco

- Elementos interativos têm `:focus-visible` com contraste mínimo 3:1.
- `prefers-reduced-motion: reduce` desativa rolagem suave, animações e
  transições não essenciais.
- O logo é estático. Não anime, pulse, gire ou desmonte as camadas.

## PNG

O fallback `logo/icon.png` deve permanecer RGBA, 512 × 512 e com transparência
externa. Exporte do SVG mestre; não introduza halo branco, fundo incorporado ou
compressão que borre o código.
