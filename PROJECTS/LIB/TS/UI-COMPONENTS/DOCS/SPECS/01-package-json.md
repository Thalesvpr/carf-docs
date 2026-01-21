---
title: "Package.json - @carf/ui"
status: review
updated: 2026-01-21
source: "CENTRAL/LIBRARIES/03-ui-components.md"
---

# Package.json - @carf/ui

Configuracao completa do package.json para a biblioteca de componentes React.

## Configuracao Completa

```json
{
  "name": "@carf/ui",
  "version": "0.1.0",
  "description": "Biblioteca de componentes React para o ecossistema CARF",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "sideEffects": [
    "**/*.css"
  ],
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./globals.css": "./dist/globals.css",
    "./tailwind.config": "./tailwind.config.js"
  },
  "files": [
    "dist",
    "tailwind.config.js",
    "README.md"
  ],
  "scripts": {
    "build": "vite build && tsc --emitDeclarationOnly",
    "dev": "vite",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist",
    "prepublishOnly": "bun run build"
  },
  "dependencies": {
    "class-variance-authority": "0.7.0",
    "clsx": "2.1.0",
    "tailwind-merge": "2.2.0"
  },
  "peerDependencies": {
    "@radix-ui/react-accordion": "1.1.2",
    "@radix-ui/react-alert-dialog": "1.0.5",
    "@radix-ui/react-avatar": "1.0.4",
    "@radix-ui/react-checkbox": "1.0.4",
    "@radix-ui/react-dialog": "1.0.5",
    "@radix-ui/react-dropdown-menu": "2.0.6",
    "@radix-ui/react-label": "2.0.2",
    "@radix-ui/react-popover": "1.0.7",
    "@radix-ui/react-progress": "1.0.3",
    "@radix-ui/react-select": "2.0.0",
    "@radix-ui/react-separator": "1.0.3",
    "@radix-ui/react-slot": "1.0.2",
    "@radix-ui/react-switch": "1.0.3",
    "@radix-ui/react-tabs": "1.0.4",
    "@radix-ui/react-toast": "1.1.5",
    "@radix-ui/react-tooltip": "1.0.7",
    "lucide-react": "0.312.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "tailwindcss": "3.4.1"
  },
  "devDependencies": {
    "@storybook/addon-essentials": "7.6.10",
    "@storybook/addon-interactions": "7.6.10",
    "@storybook/addon-links": "7.6.10",
    "@storybook/blocks": "7.6.10",
    "@storybook/react": "7.6.10",
    "@storybook/react-vite": "7.6.10",
    "@testing-library/jest-dom": "6.2.0",
    "@testing-library/react": "14.1.2",
    "@types/node": "20.11.5",
    "@types/react": "18.2.48",
    "@types/react-dom": "18.2.18",
    "@typescript-eslint/eslint-plugin": "6.19.0",
    "@typescript-eslint/parser": "6.19.0",
    "@vitejs/plugin-react": "4.2.1",
    "autoprefixer": "10.4.17",
    "eslint": "8.56.0",
    "eslint-plugin-react": "7.33.2",
    "eslint-plugin-react-hooks": "4.6.0",
    "postcss": "8.4.33",
    "storybook": "7.6.10",
    "typescript": "5.3.3",
    "vite": "5.0.11",
    "vitest": "1.2.0"
  },
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/carf/carf-ui.git"
  },
  "keywords": [
    "carf",
    "react",
    "components",
    "ui",
    "tailwind",
    "shadcn"
  ],
  "author": "CARF Team",
  "license": "MIT",
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Dependencias

### Producao

| Pacote | Versao | Justificativa |
|:-------|:-------|:--------------|
| class-variance-authority | 0.7.0 | Variantes de componentes (CVA) |
| clsx | 2.1.0 | Concatenacao condicional de classes |
| tailwind-merge | 2.2.0 | Merge inteligente de classes Tailwind |

### Peer Dependencies

Instaladas pelo projeto consumidor:

| Pacote | Versao | Uso |
|:-------|:-------|:----|
| @radix-ui/* | 1.x - 2.x | Primitivos acessiveis headless |
| lucide-react | 0.312.0 | Icones |
| react | 18.2.0 | Framework |
| react-dom | 18.2.0 | DOM rendering |
| tailwindcss | 3.4.1 | Styling |

### Desenvolvimento

| Pacote | Versao | Uso |
|:-------|:-------|:----|
| @storybook/* | 7.6.10 | Documentacao de componentes |
| @testing-library/* | 14.x | Testes de componentes |
| vite | 5.0.11 | Build tool |
| vitest | 1.2.0 | Test runner |
| typescript | 5.3.3 | Type checking |

## Instalacao em Projetos Consumidores

### Configurar Registry

```ini
# .npmrc
@carf:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

### Instalar

```bash
# Instalar biblioteca + peer dependencies
bun add @carf/ui

bun add @radix-ui/react-accordion @radix-ui/react-alert-dialog \
  @radix-ui/react-checkbox @radix-ui/react-dialog \
  @radix-ui/react-dropdown-menu @radix-ui/react-label \
  @radix-ui/react-popover @radix-ui/react-select \
  @radix-ui/react-separator @radix-ui/react-slot \
  @radix-ui/react-switch @radix-ui/react-tabs \
  @radix-ui/react-toast @radix-ui/react-tooltip \
  @radix-ui/react-avatar @radix-ui/react-progress \
  lucide-react
```

### Configurar Tailwind

```javascript
// tailwind.config.js
const carfConfig = require('@carf/ui/tailwind.config')

module.exports = {
  presets: [carfConfig],
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/@carf/ui/**/*.{js,ts,jsx,tsx}'
  ]
}
```

### Importar CSS

```tsx
// app.tsx ou _app.tsx
import '@carf/ui/globals.css'
```

## Estrutura de Arquivos

```
src/
├── index.ts                    # Entry point
├── components/
│   ├── ui/                     # shadcn/ui customizados
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   └── domain/                 # Componentes CARF
│       ├── unit-card.tsx
│       ├── holder-card.tsx
│       ├── status-badge.tsx
│       └── ...
├── hooks/
│   ├── use-theme.ts
│   └── use-media-query.ts
├── lib/
│   └── utils.ts                # cn() e helpers
└── styles/
    └── globals.css
```

## Versionamento

Segue Semantic Versioning (SemVer):

- **MAJOR**: Breaking changes (alterar props, remover componentes)
- **MINOR**: Novos componentes ou props backward-compatible
- **PATCH**: Bug fixes, ajustes visuais
