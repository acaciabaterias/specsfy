# Documentação do Specsfy

<p align="center">
  <picture>
    <source srcset="../brand/icons/icon.svg" type="image/svg+xml">
    <img src="../brand/icons/icon.png" alt="Ícone do framework Specsfy" width="96">
  </picture>
</p>

A documentação oficial possui dois percursos. Escolha de acordo com o que você
quer fazer:

| Percurso | Para quem | Comece aqui |
| --- | --- | --- |
| **User** | quem quer instalar e usar o Specsfy em um projeto | [Guia do usuário](user/README.md) |
| **Develop** | agentes e pessoas que contribuem, implementam ou modificam o framework | [Guia de desenvolvimento](develop/README.md) |

Se esta é sua primeira vez, siga o [guia do usuário](user/README.md). Ele usa
linguagem simples, mostra uma jornada completa e possui uma página com exemplos
para cada skill base.

Se você precisa entender decisões, arquitetura, testes, código do CLI ou como
alterar uma skill, siga o [guia de desenvolvimento](develop/README.md).

## Fonte da verdade

Os guias explicam o estado atual, mas não substituem as fontes executáveis:

- `skills/` implementa a metodologia;
- `cli/` implementa instalação, comandos e TUI;
- `specialists/` mantém o catálogo técnico opcional;
- `docs/develop/context/` registra decisões transversais;
- testes e manifests comprovam o comportamento implementado.
