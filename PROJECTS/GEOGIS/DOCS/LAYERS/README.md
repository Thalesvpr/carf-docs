# LAYERS - GEOGIS

Estrutura de camadas do código do plugin GEOGIS QGIS.

## Camadas do Plugin

### Auth Manager

- **[01-auth-manager.md](./01-auth-manager.md)** - AuthManager singleton class gerenciando tokens OAuth2, QSettings encrypted, refresh token logic

**Responsabilidades:**
- OAuth2 authentication flow (Client Credentials e Authorization Code + PKCE)
- Token storage em QSettings encrypted via QGIS password manager
- Token refresh automático antes de expirar
- Logout e clear credentials

### API Client

**HTTP Client:**
- requests.Session() com retry strategy
- Interceptor adicionando Authorization header automaticamente
- Endpoints para communities, units, holders

### UI Components

**Dialogs PyQt5:**
- LoginDialog - interface de login OAuth2
- SettingsDialog - configuração GEOAPI URL e Keycloak
- LayerSelectorDialog - seleção de layers para carregar

### WFS/WMS Loader

**Layer Loading:**
- WFS protocol para vector data
- WMS protocol para raster tiles
- Custom symbology QGIS styles

### Processing Algorithms

**Custom Tools:**
- ValidateGeometry - validação topológica
- CalculateArea - cálculo preciso de áreas
- ExportShapefile - export para formatos GIS

---

**Última atualização:** 2026-01-10
