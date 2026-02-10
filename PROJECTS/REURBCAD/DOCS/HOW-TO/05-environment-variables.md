---
type: leaf
status: review
updated: 2026-02-08
---

# Variaveis de Ambiente

Documentacao completa de todas as variaveis de ambiente do REURBCAD, organizacao por ambiente, integracao com EAS e procedimento para adicionar novas variaveis.

## Visao Geral

Todas as variaveis de ambiente expostas ao bundle JavaScript do app sao prefixadas com `EXPO_PUBLIC_`. Variaveis sem este prefixo nao sao acessiveis em runtime no app. As variaveis sao lidas em build-time e embutidas no bundle - alterar variaveis de ambiente exige um novo build.

## Tabela Completa de Variaveis

| Variavel | Tipo | Obrigatoria | Exemplo Dev | Exemplo Prod | Descricao |
|----------|------|-------------|-------------|-------------|-----------|
| `EXPO_PUBLIC_API_URL` | URL | Sim | `http://10.0.2.2:5000` | `https://api.carf.gov.br` | URL base da GEOAPI. Sem barra no final. Emulador Android usa `10.0.2.2` para acessar localhost do host. |
| `EXPO_PUBLIC_KEYCLOAK_URL` | URL | Sim | `http://10.0.2.2:8080` | `https://auth.carf.gov.br` | URL base do servidor Keycloak. |
| `EXPO_PUBLIC_KEYCLOAK_REALM` | string | Sim | `carf` | `carf` | Nome do realm no Keycloak. Geralmente `carf` em todos os ambientes. |
| `EXPO_PUBLIC_KEYCLOAK_CLIENT_ID` | string | Sim | `reurbcad` | `reurbcad` | Client ID configurado no Keycloak como public client com PKCE. |
| `EXPO_PUBLIC_DEEP_LINK_SCHEME` | string | Sim | `carf` | `carf` | Scheme do deep link para callback OAuth2. Resulta em `carf://oauth/callback`. |
| `EXPO_PUBLIC_SENTRY_DSN` | URL | Nao | `` (vazio) | `https://xxx@sentry.io/yyy` | DSN do Sentry para monitoramento de erros. Vazio desabilita Sentry em dev. |
| `EXPO_PUBLIC_MAP_TILE_URL` | URL | Nao | `` (vazio) | `https://tiles.carf.gov.br/{z}/{x}/{y}.png` | URL template para tiles de mapa offline. Vazio usa OpenStreetMap padrao. |
| `EXPO_PUBLIC_SYNC_INTERVAL_MS` | number | Nao | `900000` | `900000` | Intervalo de sync automatico em milissegundos. Padrao 15 minutos (900000). |
| `EXPO_PUBLIC_MAX_PHOTO_SIZE_KB` | number | Nao | `1024` | `512` | Tamanho maximo de foto apos compressao em KB. Dev permite maior para debugging. |
| `EXPO_PUBLIC_LOG_LEVEL` | string | Nao | `debug` | `error` | Nivel de log: `debug`, `info`, `warn`, `error`. |
| `EXPO_PUBLIC_ENABLE_OCR` | boolean | Nao | `true` | `true` | Habilita funcionalidade de OCR de documentos. `false` esconde opcao. |
| `EXPO_PUBLIC_BACKGROUND_SYNC` | boolean | Nao | `false` | `true` | Habilita sync em background via Expo Background Fetch. Desabilitado em dev para evitar interferencia. |

## Arquivos de Ambiente

O REURBCAD usa tres arquivos `.env`, um por ambiente:

### .env.development

Usado durante desenvolvimento local com `npx expo start`:

```env
EXPO_PUBLIC_API_URL=http://10.0.2.2:5000
EXPO_PUBLIC_KEYCLOAK_URL=http://10.0.2.2:8080
EXPO_PUBLIC_KEYCLOAK_REALM=carf
EXPO_PUBLIC_KEYCLOAK_CLIENT_ID=reurbcad
EXPO_PUBLIC_DEEP_LINK_SCHEME=carf
EXPO_PUBLIC_SENTRY_DSN=
EXPO_PUBLIC_MAP_TILE_URL=
EXPO_PUBLIC_SYNC_INTERVAL_MS=60000
EXPO_PUBLIC_MAX_PHOTO_SIZE_KB=1024
EXPO_PUBLIC_LOG_LEVEL=debug
EXPO_PUBLIC_ENABLE_OCR=true
EXPO_PUBLIC_BACKGROUND_SYNC=false
```

### .env.staging

Usado para builds de preview/homologacao:

```env
EXPO_PUBLIC_API_URL=https://api-staging.carf.gov.br
EXPO_PUBLIC_KEYCLOAK_URL=https://auth-staging.carf.gov.br
EXPO_PUBLIC_KEYCLOAK_REALM=carf
EXPO_PUBLIC_KEYCLOAK_CLIENT_ID=reurbcad
EXPO_PUBLIC_DEEP_LINK_SCHEME=carf
EXPO_PUBLIC_SENTRY_DSN=https://staging-dsn@sentry.io/project
EXPO_PUBLIC_MAP_TILE_URL=https://tiles-staging.carf.gov.br/{z}/{x}/{y}.png
EXPO_PUBLIC_SYNC_INTERVAL_MS=900000
EXPO_PUBLIC_MAX_PHOTO_SIZE_KB=512
EXPO_PUBLIC_LOG_LEVEL=info
EXPO_PUBLIC_ENABLE_OCR=true
EXPO_PUBLIC_BACKGROUND_SYNC=true
```

### .env.production

Usado para builds de producao submetidos as stores:

```env
EXPO_PUBLIC_API_URL=https://api.carf.gov.br
EXPO_PUBLIC_KEYCLOAK_URL=https://auth.carf.gov.br
EXPO_PUBLIC_KEYCLOAK_REALM=carf
EXPO_PUBLIC_KEYCLOAK_CLIENT_ID=reurbcad
EXPO_PUBLIC_DEEP_LINK_SCHEME=carf
EXPO_PUBLIC_SENTRY_DSN=https://prod-dsn@sentry.io/project
EXPO_PUBLIC_MAP_TILE_URL=https://tiles.carf.gov.br/{z}/{x}/{y}.png
EXPO_PUBLIC_SYNC_INTERVAL_MS=900000
EXPO_PUBLIC_MAX_PHOTO_SIZE_KB=512
EXPO_PUBLIC_LOG_LEVEL=error
EXPO_PUBLIC_ENABLE_OCR=true
EXPO_PUBLIC_BACKGROUND_SYNC=true
```

## Integracao com EAS Build

O `eas.json` referencia as variaveis de ambiente por profile:

```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "env": {
        "APP_ENV": "development"
      }
    },
    "preview": {
      "distribution": "internal",
      "env": {
        "APP_ENV": "staging"
      }
    },
    "production": {
      "env": {
        "APP_ENV": "production"
      }
    }
  }
}
```

O `app.config.js` carrega o arquivo `.env` correto baseado em `APP_ENV`:

```javascript
// app.config.js
import 'dotenv/config';

const envFile = process.env.APP_ENV === 'production'
  ? '.env.production'
  : process.env.APP_ENV === 'staging'
    ? '.env.staging'
    : '.env.development';

require('dotenv').config({ path: envFile, override: true });

export default {
  expo: {
    name: 'REURBCAD',
    slug: 'reurbcad',
    scheme: process.env.EXPO_PUBLIC_DEEP_LINK_SCHEME,
    // ...
  },
};
```

## Como Adicionar uma Nova Variavel

### Passo 1: Definir a variavel

Escolher nome com prefixo `EXPO_PUBLIC_` e convencao UPPER_SNAKE_CASE:

```
EXPO_PUBLIC_NOVA_FEATURE_ENABLED=true
```

### Passo 2: Adicionar em todos os arquivos .env

Adicionar em `.env.development`, `.env.staging` e `.env.production` com valores apropriados para cada ambiente.

### Passo 3: Adicionar no .env.example

Documentar no `.env.example` com valor placeholder e comentario:

```env
# Habilita nova feature (true/false)
EXPO_PUBLIC_NOVA_FEATURE_ENABLED=true
```

### Passo 4: Tipar a variavel

Adicionar ao arquivo de tipos de ambiente:

```typescript
// src/types/env.d.ts
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      EXPO_PUBLIC_NOVA_FEATURE_ENABLED: string;
      // ... demais variaveis
    }
  }
}
```

### Passo 5: Criar constante tipada

Adicionar ao arquivo de constantes para acesso tipado:

```typescript
// src/constants/env.ts
export const ENV = {
  API_URL: process.env.EXPO_PUBLIC_API_URL!,
  KEYCLOAK_URL: process.env.EXPO_PUBLIC_KEYCLOAK_URL!,
  // ...
  NOVA_FEATURE_ENABLED: process.env.EXPO_PUBLIC_NOVA_FEATURE_ENABLED === 'true',
} as const;
```

### Passo 6: Atualizar documentacao

Adicionar a nova variavel na tabela deste documento com descricao, tipo, obrigatoriedade e exemplos.

## Seguranca

Variaveis `EXPO_PUBLIC_*` sao embutidas no bundle JavaScript e podem ser extraidas por reverse engineering do APK/IPA. Portanto:

- **Nunca** colocar secrets (API keys privadas, database passwords) em variaveis `EXPO_PUBLIC_*`
- O `KEYCLOAK_CLIENT_ID` e seguro pois e um public client (PKCE, sem client_secret)
- O `SENTRY_DSN` e seguro pois o DSN permite apenas enviar eventos, nao ler
- Segredos do backend sao gerenciados exclusivamente no Docker Compose e nunca expostos ao app mobile

## Validacao de Variaveis no Boot

O app valida a presenca de variaveis obrigatorias no startup:

```typescript
// src/utils/validate-env.ts
export function validateEnvironment(): void {
  const required = [
    'EXPO_PUBLIC_API_URL',
    'EXPO_PUBLIC_KEYCLOAK_URL',
    'EXPO_PUBLIC_KEYCLOAK_REALM',
    'EXPO_PUBLIC_KEYCLOAK_CLIENT_ID',
    'EXPO_PUBLIC_DEEP_LINK_SCHEME',
  ];

  const missing = required.filter(key => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(
      `Variaveis de ambiente obrigatorias nao definidas: ${missing.join(', ')}\n` +
      'Copie .env.example para .env.development e preencha os valores.'
    );
  }
}
```

## Referencias

- [Setup Dev Environment](./04-setup-dev-environment.md)
- [Build and Release](../DEPLOYMENT/01-build-and-release.md)
- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
- [Error Handling](../ARCHITECTURE/05-error-handling.md)
