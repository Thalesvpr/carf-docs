# Deployment - @carf/ui

## Build e Publicação

@carf/ui é publicada como NPM package via [GitHub Packages NPM registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry) através de workflow automatizado no GitHub Actions acionado quando uma tag de versão (ex: `v0.1.0`) é criada no repositório. Build process usa Vite para compilar componentes TypeScript em ESM e CommonJS formats com `tsup` gerando arquivos `.js`, `.d.ts` e source maps, tree-shaking enabled para importações individuais, e externalizando peer dependencies (React, React-DOM, Tailwind) para evitar duplicação no bundle final das aplicações consumidoras. Package.json define `exports` field com conditional exports permitindo importação de subpaths (`@carf/ui/button`) e `main`/`module`/`types` fields para compatibilidade com diferentes bundlers (Webpack, Vite, esbuild). Versioning segue [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH) onde breaking changes em props ou remoção de componentes incrementam MAJOR, novas features incrementam MINOR, e bug fixes incrementam PATCH.

## Workflow CI/CD

```yaml
# .github/workflows/publish.yml
name: Publish Package

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run build
      - run: bun run test
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

## Publicação Manual

```bash
cd PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE
bun run build  # Gera dist/
bun test       # Valida
npm version patch  # Incrementa versão em package.json
git tag v0.1.1
git push --tags
npm publish  # Publica no GitHub Packages
```

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
