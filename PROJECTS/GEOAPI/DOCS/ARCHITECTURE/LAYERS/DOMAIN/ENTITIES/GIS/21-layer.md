# Layer

Entidade representando camada mapa interna Tenant contendo dados vetoriais geográficos customizados como perímetros risco áreas preservação infraestrutura ou informação espacial adicional domínio principal Unit e Community. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem TenantId Guid FK isolando camadas cliente, Name string (Áreas de Risco, Rede de Água), Description string nullable propósito e GeometryType string (POINT LINESTRING POLYGON) definindo tipo permitido features.

Campos visualização incluem StyleConfig JSON estilo visual cores espessuras ícones opacidade, IsVisible bool visibilidade padrão, DisplayOrder int z-index ordem exibição, MinZoom MaxZoom int nullable níveis zoom exibição e Metadata JSON nullable metadados fonte dados responsável. Métodos incluem ToggleVisibility() alternando, UpdateStyle(json) validando configuração, SetDisplayOrder(order) ajustando z-index e ValidateGeometryType() verificando valor válido.

Relacionamento principal LayerFeature através coleção Features onde Layer contém múltiplas geometrias mesmo GeometryType compartilhando estilo. Integra frontend GEOWEB renderizando Mapbox GL JS Leaflet, suporta importação Shapefile GeoJSON KML convertendo Features, permite exportação formatos GIS padrão e participa análises espaciais cruzando Features com Unit geometries identificando unidades áreas risco.

---

**Última atualização:** 2026-01-12
