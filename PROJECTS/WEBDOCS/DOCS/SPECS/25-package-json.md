---
type: leaf
status: review
updated: 2026-01-21
---

# Package.json e TSConfig

Arquivos de configuração do projeto WEBDOCS para setup completo do ambiente de desenvolvimento.

## package.json Completo

```json
{
  "name": "carf-webdocs",
  "version": "0.1.0",
  "type": "module",
  "private": true,
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "check": "astro check",
    "validate": "bun run validate:content && bun run validate:sources",
    "validate:content": "bun run scripts/validate-content.ts",
    "validate:sources": "bun run scripts/validate-sources.ts",
    "lint": "biome check .",
    "lint:fix": "biome check --apply .",
    "format": "biome format --write .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  },
  "dependencies": {
    "astro": "^4.16.0",
    "@astrojs/starlight": "^0.28.0",
    "@astrojs/react": "^3.6.0",
    "@astrojs/mdx": "^3.1.0",
    "@astrojs/sitemap": "^3.2.0",
    "@astrojs/vercel": "^7.8.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "jose": "^5.9.0",
    "zod": "^3.23.0",
    "@carf/tscore": "workspace:*",
    "@carf/geoapi-client": "workspace:*",
    "@carf/ui": "workspace:*"
  },
  "devDependencies": {
    "typescript": "^5.6.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@biomejs/biome": "^1.9.0",
    "vitest": "^2.1.0",
    "@playwright/test": "^1.48.0",
    "@astrojs/check": "^0.9.0"
  },
  "engines": {
    "node": ">=20.0.0"
  },
  "packageManager": "bun@1.1.0"
}
```

## Dependências Explicadas

```json
{
  "dependencies_explained": {
    "core": {
      "astro": "Framework principal",
      "@astrojs/starlight": "Template de documentação",
      "@astrojs/vercel": "Adapter para deploy Vercel com SSR"
    },
    "integrations": {
      "@astrojs/react": "Suporte a componentes React",
      "@astrojs/mdx": "Suporte a MDX em content collections",
      "@astrojs/sitemap": "Geração automática de sitemap.xml"
    },
    "react": {
      "react": "Runtime React para componentes @carf/ui",
      "react-dom": "DOM bindings para React"
    },
    "auth": {
      "jose": "JWT verification com JWKS (usado no middleware)"
    },
    "validation": {
      "zod": "Schema validation para env vars e content"
    },
    "carf_libs": {
      "@carf/tscore": "Value Objects e types compartilhados",
      "@carf/geoapi-client": "SDK para chamadas à GeoAPI",
      "@carf/ui": "Componentes React compartilhados"
    }
  }
}
```

## tsconfig.json Completo

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@lib/*": ["src/lib/*"],
      "@config/*": ["src/config/*"],
      "@content/*": ["src/content/*"]
    },
    "jsx": "react-jsx",
    "jsxImportSource": "react",
    "types": ["astro/client", "vite/client"],
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*", "tests/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## biome.json

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExcessiveCognitiveComplexity": "warn"
      },
      "correctness": {
        "noUnusedImports": "error",
        "noUnusedVariables": "error"
      },
      "style": {
        "useConst": "error",
        "noNonNullAssertion": "warn"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "es5",
      "semicolons": "always"
    }
  },
  "files": {
    "ignore": [
      "node_modules",
      "dist",
      ".astro",
      "public/admin"
    ]
  }
}
```

## playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:4321',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'bun run preview',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
  },
});
```

## vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';
import { getViteConfig } from 'astro/config';

export default defineConfig(
  getViteConfig({
    test: {
      include: ['tests/unit/**/*.{test,spec}.{js,ts}'],
      globals: true,
      environment: 'node',
      coverage: {
        provider: 'v8',
        reporter: ['text', 'json', 'html'],
        include: ['src/lib/**/*.ts'],
        exclude: ['src/lib/**/*.d.ts'],
      },
    },
  })
);
```

## Instalação

```bash
# 1. Criar projeto (se novo)
mkdir carf-webdocs && cd carf-webdocs

# 2. Inicializar com package.json acima
# Copiar package.json para a raiz

# 3. Instalar dependências
bun install

# 4. Copiar arquivos de configuração
# - tsconfig.json
# - biome.json
# - playwright.config.ts
# - vitest.config.ts

# 5. Verificar instalação
bun run check
```

## Atualização de Dependências

```bash
# Ver dependências desatualizadas
bun outdated

# Atualizar todas
bun update

# Atualizar específica
bun update astro
```

## Workspace (Monorepo)

Se WEBDOCS está no monorepo CARF, as libs usam `workspace:*`:

```json
{
  "note": "workspace:* resolve para versão local durante desenvolvimento",
  "publish_behavior": "Ao publicar, bun substitui por versão específica",
  "requirement": "Monorepo deve ter workspaces configurado no package.json raiz"
}
```

Package.json raiz do monorepo:

```json
{
  "name": "carf",
  "private": true,
  "workspaces": [
    "PROJECTS/LIB/TS/*",
    "PROJECTS/WEBDOCS/SRC-CODE/carf-webdocs",
    "PROJECTS/GEOWEB/SRC-CODE/*",
    "PROJECTS/REURBCAD/SRC-CODE/*"
  ]
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Draft
