---
type: readme
status: review
updated: 2026-01-24
---

# USE-CASES - GEOGIS

Casos de uso do plugin QGIS GEOGIS, focados na PARTE 2 do workflow: georreferenciamento e publicacao.

## Referencia

Todos os UCs implementam o [WORKFLOW-MESTRE](../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## PARTE 2: Georreferenciamento e Publicacao

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-P2-001](./UC-P2-001-autenticar-plugin-qgis/README.md) | Autenticar Plugin | Keycloak + Authentication Key |
| [UC-P2-002](./UC-P2-002-acessar-ortofotos-tenant/README.md) | Acessar Ortofotos | Catalogo do tenant |
| [UC-P2-003](./UC-P2-003-georreferenciar-poligonos/README.md) | Georreferenciar | Desenhar comunidades/quadras/lotes |
| [UC-P2-004](./UC-P2-004-publicar-trabalho-backend/README.md) | Publicar Trabalho | Liberar dados para campo |

## Fluxo Sequencial

```
[PARTE 1] -> UC-P2-001 -> UC-P2-002 -> UC-P2-003 -> UC-P2-004 -> [PARTE 3: REURBCAD]
```

## Casos de Uso Complementares

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-007](./UC-007-exportar-dados-geograficos/README.md) | Exportar Dados | Exportacao para formatos GIS |
| [UC-008](./UC-008-importar-shapefile/README.md) | Importar Shapefile | Importacao de shapefiles |

## Relacionamentos

- **GEOAPI**: Backend que processa importacoes e exportacoes
- **GEOWEB**: Portal para visualizacao dos dados processados
- **REURBCAD**: Destino dos dados publicados para campo
