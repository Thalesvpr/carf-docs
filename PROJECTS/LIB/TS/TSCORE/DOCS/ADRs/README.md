---
title: "Decisoes Arquiteturais - @carf/tscore"
description: "Registro de decisoes arquiteturais para a biblioteca core TypeScript"
status: review
updated: 2026-01-20
source: "CENTRAL/ARCHITECTURE/ADRs/ADR-011-shared-library-tscore.md"
---

# Decisoes Arquiteturais - @carf/tscore

Registro de decisoes arquiteturais (ADRs) que fundamentam a biblioteca.

## ADR Principal

A decisao de criar @carf/tscore como biblioteca compartilhada esta documentada em:

**ADR-011: Shared Library tscore**
- Localizacao: `CENTRAL/ARCHITECTURE/ADRs/ADR-011-shared-library-tscore.md`

### Resumo da Decisao

**Contexto:** GEOWEB, REURBCAD, ADMIN e WEBDOCS precisam compartilhar validacoes (CPF, CNPJ), tipos TypeScript e autenticacao Keycloak.

**Decisao:** Criar biblioteca `@carf/tscore` publicada no GitHub Packages.

**Alternativas Consideradas:**
1. Monorepo com Turborepo/Nx - Rejeitado por complexidade de CI/CD
2. Git Submodules - Rejeitado por dificuldade de versionamento
3. Duplicacao de codigo - Rejeitado por risco de divergencia

**Consequencias:**
- (+) Codigo centralizado com versao unica
- (+) Publicacao automatizada via GitHub Actions
- (+) Peer dependencies opcionais para React/Vue
- (-) Requer sincronizacao de versoes entre projetos
- (-) Processo de release adicional

## Decisoes de Implementacao

### Value Objects Imutaveis

**Decisao:** Value Objects (CPF, CNPJ, Email, Phone) sao classes imutaveis com validacao no construtor.

**Justificativa:** Garante que instancias sempre contem valores validos, evitando verificacoes repetidas.

### Peer Dependencies Opcionais

**Decisao:** React e Vue sao peer dependencies opcionais.

**Justificativa:** Permite que GEOWEB (React) e WEBDOCS (Vue) consumam a biblioteca sem carregar framework nao utilizado.

### Subpath Exports

**Decisao:** Usar exports map do package.json para subpaths.

**Justificativa:** Habilita tree-shaking e importacoes semanticas (`@carf/tscore/validations`).

### Zod para Schemas

**Decisao:** Usar Zod como unica dependencia de runtime para validacao de schemas.

**Justificativa:** TypeScript-first, inferencia de tipos automatica, bundle size pequeno (~12KB).

## Referencias CENTRAL

- CENTRAL/ARCHITECTURE/ADRs/ADR-011-shared-library-tscore.md - ADR-011 Completo
- CENTRAL/VERSIONING/03-semantic-versioning.md - Versionamento Semantico

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
