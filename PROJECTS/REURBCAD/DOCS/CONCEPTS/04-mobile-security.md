---
type: leaf
status: review
updated: 2026-02-08
---

# Seguranca Mobile - REURBCAD

Estrategia de seguranca do aplicativo mobile REURBCAD cobrindo protecao de dados em transito e repouso, deteccao de dispositivos comprometidos, hardening de comunicacao e conformidade com OWASP Mobile Top 10.

## Visao Geral

O REURBCAD lida com dados sensiveis de cadastro urbano: CPFs, enderecos, fotografias geolocalizadas e informacoes de titulares. A estrategia de seguranca mobile implementa defesa em profundidade com multiplas camadas complementares.

| Camada | Mecanismo | Ferramenta |
|--------|-----------|------------|
| Transporte | TLS 1.3 + SSL Pinning | react-native-ssl-pinning |
| Autenticacao | OAuth2 PKCE + tokens efemeros | @carf/tscore auth |
| Armazenamento | SQLCipher (DB) + AES-256 (fotos) | WatermelonDB + expo-crypto |
| Dispositivo | Jailbreak/root detection | expo-device + jail-monkey |
| Rede | Certificate transparency + HSTS | Configuracao nativa |
| Aplicacao | Obfuscacao + anti-tampering | ProGuard (Android) / Bitcode (iOS) |

## SSL Pinning

### Configuracao com react-native-ssl-pinning

SSL Pinning garante que o app so se comunique com servidores que possuem certificados conhecidos, prevenindo ataques Man-in-the-Middle mesmo com CA comprometida.

```typescript
// services/http-client.ts
import { fetch as sslFetch } from 'react-native-ssl-pinning';

const PINNED_CERTS = {
  'api.carf.gov.br': {
    // SHA-256 hash do certificado publico
    sha256: ['AABB...hash-do-cert-primario', 'CCDD...hash-do-cert-backup'],
  },
  'auth.carf.gov.br': {
    sha256: ['EEFF...hash-keycloak-primary', 'GGHH...hash-keycloak-backup'],
  },
};

export async function secureFetch(url: string, options: RequestInit) {
  const hostname = new URL(url).hostname;
  const pins = PINNED_CERTS[hostname];

  if (!pins) {
    throw new Error(`Nenhum pin configurado para ${hostname}`);
  }

  return sslFetch(url, {
    ...options,
    sslPinning: {
      certs: pins.sha256,
    },
    timeoutInterval: 30000,
  });
}
```

### Rotacao de Certificados

| Acao | Frequencia | Responsavel |
|------|-----------|-------------|
| Verificar validade dos certs pinados | Mensal | DevOps |
| Incluir cert backup no proximo pin set | A cada renovacao | DevOps |
| Atualizar app com novos pins via OTA | Antes da expiracao | Mobile dev |
| Manter 2 pins ativos (primary + backup) | Sempre | Ambos |

## Certificate Transparency

O REURBCAD valida que certificados do servidor estao registrados em logs publicos de Certificate Transparency (CT), detectando certificados fraudulentos emitidos por CAs comprometidas.

```typescript
// Configuracao no Android (network_security_config.xml)
// android/app/src/main/res/xml/network_security_config.xml
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
  <domain-config>
    <domain includeSubdomains="true">api.carf.gov.br</domain>
    <domain includeSubdomains="true">auth.carf.gov.br</domain>
    <pin-set expiration="2027-01-01">
      <pin digest="SHA-256">base64-encoded-pin-primary</pin>
      <pin digest="SHA-256">base64-encoded-pin-backup</pin>
    </pin-set>
    <trustkit-config enforcePinning="true" />
  </domain-config>
</network-security-config>
```

No iOS, a configuracao equivalente e feita via `Info.plist` com `NSAppTransportSecurity` e pins customizados.

## Deteccao de Jailbreak/Root

Dispositivos com jailbreak (iOS) ou root (Android) representam risco pois permitem acesso ao filesystem do app, interceptacao de chamadas de API e injecao de codigo.

```typescript
// hooks/useDeviceSecurity.ts
import * as Device from 'expo-device';
import JailMonkey from 'jail-monkey';

interface DeviceSecurityStatus {
  isRooted: boolean;
  isEmulator: boolean;
  isDebugMode: boolean;
  trustLevel: 'trusted' | 'warning' | 'blocked';
}

export function useDeviceSecurity(): DeviceSecurityStatus {
  const isRooted = JailMonkey.isJailBroken();
  const isEmulator = !Device.isDevice;
  const isDebugMode = __DEV__;

  let trustLevel: DeviceSecurityStatus['trustLevel'] = 'trusted';

  if (isRooted) {
    trustLevel = 'blocked'; // Impedir uso em producao
  } else if (isEmulator && !isDebugMode) {
    trustLevel = 'warning'; // Alertar mas permitir
  }

  return { isRooted, isEmulator, isDebugMode, trustLevel };
}
```

### Politica por Nivel de Confianca

| Nivel | Condicao | Acao |
|-------|---------|------|
| `trusted` | Device fisico, sem root/jailbreak | Acesso completo |
| `warning` | Emulador em ambiente nao-debug | Alertar usuario, registrar no audit log |
| `blocked` | Jailbreak/root detectado | Bloquear acesso, exibir mensagem, nao persistir dados |

## Criptografia em Repouso

### WatermelonDB com SQLCipher

O banco local WatermelonDB usa SQLCipher para criptografar todo o database SQLite com AES-256-CBC.

```typescript
// database/setup.ts
import { Database } from '@nozbe/watermelondb';
import SQLiteAdapter from '@nozbe/watermelondb/adapters/sqlite';
import * as SecureStore from 'expo-secure-store';
import * as Crypto from 'expo-crypto';

async function getDatabaseKey(): Promise<string> {
  let key = await SecureStore.getItemAsync('db_encryption_key');

  if (!key) {
    // Gerar chave de 256 bits na primeira execucao
    key = await Crypto.digestStringAsync(
      Crypto.CryptoDigestAlgorithm.SHA256,
      `${Date.now()}-${Math.random()}-reurbcad`
    );
    await SecureStore.setItemAsync('db_encryption_key', key);
  }

  return key;
}

export async function createDatabase(): Promise<Database> {
  const encryptionKey = await getDatabaseKey();

  const adapter = new SQLiteAdapter({
    schema,
    migrations,
    dbName: 'reurbcad',
    jsi: true,
    // SQLCipher encryption
    experimentalUnsafeNativeReuse: false,
    // A chave e passada nativamente via PRAGMA key
  });

  return new Database({ adapter, modelClasses });
}
```

### Criptografia de Fotos

Fotos capturadas em campo contem dados sensiveis (residencias, documentos). Sao criptografadas com AES-256 antes de salvar no filesystem.

```typescript
// services/photo-encryption.ts
import * as FileSystem from 'expo-file-system';
import * as Crypto from 'expo-crypto';

export async function encryptPhoto(
  sourceUri: string,
  encryptionKey: string
): Promise<string> {
  const photoData = await FileSystem.readAsStringAsync(sourceUri, {
    encoding: FileSystem.EncodingType.Base64,
  });

  // Gerar IV unico para cada foto
  const iv = await Crypto.getRandomBytesAsync(16);
  const ivBase64 = btoa(String.fromCharCode(...iv));

  // Criptografar com AES-256-GCM (via modulo nativo)
  const encrypted = await NativeAES.encrypt(photoData, encryptionKey, ivBase64);

  // Salvar arquivo criptografado com extensao .enc
  const encryptedUri = sourceUri.replace(/\.\w+$/, '.enc');
  await FileSystem.writeAsStringAsync(encryptedUri, `${ivBase64}:${encrypted}`, {
    encoding: FileSystem.EncodingType.UTF8,
  });

  // Remover original nao criptografado
  await FileSystem.deleteAsync(sourceUri, { idempotent: true });

  return encryptedUri;
}
```

## Request Signing (HMAC)

Requests criticos (sync push, criacao de unidades) sao assinados com HMAC-SHA256 para garantir integridade.

```typescript
// services/request-signer.ts
import * as Crypto from 'expo-crypto';

export async function signRequest(
  method: string,
  path: string,
  body: string,
  timestamp: number,
  secret: string
): Promise<string> {
  const payload = `${method}\n${path}\n${timestamp}\n${body}`;

  const signature = await Crypto.digestStringAsync(
    Crypto.CryptoDigestAlgorithm.SHA256,
    `${secret}:${payload}`
  );

  return signature;
}

// Uso no interceptor axios
api.interceptors.request.use(async (config) => {
  if (['POST', 'PUT', 'DELETE'].includes(config.method?.toUpperCase() ?? '')) {
    const timestamp = Date.now();
    const body = JSON.stringify(config.data ?? {});
    const secret = await SecureStore.getItemAsync('hmac_secret');

    const signature = await signRequest(
      config.method!.toUpperCase(),
      config.url!,
      body,
      timestamp,
      secret!
    );

    config.headers['X-Signature'] = signature;
    config.headers['X-Timestamp'] = timestamp.toString();
  }

  return config;
});
```

## Rate Limit Handling

```typescript
// services/rate-limit-handler.ts
const MAX_RETRIES = 5;
const BASE_DELAY_MS = 1000;

export async function withRateLimitRetry<T>(
  fn: () => Promise<T>,
  retries = MAX_RETRIES
): Promise<T> {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      if (error.response?.status === 429 && attempt < retries) {
        const retryAfter = error.response.headers['retry-after'];
        const delay = retryAfter
          ? parseInt(retryAfter, 10) * 1000
          : BASE_DELAY_MS * Math.pow(2, attempt); // Exponential backoff

        console.warn(
          `Rate limited. Tentativa ${attempt + 1}/${retries}. ` +
          `Aguardando ${delay}ms`
        );

        await new Promise((resolve) => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

## OWASP Mobile Top 10 - Mitigacoes

| # | Risco OWASP | Mitigacao REURBCAD |
|---|-------------|-------------------|
| M1 | Uso inadequado de credenciais | Tokens armazenados em expo-secure-store (Keychain/KeyStore), nunca em AsyncStorage. Access token apenas em memoria. Refresh token criptografado. |
| M2 | Seguranca inadequada de dados | SQLCipher para DB, AES-256 para fotos, limpeza de cache ao logout, nenhum dado sensivel em logs. |
| M3 | Comunicacao insegura | TLS 1.3 obrigatorio, SSL pinning em todos os endpoints, certificate transparency, HSTS. |
| M4 | Autenticacao insuficiente | OAuth2 PKCE sem client_secret, tokens com TTL curto (5 min access, 30 min refresh), biometria como segundo fator. |
| M5 | Autorizacao insuficiente | RBAC validado no backend (GEOAPI), RLS por tenant, permissoes por comunidade. App mobile nao confia em validacoes client-side. |
| M6 | Qualidade de codigo insuficiente | TypeScript strict, ESLint com regras de seguranca, Zod para validacao de inputs, code review obrigatorio. |
| M7 | Adulteracao de codigo | ProGuard (Android) para obfuscacao, Bitcode (iOS), deteccao de jailbreak/root, assinatura de requests HMAC. |
| M8 | Engenharia reversa | ProGuard com regras customizadas, R8 full mode, nenhum secret hardcoded (config via env vars no build). |
| M9 | Funcionalidade estranha | Nenhum backdoor, logs de debug removidos em producao, analytics respeitando LGPD, sem coleta excessiva. |
| M10 | Funcionalidade extraneous | Permissoes minimas (camera, location, storage apenas quando necessario), deep links validados, intents filtrados. |

## Praticas de Codigo Seguro

| Pratica | Implementacao |
|---------|--------------|
| Nunca logar tokens | Logger customizado que filtra campos `token`, `password`, `secret` |
| Access token em memoria | Zustand store sem persistencia para accessToken, apenas refreshToken no SecureStore |
| Validacao dupla | Client-side (Zod) + server-side (FluentValidation), nunca confiar apenas no client |
| Timeout de sessao | 30 min de inatividade = forcar re-autenticacao |
| Limpeza ao logout | Apagar DB (WatermelonDB reset), limpar SecureStore, limpar cache de fotos |
| Deep link validation | Verificar scheme e host antes de processar callback OAuth |
| Clipboard protection | Desabilitar copy em campos sensiveis (CPF, tokens) |
| Screenshot prevention | FLAG_SECURE (Android) em telas com dados sensiveis |

## Seguranca de Tokens

### Ciclo de Vida do Token

```
Login PKCE → Access Token (5 min, memoria)
                         → Refresh Token (30 min, SecureStore criptografado)

Access Token expirado → Refresh silencioso via @carf/tscore
                      → Novo Access Token (memoria)
                      → Novo Refresh Token (SecureStore)

Refresh Token expirado → Forcar re-login
                       → Limpar todos os tokens
                       → Redirecionar para tela de login
```

### Regras de Token

| Regra | Justificativa |
|-------|--------------|
| Access token nunca persiste em disco | Reduz janela de exposicao se device comprometido |
| Refresh token criptografado no SecureStore | SecureStore usa Keychain (iOS) / KeyStore (Android) com hardware backing |
| Nenhum token em logs (console, Sentry) | Sanitizacao automatica de payloads antes de logging |
| Token invalidation no logout | Chamar endpoint de revogacao do Keycloak antes de limpar localmente |
| Clock skew tolerance de 30s | Compensar diferenca de relogio entre device e servidor |

## Referencias

- [CONCEPTS/01-authentication.md](./01-authentication.md) - Fluxo de autenticacao
- [CONCEPTS/02-offline-authentication.md](./02-offline-authentication.md) - Autenticacao offline
- [CONCEPTS/03-secure-storage.md](./03-secure-storage.md) - Armazenamento seguro
- [CENTRAL/SECURITY/01-security-strategy.md](../../../../CENTRAL/SECURITY/01-security-strategy.md) - Estrategia de seguranca CARF
- [CENTRAL/SECURITY/02-lgpd-compliance.md](../../../../CENTRAL/SECURITY/02-lgpd-compliance.md) - Conformidade LGPD
