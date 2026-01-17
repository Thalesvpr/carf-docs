# GeoPoint

Value object imutável herdando de BaseValueObject representando ponto geográfico com latitude e longitude em graus decimais, usado para localização precisa de marcos geodésicos, estações RBMC, centroides de geometrias e geotags de fotos. Validações incluem verificação de latitude entre -90 e 90 graus (sul a norte) e longitude entre -180 e 180 graus (oeste a leste), rejeitando coordenadas inválidas ou fora dos limites terrestres.

Métodos principais incluem construtor recebendo latitude e longitude como decimais, propriedades Latitude e Longitude read-only, ToWkt() retornando formato "POINT(longitude latitude)" para persistência PostGIS, ToGeoJson() retornando objeto GeoJSON RFC 7946, DistanceTo(GeoPoint other) calculando distância em metros usando fórmula de Haversine para grande círculo, e operadores de igualdade comparando coordenadas com tolerância de epsilon para imprecisão de ponto flutuante.

Usado em RbmcStation.Location para coordenadas de estações da Rede Brasileira de Monitoramento Contínuo IBGE, SurveyPoint.Location e SurveyPoint.ProcessedLocation para pontos coletados em campo e processados com correção diferencial, Document.Latitude/Longitude para geotag de fotos capturadas pelo app mobile, e GeoPolygon.Centroid() retornando centro geométrico de polígonos.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
