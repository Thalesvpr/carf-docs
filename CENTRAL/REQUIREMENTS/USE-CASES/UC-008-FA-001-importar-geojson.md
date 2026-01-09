---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: scalability
---

# UC-008-FA-001: Importar GeoJSON

Fluxo alternativo do UC-008 Importar Shapefile desviando no passo 5.1 Upload onde ao invés de fazer upload de arquivo ZIP contendo componentes Shapefile (.shp .shx .dbf .prj), usuário faz upload de arquivo único .geojson ou .json contendo FeatureCollection conforme especificação RFC 7946 com features array incluindo geometrias e properties, sistema detecta tipo de arquivo verificando extensão e Content-Type application/geo+json ou application/json, valida estrutura JSON completa usando parser JSON.parse verificando sintaxe válida sem erros de parsing rejeitando arquivos corrompidos ou malformados, valida schema GeoJSON verificando presença de campos obrigatórios type="FeatureCollection" no root e features array não vazio, itera features validando cada item possui type="Feature" geometry object com type válido (Point LineString Polygon MultiPolygon) e coordinates array, e properties object contendo atributos, detecta automaticamente SRID lendo campo opcional crs.properties.name do GeoJSON padrão RFC 7946 assume EPSG:4326 se ausente pois GeoJSON por especificação sempre usa WGS84 lon/lat, conta total de features calculando features.length exibindo "Arquivo válido. 250 registros encontrados" com mensagem adicional "Formato: GeoJSON (EPSG:4326)" confirmando tipo detectado, avança automaticamente para Passo 2 Mapeamento de Campos detectando properties do primeiro feature usando Object.keys(features[0].properties) extraindo lista de campos disponíveis (ex: codigo endereco tipo area_m2 status), exibe tabela de mapeamento idêntica ao fluxo Shapefile permitindo usuário mapear properties GeoJSON para campos sistema usando dropdowns, fluxo continua normalmente através Passo 3 Preview processamento worker e criação de unidades extraindo geometrias via geometry object que já está em formato JSON estruturado facilitando parsing ao invés de binário Shapefile, vantagens incluem arquivo único mais simples sem necessidade de ZIP, encoding UTF-8 nativo sem problemas de acentuação típicos de Shapefile DBF CP1252, suporte nativo a tipos complexos como MultiPolygon sem limitações de Shapefile que falha com polígonos com buracos, e compatibilidade direta com APIs REST e bibliotecas JavaScript modernas como Leaflet Mapbox permitindo exportar de sistemas web e importar sem conversão intermediária, ideal para integrações com plataformas online de mapeamento colaborativo (OpenStreetMap HOT Tasking Manager) ou APIs governamentais (IBGE INDE) que fornecem dados em GeoJSON padrão facilitando reuso de dados públicos em contexto de regularização fundiária onde cadastros podem ser enriquecidos com limites de setores censitários áreas de risco ou zoneamento urbano disponíveis em formato aberto.

**Ponto de Desvio:** Passo 5.1 do UC-008 (upload de arquivo diferente)

**Retorno:** Validação GeoJSON, continua para mapeamento e importação normalmente

---

**Última atualização:** 2025-12-30
