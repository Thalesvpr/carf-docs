---
type: readme
status: review
updated: 2026-02-08
---

# TESTING - REURBCAD

Estrategia e padroes de testes para o aplicativo mobile REURBCAD React Native Expo. Cobre testes unitarios (Jest), testes de componentes (React Native Testing Library) e testes end-to-end (Maestro).

## Piramide de Testes

- **Unitarios (60%)** - Stores Zustand, schemas Zod, modelos WatermelonDB, utils
- **Integracao (25%)** - Componentes com providers, formularios, navegacao
- **E2E (15%)** - Fluxos completos: login, coleta, sync, offline

## Documentos

- **[00-testing-strategy.md](./00-testing-strategy.md)** - Estrategia geral de testes, piramide, ferramentas, metas de cobertura, CI
- **[01-unit-tests.md](./01-unit-tests.md)** - Testes unitarios: stores Zustand, WatermelonDB, Zod schemas, utils, React Hook Form
- **[02-component-tests.md](./02-component-tests.md)** - Testes de componentes: RNTL, providers, interacoes, formularios, mocks Expo
- **[03-e2e-tests.md](./03-e2e-tests.md)** - Testes E2E: Maestro setup, fluxos criticos, simulacao offline, CI

<!-- CARF-INDEX-START -->
## Indice

### Em Revisao

- ○ [[PROJECTS/REURBCAD/DOCS/TESTING/00-testing-strategy.md|00-testing-strategy - Estrategia de Testes]]
- ○ [[PROJECTS/REURBCAD/DOCS/TESTING/01-unit-tests.md|01-unit-tests - Testes Unitarios]]
- ○ [[PROJECTS/REURBCAD/DOCS/TESTING/02-component-tests.md|02-component-tests - Testes de Componentes]]
- ○ [[PROJECTS/REURBCAD/DOCS/TESTING/03-e2e-tests.md|03-e2e-tests - Testes End-to-End]]

<!-- CARF-INDEX-END -->
