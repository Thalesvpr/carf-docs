---
type: leaf
status: review
updated: 2026-02-08
---

# Armazenamento Seguro

## Visao Geral

Secure storage no REURBCAD usa `expo-secure-store` (Expo) ou `react-native-keychain` (bare RN) para armazenar `refresh_token` encrypted via hardware-backed security modules: Keychain (iOS) e Keystore (Android).

> **Nunca usar AsyncStorage** para tokens - plain text acessivel via device backup, root/jailbreak, ou malware.

## Comparativo iOS vs Android

| Aspecto | iOS Keychain | Android Keystore |
|---|---|---|
| Hardware Security | Secure Enclave (A7+ chips) | TEE (Trusted Execution Environment) ou StrongBox (Pixel 3+) |
| Algoritmo Encryption | AES-256-GCM | RSA-2048 ou AES-256-GCM (depende API level e hardware) |
| Key Derivation | Device hardware UID + user passcode | Keys geradas e armazenadas no TEE |
| Key Export | Nao exportavel do Secure Enclave | Nunca exported do KeyStore |
| Tamper Resistance | Hardware tamper-resistant, nao acessivel via software mesmo com root | Decryption acontece apenas dentro do secure hardware |
| Fallback (sem hardware) | Software-based encryption (menos seguro, mas melhor que plain text) | Software-based encryption |
| Backup | kSecAttrAccessibleAfterFirstUnlock items excluded do iCloud Keychain backup | KeyStore items nunca backed up automaticamente |

## iOS Keychain

### Secure Enclave

Chips A7+ possuem Secure Enclave - hardware security module tamper-resistant nao acessivel via software mesmo com root.

### Accessibility Levels

Keychain iOS implementation usa `kSecAttrAccessible` com `kSecAttrAccessibleAfterFirstUnlock`:

- Permite acesso apos device unlock primeira vez
- Garante availability mas mantem encryption at rest
- Data encrypted via AES-256-GCM usando key derivada do device hardware UID + user passcode no Secure Enclave

### Devices Antigos

Se device nao tem Secure Enclave (older devices), usa software-based encryption - menos seguro mas ainda melhor que plain text.

## Android Keystore

### TEE e StrongBox

Android KeyStore system armazena cryptographic keys em:

- **TEE** (Trusted Execution Environment) - disponivel na maioria dos devices
- **StrongBox** (hardware security module) - disponivel em Pixel 3+ e devices mais recentes

### Protecao

- Keys nunca exported do KeyStore
- Decryption acontece apenas dentro do secure hardware
- Algoritmo: RSA-2048 ou AES-256-GCM dependendo API level e hardware support

## Biometric Integration

Integracao opcional via `expo-local-authentication` antes de acessar SecureStore, adicionando layer extra exigindo fingerprint/face antes de ler `refresh_token`.

## Usage Patterns

### Salvar Token (apos login)

```typescript
await SecureStore.setItemAsync('refresh_token', refreshToken, {
  keychainAccessible: SecureStore.AFTER_FIRST_UNLOCK
});
```

Options especificam accessibility level do Keychain.

### Restaurar Sessao (app startup)

```typescript
const refreshToken = await SecureStore.getItemAsync('refresh_token');
// Retorna null se nao existe, ou string encrypted se existe
```

### Logout (remover token)

```typescript
await SecureStore.deleteItemAsync('refresh_token');
// Remove permanentemente do Keychain/Keystore
```

### Error Handling

```typescript
try {
  await SecureStore.setItemAsync('refresh_token', refreshToken);
} catch (error) {
  // Pode falhar se storage full (raro)
  // ou device encryption disabled (user setting)
}
```

## O Que Armazenar Onde

| Dado | Storage | Motivo |
|---|---|---|
| `refresh_token` | SecureStore | Sensivel, acesso ao backend |
| `access_token` | Memoria (class property) | Dura apenas 5 min, overhead de encryption desnecessario. Wiped quando app killed pelo OS |
| `tenant_id`, `user_id` | SecureStore | Dados sensiveis |
| User preferences, theme | AsyncStorage | Nao sensivel |
| Dados gerais nao sensiveis | AsyncStorage ou encrypt via crypto library | Depende do contexto |

## Backup Considerations

### iOS

iCloud Keychain backup inclui Keychain items por padrao, mas `kSecAttrAccessibleAfterFirstUnlock` items sao **excluded** - garantindo que `refresh_token` nao vaza via backup.

### Android

KeyStore items **nunca** sao backed up automaticamente, protegendo tokens.

## Migracao AsyncStorage para SecureStore

Em app update que muda de AsyncStorage para SecureStore:

1. Ler tokens de AsyncStorage
2. Salvar em SecureStore
3. Deletar de AsyncStorage via `database.clear()`
4. Evitar deixar tokens plain text apos migration

## Referencias

- [Authentication](./01-authentication.md)
- [Offline Authentication](./02-offline-authentication.md)
- [AuthService Layer](../LAYERS/01-auth-service.md)
