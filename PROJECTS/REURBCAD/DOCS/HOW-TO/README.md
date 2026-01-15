# HOW-TO - REURBCAD

Guias práticos para desenvolvimento do REURBCAD React Native.

## Autenticação

- **[01-setup-keycloak.md](./01-setup-keycloak.md)** - Configurar Keycloak redirect URIs para deep links (exp://...)
- **[02-handle-callbacks.md](./02-handle-callbacks.md)** - Configurar deep linking, Linking.addEventListener, parse authorization code
- **[03-test-offline.md](./03-test-offline.md)** - Testar autenticação offline, biometric, token refresh

## Desenvolvimento Local

**Setup:**
1. `npm install` ou `yarn install`
2. Configurar `.env` com KEYCLOAK_URL, GEOAPI_URL
3. `npx expo start` para iniciar Metro bundler
4. Executar em emulador ou device físico

**Build:**
- Android: `eas build --platform android`
- iOS: `eas build --platform ios`

---

**Última atualização:** 2026-01-10

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-setup-keycloak](./01-setup-keycloak.md) | 01-setup-keycloak |
| [02-handle-callbacks](./02-handle-callbacks.md) | 02-handle-callbacks |
| [03-test-offline](./03-test-offline.md) | 03-test-offline |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Falta parágrafo denso introdutório.
