# Brand Gate — checklist de publicação

O Specsfy não deixa uma tarefa passar de `READY` para `DONE` sem evidência.
A marca segue a mesma regra: nenhum material — slide, post, README, tela —
sai como "pronto" só porque parece certo. Ele passa pelo **Brand Gate**
abaixo primeiro.

Use isto antes de publicar qualquer coisa com o nome, o símbolo ou a voz do
Specsfy. Se um item falhar, o material não está pronto — corrija ou
justifique a exceção por escrito ao lado do item.

## Cor

- [ ] Usa apenas as 6 cores nomeadas (`colors/palette.md`) + vermelho
      funcional — nenhuma cor de acento a mais.
- [ ] Picture Book Green/Mantis aparece **apenas** onde algo foi
      verificado/provado — não como decoração ou preenchimento neutro.
- [ ] First Colors of Spring aparece só como chip com texto Midnight
      Mirage por cima — nunca como cor de texto ou fundo de área grande.
- [ ] Se há texto sobre cor, o par passa 4.5:1 (ou 3:1 para texto
      grande/UI) — conferido em `accessibility.md`, não estimado a olho.
- [ ] Nenhum gradiente.

## Tipografia

- [ ] IBM Plex Sans para título/corpo, IBM Plex Mono para IDs/estados/código
      — nenhuma terceira família.
- [ ] IDs e estados do método (`US-01`, `Gate: Passed`, `RED`) estão em
      mono mesmo fora de bloco de código.

## Logo

- [ ] O símbolo sempre inclui as três partes juntas: documento, checkmark,
      três marcas. Nunca usado incompleto.
- [ ] Checkmark é Picture Book Green (fundo claro) ou Mantis (fundo
      escuro) — nunca outra cor.
- [ ] `logo-light.svg`/`logo-dark.svg` escolhido conforme o fundo real da
      peça, não por padrão.
- [ ] Respeita clear space e tamanho mínimo (`logo/logo.md`).
- [ ] Símbolo não foi distorcido, inclinado, espelhado, nem ganhou sombra
      ou brilho.

## Ícone do framework

- [ ] Usa `icons/icon.svg` como fonte preferencial e `icons/icon.png` somente
      como fallback raster do mesmo ícone do framework.
- [ ] Mantém geometria, proporção e cores dos arquivos canônicos, sem cópia
      divergente em outro repositório.
- [ ] Fornece `alt="Ícone do framework Specsfy"` ou rótulo acessível
      equivalente.
- [ ] Não apresenta o ícone do framework como substituto do logo institucional
      nem como parte dos oito ícones conceituais.

## Ícones

- [ ] Cada ícone usado corresponde ao conceito certo (`icons/icons.md`) —
      não há dois ícones para a mesma ideia no mesmo material.
- [ ] Ícones neutros usam `currentColor`; as duas exceções de cor fixa
      (`tdd-cycle.svg`, checkmarks de `evidence.svg`/`task.svg`) não foram
      recoloridas.
- [ ] Se `tdd-cycle.svg` aparece sozinho (sem texto RED/GREEN ao redor),
      foi avaliado o risco de daltonismo (`accessibility.md`).

## Voz

- [ ] Termos do glossário (`voice/voice.md`) grafados de forma canônica —
      sem sinônimo solto para Gate, Ato, RED/GREEN, handoff, evidência.
- [ ] Tagline usada é exatamente "Especifique. Prove. Entregue." (ou uma
      das alternativas listadas em `description.md`) — não uma paráfrase
      nova.
- [ ] Nenhuma promessa que o método não garante (velocidade, "menos bugs")
      — só rastreabilidade e evidência, ditas sem hype.
- [ ] Sem emoji como marcador de seção/status, sem metáfora de guerra ou
      esporte, sem "simplesmente".

## Acessibilidade

- [ ] Elementos interativos têm estado de foco visível (`:focus-visible`),
      não só `:hover`.
- [ ] Animações/transições respeitam `prefers-reduced-motion`.
- [ ] SVGs mantêm `role="img"` + `aria-label` (ou `alt` equivalente) ao
      serem reutilizados.

## Fonte única

- [ ] Se este material mudou uma regra (nova cor, nova exceção, novo
      termo), a fonte normativa correspondente foi atualizada — não só o
      material final. Ver a tabela em `guidelines.md`.
- [ ] `README.md` e `guidelines.md` ainda apontam para todos os arquivos
      que existem — nenhum arquivo novo ficou fora do índice.

---

Se tudo acima está marcado, o material passou no Brand Gate. Se algo não
se aplica (ex.: peça sem texto, sem interatividade), marque como N/A com uma
frase dizendo por quê — omissão silenciosa não conta como "passou".
