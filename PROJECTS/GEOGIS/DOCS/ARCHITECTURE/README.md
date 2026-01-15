# ARCHITECTURE - GEOGIS

Arquitetura do plugin GEOGIS - QGIS Python 3 plugin seguindo estrutura modular.

## Estrutura Modular

**src/ directory contendo:**
- **auth/** module encapsulando OAuth2 logic via python-keycloak library
- **api/** module para HTTP requests ao GEOAPI usando requests library com session management persistent cookies
- **ui/** module para dialogs PyQt5 components (LoginDialog, SettingsDialog, LayerSelectorDialog)
- **layers/** module para WFS/WMS layer loading from GEOAPI endpoints
- **processing/** module para QGIS Processing algorithms custom tools (ValidateGeometry, CalculateArea, ExportShapefile)

## Integração Keycloak

- **[01-keycloak-integration.md](./01-keycloak-integration.md)** - Integração OAuth2/OIDC com Keycloak, AuthManager singleton, Client Credentials Flow e Authorization Code + PKCE Flow

**AuthManager class singleton** gerenciando tokens em QSettings encrypted via QGIS password manager, suporta dois fluxos OAuth2:
- **Client Credentials Flow** para operações service account automatizadas sem user interaction ideal para batch processing scripts rodando headless
- **Authorization Code + PKCE Flow** com browser OAuth para user context mantendo session user-specific permitindo audit logs por usuário

## Plugin Lifecycle

**Hooks:**
- `def initGui()` chamado quando QGIS carrega plugin adiciona toolbar actions e menu items
- `def unload()` chamado quando descarregado remove UI elements limpando resources

## API Integration

- `requests.Session()` com retry strategy Retry(total=3, backoff_factor=1) para robustez contra network failures temporários
- Interceptor adiciona Authorization header automaticamente em todas requests chamando `AuthManager.getAccessToken()` que refresh se necessário

## Layer Loading

- **WFS protocol** para vector data geometries + attributes queryable
- **WMS protocol** para raster tiles backgrounds imagery
- **Custom symbology** QGIS styles aplicados automaticamente baseado em layer type (occupations red polygons, communities blue)

## Export Functionality

Permite salvar selected features como:
- **Shapefile** via `QgsVectorFileWriter.writeAsVectorFormat()`
- **GeoJSON** via `json.dumps(layer.getFeatures())` preservando attributes e CRS transformation para EPSG:4326 universal

## Processing Algorithms

Registrados via `QgsProcessingProvider` permitindo usuário executar via Processing Toolbox com parameters input/output configuráveis.

---

**Última atualização:** 2026-01-10

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (1 arquivo)

| ID | Titulo |
|:---|:-------|
| [01-keycloak-integration](./01-keycloak-integration.md) | 01-keycloak-integration |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (17) antes do rodapé - considerar converter para parágrafo denso.
