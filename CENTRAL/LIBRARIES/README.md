# Bibliotecas TypeScript Compartilhadas

## Visão Geral

O projeto CARF possui 3 bibliotecas TypeScript compartilhadas publicadas como npm packages no GitHub Packages. Estas bibliotecas eliminam duplicação de código entre os frontends (GEOWEB, REURBCAD, ADMIN, WEBDOCS).

## Bibliotecas

### [@carf/tscore](../../PROJECTS/LIB/TS/TSCORE/DOCS/README.md)

**Biblioteca core** com validações, types e autenticação.

**Conteúdo:**
- ✅ Value Objects (CPF, CNPJ, Email, PhoneNumber)
- ✅ TypeScript Types sincronizados com backend .NET
- ✅ Hooks React de autenticação
- ✅ Composables Vue 3
- ✅ Cliente Keycloak OAuth2/OIDC

**Instalação:**
```bash
bun add @carf/tscore
```

**Documentação:** [PROJECTS/LIB/TS/TSCORE/DOCS/](../../PROJECTS/LIB/TS/TSCORE/DOCS/README.md)

---

### [@carf/geoapi-client](../../PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/README.md)

**Cliente HTTP** type-safe para comunicação com GEOAPI backend.

**Conteúdo:**
- ✅ SDK completo para todos os endpoints REST
- ✅ Autenticação automática (JWT tokens)
- ✅ Tratamento de erros tipados
- ✅ Retry logic e circuit breaker
- ✅ Suporte a offline caching
- ✅ Upload/download de arquivos

**Instalação:**
```bash
bun add @carf/geoapi-client @carf/tscore
```

**Documentação:** [PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/](../../PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/README.md)

---

### **@carf/ui**

**Componentes React** reutilizáveis com shadcn/ui + Tailwind CSS.

**Conteúdo:**
- ✅ Componentes shadcn/ui customizados
- ✅ Componentes específicos CARF (UnitCard, HolderCard, MapView)
- ✅ Dark mode support
- ✅ Acessibilidade WCAG 2.1 AA
- ✅ Storybook documentation

**Instalação:**
```bash
bun add @carf/ui @carf/tscore
```

**Documentação:** **PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/**

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Aplicações Frontend                       │
│  ┌─────────┐  ┌──────────┐  ┌───────┐  ┌──────────┐       │
│  │ GEOWEB  │  │ REURBCAD │  │ ADMIN │  │ WEBDOCS  │       │
│  └────┬────┘  └─────┬────┘  └───┬───┘  └─────┬────┘       │
└───────┼────────────┼────────────┼─────────────┼────────────┘
        │            │            │             │
        └────────────┴────────────┴─────────────┘
                     │
        ┌────────────┴───────────────────────────────┐
        │    Bibliotecas TypeScript Compartilhadas   │
        │  ┌─────────────────────────────────────┐   │
        │  │         @carf/ui                    │   │
        │  │  (Componentes React + shadcn/ui)    │   │
        │  └───────────────┬─────────────────────┘   │
        │                  │                          │
        │  ┌───────────────▼─────────────────────┐   │
        │  │      @carf/geoapi-client            │   │
        │  │   (SDK HTTP para GEOAPI backend)    │   │
        │  └───────────────┬─────────────────────┘   │
        │                  │                          │
        │  ┌───────────────▼─────────────────────┐   │
        │  │         @carf/tscore                │   │
        │  │ (Types, Validations, Auth hooks)    │   │
        │  └─────────────────────────────────────┘   │
        └────────────────┬───────────────────────────┘
                         │
        ┌────────────────▼───────────────┐
        │    GEOAPI Backend (.NET 9)     │
        │  - REST API                    │
        │  - PostgreSQL + PostGIS        │
        │  - Keycloak OAuth2             │
        └────────────────────────────────┘
```

## Estratégia de Versionamento

Todas as libs seguem **Semantic Versioning**:

- **MAJOR** (x.0.0) - Breaking changes
- **MINOR** (0.x.0) - Novas features backward-compatible
- **PATCH** (0.0.x) - Bug fixes

## Publicação

Packages são publicados no **GitHub Packages**:

```bash
# Configurar .npmrc
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc
echo "//npm.pkg.github.com/:_authToken=\${GITHUB_TOKEN}" >> .npmrc

# Publicar (requer permissões)
cd PROJECTS/LIB/TS/TSCORE/SRC-CODE
bun run build
npm publish
```

## Desenvolvimento Local

Para desenvolver nas libs localmente e testar em outro projeto:

```bash
# Na lib (ex: tscore)
cd PROJECTS/LIB/TS/TSCORE/SRC-CODE
bun link

# No projeto consumidor (ex: geoweb)
cd PROJECTS/GEOWEB/SRC-CODE
bun link @carf/tscore

# Fazer alterações na lib
cd PROJECTS/LIB/TS/TSCORE/SRC-CODE
# ... editar código ...
bun run build  # Rebuild após mudanças

# Projeto consumidor usa versão local automaticamente
```

## Relacionamento com CENTRAL/

As bibliotecas implementam conceitos documentados em CENTRAL/:

| Biblioteca | Implementa Conceitos de | Documentação CENTRAL |
|------------|-------------------------|----------------------|
| @carf/tscore | Value Objects, Types, Auth | [DOMAIN-MODEL/](../DOMAIN-MODEL/00-INDEX.md) |
| @carf/geoapi-client | REST API Endpoints | [API/](../API/README.md) |
| @carf/ui | Design System, Components | *(standalone)* |

## Links Úteis

### Documentação das Bibliotecas
- [TSCORE Docs](../../PROJECTS/LIB/TS/TSCORE/DOCS/README.md)
- [GEOAPI-CLIENT Docs](../../PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/README.md)
- **UI Docs**

### CENTRAL - Conceitos de Domínio
- [Domain Model](../DOMAIN-MODEL/00-INDEX.md) - Entidades e Value Objects
- [API Specification](../API/README.md) - Endpoints REST
- [Keycloak Integration](../INTEGRATION/KEYCLOAK/README.md) - Autenticação OAuth2

### Projetos Consumidores
- **GEOWEB** - Frontend web React
- **REURBCAD** - Mobile React Native
- **ADMIN** - Console admin React
- [WEBDOCS](../../PROJECTS/WEBDOCS/DOCS/README.md) - Portal VitePress

---

**Última atualização:** 2026-01-10
