# Bibliotecas TypeScript Compartilhadas

## Visão Geral

O projeto CARF possui 3 bibliotecas TypeScript compartilhadas publicadas como npm packages no GitHub Packages. Estas bibliotecas eliminam duplicação de código entre os frontends (GEOWEB, REURBCAD, ADMIN, WEBDOCS).

## Bibliotecas

### @carf/tscore

**Biblioteca core** com validações, types e autenticação.

**Conteúdo:**
- ✅ Value Objects (CPF, CNPJ, Email, PhoneNumber)
- ✅ TypeScript Types sincronizados com backend .NET
- ✅ Hooks React de autenticação
- ✅ Composables Vue 3
- ✅ Cliente Keycloak OAuth2/OIDC

**Instalação:** Executar comando bun add @carf/tscore no projeto consumidor.

**Documentação:** PROJECTS/LIB/TS/TSCORE/DOCS/

---

### @carf/geoapi-client

**Cliente HTTP** type-safe para comunicação com GEOAPI backend.

**Conteúdo:**
- ✅ SDK completo para todos os endpoints REST
- ✅ Autenticação automática (JWT tokens)
- ✅ Tratamento de erros tipados
- ✅ Retry logic e circuit breaker
- ✅ Suporte a offline caching
- ✅ Upload/download de arquivos

**Instalação:** Executar comando bun add @carf/geoapi-client @carf/tscore instalando ambas bibliotecas como dependencies.

**Documentação:** PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/

---

### **@carf/ui**

**Componentes React** reutilizáveis com shadcn/ui + Tailwind CSS.

**Conteúdo:**
- ✅ Componentes shadcn/ui customizados
- ✅ Componentes específicos CARF (UnitCard, HolderCard, MapView)
- ✅ Dark mode support
- ✅ Acessibilidade WCAG 2.1 AA
- ✅ Storybook documentation

**Instalação:** Executar comando bun add @carf/ui @carf/tscore instalando biblioteca de componentes UI com dependência tscore.

**Documentação:** PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/

---

## Arquitetura

Arquitetura em camadas onde aplicações frontend GEOWEB REURBCAD ADMIN e WEBDOCS consomem três bibliotecas TypeScript compartilhadas organizadas hierarquicamente sendo @carf/ui camada superior contendo componentes React com shadcn/ui dependendo de @carf/geoapi-client camada intermediária provendo SDK HTTP type-safe para comunicação com backend GEOAPI que por sua vez depende de @carf/tscore camada base contendo types validations e auth hooks compartilhados, eliminando duplicação de código e garantindo consistência entre frontends, todas bibliotecas eventualmente comunicando com GEOAPI backend .NET 9 expondo REST API conectado a PostgreSQL com PostGIS para dados espaciais e Keycloak para autenticação OAuth2.

## Estratégia de Versionamento

Todas as libs seguem **Semantic Versioning**:

- **MAJOR** (x.0.0) - Breaking changes
- **MINOR** (0.x.0) - Novas features backward-compatible
- **PATCH** (0.0.x) - Bug fixes

## Publicação

Packages são publicados no GitHub Packages configurando arquivo .npmrc com registry @carf apontando para https://npm.pkg.github.com e authToken usando variável GITHUB_TOKEN para autenticação, processo de publicação requer permissões adequadas executando build via bun run build no diretório da biblioteca seguido por npm publish que envia package para GitHub Packages registry.

## Desenvolvimento Local

Desenvolvimento local de bibliotecas permite testar mudanças antes de publicar executando bun link no diretório da biblioteca criando symlink global seguido por bun link @carf/nome-biblioteca no projeto consumidor linkando para versão local, alterações na biblioteca requerem rebuild via bun run build após edições sendo automaticamente refletidas no projeto consumidor linkado sem necessidade de republicar package permitindo iteração rápida e validação de mudanças antes de commit.

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
- [UI-COMPONENTS Docs](../../PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/README.md)

### CENTRAL - Conceitos de Domínio
- [Domain Model](../DOMAIN-MODEL/00-INDEX.md) - Entidades e Value Objects
- [API Specification](../API/README.md) - Endpoints REST
- [Keycloak Integration](../INTEGRATION/KEYCLOAK/README.md) - Autenticação OAuth2

### Projetos Consumidores
- **GEOWEB** - Frontend web React (documentação em desenvolvimento)
- **REURBCAD** - Mobile React Native (documentação em desenvolvimento)
- ADMIN - Console admin React
- WEBDOCS - Portal VitePress

---

**Última atualização:** 2026-01-10
