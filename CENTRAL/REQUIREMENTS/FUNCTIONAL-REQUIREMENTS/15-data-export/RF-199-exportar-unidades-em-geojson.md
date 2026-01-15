---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# RF-199: Exportar Unidades em GeoJSON

O sistema disponibiliza exportação de unidades em formato GeoJSON, padrão moderno baseado em JSON amplamente utilizado em aplicações web e APIs que oferece estrutura simples e legível tanto para humanos quanto máquinas, facilitando integração com sistemas externos e desenvolvimento de aplicações customizadas. A geração produz GeoJSON válido conforme especificação RFC 7946 incluindo FeatureCollection contendo array de Features onde cada unidade é representada com geometry codificando forma espacial em coordenadas GeoJSON e properties contendo todos os atributos alfanuméricos da unidade como identificação, tipo, área, status e dados cadastrais. O sistema garante inclusão de propriedades essenciais que identificam univocamente cada unidade e fornecem contexto necessário para interpretação dos dados, incluindo metadados como sistema de coordenadas utilizado, data de exportação e filtros aplicados, quando relevantes, documentados em propriedades customizadas do FeatureCollection. O arquivo .geojson resultante é disponibilizado para download direto através do navegador, podendo ser imediatamente carregado em bibliotecas JavaScript como Leaflet ou OpenLayers, importado em ferramentas de análise como Python Geopandas, ou consumido por APIs REST que aceitam dados geográficos em formato JSON, demonstrando versatilidade do formato para múltiplos casos de uso técnico.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
