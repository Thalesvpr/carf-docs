# WEBDOCS + Keycloak (VitePress - Opcional)

## Install
```bash
npm install keycloak-js
```

## Config
```typescript
// docs/.vitepress/theme/keycloak.ts
import Keycloak from 'keycloak-js';

export const keycloak = new Keycloak({
  url: 'http://localhost:8080',
  realm: 'carf',
  clientId: 'webdocs',
});
```

## Theme Setup
```typescript
// docs/.vitepress/theme/index.ts
import DefaultTheme from 'vitepress/theme';
import { keycloak } from './keycloak';

export default {
  ...DefaultTheme,
  async enhanceApp({ app }) {
    if (typeof window !== 'undefined') {
      await keycloak.init({ onLoad: 'check-sso', pkceMethod: 'S256' });

      app.config.globalProperties.$keycloak = keycloak;
      app.config.globalProperties.$isAuthenticated = keycloak.authenticated;
    }
  }
};
```

## Protected Page Component
```vue
<!-- docs/.vitepress/theme/components/ProtectedContent.vue -->
<template>
  <div v-if="$isAuthenticated">
    <slot />
  </div>
  <div v-else>
    <p>Esta documentação requer autenticação.</p>
    <button @click="login">Login</button>
  </div>
</template>

<script setup>
const login = () => {
  window.$keycloak.login();
};
</script>
```

## Usage in Markdown
```md
<!-- docs/internal/architecture.md -->
# Arquitetura Interna (Privado)

<ProtectedContent>

## Database Schema
...conteúdo protegido...

</ProtectedContent>
```

## Public by Default
```md
<!-- docs/guide/getting-started.md -->
# Getting Started

Este conteúdo é público e não requer autenticação.
```

## Environment Variables
```env
# docs/.vitepress/.env
VITE_KEYCLOAK_URL=http://localhost:8080
VITE_KEYCLOAK_REALM=carf
VITE_KEYCLOAK_CLIENT_ID=webdocs
```

Done. ✅
