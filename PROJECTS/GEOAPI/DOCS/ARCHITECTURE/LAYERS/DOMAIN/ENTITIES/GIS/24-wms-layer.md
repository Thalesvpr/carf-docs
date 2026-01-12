# WmsLayer

Entidade representando camada individual disponível WmsServer configurando quais layers WMS externos são exibidos mapa com metadados estilo ordenação permitindo seleção granular camadas servidores externos. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem WmsServerId Guid FK servidor fornece camada, LayerName string nome técnico WMS usado requests GetMap (BCIM:Municipio), Title string título legível usuário (Municípios do Brasil) e Abstract string nullable descrição conteúdo fonte.

Campos georeferenciamento incluem BoundingBox JSON extent geográfico min/max lat/lng área cobertura, Styles JSON array estilos disponíveis (name title), IsVisible bool visibilidade padrão, DisplayOrder int z-index ordem exibição e MinZoom MaxZoom int nullable níveis zoom otimização requests. Métodos incluem ToggleVisibility() alternando, SetDisplayOrder(order) ajustando ordem, UpdateMetadata(title abstract bbox styles) atualizando durante SyncCapabilities, GetStyle(name) retornando específico ou padrão e BuildGetMapUrl(bbox width height srs) construindo URL completa GetMap.

Integra WmsServer através FK descoberto criado automaticamente SyncCapabilities() parseando XML GetCapabilities, participa renderização frontend GEOWEB tile layer URL GetMap bbox dinâmico viewport navegação, permite ativação/desativação individual camadas servidor múltiplas layers usuário escolhe exibir e valida zoom range exibindo apenas MinZoom MaxZoom otimizando performance.

---

**Última atualização:** 2026-01-12
