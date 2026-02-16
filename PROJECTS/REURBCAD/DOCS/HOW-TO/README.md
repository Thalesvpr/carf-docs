---
type: readme
status: review
description: "Usa listas/bullets ao inves de paragrafos densos, contem listas numeradas nao convertidas para prosa"
updated: 2026-02-08
---

# HOW-TO - REURBCAD

Guias praticos para desenvolvimento do REURBCAD React Native.

## Autenticacao

- **[01-setup-keycloak.md](./01-setup-keycloak.md)** - Configurar Keycloak redirect URIs para deep links (exp://...)
- **[02-handle-callbacks.md](./02-handle-callbacks.md)** - Configurar deep linking, Linking.addEventListener, parse authorization code
- **[03-test-offline.md](./03-test-offline.md)** - Testar autenticacao offline, biometric, token refresh

## Desenvolvimento

- **[04-setup-dev-environment.md](./04-setup-dev-environment.md)** - Setup completo: Node, Expo CLI, emuladores Android/iOS, variaveis de ambiente
- **[05-environment-variables.md](./05-environment-variables.md)** - Configuracao de .env, app.config.ts, variaveis por ambiente (dev/staging/prod)
- **[06-troubleshooting.md](./06-troubleshooting.md)** - Problemas comuns: Metro bundler, builds nativas, permissoes, sync
- **[07-add-new-screen.md](./07-add-new-screen.md)** - Passo-a-passo para criar nova tela com Expo Router, form, validacao
- **[08-dev-start-dinamico.md](./08-dev-start-dinamico.md)** - Script automatizado: detecta IP, atualiza .env, registra redirect URIs no Keycloak, inicia Expo
- **[09-adb-wifi.md](./09-adb-wifi.md)** - Desenvolvimento sem cabo USB via ADB WiFi

## Setup Rapido

1. `npm install` ou `yarn install`
2. Configurar `.env` com KEYCLOAK_URL, GEOAPI_URL
3. `npx expo start` para iniciar Metro bundler
4. Executar em emulador ou device fisico

## Build

- Android: `eas build --platform android`
- iOS: `eas build --platform ios`

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisao

- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/01-setup-keycloak.md|01-setup-keycloak]]
- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/02-handle-callbacks.md|02-handle-callbacks]]
- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/03-test-offline.md|03-test-offline]]

### Planejados

- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/04-setup-dev-environment.md|04-setup-dev-environment]]
- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/05-environment-variables.md|05-environment-variables]]
- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/06-troubleshooting.md|06-troubleshooting]]
- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/07-add-new-screen.md|07-add-new-screen]]

### Em Revisao

- ○ [[PROJECTS/REURBCAD/DOCS/HOW-TO/08-dev-start-dinamico.md|08-dev-start-dinamico]]

<!-- CARF-INDEX-END -->
