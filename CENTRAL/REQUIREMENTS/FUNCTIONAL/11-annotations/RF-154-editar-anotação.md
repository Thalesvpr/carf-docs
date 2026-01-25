---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-154: Editar Anotacao

## Descricao

Sistema deve permitir edicao de conteudo textual e posicao geografica de anotacoes existentes sem necessidade de recriar. Edicao inline do texto diretamente no popup ou painel de detalhes onde usuario clica no campo, digita modificacoes e confirma via blur automatico ou botao de salvar, garantindo processo rapido sem modais pesados. Para ajuste de posicao, modo de edicao permite arrastar icone da anotacao para nova localizacao no mapa, com coordenada atualizada ao soltar marcador. Alteracoes geram entradas no log de auditoria registrando usuario responsavel, timestamp, campos modificados e valores anteriores versus novos, garantindo rastreabilidade quando multiplos usuarios colaboram. Sistema valida que texto nao seja vazio e coordenadas permaneçam dentro de bounds validos.

## Criterios de Aceitacao

1. Edicao inline de texto
2. Movimentacao de marcador no mapa
3. Log de auditoria com diff de valores
4. Validacao de texto nao vazio
5. Validacao de coordenadas validas

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-153, RF-133
