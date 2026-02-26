---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-159: Listar Levantamentos

## Descricao

Sistema deve fornecer endpoint e interface para listar levantamentos topograficos cadastrados permitindo navegacao e acesso a registros de trabalhos de campo. Filtros por comunidade (visualizar apenas levantamentos de localidade selecionada) e por data ou range de datas (localizar levantamentos de periodo especifico via data inicial e final ou presets como ultimo mes, ultimo trimestre). Paginacao robusta para grandes volumes com paginas de tamanho configuravel (20 a 50 registros), controles de navegacao e metadados de paginacao. Cada item exibe status do levantamento (em andamento, concluido, processado) via badge colorido para identificacao rapida. Informacoes adicionais incluem data, responsavel, comunidade e acoes disponiveis.

## Criterios de Aceitacao

1. Filtro por comunidade
2. Filtro por range de datas
3. Paginacao com metadados
4. Status com badge visual
5. Informacoes resumidas por item

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-157, RF-017
