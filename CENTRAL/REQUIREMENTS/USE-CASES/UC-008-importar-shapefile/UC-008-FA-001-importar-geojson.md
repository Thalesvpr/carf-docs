---
id: UC-008-FA-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-008-FA-001: Importar GeoJSON

Fluxo alternativo do UC-008 para importacao via arquivo GeoJSON.

## Condicao

No passo 4 do UC-008, usuario faz upload de arquivo .geojson ao inves de ZIP com Shapefile.

## Fluxo

1. Usuario faz upload de arquivo .geojson
2. Sistema detecta tipo de arquivo pela extensao
3. Sistema valida estrutura JSON
4. Sistema verifica schema GeoJSON (FeatureCollection, features)
5. Sistema valida cada feature (type, geometry, properties)
6. Sistema assume SRID padrao (GeoJSON usa WGS84)
7. Sistema exibe quantidade de registros encontrados
8. Fluxo continua para mapeamento de campos

## Vantagens do Formato

- Arquivo unico, sem necessidade de ZIP
- Encoding UTF-8 nativo
- Suporte a geometrias complexas
- Compatibilidade com APIs web modernas

## Retorno

Fluxo principal continua a partir do passo 7. Dados GeoJSON mapeados normalmente.
