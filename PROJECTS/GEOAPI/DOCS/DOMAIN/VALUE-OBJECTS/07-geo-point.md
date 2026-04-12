---
type: leaf
status: review
updated: 2026-02-08
---

# GeoPoint

Value object imutavel representando ponto geografico em coordenadas WGS84 (SRID 4326) armazenado como geometry(Point, 4326) via PostGIS. Utilizado para centroides de Units, localizacao de SurveyPoints e posicoes de GPS coletadas em campo pelo app REURBCAD.

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| Latitude | Valor entre -90 e 90 graus decimais. |
| Longitude | Valor entre -180 e 180 graus decimais. |
| SRID | Deve ser 4326 (WGS84). |
| Precisao | Minimo 6 casas decimais para precisao de aproximadamente 0.1 metro. |

## Uso no Dominio

Centroide de Unit e calculado automaticamente via ST_Centroid a partir do boundary (GeoPolygon). Tambem armazena posicoes de GPS coletadas durante cadastro em campo. Indice GiST na coluna centroid permite queries de proximidade (ST_DWithin) e busca por raio.
