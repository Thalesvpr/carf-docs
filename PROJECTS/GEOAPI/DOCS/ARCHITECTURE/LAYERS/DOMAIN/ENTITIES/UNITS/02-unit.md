# Unit

Entidade central do sistema representando unidade habitacional ou propriedade servindo como aggregate root coordenando relacionamentos com titulares documentos localização espacial e workflow regularização fundiária. Herda de BaseAggregateRoot ganhando suporte domain events notificando criação UnitCreatedEvent alteração UnitUpdatedEvent mudança status UnitStatusChangedEvent e vínculo/desvínculo titulares HolderLinkedEvent HolderUnlinkedEvent despachados após SaveChanges para workflows assíncronos integração outros bounded contexts.

Campos principais incluem PlotId Guid nullable FK para Plot opcional, BlockId Guid nullable FK para Block desnormalizado queries eficientes, Address value object completo, GeoPolygon nullable perímetro espacial, Area metros quadrados calculada ST_Area PostGIS, UnitStatus workflow (DRAFT/PENDING_ANALYSIS/IN_REVIEW/APPROVED/REJECTED/REQUIRES_CHANGES) e CustomData JSONB nullable dados específicos tenant validados não é sistema formulários dinâmicos mas escape hatch casos raros.

Relacionamentos N:N com Holder via UnitHolder especificando tipo vínculo (proprietário cônjuge morador), coleção Documents fotos PDFs e vínculo opcional Plot/Block suportando contextos urbanos formais e assentamentos informais sem organização espacial prévia permitindo flexibilidade operacional campo.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
