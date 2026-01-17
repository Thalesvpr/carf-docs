# COMMUNITIES

Entities organização espacial territorial do GEOAPI estruturando assentamentos em hierarquia Community Block Plot. Community representa núcleo habitacional urbano informal com Name identificador, Type enum (URBANA/RURAL/QUILOMBOLA) determinando regras específicas aplicáveis, Geometry GeoPolygon delimitando perímetro, TotalArea calculada ST_Area PostGIS, TotalUnits contador desnormalizado para dashboards e Status workflow agregado (PLANNING/IN_PROGRESS/COMPLETED), agregando collections Blocks e Units permitindo queries hierárquicas. Block quadra urbana dentro Community opcional para contextos planejados com Code alfanumérico único por community, Geometry perímetro e relacionamento Plots e Units facilitando endereçamento Quadra A Lote 5. Plot lote individual menor unidade espacial com Code único por block, Geometry polígono, Area calculada e LandUse enum (RESIDENTIAL/COMMERCIAL/MIXED) informando zoneamento, permitindo Units referenciar Plot quando loteamento formal existe ou null quando assentamento irregular sem demarcação.

## Arquivos

- **[04-community.md](./04-community.md)** - Núcleo habitacional agregando blocks units
- **[08-block.md](./08-block.md)** - Quadra urbana opcional dentro community
- **[09-plot.md](./09-plot.md)** - Lote individual menor unidade espacial

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [04-community](./04-community.md) | Community |
| [08-block](./08-block.md) | Block |
| [09-plot](./09-plot.md) | Plot |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
