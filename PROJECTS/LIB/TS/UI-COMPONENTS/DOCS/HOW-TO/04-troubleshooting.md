# Troubleshooting - @carf/ui

## Problemas Comuns

### 1. Tailwind Classes Não Aplicadas

**Sintoma:** Componentes renderizam mas sem estilos Tailwind.

**Causa:** `tailwind.config.ts` do app consumidor não inclui arquivos da lib no `content`.

**Solução:**

```typescript
// tailwind.config.ts (GEOWEB/ADMIN)
export default {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./node_modules/@carf/ui/**/*.{ts,tsx}"  // ← ADICIONAR ESTA LINHA
  ]
}
```

Depois rebuild:

```bash
bun run build
```

### 2. Types Não Encontrados

**Sintoma:** `Cannot find module '@carf/ui' or its corresponding type declarations`

**Causa:** `.d.ts` files não foram gerados no build da lib.

**Solução:**

```bash
# Na lib @carf/ui
cd PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE
bun run build  # Gera dist/index.d.ts

# Verificar que package.json tem:
{
  "types": "./dist/index.d.ts"
}
```

No app consumidor:

```bash
# Limpar node_modules e reinstalar
rm -rf node_modules bun.lockb
bun install
```

### 3. Componentes Não Renderizam

**Sintoma:** Componente importado mas não aparece na tela.

**Causa:** Peer dependencies (React 18) não instaladas no app consumidor.

**Solução:**

```bash
# Verificar versão do React
bun list react

# Deve ser React 18.x
# Se não for, atualizar:
bun add react@^18.0.0 react-dom@^18.0.0
```

### 4. Storybook Não Abre

**Sintoma:** `bun run storybook` falha ou trava.

**Causa:** Cache corrompido do Storybook.

**Solução:**

```bash
# Limpar cache
rm -rf node_modules/.cache/storybook

# Reinstalar e rodar
bun install
bun run storybook
```

Se ainda falhar:

```bash
# Deletar node_modules completamente
rm -rf node_modules bun.lockb
bun install
bun run storybook
```

### 5. Erros de Importação Circular

**Sintoma:** `Maximum call stack size exceeded` ou warnings de import cycle.

**Causa:** Importar `index.ts` dentro de componentes.

**Solução:**

```typescript
// ❌ EVITAR - Importação circular
// src/components/ui/button/Button.tsx
import { Card } from '../../index'  // ERRADO

// ✅ CORRETO - Importar diretamente do arquivo
import { Card } from '../card/Card'
```

### 6. Build Falhando

**Sintoma:** `bun run build` retorna erros.

**Causas e Soluções:**

#### Path inválido em import

```bash
Error: Cannot find module './NonExistent'
```

**Solução:** Verificar todos os imports, corrigir paths.

#### Erro de tipo TypeScript

```bash
Type 'string' is not assignable to type 'number'
```

**Solução:** Rodar `tsc --noEmit` para ver todos os erros, corrigir tipos.

#### Conflito de dependências

```bash
Conflicting peer dependency: react@17.0.0
```

**Solução:**

```bash
# Verificar package.json
{
  "peerDependencies": {
    "react": "^18.0.0"  // Deve ser 18.x
  }
}

# Reinstalar
rm -rf node_modules bun.lockb
bun install
```

### 7. Testes Falhando

**Sintoma:** `bun test` retorna erros.

**Causas e Soluções:**

#### jsdom não configurado

```bash
ReferenceError: document is not defined
```

**Solução:**

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'jsdom'  // ← ADICIONAR
  }
})
```

#### Testing Library setup faltando

```bash
expect(...).toBeInTheDocument is not a function
```

**Solução:**

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom'

// vitest.config.ts
export default defineConfig({
  test: {
    setupFiles: ['./src/test/setup.ts']
  }
})
```

### 8. CSS Variables Não Funcionam

**Sintoma:** Cores customizadas não aparecem.

**Causa:** CSS variables não definidas em `globals.css` do app consumidor.

**Solução:**

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --primary: 220 90% 56%;    /* ← ADICIONAR ISTO */
    --radius: 0.5rem;
    /* ... outras variables */
  }
}
```

### 9. Hot Reload Não Funciona

**Sintoma:** Mudanças em componentes não aparecem no Storybook.

**Solução:**

```bash
# Parar Storybook (Ctrl+C)
# Limpar cache
rm -rf node_modules/.cache

# Reiniciar
bun run storybook
```

Se ainda não funcionar, salvar arquivo novamente (Ctrl+S) força rebuild.

### 10. Publicação NPM Falhando

**Sintoma:** `npm publish` retorna 401 Unauthorized.

**Causa:** Token GitHub não configurado.

**Solução:**

```bash
# Criar token em: https://github.com/settings/tokens
# Com scopes: write:packages, read:packages

# Adicionar ao .npmrc
echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" >> ~/.npmrc

# Tentar publicar novamente
npm publish
```

## Checklist de Debug

Quando encontrar um problema:

1. ✅ Verificar versão do Node/Bun (`node -v`, `bun -v`)
2. ✅ Limpar node_modules (`rm -rf node_modules bun.lockb && bun install`)
3. ✅ Verificar peer dependencies (`bun list react`)
4. ✅ Rodar type check (`tsc --noEmit`)
5. ✅ Verificar console do navegador (F12)
6. ✅ Verificar logs do terminal
7. ✅ Pesquisar erro no GitHub Issues da lib
8. ✅ Se nada funcionar, abrir issue com reprodução mínima

## Obter Ajuda

- **GitHub Issues:** https://github.com/user/carf-ui/issues
- **Documentação:** `PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/`
- **Storybook:** http://localhost:6006 (exemplos interativos)

## Referências

- [Tailwind CSS Troubleshooting](https://tailwindcss.com/docs/installation#troubleshooting)
- [Vite Troubleshooting](https://vitejs.dev/guide/troubleshooting)
- [Storybook Troubleshooting](https://storybook.js.org/docs/react/configure/troubleshooting)

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (6) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.
