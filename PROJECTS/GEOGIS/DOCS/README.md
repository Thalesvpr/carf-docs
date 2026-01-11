# GEOGIS - Plugin QGIS para Operações GIS Avançadas

**[📋 Overview de Implementação](./OVERVIEW.md)** - Mapeamento completo de requirements, domain model e arquitetura técnica

Plugin QGIS Python para operações GIS avançadas complementando portal web GEOWEB com análises espaciais complexas, permitindo técnicos GIS especializados executarem geoprocessamento de dados CARF diretamente em QGIS desktop, integrando com backend [GEOAPI](../../GEOAPI/DOCS/ARCHITECTURE/01-overview.md) via REST API consumindo endpoints WFS (Web Feature Service) e WMS (Web Map Service) expostos por PostGIS conforme [ADR-002](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md), autenticação via token JWT obtido de [Keycloak](../../KEYCLOAK/DOCS/README.md), importação/exportação de Shapefiles GeoJSON KML sincronizando com [GEOAPI /api/communities](../../../CENTRAL/API/COMMUNITIES/README.md), análises de overlay buffer intersection difference gerando novos layers, validação de topologia detectando polígonos inválidos auto-overlaps gaps, e cálculos geométricos precisos (área perímetro centroid) conforme padrões OGC Simple Features.

## Funcionalidades Principais

**Conexão GEOAPI** - Autenticação via JWT, listagem de comunidades/unidades disponíveis, download de layers como vector layers QGIS temporários, e upload de edições de volta para GEOAPI.

**Análises Espaciais** - Buffer de unidades para análise de vizinhança, intersection de comunidades com limites administrativos, union de polígonos adjacentes criando áreas consolidadas, e difference para identificar gaps.

**Validação de Topologia** - Detecção automática de geometrias inválidas (self-intersection overlaps gaps slivers), correção via MakeValid, e relatório de problemas encontrados.

**Exportação de Mapas** - Layout templates para impressão de mapas cadastrais incluindo legenda escala norte, export para PDF/PNG alta resolução, e batch print de múltiplas comunidades.

**Sincronização Bidirecional** - Download incremental apenas de dados modificados desde última sync, upload de edições com conflict detection, e merge changes com estratégia configurable.

Ver [índice completo de features implementadas](./FEATURES/README.md) mapeando casos de uso do sistema.

## Documentação

- **[Arquitetura](./ARCHITECTURE/README.md)** - Decisões técnicas de integração Keycloak e estrutura do plugin
- **[Conceitos](./CONCEPTS/README.md)** - Autenticação, armazenamento de tokens, integração com API
- **[Guias Práticos](./HOW-TO/README.md)** - Setup Keycloak, login flow, API requests, instalação do plugin
- **[Camadas](./LAYERS/README.md)** - Estrutura de código do plugin (AuthManager, API Client, UI)

## Stack Tecnológico

- **Framework:** QGIS 3.28+ LTR + PyQGIS API
- **Linguagem:** Python 3.9+
- **GIS Libraries:** GDAL/OGR, Shapely, PyProj
- **API Client:** requests + JWT authentication
- **Database:** PostgreSQL + PostGIS via WFS/WMS conforme [ADR-002](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md)

## Código Fonte

Ver [carf-geogis README](../SRC-CODE/carf-geogis/README.md) para instruções de instalação do plugin e desenvolvimento local.

---

**Última atualização:** 2025-01-10
