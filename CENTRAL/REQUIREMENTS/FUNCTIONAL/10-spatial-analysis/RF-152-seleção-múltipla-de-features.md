---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
---

# RF-152: Selecao Multipla de Features

## Descricao

Sistema deve permitir selecao de multiplas features simultaneamente atraves de metodos de interacao intuitivos, facilitando operacoes em lote e analises comparativas. Usuarios podem selecionar conjunto de features via shift+click para adicionar individualmente ou desenho de retangulo de selecao (bbox) que captura todas as features cujas geometrias intersectam area delimitada. Ferramenta de selecao por retangulo permite arrastar cursor sobre mapa desenhando area e ao soltar todas features visiveis que intersectam bbox sao adicionadas. Sistema fornece highlight visual diferenciado para features selecionadas (cor, borda ou opacidade distintas) permanecendo visivel enquanto selecao esta ativa. Sistema habilita acoes em lote sobre features selecionadas incluindo exclusao multipla e edicao de atributos em massa para modificar valor de campo em todas features simultaneamente. Interface mostra contador de features selecionadas e botao para limpar selecao.

## Criterios de Aceitacao

1. Selecao via shift+click e retangulo
2. Highlight visual diferenciado
3. Exclusao multipla com confirmacao
4. Edicao de atributos em massa
5. Contador e botao limpar selecao

## Rastreabilidade

- Modulos: GEOWEB
- Requisitos dependentes: RF-132, RF-133, RF-134
