---
status: review
updated: 2026-01-12
---

# COMMUNITIES

Entities organização espacial territorial do GEOAPI estruturando assentamentos em hierarquia Community Block Plot. Community representa núcleo habitacional urbano informal com Name identificador, Type enum (URBANA/RURAL/QUILOMBOLA) determinando regras específicas aplicáveis, Geometry GeoPolygon delimitando perímetro, TotalArea calculada ST_Area PostGIS, TotalUnits contador desnormalizado para dashboards e Status workflow agregado (PLANNING/IN_PROGRESS/COMPLETED), agregando collections Blocks e Units permitindo queries hierárquicas. Block quadra urbana dentro Community opcional para contextos planejados com Code alfanumérico único por community, Geometry perímetro e relacionamento Plots e Units facilitando endereçamento Quadra A Lote 5. Plot lote individual menor unidade espacial com Code único por block, Geometry polígono, Area calculada e LandUse enum (RESIDENTIAL/COMMERCIAL/MIXED) informando zoneamento, permitindo Units referenciar Plot quando loteamento formal existe ou null quando assentamento irregular sem demarcação.

## Arquivos

- **[04-community.md](./04-community.md)** - Núcleo habitacional agregando blocks units
- **[08-block.md](./08-block.md)** - Quadra urbana opcional dentro community
- **[09-plot.md](./09-plot.md)** - Lote individual menor unidade espacial

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/ENTITIES/COMMUNITIES/04-community.md|Community]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/ENTITIES/COMMUNITIES/08-block.md|Block]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/ENTITIES/COMMUNITIES/09-plot.md|Plot]]

<!-- CARF-INDEX-END -->
