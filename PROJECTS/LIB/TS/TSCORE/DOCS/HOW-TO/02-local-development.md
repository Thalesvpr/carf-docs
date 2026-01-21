---
title: "Desenvolvimento Local - @carf/tscore"
status: review
updated: 2026-01-21
source: "interno"
---

# Desenvolvimento Local - @carf/tscore

Guia para desenvolver e testar alteracoes na biblioteca localmente.

## Setup Inicial

### Clonar e Instalar

```bash
# Clonar repositorio
git clone https://github.com/carf/carf-tscore.git
cd carf-tscore

# Instalar dependencias
bun install
```

### Estrutura do Projeto

```
carf-tscore/
├── src/
│   ├── index.ts              # Entry point principal
│   ├── validations/          # Value Objects
│   │   ├── index.ts
│   │   ├── cpf.ts
│   │   ├── cnpj.ts
│   │   ├── email.ts
│   │   └── phone.ts
│   ├── types/                # TypeScript types
│   │   ├── index.ts
│   │   ├── entities/
│   │   ├── enums/
│   │   └── dtos/
│   └── auth/                 # Autenticacao
│       ├── index.ts
│       ├── keycloak-client.ts
│       ├── react/
│       └── vue/
├── __tests__/                # Testes
├── dist/                     # Output do build
├── package.json
├── tsconfig.json
└── bun.lockb
```

## Comandos de Desenvolvimento

### Build

```bash
# Build completo
bun run build

# Build com watch mode (para desenvolvimento)
bun run build --watch
```

### Testes

```bash
# Rodar todos os testes
bun test

# Rodar testes com watch mode
bun test --watch

# Rodar testes com coverage
bun test --coverage

# Rodar teste especifico
bun test cpf
bun test --grep "should validate"
```

### Type Check

```bash
# Verificar tipos sem gerar output
bun run type-check

# Watch mode
tsc --noEmit --watch
```

### Lint

```bash
# Verificar codigo
bun run lint

# Auto-fix
bun run lint:fix
```

## Testando Localmente em Projeto Consumidor

### Usando npm link

O `npm link` cria um symlink da biblioteca local para uso em outros projetos.

**No diretorio da biblioteca:**

```bash
cd PROJECTS/LIB/TS/TSCORE/SRC-CODE/carf-tscore

# Criar link global
npm link
```

**No projeto consumidor (GEOWEB, ADMIN, etc):**

```bash
cd PROJECTS/GEOWEB/SRC-CODE

# Usar link local
npm link @carf/tscore

# Agora imports de @carf/tscore usam codigo local
```

**Para desfazer:**

```bash
# No projeto consumidor
npm unlink @carf/tscore
bun install  # Reinstala versao do registry
```

### Usando file: protocol

Alternativa ao npm link:

```json
// package.json do projeto consumidor
{
  "dependencies": {
    "@carf/tscore": "file:../../../LIB/TS/TSCORE/SRC-CODE/carf-tscore"
  }
}
```

Depois rodar:

```bash
bun install
```

## Workflow de Desenvolvimento

### 1. Criar Branch

```bash
git checkout -b feature/add-cep-validation
```

### 2. Implementar Alteracao

```typescript
// src/validations/cep.ts
export class CEP {
  private readonly value: string

  constructor(cep: string) {
    const normalized = CEP.normalize(cep)
    if (!CEP.validate(normalized)) {
      throw new ValidationError('CEP inválido')
    }
    this.value = normalized
  }

  static validate(cep: string): boolean {
    const normalized = this.normalize(cep)
    return /^\d{8}$/.test(normalized)
  }

  static normalize(cep: string): string {
    return cep.replace(/\D/g, '')
  }

  format(): string {
    return `${this.value.slice(0, 5)}-${this.value.slice(5)}`
  }

  toString(): string {
    return this.value
  }
}
```

### 3. Adicionar Testes

```typescript
// __tests__/validations/cep.test.ts
import { describe, test, expect } from 'bun:test'
import { CEP } from '../../src/validations/cep'

describe('CEP', () => {
  test('should validate valid CEP', () => {
    expect(CEP.validate('01310-100')).toBe(true)
    expect(CEP.validate('01310100')).toBe(true)
  })

  test('should reject invalid CEP', () => {
    expect(CEP.validate('123')).toBe(false)
    expect(CEP.validate('1234567890')).toBe(false)
  })

  test('should format CEP', () => {
    const cep = new CEP('01310100')
    expect(cep.format()).toBe('01310-100')
  })
})
```

### 4. Exportar

```typescript
// src/validations/index.ts
export { CPF } from './cpf'
export { CNPJ } from './cnpj'
export { Email } from './email'
export { Phone } from './phone'
export { CEP } from './cep'  // Adicionar
```

### 5. Verificar

```bash
# Rodar todos os checks
bun test
bun run lint
bun run type-check
bun run build
```

### 6. Testar em Projeto Real

```bash
# Link local
cd PROJECTS/GEOWEB/SRC-CODE
npm link @carf/tscore

# Testar no GEOWEB
bun run dev
```

### 7. Commit e PR

```bash
git add .
git commit -m "feat(validations): add CEP value object"
git push origin feature/add-cep-validation
```

## Debug

### VS Code

Configurar `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "bun",
      "request": "launch",
      "name": "Debug Tests",
      "program": "${workspaceFolder}/node_modules/bun/bin/bun",
      "args": ["test"],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### Console Logs

Para debug rapido em testes:

```typescript
test('debug example', () => {
  const cpf = new CPF('123.456.789-09')
  console.log('CPF value:', cpf.toString())
  console.log('CPF formatted:', cpf.format())
})
```

## Troubleshooting

### "Module not found" apos npm link

Verificar que o build foi executado:

```bash
cd carf-tscore
bun run build
ls dist/  # Deve existir arquivos
```

### Tipos nao atualizando no projeto consumidor

Reiniciar TypeScript server no VS Code:

1. `Ctrl+Shift+P`
2. "TypeScript: Restart TS Server"

### Conflitos de versao de React/Vue

Usar `npm link` tambem para React:

```bash
# No projeto consumidor
cd node_modules/react
npm link

# No carf-tscore
npm link react
```
