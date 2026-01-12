# UNITS

Entity central do GEOAPI representando unidade habitacional ou propriedade, servindo como aggregate root coordenando relacionamentos com titulares documentos localização espacial e workflow regularização fundiária. Unit herda BaseAggregateRoot ganhando domain events para notificar criação UnitCreatedEvent, alteração UnitUpdatedEvent, mudança status UnitStatusChangedEvent e vínculo/desvínculo titulares HolderLinkedEvent/HolderUnlinkedEvent despachados após SaveChanges para workflows assíncronos. Campos principais incluem PlotId nullable FK para Plot opcional quando loteamento formal existe, BlockId nullable desnormalizado para queries eficientes, Address value object completo, Geometry GeoPolygon nullable perímetro espacial, Area metros quadrados calculada ST_Area PostGIS, Status value object workflow (DRAFT/PENDING_ANALYSIS/IN_REVIEW/APPROVED/REJECTED/REQUIRES_CHANGES) e CustomData JSONB nullable para dados específicos tenant validados externamente. Relacionamentos N:N com Holder via UnitHolder especificando tipo vínculo (proprietário/cônjuge/morador), coleção Documents (fotos/PDFs) e vínculo opcional Plot/Block suportando contextos urbanos formais e assentamentos informais sem organização espacial prévia permitindo flexibilidade operacional campo.

## Arquivos

- **[02-unit.md](./02-unit.md)** - Unidade habitacional aggregate root central sistema

---

**Última atualização:** 2026-01-12
