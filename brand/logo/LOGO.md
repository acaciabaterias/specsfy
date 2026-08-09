# Sistema de logo do Specsfy

As três camadas com código representam especificação, implementação e
evidência conectadas. A geometria principal vive em `icon.svg`; as demais
versões são derivações aprovadas.

O arquivo `icon.svg` usa uma prancheta de 512 × 512 px, preservada também no
fallback `icon.png`.

## Variantes

| Arquivo | Fundo |
| --- | --- |
| `icon.svg` | qualquer superfície, pois inclui placa petróleo |
| `icon-light.svg` | clara e uniforme |
| `icon-dark.svg` | escura e uniforme |
| `logo-light.svg` | assinatura horizontal sobre superfície clara |
| `logo-dark.svg` | assinatura horizontal sobre superfície escura |
| `icon.png` | sistemas sem suporte a SVG |

## Proteção e tamanho

- área livre: 12,5% da largura do ativo em todos os lados;
- ícone digital: mínimo de 28 px;
- assinatura horizontal: mínimo de 130 px;
- impressão: mínimo de 9 mm para o ícone.

## Restrições

- Não distorcer, girar, inclinar ou recortar.
- Não remover, separar ou reordenar as três camadas.
- Não inverter a imagem com filtros.
- Não aplicar gradiente, sombra, brilho, textura ou contorno.
- Não trocar violeta e turquesa por cores de estado.
- Não usar uma variante transparente sobre fundo sem contraste.

No SVG informativo, preserve título e descrição. Em HTML, use
`alt="Logo do Specsfy"` ou `alt=""` quando o nome visível já identificar a
marca.
