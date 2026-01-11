# GEOGIS - Overview de Implementação

Plugin QGIS Python para operações GIS avançadas em desktop: edição de geometrias complexas, análises topológicas, processamento em batch e exportação de memoriais descritivos conforme NBR.

## Requirements Implementados

### Use Cases Principais

- [UC-007: Exportar Dados Geográficos](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md) - **CORE** - Export Shapefile/GeoJSON
- [UC-008: Importar Shapefile](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-008-importar-shapefile.md) - **CORE** - Batch import com validação topológica
- [UC-010: Configurar Camadas WMS](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-010-configurar-camadas-wms.md) - Ortofotos como base maps

## Domain Model Implementado

### Entities (subset GIS-specific)

Python dataclasses para models essenciais:

- Unit (geometry, area, attributes)
- Holder (CPF, nome, vinculação)
- Community (boundary polygon)
- WmsServer, WmsLayer (ortofotos)

### Value Objects (GIS-specific)

- GeoPolygon (Shapely geometries)
- GeoPoint (coordenadas)
- CPF (validação)

## Arquitetura Técnica

**Stack:**
- Python 3.11
- QGIS 3.34 API
- Shapely (geometrias)
- PyQt5 (UI dialogs)
- GDAL/OGR (Shapefile I/O)
- requests (HTTP client para GEOAPI)

**Autenticação:** API Key do GEOAPI (validada como ApiKey entity)

Ver [ARCHITECTURE/](./ARCHITECTURE/README.md).

## Features Documentadas

Features principais:
- Shapefile Import/Export - Importação e exportação batch com validação topológica
- Topological Validation - Detecção de overlaps, gaps, slivers

---

**Última atualização:** 2026-01-10
