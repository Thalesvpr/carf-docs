# PostGIS Setup

Configuração da extensão PostGIS para suporte geoespacial.

## Instalação

```sql
-- Script: 01-enable-postgis.sql

-- Extensão principal
CREATE EXTENSION IF NOT EXISTS postgis;

-- Topologia (opcional, para análises avançadas)
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Raster (opcional, para imagens georreferenciadas)
-- CREATE EXTENSION IF NOT EXISTS postgis_raster;

-- Verificar versão
SELECT PostGIS_Version();
-- Deve retornar: 3.4...
```

## Tipos de Dados Geoespaciais

### Geometry vs Geography

| Tipo | Uso | SRID |
|------|-----|------|
| geometry | Coordenadas projetadas (metros) | 31983 (SIRGAS 2000 UTM 23S) |
| geography | Coordenadas geográficas (lat/lon) | 4326 (WGS84) |

### Schema das Tabelas

```sql
-- Units com geometria
CREATE TABLE units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- ... outros campos ...
    boundary geometry(Polygon, 4326),
    centroid geometry(Point, 4326),
    area_m2 DECIMAL(12,2) GENERATED ALWAYS AS (
        ST_Area(boundary::geography)
    ) STORED
);

-- Communities com geometria
CREATE TABLE communities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- ... outros campos ...
    boundary geometry(Polygon, 4326),
    centroid geometry(Point, 4326),
    area_m2 DECIMAL(12,2)
);
```

## Índices Espaciais

```sql
-- Índice GiST para queries espaciais
CREATE INDEX idx_units_boundary_gist ON units USING GIST(boundary);
CREATE INDEX idx_units_centroid_gist ON units USING GIST(centroid);
CREATE INDEX idx_communities_boundary_gist ON communities USING GIST(boundary);

-- Índice para bounding box (mais rápido para filtros de viewport)
CREATE INDEX idx_units_boundary_bbox ON units USING GIST(boundary gist_geometry_ops_nd);
```

## Queries Espaciais Comuns

### Busca por Bounding Box

```sql
-- Units dentro de um viewport do mapa
SELECT * FROM units
WHERE boundary && ST_MakeEnvelope(-46.64, -23.55, -46.63, -23.54, 4326);
```

### Busca por Proximidade

```sql
-- Units em raio de 1km de um ponto
SELECT *, ST_Distance(centroid::geography, ST_Point(-46.6388, -23.5489)::geography) as distance
FROM units
WHERE ST_DWithin(centroid::geography, ST_Point(-46.6388, -23.5489)::geography, 1000)
ORDER BY distance;
```

### Detectar Sobreposição

```sql
-- Verificar se novo polígono sobrepõe units existentes
SELECT id, code
FROM units
WHERE ST_Intersects(boundary, ST_GeomFromGeoJSON($1))
  AND id != $2;  -- Excluir a própria unit em caso de update
```

### Calcular Área

```sql
-- Área em metros quadrados
SELECT ST_Area(boundary::geography) as area_m2
FROM units
WHERE id = $1;
```

### Units dentro de Community

```sql
-- Unidades contidas em uma comunidade
SELECT u.*
FROM units u
JOIN communities c ON ST_Within(u.centroid, c.boundary)
WHERE c.id = $1;
```

## Validação de Geometria

```sql
-- Verificar se polígono é válido
SELECT ST_IsValid(boundary), ST_IsValidReason(boundary)
FROM units
WHERE id = $1;

-- Corrigir geometrias inválidas
UPDATE units
SET boundary = ST_MakeValid(boundary)
WHERE NOT ST_IsValid(boundary);
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
