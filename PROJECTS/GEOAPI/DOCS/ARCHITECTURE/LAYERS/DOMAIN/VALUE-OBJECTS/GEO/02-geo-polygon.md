---
type: leaf
status: review
updated: 2026-02-08
---

# GeoPolygon

Value object imutavel herdando de BaseValueObject que representa um poligono geografico com validacao de formato WKT (Well-Known Text) ou GeoJSON. Garante que apenas geometrias validas e fechadas sejam armazenadas para perimetros de unidades, lotes, quadras e comunidades. No banco de dados, corresponde a colunas do tipo geometry(Polygon, 4326) em PostGIS, utilizando o sistema de referencia WGS84.

O objeto pode ser criado a partir de WKT via FromWkt() ou de GeoJSON via FromGeoJson(). Ambos os construtores validam a geometria antes de aceita-la. Integracao direta com PostGIS permite queries espaciais como ST_Contains e ST_Intersects.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Poligono valido | Nao pode ter auto-intersecao (self-intersecting). |
| Anel fechado | Primeiro ponto deve ser igual ao ultimo. |
| Minimo 3 vertices | Pelo menos 3 vertices unicos formando area. |
| Latitude valida | Entre -90 e 90 graus. |
| Longitude valida | Entre -180 e 180 graus. |
| SRID 4326 | Sistema de referencia WGS84 obrigatorio. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| FromWkt(string) | GeoPolygon | Cria instancia a partir de WKT. |
| FromGeoJson(string) | GeoPolygon | Cria instancia a partir de GeoJSON. |
| ToWkt() | string | Serializa para formato WKT. |
| ToGeoJson() | string | Serializa para formato GeoJSON RFC 7946. |
| Area() | decimal | Calcula area em metros quadrados via projecao adequada. |
| Centroid() | GeoPoint | Retorna centro geometrico do poligono. |
| Contains(GeoPoint) | bool | Verifica se ponto esta dentro do poligono. |

Usado em Unit.boundary para perimetro da construcao, Community.boundary para delimitacao da comunidade, Block.boundary para quadra urbana, e Plot.boundary para lote cadastral. Indice GiST no banco garante performance em queries espaciais.
