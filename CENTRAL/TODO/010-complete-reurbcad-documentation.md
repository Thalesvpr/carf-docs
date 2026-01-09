# 010 - Complete REURBCAD Documentation (Missing 13 Files)

🔴 **Prioridade:** Crítica
📅 **Criado em:** 2026-01-09
⏱️ **Estimativa:** 2 dias

## Descrição

REURBCAD (mobile) tem apenas 3 arquivos de docs. App mobile é crítico para coleta em campo, precisa documentar arquitetura offline-first, sincronização, GPS e WatermelonDB.

## Status Atual

**Completude:** 18% (3/16 arquivos)

**Existem:**
- [X] DOCS/README.md
- [X] DOCS/ARCHITECTURE/01-keycloak-integration.md
- [X] DOCS/HOW-TO/01-setup-keycloak.md

## Checklist - Arquivos Faltando

### ARCHITECTURE/ (4 faltando)
- [ ] README.md
- [ ] 01-overview.md (React Native + WatermelonDB)
- [ ] 03-data-flow.md (offline → sync → online)
- [ ] 04-integration.md (GEOAPI, GPS, Camera)
- [ ] 05-deployment.md (Android/iOS build)

### CONCEPTS/ (4 faltando)
- [ ] README.md
- [ ] 01-key-concepts.md (Offline-first, WatermelonDB, Sync)
- [ ] 02-terminology.md (Models, Sync Queue, CRUD local)
- [ ] 03-design-principles.md (Mobile UX, Performance)

### HOW-TO/ (4 faltando)
- [ ] README.md
- [ ] 01-setup-dev-environment.md (Expo/React Native CLI)
- [ ] 02-build-and-run.md (iOS Simulator, Android Emulator)
- [ ] 03-testing.md (Jest, Detox)
- [ ] 04-troubleshooting.md

### CODE (1 faltando)
- [ ] SRC-CODE/carf-reurbcad/README.md

## Conteúdo Específico Necessário

### 01-overview.md
- Diagrama arquitetura mobile
- Stack: React Native, WatermelonDB, React Navigation
- Offline-first: SQLite local
- Sincronização incremental

### 03-data-flow.md
- User input → Local DB (WatermelonDB) → Sync Queue
- Online detection → Sync Queue → API → Update local
- Conflict resolution
- GPS flow
- Camera flow

### 04-integration.md
- @carf/tscore (validations offline)
- @carf/geoapi-client (sync)
- GEOAPI backend
- Keycloak mobile (PKCE)
- Device APIs: GPS, Camera, NetInfo

### 05-deployment.md
- Expo build service
- Android: APK/AAB
- iOS: IPA, TestFlight
- Environment configs
- Code signing

## Localização

`PROJECTS/REURBCAD/DOCS/`

## Referências do Template

Ver: `CENTRAL/TEMPLATES/PROJECT-DOCS-TEMPLATE.md`
