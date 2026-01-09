# 011 - Complete TypeScript Libraries Documentation

🔴 **Prioridade:** Crítica
📅 **Criado em:** 2026-01-09
⏱️ **Estimativa:** 3 dias (1 dia por lib)

## Descrição

As 3 bibliotecas TypeScript (TSCORE, GEOAPI-CLIENT, UI-COMPONENTS) têm docs incompletas. Como são dependências de TODOS os outros projetos, precisam de documentação exemplar com guias práticos de uso.

---

## TSCORE

**Status:** 31% (5/16 arquivos)

### Arquivos Faltando (11)
- [ ] DOCS/ARCHITECTURE/03-data-flow.md
- [ ] DOCS/ARCHITECTURE/04-integration.md
- [ ] DOCS/ARCHITECTURE/05-deployment.md
- [ ] DOCS/CONCEPTS/02-terminology.md
- [ ] DOCS/CONCEPTS/03-design-principles.md
- [ ] DOCS/HOW-TO/README.md
- [ ] DOCS/HOW-TO/01-setup-dev-environment.md
- [ ] DOCS/HOW-TO/02-build-and-run.md
- [ ] DOCS/HOW-TO/03-testing.md
- [ ] DOCS/HOW-TO/04-troubleshooting.md
- [ ] DOCS/API/validations.md (adicional)

### Conteúdo Crítico
- Como usar KeycloakClient no React
- Como usar KeycloakClient no Vue
- Como usar validações (CPF, CNPJ, Email, Phone)
- Como importar types
- Exemplos de código práticos

---

## GEOAPI-CLIENT

**Status:** 12% (2/16 arquivos)

### Arquivos Faltando (14)
- [ ] DOCS/ARCHITECTURE/README.md
- [ ] DOCS/ARCHITECTURE/03-data-flow.md (request → response flow)
- [ ] DOCS/ARCHITECTURE/04-integration.md (GEOAPI, Keycloak)
- [ ] DOCS/ARCHITECTURE/05-deployment.md (publish to GitHub Packages)
- [ ] DOCS/CONCEPTS/README.md
- [ ] DOCS/CONCEPTS/01-key-concepts.md (HTTP Client, Interceptors)
- [ ] DOCS/CONCEPTS/02-terminology.md
- [ ] DOCS/CONCEPTS/03-design-principles.md
- [ ] DOCS/HOW-TO/README.md
- [ ] DOCS/HOW-TO/01-setup-dev-environment.md
- [ ] DOCS/HOW-TO/02-build-and-run.md
- [ ] DOCS/HOW-TO/03-testing.md (mock API responses)
- [ ] DOCS/HOW-TO/04-troubleshooting.md
- [ ] DOCS/API/ (API reference para cada endpoint)

### Conteúdo Crítico
- Como instalar e configurar
- Como fazer auth com Keycloak
- Como usar cada endpoint (Units, Holders, etc)
- Como tratar erros
- Como fazer retry
- Exemplos de código

---

## UI-COMPONENTS

**Status:** 0% (0/16 arquivos)

### Arquivos Faltando (16 - TODOS)
- [ ] DOCS/README.md
- [ ] DOCS/ARCHITECTURE/README.md
- [ ] DOCS/ARCHITECTURE/01-overview.md (Shadcn/ui + Radix)
- [ ] DOCS/ARCHITECTURE/03-data-flow.md
- [ ] DOCS/ARCHITECTURE/04-integration.md (React, Tailwind)
- [ ] DOCS/ARCHITECTURE/05-deployment.md (publish, Storybook)
- [ ] DOCS/CONCEPTS/README.md
- [ ] DOCS/CONCEPTS/01-key-concepts.md (variants, themes, composition)
- [ ] DOCS/CONCEPTS/02-terminology.md
- [ ] DOCS/CONCEPTS/03-design-principles.md (accessibility, composition)
- [ ] DOCS/HOW-TO/README.md
- [ ] DOCS/HOW-TO/01-setup-dev-environment.md
- [ ] DOCS/HOW-TO/02-build-and-run.md (Storybook)
- [ ] DOCS/HOW-TO/03-testing.md (a11y tests)
- [ ] DOCS/HOW-TO/04-troubleshooting.md
- [ ] DOCS/COMPONENTS/ (docs de cada componente)

### Conteúdo Crítico
- Como instalar
- Como configurar Tailwind
- Como usar ThemeProvider
- Como usar cada componente (Button, Card, Input, etc)
- Como customizar variants
- Como usar dark mode
- Guia de acessibilidade
- Exemplos de código

---

## Prioridade de Execução

1. **TSCORE** (mais urgente - já usado)
2. **GEOAPI-CLIENT** (dependência de frontends)
3. **UI-COMPONENTS** (dependência de frontends)

## Localização

- `PROJECTS/LIB/TS/TSCORE/DOCS/`
- `PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/`
- `PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/`

## Referências do Template

Ver: `CENTRAL/TEMPLATES/PROJECT-DOCS-TEMPLATE.md`
