# REURBCAD - Overview de Implementação

Aplicativo móvel React Native + Expo para coleta offline de dados cadastrais de unidades habitacionais em campo, com GPS, câmera, validações client-side e sincronização bidirecional com backend GEOAPI.

## Requirements Implementados

### Use Cases Principais

- [UC-001: Cadastrar Unidade](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-001-cadastrar-unidade-habitacional.md) - Cadastro offline em campo
- [UC-002: Aprovar Unidade](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-002-aprovar-unidade-habitacional.md) - Visualização de status
- [UC-003: Vincular Titular](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-003-vincular-titular-unidade.md) - Cadastro de holders offline
- [UC-004: Coletar Dados em Campo](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-004-coletar-dados-campo-mobile.md) - **CORE** - Coleta GPS + fotos
- [UC-005: Sincronizar Dados Offline](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-005-sincronizar-dados-offline.md) - **CORE** - Sync bidirecional
- [UC-007: Exportar Dados](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md) - Exportação GeoJSON local
- [UC-008: Importar Shapefile](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-008-importar-shapefile.md) - Import de geometrias
- [UC-010: Configurar WMS](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-010-configurar-camadas-wms.md) - Ortofotos offline
- [UC-011: Gerenciar Equipes](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-011-gerenciar-equipes-tecnicas.md) - Visualização de team

## Domain Model Implementado

### Entities (offline-first)

Todas entities implementadas com WatermelonDB (SQLite local) para persistência offline:

- [Unit](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/02-unit.md) - Local database model
- [Holder](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/03-holder.md) - Offline cadastro
- [Document](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/14-document.md) - Fotos armazenadas localmente
- [SyncLog](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/17-sync-log.md) - Controle de sincronização

### Value Objects

Implementados via [@carf/tscore](../../../PROJECTS/LIB/TS/TSCORE/DOCS/README.md):

- CPF, Email, PhoneNumber, Address, GeoPolygon, UnitStatus

## Arquitetura Técnica

**Stack:**
- React Native 0.73 + Expo SDK 50
- TypeScript 5
- WatermelonDB (offline database SQLite)
- React Native Maps (mapas nativos)
- Expo Camera (captura de fotos)
- Expo Location (GPS tracking)
- @carf/tscore (autenticação, value objects)
- @carf/geoapi-client (sync HTTP)

**Deploy:** EAS Build (APK Android + IPA iOS)

Ver [ARCHITECTURE/](./ARCHITECTURE/README.md) e [CONCEPTS/](./CONCEPTS/README.md) para conceitos de autenticação offline e armazenamento seguro.

## Features Documentadas

Ver [FEATURES/](./FEATURES/README.md):

- [Field Collection](./FEATURES/field-collection.md) - Coleta GPS + fotos
- [Offline Sync](./FEATURES/offline-sync.md) - Sincronização bidirecional
- [Holder Management](./FEATURES/holder-management.md) - Cadastro titulares offline
- [Shapefile Import](./FEATURES/shapefile-import.md) - Importação de dados geográficos
- [Team Management](./FEATURES/team-management.md) - Gestão de equipes em campo

---

**Última atualização:** 2026-01-10
