---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-130: Listar Camadas

## Descricao

Sistema deve fornecer endpoint e interface para listar camadas GIS disponiveis no contexto do usuario permitindo navegacao e gerenciamento das layers configuradas. Filtro por comunidade permite visualizar apenas camadas especificas de comunidade selecionada em ambientes multi-comunidade. Listagem apresenta camadas ordenadas por campo display_order respeitando sequencia configurada pelos administradores para Z-index de renderizacao. Cada item exibe total de features contidas na camada fornecendo indicador de densidade de dados. Informacoes adicionais incluem nome, tipo de geometria, visibilidade atual e icone/cor representativa. Endpoint suporta paginacao e filtros adicionais por tipo de geometria ou status.

## Criterios de Aceitacao

1. Filtro por comunidade
2. Ordenacao por display_order
3. Total de features por camada
4. Informacoes de tipo e estilo
5. Paginacao para grandes volumes

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-017
