---
type: leaf
status: review
updated: 2026-02-08
---

# GeoPoint

Value object imutavel herdando de BaseValueObject que representa um ponto geografico com latitude e longitude em graus decimais. Usado para localizacao precisa de centroides de geometrias, geotags de fotos e marcos geodesicos. No banco de dados, corresponde a colunas do tipo geometry(Point, 4326) em PostGIS, como units.centroid.

O construtor recebe latitude e longitude como decimais e valida os limites. Coordenadas fora dos limites terrestres geram ValidationException.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Latitude valida | Entre -90 e 90 graus (sul a norte). |
| Longitude valida | Entre -180 e 180 graus (oeste a leste). |
| Precisao de comparacao | Igualdade usa tolerancia epsilon para imprecisao de ponto flutuante. |
| SRID 4326 | Sistema de referencia WGS84. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| Latitude | decimal | Propriedade read-only da latitude. |
| Longitude | decimal | Propriedade read-only da longitude. |
| ToWkt() | string | Formato POINT(longitude latitude) para PostGIS. |
| ToGeoJson() | string | Objeto GeoJSON RFC 7946. |
| DistanceTo(GeoPoint) | decimal | Distancia em metros usando formula de Haversine. |

Usado em units.centroid como centroide calculado a partir do boundary, em SurveyPoint para coordenadas coletadas e processadas, em Document para geotag de fotos capturadas pelo app mobile REURBCAD, e retornado por GeoPolygon.Centroid().
