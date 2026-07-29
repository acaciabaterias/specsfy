# Specsfy Specialists

<!-- markdownlint-disable MD033 -->
<p align="center">
  <picture>
    <source srcset="../brand/logo/icon.svg" type="image/svg+xml">
    <img src="../brand/logo/icon.png" alt="Logo do Specsfy" width="128">
  </picture>
</p>
<!-- markdownlint-enable MD033 -->

Catálogo oficial de skills técnicas opcionais do Specsfy. O prefixo
`specsfy-specialist-` distingue contexto especializado das skills
skills base que executam a metodologia.

Os especialistas são instalados sob demanda no projeto consumidor:

```bash
specsfy skills list
specsfy skills detect
specsfy skills add specsfy-specialist-laravel
```

Para implementar interfaces React a partir de referências copiáveis, instale e
use `specsfy-specialist-react-ui-components` em conjunto com
`specsfy-specialist-ui-design`. O CLI resolve e instala essa dependência
declarada no catálogo automaticamente.

O catálogo cobre a stack Promovaweb, design de interfaces, qualidade,
arquitetura, operação e disciplinas de engenharia. A referência completa de
instalação e uso pertence à
[`documentação do Specsfy`](../docs/).

Nenhuma skill deste módulo é instalada ou executada pela raiz do
[`promovaweb/specsfy`](https://github.com/promovaweb/specsfy).

## Validar

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
uv run --quiet --with behave behave tests/features --no-capture
```
