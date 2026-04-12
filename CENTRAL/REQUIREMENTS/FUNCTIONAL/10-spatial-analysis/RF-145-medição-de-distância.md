---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-145: Medicao de Distancia

## Descricao

Sistema deve fornecer ferramenta interativa de medicao de distancia permitindo calcular comprimentos de trajetorias ou distancias entre pontos diretamente no mapa sem criar features permanentes. Interface permite ativar modo de medicao e realizar cliques sequenciais para marcar pontos, onde cada clique adiciona vertice a linha de medicao e sistema calcula automaticamente distancia acumulada. Distancia exibida em unidades apropriadas conforme magnitude (metros para distancias curtas, quilometros para longas com conversao automatica ao ultrapassar 1000m). Ferramenta inclui funcionalidade de limpeza para remover medicao atual e iniciar nova. Calculo considera geometria geodesica da Terra para precisao usando funcoes como ST_Distance com geografia. Visualizacao inclui linha conectando pontos, marcadores nos vertices e label mostrando distancia.

## Criterios de Aceitacao

1. Cliques sequenciais para marcar pontos
2. Calculo automatico de distancia acumulada
3. Unidades adaptativas (metros/quilometros)
4. Botao de limpeza para nova medicao
5. Calculo geodesico para precisao

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-053
