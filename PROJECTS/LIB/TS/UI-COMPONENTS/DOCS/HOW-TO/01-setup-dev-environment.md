# Setup Dev Environment - @carf/ui

## Requisitos

Setup do ambiente de desenvolvimento requer Node.js 18+ ou Bun 1.0+, clonar repositório `git clone https://github.com/user/carf-ui.git PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE`, instalar dependências com `bun install`, rodar Storybook com `bun run storybook` abrindo `http://localhost:6006` para ver todos os componentes com seus estados e variantes, configurar VS Code com extensões ESLint, Prettier, Tailwind CSS IntelliSense, e criar componentes novos copiando template de `src/components/_template/` seguindo padrão de estrutura (index.ts exports, component.tsx implementação, component.stories.tsx Storybook, component.test.tsx testes).

## Passo a Passo

### 1. Instalar Node.js/Bun

```bash
# Instalar Bun (recomendado)
curl -fsSL https://bun.sh/install | bash

# OU instalar Node.js 18+
# https://nodejs.org/
```

### 2. Clonar Repositório

```bash
git clone https://github.com/user/carf-ui.git PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE
cd PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE
```

### 3. Instalar Dependências

```bash
bun install
```

### 4. Rodar Storybook

```bash
bun run storybook
```

Abre automaticamente em `http://localhost:6006` com hot reload.

### 5. Configurar VS Code

Instale as seguintes extensões:

- **ESLint** (dbaeumer.vscode-eslint)
- **Prettier** (esbenp.prettier-vscode)
- **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)
- **TypeScript and JavaScript Language Features** (built-in)

`.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ]
}
```

### 6. Criar Novo Componente

```bash
# Copiar template
cp -r src/components/_template src/components/MyComponent

# Editar arquivos
# - index.ts (exports)
# - MyComponent.tsx (implementação)
# - MyComponent.stories.tsx (Storybook)
# - MyComponent.test.tsx (testes)
```

## Estrutura de Arquivos

```
src/
├── components/
│   ├── _template/         # Template para novos componentes
│   ├── ui/               # Componentes shadcn/ui
│   │   ├── button/
│   │   ├── input/
│   │   └── dialog/
│   └── domain/           # Componentes CARF
│       ├── unit-card/
│       ├── holder-card/
│       └── map-view/
├── lib/                  # Utilities
├── hooks/                # Custom hooks
└── index.ts             # Exports principais
```

## Referências

- [Bun](https://bun.sh/)
- [Storybook](https://storybook.js.org/)
- [VS Code Extensions](https://code.visualstudio.com/docs/editor/extension-marketplace)
