---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-046: Configurar Camadas WMS para Comunidade

## Descricao

Usuarios com role ADMIN podem configurar camadas WMS/WMTS de base especificas para visualizacao de comunidade. URL de servico WMS configuravel atraves de formulario validando conectividade e compatibilidade com padroes OGC. Selecao de layers disponiveis no servico apresentada atraves de interface onde sistema consulta GetCapabilities. Ordem de renderizacao configuravel atraves de drag-and-drop permitindo composicao visual adequada.

## Criterios de Aceitacao

1. Configuracao de URL de servico WMS/WMTS
2. Validacao de conectividade e compatibilidade OGC
3. Selecao de layers via GetCapabilities
4. Ordem de renderizacao configuravel
5. Persistencia de configuracao por comunidade

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-038
