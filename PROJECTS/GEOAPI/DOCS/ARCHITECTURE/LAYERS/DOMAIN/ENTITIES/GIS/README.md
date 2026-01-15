# GIS

Entities serviços GIS do GEOAPI gerenciando layers vetoriais e raster para visualização contexto espacial análise. Layer representa camada geográfica configurável com Name identificador, Type enum (VECTOR/RASTER/WMS/WFS), Source enum (DATABASE/FILE/EXTERNAL_SERVICE), IsVisible boolean toggle UI, ZIndex ordenação vertical camadas sobrepostas, Style JSON configurando simbolização cores espessuras ícones e Metadata JSON contendo attribution license bounds temporal para compliance direitos autorais descobrimento. LayerFeature junction entity armazenando geometrias vetoriais específicas Layer com FeatureId identificador externo, Geometry PostGIS tipo variável (Point/LineString/Polygon/MultiPolygon), Properties JSONB attributes alfanuméricos (nome rua, população bairro, classificação solo) e relacionamento Layer permitindo queries espaciais ST_Intersects descobrindo features próximas Unit selecionada. WmsServer registra servidores OGC WMS externos com BaseUrl endpoint capabilities, Version (1.1.1/1.3.0) e Capabilities XML cached reduzindo latency. WmsLayer referencia WmsServer especificando LayerName identifier, BoundingBox coords limitando requests e Format (image/png/jpeg) otimizando bandwidth visualização.

## Arquivos

- **[21-layer.md](./21-layer.md)** - Camada GIS vetorial raster configurável
- **[22-layer-feature.md](./22-layer-feature.md)** - Feature geometria individual dentro layer
- **[23-wms-server.md](./23-wms-server.md)** - Servidor OGC WMS externo registrado
- **[24-wms-layer.md](./24-wms-layer.md)** - Layer WMS específica servidor

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (4 arquivos)

| ID | Titulo |
|:---|:-------|
| [21-layer](./21-layer.md) | Layer |
| [22-layer-feature](./22-layer-feature.md) | LayerFeature |
| [23-wms-server](./23-wms-server.md) | WmsServer |
| [24-wms-layer](./24-wms-layer.md) | WmsLayer |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
