# How-To - @carf/ui

## Guias Práticos

- [01-setup-dev-environment.md](./01-setup-dev-environment.md) - Setup do ambiente de desenvolvimento
- [02-build-and-run.md](./02-build-and-run.md) - Build e publicação da biblioteca
- [02-customization.md](./02-customization.md) - Customizar tema via CSS variables
- [03-testing.md](./03-testing.md) - Escrever testes de componentes
- [04-troubleshooting.md](./04-troubleshooting.md) - Resolver problemas comuns

## Guias Rápidos

### Instalar a biblioteca

```bash
bun add @carf/ui @carf/tscore
```

### Rodar Storybook

```bash
cd PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE
bun install
bun run storybook
```

### Publicar nova versão

```bash
bun run build
bun test
npm version patch
git push --tags
npm publish
```
