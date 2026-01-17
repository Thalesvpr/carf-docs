# LayerFeature

Entidade representando geometria individual vetorial dentro Layer como ponto específico risco linha tubulação ou polígono área preservação com atributos descritivos permitindo armazenamento dados geográficos customizados tenant. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem LayerId Guid FK camada pertence, Geometry string WKT ou GeoJSON (Point LineString Polygon conforme GeometryType Layer), Properties JSON atributos descritivos customizados (risco alto, populacao_afetada 150, diametro_mm 100) e Label string nullable rótulo mapa.

Métodos incluem ValidateGeometry() verificando Geometry corresponde GeometryType Layer pai lançando ValidationException se incompatível, GetBoundingBox() calculando envelope retangular mínimo otimização queries, Intersects(geometry) verificando interseção análises espaciais, UpdateProperties(json) atualizando atributos e GetProperty(key) extraindo valor específico JSON.

Integra Layer através FK herdando StyleConfig renderização, suporta indexação espacial PostGIS índices GiST queries rápidas proximidade interseção contenção, participa análises identificando Unit dentro Features Áreas Risco usando ST_Within ou Units próximas Pontos Coleta usando ST_DWithin, permite queries atributos operadores JSONB PostgreSQL e integra importação Shapefile GeoJSON preservando geometria atributos.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
