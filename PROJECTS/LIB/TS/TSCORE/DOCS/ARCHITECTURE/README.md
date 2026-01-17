# Arquitetura @carf/tscore

Documentação arquitetural da biblioteca TypeScript compartilhada.

## Decisões Arquiteturais

- ****ADR-011**** - Decisão de criar biblioteca compartilhada vs duplicar código vs monorepo

## Estrutura de Módulos

@carf/tscore é organizado em módulos independentes com subpath exports:

```
@carf/tscore/
├── validations # Value Objects com validações
├── types # TypeScript types domain
├── auth # Cliente Keycloak base
├── auth/react # React hooks e components
└── auth/vue # Vue composables
```

## Subpath Exports

Package.json exports permitem importação modular e tree-shaking:

```json
{
 "exports": {
 ".": "./dist/index.js",
 "./validations": "./dist/validations/index.js",
 "./types": "./dist/types/index.js",
 "./auth": "./dist/auth/index.js",
 "./auth/react": "./dist/auth/react/index.js",
 "./auth/vue": "./dist/auth/vue/index.js"
 }
}
```

**Benefícios:**
- Tree-shaking elimina código não utilizado
- Imports semânticos (`@carf/tscore/validations`)
- Lazy loading de módulos opcionais (React vs Vue)

## Peer Dependencies

React e Vue são peer dependencies opcionais:

```json
{
 "peerDependencies": {
 "react": "^18.0.0",
 "vue": "^3.0.0"
 },
 "peerDependenciesMeta": {
 "react": { "optional": true },
 "vue": { "optional": true }
 }
}
```

**Benefícios:**
- GEOWEB instala apenas React, não Vue
- WEBDOCS instala apenas Vue, não React
- Evita bundle bloat desnecessário

## Build Pipeline

Build utiliza Bun + TypeScript:

```bash
# JavaScript bundle (ES modules)
bun build ./src/index.ts --outdir ./dist --target node --format esm

# TypeScript declarations (.d.ts)
tsc --emitDeclarationOnly --declaration
```

**Output:**
- `dist/*.js` - ES modules executáveis
- `dist/*.d.ts` - Type definitions para IDE autocomplete
- Sourcemaps para debugging

## Publicação GitHub Packages

CI/CD workflow automatizado:

```yaml
name: Publish

on:
 push:
 tags:
 - 'v*.*.*'

jobs:
 publish:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v3
 - uses: oven-sh/setup-bun@v1
 - run: bun install
 - run: bun test
 - run: bun run build
 - run: npm publish
 env:
 NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Integração com Projetos Consumidores

Projetos GEOWEB, REURBCAD, ADMIN, WEBDOCS consomem via NPM:

```bash
# .npmrc
@carf:registry=https://npm.pkg.github.com

# package.json
{
 "dependencies": {
 "@carf/tscore": "^0.1.0"
 }
}
```

**Range Operators:**
- `^0.1.0` - Permite MINOR e PATCH (0.1.x, 0.2.x)
- `~0.1.0` - Permite apenas PATCH (0.1.x)
- `0.1.0` - Versão exata fixada

## Desenvolvimento Local

Workflow de desenvolvimento testando changes localmente:

```bash
# No tscore
cd PROJECTS/TSCORE/SRC-CODE
npm link

# No projeto consumidor
cd PROJECTS/GEOWEB/SRC-CODE
npm link @carf/tscore
# Agora imports de @carf/tscore resolvem para código local

# Desfazer link
npm unlink @carf/tscore
bun install # Reinstala versão publicada
```

## Sincronização de Types

Types TypeScript em @carf/tscore devem estar sincronizados com C# models do backend:

**Backend (.NET):**
```csharp
public class Unit
{
 public Guid Id { get; set; }
 public string Code { get; set; }
 public UnitStatus Status { get; set; }
 public Polygon? Geometry { get; set; }
 // ...
}
```

**Frontend (TypeScript):**
```typescript
export interface Unit {
 id: string
 code: string
 status: UnitStatus
 geometry?: GeoJSON.Polygon | null
 // ...
}
```

**Processo:**
1. Backend altera model C#
2. Atualizar type correspondente em @carf/tscore
3. Publicar nova versão tscore (MINOR ou MAJOR)
4. Atualizar projetos consumidores

**Futuro:** Considerar geração automática via Typewriter ou similares.

## Testes

Suite de testes unitários centralizada:

```typescript
// CPF validation
import { describe, test, expect } from 'bun:test'
import { CPF } from '../cpf'

describe('CPF', () => {
 test('should validate valid CPF', () => {
 expect(CPF.validate('123.456.789-09')).toBe(true)
 })

 test('should reject invalid CPF', () => {
 expect(CPF.validate('123.456.789-00')).toBe(false)
 })
})
```

**Coverage mínimo:** 80% (forçado em CI)

## Performance Considerations

Value objects são instanciados frequentemente, otimizações:

- Regex compilados uma vez
- Memoization de validações caras (futuro)
- Lazy validation quando possível
- Zero dependencies para reduzir bundle size

## Segurança

- Tokens armazenados em localStorage (backend valida sempre)
- Validações client-side são UX, backend revalida
- Secrets nunca commitados (GITHUB_TOKEN via CI secrets)
- Dependências auditadas via `bun audit`

---

**Última atualização:** 2026-01-09
**Status do arquivo**: Incompleto
Descrição: Falta parágrafo denso introdutório; Falta seção GENERATED com índice automático; Muitas listas com bullets (21) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.
