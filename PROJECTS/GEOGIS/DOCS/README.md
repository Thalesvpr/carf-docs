# GEOGIS - Plugin QGIS para Operações GIS Avançadas

Plugin QGIS Python para operações GIS avançadas complementando portal web GEOWEB com análises espaciais complexas, permitindo técnicos GIS especializados executarem geoprocessamento de dados CARF diretamente em QGIS desktop, integrando com backend [GEOAPI](../../GEOAPI/DOCS/ARCHITECTURE/01-overview.md) via REST API consumindo endpoints WFS (Web Feature Service) e WMS (Web Map Service) expostos por PostGIS conforme [ADR-002](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md), autenticação via token JWT obtido de [Keycloak](../../KEYCLOAK/DOCS/README.md), importação/exportação de Shapefiles GeoJSON KML sincronizando com [GEOAPI /api/communities](../../../CENTRAL/API/COMMUNITIES/README.md), análises de overlay buffer intersection difference gerando novos layers, validação de topologia detectando polígonos inválidos auto-overlaps gaps, e cálculos geométricos precisos (área perímetro centroid) conforme padrões OGC Simple Features.

## Estrutura da Documentação

- **[ARCHITECTURE/](ARCHITECTURE/)** - Decisões de arquitetura plugin
  - [01-overview.md](ARCHITECTURE/01-overview.md) - Visão geral arquitetura QGIS plugin
  - [03-data-flow.md](ARCHITECTURE/03-data-flow.md) - Fluxo dados QGIS ↔ GEOAPI
  - [04-integration.md](ARCHITECTURE/04-integration.md) - Integração WFS/WMS PostGIS
  - [05-deployment.md](ARCHITECTURE/05-deployment.md) - Distribuição plugin QGIS
- **[CONCEPTS/](CONCEPTS/)** - Conceitos GIS
  - [01-key-concepts.md](CONCEPTS/01-key-concepts.md) - Geoprocessamento, topologia, análises
- **[HOW-TO/](HOW-TO/)** - Guias práticos
  - [01-setup-dev-environment.md](HOW-TO/01-setup-dev-environment.md) - Setup QGIS development
  - [02-install-plugin.md](HOW-TO/02-install-plugin.md) - Instalação plugin
  - [03-use-plugin.md](HOW-TO/03-use-plugin.md) - Uso das ferramentas

## Funcionalidades Principais

**Conexão GEOAPI** - Autenticação via JWT, listagem de comunidades/unidades disponíveis, download de layers como vector layers QGIS temporários, e upload de edições de volta para GEOAPI.

**Análises Espaciais** - Buffer de unidades para análise de vizinhança, intersection de comunidades com limites administrativos, union de polígonos adjacentes criando áreas consolidadas, e difference para identificar gaps.

**Validação de Topologia** - Detecção automática de geometrias inválidas (self-intersection overlaps gaps slivers), correção via MakeValid, e relatório de problemas encontrados.

**Exportação de Mapas** - Layout templates para impressão de mapas cadastrais incluindo legenda escala norte, export para PDF/PNG alta resolução, e batch print de múltiplas comunidades.

**Sincronização Bidirecional** - Download incremental apenas de dados modificados desde última sync, upload de edições com conflict detection, e merge changes com estratégia configurable.

## Stack Tecnológico

- **Framework:** QGIS 3.28+ LTR + PyQGIS API
- **Linguagem:** Python 3.9+
- **GIS Libraries:** GDAL/OGR, Shapely, PyProj
- **API Client:** requests + JWT authentication
- **Database:** PostgreSQL + PostGIS via WFS/WMS conforme [ADR-002](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md)

---

**Última atualização:** 2025-01-10
