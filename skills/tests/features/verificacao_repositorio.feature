@specsfy @validation
Feature: Verificação do catálogo instalado
  Para validar projetos consumidores com contexto técnico opcional
  Como mantenedor da metodologia
  Quero aceitar as nove skills base junto de especialistas válidos

  Scenario: Validar catálogo base com especialistas instalados
    Given um projeto com nove skills base e dois especialistas válidos
    When o contrato do catálogo instalado é executado
    Then as onze skills são aceitas sem enfraquecer o catálogo base
