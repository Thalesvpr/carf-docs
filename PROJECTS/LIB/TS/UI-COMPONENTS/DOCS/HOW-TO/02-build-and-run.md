# Build and Run - @carf/ui

## Build da Biblioteca

Build da biblioteca usa Vite com `bun run build` gerando arquivos em `dist/` nos formatos ESM (`dist/index.mjs`) e CommonJS (`dist/index.cjs`) com types em `dist/index.d.ts`, arquivos gerados devem ser commitados antes de publicar, rodar testes com `bun test` garantindo cobertura >80%, validar tipos com `tsc --noEmit`, e publicar no GitHub Packages com `npm version patch && git push --tags && npm publish` após autenticar com `echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" >> ~/.npmrc`.

## Comandos Disponíveis

### Build

```bash
bun run build
```

Gera:
- `dist/index.mjs` - ESM format
- `dist/index.cjs` - CommonJS format
- `dist/index.d.ts` - TypeScript declarations
- `dist/**/*.map` - Source maps

### Testes

```bash
# Rodar todos os testes
bun test

# Rodar com coverage
bun test --coverage

# Rodar em watch mode
bun test --watch

# Rodar testes específicos
bun test UnitCard
```

### Type Check

```bash
# Validar tipos sem gerar arquivos
tsc --noEmit

# Com watch mode
tsc --noEmit --watch
```

### Lint

```bash
# Verificar código
bun run lint

# Auto-fix
bun run lint:fix
```

## Publicação

### Configurar Autenticação

```bash
# Criar .npmrc com token GitHub
echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" >> ~/.npmrc
```

### Publicar Nova Versão

```bash
# 1. Build e testes
bun run build
bun test

# 2. Incrementar versão
npm version patch  # ou minor, major

# 3. Push tag
git push --follow-tags

# 4. Publicar
npm publish
```

### Versionamento Semântico

- **PATCH** (0.1.0 → 0.1.1) - Bug fixes, mudanças internas
- **MINOR** (0.1.0 → 0.2.0) - Novas features, backward-compatible
- **MAJOR** (0.1.0 → 1.0.0) - Breaking changes

## Verificação Pré-Publicação

```bash
# Checklist antes de publicar
bun run build          # ✓ Build sem erros
bun test              # ✓ Todos os testes passando
bun run lint          # ✓ Zero warnings
tsc --noEmit          # ✓ Zero erros de tipo
git status            # ✓ Working tree clean
```

## Referências

- [npm publish](https://docs.npmjs.com/cli/v10/commands/npm-publish)
- [Semantic Versioning](https://semver.org/)
- [GitHub Packages](https://docs.github.com/en/packages)
