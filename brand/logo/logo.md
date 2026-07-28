# Logo — Specsfy

## Conceito

O símbolo combina três ideias do método em uma única forma:

1. **Documento com canto dobrado** — o `spec.md`, fonte única de verdade.
2. **Checkmark verde** — nada avança sem evidência; verde é reservado para o
   que foi verificado.
3. **Três marcas na base** — os três Atos rígidos (Definir, Projetar e
   provar, Entregar e validar).

O estilo é **flat**: formas sólidas preenchidas, sem traço/contorno. O
documento é uma silhueta preenchida (com o canto dobrado recortado como
vazado, não desenhado por cima); o checkmark vive dentro de um badge
circular preenchido — não é mais um traço colorido sobre o documento. Sem
gradiente, sombra ou efeito 3D em nenhuma parte.

## Arquivos

| Arquivo | Uso |
|---|---|
| `mark.svg` | Símbolo isolado, colorido, fundo transparente. Avatar, ícone de app, redes sociais. |
| `favicon.svg` | Símbolo com fundo sólido Midnight Mirage, documento preenchido Praxeti White. Otimizado para tamanhos pequenos (16–32px). |
| `logo-light.svg` | Símbolo + wordmark "Specsfy" em Midnight Mirage. Para fundos claros (Praxeti White). |
| `logo-dark.svg` | Símbolo + wordmark em Praxeti White. Para fundos escuros (Midnight Mirage, preto, fotos escuras). |

## Fronteira com o ícone do framework

O ícone do framework publicado em [`../icons/icon.svg`](../icons/icon.svg), com
fallback [`../icons/icon.png`](../icons/icon.png), identifica o framework e seus
repositórios. Ele não substitui `mark.svg`, `favicon.svg` nem os lockups com
wordmark desta pasta. Use os arquivos de `logo/` quando a peça exigir a
assinatura institucional completa; use o ícone do framework quando o contexto
for um README, uma interface de produto ou uma referência compacta ao
ecossistema.

## Área de proteção (clear space)

Mantenha ao redor do logo um espaço livre mínimo igual à altura do símbolo
dividida por 2 (metade da altura do ícone de documento, ~13px na escala
base). Nenhum outro elemento — texto, borda, outro logo — pode invadir essa
área.

## Tamanho mínimo

- Lockup completo (símbolo + wordmark): **96px** de largura.
- Símbolo isolado: **20px** de altura. Abaixo disso, use `favicon.svg`
  (fundo sólido lê melhor em tamanhos minúsculos que a silhueta isolada).

## Fundos permitidos

- `logo-light.svg` sobre Praxeti White ou fotografia clara.
- `logo-dark.svg` sobre Midnight Mirage ou fotografia escura.
- Nunca sobre fundos com padrão/textura que reduza o contraste das formas.

## Regra do checkmark

O checkmark vive dentro de um badge circular preenchido, sempre um verde de
verificação da paleta nomeada — nunca uma cor fora dela, nunca decorativo:

- Sobre fundo claro (Praxeti White): badge **Picture Book Green** `#00804C`
  com o check em Praxeti White por cima.
- Sobre fundo escuro (Midnight Mirage): badge **Mantis** `#74C365` com o
  check em Midnight Mirage por cima — Picture Book Green perde contraste
  sobre Midnight Mirage, por isso a troca do badge (o check em si sempre
  contrasta com o próprio badge, não com o fundo da peça).

## Não fazer

- Não usar qualquer verde fora de Picture Book Green/Mantis para o badge do checkmark.
- Não distorcer, inclinar ou espelhar o símbolo.
- Não adicionar sombra, brilho, contorno/traço ou efeito 3D às formas preenchidas.
- Não recriar o wordmark digitando "Specsfy" em outra fonte — use sempre os
  arquivos SVG fornecidos ou o arquivo de fonte real (IBM Plex Sans
  SemiBold) convertido em contorno.
- Não separar o símbolo do wordmark em um mesmo contexto de marca a menos
  que o espaço só comporte o símbolo (favicon, avatar).
- Não usar o símbolo sem o checkmark — sem ele, a forma perde o significado
  ("documento provado"), não só o visual.

## Nota técnica sobre o wordmark em SVG

`logo-light.svg` e `logo-dark.svg` usam `<text>` com a stack de fontes de
`brand/typography/typography.md`. Isso garante edição fácil, mas depende de
IBM Plex Sans estar disponível no ambiente de renderização. Para impressão,
apresentações ou qualquer uso onde a fonte não está garantida, converta o
texto em contornos (`Path > Object to Path` no Inkscape/Illustrator) antes de
exportar, e salve como um `logo-light-outlined.svg` ao lado do original.
