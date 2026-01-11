# LAYERS - REURBCAD

Estrutura de camadas do código React Native do REURBCAD.

## Camadas da Aplicação

### Auth Service

- **[01-auth-service.md](./01-auth-service.md)** - AuthService class, OAuth2 flow, token management, secure storage

**Responsabilidades:**
- Gerenciar OAuth2 authorization code flow
- Store tokens em expo-secure-store
- Refresh tokens automaticamente
- Biometric authentication

### Offline Storage

**WatermelonDB:**
- Models (Unit, Holder, Community, Photo)
- Sync adapter para GEOAPI
- Query reactive observers

### Sync Service

**Conflict Resolution:**
- Detect conflits via timestamps
- Merge strategies (last-write-wins, manual)
- Batch sync para performance

### UI Components

**React Native components:**
- Navigation stack (React Navigation)
- Maps (react-native-maps)
- Camera (expo-camera)
- Forms com validation

---

**Última atualização:** 2026-01-10
