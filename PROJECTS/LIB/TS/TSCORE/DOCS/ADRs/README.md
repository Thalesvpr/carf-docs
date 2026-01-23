---
type: readme
title: "Decisoes Arquiteturais - @carf/tscore"
description: "Registro de decisoes arquiteturais para a biblioteca core TypeScript"
status: review
updated: 2026-01-21
source: "CENTRAL/ARCHITECTURE/ADRs/ADR-011-shared-library-tscore.md"
---

# Decisoes Arquiteturais - @carf/tscore

Registro de ADRs que fundamentam a biblioteca. A decisao principal (ADR-011) define a criacao de @carf/tscore como biblioteca compartilhada publicada no GitHub Packages, rejeitando alternativas como monorepo Turborepo/Nx, Git Submodules ou duplicacao de codigo. Decisoes de implementacao incluem value objects imutaveis com validacao no construtor, peer dependencies opcionais para React/Vue, subpath exports para tree-shaking e Zod como unica dependencia de runtime.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/LIB/TS/TSCORE/DOCS/ADRs/ADR-001-shared-library-tscore.md|ADR-001: Biblioteca TypeScript Compartilhada @carf/tscore]]

<!-- CARF-INDEX-END -->
