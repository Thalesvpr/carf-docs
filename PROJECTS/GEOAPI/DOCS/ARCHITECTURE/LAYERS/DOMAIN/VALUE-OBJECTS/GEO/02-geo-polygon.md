# GeoPolygon

Value object imutável herdando de BaseValueObject representando polígono geográfico com validação de formato WKT (Well-Known Text) ou GeoJSON, garantindo que apenas geometrias válidas e fechadas sejam armazenadas para perímetros de unidades, lotes, quadras e comunidades. Validações incluem verificação de polígono válido (não self-intersecting), anel externo fechado (primeiro ponto igual ao último), mínimo de 3 vértices únicos formando área, e coordenadas dentro de ranges válidos (latitude -90 a 90, longitude -180 a 180).

Métodos principais incluem construtor FromWkt(string) parseando formato "POLYGON((lon lat, lon lat, ...))" e FromGeoJson(string) parseando formato GeoJSON RFC 7946, ToWkt() e ToGeoJson() para serialização nos formatos respectivos, Area() calculando área em metros quadrados usando projeção adequada, Centroid() retornando GeoPoint do centro geométrico, e Contains(GeoPoint) verificando se ponto está dentro do polígono.

Usado em Unit.Geometry para perímetro da construção, Plot.Geometry para lote cadastral, Block.Geometry para quadra urbana, e Community.Geometry para delimitação total da comunidade, integrando com PostGIS no banco de dados para queries espaciais e com bibliotecas de mapas no frontend (Leaflet, MapLibre) e mobile (react-native-maps).

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
