---
type: leaf
status: review
updated: 2026-02-08
---

# GeoPolygon

Value object imutavel representando poligono geografico em coordenadas WGS84 (SRID 4326) armazenado como geometry(Polygon, 4326) via PostGIS. Utilizado para definir perimetros de Units, Communities e Blocks, permitindo queries espaciais como ST_Contains, ST_Intersects e ST_Area.

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| Minimo de vertices | Ao menos 4 pontos (3 vertices mais fechamento). |
| Poligono fechado | Primeiro e ultimo ponto devem ser identicos. |
| Geometria valida | ST_IsValid deve retornar true. Sem auto-interseccao. |
| SRID correto | Deve ser 4326 (WGS84). |
| Orientacao | Anel externo em sentido anti-horario conforme convencao OGC. |

## Operacoes Espaciais

| Operacao | Descricao |
|----------|-----------|
| ST_Area | Calcula area em metros quadrados (geography cast). |
| ST_Centroid | Calcula centroide para posicionamento de marcadores no mapa. |
| ST_Contains | Verifica se poligono contem outro (Block dentro de Community). |
| ST_Intersects | Detecta sobreposicao entre Units para validacao espacial. |
| ST_Buffer | Cria buffer ao redor do poligono para queries de proximidade. |

Indice GiST na coluna boundary acelera todas as queries espaciais.
