# CONCEPTS - GEOGIS

Conceitos fundamentais do plugin GEOGIS Python para QGIS.

## Autenticação e Tokens

- **[01-authentication.md](./01-authentication.md)** - OAuth2 Python adaptations, authorization code flow, PKCE implementation
- **[02-token-storage.md](./02-token-storage.md)** - QSettings usando QGIS password manager encrypted (Keychain, KWallet, Windows Credential Manager)

## QGIS Plugin Architecture

Plugin é Python package com:
- **metadata.txt** descrevendo name, version, description, author, qgisMinimumVersion
- **__init__.py** exportando classFactory() function retornando plugin instance
- **Main plugin class** com initGui() e unload() lifecycle hooks
- **Instalação** em ~/.qgis3/python/plugins/ directory carregado dinamicamente pelo QGIS ao startup

## PyQGIS API

**iface (QgisInterface)** - Acesso completo QGIS functionality para manipular map canvas, layers, toolbars, menus

**Tipos de Layers:**
- QgsVectorLayer para vector data geometries+attributes
- QgsRasterLayer para raster data tiles+bands
- QgsProject para project state save/load
- QgsProcessingAlgorithm para custom tools Processing Toolbox

## WFS/WMS Protocols

**WFS (Web Feature Service):**
- Retorna vector data XML/GML ou GeoJSON com geometries+attributes queryable
- Client-side filtering via CQL_FILTER parameter

**WMS (Web Map Service):**
- Retorna raster tiles PNG/JPEG rendered server-side
- Não queryable apenas visualization

**Authentication WFS/WMS:**
- authcfg parameter com auth config ID storing credentials encrypted
- Custom headers: `uri += '&headers=Authorization: Bearer token'`

## Shapefile/GeoJSON Export

**Shapefile Export** via `QgsVectorFileWriter.writeAsVectorFormat()` com parameters:
- layer source, output_path, encoding 'UTF-8'
- dest_crs para CRS transformation
- driver_name 'ESRI Shapefile'
- layer_options para compression/spatial_index
- Preserving attributes schema automaticamente

**GeoJSON Export** usando driver_name 'GeoJSON' ou manual json.dumps()

## Processing Algorithms

Custom tools registered via `QgsProcessingProvider` com:
- `addAlgorithm(MyAlgorithm())` onde MyAlgorithm extends QgsProcessingAlgorithm
- Defining: name(), displayName(), group(), createInstance()
- initAlgorithm() adding parameters
- processAlgorithm() implementing logic
- Executado via `processing.run('plugin:algorithm_id', parameters)` ou GUI Processing Toolbox

## Error Handling

**User-facing notifications:**
- `iface.messageBar().pushMessage('Title', 'Message', level=Qgis.Critical, duration=5)`

**Logging:**
- `QgsMessageLog.logMessage('Debug info', 'GEOGIS', level=Qgis.Info)`

**Exception handling:**
- try/except catching exceptions gracefully
- QMessageBox.critical() com stack trace details

---

**Última atualização:** 2026-01-10
