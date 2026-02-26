---
type: readme
status: review
updated: 2026-02-07
---

# USE-CASES - GEOGIS

Esta secao documenta os casos de uso do plugin QGIS GEOGIS focados na PARTE 2 do workflow mestre, que abrange georreferenciamento e publicacao. Todos os casos de uso aqui descritos implementam o fluxo definido no WORKFLOW-MESTRE documentado em CENTRAL.

O fluxo sequencial da PARTE 2 inicia com a autenticacao dupla via Keycloak e Authentication Key no UC-P2-001, seguido pelo acesso ao catalogo de ortofotos do tenant no UC-P2-002, pelo desenho de comunidades, quadras e lotes no UC-P2-003, e pela publicacao do trabalho que libera dados para campo no UC-P2-004. Ao concluir esta parte, os dados ficam disponiveis para a PARTE 3 executada pelo REURBCAD. O GEOGIS integra-se com GEOAPI como backend para processamento de importacoes e exportacoes, com REURBWEB como portal de visualizacao dos dados processados, e com REURBCAD como destino dos dados publicados para campo.

## PARTE 2: Georreferenciamento e Publicacao

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-P2-001](./UC-P2-001-autenticar-plugin-qgis/README.md) | Autenticar Plugin | Keycloak + Authentication Key |
| [UC-P2-002](./UC-P2-002-acessar-ortofotos-tenant/README.md) | Acessar Ortofotos | Catalogo do tenant |
| [UC-P2-003](./UC-P2-003-georreferenciar-poligonos/README.md) | Georreferenciar | Desenhar comunidades/quadras/lotes |
| [UC-P2-004](./UC-P2-004-publicar-trabalho-backend/README.md) | Publicar Trabalho | Liberar dados para campo |

## Casos de Uso Complementares

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-007](./UC-007-exportar-dados-geograficos/README.md) | Exportar Dados | Exportacao para formatos GIS |
| [UC-008](./UC-008-importar-shapefile/README.md) | Importar Shapefile | Importacao de shapefiles |
