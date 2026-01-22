---
type: leaf
title: "TSConfig - @carf/tscore"
status: review
updated: 2026-01-21
source: "interno"
---

# TSConfig - @carf/tscore

Configuracao do compilador TypeScript para build e type checking.

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],

    "strict": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",

    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,

    "skipLibCheck": true,
    "resolveJsonModule": true,

    "types": ["bun-types", "node"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

## Opcoes Principais

### Target e Module

| Opcao | Valor | Justificativa |
|:------|:------|:--------------|
| `target` | ES2022 | Suporte a features modernas (top-level await, private fields) |
| `module` | ESNext | Output em ES Modules para tree-shaking |
| `moduleResolution` | bundler | Resolucao moderna compativel com Bun/Vite |

### Strict Mode

Todas as opcoes de strict mode habilitadas para maxima seguranca de tipos:

```json
{
  "strict": true,
  "strictNullChecks": true,
  "strictFunctionTypes": true,
  "strictBindCallApply": true,
  "strictPropertyInitialization": true,
  "noImplicitAny": true,
  "noImplicitReturns": true,
  "noImplicitThis": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true,
  "noFallthroughCasesInSwitch": true,
  "noUncheckedIndexedAccess": true,
  "exactOptionalPropertyTypes": true
}
```

### Declarations

| Opcao | Valor | Proposito |
|:------|:------|:----------|
| `declaration` | true | Gera arquivos .d.ts |
| `declarationMap` | true | Source maps para declaracoes |
| `sourceMap` | true | Source maps para debug |

### Paths (opcional para aliases)

Se necessario configurar aliases de importacao:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@validations/*": ["src/validations/*"],
      "@types/*": ["src/types/*"],
      "@auth/*": ["src/auth/*"]
    }
  }
}
```

## tsconfig.build.json

Configuracao especifica para build de producao:

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "declaration": true,
    "declarationDir": "./dist",
    "emitDeclarationOnly": true
  },
  "include": ["src/**/*"],
  "exclude": [
    "node_modules",
    "dist",
    "**/*.test.ts",
    "**/*.spec.ts",
    "**/__tests__/**"
  ]
}
```

## Validacao

Verificar configuracao:

```bash
# Type check sem gerar arquivos
tsc --noEmit

# Mostrar configuracao resolvida
tsc --showConfig
```
