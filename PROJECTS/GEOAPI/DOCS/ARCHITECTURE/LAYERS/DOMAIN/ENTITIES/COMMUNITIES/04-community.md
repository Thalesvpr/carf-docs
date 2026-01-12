# Community

Entidade aggregate root representando comunidade assentamento agrupando unidades habitacionais contexto geográfico social específico servindo como unidade organizacional principal processos regularização fundiária. Herda de BaseAggregateRoot suportando domain events rastreamento mudanças significativas CommunityCreatedEvent CommunityUpdatedEvent. Campos principais incluem Code string único por tenant, Name nome comunidade, CommunityType (URBANA RURAL QUILOMBOLA RIBEIRINHA) definindo legislação aplicável e GeoPolygon nullable delimitando perímetro.

Campos adicionais incluem Area decimal m², Municipality Estado localização, dados complementares distrito bairro logradouro referência e Status regularização. Relacionamentos incluem coleção Unit vinculadas, hierarquia espacial opcional Block subdividindo áreas menores e CommunityAuthorization controlando quais Team ou Account têm permissões leitura edição criação.

Serve contexto bounded operações campo permitindo equipes trabalharem isoladamente comunidades específicas com sincronização offline app mobile SyncLog. Suporta tanto contextos urbanos formais com Blocks/Plots quanto assentamentos informais sem organização espacial prévia.

---

**Última atualização:** 2026-01-12
