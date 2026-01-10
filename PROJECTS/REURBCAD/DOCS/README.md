# REURBCAD - Aplicativo Mobile para Coleta em Campo

Aplicativo mobile React Native + Expo para coleta offline de dados cadastrais de unidades habitacionais em campo por técnicos e fiscais municipais, permitindo captura de coordenadas GPS, fotos georreferenciadas, cadastro de titulares, desenho de polígonos no mapa offline, e sincronização bidirecional com backend [GEOAPI](../../GEOAPI/DOCS/ARCHITECTURE/01-overview.md) quando conectado, implementando offline-first architecture via [WatermelonDB](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-006-offline-first-watermelondb.md) conforme [ADR-004: React Native](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-004-react-native-mobile.md), autenticação via [Keycloak](../../KEYCLOAK/DOCS/README.md) com PKCE flow, validações client-side reutilizando [@carf/tscore](../../LIB/TS/TSCORE/DOCS/CONCEPTS/01-value-objects.md), API client [@carf/geoapi-client](../../LIB/TS/GEOAPI-CLIENT/DOCS/README.md), sincronização inteligente detectando conflitos com estratégia last-write-wins conforme [UC-005](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-005-sincronizar-dados-offline.md), e deployment via [EAS Build](../../../CENTRAL/ARCHITECTURE/DEPLOYMENT/05-mobile-deployment.md) distribuindo APK/IPA.

## Funcionalidades Principais

**Coleta Offline** - Trabalho completo offline coletando unidades, fotos, titulares em áreas sem conectividade conforme [UC-004](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-004-coletar-dados-campo-mobile.md), dados persistidos em SQLite via WatermelonDB, sincronização automática quando WiFi disponível economizando dados móveis.

**Captura de Coordenadas GPS** - Localização precisa com GPS device nativo marcando posição de unidades, desenho de polígonos caminhando perímetro, cálculo automático de área m², e validação de bounds dentro do município.

**Fotos Georreferenciadas** - Camera nativa capturando fotos com EXIF metadata incluindo GPS coordinates timestamp, compress automático reduzindo tamanho para economizar storage/bandwidth, e upload em background quando sincronizando.

**Sincronização Inteligente** - Batch sync de 500 registros por request, conflict detection via timestamps, merge manual para conflitos em campos críticos, retry automático em falhas, e progress indicator mostrando status.

**Mapas Offline** - Tiles de mapas baixados previamente para área do município, visualização de unidades já coletadas, sobreposição de layers, e medição de distâncias/áreas.

## Stack Tecnológico

- **Framework:** React Native 0.76 + Expo SDK 52 conforme [ADR-004](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-004-react-native-mobile.md)
- **Database:** WatermelonDB + SQLite conforme [ADR-006](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-006-offline-first-watermelondb.md)
- **Maps:** react-native-maps + MapLibre
- **Camera:** expo-camera
- **Location:** expo-location
- **Navigation:** React Navigation 6
- **API Client:** [@carf/geoapi-client](../../LIB/TS/GEOAPI-CLIENT/DOCS/README.md)
- **Deployment:** EAS Build + EAS Update conforme [DEPLOYMENT/05-mobile](../../../CENTRAL/ARCHITECTURE/DEPLOYMENT/05-mobile-deployment.md)

---

**Última atualização:** 2025-01-10
