# REURBCAD - Features

Aplicativo mobile React Native Expo implementando coleta de dados offline-first para field collectors trabalharem áreas sem internet capturando informações unidades habitacionais ocupações titulares fotografias geolocalizações através de interface touch-optimized com navegação bottom tabs stack navigator formulários multi-step validações client-side persistência local WatermelonDB sincronização background queue-based quando conexão disponível garantindo zero data loss mesmo semanas offline via arquitetura offline-first local-first patterns onde device é source of truth primária sync bidirecional merge conflicts resolution last-write-wins strategy.

## Features Implementadas

- **[field-collection.md](./01-field-collection.md)** - Coleta campo wizard multi-step formulário cadastro unidades BasicInfo Address Area Geolocation PhotoCapture validações Zod React Hook Form persistência offline WatermelonDB queue sync
- **[holder-management.md](./02-holder-management.md)** - CRUD titulares mobile formulário validação CPF RG vinculação unidades many-to-many upload documentos Expo Camera Image Picker persistência offline sync
- **[offline-sync.md](./03-offline-sync.md)** - Sincronização bidirecional queue-based pull push changes conflict resolution retry logic WatermelonDB sync adapter GEOAPI endpoints background Expo Background Fetch
- **[shapefile-import.md](./04-shapefile-import.md)** - Importação shapefiles mobile Expo Document Picker validation topology CRS attribute mapping preview map turf.js offline queue upload multipart async processing
- **[team-management.md](./05-team-management.md)** - Visualização readonly teams membros líder comunidades assignment filtering units por team coordenação campo sync unidirecional server down mobile

Funcionalidades principais incluem Field Collection permitindo cadastrar unidades via formulário wizard com steps informações básicas endereço área geolocalização via GPS nativo Expo Location fotografias via Expo Camera ou Image Picker validações CPF endereço área mínima persistindo localmente WatermelonDB collections units holders occupations com status pending_sync até conexão disponível, Offline Sync gerenciando queue de changes create update delete operações acumuladas offline sincronizando automaticamente via background task Expo Background Fetch detectando network via NetInfo chamando GEOAPI endpoints POST PUT DELETE batch processando responses sucesso falha retry logic exponential backoff conflict resolution comparando timestamps server vs local decidindo winner merge strategy, Holder Management CRUD completo titulares mobile formulários nome CPF RG documentação upload photos vincular múltiplas unidades relacionamento one-to-many persistindo localmente offline disponível visualização detalhes edição remoção soft delete, Team Management visualização readonly equipes atribuídas ao field collector listando membros líder comunidades responsáveis sincronizando assignments do servidor permitindo filtrar unidades por team assignment facilitando organização trabalho campo, Shapefile Import permitindo carregar shapefiles via file picker Expo Document Picker processando geometries via turf.js ou similar validando polygons CRS convertendo para format compatível GEOAPI upload multipart quando online ou queueing para sync posterior.

Stack tecnológica React Native 0.74 Expo SDK 51 TypeScript strict mode Zustand state management TanStack Query server state com persistence adapter WatermelonDB SQLite offline storage Expo Router file-based navigation React Hook Form Zod validations Expo Location GPS Expo Camera Image Picker media capture NetInfo connectivity detection Expo Background Fetch sync tasks React Native Maps geolocation visualization axios HTTP client com interceptors retry logic Sentry error tracking CodePush OTA updates garantindo field collectors sempre versão latest sem necessidade manual update stores.

Arquitetura offline-first implementa local database WatermelonDB como source of truth primária com collections models schema migrations sync adapter conectando backend GEOAPI pull changes desde last sync timestamp push pending local changes conflict resolution estratégia, state management híbrido Zustand para UI state ephemeral (selected tab modal open filter values) TanStack Query para server state cached com staleTime infinito offline invalidation manual após sync success, navigation Expo Router app directory structure file-based routes com layouts tabs groups dynamic segments type-safe params, forms React Hook Form useForm hook com resolver Zod schema validations mode onChange reValidateMode onChange errors inline feedback submit handling optimistic UI updates, media handling Expo Image Picker selecionando photos gallery ou Camera capturing new compressing via expo-image-manipulator reduzindo size antes upload saving locally file system Expo FileSystem caching URIs persistindo references WatermelonDB, geolocation Expo Location requestForegroundPermissionsAsync obtaining coords getCurrentPositionAsync accuracy high timeout 10s caching last known location fallback watchPositionAsync streaming updates durante coleta mostrando marker React Native Maps.

Relacionamento requirements implementando UC-004 coleta campo mobile UC-001 cadastro unidades UC-005 sync offline UC-003 vinculação titulares UC-011 gestão equipes UC-008 importação shapefiles garantindo field collectors produtivos offline dados sincronizados automaticamente online accountability rastreamento via GPS timestamps photos evidências compliance LGPD multi-tenancy RLS backend isolando dados municipais diferentes.

---

**Última atualização:** 2026-01-11

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (5 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-field-collection](./01-field-collection.md) | Field Collection - Coleta em Campo |
| [02-holder-management](./02-holder-management.md) | Holder Management - Gestão de Titulares |
| [03-offline-sync](./03-offline-sync.md) | Offline Sync - Sincronização |
| [04-shapefile-import](./04-shapefile-import.md) | Shapefile Import - Importação |
| [05-team-management](./05-team-management.md) | Team Management - Gestão de Equipes |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
